---
name: telegram-bot-miniapps
description: Build Telegram Mini Apps with correct launch contexts, WebApp JS integration, signed initData authentication, backend sessions, themed interfaces and bot entry points. Use for web interfaces inside Telegram; use the Payments skill for payment fulfillment.
---

# Telegram Mini Apps

For visual tokens, responsive components and native-control lifecycle, use
[Mini App design](../telegram-bot-miniapp-design/SKILL.md). Use
[Accessibility](../telegram-bot-accessibility/SKILL.md) for contrast, labels,
focus and acceptance checks; this skill owns launch/auth/backend integration.

Read [the guide](references/guide.md) for launch selection, SDK integration, authentication, deployment and the persistent todo example. Consult [sources and compatibility](references/sources.md) for the 2026-10-04 baseline. The WebApp API exposed by a client and the bot's server API are distinct version checks.

## Workflow

1. Choose the launch method before designing auth or data return. Reply-keyboard and inline-mode launches have empty initData; inline/menu launches support signed user context and Web App queries.
2. Configure the bot entry point and serve an HTTPS app on the intended origin. Load the Telegram SDK early, then call `ready()` after essential UI is ready.
3. For your own backend, send raw `initData`, verify HMAC over decoded fields, reject duplicate keys and stale/future authentication times, then issue an expiring opaque session. For Telegram-hosted Serverless, use the platform-validated endpoint context described in the guide.
4. Authorize every API operation from the verified session or hosted endpoint context. Keep prices, entitlements, ownership and durable state on the server. `initDataUnsafe`, launch parameters and browser storage are not authorization.
5. Apply theme/safe-area/viewport behavior, loading/error/cancel states and version-gated native APIs. Test auth and persistence offline; verify actual WebView behavior separately before release.

## Invariants

- `Telegram.WebApp.sendData(data)` belongs to WebApp, not MainButton. It closes the app and is available only for reply-keyboard launches. Inline/menu apps use backend APIs and, when appropriate, `answerWebAppQuery`.
- HMAC validation with the bot token and Ed25519 third-party validation are different protocols. Follow the official field exclusion rules for the chosen protocol.
- A Telegram user ID is a database identity, not a secret session token. Validate the caller before creating/listing/deleting their records.
- Origin protection is enabled by default following the July 2026 change; BotFather can opt out. Retain protection and avoid untrusted in-app navigation.
- Feature-detect/version-gate APIs; a recent bot library cannot upgrade a user's Telegram client.
- Invoice-close events express UI status. Grant paid goods only from trusted server payment updates.

## Resources

- [scripts/miniapp_security.py](scripts/miniapp_security.py): standard-library HMAC validator and SQLite bearer-session/todo storage.
- [assets/todo/app.py](assets/todo/app.py) and adjacent frontend files: runnable single-host FastAPI example with persisted, user-scoped todos. Read the guide's setup and deployment limits before using it.
- [scripts/test_miniapp_security.py](scripts/test_miniapp_security.py): offline signature, ownership, expiry, persistence and in-process HTTP tests. Run `python -m unittest discover -s telegram-bot-miniapps/scripts -p 'test_*.py'` from the repository root.

Combine with a framework skill for bot startup, Keyboards UI for chat entry points, Payments for invoices, and Advanced Features for deployment and distributed storage.

## Upstream status

Before adopting a newer API or dependency, check [automated source observations](references/upstream-status.md) and compare them with the reviewed baseline.
