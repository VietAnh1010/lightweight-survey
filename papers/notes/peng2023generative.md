# Generative Type Inference for Python

- **Citekey:** peng2023generative
- **Record:** arxiv:2307.09163
- **Authors:** Yun Peng, Chaozheng Wang, Wenxuan Wang, Cuiyun Gao et al.
- **Venue:** ASE 2023
- **Categories:** static-analysis
- **Link:** http://arxiv.org/abs/2307.09163v1

## Problem

- Rule-based type inference for Python is accurate but covers few variables.
- Supervised inference needs large annotated datasets and cannot leave its predefined type set.
- Cloze-style zero-shot reformulations avoid annotation but perform poorly.

## Main ideas

- TypeGen makes the static analysis derivation itself the prompt, not just its conclusion.
- Type dependency graphs give the inference steps; those steps become chain-of-thought prompt text.
- The model therefore imitates how the analysis reaches a type rather than guessing the type.
- Code slices and type hints accompany the chain of thought in each example prompt.
- Five annotated examples suffice, because the examples teach a procedure rather than a type set.
- An input-explanation-output format leaves an explanation with each prediction.

## Evaluation

- Beats Type4Py by 10.0% on argument types and 22.5% on return types, top-1 exact match, with five examples.
- 27% to 84% above zero-shot performance of models from 1.3B to 175B parameters.
- Spanning 1.3B to 175B separates the method's contribution from model scale.
- Not measured: whether the generated explanations are faithful to the actual inference.

## Limitations

- Ours: the chain of thought imitates an analysis but inherits no soundness from it.
- Ours: an explanation that reads well is not evidence the model followed those steps.
- Ours: type dependency graphs must be built first, so the analysis cost remains.
- Authors: rule-based approaches have low coverage and supervised ones are limited to predefined types.

## Follow-ups

- Check predicted types against a type checker, converting the output into a verifiable claim.
- Test whether the derivation-as-prompt idea transfers to points-to or nullability analysis.
- Measure explanation faithfulness by perturbing the graph and seeing whether the chain changes.

## Evidence

> "TypeGen creates chain-of-thought (COT) prompts by translating the type inference steps of static analysis into prompts based on the type dependency graphs (TDGs), enabling language models to learn from how static analysis infers types." — abstract
> "TypeGen outperforms the best baseline Type4Py by 10.0% for argument type prediction and 22.5% in return value type prediction in terms of top-1 Exact Match by using only five examples" — abstract
> "TypeGen achieves substantial improvements of 27% to 84% compared to the zero-shot performance of large language models" — abstract
