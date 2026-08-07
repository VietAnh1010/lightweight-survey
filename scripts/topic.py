"""Topic-specific vocabulary for this survey.

Everything that encodes *what we are surveying* lives here rather than in
common.py, so the scope can be retuned without touching the pipeline. Used for
three things: gating snowball expansion, auto-tagging categories, and giving
the screening agent a cheap prior.
"""

from __future__ import annotations

import re

from common import clean_text

# --------------------------------------------------------------------------
# Is this an LLM paper at all?
# --------------------------------------------------------------------------

# Deliberately broad on model families, because papers rarely say "LLM" in the
# title. Screening narrows it; this only has to avoid throwing away good work.
LLM_TERMS = re.compile(
    r"\b("
    r"large language model|language model|\bllms?\b|\bplms?\b"
    r"|gpt-?\d|gpt-4|gpt-3|chatgpt|codex|copilot"
    r"|claude|gemini|llama|mistral|qwen|deepseek|starcoder|codellama|codet5"
    r"|neural (code|program)|code (llm|language model)"
    r"|transformer|foundation model|generative ai"
    r"|prompt(ing|-based)?|in-context learning|chain[- ]of[- ]thought"
    r"|fine-?tun(e|ing)|retrieval[- ]augmented"
    r")\b",
    re.IGNORECASE,
)

# --------------------------------------------------------------------------
# Categories (SCOPE.md item 5)
# --------------------------------------------------------------------------

CATEGORY_PATTERNS: dict[str, str] = {
    "static-analysis": r"static analysis|abstract interpretation|dataflow analysis|points-?to|taint analysis|call graph|type inference|linter",
    "fuzzing": r"fuzz|greybox|coverage-guided|seed (generation|mutation)|input generation",
    "symbolic-execution": r"symbolic execution|concolic|path constraint|symbolic (state|memory)",
    "formal-verification": r"formal verification|model check|theorem prov|proof assistant|coq|lean\b|isabelle|dafny|\btla\+|refinement type|deductive verification",
    "program-logic": r"program logic|separation logic|hoare|weakest precondition|loop invariant|invariant (inference|generation|synthesis)|ranking function",
    "specification": r"specification (inference|generation|mining)|contract (inference|generation)|precondition|postcondition|assertion generation|temporal (logic|property)",
    "constraint-solving": r"\bsmt\b|\bsat\b solver|constraint solving|z3|cvc5|solver-aided",
    "test-generation": r"unit test generation|test case generation|test oracle|regression test|property-based testing|mutation testing|differential testing",
    "program-repair": r"program repair|bug fix|patch generation|\bapr\b|automated repair",
    "bug-detection": r"bug detection|vulnerability detection|defect prediction|fault localization|anomaly detection|code smell",
    "program-synthesis": r"program synthesis|code generation|sketch|synthesiz",
    "decompilation": r"decompil|reverse engineer|binary analysis|disassembl|lifting",
    "proof-automation": r"proof (automation|search|synthesis|repair)|tactic (prediction|generation)|premise selection|autoformaliz",
    "agents": r"\bagent(ic|s)?\b|multi-agent|tool use|tool-augmented|repository-level|\bswe-bench\b",
}

_COMPILED = {name: re.compile(pat, re.IGNORECASE) for name, pat in CATEGORY_PATTERNS.items()}

# --------------------------------------------------------------------------
# Signals for the "genuinely new idea" bar
# --------------------------------------------------------------------------

# Not decisive on their own. They give the screening agent a prior; the agent
# still reads the abstract and makes the call (see prompts/literature-review.md).
CONTRIBUTION_HINTS = re.compile(
    r"\bwe (present|propose|introduce|design|develop)\b|novel (technique|approach|algorithm|framework)"
    r"|new (algorithm|technique|abstraction)|we formalize|soundness|completeness"
    r"|our (technique|approach|algorithm|insight)|key insight",
    re.IGNORECASE,
)

WRAPPER_HINTS = re.compile(
    r"\b(empirical study|an? (study|evaluation|assessment|investigation|comparison) of"
    r"|benchmark(ing)? (study|evaluation)|how (well|good|effective)|can (chatgpt|gpt-4|llms?)"
    r"|exploratory study|user study|survey of|systematic (literature )?review"
    r"|we evaluate|we (study|investigate|assess|compare) (the|how|whether))\b",
    re.IGNORECASE,
)


def _haystack(rec: dict) -> str:
    return clean_text(f"{rec.get('title', '')} {rec.get('abstract', '')}")


def is_llm_paper(rec: dict) -> bool:
    return bool(LLM_TERMS.search(_haystack(rec)))


def categorize(rec: dict) -> list[str]:
    """Every category whose vocabulary shows up in the title or abstract."""
    text = _haystack(rec)
    return sorted(name for name, pat in _COMPILED.items() if pat.search(text))


def in_topic(rec: dict) -> bool:
    """LLM paper *and* at least one program-analysis/verification/testing category."""
    return is_llm_paper(rec) and bool(categorize(rec))


def screening_prior(rec: dict) -> dict:
    """Cheap signals handed to the screening agent alongside the abstract."""
    text = _haystack(rec)
    return {
        "llm": is_llm_paper(rec),
        "categories": categorize(rec),
        "contribution_signal": bool(CONTRIBUTION_HINTS.search(text)),
        "wrapper_signal": bool(WRAPPER_HINTS.search(text)),
    }
