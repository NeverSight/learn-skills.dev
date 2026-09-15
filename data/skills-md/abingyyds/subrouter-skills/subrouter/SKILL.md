---
name: subrouter
description: 'Connect an AI agent (Claude Code, Cursor, Codex, etc.) to SubRouter — an OpenAI/Anthropic-compatible AI API gateway with smart routing and transparent pricing. Use this skill to authorize the agent via device flow, obtain an API key, pick a model by price, and configure the client. Also lets a distributor station owner (分站站长) run their station: list or delist models, set prices, manage packages and settings. Triggers: "接入 SubRouter", "配置 SubRouter", "SubRouter API key", "用 SubRouter 的模型", "管理我的分站", "分站上架", "分站套餐".'
---

# SubRouter Agent Onboarding

SubRouter is an AI API gateway: one API key, OpenAI- and Anthropic-compatible endpoints, per-request smart routing across providers, transparent per-token billing. This skill teaches an agent how to connect a user to SubRouter end to end.

Base URL: use the site the user names, or the default `https://subrouter.ai`. All examples below use `$BASE`.

## Security rules (non-negotiable)

- Send the API key ONLY to the SubRouter host the user chose. Never to any other domain.
- Always call with `--max-redirs 0` so a redirect can never carry the key elsewhere.
- Never print the full key into logs or files other than the client config the user asked for. Show at most a `sk-xxxx…` prefix when confirming.
- **Never let a credential reach stdout.** The authorization responses carry `device_code`, `key` and `access_token` in full; a bare `curl` prints them into the terminal and into the agent transcript. Always write those responses to a `0600` file and read individual fields out of it (Step 1 shows how). Report only status, `user_code`, the verification URL, and a `sk-` prefix.
- Payment is ALWAYS done by the user in their browser. Never handle card numbers, crypto seeds, or payment credentials.

## Step 0 — Agree on what you are about to change (do this first)

Getting a key and rewiring someone's coding agent are different jobs. Never infer the second from a request for the first. Before Step 1, state what you understood and get a yes:

1. **Goal** — which of these does the user want?
   - *Account only*: authorize and show the key, change nothing on disk.
   - *One-off call*: use the key in this session via env vars; nothing is written into any config, but the credential file from Step 1 stays (see Step 1) unless the user asks you to delete it.
   - *Configure an SDK/app*: write into a project the user names.
   - *Switch a coding agent's model provider*: repoint Claude Code / Codex / Cursor at SubRouter.
2. **Target** — exactly which file(s) you would touch, by absolute path, and whether the change is session-only or persistent.
3. **Existing setup** — read the target first and say what is already there. If it already holds credentials or a provider, say so and ask before touching it.

Default to the least invasive option that satisfies the request. When unsure, stop at *account only* and ask.

**Codex specifically:** most Codex users are signed in with a ChatGPT subscription, not an API key. Do **not** write `~/.codex/config.toml`, do not overwrite `~/.codex/auth.json`, and do not replace an existing `model_provider` unless the user explicitly asked to move Codex onto SubRouter. Show them the config you would add and let them approve it.

Never overwrite an existing config file. Append, or write a new profile, and tell the user how to revert.

## Step 1 — Device authorization (get an API key)

**Before starting a new flow, look for a credential you already saved** (`~/.subrouter/credentials.json` or whatever file/env var you persisted in a previous run). If `GET $BASE/v1/models` with that `sk-` key returns 200, reuse it and skip to Step 2; only authorize again when there is no saved key or it no longer works.

Start a device authorization. `channel` identifies your agent type (`claude`, `cursor`, `codex`, …). Re-authorizing with the same `channel` returns the account's existing enabled `Agent 授权令牌 (<channel>)` token instead of creating another one, so repeated logins do not pile up keys — but the key is still delivered only through this flow, so keep it once you have it:

**Every endpoint under `/api` wraps its result in an envelope.** The payload is always under `data`, alongside `success` — `{"success":true,"message":"","data":{…}}`. Some endpoints add siblings (`/api/pricing` also returns `vendors`, `usable_group`, `group_ratio`; `/api/marketplace/models` returns `total`), so read `.data` explicitly rather than assuming the whole body is the payload. On failure `success` is `false` and `message` carries the reason. Endpoints under `/v1` are the raw OpenAI/Anthropic shapes and are **not** enveloped.

