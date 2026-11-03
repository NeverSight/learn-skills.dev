---
name: telegram-bot-gotd
description: Build or repair Go MTProto bots and user-account clients with gotd/td, including authentication, sessions, typed updates, peers, generated RPCs, and media transfers.
---

# gotd/td

Use for Go MTProto work. For an ordinary Go HTTP Bot API bot, use telegram-bot-go-botapi. Application credentials and account authorization are required in addition to a bot token where applicable.

## Implement against the chosen release

- Read [the implementation guide](references/guide.md) for client lifecycle, authentication, typed dispatch, peer resolution, message/media helpers, raw RPCs, proxies, and migration.
- Read [the dated sources](references/sources.md) to match API signatures to the pinned gotd version.
- Persist the MTProto session and check authorization before logging in. Verify Self's bot flag and ID against the intended token before enabling bot handlers; an authorized saved user/different-bot session is not a valid match. Session data grants account access; isolate it per account and protect backups.
- Register a dispatcher through telegram.Options.UpdateHandler. Run the callback for the intended application lifetime; returning ends client.Run.
- Use an updates.Manager and persisted recovery state when offline recovery matters. Authentication/session persistence alone does not provide recovery or durable business processing.
- For operational helpers, add telegram-bot-gotd-contrib. Bound retries and concurrency; MTProto remains subject to Telegram's permissions and flood controls.
- Verify generated method restrictions for the actual account type. Reading raw API names does not make user-only methods available to bots.

## Starter and validation

[assets/echo/main.go](assets/echo/main.go) is a bot-account echo starter with file session storage, verified identity before update handling, and explicit lifecycle. It reads APP_ID, APP_HASH, BOT_TOKEN, and optionally SESSION_FILE. [Offline tests](assets/echo/main_test.go) exercise identity refusal, readiness, typed reply routing and error propagation through a fake invoker.

Compile before integrating; use fixtures or a fake invoker for handler tests. Starting this application contacts Telegram. Do not promise TDLib equivalence, ban immunity, unlimited file sizes, or automatic retries of arbitrary business handlers.

For bot menus, progress or recovery messages, pair this with [bot UX](../telegram-bot-ux/SKILL.md) and [accessibility](../telegram-bot-accessibility/SKILL.md). Use [Mini App design](../telegram-bot-miniapp-design/SKILL.md) only for a separate web interface; its launch-data validation is not supplied by MTProto authentication.

## Upstream status

Before adopting a newer API or dependency, check [automated source observations](references/upstream-status.md) and compare them with the reviewed baseline.
