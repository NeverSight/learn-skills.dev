---
name: slack
description: "Integrate with Slack for team messaging. Use when you need to: (1) send messages to Slack channels, (2) post notifications and updates, or (3) automate Slack communication workflows."
version: 1.0.0
skillId: skp-gzf70d11wt6x7w3thngb5eqd
workflowId: c-k1lpwjqxvtnfs6t1l82bun9e
installationId: skpi-zktzbpe4r5cz4cq6opst7yl6
category: action
---

# Slack

Integrate with Slack for team messaging. Use when you need to: (1) send messages to Slack channels, (2) post notifications and updates, or (3) automate Slack communication workflows.

## Input

Provide input as JSON:

```json
{
  "channel_name": "The Slack channel to send messages to (e.g., #general, #announcements)",
  "message_content": "The message content to send to the channel",
  "notification_type": "Type of notification to manage (e.g., urgent, info, reminder)",
  "mention_users": "Users to mention in the message (comma-separated, e.g., @john, @sarah). Leave empty for no mentions."
}
```

## Execution (Pattern C: Action)

### Step 1: Run the Skill and Get Run ID

```bash
RESULT=$(refly skill run --id skpi-zktzbpe4r5cz4cq6opst7yl6 --input '{
  "channel_name": "#general",
  "message_content": "Hello team! This is an automated notification."
}')
RUN_ID=$(echo "$RESULT" | jq -r '.payload.workflowExecutions[0].id')
# RUN_ID is we-xxx format, use this for workflow commands
```

### Step 2: Open Workflow in Browser and Wait for Completion

```bash
open "https://refly.ai/workflow/c-k1lpwjqxvtnfs6t1l82bun9e"
refly workflow status "$RUN_ID" --watch --interval 30000
```

### Step 3: Confirm Action Status

```bash
# Confirm action completed
STATUS=$(refly workflow detail "$RUN_ID" | jq -r '.payload.status')
echo "Action completed with status: $STATUS"
```

## Expected Output

- **Type**: API Response
- **Format**: JSON message confirmation
- **Action**: Confirm message sent successfully

## Rules

Follow base skill workflow: `~/.claude/skills/refly/SKILL.md`
