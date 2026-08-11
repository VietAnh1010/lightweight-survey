# Neuro-Symbolic Generation and Validation of Memory-Aware Formal Function Specifications

- **Citekey:** zhang2026neuro
- **Record:** arxiv:2603.13414
- **Authors:** Liao Zhang, Tong Chen, Xiwei Wu, Qi Liu et al.
- **Venue:** arXiv 2026
- **Categories:** specification, formal-verification, program-logic
- **Link:** http://arxiv.org/abs/2603.13414v1

## Problem

- Verifying memory-manipulating programs needs precise specifications capturing memory state.
- Models now write low-level systems code whose correctness cannot be assumed.
- An LLM judging whether a specification is right accepts plausible-but-wrong ones.

## Main ideas

- The scope is deliberately narrowed to function specifications, excluding loop invariants.
- Candidates come from in-context learning over the description and the function signature.
- Compiler diagnostics from symbolic provers drive iterative refinement of syntax.
- Validation runs in the opposite direction: a proof is constructed for the specification's negation.
- Concrete examples make that refutation machine-checkable rather than a judgement.
- Refuting is decidable where confirming is not, which is why the direction is inverted.

## Evaluation

- LeetCode-C-Spec, a new benchmark of 200 C programming problems.
- Iterative refinement substantially improves syntactic validity.
- Prover-based refutation improves correctness assessment by filtering false positives.
- The comparison point is an LLM-only judge, which accepts those false positives.

## Limitations

- Ours: refutation catches wrong specifications, not weak ones that are true but vacuous.
- Ours: no absolute correctness rate appears in the abstract.
- Ours: LeetCode-derived problems are self-contained, unlike systems code the paper motivates with.
- Authors: loop invariants are deliberately excluded, so the hardest part of the pipeline remains.

## Follow-ups

- Add a vacuity check, since refutation alone permits trivially satisfiable specifications.
- Extend to loop invariants and report how far the refutation idea carries.
- Compare refutation against counterexample-driven repair, which uses the same prover differently.

## Evidence

> "we validate candidate specifications by constructing a proof for the negation of the specification with concrete examples, enabling machine-checked rejection of plausible-but-incorrect specifications" — abstract
> "we focus exclusively on function specification generation, deliberately avoiding the synthesis of complex loop invariants that are central to traditional verification pipelines" — abstract
> "symbolic prover-based refutation significantly enhances correctness assessment by filtering false positives that LLM-only judges frequently accept" — abstract
