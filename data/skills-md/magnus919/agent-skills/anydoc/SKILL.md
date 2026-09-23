---
name: anydoc
description: >-
  Convert Word (.doc/.docx/.docm), PowerPoint (.ppt/.pps/.pot/.pptx/.pptm/.ppsx/.ppsm),
  Excel (.xls/.xlsx/.xlsm/.xlsb), OpenDocument (.odt/.ods/.odp), RTF, EPUB, CSV, and
  PDF documents to clean GitHub-Flavored Markdown locally with the Any Doc CLI
  (npx -y @firecrawl/anydoc@0.2.4): headings, GFM tables, slide structure, and
  footnotes in one pass. Use when a task needs the contents of an office document,
  spreadsheet, presentation, ebook, or PDF you cannot read directly. Do not use for
  generating, editing, or validating documents (use documents), for ebook packaging
  (use epub). For scanned or image-only PDFs, use hosted OCR only when the user
  explicitly authorizes whole-document upload; otherwise route to local OCR tooling.
license: MIT
compatibility: >-
  Node.js >= 20 and npx. The pinned CLI is @firecrawl/anydoc@0.2.4; the native
  binary ships via npm optionalDependencies (no install step, no postinstall, no
  compilation). Local conversion needs no service or API key. Hosted OCR sends the
  whole PDF to Firecrawl Parse and may use FIRECRAWL_API_KEY. The first npx run
  downloads the package once (network required); later runs use the npm cache.
metadata:
  skills: anydoc, markdown, conversion, docx, xlsx, pptx, pdf, odt, ods, odp, rtf, epub, csv, office, documents, firecrawl
  tags: conversion, markdown, office, documents
  source: https://github.com/firecrawl/anydoc
allowed-tools: Bash Read
---

# Any Doc — office documents to GitHub-Flavored Markdown

The `anydoc` skill converts office documents, spreadsheets, presentations,
ebooks, CSV, and text-based PDFs into GitHub-Flavored Markdown using the pinned
Any Doc CLI (`@firecrawl/anydoc` v0.2.4). One shared document model and one GFM
serializer produce the same logical output across formats. Local conversion runs
without a service, API key, or file upload; hosted OCR is a separate explicit route.

## Overview

Load this skill when a task needs the *contents* of a document the agent cannot
read directly: a Word report to summarize, a spreadsheet to turn into a table,
a slide deck to extract, a CSV to analyze, or an ebook or PDF to quote from.

The skill ships a small Python helper (`scripts/anydoc`) that wraps the pinned
CLI and adds input pre-validation, friendly error hints, batch conversion, and
`--dry-run`/`--json` output. Every recipe in [references/workflows.md](references/workflows.md)
also shows the raw `npx` invocation, so the skill works with or without the
helper.

## First-use decision gate

Before invoking anydoc, classify the request:

