---
name: avito-api
description: >-
  Use when the user works with Avito (avito.ru) for business via API — объявления,
  чаты, доставка/заказы, Авито.Работа, Автозагрузка, Автотека, продвижение, Авито
  Promo, Авито Реклама, аналитика, тарифы, рейтинги. Triggers: "Avito API",
  "авито апи", "Авито Promo", avito-promo, "объявления на авито", "чаты авито",
  "Автотека", "Авито Реклама", api.avito.ru.
---

# Avito Business API

This skill helps you call the Avito Business API (`https://api.avito.ru`). It bundles the full OpenAPI 3.0 spec built from the **official developer catalog** (`developers.avito.ru/api-catalog`) — 238 paths / 245 operations across 25 sections — plus the per-section integration docs Avito publishes alongside.

The spec is large (~2.0 MB). Don't read it whole — use the helpers described below to pull only what you need.

## Authentication — OAuth2 Client Credentials

Almost every endpoint requires a Bearer token. Tokens are valid for 24h. The credentials come from the user's Avito account → Настройки → Avito API → Регистрация нового приложения, which gives a `client_id` + `client_secret`.

**Get a token:**

```bash
AVITO_CLIENT_ID=... AVITO_CLIENT_SECRET=... \
  python3 scripts/get_token.py
# prints just the access_token; add --json for the full response
```

Or directly:

```bash
curl -s -X POST https://api.avito.ru/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials&client_id=$AVITO_CLIENT_ID&client_secret=$AVITO_CLIENT_SECRET"
# {"access_token":"...","token_type":"Bearer","expires_in":86400}
```

**Use the token** in every API call as `Authorization: Bearer <token>`. On `401` — refresh and retry once. Don't re-fetch the token before every call; cache it for the session and refresh on expiry/401.

