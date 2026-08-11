# CoDe-R: Refining Decompiler Output with LLMs via Rationale Guidance and Adaptive Inference

- **Citekey:** zhang2026code
- **Record:** arxiv:2604.12913
- **Authors:** Qiang Zhang, Zhongnian Li
- **Venue:** arXiv 2026
- **Categories:** decompilation
- **Link:** http://arxiv.org/abs/2604.12913v2

## Problem

- Decompilation reconstructs source from stripped executables, and compilation destroys semantics.
- Models fill that gap with logical hallucinations and semantic misalignment.
- The result is code that reads plausibly and fails to re-execute.

## Main ideas

- CoDe-R refines decompiler output in two stages rather than decompiling from scratch.
- Semantic Cognitive Enhancement trains the model to recover algorithmic intent alongside the code.
- Recovering intent is what supplies the semantics compilation removed.
- Dynamic Dual-Path Fallback runs at inference and balances semantic recovery against syntactic stability.
- A hybrid verification strategy decides which path each case takes.
- The design targets the lightweight regime, so a 1.3B backbone is the point.

## Evaluation

- HumanEval-Decompile benchmark.
- First 1.3B model to exceed a 50.00% average re-executability rate.
- Re-executability is the metric that logical hallucination directly damages.
- State of the art in the lightweight regime, not against large models.

## Limitations

- Ours: just over 50% re-executability means half the output still fails to run.
- Ours: the claim is scoped to lightweight models, so large-model comparison is absent.
- Ours: HumanEval-Decompile holds small self-contained functions, unlike real binaries.
- Authors: semantic loss during compilation is irreversible, which bounds what refinement can recover.

## Follow-ups

- Evaluate on stripped real-world binaries rather than compiled benchmark functions.
- Pair refinement with a differential check, which would turn re-executability into equivalence.
- Report how often the fallback path fires, which shows when semantic recovery is abandoned.

## Evidence

> "The first stage introduces Semantic Cognitive Enhancement (SCE), a Rationale-Guided Semantic Injection strategy that trains the model to recover high-level algorithmic intent alongside code." — abstract
> "The second stage introduces a Dynamic Dual-Path Fallback (DDPF) mechanism during inference, which adaptively balances semantic recovery and syntactic stability via a hybrid verification strategy." — abstract
> "it is the first 1.3B model to exceed an Average Re-executability Rate of 50.00%" — abstract
