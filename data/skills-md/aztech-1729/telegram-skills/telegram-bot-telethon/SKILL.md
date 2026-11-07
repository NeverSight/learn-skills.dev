---
name: telegram-bot-telethon
description: Develop, debug, or migrate Telegram MTProto applications explicitly using Telethon 1.x, including authenticated user clients, bot accounts, event handlers, entities/history, media transfers, conversations, and raw Telegram requests. Use when the existing project uses Telethon or needs MTProto capabilities and account permissions; use a Bot API framework for ordinary HTTP bots.
---

# Telegram with Telethon 1.x

Use the installed project version first. The researched baseline is **Telethon 1.45.0**, released **2026-09-10**, with generated **MTProto layer 229** types. Checked through **2026-10-03**. These examples target Python 3.10+ and were checked on Python 3.12; package metadata has a broader Python minimum, which is not a claim that every old interpreter was tested. Read [sources](references/sources.md) before changing the baseline or mixing v2 APIs.

## Workflow

1. Inspect dependencies, client lifecycle, account type, existing session, chat scope, and authorization requirements. Preserve the project's framework and architecture.
2. Identify whether the task requires a bot or an explicitly authorized user session. Obtain API credentials through Telegram's API development page; bot tokens alone are insufficient for Telethon.
3. Read the relevant sections of [the guide](references/guide.md): authentication/session lifecycle; events/buttons; friendly methods/entities; media; raw requests; conversations; retries and concurrency.
4. Implement one clear async lifecycle, validated inputs, bounded work, and complete cleanup. Confirm the chosen method is permitted for that account type and chat role.
5. Validate imports, request constructors, and application logic offline. Report live behavior separately; authenticating, sending, joining, exporting history, and changing permissions require real authorized Telegram access.

## Invariants

- Protect API hashes, bot tokens, SQLite sessions, and string sessions. A saved session can authenticate as a different account than a supplied token; verify the logged-in identity.
- Create and use a client in one event loop. Do not mix synchronous helpers with an already running async server or reuse a connected client across loops.
- Scope events with supported filters: `incoming`, `chats`, `from_users`, `pattern`, and `func`. Use `func=lambda e: e.is_private` for private messages; there are no `private=True` or `group=True` constructor filters.
- Answer callback queries promptly; validate bytes, expiry, ownership, and permissions before mutation. Give unknown/stale payloads a recovery route. Telethon can dispatch several matching handlers, so stop propagation or make callback routes disjoint. Inline buttons and reply keyboard buttons belong in separate markups.
- Resolve entities with the current account; integer IDs need appropriate access hashes/cache. MTProto does not bypass bot privacy, membership, or user-only method restrictions.
- Use actual wrappers or generated raw requests with all required fields. Do not invent client methods or event classes from their intended action.
- Respect flood wait durations and use finite retries. Replaying a timed-out mutation can repeat a side effect; multiple accounts are not a rate-limit workaround.
- Complex state needs explicit storage and locking. Telethon conversations are transient; `sequential_updates=True` is not a durable queue or a throughput guarantee.

## Resources

- [Guide and conditional application patterns](references/guide.md)
- [Canonical sources and cutoff](references/sources.md)
- [Runnable bot starter](assets/starter/bot.py), [pinned requirements](assets/starter/requirements.txt), and [offline checks](assets/starter/offline_check.py)
- [Validation record and live limits](references/validation.md)

The starter covers private text, commands, callback ownership/stale-menu recovery, and verified bot identity. User login, history export, moderation, inline queries, media pipelines, and distributed state are separate application patterns requiring their own configuration.

For a bot account's conversation or transfer feedback, add [bot UX](../telegram-bot-ux/SKILL.md) and [accessibility](../telegram-bot-accessibility/SKILL.md). For user login, keep credential entry in the authorized application's own interface. A separate web Mini App uses [Mini App design](../telegram-bot-miniapp-design/SKILL.md) and its HTTP/backend validation contract; an MTProto session does not validate Mini App launch data.

## Upstream status

Before adopting a newer API or dependency, check [automated source observations](references/upstream-status.md) and compare them with the reviewed baseline.