Write the response to a private file instead of letting it print:

```bash
umask 077
AUTH_TMP="$(mktemp -t subrouter-auth)"        # 0600 via umask
curl -s --max-redirs 0 -X POST "$BASE/api/device_auth" \
  -H 'Content-Type: application/json' \
  -d '{"channel":"claude"}' -o "$AUTH_TMP"
```

`.data` holds:

```json
{
  "user_code": "ABCD-2345",
  "device_code": "<64-char secret — never print this>",
  "verification_url": "https://subrouter.ai/device?code=ABCD-2345",
  "expires_in": 600,
  "interval": 3
}
```

Read `.data.user_code` and `.data.verification_url` out of the file and show only those. `device_code` is the machine-held secret: anyone who sees it can claim the key before you do, so it must never be echoed.

Tell the user to open the URL in a browser, log in (or register), check that the page shows the same `user_code`, and confirm. The code expires in 10 minutes.

Then poll every `.data.interval` seconds (never faster), again writing to the private file:

```bash
curl -s --max-redirs 0 -X POST "$BASE/api/device_auth/poll" \
  -H 'Content-Type: application/json' \
  -d "{\"device_code\":\"$DEVICE_CODE\"}" -o "$AUTH_TMP"
```

Branch on `.data.status`:

- `authorization_pending` — keep waiting.
- `slow_down` — you polled too fast; wait longer.
- `approved` — `.data.key` (`sk-…`), `.data.access_token`, `.data.user_id` and `.data.base_url` are now filled. **Delivered exactly once**: if you lose them you must redo the whole flow. Persist them from the file, never via an echo.
- `success:false` with "invalid or expired" — the flow expired or was already consumed; start over from Step 1.

Keep the credential. Move the approved response out of the temp path into a
stable private file the next session can find, for example
`install -m 600 "$AUTH_TMP" ~/.subrouter/credentials.json` (create the directory
with `mkdir -p -m 700 ~/.subrouter`). **Do not delete it when the task ends**:
the token does not expire, and deleting it is what forces the user through the
browser approval again next time. Remove the file only when the user asks you
to, and say which file you removed.

You receive three values, with different powers:

- `key` (`sk-…`) — the **relay token**: model calls, `/v1/models`, billing lookups. Put this in client configs.
- `access_token` — the **account management credential**: full management API access under the user's account. Never put this in a client config; use it only for the management calls below, and guard it even more carefully than the sk key.
- `user_id` — the numeric account id. Not a secret, but **every management call fails without it** (see below). Store it next to the access token.

## Step 2 — Configure the client

The same key works on both protocol surfaces.

Claude Code (Anthropic protocol):

```bash
export ANTHROPIC_BASE_URL="$BASE"
export ANTHROPIC_API_KEY="sk-…"
```

OpenAI SDK / Cursor / Codex (OpenAI protocol):

```bash
export OPENAI_BASE_URL="$BASE/v1"
export OPENAI_API_KEY="sk-…"
```

Core endpoints: `POST /v1/chat/completions` (OpenAI), `POST /v1/messages` (Anthropic), `GET /v1/models`.

The sk key also serves the full multimodal surface (availability depends on the model — check `/api/pricing`):

- Images and video: see "Step 2b" below — **use the async task API**, not the synchronous endpoints
- Audio: `POST /v1/audio/transcriptions`, `/v1/audio/speech`, `/v1/audio/translations`
- Other: `POST /v1/embeddings`, `/v1/rerank`, `/v1/moderations`, `/v1/responses`, `GET /v1/realtime` (WebSocket)

## Step 2b — Images and video: use the async task API

Image and video generation take tens of seconds to several minutes. A synchronous call holds one HTTP connection for that whole time, which is what makes it fail: proxies and CDNs in front of the gateway time out at 504, and running several in parallel exhausts connections and produces 502s. **Default to async.**

| Case | Use |
|---|---|
| Video, any model | Async — always. Never call video synchronously. |
| Images, more than one at a time | Async |
| Images, batch or unattended | Async |
| A single image, user is waiting interactively | Sync is acceptable |

