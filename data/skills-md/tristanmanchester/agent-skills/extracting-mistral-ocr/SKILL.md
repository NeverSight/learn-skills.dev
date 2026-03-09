---
name: extracting-mistral-ocr
description: >-
  Extracts text, tables, and images from PDFs (including scanned PDFs) using the Mistral OCR API.
  Use when user asks to OCR a PDF/image, extract text from a PDF, parse a scanned document,
  convert a PDF to Markdown, or extract structured fields from a document.
compatibility: >-
  Requires network access and a MISTRAL_API_KEY environment variable. Expects Python 3.9+ and the mistralai package.
allowed-tools: "Read,Write,Bash(python:*)"
metadata:
  author: generated-by-chatgpt
  version: 0.1.0
  api: mistral
  default-model: mistral-ocr-latest
---

# Mistral OCR PDF extraction

## Quick start (default)

Run the bundled script to OCR a local PDF and write Markdown + JSON outputs:

```bash
python {baseDir}/scripts/mistral_ocr_extract.py --input path/to/file.pdf --out out/ocr
```

Output directory layout:

- `combined.md` (all pages concatenated)
- `pages/page-000.md` (per-page markdown)
- `raw_response.json` (full OCR response)
- `images/` (decoded embedded images, if requested)
- `tables/` (separate tables, if requested)

## Workflow

1. **Pick input mode**
   - **Local PDF** (most common): upload via Files API, then OCR via `file_id`.
   - **Public URL**: OCR directly via `document_url`.

2. **Choose output fidelity** (defaults are safe for RAG)
   - Keep `table_format=inline` unless the user explicitly wants tables split out.
   - Set `--include-image-base64` when the user needs figures/diagrams extracted.
   - Use `--extract-header/--extract-footer` if header/footer noise hurts downstream search.

3. **Run OCR**
   - Use `scripts/mistral_ocr_extract.py` to produce a deterministic on-disk artefact set.

4. **(Optional) Structured extraction from the whole document**
   - If the user wants fields (invoice totals, contract parties, etc.), provide an annotation prompt.
   - The OCR API can return a document-level `document_annotation` in addition to page markdown.

   Example:

   ```bash
   python {baseDir}/scripts/mistral_ocr_extract.py \
     --input invoice.pdf \
     --out out/invoice \
     --annotation-prompt "Extract supplier_name, invoice_number, invoice_date (ISO-8601), currency, total_amount. Return JSON." \
     --annotation-format json_object
   ```

## Decision rules

- **If the PDF is local and not publicly accessible**, upload it (the script does this automatically).
- **If the PDF URL is private or requires authentication**, do not pass it as `document_url`; upload instead.
- **If output quality is critical**, prefer `table_format=html` for downstream parsing over brittle regex.

## Common failure modes

- **Missing `MISTRAL_API_KEY`**: set it in the environment before running.
- **URL OCR fails**: the URL likely is not publicly accessible; upload the file.
- **Large files**: upload supports large files, but very large PDFs may need page selection (`--pages`) or batch processing.

## References

- API + parameters: `references/mistral_ocr_api.md`
- Output mapping rules (placeholders to extracted images/tables): `references/output_mapping.md`
- Example annotation prompts for common document types: `references/annotation_prompts.md`
