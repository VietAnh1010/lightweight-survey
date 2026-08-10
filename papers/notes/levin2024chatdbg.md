# ChatDBG: Augmenting Debugging with Large Language Models

- **Citekey:** levin2024chatdbg
- **Record:** doi:10.1145/3729355
- **Authors:** Kyla H. Levin, Nicolas van Kempen, Emery D. Berger, Stephen N. Freund
- **Venue:** FSE 2024
- **Categories:** bug-detection, program-repair, agents
- **Link:** http://arxiv.org/abs/2403.16354v5

## Problem

- Debugging requires questions about program state that source text alone cannot answer.
- A model reading source can only guess at runtime values such as why a variable is null.
- Conventional debuggers expose that state but require the programmer to drive them.

## Main ideas

- ChatDBG gives the model control of the debugger rather than a transcript of it.
- The model acts as an agent that queries and controls the debugger to navigate stacks and inspect state.
- Root-cause claims therefore rest on observed program state, not on reading the source.
- Control returns to the programmer once the model reports its findings.
- It integrates with standard debuggers: LLDB and GDB for native code, Pdb for Python.

## Evaluation

- C and C++ code with known bugs, plus Python scripts and Jupyter notebooks.
- Python: a single query yields an actionable fix 67% of the time, 85% with one follow-up.
- Adoption reported: over 75,000 downloads.
- Not measured: how often the model's debugger commands are wrong, or the cost of a session.

## Limitations

- Ours: the reported 67% and 85% are for Python only; the C and C++ result is stated qualitatively.
- Ours: an actionable fix judged by the authors is not the same as a verified correct fix.
- Ours: download count measures uptake, not correctness, and appears alongside the accuracy claims.
- Authors: the approach depends on real-world knowledge embedded in the model for domain reasoning.

## Follow-ups

- Report per-language accuracy with an independent oracle, such as the project's test suite.
- Measure whether debugger autonomy beats simply pasting a stack trace and locals into the prompt.
- Instrument which debugger commands the agent issues, to find where autonomy pays.

## Evidence

> "ChatDBG grants the LLM autonomy to \"take the wheel\": it can act as an independent agent capable of querying and controlling the debugger to navigate through stacks and inspect program state" — abstract
> "For the Python programs, a single query led to an actionable bug fix 67% of the time; one additional follow-up query increased the success rate to 85%." — abstract
> "Our ChatDBG prototype integrates with standard debuggers including LLDB and GDB for native code and Pdb for Python." — abstract
