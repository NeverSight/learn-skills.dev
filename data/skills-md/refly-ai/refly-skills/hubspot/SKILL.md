---
name: hubspot
description: "Integrate with HubSpot for CRM management. Use when you need to: (1) manage contacts and deals, (2) track sales pipelines, or (3) automate marketing and CRM workflows."
version: 1.0.0
skillId: skp-u0mohd5c6uier9grwe0nqrdr
workflowId: c-rocmop29fu4ta02pucb4btgp
installationId: skpi-bhvgls7ymywqlsbyqfsfn92a
category: action
---

# Hubspot

Integrate with HubSpot for CRM management. Use when you need to: (1) manage contacts and deals, (2) track sales pipelines, or (3) automate marketing and CRM workflows.

## Input

Provide input as JSON:

```json
{
  "contact_email": "Email address of the contact to manage",
  "contact_name": "Full name of the contact",
  "company_name": "Company name associated with the contact",
  "deal_name": "Name of the deal to create or manage",
  "deal_amount": "Deal value in dollars (e.g., 50000)",
  "deal_stage": "Deal pipeline stage (e.g., prospecting, qualified, closed-won)"
}
```

## Execution (Pattern C: Action)

### Step 1: Run the Skill and Get Run ID

```bash
RESULT=$(refly skill run --id skpi-bhvgls7ymywqlsbyqfsfn92a --input '{
  "contact_email": "lead@example.com",
  "first_name": "Jane",
  "last_name": "Smith",
  "company": "Acme Inc"
}')
RUN_ID=$(echo "$RESULT" | jq -r '.payload.workflowExecutions[0].id')
# RUN_ID is we-xxx format, use this for workflow commands
```

### Step 2: Open Workflow in Browser and Wait for Completion

```bash
open "https://refly.ai/workflow/c-rocmop29fu4ta02pucb4btgp"
refly workflow status "$RUN_ID" --watch --interval 30000
```

### Step 3: Confirm Action Status

```bash
# Confirm contact/deal created
STATUS=$(refly workflow detail "$RUN_ID" | jq -r '.payload.status')
echo "Action completed with status: $STATUS"
```

## Expected Output

- **Type**: API Response
- **Format**: JSON CRM data (record ID, link)
- **Action**: Confirm record created/updated successfully

## Rules

Follow base skill workflow: `~/.claude/skills/refly/SKILL.md`
