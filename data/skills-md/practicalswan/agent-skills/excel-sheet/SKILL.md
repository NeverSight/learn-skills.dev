---
name: excel-sheet
description: Excel (.xlsx) manipulation via MCP server. Use for creating workbooks, formatting cells, writing formulas, building charts, pivot tables, data analysis, or any task involving Excel spreadsheets.
license: Complete terms in LICENSE.txt
---

# Excel Spreadsheet Workflows

Use this skill when the deliverable is an `.xlsx` workbook or when spreadsheet structure matters.

## Current MCP Reality

Excel MCP tooling is host-dependent. In GitHub Copilot, Excel actions may appear as grouped Office tools. In Codex or Claude, those tools may be absent entirely. Treat the included Python script as the reliable fallback.

## Activation Conditions

- Creating or updating workbooks
- Converting CSV data into structured Excel output
- Applying formulas, formatting, charts, or pivots
- Producing spreadsheet deliverables when layout matters

## Practical Workflow

1. Confirm whether the client exposes spreadsheet MCP tools.
2. If yes, inspect the actual tool names before assuming a wrapper exists.
3. If no, use the local converter or author the workbook with `openpyxl`.
4. Validate formulas and chart ranges before claiming the workbook is ready.

## Workbook Checklist

- [ ] Sheets are named clearly
- [ ] Headers are formatted consistently
- [ ] Formulas are used instead of hardcoded derived values
- [ ] Charts reference the correct ranges
- [ ] Frozen panes or filters are applied where useful

## References & Resources

### Documentation
- [Excel Formulas Reference](./references/excel-formulas-reference.md) - Formula patterns, lookup guidance, and Power Query notes

### Scripts
- [CSV to XLSX Converter](./scripts/csv-to-xlsx.py) - Local fallback for generating formatted Excel workbooks from CSV input

### Examples
- [Excel Workbook Examples](./examples/excel-workbook-examples.md) - Example workbook structures and automation patterns

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [microsoft-development](../microsoft-development/SKILL.md) | Microsoft docs and ecosystem context |
| [powerbi-modeling](../powerbi-modeling/SKILL.md) | Shape workbook exports for Power BI ingestion or review |
| [word-document](../word-document/SKILL.md) | Move spreadsheet output into formal reports |
| [powerpoint-ppt](../powerpoint-ppt/SKILL.md) | Move charts and summary data into slide decks |
