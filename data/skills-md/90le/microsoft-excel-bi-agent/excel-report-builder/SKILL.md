---
name: excel-report-builder
description: Use when creating or modifying Excel report sheets, dashboards, tables, charts, pivots, controls, formulas, or polished client-facing layouts.
---

# Excel Report Builder

## Core Rule

Build the usable report surface first, but preserve the calculation contract behind it. Separate input, calculation, output, and QA areas so the workbook remains maintainable after handoff.

## Workflow

1. **Confirm report intent**
   - Identify audience, output workbook type, visible sheets, inputs, refresh path, and delivery format.
   - Preserve existing Chinese sheet and column terms when modifying a provided workbook.

2. **Design the workbook shape**
   - Keep client-facing sheets clean.
   - Use helper sheets only when needed and hide them after validation.
   - Prefer tables, named ranges, and structured references over fragile cell-only contracts when the workbook design allows.
   - Keep charts and controls tied to stable ranges.

3. **Implement safely**
   - Use OpenXML or workbook libraries for structural `.xlsx` edits where runtime evaluation is not needed.
   - Use Excel COM for charts, PivotTables, buttons, macros, Power Query refresh, Data Model interactions, or any calculation-dependent visual output.
   - If VBA is needed, route implementation through `excel-vba-workbook-engineering`.
   - If Power Query or Data Model logic changes, route those layers through the relevant specialist skill before final report assembly.

4. **Validate the report**
   - Inspect workbook structure and generated visible sheets.
   - Run formula quality, controls, and external dependency reports when the workbook is intended for delivery.
   - Reopen in Excel for visual/runtime validation when charts, controls, macros, refresh, or pivots matter.

## Design Defaults

- Use clear worksheet titles, frozen panes, readable column widths, and consistent number formats.
- Avoid hidden process drafts on final-facing sheets.
- Keep source, config, and calculation areas traceable for maintainers.
- Do not overwrite the only source workbook.

## Boundaries

- This skill is for Excel report workbooks, not Power BI semantic model development.
- Static generation does not prove Excel recalculation or refresh.
- Use `excel-deliverable-publisher` for final pure-value cleanup after report construction.

## References

- Read `references/report-surface-standards.md` when building or reviewing a client-facing workbook layout.
