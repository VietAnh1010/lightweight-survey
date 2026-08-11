# Towards Neural Synthesis for SMT-Assisted Proof-Oriented Programming

- **Citekey:** chakraborty2024neural
- **Record:** arxiv:2405.01787
- **Authors:** Saikat Chakraborty, Gabriel Ebner, Siddharth Bhat, Sarah Fakhoury et al.
- **Venue:** ICSE 2024
- **Categories:** proof-automation, constraint-solving, program-synthesis
- **Link:** http://arxiv.org/abs/2405.01787v3

## Problem

- Proof-oriented programs mix computation with correctness proofs, and both cost human effort.
- SMT automation in F* reduces that cost without removing it.
- Research was blocked by having no large corpus and no reproducible way to check candidates.

## Main ideas

- The dataset pairs each F* definition with a formal specification expressed as an F* type.
- That framing makes synthesis type-directed: the type is the problem statement.
- A program fragment checker queries F* itself, so candidate solutions are machine-checked.
- Type-based retrieval augmentation supplies context selected by type rather than by text.
- Retrieval is the part that transfers to other proof-oriented languages.

## Evaluation

- 600K lines of open-source F*, about 32K top-level definitions; extended to 940K lines and 54k definitions.
- Code drawn from Windows, Linux, Python, and Firefox production systems.
- Fine-tuned Phi-2 and StarCoder compare favourably with GPT-4 at much lower cost.
- Type-based retrieval augmentation boosts performance significantly.

## Limitations

- Ours: the dataset is the headline, so the retrieval technique is evaluated as a secondary result.
- Ours: no absolute solve rates appear in the abstract, only relative comparisons.
- Ours: F* is one language with one SMT backend, so transfer is untested.
- Authors: strengths and weaknesses are identified through error analysis rather than measured.

## Follow-ups

- Report absolute definition-level solve rates, so later work has a number to beat.
- Test type-based retrieval in Dafny and Verus, which also carry types as specifications.
- Measure whether the small-model result holds as the specification type grows complex.

## Evidence

> "Our dataset includes around 32K top-level F* definitions, each representing a type-directed program and proof synthesis problem producing a definition given a formal specification expressed as an F* type." — abstract
> "We also identify various type-based retrieval augmentation techniques and find that they boost performance significantly." — abstract
> "the performance of fine-tuned smaller language models (such as Phi-2 or StarCoder) compare favorably with large language models (such as GPT-4), at a much lower computational cost" — abstract
