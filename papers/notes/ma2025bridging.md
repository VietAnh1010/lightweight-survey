# Bridging Natural Language and Formal Specification--Automated Translation of Software Requirements to LTL via Hierarchical Semantics Decomposition Using LLMs

- **Citekey:** ma2025bridging
- **Record:** doi:10.1109/ase63991.2025.00104
- **Authors:** Zhi Ma, Cheng Wen, Zhexin Su, Xiao Liang et al.
- **Venue:** ASE 2025
- **Categories:** specification, formal-verification
- **Link:** http://arxiv.org/abs/2512.17334v1

## Problem

- Scaling formal verification to industry needs requirements translated into formal specifications.
- Rule-based and learning-based translators both fail on real industrial requirements.
- Models extract semantics well but stumble on complexity, ambiguity, and logical depth.

## Main ideas

- Req2LTL routes the translation through OnionL, a hierarchical intermediate representation.
- The model is restricted to semantic decomposition into that representation.
- Deterministic rule-based synthesis then produces the LTL from OnionL.
- Syntactic validity comes from the rules, so the model cannot emit a malformed formula.
- Splitting decomposition from synthesis is what separates the two failure modes.

## Evaluation

- Real-world aerospace requirements.
- 88.4% semantic accuracy and 100% syntactic correctness.
- 100% syntactic correctness follows from the design, so it confirms rather than surprises.
- Significantly outperforms existing methods, per the authors.

## Limitations

- Ours: 88.4% semantic accuracy means one requirement in nine is formalised wrongly.
- Ours: a wrong formula that is syntactically valid is harder to spot than a malformed one.
- Ours: one domain, aerospace, and no dataset size in the abstract.
- Authors: models struggle with the complexity, ambiguity, and logical depth of real requirements.

## Follow-ups

- Check formalisations against each other for equivalence, as the ambiguity-auditing work does.
- Report which requirement shapes cause the 11.6% semantic failures.
- Test whether OnionL transfers to a domain without aerospace's controlled vocabulary.

## Evidence

> "we propose Req2LTL, a modular framework that bridges NL and Linear Temporal Logic (LTL) through a hierarchical intermediate representation called OnionL" — abstract
> "Req2LTL leverages LLMs for semantic decomposition and combines them with deterministic rule-based synthesis to ensure both syntactic validity and semantic fidelity." — abstract
> "Req2LTL achieves 88.4% semantic accuracy and 100% syntactic correctness on real-world aerospace requirements" — abstract
