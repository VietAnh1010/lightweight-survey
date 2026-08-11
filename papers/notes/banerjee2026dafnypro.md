# DafnyPro: LLM-Assisted Automated Verification for Dafny Programs

- **Citekey:** banerjee2026dafnypro
- **Record:** arxiv:2601.05385
- **Authors:** Debangshu Banerjee, Olivier Bouissou, Stefan Zetzsche
- **Venue:** arXiv 2026
- **Categories:** formal-verification, program-logic, proof-automation
- **Link:** http://arxiv.org/abs/2601.05385v1

## Problem

- Generating Dafny verification annotations is where model assistance stalls.
- A model asked for annotations may quietly edit the program logic instead of annotating it.
- Generated invariants accumulate, and redundant ones slow the verifier without helping.

## Main ideas

- DafnyPro adds three guards at inference time, changing no training.
- A diff-checker forbids edits to the base program, so only annotations may change.
- A pruner removes invariants that the proof does not need.
- A hint-augmentation system retrieves problem-independent proof strategies and applies them.
- Retrieved strategies are generic, so no per-problem corpus is required.

## Evaluation

- Four benchmarks: Clover, MBPP-Dafny, HumanEval-Dafny, DafnyBench.
- DafnyBench with Claude Sonnet 3.5: 86% correct proofs, 16 points above the base model.
- Fine-tuned Qwen 7B and 14B reach 68% and 70% on DafnyBench.
- Distilling from DafnyPro traces into small models is a separate, checkable result.

## Limitations

- Ours: correctness means Dafny accepts the proof, which a weak specification can also achieve.
- Ours: no ablation isolates the diff-checker, the pruner, and the hints from each other.
- Ours: the hint library is predefined, so its coverage bounds the technique.
- Authors: gains are reported per benchmark, and DafnyBench is named as the hardest.

## Follow-ups

- Ablate the three components; the diff-checker alone may explain most of the gain.
- Measure whether pruned invariant sets stay adequate under program mutation.
- Grow the hint library automatically from successful proofs, closing the loop.

## Evidence

> "DafnyPro comprises three key components: a diff-checker that prevents modifications to base program logic, a pruner that removes unnecessary invariants, and a hint-augmentation system that retrieves and applies predefined, problem-independent proof strategies." — abstract
> "on DafnyBench, the most challenging benchmark, Claude Sonnet 3.5 enhanced with DafnyPro achieves 86% correct proofs, a 16 pp improvement over the base model" — abstract
> "Our 7B and 14B models achieve 68% and 70% correct proofs on DafnyBench, respectively" — abstract
