---
name: word-document
description: Word (.docx) manipulation via MCP server. Use for reading, creating, editing, formatting Word documents including tables, footnotes, comments, images, headers, styles, and PDF conversion.
license: Complete terms in LICENSE.txt
---

# Word Document Workflows

Use this skill when `.docx` layout and document structure matter, not just the raw text.

## Current MCP Reality

Microsoft publicly documents a Word MCP server in the Microsoft 365 Agents Toolkit preview, but tool availability still depends on the host. In GitHub Copilot you may see Word-specific tools; in other clients they may be missing. If direct Word MCP access is unavailable, use the included local script workflow.

## Activation Conditions

- Creating or editing `.docx` reports, memos, or structured deliverables
- Applying headings, tables, images, or styles
- Reviewing or extracting document structure
- Preparing Word output before a later PDF conversion

## Practical Workflow

1. Confirm whether the client exposes Word MCP capabilities.
2. Start with structure: title, headings, sections, tables.
3. Apply styling consistently only after the structure is right.
4. Validate comments, footnotes, and references before export.
5. Use the local generator script when MCP access is unavailable.

## Document Checklist

- [ ] Heading hierarchy is clear
- [ ] Tables are readable and consistently styled
- [ ] Comments or review notes are intentional
- [ ] Placeholder text is removed
- [ ] The final document was re-opened or otherwise verified after generation

## References & Resources

### Documentation
- [DOCX Formatting Reference](./references/docx-formatting-reference.md) - Practical formatting notes and document structure guidance

### Scripts
- [DOC Template Generator](./scripts/doc-template-generator.py) - Local fallback for generating Word-ready document structures

### Examples
- [Report Generation Example](./examples/report-generation-example.md) - Example report workflow for `.docx` output

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [microsoft-development](../microsoft-development/SKILL.md) | Microsoft ecosystem context and official docs |
| [excel-sheet](../excel-sheet/SKILL.md) | Bring spreadsheet output into Word reports |
| [powerpoint-ppt](../powerpoint-ppt/SKILL.md) | Convert report output into presentation-ready summaries |
