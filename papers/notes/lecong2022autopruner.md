# AutoPruner: transformer-based call graph pruning

- **Citekey:** lecong2022autopruner
- **Record:** doi:10.1145/3540250.3549175
- **Authors:** Thanh Le-Cong, Hong Jin Kang, Truong Giang Nguyen, Stefanus Agus Haryono et al.
- **Venue:** FSE 2022
- **Categories:** static-analysis
- **Link:** https://doi.org/10.1145/3540250.3549175

## Problem

- Static call graph construction trades soundness against precision and is usually imprecise.
- Machine-learned pruning post-processes the graph using structural features alone.
- Structural features cannot separate a true edge from a false one when both look alike.

## Main ideas

- AutoPruner adds semantics: a pretrained code model reads the caller and callee of each edge.
- The model is fine-tuned to represent source code from descriptions of its semantics.
- Semantic features per edge are combined with the structural features earlier pruners used.
- A feed-forward network classifies each edge from the two feature sets together.
- The technique only removes edges, so it operates on an existing analyser's output.

## Evaluation

- A benchmark dataset of real-world programs.
- F-measure up to 13% better than state-of-the-art baselines at identifying false-positive edges.
- The task is scored directly on edge classification rather than on a downstream client.
- Not measured: the effect on any analysis that consumes the pruned graph.

## Limitations

- Ours: pruning an over-approximation can remove true edges, which breaks downstream soundness.
- Ours: no downstream client is evaluated, so the practical benefit is unmeasured.
- Ours: one model call per edge, and no cost figure is given for large graphs.
- Authors: call graph construction is a soundness against precision trade-off, which pruning shifts.

## Follow-ups

- Measure a downstream analysis, for example taint tracking, on pruned against unpruned graphs.
- Report how many true edges are lost at each precision setting.
- Compare against summarisation-based filtering, which targets the same imprecision differently.

## Evidence

> "AutoPruner takes a Transformer-based approach to capture the semantic relationships between the caller and callee functions associated with each edge in the call graph" — abstract
> "AutoPruner uses these semantic features together with the structural features extracted from the call graph to classify each edge via a feed-forward neural network." — abstract
> "AutoPruner outperforms the state-of-the-art baselines, improving on F-measure by up to 13% in identifying false-positive edges in a static call graph" — abstract
