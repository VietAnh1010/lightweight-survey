"""Search OpenAlex and merge the results into the library.

OpenAlex is the primary source: no API key, ~250M works, and it carries the
citation graph (`referenced_works`) that snowball.py needs.

    python3 scripts/search_openalex.py --query "large language model fuzzing"
    python3 scripts/search_openalex.py --queries-file config/queries.txt --max 200
"""

from __future__ import annotations

import argparse

from common import (
    CONTACT,
    Store,
    clean_text,
    get_json,
    inverted_to_abstract,
    log,
    log_event,
    match_venue,
    norm_arxiv,
    norm_doi,
    norm_openalex,
)
from topic import in_topic

API = "https://api.openalex.org/works"

SELECT = ",".join([
    "id",
    "doi",
    "ids",
    "display_name",
    "publication_year",
    "authorships",
    "primary_location",
    "best_oa_location",
    "abstract_inverted_index",
    "cited_by_count",
    "referenced_works",
    "type",
])


def parse_work(work: dict, discovered_via: str) -> dict | None:
    """Turn an OpenAlex work object into a library record."""
    title = clean_text(work.get("display_name"))
    if not title:
        return None

    location = work.get("primary_location") or {}
    source = location.get("source") or {}
    venue = clean_text(source.get("display_name"))
    oa = work.get("best_oa_location") or {}
    ids = work.get("ids") or {}
    doi = norm_doi(work.get("doi"))
    # OpenAlex mints arXiv preprints as 10.48550/arXiv.NNNN.NNNNN; that DOI is
    # the only place the arXiv id reliably appears.
    arxiv_id = norm_arxiv(ids.get("arxiv") or "")
    if not arxiv_id and "10.48550/arxiv" in doi:
        arxiv_id = norm_arxiv(doi)

    rec = {
        "title": title,
        "authors": [
            clean_text((a.get("author") or {}).get("display_name"))
            for a in work.get("authorships") or []
        ],
        "year": work.get("publication_year"),
        "venue": venue,
        "venue_short": match_venue(venue),
        "doi": doi,
        "openalex_id": norm_openalex(work.get("id")),
        "arxiv_id": arxiv_id,
        "abstract": inverted_to_abstract(work.get("abstract_inverted_index")),
        "cited_by_count": work.get("cited_by_count") or 0,
        "referenced_works": [norm_openalex(w) for w in work.get("referenced_works") or []],
        "url": location.get("landing_page_url") or "",
        "pdf_url": oa.get("pdf_url") or "",
        "work_type": work.get("type") or "",
        "sources": ["openalex"],
        "discovered_via": [discovered_via],
    }
    return {k: v for k, v in rec.items() if v not in (None, "", [], 0) or k in ("year", "cited_by_count")}


def search(query: str, from_year: int, max_results: int) -> list[dict]:
    """Page through OpenAlex results for one query."""
    # Commas delimit filters in OpenAlex, so they can't appear in a value.
    safe_query = query.replace(",", " ").strip()
    works: list[dict] = []
    cursor = "*"
    while len(works) < max_results:
        payload = get_json(
            API,
            {
                "filter": f"publication_year:>{from_year - 1},title_and_abstract.search:{safe_query}",
                "select": SELECT,
                "per-page": min(200, max_results - len(works)),
                "cursor": cursor,
                "mailto": CONTACT,
            },
        )
        batch = payload.get("results") or []
        works.extend(batch)
        cursor = (payload.get("meta") or {}).get("next_cursor")
        if not batch or not cursor:
            break
    return works[:max_results]


def run(queries: list[str], from_year: int, max_results: int, topic_gate: bool) -> None:
    store = Store()
    total_new = total_seen = total_skipped = 0

    for query in queries:
        try:
            works = search(query, from_year, max_results)
        except Exception as exc:  # noqa: BLE001 - one bad query must not kill the run
            log(f"query failed: {query!r}: {exc}")
            log_event("query_failed", source="openalex", query=query, error=str(exc))
            continue

        new = seen = skipped = 0
        for work in works:
            rec = parse_work(work, f"openalex:{query}")
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
        total_skipped += skipped
        log(f"{query!r}: {len(works)} hits, {seen} in-topic, {new} new, {skipped} off-topic")
        log_event(
            "query", source="openalex", query=query,
            hits=len(works), kept=seen, new=new, skipped=skipped,
        )

    store.save()
    log(f"done: {total_new} new / {total_seen} in-topic / {total_skipped} filtered out")
    log(f"library now holds {len(store.records)} records: {store.counts()}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--query", action="append", default=[], help="repeatable")
    ap.add_argument("--queries-file", help="one query per line; # comments allowed")
    ap.add_argument("--from-year", type=int, default=2020)
    ap.add_argument("--max", dest="max_results", type=int, default=200,
                    help="max results per query")
    ap.add_argument("--no-topic-gate", action="store_true",
                    help="keep hits that fail the LLM+task keyword gate")
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
