---
name: asana
description: "Integrate with Asana for task management. Use when you need to: (1) create and manage Asana tasks, (2) organize project work, or (3) automate team task tracking workflows."
version: 1.0.0
skillId: skp-aghvdv09cw7wk5nocsp3w07u
workflowId: c-r0huf9s48yo3dhu5839o9kp3
installationId: skpi-sf7xwlaqegajlfp4r7acdqk8
category: action
---

# Asana

Integrate with Asana for task management. Use when you need to: (1) create and manage Asana tasks, (2) organize project work, or (3) automate team task tracking workflows.

## Input

Provide input as JSON:

```json
{
  "project_name": "Name of the project to create or manage",
  "workspace_name": "Asana workspace name where the project will be created",
  "task_list": "List of tasks to create (one per line or comma-separated)",
  "assignee_email": "Email address of the team member to assign tasks to (optional)"
}
```

## Execution (Pattern C: Action)

### Step 1: Run the Skill and Get Run ID

```bash
RESULT=$(refly skill run --id skpi-sf7xwlaqegajlfp4r7acdqk8 --input '{
  "project_name": "Q1 Goals",
  "task_name": "Complete documentation",
  "assignee": "team@example.com"
}')
RUN_ID=$(echo "$RESULT" | jq -r '.payload.workflowExecutions[0].id')
# RUN_ID is we-xxx format, use this for workflow commands
```

### Step 2: Open Workflow in Browser and Wait for Completion

```bash
open "https://refly.ai/workflow/c-r0huf9s48yo3dhu5839o9kp3"
refly workflow status "$RUN_ID" --watch --interval 30000
```

### Step 3: Confirm Action Status

```bash
# Confirm task created
STATUS=$(refly workflow detail "$RUN_ID" | jq -r '.payload.status')
echo "Action completed with status: $STATUS"
```

## Expected Output

- **Type**: API Response
- **Format**: JSON task data (task ID, link)
- **Action**: Confirm task created successfully

## Rules

Follow base skill workflow: `~/.claude/skills/refly/SKILL.md`
