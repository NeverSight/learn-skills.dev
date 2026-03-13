---
name: paystack-plans
description: >-
  Paystack Plans API — create, list, fetch, and update subscription plans with intervals
  (daily, weekly, monthly, quarterly, biannually, annually). Use this skill whenever
  creating pricing tiers or recurring billing plans on Paystack, setting up subscription
  intervals, configuring invoice limits, managing plan currencies, or building a SaaS
  pricing page. Also use when you see references to plan_code, PLN_ prefixed codes,
  or the /plan endpoint.
---

# Paystack Plans

The Plans API lets you create and manage installment/recurring payment options. Plans define the billing cycle, amount, and currency for subscriptions.

> Depends on: **paystack-setup** for the `paystackRequest` helper.  
> Related: **paystack-subscriptions** for subscribing customers to plans.

## Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/plan` | Create a plan |
| GET | `/plan` | List plans |
| GET | `/plan/:id_or_code` | Fetch a plan |
| PUT | `/plan/:id_or_code` | Update a plan |

## Create Plan

`POST /plan`

| Param | Type | Required | Description |
| --- | --- | --- | --- |
| `name` | string | Yes | Name of the plan |
| `amount` | integer | Yes | Amount in **subunits** (e.g. 500000 = ₦5,000) |
| `interval` | string | Yes | `daily`, `weekly`, `monthly`, `quarterly`, `biannually`, `annually` |
| `description` | string | No | Plan description |
| `send_invoices` | boolean | No | Send invoices to customers (default: true) |
| `send_sms` | string | No | Send SMS to customers (default: true) |
| `currency` | string | No | Currency code e.g. `NGN`, `GHS`, `ZAR`, `USD` |
| `invoice_limit` | integer | No | Max invoices to raise during subscription |

```typescript
const plan = await paystackRequest<{
  name: string;
  plan_code: string;
  amount: number;
  interval: string;
}>("/plan", {
  method: "POST",
  body: JSON.stringify({
    name: "Pro Plan",
    amount: 500000,        // ₦5,000
    interval: "monthly",
    currency: "NGN",
    send_invoices: true,
    invoice_limit: 0,      // 0 = unlimited
  }),
});
// plan.data.plan_code → "PLN_gx2wn530m0i3w3m"
```

## List Plans

`GET /plan`

| Param | Type | Required | Description |
| --- | --- | --- | --- |
| `perPage` | integer | No | Records per page (default: 50) |
| `page` | integer | No | Page number (default: 1) |
| `status` | string | No | Filter by plan status |
| `interval` | string | No | Filter by interval |
| `amount` | integer | No | Filter by amount (in subunits) |

```typescript
const plans = await paystackRequest("/plan?perPage=20&page=1&interval=monthly");
```

## Fetch Plan

`GET /plan/:id_or_code`

Returns plan details including associated `subscriptions` array.

```typescript
const plan = await paystackRequest(
  `/plan/${encodeURIComponent("PLN_gx2wn530m0i3w3m")}`
);
```

## Update Plan

`PUT /plan/:id_or_code`

All body params are the same as Create Plan, plus:

| Param | Type | Required | Description |
| --- | --- | --- | --- |
| `update_existing_subscriptions` | boolean | No | Apply changes to existing subscriptions (default: true) |

```typescript
await paystackRequest(`/plan/${encodeURIComponent("PLN_gx2wn530m0i3w3m")}`, {
  method: "PUT",
  body: JSON.stringify({
    name: "Pro Plan (Updated)",
    amount: 750000,
    update_existing_subscriptions: false, // Only affect new subscriptions
  }),
});
```

## Intervals Reference

| Interval | Description |
| --- | --- |
| `daily` | Charge every day |
| `weekly` | Charge every 7 days |
| `monthly` | Charge every month |
| `quarterly` | Charge every 3 months |
| `biannually` | Charge every 6 months |
| `annually` | Charge every 12 months |

## Common Pattern: SaaS Pricing Setup

```typescript
async function createPricingTiers() {
  const tiers = [
    { name: "Starter", amount: 200000, interval: "monthly" as const },
    { name: "Pro", amount: 500000, interval: "monthly" as const },
    { name: "Enterprise", amount: 2000000, interval: "monthly" as const },
  ];

  const plans = await Promise.all(
    tiers.map((tier) =>
      paystackRequest("/plan", {
        method: "POST",
        body: JSON.stringify({
          ...tier,
          currency: "NGN",
          send_invoices: true,
        }),
      })
    )
  );

  return plans.map((p: any) => ({
    name: p.data.name,
    code: p.data.plan_code,
    amount: p.data.amount,
  }));
}
```
