---
name: check-calendar-today
description: "Retrieve and display all calendar events scheduled for today. Use this skill when the user asks to check their calendar, see today's schedule, view appointments, or find out what events are coming up today. Works with the native Calendar application on macOS."
tags: [calendar, scheduling, productivity, macos, auto-generated]
version: 0.1.0
---

# Skill: check-calendar-today

## Overview

This skill queries the native macOS Calendar application to fetch all events occurring on the current date and displays them in a readable format.

## When to Use

Use this skill when the user asks to:
- Check their calendar for today
- See what's on their schedule
- View today's appointments or events
- Find out if they have any meetings scheduled
- Get a summary of today's calendar

## Procedure

1. Execute the AppleScript command to query the Calendar application for the current date
2. The script retrieves the start and end of the current day (midnight to 11:59 PM)
3. Iterate through all calendars and collect events that fall within today's time range
4. Format each event with its summary, start time, and end time
5. Return the formatted event list or a message indicating no events are scheduled
6. Display the results to the user in a clear, readable format

## Output

A text summary listing all calendar events for today with their titles, start times, and end times. If no events are scheduled, returns a message indicating an empty calendar.

## Reference Commands

Commands for executing this skill (adapt to actual inputs):

```bash
osascript -e 'tell application "Calendar" to set today to current date...'
```

Replace `{{PLACEHOLDER}}` values with actual credentials from the key store.

## Example

Example requests that trigger this skill:

```
what is on my calendar for today?
```

## Notes

- This skill requires access to the native macOS Calendar application
- The script automatically uses the current system date and time
- All calendars in the Calendar app are queried, not just the primary calendar


## Keywords

calendar, events, schedule, appointments, today, agenda, meetings
