---
name: microsoft-teams
description: "Integrate with Microsoft Teams for collaboration. Use when you need to: (1) send messages to Teams channels, (2) post team notifications, or (3) automate Teams communication workflows."
version: 1.0.0
skillId: skp-eo9basul0urf7ndz6qp02yys
workflowId: c-j4l0l72bcoiez6lf89ssxcn5
installationId: skpi-jx64wgsh5ei3xynckeizacr0
category: action
---

# Microsoft Teams

Integrate with Microsoft Teams for collaboration. Use when you need to: (1) send messages to Teams channels, (2) post team notifications, or (3) automate Teams communication workflows.

## Input

Provide input as JSON:

```json
{
  "team_name": "Name of the Microsoft Teams team to manage",
  "channel_name": "Name of the channel to create or manage",
  "message_content": "Content of the message to send to the team channel"
}
```

## Execution (Pattern C: Action)

### Step 1: Run the Skill and Get Run ID

```bash
RESULT=$(refly skill run --id skpi-jx64wgsh5ei3xynckeizacr0 --input '{
  "channel": "General",
  "message": "Team update: Project milestone completed."
}')
RUN_ID=$(echo "$RESULT" | jq -r '.payload.workflowExecutions[0].id')
# RUN_ID is we-xxx format, use this for workflow commands
```

### Step 2: Open Workflow in Browser and Wait for Completion

```bash
open "https://refly.ai/workflow/c-j4l0l72bcoiez6lf89ssxcn5"
refly workflow status "$RUN_ID" --watch --interval 30000
```

### Step 3: Confirm Action Status

```bash
# Confirm message sent
STATUS=$(refly workflow detail "$RUN_ID" | jq -r '.payload.status')
echo "Action completed with status: $STATUS"
```

## Expected Output

- **Type**: API Response
- **Format**: JSON message confirmation
- **Action**: Confirm message sent successfully

## Rules

Follow base skill workflow: `~/.claude/skills/refly/SKILL.md`
