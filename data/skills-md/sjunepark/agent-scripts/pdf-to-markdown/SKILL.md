---
name: pdf-to-markdown
description: "Convert PDF inputs into clean, reusable whole-document Markdown for agents, LLM ingestion, search, or archival text, using Xberg with safe output handling, Korean scan OCR, page markers, validation, and layout escalation. Use when the user asks to create, save, generate, normalize, reconvert, or extract a Markdown or whole-document agent-readable text artifact from a PDF. Do not use for summaries or questions with no converted artifact, PDF editing or rendering, parser research, or targeted extraction into CSV, JSON, images, or other structured formats."
---

# PDF to Markdown

Create a validated Markdown sibling while preserving the PDF as the visual
authority. Default to `report.pdf` plus `report.md`; do not retain parser JSON,
coordinates, extracted assets, or chunks unless the user names a consumer for
them.

## Convert safely

1. Resolve each source PDF and intended output path. Process multiple PDFs one
   at a time so each result can be validated independently.
2. If the intended output exists, use `--overwrite` only when the user has
   explicitly authorized replacing that exact file. If that authority is
   missing, stop before conversion. Do not invent an alternate destination;
   use another path only when the user selects or approves it.
3. Check for the `xberg` executable. If it is missing, identify the current
   official installation method for the host platform and use applicable user
   approval, requesting it only when absent. Do not run an install script,
   package manager, or model download prewarming beyond that approval.
4. Resolve `scripts/convert_pdf.py` relative to this `SKILL.md` and run:

   ```bash
   python3 scripts/convert_pdf.py /absolute/path/report.pdf
   ```

   The wrapper writes `report.md` atomically, preserves the PDF, rejects empty
   or structurally inconsistent output, and never invokes a shell. It asks
   Xberg for JSON so it can validate every physical page, but publishes only
   Xberg's whole-document Markdown and retains no parser JSON.

   The wrapper's ordinary Xberg extraction uses these core flags:

   ```bash
   xberg extract /absolute/path/report.pdf \
     --no-config-discovery \
     --format json \
     --content-format markdown \
     --extract-pages true \
     --page-markers true
   ```

   When page markers are enabled, the wrapper also supplies a randomized
   private marker through `--config-json`; it later converts only those private
   markers to `<!-- PAGE n -->`. A direct fallback must use an equivalently
   collision-resistant private marker rather than public page comments during
   validation.

   The wrapper validates that Xberg's page records form a contiguous 1-based
   sequence and agree with its declared page count. If Xberg omits markers for
   pages it classifies as blank, the wrapper restores those markers from page
   metadata while preserving Xberg's Markdown body unchanged.
   It refuses publication when marker and page metadata cannot be reconciled.
   Do not rebuild the document by concatenating per-page Markdown because that
   can reset lists and damage structures spanning page boundaries. Do not
   replace the wrapper with a direct shell redirect when creating the final
   artifact.
5. For a PDF that contains scanned Korean pages, add `--korean-ocr`. This uses
   PaddleOCR with explicit Korean selection and OCRs only pages classified as
   scans while retaining native text elsewhere:

   ```bash
   python3 scripts/convert_pdf.py /absolute/path/report.pdf --korean-ocr
   ```

   The corresponding Xberg flags are:

   ```bash
   xberg extract /absolute/path/report.pdf \
     --no-config-discovery \
     --format json \
     --content-format markdown \
     --extract-pages true \
     --page-markers true \
     --ocr true \
     --ocr-backend paddle-ocr \
     --ocr-language korean \
     --ocr-scanned-pages
   ```

   The first PaddleOCR use may download models as part of the requested
   conversion. Tell the user before starting when network use or model storage
   is material in the current environment.

Do not OCR a born-digital PDF merely because its language is Korean. Use
`--force-ocr` only when the entire document is image-only or its text layer is
demonstrably broken; combine it with `--korean-ocr` for Korean documents.

If Python is unavailable but Xberg is present, reproduce the wrapper's exact
flags with a command runner while preserving the same non-overwrite, temporary
output, nonempty-result, and atomic-finalization guarantees. If those guarantees
cannot be preserved, stop and report the missing capability.

## Validate and escalate

After every conversion:

1. Inspect the beginning, middle, and end of the Markdown. Check headings,
   paragraph order, tables, lists, code, Hangul where expected, numbers, dates,
   missing pages, suspicious repetition, mojibake, and abrupt density changes.
2. Read the wrapper's validation summary. It reports physical, nonblank, and
   blank page counts and, when nonzero, how many blank-page markers it restored.
   Compare that total with an independent PDF page count when a PDF inspection
   capability is available. A blank page can legitimately contain no text, but
   it must still have a marker in the final Markdown unless `--no-page-markers`
   was requested.
   Repeated `pdf_oxide` dictionary-as-stream warnings are summarized rather than
   dumped; they mean malformed or unusual PDF objects were treated as empty
   streams, so inspect nearby visual content when fidelity is uncertain. The
   wrapper also reports Xberg's structured processing warnings with bounded
   output; treat them as page or pipeline-specific fidelity risks to inspect.
3. If ordinary extraction loses reading order, headings, tables, lists, or
   figure placement, rerun to a temporary comparison file with `--layout`:

   ```bash
   python3 scripts/convert_pdf.py /absolute/path/report.pdf \
     --output /absolute/path/report.layout.md \
     --layout
   ```

   This adds `--layout --layout-strategy auto
   --use-layout-for-markdown` to the ordinary Xberg command.

   Compare content fidelity, then replace the intended output only with the
   user's overwrite authority. Do not assume that the larger output is better.
   If layout extraction reports an ONNX Runtime API mismatch, treat that as the
   cause even if a later worker message says `Mutex poisoned`. On Windows, check
   whether an older `C:\Windows\System32\onnxruntime.dll` was loaded. Point
   `ORT_DYLIB_PATH` at a compatible runtime only with user authority; do not
   silently install or replace a system library. The wrapper publishes no
   partial layout output after this failure.
4. If Korean OCR still omits or corrupts content, retry with `--force-ocr` only
   when the native text layer is the cause. For complex visual pages that remain
   unreliable, report the failing pages and offer a Docling or document-VLM
   comparison rather than silently switching tools or installing another
   parser.

## Finish

Finish only when the Markdown exists, is nonempty, passed representative source
checks, and the source PDF remains unchanged. Report the PDF and Markdown paths,
Xberg version, OCR or layout options used, physical/nonblank/blank page counts,
restored marker count, summarized parser warnings, any overwritten file
explicitly authorized by the user, and any pages or structures that remain
uncertain.
