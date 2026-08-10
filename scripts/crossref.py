"""Crossref: metadata by DOI, and the backward half of the citation graph.

Authoritative on published venue names, and it carries deposited reference
lists. Free and keyless on the polite pool (identify with `mailto`).

Two gaps, both surfaced to the caller rather than hidden here:

  abstracts   only some publishers deposit one; enrich.py backfills from arXiv
  references  only DOI-bearing entries resolve; the rest are counted, not guessed
"""

from __future__ import annotations

from common import (
    CONTACT,
    chunked,
    clean_text,
    get_json,
    log,
    match_venue,
    norm_doi,
    strip_jats,
    title_similarity,
)

API = "https://api.crossref.org/works"

SELECT = ",".join([
    "DOI",
    "title",
    "author",
    "issued",
    "container-title",
    "event",
    "abstract",
    "URL",
    "type",
    "is-referenced-by-count",
    "link",
])

# Keeps the filter URL inside proxy length limits, and still cuts requests 40x.
BATCH = 40


def _authors(item: dict) -> list[str]:
    out = []
    for person in item.get("author") or []:
        name = clean_text(f"{person.get('given', '')} {person.get('family', '')}")
        if not name:
            name = clean_text(person.get("name"))
        if name:
            out.append(name)
    return out


def _year(item: dict) -> int | None:
    for field in ("published", "issued", "published-print", "published-online"):
        parts = ((item.get(field) or {}).get("date-parts") or [[None]])[0]
        if parts and parts[0]:
            return int(parts[0])
    return None


# Springer deposits LNCS proceedings series-first: ["Lecture Notes in Computer
# Science", "Computer Aided Verification"]. Taking entry one reads CAV, FASE,
# and TACAS as the series — the exact venue judgement SCOPE.md turns on.
SERIES_TITLES = {
    "lecture notes in computer science",
    "lecture notes in artificial intelligence",
    "lecture notes in business information processing",
    "communications in computer and information science",
    "ifip advances in information and communication technology",
}


def _venue(item: dict) -> str:
    """The committee that accepted the paper, not the series that printed it."""
    event = clean_text((item.get("event") or {}).get("name"))
    if event:
        return event

    containers = [c for c in (clean_text(t) for t in item.get("container-title") or []) if c]
    if not containers:
        return ""
    for container in containers:
        if match_venue(container):
            return container
    specific = [c for c in containers if c.lower() not in SERIES_TITLES]
    return specific[-1] if specific else containers[0]


def _pdf_url(item: dict) -> str:
    for link in item.get("link") or []:
        if link.get("content-type") == "application/pdf":
            return link.get("URL") or ""
    return ""


def parse_work(item: dict, discovered_via: str) -> dict | None:
    """Turn a Crossref work item into a library record."""
    titles = item.get("title") or []
    title = clean_text(titles[0] if titles else "")
    if not title:
        return None

    venue = _venue(item)

    rec = {
        "title": title,
        "authors": _authors(item),
        "year": _year(item),
        "venue": venue,
        "venue_short": match_venue(venue),
        "doi": norm_doi(item.get("DOI")),
        "abstract": strip_jats(item.get("abstract")),
        "cited_by_count": item.get("is-referenced-by-count") or 0,
        "url": item.get("URL") or "",
        "pdf_url": _pdf_url(item),
        "work_type": item.get("type") or "",
        "sources": ["crossref"],
        "discovered_via": [discovered_via],
    }
    return {k: v for k, v in rec.items()
            if v not in (None, "", [], 0) or k in ("year", "cited_by_count")}


def fetch_by_dois(dois: list[str], discovered_via: str) -> list[dict]:
    """Look up many DOIs as records. Unknown DOIs are simply absent."""
    out: list[dict] = []
    for batch in chunked(list(dict.fromkeys(dois)), BATCH):
        try:
            payload = get_json(
                API,
                {
                    "filter": ",".join(f"doi:{d}" for d in batch),
                    "select": SELECT,
                    "rows": len(batch),
                    "mailto": CONTACT,
                },
            )
        except Exception as exc:  # noqa: BLE001 - one bad batch must not stop a run
            log(f"crossref batch of {len(batch)} failed: {exc}")
            continue
        for item in (payload.get("message") or {}).get("items") or []:
            rec = parse_work(item, discovered_via)
            if rec:
                out.append(rec)
    return out


TITLE_MATCH_THRESHOLD = 0.8


def find_by_title(title: str, discovered_via: str) -> dict | None:
    """The published record for a title, or None if no match is confident.

    Recovers the DOI and venue for arXiv-only records: without a DOI they
    cannot be snowballed from, and without a venue they cannot be judged
    against SCOPE.md. Low yield is the data, not the matcher — a recent
    preprint usually has no published version. The threshold stays high
    because a wrong match assigns a real paper the wrong DOI.
    """
    if len(title.split()) < 3:
        return None
    try:
        payload = get_json(
            API,
            {"query.title": title, "rows": 3, "select": SELECT, "mailto": CONTACT},
        )
    except Exception as exc:  # noqa: BLE001
        log(f"crossref title lookup failed for {title[:50]!r}: {exc}")
        return None

    best, best_score = None, 0.0
    for item in (payload.get("message") or {}).get("items") or []:
        rec = parse_work(item, discovered_via)
        if not rec:
            continue
        score = title_similarity(rec["title"], title)
        if score > best_score:
            best, best_score = rec, score
    return best if best_score >= TITLE_MATCH_THRESHOLD else None


def reference_dois(doi: str) -> tuple[list[str], int]:
    """The DOIs this work cites, plus how many references had none.

    That second number is how much of the reference list was deposited as
    unstructured text, and so is invisible to snowballing.
    """
    payload = get_json(f"{API}/{doi}", {"mailto": CONTACT})
    refs = (payload.get("message") or {}).get("reference") or []
    resolved = [norm_doi(r["DOI"]) for r in refs if r.get("DOI")]
    return list(dict.fromkeys(resolved)), len(refs) - len(resolved)
