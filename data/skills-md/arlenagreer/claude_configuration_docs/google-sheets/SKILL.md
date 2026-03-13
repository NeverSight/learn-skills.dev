---
name: google-sheets
description: Manage Google Sheets with comprehensive spreadsheet operations including reading/writing cell values, formulas, formatting, sheet management, and batch operations. Use for spreadsheet data operations, cell ranges, formulas, formatting, batch updates, and data analysis workflows. Shares OAuth token with email, calendar, contacts, drive, and docs skills.
category: productivity
version: 1.0.0
key_capabilities: read/write cells, append rows, apply formatting, create sheets, batch operations, A1 notation support
when_to_use: Spreadsheet data operations, cell ranges, formulas, formatting, batch updates, data analysis workflows
---

# Google Sheets Management Skill

## Purpose

Manage Google Sheets spreadsheets with comprehensive operations:
- Read cell values and formulas
- Write and update cell values
- Append rows to sheets
- Clear cell ranges
- Create new sheets within spreadsheets
- Basic cell formatting (bold, italic, colors)
- Batch updates for efficiency
- Get spreadsheet metadata
- Share OAuth token with all Google skills

**Integration**: Works seamlessly with google-drive skill for file creation and management

**📚 Additional Resources**:
- See `references/integration-patterns.md` for complete workflow examples
- See `references/troubleshooting.md` for error handling and debugging
- See `references/cli-patterns.md` for CLI interface design rationale

## When to Use This Skill

Use this skill when:
- User requests spreadsheet operations: "Read the data from my spreadsheet", "Update the budget sheet"
- User wants to create or modify data: "Add a row to the tracking sheet", "Update cell B5"
- User mentions formulas: "Write a formula to sum column A", "Update the calculation"
- User requests formatting: "Make the header row bold", "Highlight the total in yellow"
- User needs batch operations: "Update multiple ranges", "Fill in the entire data set"
- User asks about spreadsheet structure: "How many sheets are in this workbook?", "What columns exist?"

**📋 Discovering Your Spreadsheets**:
To list or search for spreadsheets, use the google-drive skill:
```bash
# List recent spreadsheets
~/.claude/skills/google-drive/scripts/drive_manager.rb search \
  --query "mimeType='application/vnd.google-apps.spreadsheet'" \
  --max-results 50

# Search by name
~/.claude/skills/google-drive/scripts/drive_manager.rb search \
  --query "name contains 'Budget' and mimeType='application/vnd.google-apps.spreadsheet'"
```

## Core Workflows

### 1. Read Cell Values

**Read single cell**:
```bash
echo '{
  "spreadsheet_id": "abc123xyz",
  "range": "Sheet1!A1"
}' | ~/.claude/skills/google-sheets/scripts/sheets_manager.rb read
```

**Read range of cells**:
```bash
echo '{
  "spreadsheet_id": "abc123xyz",
  "range": "Sheet1!A1:D10"
}' | ~/.claude/skills/google-sheets/scripts/sheets_manager.rb read
```

**Read entire column**:
```bash
echo '{
  "spreadsheet_id": "abc123xyz",
  "range": "Sheet1!A:A"
}' | ~/.claude/skills/google-sheets/scripts/sheets_manager.rb read
```

**Read entire row**:
```bash
echo '{
  "spreadsheet_id": "abc123xyz",
  "range": "Sheet1!1:1"
}' | ~/.claude/skills/google-sheets/scripts/sheets_manager.rb read
```

**Output Format**:
```json
{
  "status": "success",
  "operation": "read",
  "spreadsheet_id": "abc123xyz",
  "range": "Sheet1!A1:D10",
  "values": [
    ["Header1", "Header2", "Header3", "Header4"],
    ["Value1", "Value2", "Value3", "Value4"]
  ],
  "row_count": 2
}
```

### 2. Write Cell Values

**Write single cell**:
```bash
echo '{
  "spreadsheet_id": "abc123xyz",
  "range": "Sheet1!A1",
  "values": [["Hello World"]]
}' | ~/.claude/skills/google-sheets/scripts/sheets_manager.rb write
```

**Write range of cells**:
```bash
echo '{
  "spreadsheet_id": "abc123xyz",
  "range": "Sheet1!A1:B2",
  "values": [
    ["Name", "Age"],
    ["Alice", 30]
  ]
}' | ~/.claude/skills/google-sheets/scripts/sheets_manager.rb write
```

