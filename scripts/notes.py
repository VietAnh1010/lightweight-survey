"""Per-paper note format: write, parse, validate.

One markdown file per included paper, at papers/notes/<citekey>.md, with a
fixed set of `## ` headings. Fixed headings rather than YAML frontmatter so the
files stay pleasant to read and edit by hand while still being machine-parsable
without a third-party dependency.

The Evidence section is not decoration. Every claim that reaches the synthesis
must be traceable to a quote here, and every quote must come from text we
fetched.
"""

from __future__ import annotations

import re
from pathlib import Path

from common import NOTES_DIR, clean_text

# Order is the order they appear in the template and the bibliography.
SECTIONS = ["Problem", "Main ideas", "Evaluation", "Limitations", "Follow-ups", "Evidence"]

# A note missing any of these cannot support a table row, so verify fails on it.
REQUIRED_SECTIONS = ["Problem", "Main ideas", "Evaluation", "Limitations", "Evidence"]

_HEADING = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)


def note_path(citekey: str) -> Path:
    return NOTES_DIR / f"{citekey}.md"


def parse_note(path: Path) -> dict[str, str]:
    """Return {lowercased heading: body text}. Unknown headings are kept."""
    text = path.read_text(encoding="utf-8")
    sections: dict[str, str] = {}
    matches = list(_HEADING.finditer(text))
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        sections[match.group(1).strip().lower()] = text[match.end():end].strip()
    return sections


def missing_sections(sections: dict[str, str]) -> list[str]:
    """Required headings that are absent or empty (a `TODO` body counts as empty)."""
    out = []
    for name in REQUIRED_SECTIONS:
        body = sections.get(name.lower(), "").strip()
        # Strip blockquote markers first, so an untouched Evidence stub
        # ("> TODO quote ...") is recognised as empty rather than as content.
        body = re.sub(r"^\s*>\s*", "", body)
        if not body or body.upper().startswith("TODO"):
            out.append(name)
    return out


def summarize(body: str, limit: int = 220) -> str:
    """Collapse a section to one table cell."""
    text = clean_text(re.sub(r"^[-*>]\s*", "", body, flags=re.MULTILINE))
    text = text.replace("|", "\\|")
    if len(text) <= limit:
        return text
    return text[: limit - 1].rsplit(" ", 1)[0] + "…"


def template(rec: dict) -> str:
    """Blank note for one record, pre-filled with metadata we already trust."""
    authors = rec.get("authors") or []
    author_line = ", ".join(authors[:4]) + (" et al." if len(authors) > 4 else "")
    venue = rec.get("venue_short") or rec.get("venue") or "?"
    link = rec.get("url") or rec.get("pdf_url") or ""

    lines = [
        f"# {rec.get('title', 'Untitled')}",
        "",
        f"- **Citekey:** {rec.get('citekey', '')}",
        f"- **Record:** {rec['id']}",
        f"- **Authors:** {author_line}",
        f"- **Venue:** {venue} {rec.get('year', '')}".rstrip(),
        f"- **Categories:** {', '.join(rec.get('categories') or [])}",
        f"- **Link:** {link}",
        "",
    ]
    for name in SECTIONS:
        lines.append(f"## {name}")
        lines.append("")
        if name == "Evidence":
            lines.append(
                "> TODO quote the sentences supporting the claims above, each with "
                "its source (abstract / §N / Table N). Verbatim — never reworded."
            )
        else:
            # The hint disappears when the section is written. See the Style
            # section of CLAUDE.md for what it is short for.
            lines.append("TODO — bullets, one claim each, ~100 characters")
        lines.append("")
    return "\n".join(lines)
