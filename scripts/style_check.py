"""Lint the written prose against the my-concise skill.

The skill is `.claude/skills/my-concise/SKILL.md`, and it — not this script —
is the contract. This checks only the mechanical subset: the hedge list, the
metaphors in the Precise-language table, and bullet and paragraph length.
Accurate confidence and complete answers are not checkable here; they are
still required.

What is checked:

  papers/notes/*.md   everything from the first `## ` heading onward
  review/*.md         except the files report.py generates

Skipped, deliberately: the note metadata block, fenced code, markdown tables,
and blockquotes. Blockquotes are Evidence — verbatim text from a paper, which
must never be reworded to satisfy a style rule.

    python3 scripts/style_check.py           # notes + hand-written review docs
    python3 scripts/style_check.py STATUS.md # any file, explicitly

Exits non-zero if any ERROR is found, so it works as a gate alongside
verify_citations.py.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

from common import NOTES_DIR, ROOT, log_event

REVIEW_DIR = ROOT / "review"

# report.py writes these from the library and the notes; fixing style here
# would be overwritten on the next run. Fix the note instead.
GENERATED = {"annotated-bibliography.md", "comparison-table.md", "references.bib"}

# The skill's list, verbatim. Deleting one of these never loses information,
# which is why they are errors rather than warnings.
HEDGES = [
    "basically", "essentially", "actually", "really", "quite",
    "it's worth noting", "it is worth noting", "a number of",
]

# The "Don't" column of the skill's Precise language table. Warnings, not
# errors: the table is explicitly a set of examples, and some of these phrases
# are literal domain terms here ("the fuzzer feeds inputs to the target").
METAPHORS = [
    (r"load-bearing", "name the dependency: 'the proof depends on X'"),
    (r"\blives? in\b", "'has type X' / 'is defined in X'"),
    (r"\bfeeds?\b.{0,20}\bto\b", "'applies f to x'"),
    (r"\blands? in\b", "'the codomain is X'"),
    (r"\bbaked[ -]in\b", "'hardcoded'"),
    (r"\bgets? picked up\b", "say when and by what it is read"),
    (r"(does|do)n't play nicely with", "'conflicts with X'"),
    (r"\bcover(s)? everything\b", "'the case analysis is exhaustive'"),
]

BULLET_TARGET = 100   # the skill's per-bullet budget
BULLET_LIMIT = 120    # "approximately 100" — warn past 20% slack
PARAGRAPH_LIMIT = 400  # past this, a paragraph should have been bullets

_HEDGE_RE = [(h, re.compile(rf"(?<!\w){re.escape(h)}(?!\w)", re.IGNORECASE)) for h in HEDGES]
_METAPHOR_RE = [(re.compile(p, re.IGNORECASE), fix) for p, fix in METAPHORS]
_BULLET = re.compile(r"^\s*([-*+]|\d+\.)\s+")

problems: list[tuple[str, str]] = []


def report(level: str, message: str) -> None:
    problems.append((level, message))


def prose_lines(path: Path) -> list[tuple[int, str]]:
    """(line number, text) for the lines the style rules apply to."""
    lines = path.read_text(encoding="utf-8").splitlines()
    is_note = path.parent == NOTES_DIR

    out: list[tuple[int, str]] = []
    in_code = False
    started = not is_note  # notes begin with a metadata block; skip it

    for n, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if is_note and not started:
            started = stripped.startswith("## ")
            continue
        if stripped.startswith(">"):      # Evidence — quoted verbatim
            continue
        if stripped.startswith("|"):      # table row
            continue
        if stripped.startswith("#"):      # heading
            continue
        out.append((n, line))
    return out


def check_wording(rel: str, lines: list[tuple[int, str]]) -> None:
    for n, line in lines:
        for word, pattern in _HEDGE_RE:
            if pattern.search(line):
                report("ERROR", f"{rel}:{n}: hedge {word!r} — delete it")
        for pattern, fix in _METAPHOR_RE:
            match = pattern.search(line)
            if match:
                report("WARN", f"{rel}:{n}: {match.group(0)!r} — prefer {fix}")


def check_shape(rel: str, lines: list[tuple[int, str]]) -> None:
    """Bullets stay near 100 characters; prose blocks do not sprawl."""
    para: list[tuple[int, str]] = []

    def flush() -> None:
        if not para:
            return
        text = " ".join(t.strip() for _, t in para).strip()
        if len(text) > PARAGRAPH_LIMIT:
            report("WARN", f"{rel}:{para[0][0]}: {len(text)}-character paragraph — "
                           f"prefer bullets, one claim each")
        para.clear()

    bullet: tuple[int, list[str]] | None = None

    def flush_bullet() -> None:
        nonlocal bullet
        if bullet is None:
            return
        n, parts = bullet
        text = _BULLET.sub("", " ".join(p.strip() for p in parts)).strip()
        if len(text) > BULLET_LIMIT:
            report("WARN", f"{rel}:{n}: {len(text)}-character bullet "
                           f"(target {BULLET_TARGET}) — split it or cut it")
        bullet = None

    for n, line in lines:
        if not line.strip():
            flush_bullet()
            flush()
            continue
        if _BULLET.match(line):
            flush_bullet()
            flush()
            bullet = (n, [line])
        elif bullet is not None and line.startswith((" ", "\t")):
            bullet[1].append(line)  # continuation of the same bullet
        else:
            flush_bullet()
            para.append((n, line))
    flush_bullet()
    flush()


def targets(explicit: list[str]) -> list[Path]:
    if explicit:
        return [Path(p) if Path(p).is_absolute() else ROOT / p for p in explicit]
    paths = sorted(NOTES_DIR.glob("*.md")) if NOTES_DIR.exists() else []
    if REVIEW_DIR.exists():
        paths += [p for p in sorted(REVIEW_DIR.rglob("*.md")) if p.name not in GENERATED]
    return paths


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*", help="files to check (default: notes + review/)")
    args = ap.parse_args()

    paths = targets(args.paths)
    if not paths:
        print("nothing to check: no notes and no hand-written review documents")
        return

    for path in paths:
        if not path.exists():
            report("ERROR", f"{path}: no such file")
            continue
        rel = str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)
        lines = prose_lines(path)
        check_wording(rel, lines)
        check_shape(rel, lines)

    grouped: dict[str, list[str]] = defaultdict(list)
    for level, message in problems:
        grouped[level].append(message)
    for level in ("ERROR", "WARN"):
        for message in grouped[level]:
            print(f"{level}: {message}")

    errors, warns = len(grouped["ERROR"]), len(grouped["WARN"])
    print(f"\nchecked {len(paths)} files against my-concise: {errors} errors, {warns} warnings")
    log_event("style_check", files=len(paths), errors=errors, warnings=warns)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
