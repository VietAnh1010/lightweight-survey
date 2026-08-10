# lightweight-survey

An unattended literature review of **LLMs in program analysis, verification,
and software testing** (2020–). Built to run overnight in a Claude cloud
session and produce something checkable in the morning.

The scope contract is `SCOPE.md`. The agent's rules are `CLAUDE.md`. The run
procedure is `prompts/literature-review.md`.

## Deliverables

| File | |
|---|---|
| `review/annotated-bibliography.md` | Included papers by category, with the note for each |
| `review/comparison-table.md` | Problem × main idea × evaluation × limitations, one row per paper |
| `review/references.bib` | BibTeX for the included set |
| `review/synthesis.md` | Cross-paper comparison, aggregated limitations, follow-ups — the one hand-written document |

## Quickstart

No dependencies. Python 3.9+, standard library only.

```bash
python3 scripts/search_arxiv.py --queries-file config/queries.txt --max 100
python3 scripts/enrich.py                       # DOIs, venues, missing abstracts
python3 scripts/screen.py next --limit 25       # candidates out, as JSON
python3 scripts/screen.py apply decisions.json  # decisions in, in bulk
python3 scripts/snowball.py --seed-status included
python3 scripts/report.py --stubs
python3 scripts/style_check.py                  # style gate
python3 scripts/verify_citations.py --all       # citation gate
```

**No API keys.** Every source is free, keyless, and unmetered:

| Source | Job |
|---|---|
| arXiv | search, and the abstract for anything Crossref left blank |
| Crossref | DOIs, published venues, and reference lists (backward snowball) |
| OpenCitations | citing papers (forward snowball) |

Optional environment:

- `SURVEY_CONTACT_EMAIL` — the polite pool for Crossref.
  - Faster and more reliable. Defaults to the repo owner's address.

Add no keyed source to this pipeline. A metered or key-gated API fails partway
through an unattended run, which is worse than not having it.

## Running this in a cloud session

**The Default cloud environment will break this run.** Its **Trusted** network
access covers package registries and cloud SDKs, none of the hosts this
pipeline needs. The repo clones, Claude reads files, and then every search,
enrichment, and snowball request is refused.

Set the environment to **Network access: Custom** at
[claude.ai/settings/claude-code](https://claude.ai/settings/claude-code), with
**"Also include default list of common package managers"** checked:

```
export.arxiv.org
api.crossref.org
api.opencitations.net
arxiv.org
```

Add the publisher domains from `.claude/settings.json` too if notes will quote
beyond the abstract — `dl.acm.org`, `openreview.net`, `link.springer.com`,
`ieeexplore.ieee.org`, `www.usenix.org`, `proceedings.mlr.press`.

## Layout

```
SCOPE.md                  the scope contract — screening decisions cite this
CLAUDE.md                 operating rules, loaded into every agent session
.claude/skills/           the style contract (my-concise), enforced on the prose
STATUS.md                 live run state; the handoff if the session dies
config/queries.txt        the query grid for the arXiv harvest
papers/library.jsonl      every paper seen, deduped, one JSON record per line
papers/notes/*.md         one note per included paper, fixed headings
review/                   the deliverables
logs/events.jsonl         every query and its yield
scripts/                  the pipeline
.cache/                   raw API responses (gitignored)
```

## Design notes

**Structured APIs, not crawling.** arXiv leads the published literature here by
months and carries a full abstract on every entry, which is what screening runs
on. Crossref supplies what arXiv cannot: the published DOI and the committee
that accepted the paper. Web fetching reads specific papers, never discovers them.

**Enrichment is load-bearing.** arXiv returns almost no DOIs — 1 of 15 on a
typical query — and both citation sources are keyed on DOI, so the Crossref
title match in `enrich.py` is what makes snowballing possible. Yield is low
because recent preprints have no published version yet; `enrich.py` reports how
many records still lack a DOI.

**Snowballing is what makes it a survey.** Keyword search finds papers that
phrase things the way you do. Chasing references and citations of the accepted
set finds the ones that do not — including the foundational work nobody
phrases your way. `snowball.py` runs both directions, gated on the topic
vocabulary and the year floor so it converges.

- backward: Crossref reference lists. Only DOI-bearing entries resolve, and the
  run reports how many were deposited as unstructured text and so were lost.
- forward: OpenCitations. Open citation data only, so a thin result means thin
  data, not an uncited paper — say which in `STATUS.md`.

**Everything is resumable.** Responses are cached on disk by URL, the library
is append-friendly JSONL written atomically, and every script is idempotent. A
crash costs the current batch. Curated fields — status, reason, categories,
priority — are never overwritten by a re-fetch, so re-running a search cannot
destroy screening work.

**Hallucination is the primary risk.** An overnight agent's worst failure is a
confident citation to a paper that does not exist. `verify_citations.py`:

- re-resolves every DOI against Crossref and every arXiv id against arXiv
- compares the returned title to the one we stored
- checks that every included paper has a complete note
- checks Evidence quotes against the abstract we fetched, verbatim

It exits non-zero, so it works as a gate. Tested against a planted fake DOI and
a planted invented quote; it catches both.

**The prose style is a contract, not a preference.** An overnight run writes
~40 notes and a synthesis with nobody to say "too verbose" halfway through.

- The style is pinned in `.claude/skills/my-concise/SKILL.md`.
- `scripts/style_check.py` checks it: hedges error, over-long bullets warn.
- Evidence blockquotes are excluded; verbatim source text is never reworded.
- The skill is a copy of `~/notes/skills/my-concise/SKILL.md`, vendored for
  the cloud session.
  - Re-copy it when the original changes.

**Two of the three review documents are generated.** The bibliography, the
comparison table, and the BibTeX derive from `papers/library.jsonl` and
`papers/notes/`. Only `review/synthesis.md` is hand-written, which keeps the
surface where prose can drift from evidence as small as possible.
