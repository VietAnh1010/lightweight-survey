"""Search Semantic Scholar and merge results into the library.

Optional third source, run after OpenAlex and arXiv: its relevance ranking
surfaces different papers than OpenAlex's, which is what we want for recall.

**Needs S2_API_KEY to be useful.** The keyless tier throttles the search
endpoints hard enough that they return nothing but 429s (unlike /paper/batch,
which enrich.py uses without a key). The script gives up after three throttled
queries rather than retrying all night. Skipping it costs recall, nothing else.

    python3 scripts/search_s2.py --query "LLM unit test generation" --max 100
"""

from __future__ import annotations

import argparse

from common import (
    S2_API_KEY,
    Store,
    clean_text,
    get_json,
    log,
    log_event,
    match_venue,
    norm_arxiv,
    norm_doi,
)
from topic import in_topic

API = "https://api.semanticscholar.org/graph/v1/paper/search"

FIELDS = ",".join([
    "paperId",
    "externalIds",
    "title",
    "abstract",
    "year",
    "venue",
    "publicationVenue",
    "publicationTypes",
    "authors",
    "citationCount",
    "openAccessPdf",
])

MAX_OFFSET = 1000  # hard cap in the relevance-search endpoint


def auth_headers() -> dict:
    return {"x-api-key": S2_API_KEY} if S2_API_KEY else {}


def parse_paper(paper: dict, discovered_via: str) -> dict | None:
    title = clean_text(paper.get("title"))
    if not title:
        return None

    external = paper.get("externalIds") or {}
    pub_venue = paper.get("publicationVenue") or {}
    venue = clean_text(pub_venue.get("name") or paper.get("venue"))
    oa = paper.get("openAccessPdf") or {}

    rec = {
        "title": title,
        "authors": [clean_text(a.get("name")) for a in paper.get("authors") or []],
        "year": paper.get("year"),
        "venue": venue,
        "venue_short": match_venue(venue),
        "doi": norm_doi(external.get("DOI")),
        "arxiv_id": norm_arxiv(external.get("ArXiv")),
        "s2_id": paper.get("paperId") or "",
        "abstract": clean_text(paper.get("abstract")),
        "cited_by_count": paper.get("citationCount") or 0,
        "pdf_url": oa.get("url") or "",
        "sources": ["s2"],
        "discovered_via": [discovered_via],
    }
    return {k: v for k, v in rec.items() if v not in (None, "", [])}


def search(query: str, from_year: int, max_results: int) -> list[dict]:
    # Query files use ` AND ` for the other two backends; S2's relevance search
    # takes plain text, where a literal "AND" token just adds noise.
    query = query.replace(" AND ", " ")
    papers: list[dict] = []
    offset = 0
    while len(papers) < max_results and offset < MAX_OFFSET:
        limit = min(100, max_results - len(papers), MAX_OFFSET - offset)
        payload = get_json(
            API,
            {
                "query": query,
                "fields": FIELDS,
                "year": f"{from_year}-",
                "offset": offset,
                "limit": limit,
            },
            headers=auth_headers(),
        )
        batch = payload.get("data") or []
        papers.extend(batch)
        if not batch or "next" not in payload:
            break
        offset = payload["next"]
    return papers[:max_results]


def run(queries: list[str], from_year: int, max_results: int, topic_gate: bool) -> None:
    store = Store()
    total_new = total_seen = 0
    throttled = 0

    for query in queries:
        try:
            papers = search(query, from_year, max_results)
        except Exception as exc:  # noqa: BLE001
            throttled += "429" in str(exc)
            log(f"query failed: {query!r}: {exc}")
            log_event("query_failed", source="s2", query=query, error=str(exc))
            if throttled >= 3:
                log("three queries lost to rate limiting; abandoning S2 search. "
                    "OpenAlex and arXiv cover this ground — see the note in README.md.")
                break
            continue

        new = seen = skipped = 0
        for paper in papers:
            rec = parse_paper(paper, f"s2:{query}")
            if rec is None:
                continue
            if topic_gate and not in_topic(rec):
                skipped += 1
                continue
            _, is_new = store.upsert(rec)
            new += is_new
            seen += 1

        total_new += new
        total_seen += seen
        log(f"{query!r}: {len(papers)} hits, {seen} in-topic, {new} new, {skipped} filtered")
        log_event("query", source="s2", query=query,
                  hits=len(papers), kept=seen, new=new, skipped=skipped)

    store.save()
    log(f"done: {total_new} new / {total_seen} in-topic")
    log(f"library now holds {len(store.records)} records: {store.counts()}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--query", action="append", default=[])
    ap.add_argument("--queries-file")
    ap.add_argument("--from-year", type=int, default=2020)
    ap.add_argument("--max", dest="max_results", type=int, default=100)
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

    run(queries, args.from_year, args.max_results, not args.no_topic_gate)


if __name__ == "__main__":
    main()
