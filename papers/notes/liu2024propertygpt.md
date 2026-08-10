# PropertyGPT: LLM-driven Formal Verification of Smart Contracts through Retrieval-Augmented Property Generation

- **Citekey:** liu2024propertygpt
- **Record:** doi:10.14722/ndss.2025.241357
- **Authors:** Ye Liu, Yue Xue, Daoyuan Wu, Yuqiang Sun et al.
- **Venue:** NDSS 2024
- **Categories:** specification, formal-verification, static-analysis
- **Link:** http://arxiv.org/abs/2405.02580v2

## Problem

- Formal verification of smart contracts needs properties, and writing them is expert work.
- Human-written properties exist in audit reports but are tied to the contracts they were written for.
- A generated property is useless unless it compiles, suits the code, and can be verified.

## Main ideas

- PropertyGPT embeds existing human-written properties in a vector database and retrieves references.
- Retrieval-augmented in-context learning transfers an audited property to unknown code.
- Three separate loops close on the three failure modes rather than one generic retry.
- Compilation and static analysis feedback act as an external oracle for iterative revision.
- Similarity along several dimensions ranks candidates, and a weighted algorithm keeps the top-K.
- A dedicated prover formally verifies the surviving properties.

## Evaluation

- 80% recall against ground-truth properties.
- 26 of 37 tested CVEs and attack incidents detected.
- 12 zero-day vulnerabilities found, earning $8,256 in bug bounties.
- Bounty-confirmed zero-days are an external oracle few papers in this set report.

## Limitations

- Ours: recall is measured against a ground-truth property set, so novel property shapes are invisible.
- Ours: the approach needs an existing corpus of audited properties, which few domains have.
- Ours: 26 of 37 CVEs means 11 were missed, and the abstract does not characterise them.
- Authors: ensuring properties are compilable, appropriate, and verifiable is the stated challenge.

## Follow-ups

- Test transfer to a domain with no audit corpus, which is where the retrieval premise breaks.
- Ablate the three loops to see which of compilation feedback, ranking, or proving carries the result.
- Measure the false positive cost of the properties that the prover accepts but no bug violates.

## Evidence

> "we embed existing properties into a vector database and retrieve a reference property for LLM-based in-context learning to generate a new property for a given code" — abstract
> "we use the compilation and static analysis feedback as an external oracle to guide LLMs in iteratively revising the generated properties" — abstract
> "It successfully detected 26 CVEs/attack incidents out of 37 tested and also uncovered 12 zero-day vulnerabilities, leading to $8,256 in bug bounty rewards." — abstract
