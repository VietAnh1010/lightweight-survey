# InferFix: End-to-End Program Repair with LLMs

- **Citekey:** jin2023inferfix
- **Record:** doi:10.1145/3611643.3613892
- **Authors:** Matthew Jin, Syed Shahriar, Michele Tufano, Xin Shi et al.
- **Venue:** FSE 2023
- **Categories:** program-repair, static-analysis
- **Link:** https://doi.org/10.1145/3611643.3613892

## Problem

- Model-based repair learns general bug-fixing patterns from uncategorized public repository commits.
- Security and performance bugs need the bug's type and a matching fix, not a generic pattern.
- Deployment also needs detection, classification, and localization, which a generator does not supply.

## Main ideas

- InferFix pairs the generator with the Infer static analyzer, which supplies detection and bug type.
- A Retriever, pretrained contrastively, searches for semantically equivalent past bugs and their fixes.
- The Generator is Codex Cushman fine-tuned on supervised bug-fix data.
- Prompts carry the bug type annotation and the retrieved fix, so both analyser and memory condition it.
- The retrieved fixes are external non-parametric memory, so new fix patterns need no retraining.

## Evaluation

- InferredBugs: bugs extracted by running Infer over change histories of thousands of Java and C# repos.
- Top-1 accuracy 65.6% in C# and 76.8% in Java, above strong LLM baselines.
- Deployed with Infer at Microsoft, integrated into the continuous integration pipeline.
- The dataset is built by the same analyser used at inference, so bug types are consistent by construction.

## Limitations

- Ours: coverage is bounded by what Infer reports; bugs it misses never reach the generator.
- Ours: top-1 accuracy is measured against the historical fix, which is stricter and weaker than correctness.
- Ours: the retriever's benefit is not isolated from the fine-tuning in the reported numbers.
- Authors: prior models learn from uncategorized bugs, which is the gap the bug type annotation fills.

## Follow-ups

- Ablate the retriever and the bug type annotation separately to see which conditions the generator.
- Validate patches against Infer re-running, not only against the historical fix.
- Report how the approach transfers to an analyser whose bug taxonomy differs from Infer's.

## Evidence

> "we propose InferFix: a transformer-based program repair framework paired with a state-of-the-art static analyzer to fix critical security and performance bugs" — abstract
> "a Generator -- a large language model (Codex Cushman) finetuned on supervised bug-fix data with prompts augmented via bug type annotations and semantically similar fixes retrieved from an external non-parametric memory" — abstract
> "InferFix outperforms strong LLM baselines, with a top-1 accuracy of 65.6% for generating fixes in C# and 76.8% in Java" — abstract
