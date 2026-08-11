# Prompt-tuned Code Language Model as a Neural Knowledge Base for Type Inference in Statically-Typed Partial Code

- **Citekey:** huang2022prompt
- **Record:** doi:10.1145/3551349.3556912
- **Authors:** Qing Huang, Zhiqiang Yuan, Zhenchang Xing, Xiwei Xu et al.
- **Venue:** ASE 2022
- **Categories:** static-analysis
- **Link:** https://doi.org/10.1145/3551349.3556912

## Problem

- Partial code carries type names that are not fully qualified and undeclared receiving objects.
- Resolving those names is a precondition for searching and reusing the snippet.
- Dictionary-lookup methods need compilation and break on unseen API names or context changes.

## Main ideas

- Type inference is recast as a cloze-style fill-in-the-blank language task.
- A code masked language model is prompt-tuned to serve as a neural knowledge base of code elements.
- The pre-train, prompt, and predict paradigm is driven from raw source code, needing no symbolic base.
- Fully-qualified-name syntax and usage are packed into model parameters rather than a lookup table.
- The result is fuzzy neural type inference that tolerates unseen names.
- Compilation requirements drop to a minimum, which is what makes partial code tractable.

## Evaluation

- Source code from GitHub and Stack Overflow, at scale.
- Results confirm effectiveness and practicality for partial code type inference.
- The authors describe the method as the first of its kind.
- No comparison numbers appear in the abstract, only a qualitative confirmation.

## Limitations

- Ours: fuzzy inference gives no soundness guarantee, unlike the symbolic methods it replaces.
- Ours: no accuracy figures in the abstract, so the trade against dictionary lookup is unquantified.
- Ours: knowledge is in the parameters, so a new API version needs retraining rather than an update.
- Authors: existing methods carry compilation overhead and break on context variation.

## Follow-ups

- Check inferred fully-qualified names against a build, converting a guess into a verified claim.
- Measure decay as libraries evolve past the training cutoff, which parameter-stored knowledge suffers.
- Compare against retrieval over an API index, which updates without retraining.

## Evidence

> "we formulate type inference as a cloze-style fill-in-blank language task" — abstract
> "our prompt-tuned code MLM packs FQN syntax and usage in its parameters and supports fuzzy neural type inference" — abstract
> "Our approach is lightweight and has minimum requirements on code compilation." — abstract
