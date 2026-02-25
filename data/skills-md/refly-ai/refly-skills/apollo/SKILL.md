---
name: apollo
description: "Search sales leads with Apollo.io. Use when you need to: (1) find company and contact information, (2) enrich lead data, or (3) search for B2B prospects."
version: 1.0.0
skillId: skp-urczy0rdx7skwsk7s93fnqb0
workflowId: c-ga8qr2v0idibvd841ypjhbix
installationId: skpi-jmvxpnmpmdkyxtrv488qwhbb
category: text-data
---

# Apollo

Search sales leads with Apollo.io. Use when you need to: (1) find company and contact information, (2) enrich lead data, or (3) search for B2B prospects.

## Input

Provide input as JSON:

```json
{
  "company_name": "Target company name to search for (e.g., Tesla, Microsoft, Apple)",
  "job_titles": "Job titles to search for (e.g., CEO, Sales Manager, Marketing Director)",
  "industry": "Target industry (e.g., Technology, Healthcare, Finance)",
  "location": "Geographic location to search (e.g., United States, San Francisco, New York)"
}
```

## Execution (Pattern B: Text/Data)

### Step 1: Run the Skill and Get Run ID

```bash
RESULT=$(refly skill run --id skpi-jmvxpnmpmdkyxtrv488qwhbb --input '{
  "company_name": "Microsoft",
  "job_title": "Software Engineer",
  "location": "San Francisco"
}')
RUN_ID=$(echo "$RESULT" | jq -r '.payload.workflowExecutions[0].id')
# RUN_ID is we-xxx format, use this for workflow commands
```

### Step 2: Open Workflow in Browser and Wait for Completion

```bash
open "https://refly.ai/workflow/c-ga8qr2v0idibvd841ypjhbix"
refly workflow status "$RUN_ID" --watch --interval 30000
```

### Step 3: Extract Text Content

```bash
# Get lead data from toolcalls
CONTENT=$(refly workflow toolcalls "$RUN_ID" --files --latest | jq -r '.payload.nodes[].content')
echo "$CONTENT"
```

## Expected Output

- **Type**: Text content
- **Format**: Sales leads data
- **Action**: Display lead information to user

## Rules

Follow base skill workflow: `~/.claude/skills/refly/SKILL.md`
