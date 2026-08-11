# AoA: Theorem Proving Agent over Abstract Syntax Tree of Redesigned Language

- **Citekey:** xu2026aoa
- **Record:** arxiv:2607.16372
- **Authors:** Qiyuan Xu, Joshua Ong Jun Leang, Renxi Wang, Wenda Li et al.
- **Venue:** arXiv 2026
- **Categories:** proof-automation, agents
- **Link:** http://arxiv.org/abs/2607.16372v1

## Problem

- Proof agents consume many tokens and cost a great deal in API calls.
- The cause is shared: agents write proofs as source text and query state by line number.
- Every edit shifts later lines, forcing repeated relocation of errors and proof states.
- The same dependence on concrete syntax blocks adoption of proof languages too new to be pretrained on.

## Main ideas

- AoA lifts the agent off source text and onto the abstract syntax tree.
- Proofs are supplied as JSON representations of the language's AST, which tool-calling models emit natively.
- A tree-edit model drives the prover, fusing proof operations and states into one proof tree.
- Each operation therefore carries its own subgoal's state, readable straight off the tree.
- No line numbers exist, so no edit can invalidate a later reference.
- The AST route also sidesteps the model's unfamiliarity with a new proof language's surface syntax.

## Evaluation

- Against Amazon's Isabelle Agent on miniF2F and NTP4VC-Pearl common success sets.
- API cost down 2.3-4.7x under normalized input-cache accounting.
- Tokens down 2.9-6.9x, tool calls down 3.9-8.9x, wall-clock 1.4-2.0x faster.
- Solves far more problems on the harder verification benchmark.

## Limitations

- Ours: cost comparisons are on common success sets, which excludes problems only one system solves.
- Ours: the approach needs a proof language with an exposed, stable AST.
- Ours: no absolute solve rate is given, only relative gains and a qualitative claim.
- Authors: heavy token consumption and API cost are the obstacle, which this reduces rather than removes.

## Follow-ups

- Report absolute solve rates, not only cost on common successes.
- Test whether AST-level interaction helps agents editing ordinary code, where line drift is the same problem.
- Measure how much of the gain comes from the tree-edit model against the JSON encoding.

## Evidence

> "current agents operate on serialized concrete syntax, emitting proofs as source text and recovering proof states through separate, line-number-based queries, so every edit shifts later lines and forces repeated relocation of errors and states" — abstract
> "the model supplies proofs as JSON representations of Minilang's AST -- native to tool-calling LLMs -- and drives the prover through a tree-edit model that fuses proof operations and states into one proof tree, so each operation carries its own subgoal's state, readable directly off the tree" — abstract
> "AoA cuts API cost by 2.3--4.7x (normalized input-cache accounting), uses 2.9--6.9x fewer tokens and 3.9--8.9x fewer tool calls, and finishes 1.4--2.0x faster" — abstract
