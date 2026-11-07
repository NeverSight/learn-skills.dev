---
name: microsoft-excel
description: "Automate Excel workbooks with Office Scripts, Power Query, VBA, and dynamic arrays while checking data consistency."
category: office
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["excel", "office-scripts", "power-query", "m-language", "xlsx", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Microsoft Excel Automation AI Skill Guide (Claude)

## Overview & Engine Architecture
Microsoft Excel combines a grid calculation engine with **tables**, **Power Query (M)**, **PivotCaches**, **dynamic array formulas**, and automation via **Office Scripts** (Excel on the web / desktop with Automate) and legacy **VBA**. Claude operates as a Principal Spreadsheet Systems Analyst, specializing in **Table-first models**, **Power Query transforms**, **Office Scripts TypeScript**, and **reproducible refresh pipelines**.

### Excel Workbook & Automation Stack

```
┌─────────────────────────────────────────────────────────────┐
│                 Excel Architecture                          │
│                                                             │
│  Calculation & Structure                                    │
│  ├── Workbooks / Worksheets / Ranges / Tables (ListObjects) │
│  ├── Formulas / Dynamic arrays / LAMBDA                     │
│  └── PivotTables / Charts / Data Model (Power Pivot)        │
│                                                             │
│  ETL & Automation                                           │
│  ├── Power Query (M) + refresh                              │
│  ├── Office Scripts (TypeScript)                            │
│  └── VBA / Office JS add-ins                                │
│                                                             │
│  Distribution                                               │
│  ├── xlsx / xlsm / csv                                      │
│  ├── SharePoint / OneDrive refresh                          │
│  └── Power Automate connectors                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Tables Over Naked Ranges**: Convert ranges to Tables for stable structured references.
2. **Power Query for ETL**: Prefer M transforms over fragile copy-paste macros for recurring imports.
3. **Office Scripts for Cloud Automation**: Author TypeScript scripts that work with Automate flows.
4. **No Magic Numbers**: Document units, as-of dates, and assumptions in a `README` sheet.
5. **Volatile Functions**: Minimize `INDIRECT`/`OFFSET` in large models; prefer structured refs.

---

## Production Office Script + Power Query M

Office Script (`Automate` → New Script):

```typescript
// ==============================================================================
// Office Scripts: normalize a "Raw" sheet into an Excel Table and flag blanks
// ==============================================================================
function main(workbook: ExcelScript.Workbook) {
  const sheet = workbook.getWorksheet("Raw");
  if (!sheet) throw new Error('Missing sheet "Raw"');

  const used = sheet.getUsedRange();
  if (!used) throw new Error("Raw sheet is empty");

  const tables = sheet.getTables();
  for (const t of tables) t.delete();

  const table = sheet.addTable(used.getAddress(), true);
  table.setName("RawData");

  const cols = table.getColumns();
  const statusCol = cols[cols.length - 1];
  // Ensure a Status column exists as last column header named Status
  const header = statusCol.getName();
  if (header.toLowerCase() !== "status") {
    table.addColumn(null, null, "Status");
  }

  const rows = table.getRangeBetweenHeaderAndTotal().getRowCount();
  const values = table.getRangeBetweenHeaderAndTotal().getValues();
  for (let r = 0; r < rows; r++) {
    const row = values[r];
    const blank = row.some((c) => c === "" || c === null);
    // Status is last column
    values[r][row.length - 1] = blank ? "NEEDS_REVIEW" : "OK";
  }
  table.getRangeBetweenHeaderAndTotal().setValues(values);
}
```

Power Query M snippet (transform CSV):

```powerquery
let
  Source = Csv.Document(File.Contents("C:\data\sales.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
  Promote = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
  Types = Table.TransformColumnTypes(Promote, {{"Amount", type number}, {"Date", type date}}),
  Filter = Table.SelectRows(Types, each [Amount] <> null and [Amount] > 0)
in
  Filter
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **Office Script can't find table** | Name/sheet mismatch. | List sheets/tables; create Table first. |
| **Power Query refresh fails path** | Local path unavailable on another machine. | Use SharePoint/OneDrive connectors or parameters. |
| **#SPILL! errors** | Blocked spill range. | Clear obstructing cells; use dynamic array-aware layouts. |
| **VBA macros blocked** | Trust Center / xlsm policy. | Prefer Office Scripts when policy blocks VBA. |

---

## Best Practices

1. One fact table + dimension sheets; avoid circular cross-sheet spaghetti.
2. Parameterize file paths in Power Query.
3. Keep raw dumps immutable; transform into clean tables.

### Essential Entry Points
- **Automate** gallery (Office Scripts)
- **Data → Get Data** (Power Query)
- **Formulas → Name Manager**

---

## Agent Operational Directive
> **MANDATORY**: Prefer Tables + Power Query for recurring data shaping. Use Office Scripts for cloud-safe automation. Document assumptions on a dedicated sheet and never overwrite raw source tabs in place.
