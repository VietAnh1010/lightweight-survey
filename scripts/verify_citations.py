"""The anti-hallucination gate. Run this before calling the review done.

An unattended agent's most damaging failure is a confident citation to a paper
that does not exist, or a real paper credited with claims it never made. This
script tries to catch both, mechanically:

  provenance  every included paper carries a source and an abstract we fetched
  existence   every DOI and arXiv id resolves live, to a matching title/year
  structure   every included paper has a note, with every required section
  quotes      Evidence quotes attributed to the abstract are in it
  references  every citekey cited in review/ resolves to an included paper

Exits non-zero if any ERROR is found, so it works as a run gate.

    python3 scripts/verify_citations.py            # sample 25 live lookups
    python3 scripts/verify_citations.py --all      # check every identifier
    python3 scripts/verify_citations.py --offline  # skip network checks
"""

from __future__ import annotations

import argparse
import random
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path

from common import (
    NOTES_DIR,
    ROOT,
    Store,
    clean_text,
    get_json,
    http_get,
    log_event,
    norm_title,
    title_similarity,
)
from notes import missing_sections, note_path, parse_note

REVIEW_DIR = ROOT / "review"
CROSSREF = "https://api.crossref.org/works"
ARXIV = "http://export.arxiv.org/api/query"
ATOM = {"atom": "http://www.w3.org/2005/Atom"}

TITLE_MATCH_THRESHOLD = 0.8

problems: list[tuple[str, str]] = []


def report(level: str, message: str) -> None:
    problems.append((level, message))


# --------------------------------------------------------------------------
# checks
# --------------------------------------------------------------------------

def check_provenance(papers: list[dict]) -> None:
    for rec in papers:
        label = rec.get("citekey") or rec["id"]
        if not rec.get("sources"):
            report("ERROR", f"{label}: no source recorded — was this fetched, or invented?")
        if not rec.get("abstract"):
            report("ERROR", f"{label}: no abstract stored; screening could not have been grounded")
        if not rec.get("doi") and not rec.get("arxiv_id"):
            report("WARN", f"{label}: no DOI and no arXiv id, so existence cannot be verified")
        if not rec.get("year"):
            report("WARN", f"{label}: no year")
        if not rec.get("reason"):
            report("WARN", f"{label}: included with no recorded reason")


def check_citekeys(papers: list[dict]) -> None:
    counts = Counter(r.get("citekey", "") for r in papers)
    for key, n in counts.items():
        if not key:
            report("ERROR", f"{n} included paper(s) have no citekey; run report.py")
        elif n > 1:
            report("ERROR", f"citekey {key!r} used by {n} papers")


def verify_doi(rec: dict) -> None:
    label = rec.get("citekey") or rec["id"]
    try:
        payload = get_json(f"{CROSSREF}/{rec['doi']}")
    except Exception as exc:  # noqa: BLE001
        report("ERROR", f"{label}: DOI {rec['doi']} did not resolve at Crossref ({exc})")
        return

    message = payload.get("message") or {}
    titles = message.get("title") or []
    if not titles:
        report("WARN", f"{label}: Crossref returned no title for {rec['doi']}")
        return

    score = title_similarity(titles[0], rec.get("title", ""))
    if score < TITLE_MATCH_THRESHOLD:
        report("ERROR",
               f"{label}: DOI {rec['doi']} resolves to {titles[0]!r}, "
               f"but we stored {rec.get('title')!r} (overlap {score:.2f})")

    parts = ((message.get("issued") or {}).get("date-parts") or [[None]])[0]
    live_year = parts[0] if parts else None
    if live_year and rec.get("year") and abs(int(live_year) - int(rec["year"])) > 1:
        report("WARN", f"{label}: year {rec['year']} but Crossref says {live_year}")


def verify_arxiv(rec: dict) -> None:
    label = rec.get("citekey") or rec["id"]
    try:
        body = http_get(ARXIV, {"id_list": rec["arxiv_id"], "max_results": 1},
                        headers={"Accept": "application/atom+xml"})
        entry = ET.fromstring(body).find("atom:entry", ATOM)
    except Exception as exc:  # noqa: BLE001
        report("ERROR", f"{label}: arXiv lookup failed for {rec['arxiv_id']} ({exc})")
        return

    if entry is None:
        report("ERROR", f"{label}: arXiv id {rec['arxiv_id']} does not exist")
        return

    live_title = clean_text(entry.findtext("atom:title", "", ATOM))
    score = title_similarity(live_title, rec.get("title", ""))
    if score < TITLE_MATCH_THRESHOLD:
        report("ERROR",
               f"{label}: arXiv {rec['arxiv_id']} is {live_title!r}, "
               f"but we stored {rec.get('title')!r} (overlap {score:.2f})")


