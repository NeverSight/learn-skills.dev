---
name: stigg-pricing-modeling
description: IMPLEMENTATION skill — use when the user is **building** a Stigg product catalog (model is already chosen). Covers features (boolean / metered / configuration), plans (free / paid / custom), add-ons, products, charges (flat / per-unit / pay-as-you-go / in-advance commitment / minimum spend / credits), overages, coupons, custom credit currencies, price localization. Triggers include "create a plan", "add an add-on", "define a feature", "model my pricing in Stigg", "set up usage-based pricing", "configure overages", "publish a plan", "publish a draft", "edit a published plan", "add a charge", "create a coupon", "set up price localization", or any Stigg catalog mutation. MCP-first — catalog work runs through the Stigg MCP, not by hand-writing REST. Skip when the user is still **picking** the model — that's stigg-pricing-expert. Skip for runtime entitlement checks (stigg-entitlements) and subscription lifecycle (stigg-subscriptions).
---

# Stigg Pricing Modeling — Build the Catalog

This skill covers the full catalog surface: products, plans, add-ons, features, charges, coupons, and credit-currency definitions. It does **not** cover runtime gating (`stigg-entitlements`) or subscription lifecycle (`stigg-subscriptions`).

## Before You Start

Per the umbrella `stigg` skill: **search first.** Catalog modeling moves fast — use the Mintlify Stigg docs MCP (`search_stigg`, `query_docs_filesystem_stigg`) or the Stigg MCP server's `search_docs` tool to read the current page before authoring config.

## MCP-First Rule of Thumb

> **Aim to do every catalog operation through the Stigg MCP. No UI required, where the MCP supports it.**

Why: the Stigg MCP exposes the full Stigg API surface for catalog modeling. The agent translates "create a Pro plan with two metered features and a $49 base charge" into the right MCP tool calls — no clicking, no copy-pasting from the UI.

Where MCP coverage is incomplete today, fall through in this order:

