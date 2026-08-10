# Synthesis

LLMs in program analysis, verification, and software testing, 2022-2026.

40 included papers from 1943 candidates seen and 255 screened. Counts here come
from `scripts/screen.py stats`; every claim about a paper traces to its note in
`papers/notes/`.

The run ended on its time budget, not on saturation. See `STATUS.md`.

---

## 1. What the field is doing

The organizing question is where the model sits relative to a sound component.
Six positions recur, and they are architectures, not prompts.

**In front of it — proposer checked by a verifier.** The most common shape.

- `sun2025veristruct` plans a module's abstractions and invariants; Verus alone decides.
- `liu2024propertygpt` generates contract properties; a dedicated prover verifies them.
- `sun2023gptscan` matches vulnerability scenarios; static confirmation validates the variables.
- `wen2024enchanting` validates every candidate specification each round, not once at the end.
- The check is what makes the composition safe to run unattended.

**Behind it — filter on the analyser's output.**

- `cheng2024semantic` removes indirect-call targets a static analyser over-approximated.
- `li2026hitchhiker` discharges warnings only when a backend proves the error state unreachable.
- Both invert the usual flow: the sound tool speaks first, the model narrows.

**Inside it — heuristic in a search.**

- `li2024guiding` puts model calls in a weighted probabilistic enumerative search over SyGuS grammars.
- The enumerator reports progress and the model returns syntactic guidance, so information flows both ways.
- `lyu2024prompt` makes the prompt itself the search state, mutated by coverage feedback.
- `xia2023fuzz4all` rewrites its own prompt each round instead of carrying a seed corpus.

**Around it — agent driving the sound tool.**

- `levin2024chatdbg` gives the model control of LLDB, GDB, and Pdb, so claims rest on observed state.
- `bouzenia2024repairagent` bounds tool choice with a finite state machine over repair-specific tools.
- `zhang2026feedback` replaces one-pass analysis with a reasoning-action-observation loop over binaries.
- `kan2026harnessing` hands a whole lemma to a general code agent inside a soundness-enforcing harness.

**Compiled into it — the model runs offline and leaves a symbolic artifact.**

- `fang2026learning` mines reusable Ltac tactics from a proof corpus and installs them in symbolic provers.
- `sheng2025solsearch` has the model rewrite SAT solver code, improving Z3's PAR-2 by 11%.
- Both pay for the model once; proving and solving afterwards cost no model calls.
- This is the only position where the model's cost does not scale with usage.

**Constraining generation instead of filtering it.**

- `wei2023copiloting` prunes infeasible tokens during decoding with a completion engine.
- `gao2025clozemaster` masks structures inside programs that already crashed rustc, generating only inside.
- Validity becomes a property of the generation process rather than a post-hoc test.

**Translating between informal and formal.**

- `cosler2023nl2spec` maps each subformula back to its natural-language fragment, so ambiguity is editable.
- `an2025neurosymbolic` formalizes redundantly and checks the results for semantic equivalence.
- `jia2025automated` inverts the target and repairs the description rather than the program.
- `ruan2024specrover` infers intent from project structure and behaviour, then vets patches against it.

---

## 2. Cross-cutting comparison

Reading down the comparison table, the same problem attracts incompatible designs.

**Coq proof automation is the sharpest disagreement in the set.**

- `thompson2024rango` retrieves premises and similar proofs at every step, adapting to the proof state.
- `lu2024proof` generates a whole proof, then repairs low-level details with targeted symbolic methods.
- `kan2026harnessing` argues both are limited by imposing a human-designed strategy at all.
- Its evidence is coverage: all 4,257 Iris core lemmas proved automatically.
- On reglang it proves all 318, where prior provers manage barely one in eight.
- `fang2026learning` rejects the premise differently: extract tactics offline, then do not run a model.

**Fuzzing splits on whether to constrain generation.**

