---
name: doc-to-markdown
description: Use when converting Word documents (.doc/.docx) to clean Markdown with images extracted to a separate folder for readability and AI compatibility
---

# Doc-to-Markdown (Word → Markdown)

Convert Microsoft Word `.doc` / `.docx` into:
- a clean Markdown file (`.md`)
- plus an optional images folder (`*_images/`) with relative image links

This is designed to keep Markdown small (good for humans + LLMs) while preserving diagrams.

## Quickstart (copy/paste)

```bash
# 1) Convert a single file (.docx or .doc)
python3 convert_word_to_markdown.py "path/to/document.docx"

# 2) Embedded mode (single self-contained .md, very large)
python3 convert_word_to_markdown.py --embedded "path/to/document.docx"

# 3) If anything fails, run a dependency check
python3 convert_word_to_markdown.py --check
```

### Batch convert (current folder)

```bash
for f in *.doc *.docx; do
  [ -e "$f" ] || continue
  python3 convert_word_to_markdown.py "$f"
done
```

## Outputs

Default (external images):
```
document.docx
document.md
document_images/
  image1.png
  image2.png
  ...
```

Embedded mode:
```
document.docx
document.md   # contains base64 images
```

## Requirements

- **Recommended (most reliable):** install `markitdown` into a local virtualenv in this repo
  - `bash setup_venv.sh`
  - (manual) `python3.11 -m venv .venv` + `.venv/bin/python -m pip install 'markitdown[all]'`
- **Alternative:** install `markitdown` globally
  - `python3 -m pip install 'markitdown[all]'` (requires Python 3.10+ and `markitdown` on `PATH`)
- **Fallback:** `uv` (provides `uvx`) so the scripts can run `markitdown` without pip installs
  - macOS: `brew install uv`
- **For `.doc` (legacy) support:** LibreOffice (`brew install --cask libreoffice`)

## Environment Overrides (for reliability)

- `MARKITDOWN_UVX_PYTHON=3.11` (default) — change the Python version used by `uvx`
- `MARKITDOWN_UVX_OFFLINE=0` — allow `uvx` to use network (default: offline)
- `MARKITDOWN_CMD="... markitdown"` — full command override (advanced)
- `UV_CACHE_DIR=/tmp/uv-cache` — use this if `uvx` can’t write to its cache directory (default: `./.uv-cache/`)

## Common Failure Modes

- **`.doc` conversion fails**:
  - LibreOffice GUI running → quit LibreOffice (or `killall soffice`) and retry
  - If you see `Abort trap: 6` / exit 134 in a sandboxed tool runner → pre-convert `.doc` to `.docx` outside the sandbox, then convert the `.docx`
- **WMF/EMF diagrams don’t display**: in sandboxed environments the WMF/EMF → PNG step may be skipped; convert those images to PNG outside the sandbox if needed
- **`markitdown not found`**: create `./.venv/` (recommended) or install `markitdown` globally
- **`Failed to initialize cache at ~/.cache/uv`**: set `UV_CACHE_DIR=/tmp/uv-cache` and retry

## Notes

- `convert_word_to_markdown.py` is the entrypoint (handles both `.doc` and `.docx`).
- `convert_with_images.py` is an internal helper and only supports `.docx`.
