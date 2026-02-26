---
name: doc-to-text
description: Extract text content from various file formats. Supports PDF, Excel, Word, Images (OCR), Email, and ZIP Archives. Use for summarizing or analyzing binary files.
status: implemented
category: Utilities
last_updated: '2026-02-13'
tags:
  - documentation
  - gemini-skill
---

# Document to Text Converter

## Overview

This skill acts as a universal converter to extract plain text and structured data from various binary and complex file formats. It enables Gemini to "read" files that are otherwise inaccessible.

## Capabilities

### 1. Document Extraction

- **PDF** (`.pdf`): Extracts plain text.
- **Excel** (`.xlsx`): Converts sheets to CSV and performs OCR on embedded images.
- **Word** (`.docx`): Extracts text and performs OCR on embedded images.
- **PowerPoint** (`.pptx`): Extracts slide text and performs OCR on embedded images.

### 2. Image OCR

- **Images** (`.png`, `.jpg`, `.jpeg`, `.webp`): Uses Tesseract.js to perform OCR (Optical Character Recognition) and extract text from images. Supports English and Japanese.

### 3. Data & Archives

- **Email** (`.eml`): Parses headers (From, To, Subject) and body text.
- **ZIP Archive** (`.zip`): Lists files and extracts content of text-based files within the archive without extracting to disk.

## Usage

To read a file, execute the `extract.cjs` script with the file path.

```bash
node scripts/extract.cjs <path/to/file>
```

**Example:**
User: "What does the error screenshot say?"
Action: `node scripts/extract.cjs error.png`

## Dependencies

This skill requires Node.js packages.
Run `npm install` in the skill directory before using.

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
