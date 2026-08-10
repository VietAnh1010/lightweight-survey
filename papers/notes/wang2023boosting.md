# Boosting Static Resource Leak Detection via LLM-based Resource-Oriented Intention Inference

- **Citekey:** wang2023boosting
- **Record:** arxiv:2311.04448
- **Authors:** Chong Wang, Jianan Liu, Xin Peng, Yang Liu et al.
- **Venue:** ICSE 2023
- **Categories:** static-analysis, bug-detection
- **Link:** http://arxiv.org/abs/2311.04448v4

## Problem

- Resource leak detectors match predefined acquisition and release APIs mechanically.
- An incomplete API list produces false negatives: unlisted resources are never tracked.
- Incomplete reachability-validation identification produces false positives on validated paths.

## Main ideas

- InferROI asks the model for intentions, not for verdicts: acquisition, release, and reachability validation.
- Intentions are facts about the code that the analyser lacked, expressed in the analyser's vocabulary.
- A two-stage static analysis then checks control-flow paths using those inferred intentions.
- The division is clean: the model supplies the API semantics, the analysis does the path reasoning.
- This attacks both error sources at once, since both stem from incomplete predefined knowledge.

## Evaluation

- DroidLeaks and JLeaks: detection rates 59.3% and 62.5%, false alarm rates 18.6% and 19.5%.
- Against three industrial static detectors: 14-45 more bugs on DroidLeaks, 149-485 more on JLeaks.
- 29 previously unknown leaks found in open-source projects, 7 confirmed by developers.
- An ablation study shows the combination matters, not either half alone.

## Limitations

- Ours: a false alarm rate near 19% is high for a detector meant to reduce triage effort.
- Ours: inferred intentions are unchecked, so a wrong intention silently corrupts the path analysis.
- Ours: 29 confirmed-by-authors bugs with 7 developer confirmations is a modest external signal.
- Authors: existing detectors suffer both false negatives and false positives from incompleteness.

## Follow-ups

- Validate inferred intentions against observed runtime behaviour before the analysis consumes them.
- Apply intention inference to other analyses whose API models are hand-maintained, such as taint sources.
- Report how the false alarm rate moves as intention confidence thresholds change.

## Evidence

> "we propose InferROI, a novel approach that leverages the exceptional code comprehension capability of large language models (LLMs) to directly infer resource-oriented intentions (acquisition, release, and reachability validation) in code" — abstract
> "InferROI first prompts the LLM to infer involved intentions for a given code snippet, and then incorporates a two-stage static analysis approach to check control-flow paths for resource leak detection based on the inferred intentions." — abstract
> "the results of an ablation study underscores the importance of combining LLM-based inference with static analysis" — abstract
