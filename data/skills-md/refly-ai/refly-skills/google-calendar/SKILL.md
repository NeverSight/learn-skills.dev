---
name: google-calendar
description: "Integrate with Google Calendar for scheduling. Use when you need to: (1) create calendar events, (2) manage schedules and appointments, or (3) automate calendar-based workflows."
version: 1.0.0
skillId: skp-x4o2qjfir2y5e50plhdwf4k3
workflowId: c-b7ypt79w572wlqnldxnrsemv
installationId: skpi-btib48o2jlex2rw3rs1gfgyx
category: action
---

# Google Calendar

Integrate with Google Calendar for scheduling. Use when you need to: (1) create calendar events, (2) manage schedules and appointments, or (3) automate calendar-based workflows.

## Input

Provide input as JSON:

```json
{
  "event_title": "Title of the calendar event",
  "event_description": "Description or notes for the event",
  "start_datetime": "Event start date and time (e.g., 2024-01-15 14:00)",
  "end_datetime": "Event end date and time (e.g., 2024-01-15 15:00)",
  "attendees": "Email addresses of attendees, separated by commas",
  "location": "Event location (physical address or virtual meeting link)"
}
```

## Execution (Pattern C: Action)

### Step 1: Run the Skill and Get Run ID

```bash
RESULT=$(refly skill run --id skpi-btib48o2jlex2rw3rs1gfgyx --input '{
  "title": "Project Review Meeting",
  "start_time": "2024-01-15T14:00:00",
  "duration": "60"
}')
RUN_ID=$(echo "$RESULT" | jq -r '.payload.workflowExecutions[0].id')
# RUN_ID is we-xxx format, use this for workflow commands
```

### Step 2: Open Workflow in Browser and Wait for Completion

```bash
open "https://refly.ai/workflow/c-b7ypt79w572wlqnldxnrsemv"
refly workflow status "$RUN_ID" --watch --interval 30000
```

### Step 3: Confirm Action Status

```bash
# Confirm event created
STATUS=$(refly workflow detail "$RUN_ID" | jq -r '.payload.status')
echo "Action completed with status: $STATUS"
```

## Expected Output

- **Type**: API Response
- **Format**: JSON event data (event ID, link)
- **Action**: Confirm event created successfully

## Rules

Follow base skill workflow: `~/.claude/skills/refly/SKILL.md`
