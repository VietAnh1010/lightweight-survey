# WaDec: Decompiling WebAssembly Using Large Language Model

- **Citekey:** she2024wadec
- **Record:** arxiv:2406.11346
- **Authors:** Xinyu She, Yanjie Zhao, Haoyu Wang
- **Venue:** ASE 2024
- **Categories:** decompilation
- **Link:** http://arxiv.org/abs/2406.11346v3

## Problem

- WebAssembly ships as a compact binary, so debugging and analysing web applications is hard.
- Traditional decompilers produce output that is not readable.
- General LLM decompilers handle ordinary binaries but not Wasm's structure.

## Main ideas

- WaDec fine-tunes a model specifically to decompile Wasm into a higher-level representation.
- Training uses a specialized dataset of wat-c snippet pairs with self-supervised learning.
- Snippet-level training is what lets it decompile fragments, not only whole wat functions.
- The reported metrics are execution-facing: recompilability, re-execution, output consistency.
- Code inflation is treated as a first-class quality measure rather than an afterthought.

## Evaluation

- Code inflation 3.34%, against 116.94% for the prior state of the art, a 97% reduction.
- Recompilability 52.11%, re-execution 43.55%, output consistency 27.15%.
- Baseline output cannot be compiled or executed at all, so these three are new measurements.
- AST edit distance similarity up 185%, cyclomatic complexity 8%, cosine similarity 41%.

## Limitations

- Ours: output consistency of 27.15% means most decompiled code does not behave identically.
- Ours: recompilability at 52.11% leaves half the output unusable as source.
- Ours: fine-tuning is Wasm-specific, so nothing transfers to other binary formats.
- Authors: general LLM decompilers face specific challenges on Wasm, which motivated specialization.

## Follow-ups

- Pair decompilation with a differential check, as RustAssure does, to raise consistency past 27%.
- Report which Wasm constructs drive the re-execution failures, to target the next training set.
- Test whether snippet-level training helps other stack machine bytecodes.

## Evidence

> "The LLM was meticulously fine-tuned using a specialized dataset of wat-c code snippets, employing self-supervised learning techniques. This enables WaDec to effectively decompile not only complete wat functions but also finer-grained wat code snippets." — abstract
> "It achieves a code inflation rate of only 3.34%, a dramatic 97% reduction compared to the state-of-the-art's 116.94%." — abstract
> "WaDec maintains a recompilability rate of 52.11%, a re-execution rate of 43.55%, and an output consistency of 27.15%" — abstract
