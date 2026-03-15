---
name: word-documents
description: "Process, analyze, and manipulate Word documents (.docx). Use when the user wants to work with Word files: analyze structure/comments/changes, add review comments, accept/reject tracked changes, apply formatting standards, convert between formats (Markdown/DOCX/PDF/HTML), compare documents, create new documents, or merge files. Essential for legal, compliance, regulatory, and professional document workflows."
tags:
  [
    word,
    docx,
    document,
    legal,
    compliance,
    comments,
    track-changes,
    formatting,
    redline,
    convert,
    merge,
    review,
  ]
version: 0.1.0
---

# Word Document Processing

## Overview

Comprehensive toolkit for working with Word documents (.docx). Covers the full lifecycle: analyzing, reviewing, formatting, converting, comparing, creating, and merging documents. Built for professional workflows in legal, compliance, regulatory, and corporate environments.

For advanced code examples and detailed library reference, see `reference.md`. For predefined formatting standards (legal, academic, corporate), see `standards.md`.

## Quick Reference

| Task                 | Script             | Command                                                                     |
| -------------------- | ------------------ | --------------------------------------------------------------------------- |
| Analyze document     | `analyze.py`       | `python3 scripts/analyze.py report.docx`                                    |
| List comments        | `comments.py`      | `python3 scripts/comments.py list report.docx`                              |
| Add comment          | `comments.py`      | `python3 scripts/comments.py add report.docx -t "search text" -c "Comment"` |
| List tracked changes | `track_changes.py` | `python3 scripts/track_changes.py list report.docx`                         |
| Accept all changes   | `track_changes.py` | `python3 scripts/track_changes.py accept report.docx -o clean.docx`         |
| Apply formatting     | `format.py`        | `python3 scripts/format.py report.docx -s legal -o formatted.docx`          |
| Convert MD to DOCX   | `convert.py`       | `python3 scripts/convert.py notes.md -f md -t docx -o report.docx`          |
| Convert DOCX to PDF  | `convert.py`       | `python3 scripts/convert.py report.docx -f docx -t pdf -o report.pdf`       |
| Compare documents    | `compare.py`       | `python3 scripts/compare.py original.docx revised.docx`                     |
| Create document      | `create.py`        | `python3 scripts/create.py -i content.md -o report.docx`                    |
| Merge documents      | `merge.py`         | `python3 scripts/merge.py doc1.docx doc2.docx -o combined.docx`             |

## When to Use

Use this skill when the user asks to:

- Analyze a Word document (structure, metadata, styles, word count)
- Extract or list comments from a document
- Add review comments to specific text
- List, accept, or reject tracked changes
- Apply formatting standards (legal, academic, corporate, regulatory)
- Convert between Markdown, DOCX, PDF, and HTML formats
- Compare two versions of a document
- Create a new Word document from text, Markdown, or a JSON specification
- Merge multiple Word documents into one
- Generate a redline or diff between document versions
- Clean up formatting or normalize styles

## Input Parameters

| Parameter     | Required | Description                  | Example                             |
| ------------- | -------- | ---------------------------- | ----------------------------------- |
| `file_path`   | Yes      | Path to the .docx file       | `/Users/me/Documents/contract.docx` |
| `output_path` | No       | Path for output file         | `./output.docx`                     |
| `standard`    | No       | Formatting standard to apply | `legal`, `academic`, `corporate`    |
| `format`      | No       | Target format for conversion | `docx`, `md`, `pdf`, `html`         |

## Procedures

### 1. Analyze a Document

Extract text, metadata, structure, styles, comments, and tracked changes.

```bash
# Full analysis as JSON
python3 scripts/analyze.py "/path/to/document.docx"

# Text only
python3 scripts/analyze.py "/path/to/document.docx" --mode text

# Metadata only
python3 scripts/analyze.py "/path/to/document.docx" --mode metadata

# Comments only
python3 scripts/analyze.py "/path/to/document.docx" --mode comments

# Tracked changes only
python3 scripts/analyze.py "/path/to/document.docx" --mode changes

# Structure (headings hierarchy)
python3 scripts/analyze.py "/path/to/document.docx" --mode structure

# Save analysis to file
python3 scripts/analyze.py "/path/to/document.docx" -o analysis.json
```

### 2. Manage Comments

List, add, remove, or export comments.

```bash
# List all comments
python3 scripts/comments.py list "/path/to/document.docx"

# Add a comment on text matching "indemnification clause"
python3 scripts/comments.py add "/path/to/document.docx" \
  -t "indemnification clause" \
  -c "This clause needs review by senior counsel" \
  -a "Review Bot" \
  -o reviewed.docx

# Remove all comments
python3 scripts/comments.py remove "/path/to/document.docx" -o clean.docx

# Remove comment by index
python3 scripts/comments.py remove "/path/to/document.docx" --index 0 -o clean.docx

# Export comments to JSON
python3 scripts/comments.py export "/path/to/document.docx" -o comments.json

# Export comments to CSV
python3 scripts/comments.py export "/path/to/document.docx" -o comments.csv --format csv
```

### 3. Track Changes

List, accept, or reject tracked changes; generate a summary.

```bash
# List all tracked changes
python3 scripts/track_changes.py list "/path/to/document.docx"

# Accept all changes (produce clean document)
python3 scripts/track_changes.py accept "/path/to/document.docx" -o accepted.docx

# Reject all changes (revert to original)
python3 scripts/track_changes.py reject "/path/to/document.docx" -o reverted.docx

# Accept changes by specific author
python3 scripts/track_changes.py accept "/path/to/document.docx" --author "Jane Doe" -o partial.docx

# Generate human-readable summary of all changes
python3 scripts/track_changes.py summary "/path/to/document.docx"
```

