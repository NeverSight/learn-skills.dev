---
name: telegram-bot-fundamentals
description: Plan or troubleshoot Telegram bot work, select HTTP Bot API versus MTProto and a language framework, configure BotFather and updates, and route to the pack's implementation guides. Start here for a new Telegram task; preserve an existing project's architecture when appropriate.
---

# Telegram bot fundamentals

## Establish the implementation context

Identify the existing language/library, bot versus user-account identity, requested behavior, chat types, and deployment constraints. Read [core guide](references/guide.md) for account setup, update handling, limits, and configuration. Read [capability routing](references/api-capabilities.md) only for the feature families involved.

Use HTTP Bot API for ordinary bot messaging, menus, payments, and Mini Apps. Use MTProto when required operations depend on an authenticated Telegram account or native protocol functionality. A local Bot API server is another option for file workflows. None of these choices grants rights the account does not have.

## Select a framework

| Context | Skill |
| --- | --- |
| Python HTTP: commands, conversations, jobs | [python-telegram-bot](../telegram-bot-python-telegram-bot/SKILL.md) |
| Python HTTP: routers, FSM, middleware | [aiogram](../telegram-bot-aiogram/SKILL.md) |
| Python MTProto | [Telethon](../telegram-bot-telethon/SKILL.md) |
| Go HTTP | [Go Bot API](../telegram-bot-go-botapi/SKILL.md) |
| Go MTProto | [gotd](../telegram-bot-gotd/SKILL.md), plus [contrib](../telegram-bot-gotd-contrib/SKILL.md) for operational helpers |
| JavaScript/TypeScript HTTP | [grammY and Telegraf](../telegram-bot-javascript/SKILL.md) |
| Java HTTP | [TelegramBots and Pengrad](../telegram-bot-java/SKILL.md) |
| C#/.NET HTTP | [Telegram.Bot](../telegram-bot-dotnet/SKILL.md) |
| PHP HTTP | [Telegram Bot SDK / Longman](../telegram-bot-php/SKILL.md) |
| Rust HTTP | [teloxide](../telegram-bot-rust/SKILL.md) |

Keep the selected framework's types, update dispatch, and lifecycle consistent. Do not combine wrappers from different libraries by copying superficially similar snippets.

## Load task-specific guidance

| Task | Read |
| --- | --- |
| Onboarding, journeys, command wording, recovery and consent | [bot UX](../telegram-bot-ux/SKILL.md) |
| Accessible text, buttons, media and interaction alternatives | [accessibility](../telegram-bot-accessibility/SKILL.md) |
| Buttons, callbacks, inline results, pagination | [keyboards/UI](../telegram-bot-keyboards-ui/SKILL.md) |
| Rich output, catalogs, reports, streaming | [rich messaging](../telegram-bot-rich-messaging/SKILL.md) |
| Invoices, Stars, refunds, subscriptions, gifts | [payments](../telegram-bot-payments-stars/SKILL.md) |
| Telegram web frontend and backend authentication | [Mini Apps](../telegram-bot-miniapps/SKILL.md) |
| Mini App layout, navigation and client interaction design | [Mini App design](../telegram-bot-miniapp-design/SKILL.md) |
| Database state, retries, broadcast, webhook, deployment | [advanced features](../telegram-bot-advanced-features/SKILL.md) |
| Moderation, reminders, quiz, RSS, AI, download, shortener | [recipes](../telegram-bot-recipes/SKILL.md) |
| Business connections, managed/guest bots, topics, communities, channel DMs, stickers, stories, paid media | [capability routing](references/api-capabilities.md) |

Read only the selected references; the pack is a routing system rather than a requirement to load every guide.

## Preserve these invariants

- Treat tokens, MTProto sessions, and application/provider credentials as secrets. Choose one token environment convention and define it explicitly.
- Use one update transport per bot token. Persist a polling offset only after the application has safely accepted the corresponding work; webhook replay requires duplicate handling.
- Check current permissions on administrative actions and application ownership on callbacks. Command visibility, button data, and client identity fields are not authorization.
- Reply to callback/pre-checkout/inline queries through the appropriate API. Do not assume every update has a message or a user.
- Scope state to the relevant bot, user, chat, topic, and business connection. Use storage appropriate to restart/concurrency requirements.
- Honor Telegram retry parameters. A timeout after sending may have an uncertain outcome; blind retries can duplicate externally visible actions.
- Distinguish SDK support from Bot API availability. Use a verified raw method adapter or upgrade when the installed SDK lacks a feature.

## Compatibility and evidence

Research cutoff: **2026-10-04**. Telegram's documented Bot API baseline is **10.3**; framework baselines vary. [Sources](references/sources.md) record the checked primary references. Examples are starters or explicitly marked patterns; validate the actual project behavior and report the checks performed.

## Upstream status

Before adopting a newer API or dependency, check [automated source observations](references/upstream-status.md) and compare them with the reviewed baseline.
