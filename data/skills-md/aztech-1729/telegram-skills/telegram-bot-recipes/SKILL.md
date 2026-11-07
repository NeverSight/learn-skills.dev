---
name: telegram-bot-recipes
description: Build a Telegram moderation, reminder, quiz, RSS publisher, AI assistant, media downloader, or URL shortener from maintained Python starters. Use for these concrete bot products; use a framework skill for unrelated framework setup.
---

# Telegram bot recipes

Choose the recipe matching the requested product, then adapt its storage and
authorization model. The supplied implementation uses python-telegram-bot 22.8;
the designs can be ported to another requested language without imposing Python.

## Select the starter

| Product | Mode | Relevant detail |
|---|---|---|
| Group moderation | `moderation` | Live administrator checks before warning writes; member rights |
| Persistent reminders | `reminders` | Owned list/cancel flow, topic context, bounded single-worker retries |
| Quiz | `quiz` | Owner/chat binding, expiry, atomic ordered scoring |
| RSS to channel | `rss` | Configured feeds, bounded async fetch, send then record |
| AI assistant | `ai` | Explicit model, Responses API, plain-text chunking |
| Media download | `download` | Approved hosts, async subprocess, quotas and upload bound |
| URL shortener | `shortener` | Stored HTTP(S) URLs plus a real redirect service |

Read [references/guide.md](references/guide.md) for setup, mode configuration,
failure behavior, and implementation boundaries. Read
[references/sources.md](references/sources.md) when verifying upstream APIs.

Copy [assets/recipes.py](assets/recipes.py), [assets/recipe_store.py](assets/recipe_store.py),
and [assets/requirements.txt](assets/requirements.txt) together. Copy
[assets/redirect_service.py](assets/redirect_service.py) for short links.
Run the [store tests](tests/test_store.py) before modifying transaction behavior.

## Preserve these invariants

- Authorize moderation before updating warning counts. Inspect the bot's actual
  rights before deleting or restricting. Anonymous administrators require a
  separate policy; do not equate `sender_chat` with an authenticated person.
- Treat callback payloads as untrusted input. Bind quiz state to user and chat,
  expire it, and accept each step once within one database transaction.
- Mark reminders or feed items complete after a confirmed send. A crash after a
  successful send can still duplicate delivery; use the
  [outbox guide](../telegram-bot-advanced-features/references/guide.md) when this matters.
- Keep network, parsing, database work and downloads off the async handler loop.
  Do not interpolate chat input into shell commands.
- Configure API credentials and costly-mode access outside source files. The AI
  and downloader starters are restricted to configured user IDs.
- Separate answer chunking from live streaming. For drafts, cancellation and final
  persistence use [streaming guidance](../telegram-bot-rich-messaging/references/streaming.md).

Use [bot UX](../telegram-bot-ux/SKILL.md) when shaping onboarding, consent and
failure recovery for a selected recipe. Use [Mini Apps](../telegram-bot-miniapps/SKILL.md) for a web interface and
[Stars](../telegram-bot-payments-stars/SKILL.md) for paid digital access. Use the
[PTB skill](../telegram-bot-python-telegram-bot/SKILL.md) for lifecycle and webhook
integration. Keep one update receiver per token.

## Upstream status

Before adopting a newer API or dependency, check [automated source observations](references/upstream-status.md) and compare them with the reviewed baseline.
