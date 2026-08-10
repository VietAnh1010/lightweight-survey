# Automated Repair of Ambiguous Problem Descriptions for LLM-Based Code Generation

- **Citekey:** jia2025automated
- **Record:** arxiv:2505.07270
- **Authors:** Haoxiang Jia, Robbie Morris, He Ye, Federica Sarro et al.
- **Venue:** ASE 2025
- **Categories:** specification, program-repair, program-synthesis
- **Link:** http://arxiv.org/abs/2505.07270v3

## Problem

- An ambiguous problem description yields an incorrect program, and the description is never blamed.
- Prompting a model to clarify its own ambiguity produces irrelevant or inconsistent edits.
- Repairing text requires knowing how the model's reading shifts when the text changes.

## Main ideas

- SpecFix repairs the description rather than the program, which inverts the usual repair target.
- A description is represented by the distribution of programs the model induces from it.
- That distribution is analysed and repaired with ordinary testing and program repair machinery.
- Contrastive specification inference then edits the text based on how the distribution moved.
- Splitting into these two steps avoids asking the model to introspect on its own ambiguity.

## Evaluation

- Four models: GPT-4o, GPT-4o-mini, DeepSeek-V3, Qwen2.5-Coder-32B-Instruct.
- Three benchmarks: HumanEval+, MBPP+, LiveCodeBench.
- 43.58% of descriptions modified; Pass@1 on that subset up 30.9%; 4.09% absolute overall.
- Repairs transfer: descriptions repaired for one model improve others by 10.48%.

## Limitations

- Ours: benchmark descriptions are short and self-contained, unlike industrial requirements.
- Ours: a description edited to raise Pass@1 may have been made more specific than the author intended.
- Ours: no check that the repaired description still describes the original task.
- Authors: directly prompting for clarification produces irrelevant or inconsistent edits.

## Follow-ups

- Check repaired descriptions against the original intent, not only against downstream Pass@1.
- Apply the distribution-shift view to formal specifications, where equivalence is decidable.
- Test on requirements documents, where ambiguity has consequences beyond one function.

## Evidence

> "we decompose this task into two simpler steps: (1) analyzing and repairing the LLM's interpretation of the description - captured by the distribution of programs it induces - using traditional testing and program repair, and (2) refining the description based on distribution changes via a method we call contrastive specification inference" — abstract
> "SpecFix modified 43.58% of descriptions, improving Pass@1 on the modified set by 30.9%. This yields a 4.09% absolute improvement across the entire benchmark." — abstract
> "We find that directly prompting LLMs to clarify ambiguity often produces irrelevant or inconsistent edits." — abstract