### Billing rules (read before generating anything)

**Every successful generation is billed, including retries.** These rules are not optional:

- **One submission per user request.** Do not generate several variants, sizes or "improved" versions on your own initiative. If the user asked for one image, submit once.
- **A retry is a new charge.** Before resubmitting after a failure, a timeout, or output the user disliked, say so explicitly — "this will bill another generation" — and get a yes. The only exception is a submission that failed before billing (a 4xx rejection with no task id).
- **Never discard a billed artifact.** Every completed task's output must be written to disk before you move on, including intermediate attempts the user did not end up liking. Losing a paid image because a later attempt overwrote it is a real loss of the user's money. Use distinct filenames per task id; never reuse one path across attempts.
- **Download completed results promptly.** Upstream result URLs expire. Fetch and save as soon as `status` is `completed`; do not leave a finished task unclaimed while you do something else.
- **Validate before submitting**, not after: check `size`/aspect ratio, duration and model capability against `/api/pricing` first. A rejected parameter after billing is money gone.
- **Report at the end**: how many generations were submitted, the model, the size/duration, the total cost, and the absolute path of every saved file.

If the connection drops mid-flow, do not resubmit. The task already exists server-side — recover it via `GET /api/task/self` (Listing past tasks, below) and download the result. This is the main reason to prefer async: a dropped sync call loses an image you already paid for.

### Submit

Images — append `/async` to the normal path:

```bash
curl -s --max-redirs 0 -X POST "$BASE/v1/images/generations/async" \
  -H "Authorization: Bearer sk-…" -H 'Content-Type: application/json' \
  -d '{"model":"<image-model>","prompt":"…","n":1,"size":"1024x1024"}'
```

`POST /v1/images/edits/async` works the same way.

Answers `202 Accepted` with a `Location: /v1/tasks/{task_id}` header and a `media.task` body:

```json
{"id":"…","object":"media.task","type":"image","action":"generate",
 "status":"pending","progress":0,"model":"…","created_at":1756400000,
 "result":{"images":[],"videos":[]},"usage":{"quota":1234},"error":null}
```

The `/async` facade always yields a task, even when the upstream merchant only supports synchronous calls — the gateway runs it in the background for you.

Video — `POST /v1/video/generations` is already asynchronous; the request body follows the model's own schema. The response is the platform's native submit shape, but the task id in it is SubRouter's, so poll it the same way. `POST /v1/videos` is the OpenAI-compatible alias.

### Poll

One endpoint covers both image and video tasks:

```bash
curl -s --max-redirs 0 "$BASE/v1/tasks/<task_id>" -H "Authorization: Bearer sk-…"
```

`status` is one of `pending`, `processing`, `completed`, `failed`. Poll no faster than every 2–3 seconds, and back off for long video jobs. On `completed` read `result.images[].url` / `result.images[].b64_json` for images and `result.videos[].url` for video; on `failed` read `error.message`. `result` always carries both arrays — the one that does not match the task type stays empty rather than null.

Native per-platform poll paths also exist (`GET /v1/images/generations/{task_id}`, `GET /v1/video/generations/{task_id}`, `GET /v1/videos/{task_id}`) — prefer `/v1/tasks/{task_id}`, whose shape is identical across every model.

### Download the video

```bash
curl -fL "$BASE/v1/videos/<task_id>/content" -H "Authorization: Bearer sk-…" -o out.mp4
```

Upstream video URLs are often short-lived or geo-restricted; this endpoint streams the file through the gateway with the sk key. Use it instead of fetching `result.videos[].url` directly.

### Listing past tasks

`GET /api/task/self` (with the access token) lists the user's media tasks — useful for recovering a task id the client lost.

## Step 3 — Pick a model (and optionally a provider)

Prices and the provider marketplace are public and need no auth:

```bash
curl -s --max-redirs 0 "$BASE/api/pricing"                        # models + prices
curl -s --max-redirs 0 "$BASE/api/marketplace/models"             # marketplace models with provider offers
curl -s --max-redirs 0 "$BASE/api/marketplace/providers"          # provider (商家) list
curl -s --max-redirs 0 "$BASE/api/marketplace/providers/<slug>"   # one provider's detail
curl -s --max-redirs 0 "$BASE/api/marketplace/reviews"            # provider reviews
```

