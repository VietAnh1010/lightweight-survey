# SpecRover: Code Intent Extraction via LLMs

- **Citekey:** ruan2024specrover
- **Record:** arxiv:2408.02232
- **Authors:** Haifeng Ruan, Yuntong Zhang, Abhik Roychoudhury
- **Venue:** ICSE 2024
- **Categories:** specification, program-repair, agents
- **Link:** http://arxiv.org/abs/2408.02232v4

## Problem

- Repair needs a specification of intended behaviour, and a GitHub issue is not one.
- An agent that searches code and edits it never states what behaviour it was aiming for.
- Without a stated intent, a developer cannot tell a good patch from a plausible one.

## Main ideas

- SpecRover interleaves specification inference with the code search, rather than running it once.
- Intent is inferred from both project structure and program behaviour.
- A separate reviewer agent vets patches against that inferred intent.
- The reviewer also attaches a confidence measure, so patches arrive ranked by credibility.
- The explanation produced is the signal the developer reads, not the patch alone.
- Built on the open-source AutoCodeRover agent, so the delta is the specification machinery.

## Evaluation

- Full SWE-Bench, 2294 GitHub issues: more than 50% improvement in efficacy over AutoCodeRover.
- Cost about $0.65 per issue on SWE-Bench lite, modest against comparable open-source agents.
- Building on a named baseline agent makes the improvement attributable.
- Not measured: whether the inferred specification is correct, only whether patches improve.

## Limitations

- Ours: SWE-Bench issues predate model training cutoffs, so leakage is a standing concern.
- Ours: resolution on SWE-Bench means the project's tests pass, which is a weak specification oracle.
- Ours: the reviewer agent shares a model family with the patcher, so its errors may correlate.
- Authors: the work is positioned as demonstrating that specification inference still matters.

## Follow-ups

- Score inferred specifications directly against maintainer-written descriptions of intended behaviour.
- Use a reviewer from a different model family to test whether correlated errors inflate confidence.
- Report calibration of the confidence measure, which is what a developer would act on.

## Evidence

> "In this work, we examine efficient and low-cost workflows for iterative specification inference within an LLM agent." — abstract
> "The intent thus captured is examined by a reviewer agent with the goal of vetting the patches as well as providing a measure of confidence in the vetted patches." — abstract
> "In an evaluation on the full SWE-Bench consisting of 2294 GitHub issues, it shows more than 50% improvement in efficacy over AutoCodeRover." — abstract
