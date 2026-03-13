---
name: markdown-converter
description: Convert documents to Markdown using markitdown. Use when you need to extract text and convert PDF, Word, PowerPoint, Excel, HTML, CSV, JSON, XML, images (with EXIF/OCR), audio, ZIP archives, YouTube URLs, or EPUBs to Markdown format for LLM processing or text analysis.
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: automated
---

# Markdown Converter

## Overview

This skill uses markitdown to convert various document formats to Markdown. It provides a reliable conversion tool for extracting content from PDFs, Word documents, presentations, spreadsheets, and many other file formats.

## Instructions

Use the `convert.sh` script to convert files to Markdown:

```bash
~/.config/opencode/skill/markdown-converter/scripts/convert.sh <input_file> [output_file]
```

- Provide an input file path to convert
- Optionally specify an output file path (defaults to stdout)
- Supported formats: PDF, DOCX, PPTX, XLSX, HTML, CSV, JSON, XML, images, audio, ZIP, YouTube, EPUB

## Examples

Convert a PDF to Markdown and save to file:
```
~/.config/opencode/skill/markdown-converter/scripts/convert.sh document.pdf document.md
```

Convert a Word document and output to stdout:
```
~/.config/opencode/skill/markdown-converter/scripts/convert.sh report.docx
```

Convert an Excel spreadsheet:
```
~/.config/opencode/skill/markdown-converter/scripts/convert.sh data.xlsx data.md
```

Direct markitdown usage:
```
/Users/johannwaldherr/.local/bin/markitdown document.pdf -o document.md
```