Choose by the user's stated preference (cheapest, specific vendor/provider, capability). Present the top candidates with prices and let the user pick; do not guess silently.

## Step 4 — Top up (user does this, not you)

**Check the balance before assuming anything.** A freshly registered account has none, but a returning user re-authorizing an existing account may already be funded. Only point the user at `$BASE/console/topup` once you have seen a zero/insufficient balance or received a 402. Top-up always happens in the user's browser.

```bash
curl -s --max-redirs 0 "$BASE/v1/dashboard/billing/subscription" -H "Authorization: Bearer sk-…"
curl -s --max-redirs 0 "$BASE/v1/dashboard/billing/usage" -H "Authorization: Bearer sk-…"
```

## Account management (uses `access_token`)

Management endpoints need **two** headers, not one:

- `Authorization: Bearer <access_token>` (the `Bearer ` prefix is optional)
- `New-Api-User: <user_id>` — the numeric account id from Step 1

Both are mandatory. Sending only the first returns `401 无权进行此操作，未提供 New-Api-User`, and a `user_id` that does not match the access token's owner returns `401 New-Api-User 与登录用户不匹配` — so it cannot be guessed. This applies to every `/api` management endpoint below, including the provider (商家) ones.

```bash
AUTH='Authorization: Bearer <access_token>'
AUTH_USER='New-Api-User: <user_id>'

# Account info & balance
curl -s --max-redirs 0 "$BASE/api/user/self" -H "$AUTH" -H "$AUTH_USER"

# Usage reconciliation ("where did my money go")
curl -s --max-redirs 0 "$BASE/api/log/self?p=1&page_size=20" -H "$AUTH" -H "$AUTH_USER"   # per-call logs
curl -s --max-redirs 0 "$BASE/api/log/self/stat" -H "$AUTH" -H "$AUTH_USER"               # totals
curl -s --max-redirs 0 "$BASE/api/data/self" -H "$AUTH" -H "$AUTH_USER"                   # per-day quota usage
curl -s --max-redirs 0 "$BASE/api/task/self" -H "$AUTH" -H "$AUTH_USER"                   # async media tasks

# Redeem a voucher code the user already has (this is NOT payment)
curl -s --max-redirs 0 -X POST "$BASE/api/user/self/topup" -H "$AUTH" -H "$AUTH_USER" \
  -H 'Content-Type: application/json' -d '{"key":"<redemption-code>"}'

# Referral: the user's invite code and earnings
curl -s --max-redirs 0 "$BASE/api/user/self/aff" -H "$AUTH" -H "$AUTH_USER"               # invite code → share $BASE/register?aff=<code>
curl -s --max-redirs 0 "$BASE/api/user/self/aff_dashboard" -H "$AUTH" -H "$AUTH_USER"
curl -s --max-redirs 0 "$BASE/api/user/self/aff_earnings" -H "$AUTH" -H "$AUTH_USER"
# Move referral earnings into the usable balance (confirm amount with the user first)
# NOTE: quota is in internal units, 500000 = $1 — never pass a dollar number directly
curl -s --max-redirs 0 -X POST "$BASE/api/user/self/aff_transfer" -H "$AUTH" -H "$AUTH_USER" \
  -H 'Content-Type: application/json' -d '{"quota":<amount-in-quota-units>}'

# List / create API tokens
curl -s --max-redirs 0 "$BASE/api/token/" -H "$AUTH" -H "$AUTH_USER"
curl -s --max-redirs 0 -X POST "$BASE/api/token/" -H "$AUTH" -H "$AUTH_USER" \
  -H 'Content-Type: application/json' \
  -d '{"name":"my-project","expired_time":-1,"unlimited_quota":true}'
```

### Model- or provider-scoped keys

A token can be restricted to specific models, to specific providers (商家) per model, and to a price ceiling. Use this when the user says "只用某商家" or "只允许这个模型":

