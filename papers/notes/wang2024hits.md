# HITS: High-coverage LLM-based Unit Test Generation via Method Slicing

- **Citekey:** wang2024hits
- **Record:** arxiv:2408.11324
- **Authors:** Zejun Wang, Kaibo Liu, Ge Li, Zhi Jin
- **Venue:** ASE 2024
- **Categories:** test-generation
- **Link:** http://arxiv.org/abs/2408.11324v1

## Problem

- Models write acceptable unit tests until the focal method gets complex.
- Complex methods hold many conditions and loops, needing varied inputs to cover branches.
- Existing methods hand the whole method to the model with no input analysis.

## Main ideas

- HITS decomposes the focal method into slices before asking for tests.
- Tests are generated slice by slice rather than for the method as a whole.
- Slicing shrinks the analysis scope the model must reason about at once.
- A smaller scope is what makes the input needed for each branch inferable.
- A dataset of complex focal methods is built from projects prior work used.

## Evaluation

- Complex focal methods collected from the projects used by state-of-the-art approaches.
- Beats current model-based test generation on line and branch coverage.
- Also beats Evosuite, the standard search-based baseline.
- Not measured: whether the sliced tests detect faults, only whether they cover code.

## Limitations

- Ours: coverage is the only reported quality metric, with no mutation score.
- Ours: slice-by-slice generation can produce tests that never exercise slices together.
- Ours: slicing cost is not reported, and complex methods are where slicing is most expensive.
- Authors: existing methods give the model no assistance on input analysis.

## Follow-ups

- Report mutation score, since slicing could raise coverage while weakening assertions.
- Measure whether cross-slice interactions are missed by the per-slice tests.
- Compare slicing against path-constraint extraction, which decomposes the same problem differently.

## Evidence

> "we propose decomposing the focal methods into slices and asking the LLM to generate test cases slice by slice" — abstract
> "Our method simplifies the analysis scope, making it easier for the LLM to cover more lines and branches in each slice." — abstract
> "our method significantly outperforms current test case generation methods with LLMs and the typical SBST method Evosuite regarding both line and branch coverage scores" — abstract