def check_existence(papers: list[dict], sample: int | None) -> None:
    checkable = [r for r in papers if r.get("doi") or r.get("arxiv_id")]
    if sample is not None and sample < len(checkable):
        checkable = random.sample(checkable, sample)
    for rec in checkable:
        if rec.get("doi"):
            verify_doi(rec)
        elif rec.get("arxiv_id"):
            verify_arxiv(rec)


_QUOTE = re.compile(r"^>\s*(.+?)\s*$", re.MULTILINE)
_ATTRIB_ABSTRACT = re.compile(r"abstract", re.IGNORECASE)


def check_notes(papers: list[dict]) -> None:
    for rec in papers:
        label = rec.get("citekey") or rec["id"]
        path = note_path(rec.get("citekey", ""))
        if not path.exists():
            report("ERROR", f"{label}: no note at {path.relative_to(ROOT)}")
            continue

        sections = parse_note(path)
        gaps = missing_sections(sections)
        if gaps:
            report("ERROR", f"{label}: note missing/empty sections: {', '.join(gaps)}")

        evidence = sections.get("evidence", "")
        quotes = _QUOTE.findall(evidence)
        if not quotes:
            report("ERROR", f"{label}: Evidence section has no quoted support")

        # A quote the note attributes to the abstract must be in the abstract
        # we fetched. This is the check that catches invented support.
        stored_abstract = norm_title(rec.get("abstract", ""))
        for quote in quotes:
            if not _ATTRIB_ABSTRACT.search(quote):
                continue
            text = quote.split("—")[0].strip().strip('"“”')
            probe = norm_title(text)
            if len(probe) < 25:
                continue
            if probe not in stored_abstract:
                report("ERROR",
                       f"{label}: Evidence quote attributed to the abstract is not "
                       f"in the stored abstract: {text[:90]!r}")


def check_orphan_notes(papers: list[dict]) -> None:
    known = {r.get("citekey") for r in papers}
    for path in sorted(NOTES_DIR.glob("*.md")):
        if path.stem not in known:
            report("WARN", f"note {path.name} has no matching included paper")


_CITE = re.compile(r"\[@([A-Za-z0-9_-]+)\]|`([a-z][a-z0-9]*\d{4}[a-z0-9]*)`")


def check_review_references(store: Store, papers: list[dict]) -> None:
    """Every citekey mentioned in review/ must resolve to an included paper."""
    valid = {r.get("citekey") for r in papers}
    all_keys = {r.get("citekey") for r in store.records.values() if r.get("citekey")}
    if not REVIEW_DIR.exists():
        return

    for path in sorted(REVIEW_DIR.rglob("*.md")):
        if path.name in {"annotated-bibliography.md", "comparison-table.md"}:
            continue  # generated from the library; nothing to verify
        text = path.read_text(encoding="utf-8")
        cited = {m.group(1) or m.group(2) for m in _CITE.finditer(text)}
        for key in sorted(cited - valid):
            if key in all_keys:
                report("WARN", f"{path.name} cites {key}, which is in the library but not included")
            else:
                report("ERROR", f"{path.name} cites {key}, which is not in the library at all")


# --------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--all", action="store_true", help="verify every identifier, not a sample")
    ap.add_argument("--sample", type=int, default=25, help="how many to verify live")
    ap.add_argument("--offline", action="store_true", help="skip all network checks")
    args = ap.parse_args()

    store = Store()
    papers = store.by_status("included")
    if not papers:
        print("nothing to verify: no papers have status=included")
        return

    check_citekeys(papers)
    check_provenance(papers)
    check_notes(papers)
    check_orphan_notes(papers)
    check_review_references(store, papers)
    if not args.offline:
        check_existence(papers, None if args.all else args.sample)

    grouped: dict[str, list[str]] = defaultdict(list)
    for level, message in problems:
        grouped[level].append(message)

    for level in ("ERROR", "WARN"):
        for message in grouped[level]:
            print(f"{level}: {message}")

    errors, warns = len(grouped["ERROR"]), len(grouped["WARN"])
    scope = "all" if args.all else ("none" if args.offline else f"sample of {args.sample}")
    print(f"\nverified {len(papers)} included papers "
          f"(live identifier checks: {scope}): {errors} errors, {warns} warnings")
    log_event("verify", papers=len(papers), errors=errors, warnings=warns)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