```bash
curl -s --max-redirs 0 -X POST "$BASE/api/token/" -H "$AUTH" -H "$AUTH_USER" \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "sonnet-via-acme",
    "expired_time": -1,
    "unlimited_quota": true,
    "model_limits_enabled": true,
    "model_limits": "claude-sonnet-4-6,claude-haiku-4-5",
    "subrouter_model_providers": "{\"claude-sonnet-4-6\":[\"acme\"]}"
  }'
```

- `model_limits` — comma-separated model whitelist (with `model_limits_enabled: true`).
- `subrouter_model_providers` — a JSON **string** mapping model name → allowed provider slugs; slugs come from `GET /api/marketplace/providers`. Models not listed keep normal routing.
- `subrouter_model_price_limits` — optional per-model input/output price caps (JSON string as well).

Echo the exact restrictions back to the user before creating the key.

### Becoming a provider (商家) and listing models

The user's account can apply to become a provider and then manage its own channels and models — all with the same `access_token`:

```bash
# Apply to become a provider (platform review may apply)
curl -s --max-redirs 0 -X POST "$BASE/api/provider/register" -H "$AUTH" -H "$AUTH_USER" \
  -H 'Content-Type: application/json' -d '{...}'

# After approval, provider management lives under /api/provider/*
curl -s --max-redirs 0 "$BASE/api/provider/self" -H "$AUTH" -H "$AUTH_USER"      # provider profile
curl -s --max-redirs 0 "$BASE/api/provider/models" -H "$AUTH" -H "$AUTH_USER"    # listed models
# List a model: POST /api/provider/models — GET first to learn the field shape
# Edit a model: PUT /api/provider/models/<id>. Pricing is all-or-nothing: to change
# the price send the COMPLETE billing block (billing_mode plus billing_expr, or
# input_price/output_price/fixed_price plus price_currency); to leave the price
# alone send NO pricing field at all. A body with only some of them is read as a
# price change with the missing ones as 0 and goes into price review.
# Channels: /api/provider/channels (GET/POST/PUT/DELETE)

# Bulk model maintenance (e.g. syncing upstream price changes)
# POST /api/provider/models/batch          — create many models at once
# POST /api/provider/models/batch-status   — enable/disable in bulk
# POST /api/provider/models/batch-delete   — remove in bulk

# Channel debugging — <id> is a channel id from GET /api/provider/channels
curl -s --max-redirs 0 "$BASE/api/provider/channels/<id>/test" -H "$AUTH" -H "$AUTH_USER"
curl -s --max-redirs 0 "$BASE/api/provider/channels/<id>/fetch_models" -H "$AUTH" -H "$AUTH_USER"

# Earnings (read-only)
curl -s --max-redirs 0 "$BASE/api/provider/earnings/summary" -H "$AUTH" -H "$AUTH_USER"
curl -s --max-redirs 0 "$BASE/api/provider/earnings" -H "$AUTH" -H "$AUTH_USER"
curl -s --max-redirs 0 "$BASE/api/provider/payouts" -H "$AUTH" -H "$AUTH_USER"   # payout history
```

Withdrawing money (`POST /api/provider/payout`) is a funds operation: do NOT call it yourself — send the user to the provider console in their browser.

Before submitting a provider application or changing anything that affects listings, prices, or money, state exactly what you are about to send and get the user's explicit confirmation. For bulk operations, show the full change list (model names, prices, statuses) first.

## Running a distributor station (分站站长)

A distributor (分销商) is a user who runs their own SubRouter-powered station. Station management lives under `/api/distributor/*` and uses the same `access_token` + `New-Api-User` pair as the account calls above; the account must already hold the distributor role. Becoming a distributor, and renewing or buying a discount for the station, is paid in the browser at `$BASE/console/distributor` — never call those endpoints (`/api/distributor/register/pay`, `/subscription/renew`, `/discount/buy`).

**Always call the main site.** `$BASE` here is the main SubRouter host (`https://subrouter.ai` unless the user names another main site), never the station's own domain: a station domain refuses every `/api` path except `/api/dist/*` with `403 该接口不能通过分站域名访问`. Run Step 1 against the main site too.

Read the station before changing anything, and re-read before every write — several PUT endpoints replace the whole object:

