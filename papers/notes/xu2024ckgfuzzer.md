# CKGFuzzer: LLM-Based Fuzz Driver Generation Enhanced By Code Knowledge Graph

- **Citekey:** xu2024ckgfuzzer
- **Record:** arxiv:2411.11532
- **Authors:** Hanxiang Xu, Wei Ma, Ting Zhou, Yanjie Zhao et al.
- **Venue:** ICSE 2024
- **Categories:** fuzzing, static-analysis, agents
- **Link:** http://arxiv.org/abs/2411.11532v3

## Problem

- Fuzzing needs drivers, and hand-writing them limits both efficiency and effectiveness.
- A generated driver that does not compile wastes the whole generation.
- Crash reports still need manual review, which dominates the human cost.

## Main ideas

- CKGFuzzer builds a code knowledge graph by interprocedural program analysis.
- Each node is a code entity such as a function or a file, so the graph spans the repository.
- The graph is queried inside the fuzzing loop, not once before it.
- Driver repair, seed synthesis, and crash triage all read from that one structure.
- Fuzz driver creation is framed as code generation, so the agent refines drivers and seeds together.
- API usage scenarios learned from the graph identify what each driver should target.

## Evaluation

- Eight open-source projects.
- Code coverage up 8.73% on average against state-of-the-art techniques.
- Manual review workload in crash analysis reduced by 84.4%.
- 11 real bugs found, nine of them previously unreported.

## Limitations

- Ours: 8.73% coverage gain is modest against the cost of building and querying the graph.
- Ours: the review-workload reduction is measured by the authors, not by external developers.
- Ours: interprocedural analysis must succeed first, which bounds applicable projects.
- Authors: manually crafted drivers limit testing efficiency and effectiveness, the premise.

## Follow-ups

- Report graph construction cost, which is paid once per repository and is not in the coverage figure.
- Separate the driver-repair benefit from the seed-generation benefit.
- Test whether the same graph helps a non-fuzzing client, such as call-graph pruning.

## Evidence

> "The code knowledge graph is constructed through interprocedural program analysis, where each node in the graph represents a code entity, such as a function or a file." — abstract
> "The knowledge graph-enhanced CKGFuzzer not only effectively resolves compilation errors in fuzz drivers and generates input seeds tailored to specific API usage scenarios, but also analyzes fuzz driver crash reports" — abstract
> "CKGFuzzer achieved an average improvement of 8.73% in code coverage compared to state-of-the-art techniques. Additionally, CKGFuzzer reduced the manual review workload in crash case analysis by 84.4%" — abstract
