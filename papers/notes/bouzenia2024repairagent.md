# RepairAgent: An Autonomous, LLM-Based Agent for Program Repair

- **Citekey:** bouzenia2024repairagent
- **Record:** arxiv:2403.17134
- **Authors:** Islem Bouzenia, Premkumar Devanbu, Michael Pradel
- **Venue:** ICSE 2024
- **Categories:** program-repair, agents
- **Link:** http://arxiv.org/abs/2403.17134v2

## Problem

- Repair pipelines fix the control flow in advance: one prompt, or one prompt-validate loop.
- A fixed loop cannot spend more effort on a bug that needs more investigation.
- The order in which to gather context, propose a fix, and validate it depends on the bug.

## Main ideas

- RepairAgent treats the model as an agent that plans and invokes tools rather than filling a template.
- A tool set specific to repair covers bug investigation, ingredient gathering, and fix validation.
- A finite state machine constrains which tools the agent may invoke next, bounding the search.
- The prompt format is rewritten as the run proceeds, carrying tool results and past attempt feedback.
- The agent interleaves the three activities freely instead of running them in a fixed order.

## Evaluation

- Defects4J: 164 bugs repaired autonomously, including 39 not fixed by prior techniques.
- Cost reported: about 270,000 tokens per bug, roughly 14 US cents at GPT-3.5 pricing.
- Not measured: how much the finite state machine contributes relative to free tool choice.
- No ablation of the tool set is reported in the abstract.

## Limitations

- Ours: Defects4J predates the model's training cutoff, so leakage is not ruled out here.
- Ours: 'repaired' on Defects4J means test-suite passing, which admits overfitted patches.
- Ours: the finite state machine is hand-designed, so the fixed control flow moved rather than left.
- Authors: cost per bug is reported but not compared against the cost of the fixed-loop baselines.

## Follow-ups

- Ablate the state machine to separate the value of tools from the value of constraining their order.
- Replace test-suite passing with a specification oracle, as the Dafny repair work does.
- Learn the state machine from successful trajectories rather than hand-writing it.

## Evidence

> "Unlike existing deep learning-based approaches, which prompt a model with a fixed prompt or in a fixed feedback loop, our work treats the LLM as an agent capable of autonomously planning and executing actions to fix bugs by invoking suitable tools." — abstract
> "Key contributions that enable RepairAgent include a set of tools that are useful for program repair, a dynamically updated prompt format that allows the LLM to interact with these tools, and a finite state machine that guides the agent in invoking the tools." — abstract
> "repairing 164 bugs, including 39 bugs not fixed by prior techniques" — abstract
