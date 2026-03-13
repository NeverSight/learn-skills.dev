---
name: x-convert-pdf-to-markdown
description: Convert PDFs to markdown using the agent-instructions Poetry environment via PyMuPDF (fast) or marker-pdf (heavy-duty OCR/tables).
---

Two tools are available depending on your needs:

| Tool | Best For | Speed | Size |
|------|----------|-------|------|
| **pymupdf** | Simple text PDFs | Very fast (~12s for 7 files) | ~15MB |
| **marker-pdf** | Complex PDFs with tables, images, OCR | Slow | ~2GB models |

## Setup

Both tools are installed in the `agent-instructions` poetry environment:

```bash
cd ~/brain/git/personal/agent-instructions
poetry install  # if not already done
```

---

## PyMuPDF (Recommended for text-only PDFs)

Fast and lightweight. Use this for most PDFs.

### Single File

```bash
cd ~/brain/git/personal/agent-instructions
poetry run pymupdf gettext -mode layout -output "/path/to/output.md" "/path/to/file.pdf"
```

### Batch Conversion

```bash
cd ~/brain/git/personal/agent-instructions
for pdf in /path/to/pdfs/*.pdf; do
  name=$(basename "$pdf" .pdf)
  poetry run pymupdf gettext -mode layout -output "/path/to/output/${name}.md" "$pdf"
done
```

### Options

| Option | Description |
|--------|-------------|
| `-mode` | `simple`, `blocks`, or `layout` (default: layout preserves formatting) |
| `-output` | Output file path |
| `-pages` | Page range to extract |

---

## marker-pdf (For complex PDFs)

Use when you need OCR, table extraction, or image handling.

### Single File

```bash
cd ~/brain/git/personal/agent-instructions
poetry run marker_single "/path/to/file.pdf" --output_dir "/path/to/output"
```

### Options

| Option | Description |
|--------|-------------|
| `--output_dir` | Directory to save output |
| `--output_format` | `markdown`, `json`, `html`, or `chunks` |
| `--page_range` | Process specific pages, e.g., `"0,5-10,20"` |
| `--force_ocr` | Force OCR on all text |

### First Run

On first use, marker downloads ML models (~2GB). This happens once.

---

## Notes

- **Fully local**: Both tools process entirely on your machine, no cloud
- **PyMuPDF**: Best for clean, text-based PDFs
- **marker-pdf**: Best for scanned docs, tables, or complex layouts

