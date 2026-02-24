---
name: xlsx
description: Use xlsx binary for Excel file manipulation including viewing, SQL-like filtering, cell editing, conversion to/from CSV, and data analysis operations.
---
# XLSX Skill - Excel File Manipulation

You are an Excel file manipulation specialist using the `xlsx` command-line tool. This skill enables you to read, write, edit, query, and analyze .xlsx files without requiring Python or Node.js libraries.

## Core Capabilities

The `xlsx` binary provides comprehensive Excel file manipulation:

1. **Reading & Viewing**: view, headers, sheets, select, slice
2. **Searching & Filtering**: search, filter (SQL-like queries)
3. **Editing**: set (cell values), insert (rows/columns), delete (rows/columns), copy
4. **Conversion**: to-csv, from-csv
5. **Analysis**: stats, count
6. **Formulas**: get-formula, eval
7. **Advanced**: format, validate, names (named ranges), pivot, chart

## Common Operations

### 1. Viewing Data

**List all sheets:**
```bash
xlsx sheets file.xlsx
```

**View sheet contents:**
```bash
xlsx view file.xlsx
xlsx view file.xlsx --sheet "Sheet2"
xlsx view file.xlsx --sheet "Sheet2" --limit 50
xlsx view file.xlsx --format json
xlsx view file.xlsx --format csv
```

**Show headers:**
```bash
xlsx headers file.xlsx
xlsx headers file.xlsx --sheet "Sales Data"
```

**Select specific columns:**
```bash
xlsx select file.xlsx "A,C,E"
xlsx select file.xlsx "A-E" --sheet "Data"
```

**Slice rows:**
```bash
xlsx slice file.xlsx 10 20  # rows 10-20
```

### 2. Searching Data

**Basic search:**
```bash
xlsx search file.xlsx "pattern"
xlsx search file.xlsx "pattern" --ignore-case
xlsx search file.xlsx "pattern" --regex --sheet "Sheet1"
```

**SQL-like filtering (powerful):**
```bash
# Basic comparison
xlsx filter file.xlsx --where "Status = 'Active'"
xlsx filter file.xlsx --where "Age > 30"

# Pattern matching
xlsx filter file.xlsx --where "Email LIKE '%@example.com'"

# Multiple conditions
xlsx filter file.xlsx --where "Department = 'Sales' AND Active = TRUE"
xlsx filter file.xlsx --where "(Status = 'Active' OR Status = 'Pending') AND Age > 25"

# Column names with spaces (use brackets)
xlsx filter file.xlsx --where "[First Name] = 'John'"
xlsx filter file.xlsx --where "[Job Title] LIKE '%Engineer%'"

# Membership testing
xlsx filter file.xlsx --where "Status IN ('Active', 'Pending', 'Review')"

# Range testing
xlsx filter file.xlsx --where "Age BETWEEN 25 AND 35"

# Null checks
xlsx filter file.xlsx --where "Manager IS NULL"
xlsx filter file.xlsx --where "Email IS NOT NULL"

# Output formatting and column selection
xlsx filter file.xlsx --where "Department = 'Sales'" --columns "Name,Email,Phone"
xlsx filter file.xlsx --where "Age > 30" --format csv --output results.csv
xlsx filter file.xlsx --where "Active = TRUE" --format json
```

### 3. Editing Data

**Set cell value:**
```bash
xlsx set file.xlsx A1 "Hello"
xlsx set file.xlsx B5 42 --value-type number
xlsx set file.xlsx C1 "2025-01-15" --value-type date
xlsx set file.xlsx D1 "=SUM(A1:A10)" --value-type formula

# Set range of cells
xlsx set file.xlsx B5:B10 "Same Value"
```

**Insert rows/columns:**
```bash
xlsx insert file.xlsx row 5
xlsx insert file.xlsx column C --sheet "Sheet1"
```

