# Status

Live run state. **Update after every batch, then commit.** If the session
dies, this file plus the git log is the entire handoff.

---

## Current

- **Phase:** complete. All seven phases done, both gates clean
- **Last updated:** 2026-08-10
- **Next action:** none required. See "Closing summary" for what another session would do

Both gates pass:

- `style_check.py`: 41 files, 0 errors, 0 warnings.
- `verify_citations.py --all`: 40 papers, every DOI and arXiv id re-resolved live.
  - 0 errors, 2 warnings, both explained under "Closing summary".

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
  - `enrich.py`: 514 published DOIs matched by title, 0 records without an abstract.
- `2026-08-10` — Phase 2 screening, 7 batches of 25, target-venue tier first.
  - Batches 1-5 exhausted all 109 target-venue candidates: 67 included.
  - Batch 6 screened the snowballed pool, which carried the well-cited older work.
  - Batch 7 was targeted at `program-logic` and `decompilation`, the two thin categories.
  - 82 records had no abstract after two enrichment passes; all marked `unavailable`.
- `2026-08-10` — Phase 3 snowballing, two rounds. Numbers in the table above.
- `2026-08-10` — Phase 4 selection. 87 included cut to 40 for category balance.
  - Every demotion carries a `reason` naming the paper it duplicates.
  - Both seed papers were still unscreened at this point; caught and screened by hand.
- `2026-08-10` — Phase 5, 40 notes written in four batches of 10.
- `2026-08-10` — Phases 6 and 7. Synthesis written, both gates clean.

## Closing summary

**Counts.** 1943 candidates seen, 255 screened, 40 included, 133 excluded, 82
unavailable, 1688 never reached.

**Which stopping criterion ended the run: the time budget.** Snowball round 2
yielded 27 new candidates, well above the fewer-than-5 threshold in `SCOPE.md`.
No claim of saturation is supported by this run. The fall from 224 new
candidates in round 1 to 27 in round 2 is consistent with approaching
saturation and does not establish it.

**Categories that came out thin, and whether that is the literature or the run.**

- `decompilation`, `symbolic-execution`, and `constraint-solving` hold 3 each.
- For all three this is the run, not the literature.
  - A targeted pass on `decompilation` found 11 more includable papers in one batch.
  - Six were cut in Phase 4 for balance, not for want of candidates.
- `formal-verification` holds 12 of 40, above the one-quarter guideline.
  - Two verification papers were cut for this and the count did not fall further.
  - The tag attaches to any paper composing a model with a sound checker.
- No category is empty, so no claim that the literature is empty anywhere is needed.

**The two citation-gate warnings.** Both are the arXiv-date against
published-year gap, which `SCOPE.md` resolves in favour of the first arXiv date.

- `wang2024perfgen`: stored 2024, Crossref says 2026 (FSE Companion).
- `wang2023boosting`: stored 2023, Crossref says 2025 (ICSE).
- Neither affects inclusion; both papers are post-2020 on either reading.

**What I was unsure about, and the calls I made.**

- Criterion 2 against pre-LLM neural models: read strictly.
  - Recoder and RewardRepair were excluded as task-specific neural models.
  - Both are cited throughout the included repair papers.
  - A reader may reasonably want them back.
- Criterion 3 against artefacts that are not programs: read strictly.
  - Plan verification, ATL strategy synthesis, and a Lean maths proof were cut.
  - All three compose a model with a sound checker.
  - They fit the architecture the synthesis describes, but not the scope.
- Papers whose contribution is what goes in the prompt: read as `wrapper`.
  - This cut the fact-selection and layered-context repair papers.
  - Both carry findings worth reading; neither proposes a technique.
- 47 papers were demoted in Phase 4 on balance rather than on merit.
  - The excluded set is part of the result, and every entry carries its reason.

**What another eight hours would buy.**

1. Screen the 1688 untouched candidates, or at least re-rank them.
   - The queue collapsed to alphabetical order once venue and citations tied.
   - The tail was therefore ordered by title rather than by promise.
2. Fix that ranking: `rank_key` needs a fourth key for the `unknown` tier.
   - Recency alone leaves the 2026 preprints unordered against each other.
3. Run snowball rounds 3 and 4 from the final 40, and test saturation properly.
   - Round 2 expanded seeds round 1 had already expanded.
   - Its low yield is partly an artefact of not re-screening between rounds.
4. Read the excluded surveys and mine their reference lists.
   - Phase 3 prescribes this. Six surveys were excluded and none were mined.
5. Fetch full text for the notes that flag an unreported number.
   - Replace "not measured in the abstract" with what the paper measured.
6. Re-screen the 82 `unavailable` records by fetching their landing pages.
