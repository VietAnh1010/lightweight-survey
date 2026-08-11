# CHAINTRIX: A multi-pipeline LLM-augmented framework for automated smart-contract security auditing

- **Citekey:** dobrita2026chaintrix
- **Record:** arxiv:2605.09350
- **Authors:** Gabriela Dobrita, Simona-Vasilica Oprea, Adela Bara
- **Venue:** arXiv 2026
- **Categories:** bug-detection, static-analysis, symbolic-execution
- **Link:** http://arxiv.org/abs/2605.09350v1

## Problem

- Smart contract exploits cost billions, and manual audits are slow and expensive.
- Static analysers report findings that fail manual triage at high rates.
- Models hallucinate findings that contradict the source code they claim to describe.

## Main ideas

- Chaintrix commits architecturally: every model-generated claim is discharged against structure.
- The Cross-Contract Interaction Model parses Solidity into function-level reads, writes, and modifiers.
- Cross-contract calls are resolved, so the substrate spans contract boundaries.
- All 12 deterministic signal engines and the parallel model pipelines read the same substrate.
- A Structural Verdict Engine applies deterministic checks as the last false-positive filter.
- High-confidence findings are then validated by symbolic execution and fuzz testing.

## Evaluation

- EVMbench, the smart-contract security benchmark from OpenAI, Paradigm, and OtterSec.
- 86 of 120 high-severity vulnerabilities detected, 71.7% recall.
- 25 audits score 100% recall.
- 26 percentage points above the strongest frontier-model baseline.

## Limitations

- Ours: recall is reported without precision, so the triage burden is unknown.
- Ours: 34 of 120 high-severity vulnerabilities are still missed.
- Ours: the structural substrate bounds what can be discharged, so novel bug shapes escape it.
- Authors: the two failure modes named are analyser triage cost and model hallucination.

## Follow-ups

- Report precision alongside recall; the design is a false-positive pipeline and should be scored as one.
- Characterise the 34 misses, which is where the structural substrate is too coarse.
- Test whether the discharge-against-structure commitment transfers outside Solidity.

## Evidence

> "we propose Chaintrix, an end-to-end auditing framework whose central architectural commitment is that every LLM-generated claim must be discharged against a deterministic structural contract representation" — abstract
> "A staged false-positive-reduction pipeline, terminating in a Structural Verdict Engine (SVE) that applies deterministic structural checks against parsed code, filters the merged finding set, with selected high-confidence findings further validated through symbolic execution and fuzz testing." — abstract
> "Chaintrix detects 86 of 120 high-severity vulnerabilities (71.7% recall), with 25 audits scoring 100% recall, placing Chaintrix 26 percentage points above the strongest frontier-model baseline." — abstract
