# Semantic-Enhanced Indirect Call Analysis with Large Language Models

- **Citekey:** cheng2024semantic
- **Record:** doi:10.1145/3691620.3695016
- **Authors:** Baijun Cheng, Cen Zhang, Kailong Wang, Ling Shi et al.
- **Venue:** ASE 2024
- **Categories:** static-analysis
- **Link:** http://arxiv.org/abs/2408.04344v3

## Problem

- Indirect calls make a precise control flow graph hard to build, which degrades downstream analyses.
- Existing indirect call analyzers reason over types and signatures, not over program meaning.
- The result is an over-large target set: every downstream client inherits the imprecision.

## Main ideas

- SEA rests on an observation: an indirect call is usually semantically similar to what it invokes.
- The model writes natural language summaries of the call site and of each candidate target.
- Summaries are produced from several perspectives, not one, so the comparison has more to match on.
- Comparing summaries decides whether a pair is a plausible caller-callee pair.
- The model filters an existing analyser's output; it never adds a target the analyser did not propose.

## Evaluation

- Reports more precise target sets for indirect calls than the static analysis methods it enhances.
- Not measured in the abstract: recall loss, which is the risk when filtering an over-approximation.
- No absolute precision or recall numbers appear in the abstract, only a direction of change.

## Limitations

- Ours: filtering an over-approximate target set can drop real edges, breaking soundness downstream.
- Ours: the semantic-similarity premise fails for dispatch tables and callbacks named generically.
- Ours: cost per call site is not reported, and there is one model query per candidate pair.
- Authors: the approach depends on the model's code summarization ability, trained on code corpora.

## Follow-ups

- Quantify the soundness cost: how many true edges the filter removes at each precision level.
- Cache summaries per function so cost grows with functions rather than with candidate pairs.
- Test whether the same filter helps points-to analysis, where over-approximation is also the problem.

## Evidence

> "Our fundamental insight is that for common programming practices, indirect calls often exhibit semantic similarity with their invoked targets." — abstract
> "SEA leverages LLMs to generate natural language summaries of both indirect calls and target functions from multiple perspectives." — abstract
> "This semantic alignment serves as a supportive mechanism for static analysis techniques in filtering out false targets." — abstract
