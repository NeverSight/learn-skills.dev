---
name: documents
description: >-
  Generate, inspect, validate, and fix PDF, Word (.docx), Excel (.xlsx), and
  PowerPoint (.pptx) documents: turn structured content into render-ready
  artifacts, verify structural and output quality before delivery, and repair
  broken files. Use when a task involves creating, editing, converting, or
  validating office documents and PDFs. Do not use for ebook packaging (use
  epub), for images, video, or other media production, for API or code
  documentation, or for data pipelines (use data-engineering).
license: MIT
compatibility: >-
  Python 3.8+ for scripts; validation uses only the standard library. Optional
  renderers for the render check: poppler-utils (pdftoppm) for PDF and
  LibreOffice for Office formats; both degrade gracefully when absent.
  Portable across all AgentSkills-compatible harnesses.
metadata:
  skills: documents, pdf, docx, xlsx, pptx, word, excel, powerpoint, office, report, generation
  tags: documents, pdf, docx, xlsx, pptx, word, excel, powerpoint, office, generation, validation
---

# Documents — PDF, Word, Excel & PowerPoint Skill

One skill for the four most common document formats. All four share a single
agent workflow — structured content in, render-ready, validated artifact out —
so they live in ONE family skill with per-format references, following the
`epub` precedent. Load the shared workflow below, then pull the per-format
reference for the format you are actually touching.

| Format | Extension | Reference (load on demand) |
|--------|-----------|----------------------------|
| PDF | `.pdf` | [references/pdf.md](references/pdf.md) |
| Word | `.docx` | [references/word.md](references/word.md) |
| Excel | `.xlsx` | [references/excel.md](references/excel.md) |
| PowerPoint | `.pptx` | [references/powerpoint.md](references/powerpoint.md) |
| All formats | — | [references/output-quality.md](references/output-quality.md) |

Generation templates for each format live in [templates/](templates/), and the
validation script with per-format fixtures lives in [scripts/](scripts/).

## When to use

Load this skill when the task involves any of the four formats:

- **Generate**: build a report, memo, spreadsheet, or deck from structured
  content (markdown, JSON, data tables, outlines).
- **Edit**: modify an existing document's content, layout, or metadata in place.
- **Extract**: pull text, tables, or structure out of an existing file.
- **Convert**: move content between formats or from a data source into a document.
- **Validate**: check that a produced artifact is structurally sound and will
  render correctly before it is delivered.

## When not to use

- **Ebooks and EPUB** — use the `epub` skill; it owns the EPUB container,
  reading order, and package validation.
- **Images, video, and other media** — this skill covers document formats only;
  route media production to the appropriate media skills.
- **Code and API documentation sites** — use the technical-documentation and
  documentation-site conventions, not office documents.
- **Data pipelines** — moving or transforming raw data belongs to
  `data-engineering`; Excel here is a *deliverable format*, not a data store.
- **Office documents to Markdown** — converting an existing office document
  (docx, xlsx, pptx, pdf, odt, rtf, epub, csv) to GitHub-Flavored Markdown
  belongs to the `anydoc` skill; this skill owns generation, editing, and
  validation, not document-to-markdown extraction.

## The Shared Workflow

Every document task follows the same six steps, regardless of format. Deep
format-specific detail is deferred to the per-format reference — read it at the
step where it matters.

### 1. Scope

Pin down what the document is for before touching a file:

- **Audience and purpose** — who reads it and what decision it supports.
- **Format** — PDF (fixed layout, print, archival), Word (editable prose,
  review), Excel (data, calculations), PowerPoint (presentation).
- **Boundaries** — page/slide count, size limits, brand or style constraints.
- **Source of truth** — the structured content the document is generated from
  (markdown, JSON, CSV, outline), so the artifact is reproducible.

### 2. Content model

Represent the document's content as structured data before rendering:

- A **title, sections/headings, body text, and metadata** for prose documents.
- A **table model** (headers, rows, column types) for spreadsheets.
- A **slide outline** (title + bullets per slide, speaker notes) for decks.
- Keep content and layout separate: content in the model, layout in the
  template. This is what makes regeneration cheap.

