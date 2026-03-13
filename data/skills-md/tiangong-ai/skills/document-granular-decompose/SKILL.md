---
name: document-granular-decompose
description: Upload local documents to TianGong AI Unstructure `/mineru_with_images` API for fine-grained parsing and return only plain fulltext content. Use when a task needs document fulltext extraction with `return_txt=true`, strict file-type allowlist validation, and API base URL/provider/model/auth token from environment variables.
---

# Document Granular Decompose

## Core Goal
- Parse a local document through `POST /mineru_with_images`.
- Always force `return_txt=true`.
- Read environment variables for endpoint, request identity, and model routing:
  - `UNSTRUCTURED_API_BASE_URL` (example: `https://your-unstructured-host:7770`)
  - `UNSTRUCTURED_AUTH_TOKEN`
  - `UNSTRUCTURED_PROVIDER`
  - `UNSTRUCTURED_MODEL`
- Return only plain fulltext (prefer API `txt`; fallback to joined `result[].text`).

## Triggering Conditions
- Need robust document fulltext extraction for PDF/Office/Markdown/image files.
- Need image-aware MinerU parsing but only textual output for downstream chunking/search/summarization.
- Need to standardize provider/model/token input via environment variables instead of ad-hoc command parameters.

## Workflow
1. Prepare environment variables.

```bash
export UNSTRUCTURED_AUTH_TOKEN="your-fastapi-bearer-token"
export UNSTRUCTURED_PROVIDER="vllm"
export UNSTRUCTURED_MODEL="Qwen/Qwen3.5-122B-A10B-FP8"
export UNSTRUCTURED_API_BASE_URL="https://your-unstructured-host:7770"
```

2. Run extraction and print fulltext to stdout.

```bash
python3 scripts/mineru_fulltext_extract.py \
  --file "/absolute/path/to/document.pdf"
```

3. Save fulltext to a local file when needed.

```bash
python3 scripts/mineru_fulltext_extract.py \
  --file "/absolute/path/to/document.pdf" \
  --output "/absolute/path/to/fulltext.txt"
```

## Request Contract
- Endpoint resolution:
  - `--api-url` if provided
  - else `UNSTRUCTURED_API_BASE_URL + /mineru_with_images`
  - else fail fast with missing environment variable error
- Method: `POST` multipart form.
- Query params:
  - Force `return_txt=true` (always set by script).
- Form fields sent:
  - `file` (required)
  - `provider` (from `UNSTRUCTURED_PROVIDER`)
  - `model` (from `UNSTRUCTURED_MODEL`)
- Header sent:
  - `Authorization: Bearer $UNSTRUCTURED_AUTH_TOKEN`

## Supported File Types (Strict)
- Supported file types:
  - `.bmp, .doc, .docm, .docx, .dot, .dotx, .gif, .jp2, .jpeg, .jpg, .markdown, .md, .odp, .odt, .pdf, .png, .pot, .potx, .pps, .ppsx, .ppt, .pptm, .pptx, .tiff, .webp, .xls, .xlsm, .xlsx, .xlt, .xltx`
- Office formats:
  - `.doc, .docm, .docx, .dot, .dotx, .odp, .odt, .pot, .potx, .pps, .ppsx, .ppt, .pptm, .pptx, .xls, .xlsm, .xlsx, .xlt, .xltx`
- Any other extension is rejected before sending API requests.

## Output Rules
- Success output must be plain text fulltext only.
- Fulltext source priority:
  1. `response.txt`
  2. join non-empty `response.result[].text` by blank lines
- Do not output chunk metadata/json unless the user explicitly requests debugging.

## Error Handling
- Missing env vars: fail fast with actionable message.
- HTTP 401/403: report token/auth issue.
- HTTP 4xx/5xx: print status and API error body if available.
- Missing text in response: fail with explicit schema mismatch error.

## References
- `references/env.md`
- `references/request-response.md`

## Assets
- `assets/config.example.env`

## Scripts
- `scripts/mineru_fulltext_extract.py`
