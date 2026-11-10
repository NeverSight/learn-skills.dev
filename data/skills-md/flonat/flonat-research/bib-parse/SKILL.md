---
name: bib-parse
description: "Extract citations from a PDF and generate a validated .bib file. Use when the user asks to extract citations from a PDF and generate a validated .bib file. Reads the PDF, identifies referenced works, constructs BibTeX entries, and verifies metadata."
allowed-tools: Read, Glob, Grep, Write, Bash(mkdir*), Bash(ls*), Bash(uv*), WebFetch, WebSearch, Skill(split-pdf), Bash(paperpile*)
argument-hint: <path-to-pdf>
skill-dependencies: [split-pdf]
---

# Bibliography Parser — PDF to .bib

**LIBRARY-FIRST RULE: ALWAYS check Paperpile membership by DOI (`paperpile lookup-by-doi`) for each parsed reference BEFORE generating new BibTeX entries.** Topic/title `search-library` is a lossy discovery aid, NOT a membership test — never tag a reference `NEW` off a title-search miss. Reuse existing library entries instead of constructing from scratch. Enforced in Phase 2.3 per [`shared/reference-resolution.md`](../shared/reference-resolution.md) § Membership Check.

**Goal:** given a PDF file, extract all cited references and produce a clean, validated `.bib` file.

## When to Use

- You have a PDF (paper, report, thesis) and need a `.bib` file for its references
- Importing references from a paper that doesn't have a companion `.bib` file
- Reconstructing a bibliography from a document with embedded `\begin{thebibliography}` or numbered references
- Converting a reference list from any format into BibTeX

## When NOT to Use

- **You already have a `.bib` file** and just need to validate it — use the configured bibliography validator
- **Finding new references on a topic** — use an installed literature workflow or scholarly search
- **The PDF is already in Paperpile** — export via `paperpile export-bib` instead (faster, more accurate)

## Input

A single PDF file path. The PDF should contain a bibliography, reference list, or works cited section.

## Output

A `.bib` file, located by context:

- **PDF inside a research project** (e.g. `articles/`, `paper-*/`, project root) — write to the same directory as the input PDF, named `references.bib` (per project convention). If `references.bib` already exists, ask before overwriting — offer to merge or use a different name (e.g., `extracted-refs.bib`).
- **Standalone PDF** (ad-hoc extraction with no project home — e.g. a client-managed upload) — write to `~/vault/parsed-bibs/<slug>.bib`, where `<slug>` describes the source (e.g. `kasberger-algorithmic-cooperation-geb-2026.bib`). This is the standing location for one-off parses (established 2026-06-14). Create the folder if absent.

Any staged Paperpile-import entry (Phase 4.1) is written into a `.bib` under `.paperpile-import/` next to the output `.bib`.

---

## Phase 1: Read

### 1.1 Read the PDF

Use `split-pdf` to read the PDF contents. This handles large PDFs by splitting into chunks. Focus on the bibliography / references section — typically the last few pages. Identify:

- Numbered reference lists (e.g., `[1] Smith, J. (2020)...`)
- APA / Harvard style reference lists
- `\bibitem` entries (if the PDF was generated from LaTeX)
- Footnote-based citations

### 1.2 Skeleton confirmation (mandatory for ≥10 references)

Before running any enrichment queries, **render the parsed reference list as a numbered table and ask the user to confirm the split is correct**. A misparsed reference list (one citation accidentally split across two rows, or two citations merged into one) makes Phase 2 spend 30+ API calls on the wrong entries — expensive in time and rate-limit budget.

```markdown
Detected N references. Confirm the split before I enrich each one:

| # | parsed reference (verbatim) |
|---|----------------------------|
| 1 | Bebchuk, L. A., Cohen, A., & Hirst, S. (2017). The agency problems of institutional investors... |
| 2 | Smith, J. (2020). Title... |
| ... | ... |

Anything wrong with the split? (Reply "ok" to proceed, or list the row numbers that need merging/splitting.)
```

Skip the confirmation step if any of these:

- Fewer than 10 references parsed (cheap to fix after the fact)
- The PDF was generated from LaTeX and `\bibitem` boundaries are unambiguous
- The user explicitly said "just go" / "no confirmation"

When the user flags a bad split, fix it and re-render the skeleton before proceeding. Don't proceed to Phase 2 with unaddressed split issues — that's exactly the failure case this gate prevents.

---

## Phase 2: Enrich

### 2.1 Extract reference metadata

For each reference found, extract:

| Field | Priority | Notes |
|-------|----------|-------|
| **Authors** | Required | Full names, `{Last, First and Last, First}` BibTeX format |
| **Title** | Required | Exact title from the reference |
| **Year** | Required | Publication year |
| **Journal / Booktitle** | Required (articles/proceedings) | Full journal name, not abbreviation |
| **Volume / Number / Pages** | If available | Standard bibliographic fields |
| **Publisher** | If available | For books and proceedings |
| **DOI** | Best effort | Extract if printed in the reference |