- `xia2023fuzz4all` writes no grammar and targets six languages with one fuzzer.
- `gao2025clozemaster` keeps a bug-triggering scaffold and generates only inside masked brackets.
- The trade is breadth against validity, and neither paper measures the other's metric.

**Specification synthesis splits on what refutes a candidate.**

- `ayon2026specpylot` refutes with a concrete counterexample from symbolic execution.
- `pirzada2026conver` refines contracts through CEGAR-CEGIS with ICE learning when a check fails.
- `wen2024enchanting` validates each round to stop errors accumulating across the interaction.
- `sun2025veristruct` repairs annotation errors, so syntax failure does not end the run.

**Bug reporting splits on how much proof a model owes.**

- `li2026hitchhiker` requires a validated harness and a backend reachability check before discharging.
- `moine2026mizzle` requires a machine-checked derivation in a sound and complete incorrectness logic.
- `cambronero2026abstain` requires neither and uses a second model to reject unpromising patches.
- The three answers span mechanical proof, mechanical check, and model judgement.

**Repair splits on what serves as the oracle.**

- `wu2025specification` uses Dafny pre- and postconditions, and localizes faults with Hoare logic.
- `jin2023inferfix` uses the Infer static analyzer for detection and bug-type conditioning.
- `yang2024revisiting` uses model entropy, so patches are ranked before any test runs.
- `bouzenia2024repairagent` and `ruan2024specrover` use the project's own test suite.

---

## 3. Evaluation practice

**Recurring benchmarks.**

- Defects4J appears in `wei2023copiloting`, `bouzenia2024repairagent`, `kang2022large`, `yang2024revisiting`.
- SWE-Bench in `ruan2024specrover`; DafnyBench in `wu2025specification`; CoqStoq in `thompson2024rango`.
- SyGuS in `li2024guiding`; Quixbugs in `li2023nuances`; HumanEval+ and MBPP+ in `jia2025automated`.

**Contamination is addressed by three papers out of 40.**

- `kang2022large` re-runs on 31 bug reports filed after the training data cutoff, and holds 32%.
- `jia2025automated` includes LiveCodeBench alongside the older benchmarks.
- `yang2024revisiting` avoids model output entirely, using entropy, which it states removes the leakage concern.
- Defects4J predates every model in this set, and the other papers using it do not discuss leakage.

**What counts as correct varies by an order of magnitude in strength.**

- Machine-checked: `sun2025veristruct` (Verus), `kan2026harnessing` (Coq kernel).
- Also machine-checked: `moine2026mizzle` (Rocq), `pirzada2026conver` (bounded model checking).
- Test-suite passing: the Defects4J and SWE-Bench papers, which admits patches that overfit the suite.
- Author judgement: `levin2024chatdbg` counts an actionable fix, scored by the authors.

**External oracles appear where the field is strongest.**

- `liu2024propertygpt` reports 12 zero-days and $8,256 in bug bounties.
- `chu2025palm` submitted 91 tests upstream: 80 accepted, 5 rejected, 6 pending.
- `lyu2024prompt` reports 30 of 33 bugs confirmed by the projects' own communities.
- `zhang2025your`, `gao2025clozemaster`, and `wang2023boosting` report developer-confirmed fixes.
- These are the hardest numbers in the survey, and they cost the authors real engagement.

**Cost is reported by three papers.**

- `bouzenia2024repairagent`: about 270,000 tokens and 14 US cents per bug.
- `ruan2024specrover`: $0.65 per SWE-Bench lite issue.
- `sun2023gptscan`: 14.39 seconds and 0.01 USD per thousand lines of Solidity.
- Without a budget, a composition that beats a cheaper baseline cannot be distinguished from one that buys the win.

**Baseline discipline is uneven, and one paper sets the standard.**

- `li2024guiding` reports the model alone, the enumerator alone, and the winning competition tool.
- That triple is what makes a composition claim checkable; most papers report one baseline.

