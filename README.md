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
python3 scripts/search_openalex.py --queries-file config/queries.txt --max 200
python3 scripts/search_arxiv.py    --queries-file config/queries.txt --max 100
python3 scripts/search_s2.py       --queries-file config/queries.txt --max 100  # optional, see below
python3 scripts/enrich.py                       # backfill abstracts and venues
python3 scripts/screen.py next --limit 25       # candidates out, as JSON
python3 scripts/screen.py apply decisions.json  # decisions in, in bulk
python3 scripts/snowball.py --seed-status included
python3 scripts/report.py --stubs
python3 scripts/style_check.py                  # style gate
python3 scripts/verify_citations.py --all       # citation gate
```

Optional environment:

- `SURVEY_CONTACT_EMAIL` — the polite pool for OpenAlex and Crossref.
  - Faster and more reliable. Defaults to the repo owner's address.
- `S2_API_KEY` — **effectively required for `search_s2.py`.** Free from
  semanticscholar.org.
  - Semantic Scholar's keyless search endpoints return nothing but 429s.
  - The script gives up after three rather than spending the night on backoff.
  - Enrichment is unaffected: `enrich.py` uses `/paper/batch`, which works keylessly.
  - Without a key, OpenAlex and arXiv do the harvesting. S2 search is a recall bonus.

## Layout

```
SCOPE.md                  the scope contract — screening decisions cite this
CLAUDE.md                 operating rules, loaded into every agent session
.claude/skills/           the style contract (my-concise), enforced on the prose
STATUS.md                 live run state; the handoff if the session dies
config/queries.txt        the query grid, shared by all three search backends
papers/library.jsonl      every paper seen, deduped, one JSON record per line
papers/notes/*.md         one note per included paper, fixed headings
review/                   the deliverables
logs/events.jsonl         every query and its yield
scripts/                  the pipeline
.cache/                   raw API responses (gitignored)
```

## Design notes

**Structured APIs, not crawling.** OpenAlex is primary and supplies the
citation graph; arXiv covers preprints, which lead the published literature
here by months; Semantic Scholar adds a different relevance ranking, so
different recall. S2's batch endpoint backfills abstracts and Crossref
backfills venues. Web fetching reads specific papers; it is not for discovery.

**Snowballing is what makes it a survey.** Keyword search finds papers that
phrase things the way you do. Chasing references and citations of the accepted
set finds the ones that do not — including the foundational work nobody
phrases your way. `snowball.py` runs both directions, gated on the topic
vocabulary and the year floor so it converges.

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
