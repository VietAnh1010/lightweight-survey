# RustAssure: Differential Symbolic Testing for LLM-Transpiled C-to-Rust Code

- **Citekey:** bai2025rustassure
- **Record:** arxiv:2510.07604
- **Authors:** Yubo Bai, Tapti Palit
- **Venue:** ASE 2025
- **Categories:** symbolic-execution, test-generation
- **Link:** http://arxiv.org/abs/2510.07604v1

## Problem

- C codebases must be transpiled to Rust before Rust's memory-safety guarantees apply.
- Model-transpiled code carries subtle semantic bugs that compile and pass existing tests.
- Unit and fuzz testing miss these because they sample inputs rather than reason over them.

## Main ideas

- RustAssure pairs generation with a check: transpile with an LLM, then test the pair differentially.
- Differential symbolic testing compares symbolic return values of the C and Rust functions.
- Symbolic comparison covers input classes, so equivalence is argued over ranges rather than samples.
- The check is per function, which keeps each symbolic query small enough to discharge.

## Evaluation

- Five real-world applications and libraries.
- 89.8% of C functions yield compilable Rust; 69.9% of those match on symbolic return values.
- Not measured: whether the 30% mismatch is a transpilation bug or a limit of the symbolic check.
- Return values only. Side effects, memory state, and panics are outside the compared relation.

## Limitations

- Ours: symbolic equivalence on return values is weaker than semantic equivalence.
- Ours: the 69.9% is conditioned on compiling, so the end-to-end rate is about 63% of all functions.
- Ours: prompt engineering does the transpiling, so that half fails the swap-the-model test.
- Authors: the abstract states no scalability bound for the symbolic engine.

## Follow-ups

- Extend the compared relation to heap state and observable side effects, not just return values.
- Feed each mismatch back as a repair signal rather than reporting it as a failure.
- Measure how far symbolic equivalence scales past function granularity.

## Evidence

> "because LLMs often generate code with subtle bugs that can be missed under traditional unit or fuzz testing, RustAssure performs differential symbolic testing to establish the semantic similarity between the original C and LLM-transpiled Rust code" — abstract
> "our system is able to generate compilable Rust functions for 89.8% of all C functions, of which 69.9% produced equivalent symbolic return values for both the C and Rust functions" — abstract
