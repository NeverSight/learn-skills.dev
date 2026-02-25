---
name: google-analytics
description: "Integrate with Google Analytics for web metrics. Use when you need to: (1) retrieve website analytics reports, (2) track traffic and user metrics, or (3) analyze web performance data."
version: 1.0.0
skillId: skp-pd5q1x9nd5zoqjihacwf7apk
workflowId: c-o5nfiwa9rm39qmcjglnva7ye
installationId: skpi-mtb0qx9adafqm4d2ll3f9zqr
category: text-data
---

# Google Analytics

Integrate with Google Analytics for web metrics. Use when you need to: (1) retrieve website analytics reports, (2) track traffic and user metrics, or (3) analyze web performance data.

## Input

Provide input as JSON:

```json
{
  "property_id": "Google Analytics property ID (e.g., properties/123456789)",
  "date_range": "Date range for the report (e.g., last 7 days, last 30 days, last 90 days)",
  "metrics": "Metrics to retrieve (e.g., sessions, users, pageviews, bounce rate, conversion rate)",
  "dimensions": "Dimensions to group by (e.g., date, country, device category, page path)"
}
```

## Execution (Pattern B: Text/Data)

### Step 1: Run the Skill and Get Run ID

```bash
RESULT=$(refly skill run --id skpi-mtb0qx9adafqm4d2ll3f9zqr --input '{
  "property_id": "GA-XXXXXXX",
  "start_date": "2024-01-01",
  "end_date": "2024-01-31",
  "metrics": "sessions,pageviews"
}')
RUN_ID=$(echo "$RESULT" | jq -r '.payload.workflowExecutions[0].id')
# RUN_ID is we-xxx format, use this for workflow commands
```

### Step 2: Open Workflow in Browser and Wait for Completion

```bash
open "https://refly.ai/workflow/c-o5nfiwa9rm39qmcjglnva7ye"
refly workflow status "$RUN_ID" --watch --interval 30000
```

### Step 3: Extract Text Content

```bash
# Get analytics data from toolcalls
CONTENT=$(refly workflow toolcalls "$RUN_ID" --files --latest | jq -r '.payload.nodes[].content')
echo "$CONTENT"
```

## Expected Output

- **Type**: Text content
- **Format**: JSON analytics data
- **Action**: Display analytics report to user

## Rules

Follow base skill workflow: `~/.claude/skills/refly/SKILL.md`
