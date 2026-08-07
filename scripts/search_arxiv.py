"""Search the arXiv API and merge results into the library.

arXiv matters here because much of the LLM-for-PL/SE work appears as a
preprint months before it lands at a committee, and OpenAlex indexes preprint
abstracts unevenly.

    python3 scripts/search_arxiv.py --query '"large language model" AND fuzzing'
    python3 scripts/search_arxiv.py --queries-file config/queries.txt --max 100
"""

from __future__ import annotations

import argparse
import re
import xml.etree.ElementTree as ET

from common import (
    Store,
    clean_text,
    http_get,
    log,
    log_event,
    match_venue,
    norm_arxiv,
    norm_doi,
)
from topic import in_topic

API = "http://export.arxiv.org/api/query"
NS = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}

# The categories this survey covers: software engineering, programming
# languages, logic in CS, cryptography/security, and machine learning.
DEFAULT_CATEGORIES = ["cs.SE", "cs.PL", "cs.LO", "cs.CR", "cs.AI", "cs.LG"]


def _text(entry: ET.Element, path: str) -> str:
    node = entry.find(path, NS)
    return clean_text(node.text) if node is not None and node.text else ""


def parse_entry(entry: ET.Element, discovered_via: str) -> dict | None:
    title = _text(entry, "atom:title")
    if not title:
        return None

    arxiv_url = _text(entry, "atom:id")
    published = _text(entry, "atom:published")
    journal_ref = _text(entry, "arxiv:journal_ref")
    year = None
    if published[:4].isdigit():
        year = int(published[:4])

    pdf_url = ""
    for link in entry.findall("atom:link", NS):
        if link.get("title") == "pdf":
            pdf_url = link.get("href") or ""

    venue = journal_ref or "arXiv"
    rec = {
        "title": title,
        "authors": [
            clean_text(a.findtext("atom:name", "", NS))
            for a in entry.findall("atom:author", NS)
        ],
        "year": year,
        "venue": venue,
        "venue_short": match_venue(venue),
        "arxiv_id": norm_arxiv(arxiv_url),
        "doi": norm_doi(_text(entry, "arxiv:doi")),
        "abstract": _text(entry, "atom:summary"),
        "url": arxiv_url,
        "pdf_url": pdf_url,
        "arxiv_categories": [
            c.get("term", "") for c in entry.findall("atom:category", NS)
        ],
        "sources": ["arxiv"],
        "discovered_via": [discovered_via],
    }
    return {k: v for k, v in rec.items() if v not in (None, "", [])}


def search(query: str, categories: list[str], max_results: int) -> list[ET.Element]:
    """Page through arXiv results. The API caps a single page at 2000."""
    # Shared query files are written as plain phrases for OpenAlex; arXiv needs
    # an explicit field prefix, so add one when the query has no `field:` term.
    if not re.search(r"\b(all|ti|abs|au|cat|co|jr|rn|id):", query):
        query = " AND ".join(f'all:"{part.strip()}"'
                             for part in query.split(" AND ") if part.strip())

    cat_clause = " OR ".join(f"cat:{c}" for c in categories)
    search_query = f"({query}) AND ({cat_clause})" if categories else query

    entries: list[ET.Element] = []
    start = 0
    while len(entries) < max_results:
        page_size = min(100, max_results - len(entries))
        body = http_get(
            API,
            {
                "search_query": search_query,
                "start": start,
                "max_results": page_size,
                "sortBy": "relevance",
                "sortOrder": "descending",
            },
            headers={"Accept": "application/atom+xml"},
        )
        root = ET.fromstring(body)
        page = root.findall("atom:entry", NS)
        entries.extend(page)
        if len(page) < page_size:
            break
        start += page_size
    return entries[:max_results]


def run(queries: list[str], categories: list[str], max_results: int,
        from_year: int, topic_gate: bool) -> None:
    store = Store()
    total_new = total_seen = 0

    for query in queries:
        try:
            entries = search(query, categories, max_results)
        except Exception as exc:  # noqa: BLE001
            log(f"query failed: {query!r}: {exc}")
            log_event("query_failed", source="arxiv", query=query, error=str(exc))
            continue

        new = seen = skipped = 0
        for entry in entries:
            rec = parse_entry(entry, f"arxiv:{query}")
            if rec is None:
                continue
            if rec.get("year") and rec["year"] < from_year:
                skipped += 1
                continue
            if topic_gate and not in_topic(rec):
                skipped += 1
                continue
            _, is_new = store.upsert(rec)
            new += is_new
            seen += 1

        total_new += new
        total_seen += seen
        log(f"{query!r}: {len(entries)} hits, {seen} kept, {new} new, {skipped} filtered")
        log_event("query", source="arxiv", query=query,
                  hits=len(entries), kept=seen, new=new, skipped=skipped)

    store.save()
    log(f"done: {total_new} new / {total_seen} kept")
    log(f"library now holds {len(store.records)} records: {store.counts()}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--query", action="append", default=[], help="repeatable")
    ap.add_argument("--queries-file")
    ap.add_argument("--max", dest="max_results", type=int, default=100)
    ap.add_argument("--from-year", type=int, default=2020)
    ap.add_argument("--categories", default=",".join(DEFAULT_CATEGORIES),
                    help="comma-separated arXiv categories, or '' for all")
    ap.add_argument("--no-topic-gate", action="store_true")
    args = ap.parse_args()

    queries = list(args.query)
    if args.queries_file:
        for line in open(args.queries_file, encoding="utf-8"):
            line = line.split("#")[0].strip()
            if line:
                queries.append(line)
    if not queries:
        ap.error("give --query or --queries-file")

    categories = [c.strip() for c in args.categories.split(",") if c.strip()]
    run(queries, categories, args.max_results, args.from_year, not args.no_topic_gate)


if __name__ == "__main__":
    main()
