---
name: telegram-checker
description: Check Telegram for unanswered messages, find pending conversations, list unread chats. Use when user asks to check Telegram, find unanswered messages, see pending responses, or review Telegram inbox.
allowed-tools: Bash(python3 ~/.claude/skills/telegram-checker/scripts/check_messages.py:*)
---

# Telegram Message Checker

Check unanswered messages and manage Telegram conversations.

## First-time setup

Run once in terminal to authenticate:
```bash
python3 ~/.claude/skills/telegram-checker/scripts/check_messages.py
```
Enter your phone number and verification code when prompted. Session saves to ~/.telegram_checker_session

## Usage

```bash
python3 ~/.claude/skills/telegram-checker/scripts/check_messages.py
```

## Options

- `--limit N` - Max results (default 50)
- `--private` - Only private chats
- `--groups` - Only groups
- `--chat "Name"` - Filter by chat name
