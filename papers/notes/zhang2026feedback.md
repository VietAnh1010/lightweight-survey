# Feedback-Driven Execution for LLM-Based Binary Analysis

- **Citekey:** zhang2026feedback
- **Record:** arxiv:2604.15136
- **Authors:** XiangRui Zhang, Qiang Li, Haining Wang
- **Venue:** arXiv 2026
- **Categories:** decompilation, bug-detection, agents
- **Link:** http://arxiv.org/abs/2604.15136v1

## Problem

- Binary analysis with models runs one pass over a representation static tools built in advance.
- A fixed representation cannot be extended when an intermediate result suggests where to look next.
- Long-horizon, multi-path analysis then exceeds the context the model can hold.

## Main ideas

- FORGE recasts the analysis as a feedback-driven execution process rather than a single query.
- A reasoning-action-observation loop interleaves model reasoning with tool interaction.
- Exploration is incremental, and evidence is accumulated as the loop proceeds.
- A Dynamic Forest of Agents decomposes the work so each agent's context stays bounded.
- Parallel exploration is coordinated dynamically, which is what keeps long horizons stable.

## Evaluation

- 3,457 real-world firmware binaries.
- 1,274 vulnerabilities identified across 591 unique binaries, at 72.3% precision.
- Broader coverage of vulnerability types than prior approaches.
- Scale here is unusual for this literature; most binary papers evaluate on tens of samples.

## Limitations

- Ours: 72.3% precision means over a quarter of the 1,274 reports are false.
- Ours: no recall figure, so it is unknown what share of real vulnerabilities the loop misses.
- Ours: no cost is reported, and a forest of agents multiplies model calls per binary.
- Authors: long-horizon reasoning is unstable, which is the problem the forest bounds.

## Follow-ups

- Pair reports with a reachability check, as Evident does, to remove the false quarter.
- Report recall on a labelled firmware subset, so precision has a counterpart.
- Measure how forest width trades off against cost and against precision.

## Evidence

> "existing approaches largely adopt a one-pass execution paradigm, where reasoning operates over a fixed program representation constructed by static analysis tools" — abstract
> "FORGE interleaves reasoning and tool interaction through a reasoning-action-observation loop, enabling incremental exploration and evidence construction." — abstract
> "FORGE identifies 1,274 vulnerabilities across 591 unique binaries, achieving 72.3% precision while covering a broader range of vulnerability types than prior approaches." — abstract
