# SAGE: Semantic-Aware Gray-Box Game Regression Testing with Large Language Models

- **Citekey:** cai2025sage
- **Record:** arxiv:2512.00560
- **Authors:** Jinyu Cai, Jialong Li, Nianyu Li, Zhenyu Mao et al.
- **Venue:** ASE 2025
- **Categories:** test-generation, bug-detection
- **Link:** http://arxiv.org/abs/2512.00560v2

## Problem

- Live-service games ship often, so regression suites must be rebuilt every iteration.
- Gray-box settings deny source access, which rules out coverage-guided generation.
- Suites grow redundant, and nothing tells the team which tests a given update needs.

## Main ideas

- SAGE covers generation, maintenance, and selection in one framework rather than one of the three.
- LLM-guided reinforcement learning explores the game toward goals, producing the base suite.
- Semantic multi-objective optimisation compacts that suite by balancing cost, coverage, and rarity.
- Update logs are analysed semantically to prioritise tests relevant to each version change.
- Selection is therefore driven by what changed, not by static test metadata.

## Evaluation

- Two environments: Overcooked Plus and Minecraft.
- Compared against automated baselines and human-recorded test cases.
- Better bug detection at lower execution cost, with adaptation across version updates.
- Not reported in the abstract: absolute bug counts or suite sizes.

## Limitations

- Ours: two game environments, one of them a research testbed, so transfer is untested.
- Ours: no absolute numbers in the abstract, only relative direction.
- Ours: rarity as an objective can favour tests that are unusual rather than important.
- Authors: gray-box settings lack source access, which constrains every stage.

## Follow-ups

- Report mutation-style scores so suite compaction can be shown to preserve fault detection.
- Test the update-log prioritisation on a non-game product with a public changelog.
- Separate the reinforcement learning contribution from the semantic selection contribution.

## Evidence

> "It employs LLM-guided reinforcement learning for efficient, goal-oriented exploration to automatically generate a diverse foundational test suite." — abstract
> "it applies a semantic-based multi-objective optimization to refine this suite into a compact, high-value subset by balancing cost, coverage, and rarity" — abstract
> "it leverages LLM-based semantic analysis of update logs to prioritize test cases most relevant to version changes" — abstract
