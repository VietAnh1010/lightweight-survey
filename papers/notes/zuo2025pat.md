# PAT-Agent: Autoformalization for Model Checking

- **Citekey:** zuo2025pat
- **Record:** arxiv:2509.23675
- **Authors:** Xinyue Zuo, Yifan Zhang, Hongshu Wang, Yufan Cai et al.
- **Venue:** ASE 2025
- **Categories:** formal-verification, proof-automation, agents
- **Link:** http://arxiv.org/abs/2509.23675v1

## Problem

- Specification languages are complex, which blocks non-experts from model checking.
- Model output can be hallucinated, and the semantic gap to formal logic is wide.
- A generated formal model that is syntactically fine may still not mean what was intended.

## Main ideas

- PAT-Agent separates planning from code generation, giving each stage one job.
- A Planning LLM extracts key modeling elements and writes a detailed plan from semantic prompts.
- A Code Generation LLM then synthesises the formal model under that plan.
- The PAT model checker verifies the result against user-specified properties.
- A repair loop triggers on discrepancy and corrects the model using counterexamples.
- A web interface lets non-experts describe and verify behaviours interactively.

## Evaluation

- 40 systems; consistently outperforms baselines with high verification success and better efficiency.
- Ablation studies confirm both the planning and the repair components matter.
- A user study shows the interface works for users with limited formal methods experience.
- Ablations plus a user study is unusually complete for this literature.

## Limitations

- Ours: 40 systems is a modest evaluation for an end-to-end autoformalization claim.
- Ours: verification success measures the model checker accepting, not the model matching intent.
- Ours: user-specified properties are assumed correct, so the specification burden only moves.
- Authors: hallucinated output and the semantic gap remain the standing risks.

## Follow-ups

- Check the synthesised model against the natural language independently, as ambiguity audits do.
- Report how many repair iterations are needed, which sizes the counterexample loop's cost.
- Test whether the planning stage transfers to other model checkers besides PAT.

## Evidence

> "In PAT-Agent, a Planning LLM first extracts key modeling elements and generates a detailed plan using semantic prompts, which then guides a Code Generation LLM to synthesize syntactically correct and semantically faithful formal models." — abstract
> "The resulting code is verified using the Process Analysis Toolkit (PAT) model checker against user-specified properties, and when discrepancies occur, a Repair Loop is triggered to iteratively correct the model using counterexamples." — abstract
> "The ablation studies confirm the importance of both planning and repair components, and the user study demonstrates that our interface is accessible" — abstract
