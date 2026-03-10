---
name: ocr
description: OCR skill for extracting text from images and PDFs. Use when you need to read text from screenshots, photos, scanned documents, or any image file. Supports Chinese, English, and 100+ languages.
---

# OCR Skill

## Usage

To extract text from an image or PDF, run:

```bash
python3 "/Users/mrshaper/Library/Application Support/com.differentai.openwork/workspaces/starter/.opencode/skills/paddle-ocr/scripts/ocr.py" "/path/to/image.png"
```

## Options

| Option | Description |
|--------|-------------|
| `--prompt "text"` | Custom prompt (e.g., "Extract table as markdown") |
| `--fast` | Use faster PaddleOCR instead of DeepSeek-OCR |
| `--json` | Output as JSON format |

## Examples

```bash
# Basic OCR
python3 scripts/ocr.py image.png

# Extract table as markdown
python3 scripts/ocr.py table.png --prompt "Extract this table as markdown"

# Fast mode
python3 scripts/ocr.py image.png --fast

# PDF OCR
python3 scripts/ocr.py document.pdf
```

## Supported Formats

Images: PNG, JPG, JPEG, BMP, GIF, WEBP, TIFF
Documents: PDF
