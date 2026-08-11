# FastFixer: An Efficient and Effective Approach for Repairing Programming Assignments

- **Citekey:** liu2024fastfixer
- **Record:** arxiv:2410.21285
- **Authors:** Fang Liu, Zhenwei Liu, Qianhui Zhao, Jing Jiang et al.
- **Venue:** ASE 2024
- **Categories:** program-repair
- **Link:** http://arxiv.org/abs/2410.21285v1

## Problem

- Programming education needs personalised feedback quickly, which manual review cannot supply.
- Standard fine-tuning does not teach the model where to edit in an advanced assignment.
- Autoregressive decoding makes patch generation slow enough to break timely feedback.

## Main ideas

- FastFixer attacks accuracy and latency as one problem, not two.
- A repair-oriented fine-tuning strategy directs attention to the patch and its surrounding context.
- Learning the patch plus its context is what lets the model locate the edit.
- A second contribution accelerates inference specifically for repair.
- The acceleration exploits that a patch mostly repeats its context, which general decoding ignores.

## Evaluation

- 20.46% overall improvement in assignment fixing over the state-of-the-art baseline.
- 16.67 times inference speedup against autoregressive decoding.
- Speed and accuracy are reported together, which matters for the feedback use case.
- Not reported in the abstract: the assignment dataset size or language.

## Limitations

- Ours: student assignments are short and self-contained, so transfer to real projects is untested.
- Ours: correctness is assignment test passing, which admits patches that overfit the tests.
- Ours: no ablation separates the fine-tuning gain from the decoding gain.
- Authors: current fine-tuning strategies are inadequate for guiding edits, which is the premise.

## Follow-ups

- Ablate fine-tuning against acceleration; they address different failures and may not compose.
- Test the repair-specific decoding on Defects4J, where patches also largely copy context.
- Measure whether faster feedback changes student outcomes, which is the stated motivation.

## Evidence

> "we first propose a novel repair-oriented fine-tuning strategy, aiming to enhance the LLM's attention towards learning how to generate the necessary patch and its associated context" — abstract
> "to speed up the patch generation, we propose an inference acceleration approach that is specifically tailored for the program repair task" — abstract
> "FastFixer obtains an overall improvement of 20.46% in assignment fixing when compared to the state-of-the-art baseline. Considering the repair efficiency, FastFixer achieves a remarkable inference speedup of 16.67 times" — abstract
