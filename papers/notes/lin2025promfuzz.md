# PromFuzz: Leveraging LLM-Driven and Bug-Oriented Composite Analysis for Detecting Functional Bugs in Smart Contracts

- **Citekey:** lin2025promfuzz
- **Record:** doi:10.1109/ase63991.2025.00091
- **Authors:** Xingshuang Lin, Qinge Xie, Binbin Zhao, Yuan Tian et al.
- **Venue:** ASE 2025
- **Categories:** fuzzing, bug-detection, specification
- **Link:** https://doi.org/10.1109/ase63991.2025.00091

## Problem

- Over 80% of exploitable smart contract bugs are functional and evade current tools.
- The gap is between the business model's high-level logic and the low-level implementation.
- Detecting these bugs requires oracles generated automatically from bug features.

## Main ideas

- PromFuzz composes three stages rather than detecting in one pass.
- A dual-agent strategy first pinpoints functions worth scrutinising.
- A dual-stage coupling approach generates invariant checkers from those functions' logic.
- The checkers are the oracles, which is what functional bug detection previously lacked.
- A bug-oriented fuzzing engine maps business-model logic onto the implementation.
- Fuzzing is directed at the targeted functions rather than the whole contract.

## Evaluation

- 86.96% recall and 93.02% F1 on functional bug detection.
- At least 50% improvement in both metrics over state-of-the-art methods.
- 30 zero-day bugs found in real DeFi projects; 24 have CVE IDs.
- CVE assignment is an external oracle, stronger than benchmark scoring.

## Limitations

- Ours: generated invariant checkers are unverified, so a wrong checker yields a wrong verdict.
- Ours: recall is measured against a known bug set, so unrepresented bug shapes stay invisible.
- Ours: the first stage is prompt engineering, so that part fails the swap-the-model test.
- Authors: the primary issue is the gap between high-level logic and low-level implementation.

## Follow-ups

- Check generated invariants against known-good contract executions before fuzzing with them.
- Report how many candidate functions the first stage discards, which bounds recall.
- Compare invariant-checker oracles against property retrieval, which solves the same oracle problem.

## Evidence

> "we first propose a novel Large Language Model (LLM)-driven analysis framework, which leverages a dual-agent prompt engineering strategy to pinpoint potentially vulnerable functions for further scrutiny" — abstract
> "we design a bug-oriented fuzzing engine, which maps the logical information from the high-level business model to the low-level smart contract implementations, and performs the bug-oriented fuzzing on targeted functions" — abstract
> "we perform an in-depth analysis on real-world DeFi projects and detect 30 zero-day bugs. Up to now, 24 zero-day bugs have been assigned CVE IDs." — abstract
