# SolSearch: An LLM-Driven Framework for Efficient SAT-Solving Code Generation

- **Citekey:** sheng2025solsearch
- **Record:** arxiv:2502.14328
- **Authors:** Junjie Sheng, Yanqiu Lin, Jiehao Wu, Yanhong Huang et al.
- **Venue:** ICSE 2025
- **Categories:** constraint-solving, program-synthesis
- **Link:** http://arxiv.org/abs/2502.14328v1

## Problem

- SAT solving underlies automated testing, configuration management, and program verification.
- Solver heuristics are hand-designed, and improving them is slow expert work.
- Model-based work targets the problems given to solvers, not the solvers themselves.

## Main ideas

- SolSearch inverts the usual arrangement: the model edits the solver, not the query.
- The model iteratively modifies and generates SAT solver code to improve solving efficiency.
- A curriculum-based trial-and-error process supplies the training signal.
- The result is plug-and-play: any SAT solver can be the starting point.
- The model's output is code that runs without the model, so inference cost stays offline.

## Evaluation

- Improves state-of-the-art SAT solvers on general SAT benchmarks.
- Z3 improves by 11% on PAR-2 score.
- The authors describe the results as preliminary.
- Not reported: search cost, number of curriculum rounds, or variance across runs.

## Limitations

- Authors: the experimental results are preliminary and future work is needed to validate them.
- Ours: PAR-2 on general benchmarks can improve by overfitting to that benchmark distribution.
- Ours: no check that the modified solver remains sound, which is the risk when editing a solver.
- Ours: a four-page New Ideas paper, so the evaluation is thin against the claim's reach.

## Follow-ups

- Check the modified solver against a proof checker, so an unsound speedup cannot pass.
- Report held-out benchmark families to separate real gains from distribution fitting.
- Apply the same loop to SMT theory solvers, where hand-tuned heuristics are also the bottleneck.

## Evidence

> "Leveraging a curriculum-based, trial-and-error process, SolSearch enables the LLM to iteratively modify and generate SAT solver code, thereby improving solving efficiency and performance." — abstract
> "Our preliminary experimental results are encouraging by demonstrating that the LLM-powered paradigm improves state-of-the-art SAT solvers on general SAT benchmarks and significantly enhances the performance of the widely used Z3 solver" — abstract
> "This automated SAT-solving paradigm has the advantage of being plug-and-play, allowing integration with any SAT solver" — abstract
