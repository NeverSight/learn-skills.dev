---
name: excel-artisan
description: Generates and edits Excel (.xlsx) files. Capable of converting JSON/CSV/HTML to Excel, modifying cell values, and applying basic formatting. Use when you need to produce Excel reports or modify existing spreadsheets.
status: implemented
category: Data & Content
last_updated: '2026-02-13'
tags:
  - automation
  - gemini-skill
---

# Excel Artisan

## Overview

Excel Artisan is a specialized skill for **creating and modifying Excel files**. While `doc-to-text` reads files, this skill focuses on **writing** them. It enables automated reporting, data conversion, and spreadsheet manipulation directly from the CLI.

## Capabilities

### 1. Visual Excel Generation

- **Theme Awareness**: Automatically applies layout patterns defined in `knowledge/templates/themes/excel_design_guide.md`.
- **Metadata Injection**: Automatically populates project headers (System Name, Phase, etc.).
- **Grid Optimization**: Formats tables with consistent borders, alternating row colors, and professional fonts.

### 2. Data Conversion

2.  **HTML to Excel**: Scrapes an HTML table and saves it as an Excel file (preserving layout like merged cells).
3.  **Edit Spreadsheet**: Loads an existing `.xlsx`, updates specific cells, and saves the result.

## Usage

### 1. Convert Data to Excel

```bash
# Convert a JSON file to Excel
node scripts/generate.cjs input.json output.xlsx

# Convert an HTML file (containing <table>) to Excel
node scripts/html_to_excel.cjs input.html output.xlsx
```

### 2. Dependencies

Requires `xlsx` (SheetJS) and `jsdom` (for HTML parsing).

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
