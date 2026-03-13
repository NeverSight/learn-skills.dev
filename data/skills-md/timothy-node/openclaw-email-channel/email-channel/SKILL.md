---
name: email-channel
description: Send and receive emails via IMAP/SMTP. Use for email-based conversations, notifications, and automated replies.
homepage: https://github.com/timothy-node/openclaw-email-channel
metadata: { "openclaw": { "emoji": "📧", "requires": { "channel": "email" } } }
---

# Email Channel

Two-way email communication via IMAP/SMTP.

## When to Use

- User asks to send an email
- Responding to incoming emails (automatic)
- Sending notifications or reports via email

## Sending Emails

Use the `message` tool with `channel: "email"`:

```
message action=send channel=email target=recipient@example.com message="Your message here"
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `target` | Yes | Recipient email address |
| `message` | Yes | Email body (plain text or HTML) |
| `subject` | No | Email subject |
| `replyTo` | No | Message ID to reply to (maintains thread) |

### Examples

**Simple email:**
```
message action=send channel=email target=user@example.com message="Hello! This is a test."
```

**With subject:**
```
message action=send channel=email target=user@example.com subject="Weekly Report" message="Here's your summary..."
```

**Reply to thread:**
```
message action=send channel=email target=user@example.com replyTo=<message-id> message="Thanks for your question..."
```

## Receiving Emails

Emails from allowed senders automatically appear as user messages. The channel handles:

- IMAP polling at configured intervals
- Thread tracking via Message-ID/References headers
- Sender verification against allowlist

## Attachments

Incoming attachments are processed and available in the message context.

To send attachments, use `filePath` or `buffer`:

```
message action=send channel=email target=user@example.com message="See attached" filePath=/path/to/file.pdf
```

## Security Notes

1. Only addresses in `allowFrom` can trigger responses
2. Use `${ENV_VAR}` syntax for passwords in config
3. App passwords recommended over account passwords

## Troubleshooting

- **Email not received**: Check sender is in `allowFrom` list
- **Send failed**: Verify SMTP settings and credentials
- **Thread broken**: Ensure `replyTo` uses correct Message-ID format
