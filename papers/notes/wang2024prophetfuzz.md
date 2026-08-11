# ProphetFuzz: Fully Automated Prediction and Fuzzing of High-Risk Option Combinations with Only Documentation via Large Language Model

- **Citekey:** wang2024prophetfuzz
- **Record:** doi:10.1145/3658644.3690231
- **Authors:** Dawei Wang, Geng Zhou, Li Chen, Dan Li et al.
- **Venue:** CCS 2024
- **Categories:** fuzzing, bug-detection
- **Link:** http://arxiv.org/abs/2409.00922v1

## Problem

- Option combinations create a vast search space for security testing.
- Mutation and filtering treat every combination as equally likely to hold a vulnerability.
- Time is therefore spent on targets that were never going to be vulnerable.

## Main ideas

- ProphetFuzz predicts which option combinations are high-risk before fuzzing them.
- Prediction uses documentation alone, so no source or execution is needed first.
- Documentation encodes intent about option interaction, which a mutator cannot read.
- The prediction supplies a prior over a combinatorial space, replacing uniform treatment.
- The whole pipeline runs without human intervention.

## Evaluation

- 52 programs from three related studies; the experiment consumed 10.44 CPU years.
- 1748 high-risk combinations predicted at $8.69 per program.
- After 72 hours, 364 unique vulnerabilities in 12.30% of predicted combinations.
- 32.85% more than state of the art in the same timeframe.
- Persistent fuzzing found 140 vulnerabilities: 93 developer-confirmed, 21 with CVE numbers.

## Limitations

- Ours: 12.30% of predicted combinations yielded vulnerabilities, so most predictions were wrong.
- Ours: programs with poor documentation give the predictor nothing to read.
- Ours: the mechanism is prompt engineering, so part of the contribution rides on the prompt.
- Authors: prior methods waste time on non-vulnerable targets, which the prior reduces.

## Follow-ups

- Report precision of the risk prediction directly, not only downstream vulnerability counts.
- Test on programs with sparse documentation, where the premise breaks.
- Combine documentation priors with coverage feedback, which measures a different signal.

## Evidence

> "we utilize carefully designed prompt engineering to drive the large language model (LLM) to predict high-risk option combinations (i.e., more likely to contain vulnerabilities) and perform fuzz testing automatically without human intervention" — abstract
> "ProphetFuzz successfully predicted 1748 high-risk option combinations at an average cost of only \\$8.69 per program." — abstract
> "uncovering 140 vulnerabilities, with 93 confirmed by developers and 21 awarded CVE numbers" — abstract
