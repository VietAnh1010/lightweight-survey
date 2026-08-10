# Abstain and Validate: A Dual-LLM Policy for Reducing Noise in Agentic Program Repair

- **Citekey:** cambronero2026abstain
- **Record:** doi:10.1145/3786583.3786858
- **Authors:** José Cambronero, Michele Tufano, Sherry Shi, Renyao Wei et al.
- **Venue:** ICSE 2026
- **Categories:** program-repair, agents
- **Link:** https://doi.org/10.1145/3786583.3786858

## Problem

- Agentic repair now produces patches for repository-level bugs, but a human still reviews each one.
- Patches that will be rejected cost reviewer time and erode trust in the whole system.
- Raising patch quality is one route; not showing the bad ones is a separate, cheaper route.

## Main ideas

- Two gatekeeping policies wrap an existing repair system rather than changing how it generates.
- Bug abstention drops bugs the system is unlikely to fix, before any patch is generated.
- Patch validation rejects generated patches unlikely to fix the bug they target.
- Both policies are themselves LLM-based, so the architecture is a model judging model output.
- The two compose: filtering the input and the output attacks noise at both ends.

## Evaluation

- Three bug sets from Google's codebase, with patches from an internal agentic repair system.
- On 174 human-reported bugs: up to 13 and 15 percentage points separately, 39 combined.
- Patch validation also raises single-sample success on null pointer and sanitizer-reported bugs.
- Not measured: how many real fixes the policies discard, which is the cost side of the trade.

## Limitations

- Ours: success rate rises partly by removing hard bugs, so it is not comparable to an unfiltered rate.
- Ours: no false-abstention rate is reported, so the recall cost of the policies is unknown.
- Ours: evaluation is on one company's internal system, so transfer is untested.
- Authors: the patches still require human review; the policies reduce noise rather than remove review.

## Follow-ups

- Report precision and recall of the policies themselves, not only the downstream success rate.
- Compare an LLM validator against running the test suite, which is a cheaper and sound signal.
- Test whether abstention transfers across repair systems or is tuned to one generator's failures.

## Evidence

> "We introduce two complementary LLM-based policies to reduce such noise: bug abstention and patch validation policies." — abstract
> "removing bugs and patches rejected by our policies can raise success rates by up to 13 percentage points and 15 percentage points, respectively, and by up to 39 percentage points in combination" — abstract
> "Showing patches unlikely to be accepted can lead to substantial noise, wasting valuable developer time and eroding trust in automated code changes." — abstract
