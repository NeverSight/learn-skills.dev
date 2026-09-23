---
name: stripe
description: >-
  Read Stripe account state from a terminal or agent: balance, payment
  intents, and subscriptions — and perform guarded mutations like canceling a
  subscription — backed by a bundled stripe-cli script that is read-only first
  and gates every state-changing command behind a --dry-run/--yes
  confirmation. Use when an agent needs to answer questions about account
  balance, recent payments, active subscriptions, or apply a confirmed
  subscription cancellation. Do not use for building Stripe payments into an
  application (that is Stripe integration development), managing Stripe
  dashboard settings, or other payment processors (that is their own tooling).
license: MIT
compatibility: >-
  The bundled stripe-cli script runs on Python 3.9+ with only the standard
  library. --help and the read-only surface (balance, payments,
  subscriptions) need no network beyond api.stripe.com; live reads require a
  Stripe secret or restricted API key with read access and network access to
  api.stripe.com.
metadata:
  source: https://docs.stripe.com/api
  source_index: references/00-source-index.md
  research_checked: "2026-08-03"
---

# Stripe Operations

Use this skill to read Stripe account state and, with explicit confirmation, perform guarded mutations: account balance, payment intents, subscriptions, and subscription cancellation. This is a **tool skill** for the Stripe platform. Building Stripe payments into an application is integration development; this skill owns the everyday agent workflow: answering "what is our balance?", "which payments succeeded?", "what subscriptions are active?", and applying a confirmed cancellation.

## Operating contract

1. **Read-only first.** Balance, payment, and subscription queries run freely and never change anything. The bundled `stripe-cli` script's primary surface is these reads.
2. **Guard every mutation.** State-changing operations — canceling a subscription — require an explicit human directive plus `--dry-run` preview and `--yes` confirmation through `stripe-cli`. Cancellations are financial actions with billing consequences: confirm the subscription, the timing, and the impact before acting.
3. **Respect bounded reads.** Stripe paginates with `limit` and `has_more`; never page past what the task needs. `stripe-cli --limit` caps every listing.
4. **Keep evidence bounded.** Quote short IDs, amounts, and statuses; never dump full API keys, customer data, or raw payloads into chat.
5. **Treat money data as sensitive.** Balances, payments, and subscription details are financial records; quote only what the question needs and never expose full card or customer data.

## The stripe-cli script

`scripts/stripe-cli` is an agent-first, stdlib-only CLI over the Stripe API. It is **read-only-first**: balance, payments, and subscriptions are the primary surface; the only mutation is guarded.

```bash
stripe/scripts/stripe-cli --help                          # no key or network needed
stripe/scripts/stripe-cli --json balance show
stripe/scripts/stripe-cli --json --limit 20 payments list
stripe/scripts/stripe-cli --json --limit 20 subscriptions list
stripe/scripts/stripe-cli --json subscriptions get --id sub_123
stripe/scripts/stripe-cli subscriptions cancel --id sub_123 --dry-run   # preview
stripe/scripts/stripe-cli subscriptions cancel --id sub_123 --yes       # confirmed
```

Exit codes: 0 success, 1 API error or failed check, 2 usage error. Cancellations are guarded: without `--dry-run` or `--yes` the script refuses with exit 1 and never calls the API. Reads are bounded by `--limit` (default 20, max 100).

## Operating loop

1. **Scope the question**: is this a read (balance, payments, subscriptions) or a mutation (cancel)? Locate the object with the read surface first.
2. **Read with bounds**: `balance show` for available and pending funds; `payments list` for recent payment intents; `subscriptions list`/`subscriptions get` for active subscriptions and their items.
3. **Triage the answer**: map the question to evidence (amounts, statuses, customers, period end dates).
4. **Act with confirmation**: only a human directive to change, previewed with `--dry-run` and confirmed with `--yes`.
5. **Verify**: re-read the subscription and confirm `cancel_at_period_end` is set (cancellation at period end) — and state that the customer keeps service until that date.

## Read surface: balance, payments, subscriptions

