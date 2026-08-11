# LineBreaker: Finding Token-Inconsistency Bugs with Large Language Models

- **Citekey:** chen2024linebreaker
- **Record:** arxiv:2405.01668
- **Authors:** Hongbo Chen, Yifan Zhang, Xing Han, Tianhao Mao et al.
- **Venue:** ASE 2024
- **Categories:** bug-detection, static-analysis
- **Link:** http://arxiv.org/abs/2405.01668v2

## Problem

- Token-inconsistency bugs use valid syntax with the wrong variable or function.
- They are semantic and context-dependent, so static analysis and dynamic testing both struggle.
- Some survive undetected for years.

## Main ideas

- A systematic measurement first: GPT-4 shows promise but loses precision and does not scale.
- The diagnosed causes are attention to clean snippets and the cost of inspecting all code.
- LineBreaker cascades: small code-specific models filter snippets unlikely to hold a bug.
- Only survivors reach the expensive model, which is what makes repository-scale sweeps affordable.
- The cascade improves precision, recall, and scalability together rather than trading them.

## Evaluation

- 154 Python and C GitHub repositories, each with over 1,000 stars.
- 123 new flaws found; 45% could be exploited to disrupt program functionality.
- 69 fixes submitted, 41 confirmed or merged.
- Merged fixes are an external oracle, stronger than a labelled benchmark.

## Limitations

- Ours: the cheap filter can discard true positives, and no recall loss figure is given.
- Ours: exploitability is assessed by the authors rather than by maintainers.
- Ours: cost per repository is not reported, though cost motivates the design.
- Authors: GPT-4 tends to focus on snippets that contain no bug, which the filter compensates for.

## Follow-ups

- Measure how many true bugs the cheap filter discards at each threshold.
- Report dollar cost per repository, which is the quantity the cascade optimises.
- Apply the cascade to other semantic bug classes where inspection cost dominates.

## Evidence

> "This paper reports the first systematic measurement of LLMs' capabilities in detecting TIBs, revealing that while GPT-4 shows promise, it exhibits limitations in precision and scalability." — abstract
> "\\name leverages smaller, code-specific, and highly efficient language models to filter out large numbers of code snippets unlikely to contain TIBs, thereby significantly enhancing the system's performance in terms of precision, recall, and scalability." — abstract
> "uncovering 123 new flaws, 45\\% of which could be exploited to disrupt program functionalities. Out of our 69 submitted fixes, 41 have already been confirmed or merged." — abstract
