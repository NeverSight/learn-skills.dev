---
name: paystack-payment-pages
description: >-
  Paystack Payment Pages API — create and manage hosted payment pages for collecting
  payments without writing frontend code. Supports fixed/flexible amounts, custom slugs,
  subscription pages, product pages, split payments, redirects, custom fields, and phone
  collection. Use this skill whenever building checkout pages, donation pages, event
  ticket sales, product catalogs with payments, or any hosted payment link. Also use when
  you see references to page slug, /page endpoint, paystack.com/pay/ URLs, or need to
  add products to a payment page.
---

# Paystack Payment Pages

The Payment Pages API lets you create hosted payment pages at `https://paystack.com/pay/[slug]` — no frontend code needed.

> Depends on: **paystack-setup** for the `paystackRequest` helper.

## Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/page` | Create a payment page |
| GET | `/page` | List payment pages |
| GET | `/page/:id_or_slug` | Fetch a payment page |
| PUT | `/page/:id_or_slug` | Update a payment page |
| GET | `/page/check_slug_availability/:slug` | Check slug availability |
| POST | `/page/:id/product` | Add products to page |

## Create Payment Page

`POST /page`

| Param | Type | Required | Description |
| --- | --- | --- | --- |
| `name` | string | Yes | Page name |
| `description` | string | No | Page description |
| `amount` | integer | No | Fixed amount in subunits (kobo/pesewas) |
| `currency` | string | No | Defaults to integration currency |
| `slug` | string | No | Custom URL slug |
| `type` | string | No | `payment` (default), `subscription`, `product`, or `plan` |
| `plan` | string | No | Plan ID (when type is `subscription`) |
| `fixed_amount` | boolean | No | If `true`, `amount` is required and unchangeable |
| `split_code` | string | No | Split code for revenue sharing |
| `redirect_url` | string | No | Redirect URL after payment |
| `success_message` | string | No | Success message on completion |
| `notification_email` | string | No | Email for transaction notifications |
| `collect_phone` | boolean | No | Collect phone numbers |
| `custom_fields` | array | No | Custom fields to collect |
| `metadata` | object | No | Extra config (subaccount, logo, etc.) |

```typescript
// Simple payment page
const page = await paystackRequest<{
  slug: string;
  id: number;
}>("/page", {
  method: "POST",
  body: JSON.stringify({
    name: "Buttercup Brunch",
    amount: 500000, // ₦5,000
    description: "Gather your friends for the ritual that is brunch",
    slug: "buttercup-brunch",
    redirect_url: "https://mysite.com/thank-you",
    collect_phone: true,
  }),
});
// Page URL: https://paystack.com/pay/buttercup-brunch

// Subscription page
await paystackRequest("/page", {
  method: "POST",
  body: JSON.stringify({
    name: "Monthly Pro Plan",
    type: "subscription",
    plan: 1716,
  }),
});

// Donation page (flexible amount)
await paystackRequest("/page", {
  method: "POST",
  body: JSON.stringify({
    name: "Support Our Cause",
    description: "Any amount helps",
    // No amount = donor chooses
    custom_fields: [
      { display_name: "Full Name", variable_name: "full_name" },
      { display_name: "Message", variable_name: "message" },
    ],
  }),
});
```

## List Payment Pages

```typescript
const pages = await paystackRequest("/page?perPage=20&page=1");
```

## Fetch Payment Page

```typescript
const page = await paystackRequest(`/page/${encodeURIComponent("buttercup-brunch")}`);
```

## Update Payment Page

```typescript
await paystackRequest(`/page/${encodeURIComponent("buttercup-brunch")}`, {
  method: "PUT",
  body: JSON.stringify({
    name: "Updated Brunch",
    description: "New brunch description",
    amount: 750000,
    active: true,
  }),
});
```

## Check Slug Availability

```typescript
const check = await paystackRequest(
  `/page/check_slug_availability/${encodeURIComponent("my-slug")}`
);
// { status: true, message: "Slug is available" }
```

## Add Products to Page

```typescript
await paystackRequest(`/page/${pageId}/product`, {
  method: "POST",
  body: JSON.stringify({
    product: [473, 292], // Product IDs
  }),
});
```