**Large reference lists (50+ entries):** process in batches of ~20. Verify each batch before moving to the next. Report progress: "Processed 20/87 references...". This caps the rate-limit blast radius if a batch fails.

### 2.2 Verify and enrich

For each extracted reference, verify and enrich using available tools:

1. **Search by title** via `web search` to confirm the reference exists and pull missing metadata (DOI, volume, pages).
2. **Use the `scholarly` CLI** for multi-source enrichment:
   - `scholarly scholarly-search "<title>" --json` — search by title across OpenAlex + S2 + Scopus + WoS
   - `scholarly scholarly-paper-detail <paper_id> --json` — get full metadata including pre-formatted BibTeX (`citationStyles`), TLDR summary, and open access PDF link. When BibTeX is available, use it as the primary template instead of manually constructing entries — reduces formatting errors.
   - `scholarly openalex-lookup-doi <doi> --json` — get full metadata if DOI was found.
3. **Cross-check** extracted metadata against search results: confirm author names, year, fill in missing DOI/volume/pages/publisher.

**Important:** do NOT silently replace the extracted metadata with search results. If there's a conflict (e.g., different year, different spelling of author name), flag it as a `note` field in the `.bib` entry and keep the original from the PDF.

### 2.3 Check Paperpile library (LIBRARY-FIRST gate)

For each parsed reference, check if it already exists in Paperpile using the resolution order from [`shared/reference-resolution.md`](../shared/reference-resolution.md):

1. **Check membership by DOI** — `paperpile lookup-by-doi --doi <DOI>` for each parsed reference (verify the DOI itself first if unsure). This is the membership test. Batch ≥6 references via one Bash sub-agent returning a merged `{doi: citekey-or-null}` map.
2. **Only for DOI-less references**, fall back to `paperpile search-library` with first-author surname + title keywords (limit ≥10) — a discovery aid, not a membership test.
3. **Match → ALREADY IN PAPERPILE**: reuse the returned Paperpile citekey, skip staging in Phase 4.1. **A confirmed DOI miss (or, for DOI-less refs, an author+title miss) → `NEW`** — never tag `NEW` off a `search-library` miss alone. Foundational classics (Simon, March, Levinthal, Cyert & March, …) are the most common false `NEW`; check them by DOI too.

**Status summary:**

| Paperpile | Status | Phase 4.1 action |
|-----------|--------|------------------|
| Yes | `ALREADY IN PAPERPILE` | Skip (reuse key) |
| No | `NEW` | Stage as BibTeX for Paperpile import |

**Graceful degradation:** if the `paperpile` CLI is unavailable, skip with a warning and treat all references as `NEW`.

---

## Phase 3: Construct

### 3.1 Generate citation keys

Better BibTeX conventions:

