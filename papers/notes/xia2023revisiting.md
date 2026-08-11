# Revisiting the Plastic Surgery Hypothesis via Large Language Models

- **Citekey:** xia2023revisiting
- **Record:** doi:10.1109/ase56229.2023.00047
- **Authors:** Chunqiu Steven Xia, Yifeng Ding, Lingming Zhang
- **Venue:** ASE 2023
- **Categories:** program-repair
- **Link:** http://arxiv.org/abs/2303.10494v2

## Problem

- Template-based repair is limited in the bug types and patch variety it can produce.
- Model-based repair does not know project-specific variable and method names.
- The plastic surgery hypothesis says the fix ingredients already exist in the same project.
- Model-based work had set that hypothesis aside.

## Main ideas

- FitRepair revives the hypothesis, and observes that models can automate it fully.
- Two domain-specific fine-tuning strategies teach the model the project's own identifiers.
- One prompting strategy supplies project-local code ingredients at repair time.
- Fine-tuning and prompting attack the same gap from the parameter and context sides.
- The hypothesis becomes automatic rather than encoded by hand as in template tools.

## Evaluation

- Defects4J 1.2 and 2.0: 89 and 44 bugs fixed.
- That is 15 and 8 more than the best-performing baseline.
- Both dataset versions are reported, which separates tuning from generalisation.
- Not measured: how much each of the three strategies contributes.

## Limitations

- Ours: Defects4J predates model training cutoffs, so leakage is not addressed.
- Ours: fixes are counted by test-suite passing, which admits overfitted patches.
- Ours: no ablation across the two fine-tuning strategies and the prompting strategy.
- Authors: models used for direct repair are unaware of project-specific information.

## Follow-ups

- Ablate the three strategies; fine-tuning per project is far costlier than prompting.
- Test on post-cutoff bugs, since project-specific memorisation is the obvious confound.
- Compare against retrieval over the project, which supplies ingredients without fine-tuning.

## Evidence

> "The plastic surgery hypothesis is a well-known insight for APR, which states that the code ingredients to fix the bug usually already exist within the same project." — abstract
> "we propose FitRepair, which combines the direct usage of LLMs with two domain-specific fine-tuning strategies and one prompting strategy for more powerful APR" — abstract
> "FitRepair fixes 89 and 44 bugs (substantially outperforming the best-performing baseline by 15 and 8), respectively" — abstract
