# Your Fix Is My Exploit: Enabling Comprehensive DL Library API Fuzzing with Large Language Models

- **Citekey:** zhang2025your
- **Record:** arxiv:2501.04312
- **Authors:** Kunpeng Zhang, Shuai Wang, Jitao Han, Xiaogang Zhu et al.
- **Venue:** ICSE 2025
- **Categories:** fuzzing, bug-detection
- **Link:** http://arxiv.org/abs/2501.04312v1

## Problem

- Deep learning libraries carry memory-safety bugs and expose over 1,000 APIs each.
- Traditional fuzzing cannot cover that API surface: inputs are complex and usage varies.
- Existing model-based fuzzers lack knowledge of API edge cases and generate weak inputs.

## Main ideas

- DFUZZ gives the model a white-box view of API implementations rather than signatures alone.
- First insight: the model can reason about error-triggering edge cases from the API code itself.
- That reasoning transfers, so edge cases learned from one API are applied to untested APIs.
- Transfer is what makes a 1,000-API surface tractable without per-API effort.
- Second insight: the model synthesizes the test programs, so API testing needs no harness authoring.

## Evaluation

- TensorFlow and PyTorch; higher API coverage than state-of-the-art fuzzers.
- 37 bugs uncovered, 8 fixed and 19 under developer investigation.
- Developer engagement on 27 of 37 is a meaningful external signal.
- Not reported: how many APIs were covered in absolute terms, or the cost per API.

## Limitations

- Ours: the white-box view needs source access, so closed-source libraries are out of reach.
- Ours: transfer of edge cases is claimed but not measured separately from generation quality.
- Ours: 37 bugs across two libraries is modest against a 1,000-API surface.
- Authors: existing LLM-based fuzzers lack deep knowledge of API edge cases.

## Follow-ups

- Measure edge-case transfer directly: hold out APIs and test whether their bugs are still found.
- Report per-API cost, since a white-box view means reading implementation code for each.
- Combine with PromptFuzz's coverage-guided prompt mutation, which optimises a different signal.

## Evidence

> "DFUZZ leverages two insights: (1) LLMs can reason about error-triggering edge cases from API code and apply this knowledge to untested APIs, and (2) LLMs can accurately synthesize test programs to automate API testing." — abstract
> "By providing LLMs with a \"white-box view\" of APIs, DFUZZ enhances reasoning and generation for comprehensive fuzzing." — abstract
> "DFUZZ outperforms state-of-the-art fuzzers in API coverage for TensorFlow and PyTorch, uncovering 37 bugs, with 8 fixed and 19 under developer investigation" — abstract
