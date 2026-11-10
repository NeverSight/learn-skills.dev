---
name: pdf
description: "Read, create, combine, split, rotate, OCR, watermark, secure, or extract content from PDF files. Use when a PDF is a primary input or requested output. Not for LaTeX source editing or Word and spreadsheet deliverables."
license: Proprietary. LICENSE.txt has complete terms
allowed-tools: Bash(uv*, pdftotext*, qpdf*, pdftk*, mkdir*, ls*), Read, Write
---

# PDF Processing Guide

## Overview

This guide covers essential PDF processing operations using Python libraries and command-line tools. For advanced features, JavaScript libraries, and detailed examples, see REFERENCE.md. If you need to fill out a PDF form, read FORMS.md and follow its instructions.

## Quick Start

```python
from pypdf import PdfReader, PdfWriter

# Read a PDF
reader = PdfReader("document.pdf")
print(f"Pages: {len(reader.pages)}")

# Extract text
text = ""
for page in reader.pages:
    text += page.extract_text()
```

## Library & Tool Recipes

All Python library examples (pypdf, pdfplumber, reportlab), CLI tools (pdftotext, qpdf, pdftk), and common tasks (OCR, watermarks, image extraction, encryption):

**[references/pdf-recipes.md](references/pdf-recipes.md)**

## Quick Reference

| Task | Best Tool | Command/Code |
|------|-----------|--------------|
| Merge PDFs | pypdf | `writer.add_page(page)` |
| Split PDFs | pypdf | One page per file |
| Extract text | pdfplumber | `page.extract_text()` |
| Extract tables | pdfplumber | `page.extract_tables()` |
| Create PDFs | reportlab | Canvas or Platypus |
| Command line merge | qpdf | `qpdf --empty --pages ...` |
| OCR scanned PDFs | pytesseract | Convert to image first |
| Fill PDF forms | pdf-lib or pypdf (see FORMS.md) | See FORMS.md |

## Next Steps

- For advanced pypdfium2 usage, see REFERENCE.md
- For JavaScript libraries (pdf-lib), see REFERENCE.md
- If you need to fill out a PDF form, follow the instructions in FORMS.md
- For troubleshooting guides, see REFERENCE.md
