# Clozemaster: Fuzzing Rust Compiler by Harnessing Llms for Infilling Masked Real Programs

- **Citekey:** gao2025clozemaster
- **Record:** doi:10.1109/icse55347.2025.00175
- **Authors:** Hongyan Gao, Yibiao Yang, Maolin Sun, Jiangchang Wu et al.
- **Venue:** ICSE 2025
- **Categories:** fuzzing, bug-detection
- **Link:** https://doi.org/10.1109/icse55347.2025.00175

## Problem

- Rust's syntax and borrow rules make most freely generated test programs invalid.
- An invalid program never reaches the compiler stages a fuzzer wants to exercise.
- Programs that historically triggered compiler bugs are known to be productive seeds.

## Main ideas

- clozeMask extracts test code from historical rustc issue reports rather than generating from nothing.
- It identifies bracket-delimited code snippets with specific structures and masks them.
- The model infills the masked regions, so the surrounding bug-triggering scaffold survives intact.
- Masking at bracket boundaries keeps the infill syntactically self-contained.
- Generation is constrained by structure, which is why validity does not collapse as in free generation.

## Evaluation

- 27 confirmed bugs in rustc and mrustc; 10 fixed by developers.
- Outperforms existing fuzzers on code coverage and effectiveness.
- Confirmed-and-fixed bug counts are a stronger signal than coverage, and both are reported.
- Not measured: how many masked programs remain valid, the quantity the design targets.

## Limitations

- Ours: seeding from historical issues biases the search toward already-explored compiler regions.
- Ours: no validity rate is reported, so the mechanism's stated benefit is not directly measured.
- Ours: the approach needs a public issue tracker with reproducer programs.
- Authors: directly using LLMs to generate Rust programs yields many invalid test cases.

## Follow-ups

- Report the validity rate before and after masking, which isolates what the structure buys.
- Mask at other structural boundaries, for example trait bounds or lifetimes, and compare yields.
- Test the method on a compiler with no public reproducer corpus to measure the seed dependency.

## Evidence

> "The clozeMask strategy involves extracting test code from historical issue reports, identifying and masking code snippets with specific structures, and using an LLM to fill in the masked portions for synthesizing new test programs." — abstract
> "This approach harnesses the generative capabilities of LLMs while retaining the ability to trigger Rust compiler bugs." — abstract
> "CLOZEMASTER has identified 27 confirmed bugs for rustc and mrustc, of which 10 have been fixed by developers." — abstract
