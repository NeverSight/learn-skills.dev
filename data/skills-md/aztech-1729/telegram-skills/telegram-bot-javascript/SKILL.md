---
name: telegram-bot-javascript
description: Build or migrate JavaScript and TypeScript Telegram HTTP Bot API bots with grammY or Telegraf, including middleware, sessions, conversations, callbacks, polling/webhooks and reliable async processing. Use for Node.js projects; inspect runtime support before adapting to Deno or edge environments.
---

# JavaScript / TypeScript Telegram bots

## Select and verify

Keep an existing project's framework. For a new project, grammY provides a documented plugin ecosystem and current Bot API types; Telegraf fits an existing Composer/Scenes application. These are HTTP Bot API frameworks, not user-account MTProto clients.

Checked **2026-10-03**: grammY **1.46.0**, Telegraf **4.16.3**. Their Bot API coverage differs. Do not assume a recent Telegram feature has a Telegraf type or convenience method. [Sources](references/sources.md) record official releases and topic references.

Read [implementation guide](references/guide.md) for state, concurrency, media, webhooks, plugins, errors and deployment. Read only the plugin documentation needed by the task.

For multi-step grammY input, read [dialogs and replay](references/conversations.md)
and its tested private-chat feedback factory for confirmation, external operations,
cached authorization, cancellation and durable idempotency boundaries.

For a failing handler, missing API, session race or shutdown issue, use [framework diagnostics](references/troubleshooting.md) before changing transport/framework. The focused audit there is dated separately from the release baseline.

## Implementation workflow

1. Establish bot token configuration (`TELEGRAM_BOT_TOKEN` in pack starters), runtime/module format, dependency lockfile, and one update transport.
2. Register middleware in deliberate order; await API calls and `next()` when continuing the chain.
3. Narrow update types before accessing fields; use framework filters and answer callback queries promptly.
4. Choose session keys and persistence from the application's scope; serialize conflicting updates or use transactional state.
5. Add bounded error handling, shutdown and replay handling suited to the deployment.

## Starter and validation

The [starter assets](assets/starter/package.json) include separate grammY and Telegraf polling entrypoints and reusable bot factories. They provide `/start`, `/help`, a button callback and text echo. Real polling requires a token; tests use synthetic updates and a local fake HTTP server, with no Telegram calls.

```bash
cd telegram-bot-javascript/assets/starter
npm ci --ignore-scripts
npm test
node grammy.mjs
# Or choose the Telegraf entrypoint, not both for one token:
node telegraf.mjs
```

Install the chosen framework in the actual project, rather than carrying both dependencies by default. Adapt JavaScript starters to TypeScript with framework context types and `strict` checking; do not disable types to hide unsupported API fields.

## Required integration decisions

- A memory session is lost on restart and is not an order ledger. Concurrency must respect the same keys as state storage.
- Conversation replay can repeat surrounding code: keep external side effects in the plugin's documented external-operation mechanism and use durable application idempotency.
- Validate callback/action identity independently of a session. Text or callback data cannot grant administrative rights.
- With webhooks, validate a dedicated secret and accept work before acknowledgment when durability matters. Avoid serverless long polling.
- Bound retries and respect `retry_after`; transport failures can have uncertain send outcomes. Sanitize error logs.
- Graceful shutdown must stop reception and drain accepted work, with a deployment-appropriate deadline.

Combine with [keyboards](../telegram-bot-keyboards-ui/SKILL.md), [payments](../telegram-bot-payments-stars/SKILL.md), [Mini Apps](../telegram-bot-miniapps/SKILL.md), [rich messaging](../telegram-bot-rich-messaging/SKILL.md) or [advanced operations](../telegram-bot-advanced-features/SKILL.md) when requested.

For product flows, load [bot UX](../telegram-bot-ux/SKILL.md); for keyboard/focus or readable feedback, load [accessibility](../telegram-bot-accessibility/SKILL.md). These decisions complement the framework handlers.

## Upstream status

Before adopting a newer API or dependency, check [automated source observations](references/upstream-status.md) and compare them with the reviewed baseline.