```bash
curl -s --max-redirs 0 "$BASE/api/distributor/self" -H "$AUTH" -H "$AUTH_USER"        # name, domain, display_mode, enable_all_models, global_markup, registration_mode, …
curl -s --max-redirs 0 "$BASE/api/distributor/dashboard" -H "$AUTH" -H "$AUTH_USER"   # traffic, revenue, customer counts
```

### Which listing mode the station is in

`enable_all_models` on `/self` decides how models reach the shelf, and the two modes use different endpoints. Check it first and use the matching family.

| `enable_all_models` | How models get listed | Endpoints |
|---|---|---|
| `true` (全站上架) | Every model of every provider the owner subscribes to is listed automatically; the owner only excludes or reprices | `/models/global*` |
| `false` (manual) | The owner lists models one by one | `/models`, `/providers/:id/models` |

Both modes share one precondition: the owner's own account must subscribe to a provider on the main marketplace before any of its models can be listed, or the API answers `该商家不在当前分站订阅范围内`. `GET /api/distributor/providers?keyword=&page=1&page_size=50` lists only the subscribed providers. To add one, `POST /api/marketplace/subscribe` with `{"provider_id":<id>}` (ids come from `GET /api/marketplace/providers`); `DELETE /api/marketplace/subscribe/<id>` reverses it. Subscribing costs nothing by itself.

`provider_id` values returned by these endpoints may be virtual ids that stand for a shared plan rather than a provider. Pass them through unchanged; never construct one.

### 上架 / 下架 with 全站上架 on

```bash
curl -s --max-redirs 0 "$BASE/api/distributor/models/global" -H "$AUTH" -H "$AUTH_USER"
# items: provider_id, provider_slug, provider_name, model_name, display_name, enabled,
#        input_price, output_price, fixed_price, price_currency, has_custom_price, custom_*

# 下架 one model (adds an exclusion); "enabled": true restores it
curl -s --max-redirs 0 -X PUT "$BASE/api/distributor/models/global/status" -H "$AUTH" -H "$AUTH_USER" \
  -H 'Content-Type: application/json' -d '{"provider_id":12,"model_name":"gpt-5.4","enabled":false}'

# a whole provider at once
curl -s --max-redirs 0 -X PUT "$BASE/api/distributor/models/global/provider-status" -H "$AUTH" -H "$AUTH_USER" \
  -H 'Content-Type: application/json' -d '{"provider_id":12,"enabled":false}'

# override the price of one model; omit a field to leave it alone
curl -s --max-redirs 0 -X PUT "$BASE/api/distributor/models/global/price" -H "$AUTH" -H "$AUTH_USER" \
  -H 'Content-Type: application/json' \
  -d '{"provider_id":12,"model_name":"gpt-5.4","custom_input_price":2.5,"custom_output_price":10}'
# alternatives: "custom_fixed_price" (per-call models), "custom_price_multiplier";
# {"provider_id":12,"model_name":"gpt-5.4","clear_custom_pricing":true} returns to provider price + markup
```

### 上架 / 下架 in manual mode

```bash
curl -s --max-redirs 0 "$BASE/api/distributor/models" -H "$AUTH" -H "$AUTH_USER"                       # what is listed now (id, provider_id, model_name, display_name, markup_percent, custom_*_price, enabled, sort_order)
curl -s --max-redirs 0 "$BASE/api/distributor/providers/12/models" -H "$AUTH" -H "$AUTH_USER"          # a provider's catalogue, marked with what the station already lists

# 上架 several models from one provider
curl -s --max-redirs 0 -X POST "$BASE/api/distributor/providers/12/models" -H "$AUTH" -H "$AUTH_USER" \
  -H 'Content-Type: application/json' \
  -d '{"models":[{"model_name":"gpt-5.4","display_name":""},{"model_name":"gpt-5.4-mini","display_name":""}]}'

# 上架 one model with its own markup
curl -s --max-redirs 0 -X POST "$BASE/api/distributor/models" -H "$AUTH" -H "$AUTH_USER" \
  -H 'Content-Type: application/json' \
  -d '{"provider_id":12,"model_name":"gpt-5.4","display_name":"","markup_percent":20,"enabled":true,"sort_order":0}'

# edit: send the full record from GET /models with your changes. display_name, markup_percent,
# custom_input_price, custom_output_price and sort_order are overwritten by whatever you send;
# "enabled" only changes when present.
curl -s --max-redirs 0 -X PUT "$BASE/api/distributor/models/<id>" -H "$AUTH" -H "$AUTH_USER" \
  -H 'Content-Type: application/json' -d '{...full record..., "enabled": false}'

# 下架 for good: remove the record. PUT enabled:false hides it but keeps the configuration.
curl -s --max-redirs 0 -X DELETE "$BASE/api/distributor/models/<id>" -H "$AUTH" -H "$AUTH_USER"
```

