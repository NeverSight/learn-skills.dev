---
name: office-suite
description: "Microsoft Office document manipulation (Word, Excel, PowerPoint, PDF). Use when: creating professional .docx documents, filling PDF forms, extracting tables from PDFs, building presentations, working with spreadsheets, or any task involving Office file formats. Triggers: Word, Excel, PowerPoint, PDF, .docx, .xlsx, .pptx, spreadsheet, presentation, slides, form, invoice, report, memo, letter, budget, financial model."
---

# Office Suite Skills

Comprehensive toolkit for creating, editing, and manipulating Microsoft Office documents and PDFs.

## Quick Navigation

| Task | Skill | Path |
|------|-------|------|
| Word documents (.docx) | docx | `./docx/SKILL.md` |
| PDF forms & manipulation | pdf | `./pdf/SKILL.md` |
| PowerPoint presentations | pptx | `./pptx/SKILL.md` |
| Excel spreadsheets | xlsx | `./xlsx/SKILL.md` |

## When to Use Each

### PDF (`./pdf/SKILL.md`)
- Extract text or tables from PDFs
- Fill out PDF forms (invoices, applications)
- Merge/split PDF files
- OCR scanned documents
- Add watermarks or passwords

### DOCX (`./docx/SKILL.md`)
- Create professional Word documents
- Work with tracked changes and comments
- Generate reports, letters, memos
- Insert images and tables
- Convert between formats

### PPTX (`./pptx/SKILL.md`)
- Create slide decks from scratch
- Edit existing presentations
- Add charts, images, animations
- Build pitch decks and proposals

### XLSX (`./xlsx/SKILL.md`)
- Create spreadsheets with formulas
- Build financial models and budgets
- Extract data from Excel files
- Recalculate and validate spreadsheets

## Shared Utilities

The `shared/office/` directory contains Python utilities used across all Office formats:
- `pack.py` - Repack XML into Office format
- `unpack.py` - Unpack Office file to XML
- `validate.py` - Validate Office document structure
- `soffice.py` - LibreOffice automation wrapper

## Dependencies

```bash
# Python libraries
pip install pypdf pdfplumber reportlab python-docx openpyxl

# Node libraries (for document creation)
npm install -g docx pptxgenjs

# System tools (optional but recommended)
brew install poppler qpdf libreoffice
```

## VULKN-Specific Notes

For Mexican SMB invoices (CFDI/Facturapi):
- Use PDF skill to extract data from received invoices
- Use DOCX skill to generate professional quotes and contracts
- Use XLSX skill for financial reporting

---

*Adapted from Anthropic's Claude Cowork skills, Feb 2026*
