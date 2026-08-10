"""The screening interface between the agent and the library.

The agent reads batches of candidates, judges each against SCOPE.md, and
writes the decisions back in bulk. Bulk matters: 400 candidates must not mean
400 subprocess calls.

    python3 scripts/screen.py next --limit 25 > batch.json
    python3 scripts/screen.py apply decisions.json
    python3 scripts/screen.py set doi:10.1145/1234 --status included --priority 3
    python3 scripts/screen.py stats
"""

from __future__ import annotations

import argparse
import json
import sys
import time

from common import STATUSES, Store, assign_citekeys, log, log_event, venue_tier
from topic import categorize, screening_prior


def resolve(store: Store, ident: str) -> dict | None:
    """Accept a record id, a citekey, or an alias."""
    if ident in store.records:
        return store.records[ident]
    for rec in store.records.values():
        if rec.get("citekey") == ident:
            return rec
    found = store._alias_index.get(ident)
    return store.records.get(found) if found else None


def candidate_view(rec: dict) -> dict:
    """What the screening agent sees. Abstract included in full — the whole
    point is that the decision is made from the real text, never from memory."""
    return {
        "id": rec["id"],
        "citekey": rec.get("citekey", ""),
        "title": rec.get("title", ""),
        "authors": (rec.get("authors") or [])[:6],
        "year": rec.get("year"),
        "venue": rec.get("venue", ""),
        "venue_short": rec.get("venue_short", ""),
        "venue_tier": venue_tier(rec),
        "cited_by_count": rec.get("cited_by_count", 0),
        "abstract": rec.get("abstract", ""),
        "url": rec.get("url") or rec.get("pdf_url", ""),
        "discovered_via": rec.get("discovered_via", []),
        "signals": screening_prior(rec),
    }


def rank_key(rec: dict):
    """Screen the most promising first, so an interrupted run still has the
    good papers: target venues, then citations, then recency.

    This only sorts anything once `enrich.py` has run. A fresh arXiv harvest
    gives every record the venue "arXiv" and no citation count, so all three
    keys tie and the order collapses to recency. Enrichment is what assigns the
    published venue that makes a record rank as `target`.
    """
    tier_rank = {"target": 0, "other": 1, "unknown": 2}[venue_tier(rec)]
    return (tier_rank, -(rec.get("cited_by_count") or 0), -(rec.get("year") or 0))


def cmd_next(store: Store, args) -> None:
    pool = [r for r in store.by_status("candidate")]
    if args.venue_tier:
        pool = [r for r in pool if venue_tier(r) == args.venue_tier]
    if args.category:
        pool = [r for r in pool if args.category in categorize(r)]
    pool.sort(key=rank_key)
    batch = pool[: args.limit]
    json.dump(
        {"remaining": len(pool), "batch": [candidate_view(r) for r in batch]},
        sys.stdout,
        ensure_ascii=False,
        indent=2,
    )
    print()


def apply_decision(store: Store, decision: dict) -> str:
    """Apply one decision. Returns a short outcome string for logging."""
    ident = decision.get("id") or decision.get("citekey")
    rec = resolve(store, ident) if ident else None
    if rec is None:
        return f"UNKNOWN {ident}"

    status = decision.get("status")
    if status not in STATUSES:
        return f"BAD-STATUS {ident}: {status!r}"

    rec["status"] = status
    rec["reason"] = decision.get("reason", "").strip()
    rec["screened_at"] = time.strftime("%Y-%m-%d")
    # Fall back to keyword categories when the agent doesn't override them.
    rec["categories"] = decision.get("categories") or categorize(rec)
    if decision.get("priority") is not None:
        rec["priority"] = int(decision["priority"])
    if decision.get("tags"):
        rec["tags"] = decision["tags"]
    return f"{status} {rec.get('citekey') or rec['id']}"


def cmd_apply(store: Store, args) -> None:
    raw = open(args.file, encoding="utf-8").read().strip()
    if raw.startswith("["):
        decisions = json.loads(raw)
    elif raw.startswith("{") and '"decisions"' in raw[:200]:
        decisions = json.loads(raw)["decisions"]
    else:  # JSONL
        decisions = [json.loads(line) for line in raw.splitlines() if line.strip()]

    outcomes = [apply_decision(store, d) for d in decisions]
    problems = [o for o in outcomes if o.startswith(("UNKNOWN", "BAD-STATUS"))]

    assign_citekeys(store)
    store.save()

    applied = len(outcomes) - len(problems)
    log(f"applied {applied}/{len(outcomes)} decisions")
    for problem in problems:
        log(f"  !! {problem}")
    log(f"library: {store.counts()}")
    log_event("screen_apply", applied=applied, failed=len(problems))
    if problems:
        sys.exit(1)


def cmd_set(store: Store, args) -> None:
    outcome = apply_decision(store, {
        "id": args.ident,
        "status": args.status,
        "reason": args.reason,
        "categories": [c.strip() for c in args.categories.split(",") if c.strip()],
        "priority": args.priority,
    })
    assign_citekeys(store)
    store.save()
    log(outcome)
    if outcome.startswith(("UNKNOWN", "BAD-STATUS")):
        sys.exit(1)


def cmd_stats(store: Store, args) -> None:
    from collections import Counter

    counts = store.counts()
    included = store.by_status("included")
    cats = Counter(c for r in included for c in (r.get("categories") or categorize(r)))
    venues = Counter(r.get("venue_short") or "other" for r in included)
    tiers = Counter(venue_tier(r) for r in store.records.values())
    years = Counter(r.get("year") for r in included)

    print(f"library: {len(store.records)} records")
    for status, n in counts.items():
        print(f"  {status:12} {n}")
    print(f"\nvenue tier (all records): {dict(tiers)}")
    print(f"\nincluded by category ({len(included)} papers):")
    for cat, n in cats.most_common():
        print(f"  {cat:22} {n}")
    print("\nincluded by venue:")
    for venue, n in venues.most_common():
        print(f"  {venue:22} {n}")
    print("\nincluded by year:")
    for year, n in sorted(years.items(), key=lambda kv: (kv[0] or 0)):
        print(f"  {year}  {n}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_next = sub.add_parser("next", help="emit a batch of candidates as JSON")
    p_next.add_argument("--limit", type=int, default=25)
    p_next.add_argument("--venue-tier", choices=["target", "other", "unknown"])
    p_next.add_argument("--category")
    p_next.set_defaults(func=cmd_next)

    p_apply = sub.add_parser("apply", help="apply a JSON/JSONL file of decisions")
    p_apply.add_argument("file")
    p_apply.set_defaults(func=cmd_apply)

    p_set = sub.add_parser("set", help="decide a single record")
    p_set.add_argument("ident")
    p_set.add_argument("--status", required=True, choices=sorted(STATUSES))
    p_set.add_argument("--reason", default="")
    p_set.add_argument("--categories", default="")
    p_set.add_argument("--priority", type=int)
    p_set.set_defaults(func=cmd_set)

    p_stats = sub.add_parser("stats", help="library breakdown")
    p_stats.set_defaults(func=cmd_stats)

    args = ap.parse_args()
    args.func(Store(), args)


if __name__ == "__main__":
    main()
