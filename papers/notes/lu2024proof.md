# Proof Automation with Large Language Models

- **Citekey:** lu2024proof
- **Record:** arxiv:2409.14274
- **Authors:** Minghai Lu, Benjamin Delaware, Tianyi Zhang
- **Venue:** ASE 2024
- **Categories:** proof-automation, formal-verification
- **Link:** http://arxiv.org/abs/2409.14274v1

## Problem

- Coq guarantees correctness but demands manual effort and expertise.
- Models write informal proofs well and formal proofs badly, and the reason was not established.
- Without knowing which part fails, a system cannot decide what to automate and what to check.

## Main ideas

- A formative study of 520 GPT-3.5 proof errors supplies the design premise rather than an intuition.
- The finding: the high-level proof structure is usually right, the low-level details usually wrong.
- PALM therefore generates a whole proof first, then repairs it, rather than predicting tactic by tactic.
- Repair uses targeted symbolic methods, so the corrections come from the prover, not the model.
- Repair iterates, so each symbolic fix exposes the next low-level defect.

## Evaluation

- More than 10K theorems.
- 76.6% to 180.4% more theorems proved than state-of-the-art approaches.
- 1270 theorems proved that existing approaches cannot reach.
- Generalizability shown across different LLMs, which separates the method from one model.

## Limitations

- Ours: the formative study used GPT-3.5, so the structure-right details-wrong premise may not hold later.
- Ours: the repair methods are targeted, so unfamiliar low-level failures fall outside their reach.
- Ours: percentage ranges without absolute counts make the baselines hard to place.
- Authors: models are less effective at formal proofs than at informal ones, the gap being attacked.

## Follow-ups

- Repeat the error study on a current model to test whether the structure-details split survives.
- Compare generate-then-repair against agent-driven proving on the same corpus and compute budget.
- Report which symbolic repair rules fire most, which shows where models still fail systematically.

## Evidence

> "By analyzing 520 proof generation errors made by GPT-3.5, we found that GPT-3.5 often identified the correct high-level structure of a proof, but struggled to get the lower-level details correct." — abstract
> "we propose PALM, a novel generate-then-repair approach that first prompts an LLM to generate an initial proof and then leverages targeted symbolic methods to iteratively repair low-level problems" — abstract
> "PALM significantly outperforms other state-of-the-art approaches, successfully proving 76.6% to 180.4% more theorems" — abstract
