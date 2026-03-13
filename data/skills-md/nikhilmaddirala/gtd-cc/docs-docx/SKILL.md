---
name: docs-docx
description: Parse Word documents (.docx) into repository-friendly markdown artifacts. Use when users need to extract content from Word files, convert to markdown, or batch process document directories.
---

# Word Document Parsing

Parse Word documents (.docx) into markdown, JSON, and image artifacts using multi-method extraction.

## Usage

Run the parsing script directly:

```bash
./scripts/parse_docx.py <path_to_file.docx> <output_dir>
```

**Example:**
```bash
./scripts/parse_docx.py ~/documents/report.docx ./parsed/
```

The script uses 4 extraction methods:
- python-docx (basic) - Fast text extraction
- python-docx (detailed) - Full structure with tables
- docx2txt - Simple text-only fallback
- markitdown - Microsoft's markdown converter

## Output Structure

```
output_dir/
├── file.docx/
│   ├── parsing_summary.json
│   ├── python_docx_basic/
│   │   └── content.md
│   ├── python_docx_detailed/
│   │   ├── content.md
│   │   ├── tables.json
│   │   └── images/
│   ├── docx2txt/
│   │   └── content.txt
│   └── markitdown/
│       └── content.md
```

## Script Features

- Self-contained Python script with inline uv metadata
- Handles multiple extraction methods for redundancy
- Creates JSON metadata for tables and document structure
- Extracts images with dimensions and metadata
- Continues on errors (one method failure doesn't stop others)
