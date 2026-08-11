# Neurosymbolic Auditing of Natural-Language Software Requirements

- **Citekey:** hall2026neurosymbolic
- **Record:** arxiv:2605.13817
- **Authors:** Bethel Hall, William Eiers
- **Venue:** arXiv 2026
- **Categories:** specification, formal-verification, constraint-solving
- **Link:** http://arxiv.org/abs/2605.13817v1

## Problem

- Natural-language requirements are ambiguous, inconsistent, and underspecified.
- In safety-critical domains those defects propagate into formal models that verify the wrong thing.
- Nothing flags an ambiguous requirement before it is formalised once and trusted.

## Main ideas

- VERIMED formalises each requirement several times independently, not once.
- Stochastic variation across those formalisations is treated as the ambiguity signal.
- Bidirectional SMT equivalence checking turns that disagreement into a solver-checkable test.
- Solver queries then expose inconsistency, vacuousness, and safety violations in the specification.
- Counterexample granularity matters: concrete SMT counterexamples drive repair, not summaries.

## Evaluation

- Open-source hemodialysis safety requirements for medical-device software.
- Counterexample-guided repair raises verified accuracy from 55.4% to 98.5%.
- Ambiguity-sensitive requirements are reduced across the evaluation.
- The two findings are separable: ambiguity detection and repair granularity are measured apart.

## Limitations

- Ours: agreement across formalisations detects disagreement, not a shared misreading.
- Ours: one domain, medical-device requirements, so transfer is untested.
- Ours: the 98.5% is on a question-answering benchmark, not on the requirements themselves.
- Authors: requirement defects propagate into implementations, which the audit reduces rather than removes.

## Follow-ups

- Report how many independent formalisations are needed before agreement stops being informative.
- Apply the ambiguity test to code contracts, where an executable oracle also exists.
- Measure whether flagged requirements correlate with defects found later in implementation.

## Evidence

> "stochastic variation across independent formalizations is a signal of ambiguity: requirements that admit multiple plausible interpretations produce SMT-inequivalent formalizations, and bidirectional SMT equivalence checking turns this disagreement into a solver-checkable test" — abstract
> "in counterexample-guided repair on a hemodialysis question-answering benchmark, concrete SMT counterexamples raise verified accuracy from 55.4% to 98.5%" — abstract
> "the usefulness of symbolic feedback depends on its granularity" — abstract
