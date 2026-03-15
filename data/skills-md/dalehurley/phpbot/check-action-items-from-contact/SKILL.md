---
name: check-action-items-from-contact
description: "Search email inbox for messages from a specific contact and extract action items, tasks, and requests. Use this skill when the user asks to check what someone needs them to do, find tasks from a specific person, review emails from a contact, or identify pending action items from someone. Analyzes email content to distinguish between urgent requests, actionable tasks, and informational messages."
tags: [email, task-management, action-items, contact-search, inbox, auto-generated]
version: 0.1.0
---

# Skill: check-action-items-from-contact

## Overview

This skill searches your email inbox for messages from a specified contact and analyzes them to extract action items, tasks, and requests. It categorizes findings by urgency and actionability, helping you quickly identify what needs to be done.

## When to Use

Use this skill when the user asks to:
- Check what someone needs them to do
- Find tasks or action items from a specific contact
- Review emails from a particular person
- Identify pending requests from someone
- Search for messages from a contact and extract next steps

## Input Parameters

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `contact_name` | Yes | The name of the contact to search for in the inbox | Nicole |

## Procedure

1. Get the contact name from the user if not provided (use `ask_user`)
2. Execute the bundled AppleScript to search the Mail inbox for all messages from the specified contact
3. Parse the returned email list to extract sender, subject, date, and content
4. Analyze each email to identify action items, tasks, and requests
5. Categorize findings as URGENT (immediate action needed), ACTIONABLE (tasks to complete), or FYI (informational only)
6. Compile results with clear summaries of what the contact needs from the user
7. Present findings in priority order with specific next steps

## Output

A formatted summary document listing all action items from the contact, organized by urgency level (URGENT, ACTIONABLE, FYI), with specific tasks, email dates, and recommended next steps.

## Reference Commands

Commands for executing this skill (adapt to actual inputs):

```bash
osascript << 'EOF'
use framework "Foundation"
use scripting additions

tell application "Mail"
    set allMessages to (every message of inbox)
    set contactEmails to {}
    
    repeat with msg in allMessages
        set senderName to extract name from sender of msg
        if senderName contains "{{CONTACT_NAME}}" then
            set emailInfo to "FROM: " & senderName & return & "SUBJECT: " & (subject of msg) & return & "DATE: " & (date received of msg) & return & "CONTENT: " & (content of msg) & return & "---END EMAIL---" & return & return
            set end of contactEmails to emailInfo
        end if
    end repeat
    return contactEmails
end tell
EOF
```

Replace `{{PLACEHOLDER}}` values with actual credentials from the key store.

## Example

Example requests that trigger this skill:

```
what does Nicole need me to do?
```

## Notes

- This skill searches all emails (read and unread) from the specified contact
- Action items are identified through keyword analysis (pay, submit, send, review, etc.)
- Results are automatically prioritized by urgency and recency
- Contact name matching is case-insensitive


## Keywords

action items, tasks, requests, contact, email search, pending work, to-do, follow-up