### Pricing rules

- `global_markup` (set via `PUT /self`) is a percentage — `30` means +30% — applied to every listed model without its own price.
- Per model, `markup_percent` (`0` = use the global value) or explicit `custom_input_price` / `custom_output_price`. Custom prices are per million tokens in the currency the listing reports as `price_currency`; read it before setting a number.
- The change list you show the user must carry the effective price after markup, not just the percentage.

### 套餐 (packages)

```bash
curl -s --max-redirs 0 "$BASE/api/distributor/packages" -H "$AUTH" -H "$AUTH_USER"

curl -s --max-redirs 0 -X POST "$BASE/api/distributor/packages" -H "$AUTH" -H "$AUTH_USER" \
  -H 'Content-Type: application/json' \
  -d '{"name":"入门包","description":"","type":"quota","price":99,"original_price":129,
       "quota_amount":50000000,"duration":30,"quota_reset_period":"never","enabled":true,"sort_order":0}'
```

Server rules: `name` required, at most 128 characters; `type` is `quota`, `daily`, `weekly` or `monthly`; `price` in CNY, must be > 0; `original_price` ≥ 0 (the strike-through price); `quota_amount` > 0 **in quota units, 500000 = $1** — a "$100 package" is `50000000`; `duration` in days, defaults to 30; `quota_reset_period` is `never`, `daily`, `weekly` or `monthly`.

`PUT /api/distributor/packages/<id>` replaces every field — send the full object from GET with the change applied. `DELETE /api/distributor/packages/<id>` removes it.

Sold packages: `GET /api/distributor/package-subscriptions` lists them; `POST /package-subscriptions/<id>/reset-usage` and `POST /package-subscriptions/<id>/invalidate` change what a paying customer receives — name the customer and the effect, then get a yes.

### Station settings

`PUT /api/distributor/self` is a partial update: only the fields you send change. The ones an owner usually asks for: `name`, `domain`, `logo`, `favicon`, `announcement`, `display_mode` (`simple` or `full`), `registration_mode` (`open`, `invite`, `closed`), `global_markup`, `enable_all_models`, `enable_topup`, `hide_provider_info`, `currency_display`. Read `GET /self`, show each key as old → new, then write.

Never set the payment, mail or OAuth credential fields (`epay_*`, `stripe_*`, `creem_*`, `smtp_*`, `*_oauth_client_id`, `*_oauth_client_secret`, `theme_password`) — the owner enters those in the console.

Routing sources and markup live on the same endpoint and decide what the station earns, so read them back before and after a change:

| Field | Default | Effect |
| --- | --- | --- |
| `include_official_channels` | `true` | Whether station keys may route to platform official channels |
| `include_shared_subscriptions` | `true` | Whether station keys may route to subscription-sharing lines |
| `include_provider_self` | `true` | Whether station keys may route to a provider's own listings |
| `include_cache_hit_rate` | `true` | Weigh cache hit rate when ordering candidates |
| `subrouter_route_preference` | platform default | Candidate ordering, e.g. `price_first`, `stability_first` |
| `shared_subscription_markup` | `0` | Markup applied to shared-subscription routes, 0-10000 (percent) |

Every row above except `shared_subscription_markup` only takes effect when `display_mode` is `simple`. Under `full` the station value is ignored and each key carries its own copy of it, so writing the station value there returns success but changes no routing.

Turning a source off removes every model that only that source provided — those calls start failing for customers rather than becoming more profitable. Say which models disappear before writing.

### Customers, key groups, shared subscriptions, official channels

