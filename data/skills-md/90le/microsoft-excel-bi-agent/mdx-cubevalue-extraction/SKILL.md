---
name: mdx-cubevalue-extraction
description: Use when Excel work involves CUBEVALUE, CUBEMEMBER, CUBESET, MDX measures, dimensions, hierarchies, members, ThisWorkbookDataModel, or report-cell extraction.
---

# MDX CUBEVALUE Extraction

## Core Rule

Treat Excel CUBE formulas as the report layer over a model. Confirm the measure and member paths before changing formulas.

## Workflow

1. Identify connection name, usually `ThisWorkbookDataModel`.
2. Run `tools/inspect_excel_bi_workbook.py <workbook> --markdown` from the plugin root when a workbook file is available.
3. If the workbook uses Power Pivot/Data Model measures, generate a model report with `tools/build_excel_bi_model_report.py` or `tools/invoke_excel_bi_com.sh model-report` on Windows Git Bash.
4. Generate a CUBE dependency report with `tools/build_cube_dependency_report.py` when formulas must be traced by sheet, cell, measure, member, or helper cell.
5. Run `tools/analyze_measure_rename_impact.py` before renaming or deleting model measures used by report-layer CUBE formulas.
6. Run `tools/build_measure_rename_rewrite_plan.py` when a measure rename needs a reviewable list of report-layer `[Measures].[...]` replacements; for measure deletion, block direct and downstream helper-cell references for manual review.
7. Use `tools/create_cube_formula_fixture.py` only for parser/report smoke tests when no safe workbook fixture is available; it does not contain a live model.
8. When a real ADOMD/MSOLAP endpoint connection string is available, use `tools/test_excel_adomd_query.ps1` to validate MDX query behavior outside the worksheet formula layer.
9. Identify measure, dimension, hierarchy, and member references.
10. Determine whether formulas should use direct MDX strings or helper `CUBEMEMBER` cells.
11. Build formulas from stable cell references where the report is parameterized.
12. Validate returned values, `#N/A`, and `#GETTING_DATA` behavior in Excel.

## Reference Selection

Read:

- `references/cube-formulas.md` for formula templates.
- `references/cube-dependency-report.md` for report-layer dependency tracing and diagnostic flags.
- `references/mdx-member-paths.md` for member path patterns.
- `references/official-links.md` for Microsoft references.

## Common Issues

- Wrong hierarchy or member unique name.
- Measure exists in DAX but is referenced with the wrong MDX measure path.
- Report formula references stale helper cells.
- Data Model not refreshed.
- `#GETTING_DATA` persists because the model/query has not completed.

## Cross-Platform Boundary

CUBE formulas can be generated anywhere. Actual evaluation against `ThisWorkbookDataModel` requires Excel.

## Scripts

- `tools/inspect_excel_bi_workbook.py <workbook> [--markdown] [--out-json <path>]`
  scans OpenXML workbook structure for CUBE formulas, workbook connections, pivot caches, tables, VBA parts, Power Pivot-like parts, and Power Query-like parts. Use this before changing report formulas.
- `tools/build_excel_bi_model_report.py --model-json <path> [--openxml-json <path>] [--out-md <path>] [--out-json <path>]`
  maps scanned CUBE formula measure references back to exported Data Model measures and flags missing or unused references.
- `tools/build_cube_dependency_report.py --openxml-json <path> [--model-json <path>] [--out-md <path>] [--out-json <path>] [--out-mermaid <path>]`
  builds a report-layer dependency graph by sheet, cell, measure, member reference, and helper cell reference. Measure/member parsing supports MDX escaped closing brackets such as `]]` inside bracket identifiers.
- `tools/analyze_measure_rename_impact.py --model-json <path> --openxml-json <path> --rename "Old=New" [--delete <measure>] [--out-json <path>] [--out-md <path>]`
  reports which report-layer CUBE formulas and DAX measures reference a measure planned for rename or deletion, including escaped MDX measure names.
- `tools/build_measure_rename_rewrite_plan.py --model-json <path> --openxml-json <path> --rename "Old=New" [--delete <measure>] [--out-json <path>] [--out-md <path>] [--fail-on-manual-review]`
  builds a reviewable formula replacement plan for DAX dependencies and report-layer CUBE formulas, including escaped MDX measure identifiers. It keeps dynamic period/member helper references visible and marks CUBE formulas that depend on rewritten measure helper cells. It does not edit the workbook or evaluate formulas. Delete operations are manual-review only, including formulas that depend on a deleted-measure helper cell.
- `tools/create_cube_formula_fixture.py --workbook <path> [--model-json <path>]`
  creates a generic `.xlsx` containing structural `CUBEMEMBER` and `CUBEVALUE` formulas plus an optional known-measure JSON file for dependency-report smoke tests. This validates parsing and diagnostics only, not Excel calculation.
- `tools/test_excel_adomd_query.ps1 [-ProbeOnly] [-ConnectionString <text>] [-Mdx <text>|-MdxPath <path>] [-OutJson <path>]`
  validates ADOMD COM activation or runs an explicit endpoint MDX query. This is for MSOLAP/ADOMD endpoints, not for directly evaluating in-workbook `CUBEVALUE` formulas.
- `tools/invoke_excel_bi_com.sh model-report -w <workbook> [--include-columns] [--out-md <path>] [--out-json <path>]`
  runs the Windows Excel COM Data Model export plus CUBE formula scan from Git Bash/MSYS/Cygwin.
- `tools/invoke_excel_bi_com.sh cube-report -w <workbook> [--include-model] [--out-md <path>] [--out-json <path>] [--out-mermaid <path>]`
  runs OpenXML CUBE scanning plus optional Data Model measure export from Windows Git Bash/MSYS/Cygwin.
- `tools/invoke_excel_bi_com.sh adomd-query [--probe-only] [--connection-string <text>] [--mdx <text>|--mdx-file <path>] [--out-json <path>]`
  runs ADOMD probing or endpoint query validation from Windows Git Bash/MSYS/Cygwin.
