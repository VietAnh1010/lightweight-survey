# Operating rules

This repo runs a literature review unattended, overnight. Read `SCOPE.md`
before making any screening decision; follow `prompts/literature-review.md`
for the run itself.

## The one rule that matters

**Never write a paper, a title, an author, a venue, a year, a DOI, a number,
or a quotation from memory.** Every fact in this repo must come from a
response that a script or a fetch returned in this session.

You know a great deal about this literature. That knowledge is for *deciding
what to search for* and *judging what you find* — never for filling in a
field. A plausible citation is worse than a missing one, because it is
invisible. If a lookup fails, set `status: unavailable` and move on.

`scripts/verify_citations.py` enforces this: it re-resolves DOIs and arXiv ids
against live APIs, and checks that every Evidence quote attributed to an
abstract appears in the abstract we fetched. It will catch you. Run it before
declaring anything finished.

## Where state lives

| Path | What it is |
|---|---|
| `SCOPE.md` | The scope contract. Screening decisions are made against this |
| `.claude/skills/my-concise/SKILL.md` | The style contract. Every word written is judged against this |
| `papers/library.jsonl` | Every paper seen. One JSON record per line, deduped |
| `papers/notes/<citekey>.md` | One note per included paper, fixed headings |
| `review/` | Deliverables. Two of the three are generated — do not hand-edit them |
| `STATUS.md` | Live run state. The handoff if the session dies |
| `logs/events.jsonl` | Structured record of every query and its yield |
| `.cache/` | Raw API responses. Gitignored; makes re-runs free |

## Pipeline

```bash
python3 scripts/search_arxiv.py --queries-file config/queries.txt --max 100
python3 scripts/enrich.py                      # DOIs, venues, missing abstracts
python3 scripts/screen.py next --limit 25      # candidates -> stdout as JSON
python3 scripts/screen.py apply decisions.json # decisions -> library, in bulk
python3 scripts/snowball.py --seed-status included
python3 scripts/report.py --stubs              # regenerate review/, stub notes
python3 scripts/style_check.py                 # gate: my-concise, on notes + review/
python3 scripts/verify_citations.py --all      # gate: citations; non-zero on error
```

Every script is idempotent and resumable — safe to re-run after any crash.
Nothing needs installing; it is all stdlib.

**Every source here is free, keyless, and unmetered.** arXiv searches, Crossref
resolves DOIs and gives reference lists, OpenCitations gives citing papers.
Never add a keyed or metered source: it fails partway through an unattended run.

`enrich.py` is not optional. arXiv supplies almost no DOIs, and **both citation
sources are keyed on DOI**, so its Crossref title match is what makes Phase 3
possible. Run it after every harvest and every snowball round.

## Working rules

- **Screen in bulk.** `next` emits a batch, `apply` writes the verdicts back.
  - Never one subprocess per paper.
- **Screen from the abstract, not the title.** The abstract is in the batch JSON.
  - No abstract? Run `enrich.py`. Still none: mark `unavailable` rather than guess.
- **`signals` is a prior, not a verdict.** It is a keyword match; good papers trip it.
- **Checkpoint constantly.** Every batch: update `STATUS.md`, then `git add -A && git commit`.
  - A lost batch costs ten minutes. A lost session costs the night.
- **Record why.** Every include and exclude carries a `reason`.
  - A decision without one cannot be reviewed in the morning.
- **Failures are data.** A paper you could not fetch is `unavailable`, with the reason.
  - Never drop it silently, never fill the gap from memory.

## Style

**`.claude/skills/my-concise/SKILL.md` governs every word written here** —
`papers/notes/*.md`, `review/synthesis.md`, `STATUS.md`, and anything said to
the user. Read it before writing the first note.

Two things about applying it in this repo:

- **Length and format rules apply to the deliverables.** The skill exempts
  documents; that exemption is overridden here.
  - Notes and the synthesis are bullets, one claim each, near 100 characters.
- **Evidence blockquotes are exempt.** They are verbatim paper text.
  - Rewording one to pass the lint fails the quote check in `verify_citations.py`.

`scripts/style_check.py` enforces the mechanical part — the hedge list, the
metaphors from the Precise-language table, bullet and paragraph length. It
exits non-zero, like the citation gate. Accurate confidence and complete
answers it cannot check; they are still required.

Repo-specific, on top of the skill:

- Distinguish what the authors claim from what they demonstrate.
- Every claim that a technique achieves something needs its quote in Evidence.
- Attribute limitations: authors' own, or ours.
