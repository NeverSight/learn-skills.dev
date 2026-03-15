---
name: csv-tools
description: "Parse, query, filter, sort, transform, and summarize CSV and JSON data files. Use this skill when the user asks to view a CSV, filter data, get statistics from a data file, convert CSV to JSON or vice versa, sort data, or analyze tabular data."
tags: [csv, json, data, filter, sort, statistics, transform, utility]
version: 0.1.0
---

# Skill: csv-tools

## When to Use

Use this skill when the user asks to:

- View or pretty-print a CSV/JSON file
- Filter rows from a data file
- Sort data by a column
- Get summary statistics (count, mean, min, max)
- Convert CSV to JSON or JSON to CSV
- Query or analyze tabular data
- Count rows or summarize a dataset

## Input Parameters

| Parameter   | Required        | Description                                                          | Example   |
| ----------- | --------------- | -------------------------------------------------------------------- | --------- |
| `action`    | Yes             | `view`, `filter`, `sort`, `stats`, `convert`                         | view      |
| `file_path` | Yes             | Path to the CSV or JSON file                                         | data.csv  |
| `column`    | For filter/sort | Column name to operate on                                            | age       |
| `value`     | For filter      | Value to match (supports operators: `>`, `<`, `>=`, `<=`, `!=`, `=`) | >30       |
| `order`     | For sort        | `asc` (default) or `desc`                                            | desc      |
| `output`    | For convert     | Output file path                                                     | data.json |
| `limit`     | For view        | Max rows to display (default: 50)                                    | 20        |

## Procedure

1. Determine the action from the user's request
2. Run the bundled script:

   ```bash
   # View first 50 rows
   python3 skills/csv-tools/scripts/query.py view data.csv

   # Filter rows
   python3 skills/csv-tools/scripts/query.py filter data.csv --column age --value ">30"

   # Sort by column
   python3 skills/csv-tools/scripts/query.py sort data.csv --column name --order asc

   # Summary statistics
   python3 skills/csv-tools/scripts/query.py stats data.csv

   # Convert CSV to JSON
   python3 skills/csv-tools/scripts/query.py convert data.csv --output data.json
   ```

3. Report the result to the user

## Bundled Scripts

| Script             | Type   | Description                                      |
| ------------------ | ------ | ------------------------------------------------ |
| `scripts/query.py` | Python | Query, filter, sort, and transform CSV/JSON data |

### Script Usage

```bash
# View data (pretty-printed table)
python3 scripts/query.py view data.csv
python3 scripts/query.py view data.csv --limit 10

# Filter rows
python3 scripts/query.py filter data.csv --column status --value "active"
python3 scripts/query.py filter data.csv --column price --value ">100"
python3 scripts/query.py filter data.csv --column name --value "!=John"

# Sort
python3 scripts/query.py sort data.csv --column date --order desc

# Statistics
python3 scripts/query.py stats data.csv
python3 scripts/query.py stats data.csv --column revenue

# Convert formats
python3 scripts/query.py convert data.csv --output data.json
python3 scripts/query.py convert data.json --output data.csv
```

## Example

```
show me the contents of sales.csv
filter users.csv where age is greater than 30
sort the data by revenue descending
what are the statistics for this CSV file
convert this CSV to JSON
how many rows are in data.csv
```
