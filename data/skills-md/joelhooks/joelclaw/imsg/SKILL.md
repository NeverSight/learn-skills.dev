---
name: imsg
displayName: iMessage
description: "iMessage/SMS CLI for listing chats, reading message history, watching for new messages, and sending messages. Triggers on: check messages, read imessage, send text, imsg, message history, sms, who texted me."
version: 1.0.0
author: Joel Hooks
tags: [joelclaw, messaging, imessage, sms, communication]
---

# iMessage

Read and send iMessages and SMS from the terminal via the `imsg` CLI.

## Setup (Panda)

- **Messages.app signed in as**: the agent Apple ID (see USER.md)
- **Joel's iMessage address**: see USER.md → `imessage`
- Full Disk Access must be granted to the terminal for **read** operations (`chats`, `history`, `watch`)
- Automation permission for Messages.app required for **send**
- `imsg send` returns `"sent"` optimistically — this means AppleScript fired, not delivery confirmed

## Commands

### List chats

```bash
imsg chats --limit 10 --json
```

### Read history

```bash
imsg history --chat-id <id> --limit 20 --attachments --json
```

### Watch for new messages

```bash
imsg watch --chat-id <id> --attachments
```

### Send

```bash
# By email (iMessage)
imsg send --to "user@example.com" --text "hello"

# By phone number (iMessage or SMS)
imsg send --to "+18005551234" --text "hello"

# With file attachment
imsg send --to "user@example.com" --text "see attached" --file /path/to/file.jpg
```

## Delivery Notes

- `"sent"` from CLI = AppleScript successfully handed off to Messages.app
- "Not delivered" in Messages.app = actual delivery failure (auth issue, recipient offline, etc.)
- Full Disk Access missing = read commands fail with `permissionDenied`; send still works via AppleScript
- Messages appear as coming from the agent Apple ID, not from Joel

## Sending to Joel

Joel's iMessage address is in USER.md (`imessage` field). Use it to notify him directly:

```bash
imsg send --to "<joel-imessage>" --text "your message"
```

## Safety

- Read-only by default — use `chats` and `history` before sending
- Always confirm recipient and message text before `imsg send`
- `--json` flag preferred for all read operations (deterministic parsing)

## Install

```bash
brew install steipete/tap/imsg
```

## Credit

CLI by [steipete](https://github.com/steipete/imsg). Adopted per ADR-0067.
