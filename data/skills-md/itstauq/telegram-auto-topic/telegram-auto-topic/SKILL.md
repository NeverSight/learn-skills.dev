---
name: telegram-auto-topic
description: >
  Add `/topic` to the start of any message in a Telegram forum group to
  auto-create a new topic from it. A title is generated automatically from
  the message content.
  Github: https://github.com/itstauq/telegram-auto-topic
metadata:
  openclaw:
    requires:
      config:
        - ~/.openclaw/openclaw.json
      env:
        - OPENCLAW_CONFIG
      bins:
        - curl
        - jq
---

# Telegram Auto-Topic

Add `/topic` to the start of any message in a Telegram forum group → a new topic is created from it. The title is figured out from your message automatically — no need to think of one yourself.

### Example

**1.** You send a message starting with `/topic`:
> /topic @your_bot I need to look into renewing my passport before March

**2.** A new forum topic **"Passport Renewal Before March"** is created with your message quoted inside it. You get a reply linking directly to the new topic.

## Prerequisites

- The group must be configured in OpenClaw (`channels.telegram.groups.<CHAT_ID>`) — this is how OpenClaw knows to process messages from it.
- The group must have **forum/topics** enabled.
- Your bot must be an admin in the group with **Manage Topics** permission.

## Handling /topic

When a message starts with `/topic`:

1. Generate a concise 3-7 word title summarising the message.
2. Run the script — replace placeholders with actual values from the message context:
   ```
   scripts/telegram-auto-topic.sh <chat_id> <message_id> "<sender name>" "<title>" "<text after /topic>"
   ```
   Pass an empty string for the text arg if there's no text (e.g. media-only).
   Use the path relative to this skill's directory.
3. The script returns JSON with `topic_id`, `title`, and `link`.
4. Reply to the original message with: `Topic created → [<title>](<link>)`
5. Then send a response to the actual message content in the NEW topic (use message tool with `threadId` from the returned `topic_id`). Respond naturally as you would to any message.
6. After both replies are sent, respond with NO_REPLY.

## How It Works

1. You send a message starting with `/topic`
2. A new forum topic is created — titled from your message automatically
3. Your message is quoted in the new topic with your name
4. You get a reply with a clickable link to the new topic
5. The bot responds to your message in the new topic

Works with media too — photos, videos, or documents with `/topic` in the caption get forwarded into the new topic.

## Script Reference

```bash
scripts/telegram-auto-topic.sh <chat_id> <message_id> <sender> [title] [text]
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chat_id` | arg | yes | Supergroup chat ID (negative number) |
| `message_id` | arg | yes | Original message to quote |
| `sender` | arg | yes | Display name of original sender |
| `title` | arg | no | Topic title. Falls back to first ~50 chars of text if omitted |
| `text` | arg | no | Message body after `/topic`. If empty, forwards as media |

Returns JSON: `{"topic_id": 123, "title": "Used title", "link": "https://t.me/c/..."}`

## Optional configuration

**Skip the @bot mention** — by default, the bot only responds when mentioned. To use `/topic` without mentioning the bot:

```json
"channels.telegram.groups.<CHAT_ID>": {
  "requireMention": false
}
```

**Telegram autocomplete** — to get `/topic` in Telegram's command menu, add under `channels.telegram`:

```json
{
  "customCommands": [
    {
      "command": "topic",
      "description": "Create a new forum topic from a message"
    }
  ]
}
```

## Limitations

- **Attribution:** Quoted messages appear as sent by the bot (Telegram API limitation). Sender name is included as attribution text below the quote.
- **Media:** Forwarded media shows a "Forwarded from" header — best available but not native.
- **Forum groups only:** Won't work in regular groups or DMs.
- **Permissions:** Bot needs admin with Manage Topics.
- **Title length:** Telegram caps topic names at 128 characters.
