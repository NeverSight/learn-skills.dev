---
name: excel-deliverable-publisher
description: Use when preparing or auditing client-ready .xlsx/.xlsm copies that must remove external links, queries, Data Model, VBA, hidden process sheets, or other non-client artifacts without altering the source.
---

# Excel Deliverable Publisher

## Core Rule

Treat publishing as a non-destructive release step. Work from a copied workbook, keep the source workbook intact, create a cleanup plan before editing, and verify the final copy after cleanup.

## Workflow

1. **Inventory the source**
   - Inspect the workbook with `tools/inspect_excel_bi_workbook.py`.
   - Build an external dependency report with `tools/build_external_dependency_report.py`.
   - If the workbook may include formulas, controls, Power Query, CUBE formulas, or VBA buttons, also build the relevant specialist reports before cleanup.

2. **Plan the delivery shape**
   - Use `tools/build_pure_deliverable_cleanup_plan.py` to define the copy, refresh, value-freeze, connection/link removal, sheet removal, and post-clean audit steps.
   - Do not delete working sheets, queries, macros, or model parts from the source workbook.
   - Decide whether the target is pure `.xlsx`, macro-enabled `.xlsm`, or an internal review copy.

3. **Publish the copy**
   - On Windows desktop Excel, use Excel COM when formulas, Power Query refresh, Data Model, CUBE formulas, buttons, charts, or VBA behavior must be evaluated before freezing.
   - On Linux/macOS, limit work to structural OpenXML-safe transformations unless the user accepts that Excel runtime behavior is not verified.
   - Convert formulas to values only after required refresh/calculation completes.
   - Remove or hide config/process sheets only in the delivery copy.

4. **Verify the output**
   - Re-run inspection and external dependency reporting on the cleaned workbook.
   - Use `tools/build_pure_deliverable_verification_report.py` with `--fail-on-fail` when the deliverable must contain no links, queries, model markers, or formulas.
   - Record known accepted remnants, such as intentional macros in an `.xlsm`, as explicit delivery boundaries.

## Required Evidence

- Source path and output path.
- Cleanup plan.
- Post-clean dependency report.
- Verification report.
- Statement of what was intentionally preserved, if anything.

## References

- Read `references/delivery-checklist.md` when deciding whether a workbook is a pure `.xlsx`, live `.xlsm`, or internal review copy, and when writing the final publish note.

## Boundaries

- OpenXML inspection proves workbook structure, not live formula results.
- Removing Power Query or Data Model dependencies from a copy does not prove that upstream data is correct.
- Do not ship customer-specific intermediate reports inside this plugin package.
