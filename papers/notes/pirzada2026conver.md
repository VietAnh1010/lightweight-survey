# ConVer: Using Contracts and Loop Invariant Synthesis for Scalable Formal Software Verification

- **Citekey:** pirzada2026conver
- **Record:** arxiv:2605.27051
- **Authors:** Muhammad A. A. Pirzada, Weiqi Wang, Yiannis Charalambous, Konstantin Korovin et al.
- **Venue:** arXiv 2026
- **Categories:** formal-verification, program-logic, specification
- **Link:** http://arxiv.org/abs/2605.27051v1

## Problem

- Bounded model checking of large C programs hits state-space explosion.
- The tool must encode the whole state space up to the bound by unrolling every nested construct.
- Compositional verification avoids this but needs function contracts, which nobody writes.

## Main ideas

- ConVer synthesises the missing contracts with an LLM, taking the top-level assertion as the goal.
- Verification then decomposes top-down instead of unrolling bottom-up.
- System-level and function-level checks alternate inside a CEGAR-CEGIS loop.
- A failed check refines the contracts through SMART ICE learning, so failure is informative.
- The model proposes; the model checker and the learner decide, so no contract is trusted unchecked.
- ESBMC-LF converts Lingua Franca models to C, extending the tool's reach to that benchmark family.

## Evaluation

- Frama-C benchmark, 45 simple C programs: 82-96% success across three LLM backends.
- 93-95% of converged programs need only one CEGAR-CEGIS iteration.
- X.509 parser: 33-50% on 6 programs. LF2C-Simple: 82-88% on 17 programs.
- VerifyThis, 11 recursive and loop-intensive programs: 55-64% with the Pre-Abstraction strategy.
- LF-Hard, transpiled from the LF Verifier Benchmarks: 67% verified.

## Limitations

- Ours: success drops from 82-96% on simple programs to 33-50% on the X.509 parser.
- Ours: the harder suites hold 6 to 17 programs, so those percentages rest on few cases.
- Ours: three backends give a range, which shows the result depends on the model chosen.
- Authors: state-space explosion is the premise, and the top-down split is what avoids it.

## Follow-ups

- Characterise which program shapes defeat contract synthesis, since the X.509 gap is the informative one.
- Compare ICE learning against feeding the counterexample straight back to the model.
- Report verification time, since the single-iteration convergence claim implies a cost argument.

## Evidence

> "it uses a large language model (LLM) to synthesise function contracts from the system property, then alternates system-level and function-level checks in a CEGAR-CEGIS loop, refining contracts whenever a check fails via SMART ICE learning" — abstract
> "On the Frama-C benchmark of 45 simple C programs, ConVer achieves 82-96% verification success across three LLM backends, with 93-95% of converged programs requiring only a single CEGAR-CEGIS iteration." — abstract
> "Formal verification of large C programs is impeded by state-space explosion" — abstract
