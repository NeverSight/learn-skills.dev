---
name: linear
description: "Integrate with Linear for issue tracking. Use when you need to: (1) create and manage Linear issues, (2) track development tasks and bugs, or (3) automate engineering project workflows."
version: 1.0.0
skillId: skp-if87skcz08aq8bcos9kd3hm5
workflowId: c-ijjrk8c5aqb5dp3z0nih7xfk
installationId: skpi-igoaqxgoy7waoxcesfq2l0sc
category: action
---

# Linear

Integrate with Linear for issue tracking. Use when you need to: (1) create and manage Linear issues, (2) track development tasks and bugs, or (3) automate engineering project workflows.

## Input

Provide input as JSON:

```json
{
  "project_name": "Name of the Linear project or team to work with",
  "issue_title": "Title for the new issue to create",
  "issue_description": "Detailed description of the issue",
  "issue_priority": "Priority level for the issue (e.g., urgent, high, medium, low)",
  "assignee_email": "Email address of the team member to assign the issue to"
}
```

## Execution (Pattern C: Action)

### Step 1: Run the Skill and Get Run ID

```bash
RESULT=$(refly skill run --id skpi-igoaqxgoy7waoxcesfq2l0sc --input '{
  "title": "Bug fix: Login page error",
  "description": "Users unable to login on mobile devices",
  "team": "Engineering"
}')
RUN_ID=$(echo "$RESULT" | jq -r '.payload.workflowExecutions[0].id')
# RUN_ID is we-xxx format, use this for workflow commands
```

### Step 2: Open Workflow in Browser and Wait for Completion

```bash
open "https://refly.ai/workflow/c-ijjrk8c5aqb5dp3z0nih7xfk"
refly workflow status "$RUN_ID" --watch --interval 30000
```

### Step 3: Confirm Action Status

```bash
# Confirm issue created
STATUS=$(refly workflow detail "$RUN_ID" | jq -r '.payload.status')
echo "Action completed with status: $STATUS"
```

## Expected Output

- **Type**: API Response
- **Format**: JSON issue data (issue ID, link)
- **Action**: Confirm issue created successfully

## Rules

Follow base skill workflow: `~/.claude/skills/refly/SKILL.md`
