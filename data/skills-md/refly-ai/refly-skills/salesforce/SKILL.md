---
name: salesforce
description: "Integrate with Salesforce for CRM operations. Use when you need to: (1) create and query Salesforce records, (2) manage accounts and opportunities, or (3) automate sales workflows."
version: 1.0.0
skillId: skp-siml24dbdrn4obppygeaq8kc
workflowId: c-voxvui1zpu15a7j8zmf6mjwa
installationId: skpi-l8hjpo6mjeb871d1y8ttw0og
category: action
---

# Salesforce

Integrate with Salesforce for CRM operations. Use when you need to: (1) create and query Salesforce records, (2) manage accounts and opportunities, or (3) automate sales workflows.

## Input

Provide input as JSON:

```json
{
  "record_type": "Type of CRM record to create (e.g., Lead, Contact, Account, Opportunity)",
  "record_data": "JSON data for the new record (e.g., {\"FirstName\": \"John\", \"LastName\": \"Doe\", \"Company\": \"Acme Corp\", \"Email\": \"john@acme.com\"})",
  "query_criteria": "Search criteria for querying records (e.g., company name, email domain, date range)"
}
```

## Execution (Pattern C: Action)

### Step 1: Run the Skill and Get Run ID

```bash
RESULT=$(refly skill run --id skpi-l8hjpo6mjeb871d1y8ttw0og --input '{
  "object_type": "Lead",
  "first_name": "John",
  "last_name": "Doe",
  "company": "Tech Corp"
}')
RUN_ID=$(echo "$RESULT" | jq -r '.payload.workflowExecutions[0].id')
# RUN_ID is we-xxx format, use this for workflow commands
```

### Step 2: Open Workflow in Browser and Wait for Completion

```bash
open "https://refly.ai/workflow/c-voxvui1zpu15a7j8zmf6mjwa"
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
- **Format**: JSON CRM data (record ID)
- **Action**: Confirm record created/updated successfully

## Rules

Follow base skill workflow: `~/.claude/skills/refly/SKILL.md`
