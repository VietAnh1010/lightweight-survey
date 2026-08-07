"""Expand the library along the citation graph.

Keyword search alone reliably misses foundational work — nobody phrases their
seminal paper the way you phrase your query. Snowballing fixes that:

  backward  the references of papers we already accepted
  forward   the papers that cite papers we already accepted

Both directions are gated on the topic vocabulary and the year floor, so a run
converges instead of swallowing all of computer science.

    python3 scripts/snowball.py --seed-status included
    python3 scripts/snowball.py --direction forward --max-forward 80
"""

from __future__ import annotations

import argparse

from common import (
    CONTACT,
    Store,
    chunked,
    get_json,
    log,
    log_event,
    norm_openalex,
)
from search_openalex import SELECT, parse_work
from topic import in_topic

API = "https://api.openalex.org/works"


def fetch_works(openalex_ids: list[str]) -> list[dict]:
    """Look up works by OpenAlex id, 50 per request."""
    out: list[dict] = []
    for batch in chunked(openalex_ids, 50):
        payload = get_json(
            API,
            {
                "filter": f"openalex_id:{'|'.join(batch)}",
                "select": SELECT,
                "per-page": len(batch),
                "mailto": CONTACT,
            },
        )
        out.extend(payload.get("results") or [])
    return out


def citing_works(openalex_id: str, from_year: int, limit: int) -> list[dict]:
    """Works citing `openalex_id`, most-cited first so the cap keeps the best."""
    payload = get_json(
        API,
        {
            "filter": f"cites:{openalex_id},publication_year:>{from_year - 1}",
            "select": SELECT,
            "sort": "cited_by_count:desc",
            "per-page": min(200, limit),
            "mailto": CONTACT,
        },
    )
    return (payload.get("results") or [])[:limit]


def known_openalex_ids(store: Store) -> set[str]:
    return {r["openalex_id"] for r in store.records.values() if r.get("openalex_id")}


def backward(store: Store, seeds: list[dict], from_year: int, topic_gate: bool) -> int:
    known = known_openalex_ids(store)
    wanted: dict[str, str] = {}  # openalex id -> citekey/id of the seed citing it
    for seed in seeds:
        label = seed.get("citekey") or seed["id"]
        for ref in seed.get("referenced_works") or []:
            ref = norm_openalex(ref)
            if ref and ref not in known:
                wanted.setdefault(ref, label)

    log(f"backward: {len(wanted)} unseen references across {len(seeds)} seeds")
    if not wanted:
        return 0

    new = skipped = 0
    for work in fetch_works(list(wanted)):
        seed_label = wanted.get(norm_openalex(work.get("id")), "?")
        rec = parse_work(work, f"snowball:backward:{seed_label}")
        if rec is None:
            continue
        if rec.get("year") and rec["year"] < from_year:
            skipped += 1
            continue
        if topic_gate and not in_topic(rec):
            skipped += 1
            continue
        rec["snowball_depth"] = 1
        _, is_new = store.upsert(rec)
        new += is_new
    log(f"backward: {new} new, {skipped} filtered out")
    return new


def forward(store: Store, seeds: list[dict], from_year: int,
            max_per_seed: int, topic_gate: bool) -> int:
    new = skipped = 0
    for seed in seeds:
        oa_id = seed.get("openalex_id")
        if not oa_id:
            continue
        label = seed.get("citekey") or seed["id"]
        try:
            works = citing_works(oa_id, from_year, max_per_seed)
        except Exception as exc:  # noqa: BLE001
            log(f"forward lookup failed for {label}: {exc}")
            log_event("snowball_failed", direction="forward", seed=label, error=str(exc))
            continue

        seed_new = 0
        for work in works:
            rec = parse_work(work, f"snowball:forward:{label}")
            if rec is None:
                continue
            if topic_gate and not in_topic(rec):
                skipped += 1
                continue
            rec["snowball_depth"] = 1
            _, is_new = store.upsert(rec)
            seed_new += is_new
        new += seed_new
        log(f"forward: {label} cited by {len(works)} in-scope works, {seed_new} new")
    log(f"forward: {new} new, {skipped} filtered out")
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

    topic_gate = not args.no_topic_gate
    added = 0
    if args.direction in ("backward", "both"):
        added += backward(store, seeds, args.from_year, topic_gate)
    if args.direction in ("forward", "both"):
        added += forward(store, seeds, args.from_year, args.max_forward, topic_gate)

    store.save()
    log(f"snowball added {added} records; library holds {len(store.records)}: {store.counts()}")
    log_event("snowball", direction=args.direction, seeds=len(seeds), added=added)


if __name__ == "__main__":
    main()
