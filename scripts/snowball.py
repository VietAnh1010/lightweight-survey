"""Expand the library along the citation graph.

Keyword search alone reliably misses foundational work — nobody phrases their
seminal paper the way you phrase your query. Snowballing fixes that:

  backward  the references of papers we already accepted, from Crossref
  forward   the papers that cite papers we already accepted, from OpenCitations

Both directions are gated on the topic vocabulary and the year floor, so a run
converges instead of swallowing all of computer science.

    python3 scripts/snowball.py --seed-status included
    python3 scripts/snowball.py --direction forward --max-forward 80

Both sources are DOI-keyed, so a seed without one — normally an arXiv-only
preprint — cannot be expanded. The run reports how many it skipped; that
number belongs in STATUS.md.
"""

from __future__ import annotations

import argparse

import crossref
import opencitations
import search_arxiv
from common import Store, log, log_event
from topic import in_topic


def known_ids(store: Store) -> tuple[set[str], set[str]]:
    """DOIs and arXiv ids already in the library, to skip before fetching."""
    dois = {r["doi"] for r in store.records.values() if r.get("doi")}
    arxiv = {r["arxiv_id"] for r in store.records.values() if r.get("arxiv_id")}
    return dois, arxiv


def absorb(store: Store, records: list[dict], from_year: int,
           topic_gate: bool) -> tuple[int, int]:
    """Filter fetched records on year and topic, then merge. Returns (new, skipped)."""
    new = skipped = 0
    for rec in records:
        if rec.get("year") and rec["year"] < from_year:
            skipped += 1
            continue
        if topic_gate and not in_topic(rec):
            skipped += 1
            continue
        rec["snowball_depth"] = 1
        _, is_new = store.upsert(rec)
        new += is_new
    return new, skipped


def backward(store: Store, seeds: list[dict], from_year: int, topic_gate: bool) -> int:
    """Pull the reference lists of the seeds, one Crossref request per seed."""
    known_dois, _ = known_ids(store)
    wanted: dict[str, str] = {}  # reference doi -> citekey of the seed citing it
    seeds_with_doi = unresolvable = 0

    for seed in seeds:
        if not seed.get("doi"):
            continue
        seeds_with_doi += 1
        label = seed.get("citekey") or seed["id"]
        try:
            refs, unstructured = crossref.reference_dois(seed["doi"])
        except Exception as exc:  # noqa: BLE001 - a seed without deposited refs is routine
            log(f"backward: no reference list for {label}: {exc}")
            log_event("snowball_failed", direction="backward", seed=label, error=str(exc))
            continue
        unresolvable += unstructured
        for ref in refs:
            if ref not in known_dois:
                wanted.setdefault(ref, label)

    log(f"backward: {len(wanted)} unseen references across {seeds_with_doi} seeds "
        f"with a DOI ({len(seeds) - seeds_with_doi} seeds skipped, no DOI); "
        f"{unresolvable} references had no DOI to resolve")
    if not wanted:
        return 0

    # Fetch in batches, then attribute each record to the seed that cited it.
    fetched = crossref.fetch_by_dois(list(wanted), "snowball:backward")
    for rec in fetched:
        seed_label = wanted.get(rec.get("doi", ""))
        if seed_label:
            rec["discovered_via"] = [f"snowball:backward:{seed_label}"]

    new, skipped = absorb(store, fetched, from_year, topic_gate)
    log(f"backward: {len(fetched)} resolved, {new} new, {skipped} filtered out")
    log_event("snowball_leg", direction="backward", wanted=len(wanted),
              resolved=len(fetched), new=new, skipped=skipped,
              unstructured_refs=unresolvable)
    return new


def forward(store: Store, seeds: list[dict], from_year: int,
            max_per_seed: int, topic_gate: bool) -> int:
    """Pull citing works from OpenCitations, then resolve their metadata.

    The year floor applies before any metadata request is spent. Each result
    carries a DOI, an arXiv id, or both, and goes to whichever can resolve it.
    """
    known_dois, known_arxiv = known_ids(store)
    new = skipped = 0

    for seed in seeds:
        doi = seed.get("doi")
        label = seed.get("citekey") or seed["id"]
        if not doi:
            continue
        try:
            edges = opencitations.citing_works(doi)
        except Exception as exc:  # noqa: BLE001
            log(f"forward lookup failed for {label}: {exc}")
            log_event("snowball_failed", direction="forward", seed=label, error=str(exc))
            continue

        in_window = [e for e in edges if not e["year"] or e["year"] >= from_year]
        # Newest first: when the cap bites, keep the work closest to the frontier.
        in_window.sort(key=lambda e: e["year"] or 0, reverse=True)
        capped = in_window[:max_per_seed]

        dois = [e["doi"] for e in capped if e["doi"] and e["doi"] not in known_dois]
        arxiv = [e["arxiv_id"] for e in capped
                 if e["arxiv_id"] and not e["doi"] and e["arxiv_id"] not in known_arxiv]

        fetched = crossref.fetch_by_dois(dois, f"snowball:forward:{label}")
        fetched += search_arxiv.fetch_by_ids(arxiv, f"snowball:forward:{label}")

        seed_new, seed_skipped = absorb(store, fetched, from_year, topic_gate)
        new += seed_new
        skipped += seed_skipped
        log(f"forward: {label} cited by {len(edges)} ({len(capped)} in window), "
            f"{len(fetched)} resolved, {seed_new} new")

    log(f"forward: {new} new, {skipped} filtered out")
    log_event("snowball_leg", direction="forward", new=new, skipped=skipped)
    return new


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--seed-status", default="included",
                    help="which records to expand from (default: included)")
    ap.add_argument("--direction", choices=["backward", "forward", "both"], default="both")
    ap.add_argument("--from-year", type=int, default=2020)
    ap.add_argument("--max-forward", type=int, default=50,
                    help="cap on citing works pulled per seed")
    ap.add_argument("--no-topic-gate", action="store_true")
    args = ap.parse_args()

    store = Store()
    seeds = store.by_status(args.seed_status)
    if not seeds:
        log(f"no records with status={args.seed_status!r}; screen some papers first")
        return

    without_doi = sum(1 for s in seeds if not s.get("doi"))
    if without_doi:
        log(f"{without_doi} of {len(seeds)} seeds have no DOI and cannot be expanded; "
            f"run enrich.py first if that number looks high")

    topic_gate = not args.no_topic_gate
    added = 0
    if args.direction in ("backward", "both"):
        added += backward(store, seeds, args.from_year, topic_gate)
    if args.direction in ("forward", "both"):
        added += forward(store, seeds, args.from_year, args.max_forward, topic_gate)

    store.save()
    log(f"snowball added {added} records; library holds {len(store.records)}: {store.counts()}")
    log_event("snowball", direction=args.direction, seeds=len(seeds),
              seeds_without_doi=without_doi, added=added)


if __name__ == "__main__":
    main()
