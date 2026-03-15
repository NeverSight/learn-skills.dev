---
name: extract-email-actions-to-reminders
description: "Analyze recent emails to identify action items and automatically create prioritized reminders in the Reminders app. Use this skill when the user asks to convert emails into to-do items, create reminders from email, organize email tasks, or build a task list from inbox messages. Scans for action keywords like 'pay', 'review', 'urgent', 'deadline', 'invoice', and 'approval' to intelligently extract actionable items."
tags: [email, task-management, automation, reminders, productivity, auto-generated]
version: 0.1.0
---

# Skill: extract-email-actions-to-reminders

## Overview

This skill bridges email and task management by analyzing your recent emails, identifying action items based on keywords and context, and automatically creating organized reminders with priority levels and detailed notes.

## When to Use

Use this skill when the user asks to:
- Convert emails into a to-do list
- Create reminders from recent emails
- Extract action items from inbox
- Organize email tasks by priority
- Build a task list from email messages
- Scan emails for deadlines and action items

## Input Parameters

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `email_count` | No | Number of most recent emails to analyze | 100 |
| `list_name` | No | Name of the Reminders list to create or use | Email To-Dos |

## Procedure

1. Scan the user's Mail library to locate the 100 most recent .emlx files, sorted by modification date
2. Parse each email file to extract subject, sender, date, and body content
3. Apply action-detection patterns to identify emails containing action keywords (pay, review, urgent, invoice, deadline, approval, etc.)
4. Categorize identified action items by priority (high, medium, low) based on urgency indicators
5. Create or use existing "Email To-Dos" list in the Reminders app via AppleScript
6. Add each reminder with title, detailed notes (including sender and date), and priority level
7. Generate a summary markdown document on the Desktop listing all created reminders by priority
8. Open the Reminders app to display the newly created list

## Output

A new or updated Reminders list containing prioritized reminder items with detailed notes, plus a markdown summary document saved to the Desktop listing all extracted action items organized by priority level.

## Bundled Scripts

| Script | Type | Description |
|--------|------|-------------|
| `scripts/create_reminders.sh` | SH | Auto-captured from task execution |

Credentials in scripts use environment variables. Set them via `get_keys` before running.

## Reference Commands

Commands for executing this skill (adapt to actual inputs):

```bash
find {{MAIL_DIR}} -name "*.emlx" -type f | head -{{EMAIL_COUNT}}
python3 {{PARSE_EMAILS_SCRIPT}}
osascript {{CREATE_REMINDERS_SCRIPT}}
open -a Reminders
```

Replace `{{PLACEHOLDER}}` values with actual credentials from the key store.

## Example

Example requests that trigger this skill:

```
go through my recent emails and create a to-do list in reminders
```

## Notes

- Email parsing uses .emlx format from macOS Mail library; may not work with other email clients
- Action detection uses keyword patterns; some emails may be missed or incorrectly flagged
- Reminders are created with sender and date information in notes for easy reference back to original email
- High-priority items are identified by keywords like 'urgent', 'asap', 'action required', and 'due today'
- The script creates a summary markdown file on Desktop for offline reference


## Keywords

email, action items, to-do, reminders, task extraction, inbox, priority, deadline, organize