A small subset of endpoints (those that touch *another* user's data — e.g. responding to job applications on behalf of a partner) require the **OAuth2 Authorization Code** flow with scopes (`messenger:read`, `items:apply_vas`, `job:cv`, etc.). The lookup tool will show this in the operation's `security` field — if it lists `OAuth2AuthorizationCode`, the simple Client Credentials flow is not enough.

## How to find the right endpoint — DO THIS FIRST

The OpenAPI spec is too big to read whole. The skill ships a CLI to navigate it:

```bash
# 1) See all categories with endpoint counts
python3 scripts/lookup_endpoint.py tags

# 2) Find endpoints by keyword (matches path, summary, tag — case-insensitive,
#    auto-falls-back to a shorter stem so Russian inflections work)
python3 scripts/lookup_endpoint.py search чат
python3 scripts/lookup_endpoint.py search остатки      # finds "Управление остатками" too
python3 scripts/lookup_endpoint.py search --tag Продвижение
python3 scripts/lookup_endpoint.py search /autoload/v2

# 3) Get the full operation details (parameters, request/response schemas, rate limit)
python3 scripts/lookup_endpoint.py show /messenger/v2/accounts/{user_id}/chats
python3 scripts/lookup_endpoint.py show /stock-management/1/info --method post
```

`show` resolves top-level `$ref` for readability but leaves nested refs alone — for a deeper schema, read `references/avito-api-openapi.json` directly with `jq`:

```bash
jq '.components.schemas.stocksInfoResult' references/avito-api-openapi.json
```

For a category overview, browse [references/index.md](references/index.md) — a flat per-section list of all paths and summaries.

**Per-section integration docs.** Every section also has a markdown doc in `references/sections/<slug>.md` — these are the official Avito integration guides (sandbox setup, examples, edge cases, scope details) and they're often more useful than the OpenAPI spec for non-trivial flows. Available slugs (load on demand):

`accounts-hierarchy`, `ads`, `auction`, `auth`, `autoload`, `autostrategy`, `autoteka`, `avito-promo`, `calltracking`, `cpa`, `cpxpromo`, `delivery-sandbox`, `item`, `job`, `messenger`, `order-management`, `promotion`, `ratings`, `sbc-gateway`, `stock-management`, `str`, `tariff`, `trxpromo`, `user`.

(`realty-reports` is in the catalog/OpenAPI; Avito currently ships no markdown body for it, so there is no `sections/realty-reports.md`.)

**Why this matters:** the spec has many similar-looking paths (`/messenger/v1/...` vs `/messenger/v2/...`, ru/en duplicate tags, deprecated endpoints with newer replacements). Guessing leads to 404s, wrong schemas, or calling deprecated paths. Always look up before composing a request.

## Calling pattern

Once you have the endpoint details and a token:

```bash
ACCESS_TOKEN=$(AVITO_CLIENT_ID=... AVITO_CLIENT_SECRET=... python3 scripts/get_token.py)

# example: list user's items
curl -s "https://api.avito.ru/core/v1/items" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  | jq .

# example: send a chat message (Messenger v1)
curl -s -X POST "https://api.avito.ru/messenger/v1/accounts/$USER_ID/chats/$CHAT_ID/messages" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"type":"text","message":{"text":"Здравствуйте! Чем могу помочь?"}}'
```

For Python, use `requests` (or `httpx`) with the same Bearer header. There's no need for a heavy Avito SDK — every endpoint is a plain JSON HTTP call.

## Conventions and gotchas

- **Base URL** is always `https://api.avito.ru` (no trailing slash). Paths in the spec are appended directly.
- **User ID** (`user_id` in messenger and similar endpoints) is the numeric Avito account ID, not the login. Get it from `GET /core/v1/accounts/self`.
- **Rate limits** are per-endpoint. The spec exposes them in `x-rate-limiter.default` (requests per minute). Some endpoints cap at 5 rpm (CallTracking), others at 1000 rpm. Respect them — `429` responses are common otherwise.
- **Pagination** is mostly `limit`/`offset` query params. Some newer endpoints use cursor-based pagination; check the response schema with `show`.
- **Date formats** are RFC3339 unless the field description says otherwise. Some Autoload endpoints use Unix timestamps.
- **Timezones**: many endpoints accept and return UTC. Don't pass local time without a `Z` or `+03:00` suffix.
- **Versioning**: when `/v1` and `/v2` of the same path both exist, prefer `/v2`. Endpoints with `(deprecated)` in the summary are still callable but will be removed — flag this to the user instead of silently using them.
- **Autoload deprecation / migration:** several Autoload report/list methods are being retired. Official docs: partial degradation from **08.09.2026** (methods start returning less data); removal with **HTTP 410 Gone** on **08.03.2027**. Prefer the current v4 upload-status paths (`/autoload/v4/uploads/...`) and read `sections/autoload.md` + the catalog migration plan before writing new Autoload integrations.
- **Shared path+method across sections:** a few operations appear in more than one catalog section (e.g. Promo agency stats vs item stats, `/token` in auth vs autoteka). The merged OpenAPI keeps one **canonical** body (`x-avito-section`) and lists other publishers in `x-avito-also-in`. Do not invent extra OAuth scopes for Авито Promo — official Promo agency ops use the section’s published `security` (typically Client Credentials as declared on the operation); check `show` rather than assuming scopes.
- **Russian/English duplicate tags** (`Messenger` and `Мессенджер`, `Доставка`, etc.) refer to the same endpoints. The lookup tool handles both — search either language.
- **Spec text vs JSON schema can disagree on limits.** Several Avito operations have a stricter cap in the prose `description` than in the machine-readable schema. Real example: `POST /stock-management/1/info` has `description` saying «макс. 10 элементов в одном запросе», while the JSON schema sets `maxItems: 500`. Empirical reality matches the description — sending 11+ ids returns HTTP 500, not a graceful 400. **Trust the description for hard caps; if you must push the limit, probe with one over-limit request first instead of a full batch.** Same caution for rate limits: `x-rate-limiter.default` is the floor, not always the ceiling.
- **Field naming is mostly camelCase but stock-management uses snake_case** (`item_ids`, `external_id`, `is_unlimited`). Don't assume one convention across the API — read the request body schema with `show` before composing.

## Errors

Standard HTTP codes. **The error body shape is not consistent across endpoints** — Avito uses several. The two most common ones in the wild:

```json
// shape A — short list of human-readable strings
{"errors": ["Тариф должен принадлежать к категории \"Транспорт\"."]}

// shape B — single structured error
{"error": {"code": 400, "message": "human-readable reason"}}
```

Other endpoints return `{"result": {"status": "error", "messages": [...]}}` or a bare `{"message": "...", "code": N}`. Don't write code that depends on one specific shape — log the full body, extract any non-empty string-ish field for display.

Common codes:

- `400` — validation: re-read the request schema with `show`.
- `401` — token expired or revoked: refresh once and retry.
- `403` — your Client Credentials don't grant this scope. Many endpoints need the Authorization Code flow with a specific scope (e.g. `messenger:write`, `items:apply_vas`, `job:cv`) — check the operation's `security` field via `show`.
- `404` — wrong path, wrong ID, item belongs to a different user, OR a soft "not applicable" (e.g. `/tariff/info/1` returns 404 with `errors: [...]` for non-Транспорт accounts — that's not a path bug).
- `429` — rate limit: back off, halve the request rate, retry with exponential backoff.
- `5xx` — Avito's side: retry with backoff.

When you report an error to the user, include the HTTP code and the full body — different endpoints surface different fields.

## Sections at a glance

25 sections, sorted by endpoint count (canonical `x-avito-section` attribution). Full list with paths is in [references/index.md](references/index.md).

| Section | # | Notes |
|---|---:|---|
| Доставка | 31 | Avito Доставка integration: parcel processing, tariffs, sandbox. Includes B2C Дверь–Терминал and reverse-direction flows. Detailed sandbox docs in `sections/delivery-sandbox.md`. |
| Автотека | 27 | Paid car history reports. |
| Авито.Работа | 25 | Vacancies, applications, resumes, webhooks. Mix of v1 and v2 — prefer v2. |
| Авито Реклама | 24 | Ads cabinet API (`/ads/v1/...`): accounts, advertisers, contracts, campaigns/groups/creatives stats, budgets. Own `client_id`/`client_secret` from the Авито Реклама cabinet (per ad account). Sandbox at `/ads-sandbox/`. Partial multi-entity responses use `207 Multi-Status` with per-item `warnings` — see `sections/ads.md`. |
| Автозагрузка | 22 | Bulk listing upload via XML/JSON feeds. Prefer `/autoload/v4/uploads/...` for upload status. Legacy report/list methods: partial degradation from **08.09.2026**, removal / **410 Gone** on **08.03.2027** — see `sections/autoload.md` and the official migration plan. |
| Мессенджер | 13 | Chats and messages. v1 and v2 both exist; v2 is the current one for reads. Sending text messages is still `POST /messenger/v1/.../messages`. |
| Управление заказами | 12 | Order lifecycle for marketplace sellers, including label generation. |
| CPA Авито | 11 | Performance-billing actions, complaints, chats by time. |
| Авито Promo | 11 | Agency API (`avito-promo`): client list/invite/INN checks, agency balance & transfers, client stats. Official catalog also publishes 2 stats paths shared with Объявления (`x-avito-also-in`); use `show` for the canonical security/schema. Do not invent Promo-specific OAuth scopes beyond what the operation declares. |
| Объявления | 11 | Item CRUD-ish: list, view, status, edit price, deactivate. Owns canonical stats ops also listed under Promo. |
| Автостратегия | 7 | Auto-bidding strategies. |
| Иерархия Аккаунтов | 7 | Multi-account / agency setups. Employee calls on behalf of a company need the `X-Employee-Of` header (`X-Is-Employee` is deprecated). Prefer `checkAhUserV2` + `getAhInfoV1`. |
| Продвижение | 7 | Paid promotion services and BBIP (bbip = повышенный показ). |
| Настройка цены целевого действия | 5 | CPA price tuning (`cpxpromo`). |
| Краткосрочная аренда | 5 | STR (short-term rent). |
| Рассылка скидок и спецпредложений в мессенджере (beta-version) | 5 | `sbc-gateway`. |
| Рейтинги и отзывы | 4 | |
| CallTracking[КТ] | 3 | Strict 5 rpm limit. Audio recordings ~30 min after call ends. |
| TrxPromo | 3 | Promo transactions. |
| Информация о пользователе | 3 | `GET /core/v1/accounts/self`, etc. |
| CPA-аукцион | 2 | |
| Авторизация | 2 | Token issue/refresh paths unique to auth; `/token` is also published by Автотека (canonical body may be the latter — see `x-avito-also-in`). |
| Аналитика по недвижимости | 2 | Realty market price reports (`realty-reports`). |
| Управление остатками | 2 | Read + bulk update stock quantities. |
| Тарифы | 1 | Current + scheduled tariff info. **Транспорт only, non-CPA.** |

For non-trivial flows (delivery sandbox, Promo agency, scope/auth setup, vacancies v2), open the matching `references/sections/<slug>.md` first — those docs cover prerequisites and gotchas the OpenAPI spec doesn't.

## Working with the user

- If the user's request maps to one obvious endpoint, look it up, show them the call you're about to make (URL, method, body), and execute when they confirm.
- If the request is ambiguous (e.g. "посмотри статистику по объявлениям" — Stats? Autoload reports? CPA?), `search` first and ask which they mean before making calls.
- When credentials are missing, ask for `AVITO_CLIENT_ID` / `AVITO_CLIENT_SECRET` and explain where to get them (Avito personal cabinet → API). Don't fabricate test calls without credentials — instead, prepare the curl/python command and let the user run it.
- Watch out for endpoints that mutate state (POST/PUT/DELETE on items, orders, messages). Confirm with the user before sending — sending a chat message or deactivating a listing is not undoable.
