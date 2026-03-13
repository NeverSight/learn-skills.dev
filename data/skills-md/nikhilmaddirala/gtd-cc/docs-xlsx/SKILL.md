---
name: docs-xlsx
description: Parse Excel spreadsheets (.xlsx) into repository-friendly CSV and JSON artifacts. Use when users need to extract data, formulas, or structure from Excel files.
---

# Excel Spreadsheet Parsing

Parse Excel spreadsheets (.xlsx) into CSV files, JSON metadata, and formula artifacts using multi-method extraction.

## Usage

Run the parsing script directly:

```bash
./scripts/parse_xlsx.py <path_to_file.xlsx> <output_dir>
```

**Example:**
```bash
./scripts/parse_xlsx.py ~/data/workbook.xlsx ./parsed/
```

The script uses 4 extraction methods:
- pandas (basic) - CSV exports + schema
- pandas (detailed) - Data types + statistics
- openpyxl (structure) - Workbook structure JSON
- openpyxl (formulas) - Formula extraction

## Output Structure

```
output_dir/
├── file.xlsx/
│   ├── parsing_summary.json
│   ├── pandas_basic/
│   │   ├── Sheet1.csv
│   │   ├── Sheet2.csv
│   │   └── metadata.json
│   ├── pandas_detailed/
│   │   ├── Sheet1.csv
│   │   ├── Sheet2.csv
│   │   ├── statistics.json
│   │   └── data_types.json
│   ├── openpyxl_structure/
│   │   └── workbook.json
│   └── openpyxl_formulas/
│       └── formulas.json
```

## Script Features

- Exports each sheet as separate CSV file
- Captures data types and statistics
- Extracts formulas with cell references
- Handles multiple sheets per workbook
- Provides schema information for each sheet
