---
name: table-design
description: "Decide, design, and validate research, financial, comparison, matrix, survey, annex, and compact presentation tables. Use when structured values need accurate lookup, row and column comparison, repeated headers, numeric alignment, totals, footnotes, sources, landscape handling, annex routing, or a decision about whether a chart is more appropriate."
---

# Table Design

Make exact comparison readable without shrinking it into illegibility.

## When to use

Use when readers must look up or compare precise values, categories, or definitions.

## When not to use

Choose a chart for pattern recognition or prose for a simple list.

## Inputs

Structured data, table purpose, audience, output size, design tokens, hierarchy, units, source and footnote requirements.

## Outputs

Table specification, editable table, accessibility headers, display and annex variants where needed, and density warnings.

## Required workflow

1. Read [TABLE-DESIGN.md](references/TABLE-DESIGN.md).
2. Confirm that a table is the right form.
3. Identify primary comparison direction and sort accordingly.
4. Define headers, stubs, units, alignment, decimals, totals, subtotals, footnotes, and source line.
5. Test width, row splits, repeated headers, landscape options, and annex routing.
6. Render in the target artifact and inspect at intended size.

## Hard rules

- Do not use tiny type to preserve all columns.
- Repeat headers after page breaks and avoid split rows where practical.
- Align numbers by decimal or place value; distinguish totals and subtotals.
- Preserve units, missing-value notation, footnotes, and sources.
- Abbreviate display tables and move full versions to annexes when the narrative does not require every field.

## Checkpoints

Escalate tables that require changed data scope, landscape orientation, annex movement, or more than one page or slide.

## Files to read by phase

Read the table reference before specification and the target publication or presentation composition reference before layout.

## Quality checks

Check values, order, column spans, numeric alignment, row and header breaks, footnote markers, sources, contrast, responsive or print behavior, and accessibility headers.

## Failure and fallback behaviour

When a table cannot fit, return ranked remedies: remove redundant fields, abbreviate with a key, split by analytical question, rotate to landscape, move to annex, or provide a downloadable data file.

## Example invocations

- "Redesign this survey table for an A4 research report."
- "Create a compact presentation table with only decision-critical values."
- "Split this financial table without breaking totals or notes."

## Adjacent skills

Use data visualisation when the primary job is pattern recognition and copy fitting for concise headers and notes.