**Write with formulas**:
```bash
echo '{
  "spreadsheet_id": "abc123xyz",
  "range": "Sheet1!C1",
  "values": [["=SUM(A1:A10)"]],
  "input_option": "USER_ENTERED"
}' | ~/.claude/skills/google-sheets/scripts/sheets_manager.rb write
```

**Input Options**:
- `USER_ENTERED` (default): Parses input as if typed by user (formulas, dates, numbers)
- `RAW`: Stores input exactly as provided (everything as strings)

**Output Format**:
```json
{
  "status": "success",
  "operation": "write",
  "spreadsheet_id": "abc123xyz",
  "range": "Sheet1!A1:B2",
  "updated_cells": 4,
  "updated_rows": 2,
  "updated_columns": 2
}
```

### 3. Append Rows

**Append single row**:
```bash
echo '{
  "spreadsheet_id": "abc123xyz",
  "range": "Sheet1!A1",
  "values": [["New", "Row", "Data"]]
}' | ~/.claude/skills/google-sheets/scripts/sheets_manager.rb append
```

**Append multiple rows**:
```bash
echo '{
  "spreadsheet_id": "abc123xyz",
  "range": "Sheet1!A1",
  "values": [
    ["Row1Col1", "Row1Col2"],
    ["Row2Col1", "Row2Col2"],
    ["Row3Col1", "Row3Col2"]
  ]
}' | ~/.claude/skills/google-sheets/scripts/sheets_manager.rb append
```

**How Append Works**:
- Finds the last row with data in the specified range
- Appends new rows immediately after
- Does not overwrite existing data
- Perfect for logging, tracking, and data collection

### 4. Clear Cell Values

**Clear specific range**:
```bash
echo '{
  "spreadsheet_id": "abc123xyz",
  "range": "Sheet1!A1:D10"
}' | ~/.claude/skills/google-sheets/scripts/sheets_manager.rb clear
```

**Clear entire sheet**:
```bash
echo '{
  "spreadsheet_id": "abc123xyz",
  "range": "Sheet1"
}' | ~/.claude/skills/google-sheets/scripts/sheets_manager.rb clear
```

**Important**: Clear only removes cell values, not formatting or formulas

### 5. Get Spreadsheet Metadata

```bash
echo '{
  "spreadsheet_id": "abc123xyz"
}' | ~/.claude/skills/google-sheets/scripts/sheets_manager.rb metadata
```

**Output Format**:
```json
{
  "status": "success",
  "operation": "metadata",
  "spreadsheet_id": "abc123xyz",
  "title": "Budget 2024",
  "locale": "en_US",
  "timezone": "America/Chicago",
  "sheets": [
    {
      "sheet_id": 0,
      "title": "Sheet1",
      "index": 0,
      "row_count": 1000,
      "column_count": 26
    },
    {
      "sheet_id": 123456,
      "title": "Summary",
      "index": 1,
      "row_count": 100,
      "column_count": 10
    }
  ]
}
```

### 6. Create New Sheet

**Create sheet with default size**:
```bash
echo '{
  "spreadsheet_id": "abc123xyz",
  "title": "Q4 Data"
}' | ~/.claude/skills/google-sheets/scripts/sheets_manager.rb create_sheet
```

**Create sheet with custom size**:
```bash
echo '{
  "spreadsheet_id": "abc123xyz",
  "title": "Large Dataset",
  "row_count": 5000,
  "column_count": 50
}' | ~/.claude/skills/google-sheets/scripts/sheets_manager.rb create_sheet
```

**Default Dimensions**:
- Rows: 1000
- Columns: 26 (A-Z)

### 7. Basic Cell Formatting

**Format header row (bold + background color)**:
```bash
echo '{
  "spreadsheet_id": "abc123xyz",
  "sheet_id": 0,
  "start_row": 0,
  "end_row": 1,
  "start_col": 0,
  "end_col": 5,
  "format": {
    "bold": true,
    "fontSize": 12,
    "backgroundColor": {
      "red": 0.9,
      "green": 0.9,
      "blue": 0.9,
      "alpha": 1
    }
  }
}' | ~/.claude/skills/google-sheets/scripts/sheets_manager.rb format
```

**Available Format Options**:
- `bold`: true/false
- `italic`: true/false
- `fontSize`: Number (e.g., 10, 12, 14)
- `backgroundColor`: Object with red, green, blue, alpha (0-1 scale)

**Important Notes**:
- Row and column indices are 0-based (first row = 0, first column = 0)
- Ranges are half-open: start is inclusive, end is exclusive
- To format row 1 (the first row): `start_row: 0, end_row: 1`

