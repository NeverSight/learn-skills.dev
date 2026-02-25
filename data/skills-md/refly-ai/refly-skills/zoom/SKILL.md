---
name: zoom
description: "Integrate with Zoom for video meetings. Use when you need to: (1) schedule Zoom meetings, (2) create instant meetings, or (3) manage meeting details and invitations programmatically."
version: 1.0.0
skillId: skp-j6gbs1kwum5hzso01vfqip48
workflowId: c-i7aldav874yefwaw38vhw1m6
installationId: skpi-t09brobxlux8m46nrtcg38ui
category: action
---

# Zoom

Integrate with Zoom for video meetings. Use when you need to: (1) schedule Zoom meetings, (2) create instant meetings, or (3) manage meeting details and invitations programmatically.

## Input

Provide input as JSON:

```json
{
  "meeting_topic": "The topic or title of the meeting",
  "meeting_date": "Meeting date and time (e.g., 2024-03-15 14:00)",
  "duration_minutes": "Meeting duration in minutes",
  "participant_emails": "Comma-separated list of participant email addresses",
  "meeting_agenda": "Meeting agenda or description"
}
```

## Execution (Pattern C: Action)

### Step 1: Run the Skill and Get Run ID

```bash
RESULT=$(refly skill run --id skpi-t09brobxlux8m46nrtcg38ui --input '{
  "topic": "Weekly Team Standup",
  "duration": "30",
  "start_time": "2024-01-15T10:00:00Z"
}')
RUN_ID=$(echo "$RESULT" | jq -r '.payload.workflowExecutions[0].id')
# RUN_ID is we-xxx format, use this for workflow commands
```

### Step 2: Open Workflow in Browser and Wait for Completion

```bash
open "https://refly.ai/workflow/c-i7aldav874yefwaw38vhw1m6"
refly workflow status "$RUN_ID" --watch --interval 30000
```

### Step 3: Confirm Action Status

```bash
# Confirm meeting created
STATUS=$(refly workflow detail "$RUN_ID" | jq -r '.payload.status')
echo "Action completed with status: $STATUS"
```

## Expected Output

- **Type**: API Response
- **Format**: JSON meeting details (join URL, meeting ID)
- **Action**: Confirm meeting created successfully

## Rules

Follow base skill workflow: `~/.claude/skills/refly/SKILL.md`
