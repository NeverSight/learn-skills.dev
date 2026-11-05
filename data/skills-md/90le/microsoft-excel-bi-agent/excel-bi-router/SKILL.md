---
name: excel-bi-router
description: Use when an Excel BI request is broad, mixed, or unclear and must be routed among workbook, VBA, Power Query, DAX, MDX/CUBE, ADO/SQL, reporting, QA, delivery, or environment skills.
---

# Excel BI Router

## Purpose

Use this skill first for ambiguous or mixed Excel BI work. Identify the actual layer before editing files or writing code.

## Route By User Signal

| User signal | Use skill |
|---|---|
| `.xlsx`, `.xlsm`, buttons, macros, sheet formatting, hidden sheets, or implementation against an already-confirmed Excel runtime | `excel-vba-workbook-engineering` |
| Power Query, M, query editor, refresh error, `Table.*`, `Excel.Workbook`, folder combine | `power-query-m-engineering` |
| Power Pivot, Data Model, relationships, DAX, measure, `CALCULATE`, filter context | `power-pivot-dax-modeling` |
| `CUBEVALUE`, `CUBEMEMBER`, `ThisWorkbookDataModel`, MDX member, cube formula | `mdx-cubevalue-extraction` |
| ADO, OLEDB, ADOMD, SQL in VBA, connection string, query workbook table/model | `excel-ado-sql-data-access` |
| Publish, clean copy, pure `.xlsx`, values-only, remove formulas/links/queries/model, delete config sheets | `excel-deliverable-publisher` |
| QA, audit, review, delivery readiness, workbook risks, formula quality, hidden/process sheets | `excel-workbook-qa-auditor` |
| Compatibility, supported platform/version, Windows/Linux/macOS/web, Excel COM availability, Office environment, bitness, provider drift, or Trust Center | `office-environment-diagnostics` |
| Report workbook, dashboard, layout, chart, pivot, client-facing sheet, polished output | `excel-report-builder` |
| Power BI, PBIX, semantic model, TMDL, XMLA, Fabric, calculation groups, DAX portability | `power-bi-semantic-model` |
| Fixture, smoke test, regression, sanitized workbook, sample workbook, forward-test prompts | `excel-testing-fixtures` |

## Scripted Routing

Use `scripts/route_excel_bi_task.py --text "<task>" [--out-json <path>] [--out-md <path>]` when the first step should be machine-readable or reviewed by another agent. The script emits the selected layer, skill, matched keywords, validation boundary, and recommended package scripts. Treat it as a first-pass routing aid, not as proof of workbook behavior.

## Compatibility First

Route platform, Office-version, offline, Excel COM, Linux, macOS, or web compatibility questions to `office-environment-diagnostics` before choosing an implementation skill. Keep the execution environment—the machine running the agent and probe—separate from the target environment where the workbook must be authored, automated, consumed, or delivered.

Use three evidence levels:

- **Structural evidence**: package, OpenXML, formulas, and source inspection without claiming Excel runtime behavior.
- **Runtime capability evidence**: local Office, COM, provider, and generated-fixture smoke results.
- **Workbook behavior evidence**: task-specific refresh, calculation, macro, model, endpoint, or rendered-output proof from the target workbook and host.

DAX or Power Pivot compatibility remains a `power-pivot-dax-modeling` task when the question concerns formula/function support rather than host availability.

## Mixed Task Order

1. Use `office-environment-diagnostics` first when the task is blocked by local Excel, provider, or COM readiness.
2. Inspect workbook shape with `excel-vba-workbook-engineering` or audit it with `excel-workbook-qa-auditor` when the request is review-first.
3. If data transformation is involved, inspect Power Query with `power-query-m-engineering`.
4. If Data Model calculations are involved, inspect DAX with `power-pivot-dax-modeling`.
5. If Excel formulas pull model values, inspect CUBE/MDX with `mdx-cubevalue-extraction`.
6. If VBA queries data sources directly, inspect ADO/SQL with `excel-ado-sql-data-access`.
7. Use `excel-report-builder` when the primary deliverable is a readable workbook/report surface.
8. Use `excel-deliverable-publisher` only after required refresh/calculation/report validation is complete.
9. Use `excel-testing-fixtures` when the task needs safe regression evidence without customer files.

## Boundary Rules

- Do not solve DAX problems with M patterns.
- Do not solve Power Query refresh problems by changing CUBE formulas unless the error is at the report layer.
- Do not claim Linux/macOS can validate Excel VBA, Power Query refresh, Power Pivot, or Solver without desktop Excel.
- When the user says "Excel formula taking data from Power Pivot", check CUBE/MDX before DAX.
- When the user says "VBA SQL from Power Pivot", check ADO/ADOMD and workbook connections before writing SQL.
- When the user asks for a client-ready file, separate report construction from final publish cleanup.
- When the user asks about Power BI semantic models, do not assume Excel Power Pivot function support is identical.

## Output

After routing, state:

```text
Layer: <Workbook/VBA | Power Query M | DAX | MDX/CUBE | ADO/SQL | Mixed>
Skill: <skill-name>
Why: <short reason>
Validation needed: <platform/tool>
```
