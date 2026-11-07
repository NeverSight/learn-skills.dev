---
name: telegram-bot-python-telegram-bot
description: Build, migrate, or debug Telegram Bot API applications using python-telegram-bot (PTB), including handlers, callback menus, conversations, jobs, persistence, and polling or webhooks. Use for existing PTB projects or an explicit PTB choice; user-account MTProto automation needs a different framework.
---

# Telegram bots with python-telegram-bot

Use the project's installed PTB version and architecture. The researched baseline is **PTB 22.8, released 2026-06-12, Python 3.10+, native Bot API 10.0 support**, checked **2026-10-03**. Telegram's Bot API 10.3 features can exceed this wrapper's typed coverage: inspect the installed signature and official API before using a new field. See [sources](references/sources.md) for the cutoff and compatibility evidence.

## Workflow

1. Inspect dependencies, bot delivery mode, registered handlers, existing storage, and requested behavior. Preserve a user's framework choice. PTB suits Bot API applications with its Application, ConversationHandler and optional JobQueue; do not migrate an existing project just to obtain a different syntax.
2. Read the relevant section of [the implementation guide](references/guide.md): handlers/context, conversations/persistence, jobs, media, webhooks, inline/admin features, or errors/performance.
3. Implement the smallest complete flow, including cancellation, malformed input, authorization and failure behavior where relevant. Keep bot tokens outside code and logs; the starter uses `BOT_TOKEN` as a local convention.
4. Verify imports, handler routing and pure business behavior offline. Use a dedicated test bot for the requested live acceptance checks. State which checks were actually run; offline checks do not establish Telegram delivery or deployment readiness.

## Invariants that change implementation decisions

- Handlers and Bot API calls are async. `run_polling()` / `run_webhook()` own the application lifecycle in ordinary scripts; do not nest them in an already running event loop. Embedded frameworks need explicit lifecycle management.
- ConversationHandler requires sequential update processing: keep `concurrent_updates(False)`. Give persisted conversations a stable `name`, `persistent=True`, and Application persistence. Persistence alone does not opt a conversation into saving.
- Numeric JobQueue delays are **seconds**. Convert minutes explicitly. JobQueue needs the `job-queue` extra; restart-safe reminders also need durable records and recovery logic.
- Answer callback queries promptly, validate their data and check the actor's permission. A callback may have an inline message ID or an inaccessible message; do not assume `update.message` exists.
- Preserve flow data when a reply fails. Conversation state changes after its callback returns; removing data before an awaited completion reply can strand the previous state. Place an expired-menu callback fallback after specific routes.
- Register specific handlers before catch-all handlers within a group. `filters.TEXT` also includes commands unless excluded. Administrative status is an API/authorization check, not `filters.StatusFilter.ADMIN`.
- Polling and a webhook are mutually exclusive for one bot token. Put `secret_token` on `run_webhook`, `start_webhook`, or Bot API `set_webhook`, not ApplicationBuilder. Keep an Updater when using PTB's webhook receiver.
- Avoid blocking I/O, unbounded background work and shared mutable per-user globals. Match concurrency, connection-pool capacity, state locking and retry policy to the application.
- Retry explicit rate-limit responses within a bounded policy. A timeout can leave a send's outcome unknown; retrying a side effect can duplicate it. Preserve idempotency at the business-operation boundary.

## Included starter

[assets/starter/bot.py](assets/starter/bot.py) is an original, self-contained polling bot with echo, callback menu, validated reminders and a two-step form. Install [its requirements](assets/starter/requirements.txt), set `BOT_TOKEN`, and run the file only when Telegram interaction is intended. Optional `BOT_STATE_FILE` enables local trusted-file persistence for the form; scheduled reminders remain process-local.

[assets/starter/offline_check.py](assets/starter/offline_check.py) checks routing, stale-menu recovery, failed-reply state retention, nontext form input, scheduling units and persistence without contacting Telegram. It can be run before supplying any token. Detailed deployment and feature snippets in the guide are **application patterns**, with their integration boundaries stated.

For onboarding, form copy or navigation, add [bot UX](../telegram-bot-ux/SKILL.md). For text alternatives, localization and assistive-technology checks, add [accessibility](../telegram-bot-accessibility/SKILL.md). A requested web interface also needs [Mini App design](../telegram-bot-miniapp-design/SKILL.md) and [Mini App security](../telegram-bot-miniapps/SKILL.md).

## Upstream status

Before adopting a newer API or dependency, check [automated source observations](references/upstream-status.md) and compare them with the reviewed baseline.
