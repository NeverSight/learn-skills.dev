---
name: poke-assistant
description: Send messages and notifications to Poke (poke.com) via webhook API. Use when alerting the user, sending task completion notifications, status updates, reminders, or any message to their Poke assistant.
---

# Poke Assistant

## Overview

Send messages to your Poke assistant via the inbound webhook API. Poke is a conversational AI assistant that supports iMessage, SMS, and WhatsApp messaging. This skill enables Claude to send you notifications, alerts, and updates directly to your Poke.

## When to Use

- Notifying the user when a long-running task completes
- Sending error alerts or warnings that need attention
- Providing status updates on build, test, or deployment progress
- Sending reminders or summaries
- Alerting about important events (CI failures, security issues, etc.)

## Prerequisites

- Poke account at [poke.com](https://poke.com)
- `POKE_API_KEY` environment variable

## Installation

### Getting Your API Key

1. Go to [poke.com/settings](https://poke.com/settings)
2. Navigate to the **Advanced** section
3. Generate or copy your API key
4. Add to your shell profile:

```bash
echo 'export POKE_API_KEY="your-api-key"' >> ~/.zshrc
source ~/.zshrc
```

## Quick Start

Send a simple message:

```bash
python scripts/send_message.py -m "Hello from Claude Code!"
```

Pipe content to Poke:

```bash
echo "Build completed successfully" | python scripts/send_message.py
```

## Command Reference

```
python scripts/send_message.py [options]

Options:
  -m, --message TEXT    Message to send to Poke
  -v, --verbose         Show detailed output
  -h, --help            Show help message

Input:
  Message can be provided via -m flag or piped to stdin.
  If both are provided, -m takes precedence.

Exit codes:
  0  Success
  1  Missing message or API key
  2  API error (authentication, rate limit, etc.)
  3  Network error
```

## Examples

### Task Completion Alert

```bash
python scripts/send_message.py -m "Build completed: 42 tests passed, 0 failed"
```

### Error Notification

```bash
python scripts/send_message.py -m "ERROR: Deployment to production failed. Check logs."
```

### Pipe Command Output

```bash
git log --oneline -5 | python scripts/send_message.py -m "Recent commits:
$(cat)"
```

### Status Update with Details

```bash
python scripts/send_message.py -m "Code review complete:
- 3 files changed
- 2 suggestions made
- Ready for merge"
```

### Alert on Test Failure

```bash
npm test || python scripts/send_message.py -m "Tests failed! Check the output."
```

## Workflow Integration

### Notify After Long Tasks

When running tasks that take time, notify on completion:

```bash
# Run build and notify
npm run build && python scripts/send_message.py -m "Build finished successfully" \
  || python scripts/send_message.py -m "Build failed!"
```

### Daily Summary

Send a summary of work done:

```bash
python scripts/send_message.py -m "Daily summary:
- Implemented user auth
- Fixed 3 bugs
- Updated documentation"
```

## Best Practices

### When to Send Notifications

- Tasks taking longer than 2-3 minutes
- Errors requiring user attention
- Important milestones (deployment, release)
- Security-related alerts

### When NOT to Send

- Routine operations that complete quickly
- Every small step (avoid notification fatigue)
- Sensitive information (credentials, tokens)

### Message Guidelines

- Keep messages concise but informative
- Include actionable context (what happened, what to do)
- Use clear formatting for multi-line messages

## Troubleshooting

### "POKE_API_KEY environment variable not set"

Set your API key:
```bash
export POKE_API_KEY="your-api-key"
```

Or add to `~/.zshrc` for persistence.

### "API returned 401: Unauthorized"

Your API key is invalid or expired. Generate a new one at [poke.com/settings](https://poke.com/settings).

### "API returned 429: Too Many Requests"

You're being rate limited. Wait a few minutes before sending more messages.

### "Network error: Connection refused"

Check your internet connection. The Poke API requires network access.

### Message not appearing in Poke

- Verify your API key is correct
- Check that messaging is enabled in your Poke settings
- Ensure your messaging channel (iMessage/SMS/WhatsApp) is configured
