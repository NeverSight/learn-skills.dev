---
name: sdlc-convert-doc
description: Convert local documents into Markdown by routing text-bearing files through Microsoft MarkItDown and OCR-heavy inputs through Datalab Marker. Use when asked to convert PDFs, scanned PDFs, images, Word, PowerPoint, Excel, HTML, EPUB, email, archives, or other document files to Markdown, especially when OCR, tables, equations, layout preservation, or extraction-quality fallback is needed.
---

# SDLC Doc to Markdown

Convert local files with the bundled router. Prefer MarkItDown for lightweight
structured extraction and Marker when OCR or document-layout recovery is needed.

## Workflow

Resolve `SKILL_DIR` to the directory containing this `SKILL.md`; do not assume the
current working directory is the skill directory.

1. Confirm the input is a local file and choose a separate `.md` output path.
2. Run the dependency preflight:

   ```bash
   python3 "$SKILL_DIR/scripts/check_dependencies.py" --engine auto
   ```

3. Preview the routing decision when the file type or OCR need is uncertain:

   ```bash
   python3 "$SKILL_DIR/scripts/convert_to_markdown.py" INPUT \
     --output OUTPUT.md --dry-run
   ```

4. Convert with automatic routing:

   ```bash
   python3 "$SKILL_DIR/scripts/convert_to_markdown.py" INPUT --output OUTPUT.md
   ```

5. Read the generated Markdown. Check headings, reading order, tables, equations,
   image links, missing text, and OCR corruption before reporting success.
6. If a digital PDF produces sparse text, let the script retry it with Marker and
   forced OCR. If quality is still poor, rerun explicitly:

   ```bash
   python3 "$SKILL_DIR/scripts/convert_to_markdown.py" INPUT.pdf --output OUTPUT.md \
     --engine marker --force-ocr --overwrite
   ```

Never overwrite an existing output unless the user approved replacement. The script
enforces this unless `--overwrite` is passed.

## Engine selection

| Input or condition | Engine | Reason |
|---|---|---|
| DOCX, PPTX, XLSX/XLS, HTML, EPUB, email, CSV, JSON, XML, ZIP, and ordinary text-bearing files | MarkItDown | Fast, lightweight structured extraction |
| PNG, JPEG, TIFF, BMP, GIF, or WebP | Marker | Image inputs require OCR and layout recovery |
| PDF with usable embedded text | MarkItDown first | Avoid unnecessary model loading |
| Scanned, image-only, sparse, or garbled PDF | Marker with OCR | Recover text and reading order |
| Layout-heavy PDF, equations, or complex tables | Marker | Stronger layout and math handling |

Use `--engine markitdown` or `--engine marker` only to override this policy. Use
`--page-range`, `--force-ocr`, `--strip-existing-ocr`, `--use-llm`, or
`--disable-image-extraction` for Marker-specific work. Marker-specific options make
automatic routing choose Marker directly.

## Output rules

- Keep the source file unchanged.
- Preserve Marker-generated images beside the Markdown so relative links remain valid.
- Treat conversion as extraction, not proof of correctness. Compare critical values,
  names, dates, tables, and formulas against the source.
- Do not enable `--use-llm` without confirming the configured service and whether the
  document may be sent to it.
- Do not process an untrusted path or URL. The router accepts local files only.

## Dependencies and troubleshooting

Require `markitdown[all]==0.1.6` and `marker-pdf==1.10.2`; treat a missing or
mismatched version as a failed preflight. Do not upgrade these pins implicitly.

Read [references/converters.md](references/converters.md) when installing converters,
choosing optional packages, reviewing supported formats, handling model downloads, or
evaluating Marker licensing and compute requirements.

Run `python3 "$SKILL_DIR/scripts/convert_to_markdown.py" --help` for all conversion
options.
