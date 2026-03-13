---
name: macos-reminders
description: Create, list, and manage macOS Reminders via AppleScript. Use when the user asks to create a reminder, add a to-do, make a task, set a reminder for something, or anything involving Apple Reminders on macOS. Triggers on requests like "remind me to buy milk", "add a to-do to call the dentist", "create a reminder for Friday", "add to my shopping list", "flag this as important". macOS only.
license: MIT
compatibility: Requires macOS with Reminders.app. Uses osascript (AppleScript) and python3 for JSON parsing.
metadata:
  author: lucaperret
  version: "1.0.0"
  openclaw:
    os: macos
    emoji: "\U00002705"
    homepage: https://github.com/lucaperret/agent-skills
    requires:
      bins:
        - osascript
        - python3
---

# macOS Reminders

Manage Apple Reminders via `$SKILL_DIR/scripts/reminders.sh`. All date handling uses relative math (`current date + N * days`) to avoid locale issues (FR/EN/DE date formats).

## Quick start

### List reminder lists

Always list reminder lists first to find the correct list name:

```bash
"$SKILL_DIR/scripts/reminders.sh" list-lists
```

### Create a reminder

```bash
echo '<json>' | "$SKILL_DIR/scripts/reminders.sh" create-reminder
```

JSON fields:

| Field | Required | Default | Description |
|---|---|---|---|
| `name` | yes | - | Reminder title |
| `list` | no | default list | Reminder list name (from list-lists) |
| `body` | no | "" | Notes/details |
| `offset_days` | no | - | Due date as days from today (0=today, 1=tomorrow) |
| `iso_date` | no | - | Absolute due date `YYYY-MM-DD` (overrides offset_days) |
| `hour` | no | 9 | Due time hour (0-23) |
| `minute` | no | 0 | Due time minute (0-59) |
| `priority` | no | 0 | Priority: 0=none, 1=high, 5=medium, 9=low |
| `flagged` | no | false | Mark as flagged |

### List reminders

```bash
echo '<json>' | "$SKILL_DIR/scripts/reminders.sh" list-reminders
```

JSON fields:

| Field | Required | Default | Description |
|---|---|---|---|
| `list` | no | all lists | Filter by list name |
| `include_completed` | no | false | Include completed reminders |

## Interpreting natural language

Map user requests to JSON fields:

| User says | JSON |
|---|---|
| "remind me tomorrow at 2pm" | `offset_days: 1, hour: 14` |
| "remind me in 3 days" | `offset_days: 3` |
| "add to my shopping list" | `list: "Shopping"` (match closest list name) |
| "high priority" or "important" | `priority: 1, flagged: true` |
| "remind me on February 25 at 3:30pm" | `iso_date: "2026-02-25", hour: 15, minute: 30` |
| "remind me next Monday" | Calculate offset_days from today to next Monday |
| "flag this" | `flagged: true` |

For "next Monday", "next Friday" etc: compute the day offset using the current date. Use `date` command if needed:

```bash
# Days until next Monday (1=Monday)
target=1; today=$(date +%u); echo $(( (target - today + 7) % 7 ))
```

## Example prompts

These are real user prompts and the commands you should run:

**"Remind me to buy milk"**
```bash
"$SKILL_DIR/scripts/reminders.sh" list-lists
```
Then:
```bash
echo '{"name":"Buy milk","list":"Reminders"}' | "$SKILL_DIR/scripts/reminders.sh" create-reminder
```

**"Add a to-do to call the dentist tomorrow at 10am"**
```bash
echo '{"name":"Call the dentist","offset_days":1,"hour":10}' | "$SKILL_DIR/scripts/reminders.sh" create-reminder
```

**"Remind me to submit the report on February 28 — high priority"**
```bash
echo '{"name":"Submit the report","iso_date":"2026-02-28","hour":9,"priority":1,"flagged":true}' | "$SKILL_DIR/scripts/reminders.sh" create-reminder
```

**"Add eggs, bread, and butter to my shopping list"**
```bash
echo '{"name":"Eggs","list":"Shopping"}' | "$SKILL_DIR/scripts/reminders.sh" create-reminder
echo '{"name":"Bread","list":"Shopping"}' | "$SKILL_DIR/scripts/reminders.sh" create-reminder
echo '{"name":"Butter","list":"Shopping"}' | "$SKILL_DIR/scripts/reminders.sh" create-reminder
```

**"What's on my reminders?"**
```bash
echo '{}' | "$SKILL_DIR/scripts/reminders.sh" list-reminders
```

**"Show my work to-dos"**
```bash
echo '{"list":"Work"}' | "$SKILL_DIR/scripts/reminders.sh" list-reminders
```

## Critical rules

1. **Always list reminder lists first** if the user hasn't specified one — use the closest matching list name
2. **Never use hardcoded date strings** in AppleScript — always use `offset_days` or `iso_date`
3. **Confirm the list name** with the user if the intended list is ambiguous
4. **Pass JSON via stdin** — never as a CLI argument (avoids leaking data in process list)
5. **All fields are validated** by the script (type coercion, range checks, format validation) — invalid input is rejected with an error message
6. **All actions are logged** to `logs/reminders.log` with timestamp, command, list, and name
7. **Due date is optional** — reminders without a due date are valid (undated tasks)
8. **Multiple items**: when the user lists several items, create one reminder per item
