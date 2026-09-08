---
name: stigg-subscriptions
description: Use when operating subscriptions in Stigg — provision a customer onto a plan, preview a subscription's pricing, update an active subscription (plan, add-ons, period, quantities, coupons, spend limits), cancel, run free trials and convert them to paid, support multiple subscriptions per customer (workspaces / projects), or migrate an existing subscription to the latest published plan version. Triggers include "provisionSubscription", "preview a subscription", "upgrade", "downgrade", "cancel subscription", "schedule cancellation", "trial expired", "migrate subscription to latest version".
---

# Stigg Subscriptions — Lifecycle Operations

This skill covers day-to-day subscription operations: provision, preview, update, cancel, trials, multi-subscription products, and **plan-version migration** (moving an existing sub from plan v1 to plan v2 after a publish).

## Before You Start

Per the umbrella `stigg` skill: **search first.** Provisioning options, billing-cycle behavior, and trial-conversion semantics evolve. Open the relevant SDK / REST page (Mintlify Stigg docs MCP) before authoring.

## The Operation Map

| Op | Purpose | Reference |
|---|---|---|
| **Provision** | Create a subscription for a customer on a plan (+ add-ons, trial, billing details) | `references/provisioning.md` |
| **Preview** | Calculate pricing for a hypothetical subscription before provisioning | inline below |
| **Update** | Change an active subscription's plan / add-ons / period / quantities / spend / coupons / trial | `references/updates.md` |
| **Cancel** | End a subscription immediately, at end-of-period, or on a specific date | inline below |
| **Trials** | Start a trial, convert to paid, handle expiry | `references/trials.md` |
| **Multiple active subscriptions** | One customer, many subscriptions, scoped by `resourceId` | inline below |
| **Plan-version migration** | Move an existing sub from plan v1 to plan v2 (after a publish) | `references/plan-version-migration.md` |

## Provision a Subscription

### Minimal backend call

```ts
const sub = await stigg.provisionSubscription({
  customerId: 'customer-123',
  planId: 'plan-pro',
  billingCountryCode: 'US',           // required for paid plans w/ price localization
});
```

The provisioning surface includes (see `references/provisioning.md` for the full list):

- **Resource ID** — required when the product allows multiple active subscriptions.
- **Billing period** — monthly / annual / etc., for paid plans.
- **Plan configuration** — unit quantities for in-advance commitment charges and variable entitlements; price overrides.
- **Add-ons** — list of add-ons (and quantities) compatible with the plan.
- **Subscription start date** — `Immediately` (default) / `EndOfCurrentBillingPeriod` (if an active paid sub already exists) / `SpecificDate` (past = back-dated, no immediate charge; future = activates on date).
- **Free trial** — applicable to paid / custom plans.
- **Spend management** — `minimumSpend`, `maximumSpend`.
- **Discounts** — applied coupons (catalog-wide or ad-hoc subscription-specific).
- **Payment method** — `automaticallyUsePaymentMethodOnFile` / generate-an-invoice / no-payment-via-Stigg.
- **Billing cycle anchor** — `UNCHANGED` (default) / `NOW`.
- **Proration** — `ProrateNow` / `ProrateOnNextInvoice` / `NoProration`.

**Generous-entitlement rule:** when a customer's effective entitlements come from multiple sources — active subscription, add-ons, trial, promotional entitlements, additional product subscriptions — Stigg picks the **most generous** value across all of them. The "trial vs paid" case is just one instance of this rule; it applies whenever sources overlap.

## Preview a Subscription

Before provisioning, preview the immediate and recurring invoices:

```ts
const preview = await stigg.previewSubscription({
  customerId: 'customer-123',
  planId: 'plan-pro',
  billingPeriod: 'MONTHLY',
  addons: [{ addonId: 'addon-seats', quantity: 10 }],
  couponId: 'SAVE20',                          // optional
  subscriptionId: 'sub-789',                   // optional — preview an UPDATE to an existing sub
});
```

