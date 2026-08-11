# Not All Invariants Are Equal: Curating Training Data to Accelerate Program Verification with SLMs

- **Citekey:** pinto2026not
- **Record:** arxiv:2603.15510
- **Authors:** Ido Pinto, Yizhak Yisrael Elboher, Haoze Wu, Nina Narodytska et al.
- **Venue:** arXiv 2026
- **Categories:** program-logic, formal-verification
- **Link:** http://arxiv.org/abs/2603.15510v2

## Problem

- Inductive loop invariant synthesis is the bottleneck in automated program verification.
- Models produce invariants that are invalid, or valid but computationally ineffective.
- Fine-tuning is the obvious fix, and high-quality training invariants are hard to obtain.

## Main ideas

- The paper first formalises what makes a training invariant high quality.
- Wonda then curates such invariants from raw verifier output rather than from human labels.
- AST-based normalisation puts verifier output into a canonical form.
- Model-driven semantic rewriting and augmentation follow, with provable quality guarantees.
- Curating data, not changing the architecture, is what lets small models compete.

## Evaluation

- Consistent gains across the Qwen3, Llama-3.1, and Mistral families.
- Qwen3 4B and 8B nearly double invariant correctness and double speedup rates.
- Llama-3.1-8B triples both.
- On InvBench a 4B model beats an off-the-shelf model 20 times its size.
- A 14B Qwen3 matches GPT-5.2 on end-to-end verification time, without test-time compute overhead.

## Limitations

- Ours: the quality guarantees apply to the curation pipeline, not to the invariants a tuned model emits.
- Ours: gains are relative, so absolute invariant correctness on InvBench is unclear.
- Ours: curation depends on verifier output, so unverifiable programs contribute nothing.
- Authors: models fail on complex programs, which curation mitigates rather than solves.

## Follow-ups

- Report absolute correctness on InvBench so later work has a target.
- Test whether curated data transfers across verifiers, or encodes one tool's output style.
- Apply the same curation idea to specifications, where verifier output is also available.

## Evidence

> "We first formalize the properties required for a high-quality training invariant, and then present Wonda, a rigorous data curation pipeline that extracts such invariants from raw verifier output via AST-based normalization followed by LLM-driven semantic rewriting and augmentation with provable quality guarantees." — abstract
> "the 4B and 8B Qwen3 models nearly double invariant correctness and double speedup rates, while Llama-3.1-8B triples both" — abstract
> "the same 4B model outperforms an off-the-shelf model 20x its size and matches the end-to-end verification time of GPT-OSS-120B" — abstract
