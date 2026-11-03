---
name: telegram-bot-aiogram
description: Build, migrate, or debug Telegram Bot API bots using aiogram 3, especially router-based applications, typed callback menus, middleware/dependency injection, and FSM conversations. Use for an explicit aiogram choice or existing aiogram project; user-account MTProto automation needs another framework.
---

# Telegram bots with aiogram 3

The researched baseline is **aiogram 3.31.0**, released **2026-08-26**, **Python 3.10+**, **Bot API 10.3**, checked **2026-10-03**. Respect the project's installed version; consult [sources](references/sources.md) before using newer API fields or migrating aiogram 2 code.

## Workflow

1. Inspect the dependency pin, routers, delivery mode, FSM storage and business services. Preserve the user's framework choice. aiogram is useful for FSM/DI/router-heavy Bot API applications; PTB remains a valid choice for existing PTB code or its ConversationHandler/JobQueue.
2. Read relevant sections of [the guide](references/guide.md): router/filter ordering, callbacks, FSM/isolation, DI/middleware, media, webhooks, scheduling, translation, errors, or migration/testing.
3. Implement a complete flow with validation, cancellation and authorization. Use named injected services and application-owned persistence; avoid per-user mutable globals.
4. Validate routing and state transitions offline, then use a dedicated test bot for requested live checks. Record which validation occurred; imports do not prove Telegram delivery or production operation.

## Operational invariants

- Bot methods and handlers are async; Telegram models/methods use keyword fields. Configure defaults through `DefaultBotProperties`, not legacy Bot constructor arguments.
- Router/handler order determines the first match. Explicitly filter message content and FSM states; aiogram 3 does not apply the old implicit text/state filtering. Use parenthesized `F` comparisons and `CommandObject` for injected command arguments.
- Answer callbacks promptly. Typed CallbackData validates a shape, not authority; enforce actor/resource permissions server-side and respect the 64-byte payload cap. A callback's message can be inaccessible or absent.
- MemoryStorage loses state on restart. Shared Redis storage and event isolation solve different problems; include bot identity in keys when multiple bots share a namespace and use the same key builder for state/locks. Changing the key scheme requires a migration or explicit flow expiry. Keep payments/orders outside transient FSM data.
- Polling and webhooks are mutually exclusive per token. aiohttp integration is included; another web framework needs its own validated request adapter and lifecycle. There is no `aiogram[fastapi]` extra in the researched package.
- `FSInputFile` is for paths, `BufferedInputFile` for bytes. Callback edits go through `cb.message` or Bot methods, not `cb.edit_text`.
- An error handler that sleeps does not retry a failed request. Retry explicit flood responses at the operation boundary within a bounded policy; treat timeouts as potentially ambiguous side effects.
- Own and close bot/HTTP/DB/storage resources on shutdown. Bound concurrency/background work; keep duplicate-delivery handling and durable acknowledgments explicit.

## Included starter

[assets/starter/bot.py](assets/starter/bot.py) is an original complete polling entrypoint with echo, a typed menu and a validated private-chat FSM form. Install [requirements](assets/starter/requirements.txt), set `BOT_TOKEN`, and run it only when Telegram interaction is intended. Optional `REDIS_URL` selects Redis storage plus matching event isolation; without it, state is process-local.

[assets/starter/offline_check.py](assets/starter/offline_check.py) tests form recovery/cancellation, real stale-callback dispatch, Redis bot/lock key separation and callback bounds without Telegram or Redis connections. The guide's webhook/middleware/scheduler snippets are application patterns with stated integration requirements.

For dialogue structure, validation copy and menu navigation, add [bot UX](../telegram-bot-ux/SKILL.md); for nonvisual operation and localized input, add [accessibility](../telegram-bot-accessibility/SKILL.md). Use [Mini App design](../telegram-bot-miniapp-design/SKILL.md) when the task includes a web interface, alongside [Mini App security](../telegram-bot-miniapps/SKILL.md).

## Upstream status

Before adopting a newer API or dependency, check [automated source observations](references/upstream-status.md) and compare them with the reviewed baseline.
