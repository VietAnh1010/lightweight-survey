# Status

Live run state. **Update after every batch, then commit.** If the session
dies, this file plus the git log is the entire handoff.

---

## Current

- **Phase:** not started — repo scaffolded, pipeline smoke-tested, awaiting the run
- **Last updated:** 2026-08-10
- **Next action:** Phase 1 harvest, per `prompts/literature-review.md`
- **Before a cloud run:** check the environment's network allowlist covers the
  four API hosts — see "Running this in a cloud session" in `README.md`.

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

| Round | Direction | Seeds | Seeds w/o DOI | New candidates |
|---|---|---|---|---|
| — | — | — | — | — |

Stopping criterion (`SCOPE.md`): two consecutive rounds each yielding fewer
than 5 new in-scope candidates.

Also record what each round could not reach, from what `snowball.py` prints —
references deposited without a DOI, and how many citing works OpenCitations
knew about. A thin round is only a finding if the sources were not the limit.

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
  - Citation gate catches a planted fake DOI and a planted invented quote.
  - Library reset to empty for the real run.
- `2026-08-09` — sources are arXiv + Crossref + OpenCitations; all free and keyless.
  - Snowballing: Crossref reference lists backward, OpenCitations citations forward.
  - `enrich.py` now finds published DOIs by title, which is what snowballing needs.
  - Verified end to end on 15 arXiv hits: 6 DOIs resolved, 8 papers snowballed.
- `2026-08-10` — Phase 1 harvest. Network allowlist covers all four API hosts.
  - Grid pass: 51 queries, 1449 candidates after dedup and the topic gate.
  - `large language model AND program contract generation` returned 0 hits.
    - The arXiv phrase match is literal; shortened to `contract generation`.
  - `temporal logic specification` returned 1 hit; shortened to `temporal logic`.
  - Widening pass: 36 queries added for concepts the grid missed, 241 more.
    - Proof repair, fuzz driver generation, GUI and metamorphic testing.
    - Equivalence checking, translation validation, runtime verification.
    - Generic `program analysis` and `program verification` phrasings.
  - Both `SCOPE.md` seed papers resolved through `search_arxiv.py --query`.
    - `arxiv:2606.15122` needed `--no-topic-gate`; its abstract trips no
      category pattern, so the gate dropped it.
  - Library: 1692 candidates.
