# Defusing Logic Bombs in Symbolic Execution with LLM-Generated Ghost Code

- **Citekey:** bouras2026defusing
- **Record:** arxiv:2603.19239
- **Authors:** Dimitrios Stamatios Bouras, Sergey Mechtaev
- **Venue:** arXiv 2026
- **Categories:** symbolic-execution, constraint-solving
- **Link:** http://arxiv.org/abs/2603.19239v1

## Problem

- Symbolic execution stalls on solver-hostile fragments, hard arithmetic, and unbounded heaps.
- Replacing the solver with a model loses the global reasoning deep paths need.
- Real codebases require consistency across many interacting constraints at once.

## Main ideas

- Gordian keeps the SMT solver and uses the model to write ghost code that helps it.
- Ghost code is lightweight and inserted selectively, so the solver still does global reasoning.
- Type one inverts difficult fragments by iterative bidirectional constraint propagation.
- Type two replaces a fragment with a solver-friendly surrogate that preserves relevant behaviour.
- Type three partitions unbounded heap space semantically so it becomes finitely reasonable.
- Built on KLEE, so the baseline engine is unchanged.

## Evaluation

- Synthetic logic bombs, the FDLibM maths library, and libexpat, jq, and bc.
- Coverage up 52-84% over symbolic execution baselines.
- Coverage up 86-419% over LLM-as-solver techniques.
- Token usage down 90-96% against those same LLM-based techniques.

## Limitations

- Ours: ghost code is model-written and unverified, so a wrong surrogate misreports reachability.
- Ours: the abstract claims no soundness theorem for the surrogate or the heap partitioning.
- Ours: logic bombs are synthetic and built to isolate the challenges the method targets.
- Authors: the limits attacked are solver-hostile fragments, numerical reasoning, and unbounded heaps.

## Follow-ups

- State and check a soundness condition for surrogates, so coverage gains cannot hide false paths.
- Validate each surrogate by concrete execution, as NeuroSCA does for dropped constraints.
- Report how often ghost code is requested, which shows how selective the mechanism is.

## Evidence

> "We present Gordian, a hybrid symbolic execution framework that uses LLMs selectively to generate lightweight ghost code that aids an SMT solver in handling solver-hostile code fragments, while preserving its precise, global reasoning capability." — abstract
> "Gordian improves coverage on average by 52-84% over traditional symbolic execution baselines, and by 86-419% over LLM-based techniques, while reducing LLM token usage by an average of 90-96%" — abstract
> "Recent work proposed replacing constraint solvers with large language models (LLMs) to bypass these limitations, but such approaches struggle to analyze real-world codebases" — abstract
