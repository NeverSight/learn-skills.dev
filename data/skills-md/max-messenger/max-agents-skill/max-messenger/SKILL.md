---
name: max-messenger
description: >
  Build bots and mini-apps for MAX Messenger (max.ru, МАКС) — Bot API at platform-api2.max.ru,
  official Go client (max-bot-api-client-go), Go framework maxbot, TypeScript client
  @maxhub/max-bot-api, MAX Bridge (window.WebApp) and the @maxhub/max-ui React kit.
  Use for any code that sends/receives MAX messages, webhooks or long polling, uploads media,
  inline keyboards and callbacks, message formatting, chat/channel admin, comments,
  mini-app initData / phone verification, and TLS errors caused by the Минцифры root CA.
  Triggers: MAX bot, MAX Bot API, platform-api.max.ru, platform-api2.max.ru, max.ru bot,
  бот для МАКС, бот в MAX, мини-приложение MAX, MAX Bridge, window.WebApp in MAX, max-ui,
  maxbot, @maxhub. Not for MAX product/market strategy questions without code.
---

# MAX Messenger development

Verified against official sources on **2026-09-21** (see `references/sources.md`). MAX changes
fast: when a detail here conflicts with the live docs or the client source, trust the source.

## Quick reference

| What | Value |
|------|-------|
| Base URL | `https://platform-api2.max.ru` (mandatory since 2026-07-19; old `platform-api.max.ru` is deprecated) |
| TLS | API host is signed by **Russian Trusted Root CA (Минцифры)** — add it to your trust store, never disable verification → `references/tls-trust.md` |
| Auth | Header `Authorization: <token>` (no `Bearer`; query-param token no longer supported) |
| Get a token | business.max.ru → Чат-боты → bot → ⋮ → Настройки |
| Rate limit | 30 requests/s to the API; callback answers ≤ 2/s per chat |
| Message text | ≤ 4000 characters, `format`: `markdown` or `html` |
| Updates | Webhook (`POST /subscriptions`, HTTPS on port 443 only) for production; long polling (`GET /updates`) for development. They are mutually exclusive |
| Go | `github.com/max-messenger/max-bot-api-client-go/v2` v2.4.0 (primary); `github.com/max-messenger/maxbot` v1.1.0 (optional framework, **needs Go ≥ 1.26** despite its go.mod saying 1.24) |
| TypeScript | `@maxhub/max-bot-api` 0.3.1, Node ≥ 20.19, ESM only |
| Mini-apps | `<script src="https://st.max.ru/js/max-web-app.js">` → `window.WebApp`; UI kit `@maxhub/max-ui` 0.5.0 (React 19.2.8) |

## Hard constraints — violating these ships bugs

1. **Host + CA.** Call `platform-api2.max.ru`. Stock Docker/CI/Node images do not trust its CA and fail with
   `x509: certificate signed by unknown authority` / `unable to get local issuer certificate`. Fix the trust
   store (`references/tls-trust.md`); never `InsecureSkipVerify`, `NODE_TLS_REJECT_UNAUTHORIZED=0` or `verify=False`.
2. **No inline media.** A message is `text` + a separate `attachments[]` array with no position/order field,
   so media cannot be placed between paragraphs. To interleave text and images, send several messages.
3. **4000 characters, no "read more".** Every character of raw `text` counts (markup, spaces, emoji included);
   count characters, not bytes. Split longer content into several messages (`references/patterns.md`).
4. **No scheduled sending.** There is no `send_at`. Run your own scheduler.
5. **No `GET /chats` (removed 2026-06).** Track chats yourself from `bot_added` / `bot_removed` / `bot_started`
   updates. Single chat: `GET /chats/{chatId}`.
6. **`POST /chats/{chatId}/members` is retired** (restricted 2026-09-09, removed 2026-09-30). Don't build on it.
7. **Uploads are asynchronous.** After uploading, sending too early returns `attachment.not.ready` — retry
   with backoff. Upload to the `url` returned by `POST /uploads`; hosts differ per type, never hardcode them.
8. **Webhook rules.** HTTPS, port 443, certificate from a trusted CA or Минцифры (self-signed and plain HTTP
   rejected since 2026-05-25), full chain, reply `200` within 30 s. Verify `X-Max-Bot-Api-Secret` with a
   constant-time compare. After 8 h of failed deliveries the subscription is dropped.
9. **Formatting subset.** No lists, tables or horizontal rules — they arrive as plain text. Code blocks
   render as monospace but line breaks collapse into spaces. Headings, bold/italic/underline/strike, inline
   code, links, quotes, mentions, highlight work (`references/formatting.md`).
10. **Mini-app auth is server-side.** Validate `initData` on your backend with the two-step HMAC that starts
    from the `"WebAppData"` key; never trust `initDataUnsafe`. Formula and tested Go/TS code:
    `references/webhooks-and-security.md`.

## Pick your stack

