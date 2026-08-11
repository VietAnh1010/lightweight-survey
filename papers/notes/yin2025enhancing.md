# Enhancing LLM's Ability to Generate More Repository-Aware Unit Tests Through Precise Contextual Information Injection

- **Citekey:** yin2025enhancing
- **Record:** arxiv:2501.07425
- **Authors:** Xin Yin, Chao Ni, Xinrui Li, Liushan Chen et al.
- **Venue:** ASE 2025
- **Categories:** test-generation
- **Link:** http://arxiv.org/abs/2501.07425v1

## Problem

- Models hallucinate when writing unit tests: calls to methods that do not exist, wrong parameters.
- The cause is no awareness of the project's global context.
- Studies extract fixed patterns of context, which suits neither every model nor every focal method.
- Excessive irrelevant context is its own failure, crowding out what matters.

## Main ideas

- RATester injects context on demand rather than packing a fixed amount in advance.
- The gopls language server supplies definitions and documentation comments.
- Lookup is triggered by the model meeting an unfamiliar identifier, such as a struct name.
- That makes retrieval demand-driven, which is what avoids irrelevant context.
- The language server is authoritative, so fetched definitions cannot be hallucinated.

## Evaluation

- The abstract states the mechanism and the intended reduction in hallucination.
- No quantitative results appear in the abstract.
- The target language is Go, matching the gopls dependency.
- Not measured here: hallucination rate before and after, or coverage.

## Limitations

- Ours: no numbers in the abstract, so the effect size cannot be assessed.
- Ours: the technique is tied to a language with a mature language server.
- Ours: definition lookup fixes unknown identifiers, not wrong logic.
- Authors: fixed context patterns may not suit all generation processes, which motivates the design.

## Follow-ups

- Report hallucination rates with and without gopls, which is the claim being made.
- Measure cost: a language server query per unfamiliar identifier adds latency per test.
- Test the same demand-driven pattern in Java or C++, where language servers also exist.

## Evidence

> "LLMs may exhibit hallucinations when generating unit tests for focal methods or functions due to their lack of awareness regarding the project's global context" — abstract
> "When RATester encounters an unfamiliar identifier (e.g., an unfamiliar struct name), it first leverages gopls to fetch relevant definitions and documentation comments, and then uses this global knowledge to guide the LLM." — abstract
> "they often extract fixed patterns of context for different models and focal methods, which may not be suitable for all generation processes" — abstract
