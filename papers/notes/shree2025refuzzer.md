# ReFuzzer: Feedback-Driven Approach to Enhance Validity of LLM-Generated Test Programs

- **Citekey:** shree2025refuzzer
- **Record:** doi:10.1109/ase63991.2025.00364
- **Authors:** Iti Shree, Karine Even-Mendoza, Tomasz Radzik
- **Venue:** ASE 2025
- **Categories:** fuzzing, test-generation
- **Link:** https://doi.org/10.1109/ase63991.2025.00364

## Problem

- Model-generated compiler test programs are often syntactically or semantically invalid.
- An invalid program never reaches the optimizer or backend the fuzzer wants to exercise.
- Crash detection alone misses the coverage those stages would have provided.

## Main ideas

- ReFuzzer refines generated programs instead of discarding them.
- It detects and corrects compilation and runtime violations such as division by zero.
- A local model runs the feedback loop, so refinement is cheap enough to apply to every program.
- Validation and filtering happen before execution, not after a crash.
- The goal is diverse yet valid programs, so refinement must not collapse variety.

## Evaluation

- Black-box, grey-box, and white-box fuzzing against LLVM and Clang.
- Validity rises from 47.0-49.4% to 96.6-97.3%.
- Processing costs 2.9-3.5 seconds per program on a dual-GPU machine.
- Vectorization coverage gains 9.2, 2.3, and 7.1 absolute points across the three modes.

## Limitations

- Ours: no bug counts are reported, so validity gains are not tied to findings.
- Ours: refinement could reduce diversity, and no diversity measure is given.
- Ours: 3 seconds per program is a real cost against a fuzzer's throughput budget.
- Authors: invalid programs limit effectiveness in exercising optimizations and backends.

## Follow-ups

- Report bugs found per CPU-hour, which is what a fuzzer is ultimately judged on.
- Measure input diversity before and after refinement.
- Compare refinement against structural masking, which prevents invalidity rather than repairing it.

## Evidence

> "We introduce ReFuzzer, a framework for refining LLM-generated test programs by systematically detecting and correcting compilation and runtime violations (e.g. division by zero or array out-of-bounds accesses)." — abstract
> "ReFuzzer improved test programs' validity from 47.0-49.4% to 96.6-97.3%, with an average processing time of 2.9-3.5 s per test program on a dual-GPU machine." — abstract
> "vectorization coverage had an absolute improvement of 9.2%, 2.3%, and 7.1% in black-, grey-, and white-box fuzzing" — abstract
