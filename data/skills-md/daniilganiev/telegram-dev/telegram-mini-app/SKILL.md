---
name: telegram-mini-app
description: Build Telegram Mini Apps (Web Apps) — BotFather setup, launch methods and start_param, the Telegram WebApp SDK and tma.js, theming, safe areas, full-screen, storage, haptics, validating initData on a TypeScript or Python backend, Stars purchases from the app, and wallet connection. Use this skill whenever the user works on an app inside Telegram, a Telegram Web App, Telegram.WebApp, tma.js, initData, a menu button that opens a web page, a Telegram game in the browser, or says "app inside Telegram" or "connect wallet in Telegram".
---

# Telegram Mini App

## Stack

- From scratch: an official Telegram Mini Apps template (React, Next.js, Vue, Solid) on
  `@tma.js/sdk`, or plain `telegram-web-app.js` for a small page.
- With a TON contract: Acton `--app` already gives Vite + React + TON Connect; add the Telegram
  layer on top (see `telegram-ton`).
- Backend in any language. The only hard requirement is validating `initData` there.

These SDKs change often; check the current package docs before writing integration code.

## Setup

1. Bot in @BotFather (`/newbot`); token only in a backend env var.
2. Mini App via `/newapp`, or set the bot's menu button to the app URL.
3. HTTPS hosting; a tunnel (ngrok, cloudflared) for local development.
4. Telegram has a separate **test environment** (own accounts and bots) for testing payments and
   flows without real Stars.

## Rules

- **Never trust client data.** `initDataUnsafe` is for display only. Send raw `initData` to the
  backend and validate it: `references/init-data-validation.md` (TypeScript and Python).
- Money and entitlements live on the server. CloudStorage, DeviceStorage and SecureStorage are
  conveniences, not a source of truth.
- Digital goods in the app are paid in Stars: create the invoice link on the server and open it
  with `openInvoice` (`telegram-payments`). Do not add a crypto checkout for them.
- **Cross-origin hardening** (Bot API 10.2): since 20 July 2026 Mini App methods can't be called
  from origins other than the app's own domain. An iframe or embedded third-party page that
  used to call `Telegram.WebApp` will silently stop working. The owner can opt out in @BotFather
  but then takes responsibility for every link in the app; don't recommend opting out.
- Respect theme params (CSS variables) and both safe-area insets; test on iOS, Android, Desktop
  and the Web clients (WebK and WebA). Full-screen mode changes the insets.
- Keep the bot token, API keys and any backend secret out of the front-end bundle.

## Wallets

Connecting a TON wallet, signing transactions and proving wallet ownership are covered in
`telegram-ton` (TON Connect, `ton_proof`). Show a visible network badge while on testnet.

## References

- `references/init-data-validation.md` — server-side validation, TS and Python, common mistakes.
- `references/webapp-features.md` — launch methods, storage tiers, tma.js, TON Connect settings.

Related skills: `telegram-bot` (bot, webhooks, deep links), `telegram-payments` (Stars),
`telegram-ton` (wallets, tokens), `telegram-launch` (checklist before release).
