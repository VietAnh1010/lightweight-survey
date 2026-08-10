# Guiding Enumerative Program Synthesis with Large Language Models

- **Citekey:** li2024guiding
- **Record:** arxiv:2403.03997
- **Authors:** Yixuan Li, Julian Parsert, Elizabeth Polgreen
- **Venue:** CAV 2024
- **Categories:** program-synthesis, constraint-solving
- **Link:** http://arxiv.org/abs/2403.03997v2

## Problem

- Formal synthesis from precise logical specifications is still won by enumerative algorithms.
- Language models dominate synthesis from natural language but not from logical specifications.
- A model used one-shot has no way to learn what the enumerator has already ruled out.

## Main ideas

- The model is placed inside a weighted probabilistic enumerative search, not in front of it.
- Information flows both ways: the enumerator reports progress, the model returns syntactic guidance.
- The loop iterates, so guidance is conditioned on the search state rather than on the problem alone.
- One-shot synthesis is tried first; the integrated algorithm is the fallback when it fails.
- The enumerator retains its completeness argument; the model only reweights the search.

## Evaluation

- Benchmarks from the Syntax-Guided Synthesis competition.
- GPT-3.5 alone is easily outperformed by state-of-the-art formal synthesis algorithms.
- The integration beats the model alone, the enumerator alone, and the winning SyGuS competition tool.
- Reporting all three baselines is what makes the composition claim checkable.

## Limitations

- Authors: a stand-alone model is easily outperformed on formal synthesis benchmarks.
- Ours: gains are reported qualitatively as significant, with no per-benchmark numbers in the abstract.
- Ours: a library of prompts is crafted for the domain, so part of the result is prompt engineering.
- Ours: SyGuS benchmarks are public and predate the model, so leakage is not addressed.

## Follow-ups

- Report solve counts and times per SyGuS track, so the composition's cost is visible.
- Test whether guidance still helps once the enumerator's grammar is unfamiliar to the model.
- Apply the two-way loop to invariant synthesis, where the checker also reports partial progress.

## Evidence

> "we propose a novel enumerative synthesis algorithm, which integrates calls to an LLM into a weighted probabilistic search" — abstract
> "This allows the synthesizer to provide the LLM with information about the progress of the enumerator, and the LLM to provide the enumerator with syntactic guidance in an iterative loop." — abstract
> "our approach integrating the LLM into an enumerative synthesis algorithm shows significant performance gains over both the LLM and the enumerative synthesizer alone and the winning SyGuS competition tool" — abstract
