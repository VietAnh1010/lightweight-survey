# Rango: Adaptive Retrieval-Augmented Proving for Automated Software Verification

- **Citekey:** thompson2024rango
- **Record:** arxiv:2412.14063
- **Authors:** Kyle Thompson, Nuno Saavedra, Pedro Carrott, Kevin Fisher et al.
- **Venue:** ICSE 2024
- **Categories:** proof-automation, formal-verification
- **Link:** http://arxiv.org/abs/2412.14063v3

## Problem

- Coq verification needs proofs, and writing them needs expertise and manual effort.
- Prior work shows relevant premises aid synthesis, but selecting them once per theorem is static.
- A proof's context needs change as the proof state evolves, and a fixed context cannot track that.

## Main ideas

- Rango retrieves at every step of the proof, not once per theorem.
- It retrieves two things: relevant premises, and similar proofs from the same project.
- Retrieving proofs, not only lemmas, is the part prior premise-selection work omitted.
- The retrieved context therefore adapts to the project and to the evolving proof state.
- The retriever feeds a fine-tuned model, so retrieval and generation are trained together.

## Evaluation

- CoqStoq: 2,226 open-source Coq projects and 196,929 theorems from GitHub.
- On the curated benchmark of well-maintained projects, Rango proves 32.0% of theorems.
- That is 29% more theorems than Tactician, the prior state of the art.
- Ablation: adding relevant proofs to the context raises theorems proven by 47%.

## Limitations

- Ours: 32.0% leaves two thirds of theorems unproved, so the absolute level remains low.
- Ours: training and evaluation both come from CoqStoq, so project-level overlap needs care.
- Ours: per-step retrieval costs a retrieval query per tactic, and no cost figure is given.
- Authors: verification requires significant expertise and manual effort, which this reduces rather than removes.

## Follow-ups

- Report retrieval cost per proof, since the per-step design multiplies queries by proof length.
- Test on projects absent from CoqStoq to separate adaptation from memorisation.
- Compare per-step retrieval against handing whole lemmas to an agent, as Aria does.

## Evidence

> "Rango uses retrieval augmentation at every step of the proof to automatically determine which proofs and premises to include in the context of its fine-tuned LLM. In this way, Rango adapts to the project and to the evolving state of the proof." — abstract
> "Rango synthesizes proofs for 32.0% of the theorems, which is 29% more theorems than the prior state-of-the-art tool Tactician" — abstract
> "Rango adding relevant proofs to its context leads to a 47% increase in the number of theorems proven" — abstract
