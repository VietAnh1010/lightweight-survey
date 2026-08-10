# Specification-Guided Repair of Arithmetic Errors in Dafny Programs using LLMs

- **Citekey:** wu2025specification
- **Record:** arxiv:2507.03659
- **Authors:** Valentina Wu, Alexandra Mendes, Alexandre Abreu
- **Venue:** FM 2025
- **Categories:** program-repair, program-logic, formal-verification
- **Link:** http://arxiv.org/abs/2507.03659v3

## Problem

- When a program fails to verify, finding and fixing the fault is slow.
- Repair tools validate with test suites, which do not capture every scenario.
- A verification-aware language already carries stronger correctness criteria than any test suite.

## Main ideas

- The Dafny specification, not a test suite, is the oracle for both localization and repair.
- Pre-conditions, post-conditions, and invariants are assumed correct; the code is what is wrong.
- Hoare logic determines the state at each statement, which is how faults are localized.
- Localization is therefore deductive rather than statistical, unlike spectrum-based ranking.
- The model synthesizes candidate fixes at the located statement.
- Scope is narrowed to arithmetic bugs, which keeps the state reasoning tractable.

## Evaluation

- DafnyBench, a benchmark of real-world Dafny programs.
- Fault localization coverage 89.6%.
- Repair success 74.18% with GPT-4o mini, the best of four models tried.
- Four models compared: GPT-4o mini, Llama 3, Mistral 7B, Llemma 7B.

## Limitations

- Authors: correctness of the specifications is assumed, and the scope is arithmetic bugs.
- Ours: assuming the specification is right inverts the common case, where the specification is also new.
- Ours: arithmetic bugs are the subset where per-statement state reasoning stays cheap.
- Ours: a smaller model reaching 74.18% is not reported, so cost-quality trade-offs are unclear.

## Follow-ups

- Relax the assumption: decide from the counterexample whether the code or the specification is wrong.
- Extend past arithmetic to heap and aliasing bugs, where the state reasoning is harder.
- Compare Hoare-logic localization against spectrum-based localization on the same programs.

## Evidence

> "we present an APR tool for Dafny, a verification-aware programming language that uses formal specifications - including pre-conditions, post-conditions, and invariants - as oracles for fault localization and repair" — abstract
> "we localize faults through a series of steps, which include using Hoare logic to determine the state of each statement within the program, and applying Large Language Models (LLMs) to synthesize candidate fixes" — abstract
> "Our tool achieves 89.6% fault localization coverage and GPT-4o mini yields the highest repair success rate of 74.18%." — abstract
