# $λ_A$: A Typed Lambda Calculus for LLM Agent Composition

- **Citekey:** liu2026typed
- **Record:** arxiv:2604.11767
- **Authors:** Qin Liu
- **Venue:** arXiv 2026
- **Categories:** program-logic, static-analysis, agents
- **Link:** http://arxiv.org/abs/2604.11767v2

## Problem

- Agent frameworks have no formal semantics.
- Nothing decides whether an agent configuration is well-formed or whether it terminates.
- Configuration is split between declarative files and imperative code, so neither alone is checkable.

## Main ideas

- The calculus extends simply-typed lambda calculus with the four features agents need.
- Those are oracle calls, bounded fixpoints for the ReAct loop, probabilistic choice, and mutable environments.
- Type safety, termination of bounded fixpoints, and lint-rule soundness are all proved.
- The proofs are mechanized in Coq: 1,519 lines, 42 theorems, nothing admitted.
- The lint tool is derived from the operational semantics rather than written by hand.
- Five mainstream frameworks embed as typed fragments, so the calculus is a common target.

## Evaluation

- 835 real-world GitHub agent configurations: 94.1% are structurally incomplete under the calculus.
- Lint precision is 54% on YAML alone, rising to 96-100% with joint YAML and Python AST analysis.
- That gap quantifies how much configuration meaning sits in imperative code.
- LangGraph, CrewAI, AutoGen, the OpenAI SDK, and Dify are all shown to embed.

## Limitations

- Ours: the artefact analysed is an agent configuration, not a program under test.
- Ours: structural incompleteness at 94.1% may say more about the calculus's strictness than about the configs.
- Ours: the joint analysis needs both files, so single-file linting stays at 54% precision.
- Authors: existing frameworks lack formal semantics, which is the gap rather than a measured defect.

## Follow-ups

- Report what fraction of the 94.1% correspond to real runtime failures.
- Extend the calculus to model tool side effects, which mutable environments only partly capture.
- Use the type system to reject unsafe configurations before deployment, not only to lint them.

## Evidence

> "We present $λ_A$, a typed lambda calculus for agent composition that extends the simply-typed lambda calculus with oracle calls, bounded fixpoints (the ReAct loop), probabilistic choice, and mutable environments." — abstract
> "We prove type safety, termination of bounded fixpoints, and soundness of derived lint rules, with full Coq mechanization (1,519 lines, 42 theorems, 0 Admitted)." — abstract
> "An evaluation on 835 real-world GitHub agent configurations shows that 94.1% are structurally incomplete under $λ_A$, with YAML-only lint precision at 54%, rising to 96--100% under joint YAML+Python AST analysis on 175 samples." — abstract
