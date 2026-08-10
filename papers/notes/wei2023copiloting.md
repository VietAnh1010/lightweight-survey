# Copiloting the Copilots: Fusing Large Language Models with Completion Engines for Automated Program Repair

- **Citekey:** wei2023copiloting
- **Record:** doi:10.1145/3611643.3616271
- **Authors:** Yuxiang Wei, Chunqiu Steven Xia, Lingming Zhang
- **Venue:** FSE 2023
- **Categories:** program-repair, program-synthesis
- **Link:** http://arxiv.org/abs/2309.00608v3

## Problem

- Patches for real-world systems in general-purpose languages are hard to synthesize correctly.
- Models treat programs as token sequences and ignore the language's semantic constraints.
- The result is many statically invalid patches, which makes the technique impractical.

## Main ideas

- Repilot intervenes during decoding rather than filtering completed patches.
- The insight is that autoregressive generation resembles typing, so a completion engine can assist it.
- The completion engine prunes infeasible tokens the model suggests, before they are committed.
- It also proactively completes tokens when its own suggestion set is determined.
- Validity is therefore a property of the generation process, not of a post-hoc filter.
- The approach generalizes past repair to other code generation tasks.

## Evaluation

- Subsets of Defects4J 1.2 and 2.0: 27% and 47% more bugs fixed than state-of-the-art techniques.
- More valid and correct patches than the base model at the same budget.
- Holding the budget fixed is what isolates the completion engine's contribution.
- Not measured: decoding overhead from consulting the engine at each token.

## Limitations

- Ours: static validity is necessary, not sufficient; a compiling patch can still be wrong.
- Ours: Defects4J correctness is judged by the test suite, which admits overfitted patches.
- Ours: the completion engine is language-specific, so each new language needs one.
- Authors: models are ignorant of the target language's semantic constraints, which is the premise.

## Follow-ups

- Report per-token decoding overhead, since the engine is consulted throughout generation.
- Extend the pruning signal past syntax and types to a lightweight semantic check.
- Compare against constrained decoding with a grammar, which is the cheaper alternative.

## Evidence

> "most LLMs treat programs as sequences of tokens, meaning that they are ignorant of the underlying semantics constraints of the target programming language. This results in plenty of statically invalid generated patches" — abstract
> "Repilot synergistically synthesizes a candidate patch through the interaction between an LLM and a Completion Engine, which 1) prunes away infeasible tokens suggested by the LLM and 2) proactively completes the token based on the suggestions provided by the Completion Engine." — abstract
> "Repilot outperforms state-of-the-art techniques by fixing 27% and 47% more bugs, respectively" — abstract
