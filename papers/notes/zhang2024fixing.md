# Fixing Security Vulnerabilities with AI in OSS-Fuzz

- **Citekey:** zhang2024fixing
- **Record:** arxiv:2411.03346
- **Authors:** Yuntong Zhang, Jiawei Wang, Dominic Berzin, Martin Mirchev et al.
- **Venue:** ICSE 2024
- **Categories:** program-repair, fuzzing, agents
- **Link:** http://arxiv.org/abs/2411.03346v2

## Problem

- OSS-Fuzz has found over 10,000 vulnerabilities across 1000 or more projects.
- Fixing them stays manual, so found vulnerabilities remain unpatched.
- Agents built for issue descriptions search code from text, which a fuzzer crash does not provide.

## Main ideas

- AutoCodeRover is customised for security patching rather than issue resolution.
- The exploit input is executed, and the execution identifies the code elements relevant to the fix.
- Execution replaces issue-text search, which is the adaptation the setting demands.
- Agent autonomy beats fixed control flow such as Agentless for this task.
- A second finding concerns measurement, not the patcher itself.

## Evaluation

- OSS-Fuzz vulnerability data.
- Agent autonomy proves useful for successful security patching against fixed-control-flow approaches.
- Patches with high CodeBLEU scores still fail against the exploit input.
- Patch correctness therefore needs dynamic attributes, not text or code similarity.

## Limitations

- Ours: no patch success rate appears in the abstract, so the technique's yield is unclear.
- Ours: passing the exploit input is necessary, not sufficient, for a correct security patch.
- Ours: the comparison against Agentless is qualitative in the abstract.
- Authors: their measurement finding refutes the similarity metrics prior work relied on.

## Follow-ups

- Report patch acceptance by maintainers, which is the standard the exploit test cannot reach.
- Check patches for regressions, since passing the exploit says nothing about other behaviour.
- Adopt exploit-execution scoring as the benchmark standard, replacing CodeBLEU.

## Evidence

> "Instead for security patching, we rely on the test execution of the exploit input to extract code elements relevant to the fix." — abstract
> "our findings show that we cannot measure quality of patches by code similarity of the patch with reference codes (as in CodeBLEU scores used in VulMaster), since patches with high CodeBLEU scores still fail to pass given the given exploit input" — abstract
> "LLM agent autonomy is useful for successful security patching, as opposed to approaches like Agentless where the control flow is fixed" — abstract
