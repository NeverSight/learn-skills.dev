---
name: power-query-m-engineering
description: Use when creating, debugging, or optimizing Power Query M in Excel or Power BI, including Excel.Workbook, Csv.Document, folders, joins, grouping, expansion, types, dependencies, refresh errors, or performance.
---

# Power Query M Engineering

## Core Rule

Treat Power Query M as an ETL graph. Inspect sources, query dependencies, row counts, types, and join cardinality before editing formulas.

## Workflow

1. Identify whether the query runs in Excel Power Query or Power BI.
2. Extract or inspect the M code from workbook queries when possible.
3. Map inputs, parameters, intermediate tables, and outputs.
4. Check row count risks before joins, expands, groups, and combines.
5. Edit M with clear step names and stable types.
6. Run the M source lint before importing changed query text into a workbook copy.
7. Validate refresh behavior, row counts, key columns, ordering, and final schema.
8. If refresh fails, classify the refresh JSON or copied error text before rewriting M.

## High-Risk Areas

- `Table.NestedJoin` followed by expand can multiply rows when lookup keys are duplicated.
- `Table.Group` can change row order unless an order column is preserved.
- `Table.PromoteHeaders` can corrupt files with extra title rows or inconsistent headers.
- `Changed Type` steps can break when source columns are missing or localized.
- Folder combine logic often fails on hidden `~$` files or mixed `.xls/.xlsx/.csv`.
- Dynamic columns require explicit missing-field handling.

## Reference Selection

Read:

- `references/m-patterns.md` for common M transformation patterns.
- `references/m-style-guide.md` before writing or rewriting substantial M queries.
- `references/m-lifecycle-vba.md` when using VBA/COM to add, edit, delete, refresh, wait for completion, or benchmark Power Query.
- `references/m-troubleshooting.md` for refresh and formula errors.
- `references/m-validation.md` when validating row counts, schema, joins, and refresh behavior.
- `references/official-docs-kb.md` and `references/official-links.md` when exact function semantics, host behavior, or customer-facing citations are needed.

## Scripts

- `scripts/export_power_queries_excel_com.ps1 -WorkbookPath <path> -OutDir <folder>`
  exports workbook Power Query formulas through Windows Excel COM. Use this when exact M source is needed from an `.xlsx` or `.xlsm`.
- `scripts/manage_power_queries_excel_com.ps1 -WorkbookPath <path> -Action List|Add|Update|Delete ...`
  lists, inserts, updates, or deletes workbook queries through Excel COM. Add/update/delete require an output copy unless `-InPlace` is explicitly supplied.
- `scripts/refresh_power_queries_excel_com.ps1 -WorkbookPath <path> [-QueryName <name>] [-OutputWorkbookPath <path>]`
  refreshes all queries or one query, waits for async completion, records timings, captures errors, and optionally saves a refreshed copy.
- `scripts/build_power_query_refresh_report.py <refresh-json> [--max-elapsed-seconds <n>] [--require-completed] [--out-json <path>] [--out-md <path>]`
  summarizes refresh completion, elapsed time, still-refreshing connections, background-refresh settings, and captured errors from refresh JSON. Use it after a refresh and before dependent VBA/report steps continue.
- `scripts/classify_power_query_refresh_errors.py <refresh-json-or-error-text> [--out-json <path>] [--out-md <path>]`
  classifies refresh errors into diagnostic buckets such as credentials, privacy firewall, missing source, missing columns, type conversion, syntax, provider/driver, timeout, and row-cardinality risks. Use it after refresh failures and before changing M code.
- `scripts/create_power_query_fixture_excel_com.ps1 -OutputWorkbookPath <path>`
  creates a small workbook with a Power Query formula loaded to a worksheet table, then refreshes synchronously. Use this to smoke-test query creation, load-to-sheet, and refresh behavior on Windows desktop Excel.
- `scripts/invoke_power_query_excel_com.sh export|manage|refresh|fixture ...`
  runs the Excel COM scripts from Windows Git Bash/MSYS/Cygwin.
- `scripts/inspect_power_query_openxml.py <workbook> [--out-json <path>]`
  performs cross-platform OpenXML inspection for connections, query tables, external links, and mashup-like package parts. It does not compile, refresh, or fully decode Excel's mashup binary.
- `scripts/search_power_query_official_kb.py <keyword> [--json]`
  searches the local official-documentation index and returns Microsoft Learn URLs plus online search queries for Power Query M, Excel-hosted refresh, and diagnostics topics.
- `scripts/lint_power_query_m.py <source> [--warnings-as-errors] [--out-json <path>]`
  statically checks `.m`, `.pq`, text, Markdown, or JSON-exported query source for query-shape issues, risky `Folder.Files` ingestion, join cardinality risk, order restoration gaps, hard-coded expand columns, and unguarded `List.Max` usage. Use it before add/update/import operations.
- Package root `tools/build_power_query_lineage_report.py <query-dir> [--out-json <path>] [--out-md <path>] [--fail-on-high-risk]`
  builds a static query dependency and source-risk report from exported `.m`/`.pq` files. Use it after exporting queries and before large rewrites or delivery reviews to flag query cycles, hard-coded local paths, web/database/cloud-service sources, native SQL pass-through via `Value.NativeQuery`, credential-like literals or authorization keys, and mixed-source lineage that can trigger privacy or credential problems. It distinguishes workbook-table/config sources such as `Excel.CurrentWorkbook` so parameterized folder paths are visible without being treated as mixed-source privacy risk by themselves, and it recognizes common enterprise connectors such as OData, Azure Storage, Power Platform Dataflows, Dataverse, and additional database connectors. Credential-like evidence is redacted to indicators and counts; do not rely on this static check as a full secret scanner.

## Validation

Minimum checks:

- Input file count and filtered file list.
- Query lineage and source-risk report reviewed when the workbook has multiple Power Query queries or external sources.
- M source lint passed before changed formulas were imported.
- Row counts before and after joins/expands/groups.
- Final columns and data types.
- No unexpected duplicated rows.
- Stable row order if the output is report-facing.
- Excel refresh tested when a workbook deliverable depends on refresh.
- Refresh timing/status report reviewed before downstream automation continues.
- Refresh failures classified and summarized when refresh did not complete.
- For package maintenance, the full release gate creates a loaded Power Query workbook, updates its M formula, refreshes and waits through Excel COM, saves a refreshed copy, exports the query, and verifies the worksheet table result. The structural release gate intentionally skips this Excel runtime fixture.

## Cross-Platform Boundary

M code can be generated and reviewed anywhere. Exact query CRUD, refresh, load-to-sheet/model behavior, popup errors, credential prompts, and completion waiting must be tested in desktop Excel or Power BI.
