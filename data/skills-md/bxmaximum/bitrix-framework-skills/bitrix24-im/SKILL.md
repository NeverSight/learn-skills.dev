---
name: bitrix24-im
description: 'Bitrix24 on-premise messenger in PHP: chats and messages (Bitrix\Im\V2\Chat, CIMChat), notifications (CIMNotify), chat bots (Im\Bot, imbot, slash commands). Use when sending a message, creating a chat, notifying a user or building a bot.'
---

# Bitrix24 messenger (server side)

Scope: Bitrix24 on-premise · Verified: im 26.900.0, imbot 26.400.0, main 26.800.0

| Task | Read |
| --- | --- |
| Send messages, system messages, attach/keyboard, create chats, members, im events | `rules/messages-chats.md` |
| Notifications: types, tags, delete, confirm buttons, user settings schema | `rules/notifications.md` |
| Chat bots and slash commands from a module; REST `imbot.v2`; open lines | `rules/bots.md` |
| Breaking changes im 26.700–26.900, REST ↔ PHP mapping | `rules/pitfalls.md` |

## Invariants

- `Loader::includeModule('im')` before any messenger class (`Bitrix\Im\V2\Chat`, `CIMChat`, `CIMNotify` …).
- Pass explicit user ids (`FROM_USER_ID`, `AUTHOR_ID`, `TO_USER_ID`, context user). Agents and CLI have no `$USER`.
- `Bitrix\Im\V2\Chat::sendMessage()` does not check the author's rights: call `canDo(Action::Send)` first, or use `CIMChat::AddMessage()`, which checks unless `SYSTEM`/`SKIP_USER_CHECK` is `Y`.
- After-send work (push, counters, `OnAfterMessagesAdd`, bots) runs as a background job after the response. In CLI scripts call `$result->getPromise()?->wait()`; the `CIM*` wrappers wait by default.
- Notifications: `CIMNotify::Add()` only. `NotifyChat::sendMessage()` is a stub in im 26.900.
- Give every notification a `NOTIFY_TAG`: it dedupes (same tag replaces the older one for the user) and allows deletion.
- Custom chats bound to your entity: `ENTITY_TYPE` in your own namespace + `addUniqueChat()`; never write `b_im_*` tables.
