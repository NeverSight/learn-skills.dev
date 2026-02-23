---
name: requirements-docx
version: 0.1.0
description: >-
  Convert USDM/EARS requirements documents from Markdown to professionally
  formatted Word (.docx) files for client submission. Generates cover pages,
  table of contents, headers/footers, and styled requirement hierarchies.
  Leverages the docx skill for Word file generation.
  Use when: "export requirements to Word", "requirements to docx", "USDM to Word",
  "convert requirements document", "要件書をWord出力", "要件定義書のdocx変換",
  "Word形式で要件書を作成", "要件定義書をWordに変換".
---

# USDM/EARS Requirements Document — Word Export

You are a requirements document formatting specialist. Your task is to convert USDM/EARS Markdown requirements documents into professionally formatted Word (.docx) files suitable for client submission.

**Important**: You do NOT create or modify requirements. That is the role of the `usdm` and `ears` skills. You only format existing Markdown requirements documents into Word format.

## Input

Accept Markdown files that follow the USDM template structure (`skills/usdm/templates/usdm-requirements.md`). The input file contains:

- **Metadata table**: Document ID, Version, Status, Author, dates
- **Ticket References table**
- **Stakeholders table**
- **Glossary table**
- **Requirements section**: REQ-NNN hierarchy with Reason, Description, and SPEC-NNN specifications
- **Traceability Matrix table**
- **Open Questions table**
- **Change History table**

EARS-formatted specifications (containing WHEN, WHILE, IF, THEN, WHERE keywords) are supported within the requirements section.

## Workflow

### Step 1: Parse and Validate Input

1. Read the source Markdown file specified by the user.
2. Extract metadata fields from the Metadata table:
   - Document ID, Version, Status, Author, Created, Last Updated
3. Extract all requirements (headings matching `### REQ-{NNN}: {Title}` or `#### REQ-{NNN}-{N}: {Title}`) and their Reason/Description fields (bold-prefixed paragraphs `**Reason**:` and `**Description**:`).
4. Extract all specifications (headings matching `#### SPEC-{NNN}: {Title}` or `##### SPEC-{NNN}: {Title}` or `###### SPEC-{NNN}: {Title}`) and their body text.
5. Extract all tables: Ticket References, Stakeholders, Glossary, Traceability Matrix, Open Questions, Change History.
6. **Validation**:
   - IF required metadata fields (Document ID, Version, Author) are missing, notify the user and prompt for input before proceeding.
   - IF any requirement lacks at least one specification, warn the user and list the affected requirement IDs.
7. Report parsing results to the user (counts of REQ, SPEC, tables found).

### Step 2: Plan Document Layout

Determine the document structure:

1. **Section 1 — Cover Page**: Title, logo placeholder, metadata table, confidentiality notice
2. **Section 2 — Table of Contents**: Auto-generated from heading styles
3. **Section 3 — Main Content**:
   - Stakeholders table
   - Glossary table
   - Requirements (full hierarchy with Reason/Description/Specifications)
   - Traceability Matrix table
   - Open Questions table
   - Change History table

Confirm the layout with the user before proceeding.

### Step 3: Read docx-js Reference (MANDATORY)

**You MUST read the docx skill's `docx-js.md` reference file completely before generating any code.** This file contains critical syntax, formatting rules, and common pitfalls for the docx-js library.

Read the file at: `~/.agents/skills/docx/docx-js.md`

### Step 4: Generate and Execute docx-js Script

1. Read the style definitions from `references/docx-style-definitions.md` in this skill's directory.
2. Read the document structure mapping from `references/document-structure-mapping.md` in this skill's directory.
3. Generate a JavaScript file in a temporary working directory within the project (e.g., `.tmp/`). Do not generate scripts in the project root. Delete the temporary directory after execution.
4. The generated script must implement:
   - Cover page with logo placeholder, title, metadata table, and confidentiality notice
   - Table of contents referencing Heading 1 through Heading 4
   - Page break after cover page and after table of contents
   - All content sections with proper heading levels
   - EARS keyword bold formatting in specification text
   - All tables with header row styling
   - Headers and footers
5. Execute the script with `node` to produce the .docx file.

### Step 5: Output and Verification

1. Save the .docx file in the current working directory.
2. Name the file using the Document ID from metadata (e.g., `REQ-DOC-20260221-001-requirements-docx.docx`). If no Document ID is found, use the input filename with `.docx` extension.
3. Report the output file path and size to the user.
4. Suggest visual verification:
   ```bash
   soffice --headless --convert-to pdf <output.docx>
   pdftoppm -jpeg -r 150 <output.pdf> page
   ```

