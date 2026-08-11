# Lares: LLM-driven Code Slice Semantic Search for Patch Presence Testing

- **Citekey:** li2025lares
- **Record:** arxiv:2511.01252
- **Authors:** Siyuan Li, Yaowen Zheng, Hong Li, Jingdong Guo et al.
- **Venue:** ASE 2025
- **Categories:** decompilation, bug-detection, constraint-solving
- **Link:** http://arxiv.org/abs/2511.01252v1

## Problem

- 1-day vulnerabilities spread through code reuse, so finding the vulnerable function is not enough.
- The question is whether that function has already been patched in the target binary.
- Existing methods need the compilation process and confuse patch changes with compiler variation.

## Main ideas

- Code Slice Semantic Search extracts features from the patch source rather than from a build.
- It then looks for semantically equivalent code slices in the target binary's pseudocode.
- Dropping the compilation requirement is what makes the method usable on arbitrary software.
- The model performs the code analysis; SMT solvers perform the logical reasoning.
- Splitting those two roles is what keeps accuracy while removing the build dependency.

## Evaluation

- Superior precision, recall, and usability against existing patch presence testing methods.
- First evaluation of patch presence testing across optimization levels, architectures, and compilers.
- That cross-configuration matrix is the contribution the field lacked.
- No absolute precision or recall values appear in the abstract.

## Limitations

- Ours: no absolute numbers in the abstract, so the margin over baselines is unclear.
- Ours: semantic equivalence of slices is judged by a model, so errors are silent.
- Ours: the method needs patch source, which is unavailable for closed-source fixes.
- Authors: prior work cannot separate patch-induced changes from compilation-induced ones.

## Follow-ups

- Report precision and recall per optimization level, since the matrix is the paper's novelty.
- Test on patches whose source is unavailable, using only the binary difference.
- Measure how often the SMT stage overturns the model's slice judgement.

## Evidence

> "Lares introduces Code Slice Semantic Search, which directly extracts features from the patch source code and identifies semantically equivalent code slices in the pseudocode of the target binary." — abstract
> "By eliminating the need for the compilation process, Lares improves usability, while leveraging large language models (LLMs) for code analysis and SMT solvers for logical reasoning to enhance accuracy." — abstract
> "it is the first work to evaluate patch presence testing across optimization levels, architectures, and compilers" — abstract
