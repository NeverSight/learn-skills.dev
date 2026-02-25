---
name: telegram
description: |
  Send Telegram messages to users and groups. Use when:
  (1) Need to send a private DM to someone
  (2) Need to send a message to a group
  (3) Posting updates or status to Telegram
---

# Telegram

## CRITICAL: Finding Chat IDs

**Don't know a chat ID? Run this FIRST:**
```bash
openclaw sessions list
```
This shows ALL active chats. Look for `deliveryContext: telegram:<chat_id>` — extract the number.

**NEVER:**
- Use @usernames (they fail with "chat not found")
- Grep through files looking for IDs
- Ask the user for the ID
- Guess or make up IDs

**ALWAYS:**
- Run `openclaw sessions list` first
- Use the numeric ID from deliveryContext
- Save IDs to journal after you learn them

**ID format:**
- User IDs: positive numbers (e.g., `123456789`)
- Group IDs: negative numbers starting with `-100` (e.g., `-1001234567890`)

## Sending Messages

```bash
openclaw message send --channel telegram --target <CHAT_ID> --message "Your message"
```

## Behavior

- **Plain text only** — No markdown, no **, no _, no backticks
- Respond when mentioned or asked directly
- Add value or stay quiet
- Don't spam groups
