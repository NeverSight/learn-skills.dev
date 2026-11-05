---
name: power-pivot-dax-modeling
description: Use when Excel Power Pivot or Data Model work involves DAX measures, calculated columns, relationships, CALCULATE, iterators, filter/row context, time intelligence, or model validation.
---

# Power Pivot DAX Modeling

## Core Rule

Treat DAX as semantic-model logic, not row-by-row spreadsheet formulas. Identify tables, relationships, filter context, and measure grain before writing or changing expressions.

## Workflow

1. Identify the model tables, relationships, and reporting grain.
2. Run `tools/inspect_excel_bi_workbook.py <workbook> --markdown` from the plugin root when a workbook file is available, to detect connections, pivot caches, CUBE formulas, and Data Model-like parts.
3. If provider availability is uncertain, run `tools/probe_excel_bi_providers.ps1 -RunExcelComSmoke` to record Excel COM, MSOLAP/ADOMD, and bitness evidence before attempting Data Model automation; the full release gate runs the provider probe with Excel COM and ADO workbook smoke enabled when Windows runtime support is available.
4. On Windows desktop Excel, run `tools/inspect_excel_data_model_com.ps1 -WorkbookPath <workbook>` when actual model tables, relationships, or measures are needed.
5. When both OpenXML and Data Model JSON are available, run `tools/build_excel_bi_model_report.py` to create a Markdown model report before changing DAX.
6. Use `tools/create_cube_formula_fixture.py` only when you need a safe structural fixture for validating the model-report pipeline; it does not contain a live Power Pivot model.
7. Determine whether the calculation should be a measure or calculated column.
8. Define the filter context expected from PivotTables, slicers, or CUBE formulas.
9. Write or revise DAX with explicit context handling.
10. Run `lint_dax_compat.py` before handing Excel-targeted DAX to a workbook when source formulas are available.
11. Run `analyze_dax_dependencies.py` when model JSON or DAX source is available, especially before renaming or deleting measures.
12. Run `tools/analyze_measure_rename_impact.py` before renaming or deleting measures when OpenXML report metadata is available.
13. Run `tools/build_measure_rename_rewrite_plan.py` when a measure rename needs an auditable list of dependent DAX and report-layer CUBE formula replacements; for deletion, require manual review for direct and downstream helper-cell references instead of proposing replacements.
14. Validate against small known totals before broad report use.

## Use Measure When

- Result changes with slicers, filters, PivotTable rows/columns, or report context.
- Calculation aggregates values.
- The expression should be reused in multiple reports.

## Use Calculated Column When

- Row-level attribute is needed for relationships, slicing, or grouping.
- The value is independent of report filter context.

## Reference Selection

Read:

- `references/dax-context.md` for context rules.
- `references/dax-patterns.md` for common measure patterns.
- `references/model-inspection.md` for Data Model export, relationship inspection, and model-report workflow.
- `references/official-links.md` for exact function semantics.

## Validation

- Check simple totals against source data.
- Test at multiple grains: grand total, category, date, and filtered subsets.
- Confirm slicer/filter behavior.
- Check blank and zero handling.
- Avoid hiding model ambiguity behind CUBE formulas; fix the measure/model first.

## Cross-Platform Boundary

DAX code can be drafted anywhere. Actual Power Pivot model validation requires Excel with the Data Model or Power BI tooling.

## Scripts

- `tools/inspect_excel_bi_workbook.py <workbook> [--markdown] [--out-json <path>]`
  scans OpenXML workbook structure for model-like parts, CUBE formulas, workbook connections, pivot caches, and report-facing formula surfaces. It does not decode the full Data Model or evaluate DAX.
- `tools/inspect_excel_data_model_com.ps1 -WorkbookPath <workbook> [-IncludeColumns] [-OutJson <path>]`
  uses Windows Excel COM to read Data Model tables, relationships, measures, and connection metadata without refreshing the workbook.
- `tools/probe_excel_bi_providers.ps1 [-RunExcelComSmoke] [-OutJson <path>]`
  records local Excel COM, MSOLAP/ADOMD provider registration, COM ProgID activation, .NET ADOMD assembly availability, 32/64-bit process facts, and optional generated-workbook ADO smoke evidence. The full release gate uses this as a Windows provider baseline check but treats missing local providers as an environment skip rather than package failure.
- `tools/build_excel_bi_model_report.py --model-json <path> [--openxml-json <path>] [--out-md <path>] [--out-json <path>]`
  combines exported Data Model metadata and workbook/CUBE formula metadata into a Markdown report and normalized summary JSON.
- `tools/create_cube_formula_fixture.py --workbook <path> [--model-json <path>]`
  creates a generic workbook with CUBE formulas and a companion structural model summary. Use it to smoke-test `build_excel_bi_model_report.py` without customer files; do not treat it as a live model validation.
- `.agents/skills/power-pivot-dax-modeling/scripts/lint_dax_compat.py <source> [--profile excel] [--warn-division] [--warnings-as-errors] [--out-json <path>]`
  statically checks `.dax`, text, Markdown, or JSON model-report DAX expressions for Excel Power Pivot compatibility risks. Under the Excel profile, `REMOVEFILTERS` is a blocking compatibility error, `SELECTEDVALUE` is a version-sensitive warning with an older-Excel rewrite suggestion, and `--warn-division` warns on `/` so ratio measures can be reviewed for `DIVIDE`.
- `.agents/skills/power-pivot-dax-modeling/scripts/analyze_dax_dependencies.py <source> [--out-json <path>] [--out-md <path>]`
  statically extracts measure-to-measure dependencies from model JSON or DAX source and reports missing measure references, direct self references, dependency cycles, and duplicate measure names. It does not evaluate DAX or validate table/column references.
- `tools/analyze_measure_rename_impact.py --model-json <path> --openxml-json <path> --rename "Old=New" [--delete <measure>] [--out-json <path>]`
  combines Data Model and OpenXML metadata to show which DAX measures and report-layer CUBE formulas reference a measure planned for rename or deletion. Report-layer MDX parsing supports escaped bracket identifiers such as `[Measures].[Revenue ]] Special]`.
- `tools/build_measure_rename_rewrite_plan.py --model-json <path> --openxml-json <path> --rename "Old=New" [--delete <measure>] [--out-json <path>] [--out-md <path>] [--fail-on-manual-review]`
  builds a reviewable static replacement plan for dependent DAX formulas and report-layer `[Measures].[...]` CUBE formulas, including MDX escaped bracket identifiers. It preserves parameter helper references, flags downstream formulas that depend on rewritten measure helper cells, and does not write workbook changes. Delete operations do not generate replacements; direct DAX/CUBE references and downstream helper-cell dependents are manual-review blockers.
- `tools/invoke_excel_bi_com.sh inspect-model -w <workbook> [--include-columns] [--out-json <path>]`
  runs the Data Model COM inspector from Windows Git Bash/MSYS/Cygwin.
- `tools/invoke_excel_bi_com.sh model-report -w <workbook> [--include-columns] [--out-md <path>] [--out-json <path>]`
  runs Data Model export, OpenXML inspection, and model-report generation from Windows Git Bash/MSYS/Cygwin.