### 4. Apply Formatting Standards

Normalize styles, fonts, spacing, and headings to a named standard.

```bash
# Apply legal formatting standard
python3 scripts/format.py "/path/to/document.docx" -s legal -o formatted.docx

# Apply academic formatting (APA)
python3 scripts/format.py "/path/to/document.docx" -s academic -o formatted.docx

# Apply corporate standard
python3 scripts/format.py "/path/to/document.docx" -s corporate -o formatted.docx

# Apply regulatory/compliance standard
python3 scripts/format.py "/path/to/document.docx" -s regulatory -o formatted.docx

# Apply custom standard from JSON file
python3 scripts/format.py "/path/to/document.docx" --custom-standard my_standard.json -o formatted.docx

# Normalize heading hierarchy only
python3 scripts/format.py "/path/to/document.docx" --fix-headings -o formatted.docx

# Clean up direct formatting (convert to named styles)
python3 scripts/format.py "/path/to/document.docx" --clean-direct-formatting -o formatted.docx
```

### 5. Convert Between Formats

Convert documents between Markdown, DOCX, PDF, and HTML using pandoc.

```bash
# Markdown to DOCX
python3 scripts/convert.py notes.md -f md -t docx -o report.docx

# DOCX to Markdown
python3 scripts/convert.py report.docx -f docx -t md -o report.md

# DOCX to PDF
python3 scripts/convert.py report.docx -f docx -t pdf -o report.pdf

# HTML to DOCX
python3 scripts/convert.py page.html -f html -t docx -o document.docx

# DOCX to HTML
python3 scripts/convert.py report.docx -f docx -t html -o report.html

# Markdown to DOCX with reference template for styling
python3 scripts/convert.py notes.md -f md -t docx -o report.docx --reference template.docx

# DOCX to Markdown preserving track changes
python3 scripts/convert.py report.docx -f docx -t md -o report.md --track-changes all
```

### 6. Compare Documents

Compare two versions of a document and produce a diff or redline.

```bash
# Compare and output diff as Markdown
python3 scripts/compare.py original.docx revised.docx

# Compare and save diff report as JSON
python3 scripts/compare.py original.docx revised.docx -o diff.json --format json

# Compare and produce a redline DOCX with tracked changes
python3 scripts/compare.py original.docx revised.docx -o redline.docx --format docx

# Word-level diff (more granular)
python3 scripts/compare.py original.docx revised.docx --granularity word
```

### 7. Create a New Document

Create a DOCX from text, Markdown, or a structured JSON specification.

```bash
# Create from Markdown file
python3 scripts/create.py -i content.md -o report.docx

# Create from plain text
python3 scripts/create.py -i notes.txt -o document.docx

# Create from JSON specification
python3 scripts/create.py -i spec.json -o report.docx

# Create with a template for styling
python3 scripts/create.py -i content.md -o report.docx --template template.docx

# Create with headers and footers
python3 scripts/create.py -i content.md -o report.docx \
  --header "Confidential" --footer "Page {page}"
```

**JSON Specification Format:**

```json
{
  "title": "Quarterly Report",
  "metadata": {
    "author": "Jane Doe",
    "subject": "Q4 2025 Financial Review"
  },
  "sections": [
    {
      "heading": "Executive Summary",
      "level": 1,
      "content": "This report covers the fourth quarter..."
    },
    {
      "heading": "Revenue",
      "level": 2,
      "content": "Total revenue reached $2.5M...",
      "table": {
        "headers": ["Quarter", "Revenue", "Growth"],
        "rows": [
          ["Q3", "$2.1M", "5%"],
          ["Q4", "$2.5M", "19%"]
        ]
      }
    }
  ]
}
```

### 8. Merge Documents

Combine multiple DOCX files into a single document.

```bash
# Merge two or more documents
python3 scripts/merge.py doc1.docx doc2.docx doc3.docx -o combined.docx

# Merge with page breaks between documents
python3 scripts/merge.py doc1.docx doc2.docx -o combined.docx --page-breaks

# Merge using first document as style master
python3 scripts/merge.py master.docx appendix.docx -o full.docx --style-from first
```

## Bundled Scripts

| Script                     | Type   | Description                                                             |
| -------------------------- | ------ | ----------------------------------------------------------------------- |
| `scripts/analyze.py`       | Python | Analyze document structure, metadata, styles, comments, tracked changes |
| `scripts/comments.py`      | Python | List, add, remove, export comments with author/date/position            |
| `scripts/track_changes.py` | Python | List, accept, reject tracked changes; generate change summary           |
| `scripts/format.py`        | Python | Apply formatting standards (legal, academic, corporate, regulatory)     |
| `scripts/convert.py`       | Python | Convert between MD, DOCX, PDF, HTML formats via pandoc                  |
| `scripts/compare.py`       | Python | Compare two documents, produce diff report or redline DOCX              |
| `scripts/create.py`        | Python | Create new DOCX from text, Markdown, or JSON specification              |
| `scripts/merge.py`         | Python | Merge multiple DOCX files into one                                      |

## Examples

Example requests that trigger this skill:

```
analyze this word document and show me the comments
add a review comment on the indemnification clause
accept all tracked changes in this contract
format this document to legal standards
convert my meeting notes from markdown to word
compare the original contract with the revised version
create a word document from this markdown content
merge these three word documents into one
show me all the tracked changes in this agreement
apply corporate formatting to the quarterly report
export all comments from this document to a spreadsheet
generate a redline between the two contract versions
```
