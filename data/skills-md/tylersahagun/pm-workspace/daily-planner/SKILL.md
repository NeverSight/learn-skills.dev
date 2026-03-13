---
name: daily-planner
description: Generate daily focus by pulling from Google Calendar, Google Tasks, Slack, Linear, and PM workspace initiatives. Use for /morning command or daily planning.
---

# Daily Planner Skill

Procedural knowledge for generating a prioritized daily focus view.

## When to Use

- Running `/morning` command
- Running `/block [task] [duration]` command
- Answering "what should I do today?"
- Daily planning at start of day

## Prerequisites

Requires MCP tools from multiple servers:

### Google MCP (`google`)

- `GOOGLESUPER_LIST_EVENTS` - Get calendar events
- `GOOGLESUPER_CREATE_EVENT` - Create focus time blocks
- `GOOGLESUPER_LIST_ALL_TASKS` - Get Google Tasks
- `GOOGLESUPER_UPDATE_TASK` - Mark tasks complete

### Slack MCP (via Composio)

- Slack monitor subagent or `SLACK_FETCH_CONVERSATION_HISTORY`

### Linear MCP (`linear`)

- `LINEAR_SEARCH_ISSUES` - Get Tyler's assigned issues

### Local Data

- `pm-workspace-docs/roadmap/roadmap.json` - Initiative priorities and next_actions

## Daily Planning Procedure

### Step 1: Pull Calendar Events

```
1. Call GOOGLESUPER_LIST_EVENTS for today
   - calendarId: "primary"
   - timeMin: start of today (ISO8601)
   - timeMax: end of today (ISO8601)
2. Extract: start time, end time, title, attendees
3. Calculate available focus blocks (gaps between meetings)
```

### Step 2: Pull Google Tasks

```
1. Call GOOGLESUPER_LIST_ALL_TASKS
   - showCompleted: false
   - showHidden: false
2. Filter by due date (today or overdue)
3. Group by task list (Personal, Work-Quick, Habits)
```

### Step 3: Run Slack Monitor

```
1. Invoke slack-monitor subagent or check state file
2. Get messages requiring response:
   - Direct mentions
   - DMs from leadership
   - Product discussions needing input
3. Classify by priority
```

### Step 4: Extract Initiative Actions

```
1. Read pm-workspace-docs/roadmap/roadmap.json
2. Filter initiatives where owner = "Tyler" or "tyler"
3. Filter by priority: P0 and P1 only
4. Extract next_action field
5. Check for blockers requiring action
```

### Step 5: Prioritize and Generate Output

Priority order:

1. **Blockers** - Things blocking others
2. **Calendar-bound** - Meetings and deadlines
3. **P0 initiative actions** - Highest priority work
4. **Slack responses** - Communication debt
5. **P1 initiative actions** - Important but not urgent
6. **Personal tasks** - From Google Tasks

## Task Routing Guidance (Reference Only)

When deciding where work should live, prefer the defaults in
`pm-workspace-docs/workflows/workspace-config.yaml` under `task_routing`.

- **Linear:** Cross-team work, engineering handoffs, or anything that should
  be tracked in sprint/project metrics.
- **Google Tasks:** Personal or life-admin items, quick follow-ups that do
  not require team visibility.
- **PM workspace docs:** PRDs, research, design briefs, eng specs, prototype
  notes, and decision logs (use templates listed in `task_routing.templates`).

## Output Format

### Today File (`pm-workspace-docs/status/today.md`)

```markdown
# Today: {Day of Week} {Month} {Day}

## Calendar ({count} events)

- {start}-{end} - {title}
- {start}-{end} - {title}

## Priority Actions (P0/P1 only)

1. [{est}] {action} ({initiative})
2. [{est}] {action} ({initiative})
3. [{est}] {action} ({initiative})

## Personal Tasks (Google Tasks)

- [ ] {task from Personal list}
- [ ] {task from Work-Quick list}

## Slack Requiring Response

- {count} messages in #{channel} from {who}
- {count} DMs from {who}

## Focus Blocks Available

- {start}-{end} ({duration} deep work)
- {start}-{end} ({duration} deep work)

---

_Generated: {timestamp}_
_Run `/morning` to regenerate_
```

## Time Blocking Procedure

### `/block [task] [duration]` Command

```
1. Parse task description and duration (e.g., "2h", "45m")
2. Call GOOGLESUPER_LIST_EVENTS to find next available slot
3. Create event with:
   - summary: "Focus: {task}"
   - description: "Protected time for: {task}"
   - eventType: "focusTime" (if supported)
   - start/end: calculated from available slot
4. Confirm creation to user
```

### `/protect [hours]` Command

```
1. Parse hours requested per day
2. For each day in current week:
   - Find gaps in calendar
   - Create focus time blocks
3. Report total protected time created
```

## MCP Tool Reference

### GOOGLESUPER_LIST_EVENTS

```json
{
  "calendarId": "primary",
  "timeMin": "2026-01-31T00:00:00-07:00",
  "timeMax": "2026-01-31T23:59:59-07:00",
  "singleEvents": true,
  "orderBy": "startTime"
}
```

### GOOGLESUPER_CREATE_EVENT

```json
{
  "calendarId": "primary",
  "summary": "Focus: Advance flagship-meeting-recap",
  "description": "Protected deep work time",
  "start": {
    "dateTime": "2026-01-31T11:00:00-07:00",
    "timeZone": "America/Denver"
  },
  "end": {
    "dateTime": "2026-01-31T13:00:00-07:00",
    "timeZone": "America/Denver"
  },
  "eventType": "focusTime"
}
```

### GOOGLESUPER_LIST_ALL_TASKS

```json
{
  "showCompleted": false,
  "showHidden": false
}
```

## Integration Points

### With Slack Monitor

- Daily planner calls slack-monitor for priority messages
- Or reads from `status/slack/.slack-monitor-state.json`

### With Team Dashboard

- `/morning` shows Tyler's work from `/team tyler`
- Avoids duplicate MCP calls when possible

### With Portfolio Status

- Reads from `roadmap.json` for initiative priorities
- Uses same data structure as `/status-all`

## Error Handling

### No Calendar Access

```
⚠️ Google Calendar not accessible.

Calendar events will not be shown. Check MCP configuration.

Continuing with other sources...
```

### No Tasks

```
ℹ️ No Google Tasks found for today.

Either no tasks are due, or Google Tasks is not configured.
Consider adding tasks via Google Tasks app or web.
```

## Tyler's Daily Ritual (Recommended)

**8:30am:**

```
/morning
```

- Review today.md
- Adjust priorities if needed
- Identify biggest blocker to tackle first

**9:00am:**

```
/triage
```

- Process morning Slack/email batch
- Respond to urgent items
- Schedule non-urgent items

**2:00pm:**

```
/triage
```

- Process afternoon batch
- Clear communication debt

**5:30pm:**

```
/eod --digest
```

- Capture what shipped
- Prep for tomorrow

## Response Format

After generating the daily plan:

1. Display the formatted today.md content
2. Highlight top 3 priorities
3. Note any blockers that need immediate attention
4. Offer to create time blocks for focus work
