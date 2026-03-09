---
name: local-ocr
description: Local OCR pipeline for AI agents featuring auto-rotation, deskew, and searchable PDF generation via ocrmypdf and Tesseract.
---

# Local OCR Pipeline Skill

Robust Optical Character Recognition (OCR) pipeline driven by `ocrmypdf` and `tesseract`.
Handles scanned PDFs, rotated image inputs, and raw text extraction securely and locally without external APIs.

> **Why not GPU via PyTorch/EasyOCR?** The `ocrmypdf` tool is the industry standard for producing searchable PDFs. It leverages `tesseract` for pixel-accurate text placement. A pure-CPU pipeline is leaner (avoids a 1.5GB PyTorch payload) and reliably embeds text exactly where it appears in the scanned image. 

## Capabilities

1. **Searchable PDF Generation**: Converts rasterized/scanned PDFs or raw images (`.jpg`, `.png`, etc.) into PDFs with a selectable, searchable text layer.
2. **Auto-Rotation & Deskew**: Automatically detects incorrectly rotated text and straightens crooked scans.
3. **Idempotent In-Place Processing**: Safely processes files in-place using `--skip-text`, preventing double-processing of a PDF that already has embedded text.
4. **Structured JSON Output**: All commands output structured JSON, making failure states (like missing dependencies) parseable by agents.
5. **Raw Text Extraction**: Raw string extraction fallback for when agents need text directly in-memory instead of a PDF file.

## Setup

```bash
# Installs system dependencies (tesseract, ocrmypdf, ghostscript) and sets up isolated venv
bash skills/ocr/scripts/setup.sh
```

## Usage

```bash
uv run --project ~/.local-ocr scripts/ocr.py <command>
```

### 1. Generate a Searchable PDF (`pdf`)

Produces a standard, layered PDF. If you give it an image, it wraps it in a PDF. If you give it a scanned PDF, it adds the invisible text layer.

```bash
# Overwrites the file in-place, skipping it safely if it already contains text
uv run --project ~/.local-ocr scripts/ocr.py pdf ./scanned_invoice.pdf

# Output to a different file
uv run --project ~/.local-ocr scripts/ocr.py pdf ./scan_001.png -o ./contract.pdf

# Force reprocessing (ignore existing text layer)
uv run --project ~/.local-ocr scripts/ocr.py pdf ./scanned_invoice.pdf --force
```

**Note**: By default, `auto-rotate` and `deskew` are enabled. Disable with `--no-rotate` or `--no-deskew`.

### 2. Batch Process a Directory (`batch`)

Recursively scans a directory for images and PDFs, applying OCR.

```bash
# Process all files. Skips already-OCRed PDFs.
uv run --project ~/.local-ocr scripts/ocr.py batch ./archives/
```

### 3. Extract Raw Text (`text`)

Does not create a PDF. Just reads the words off the page and returns them as a JSON string. Good for agents reading documents on the fly.

```bash
uv run --project ~/.local-ocr scripts/ocr.py text ./han_solo_invoice.png
```

## Franchise Examples (Star Wars)

- Process the Death Star blueprints: `uv run --project ~/.local-ocr scripts/ocr.py pdf ./ds-1_schematics.pdf`
- Extract raw orders: `uv run --project ~/.local-ocr scripts/ocr.py text ./order_66_memo.jpg`
- Archive run: `uv run --project ~/.local-ocr scripts/ocr.py batch /archives/jedi_temple`

## Troubleshooting

- **File already contains text**: This is the most common "error", but it isn't an error. `ocrmypdf` returns exit code 6 when it skips a file that already has text. The wrapper script catches this and reports a JSON `"status": "success"` with a message noting the side-step.
- **Dependencies Missing**: Run the `setup.sh` script again if the agent complains about missing `tesseract` or Python modules.
