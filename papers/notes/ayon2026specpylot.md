# SpecPylot: Python Specification Generation using Large Language Models

- **Citekey:** ayon2026specpylot
- **Record:** doi:10.1145/3803437.3806427
- **Authors:** Ragib Shahariar Ayon, Shibbir Ahmed
- **Venue:** FSE 2026
- **Categories:** specification, symbolic-execution
- **Link:** http://arxiv.org/abs/2604.16560v1

## Problem

- Automated verification tools go unused because developers do not write contracts by hand.
- Model-generated specifications fail verification on syntax, over-strict constraints, or wrong behaviour.
- A generated specification with no checker is unfalsifiable: nothing says which of the three it is.

## Main ideas

- SpecPylot emits icontract annotations, which are executable, so a symbolic engine can check them.
- crosshair symbolically explores the program against each candidate contract.
- A concrete counterexample from crosshair drives repair of the contract, never of the program.
- Holding the program fixed makes the loop a specification search, not a joint code-and-spec search.
- Coverage-driven pytest stubs and execution artifacts fall out of the same run.

## Evaluation

- Reports crosshair-compatible contracts for most programs in the evaluation set.
- Not measured: contract strength. Compatibility with the checker is weaker than capturing intent.
- No baseline against hand-written contracts or against unchecked generation is given.

## Limitations

- Authors: bounded symbolic exploration limits what crosshair can refute.
- Authors: results vary with LLM behaviour across runs.
- Ours: a vacuous contract passes crosshair, and nothing reported rules that out.
- Ours: the abstract gives no program count, so 'most programs' has no denominator.

## Follow-ups

- Score contract strength, for example by mutating the program and counting contracts that catch it.
- Let the loop propose a program change when the counterexample shows the code, not the spec, is wrong.
- Compare bounded symbolic execution against property-based testing as the refutation oracle.

## Evidence

> "The tool relies on LLMs to propose candidate contracts and uses crosshair to validate them." — abstract
> "When crosshair finds a concrete counterexample, SpecPylot updates only the generated contracts and leaves the program itself untouched." — abstract
> "it also highlights the practical limits introduced by bounded symbolic exploration and differences in LLM behavior" — abstract
