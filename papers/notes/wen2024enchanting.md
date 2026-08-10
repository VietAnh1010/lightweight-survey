# Enchanting Program Specification Synthesis by Large Language Models using Static Analysis and Program Verification

- **Citekey:** wen2024enchanting
- **Record:** arxiv:2404.00762
- **Authors:** Cheng Wen, Jialun Cao, Jie Su, Zhiwu Xu et al.
- **Venue:** CAV 2024
- **Categories:** specification, program-logic, formal-verification, static-analysis
- **Link:** http://arxiv.org/abs/2404.00762v2

## Problem

- A full proof needs specifications, and writing them takes domain expertise and manpower.
- Existing synthesis is narrow: loop invariants for numerical programs, or one program family.
- Arrays, pointers, nested loops, and function calls fall outside those approaches.

## Main ideas

- AutoSpec is driven by static analysis and program verification, with the model as generator.
- Programs are decomposed so the model attends to one part at a time.
- Candidate specifications are validated every round, not once at the end.
- Per-round validation is what stops errors accumulating across a long interaction.
- The loop is incremental: each validated specification becomes context for the next.
- The target is satisfiable and adequate specifications, so both directions of failure are named.

## Evaluation

- 79% of programs verified through automatic specification synthesis.
- A 1.592x improvement over existing work.
- Applied to a real-world X509-parser project, not only to benchmarks.
- Not reported in the abstract: the benchmark size behind the 79%.

## Limitations

- Ours: adequacy is checked by whether the proof closes, which a weak specification can also achieve.
- Ours: no ablation separates decomposition from per-round validation.
- Ours: the abstract gives no runtime, and per-round validation implies repeated verifier calls.
- Authors: existing automated approaches are limited in versatility, which is the gap addressed.

## Follow-ups

- Separate the contributions of decomposition and per-round validation with an ablation.
- Measure specification adequacy independently, for example against mutants of the program.
- Compare against ConVer's CEGAR-CEGIS refinement on the same C programs.

## Evidence

> "AutoSpec addresses the practical challenges in three ways: (1) driving \\name by static analysis and program verification, LLMs serve as generators to generate candidate specifications, (2) programs are decomposed to direct the attention of LLMs, and (3) candidate specifications are validated in each round to avoid error accumulation during the interaction with LLMs." — abstract
> "it outperforms existing works by successfully verifying 79% of programs through automatic specification synthesis, a significant improvement of 1.592x" — abstract
> "It can also be successfully applied to verify the programs in a real-world X509-parser project." — abstract
