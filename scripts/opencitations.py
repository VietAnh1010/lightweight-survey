"""OpenCitations: who cites a given DOI, the forward half of the citation graph.

Open citation data only: a citing paper appears here only if its publisher
deposited an open reference list. A thin result is thin data, not an uncited
paper — record which in STATUS.md rather than claiming exhaustive coverage.
"""

from __future__ import annotations

import re

from common import get_json, norm_arxiv, norm_doi

# Canonical host; opencitations.net/index/api/v2/... 301s here.
API = "https://api.opencitations.net/index/v2/citations"

# The `citing` field packs several id namespaces into one space-separated
# string, e.g. "omid:br/06023053062 arxiv:2502.13499 doi:10.1145/3597503".
_DOI = re.compile(r"doi:(\S+)")
_ARXIV = re.compile(r"arxiv:(\S+)")


def _year(value: str | None) -> int | None:
    """`creation` is the citing work's date: "2026" or "2026-01" or ""."""
    if value and value[:4].isdigit():
        return int(value[:4])
    return None


def citing_works(doi: str) -> list[dict]:
    """Identifiers of the works citing `doi`, with the citing year.

    The year comes back here, so the year floor applies before any metadata
    request is spent.
    """
    payload = get_json(f"{API}/doi:{doi}")
    out: list[dict] = []
    for edge in payload or []:
        citing = edge.get("citing") or ""
        doi_match = _DOI.search(citing)
        arxiv_match = _ARXIV.search(citing)
        if not doi_match and not arxiv_match:
            continue  # OMID only: nothing we can resolve metadata for
        out.append({
            "doi": norm_doi(doi_match.group(1)) if doi_match else "",
            "arxiv_id": norm_arxiv(arxiv_match.group(1)) if arxiv_match else "",
            "year": _year(edge.get("creation")),
        })
    return out
