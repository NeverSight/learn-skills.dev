---
name: md-to-pdf
description: Convert markdown files to well-formatted PDF. Use when the user wants to export, render, or convert a .md file to PDF.
version: 1.0.0
---

# Markdown to PDF

Convert markdown to PDF using pandoc with xelatex. Produces clean sans-serif output with syntax-highlighted code blocks.

## Prerequisites

- `pandoc` (brew install pandoc)
- `basictex` (brew install --cask basictex)
- LaTeX packages: `sudo tlmgr install fontspec unicode-math selnolig upquote microtype parskip xurl bookmark fancyvrb csquotes framed`

## Command

```bash
pandoc INPUT.md -o OUTPUT.pdf \
  --resource-path=DIRECTORY_CONTAINING_IMAGES \
  --pdf-engine=xelatex \
  -V mainfont="Helvetica Neue" \
  -V monofont="Menlo" \
  -V fontsize=11pt \
  -V geometry:margin=1in \
  -V colorlinks=true \
  -V linkcolor=NavyBlue \
  -V urlcolor=NavyBlue \
  --syntax-highlighting=tango
```

## Usage Notes

- `--resource-path` must point to the directory containing any images referenced in the markdown (relative paths). Usually the directory the markdown file lives in.
- On macOS, `Helvetica Neue` and `Menlo` are always available. On Linux, substitute with `DejaVu Sans` / `DejaVu Sans Mono`. On Windows, `Segoe UI` / `Cascadia Code`.
- For long code blocks that overflow, add `-V geometry:margin=0.75in` to give more horizontal room.
- The `tango` syntax highlighting theme works well with light backgrounds. Other options: `kate`, `monochrome`, `espresso`, `haddock`, `zenburn`.
