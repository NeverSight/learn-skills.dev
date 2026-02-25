---
name: onedrive
description: "Integrate with OneDrive for cloud storage. Use when you need to: (1) upload and download files, (2) manage cloud documents, or (3) automate file storage workflows."
version: 1.0.0
skillId: skp-l7ya0pqf3i8x2mmz4saz4hva
workflowId: c-wc1jqswsu81farjbug1967fb
installationId: skpi-x34u17y8emkwaen73zduzrr2
category: action
---

# Onedrive

Integrate with OneDrive for cloud storage. Use when you need to: (1) upload and download files, (2) manage cloud documents, or (3) automate file storage workflows.

## Input

Provide input as JSON:

```json
{
  "file_to_upload": "<file-reference>",
  "target_folder": "Target folder path in OneDrive where files will be uploaded (e.g., /Documents/Work)",
  "search_query": "Search term to find files in OneDrive (e.g., file name, content keywords)"
}
```

## Execution (Pattern C: Action)

### Step 1: Run the Skill and Get Run ID

```bash
RESULT=$(refly skill run --id skpi-x34u17y8emkwaen73zduzrr2 --input '{
  "file_path": "/Documents/report.pdf",
  "action": "download"
}')
RUN_ID=$(echo "$RESULT" | jq -r '.payload.workflowExecutions[0].id')
# RUN_ID is we-xxx format, use this for workflow commands
```

### Step 2: Open Workflow in Browser and Wait for Completion

```bash
open "https://refly.ai/workflow/c-wc1jqswsu81farjbug1967fb"
refly workflow status "$RUN_ID" --watch --interval 30000
```

### Step 3: Confirm Action Status

```bash
# Confirm file operation completed
STATUS=$(refly workflow detail "$RUN_ID" | jq -r '.payload.status')
echo "Action completed with status: $STATUS"
```

## Expected Output

- **Type**: API Response
- **Format**: JSON file operation result
- **Action**: Confirm file uploaded/downloaded successfully

## Rules

Follow base skill workflow: `~/.claude/skills/refly/SKILL.md`