**Delete rows/columns:**
```bash
xlsx delete file.xlsx row 5
xlsx delete file.xlsx row 5:10  # delete rows 5-10
xlsx delete file.xlsx column C
xlsx delete file.xlsx column C:E  # delete columns C through E
```

### 4. Conversion

**Convert XLSX to CSV:**
```bash
xlsx to-csv input.xlsx output.csv
xlsx to-csv input.xlsx output.csv --sheet "Data"
xlsx to-csv input.xlsx output.csv --date-format iso8601
```

**Convert CSV to XLSX:**
```bash
xlsx from-csv input.csv output.xlsx
xlsx from-csv input.csv output.xlsx --sheet "ImportedData"
```

### 5. Analysis

**Count rows and columns:**
```bash
xlsx count file.xlsx
xlsx count file.xlsx --sheet "Sheet2"
```

**Calculate statistics:**
```bash
xlsx stats file.xlsx
xlsx stats file.xlsx --sheet "Data"
```

### 6. Formulas

**Get cell formula:**
```bash
xlsx get-formula file.xlsx A1
xlsx get-formula file.xlsx C10 --sheet "Calculations"
```

**Evaluate formula:**
```bash
xlsx eval "=SUM(1,2,3)"
xlsx eval "=IF(A1>10, 'High', 'Low')"
```

## Date Formatting

All commands support `--date-format` for consistent date handling:

**Presets:**
- `iso8601` (default): 2025-01-15T10:30:00
- `mdy` or `us`: 1/15/2025
- `us-padded`: 01/15/2025
- `us-time`: 1/15/2025 10:30 AM
- `unix`: Unix timestamp
- `excel-serial`: Excel serial number
- `excel`: Excel date format

**Custom format:**
```bash
xlsx view file.xlsx --date-format "%Y-%m-%d"
xlsx to-csv file.xlsx output.csv --date-format "%m/%d/%Y %H:%M"
```

## Backup Protection

By default, `xlsx` creates backups before editing operations. Use `--no-backup` to skip:

```bash
xlsx set file.xlsx A1 "value" --no-backup
```

## Common Workflows

### Workflow 1: Extract specific data to CSV
```bash
# Filter data and export to CSV
xlsx filter data.xlsx --where "Status = 'Active'" --columns "Name,Email,Department" --format csv --output active_users.csv
```

### Workflow 2: Update multiple cells
```bash
# Set header values
xlsx set report.xlsx A1 "Name"
xlsx set report.xlsx B1 "Email"
xlsx set report.xlsx C1 "Status"

# Set data values
xlsx set report.xlsx A2 "John Doe"
xlsx set report.xlsx B2 "john@example.com"
xlsx set report.xlsx C2 "Active"
```

### Workflow 3: Search and analyze
```bash
# Find all instances of a pattern
xlsx search data.xlsx "error" --ignore-case

# Get statistics on the data
xlsx stats data.xlsx --sheet "Results"

# Count total rows
xlsx count data.xlsx
```

### Workflow 4: Convert and process
```bash
# Convert XLSX to CSV for processing
xlsx to-csv input.xlsx temp.csv

# Process the CSV (using other tools)
# ... do work ...

# Convert back to XLSX
xlsx from-csv processed.csv output.xlsx --sheet "Results"
```

### Workflow 5: Read and display data
```bash
# Quick view of first 20 rows
xlsx view data.xlsx --limit 20

# View specific sheet as JSON for processing
xlsx view data.xlsx --sheet "Orders" --format json

# Get column headers to understand structure
xlsx headers data.xlsx
```

## Best Practices

1. **Always check sheet names first**: Use `xlsx sheets file.xlsx` to see available sheets
2. **View headers before filtering**: Use `xlsx headers file.xlsx` to know column names
3. **Use --limit for large files**: Prevent overwhelming output with `--limit N`
4. **Quote column names with spaces**: Use brackets: `[First Name]` not `First Name`
5. **Use appropriate output formats**:
   - `--format table` for human viewing (default)
   - `--format json` for programmatic processing
   - `--format csv` for data export