Node SDK / GraphQL returns `immediateInvoice` and `recurringInvoice` with each amount as a `{ amount, currency }` Money object (lowercase `subtotal`). Direct REST callers see a flatter DTO with scalar amounts and the field name `subTotal` (capital T). **Amounts are in full dollars / units of the currency, not cents** — `49` means $49.00 (Stripe convention is the opposite, this catches Stripe-savvy devs). See `references/provisioning.md` for the full shape and `previewSubscription` use cases.

## Update a Subscription

> **Critical:** `updateSubscription` (the GraphQL mutation) does **not** support changing the plan. **To change a subscription's plan, call `provisionSubscription` again** — Stigg routes it through the right mechanism (in-place update or replace, depending on plan-type transition; see the migration matrix below).

```ts
// Update — addons, billing period, billable features, price overrides
await stigg.updateSubscription({
  subscriptionId: 'sub-123',
  addons: [{ addonId: 'addon-seats', quantity: 10 }],
  billingPeriod: 'ANNUAL',
});

// Change plan — re-provision (NOT updateSubscription)
await stigg.provisionSubscription({
  customerId: 'customer-123',
  planId: 'plan-pro',          // new plan
  // ...other provisioning fields
});
```

What `updateSubscription` directly supports (per the GraphQL mutation surface):

- **Billing period** (paid plans, e.g. `MONTHLY` → `ANNUAL`).
- **Add-ons** (replaces existing — pass the new full list).
- **Billable features** (in-advance commitment quantities, per-unit quantities).
- **Price overrides.**

Other update flows surfaced by the Stigg app UI (trial extension / shortening, spend-limit changes, coupon application, billing-cycle anchor reset, proration on the change) flow through **separate SDK methods or `provisionSubscription` re-calls** — search the docs for the specific operation.

> **Scheduled updates replace, don't queue:** a new update overrides any pending scheduled update and applies immediately (documented for the Stigg app UI; SDK behavior generally matches — confirm in your SDK's docs).

Detailed flow + patterns: `references/updates.md`.

## Cancel a Subscription

Via `@stigg/node-server-sdk` (which translates to the `cancelSubscription` GraphQL mutation):

```ts
await stigg.cancelSubscription({
  subscriptionId: 'sub-789',                              // Node SDK uses subscriptionId
  subscriptionCancellationTime: 'END_OF_BILLING_PERIOD',  // or 'IMMEDIATE' / 'SPECIFIC_DATE'
  // endDate: '2026-06-01T00:00:00Z',                     // required when SPECIFIC_DATE
  // subscriptionCancellationAction: 'DEFAULT',           // or 'REVOKE_ENTITLEMENTS'
  // prorate: false,
});
```

> **Field-name note:** Node SDK uses `subscriptionId`. Python / Go / Ruby / Java / .NET SDKs and the raw GraphQL mutation use `subscriptionRefId`. Direct REST takes the ID in the URL path.

`subscriptionCancellationTime`:

| Value | Behavior |
|---|---|
| `IMMEDIATE` | Cancel immediately. |
| `END_OF_BILLING_PERIOD` | Cancel at the end of the current billing period. Default for most products. **Not applicable to custom-priced plans or trial subscriptions.** |
| `SPECIFIC_DATE` | Cancel on the date specified by `endDate`. **Not applicable for trial periods.** |

`subscriptionCancellationAction`:

| Value | Behavior |
|---|---|
| `DEFAULT` | Product's default cancellation behavior (revoke access *or* downgrade to free, per product policy). |
| `REVOKE_ENTITLEMENTS` | Immediately revoke all entitlements upon cancellation. |

States after cancel: `CANCELED` (already ended) or `CANCELLATION_SCHEDULED` (pending).

> **Direct REST users** (calling `https://api.stigg.io/api/v1` via curl): the unprefixed REST field names are `cancellationTime`, `cancellationAction`, `endDate`, `prorate`. Same enum values.

## Trials

Trials apply to paid and custom plans. The plan defines the default trial; provisioning can override it.

