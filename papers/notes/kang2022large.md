# Large Language Models are Few-shot Testers: Exploring LLM-based General Bug Reproduction

- **Citekey:** kang2022large
- **Record:** arxiv:2209.11515
- **Authors:** Sungmin Kang, Juyeon Yoon, Shin Yoo
- **Venue:** ICSE 2022
- **Categories:** test-generation, bug-detection
- **Link:** http://arxiv.org/abs/2209.11515v3

## Problem

- Test generation targets coverage or exploratory inputs, not semantic goals like reproducing a report.
- Turning the expected semantics in a bug report into an oracle is the hard part.
- Existing failure reproduction handles crashes only, a small share of all bug reports.

## Main ideas

- LIBRO takes the bug report as the input and asks the model for a reproducing test.
- The model cannot execute the buggy code, so the design puts the judgement in post-processing.
- Post-processing discerns when the model is effective rather than trusting each generation.
- Generated tests are ranked by validity, so the developer sees the most credible candidate first.
- Ranking is what converts an unreliable generator into a usable suggestion list.

## Evaluation

- Defects4J: reproducing tests for 33% of cases, 251 of 750; a correct test ranked first for 149 bugs.
- Contamination check: 31 reports filed after the training data cutoff, 32% reproduced.
- The post-cutoff rate matching the benchmark rate is the strongest evidence in the paper.
- An empirical study establishes that issue-driven tests are about 28% of project suite size.

## Limitations

- Authors: models cannot execute the target buggy code, which is why post-processing carries the design.
- Ours: 33% reproduction leaves the majority of reports unaddressed.
- Ours: 31 post-cutoff reports is a small sample for a contamination claim.
- Ours: validity ranking measures whether a test runs and fails, not whether it captures the report.

## Follow-ups

- Grow the post-cutoff evaluation set, since it is the only leakage-free measurement here.
- Combine report-driven generation with differential testing to strengthen the oracle.
- Measure whether reproducing tests improve downstream repair, the use the paper motivates.

## Evidence

> "Since LLMs themselves cannot execute the target buggy code, we focus on post-processing steps that help us discern when LLMs are effective, and rank the produced tests according to their validity." — abstract
> "LIBRO can generate failure reproducing test cases for 33% of all studied cases (251 out of 750), while suggesting a bug reproducing test in first place for 149 bugs" — abstract
> "To mitigate data contamination, we also evaluate LIBRO against 31 bug reports submitted after the collection of the LLM training data terminated: LIBRO produces bug reproducing tests for 32% of the studied bug reports." — abstract