### 8. Batch Updates

**Update multiple ranges efficiently**:
```bash
echo '{
  "spreadsheet_id": "abc123xyz",
  "updates": [
    {
      "range": "Sheet1!A1:A3",
      "values": [["Value1"], ["Value2"], ["Value3"]]
    },
    {
      "range": "Sheet1!B1:B3",
      "values": [["100"], ["200"], ["300"]]
    },
    {
      "range": "Sheet1!C1",
      "values": [["=SUM(B1:B3)"]]
    }
  ]
}' | ~/.claude/skills/google-sheets/scripts/sheets_manager.rb batch_update
```

**Benefits**:
- Single API call for multiple updates
- More efficient than individual writes
- Atomic operation (all succeed or all fail)
- Perfect for populating templates or data imports

## A1 Notation Reference

**Single Cells**:
- `A1`: First cell
- `B5`: Column B, Row 5
- `Z10`: Column Z, Row 10

**Ranges**:
- `A1:B10`: Rectangle from A1 to B10
- `C5:F20`: Rectangle from C5 to F20

**Entire Rows/Columns**:
- `A:A`: Entire column A
- `C:E`: Columns C through E
- `1:1`: Entire row 1
- `5:10`: Rows 5 through 10

**Named Sheets**:
- `Sheet1!A1:B10`: Range on specific sheet
- `Q4 Data!A1`: Cell A1 on "Q4 Data" sheet
- Use single quotes for sheet names with spaces: `'Budget 2024'!A1`

## Natural Language Examples

### User Says: "Read the budget data from cells A1 to D10"
```bash
echo '{
  "spreadsheet_id": "[GET_FROM_CONTEXT_OR_ASK_USER]",
  "range": "Sheet1!A1:D10"
}' | ~/.claude/skills/google-sheets/scripts/sheets_manager.rb read
```

### User Says: "Add a new row with Name: John, Age: 30, City: Chicago"
```bash
echo '{
  "spreadsheet_id": "[SPREADSHEET_ID]",
  "range": "Sheet1!A1",
  "values": [["John", 30, "Chicago"]]
}' | ~/.claude/skills/google-sheets/scripts/sheets_manager.rb append
```

### User Says: "Update cell B5 to the value 1000"
```bash
echo '{
  "spreadsheet_id": "[SPREADSHEET_ID]",
  "range": "Sheet1!B5",
  "values": [[1000]]
}' | ~/.claude/skills/google-sheets/scripts/sheets_manager.rb write
```

### User Says: "Write a formula in C10 to sum all values in column C from rows 1 to 9"
```bash
echo '{
  "spreadsheet_id": "[SPREADSHEET_ID]",
  "range": "Sheet1!C10",
  "values": [["=SUM(C1:C9)"]],
  "input_option": "USER_ENTERED"
}' | ~/.claude/skills/google-sheets/scripts/sheets_manager.rb write
```

### User Says: "Make the first row bold with a gray background"
```bash
# First get metadata to find sheet_id
echo '{"spreadsheet_id":"[SPREADSHEET_ID]"}' | ~/.claude/skills/google-sheets/scripts/sheets_manager.rb metadata

# Then format the row (assuming sheet_id is 0)
echo '{
  "spreadsheet_id": "[SPREADSHEET_ID]",
  "sheet_id": 0,
  "start_row": 0,
  "end_row": 1,
  "start_col": 0,
  "end_col": 26,
  "format": {
    "bold": true,
    "backgroundColor": {"red": 0.9, "green": 0.9, "blue": 0.9, "alpha": 1}
  }
}' | ~/.claude/skills/google-sheets/scripts/sheets_manager.rb format
```

### User Says: "Clear all data from the sheet"
```bash
echo '{
  "spreadsheet_id": "[SPREADSHEET_ID]",
  "range": "Sheet1"
}' | ~/.claude/skills/google-sheets/scripts/sheets_manager.rb clear
```

## Integration with Google Drive Skill

**Create Spreadsheet + Populate Data Workflow**:

1. **Create spreadsheet file** (using google-drive skill):
```bash
# See google-drive skill for file creation
# Returns spreadsheet_id
```

2. **Populate with data** (using this skill):
```bash
echo '{
  "spreadsheet_id": "[ID_FROM_DRIVE_SKILL]",
  "range": "Sheet1!A1:C3",
  "values": [
    ["Name", "Age", "City"],
    ["Alice", 30, "Chicago"],
    ["Bob", 25, "New York"]
  ]
}' | ~/.claude/skills/google-sheets/scripts/sheets_manager.rb write
```

