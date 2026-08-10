# VeriStruct: AI-assisted Automated Verification of Data-Structure Modules in Verus

- **Citekey:** sun2025veristruct
- **Record:** arxiv:2510.25015
- **Authors:** Chuyue Sun, Yican Sun, Daneshvar Amrollahi, Ethan Zhang et al.
- **Venue:** TACAS 2025
- **Categories:** formal-verification, specification, program-logic, proof-automation
- **Link:** http://arxiv.org/abs/2510.25015v4

## Problem

- AI-assisted verification had been demonstrated on single functions, not on modules.
- A data-structure module needs abstractions and type invariants before any function can be verified.
- Models misunderstand Verus annotation syntax and verification-specific semantics.

## Main ideas

- VeriStruct raises the unit of verification from the function to the data-structure module.
- A planner module orchestrates generation in order: abstractions, type invariants, specifications, proofs.
- Ordering matters because later artefacts depend on the abstractions chosen earlier.
- Syntax guidance is embedded in prompts to address the Verus-specific misunderstanding directly.
- A repair stage corrects annotation errors automatically, so syntax failures do not end the run.
- Verus itself decides success, so the framework never certifies its own output.

## Evaluation

- Eleven Rust data structure modules; VeriStruct succeeds on ten.
- 128 of 129 functions verified, 99.2%.
- Verification is by Verus, so the pass criterion is machine-checked rather than judged.
- Not measured: specification strength, so a weak invariant that verifies still counts as success.

## Limitations

- Ours: eleven modules is a small evaluation for a 99.2% figure.
- Ours: verifying against generated specifications risks specifications weak enough to be easy.
- Ours: no comparison against a function-at-a-time baseline on the same modules.
- Authors: models often misunderstand Verus annotation syntax and verification-specific semantics.

## Follow-ups

- Measure specification strength, for example by mutating the data structure and checking that proofs break.
- Scale past eleven modules and report where the planner's ordering assumption fails.
- Compare against verifying each function separately, to isolate what module-level planning buys.

## Evidence

> "VeriStruct employs a planner module to orchestrate the systematic generation of abstractions, type invariants, specifications, and proof code." — abstract
> "To address the challenge that LLMs often misunderstand Verus' annotation syntax and verification-specific semantics, VeriStruct embeds syntax guidance within prompts and includes a repair stage to automatically correct annotation errors." — abstract
> "In an evaluation on eleven Rust data structure modules, VeriStruct succeeds on ten of the eleven, successfully verifying 128 out of 129 functions (99.2%) in total." — abstract