---

## 4. Limitations, aggregated

These recur across papers, so they are the field's open problems rather than one author's.

**Nobody measures specification strength.**

- `sun2025veristruct` verifies 128 of 129 functions against specifications it generated itself.
- `wen2024enchanting`, `ayon2026specpylot`, and `liu2024propertygpt` share the shape.
- A weak invariant that verifies scores the same as a strong one, and no paper here separates them.

**Soundness claims are relative to a generated artifact.**

- `li2026hitchhiker` is sound relative to a harness the model wrote; a wrong assumption discharges wrongly.
- `cheng2024semantic` filters an over-approximate target set, so removing a real edge breaks soundness downstream.
- Only `moine2026mizzle` makes the guarantee unconditional, by proving its logic sound and complete.

**Precision is the binding constraint in detection.**

- `zhang2026feedback` reports 72.3% precision over 1,274 vulnerabilities.
- `sun2023gptscan` reports 57.14% precision on large projects, against over 90% on token contracts.
- `wang2023boosting` reports false alarm rates near 19% on both datasets.
- Every one of these still needs human triage on a substantial fraction of reports.

**Percentages rest on small evaluations.**

- `sun2025veristruct`: eleven modules. `wang2024perfgen`: four case studies.
- `pirzada2026conver`: 6 programs on X.509, 11 on VerifyThis, 17 on LF2C-Simple.
- `kang2022large`'s contamination check, the best in the set, uses 31 reports.

**Results depend on the model and the papers rarely quantify it.**

- `pirzada2026conver` reports 82-96% across three backends, which is a 14-point spread from the model alone.
- `ayon2026specpylot` names differences in LLM behaviour as a limit on reproducibility.
- `lu2024proof` and `peng2023generative` test across models; most papers report one.

---

## 5. Follow-ups

Concrete gaps, each with a reason it is feasible now.

**Measure specification strength by mutation.**

- Mutate the program, then count how many generated specifications break.
- Mutation tooling is mature and the verifier is already in the loop for `sun2025veristruct` and `wen2024enchanting`.
- This turns "the proof closed" into a graded score, which no paper in this set reports.

**Apply redundant generation where a single artifact is currently trusted.**

- `an2025neurosymbolic` cross-checks redundant formalizations for semantic equivalence.
- `li2023nuances` trusts one synthesized reference program as its differential oracle.
- `li2026hitchhiker` trusts one generated harness. Both could require agreement across several.

**Extend offline compilation past tactics and SAT heuristics.**

- `fang2026learning` mines Ltac tactics; `sheng2025solsearch` rewrites solver code.
- Nobody has mined widening heuristics for abstract interpretation or summaries for alias analysis.
- Those heuristics are hand-tuned, corpora of analysis runs exist, and the artifact stays symbolic.

**Measure whether models can produce checkable incorrectness derivations.**

- `moine2026mizzle` proves the logic sound and complete, and demonstrates model use as a proof of concept.
- The missing number is the rate at which a model produces a derivation the Rocq mechanization accepts.
- Without it, proof-carrying bug reports remain a design rather than a result.

**Constrain decoding with a proof obligation, not only with syntax.**

- `wei2023copiloting` prunes tokens a completion engine rules out.
- No paper here prunes tokens a verifier's obligation rules out, though `sun2025veristruct` runs a verifier each round.
- Verus and Dafny check fast enough to sit inside a decoding loop for short annotations.

**Report cost-normalized comparisons.**

- `li2024guiding` shows how to argue a composition against both of its components.
- No paper here fixes a token or wall-clock budget across the compared systems.
- Until it does, "the composition wins" and "the composition spent more" are indistinguishable.

**Screen the tail this run never reached.**

- 1688 candidates were never screened; 82 had no abstract and were marked unavailable.
- Round 2 of snowballing still yielded 27 new candidates, so the citation graph is not exhausted.