| You are building | Read |
|------------------|------|
| Go bot (default path) | `references/go-client.md` → raw client `NewApi`, polling/webhook, builders |
| Go bot with routing/middleware | `references/go-maxbot.md` (optional layer on the client) |
| TypeScript / Node bot | `references/ts-client.md` |
| Any other language / raw HTTP | `references/bot-api.md` + `references/objects-and-updates.md` |
| Mini-app frontend | `references/mini-apps-bridge.md`, UI with `references/max-ui.md` |
| Mini-app backend auth | `references/webhooks-and-security.md` |
| Webhook server | `references/webhooks-and-security.md` + `references/tls-trust.md` |
| Rate limits, retries, chat tracking, scheduling, long text | `references/patterns.md` |

Both Go packages are named `maxbot`. Always import with the full path; alias one of them if you use both.

## Minimal bots

Go — long polling with the official client:

```go
package main

import (
	"context"
	"log"
	"os"
	"os/signal"
	"time"

	maxbot "github.com/max-messenger/max-bot-api-client-go/v2"
	"github.com/max-messenger/max-bot-api-client-go/v2/model"
)

func main() {
	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt)
	defer stop()

	api, err := maxbot.NewApi(os.Getenv("MAX_BOT_TOKEN"))
	if err != nil {
		log.Fatalf("init: %v", err)
	}

	var marker int64
	for ctx.Err() == nil {
		updates, next, err := api.Subscriptions.GetUpdates(ctx, marker)
		if err != nil {
			log.Printf("get updates: %v", err)
			select { // back off without ignoring shutdown
			case <-ctx.Done():
			case <-time.After(time.Second):
			}
			continue
		}
		marker = next
		for _, u := range updates {
			if u.UpdateType != model.UpdateMessageCreated {
				continue
			}
			msg := maxbot.NewMessage().
				SetChat(u.ChatID).
				SetFormat(model.FormatMarkdown).
				SetText("**Hi!** Docs: [dev.max.ru](https://dev.max.ru/docs-api)")
			if _, err := api.Messages.Send(ctx, msg); err != nil {
				log.Printf("send: %v", err)
			}
		}
	}
}
```

If this fails with an x509 error, pass an HTTP client that trusts the Минцифры root via
`maxbot.WithHTTPClient(...)` — see `references/tls-trust.md`.

TypeScript:

```ts
import { Bot } from '@maxhub/max-bot-api';

const bot = new Bot(process.env.MAX_BOT_TOKEN!);

bot.command('start', (ctx) =>
  ctx.reply('**Hi!** Docs: [dev.max.ru](https://dev.max.ru/docs-api)', { format: 'markdown' }),
);

bot.start();
```

Node does not trust the Минцифры root by default: run with
`NODE_EXTRA_CA_CERTS=/path/russian_trusted_root_ca.pem` (details in `references/tls-trust.md`).

## Common mistakes

| Wrong | Right |
|-------|-------|
| `https://api.max.ru`, `https://platform-api.max.ru` | `https://platform-api2.max.ru` |
| Disabling TLS verification to "fix" x509 errors | Trust Russian Trusted Root CA |
| `POST /webhook` | `POST /subscriptions` |
| Verifying the webhook by HMAC of the body | `X-Max-Bot-Api-Secret` header equals your secret (constant-time compare) |
| initData HMAC keyed directly with the bot token | Derive `secret = HMAC_SHA256("WebAppData", token)` first |
| `type=photo` | `type=image` |
| `disable_link_preview` in the JSON body | It is a query parameter of `POST /messages`, `POST /messages/{messageId}/comments`, and `POST /answers` — not available on `PUT` |
| `GET /chats` or `GET /chats/{link}` | Track chats from updates; `GET /chats/{chatId}` for one chat |
| Hardcoded upload hosts | Use the `url` from `POST /uploads` |
| Markdown lists/tables in messages | Plain lines, headings, quotes |
| `log.Fatal` / unhandled errors in update handlers | Log and continue; one bad update must not stop the bot |
| Ignoring callback taps | Answer with `POST /answers` (≤ 2/s per chat) |

## References

| File | Contents |
|------|----------|
| `references/sources.md` | All official sources, priority when they disagree, versions, how to check latest |
| `references/bot-api.md` | Endpoints, parameters, uploads, limits, errors, dated platform changes |
| `references/objects-and-updates.md` | Message, attachments, buttons, Update types, Chat, User, callbacks, comments |
| `references/formatting.md` | Markdown and HTML subset, mentions, what is not supported |
| `references/tls-trust.md` | Минцифры root CA for Go, Node, Docker, curl, Python; troubleshooting |
| `references/webhooks-and-security.md` | Subscriptions, delivery rules, secret header, initData, phone and contact hashes |
| `references/go-client.md` | Official Go client v2: API surface, builders, polling, webhooks, uploads |
| `references/go-maxbot.md` | maxbot framework: handlers, context, middleware; when to use it |
| `references/ts-client.md` | `@maxhub/max-bot-api`: Bot, handlers, context, keyboards, sessions, webhook |
| `references/mini-apps-bridge.md` | `window.WebApp` API, initData, deeplinks, setup |
| `references/max-ui.md` | `@maxhub/max-ui` components and setup |
| `references/patterns.md` | Rate limiting, retries, chat tracking, scheduling, splitting, idempotency |
