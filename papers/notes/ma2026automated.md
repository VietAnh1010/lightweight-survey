# Automated LTL Specification Generation from Industrial Aerospace Requirements

- **Citekey:** ma2026automated
- **Record:** arxiv:2604.21715
- **Authors:** Zhi Ma, Xiao Liang, Cheng Wen, Rui Chen et al.
- **Venue:** FM 2026
- **Categories:** specification, formal-verification
- **Link:** http://arxiv.org/abs/2604.21715v1

## Problem

- Aerospace verification uses LTL, and writing it from requirements needs two rare skills at once.
- The translation is labour-intensive and error-prone in industrial practice.
- NL2SPEC, NL2TL, and NL2LTL fail on real requirement documents.

## Main ideas

- AeroReq2LTL attacks the two named causes of that failure separately.
- A data dictionary normalises technical jargon into precise atomic propositions.
- That removes domain terminology as a source of translation error.
- A template-based requirement language makes temporal cues and logical relations explicit.
- Restructuring happens before translation, so the model sees an unambiguous input.
- Outputs are consumed directly by existing verification tools with no manual step.

## Evaluation

- A real aerospace dataset.
- 85% precision and 88% recall in LTL generation.
- Outputs feed existing verification tools directly, which is the practical bar.
- Not reported: dataset size, or how much each of the two innovations contributes.

## Limitations

- Ours: no ablation, so the dictionary and the template language cannot be told apart.
- Ours: 85% precision means roughly one property in seven is wrong yet well-formed.
- Ours: the data dictionary is built per domain, so setup cost transfers to each new project.
- Authors: prior tools fail on complex domain terminology and implicit temporal structure.

## Follow-ups

- Ablate the dictionary against the template language on the same dataset.
- Measure the cost of building a data dictionary for a new domain.
- Compare against the intermediate-representation route, which targets the same failures differently.

## Evidence

> "we present AeroReq2LTL, a framework that automates LTL property generation for aerospace requirements using large language models (LLMs), with two key industrial innovations: (i) a data dictionary that normalizes technical jargon into precise atomic propositions; and (ii) a template-based requirement language that makes temporal cues and logical relations explicit before translation" — abstract
> "On a real aerospace dataset, AeroReq2LTL achieves 85% precision and 88% recall in LTL generation, and its outputs can be directly consumed by existing verification tools." — abstract
> "they often fail on real requirement documents in industrial settings, due to complex domain terminology or implicit temporal and logical structure" — abstract