3. **Share spreadsheet** (using google-drive skill):
```bash
# See google-drive skill for sharing operations
```

## Authentication Setup

**Shared OAuth Token**:
- Uses same token as email, calendar, contacts, drive, and docs skills
- Location: `~/.claude/.google/token.json`
- Credentials: `~/.claude/.google/client_secret.json`

**Required Scopes**:
- `https://www.googleapis.com/auth/spreadsheets` (Sheets operations)
- `https://www.googleapis.com/auth/drive` (Drive integration)
- `https://www.googleapis.com/auth/documents` (Docs integration)
- `https://www.googleapis.com/auth/calendar` (Calendar integration)
- `https://www.googleapis.com/auth/contacts` (Contacts integration)
- `https://www.googleapis.com/auth/gmail.modify` (Gmail integration)

**First-Time Setup**:
1. Run any sheets operation
2. Script will prompt for authorization URL
3. Visit URL and authorize all Google services
4. Enter authorization code when prompted
5. Token stored for future use across all Google skills

**Re-authorization**:
- Token automatically refreshes when expired
- If refresh fails, re-run authorization flow
- One authorization grants access to all Google skills

## Bundled Resources

### Scripts

**`scripts/sheets_manager.rb`**
- Comprehensive Google Sheets API wrapper
- All core operations: read, write, append, clear, metadata
- Sheet management: create new sheets within spreadsheets
- Basic formatting: bold, italic, colors, font size
- Batch updates for efficiency
- Shared OAuth with all Google skills

**Operations**:
- `auth`: Complete OAuth authorization
- `read`: Read cell values
- `write`: Write cell values
- `append`: Append rows to sheet
- `clear`: Clear cell values
- `metadata`: Get spreadsheet metadata
- `create_sheet`: Create new sheet within spreadsheet
- `format`: Update cell formatting
- `batch_update`: Batch update multiple ranges

**Output Format**:
- JSON with `status: 'success'` or `status: 'error'`
- Operation-specific data in response
- Exit codes: 0=success, 1=failed, 2=auth, 3=api, 4=args

**Ruby Gem Requirement**:
```bash
gem install google-apis-sheets_v4
```

### References

**`references/sheets_operations.md`**
- Complete operation reference with examples
- Parameter documentation for all operations
- Common use cases and patterns
- Error scenarios and solutions

**`references/cell_formats.md`**
- Cell formatting options and examples
- Color specifications (RGB + alpha)
- Text formatting (bold, italic, size)
- Background colors and patterns
- Format combinations and best practices

### Examples

**`examples/sample_operations.md`**
- Real-world usage examples
- Common workflows and patterns
- Data import/export scenarios
- Formula writing examples
- Batch operation patterns

## Error Handling

**Authentication Error**:
```json
{
  "status": "error",
  "error_code": "AUTH_REQUIRED",
  "message": "Authorization required. Please visit the URL and enter the code.",
  "auth_url": "https://accounts.google.com/o/oauth2/auth?..."
}
```
**Action**: Follow authorization instructions

**API Error**:
```json
{
  "status": "error",
  "error_code": "API_ERROR",
  "operation": "read",
  "message": "Sheets API error: Requested entity was not found."
}
```
**Action**: Verify spreadsheet_id and range, check permissions

**Invalid Arguments**:
```json
{
  "status": "error",
  "error_code": "MISSING_REQUIRED_FIELDS",
  "message": "Required fields: spreadsheet_id, range"
}
```
**Action**: Review command parameters and retry

**Range Error**:
```json
{
  "status": "error",
  "error_code": "API_ERROR",
  "message": "Unable to parse range: InvalidRange"
}
```
**Action**: Check A1 notation syntax, ensure sheet name exists

## Best Practices

### Getting Spreadsheet ID
1. **From URL**: Extract from Google Sheets URL
   - URL: `https://docs.google.com/spreadsheets/d/ABC123XYZ/edit`
   - ID: `ABC123XYZ`
2. **From google-drive skill**: Use search or list operations
3. **Store ID**: Keep commonly-used spreadsheet IDs in context

### Reading Data Efficiently
1. Read only the data you need (specific ranges)
2. Use metadata operation to understand sheet structure first
3. For large datasets, read in chunks
4. Cache read results when making multiple queries

