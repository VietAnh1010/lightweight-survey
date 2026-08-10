# Exposing Hidden Interfaces: LLM-Guided Type Inference for Reverse Engineering macOS Private Frameworks

- **Citekey:** kharlamova2026exposing
- **Record:** arxiv:2601.01673
- **Authors:** Arina Kharlamova, Youcheng Sun, Ting Yu
- **Venue:** arXiv 2026
- **Categories:** decompilation, static-analysis, agents
- **Link:** http://arxiv.org/abs/2601.01673v1

## Problem

- Private macOS frameworks underpin critical services but ship as stripped, undocumented binaries.
- Without method signatures there is no interface to audit, so security analysis stalls.
- Static tooling alone recovers a small fraction of Objective-C signatures.

## Main ideas

- MOTIF is an agent that drives tools while a fine-tuned model specializes in Objective-C type inference.
- The agent handles runtime metadata extraction, binary inspection, and constraint checking.
- The model proposes candidate method signatures; the agent validates and refines them.
- Compilability is the acceptance test: a signature is kept when the header compiles.
- Specializing the model and delegating tool use separates guessing from checking.

## Evaluation

- MOTIF-Bench, built from public frameworks that have ground-truth headers.
- Signature recovery rises from 15% to 86% against baseline static analysis tooling.
- Reported gains in tool-use correctness and inference stability alongside recovery.
- Case studies on private frameworks: reconstructed headers compile and link.

## Limitations

- Ours: the benchmark uses public frameworks, while the target is private ones with no ground truth.
- Ours: compiling and linking do not establish that a recovered signature is the original one.
- Ours: the fine-tuned model is Objective-C specific, so transfer to other ABIs is untested.
- Authors: private frameworks remain undocumented, so case-study results cannot be scored.

## Follow-ups

- Cross-check recovered signatures against runtime call traces, which is an independent oracle.
- Measure how recovery degrades with optimization level and stripping aggressiveness.
- Test whether the agent plus specialized model split transfers to C++ name recovery.

## Evidence

> "The agent manages runtime metadata extraction, binary inspection, and constraint checking, while the model generates candidate method signatures that are validated and refined into compilable headers." — abstract
> "MOTIF improves signature recovery from 15% to 86% compared to baseline static analysis tooling, with consistent gains in tool-use correctness and inference stability" — abstract
> "Private macOS frameworks underpin critical services and daemons but remain undocumented and distributed only as stripped binaries, complicating security analysis." — abstract
