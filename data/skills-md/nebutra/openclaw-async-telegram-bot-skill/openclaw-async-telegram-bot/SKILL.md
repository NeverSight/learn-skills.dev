---
name: openclaw-async-telegram-bot
description: Add or update asynchronous Telegram bot accounts in OpenClaw. Use when user asks to add multiple Telegram bots, run bots in parallel, or asks OpenClaw to guide BotFather-based provisioning. Enforces username pattern Nebutra[three digits]_bot and philosopher-style English bot names.
---

# OpenClaw Async Telegram Bot

## Use This Skill When

- User asks for multiple Telegram bots in parallel ("async bots", "multi-bot setup", "parallel telegram bots")
- User asks OpenClaw to guide creation of a new Telegram bot via BotFather and configure it
- User wants one bot per account (optionally one bot per dedicated agent)

## Naming Rules

- Bot username must be `Nebutra[three-digits]_bot` (example: `Nebutra007_bot`)
- Bot display name must be an English ancient Greek philosopher name
- This skill uses this fixed set:
  - `Socrates`
  - `Plato`
  - `Aristotle`
  - `Pythagoras`
  - `Heraclitus`
  - `Democritus`
  - `Epicurus`
  - `Zeno`
  - `Thales`
  - `Anaxagoras`

## BotFather Constraint

- OpenClaw cannot mint new Telegram bot tokens directly.
- Telegram bot token creation must be done in BotFather by the user (`/newbot`).
- This skill must guide the user through BotFather, then configure OpenClaw with the fresh token.

## Token Freshness Rules

- For **new bot** requests, never auto-reuse a token from memory or earlier conversation context.
- Always request a fresh token generated in BotFather for the new bot.
- If a provided token is already bound to an existing OpenClaw account, treat it as an update flow and require explicit confirmation.

## Workflow

1. If user asks for a **new bot**, prefer RPA-assisted flow on macOS with `botfather_rpa_assist_mac.sh`.
2. If RPA is not available, run `prepare_botfather_new_bot.sh` to generate deterministic BotFather inputs.
3. Get fresh token from BotFather.
4. Validate token with Telegram `getMe`.
5. Reject token if username does not match `^Nebutra[0-9]{3}_bot$`.
6. Reject token if it is already registered in OpenClaw, unless user explicitly confirms update flow.
7. Add/update Telegram account in OpenClaw (`channels add`).
8. Restart gateway and verify `running + probe.ok=true`.
9. Optional: create a dedicated isolated agent bound to `telegram:<accountId>`.

## Command

RPA-assisted end-to-end flow (macOS):

```bash
bash scripts/botfather_rpa_assist_mac.sh --name "Aristotle"
```

Optional RPA flags:

```bash
# include dedicated agent creation
bash scripts/botfather_rpa_assist_mac.sh --name "Aristotle" --agent-id "aristotle-agent"

# run only the BotFather RPA step (no OpenClaw configuration yet)
bash scripts/botfather_rpa_assist_mac.sh --name "Aristotle" --no-configure

# extend clipboard wait window for auto-token pickup
bash scripts/botfather_rpa_assist_mac.sh --name "Aristotle" --wait-clipboard 300
```

BotFather-assisted new bot planning:

```bash
bash scripts/prepare_botfather_new_bot.sh
```

Optional planning flags:

```bash
# Force serial (otherwise auto-pick next available)
bash scripts/prepare_botfather_new_bot.sh --serial 2

# Force display name and include dedicated agent in follow-up command
bash scripts/prepare_botfather_new_bot.sh --name "Aristotle" --agent-id "aristotle-agent"

# Emit machine-readable JSON for automation
bash scripts/prepare_botfather_new_bot.sh --json
```

Configure bot after receiving fresh token:

```bash
bash scripts/add_async_telegram_bot.sh --token "<TOKEN>"
```

Optional flags:

```bash
# Force account id
bash scripts/add_async_telegram_bot.sh --token "<TOKEN>" --account-id "plato-007"

# Force philosopher display name
bash scripts/add_async_telegram_bot.sh --token "<TOKEN>" --name "Plato"

# Create isolated agent bound to this telegram account
bash scripts/add_async_telegram_bot.sh --token "<TOKEN>" --agent-id "plato-agent"

# Reuse an already-registered token intentionally (update flow only)
bash scripts/add_async_telegram_bot.sh --token "<TOKEN>" --allow-existing-token

# Dry run
bash scripts/add_async_telegram_bot.sh --token "<TOKEN>" --dry-run
```

## BotFather Notes

If user needs a fresh token, or username validation fails, stop and ask user to recreate bot in BotFather:

1. `/newbot`
2. Bot display name: philosopher English name
3. Bot username: `Nebutra###_bot`
4. Return the new token
