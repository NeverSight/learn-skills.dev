---
name: standard-word-doc
description: >
  Use when a Word/.docx document must be generated, converted, standardized,
  audited, or repaired; when Markdown, LLMWiki, API design, implementation
  plans, reports, or formal Chinese materials need reliable Word formatting;
  or when headings, bullets, tables, fonts, spacing, page numbers, WPS/Google
  Docs compatibility, or "word排版乱了/格式不对/转docx/fix word formatting"
  quality matters.
---

# Standard Word Doc Skill

## Core Principle

This skill is a document template engine. Format consistency has priority over
content richness. Prefer deterministic `.docx` generation and repair over
manual visual tweaks.

`assets/standard-word-template.docx` is the formatting authority for headings,
body text, lists, page setup, headers, footers, numbering, and spacing. It is
based on the Pudong feasibility-study document style. Tables are the explicit
exception: always use the standard blue-header table style described in
`references/style-guide.md`. Do not hard-code blue headings, Arial/微软雅黑, or
other fallback styles when the template exists.

If the template is missing, use the fallback style specification in
`references/style-guide.md` instead of stopping.

## Workflow Decision

Classify the task before acting:

| User request | Pipeline |
| --- | --- |
| User provides requirements, notes, outline, or asks for a new Word document | Pipeline A: Generate |
| User provides Markdown text, `.md`, LLMWiki output, API design Markdown, or asks to convert to Word | Pipeline B: Markdown to DOCX |
| User provides an existing `.docx` and asks to check, fix, repair, standardize, or audit formatting | Pipeline C: Audit and Repair |

If the request mixes pipelines, run them in order. For example: convert Markdown
to `.docx`, then audit/repair the generated `.docx`.

## Pipeline A: Generate

1. Identify document type: implementation plan, construction plan, test report,
   summary report, API detail design, data governance report, or other.
2. Organize content into H1-H7 structure. Do not hard-code chapter numbers in
   body text; use Word Heading styles.
3. Write a temporary Markdown file with frontmatter when useful:

```markdown
---
title: 大数据平台接口详细设计
document_type: 详细设计文档
organization: XXXX单位
version: V1.0
date: 2026年05月15日
---
```

4. Run:

```bash
python3 scripts/render_standard_docx.py input.md --output-dir "$HOME/Documents/AI-Stack-Outputs/word-docs"
```

5. Return the output path and state whether TOC/page fields need refreshing in
   Word/WPS or via `scripts/finalize_docx.sh`.

## Pipeline B: Markdown To DOCX

1. If the user pasted Markdown, save it to a temporary `.md` file.
2. Preserve semantic structure: `#` to `####` for H1-H4, Markdown tables for
   tables, `-`/`*`/`+` for bullets, and `1.` for ordered lists.
3. For LLMWiki or API detail design content, normalize overly wide tables and
   fenced JSON/SQL/Java blocks before rendering. Prefer formal tables for API
   metadata, request parameters, response fields, error codes, and examples.
4. Run `scripts/render_standard_docx.py`. The script handles frontmatter,
   headings, body paragraphs, bullet lists, ordered lists, tables, and fenced
   code blocks.
5. For parallel items, use the approved black-diamond marker `◆` followed by
   the item text. Do not use other decorative bullet characters such as `•`,
   `·`, `▪`, or `—` as manual bullets.
6. Strip manual heading numbers such as `一、`, `第一章`, `1.1`, and `1.1.1`
   before applying Word Heading styles. Word/WPS heading numbering supplies the
   visible number.

## Pipeline C: Audit And Repair

For audit only:

```bash
python3 scripts/audit_standard_docx.py input.docx --output "$HOME/Documents/AI-Stack-Outputs/word-docs/input_audit.md"
```

For direct repair:

```bash
python3 scripts/repair_standard_docx.py input.docx
```

Repair output must not overwrite the source file. When the template exists,
repair rebuilds the document from `assets/standard-word-template.docx`: it
extracts source content, recreates paragraphs and tables in document order, and
applies the template's styles instead of preserving source direct formatting.
The repaired file uses the `_repaired.docx` suffix and a companion
`_repair_summary.md` explains what was changed and what still requires human
confirmation.

## Format Checklist

Use this checklist for both auditing and repair. See
`references/style-guide.md` for exact numeric style values.

### Errors: Repair Automatically

- Unicode bullet characters at paragraph start -> remove the character and
  apply Word `List Bullet`.
- Parallel list paragraphs -> normalize to `◆内容`.
- Body paragraph using inline bold plus size >= 14pt as a fake heading -> apply
  the matching Heading style.
- Manual numbering at the start of Heading paragraphs, such as `一、`, `第一章`,
  `1.1`, or `1.1.1` -> remove the manual number and keep the Heading style.
- Symbol, Wingdings, Wingdings 2, or Wingdings 3 fonts -> replace with
  Arial/微软雅黑.
- Hard line breaks inside a paragraph -> split into independent paragraphs.

### Warnings: Repair When Safe And Report

- Body text uses more than two different font sizes -> rebuild from template
  when available; otherwise normalize body runs to the fallback body size.
- Table width uses percent values -> convert tables to fixed DXA widths.
- Consecutive empty paragraphs -> keep one and remove extras.

### Needs Human Confirmation: Report Only

- Manual numbering such as `1.`, `（一）`, or `第一章` written in body style.
  Heading-style manual numbering is repaired automatically.
- Heading hierarchy jumps, such as H1 directly followed by H3.
- Missing page-number field.
- Full-width spaces or missing Chinese-English spacing in body text.

## Template Formatting Rules

When `assets/standard-word-template.docx` exists:

- Treat the template as the only visual standard.
- Use template styles such as `Title`, `Heading 1` through `Heading 7`,
  `Body Ref`, `List Paragraph`, `Table Grid`, and `Footer` when present.
- Keep template page sections, headers, footers, numbering, fonts, colors,
  paragraph spacing, table style, and margins.
- Override tables with the standard table style: blue header with white bold
  centered text, black regular-weight body text, light-blue/white alternating body rows,
  and light-gray borders.
- Do not apply direct run formatting unless needed to preserve code blocks in a
  no-template fallback or to enforce the standard table style.
- Do not keep source-document direct formatting during repair. Source content is
  the input; template formatting is the output.

## Default Style Fallback

When no template exists, scripts must create a valid `.docx` using:

- Body: Arial/微软雅黑, 11pt, black, 0pt before, 8pt after, 1.15 line spacing.
- H1: 22pt bold, black, 24pt before, 4pt after.
- H2: 16pt bold, black, 8pt before, 4pt after.
- H3: 15pt bold, black, 8pt before, 4pt after.
- H4: 14pt bold, black, 4pt before, 2pt after.
- Page: A4, top/bottom 2.54cm, left/right 3.17cm.
- Table header: `#1F5FAE` background, white bold centered text.
- Table body: alternating `#F3F6FB` and `#FFFFFF` rows, black regular-weight text.

## Hard Rules

- Never use unapproved Unicode bullets. Use `◆` only for parallel list items.
- Never simulate headings with bold body text. Use Heading styles.
- Never use Symbol or Wingdings fonts.
- Never overwrite user source `.docx` files during repair.
- Default output directory is `$HOME/Documents/AI-Stack-Outputs/word-docs`.
- Do not require LibreOffice, Word, WPS, or Pandoc for default generation.
- If LibreOffice is available and the user asks to refresh fields, run
  `scripts/finalize_docx.sh`.

## Dependencies

Required:

```bash
pip install python-docx
scripts/check_dependencies.sh
```

Optional field refresh:

```bash
brew install --cask libreoffice
```
