---
name: link-cli
description: Stripe Link agent wallet CLI. Use when the user wants an agent to make
  payments on their behalf, create one-time-use virtual cards, spend via Machine
  Payments Protocol (MPP), or manage their Link wallet. Triggers on mentions of
  "buy with Link", "agent payment", "Link wallet", "spend request", or "link-cli".
---

# link-cli — Stripe Link Agent Wallet

Let AI agents get secure, one-time-use payment credentials from a Link wallet — so they can complete purchases on your behalf without ever storing your real card details. Uses the OAuth 2.0 device authorization grant (RFC 8628): no browser, no localhost callback, no API token.

> Repo: https://github.com/stripe/link-cli
> Install: runs via `npx -y @stripe/link-cli` (no pre-install needed)

## Auth Flow

link-cli uses device authorization. The pattern for every auth-dependent command:

1. Run the command — if unauthenticated, it returns a `verification_url` + `phrase`
2. Present the URL to the user and ask them to approve in the Link app
3. Poll until authenticated — do not wait for the user to reply before polling

Credentials are stored at `~/.config/link-cli-nodejs/config.json`.

### 1. Log In

```bash
npx -y @stripe/link-cli auth login --format json
```

Returns `verification_url`, `phrase`, and `_next.command`. The user visits the URL and enters the phrase in their Link app.

### 2. Poll Until Authenticated

Use the `_next.command` from the login response, or:

```bash
npx -y @stripe/link-cli auth status --interval 5 --max-attempts 60 --format json
```

Exits when `authenticated` is `true`. The `--interval` / `--max-attempts` flags control polling behavior.

### 3. Check Auth Status

```bash
npx -y @stripe/link-cli auth status --format json
```

Returns `authenticated` (bool), `credentials_path`, and if pending, the current `verification_url` + `phrase`.

### 4. Log Out

```bash
npx -y @stripe/link-cli auth logout --format json
```

---

## Payment Methods

### 5. List Payment Methods

```bash
npx -y @stripe/link-cli payment-methods list --format json
```

Returns saved payment methods with `id`, `type` (CARD), `name`, `is_default`, and `card_details` (brand, last4, exp_month, exp_year).

---

## Spend Requests

The core flow: create a spend request → user approves in Link app → agent receives one-time credentials.

### 6. Create a Spend Request

```bash
npx -y @stripe/link-cli spend-request create \
  --payment-method-id "<payment-method-id>" \
  --merchant-name "Gumroad" \
  --merchant-url "https://example.com/checkout" \
  --amount 100 \
  --currency usd \
  --context "Buying HTTPZine from Gumroad — a free comic about HTTP. Patrick Collison demoed this at Stripe Sessions 2026. This is a test of the Link CLI agent payment flow." \
  --format json
```

**Required for virtual card flow** (`--credential-type card`, the default):
- `--payment-method-id` — from `payment-methods list`
- `--merchant-name` — human-readable merchant name
- `--merchant-url` — the merchant's website
- `--amount` — in cents, max 50000 ($500.00)
- `--currency` — 3-letter ISO code (default: `usd`)
- `--context` — **min 100 characters** describing the purchase and rationale

**Optional:**
- `--credential-type shared_payment_token` — for MPP/HTTP 402 flows (omits `--merchant-name`/`--merchant-url`)
- `--test` — use test mode (generates test card `4242 4242 4242 4242`)
- `--line-item name:<name>,unit_amount:<cents>,quantity:<n>` — repeatable
- `--total type:<type>,display_text:<text>,amount:<cents>` — repeatable

Returns an `approval_url` and `_next.command` for polling.

### 7. Poll for Approval

```bash
npx -y @stripe/link-cli spend-request retrieve <spend-request-id> \
  --interval 2 --max-attempts 150 --format json
```

Exits when status is `approved`, `denied`, or `expired`. On timeout while `pending`, exits non-zero with `POLLING_TIMEOUT`.

### 8. Reveal Card Details

```bash
npx -y @stripe/link-cli spend-request retrieve <spend-request-id> \
  --include card --format json
```

When approved, the response includes a `card` object with `number`, `cvc`, `brand`, `exp_month`, `exp_year`, `billing_address`, and `valid_until`. The card is **one-time-use** and expires after `valid_until`.

### 9. Update a Spend Request

```bash
npx -y @stripe/link-cli spend-request update <spend-request-id> \
  --merchant-url "https://example.com/new-url" --format json
```

### 10. Request Approval (Separately)

If `--request-approval` was omitted during `create`:

```bash
npx -y @stripe/link-cli spend-request request-approval <spend-request-id> --format json
```

---

## Machine Payments Protocol (MPP)

For merchants that support MPP/HTTP 402, skip the checkout form entirely.

### 11. Decode an MPP Challenge

```bash
npx -y @stripe/link-cli mpp decode \
  --challenge '<WWW-Authenticate header value>' --format json
```

Extracts the `network_id` needed for SPT spend requests.

### 12. Pay via MPP

```bash
npx -y @stripe/link-cli mpp pay "https://api.example.com/resource" \
  --spend-request-id "<approved-spend-request-id>" \
  --method GET --format json
```

The spend request must be approved and have `credential_type: shared_payment_token`. The token is single-use — if payment fails, create a fresh spend request.

Options: `--method` (GET/POST/PUT/DELETE/PATCH), `--data '<json>'`, `--header "Key: value"` (repeatable).

---

## Guided Setup

### 13. Interactive Onboarding

```bash
npx -y @stripe/link-cli onboard
```

Walks through auth, payment methods check, app download QR, and demo flows. **Requires a TTY** — not suitable for headless/agent-driven use.

### 14. Run Demo (TTY required)

```bash
npx -y @stripe/link-cli demo --only-card --format json
```

Test mode only. Use `--only-card` or `--only-spt` to run a single flow.

---

## MCP Server Mode

```bash
npx -y @stripe/link-cli --mcp
```

Runs link-cli as a local MCP server for MCP-compatible clients.

---

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `NO_UPDATE_NOTIFIER=1` | Suppress version update checks (use in CI/automation) |
| `LINK_API_BASE_URL` | Override API base URL |
| `LINK_AUTH_BASE_URL` | Override auth base URL |

---

## Guidelines

1. **Always use `--format json`** — the default `toon` format is for human TTY consumption. JSON is machine-parseable.
2. **Never wait for the user between login and polling** — call `auth login`, present the URL, and immediately start polling `auth status`. Same for spend requests: create, present `approval_url`, poll immediately.
3. **Test mode for demos** — use `--test` on `spend-request create` to avoid real charges during testing.
4. **Context is required and must be ≥100 chars** — the user reads this when approving. Describe the purchase and rationale clearly.
5. **Virtual cards are one-time-use** and have a short validity window (typically ~1 hour). Use them immediately after approval.
6. **Credentials persist across sessions** at `~/.config/link-cli-nodejs/config.json`. Check `auth status` before assuming the user is logged in.
7. **Check `_next` in responses** — many commands return a `_next.command` field with the exact polling command to use.
8. **Amounts are in cents** — `100` = $1.00, `50000` = $500.00 (max).
9. **`demo` and `onboard` require TTY** — they won't work in headless sandbox environments.
10. **No API token or connector needed** — link-cli manages its own OAuth device flow and stores credentials locally.
