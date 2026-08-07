# Scope contract

Re-read before every screening decision. A judgement call not settled here is
not settled — add it here rather than deciding ad hoc at 3am.

## Research question

**How are large language models being used in program analysis, verification,
and software testing, and what genuinely new techniques has that produced?**

## Inclusion criteria

A paper is **included** only if all four hold:

1. **Published 2020 or later.** Preprints count; use the first arXiv date.
2. **An LLM or pretrained code model is significant to the work** — not a
   mention, a baseline, or future work.
3. **The subject is program analysis, verification, or testing.** See the
   categories below.
   - General code generation counts only when it targets a test, proof,
     invariant, specification, or patch.
4. **It proposes a technique** — an idea, design, algorithm, or system with
   something non-obvious in it.

## Exclusion criteria

Exclude, and record which one applies in `reason`:

- **`wrapper`** — prompts an off-the-shelf LLM and reports results, no new technique.
  - Test: *swap the model for another one. Is any contribution left?* If no, exclude.
- **`benchmark-only`** — the contribution is a benchmark, leaderboard, or measurement.
  - Valuable, but not this survey. A benchmark *and* a technique is included
    on the technique.
- **`survey`** — exclude surveys and SLRs, but **read them and mine their references**.
  - They are the best snowball seeds available.
- **`out-of-scope`** — no LLM, or not about analysis/verification/testing.
- **`pre-2020`**.

### The judgement call

Criterion 4 requires thought, and it is where an unattended run will drift.
Signals that a paper clears the bar:

- a new algorithm, abstraction, or representation, not just a new prompt
- composed with something sound — solver, checker, fuzzer, abstract
  interpreter — with the interface discussed
- guarantees are discussed: soundness, completeness, or what is *not* guaranteed
- the technique repairs, constrains, validates, or iterates on LLM output

Signals it does not:

- the contribution is a prompt template or a choice of few-shot examples
- the evaluation is "GPT-4 scores X% on benchmark Y"
- the pipeline is: call model, parse output, done

When torn, include with `priority: 1` and note the doubt in `reason`.
Over-inclusion is recoverable at synthesis; an unscreened paper is invisible.

## Venues

Named committees, treated as a quality signal and tracked as `venue_tier:
target`:

**POPL, PLDI, OOPSLA, ICSE, FSE, ASE, CAV, FM**

Also relevant, tracked as `other`: ISSTA, TACAS, ITP, CPP, NDSS, IEEE S&P,
USENIX Security, CCS, and the ML venues (NeurIPS, ICML, ICLR).

arXiv-only preprints are **in scope** — much of this literature appears there
first — but where a paper has both a preprint and a published version, prefer
the published metadata.

## Categories

Assigned automatically by `scripts/topic.py` and overridable during screening.
A paper may hold several:

`static-analysis`, `fuzzing`, `symbolic-execution`, `formal-verification`,
`program-logic`, `specification`, `constraint-solving`, `test-generation`,
`program-repair`, `bug-detection`, `program-synthesis`, `decompilation`,
`proof-automation`, `agents`

## Comparison axes

Recorded per paper in `papers/notes/<citekey>.md`, and the columns of
`review/comparison-table.md`:

| Axis | What goes in it |
|---|---|
| **Problem** | The specific problem addressed, stated concretely enough to distinguish it from neighbouring papers |
| **Main ideas** | The technical core. What is actually new. Name the mechanism, not the outcome |
| **Evaluation** | Benchmarks, baselines, metrics, scale — and what was *not* measured |
| **Limitations** | Stated by the authors *and* observed by us; mark which is which |
| **Follow-ups** | What this opens up; gaps a next paper could take |

## Target

**40 included papers**, selected for coverage across categories rather than
citation count alone. Aim for every category above to have at least one
representative, and no single category to hold more than about a quarter of
the total.

## Stopping criteria

Stop harvesting when **two consecutive snowball rounds each yield fewer than 5
new in-scope candidates**, or when the time budget is spent. Record which one
ended the run in `STATUS.md`: only saturation justifies claims about coverage.

## Seed papers

Supplied by the user. Harvest these first — resolve each through
`scripts/search_arxiv.py --query "<title>"`, never by hand into the library —
then snowball from them in Phase 3 alongside the first screening pass.
`config/queries.txt` still drives the rest of the harvest.

- `arxiv:2606.15122` — *The Hitchhiker's Guide to Program Analysis, Part III:
  Mostly Harmless LLMs* (2026-06-13). Argues a plausible LLM rationale does not
  discharge a static-analysis warning; sits on criterion 4, the judgement call.
- `arxiv:2510.25015` — *VeriStruct: AI-assisted Automated Verification of
  Data-Structure Modules in Verus* (2025-10-28). LLM composed with a sound
  verifier, with a repair stage — the pattern the synthesis is built around.

<!-- Add as: - <citekey or DOI or arXiv id> — <one line on why it is a seed> -->
