# Fuzz4All: Universal Fuzzing with Large Language Models

- **Citekey:** xia2023fuzz4all
- **Record:** doi:10.1145/3597503.3639121
- **Authors:** Chunqiu Steven Xia, Matteo Paltenghi, Jia Le Tian, Michael Pradel et al.
- **Venue:** ICSE 2023
- **Categories:** fuzzing, constraint-solving
- **Link:** http://arxiv.org/abs/2308.04748v3

## Problem

- Compilers, runtime engines, constraint solvers, and API libraries take formal languages as input.
- Each existing fuzzer targets one language, and often one version of it.
- Generated inputs stick to the language features the fuzzer's grammar encodes.

## Main ideas

- Fuzz4All uses the model as the input generation and mutation engine, so no grammar is written.
- One fuzzer therefore targets many input languages and many features of each.
- Autoprompting constructs prompts suited to fuzzing rather than reusing a task prompt.
- The fuzzing loop rewrites its own prompt each round to produce new inputs.
- The prompt, not a corpus of seeds, is the state that the search carries forward.

## Evaluation

- Nine systems under test across six languages: C, C++, Go, SMT2, Java, Python.
- Higher coverage than existing language-specific fuzzers in all six languages.
- 98 bugs found in GCC, Clang, Z3, CVC5, OpenJDK, and Qiskit; 64 confirmed as previously unknown.
- Beating specialised fuzzers on their own languages is the strongest form of the universality claim.

## Limitations

- Ours: no soundness or completeness notion applies, so coverage is the only guidance signal.
- Ours: cost per bug is not reported, and every input is a model generation.
- Ours: generation quality depends on how much of each language appeared in pretraining.
- Authors: existing fuzzers cannot be applied across languages or even versions, the gap addressed.

## Follow-ups

- Report cost per bug against language-specific fuzzers, which generate inputs almost for free.
- Measure whether coverage advantage holds for a language with little public code.
- Combine autoprompting with structural masking, as Clozemaster does, to raise input validity.

## Evidence

> "The key idea behind Fuzz4All is to leverage large language models (LLMs) as an input generation and mutation engine, which enables the approach to produce diverse and realistic inputs for any practically relevant language." — abstract
> "we present a novel autoprompting technique, which creates LLM prompts that are wellsuited for fuzzing, and a novel LLM-powered fuzzing loop, which iteratively updates the prompt to create new fuzzing inputs" — abstract
> "Fuzz4All has identified 98 bugs in widely used systems, such as GCC, Clang, Z3, CVC5, OpenJDK, and the Qiskit quantum computing platform, with 64 bugs already confirmed by developers as previously unknown." — abstract
