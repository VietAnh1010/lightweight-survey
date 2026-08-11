# Automated Testing of COBOL to Java Transformation

- **Citekey:** hans2025automated
- **Record:** arxiv:2504.10548
- **Authors:** Sandeep Hans, Atul Kumar, Toshikai Yasue, Kouichi Ono et al.
- **Venue:** FSE 2025
- **Categories:** test-generation, symbolic-execution
- **Link:** http://arxiv.org/abs/2504.10548v1

## Problem

- Model-based COBOL to Java translation is feasible but the output cannot be trusted.
- Validating translated Java by hand is time-consuming and labour-intensive.
- Legacy COBOL programs rarely come with a test suite that could serve as the oracle.

## Main ideas

- Symbolic execution generates unit tests for the COBOL side, where no tests existed.
- External calls are mocked, which is what makes symbolic execution tractable on enterprise code.
- Those COBOL tests are transformed into JUnit tests that run against the translated Java.
- The pair then forms a differential oracle for semantic equivalence.
- Detected discrepancies are reported back, and the authors use them to improve the model.

## Evaluation

- Industrial context: IBM Watsonx Code Assistant for Z.
- The framework automates equivalence testing that was previously manual.
- Discrepancies both trigger repair and feed model improvement.
- No quantitative results appear in the abstract; this is an experience report.

## Limitations

- Ours: no numbers in the abstract, so the framework's yield cannot be assessed here.
- Ours: mocking external calls removes exactly the behaviour enterprise COBOL depends on.
- Ours: equivalence is checked on generated tests, so coverage bounds the guarantee.
- Authors: translated code cannot be trusted, which is the premise rather than a measured claim.

## Follow-ups

- Report discrepancy counts and their severity, which an experience report can supply.
- Compare symbolic test generation against differential symbolic execution on the pair directly.
- Measure how much the model improves from discrepancy feedback, which the paper claims but does not size.

## Evidence

> "Our framework uses symbolic execution to generate unit tests for COBOL, mocking external calls and transforming them into JUnit tests to validate semantic equivalence with translated Java." — abstract
> "the resulting code cannot be trusted to correctly translate the original code, making manual validation of translated Java code from COBOL a necessary but time-consuming and labor-intensive process" — abstract
> "The results not only help identify and repair any detected discrepancies but also provide feedback to improve the AI model." — abstract
