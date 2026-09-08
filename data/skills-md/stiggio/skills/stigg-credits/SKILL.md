---
name: stigg-credits
description: Use for any credits work in Stigg — defining a credit currency (also called "credit type"), the full lifecycle (create / update / archive / list / inspect associations), granting recurring / prepaid / promotional credits, configuring consumption mappings or custom formulas per plan, auto-recharge, ledger inspection, overdraft, billing integration for paid credits, or driving credit-based monetization end-to-end. Triggers include "monetize with credits", "AI tokens", "API credits", "compute units", "credit grants", "credit pool", "credit balance low", "auto-recharge", "credit ledger", "consumption mapping", "custom credit formula", "seat-based credits", "OpenAI-style pricing", "create credit currency", "credit type", "tokens consumed", "deduct credits", "prepaid credits". Skip for static catalog modeling of non-credit features (stigg-pricing-modeling), runtime gating of non-credit features (stigg-entitlements), or subscription lifecycle (stigg-subscriptions).
---

# Stigg Credits — Credit-Based Monetization

This skill is the canonical home for credits end-to-end: credit currency definition, granting credits (recurring / prepaid / promotional / manual / overdraft), runtime consumption (mappings, custom formulas, ledger), auto-recharge, seat-based pools, billing integration, and revenue recognition. The static *catalog* shape (recurring credit grants attached to plans / add-ons as entitlements) is in `stigg-pricing-modeling/references/credits-modeling.md`; everything else lives here.

## Before You Start

Per the umbrella `stigg` skill: **search first.** The credits surface evolves quickly (custom formulas, overdraft mechanics, seat-based pools are recent additions). Use the Mintlify Stigg docs MCP (`search_stigg`, `query_docs_filesystem_stigg`) to confirm specifics before authoring.

## Mental Model — Five Pieces

```text
                              ┌──────────────────────────────────┐
                              │   Credit currency (the unit)     │
                              │   "AI tokens", "API credits",    │
                              │   "compute units"                │
                              └────────────────┬─────────────────┘
                                               │ denominates
                                               ▼
   Grants funded by:        ┌──────────────────────────────────┐
   • Recurring (plan/addon)  │   Credit pool (per customer,    │
   • Prepaid (purchase)      │   per credit currency)          │
   • Promotional (zero cost) │   = balance + many grants       │
   • Manual                  └────────────────┬─────────────────┘
   • Overdraft (system)                       │ deducted by
                                              ▼
                              ┌──────────────────────────────────┐
                              │   Consumption mapping or         │
                              │   custom formula  (per plan)     │
                              │   metered feature → credits      │
                              └────────────────┬─────────────────┘
                                               │ records
                                               ▼
                              ┌──────────────────────────────────┐
                              │   Credit ledger (append-only)    │
                              │   grants, burns, expirations,    │
                              │   revocations, adjustments       │
                              └──────────────────────────────────┘
```

`references/grants.md`, `references/consumption.md`, `references/ledger.md`, `references/auto-recharge.md`, `references/seat-pools.md`, `references/custom-formulas.md`, `references/billing-integration.md`, `references/revenue-recognition.md`.

## Credit Currency

