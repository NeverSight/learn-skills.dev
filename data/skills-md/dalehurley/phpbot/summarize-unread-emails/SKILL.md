---
name: summarize-unread-emails
description: "Retrieve and summarize all unread emails from your inbox, organized by category, sender, and date. Use this skill when the user asks to summarize unread emails, get an overview of unread messages, organize inbox emails, or review pending email communications. Provides a structured summary with categorization and timeline analysis."
tags: [email, productivity, inbox-management, summarization, auto-generated]
version: 0.1.0
---

# Skill: summarize-unread-emails

## Overview

This skill accesses your email inbox via AppleScript (macOS Mail) or email API to retrieve unread messages and generate a comprehensive summary organized by category, sender, and recency.

## When to Use

Use this skill when the user asks to:
- Summarize unread emails
- Get an overview of unread messages
- Organize or review inbox emails
- See what emails are pending
- Categorize unread messages by type or sender

## Procedure

1. Execute AppleScript to retrieve all unread messages from the inbox: `osascript -e 'tell application "Mail" to set unreadMessages to (messages of inbox whose read status is false) | return count of unreadMessages'`
2. Extract email metadata (sender, subject, date received) for each unread message using AppleScript
3. Parse and organize emails into logical categories (Development, Bills, Family, Shopping, Appointments, Professional, Marketing, Government, Other)
4. Sort emails within each category by date received (most recent first)
5. Generate a formatted summary report with category headers, email counts, and timeline breakdown
6. Present summary to user with key insights and action items highlighted

## Output

A formatted text summary organized by category and date, including sender, subject, and date received for each unread email. Includes category totals, timeline breakdown, and visual formatting with emojis for easy scanning.

## Reference Commands

Commands for executing this skill (adapt to actual inputs):

```bash
osascript -e 'tell application "Mail" to set unreadMessages to (messages of inbox whose read status is false) | return count of unreadMessages'
osascript << 'EOF'
tell application "Mail"
    set unreadMessages to (messages of inbox whose read status is false)
    repeat with msg in unreadMessages
        set output to output & "From: " & (sender of msg) & return & "Subject: " & (subject of msg) & return & "Date: " & (date received of msg) & return & return
    end repeat
end tell
EOF
```

Replace `{{PLACEHOLDER}}` values with actual credentials from the key store.

## Example

Example requests that trigger this skill:

```
summarize my unread emails
```

## Notes

- This skill uses AppleScript and requires Mail.app to be running on macOS
- Large numbers of unread emails (100+) may take several seconds to process
- Emails are categorized based on subject line keywords and sender domain analysis
- The summary is generated locally and not stored or transmitted externally


## Keywords

unread, inbox, email summary, organize emails, pending messages, email overview