### Writing Data Efficiently
1. Use batch_update for multiple ranges
2. Group related updates into single operations
3. Use append for adding rows (don't overwrite)
4. Prefer USER_ENTERED for formulas and dates

### Formulas
1. Always use `input_option: "USER_ENTERED"` for formulas
2. Formula syntax is standard Google Sheets formula language
3. Example: `=SUM(A1:A10)`, `=AVERAGE(B:B)`, `=IF(C1>100,"High","Low")`
4. Test formulas in Google Sheets UI before automating

### Formatting
1. Get sheet_id from metadata operation first
2. Remember: row/column indices are 0-based
3. Format ranges, not individual cells for efficiency
4. Background colors use 0-1 scale (0=0%, 0.5=50%, 1=100%)

### Sheet Management
1. Check existing sheets with metadata before creating
2. Use descriptive sheet names
3. Default size (1000x26) works for most use cases
4. Create larger sheets only when needed

## Quick Reference

**Read values**:
```bash
echo '{"spreadsheet_id":"ID","range":"Sheet1!A1:B10"}' | sheets_manager.rb read
```

**Write values**:
```bash
echo '{"spreadsheet_id":"ID","range":"Sheet1!A1","values":[["Data"]]}' | sheets_manager.rb write
```

**Append rows**:
```bash
echo '{"spreadsheet_id":"ID","range":"Sheet1!A1","values":[["Row1"],["Row2"]]}' | sheets_manager.rb append
```

**Write formula**:
```bash
echo '{"spreadsheet_id":"ID","range":"Sheet1!C1","values":[["=SUM(A1:A10)"]],"input_option":"USER_ENTERED"}' | sheets_manager.rb write
```

**Get metadata**:
```bash
echo '{"spreadsheet_id":"ID"}' | sheets_manager.rb metadata
```

**Clear range**:
```bash
echo '{"spreadsheet_id":"ID","range":"Sheet1!A1:Z100"}' | sheets_manager.rb clear
```

**Create sheet**:
```bash
echo '{"spreadsheet_id":"ID","title":"New Sheet"}' | sheets_manager.rb create_sheet
```

**Format cells**:
```bash
echo '{"spreadsheet_id":"ID","sheet_id":0,"start_row":0,"end_row":1,"start_col":0,"end_col":5,"format":{"bold":true}}' | sheets_manager.rb format
```

**Batch update** (multiple operations in one call):
```bash
echo '{
  "spreadsheet_id": "ID",
  "requests": [
    {
      "updateCells": {
        "range": {"sheetId": 0, "startRowIndex": 0, "endRowIndex": 1, "startColumnIndex": 0, "endColumnIndex": 5},
        "fields": "userEnteredFormat.backgroundColor,userEnteredFormat.textFormat.bold",
        "userEnteredFormat": {
          "backgroundColor": {"red": 0.2, "green": 0.6, "blue": 0.9},
          "textFormat": {"bold": true}
        }
      }
    },
    {
      "updateCells": {
        "range": {"sheetId": 0, "startRowIndex": 1, "endRowIndex": 10, "startColumnIndex": 0, "endColumnIndex": 1},
        "fields": "userEnteredFormat.textFormat.italic",
        "userEnteredFormat": {
          "textFormat": {"italic": true}
        }
      }
    }
  ]
}' | sheets_manager.rb batch_update
```

## Common Workflows

### Data Entry Workflow
1. Get metadata to understand structure
2. Append new rows with data
3. Optionally format new rows
4. Verify with read operation

### Report Generation Workflow
1. Clear existing data (optional)
2. Write headers with formatting
3. Batch update data rows
4. Write formula rows for calculations
5. Format summary/total rows

### Data Analysis Workflow
1. Read data range
2. Process data in your code
3. Write results to new range or sheet
4. Add formulas for ongoing calculations

### Template Population Workflow
1. Create spreadsheet from template (google-drive)
2. Batch update with personalized data
3. Apply formatting to key areas
4. Share with collaborators (google-drive)

## Version History

- **1.0.0** (2025-11-10) - Initial google-sheets skill with comprehensive spreadsheet operations: read/write cells, append rows, clear ranges, sheet management, basic formatting, batch updates, and shared OAuth token with all Google skills (email, calendar, contacts, drive, docs)

---

**Dependencies**: Ruby with `google-apis-sheets_v4`, `google-apis-drive_v3`, `google-apis-docs_v1`, `google-apis-calendar_v3`, `google-apis-people_v1`, `googleauth` gems (shared with all Google skills)
