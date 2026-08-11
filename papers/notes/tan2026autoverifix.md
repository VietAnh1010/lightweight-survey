# AutoVeriFix+: High-Correctness RTL Generation via Trace-Aware Causal Fix and Semantic Redundancy Pruning

- **Citekey:** tan2026autoverifix
- **Record:** arxiv:2603.11489
- **Authors:** Yan Tan, Xiangchen Meng, Zijun Jiang, Yangdi Lyu
- **Venue:** arXiv 2026
- **Categories:** symbolic-execution, test-generation, program-synthesis
- **Link:** http://arxiv.org/abs/2603.11489v1

## Problem

- Verilog generation suffers from scarce high-quality training data.
- Current approaches chase syntactic correctness and ship functional errors.
- A syntactically valid circuit with wrong state transitions passes every syntax check.

## Main ideas

- Stage one generates a Python reference model that states the intended circuit behaviour.
- Having a reference in a well-supported language gives the pipeline an oracle it otherwise lacks.
- Stage two generates Verilog candidates and iteratively fixes syntax errors.
- Stage three runs a concolic testing engine over deep sequential logic for corner cases.
- Cycle-accurate traces and register snapshots give the model causal context for state-transition errors.
- A coverage report identifies redundant branches, which drives semantic pruning for area.

## Evaluation

- Over 80% functional correctness on the rigorous benchmarks used.
- pass@10 of 90.2% on VerilogEval-machine.
- 25% of redundant logic eliminated on average through trace-aware optimization.
- Correctness and area are reported together, which matches what hardware design optimises.

## Limitations

- Ours: the Python reference is model-generated, so a wrong reference makes the oracle wrong.
- Ours: pass@10 allows ten attempts, which overstates single-shot reliability.
- Ours: no ablation separates the concolic engine from the trace feedback.
- Authors: Verilog generation is hampered by the scarcity of high-quality training data.

## Follow-ups

- Validate the Python reference independently, since every later stage depends on it.
- Report pass@1 alongside pass@10 for a single-shot reliability figure.
- Test whether trace-derived causal context helps software repair, where traces are also available.

## Evidence

> "In the first stage, an LLM is employed to generate high-level Python reference models that define the intended circuit behavior." — abstract
> "With cycle-accurate execution traces and internal register snapshots, AutoVeriFix+ provides the LLM with the causal context necessary to resolve complex state-transition errors." — abstract
> "AutoVeriFix+ achieves over 80% functional correctness on rigorous benchmarks, reaching a pass@10 score of 90.2% on the VerilogEval-machine dataset" — abstract