- Format: `{Author}{Year}-{xx}` — e.g., `Smith2020-xy`
- First author's last name, title-cased
- Four-digit year
- Two-character suffix (Better BibTeX style)
- If merging into an existing `.bib`, match the key format already in use
- For references already in Paperpile (Phase 2.3), **copy the Paperpile citekey into the entry** (do not keep the generated key) and **backfill the DOI** from Paperpile, but **keep the richer local metadata** (type, journal, volume, pages, full authors — Paperpile's `export-bib` is `@misc`/thin). Add `note = {key reconciled to Paperpile <key>}`. Full rule + first-author-match guard: [`shared/reference-resolution.md`](../shared/reference-resolution.md) § Key Reconciliation.

### 3.2 Determine entry types

| Source type | BibTeX type | Key fields |
|-------------|-------------|------------|
| Journal article | `@article` | author, title, journal, year, volume, number, pages |
| Conference paper | `@inproceedings` | author, title, booktitle, year, pages |
| Book | `@book` | author/editor, title, publisher, year |
| Book chapter | `@incollection` | author, title, booktitle, publisher, year, pages |
| Working paper / preprint | `@techreport` or `@unpublished` | author, title, institution/note, year |
| Thesis | `@phdthesis` or `@mastersthesis` | author, title, school, year |
| Website / online | `@misc` | author, title, howpublished, year, note |

### 3.3 Write the .bib file

Write entries to the output `.bib` file with:

- One blank line between entries
- Fields indented with 2 spaces
- Required fields first, then optional fields
- DOI field included when available
- A `note` field for any metadata conflicts or uncertainties flagged in 2.2

Example entry:

```bibtex
@article{smith2020optimal,
  author = {Smith, John and Doe, Jane},
  title = {Optimal Decision Making Under Uncertainty},
  journal = {Management Science},
  year = {2020},
  volume = {66},
  number = {3},
  pages = {1234--1256},
  doi = {10.1287/mnsc.2019.3456}
}
```

### 3.4 Quality fallbacks

Two cases that cross sub-steps:

**Poor OCR / unreadable references** (PDFs with poor text extraction, scanned documents, unusual formatting):

1. Flag references that couldn't be reliably parsed.
2. Add them as `@misc` entries with `note = {MANUAL CHECK NEEDED: ...}`.
3. Include whatever text was extracted so the user can fix it manually.

**Incomplete references** (missing key fields like year or journal):

1. Attempt to find the complete reference via web search (typically already done in 2.2).
2. If found, fill in the missing fields and add `note = {metadata enriched from web search}`.
3. If not found, write what's available and flag with `note = {INCOMPLETE: missing [field]}`.

---

## Phase 4: Validate

### 4.1 Stage for Paperpile import

Follow the filing sequence from [`shared/reference-resolution.md`](../shared/reference-resolution.md). For references marked **NEW** in Phase 2.3:

1. Present a summary table before staging:

   | # | Key | Title | Authors | Year | Status |
   |---|-----|-------|---------|------|--------|
   | 1 | Smith2020-xy | Title... | Smith, J. | 2020 | NEW — staging for import |
   | 2 | Doe2019-ab | Title... | Doe, J. | 2019 | ALREADY IN PAPERPILE (skipped) |

2. **Stage under `.paperpile-import/`** — write each new entry's BibTeX into a `.bib` under `.paperpile-import/` (Paperpile CLI is read-only; `write-bib --citekeys` only exports entries already in the library). Mark any draft cite `\CiteTodo{...}` until imported.
3. **Remind user** — "Import the staged `.bib` under `.paperpile-import/` into Paperpile to complete the sync."

**Graceful degradation:** if the `paperpile` CLI is unavailable, skip this sub-step. The `.bib` file from Phase 3.3 is still the primary output.

### 4.2 Validate the generated bibliography (HARD GATE)

Run the configured bibliography validator when installed. Otherwise perform these checks directly:

- Check for required fields
- Verify DOIs resolve correctly
- Flag any remaining issues

Surface the validation report inline in the final summary (see Report section below). Do not proceed to 4.3 when citation keys are unresolved, required fields are missing, or metadata cannot be verified—fix and re-validate first.

### 4.3 Output verification (before commit)

Before any auto-commit, emit an outputs manifest and run the shared verifier per [`_shared/verify-outputs.md`](../_shared/verify-outputs.md):

1. Write manifest to `<project>/.claude/state/outputs-manifest-<UTC-timestamp>.json` listing every file this skill claims to have written, paths relative to the project root.
2. Run:

   ```bash
   uv run python "<skills-root>/_shared/verify_outputs.py" \
       --manifest "$MANIFEST" \
       --project-root "$PROJECT_ROOT"
   ```

3. If the verifier exits non-zero, **do not commit**. Surface the missing-files list and stop. The verifier logs an `error` entry to `~/.local/state/ai-workflows/skill-outcomes.jsonl`.

Closes the "hallucinated outputs" failure class (commit `b2cff75`, 2026-04-18).

---

## Report

After completion, provide a summary:

```
## bib-parse Summary

**Input:** [filename.pdf]
**Output:** [output.bib]

| Metric | Count |
|--------|-------|
| References found in PDF | X |
| Successfully parsed | Y |
| DOIs found/verified | Z |
| Already in Paperpile | A |
| Staged for Paperpile import | B |
| Flagged for manual review | W |

### Bibliography validation report
[paste the configured validator's verdict, or the direct checks performed, plus any critical issues]

### Entries needing attention
- `key1` — missing journal name
- `key2` — year mismatch between PDF (2019) and DOI lookup (2020)
```

---

## Cross-References

- Installed bibliography validator — validates the generated `.bib` file when available in Phase 4.2
- [`bib-coverage`](../bib-coverage/SKILL.md) — compare project `.bib` vs Paperpile project/topic folder — find uncited papers and unfiled references
- [`split-pdf`](../split-pdf/SKILL.md) — reads the input PDF (called in Phase 1.1)
- Installed literature workflow or scholarly search — for finding additional references beyond what's in the PDF
- [`shared/reference-resolution.md`](../shared/reference-resolution.md) — canonical lookup + filing sequence used by Phase 2.3 and Phase 4.1

## Citation Contract

<!-- paperpile-citation-contract -->
1. Paperpile is the only source of truth for committed citation keys and BibTeX metadata.
2. Before writing `\cite{key}`, verify with `paperpile get-item key` and `paperpile export-bib key`.
3. Resolve unknowns in order: DOI lookup → Paperpile substring search → `refpile` semantic search → Paperpile verify.
4. A DOI miss is **not** non-membership; continue with title/author search and refpile.
5. If unresolved, write `\CiteTodo{slug}{title/author/year/DOI hint}` — never a guessed key.
6. Drafting sub-agents must not write/edit the active `.bib`; only the orchestrator regenerates it from Paperpile exports.
7. Stage genuine new refs under `.paperpile-import/` for manual Paperpile import; don't cite until Paperpile mints the key.
8. Run `scripts/bib/citation_lint.py` before commit; zero placeholders, zero non-Paperpile keys, zero hand-authored metadata.

See `rules/paperpile-citations.md` for the full workflow.
