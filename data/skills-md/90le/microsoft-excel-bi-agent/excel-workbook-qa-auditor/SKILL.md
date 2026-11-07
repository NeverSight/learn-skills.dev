---
name: excel-workbook-qa-auditor
description: Use when auditing an Excel workbook's formulas, controls, hidden sheets, protection, links, Power Query, Data Model, CUBE formulas, VBA buttons, visual quality, or delivery readiness.
---

# Excel Workbook QA Auditor

## Core Rule

Review the workbook as a layered artifact. Start with structural inventory, add specialist reports only for surfaces that exist, then separate true blockers from accepted workbook design choices.

## Workflow

1. **Create the baseline inventory**
   - Run `tools/inspect_excel_bi_workbook.py` for OpenXML structure.
   - Use Windows Excel COM only when the audit requires live VBA, refresh, calculation, Data Model, or button behavior.

2. **Add targeted reports**
   - Formula quality: `tools/build_formula_quality_report.py`.
   - Workbook controls and visibility: `tools/build_workbook_controls_report.py`.
   - External dependency readiness: `tools/build_external_dependency_report.py`.
   - Workbook triage: `tools/build_workbook_triage_report.py`.
   - CUBE formulas: `tools/build_cube_dependency_report.py`.
   - Power Query lineage: `tools/build_power_query_lineage_report.py`.
   - Data Model report: `tools/build_excel_bi_model_report.py`.
   - VBA button bindings: `tools/build_vba_button_binding_report.py`.

3. **Classify findings**
   - High: broken formulas, unresolved button macros, leaked external links, unexpected credentials, missing model measures, failed refresh, or delivery-cleanup failures.
   - Medium: volatile formulas, dynamic references, hidden or protected sheets that need owner confirmation, hard-coded local paths, mixed-source query lineage, stale helper-cell dependencies.
   - Low: naming/style/documentation issues that do not affect calculation or delivery.

4. **Report QA output**
   - Lead with findings and file/sheet/cell references where available.
   - State which checks are static and which require Excel runtime proof.
   - Recommend the next validation command for every unresolved high-risk item.

## Boundaries

- Do not conclude that workbook values are correct from static reports alone.
- Do not change formulas, sheets, queries, or VBA in an audit-only request.
- Keep generated QA reports outside this plugin package unless they are generic fixtures.

## References

- Read `references/qa-severity-rubric.md` when writing a client-facing or developer-facing QA finding list.
