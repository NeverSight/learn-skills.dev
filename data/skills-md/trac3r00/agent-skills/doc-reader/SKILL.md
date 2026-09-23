---
name: doc-reader
description: Extracts plain text from office and web documents with zero dependencies — docx, pptx, xlsx, html, markdown, and plain text, using only Python's stdlib (zipfile + xml.etree). No LibreOffice, no python-docx, no network. PDF delegates to pdftotext when installed, reporting honestly when it is not. Use when an agent needs to read, summarize, or compare documents without installing document tooling.
when_to_use: Any task that involves reading documents an agent or user dropped into a session — a contract, a slide deck, a spreadsheet, a saved webpage. NOT a document editor or a format converter; it reads text out, it does not write documents back.
version: 1.0.0
license: MIT
metadata:
  agentskills:
    tags: [documents, docx, pptx, xlsx, html, extraction]
---

# Doc Reader

Office files are ZIPs of XML. This reads them with the stdlib, so an agent
can work with documents on any machine with zero installs.

## Commands

```bash
python3 scripts/doc_reader.py report.docx
python3 scripts/doc_reader.py slides.pptx --json
python3 scripts/doc_reader.py data.xlsx | head -50
python3 scripts/doc_reader.py page.html notes.md book.pdf
```

## Supported formats

| Format | How | Notes |
|---|---|---|
| `.docx` | ZIP + word/document.xml paragraphs | headings preserved as paragraphs |
| `.pptx` | ZIP + ppt/slides/slideN.xml | per-slide text, slide count |
| `.xlsx` | ZIP + shared strings + sheet rows | tab-separated rows |
| `.html`/`.htm` | html.parser, scripts/styles stripped | clean readable text |
| `.md`/`.txt` | raw text | passthrough |
| `.pdf` | delegates to `pdftotext` | honest error if not installed |

## Exit codes

0 = all files read, 1 = some failed, 2 = all failed or unsupported format.
Corrupt files (bad ZIP, malformed XML) are reported as corrupt, not silently
skipped.

## Pairs with

`resume-audit` (convert a PDF resume with doc-reader first, then audit),
`seo-audit` (read the HTML doc-reader extracts, then score it).
