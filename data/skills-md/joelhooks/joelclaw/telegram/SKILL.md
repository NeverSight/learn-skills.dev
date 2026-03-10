---
name: telegram
description: Operate the joelclaw Telegram channel — primary mobile interface between Joel and the gateway. Covers grammy Bot API, text/media/reactions, inline buttons, callbacks, and streaming.
---

# Telegram Channel Skill

Operate the joelclaw Telegram channel — the primary mobile interface between Joel and the gateway agent. Built on grammy (Bot API wrapper), supports text, media, reactions, replies, inline buttons, callbacks, and streaming.

## Architecture

```
Joel (Telegram app)
  → Bot API (long polling via grammy)
    → telegram.ts channel adapter
      → enrichPromptWithVaultContext()
        → command-queue → pi session
          → outbound router → telegram.ts send → Bot API → Joel
```

**Key files:**
- `packages/gateway/src/channels/telegram.ts` — channel adapter (inbound + outbound)
- `packages/gateway/src/telegram-stream.ts` — streaming UX (progressive text updates)
- `packages/gateway/src/outbound/router.ts` — response routing
- `packages/gateway/src/channels/types.ts` — `Channel` interface

**SDK:** `grammy@1.40.0` — Bot instance at module scope, exposed via `getBot()`.

Multi-instance poll ownership (2026-03-05): Telegram long polling now uses a Redis lease per bot token hash.

- Owner key: `joelclaw:gateway:telegram:poll-owner:<tokenHash>`
- Status key: `joelclaw:gateway:telegram:poll-status:<tokenHash>`
- Only owner polls `getUpdates`; non-owners stay passive/send-only and retry lease acquisition with backoff.

Conflict guard still applies for non-cooperative pollers: `telegram.channel.start_failed` (with `conflict` metadata) + `telegram.channel.retry_scheduled` + `telegram.channel.polling_recovered`.

## Capabilities

### Sending Messages

```typescript
// Via channel adapter
await telegramChannel.send("telegram:7718912466", "Hello", { format: "html" });

// Direct grammy API (from telegram-stream or daemon)
const bot = getBot();
await bot.api.sendMessage(chatId, text, { parse_mode: "HTML" });
```

- Max message length: **4096 chars** (Telegram API limit)
- Chunking: `TelegramConverter.chunk()` for HTML-aware splitting, `chunkMessage()` for raw text
- Format: markdown→HTML via `TelegramConverter.convert()`, with plain text fallback on validation failure
- Buttons: `InlineButton[][]` → `inline_keyboard` reply markup

### Reactions (ADR-0162)

```typescript
// grammy API
await bot.api.setMessageReaction(chatId, messageId, [
  { type: "emoji", emoji: "👍" }
]);
```

