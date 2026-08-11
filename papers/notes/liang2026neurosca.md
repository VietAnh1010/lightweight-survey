# NeuroSCA: Neuro-Symbolic Constraint Abstraction for Smart Contract Hybrid Fuzzing

- **Citekey:** liang2026neurosca
- **Record:** arxiv:2603.01272
- **Authors:** Haochen Liang, Jiawei Chen, Hideya Ochiai
- **Venue:** arXiv 2026
- **Categories:** fuzzing, symbolic-execution, constraint-solving
- **Link:** http://arxiv.org/abs/2603.01272v1

## Problem

- Hybrid fuzzing pairs greybox throughput with symbolic precision to reach deep contract bugs.
- Path conditions collect semantic noise from global state and defensive checks.
- That noise is syntactically entangled with the target branch, so SMT queries time out.

## Main ideas

- NeuroSCA inserts the model as a semantic constraint abstraction layer, selectively.
- The model picks a small core of goal-relevant constraints out of the polluted path condition.
- Only that abstraction is handed to the SMT solver, which is why solving speeds up.
- Models are validated by concrete execution, so an over-aggressive abstraction is caught.
- A verifier-in-the-loop mechanism reintroduces missed constraints, which preserves soundness.
- A selective invocation policy keeps easy contracts on the unmodified path.

## Evaluation

- Real-world contracts, split into polluted and easy paths.
- Faster solving on polluted paths, with higher coverage and bug-finding rates on hard contracts.
- Modest overhead, and no loss of effectiveness on easy contracts.
- The selective policy is evaluated as a component, not assumed.

## Limitations

- Ours: soundness is preserved by refinement, so the guarantee depends on the validation catching every drop.
- Ours: no absolute coverage or bug counts appear in the abstract.
- Ours: constraint relevance is judged by a model with no explanation of its criterion.
- Authors: constraint pollution comes from global state and defensive checks, which the abstraction targets.

## Follow-ups

- State the soundness argument formally: what refinement guarantees no reachable path is lost.
- Report how often refinement fires, which measures how often the abstraction was wrong.
- Apply constraint abstraction outside smart contracts, where pollution also causes timeouts.

## Evidence

> "NeuroSCA uses the LLM to identify a small core of goal-relevant constraints, solves only this abstraction with an SMT solver, and validates models via concrete execution in a verifier-in-the-loop refinement mechanism that reintroduces any missed constraints and preserves soundness." — abstract
> "its effectiveness is often limited by constraint pollution: in real world contracts, path conditions pick up semantic noise from global state and defensive checks" — abstract
> "through its selective invocation policy, achieves these gains with only modest overhead and no loss of effectiveness on easy contracts" — abstract