| If the user needs... | Do this |
| --- | --- |
| The contents of an existing supported document | Continue to [Command Map](#command-map). |
| Generation, editing, validation, EPUB packaging, HTML scraping, or password decryption | Stop and use the route in [When not to use](#when-not-to-use). |
| A format-fidelity or failure decision | Load the matching row in [Reference Routing](#reference-routing) before choosing a command. |
| A conversion result | Choose stdout, `-o`, or batch; run it; then follow [Verification](#verification). |

> **Hard boundary:** local anydoc conversion reads existing supported documents to Markdown without uploading them. Hosted OCR is opt-in only: it sends the whole OCR-required PDF to the configured Parse service. AnyDoc does not create, edit, validate, package, decrypt, or scrape documents.

## When to use

- **Convert a document to markdown** — Word, PowerPoint, Excel, OpenDocument,
  RTF, EPUB, CSV, or text-based PDF.
- **Extract structure** — headings, GFM tables, slide titles, speaker notes
  (as blockquotes), and footnotes.
- **Feed documents to an LLM** — one-pass conversion to clean markdown for
  summarization, extraction, or retrieval ingestion.
- **Batch a folder** — convert a directory of mixed office files for a vault
  or knowledge base.
- **Read a document from stdin** — pipe bytes into `anydoc -`.

## Format coverage (summary)

anydoc covers **8 format families / 21 extensions** through **12 canonical
parsers**. The canonical formats are `doc, docx, odt, pdf, ppt, pptx, rtf,
epub, xlsx, ods, odp, csv`; extension aliases map through them (`.docm`→docx,
`.xls`→xlsx, `.pptm`→pptx, and so on).

| Family | Extensions | Expected GFM output | Decision cue |
| --- | --- | --- | --- |
| Word | `.doc` `.docx` `.docm` | `#`–`######` headings, GFM tables, `[^n]` footnotes | Use when content extraction is enough; use `documents` when rendered layout matters. |
| PowerPoint | `.ppt` `.pps` `.pot` `.pptx` `.pptm` `.ppsx` `.ppsm` | slide titles as plain paragraphs, bullet lists, speaker notes as `>` blockquotes, GFM tables (PPTX/ODP; legacy `.ppt` flattens tables to text lines) | Need table fidelity? Prefer PPTX or ODP; legacy `.ppt` preserves cell text but not table structure. |
| Excel | `.xls` `.xlsx` `.xlsm` `.xlsb` | `## <sheet name>` heading + one GFM table per worksheet; number formats dropped (raw cell values) | Need displayed percentages, currency, or number formats? Prefer ODS; XLS/XLSX output is raw values. |
| OpenDocument | `.odt` `.ods` `.odp` | same document/slide shapes as DOCX/PPTX; ODS keeps formatted display values | Prefer ODS when spreadsheet display formatting is part of the meaning. |
| Rich Text Format | `.rtf` | same document shape as DOCX/ODT | Use for text extraction, not layout preservation. |
| EPUB | `.epub` | `#` chapter headings, GFM tables, internal anchor links | Use to read an existing EPUB; use `epub` to author or package one. |
| CSV | `.csv` | one GFM table; label-like first row promoted to header; delimiter sniffing; UTF-16 with BOM | Use for delimited tabular content; inspect delimiter and encoding when output looks wrong. |
| PDF | `.pdf` | headings + inline emphasis, but a lower-fidelity pipeline: tables flatten to text, footnotes and links degrade. Text-based PDFs stay local; scanned/image-only PDFs require explicit hosted OCR or another OCR tool | Use local mode by default; hosted mode uploads the whole PDF and has no page selection. |

See [references/formats.md](references/formats.md) for the full per-format
expectations and fidelity caveats, and [references/errors.md](references/errors.md)
for the exact failure messages (including the no-OCR error).

## Command Map

Commands are shown relative to the repository root. `<file>` is any document
path (for example `anydoc/fixtures/fixture-handmade-outline.docx`); `-` reads
the document from stdin.

| Need | Command | Choose it when |
| --- | --- | --- |
| Convert one file to small markdown on stdout | `anydoc/scripts/anydoc convert <file>` | The caller needs immediate content and does not need a saved artifact. |
| Convert one file to a markdown file | `anydoc/scripts/anydoc convert <file> -o out.md` | The output is large, must be reviewed later, or should be preserved as an artifact. |
| Convert many files to a directory | `anydoc/scripts/anydoc batch <file1> <file2> ... --out-dir out/` | The request is a bounded batch and per-file output/status is useful. |
| Show the tool and pinned CLI version | `anydoc/scripts/anydoc info` | You need to confirm the executable and version before troubleshooting or reporting an environment issue. |
| Raw pinned CLI, one document | `npx -y @firecrawl/anydoc@0.2.4 <file> [-o out.md]` | The wrapper is unavailable; preserve the pinned CLI and its documented semantics. |
| Raw pinned CLI, read stdin | `cat data.csv \| npx -y @firecrawl/anydoc@0.2.4 - --format csv` | Bytes already arrive on stdin and the format is known; keep the producer pipeline separate from the converter. |

For an OCR-required PDF, first use the local default so the failure is visible:

```bash
anydoc/scripts/anydoc convert scan.pdf --ocr reject
```

If the user explicitly authorizes sending the complete PDF to Firecrawl Parse,
use the wrapper acknowledgement and a trusted `FIRECRAWL_API_KEY` environment
variable when needed:

```bash
anydoc/scripts/anydoc convert scan.pdf --ocr hosted --allow-hosted-upload
```

The wrapper never places the key on the command line. Hosted OCR has no page
selection, and a hosted failure is not permission to silently switch endpoints.

Notes:

- `scripts/anydoc` is an executable Python 3 script (shebang `#!/usr/bin/env
  python3`); `python3 anydoc/scripts/anydoc ...` is equivalent when the
  executable bit is unavailable.
- The raw `npx -y @firecrawl/anydoc@0.2.4` rows are the ground truth for
  conversion behavior; the wrapper delegates to exactly that command.
- Always pin `@0.2.4` for reproducible conversions. `-y` answers npx's
  "Ok to proceed?" prompt non-interactively — the CLI itself never prompts.
- Both forms share the same contract: one document per invocation, exit code
  `0` success / `1` conversion or IO failure / `2` usage error, diagnostics as
  exactly one `anydoc: <message>` line on stderr, and no prompts.

Hosted OCR is supported by the 0.2.4 library and CLI, but the wrapper requires
both `--ocr hosted` and `--allow-hosted-upload` so an upload cannot be selected
implicitly. The hosted route sends the complete PDF to Firecrawl Parse because
page selection is unavailable. Do not place API keys on the command line.

## Reference Routing

Load only the row that answers the immediate question; the command examples and verification contract remain in this file.

| When you need to... | Load | It answers |
| --- | --- | --- |
| Choose a format or predict fidelity | [references/formats.md](references/formats.md) | Supported families, output shapes, and caveats such as raw XLSX values, ODS display values, legacy `.ppt` table flattening, and PDF degradation. |
| Select flags, stdin syntax, output behavior, or version details | [references/cli-reference.md](references/cli-reference.md) | Verbatim help, accepted options, stdin rules, stdout/stderr behavior, pinning, and runtime requirements. |
| Classify a failure or decide whether to retry | [references/errors.md](references/errors.md) | Exit codes, exact error vocabulary, no-OCR/encryption boundaries, and the next route. |
| Choose a single-file, stdin, batch, vault, or large-output recipe | [references/workflows.md](references/workflows.md) | End-to-end recipes, safe output handling, per-file failure routing, and resource-limit behavior. |
| Verify a documented upstream or fixture claim | [references/sources.md](references/sources.md) | Source URLs, access dates, fixture provenance, and the verification basis for documented claims. |
| Shape the final evidence report | [references/report-examples.md](references/report-examples.md) | Complete success, expected-failure, and fidelity-boundary reports to imitate after following Verification. |

## When not to use

Use this routing table before reaching for a conversion command:

| User's request | Reach for | Why |
| --- | --- | --- |
| Generate, edit, inspect rendered layout, or validate a PDF/Word/Excel/PowerPoint artifact | `documents` skill | anydoc extracts existing document contents to Markdown; it does not author, preserve rendered layout, or validate artifacts. |
| Package or author an EPUB | `epub` skill | anydoc reads an existing EPUB to Markdown but never writes or validates an EPUB container. |
| OCR a scanned or image-only PDF | Local OCR tooling, or AnyDoc hosted OCR after explicit authorization | Local mode reports the OCR-required error without uploading; hosted mode sends the whole PDF to Firecrawl Parse. |
| Scrape HTML or other web content | A web-scraping skill | HTML is not a supported anydoc input. |
| Transcribe binary media such as images, video, or audio | A media or transcription tool | Embedded images become alt text; anydoc cannot transcribe media. |
| Preserve pagination, fonts, templates, or rendered layout | A document/layout tool | The only output contract is GitHub-Flavored Markdown. |
| Convert a password-protected file | An unencrypted copy from the document owner | anydoc has no password or decryption option. |

## Verification

**Report evidence, not just success.** For every attempted conversion, return the input, exact command or wrapper path, observed exit code, output destination (stdout or file), structural markers checked, and any documented caveat or next route.

**Compact report shape:**
```text
Input: <path or stdin source>
Command: <exact wrapper or pinned CLI path>
Exit: <observed code>
Output: <stdout or destination file>
Checks: <markers or fidelity facts observed>
Caveat/route: <documented limitation or next action>
```

### Common stop conditions

| Condition | Do not | Next |
| --- | --- | --- |
| Scanned or image-only PDF / OCR-required error | Retry unchanged or upload implicitly | Use local OCR, or explicitly authorize and run `--ocr hosted --allow-hosted-upload`; page selection is unavailable. |
| Encrypted or password-protected document | Guess a password or retry unchanged | Request an unencrypted copy or owner-authorized re-export. |
| Unsupported, malformed, or resource-limit error | Guess a parser or claim partial success | Match the exact error in [references/errors.md](references/errors.md) and follow its bounded route. |
| Exit 0 but expected structural markers are absent | Report success from the exit code alone | Inspect the output shape and source fidelity before reporting completion. |

Confirm a conversion before reporting it as done:

1. **Check the exit code.** `0` means the CLI produced markdown. `1` means the
   document could not be read or converted — read the single `anydoc: <message>`
   stderr line and match it against [references/errors.md](references/errors.md).
   `2` means the command itself was a usage error (bad flag, missing input,
   invalid `--format`).
2. **Check the output shape.** The markdown must contain the structural markers
   your format actually produces:
   - Word / ODT / RTF / text-based PDF: `#`/`##` headings. For PDF, do not
     expect GFM tables or `[^1]:` footnote definitions — that pipeline
     flattens them.
   - Spreadsheets (xlsx/xls/ods) and CSV: `|`-delimited GFM tables. xlsx/xls
     show raw cell values (`0.155`, `1234.5`); ODS shows formatted display
     values (`15.5%`, `$1,234.50`).
   - Presentations (pptx/odp): slide titles as plain paragraphs, `>`
     blockquote speaker notes, GFM tables. Legacy `.ppt` flattens tables to
     bare text lines.
   - EPUB: `#` chapter headings and internal anchor links.
3. **Write large outputs to a file with `-o`.** `-o out.md` keeps stdout silent
   and gives a reviewable file instead of streaming the whole document into
   context.
4. **Verify tables survived.** If the source had tables and the output has no
   `|` rows, consult the format caveats — PDF and legacy `.ppt` flatten tables
   by design, not by error.

**Stop when** the conversion exits 0 and the structural markers match the
source format. Do not re-run or retry on a documented failure mode (encrypted,
malformed, scanned/image-only, unsupported) without changing the input; report
the documented message and route as [references/errors.md](references/errors.md)
instructs.