1. **Stigg MCP** (`mcp.stigg.io`) — preferred. See `stigg-mcp`.
2. **Stigg CLI** (`brew install stiggio/tools/stigg` — https://github.com/stiggio/stigg-cli) — only when the user explicitly asks for the CLI or a deterministic script / CI step.
3. **REST API** — for ops the SDK doesn't surface yet.
4. **Stigg UI** (`app.stigg.io`) — last resort, only for ops not yet covered above. **Name the operation explicitly** in the skill's MCP-coverage matrix and link to the UI page.

The **canonical, live coverage table** lives at `references/mcp-coverage-matrix.md`. Update that file as MCP coverage expands; **do not** silently let the skill drift to "use the UI" instructions.

## The Catalog at a Glance

| Concept | What it is | Reference |
|---|---|---|
| **Product** | Top-level product line. Anchors plans, add-ons, customer journey. Controls single vs multiple subs per customer. | `references/products.md` |
| **Plan** | A tier on a product. Three types: **Free**, **Paid**, **Custom**. | `references/plans.md` |
| **Add-on** | Modular extension of a paid/custom plan. Entitlements are additive. | `references/addons.md` |
| **Feature** | Capability you can gate. Types: **boolean**, **configuration** (numeric / enum), **metered**. | `references/features.md` |
| **Entitlement** | Feature + configuration on a plan or add-on. *("10,000 API calls / month".)* | covered in plans/addons |
| **Charge** | What's billed: base flat fee, per-unit, pay-as-you-go, in-advance commitment, minimum spend, overages, credits charge. | `references/charges-and-pricing-models.md` |
| **Coupon** | Discount instrument applied to customers or specific subscriptions. | `references/coupons.md` |
| **Credits modeling** | Catalog-side credits — credit grants on plans / add-ons, consumption mappings. | `references/credits-modeling.md` (definition + runtime ops live in `stigg-credits`) |
| **Price localization** | Multi-currency / multi-region billing. Distinct from custom credit currencies. | `references/price-localization.md` |

## Pick the Right Plan Type

| Goal | Plan type |
|---|---|
| Freemium tier, no payment info, drives upgrades | **Free** |
| Self-serve paid offering (fixed and/or usage-based, optional trial) | **Paid** |
| Sales-led, per-customer pricing, variable entitlements | **Custom** |

A product can have all three. A customer typically has one active subscription per product (configurable; some products allow multiple active subscriptions in parallel — see `references/products.md`).

## Pick the Right Charge Model

| Goal | Use |
|---|---|
| Predictable monthly fee | **Flat fee** (e.g. $49/month) |
| Pay per resource selected | **Per-unit** (e.g. $10/seat/month) |
| Bill purely by consumption | **Usage-based — pay-as-you-go** |
| Customer commits to a quota in advance, true-up after | **In-advance commitment** |
| Floor on revenue regardless of usage | **Minimum spend** |
| Quota included; charge above quota | **Overages** (volume / graduated / per-unit volume) |
| Credit-based monetization | **Credits charge** |
| Multi-region pricing | **Price localization** (separate axis — applies on top of the model) |

Detailed mechanics, when to combine, and trade-offs: `references/charges-and-pricing-models.md`. Strategic guidance on *which* model to pick lives in the `stigg-pricing-expert` skill — this skill is for *executing* a chosen model.

## Features — The Three Types

| Type | When | Entitlement is… |
|---|---|---|
| **Boolean** | On/off capability ("Premium support") | granted or denied |
| **Configuration** | Numeric or enum value ("Number of seats", "Available templates") | a value |
| **Metered** | Tracked consumption ("API calls / month") | a value with optional usage reset (hourly / daily / weekly / monthly) and a meter aggregation (sum / count / count-unique / average / min / max) |

> Connect features to plans/add-ons via **entitlements**. The same feature can have different entitlements on different plans (e.g. "API calls" = 1k on Starter, 10k on Pro, unlimited on Enterprise).

## Custom Credit Currencies vs Price Localization

These are easy to confuse — they are **different concepts**.

- **Custom credit currency** — you define a unit of consumption (e.g. "AI tokens", "API credits"). Customers' usage of metered features deducts from a credit pool denominated in that currency. **Has nothing to do with billing currency.** See `references/credits-modeling.md` and the `stigg-credits` skill.
- **Price localization** — multi-currency *billing* (e.g. show / charge prices in EUR for EU customers, JPY for JP customers). Independent axis on top of any pricing model. See `references/price-localization.md`.

Most commonly: a single product uses **one** custom credit currency for credit-based pricing, but offers **multiple** localized billing currencies on its paid plans.

## Drafts, Versions, and Publishing

Plan and add-on edits use a **draft → published-version** flow:

- Open a draft, edit, **publish** to make it the new active version.
- Existing subscriptions on older versions stay grandfathered until you migrate them (covered in `stigg-subscriptions/references/plan-version-migration.md`).
- When publishing, choose the migration policy (e.g. `NEW_CUSTOMERS` only, vs forced migration) per the publish-plan endpoint.
- For add-ons there's a parallel draft / publish flow — same shape.

> Always re-fetch the current draft/publish docs page before authoring rollout logic. The available migration types and side-effects evolve.

## Catalog Modeling Workflow

A typical end-to-end (over the MCP):

```text
1. Define features.            ← reusable building blocks
2. Group features (optional).  ← for shared entitlements across plans
3. Create the product.         ← anchors plans & add-ons
4. Create plans.               ← assign feature entitlements + charges
5. Create add-ons.             ← additive entitlements + their own charges
6. (Optional) Define coupons.
7. (Optional) Configure price localization.
8. Publish.                    ← chooses migration policy for existing subs
```

For each step, **search the docs first**, then call the MCP. The order matters because plans and add-ons reference features, and add-ons reference plans for compatibility.

## When NOT to Use This Skill

- Runtime entitlement checks (`getMeteredEntitlement`, `getBooleanEntitlement`, `getEntitlement`, and the `entitlement.hasAccess` property they return) → use `stigg-entitlements`.
- Provisioning, updating, or canceling a subscription → use `stigg-subscriptions`.
- Picking *which* monetization model fits the customer's product → `stigg-pricing-expert`.
- Operating credit grants, ledger, auto-recharge in production → `stigg-credits`. (This skill covers the *modeling* of credit currencies and credit charges in the catalog.)

## Common Mistakes

| Mistake | Fix |
|---|---|
| Editing a published plan directly without a draft | Always draft → edit → publish; pick the migration type for existing subs at publish time. |
| Forgetting compatibility rules between an add-on and its plan | Add-ons declare compatibility per plan; ensure the add-on is listed in the plan's compatible add-ons. |
| Treating "custom credit currency" as a billing currency | Custom credit currency = consumption unit (tokens, credits). Billing currency = USD/EUR/etc. — see price localization. |
| Modeling per-seat as a metered feature | Use a **configuration** feature with a per-unit charge. Metered is for consumption tracked over time. |
| Setting a usage reset cadence that doesn't match the billing period | Cadences should align with how customers see the bill — typically monthly resets for monthly billing periods. |
| Adding plan-level entitlements for things that should be add-on entitlements | If it's optional / extra-billable, model it as an add-on so it's additive and separately priced. |
| Using the UI for an op that the MCP supports | Default to the MCP. Update `references/mcp-coverage-matrix.md` if you find missing coverage; the goal is to drive UI fallbacks to zero. |
