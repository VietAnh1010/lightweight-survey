# From Obfuscated to Obvious: A Comprehensive JavaScript Deobfuscation Tool for Security Analysis

- **Citekey:** zhou2025obfuscated
- **Record:** doi:10.14722/ndss.2026.242198
- **Authors:** Dongchao Zhou, Lingyun Ying, Huajun Chai, Dongbin Wang
- **Venue:** NDSS 2025
- **Categories:** decompilation, static-analysis
- **Link:** http://arxiv.org/abs/2512.14070v1

## Problem

- Attackers obfuscate JavaScript to hide malicious behaviour.
- Existing deobfuscators handle only specific obfuscation types and few input formats.
- Their output stays cryptic, so a human analyst still cannot read it.

## Main ideas

- JSIMPLIFIER stages the work: preprocessing, AST static analysis, then dynamic execution tracing.
- Static and dynamic stages together undo transformations neither handles alone.
- The model is used only for identifier renaming, the last stage.
- Renaming changes no semantics, so the model cannot corrupt the recovered program.
- Confining the model to a semantics-preserving step is the design's safety property.
- Evaluation metrics combine flow analysis, complexity, entropy, and readability judgements.

## Evaluation

- A released dataset of 44,421 real-world samples: 23,212 wild malicious and 21,209 benign.
- 100% processing capability across 20 obfuscation techniques.
- 100% correctness on the evaluation subsets, and 88.2% code complexity reduction.
- Over four-fold readability improvement, validated by multiple models.

## Limitations

- Ours: readability judged by models is circular when models also did the renaming.
- Ours: 100% correctness is on subsets, not on the full 44,421-sample dataset.
- Ours: dynamic tracing needs execution, which evasive malware can detect and defeat.
- Authors: existing tools produce cryptic output, which the renaming stage targets.

## Follow-ups

- Validate readability with human analysts, since model judgement shares the renamer's biases.
- Report correctness on the full dataset, not the evaluation subsets.
- Measure how tracing fares against samples with anti-analysis checks.

## Evidence

> "we present JSIMPLIFIER, a comprehensive deobfuscation tool using a multi-stage pipeline with preprocessing, abstract syntax tree-based static analysis, dynamic execution tracing, and Large Language Model (LLM)-enhanced identifier renaming" — abstract
> "We construct and release the largest real-world obfuscated JavaScript dataset with 44,421 samples (23,212 wild malicious + 21,209 benign samples)." — abstract
> "JSIMPLIFIER outperforms existing tools with 100% processing capability across 20 obfuscation techniques, 100% correctness on evaluation subsets, 88.2% code complexity reduction, and over 4-fold readability improvement validated by multiple LLMs" — abstract