Telegram supports a [fixed set of emoji reactions](https://core.telegram.org/bots/api#reactiontypeemoji). Common ones: 👍 👎 ❤️ 🔥 🎉 🤔 👀 ✅ ❌ 🤯 💯

**Agent convention:** Include `<<react:EMOJI>>` at the start of a response. The outbound router strips it and calls `setMessageReaction` before sending text.

### Replies

```typescript
// grammy API — reply to a specific message
await bot.api.sendMessage(chatId, text, {
  reply_parameters: { message_id: targetMessageId }
});
```

Already wired in the adapter via `RichSendOptions.replyTo`. The agent uses `<<reply:MSG_ID>>` directive.

### Media

Supports photo, video, audio, voice, and document sending/receiving:

```typescript
// Send
await telegramChannel.sendMedia(chatId, "/path/to/file.jpg", { caption: "Look at this" });

// Receive — handled by bot.on("message:photo") etc.
// Downloads via Bot API getFile → local /tmp/joelclaw-media/
// Emits media/received Inngest event for pipeline processing
```

File size limit: 20MB download via Bot API (larger files need direct Telegram API).

### Streaming (ADR-0160)

Progressive text updates with cursor:

```typescript
import { begin, pushDelta, finish, abort } from "./telegram-stream";

// On prompt dispatch
begin({ chatId, bot, replyTo });

// On each text_delta event
pushDelta(delta);

// On message_end
await finish(fullText);
```

- Plain text during streaming (no parse_mode) — avoids broken HTML on partial content
- HTML formatting only on `finish()` — final edit with `parse_mode: "HTML"`
- Throttled edits: 800ms minimum between API calls
- Cursor: ` ▌` appended during streaming, removed on finish
- `initialSendPromise` awaited in `finish()` to prevent race conditions

### Inline Buttons & Callbacks (ADR-0070)

```typescript
// Send message with buttons
await sendTelegramMessage(chatId, "Choose:", {
  buttons: [
    [{ text: "✅ Approve", action: "approve:item123" }],
    [{ text: "❌ Reject", action: "reject:item123" }],
  ]
});

// Callback handler fires telegram/callback.received Inngest event
// Then edits message to show action taken + removes buttons
```

Callback data max: 64 bytes. Format: `action:context`.

### Commands

- `/stop` — abort current turn without killing the daemon.
- `/esc` — alias for `/stop`.
- `/kill` — hard stop: disables launchd service + kills process. Emergency use only.

## Configuration

Currently via environment variables (migrating to `~/.joelclaw/channels.toml` per ADR-0162):

| Env Var | Purpose |
|---------|---------|
| `TELEGRAM_BOT_TOKEN` | Grammy bot token |
| `TELEGRAM_USER_ID` | Joel's Telegram user ID (only authorized user) |

## Security

- **Single-user lockdown** — middleware drops all messages from users other than `TELEGRAM_USER_ID`
- **No token in config** — `channels.toml` references `agent-secrets` key names, not raw tokens
- **Media downloads** to `/tmp/joelclaw-media/` with UUID filenames (no path traversal)

## Troubleshooting

### Bot not receiving messages
1. Check gateway is running: `cat /tmp/joelclaw/gateway.pid && ps aux | grep daemon.ts`
2. Check Telegram polling started: `grep "telegram.*started" /tmp/joelclaw/gateway.log`
3. Verify token: `curl https://api.telegram.org/bot<TOKEN>/getMe`
4. Check polling errors in stderr: `rg "telegram.channel.start_failed|failed to start polling|getUpdates" /tmp/joelclaw/gateway.err`
5. Check ownership lifecycle telemetry:
   - `joelclaw otel search "telegram.channel.poll_owner" --hours 1`
   - `joelclaw otel search "telegram.channel.retry_scheduled" --hours 1`

If you see repeated 409 conflicts, another **bot process** is polling the same token. Telegram phone/desktop apps are not Bot API pollers and do not cause `getUpdates` contention.

### Messages arriving but no response
1. Check command queue: `grep "command-queue\|enqueue" /tmp/joelclaw/gateway.log | tail -10`
2. Check pi session health: `grep "session\|prompt" /tmp/joelclaw/gateway.log | tail -10`
3. Check outbound routing: `grep "outbound\|response ready" /tmp/joelclaw/gateway.log | tail -10`

### Streaming not working
1. Verify `text_delta` events: `grep "text_delta" /tmp/joelclaw/gateway.log | tail -5`
2. Check `telegram-stream` lifecycle: `grep "telegram-stream" /tmp/joelclaw/gateway.log | tail -10`
3. Common issue: model does tool calls before text → no deltas until after tools complete
4. Race condition fix: `initialSendPromise` in `finish()` (commit 175c6ca)

### HTML formatting broken
1. Check converter output: `TelegramConverter.convert(text)` + `.validate(result)`
2. Fallback: adapter auto-strips HTML and sends plain text if validation fails
3. Streaming path sends plain text (no parse_mode), only `finish()` adds HTML

## Related ADRs

- **ADR-0042** — Media download pipeline
- **ADR-0070** — Inline buttons and callbacks
- **ADR-0160** — Telegram streaming UX
- **ADR-0162** — Reactions, replies, and channel configuration
