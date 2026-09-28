---
name: postlake-inbox
description: Read and handle PostLake direct-message conversations across Facebook, Instagram, X, and Bluesky. Use when checking DMs, reading a thread, marking it read, drafting a reply, or sending an approved reply.
---

# PostLake: unified inbox

Use PostLake's normalized inbox instead of calling four network APIs.

## Start safely

1. Call `list_social_accounts` to identify the connection.
2. Call `get_platform_capabilities` if you do not know whether that connection supports messaging.
3. Call `list_conversations`, optionally filtered by `account`.
4. Check `problems` before claiming there are no messages.
5. Call `read_conversation` with both the conversation id and account id.
6. Draft a concise reply. Do not send until the user has asked you to send it.
7. Call `send_message`, then `mark_conversation_read` after the thread is handled.

Conversation ids are scoped to one connected account. Never guess the account
or reuse a conversation id with another connection.

## REST equivalents

| Action | REST endpoint |
| --- | --- |
| List conversations | `GET /v1/conversations` |
| Find or open a thread | `POST /v1/conversations` with `account` and `handle` |
| Read messages | `GET /v1/conversations/{id}/messages?account=acc_...` |
| Mark read | `POST /v1/conversations/{id}/read` |
| Send a message | `POST /v1/conversations/{id}/messages` |

All REST requests use `Authorization: Bearer $POSTLAKE_API_KEY`. Reading,
marking, and sending require the connected `account` id because a conversation
id has meaning only within that connection.

## What the response means

- `fromMe` identifies which side sent a message. Do not infer this from handles.
- `content` can describe an attachment, shared media, or an unsupported provider
  payload. Do not claim that an empty `text` means the message itself was empty.
- The optional shape is
  `{ "kind": "attachment" | "shared_media" | "unsupported", "label": "...", "url": "..." | null }`.
- A `problems` entry means PostLake could not read a network. Report it. An empty
  `items` array without a problem means the network answered with no threads.
- Cursors are opaque. Pass them back exactly as returned.

## Network rules

- Facebook and Instagram can produce `message.received` webhooks.
- X and Bluesky require polling with `list_conversations`.
- Sending a direct message on X costs 6 credits. Messaging on the other
  currently supported inbox networks does not spend credits.
- Meta normal replies must be within 24 hours of the person's last message.
- Never send `humanAgent: true` from an autonomous workflow. It asserts that a
  person wrote the reply, and Meta can penalize the connected account when that
  assertion is false. MCP deliberately does not expose this override.
- Bluesky app passwords need direct-message access enabled when created.
- Facebook and Instagram messaging may be unavailable until Meta grants the
  required permission to the connected business.

## Supported boundary

PostLake currently exposes inbox messaging for Facebook, Instagram, X, and
Bluesky. LinkedIn, TikTok, Threads, YouTube, and Pinterest do not provide a
usable creator DM API for this product.

Docs: https://docs.postlake.dev/messages
MCP: https://api.postlake.dev/mcp