- **Balance** (`GET /balance`): available and pending balances per currency. A read-only snapshot of account funds.
- **Payments** (`GET /payment_intents`): recent payment intents with amount, currency, status (`succeeded`, `requires_action`, etc.), and customer. Bounded by `--limit`; `has_more` tells you whether the cap hid further records.
- **Subscriptions** (`GET /subscriptions`, `GET /subscriptions/{id}`): active subscriptions with status, customer, period end, and items (price, amount, interval). A read before any cancellation.

## Guarded mutation: subscription cancellation

- `subscriptions cancel --id sub_... --dry-run` previews the cancellation; `--yes` confirms and posts `cancel_at_period_end=true` — the safe default that **schedules cancellation at the period end** (customer keeps service until then) rather than canceling immediately.
- The script verifies Stripe confirmed the change (response `cancel_at_period_end: true`) before reporting success; a mismatch raises an error and no state change is assumed.
- Cancellation scheduled at period end is reversible by setting `cancel_at_period_end=false` before the period ends. Immediate cancellation and refunds are deliberately NOT in this skill's mutation surface — they need a human at the Stripe dashboard or a dedicated integration.

## Access model and credentials

- Stripe authenticates with secret keys (`sk_...`) or restricted keys (`rk_...`). Use a **restricted key scoped to read-only** (`balance:read`, `payment_intents:read`, `subscriptions:read`) for the read surface; add `subscriptions:write` only where cancellations are genuinely needed.
- Keys are live or test (`sk_live_`/`sk_test_`). Never point live keys at test data or vice versa; verify the key type before running anything that could touch real charges.
- Store keys in `STRIPE_API_KEY`, never in code, chat, or commits. Rotate a leaked key immediately in the Stripe dashboard.

## Reference routing

| Load when | Reference |
|---|---|
| Sources, refresh procedure | `references/00-source-index.md` |
| Endpoints, pagination, cancellation semantics, errors | `references/01-stripe-read-operations.md` |

## Included artifacts

- `scripts/stripe-cli`: bounded, stdlib-only CLI (balance, payments list, subscriptions list/get, guarded cancel; `--json`; `--limit`; mutation gated by `--dry-run`/`--yes`).
- `tests/test_stripe_cli.py`: 12 deterministic tests against a stub Stripe API, including the read-only-first contract and the mutation gate.
- `references/`: dated source index + Stripe read-operations reference.
- `evals/evals.json`: six output-quality evaluation cases for agent runs.

## Verification boundary

| Claim | Minimum evidence |
|---|---|
| Balance is current | `stripe-cli balance show --json` returns available and pending per currency |
| A payment succeeded | `stripe-cli payments list --json` shows the intent with status `succeeded` |
| A subscription is active | `stripe-cli subscriptions get --json` returns status `active` and period end |
| A cancellation was accepted | `stripe-cli subscriptions cancel --yes` exits 0 and the response has `cancel_at_period_end: true` |
| A mutation is safe to run | `stripe-cli subscriptions cancel --dry-run` prints the exact subscription ID |

## Hard boundaries

- Never cancel a subscription without a human directive, `--dry-run` preview, and `--yes` confirmation — cancellations have billing consequences.
- The mutation surface is limited to scheduling cancellation at period end. Refunds, immediate cancellations, and charge operations are out of scope.
- Never page reads past `--limit`; never dump full API keys, customer data, or raw payloads into chat.
- This skill operates the Stripe API. It does not build payments into applications or cover other payment processors.

## When not to use

- **Building Stripe payments into an application** (Checkout, Payment Intents in code, webhooks for your app, billing logic) — that is integration development; see [backend-engineering](../backend-engineering/SKILL.md).
- **Stripe dashboard administration** (account settings, bank accounts, disputes, tax registration) — that is the Stripe Dashboard.
- **Refunds, immediate cancellations, or charge operations** — deliberately out of this skill's guarded-mutation surface; those are human decisions in the dashboard or a dedicated integration.
- **Other payment processors** (Braintree, Adyen, PayPal) — each has its own API and tooling; this skill covers Stripe.