A **credit currency** (called a "credit type" in the Stigg app's catalog UI) is your unit of consumption — `tokens`, `credits`, `compute units`. Customers' usage of metered features deducts from a pool denominated in that currency.

- **The full currency lifecycle — define, update, archive, unarchive, list, and inspect associated plans/add-ons — is available via the Stigg MCP** (preferred for AI-assisted dev) **or the Stigg app under Product Catalog → Credits**. An end-to-end credits-consumption workflow (currency → metered feature → per-plan consumption mapping → grants → usage reporting) can run entirely through the MCP. Refresh the live MCP tool listing or the docs before authoring — operation names and field shapes are owned by the live surface, not this skill.
- **Singular / plural display names** like "token" / "tokens", immutable ID. **Inspect dependencies before archiving** — Stigg blocks archive while the currency is referenced by active plans or add-ons.
- **Non-interchangeable** across currencies — usage against one currency cannot consume another.
- **Not a billing currency.** Custom credit currency is a consumption unit; for multi-currency *billing* (USD/EUR/JPY), see `stigg-pricing-modeling/references/price-localization.md`.
- The catalog-side modeling shape (recurring grants attached to plans / add-ons as entitlements) is in `stigg-pricing-modeling/references/credits-modeling.md`.

## Credit Pool

One pool per `(customer, credit currency)` (and per `resourceId` for multi-active products). The pool holds many **credit blocks** (also called "grants" or "allocations"), each with `amount`, lifecycle dates (`effective_at` / `expires_at`), `category` (paid / promotional), `cost_basis` ($ per credit, used for revenue rec), `priority` (lower = higher), and `status`. Full field reference: `references/grants.md`.

## Five Grant Types

| Type | Origin | Cost basis | Usual cadence |
|---|---|---|---|
| **Recurring** | Plan / add-on entitlement | Paid (the price of the plan) | Per billing cycle (monthly / annual / etc.) |
| **Prepaid** | Customer purchases up front | Paid | One-time pack |
| **Promotional** | Granted manually for adoption / incentive | **Zero** (never affects revenue) | One-time, usually time-bound |
| **Manual adjustment** | Admin-added or admin-removed | Paid or zero (admin choice) | Ad-hoc |
| **Overdraft** | System-generated; tracks negative balance | n/a | Auto-created, auto-settled |

Modeling shape (recurring credits attached to a plan or add-on as an entitlement) is covered in `stigg-pricing-modeling/references/credits-modeling.md`. **Granting** credits at runtime (prepaid / promotional / manual) lives here in `references/grants.md`.

## Consumption — Configured on the Plan

How a metered feature converts to credits is configured **on the plan** (and on each add-on) — not on the feature or the credit currency. Each plan picks a flat conversion rate (`1 token = 1 credit`) or a custom formula on dimensions (`credits = 2.5 × input + 10 × output`). Same feature, different rules per plan, is fully supported.

Path: **Product catalog → Plans → select plan → Edit price → Set price → Credit consumption** (per metered feature on the plan).

## Burn order — when multiple grants are eligible

Once an event consumes N credits, Stigg picks which grant(s) to deduct in this order:

1. **Priority** — lower number = higher priority.
2. **Expiration date** — sooner-expiring grants burn first.
3. **Category** — promotional before paid (when other attributes match).
4. **Effective date** — earlier-effective first.
5. **Created date** — older first if all else ties.

If a single event needs more credits than the highest-ranked grant has, Stigg consumes from the next, then the next, with **a separate ledger entry per grant consumed**. Worked example in `references/consumption.md`.

## Overdraft — Negative Balance

Stigg supports negative credit balances. When a usage event needs more credits than the customer has, an **overdraft grant** is auto-created to track the deficit. **Always enabled — there is no off switch.** Overdraft grants:

- `grant_type: OVERDRAFT`, `amount: 0`, `consumed_amount` = the deficit.
- One overdraft per `(customer, currency)` (and per resource, if resource-scoped).
- Cannot be edited or voided manually.
- Auto-settled when new credits arrive — full or partial.

Detailed behavior + worked example: `references/consumption.md`.

## Custom Consumption Formulas

For variable-cost workloads (multi-model LLM ops, multi-input processing, weighted token costs), define a **custom formula** instead of a fixed conversion rate:

```text
credits_used = (a × documents) + (b × emails) + (c × images)
credits_used = (1.1 × model1_tokens) + (1.5 × model2_tokens) + (5 × model3_tokens)
```

Configured per metered feature, in **Product Catalog → Plans → Edit price → Set price → Credit consumption → Calculation mode: Advanced formula**. Full mechanics: `references/custom-formulas.md`.

## Auto-Recharge

Keep a customer's prepaid balance from depleting by auto-purchasing credits when the balance drops below a threshold:

| Setting | What it does |
|---|---|
| **When credit balance goes below** | Trigger threshold. |
| **Then bring credit balance back up to** | Target balance after recharge. |
| **Limit total monthly spend to** | Hard cap on auto-recharge spend per period. |
| **Spend limit resets every** | Cadence for the cap. |
| **Grant expiration** | How long auto-purchased credits stay valid. |
| **Payment method** | Card / etc. used for auto-recharges. |

Webhook events to handle:

- `automatic_recharge.operation.attempted` — every attempt (success and failure).
- `credits.automatic_recharge_limit_exceeded` — fired at 80%, 90%, 100% of the spend limit.
- `automatic_recharge.configuration.changed` — enabled / disabled, including system-driven (e.g. payment failure).

Setup walkthrough: `references/auto-recharge.md`.

## Seat-Based Credit Pools

Link a recurring credit grant to a metered seat feature so credits scale with team size:

> "1,000 AI credits per seat per month" → 5 seats = 5,000 credits/month → adding a 6th seat auto-provisions another 1,000.

Credits go into a **shared pool** (not siloed per user) — the org draws from one balance. **Requires Stripe integration.** Available on plans/add-ons that include both a credit entitlement and a metered seat feature. Configuration in `references/seat-pools.md`.

## Billing Integration

Stigg sits **alongside** your billing stack — no rip-and-replace. Your billing provider (Stripe / Zuora / custom) handles payments, taxes, invoices, payment methods. Stigg handles credit pools, grants, consumption, and enforcement.

When money moves:

| Event | Stigg's reaction |
|---|---|
| Customer pays | Stigg creates a **paid grant** with amount + cost_basis + dates, updates the pool, writes to the ledger. |
| Promo issued | Stigg creates a grant with **zero cost_basis** (no revenue impact). |
| Refund / revocation | You revoke the corresponding grant in Stigg to keep deferred / recognized aligned. |

System boundaries (who owns what):

- **Your billing system:** product catalog and prices, taxes, invoicing, payments, refunds, collections.
- **Stigg:** credit currencies (the catalog UI calls them "credit types"), pools, grants, real-time consumption, ledger, customer widgets.

Common flows (self-serve top-up, sales-led invoice, automatic top-up): `references/billing-integration.md`.

## Revenue Recognition

Stigg gives Finance an auditable trail. Per grant: `amount_granted`, `amount_remaining`, `amount_consumed`, `expires_at`, `category`, `cost_basis` (per-unit). The append-only ledger captures every burn / expiry / revocation.

```text
Deferred revenue   = amount_remaining × cost_basis      (paid grants only)
Recognized revenue = consumed_in_period × cost_basis
Breakage           = expired_in_period × cost_basis     (per your policy)
```

Promotional grants have **zero cost basis** → never affect revenue. Full journal-entry model + reconciliation pattern: `references/revenue-recognition.md`.

## Credits Webhooks

Credit-specific events (`credit.balance.low` / `.depleted`, `credit.grant.*`, `automatic_recharge.*`) drive in-app notifications, win-back campaigns, and payment-failure flows. **For payload shape, signature verification, retry semantics, and a handler skeleton, see `stigg-webhooks`.**

## When NOT to Use This Skill

- Modeling non-credit features / plans / add-ons → `stigg-pricing-modeling`.
- Runtime entitlement checks for boolean / configuration features (no credits involved) → `stigg-entitlements`.
- Provisioning / canceling subscriptions → `stigg-subscriptions`.
- Deciding whether credits are the right pricing model in the first place → `stigg-pricing-expert`.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Trying to disable overdraft | Not configurable. The system always tracks deficit rather than rejecting events. Plan around this. |
| Setting promotional cost_basis to nonzero | Pollutes revenue rec. Promotional must be zero. |
| Granting credits before subscription is provisioned | Allowed (pool persists), but most teams want credits to follow plan lifecycle — check expectations. |
| Picking priority numbers ad-hoc per grant | Lower number = higher priority. Document a convention (e.g. promo=1, recurring=10, prepaid=20) and stick to it. |
| Forgetting to add consumption mappings on plans | The mapping is **on the plan**, not on the feature. Adding a metered feature to the catalog doesn't make existing plans consume it for credits — each plan needs its own mapping. |
| Configuring the formula on the feature instead of the plan | The feature defines what's measured; the **plan** decides how that measurement converts into credits. Different plans can use different rates / formulas for the same feature. |
| Modeling per-token-model price as separate features | Use a custom formula instead — `credits_used = w1 * tok1 + w2 * tok2`. |
| Auto-recharge configured with a payment method that fails | Stigg fires `automatic_recharge.configuration.changed` and disables auto-recharge. Surface this in your app immediately. |
| Building credit-balance UI from scratch | Stigg ships ready widgets (Credits Balance, Utilization, Usage Chart, Grants Table, Auto-Recharge Status, Auto-Recharge Configuration) — see `stigg-widgets`. |
| Exporting credit data to BI without `cost_basis` | You can't compute revenue without it. Always include `cost_basis` and the grant ID in exports. |
| Treating the ledger as eventually consistent | It's append-only and authoritative. Read from the ledger for finance reconciliation; don't reconstruct from individual events. |
