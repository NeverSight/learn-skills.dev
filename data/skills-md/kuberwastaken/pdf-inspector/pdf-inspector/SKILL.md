---
name: pdf-inspector
description: >-
  Read, classify, and convert PDF files to Markdown locally in ~10-200ms using
  Firecrawl's pdf-inspector Rust library — no OCR service, no network, no ML
  models. Use whenever a task involves reading, extracting, summarizing, or
  converting a PDF file. Classifies text-based vs scanned first, so scanned
  pages get routed to OCR instead of silently coming back empty.
license: MIT
---

# pdf-inspector

Local PDF → Markdown built on [firecrawl/pdf-inspector](https://github.com/firecrawl/pdf-inspector):
pure Rust, single `lopdf` dependency, tops the opendataloader-bench local-parser
comparison for reading order and tables, and runs entirely offline.

## Quick use

Run the bundled wrapper (paths relative to this skill's folder). On first run it
bootstraps a venv at `~/.venvs/pdf-inspector` (override with `$PDF_INSPECTOR_VENV`)
and installs the `pdf-inspector` wheel — everything after that is offline.

```bash
python3 scripts/pdfmd.py document.pdf                  # Markdown on stdout, status on stderr
python3 scripts/pdfmd.py document.pdf --detect         # classification only (fast), JSON output
python3 scripts/pdfmd.py document.pdf --json           # full result (markdown + metadata) as JSON
python3 scripts/pdfmd.py document.pdf --text           # plain text, no Markdown structure
python3 scripts/pdfmd.py document.pdf --pages 1,3,5-10 # only these pages (1-indexed; not with --text)
```

Exit codes: `0` = extracted, `2` = no extractable text (scanned/image PDF — needs OCR), `1` = error.

## Reading the result

- `pdf_type`: `text_based` | `scanned` | `image_based` | `mixed`, with `confidence` 0.0–1.0.
- `pages_needing_ocr`: 1-indexed pages with no extractable text. Their content is **absent** from the output.
- `has_encoding_issues`: `true` means extracted text may be garbage (broken font encodings) — treat the document like a scanned one.
- `pages_with_tables` / `pages_with_columns`: 1-indexed; useful when spot-checking layout-heavy pages.

## Rules

1. **Never fabricate content for pages that need OCR.** If `pdf_type` is `scanned`/`image_based`, or `pages_needing_ocr` is non-empty, say exactly which pages could not be read and route them to an OCR tool (or ask the user). Exit code 2 means the whole document needs OCR.
2. For `mixed` PDFs, use the extracted Markdown for text pages and explicitly flag the OCR pages — partial output is fine as long as the gap is stated.
3. For large PDFs (100+ pages), run `--detect` first (~10–50ms), then extract only the pages you need with `--pages`.
4. If `has_encoding_issues` is true, distrust the text even when it looks plausible.

## Direct Python API (advanced)

For region- or position-level work, use the venv's Python directly
(`~/.venvs/pdf-inspector/bin/python`):

```python
import pdf_inspector
r = pdf_inspector.process_pdf("doc.pdf", pages=[1, 3])      # full result; pages= is 1-indexed
c = pdf_inspector.classify_pdf("doc.pdf")                   # lightweight; pages_needing_ocr is 0-indexed here
items = pdf_inspector.extract_text_with_positions("doc.pdf")  # TextItem: text, x, y, font, page, bold/italic
per_page = pdf_inspector.extract_pages_markdown("doc.pdf", pages=[0, 2])  # 0-indexed pages arg
regions = pdf_inspector.extract_text_in_regions("doc.pdf", [(0, [[50, 50, 400, 200]])])
```

Watch the indexing — it varies by function: `process_pdf(pages=)` is 1-indexed,
`extract_pages_markdown(pages=)` and `classify_pdf` results are 0-indexed, and
`pages_needing_ocr` / `pages_with_tables` on full results are 1-indexed. The
wrapper script handles this for you; verify empirically if using other functions.

## If the wheel install fails

PyPI ships wheels for macOS (x64/arm64), Linux (x64/aarch64), and Windows x64. On
anything else, build from source instead: `cargo install pdf-inspector` provides
equivalent `pdf2md` and `detect-pdf` binaries (pure Rust, no system libraries).
The npm package `@firecrawl/pdf-inspector` only has linux-x64/darwin-arm64/win-x64
prebuilds — prefer the Python wheel on Linux arm64 machines.

## Credits

All the heavy lifting is [pdf-inspector](https://github.com/firecrawl/pdf-inspector)
by the [Firecrawl](https://firecrawl.dev) team (MIT, © 2026 Firecrawl). This skill
just packages it for coding agents.
