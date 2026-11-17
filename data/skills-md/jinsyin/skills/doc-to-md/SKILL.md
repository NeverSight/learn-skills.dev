---
name: doc-to-md
description: >-
  Convert documents (PDF, Office, HTML, EPUB, images, audio, etc.) to faithful
  Markdown saved beside the source: markitdown and markdownlint, then refine
  structure and strip extraction noise against the source without rewriting text.
disable-model-invocation: true
---

# doc-to-md

Convert documents into clean, **faithful, structurally correct** Markdown, saved **in the source file's directory, with the same base name, and only the extension changed to `.md`**.

The pipeline has two stages:

1. **Deterministic stage (`scripts/convert.sh`)**: `markitdown` (extract) → `postprocess.py` (semantic cleanup) → `markdownlint-cli2 --fix` (lenient formatting rules). **Always call the script** for conversion and lint; it handles output paths, directory expansion, overwrite protection, cleanup, and lint config.
2. **LLM refinement stage (you, on by default)**: markitdown flattens layout into text, losing heading levels, tables, multi-column reading order, and hyphenation/page breaks — the script cannot recover these. After the script runs, **compare against the source** to restore structure and strip extraction noise. See [LLM refinement](#llm-refinement).

## Workflow

### 1. Check tools

`markitdown` must be on PATH (`command -v markitdown`). If missing, tell the user to run `pip install 'markitdown[all]'`, then stop.
Lint runs via `npx markdownlint-cli2`. Without `npx`, the script skips lint and keeps the conversion — an acceptable fallback.

### 2. Overwrite protection

By default the script **refuses to overwrite** an existing `.md` and reports `EXISTS\t<path>` with exit code `3`. Overwriting is the user's call, not the script's.

So **first run without `--force`**:

- No conflict → conversion completes.
- `EXISTS` (exit 3) → name the files that would be overwritten and **ask the user**. If they agree, rerun with `--force` on those inputs only; if not, keep the originals and skip them.

### 3. Run the script

Resolve the directory containing this `SKILL.md` as `SKILL_DIR` and call the bundled script through that path.

```bash
# Single file
"$SKILL_DIR/scripts/convert.sh" path/to/report.pdf

# Batch: several files
"$SKILL_DIR/scripts/convert.sh" a.docx b.pptx c.html

# Batch: a directory (all supported documents, not recursive)
"$SKILL_DIR/scripts/convert.sh" ./docs

# After the user confirms overwrite
"$SKILL_DIR/scripts/convert.sh" --force path/to/report.pdf
```

The script derives the output path: `report.pdf` → `report.md` in the same directory.

### 4. LLM refinement (default)

**Refine every `.md` generated in this run** following [LLM refinement](#llm-refinement).

Skip refinement when the user asks for raw output / no refinement / speed, or when conversion produced nothing. For a large batch (more than about ten files), first say refinement goes file by file and takes time, then ask: refine all, refine only key files, or keep the raw output. Wait for the answer before refining.

### 5. Report

Briefly tell the user:

- Which `.md` files were generated (full paths).
- **What refinement changed**, in one sentence (e.g., "fixed 3 heading levels, rebuilt the broken table on page 2, removed repeated headers"), so they can tell structural fixes from content changes.
- Any **non-auto-fixable** lint warnings the script printed, summarized, noting they usually stem from the source structure and do not mean the conversion failed.

## LLM refinement

**Why**: these defects come from extraction, not the document; `postprocess.py` and lint fix only the safe deterministic cases, the rest needs your judgment against the source.

**Hard rule — stay faithful: fix structure, remove noise, keep the author's words verbatim.** Others will treat the output as a trustworthy copy; one "polished" sentence silently corrupts it.

- You are restoring what the author wrote, not creating. The moment you want to "smooth this sentence" or "add a clarifying line", stop — that is content drift.
- When unsure whether something is noise or content, **keep it**. A stray page number is better than a lost line of body text.
- **Never invent** what the source does not show. Fix garbled or missing characters only when the source confirms them; otherwise leave them as is.

**How:**

1. `Read` the source file first (Read renders PDFs and images; HTML, CSV, JSON, and XML read as text); it is the **only source of truth**. Then `Read` the generated `.md`.
   When `Read` cannot render the source (Office files, EPUB, audio, huge PDFs), refine from the `.md` alone: fix only structure visible in it (hyphenation, obvious lists/headings), leave unverifiable table content as converted, and tell the user the source was not checked.
2. Make **targeted `Edit`s** that change only what is wrong. Targeted edits keep changes visible and avoid dropping content. Rewrite fully only when the structure is too broken to patch, then check section count and length against the source to confirm nothing is missing.
3. Finish with `"$SKILL_DIR/scripts/convert.sh" --lint-only <those .md>` to tidy indentation, blank lines, and trailing spaces from manual edits. It does **not** reconvert or overwrite your work.

**Checklist (moderate: structural fixes + noise removal, wording untouched)**

Structural fixes (against the source layout):

- **Heading levels**: markitdown often flattens or misassigns them. Set `#` levels from the source's visual hierarchy (font size, numbering like `1.` / `1.1` / `一、`).
- **Tables**: rebuild scattered, column-shifted, or merged-cell-lost tables from the source — align column counts, restore merged/empty cell content, rejoin rows split across lines.
- **Lists**: turn items rendered as plain paragraphs into `-` / `1.` lists; fix nesting.
- **Reading order**: multi-column PDFs are often interleaved; reorder to the source's natural flow.
- **Hyphenation and line wraps**: rejoin words split at line ends (`infor-\nmation` → `information`); merge hard-wrapped lines back into full paragraphs.
- **Code / formulas**: fence code blocks; keep formulas verbatim (keep LaTeX that is clearly LaTeX).

Noise removal (confirm in the source that it is layout decoration, not body text):

- Headers/footers repeated on every page (book or chapter titles).
- Standalone page numbers.
- Watermark text bleeding into the body.
- Leftover TOC dot leaders that `postprocess` missed.
- **Obvious, verifiable** OCR errors (e.g., `rn`→`m`, `0`↔`O`) — only when the source makes the correct form unambiguous.

**Self-check**: every heading, table, caption, and paragraph in the source must have a counterpart in the output. Removing noise is fine; losing content is not.

## Edge cases and fallbacks

- **Conversion fails** (markitdown exits non-zero, e.g., encrypted PDF, corrupt file): the script deletes the partial output, reports exit code 2, and continues with other inputs. Report the failed files truthfully.
- **No npx**: lint is skipped; the conversion is saved.
- Exit codes: `0` success / `2` conversion failed / `3` overwrite needs confirmation / `4` no input to process; `--lint-only` follows the same codes (no `.md` input → 4).

## Reference: deterministic stage

### postprocess.py

`scripts/postprocess.py` runs before lint and fixes structure lint cannot. Rules are conservative — anything unmatched passes through untouched:

- **TOC block** → list: consecutive entries after a `目录` / `Table of Contents` / `Contents` heading become `- ` items, dot leaders (`......`) collapse to one space, page numbers stay; existing list items are left alone.
- **Bare JSON** → fenced: a paragraph that `json.loads` parses is wrapped in ` ```json `; already-fenced blocks and non-JSON like `{placeholder}` are untouched.
- **Empty table rows** → removed: rows with only empty cells (e.g., `|  |  |`) go; separator rows `| --- |` and data rows stay.

Pure Python with no dependencies; always runs, even with `--no-lint`, because it shapes output structure rather than formatting.

### Lint rules

`assets/markdownlint.jsonc` is a lenient ruleset for converted output: rules meaningless for extracted text (line length, inline HTML, first-line heading, multiple H1s, list renumbering, etc.) are off; the rest stay default so `--fix` cleans what it can.