- **Provision with trial** — pass trial config at provision time.
- **Convert trial → paid** — provision a paid subscription on top; Stigg starts the paid plan at the trial end.
- **Trial expired without conversion** — fires the `trial.expired` event; trigger win-back from your app.
- **One trial per customer per product** in self-served flows (admin overrides exist).
- **Customers who already paid** are not eligible for another self-serve free trial.

Detailed mechanics + examples (in-app upgrade, trial with add-ons): `references/trials.md`.

## Multiple Active Subscriptions Per Customer

For multi-tenant products (workspaces / projects / apps), a single customer holds many subscriptions, scoped by `resourceId`:

```ts
const sub = await stigg.provisionSubscription({
  customerId: 'customer-123',
  resourceId: 'workspace-abc',
  planId: 'plan-team',
});
```

Once enabled (it's a **product-level setting**, fixed at product creation):

- **Pass `resourceId` on every relevant call** — provision, update, entitlement check, usage report, paywall widget.
- The customer can have **separate plans on each workspace**, all paid with the same payment method.
- **Trial vs paid:** at most one active trial *and* one active non-trial subscription **per `(customer, resource)` pair**.
- Combine with single-instance products (set the other product to "single active subscription") to model "account + sub-accounts" / "platform + app instances" — e.g., Webflow's account + per-site model.

> **Once a product has any subscriptions, you cannot toggle multi-active on/off.** Decide at product creation.

## Plan-Version Migration (Catalog v1 → v2)

When a plan is republished, existing subscriptions stay on the old version unless migrated. **Routine, ongoing operation.**

> **Catalog-side publish flow** (drafts, version policy, what triggers grandfathering) lives in `stigg-pricing-modeling/references/plans.md`. This section is the *subscription-side* migration mechanics.

Two migration *mechanisms*, picked automatically by Stigg based on the plan-type transition:

| Path | Mechanism | Why |
|---|---|---|
| Free → Paid | **Provision new subscription** | Paid plans need billable metric values. |
| Free → Custom | **Provision new subscription** | Custom plans need values for variable entitlements. |
| Paid → Free | **Migrate to latest version** | In-place. |
| Paid → Custom | **Migrate to latest version** | In-place; the existing external-billing-system subscription is **not canceled** — only Stigg-side metadata is removed. |
| Custom → Paid | **Provision new subscription** | Paid plans need billable metric values. |
| Custom → Free | **Migrate to latest version** | In-place. |

**Triggering migration:**

- **UI:** open the subscription, `⋮` → **Migrate to latest** → pick **Immediately** or **At end of current period**.
- **Programmatic:** the migrate-subscription mutation / SDK method. Allows gradual rollout.

If migration is **immediate** and the customer's current price differs from the latest published price, Stigg auto-charges or credits the prorated amount.

Detailed migration reference: `references/plan-version-migration.md`.

## When NOT to Use This Skill

- Modeling features / plans / add-ons → `stigg-pricing-modeling`.
- Runtime entitlement checks / usage reporting → `stigg-entitlements`.
- Strategic advice on pricing models → `stigg-pricing-expert`.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Forgetting `resourceId` on multi-active products | Every call (provision / update / entitlement / usage / widget) needs it. |
| Treating scheduled updates as a queue | A new update **replaces** scheduled ones. If you need a queue, model it in your app. |
| Cancelling immediately when the product policy says end-of-period | Use the product's default; opt-in to immediate only when you mean it. |
| Trying to cancel a custom-priced plan at end of period | Not supported by the cancellation modal. Use a specific date or coordinate with billing. |
| Self-serve trial for a customer who's already paid | Not eligible. Admin override needed. Surface the right CTA in your app. |
| Skipping `previewSubscription` before charging | Customers expect to see what they'll pay. Preview first, then provision. |
| Not setting `billingCycleAnchor: NOW` on a major upgrade | The customer's bill cycle drifts. Reset explicitly when the change should start a fresh period. |