```bash
# Customers (the station's end users)
curl -s --max-redirs 0 "$BASE/api/distributor/customers?page=1&page_size=20&keyword=" -H "$AUTH" -H "$AUTH_USER"
curl -s --max-redirs 0 "$BASE/api/distributor/customers/<userId>/dashboard" -H "$AUTH" -H "$AUTH_USER"
# status 1 = enabled, 2 = banned — confirm with the owner first
curl -s --max-redirs 0 -X PUT "$BASE/api/distributor/customers/<userId>/status" -H "$AUTH" -H "$AUTH_USER" \
  -H 'Content-Type: application/json' -d '{"status":2}'

# Key groups (bundles of listed models sold under one label)
curl -s --max-redirs 0 "$BASE/api/distributor/key-groups" -H "$AUTH" -H "$AUTH_USER"
curl -s --max-redirs 0 "$BASE/api/distributor/key-groups/models" -H "$AUTH" -H "$AUTH_USER"      # models a group may include
# POST /key-groups and PUT /key-groups/<id> take the group record: name, vendor_category, description,
# model_limits (comma-separated, only models from /key-groups/models), subrouter_providers (comma-separated slugs),
# price_discount (0.8 = 20% off), is_private, is_recommended, enabled, sort_order.
# Members of a private group: GET/POST /key-groups/<id>/users, DELETE /key-groups/<id>/users/<userId>

# Shared subscriptions (进货 a shared plan, then list it)
curl -s --max-redirs 0 "$BASE/api/distributor/shared-subscriptions" -H "$AUTH" -H "$AUTH_USER"
# PUT /shared-subscriptions/<id> {"purchased":true,"enabled":true,"markup_percent":0,"sort_order":0}
#   "purchased": true records the procurement and activates the plan on the owner's account — confirm first;
#   "enabled" cannot be true unless "purchased" is.
# PUT /shared-subscriptions/<id>/models {"model_name":"…","enabled":true,"markup_percent":0,"sort_order":0}
#   (also custom_input_price / custom_output_price / custom_fixed_price / custom_price_multiplier)
# PUT /shared-subscriptions/<id>/models/bulk-status — enable or disable many at once

# Official channels offered by the platform
curl -s --max-redirs 0 "$BASE/api/distributor/official-channels" -H "$AUTH" -H "$AUTH_USER"
# PUT /official-channels/<id> — GET first to learn the record shape
```

Read-only endpoints for questions like "how is the station doing": `GET /logs` (`p`, `page_size`, `type`, `start_timestamp`, `end_timestamp`, `model_name`, `username`, `token_name`), `/logs/stat`, `/earnings`, `/earnings/summary`, `/earnings/payouts`, `/topups`, `/redemptions`, `/invoices`, `/sub-distributors`, `/package-fund`.

### Station endpoints you must not call

These move money or credentials. Say so, and send the owner to `$BASE/console/distributor`:

- `POST /earnings/withdraw`, `POST /package-fund/topup`, `POST /package-fund/withdraw`, `PUT /package-fund/settings`
- `POST /redemptions` — creating redemption codes issues balance
- `PUT /customers/<userId>/password`, `PUT /customers/<userId>/commission`, `PUT /customers/<userId>/commission-application`
- `/saas-activation-token` (`GET`, `rotate`, `DELETE`), `POST /smtp/test`, `PUT /invoices/<id>`

Before any other write under `/api/distributor`, list exactly what will change — model names with effective prices, package fields, setting keys as old → new, customer ids — and get an explicit yes. A bulk 上架 or 下架 shows the complete model list first, never a count.

## More capabilities (not detailed here)

The platform also offers shared subscriptions for end users, an official-key market, invoices, 2FA/passkey management, and payment initiation. These involve credentials, purchases, or account security — do not drive them via API. When the user asks, point them to the web console (`$BASE/console`).

## Troubleshooting

- **401 Unauthorized** — key missing/wrong, or the `sk-` prefix was dropped. Re-check the config you wrote.
- **402 / quota messages** — account balance is empty; the user needs to top up (Step 4).
- **429** — rate limited; back off and retry with exponential delay.
- **Model not found** — the model name must match `GET /api/pricing` exactly; do not invent names.

## Destructive actions

Deleting tokens, changing account settings, anything under `/console` management APIs, and every write under `/api/distributor`: always confirm with the user first.
