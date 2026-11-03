---
name: telegram-bot-go-botapi
description: Build or repair Go HTTP Telegram Bot API bots with go-telegram/bot, gotgbot/v2, or go-telegram-bot-api/v5; use for handlers, polling, webhooks, media, and framework migration.
---

# Go HTTP Bot API

Use with the fundamentals guide for HTTP bots written in Go. For Go user-account actions or raw MTProto, use telegram-bot-gotd instead.

## Work from the project

- Keep the existing library when it meets the requested behavior. For a new project, compare the maintained go-telegram/bot framework with gotgbot's dispatcher/filters; retain classic v5 for compatible existing integrations.
- Read [the framework guide](references/guide.md) for the selected library, handler and webhook wiring, media, error handling, and migration differences.
- Check [the dated source record](references/sources.md) before using a version-sensitive method. A Bot API release and a Go library release are separate compatibility decisions.
- Complete configuration, callback authorization, durable business state, and update ownership before running a bot. Use one polling receiver or a coordinated webhook deployment per token.
- At go-telegram/bot v1.27.0, the native webhook handler logs rejected secrets/JSON but returns implicit HTTP 200. Supply explicit HTTP validation, bounded request bodies and the required acknowledgment policy around it; its queue is process memory.
- Validate compilation and relevant update behavior with a fake client or fixture before live integration. Report compilation separately from Telegram integration tests.

## Starters

The guide links three small applications under assets/, one for each library. They read TELEGRAM_BOT_TOKEN and intentionally send plain text. Do not run them during documentation checks: construction or polling can contact Telegram.

For a requested chat interface, add [bot UX](../telegram-bot-ux/SKILL.md) and [accessibility](../telegram-bot-accessibility/SKILL.md); for a web interface add [Mini App design](../telegram-bot-miniapp-design/SKILL.md) and [Mini App security](../telegram-bot-miniapps/SKILL.md). Framework choice does not change Telegram's API permissions or rate limits.

## Upstream status

Before adopting a newer API or dependency, check [automated source observations](references/upstream-status.md) and compare them with the reviewed baseline.
