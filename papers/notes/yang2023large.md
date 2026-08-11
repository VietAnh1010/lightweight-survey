# Large Language Models for Test-Free Fault Localization

- **Citekey:** yang2023large
- **Record:** arxiv:2310.01726
- **Authors:** Aidan Z. H. Yang, Ruben Martins, Claire Le Goues, Vincent J. Hellendoorn
- **Venue:** ICSE 2023
- **Categories:** bug-detection, program-repair
- **Link:** http://arxiv.org/abs/2310.01726v1

## Problem

- Fault localization assumes input tests are available.
- It also tends to need program analysis, instrumentation, or data preprocessing.
- Deep learning for repair learns poorly from small datasets and transfers badly to real programs.

## Main ideas

- LLMAO localizes buggy lines with no test coverage information at all.
- The obstacle is that language models read left to right, and localization needs both directions.
- A small set of bidirectional adapter layers is fine-tuned over the model's representations.
- Only the adapters are trained, which is why small curated corpora suffice.
- Performance scales with model size, tested at 350M, 6B, and 16B parameters.

## Evaluation

- Fine-tuned on small manually curated corpora such as Defects4J.
- Top-1 improves 2.3% to 54.4% over machine-learning fault localization baselines.
- Top-5 improves 14.4% to 35.6%.
- First fault localization technique with a language model architecture that reaches line-level vulnerabilities.

## Limitations

- Ours: wide improvement ranges suggest results vary sharply by baseline and dataset.
- Ours: Defects4J predates the models, so leakage is a standing concern for a memorisation-friendly task.
- Ours: dropping tests removes the only oracle, so predictions cannot be checked automatically.
- Authors: localization confidence depends on model size, which raises the cost of the best results.

## Follow-ups

- Evaluate on post-cutoff bugs, since line-level localization is exactly what memorisation would ace.
- Combine adapter scores with entropy signals, which target the same ranking problem differently.
- Report calibration, since a localizer without tests must communicate its own uncertainty.

## Evidence

> "we propose to overcome the left-to-right nature of LLMs by fine-tuning a small set of bidirectional adapter layers on top of the representations learned by LLMs to produce LLMAO, the first language model based fault localization approach that locates buggy lines of code without any test coverage information" — abstract
> "LLMAO improves the Top-1 results over the state-of-the-art machine learning fault localization (MLFL) baselines by 2.3%-54.4%, and Top-5 results by 14.4%-35.6%" — abstract
> "bug localization performance scaling consistently with the LLM size" — abstract
