---
name: docs-pdf
description: Parse PDF documents into repository-friendly markdown and text artifacts. Use when users need to extract text, tables, or structure from PDF files.
---

# PDF Document Parsing

Parse PDF documents into markdown, text, and structured JSON using multi-method extraction.

## Usage

Run the parsing script directly:

```bash
./scripts/parse_pdf.py <path_to_file.pdf> <output_dir>
```

**Example:**
```bash
./scripts/parse_pdf.py ~/documents/manual.pdf ./parsed/
```

The script uses 4 extraction methods:
- pypdf - Basic text extraction with page markers
- pdfminer - Detailed layout preservation
- pdfplumber - Table extraction and structure
- markitdown - Microsoft's markdown converter

## Output Structure

```
output_dir/
├── file.pdf/
│   ├── parsing_summary.json
│   ├── pypdf/
│   │   └── content.md
│   ├── pdfminer/
│   │   └── content.txt
│   ├── pdfplumber/
│   │   ├── content.md
│   │   └── tables.json
│   └── markitdown/
│       └── content.md
```

## Script Features

- Handles text-heavy and table-heavy PDFs
- Preserves layout information where possible
- Extracts tables as structured JSON
- Provides multiple format options (md, txt, json)
- Continues on errors (one method failure doesn't stop others)

## Method Selection

- **markitdown** - Best for AI understanding (continuous markdown, no page breaks)
- **pdfplumber** - Best for documents with complex tables
- **pypdf** - Fast fallback for simple text extraction
- **pdfminer** - Best when layout preservation is critical
