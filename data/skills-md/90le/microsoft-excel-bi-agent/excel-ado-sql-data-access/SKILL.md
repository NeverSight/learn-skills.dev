---
name: excel-ado-sql-data-access
description: Use when Excel work needs ADO, ADODB, OLEDB, ADOMD, SQL, connection strings, parameters, recordsets, or queries against workbooks, CSV, Access, or Data Model sources.
---

# Excel ADO SQL Data Access

## Core Rule

Treat VBA SQL as data-access infrastructure. Confirm provider, connection target, query dialect, and result shape before writing code.

## Workflow

1. Identify source: worksheet table, workbook file, Access, CSV, external database, Data Model/cube.
2. Run `tools/inspect_excel_bi_workbook.py <workbook> --markdown` from the plugin root when an Excel workbook is the source or target.
3. Choose provider: ACE OLEDB for workbook-like files, ADODB for tabular sources, ADOMD for multidimensional/model queries.
4. If provider availability is uncertain, run `tools/probe_excel_bi_providers.ps1` first to detect ACE, MSOLAP, ADOMD, Excel COM, and process bitness; the full release gate also runs this probe with Excel COM and ADO workbook smoke enabled.
5. For Excel workbook SQL, run `tools/test_excel_ado_sql_access.ps1` to validate provider, schema, SQL, row count, and cleanup before writing VBA.
6. For multidimensional/model endpoints, first use `tools/test_excel_adomd_query.ps1 -ProbeOnly` to confirm ADODB/ADOMD COM activation; with an explicit connection string, run the same script to validate connection, MDX, and cellset shape.
7. Write connection string with explicit path and extended properties.
8. Use parameterized queries where supported; otherwise sanitize inputs carefully.
9. Load recordsets into arrays or worksheet ranges.
10. Close and release connection/recordset objects.

## Reference Selection

Read:

- `references/data-access-workflow.md` for source selection, smoke tests, and validation boundaries.
- `references/ado-patterns.md` for VBA ADO examples.
- `references/connection-strings.md` for provider templates.
- `references/official-links.md` for Microsoft references.

## Validation

- Test connection opens.
- Test SQL returns expected row/column count.
- Test empty result handling.
- Test file path with spaces and non-ASCII characters.
- Test cleanup closes files and connections.

## Boundary

Power Query is not a SQL database. Query Power Query output only after it is loaded to a sheet, table, connection, or Data Model.

## Scripts

- `tools/inspect_excel_bi_workbook.py <workbook> [--markdown] [--out-json <path>]`
  scans workbook connections, tables, pivot caches, formulas, VBA parts, and model/query-like parts so the data-access target can be chosen before writing ADO code.
- `tools/probe_excel_bi_providers.ps1 [-RunExcelComSmoke] [-RunAdoWorkbookSmoke] [-OutJson <path>]`
  detects registered provider ProgIDs, creatable COM ProgIDs, .NET ADOMD assembly availability, optional Excel COM smoke status, and optional ACE workbook SQL smoke status. The full release gate uses this script with both smoke switches to validate the local Windows provider baseline when available; structural profile skips it.
- `tools/test_excel_ado_sql_access.ps1 -WorkbookPath <path> [-CreateFixture] -SqlText <sql> [-IncludeSchema] [-OutJson <path>]`
  creates a known Excel fixture when requested, opens an ADODB connection through ACE OLEDB, runs workbook SQL, and emits JSON with fields, rows, schema, timing, and provider errors. The full release gate uses this script with a generic fixture to verify provider/runtime behavior; structural profile skips it for non-Excel environments.
- `tools/test_excel_adomd_query.ps1 [-ProbeOnly] [-ConnectionString <text>] [-Mdx <text>|-MdxPath <path>] [-OutJson <path>]`
  probes ADOMD COM activation or runs an explicit ADOMD/MSOLAP endpoint MDX query and emits axes, cells, truncation, and redacted connection-string metadata. The full release gate uses `-ProbeOnly` to validate local COM runtime availability without claiming that any specific cube endpoint has been queried.
- `tools/invoke_excel_bi_com.sh provider-probe [--excel-com] [--ado-workbook-smoke] [--out-json <path>]`
  runs the provider probe from Windows Git Bash/MSYS/Cygwin.
- `tools/invoke_excel_bi_com.sh ado-query -w <workbook> --sql <sql> [--create-fixture] [--include-schema] [--out-json <path>]`
  runs the ADO workbook SQL smoke tool from Windows Git Bash/MSYS/Cygwin.
- `tools/invoke_excel_bi_com.sh adomd-query [--probe-only] [--connection-string <text>] [--mdx <text>|--mdx-file <path>] [--out-json <path>]`
  runs ADOMD probing or endpoint query validation from Windows Git Bash/MSYS/Cygwin.
