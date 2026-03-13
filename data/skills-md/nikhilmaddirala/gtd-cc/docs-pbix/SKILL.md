---
name: docs-pbix
description: Parse Power BI files (.pbix) into repository-friendly JSON and CSV artifacts. Use when users need to extract metadata, measures, or data model structure from Power BI files.
---

# Power BI File Parsing

Parse Power BI files (.pbix) into JSON metadata, DAX measures, and CSV data exports using multi-method extraction.

## Usage

Run the parsing script directly:

```bash
./scripts/parse_pbix.py <path_to_file.pbix> <output_dir>
```

**Example:**
```bash
./scripts/parse_pbix.py ~/analytics/report.pbix ./parsed/
```

The script uses 2 extraction methods:
- pbixray - Metadata, measures, relationships
- zipfile - Raw file structure (debugging)

## Output Structure

```
output_dir/
├── file.pbix/
│   ├── parsing_summary.json
│   ├── pbixray/
│   │   ├── model.json
│   │   ├── measures.json
│   │   ├── tables/
│   │   │   ├── Table1.csv
│   │   │   └── Table2.csv
│   │   └── relationships.json
│   └── zipfile/
│       └── structure.json
```

## Script Features

- Extracts semantic model structure (tables, measures, relationships)
- Exports tables as CSV files for data access
- Provides DAX expressions in readable format
- Captures data model relationships and dependencies
- Works on Linux (no Windows Power BI dependency)

## Method Selection

- **pbixray** - Primary method for metadata and model structure
- **zipfile** - Debugging fallback for raw file inspection
