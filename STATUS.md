# Status

Live run state. **Update after every batch, then commit.** If the session
dies, this file plus the git log is the entire handoff.

---

## Current

- **Phase:** not started — repo scaffolded, pipeline smoke-tested, awaiting the run
- **Last updated:** 2026-08-06
- **Next action:** Phase 1 harvest, per `prompts/literature-review.md`

## Counts

| | |
|---|---|
| candidates seen | 0 |
| screened | 0 |
| included | 0 |
| excluded | 0 |
| unavailable | 0 |

_Refresh with `python3 scripts/screen.py stats`._

## Coverage by category

_Filled in from `screen.py stats` once screening starts. Categories still at
zero late in the run need targeted queries before concluding the literature is
thin there._

## Snowball rounds

| Round | Direction | Seeds | New candidates |
|---|---|---|---|
| — | — | — | — |

Stopping criterion (`SCOPE.md`): two consecutive rounds each yielding fewer
than 5 new in-scope candidates.

## Open questions

Things to raise with the user rather than block on. Record and keep going.

- Two seed papers supplied (`SCOPE.md` § Seed papers), `2026-08-08`.
  - Resolve both through `search_arxiv.py --query "<title>"` before Phase 2.

## Decisions made under uncertainty

Judgement calls worth a second look in the morning. Borderline
include/exclude calls, category assignments, papers cut for balance.

| Paper | Call | Why |
|---|---|---|
| — | — | — |

## Run log

Append one line per batch: what ran, what it yielded.

- `2026-08-06` — repo scaffolded; pipeline verified end to end against live APIs.
  - OpenAlex and arXiv search, S2 batch enrichment, screening, report generation.
  - Citation gate catches a planted fake DOI and a planted invented quote.
  - Library reset to empty for the real run.
