---
name: md-to-pdf
description: Converts markdown files into professionally styled PDF documents. Use this
  skill whenever the user asks to generate a PDF, export markdown as PDF,
  convert .md to .pdf, or create a printable version of a document. Also
  triggers when the user wants status-colored tables, styled documentation
  export, or says things like "make this a PDF", "I need a PDF version",
  "export this doc". Supports auto orientation, optional keyword-based cell
  coloring, and graceful engine fallback.
---

# Markdown to PDF

Convert any markdown file into a clean, professionally styled PDF. Handles tables, code blocks, blockquotes, and deep heading hierarchies out of the box. Optionally color-codes table cells based on status keywords.

## When to Apply

Reference these guidelines when:
- The user asks to convert a markdown file to PDF
- The user wants a printable or shareable version of a document
- The user asks to "export", "generate PDF", or "make a PDF"
- The user wants styled tables with color-coded status cells
- The user needs landscape orientation for wide tables

## How It Works

This skill bundles a Python script (`scripts/md_to_pdf.py`) that handles the full conversion pipeline:

```
Markdown → HTML (via markdown2) → Styled HTML → PDF (via weasyprint or xhtml2pdf)
```

**Always run the bundled script** rather than writing conversion code inline. This ensures consistent styling and avoids reinventing the wheel each time.

## Quick Start

Basic conversion — the script auto-detects the best orientation:

```bash
python3 <skill-path>/scripts/md_to_pdf.py input.md output.pdf
```

With status cell coloring (colors the table cells, not the text):

```bash
python3 <skill-path>/scripts/md_to_pdf.py input.md output.pdf --status-colors
```

Force landscape or portrait:

```bash
python3 <skill-path>/scripts/md_to_pdf.py input.md output.pdf --landscape
python3 <skill-path>/scripts/md_to_pdf.py input.md output.pdf --portrait
```

Custom status keywords and colors:

```bash
python3 <skill-path>/scripts/md_to_pdf.py input.md output.pdf --status-colors \
  --custom-colors '{"APPROVED": "#d4edda:#155724", "REJECTED": "#f8d7da:#721c24"}'
```

## Features

### Auto Orientation

The script scans for tables in the markdown. If any table has 4 or more columns, it defaults to landscape. Otherwise, portrait. The user can always override with `--landscape` or `--portrait`.

### Status Cell Coloring

When `--status-colors` is passed, the script identifies table cells in the **Status column** that contain bold keywords and applies background colors to the entire cell. This is column-aware — it only targets cells in columns named "Status", not every bold word in the document.

Built-in keyword → color mappings:

| Keyword | Background | Text Color | Use Case |
|---|---|---|---|
| EXISTS | `#d4edda` (green) | `#155724` | Available, implemented |
| MISSING | `#f8d7da` (red) | `#721c24` | Not available, needed |
| PARTIAL | `#fff3cd` (yellow) | `#856404` | Partially available |
| TODO | `#fff3cd` (yellow) | `#856404` | Pending work |
| DONE | `#d4edda` (green) | `#155724` | Completed |
| CLIENT-SIDE | `#d1ecf1` (blue) | `#0c5460` | Handled by client |
| NEEDS CLARIFICATION | `#e8daef` (purple) | `#512e5f` | Requires discussion |
| WARNING | `#fff3cd` (yellow) | `#856404` | Caution |
| ERROR | `#f8d7da` (red) | `#721c24` | Failure |
| N/A | `#e2e3e5` (gray) | `#495057` | Not applicable |

Users can add or override mappings with `--custom-colors`.

### Engine Fallback

The script tries `weasyprint` first (better CSS support, proper page breaks, modern rendering). If weasyprint is not installed, it falls back to `xhtml2pdf` (pure Python, always installable). If neither is available, the script prints install instructions and exits — it does not auto-install packages.

**Before first use, install dependencies explicitly:**

```bash
pip install markdown2==2.5.3
pip install weasyprint          # recommended
# OR
pip install xhtml2pdf==0.2.16   # pure Python fallback
```

### Page Breaks

Each `## ` (h2) heading starts on a new page for long documents. This keeps sections cleanly separated in the PDF output.

## Default Styling

The generated PDF includes sensible defaults:
- **Font**: Helvetica / Arial sans-serif, 9px body
- **Headings**: Scaled sizes (h1: 20px → h4: 10px), h1/h2 with bottom borders
- **Tables**: Collapsed borders, dark header row (`#2c3e50` background, white text), alternating row colors
- **Code blocks**: Light gray background, monospace font
- **Blockquotes**: Left blue border, light background
- **Page margins**: 1.5cm on all sides

## Arguments Reference

| Argument | Required | Default | Description |
|---|---|---|---|
| `input` | Yes | — | Path to the markdown file |
| `output` | No | `<input>.pdf` | Output PDF path. Defaults to same name with .pdf extension |
| `--landscape` | No | Auto | Force landscape orientation |
| `--portrait` | No | Auto | Force portrait orientation |
| `--status-colors` | No | Off | Enable status keyword cell coloring |
| `--custom-colors` | No | — | JSON string of custom keyword → color mappings. Format: `'{"KEYWORD": "#bg:#text"}'` |

## Troubleshooting

**Tables look clipped or overflow**: Try `--landscape` to give tables more horizontal space.

**Status colors not appearing**: Make sure you passed `--status-colors`. The feature is off by default. Also verify that the status keywords are wrapped in `**bold**` in the markdown source.

**weasyprint won't install**: It requires system libraries (cairo, pango). On macOS: `brew install cairo pango`. On Ubuntu: `apt install libcairo2-dev libpango1.0-dev`. If you can't install them, the script falls back to xhtml2pdf automatically.

**Fonts look different**: weasyprint uses system fonts, xhtml2pdf uses built-in PDF fonts. Results may vary slightly between engines.
