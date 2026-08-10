# Revisiting Unnaturalness for Automated Program Repair in the Era of Large Language Models

- **Citekey:** yang2024revisiting
- **Record:** arxiv:2404.15236
- **Authors:** Aidan Z. H. Yang, Sophia Kolak, Vincent J. Hellendoorn, Ruben Martins et al.
- **Venue:** ICSE 2024
- **Categories:** program-repair, bug-detection
- **Link:** http://arxiv.org/abs/2404.15236v1

## Problem

- Fault localization scores lack diversity, so many statements tie in the ranking.
- Patch generation is inefficient: every test must run before a patch's plausibility is known.
- Patch ranking overfits the test suite, and using an LLM directly raises data leakage concerns.

## Main ideas

- Entropy is an intermediate value the model already computes, and it measures token naturalness.
- Using entropy rather than model output sidesteps the leakage concern the authors raise.
- Entropy re-ranks suspicious statements and is complementary to existing localization tools.
- entropy-delta measures patch naturalness, so plausible patches are ranked before any test runs.
- The same signal therefore serves localization, generation efficiency, and patch classification.

## Evaluation

- Re-ranking achieves a 50% Top-5 improvement over spectrum-based fault localization.
- entropy-delta ranks correct patches better than state-of-the-art machine learning tools, 49% Top-1.
- The claim of complementarity is measured against prior tools rather than replacing them.
- Not measured: cost of computing entropy over every candidate.

## Limitations

- Ours: naturalness correlates with correctness, and the paper does not claim causation.
- Ours: entropy comes from a model trained on public code, so leakage is reduced, not removed.
- Ours: improvements are relative percentages, so the absolute Top-1 and Top-5 levels are unclear.
- Authors: test-suite overfitting and data leakage are the two problems this design minimises.

## Follow-ups

- Report absolute Top-1 and Top-5 alongside the relative gains.
- Test whether entropy from a model that never saw the project still ranks patches well.
- Apply entropy-delta as an early-exit signal inside an agentic repair loop, before validation.

## Evidence

> "One intermediate value an LLM can emit is entropy, which measures the naturalness of a token of code." — abstract
> "We propose a patch-naturalness measurement, entropy-delta, to improve the efficiency of template-based repair techniques by ranking plausible patches before undergoing testing." — abstract
> "Our proposed re-ranking method achieves a 50% Top-5 score improvement over SBFL." — abstract
