---
name: telegram-bot-rust
description: Build or repair Rust HTTP Telegram Bot API bots with teloxide, including Tokio lifecycle, dptree dispatch, typed commands, dialogues, callbacks, media, webhooks, and SDK feature compatibility.
---

# Rust with teloxide

Use for Rust HTTP bots with teloxide. MTProto user-account clients require a separately selected library and account-specific workflow.

## Implement against the published crate

- Read [the Rust guide](references/guide.md) for feature flags, REPL versus Dispatcher, commands, dependency injection, dialogue storage, callbacks, media, errors, and webhook listeners.
- Use [teloxide diagnostics](references/troubleshooting.md) for feature/toolchain failures, dispatch scope, topic routing and stalled async work.
- Read [the dated source record](references/sources.md) before relying on a recent Bot API field. Published teloxide 0.17.0 and the development branch have different coverage.
- Use Tokio-compatible async work; move blocking operations to bounded worker tasks. Do not hold synchronous locks across await points.
- Use one update receiver, explicit authorization, durable application state, and bounded retries. Request adaptors assist delivery; they do not make effects exactly once.
- Compile with the project's supported Rust toolchain and selected features. Test handler logic locally before starting a receiver or making Telegram calls.
- For API features absent from the pinned crate, choose a documented fallback or isolate a small official-HTTP request adapter. Do not invent a teloxide method or change the framework without explaining the compatibility decision.

## Starter

[assets/echo/Cargo.toml](assets/echo/Cargo.toml) and [src/main.rs](assets/echo/src/main.rs) provide a minimal text echo design. It reads TELOXIDE_TOKEN. The source record states whether compilation was available; source review alone is not a cargo check.

`cargo test` exercises plain-text/topic request construction and ignored non-text messages without awaiting Telegram requests. `cargo run` is the separate live receiver entrypoint.

Use the feature guides for interaction design, Stars, Mini Apps, and operations when relevant, translating examples to Rust.

Load [bot UX](../telegram-bot-ux/SKILL.md) for product flows and [accessibility](../telegram-bot-accessibility/SKILL.md) for usable labels and feedback, then map actions to the published crate's actual fields.

## Upstream status

Before adopting a newer API or dependency, check [automated source observations](references/upstream-status.md) and compare them with the reviewed baseline.
