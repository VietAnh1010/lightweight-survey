# Harnessing Code Agents for Automatic Software Verification

- **Citekey:** kan2026harnessing
- **Record:** arxiv:2607.06341
- **Authors:** Shuangxiang Kan, Shuanglong Kan, Sebastian Ertel
- **Venue:** arXiv 2026
- **Categories:** proof-automation, formal-verification, program-logic, agents
- **Link:** http://arxiv.org/abs/2607.06341v1

## Problem

- Interactive theorem proving does not scale: Coq proofs demand enormous expert effort.
- Existing LLM provers hardwire a human-designed proof strategy and force the model to follow it.
- Step-wise tactic prediction and divide-and-conquer both prove only a fraction of their targets.

## Main ideas

- Aria's claim is negative and structural: the imposed strategy is what limits the prior systems.
- A general code agent receives the whole lemma and chooses its own approach.
- A verification harness supplies feedback and hard constraints instead of a proof strategy.
- The harness enforces three properties: soundness, completeness, and termination.
- Soundness means acceptance only when the prover's kernel closes the proof, so the agent cannot bluff.
- Completeness means no obligation may be left unproved or silently dropped.

## Evaluation

- Iris core logic: all 4,257 lemmas of four core modules proved, plus 217 for Rust's standard libraries.
- reglang: all 318 lemmas proved, where prior provers manage roughly one in eight.
- iris-lean: 72 not-yet-ported lemmas proved, so the approach is not Coq-specific.
- No Coq expert intervention is reported for any of the three.

## Limitations

- Ours: full coverage on a chosen corpus is not the same as full coverage on arbitrary lemmas.
- Ours: no cost per lemma is reported, and a frontier model with agent scaffolding is expensive.
- Ours: Iris lemmas come with an existing proof in the repository, so leakage is not ruled out.
- Authors: the result is tied to a state-of-the-art model, which they name explicitly.

## Follow-ups

- Report token and wall-clock cost per lemma, so the harness can be compared against step-wise provers.
- Run on lemmas with no published proof, which removes the leakage question the corpora raise.
- Test which of the three harness constraints is doing the work by relaxing each in turn.

## Evidence

> "existing approaches wire a fixed, human-designed proof strategy into the system and constrain the model to follow it (retrieving premises and predicting tactics one step at a time, or splitting goals by divide-and-conquer), and still prove only a fraction of their target theorems" — abstract
> "The agent writes the proofs under feedback and hard constraints from the harness that keep each one sound (accepted only when the prover's kernel closes it), complete (no obligation left unproved or silently dropped), and terminating (no divergent tactics)." — abstract
> "Aria proves all 4,257 lemmas of the four core modules and the 217 lemmas verifying Rust's standard libraries built on it, fully automatically" — abstract
