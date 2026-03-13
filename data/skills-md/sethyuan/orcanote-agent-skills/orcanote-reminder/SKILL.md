---
name: orcanote-reminder
description: Guide for creating and managing reminders in Orca Note. Use this skill when the user wants to set a reminder or schedule a task.
---

# Orca Note Reminder Skill

This skill provides a standard workflow for creating reminders within Orca Note.

## Workflow

To create a reminder, follow these two steps:

1. **Insert Descriptive Content**: Use the `insert_markdown` tool to write the content of the reminder into the note.
2. **Tag the Reminder Block**: Use the `insert_tags` tool to apply a "Reminder" tag to the block, specifying its trigger time and recurrence properties.

## The Reminder Tag

The "Reminder" tag is used to define the scheduling logic. It supports the following properties:

| Property | Description | Required | Format/Units |
| :--- | :--- | :--- | :--- |
| `Date time` | The trigger date and time for the reminder. | **Yes** | Unix timestamp in seconds |
| `Repeat every` | The recurrence interval. Multiple intervals can be separated by commas (`,`). | No | `m,h,d,w,M,y` (min, hour, day, week, month, year) |
| `Repeat until` | The expiration date for recurring reminders. | No | Unix timestamp in seconds |

### Recurrence Units

When setting the `Repeat every` property, use these abbreviated units:
- `m`: Minute(s)
- `h`: Hour(s)
- `d`: Day(s) - e.g., `1d` for every day
- `w`: Week(s) - e.g., `1w` for every week
- `M`: Month(s) - e.g., `1M` for every month
- `y`: Year(s) - e.g., `1y` for every year

## Usage Examples

### Simple Reminder
1. `insert_markdown`: "Buy groceries"
2. `insert_tags`: `Reminder` with `Date time: 1771149600` (corresponds to 2026-02-15 18:00)

### Weekly Recurring Reminder
1. `insert_markdown`: "Team Sync Meeting"
2. `insert_tags`: `Reminder` with attributes:
   - `Date time`: `1770773400` (corresponds to 2026-02-11 09:30)
   - `Repeat every`: `"1w"`
   - `Repeat until`: `1798646400` (corresponds to 2026-12-31)
