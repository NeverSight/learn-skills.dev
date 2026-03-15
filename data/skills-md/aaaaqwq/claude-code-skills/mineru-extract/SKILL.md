---
name: mineru-extract
description: Use the official MinerU (mineru.net) parsing API to convert a URL (HTML pages like WeChat articles, or direct PDF/Office/image links) into clean Markdown + structured outputs. Use when web_fetch/browser can’t access or extracts messy content, and you want higher-fidelity parsing (layout/table/formula/OCR).
---

# MinerU Extract (official API)

Use MinerU as an upstream “content normalizer”: submit a URL to MinerU, poll for completion, download the result zip, and extract the main Markdown.

## Quick start (MCP-aligned)

We align to the **MinerU MCP** mental model, but we do **not** run an MCP server.

- Primary script (MCP-style): `scripts/mineru_parse_documents.py`
  - Input: `--file-sources` (comma/newline-separated)
  - Output: **JSON contract** on stdout: `{ ok, items, errors }`
- Low-level script (single URL): `scripts/mineru_extract.py`

Auth:
- Set `MINERU_TOKEN` (Bearer token from mineru.net)

Default model heuristic:
- URLs ending with `.pdf/.doc/.ppt/.png/.jpg` → `pipeline`
- Otherwise → `MinerU-HTML` (best for HTML pages like WeChat articles)

### 1) Configure token (skill-local)

Put secrets in **skill root** `.env` (do not paste into chat outputs):

```bash
# In the mineru-extract skill directory: .env
MINERU_TOKEN=your_token_here
MINERU_API_BASE=https://mineru.net
```

### 2) Parse URL(s) → Markdown (recommended)

MCP-style wrapper (returns JSON, optionally includes markdown text):

```bash
python3 mineru-extract/scripts/mineru_parse_documents.py \
  --file-sources "<URL1>\n<URL2>" \
  --language ch \
  --enable-ocr \
  --model-version MinerU-HTML
```

If you want the markdown content inline in the JSON (can be large):

```bash
python3 mineru-extract/scripts/mineru_parse_documents.py \
  --file-sources "<URL>" \
  --model-version MinerU-HTML \
  --emit-markdown --max-chars 20000
```

Low-level (single URL, print markdown to stdout):

```bash
python3 mineru-extract/scripts/mineru_extract.py "<URL>" --model MinerU-HTML --print > /tmp/out.md
```

## Output

The script always downloads + extracts the MinerU result zip to:

`~/.openclaw/workspace/mineru/<task_id>/`

It writes:
- `result.zip`
- extracted files (Markdown + JSON + assets)

It prints a JSON summary to **stderr** with paths:
- `task_id`, `full_zip_url`, `out_dir`, `markdown_path`

## Parameters (common)

- `--model`: `pipeline | vlm | MinerU-HTML`  (HTML requires `MinerU-HTML`)
- `--ocr/--no-ocr`: enable OCR (effective for `pipeline`/`vlm`)
- `--table/--no-table`: table recognition
- `--formula/--no-formula`: formula recognition
- `--language ch|en|...`
- `--page-ranges "2,4-6"` (non-HTML)
- `--timeout 600` / `--poll-interval 2`

## Failure modes & fallbacks

- MinerU may fail to fetch some URLs (anti-bot / geo / login).
  - Fallback: provide an HTML file or a PDF/long screenshot; then implement “upload + parse” flow with MinerU batch upload endpoints.
  - Always report the failing URL + MinerU `err_msg` and keep an original-source link in outputs.

## References

- MinerU API docs: https://mineru.net/apiManage/docs
- MinerU output files: https://opendatalab.github.io/MinerU/reference/output_files/
