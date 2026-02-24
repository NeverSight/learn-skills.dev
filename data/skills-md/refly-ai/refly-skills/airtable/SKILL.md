---
name: airtable
description: "Integrate with Airtable for database management. Use when you need to: (1) create and query Airtable records, (2) manage structured data in bases, or (3) automate data workflows."
version: 1.0.0
skillId: skp-sgzkygrassikberbett539ai
workflowId: c-wl4zkncuw4uv5etp3yb0dy1y
installationId: skpi-h0qwl26a3tovbejlear9z7rq
category: action
---

# Airtable

Integrate with Airtable for database management. Use when you need to: (1) create and query Airtable records, (2) manage structured data in bases, or (3) automate data workflows.

## Input

Provide input as JSON:

```json
{
  "base_id": "Airtable base ID (found in the URL when viewing your base)",
  "table_name": "Name of the table to work with",
  "record_data": "Data for the new record in JSON format (e.g., {\"Name\": \"Task 1\", \"Status\": \"In Progress\"})",
  "query_filter": "Optional filter formula for querying records (e.g., {Status} = 'In Progress')"
}
```

## Execution (Pattern C: Action)

### Step 1: Run the Skill and Get Run ID

```bash
RESULT=$(refly skill run --id skpi-h0qwl26a3tovbejlear9z7rq --input '{
  "base_id": "appXXXXXXXXX",
  "table_name": "Contacts",
  "record_data": {"Name": "John Doe", "Email": "john@example.com"}
}')
RUN_ID=$(echo "$RESULT" | jq -r '.payload.workflowExecutions[0].id')
# RUN_ID is we-xxx format, use this for workflow commands
```

### Step 2: Open Workflow in Browser and Wait for Completion

```bash
open "https://refly.ai/workflow/c-wl4zkncuw4uv5etp3yb0dy1y"
refly workflow status "$RUN_ID" --watch --interval 30000
```

### Step 3: Confirm Action Status

```bash
# Confirm record created
STATUS=$(refly workflow detail "$RUN_ID" | jq -r '.payload.status')
echo "Action completed with status: $STATUS"
```

## Expected Output

- **Type**: API Response
- **Format**: JSON record data (record ID)
- **Action**: Confirm record created/updated successfully

## Rules

Follow base skill workflow: `~/.claude/skills/refly/SKILL.md`
