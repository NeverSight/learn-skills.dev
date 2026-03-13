---
name: excel-inspector
description: Inspect Excel file structure (sheets, data types, VBA code) to help AI understand the workbook before writing code. Use when you need to understand an Excel file's schema, analyze data structure, or extract VBA code for modification.
---

# Excel Inspector Skill

> Automated Excel file structure analysis for AI code generation

## Overview

This skill analyzes Excel files and outputs structured metadata (JSON) to help AI understand:
- Sheet structure and table definitions
- Column names and data types
- VBA code modules
- Sample data and statistics

## When to Use

- **Before writing VBA code**: understand existing modules and procedures
- **Before Python Excel automation**: know sheet/column structure and data types
- **When analyzing Excel file structure**: get complete metadata in JSON format
- **When modifying existing Excel macros**: extract current VBA code to a file
- **When debugging Excel data issues**: analyze data types and sample values

## Usage

```bash
# Analyze an Excel file
conda run -n excel python script/inspect_excel.py path/to/file.xlsm

# Example
conda run -n excel python script/inspect_excel.py perturb_inform.xlsm
```

## Output

1. **JSON file**: `{filename}_structure.json` in current directory
   - Complete metadata: sheets, columns, data types, VBA modules
   - Used by AI to understand file structure before coding

2. **Console output**: Summary report for quick reference
   - Number of sheets, tables, VBA modules
   - Analysis status and any warnings

3. **VBA files**: Extracted to `.claude/vba/{filename}/` directory
   - Individual module files: `ThisWorkbook.vba`, `Module1.vba`, etc.
   - Enables version control and easy modification

## JSON Output Schema

```json
{
  "file_path": "/absolute/path/to/file.xlsm",
  "file_info": {
    "name": "perturb_inform.xlsm",
    "size_kb": 170,
    "is_macro_enabled": true,
    "last_modified": "2025-12-10T12:34:56"
  },
  "sheets": [
    {
      "name": "platform",
      "dimensions": "A1:K951",
      "row_count": 951,
      "col_count": 11,
      "tables": [
        {
          "name": "tbl_in",
          "range": "A1:I951",
          "row_count": 951,
          "col_count": 9
        }
      ],
      "head_data": [
        ["subject", "trial", "condition", ...],
        ["김연옥", 1, "baseline", ...],
        ...
      ],
      "columns": [
        {
          "index": 0,
          "header": "subject",
          "inferred_type": "string",
          "na_ratio": 0.0,
          "sample_values": ["김연옥", "김윤자", "윤순자"]
        },
        {
          "index": 1,
          "header": "trial",
          "inferred_type": "numeric",
          "na_ratio": 0.05,
          "sample_values": [1, 2, 3]
        }
      ]
    }
  ],
  "vba_modules": [
    {
      "name": "ThisWorkbook",
      "type": "workbook",
      "code_path": ".claude/vba/perturb_inform/ThisWorkbook.vba",
      "has_open_event": true,
      "has_close_event": true
    },
    {
      "name": "Module2",
      "type": "module",
      "code_path": ".claude/vba/perturb_inform/Module2.vba",
      "public_subs": ["BuildMetaSummary"],
      "private_functions": ["IsNA", "FindItemRow", "AddNumeric", "WriteNumericSummary"]
    }
  ],
  "analysis_summary": {
    "total_sheets": 5,
    "total_tables": 1,
    "total_vba_modules": 2,
    "has_macros": true,
    "primary_data_sheet": "platform"
  }
}
```

## Data Types

The skill infers the following column data types:

- **numeric**: Integer or float values
- **string**: Text values
- **date**: Date or datetime values
- **boolean**: TRUE/FALSE values
- **mixed**: Multiple types in the same column
- **empty**: All values are empty

## Files

| File | Purpose |
|------|---------|
| `inspect_excel.py` | Main CLI script entry point |
| `excel_structure_utils.py` | Sheet/data structure analysis utilities |
| `vba_extractor.py` | VBA code extraction utilities |

## Error Handling

| Scenario | Behavior |
|----------|----------|
| File not found | Clear error message and exit |
| .xlsx file (no macros) | Analyze sheets normally, skip VBA extraction |
| VBA access denied | Warn about Trust Center, continue with sheet analysis |
| MCP server unavailable | Fallback to openpyxl for sheet structure |
| Invalid Excel file | Error with detailed diagnostics |

## Requirements

- **Environment**: `excel` conda environment
- **Python packages**: xlwings, polars, openpyxl
- **OS**: Windows (for xlwings COM access to VBA)
- **Trust Center**: Allow programmatic access to VBA project (Excel > Options > Trust Center)

## Example Output

After running:
```bash
conda run -n excel python script/inspect_excel.py perturb_inform.xlsm
```

You get:
- `perturb_inform_structure.json` - Complete metadata for AI to read
- `.claude/vba/perturb_inform/` directory with extracted VBA modules
- Console summary showing analysis results

AI then reads the JSON file to understand the workbook structure before writing code.
