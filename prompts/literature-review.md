# Overnight literature review run

Paste this as the prompt for the cloud session. `CLAUDE.md` and `SCOPE.md`
carry the rules; this is the procedure.

---

You are running an unattended literature review. Read `CLAUDE.md`, `SCOPE.md`,
and `.claude/skills/my-concise/SKILL.md` first, in full, and work through the
phases below. The three are the contracts: rules, scope, style.

Two things matter more than finishing: **never invent a citation** (see the
rule in `CLAUDE.md`), and **commit after every batch** so a crash costs one
batch and not the night.

Work continuously. Do not stop to ask questions — record the question in
`STATUS.md` under "Open questions" and proceed with your best judgement.

**If the first search fails against every host, stop.** That is the cloud
environment's network allowlist, not the APIs — see "Running this in a cloud
session" in `README.md`. Retrying cannot fix it. Record it in `STATUS.md` and
end the session rather than burning the night on backoff.

## Phase 1 — Harvest (target ~1 hour)

```bash
python3 scripts/search_arxiv.py --queries-file config/queries.txt --max 100
python3 scripts/enrich.py
python3 scripts/screen.py stats
```

The grid in `config/queries.txt` carries the whole harvest — widen it before
screening rather than after. It also caps the harvest: 80 queries at `--max
100` is 8000 hits before dedup and the topic gate.

`enrich.py` is the second half of the harvest, not a tidy-up: it finds the
published DOI and venue for records that arrive as bare preprints. Two numbers
it prints belong in `STATUS.md`:

- **no abstract** — unscreenable. Mark those `unavailable`, never guess.
- **no DOI** — cannot be snowballed from. If most included papers land here,
  Phase 3 will be thin, and that is a coverage claim you have to make honestly.

Judge the harvest by yield per query, not by the total:

- Read `logs/events.jsonl`. A query with **0 in-topic hits** is probably malformed.
- One returning far more than the rest is probably too broad.
  - Fix `config/queries.txt` and re-run that query.
- Add queries for what the grid misses. Use your knowledge to *choose
  queries*, never to add papers.
- Commit: `git add -A && git commit -m "harvest: N candidates"`.

## Phase 2 — Screen (the long phase)

Loop until the candidate pool is exhausted or the target is met:

```bash
python3 scripts/screen.py next --limit 25 > /tmp/batch.json
```

Read every abstract in the batch. For each paper decide `included`,
`excluded`, or `unavailable` against `SCOPE.md`, then write
`/tmp/decisions.json`:

```json
[
  {"id": "doi:10.1145/...", "status": "included",
   "reason": "composes an LLM proposal step with an SMT check; the repair loop is the contribution",
   "categories": ["formal-verification", "program-logic"], "priority": 3},
  {"id": "arxiv:2401.12345", "status": "excluded",
   "reason": "wrapper — prompts GPT-4 for tests and reports pass rates, no technique"}
]
```

```bash
python3 scripts/screen.py apply /tmp/decisions.json
```

`priority` is 1–3 and drives ordering later: **3** = clearly central, **2** =
solid and in scope, **1** = borderline, included with doubt noted.

Batches are ordered target-venue-first, so if the run is cut short, what got
screened is what mattered. **Never screen a pool you have not enriched** —
straight from arXiv every record reads as venue "arXiv" with no citation count,
the sort keys all tie, and that guarantee does not hold.

After every batch: update `STATUS.md` with counts and where you are, then
commit.

## Phase 3 — Snowball

Once ~20 papers are included:

```bash
python3 scripts/snowball.py --seed-status included --direction both
python3 scripts/enrich.py
```

This adds candidates from the references (Crossref) and citations
(OpenCitations) of what you accepted. Snowballed records arrive as bare DOIs,
so `enrich.py` is what makes them screenable. Screen the new pool as in Phase
2, then snowball again.

