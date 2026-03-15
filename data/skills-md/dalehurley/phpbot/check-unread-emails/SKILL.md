---
name: check-unread-emails
description: "Check and summarize unread emails in your inbox, highlighting urgent messages, appointments, and items needing action. Use this skill when the user asks to check emails, review unread messages, see what emails need attention, or get an email summary. Automatically categorizes emails by priority, sender type, and action required."
tags: [email, inbox, communication, productivity, notifications, auto-generated]
version: 0.1.0
---

# Skill: check-unread-emails

## Overview

This skill retrieves and analyzes unread emails from your inbox, organizing them by urgency and category. It provides a prioritized summary of messages requiring immediate attention, appointments, financial updates, and promotional content that can be archived.

## When to Use

Use this skill when the user asks to:
- Check unread emails
- Review new emails
- See what emails need attention
- Get an email summary
- Check inbox for important messages
- See recent emails from the last 7 days

## Input Parameters

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `days_back` | No | Number of days to look back for recent emails (default: 7) | 7 |
| `max_results` | No | Maximum number of emails to retrieve (default: 30) | 30 |

## Procedure

1. Execute the bundled script `check_new_emails.py` to retrieve the total unread email count from the system mail client
2. Execute the bundled script `get_recent_emails.py` to fetch detailed information about the 30 most recent unread emails from the last 7 days
3. Parse email metadata including subject, sender, date received, and preview content
4. Categorize emails by type: urgent/action-required, appointments, financial, work/development, promotional, and personal
5. Identify priority items based on keywords (security, urgent, action required, confirmation, etc.)
6. Format and present the summary to the user with emoji indicators for urgency levels
7. Offer to help with any of the top priority items

## Output

A formatted summary report including: total unread count, emails organized by category (urgent, appointments, financial, work, promotional), sender information, dates, and recommended actions. Includes emoji indicators for priority levels and a top 3 priorities list.

## Bundled Scripts

| Script | Type | Description |
|--------|------|-------------|
| `scripts/check_new_emails.py` | PY | Auto-captured from task execution |
| `scripts/get_recent_emails.py` | PY | Auto-captured from task execution |

Credentials in scripts use environment variables. Set them via `get_keys` before running.

## Reference Commands

Commands for executing this skill (adapt to actual inputs):

```bash
python3 /tmp/check_new_emails.py
python3 /tmp/get_recent_emails.py
```

Replace `{{PLACEHOLDER}}` values with actual credentials from the key store.

## Example

Example requests that trigger this skill:

```
check my unread emails and let me know what needs my attention
```

## Notes

- Requires access to the system mail client (Mail.app on macOS)
- Uses AppleScript to query the inbox, which may require accessibility permissions
- Emails are categorized automatically based on sender domain and subject keywords
- Promotional emails are flagged for archiving but not deleted
- The skill respects email read/unread status and does not modify it


## Keywords

inbox, unread, new messages, email summary, urgent emails, check mail, email review
