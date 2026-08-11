# RAP-Gen: Retrieval-Augmented Patch Generation with CodeT5 for Automatic Program Repair

- **Citekey:** wang2023rap
- **Record:** doi:10.1145/3611643.3616256
- **Authors:** Weishi Wang, Yue Wang, Shafiq Joty, Steven C.H. Hoi
- **Venue:** FSE 2023
- **Categories:** program-repair
- **Link:** https://doi.org/10.1145/3611643.3616256

## Problem

- Search-based repair mines fix patterns from heuristics or a redundancy assumption.
- Learned repair models hold the fix space in a fixed set of parameters.
- That parameter budget bounds how much of a complex repair space a model can represent.

## Main ideas

- RAP-Gen retrieves relevant fix patterns from a codebase of past bug-fix pairs.
- Retrieval moves fix knowledge out of parameters and into an external store.
- A hybrid retriever combines lexical and semantic matching over raw source code.
- It uses no code-specific features, so it stays language-agnostic.
- CodeT5 serves both retrieval and generation, unifying the two stages in one model.
- The retriever runs first and augments the buggy input the generator sees.

## Evaluation

- Three benchmarks in two languages: TFix in JavaScript, Code Refinement and Defects4J in Java.
- Evaluated both with and without bug localization information provided.
- Outperforms previous state of the art on all benchmarks.
- 15 more bugs repaired on the 818-bug Defects4J set.

## Limitations

- Ours: retrieval quality depends on the bug-fix corpus, so novel bug classes gain nothing.
- Ours: 15 more bugs out of 818 is a small absolute margin.
- Ours: no ablation of the lexical against the semantic half of the retriever.
- Authors: parametric models are limited by a fixed parameter set modelling a complex space.

## Follow-ups

- Ablate the hybrid retriever to see which matching mode carries the gain.
- Measure performance on bugs with no similar fix in the corpus, which is the failure case.
- Compare retrieval against pairing with a static analyser, which conditions repair differently.

## Evidence

> "we propose a novel Retrieval-Augmented Patch Generation framework (RAP-Gen) by explicitly leveraging relevant fix patterns retrieved from a codebase of previous bug-fix pairs" — abstract
> "we build a hybrid patch retriever to account for both lexical and semantic matching based on the raw source code in a language-agnostic manner, which does not rely on any code-specific features" — abstract
> "RAP-Gen significantly outperforms previous state-of-the-art approaches on all benchmarks, e.g., repairing 15 more bugs on 818 Defects4J bugs" — abstract
