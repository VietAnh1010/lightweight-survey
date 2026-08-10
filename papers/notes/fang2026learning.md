# A Learning Method for Symbolic Systems Using Large Language Models

- **Citekey:** fang2026learning
- **Record:** arxiv:2605.08694
- **Authors:** Jian Fang, Yixun Yao, Yingfei Xiong
- **Venue:** arXiv 2026
- **Categories:** proof-automation, formal-verification
- **Link:** http://arxiv.org/abs/2605.08694v1

## Problem

- End-to-end neural provers are expensive to run and opaque about why a proof succeeded.
- Symbolic provers are cheap and inspectable but cannot improve themselves from a proof corpus.
- Nothing connects the two: the corpus of formal proofs does not feed back into the symbolic tools.

## Main ideas

- LLM2Ltac uses the model as a synthesizer of tactics, not as a prover.
- It asks the model to identify latent proof strategies in a corpus and formalize them as tactics.
- Mined tactics are checked for validity and generalizability before they are kept.
- Surviving tactics are integrated into symbolic provers, so proving costs no model calls.
- The model is paid for once, offline; the improvement it produces is a permanent symbolic artifact.

## Evaluation

- Tactics mined from 11,725 theorems in the Rocq 8.20.0 standard library.
- Evaluated on 6,199 theorems from compcert, Coq-Art, Ext-Lib, and VFA.
- CoqHammer proves 23.87% more theorems with the mined tactics.
- Improved CoqHammer combined with Claude Code raises the total proved by a further 9.90%.

## Limitations

- Ours: mining and evaluation both draw on Rocq, so cross-prover transfer is untested.
- Ours: no count of mined tactics or of those rejected by the validity check is reported.
- Ours: gains are relative to CoqHammer, not to an end-to-end neural prover on the same theorems.
- Authors: end-to-end LLM provers are resource-intensive and opaque, the cost this design avoids.

## Follow-ups

- Report how many mined tactics survive validation, which measures the yield of the mining step.
- Mine tactics from project corpora rather than the standard library, and test domain specialization.
- Compare against retrieval-based proving on equal compute, since both reuse a corpus.

## Evidence

> "LLM2Ltac, the first approach that leverages the reasoning power of LLMs not as end-to-end provers, but as intelligent synthesizers to mine purely symbolic tactics from data" — abstract
> "These tactics are verified for validity and generalizability, and finally integrated into symbolic provers to enhance their automated proving capabilities without the runtime cost of LLMs." — abstract
> "Results show that the mined tactics improve CoqHammer to prove 23.87% more theorems" — abstract