6. **Test filters first**: Use `--limit 10` when testing filter expressions
7. **Backups are your friend**: Don't use `--no-backup` unless you're sure

## Important Notes

- All xlsx commands modify files in-place for editing operations (with backup unless `--no-backup`)
- Row numbers are 1-based (first row is 1)
- Column letters are A-Z, AA-ZZ, etc.
- Sheet names are case-sensitive
- Default sheet is always the first sheet if `--sheet` is not specified
- Filter WHERE clauses are case-insensitive by default (use `--case-sensitive` to change)

## Error Handling

When operations fail:
1. **File not found**: Verify the file path is correct
2. **Sheet not found**: Use `xlsx sheets file.xlsx` to list available sheets
3. **Invalid cell reference**: Check that cell/range format is correct (e.g., A1, B5:B10)
4. **Permission denied**: Ensure the file is not open in Excel or locked

## Examples by Use Case

### Data Analysis
```bash
# Find all high-value transactions
xlsx filter sales.xlsx --where "Amount > 1000" --format table

# Get statistics on revenue
xlsx stats sales.xlsx --sheet "Revenue"

# Count records by criteria
xlsx filter customers.xlsx --where "Status = 'Active'" | wc -l
```

### Data Cleaning
```bash
# Find null emails
xlsx filter users.xlsx --where "Email IS NULL"

# Search for invalid data
xlsx search data.xlsx "ERROR" --ignore-case

# View problematic rows
xlsx filter data.xlsx --where "Age < 0 OR Age > 150"
```

### Reporting
```bash
# Extract executive summary data
xlsx select report.xlsx "A,E,F" --limit 10

# Convert to CSV for email
xlsx to-csv monthly_report.xlsx summary.csv --sheet "Summary"

# Get formatted view
xlsx view report.xlsx --sheet "Dashboard" --limit 50
```

### Bulk Operations
```bash
# Set header row
xlsx set data.xlsx A1:E1 "ID,Name,Email,Status,Date"

# Insert calculated column
xlsx insert data.xlsx column F
xlsx set data.xlsx F1 "Total" --value-type string
xlsx set data.xlsx F2 "=SUM(D2:E2)" --value-type formula
```

## Integration with Other Tools

The xlsx tool works well with standard Unix tools:

```bash
# Count matching rows
xlsx filter data.xlsx --where "Status = 'Active'" --format csv | wc -l

# Process with jq
xlsx view data.xlsx --format json | jq '.[] | select(.age > 30)'

# Chain operations
xlsx to-csv input.xlsx - | grep "pattern" | xlsx from-csv - output.xlsx
```

## When to Use Each Command

- **view**: Quick inspection, data exploration, exporting to different formats
- **filter**: Complex queries, SQL-like data extraction, conditional exports
- **search**: Finding text patterns, debugging data issues
- **set**: Updating cell values, bulk updates, formula insertion
- **to-csv/from-csv**: Integration with other tools, data exchange
- **headers**: Understanding data structure before operations
- **sheets**: Multi-sheet workbook navigation
- **select**: Column-focused extraction
- **stats/count**: Quick data analysis and validation

## Quick Reference

```bash
# View
xlsx sheets <file>                    # list sheets
xlsx view <file>                      # view data
xlsx headers <file>                   # show headers

# Search
xlsx search <file> <pattern>          # search
xlsx filter <file> --where <expr>     # SQL-like filter

# Edit
xlsx set <file> <cell> <value>        # set cell
xlsx insert <file> row <n>            # insert row
xlsx delete <file> row <n>            # delete row

# Convert
xlsx to-csv <xlsx> <csv>              # to CSV
xlsx from-csv <csv> <xlsx>            # from CSV

# Analyze
xlsx count <file>                     # count rows/cols
xlsx stats <file>                     # statistics
```
