---
name: read-source
description: Extract text from source documents (PDF, DOCX, PPTX, HTML, Markdown) for spreadsheet workflows. Use to understand source material before populating workbooks.
---

## When to Use

Use `witan read` to convert source documents into LLM-ready text. This is for **source material** — PDFs, Word docs, presentations, HTML pages, and Markdown files that contain data you need to extract.

- **PDF** → plain text
- **Word** (.doc, .docx) → markdown
- **PowerPoint** (.ppt, .pptx) → markdown
- **HTML** → markdown
- **Markdown** (.md) → outline support via `--outline`

This is not for reading spreadsheet data (.xlsx, .xls) — use spreadsheet-specific tools for that.

## Setup

Files are cached server-side by content hash so repeated operations skip re-upload. If `WITAN_STATELESS=1` is set (or `--stateless` is passed), files are processed but not stored.

The CLI automatically applies per-attempt request timeouts and retries transient API failures (`408`, `429`, `500`, `502`, `503`, `504`, plus timeout/network errors). Non-retryable `4xx` responses fail immediately.

## Quick Reference

```bash
# Get document structure first
witan read report.pdf --outline
witan read slides.pptx --outline

# Read specific sections
witan read report.pdf --pages 1-5
witan read slides.pptx --slides 1-3
witan read notes.docx --offset 50 --limit 100

# Read from URLs
witan read https://example.com/report.pdf --outline
witan read https://example.com/data.csv

# JSON output for automation
witan read report.pdf --json
witan read report.pdf --outline --json
```

## Exit Codes

| Code | Meaning |
|------|---------|
| `0`  | Success |
| `1`  | Error (bad arguments, network failure, unsupported format) |

## Navigation Strategy

Go directly with `--pages`, `--slides`, or `--offset`/`--limit` when you know where to look. Use `--outline` when you don't — it gives document structure to target the right section.

**PDF workflow:**
1. `witan read report.pdf --outline` → see chapter/section structure with page ranges
2. `witan read report.pdf --pages 12-15` → read the section you need

**PPTX workflow:**
1. `witan read deck.pptx --outline` → see slide titles
2. `witan read deck.pptx --slides 5-8` → read specific slides

**Text/DOCX workflow:**
1. `witan read notes.docx --outline` → see heading structure with line offsets
2. `witan read notes.docx --offset 120 --limit 50` → read a section

## Command Reference

```
witan read <file-or-url> [flags]
```

| Flag       | Default | Description |
|------------|---------|-------------|
| `--pages`  | —       | PDF page range (e.g. `1-5`, `1,3,5`, `1-5,10-15`) |
| `--slides` | —       | Presentation slide range (e.g. `1-3`) |
| `--offset` | `1`     | Start line (1-indexed) |
| `--limit`  | `2000`  | Maximum lines to return |
| `--outline`| `false` | Show document structure instead of content |
| `--json`   | `false` | Output full JSON response |

## Pagination Limits

| Constraint | Value |
|-----------|-------|
| Max PDF pages per read | 10 |
| Max PPTX slides per read | 10 |
| Default line limit | 2000 |
| Max file size | 25 MB |

## Pipeline: Source → Spreadsheet

The typical flow for reading source material and populating a spreadsheet:

1. **Explore** — `witan read source.pdf --outline` to understand structure
2. **Read** — `witan read source.pdf --pages 3-8` to get the data
3. **Parse** — extract values from the text (LLM or regex)
4. **Write** — `witan xlsx exec model.xlsx --input-json '...'` to populate the spreadsheet

## Output Format

**Content mode** (default): line-numbered text to stdout, metadata to stderr.

```
     1	Revenue Summary
     2
     3	Q1: $1,250,000
     4	Q2: $1,380,000
text/plain  [15 pages, 10 read, 847 lines total, showing 1–847]
```

**Outline mode** (`--outline`): indented structure to stdout.

```
Introduction  [pages 1-2]
  Background  [pages 1-1]
  Methodology  [pages 2-2]
Results  [pages 3-8]
  Financial Summary  [pages 3-5]
  Projections  [pages 6-8]
Appendix  [pages 9-15]
[15 pages]
```

## Error Guide

| Error | Fix |
|-------|-----|
| `cannot access file` | Check file path exists and is readable |
| `downloading URL: HTTP 4xx/5xx` | Check the URL is accessible |
| `payload_too_large` | File exceeds 25 MB limit |
| `missing_content_type` | Set Content-Type header (API only) |
| Empty outline | Document has no bookmarks/headings; use offset/limit to navigate |
| Truncated text | Use `--pages`, `--slides`, or increase `--limit` |