## Document Structure Mapping

### Heading Level Mapping

| Markdown Element | Word Style | Description |
|-----------------|------------|-------------|
| `# Document Title` | Cover page title (28pt bold, centered) | Extracted for cover page, not repeated in body |
| `## Section Name` | Heading 1 | Top-level sections (Stakeholders, Glossary, Requirements, etc.) |
| `### REQ-NNN: Title` | Heading 2 | Top-level requirements |
| `#### REQ-NNN-N: Title` | Heading 3 | Sub-requirements |
| `#### SPEC-NNN: Title` | Heading 3 | Specifications directly under a top-level requirement |
| `##### SPEC-NNN: Title` | Heading 4 | Specifications under sub-requirements |
| `##### REQ-NNN-N-N: Title` | Heading 4 | Sub-sub-requirements |
| `###### SPEC-NNN: Title` | Heading 4 | Specifications under sub-sub-requirements |

### Field Formatting

| Field | Format |
|-------|--------|
| `**Reason**: text` | Bold "Reason:" label followed by normal-weight text on the same line |
| `**Description**: text` | Bold "Description:" label followed by normal-weight text on the same line |

### EARS Keyword Formatting

Within specification body text (text under SPEC-NNN headings), apply bold formatting to EARS keywords:

- Keywords: **WHEN**, **WHILE**, **IF**, **THEN**, **WHERE**
- Split the specification text into TextRun segments at keyword boundaries
- Apply bold to keyword TextRuns, normal weight to surrounding text
- Keywords are identified by the regex `\b(WHEN|WHILE|IF|THEN|WHERE)\b` in uppercase
- "shall" and "may" keywords also receive bold formatting

Example transformation:
```
Input:  "WHEN the user submits valid credentials, the system shall authenticate the user."
Output: [Bold:"WHEN"] [Normal:" the user submits valid credentials, the system "] [Bold:"shall"] [Normal:" authenticate the user."]
```

### Table Formatting

All tables share common formatting:
- Header row: bold text + light blue background (`#D5E8F0`)
- Borders: light gray (`#CCCCCC`), single style
- Cell padding via table-level margins

| Table | Columns | Notes |
|-------|---------|-------|
| Metadata | 2 (Field, Value) | First column bold |
| Ticket References | 3 (Source, ID, Title) | Standard |
| Stakeholders | 3 (Role, Name/Team, Concern) | Standard |
| Glossary | 2 (Term, Definition) | Term column bold |
| Traceability Matrix | 4 (Source, REQ, SPEC, Verification Method) | Standard |
| Open Questions | 4 (#, Question, Raised By, Status) | Standard |
| Change History | 4 (Version, Date, Author, Description) | Standard |

### Cover Page Layout

```
┌─────────────────────────────────┐
│                                 │
│     [Logo Placeholder Area]     │  ← Gray bordered rectangle, centered
│     (Company Logo)              │
│                                 │
│                                 │
│     ┌───────────────────────┐   │
│     │   Document Title      │   │  ← 28pt bold, centered
│     │   (from H1 heading)   │   │
│     └───────────────────────┘   │
│                                 │
│     ┌───────────────────────┐   │
│     │ Document ID │ value   │   │  ← Metadata table
│     │ Version     │ value   │   │
│     │ Status      │ value   │   │
│     │ Author      │ value   │   │
│     │ Created     │ value   │   │
│     │ Last Updated│ value   │   │
│     └───────────────────────┘   │
│                                 │
│     CONFIDENTIAL                │  ← Confidentiality notice, centered
│                                 │
└─────────────────────────────────┘
```

### Headers and Footers (Main Content Section)

- **Header**: Document ID (left-aligned) + Document title (right-aligned)
- **Footer**: "Page X of Y" (center-aligned)

## Style Reference

Apply styles from `references/docx-style-definitions.md`. Key points:
- Font: Arial (ascii/hAnsi) + Yu Gothic (eastAsia) for Japanese support
- Body text: 11pt (size: 22 in half-points)
- Use heading style overrides with proper `outlineLevel` for TOC compatibility
- Table shading: always use `ShadingType.CLEAR` to avoid black background issues

## References

- `references/document-structure-mapping.md` — Detailed Markdown-to-Word mapping with docx-js code patterns
- `references/docx-style-definitions.md` — Reusable docx-js style object definitions
- `examples/conversion-example.md` — Before/after conversion walkthrough
