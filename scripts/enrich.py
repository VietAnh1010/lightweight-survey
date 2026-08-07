"""Fill in fields the search APIs left blank.

Two gaps matter for this survey. Missing abstracts make screening impossible,
and missing venues make the "was this at POPL/PLDI/ICSE/..." judgement
impossible. OpenAlex leaves both blank often enough to matter, so we backfill
from Semantic Scholar (batch, fast) and then Crossref (per-DOI, authoritative
on venue).

    python3 scripts/enrich.py              # everything missing a field
    python3 scripts/enrich.py --status included
"""

from __future__ import annotations

import argparse

from common import (
    S2_API_KEY,
    Store,
    chunked,
    clean_text,
    get_json,
    log,
    log_event,
    match_venue,
    norm_arxiv,
    norm_doi,
    post_json,
)

S2_BATCH = "https://api.semanticscholar.org/graph/v1/paper/batch"
CROSSREF = "https://api.crossref.org/works"

S2_FIELDS = "paperId,externalIds,title,abstract,year,venue,publicationVenue,authors,citationCount,openAccessPdf"


def needs_work(rec: dict) -> bool:
    return not rec.get("abstract") or not rec.get("venue")


def s2_id_for(rec: dict) -> str | None:
    """Semantic Scholar accepts several id namespaces; prefer the strongest."""
    if rec.get("s2_id"):
        return rec["s2_id"]
    if rec.get("doi"):
        return f"DOI:{rec['doi']}"
    if rec.get("arxiv_id"):
        return f"ARXIV:{rec['arxiv_id']}"
    return None


def enrich_from_s2(store: Store, targets: list[dict]) -> int:
    lookup: dict[str, dict] = {}
    for rec in targets:
        key = s2_id_for(rec)
        if key:
            lookup.setdefault(key, rec)
    if not lookup:
        return 0

    headers = {"x-api-key": S2_API_KEY} if S2_API_KEY else {}
    filled = 0
    ids = list(lookup)
    for batch in chunked(ids, 400):
        try:
            results = post_json(
                S2_BATCH, {"ids": batch}, {"fields": S2_FIELDS}, headers=headers
            )
        except Exception as exc:  # noqa: BLE001
            log(f"s2 batch failed ({len(batch)} ids): {exc}")
            log_event("enrich_failed", source="s2", count=len(batch), error=str(exc))
            continue

        for key, paper in zip(batch, results or []):
            if not paper:
                continue  # S2 doesn't know this paper; not an error
            rec = lookup[key]
            external = paper.get("externalIds") or {}
            pub_venue = paper.get("publicationVenue") or {}
            venue = clean_text(pub_venue.get("name") or paper.get("venue"))

            before = (rec.get("abstract"), rec.get("venue"))
            if not rec.get("abstract") and paper.get("abstract"):
                rec["abstract"] = clean_text(paper["abstract"])
            if not rec.get("venue") and venue:
                rec["venue"] = venue
                rec["venue_short"] = match_venue(venue)
            if not rec.get("s2_id") and paper.get("paperId"):
                rec["s2_id"] = paper["paperId"]
            if not rec.get("doi") and external.get("DOI"):
                rec["doi"] = norm_doi(external["DOI"])
            if not rec.get("arxiv_id") and external.get("ArXiv"):
                rec["arxiv_id"] = norm_arxiv(external["ArXiv"])
            if not rec.get("cited_by_count") and paper.get("citationCount"):
                rec["cited_by_count"] = paper["citationCount"]
            if (rec.get("abstract"), rec.get("venue")) != before:
                filled += 1
        log(f"s2 batch: {len(batch)} ids, {filled} records improved so far")
    return filled


def enrich_from_crossref(store: Store, targets: list[dict]) -> int:
    """Crossref is the authority on published venue names; DOI-only."""
    filled = 0
    for rec in targets:
        if rec.get("venue") or not rec.get("doi"):
            continue
        try:
            payload = get_json(f"{CROSSREF}/{rec['doi']}", {"mailto": ""})
        except Exception:  # noqa: BLE001 - a missing DOI record is routine
            continue
        message = payload.get("message") or {}
        container = message.get("container-title") or []
        event = (message.get("event") or {}).get("name")
        venue = clean_text(event or (container[0] if container else ""))
        if venue:
            rec["venue"] = venue
            rec["venue_short"] = match_venue(venue)
            filled += 1
    return filled


def refresh_venue_shorts(store: Store) -> int:
    """Re-derive venue_short for everything: VENUE_PATTERNS may have changed."""
    changed = 0
    for rec in store.records.values():
        current = rec.get("venue_short", "")
        derived = match_venue(rec.get("venue"))
        if derived and derived != current:
            rec["venue_short"] = derived
            changed += 1
    return changed


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--status", help="only enrich records with this status")
    ap.add_argument("--skip-crossref", action="store_true",
                    help="Crossref is one request per DOI and can be slow")
    args = ap.parse_args()

    store = Store()
    pool = store.by_status(args.status) if args.status else list(store.records.values())
    targets = [r for r in pool if needs_work(r)]
    log(f"{len(targets)} of {len(pool)} records missing an abstract or venue")

    from_s2 = enrich_from_s2(store, targets)
    from_crossref = 0 if args.skip_crossref else enrich_from_crossref(store, targets)
    revised = refresh_venue_shorts(store)
    store.save()

    still_missing = sum(1 for r in pool if needs_work(r))
    log(f"s2 filled {from_s2}, crossref filled {from_crossref}, "
        f"{revised} venue tags revised, {still_missing} still incomplete")
    log_event("enrich", s2=from_s2, crossref=from_crossref,
              revised=revised, remaining=still_missing)


if __name__ == "__main__":
    main()
