# nl2spec: Interactively Translating Unstructured Natural Language to Temporal Logics with Large Language Models

- **Citekey:** cosler2023nl2spec
- **Record:** arxiv:2303.04864
- **Authors:** Matthias Cosler, Christopher Hahn, Daniel Mendoza, Frederik Schmitt et al.
- **Venue:** CAV 2023
- **Categories:** specification, formal-verification
- **Link:** http://arxiv.org/abs/2303.04864v1

## Problem

- Verification needs a formal specification, and writing one by hand is slow and error-prone.
- Natural language requirements are ambiguous, so any single translation silently picks one reading.
- When a whole formula is wrong, the user's only recourse is to redraft it from scratch.

## Main ideas

- nl2spec derives temporal logic formulas from unstructured natural language with an LLM.
- Its methodology maps each subformula back to the natural language fragment it came from.
- These sub-translations make ambiguity visible at the point where the reading was chosen.
- The user adds, deletes, and edits sub-translations rather than rewriting the formalization.
- The framework is domain-agnostic and extends to other specification languages and models.

## Evaluation

- A user study supplies a challenging dataset, which then drives translation-quality experiments.
- Open-source implementation with a web frontend is provided.
- Not measured in the abstract: how much the sub-translation interface reduces user effort.
- The dataset is built by the same study that motivates the tool, so it is not independent.

## Limitations

- Ours: this is interactive, not automatic; the user remains in the loop for every ambiguity.
- Ours: a sub-translation is only as trustworthy as the mapping the model produced for it.
- Ours: no accuracy figure appears in the abstract, only the existence of experiments.
- Authors: writing formal specifications remains error-prone and time-consuming, the premise they attack.

## Follow-ups

- Compare sub-translation editing against whole-formula redrafting in a controlled user study.
- Check sub-translations against each other for consistency, as ARc does for whole formalizations.
- Apply the mapping idea to code contracts, where the fragment is a statement rather than a phrase.

## Evidence

> "we utilize LLMs to map subformulas of the formalization back to the corresponding natural language fragments of the input" — abstract
> "Users iteratively add, delete, and edit these sub-translations to amend erroneous formalizations, which is easier than manually redrafting the entire formalization." — abstract
> "We perform a user study to obtain a challenging dataset, which we use to run experiments on the quality of translations." — abstract
