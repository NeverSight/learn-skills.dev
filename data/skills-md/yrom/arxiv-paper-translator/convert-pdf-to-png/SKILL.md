---
name: convert-pdf-to-png
description: Use when needing to convert PDF pages to PNG images for preview, comparison, or image processing.
---

# Convert PDF to PNG

Convert PDF file pages to PNG images.

## Backend Selection

Try system tools first (better rendering for complex PDFs), fall back to the JS script.

Backends you can try:

1. magick (ImageMagick) - Linux/MacOS
2. mutool (MuPDF) - Linux/MacOS
3. pdftoppm (Poppler) - Linux/MacOS
4. sips (Scriptable Image Processing System) - MacOS Only
5. JS fallback (pdfjs) - under `<CURRENT_SKILL_DIR>/scripts/` directory.

**NOTICE**: All backends should output `<pdf-name>_page_<N>.png` in the target directory.

## System Backend Examples

```bash
# magick (ImageMagick) — density 144 ≈ scale 2x (72 * 2)
magick -density 144 paper.pdf -quality 90 paper_page_%d.png
# Note: magick outputs 0-based index; rename if 1-based is needed

# mutool (MuPDF) — resolution 144 ≈ scale 2x
mutool convert -o paper_page_%d.png -O resolution=144 paper.pdf

# pdftoppm (Poppler) — -r sets DPI
pdftoppm -png -r 144 paper.pdf paper_page
# Outputs paper_page-1.png, paper_page-2.png, etc.

# sips (macOS only) — convert a single-page PDF
sips -s format png paper.pdf --out paper_page_1.png
```

> Different backends produce slightly different filename patterns (0-based vs 1-based, padding, separator).
> Rename after conversion if the downstream consumer requires strict `<pdf-name>_page_<N>.png` format.

## JS Script Prerequisites

Dependencies are in `<CURRENT_SKILL_DIR>/scripts/package.json`. Install on first use:

```bash
cd skills/convert-pdf-to-png/scripts && bun install 
# or npm install
```

## JS Script Quick Start

```bash
SCRIPT_DIR=skills/convert-pdf-to-png/scripts

# Convert all pages (default scale: 2.0x)
bun $SCRIPT_DIR/convert-pdf-to-png.mjs paper.pdf

# Specify output directory
bun $SCRIPT_DIR/convert-pdf-to-png.mjs paper.pdf --output-dir ./output

# Convert specific pages with higher resolution
bun $SCRIPT_DIR/convert-pdf-to-png.mjs paper.pdf --pages 1,3,5 --scale 3

# Encrypted PDF
bun $SCRIPT_DIR/convert-pdf-to-png.mjs protected.pdf --password "secret"
```

## JS Script CLI Options

| Option | Default | Description |
|--------|---------|-------------|
| `--output-dir <dir>` | Same as PDF | Output directory for PNG files |
| `--scale <number>` | `2.0` | Viewport scale factor (higher = better quality, larger files) |
| `--pages <list>` | all | Comma-separated 1-based page numbers |
| `--password <string>` | - | Password for encrypted PDF |

## Output

Filenames follow the pattern: `<pdf-name>_page_<N>.png`

## Common Issues

| Issue | Solution |
|-------|----------|
| Complex figures render as blank (pdfjs) | Use `magick` (ImageMagick) or `mutool` (MuPDF) instead |
| `Cannot find module 'pdf-to-png-converter'` | `cd skills/convert-pdf-to-png/scripts && bun install` |
| Poor text quality | Increase `--scale` / DPI (try 3.0 / 216) |
| Large PDF causes OOM | Convert specific pages with `--pages` instead of all |
| Encrypted PDF fails | Provide `--password` (JS) or `-p` (mutool) / `-upw` (pdftoppm) |
