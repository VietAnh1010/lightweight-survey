# Testing the Limits: Unusual Text Inputs Generation for Mobile App Crash Detection with Large Language Model

- **Citekey:** liu2023testing
- **Record:** arxiv:2310.15657
- **Authors:** Zhe Liu, Chunyang Chen, Junjie Wang, Mengzhuo Chen et al.
- **Venue:** ICSE 2023
- **Categories:** test-generation, fuzzing, bug-detection
- **Link:** http://arxiv.org/abs/2310.15657v1

## Problem

- Special text inputs such as a negative font size crash mobile apps.
- Generating diverse unusual inputs is hard: the space explodes and inputs are context sensitive.
- Constraint relations between fields compound the difficulty.

## Main ideas

- InputBlaster reframes the task: generate test generators, not individual inputs.
- Each generator yields a batch of unusual inputs under one mutation rule.
- The mutation rule is emitted alongside the generator and serves as the reasoning chain.
- One model call therefore produces many inputs plus a stated rationale for them.
- In-context examples are used to raise generator quality.

## Evaluation

- 36 text input widgets with crash bugs across 31 popular Android apps.
- 78% bug detection rate, 136% above the best baseline.
- Integrated with an automated GUI testing tool, it found 37 unseen crashes in Google Play apps.
- Crashes in shipped apps are an external signal, unlike the curated widget set.

## Limitations

- Ours: crashes are the only oracle, so unusual inputs causing silent corruption are missed.
- Ours: 36 widgets is a small curated set for a 78% figure.
- Ours: mutation rules are model-written and unchecked against the app's input contract.
- Authors: the difficulty is the combination of explosion, context sensitivity, and constraint relations.

## Follow-ups

- Extend the oracle past crashes to state corruption, which needs a differential comparison.
- Reuse mutation rules across apps, which would amortise generation cost.
- Compare generator synthesis against direct input generation at matched model cost.

## Evidence

> "It formulates the unusual inputs generation problem as a task of producing a set of test generators, each of which can yield a batch of unusual text inputs under the same mutation rule." — abstract
> "InputBlaster leverages LLM to produce the test generators together with the mutation rules serving as the reasoning chain" — abstract
> "it achieves 78% bug detection rate, with 136% higher than the best baseline. Besides, we integrate it with the automated GUI testing tool and detect 37 unseen crashes in real-world apps from Google Play." — abstract
