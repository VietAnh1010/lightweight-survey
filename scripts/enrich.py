"""Fill in fields the harvest left blank.

No abstract means no screening — `CLAUDE.md` forbids screening from the title.
No venue means no "was this at POPL/PLDI/ICSE" judgement. No DOI means no
snowballing. All three are filled here:

  crossref  venue and DOI; an abstract for the publishers that deposit one
  arxiv     the abstract for everything Crossref left blank, matched on title

A record still missing an abstract afterwards is `unavailable`, never guessed.

    python3 scripts/enrich.py              # everything missing a field
    python3 scripts/enrich.py --status included
"""

from __future__ import annotations

import argparse

import crossref
import search_arxiv
from common import Store, has_real_venue, log, log_event, match_venue


def needs_work(rec: dict) -> bool:
    """A missing DOI counts as a gap: it blocks snowballing.

    Records that have none are retried every run. Cached lookups make that
    cheap, and a paper picks up its DOI on the run after it is published.
    """
    return not rec.get("abstract") or not has_real_venue(rec) or not rec.get("doi")


def enrich_from_crossref(targets: list[dict]) -> int:
    """One batched lookup for everything with a DOI and a hole to fill."""
    by_doi = {r["doi"]: r for r in targets if r.get("doi")}
    if not by_doi:
        return 0

    filled = 0
    for fresh in crossref.fetch_by_dois(list(by_doi), "enrich:crossref"):
        rec = by_doi.get(fresh.get("doi", ""))
        if rec is None:
            continue
        before = (rec.get("abstract"), rec.get("venue"))
        if not rec.get("abstract") and fresh.get("abstract"):
            rec["abstract"] = fresh["abstract"]
        if not has_real_venue(rec) and fresh.get("venue"):
            rec["venue"] = fresh["venue"]
            rec["venue_short"] = fresh.get("venue_short") or match_venue(fresh["venue"])
        for field in ("authors", "year", "url", "pdf_url", "cited_by_count"):
            if not rec.get(field) and fresh.get(field):
                rec[field] = fresh[field]
        if (rec.get("abstract"), rec.get("venue")) != before:
            filled += 1
    log(f"crossref: {len(by_doi)} looked up, {filled} improved")
    return filled


def match_published_version(store: Store, targets: list[dict]) -> int:
    """Find the published DOI for arXiv-only records, by title.

    The step that keeps snowballing possible: the harvest is arXiv, most
    records arrive with no DOI, and both citation sources are DOI-keyed. It
    also swaps the venue "arXiv" for the committee SCOPE.md screens on.
    """
    pending = [r for r in targets if not r.get("doi") and r.get("title")]
    if not pending:
        return 0

    log(f"crossref: title-matching {len(pending)} records with no DOI")
    matched = 0
    for rec in pending:
        published = crossref.find_by_title(rec["title"], "enrich:crossref-title")
        if published is None or not published.get("doi"):
            continue
        if store.find({"doi": published["doi"]}):
            continue  # the published version is already a separate record
        rec["doi"] = published["doi"]
        if published.get("venue"):
            rec["venue"] = published["venue"]
            rec["venue_short"] = published.get("venue_short") or match_venue(published["venue"])
        if not rec.get("abstract") and published.get("abstract"):
            rec["abstract"] = published["abstract"]
        rec["sources"] = list(dict.fromkeys(rec.get("sources", []) + ["crossref"]))
        store.reindex(rec)
        matched += 1
    log(f"crossref: {matched} of {len(pending)} matched to a published version")
    return matched


def enrich_from_arxiv(targets: list[dict]) -> int:
    """Recover abstracts from the preprint, one title search per record.

    The slow path — arXiv asks for one request per three seconds — so it runs
    only for records still missing an abstract.
    """
    pending = [r for r in targets if not r.get("abstract") and r.get("title")]
    if not pending:
        return 0

    log(f"arxiv: title-matching {len(pending)} records with no abstract")
    filled = 0
    for rec in pending:
        match = search_arxiv.find_by_title(rec["title"])
        if match is None:
            continue
        rec["abstract"] = match["abstract"]
        if not rec.get("arxiv_id") and match.get("arxiv_id"):
            rec["arxiv_id"] = match["arxiv_id"]
        if not rec.get("pdf_url") and match.get("pdf_url"):
            rec["pdf_url"] = match["pdf_url"]
        rec["sources"] = list(dict.fromkeys(rec.get("sources", []) + ["arxiv"]))
        filled += 1
    log(f"arxiv: {filled} abstracts recovered from preprints")
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
    ap.add_argument("--skip-arxiv", action="store_true",
                    help="arXiv title matching is one request per record, and slow")
    ap.add_argument("--skip-title-match", action="store_true",
                    help="skip the Crossref title lookup that finds published DOIs")
    args = ap.parse_args()

    store = Store()
    pool = store.by_status(args.status) if args.status else list(store.records.values())
    targets = [r for r in pool if needs_work(r)]
    log(f"{len(targets)} of {len(pool)} records missing an abstract, venue, or DOI")

    from_crossref = enrich_from_crossref(targets)
    published = 0 if args.skip_title_match else match_published_version(store, targets)
    from_arxiv = 0 if args.skip_arxiv else enrich_from_arxiv(targets)
    revised = refresh_venue_shorts(store)
    store.save()

    no_abstract = sum(1 for r in pool if not r.get("abstract"))
    no_doi = sum(1 for r in pool if not r.get("doi"))
    log(f"crossref filled {from_crossref}, {published} matched to a published version, "
        f"arxiv filled {from_arxiv}, {revised} venue tags revised")
    log(f"{no_abstract} still have no abstract (unscreenable); "
        f"{no_doi} still have no DOI (cannot be snowballed from)")
    log_event("enrich", crossref=from_crossref, published=published, arxiv=from_arxiv,
              revised=revised, no_abstract=no_abstract, no_doi=no_doi)


if __name__ == "__main__":
    main()
