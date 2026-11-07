---
name: telegram-bot-php
description: Implement PHP Telegram HTTP Bot API applications with irazasyed/telegram-bot-sdk or maintain php-telegram-bot/core (Longman) projects, including Laravel integration, commands, webhook updates, Composer dependencies and durable application processing.
---

# PHP Telegram bots

Checked **2026-10-03**: Telegram Bot SDK **3.16.0**, published 2026-03-23. Read [guide](references/guide.md) for SDK selection, commands, webhooks, Laravel, storage, files and API lag; [sources](references/sources.md) record primary references.

For ingress rejection, stale Laravel config, replayed jobs or missing wrappers, use [PHP diagnostics](references/troubleshooting.md).

## Select the implementation

Keep the framework already in use. `irazasyed/telegram-bot-sdk` provides `Telegram\Bot\Api`, command handling, multi-bot configuration and Laravel integration. `php-telegram-bot/core` uses the `Longman\TelegramBot` architecture and its own commands/request/database flow; do not exchange their objects or methods.

For a new SDK project, pin the Composer dependency and select standalone PHP or the actual Laravel version's integration. The SDK's PHP requirement and the host framework's requirement may differ.

## Required decisions

- Configure a bot token and a separate webhook secret; do not expose a token in a public route.
- For webhook receipt, validate the secret header before SDK processing, constrain the body, and deduplicate accepted updates where side effects need replay safety.
- Route one parsed update, not an imagined list from `getWebhookUpdate`. Check optional message/callback/payment fields.
- Use the installed SDK's command architecture; command registration does not authorize administrative actions.
- Use durable application jobs/storage for slow work. PHP HTTP request completion is not a substitute for a background worker lifecycle.
- Treat file uploads as the SDK's documented input type, and confirm newer Bot API method availability against package source.

## Starter

[webhook.php](assets/starter/webhook.php) is a standalone SDK echo endpoint with header validation, bounded JSON body checks and sanitized failures. [composer.json](assets/starter/composer.json) pins the verified SDK baseline. It is a starter, without durable replay storage; read advanced-features before using it for consequential side effects.

```bash
cd telegram-bot-php/assets/starter
composer install
php -l webhook.php
php test.php
```

Configure `TELEGRAM_BOT_TOKEN` and `TELEGRAM_WEBHOOK_SECRET` in the HTTP worker environment, expose the script through the chosen HTTPS host, and register that endpoint with the same secret. Do not use the sample command as proof of a deployed webhook.

`test.php` exercises secret/JSON/size rejection and topic-aware request construction without loading the SDK or contacting Telegram. Copy WebhookInput.php with the endpoint; it is the shared input/routing helper.

## Task companions

Load [UI](../telegram-bot-keyboards-ui/SKILL.md), [payments](../telegram-bot-payments-stars/SKILL.md), [Mini Apps](../telegram-bot-miniapps/SKILL.md), [rich messaging](../telegram-bot-rich-messaging/SKILL.md), and [advanced operations](../telegram-bot-advanced-features/SKILL.md) for the relevant application behavior. Adapt their conceptual examples to PHP rather than mixing Python/Go wrapper syntax.

Use [bot UX](../telegram-bot-ux/SKILL.md) for product flows and [accessibility](../telegram-bot-accessibility/SKILL.md) for labels and recoverable feedback.

## Upstream status

Before adopting a newer API or dependency, check [automated source observations](references/upstream-status.md) and compare them with the reviewed baseline.
