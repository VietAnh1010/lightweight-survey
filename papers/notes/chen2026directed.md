# Directed Symbolic Execution for Vulnerability Discovery: An LLM-Guided Approach in KLEE

- **Citekey:** chen2026directed
- **Record:** arxiv:2607.21676
- **Authors:** Lingfeng Chen, Tao Xiao, Masanari Kondo, Yasutaka Kamei
- **Venue:** arXiv 2026
- **Categories:** symbolic-execution, bug-detection
- **Link:** http://arxiv.org/abs/2607.21676v1

## Problem

- Symbolic execution finds security violations but suffers path explosion.
- KLEE's path prioritisation optimises coverage, which is not the same as reaching vulnerable code.
- Cyclic control-flow regions absorb the exploration budget before deeper code is reached.

## Main ideas

- KLEECopilot makes the search directed: the model marks code it judges potentially vulnerable.
- Those marks reorder KLEE's path prioritisation toward security-relevant targets.
- Loop-exit prioritisation is a separate mechanism for escaping cycles.
- The model supplies security semantics that a coverage heuristic has no way to express.
- KLEE still performs every constraint solve, so precision is unchanged.

## Evaluation

- Against baselines including Empc: basic block coverage up 42.24%, line coverage up 125.82%.
- 1,335 total violations and 87 unique violations found.
- 32.2% more total violations than the second-best baseline; 24.3% more unique than Empc.
- Ablations over searchers, marking sources, and prompts yield only 54-61 unique violations.

## Limitations

- Authors: results are sensitive to model family, though only marginally to model scale.
- Ours: marks are unverified judgements, so a wrong mark wastes budget silently.
- Ours: violation counts depend on KLEE's checkers, so they measure reachability not exploitability.
- Ours: no cost per campaign is reported, and marking requires model calls.

## Follow-ups

- Report budget spent on paths whose marks proved wrong, which measures the guidance's cost.
- Test whether marks transfer across programs, which would amortise the model calls.
- Combine directed prioritisation with ghost code for solver-hostile fragments.

## Evidence

> "KLEECopilot uses LLMs to mark potentially vulnerable code and guide path prioritization. It also integrates loop-exit prioritization to escape potentially non-vulnerable cycles and progress toward deeper vulnerabilities." — abstract
> "KLEECopilot improves basic block coverage by 42.24% and line coverage by 125.82%. It discovers 1,335 total violations and 87 unique violations" — abstract
> "Although KLEECopilot is sensitive to model family, it exhibits only marginal sensitivity to model scale" — abstract
