# Nuances are the Key: Unlocking ChatGPT to Find Failure-Inducing Tests with Differential Prompting

- **Citekey:** li2023nuances
- **Record:** arxiv:2304.11686
- **Authors:** Tsz-On Li, Wenxi Zong, Yibo Wang, Haoye Tian et al.
- **Venue:** ASE 2023
- **Categories:** test-generation, program-synthesis
- **Link:** http://arxiv.org/abs/2304.11686v6

## Problem

- Finding a failure-inducing test needs both an input that triggers the fault and an oracle.
- ChatGPT alone finds a correct failure-inducing test only 28.8% of the time.
- The task turns on subtle differences between the buggy program and its correct version.

## Main ideas

- The diagnosis is specific: the model is weak at spotting subtle differences between similar syntax.
- The countervailing observation is that the model infers a buggy program's intended behaviour well.
- So the intended behaviour is used to synthesize a second program that realises it.
- The difference between the buggy program and the synthesized one is then explicit, not subtle.
- Differential testing over the pair supplies the oracle the model could not construct.

## Evaluation

- Quixbugs, against baselines including direct ChatGPT use and Pynguin.
- 77.8% of cases yield a correct failure-inducing test, 2.7 times the best baseline.
- The 28.8% baseline is measured in the same study, so the comparison is internally consistent.
- Not measured: whether the synthesized reference program is itself correct.

## Limitations

- Authors: ChatGPT is weak at recognizing subtle code differences when two versions share syntax.
- Ours: the oracle is only as good as the synthesized program, which has no independent check.
- Ours: Quixbugs programs are small and single-function, so scale is untested.
- Ours: the method needs a buggy program whose intent the model can infer, which excludes novel domains.

## Follow-ups

- Validate the synthesized reference against a specification, so a wrong reference cannot produce a wrong oracle.
- Synthesize several references and require agreement, which is the redundancy idea from autoformalization.
- Test on multi-function bugs where intended behaviour is distributed across the program.

## Evidence

> "our study shows that ChatGPT has a low probability (28.8%) of finding correct failure-inducing test cases for buggy programs" — abstract
> "The intended behavior can be leveraged to synthesize programs, in order to make the subtle code difference between a buggy program and its correct version (i.e., the synthesized program) explicit." — abstract
> "our approach has a much higher probability (77.8%) of finding correct failure-inducing test cases, 2.7X as the best baseline" — abstract
