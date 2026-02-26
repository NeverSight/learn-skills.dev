---
name: whatsapp-web-js
description: >-
  Provides expert guidance on WhatsApp Web JS, including how to use the WhatsApp Web JS API to send and receive messages, create groups, and more. Use when working with WhatsApp Web JS, WhatsApp Web JS API, or WhatsApp Web JS SDK.
---

# WhatsApp Web.js Expert Guidance

## Overview

WhatsApp-web.js is a Puppeteer-based library that automates a Chromium browser instance running WhatsApp Web. It provides a high-level API for interacting with WhatsApp programmatically. Understanding its browser-based nature is crucial for proper deployment and troubleshooting.

## Core Architecture Principles

**Browser automation foundation**: This library runs a real Chromium browser via Puppeteer. Consider memory implications for multi-client setups and ensure your deployment environment can handle headless browsers.

**Non-blocking initialization**: The `client.initialize()` method returns immediately. Always listen for the `ready` event before attempting to use client methods. Calling methods before the client is ready will result in errors.

**ID format conventions**: Phone numbers must follow specific formats without symbols. Private chats use `<country_code><phone>@c.us` (e.g., `5511999999999@c.us` for a Brazilian number). Groups use `<id>@g.us`, channels use `<id>@newsletter`, and status broadcasts use `status@broadcast`. Never include `+` or leading zeros in phone numbers.

## Authentication Strategy Selection

Choose authentication strategies based on deployment model:

- **NoAuth**: No session persistence. Requires QR scan on every restart. Use only for testing.
- **LocalAuth**: Saves session to local filesystem. Recommended for single-instance bots on persistent infrastructure. Sessions survive restarts.
- **RemoteAuth**: Saves session to external store (MongoDB, Redis, etc.). Required for cloud deployments, containerized environments, or multi-instance scenarios where filesystem is ephemeral.

**Pairing code alternative**: Instead of QR scanning, use `pairWithPhoneNumber` in ClientOptions to receive a pairing code via the target WhatsApp account. Useful for automated setups where QR display is impractical.

## Message Event Handling

**Critical distinction**: The `message` event fires only for incoming messages. The `message_create` event fires for all messages, including those sent by the bot itself. Use `message_create` when you need to log or process outbound messages, but be careful to avoid infinite loops when auto-replying.

**Message ID serialization**: When storing or referencing message IDs, always use `msg.id._serialized` for the string representation. The `id` object itself contains internal properties that shouldn't be used directly as identifiers.

## Media Operations

**Media download timing**: Only messages with `msg.hasMedia === true` can be downloaded. Always check this property before calling `msg.downloadMedia()` to avoid errors.

**Sticker conversion dependency**: Sending media as stickers (`sendMediaAsSticker: true`) requires `ffmpeg` to be installed and available on the system PATH. This is an external dependency not handled by npm.

**Media encoding**: MessageMedia stores file data as base64 in the `data` property. The `mimetype` must be accurate for WhatsApp to process the media correctly. When using `MessageMedia.fromUrl()`, the library attempts to detect mimetype automatically, but you can override with `unsafeMime: true` if needed.

## Group Management Constraints

**Admin requirement**: Operations like `setSubject()`, `removeParticipants()`, `setDescription()`, and permission changes require the bot to be a group admin. Attempting these operations without admin privileges will fail silently or throw errors.

**Private group invites**: When adding participants with `addParticipants()`, some users may require private invites (code 403 in result). The default behavior (`autoSendInviteV4: true`) automatically sends these invites, but you can disable this and handle manually if needed.

## Rate Limiting Awareness

**Bulk operation delays**: WhatsApp imposes rate limits on rapid-fire operations. When sending multiple messages or adding multiple group participants, add delays between operations (250-500ms minimum). The library provides sleep options in some methods like `addParticipants()` for this purpose.

**Temporary blocks**: Excessive rate limit violations can result in temporary blocks where WhatsApp prevents the account from sending messages for minutes to hours. Implement exponential backoff and respect rate limits in production.

## Message History Behavior

**Cache vs. history**: The `chat.fetchMessages({ limit })` method loads from the local cache maintained by the browser session. For full historical messages, call `chat.syncHistory()` first to sync with WhatsApp servers. This is especially important after authentication or when accessing older messages.

**Fetch limitations**: The `fetchMessages()` limit parameter controls how many messages to retrieve, but WhatsApp may return fewer if not all messages are cached locally. Always check the returned array length.

## Tool Creation Patterns

When wrapping client operations for AI agent tools:

**Normalize chat IDs**: Accept phone numbers with or without the `@c.us` suffix. Normalize by checking if `@` is present, and append `@c.us` if not.

**Return serialized IDs**: When returning message or chat references, use `_serialized` properties so the AI can reference them in subsequent operations.

**Handle async properly**: All client operations are async. Wrap in try-catch blocks and return meaningful error information to the AI agent, not just stack traces.

**Validate before operations**: Check prerequisites (e.g., `await client.isRegisteredUser(id)` before sending) to provide clear error messages rather than cryptic failures.

## Common Gotchas

**Status message target**: To post status updates (stories), send to the special chat ID `status@broadcast`, not a regular contact or group.

**Quote vs. Reply**: Using `msg.reply()` creates a quoted reply in the same chat. To quote a message but send to a different chat, use `client.sendMessage(otherChatId, content, { quotedMessageId: msg.id._serialized })`.

**Edit and delete timing**: Message edits have time limits imposed by WhatsApp (typically 15 minutes). Attempting to edit older messages will fail. Deletes for everyone also have time windows.

**Poll vote format**: When voting on polls with `msg.vote(selectedOptions)`, pass an array of option indices (0-based), not the option text strings.

**Memory management**: The browser instance accumulates memory over time. For long-running bots, monitor memory usage and consider periodic restarts or implement the `disconnected` event handler to gracefully restart the client.

## References

For detailed API information, method signatures, and comprehensive examples, see:

- **[references/detailed-guide.md](references/detailed-guide.md)** — Complete guide covering authentication setup, all messaging patterns (text, media, polls, reactions, locations), event handling, group/channel management, and practical examples for building AI agent tools. Consult this for specific method parameters, options objects, and advanced use cases.