### 3. Template

Choose the generation template for the target format from [templates/](templates/):

- [templates/pdf-template.md](templates/pdf-template.md) — fixed-layout
  document skeleton (print-ready HTML/CSS or LaTeX source).
- [templates/word-template.md](templates/word-template.md) — Word processing
  document structure (styles, headings, tables).
- [templates/excel-template.md](templates/excel-template.md) — workbook
  structure (sheets, cells, shared strings, formulas).
- [templates/powerpoint-template.md](templates/powerpoint-template.md) — slide
  deck structure (slides, layouts, notes).

Fill the `[fill: ...]` markers in the template with content from the content
model. Templates are the contract between content and layout — changing the
template is how you change appearance without touching content.

### 4. Render

Produce the artifact file:

- **PDF** — render the template to PDF (print CSS in a browser or engine, or a
  LaTeX toolchain). See [references/pdf.md](references/pdf.md) for tooling.
- **Word / Excel / PowerPoint** — write the OOXML package directly (stdlib
  `zipfile` + XML for small artifacts) or with the conventional library for the
  format (python-docx, openpyxl, python-pptx). See the per-format reference for
  the exact package layout to produce.

### 5. Validate

Never deliver unvalidated output. Run the validation script:

```bash
python3 scripts/validate-documents.py --render-check --json report.pdf brief.docx data.xlsx deck.pptx
```

The script performs **structural sanity** (container signatures, required
parts, XML well-formedness) and, when a renderer is installed, a **render
check** (actually renders the file). When no renderer is present it reports
`unavailable` instead of failing — validation never hard-requires a renderer.
See [references/output-quality.md](references/output-quality.md) for the full
output-quality checklist, and the fixture files in
[fixtures/](fixtures/) (one per format) to smoke-test the script itself:

```bash
python3 scripts/validate-documents.py --json fixtures/sample.pdf fixtures/sample.docx fixtures/sample.xlsx fixtures/sample.pptx
```

### 6. Deliver

Hand off the artifact with its provenance:

- The **source content model** (so it can be regenerated).
- The **template version** used.
- The **validation result** (structure passed; render checked or unavailable).
- Any **known deviations** (fonts substituted, images downscaled, layout drift).

## Exit conditions

The task is complete when the artifact exists, passes structural validation
(and the render check when a renderer is available), and the content matches
the agreed scope. Stop after delivering the validated artifact with its
provenance; do not keep iterating on layout without a new scope instruction.

## Scripts

All scripts live in [scripts/](scripts/) relative to this skill's directory and
follow cli-builder conventions: `--json` for machine output, non-interactive,
errors to stderr. Run with `--help` for full flag details.

### validate-documents.py — Structural Sanity + Render Check

```bash
python3 scripts/validate-documents.py report.pdf            # human report
python3 scripts/validate-documents.py --json report.pdf    # machine report
python3 scripts/validate-documents.py --render-check --json report.pdf data.xlsx deck.pptx
```

Behavior:

- **Structural sanity** per format: PDF header/EOF/page objects; OOXML ZIP
  container, `[Content_Types].xml`, required parts, XML well-formedness.
  Legacy `.doc/.xls/.ppt` files are recognized via OLE2 magic bytes.
- **Render check** (`--render-check`): renders PDF via `pdftoppm`/`mutool`/`gs`
  and Office formats via LibreOffice. Reports `unavailable` — exit 0 — when no
  renderer is installed (graceful degradation, never a crash).
- **Exit codes**: 0 all pass (or render check unavailable); 1 a file fails
  structure or rendering; 2 usage/I/O error.
- **JSON output**: top-level `status` (`ok` / `fail` / `unavailable` / `error`)
  with per-file checks and render results.

## Related skills

- [epub](../epub/SKILL.md) — ebook container skill; the sibling family-skill
  precedent for this format family.
- [data-engineering](../data-engineering/SKILL.md) — data pipelines and
  transformation; Excel is a deliverable format here, not a data store.
- [cli-builder](../cli-builder/SKILL.md) — the CLI conventions the validation
  script follows (`--json`, non-interactive, exit codes).
