# ConCovUp: Effective Agent-Based Test Driver Generation for Concurrency Testing

- **Citekey:** cai2026concovup
- **Record:** arxiv:2605.09573
- **Authors:** Yuandao Cai, Shuhao Fu, Wensheng Tang, Cheng Wen et al.
- **Venue:** arXiv 2026
- **Categories:** test-generation, symbolic-execution, agents
- **Link:** http://arxiv.org/abs/2605.09573v1

## Problem

- Race detectors such as TSan report only what the test drivers exercise at runtime.
- Test generation research targets sequential logic, leaving concurrent drivers unautomated.
- Models write sequential tests well and lack the concurrency semantics for shared-memory interleavings.

## Main ideas

- ConCovUp grounds generation in static analysis that extracts shared memory accesses.
- Calling contexts are extracted alongside, so the target is a reachable access, not a line.
- Backward tracing runs from the target access to deduce inputs satisfying its path constraints.
- The model does the semantic deduction that a solver would find intractable at this scale.
- Dynamic execution feedback refines drivers that miss their target.

## Evaluation

- Nine real-world C and C++ libraries.
- Shared Memory Access Pair coverage rises from 36.6% to 68.1%.
- The baseline is a general Claude Code agent, which isolates what the grounding adds.
- SMAP coverage is the right metric here, since it measures what a race detector observes.

## Limitations

- Ours: coverage of access pairs is necessary for race detection, not sufficient for a race to surface.
- Ours: no count of races found is given in the abstract.
- Ours: backward tracing is model-driven, so satisfying constraints is not guaranteed.
- Authors: models struggle with concurrency semantics, which is why the analysis grounds them.

## Follow-ups

- Report races TSan reports under the generated drivers, not only access-pair coverage.
- Compare backward tracing against a solver on the same path constraints where both apply.
- Extend the target set from shared accesses to lock-order pairs, which catch deadlocks.

## Evidence

> "ConCovUp grounds test generation in static analysis to extract shared memory accesses and their calling contexts." — abstract
> "it introduces an LLM-driven backward tracing approach, leveraging the model's semantic reasoning to deduce concrete inputs that satisfy complex path constraints, and iteratively refines the generated tests via dynamic execution feedback" — abstract
> "ConCovUp improves average Shared Memory Access Pair Coverage (SMAP Coverage) from 36.6% to 68.1% over the general Claude Code agent baseline" — abstract
