---
name: paystack-subscriptions
description: >-
  Paystack Subscriptions API — create, list, fetch, enable, disable subscriptions
  and manage card update links. Use this skill whenever implementing recurring billing,
  subscribing customers to plans, enabling or disabling auto-renewal, generating card
  update links for expiring cards, or handling subscription lifecycle events. Also use
  when you see references to subscription_code, SUB_ prefixed codes, email_token, or
  the /subscription endpoint.
---

# Paystack Subscriptions

The Subscriptions API lets you create and manage recurring payments. A subscription links a customer to a plan and charges them automatically at the plan's interval.

> Depends on: **paystack-setup** for the `paystackRequest` helper.  
> Related: **paystack-plans** for creating plans, **paystack-customers** for customer management.

## Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/subscription` | Create a subscription |
| GET | `/subscription` | List subscriptions |
| GET | `/subscription/:id_or_code` | Fetch a subscription |
| POST | `/subscription/enable` | Enable a subscription |
| POST | `/subscription/disable` | Disable a subscription |
| GET | `/subscription/:code/manage/link` | Generate card update link |
| POST | `/subscription/:code/manage/email` | Email card update link |

## Create Subscription

`POST /subscription`

| Param | Type | Required | Description |
| --- | --- | --- | --- |
| `customer` | string | Yes | Customer email or customer code |
| `plan` | string | Yes | Plan code (e.g. `PLN_gx2wn530m0i3w3m`) |
| `authorization` | string | No | Specific authorization code (uses most recent if omitted) |
| `start_date` | string | No | First debit date in ISO 8601 (e.g. `2024-05-16T00:30:13+01:00`) |

```typescript
const subscription = await paystackRequest<{
  subscription_code: string;
  email_token: string;
  status: string;
  amount: number;
}>("/subscription", {
  method: "POST",
  body: JSON.stringify({
    customer: "CUS_xnxdt6s1zg1f4nx",
    plan: "PLN_gx2wn530m0i3w3m",
    start_date: "2024-06-01T00:00:00+01:00", // Optional: delay first charge
  }),
});
// subscription.data.subscription_code → "SUB_vsyqdmlzble3uii"
// subscription.data.email_token → "d7gofp6yppn3qz7" (needed for enable/disable)
```

## List Subscriptions

`GET /subscription`

| Param | Type | Required | Description |
| --- | --- | --- | --- |
| `perPage` | integer | No | Records per page (default: 50) |
| `page` | integer | No | Page number (default: 1) |
| `customer` | integer | No | Filter by Customer ID |
| `plan` | integer | No | Filter by Plan ID |

```typescript
const subscriptions = await paystackRequest("/subscription?perPage=20&page=1");
```

## Fetch Subscription

`GET /subscription/:id_or_code`

Returns full subscription details including `invoices`, `customer`, `plan`, and `authorization` objects.

```typescript
const sub = await paystackRequest(
  `/subscription/${encodeURIComponent("SUB_vsyqdmlzble3uii")}`
);
```

## Enable Subscription

`POST /subscription/enable`

Re-enable a previously disabled subscription.

| Param | Type | Required | Description |
| --- | --- | --- | --- |
| `code` | string | Yes | Subscription code |
| `token` | string | Yes | Email token (from create response or fetch) |

```typescript
await paystackRequest("/subscription/enable", {
  method: "POST",
  body: JSON.stringify({
    code: "SUB_vsyqdmlzble3uii",
    token: "d7gofp6yppn3qz7",
  }),
});
```

## Disable Subscription

`POST /subscription/disable`

Disable auto-renewal for a subscription. Same params as enable.

```typescript
await paystackRequest("/subscription/disable", {
  method: "POST",
  body: JSON.stringify({
    code: "SUB_vsyqdmlzble3uii",
    token: "d7gofp6yppn3qz7",
  }),
});
```

## Generate Update Subscription Link

`GET /subscription/:code/manage/link`

Generate a link for the customer to update their card on a subscription. Useful when cards are about to expire — listen for `subscription.expiring_cards` webhook.

```typescript
const result = await paystackRequest(
  `/subscription/${encodeURIComponent("SUB_vsyqdmlzble3uii")}/manage/link`
);
// result.data.link → "https://paystack.com/manage/subscriptions/..."
```

## Send Update Subscription Link via Email

`POST /subscription/:code/manage/email`

Automatically emails the customer a link to update their card.

```typescript
await paystackRequest(
  `/subscription/${encodeURIComponent("SUB_vsyqdmlzble3uii")}/manage/email`,
  { method: "POST" }
);
```

## Full Subscription Flow

```typescript
// 1. Customer pays (creates authorization via checkout/charge)
// 2. Create subscription using customer's authorization
const sub = await paystackRequest("/subscription", {
  method: "POST",
  body: JSON.stringify({
    customer: "customer@email.com",
    plan: "PLN_gx2wn530m0i3w3m",
  }),
});

// 3. Store email_token for later management
const { subscription_code, email_token } = sub.data;

// 4. Handle webhook events for subscription lifecycle
// - invoice.create: 3 days before charge
// - invoice.update: after successful charge
// - invoice.payment_failed: charge failed
// - subscription.disable: subscription disabled
// - subscription.not_renew: set to non-renewing
// - subscription.expiring_cards: monthly card expiry notice

// 5. Customer wants to cancel
await paystackRequest("/subscription/disable", {
  method: "POST",
  body: JSON.stringify({ code: subscription_code, token: email_token }),
});

// 6. Customer wants to resume
await paystackRequest("/subscription/enable", {
  method: "POST",
  body: JSON.stringify({ code: subscription_code, token: email_token }),
});
```

## Important Notes

- A customer must have at least one valid authorization (from a previous charge) before subscribing
- The `email_token` is essential for enable/disable operations — store it when creating subscriptions
- Use `start_date` to delay the first charge (e.g. for free trial periods)
- Plan updates with `update_existing_subscriptions: true` propagate to active subscriptions
- Listen for `subscription.expiring_cards` webhook to proactively send card update links
