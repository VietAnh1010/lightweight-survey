# Status

Live run state. **Update after every batch, then commit.** If the session
dies, this file plus the git log is the entire handoff.

---

## Current

- **Phase:** 5 — notes. Phases 1-4 complete, 40 papers selected
- **Last updated:** 2026-08-10
- **Next action:** fill `papers/notes/*.md`, then synthesis and the two gates

## Counts

| | |
|---|---|
| candidates seen | 1943 |
| screened | 255 |
| included | 40 |
| excluded | 133 |
| unavailable | 82 |
| never reached | 1688 |

_Refresh with `python3 scripts/screen.py stats`._

The 133 excluded include 47 demoted in Phase 4 for balance, not on merit.
The 1688 never reached are the tail of the harvest: uncited 2026 preprints
ordered alphabetically once the venue and citation keys tie.

## Coverage by category

40 included papers. Every category in `SCOPE.md` has a representative.

| Category | Papers |
|---|---|
| formal-verification | 12 |
| program-repair | 10 |
| bug-detection | 10 |
| agents | 8 |
| specification | 8 |
| static-analysis | 8 |
| proof-automation | 6 |
| program-logic | 5 |
| program-synthesis | 5 |
| fuzzing | 5 |
| test-generation | 5 |
| decompilation | 3 |
| symbolic-execution | 3 |
| constraint-solving | 3 |

Papers carry several categories, so the column sums past 40. `formal-verification`
holds 12 of 40, above the one-quarter guideline in `SCOPE.md`. Two verification
papers were cut for this and it did not fall further: the tag attaches to any
paper composing a model with a sound checker, which is the survey's subject.

## Snowball rounds

| Round | Direction | Seeds | Seeds w/o DOI | New candidates |
|---|---|---|---|---|
| 1 | backward | 67 | 4 | 45 |
| 1 | forward | 67 | 4 | 179 |
| 2 | backward | 76 | 4 | 2 |
| 2 | forward | 76 | 4 | 25 |

What the rounds could not reach:

- Round 1 backward: 1538 references were deposited without a DOI, so unresolvable.
- Round 2 backward: 1781 such references; 1291 of 1339 unseen DOIs resolved.
- One seed, `ahmed2026specops`, returns HTTP 404 at Crossref for its own DOI.
- Forward reach is OpenCitations coverage only, and it caps at 50 per seed.
  - Six seeds hit that cap, so their citing sets are truncated, not exhausted.

**The run ended on the time budget, not on saturation.** Round 2 yielded 27 new
candidates, above the fewer-than-5 threshold in `SCOPE.md`. No claim of
saturation is supported. Round 1 to round 2 fell from 224 to 27, which is
consistent with approaching saturation but does not establish it.

## Open questions

Things to raise with the user rather than block on. Record and keep going.

- Two seed papers supplied (`SCOPE.md` § Seed papers), `2026-08-08`.
  - Both resolved through `search_arxiv.py --query "<title>"`, `2026-08-10`.
  - `arxiv:2606.15122` was screened out; see the table below.
- Does criterion 2 cover pre-LLM neural models trained for one task?
  - Read strictly here: Recoder and RewardRepair were excluded on it.
  - Both are cited constantly by the included repair papers.
- Does criterion 3 cover artefacts that are not programs?
  - Read strictly: agent plans, ATL strategies, and a maths conjecture were cut.
  - Kept: analysis of LLM agent programs, where the artefact is still code.
- `topic.py` drops papers whose abstract trips no category pattern.
  - Seed `arxiv:2606.15122` needed `--no-topic-gate` to enter the library.
  - Unknown how many other in-scope papers the gate silently dropped.

## Decisions made under uncertainty

Judgement calls worth a second look in the morning. Borderline
include/exclude calls, category assignments, papers cut for balance.

| Paper | Call | Why |
|---|---|---|
| Both seed papers | screened last, by hand | Neither reached a batch on its own. Both sit in tiers the ranking reaches late, so the venue-first order buried the two papers the scope named first. Caught and corrected before Phase 5 |
| `arxiv:2606.15122` (seed, Hitchhiker's Guide III) | included, priority 3 | `SCOPE.md` flags it as sitting on criterion 4. It clears the bar: Evident is a system, not only an argument, and the harness-construction split is the technique |
| `arxiv:2510.25015` (seed, VeriStruct) | included, priority 3 | The pattern the synthesis is built around, per `SCOPE.md` |
| PAT-Agent, LLMAO | cut for balance | Displaced by the two seeds. Both would otherwise have stayed |
| Recoder, RewardRepair | excluded | Criterion 2 read strictly: task-specific neural models, not LLMs or pretrained code models. Both are foundational to the included repair papers |
| Plan verification, ATL strategy synthesis, a Lean maths proof | excluded | Criterion 3 read strictly: the verified artefact must be a program. All three compose an LLM with a sound checker, so they fit the architecture but not the scope |
| `arxiv:2604.11767` (typed calculus for agents) | included, then cut | Included because it analyses agent programs; cut in Phase 4 because the analysed artefact is a configuration, not a program under test |
| HFuzzer, ABLE | included at priority 1, then cut | Both test or analyse a model rather than a program. Recorded rather than resolved |
| 47 papers | demoted in Phase 4 | Cut for balance, not on merit. Every one carries a `reason` naming what it duplicates |

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
