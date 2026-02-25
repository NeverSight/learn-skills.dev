---
name: trello
description: "Integrate with Trello for project management. Use when you need to: (1) create and manage Trello cards, (2) organize tasks in lists and boards, or (3) automate project tracking workflows."
version: 1.0.0
skillId: skp-x4da1f3j06ctgybq9ifva7i3
workflowId: c-qk05acujevzakrmg712he1jl
installationId: skpi-lf49v8tqaxyntty5p5jcpxk4
category: action
---

# Trello

Integrate with Trello for project management. Use when you need to: (1) create and manage Trello cards, (2) organize tasks in lists and boards, or (3) automate project tracking workflows.

## Input

Provide input as JSON:

```json
{
  "board_name": "Name of the Trello board to create or manage",
  "list_names": "Comma-separated list names to create (e.g., To Do, In Progress, Done)",
  "card_title": "Title for the card to create",
  "card_description": "Description for the card"
}
```

## Execution (Pattern C: Action)

### Step 1: Run the Skill and Get Run ID

```bash
RESULT=$(refly skill run --id skpi-lf49v8tqaxyntty5p5jcpxk4 --input '{
  "board_name": "Project Tasks",
  "card_title": "New feature implementation",
  "list_name": "To Do"
}')
RUN_ID=$(echo "$RESULT" | jq -r '.payload.workflowExecutions[0].id')
# RUN_ID is we-xxx format, use this for workflow commands
```

### Step 2: Open Workflow in Browser and Wait for Completion

```bash
open "https://refly.ai/workflow/c-qk05acujevzakrmg712he1jl"
refly workflow status "$RUN_ID" --watch --interval 30000
```

### Step 3: Confirm Action Status

```bash
# Confirm card created
STATUS=$(refly workflow detail "$RUN_ID" | jq -r '.payload.status')
echo "Action completed with status: $STATUS"
```

## Expected Output

- **Type**: API Response
- **Format**: JSON card data (card ID, link)
- **Action**: Confirm card created successfully

## Rules

Follow base skill workflow: `~/.claude/skills/refly/SKILL.md`
