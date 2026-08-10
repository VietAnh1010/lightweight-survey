# Mizzle: A Complete Concurrent Incorrectness Logic for Preventing False Alarms in Agentic Bug Finding

- **Citekey:** moine2026mizzle
- **Record:** arxiv:2607.11611
- **Authors:** Alexandre Moine, Sam Westrick, Joseph Tassarotti
- **Venue:** arXiv 2026
- **Categories:** program-logic, formal-verification, bug-detection
- **Link:** http://arxiv.org/abs/2607.11611v1

## Problem

- Models find real bugs in real programs and also emit a flood of false alarms.
- A false alarm costs developer time, so precision matters more than raw detection count.
- Filtering alarms with another model moves the problem rather than deciding it.

## Main ideas

- Mizzle requires each bug report to carry a machine-checked proof that the bug is real.
- Incorrectness logic is the right frame: under-approximate reasoning shows a behaviour is reachable.
- The logic must model a realistic language, be mechanized, and be complete, or it rejects real bugs.
- Mizzle is an incorrectness separation logic for concurrent programs in a substantial OCaml subset.
- It is parametric in the notion of incorrectness, so one logic serves several bug classes.
- Mechanized in Rocq on top of Iris, with soundness and completeness both proved.

## Evaluation

- Three instantiations: stuckness, non-linearizability of a data structure, and the presence of a race.
- Soundness proved: the logic never justifies a false alarm.
- Completeness proved: every incorrect execution admits a derivation.
- The model-facing part is a proof of concept only, not a measured bug-finding evaluation.

## Limitations

- Authors: the LLM use is illustrated as a proof of concept rather than evaluated.
- Ours: no measurement of how often a model produces a Mizzle derivation that checks.
- Ours: the language is a substantial OCaml subset, so C and Java bug reports are out of reach.
- Ours: completeness guarantees a derivation exists, not that any prover or model will find it.

## Follow-ups

- Measure the rate at which a model produces checkable derivations for real reported bugs.
- Instantiate the logic for a memory-unsafe language, where LLM bug finding is most used.
- Compare proof-carrying bug reports against LLM-judge filtering on the same alarm stream.

## Evidence

> "We propose a method to prevent these false alarms by requiring an LLM to accompany each bug report with a machine-checked proof, in a program logic, that the reported bug is real." — abstract
> "we prove that it is both sound (that is, it never justifies a false alarm) and complete (that is, every incorrect execution admits a derivation)" — abstract
> "As a proof of concept, we illustrate how an LLM can use Mizzle in order to certify the existence of a bug." — abstract
