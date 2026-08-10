# GPTScan: Detecting Logic Vulnerabilities in Smart Contracts by Combining GPT with Program Analysis

- **Citekey:** sun2023gptscan
- **Record:** doi:10.1145/3597503.3639117
- **Authors:** Yuqiang Sun, Daoyuan Wu, Yue Xue, Han Liu et al.
- **Venue:** ICSE 2023
- **Categories:** bug-detection, static-analysis
- **Link:** http://arxiv.org/abs/2308.03314v3

## Problem

- Smart contract tools target fixed control-flow or data-flow patterns such as re-entrancy.
- About 80% of Web3 security bugs escape those tools for want of domain-specific properties.
- Asking a model directly gives high false positives and is bounded by its pretrained knowledge.

## Main ideas

- GPTScan uses the model as a code understanding tool, not as the vulnerability oracle.
- Each logic vulnerability type is decomposed into scenarios and properties the model can match.
- Matching produces candidates, which is a recall step, deliberately permissive.
- The model is then asked to name the key variables and statements behind each candidate.
- Static confirmation validates those named variables and statements, which is the precision step.
- Separating recall from precision is what makes the composition work.

## Evaluation

- About 400 contract projects and 3K Solidity files.
- Precision over 90% on token contracts, 57.14% on large projects such as Web3Bugs.
- Recall over 70% on ground-truth logic vulnerabilities, including 9 missed by human auditors.
- Cost: 14.39 seconds and 0.01 USD per thousand lines of Solidity.
- Static confirmation removes two-thirds of false positives.

## Limitations

- Ours: 57.14% precision on large projects means nearly half of reports there are still false.
- Ours: scenarios and properties are hand-written per vulnerability type, so new types need manual work.
- Ours: recall is measured against ground truth, so vulnerability types outside the taxonomy are invisible.
- Authors: relying solely on GPT gives high false positives and is limited by pretrained knowledge.

## Follow-ups

- Generate the scenario and property decomposition itself, which is the remaining manual step.
- Explain the precision gap between token contracts and large projects, and target it.
- Compare static confirmation against symbolic confirmation on the same candidate set.

## Evidence

> "Instead of relying solely on GPT to identify vulnerabilities, which can lead to high false positives and is limited by GPT's pre-trained knowledge, we utilize GPT as a versatile code understanding tool." — abstract
> "GPTScan further instructs GPT to intelligently recognize key variables and statements, which are then validated by static confirmation" — abstract
> "Moreover, static confirmation helps GPTScan reduce two-thirds of false positives." — abstract