Snowballing only reaches seeds with a DOI. Put the reach numbers `snowball.py`
prints into `STATUS.md`: they separate "the literature is thin here" from "our
sources are thin here", and only the first is a finding.

Stop when the criterion in `SCOPE.md` is met — two consecutive rounds each
yielding fewer than 5 new in-scope candidates — or the time budget runs out.
**Write down which one it was**; it determines what can honestly be claimed
about coverage.

Also: read the surveys you excluded. Their reference lists are the highest
yield seeds available. Feed titles you find there back through
`search_arxiv.py --query "<title>"` — never straight into the library.

## Phase 4 — Select the 40

Aim for 40 included papers with coverage across categories, not the 40 most
cited. `python3 scripts/screen.py stats` shows the category and venue
breakdown.

If a category is empty, run targeted queries for it before concluding the
literature is empty there. If one category dominates, demote its weakest
entries to `excluded` with `reason: "cut for balance — <what it duplicates>"`.
Never delete a record; the excluded set is part of the result.

## Phase 5 — Notes

```bash
python3 scripts/report.py --stubs
```

Fill in `papers/notes/<citekey>.md` for every included paper, highest priority
first. Each note needs Problem, Main ideas, Evaluation, Limitations,
Follow-ups, and Evidence.

**Read `.claude/skills/my-concise/SKILL.md` before the first note.** Every
section is bullets, one claim per bullet, near 100 characters. No hedges, no
metaphors where an exact term exists. Run `python3 scripts/style_check.py`
after each batch of notes and fix what it reports.

Write from the abstract you have. Where more depth is needed, fetch the paper
(`pdf_url` in the record, or arXiv) and read it — then say so in the note.
**Evidence quotes attributed to the abstract are checked verbatim against the
stored abstract**, so quote exactly or attribute to the section you read.
Quotes are exempt from the style rules — never reword one.

Commit every 5 notes.

## Phase 6 — Synthesise

```bash
python3 scripts/report.py
```

That regenerates `review/annotated-bibliography.md`,
`review/comparison-table.md`, and `review/references.bib`. Do not hand-edit
them.

Then write `review/synthesis.md` — the one hand-written document. Cite papers
by citekey in backticks. `.claude/skills/my-concise/SKILL.md` applies in full:
bullets under headings, one claim each, no hedges. This is the document where
prose sprawl is most tempting and least useful. It should cover:

1. **What the field is doing** — the recurring architectural patterns.
   - Where does the LLM sit relative to the sound component?
   - Proposer checked by a verifier; heuristic in a search.
   - Translator between informal and formal; repair loop over a failing check.
2. **Cross-cutting comparison** — read down the columns of the comparison table.
   - Which problems attract which patterns, and why.
   - Where papers on the same problem disagree about approach.
3. **Evaluation practice** — what is measured, what is not, which benchmarks recur.
   - Where contamination or weak baselines make numbers incomparable.
4. **Limitations, aggregated** — what recurs across papers is the field's open
   problem, not one paper's.
5. **Follow-ups** — concrete gaps.
   - Prefer "no one has tried X for Y, and why that is now feasible" over
     "more research is needed".

Every claim about a paper traces to its note. Every count and every category
figure comes from `screen.py stats`, not from your impression.

## Phase 7 — Verify

```bash
python3 scripts/report.py
python3 scripts/style_check.py
python3 scripts/verify_citations.py --all
```

**Fix every ERROR from both.** `verify_citations.py` errors are
hallucinations, broken identifiers, or missing notes. `style_check.py` errors
are hedges, safe to delete. Fix the WARNs or explain them in `STATUS.md`.

Re-run both until they exit clean, then commit.

## Finally

Write the closing summary in `STATUS.md`:

- counts: candidates seen, screened, included, excluded, unavailable
- which stopping criterion ended the run
- categories that came out thin, and whether that is the literature or the run
- anything you were unsure about, and the calls you made
- what you would do with another eight hours

Then a final `git commit`.
