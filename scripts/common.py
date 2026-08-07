"""Shared plumbing for the survey pipeline.

Stdlib only, on purpose: the overnight cloud session should never need to
install anything. Provides HTTP with on-disk caching / retry / per-host rate
limiting, record normalization and deduplication, and the JSONL paper store.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE_DIR = ROOT / ".cache"
LIBRARY = ROOT / "papers" / "library.jsonl"
NOTES_DIR = ROOT / "papers" / "notes"
LOG_DIR = ROOT / "logs"

CONTACT = os.environ.get("SURVEY_CONTACT_EMAIL", "vietanh101003@gmail.com")
USER_AGENT = f"lightweight-survey/0.1 (mailto:{CONTACT})"
S2_API_KEY = os.environ.get("S2_API_KEY", "")

# Minimum seconds between requests to the same host. arXiv asks for one
# request per three seconds; Semantic Scholar's keyless tier is ~1/sec.
RATE_LIMITS = {
    "api.openalex.org": 0.15,
    "export.arxiv.org": 3.0,
    # S2's keyless tier is aggressive: search often 429s outright, though
    # /paper/batch usually survives. Set S2_API_KEY to make search viable.
    "api.semanticscholar.org": 3.0 if not S2_API_KEY else 1.0,
    "api.crossref.org": 0.5,
    "dblp.org": 1.0,
}
DEFAULT_RATE = 1.0
_last_request: dict[str, float] = {}


# --------------------------------------------------------------------------
# logging
# --------------------------------------------------------------------------

def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", file=sys.stderr, flush=True)


def log_event(kind: str, **fields) -> None:
    """Append a structured event to logs/events.jsonl for run forensics."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    event = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "kind": kind, **fields}
    with (LOG_DIR / "events.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(event, ensure_ascii=False) + "\n")


# --------------------------------------------------------------------------
# HTTP
# --------------------------------------------------------------------------

class FetchError(RuntimeError):
    """A request failed permanently (after retries) or was refused."""


def _cache_path(url: str) -> Path:
    host = urllib.parse.urlparse(url).netloc or "unknown"
    digest = hashlib.sha256(url.encode("utf-8")).hexdigest()[:24]
    return CACHE_DIR / host / f"{digest}.json"


def _throttle(host: str) -> None:
    gap = RATE_LIMITS.get(host, DEFAULT_RATE)
    elapsed = time.monotonic() - _last_request.get(host, 0.0)
    if elapsed < gap:
        time.sleep(gap - elapsed)
    _last_request[host] = time.monotonic()


def http_get(
    url: str,
    params: dict | None = None,
    *,
    headers: dict | None = None,
    use_cache: bool = True,
    retries: int = 5,
    timeout: int = 60,
) -> str:
    """GET a URL, returning the body as text.

    Responses are cached on disk keyed by full URL, so re-running any stage of
    the pipeline is cheap and the whole run stays reproducible. 4xx responses
    other than 429 are permanent and are not retried.
    """
    if params:
        url = f"{url}?{urllib.parse.urlencode(params, safe=':,>|<*')}"
    cache_file = _cache_path(url)
    if use_cache and cache_file.exists():
        try:
            return json.loads(cache_file.read_text(encoding="utf-8"))["body"]
        except (json.JSONDecodeError, KeyError):
            cache_file.unlink(missing_ok=True)  # corrupt entry, refetch

    host = urllib.parse.urlparse(url).netloc
    req_headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    if headers:
        req_headers.update(headers)

    backoff = 2.0
    last_error = ""
    for attempt in range(1, retries + 1):
        _throttle(host)
        req = urllib.request.Request(url, headers=req_headers)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read().decode("utf-8", errors="replace")
            cache_file.parent.mkdir(parents=True, exist_ok=True)
            cache_file.write_text(
                json.dumps({"url": url, "fetched": time.time(), "body": body}),
                encoding="utf-8",
            )
            return body
        except urllib.error.HTTPError as exc:
            last_error = f"HTTP {exc.code}"
            if exc.code == 429 or exc.code >= 500:
                wait = float(exc.headers.get("Retry-After") or backoff)
                log(f"{last_error} from {host}, retry {attempt}/{retries} in {wait:.0f}s")
                time.sleep(wait)
                backoff = min(backoff * 2, 120)
                continue
            raise FetchError(f"{last_error} for {url}") from exc
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last_error = str(exc)
            log(f"network error ({last_error}), retry {attempt}/{retries} in {backoff:.0f}s")
            time.sleep(backoff)
            backoff = min(backoff * 2, 120)

    log_event("fetch_failed", url=url, error=last_error)
    raise FetchError(f"giving up on {url} after {retries} attempts: {last_error}")


def get_json(url: str, params: dict | None = None, **kwargs) -> dict:
    return json.loads(http_get(url, params, **kwargs))


def post_json(
    url: str,
    payload: dict,
    params: dict | None = None,
    *,
    headers: dict | None = None,
    retries: int = 5,
    timeout: int = 90,
):
    """POST JSON and decode the reply. Uncached — used for batch lookups.

    Only Semantic Scholar's /paper/batch needs this, and it is what makes
    enrichment take minutes instead of hours on the keyless tier.
    """
    if params:
        url = f"{url}?{urllib.parse.urlencode(params, safe=':,>|<*')}"
    host = urllib.parse.urlparse(url).netloc
    req_headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    if headers:
        req_headers.update(headers)
    data = json.dumps(payload).encode("utf-8")

    backoff = 2.0
    last_error = ""
    for attempt in range(1, retries + 1):
        _throttle(host)
        req = urllib.request.Request(url, data=data, headers=req_headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8", errors="replace"))
        except urllib.error.HTTPError as exc:
            last_error = f"HTTP {exc.code}"
            if exc.code == 429 or exc.code >= 500:
                wait = float(exc.headers.get("Retry-After") or backoff)
                log(f"{last_error} from {host}, retry {attempt}/{retries} in {wait:.0f}s")
                time.sleep(wait)
                backoff = min(backoff * 2, 120)
                continue
            raise FetchError(f"{last_error} for {url}") from exc
        except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
            last_error = str(exc)
            time.sleep(backoff)
            backoff = min(backoff * 2, 120)

    log_event("post_failed", url=url, error=last_error)
    raise FetchError(f"giving up on POST {url}: {last_error}")


def chunked(items: list, size: int):
    for start in range(0, len(items), size):
        yield items[start : start + size]


# --------------------------------------------------------------------------
# normalization
# --------------------------------------------------------------------------

_WS = re.compile(r"\s+")
_NON_ALNUM = re.compile(r"[^a-z0-9 ]+")


def clean_text(value: str | None) -> str:
    if not value:
        return ""
    text = unicodedata.normalize("NFKC", value)
    return _WS.sub(" ", text).strip()


def norm_title(title: str | None) -> str:
    """Aggressively normalized title, used only as a dedup alias."""
    text = clean_text(title).lower()
    text = _NON_ALNUM.sub(" ", text)
    return _WS.sub(" ", text).strip()


def norm_doi(doi: str | None) -> str:
    if not doi:
        return ""
    doi = clean_text(doi).lower()
    doi = re.sub(r"^(https?://)?(dx\.)?doi\.org/", "", doi)
    return doi.removeprefix("doi:").strip()


def norm_arxiv(value: str | None) -> str:
    """Extract a bare arXiv id (no version suffix) from an id or URL."""
    if not value:
        return ""
    match = re.search(r"(\d{4}\.\d{4,5})(v\d+)?", value)
    if match:
        return match.group(1)
    match = re.search(r"([a-z-]+(\.[A-Z]{2})?/\d{7})(v\d+)?", value)
    return match.group(1) if match else ""


def norm_openalex(value: str | None) -> str:
    if not value:
        return ""
    match = re.search(r"(W\d+)", value)
    return match.group(1) if match else ""


def aliases(rec: dict) -> list[str]:
    """Every identifier this record can be recognized by, strongest first."""
    out = []
    if rec.get("doi"):
        out.append(f"doi:{rec['doi']}")
    if rec.get("arxiv_id"):
        out.append(f"arxiv:{rec['arxiv_id']}")
    if rec.get("openalex_id"):
        out.append(f"openalex:{rec['openalex_id']}")
    if rec.get("s2_id"):
        out.append(f"s2:{rec['s2_id']}")
    title = norm_title(rec.get("title"))
    if title:
        out.append(f"title:{title}")
    return out


def record_id(rec: dict) -> str:
    """Stable primary key. DOI wins, then arXiv, then OpenAlex, then title."""
    for alias in aliases(rec):
        if not alias.startswith("title:"):
            return alias
    title = norm_title(rec.get("title"))
    if not title:
        raise ValueError("record has no identifier and no title")
    return "title:" + hashlib.sha1(title.encode()).hexdigest()[:12]


def inverted_to_abstract(index: dict | None) -> str:
    """Rebuild OpenAlex's inverted abstract index into plain text."""
    if not index:
        return ""
    positions: list[tuple[int, str]] = []
    for word, spots in index.items():
        positions.extend((spot, word) for spot in spots)
    positions.sort()
    return clean_text(" ".join(word for _, word in positions))


# --------------------------------------------------------------------------
# venues
# --------------------------------------------------------------------------

# The committees named in SCOPE.md. POPL/OOPSLA now publish through PACMPL and
# FSE through PACMSE, so match on the conference name as well as the journal.
VENUE_PATTERNS = {
    "POPL": r"\bpopl\b|principles of programming languages",
    "PLDI": r"\bpldi\b|programming language design and implementation",
    "OOPSLA": r"\boopsla\b|object-oriented programming.*systems.*languages",
    "ICSE": r"\bicse\b|international conference on software engineering",
    "FSE": r"\bfse\b|foundations of software engineering|\besec\b",
    "ASE": r"\base\b|automated software engineering",
    "CAV": r"\bcav\b|computer[- ]aided verification",
    "FM": r"\bfm\b|formal methods(?! in)|international symposium on formal methods",
    "ISSTA": r"\bissta\b|software testing and analysis",
    "NDSS": r"\bndss\b|network and distributed system security",
    "S&P": r"\bieee symposium on security and privacy\b|\boakland\b",
    "USENIX-SEC": r"usenix security",
    "CCS": r"\bccs\b|computer and communications security",
    "TACAS": r"\btacas\b|tools and algorithms for the construction",
    "ITP": r"\bitp\b|interactive theorem proving",
    "CPP": r"certified programs and proofs",
    "NeurIPS": r"\bneurips\b|neural information processing systems",
    "ICML": r"\bicml\b|international conference on machine learning",
    "ICLR": r"\biclr\b|learning representations",
    "ACL": r"\bacl\b|association for computational linguistics",
    "arXiv": r"\barxiv\b|corr",
}

# Committees the scope calls out explicitly; everything else is secondary.
TARGET_VENUES = {"POPL", "PLDI", "OOPSLA", "ICSE", "FSE", "ASE", "CAV", "FM"}


def match_venue(venue: str | None) -> str:
    """Map a raw venue string onto a canonical short name, or "" if unknown."""
    text = clean_text(venue).lower()
    if not text:
        return ""
    for name, pattern in VENUE_PATTERNS.items():
        if re.search(pattern, text):
            return name
    return ""


def venue_tier(rec: dict) -> str:
    """target = a committee named in SCOPE.md, other = known, unknown = rest."""
    canonical = rec.get("venue_short") or match_venue(rec.get("venue"))
    if canonical in TARGET_VENUES:
        return "target"
    return "other" if canonical else "unknown"


# --------------------------------------------------------------------------
# store
# --------------------------------------------------------------------------

# Fields owned by the screening/notetaking process. A re-fetch from any API
# must never clobber them, or an interrupted run loses its human judgment.
CURATED_FIELDS = {
    "status",
    "reason",
    "tags",
    "categories",
    "citekey",
    "note_path",
    "screened_at",
    "priority",
}

STATUSES = {"candidate", "included", "excluded", "unavailable"}


class Store:
    """The paper library, persisted as JSONL (one record per line).

    JSONL rather than SQLite so the state stays greppable, diffable, and
    trivially recoverable if a run dies mid-write.
    """

    def __init__(self, path: Path = LIBRARY):
        self.path = path
        self.records: dict[str, dict] = {}
        self._alias_index: dict[str, str] = {}
        self.load()

    def load(self) -> None:
        self.records.clear()
        self._alias_index.clear()
        if not self.path.exists():
            return
        for line_no, line in enumerate(self.path.read_text(encoding="utf-8").splitlines(), 1):
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                log(f"skipping malformed library line {line_no}")
                continue
            self.records[rec["id"]] = rec
            self._index(rec)

    def _index(self, rec: dict) -> None:
        for alias in aliases(rec):
            self._alias_index.setdefault(alias, rec["id"])

    def find(self, rec: dict) -> str | None:
        """Return the id of an existing record matching any alias of `rec`."""
        for alias in aliases(rec):
            if alias in self._alias_index:
                return self._alias_index[alias]
        return None

    def upsert(self, rec: dict) -> tuple[str, bool]:
        """Insert or merge a record. Returns (id, is_new).

        Merging fills in fields the existing record lacks and unions list
        fields, but never overwrites curated fields or non-empty scalars.
        """
        rec = {k: v for k, v in rec.items() if v not in (None, "", [], {})}
        existing_id = self.find(rec)
        now = time.strftime("%Y-%m-%d")

        if existing_id is None:
            rec["id"] = record_id(rec)
            rec.setdefault("status", "candidate")
            rec.setdefault("first_seen", now)
            rec["last_updated"] = now
            self.records[rec["id"]] = rec
            self._index(rec)
            return rec["id"], True

        current = self.records[existing_id]
        for key, value in rec.items():
            if key in CURATED_FIELDS or key == "id":
                continue
            if key in ("sources", "discovered_via", "referenced_works"):
                merged = list(dict.fromkeys(current.get(key, []) + list(value)))
                current[key] = merged
            elif not current.get(key):
                current[key] = value
        current["last_updated"] = now
        self._index(current)
        return existing_id, False

    def save(self) -> None:
        """Atomic write: a crash mid-save must not truncate the library."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(".jsonl.tmp")
        ordered = sorted(
            self.records.values(),
            key=lambda r: (-(r.get("year") or 0), r.get("title", "")),
        )
        with tmp.open("w", encoding="utf-8") as fh:
            for rec in ordered:
                fh.write(json.dumps(rec, ensure_ascii=False, sort_keys=True) + "\n")
        tmp.replace(self.path)

    def by_status(self, status: str) -> list[dict]:
        return [r for r in self.records.values() if r.get("status") == status]

    def counts(self) -> dict[str, int]:
        out = {s: 0 for s in STATUSES}
        for rec in self.records.values():
            out[rec.get("status", "candidate")] = out.get(rec.get("status", "candidate"), 0) + 1
        return out


# --------------------------------------------------------------------------
# citekeys
# --------------------------------------------------------------------------

_STOPWORDS = {
    "a", "an", "the", "of", "for", "and", "on", "in", "to", "with", "via",
    "using", "towards", "toward", "by", "at", "from", "is", "are",
}


def make_citekey(rec: dict, taken: set[str]) -> str:
    """author + year + first content word, disambiguated with a/b/c."""
    authors = rec.get("authors") or []
    surname = "anon"
    if authors:
        parts = clean_text(authors[0]).split()
        if parts:
            surname = _NON_ALNUM.sub("", parts[-1].lower()) or "anon"
    year = rec.get("year") or "nd"
    word = "paper"
    for candidate in norm_title(rec.get("title")).split():
        if candidate not in _STOPWORDS and len(candidate) > 2:
            word = candidate
            break
    base = f"{surname}{year}{word}"
    key, suffix = base, ord("a")
    while key in taken:
        key = f"{base}{chr(suffix)}"
        suffix += 1
    taken.add(key)
    return key


def assign_citekeys(store: Store) -> None:
    """Give every record a stable citekey, preserving ones already assigned."""
    taken = {r["citekey"] for r in store.records.values() if r.get("citekey")}
    for rec in sorted(store.records.values(), key=lambda r: r.get("first_seen", "")):
        if not rec.get("citekey"):
            rec["citekey"] = make_citekey(rec, taken)
