---
name: excel
description: "Integrate with Microsoft Excel for spreadsheets. Use when you need to: (1) read and write Excel data, (2) manage spreadsheet workbooks, or (3) automate data analysis workflows."
version: 1.0.0
skillId: skp-qd0qwkkmoeategaqcxa4f82v
workflowId: c-af86a8xmozt53tyhs77stl9y
installationId: skpi-xcyq0shrulrg3h96hd4gquli
category: file-generation
---

# Excel

Integrate with Microsoft Excel for spreadsheets. Use when you need to: (1) read and write Excel data, (2) manage spreadsheet workbooks, or (3) automate data analysis workflows.

## Input

Provide input as JSON:

```json
{
  "spreadsheet_file": "Name or path of the Excel spreadsheet file to work with",
  "worksheet_name": "Name of the worksheet/sheet to read from or write to",
  "data_to_write": "Data content to write to the spreadsheet (e.g., CSV format or structured data)"
}
```

## Execution (Pattern A: File Generation)

### Step 1: Run the Skill and Get Run ID

```bash
RESULT=$(refly skill run --id skpi-xcyq0shrulrg3h96hd4gquli --input '{
  "workbook_name": "Sales Report",
  "sheet_name": "Q1 Data",
  "range": "A1:D10"
}')
RUN_ID=$(echo "$RESULT" | jq -r '.payload.workflowExecutions[0].id')
# RUN_ID is we-xxx format, use this for workflow commands
```

### Step 2: Open Workflow in Browser and Wait for Completion

```bash
open "https://refly.ai/workflow/c-af86a8xmozt53tyhs77stl9y"
refly workflow status "$RUN_ID" --watch --interval 30000
```

### Step 3: Download and Show Result

```bash
# Get files from this run
FILES=$(refly workflow toolcalls "$RUN_ID" --files --latest | jq -r '.payload.files[]')

# Download and open each file
echo "$FILES" | jq -c '.' | while read -r file; do
  FILE_ID=$(echo "$file" | jq -r '.fileId')
  FILE_NAME=$(echo "$file" | jq -r '.name')
  if [ -n "$FILE_ID" ] && [ "$FILE_ID" != "null" ]; then
    refly file download "$FILE_ID" -o "$HOME/Desktop/${FILE_NAME}"
    open "$HOME/Desktop/${FILE_NAME}"
  fi
done
```

## Expected Output

- **Type**: Spreadsheet
- **Format**: .xlsx Excel file
- **Location**: `~/Desktop/`
- **Action**: Opens automatically to show user

## Rules

Follow base skill workflow: `~/.claude/skills/refly/SKILL.md`
