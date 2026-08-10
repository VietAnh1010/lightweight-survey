# A Neurosymbolic Approach to Natural Language Formalization and Verification

- **Citekey:** an2025neurosymbolic
- **Record:** arxiv:2511.09008
- **Authors:** Chenyang An, Sam Bayless, Stefano Buliani, Darion Cassel et al.
- **Venue:** CAV 2025
- **Categories:** specification, formal-verification, proof-automation
- **Link:** http://arxiv.org/abs/2511.09008v2

## Problem

- Regulated industries cannot deploy an LLM that offers no formal correctness guarantee.
- Policies are written in natural language; checking a statement against one needs a formalization.
- A single formalization is a silent failure point: nothing detects that it misreads the policy.

## Main ideas

- ARc splits the job: formalize the policy once, then check statements against that formalization.
- Formalization is done several times redundantly, and the results checked for semantic equivalence.
- Disagreement between redundant formalizations is the signal that the translation is untrusted.
- Human guidance is optional and applies to the formalization step, not to each verification.
- Every outcome carries an auditable artifact, so a decision can be re-examined after the fact.

## Evaluation

- Benchmarks report over 99% soundness and a near-zero false positive rate on logical validity.
- Deployed as a public cloud service, which the authors call the first such commercial offering.
- Not measured: how often redundant formalization abstains, or the cost of that abstention.
- No baseline against a single-formalization pipeline is reported in the abstract.

## Limitations

- Authors: adoption is limited by the absence of formal correctness guarantees in the model itself.
- Ours: soundness is reported against the formalized policy, not against the English one.
- Ours: semantic equivalence across formalizations detects disagreement, not shared misreading.
- Ours: the abstract gives no benchmark size, so the 99% figure has no denominator here.

## Follow-ups

- Measure how many independent formalizations are needed before agreement stops being informative.
- Apply redundant formalization to code specifications, where an oracle for equivalence exists.
- Report the abstention rate alongside soundness; a sound checker that abstains often is cheap.

## Evidence

> "ARc performs multiple redundant formalization steps at inference time, checking the formalizations for semantic equivalence." — abstract
> "Our benchmarks show that ARc exceeds 99% soundness and achieves a near-zero false positive rate in identifying logical validity." — abstract
> "their lack of formal correctness guarantees limits their adoption in regulated industries" — abstract
