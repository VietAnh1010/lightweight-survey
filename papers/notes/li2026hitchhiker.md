# The Hitchhiker's Guide to Program Analysis, Part III: Mostly Harmless LLMs

- **Citekey:** li2026hitchhiker
- **Record:** arxiv:2606.15122
- **Authors:** Haonan Li, Tianyang Zhou, Manu Sridharan, Hang Zhang et al.
- **Venue:** arXiv 2026
- **Categories:** static-analysis, bug-detection
- **Link:** http://arxiv.org/abs/2606.15122v1

## Problem

- Models are used to judge whether a reported bug can trigger, with promising empirical results.
- Empirical effectiveness does not make a plausible rationale sufficient to discharge a warning.
- Dismissing a warning requires showing the error state is unreachable, not explaining why it may not occur.

## Main ideas

- Evident separates model assistance from program-behavior reasoning, and delegates the latter.
- The model's only job is to construct a warning-specific analysis harness.
- Evident validates the harness before the backend is invoked, so a bad harness is caught first.
- The backend answers one question: is the error state unreachable under this harness and its assumptions.
- The claim is relative to the harness, which makes the assumptions explicit rather than implicit.

## Evaluation

- 200 real Android kernel driver warnings from two existing static detectors.
- 151 of 200 classified correctly (76%), including 111 false alarms discharged.
- No confirmed bug in the dataset was discharged, which is the safety property that matters here.
- Remaining cases are unresolved or conservatively retained as potential bugs.

## Limitations

- Ours: soundness holds relative to the harness, so a harness with wrong assumptions still discharges wrongly.
- Ours: 76% correct classification means a quarter of warnings still need human triage.
- Ours: one warning domain, Android kernel drivers, from two detectors.
- Authors: the remaining cases are unresolved rather than decided, which is the conservative choice.

## Follow-ups

- Check generated harnesses against a second, independent harness for the same warning.
- Measure how harness quality degrades outside kernel drivers, where aliasing patterns differ.
- Report the cost of the validation step, since it gates every backend invocation.

## Evidence

> "empirical effectiveness does not make a plausible model-generated rationale sufficient for discharging warnings" — abstract
> "Evident uses an LLM only to construct a warning-specific analysis harness. Evident then validates the harness before invoking the backend." — abstract
> "Evident correctly classifies 151 cases (76%), including discharging 111 false alarms, without discharging any confirmed bug in the dataset" — abstract
