---
name: paystack-payment-requests
description: >-
  Paystack Payment Requests (Invoicing) API — create, manage, and send payment requests
  (invoices) to customers. Supports line items, taxes, due dates, draft mode, auto
  invoice numbering, split payments, email notifications, and archiving. Use this skill
  whenever building invoicing systems, sending payment requests to customers, managing
  invoice line items and taxes, tracking invoice totals and statuses, or implementing
  B2B payment collection. Also use when you see references to /paymentrequest endpoint,
  PRQ_ prefixed codes, invoice numbers, or payment request finalization.
---

# Paystack Payment Requests

The Payment Requests API lets you create and manage invoices for goods and services.

> Depends on: **paystack-setup** for the `paystackRequest` helper.  
> Related: **paystack-customers** for customer codes used in requests.

## Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/paymentrequest` | Create a payment request |
| GET | `/paymentrequest` | List payment requests |
| GET | `/paymentrequest/:id_or_code` | Fetch a payment request |
| PUT | `/paymentrequest/:id_or_code` | Update a payment request |
| GET | `/paymentrequest/verify/:code` | Verify a payment request |
| POST | `/paymentrequest/notify/:code` | Send notification |
| GET | `/paymentrequest/totals` | Get totals/metrics |
| POST | `/paymentrequest/finalize/:code` | Finalize a draft |
| POST | `/paymentrequest/archive/:code` | Archive a request |

## Create Payment Request

| Param | Type | Required | Description |
| --- | --- | --- | --- |
| `customer` | string | Yes | Customer ID or code |
| `amount` | integer | No | Amount in subunits (if no line items) |
| `due_date` | datetime | No | ISO 8601 due date |
| `description` | string | No | Short description |
| `line_items` | array | No | `[{ name, amount, quantity? }]` |
| `tax` | array | No | `[{ name, amount }]` |
| `currency` | string | No | Currency code (default: NGN) |
| `send_notification` | boolean | No | Send email (default: true) |
| `draft` | boolean | No | Save as draft (default: false) |
| `has_invoice` | boolean | No | Add auto-incrementing invoice number |
| `invoice_number` | integer | No | Override invoice number |
| `split_code` | string | No | Split code for revenue sharing |

```typescript
// Invoice with line items and tax
const invoice = await paystackRequest<{
  id: number;
  request_code: string;
  invoice_number: number;
}>("/paymentrequest", {
  method: "POST",
  body: JSON.stringify({
    customer: "CUS_xwaj0txjryg393b",
    description: "Q1 2024 Services",
    due_date: "2024-03-31",
    line_items: [
      { name: "Consulting (10 hours)", amount: 500000, quantity: 1 },
      { name: "Design work", amount: 200000, quantity: 1 },
    ],
    tax: [
      { name: "VAT (7.5%)", amount: 52500 },
    ],
    send_notification: true,
    has_invoice: true,
  }),
});
// invoice.data.request_code → "PRQ_1weqqsn2wwzgft8"

// Draft invoice (no notification sent)
await paystackRequest("/paymentrequest", {
  method: "POST",
  body: JSON.stringify({
    customer: "CUS_xwaj0txjryg393b",
    amount: 100000,
    description: "Draft invoice",
    draft: true,
  }),
});
```

## List Payment Requests

```typescript
const requests = await paystackRequest(
  "/paymentrequest?status=pending&currency=NGN&perPage=20"
);
```

## Fetch / Verify

```typescript
// Fetch
const req = await paystackRequest(`/paymentrequest/${encodeURIComponent("PRQ_code")}`);

// Verify (includes payment status)
const verified = await paystackRequest(
  `/paymentrequest/verify/${encodeURIComponent("PRQ_code")}`
);
```

## Send Notification

Re-send the payment request email to the customer:

```typescript
await paystackRequest(`/paymentrequest/notify/${encodeURIComponent("PRQ_code")}`, {
  method: "POST",
});
```

## Get Totals

```typescript
const totals = await paystackRequest("/paymentrequest/totals");
// totals.data.pending → [{ currency: "NGN", amount: 42000 }]
// totals.data.successful → [{ currency: "NGN", amount: 0 }]
// totals.data.total → [{ currency: "NGN", amount: 42000 }]
```

## Finalize Draft

```typescript
await paystackRequest(`/paymentrequest/finalize/${encodeURIComponent("PRQ_code")}`, {
  method: "POST",
  body: JSON.stringify({ send_notification: true }),
});
```

## Update Payment Request

```typescript
await paystackRequest(`/paymentrequest/${encodeURIComponent("PRQ_code")}`, {
  method: "PUT",
  body: JSON.stringify({
    customer: "CUS_xwaj0txjryg393b",
    description: "Updated invoice",
    due_date: "2024-06-30",
    amount: 150000,
  }),
});
```

## Archive

```typescript
await paystackRequest(`/paymentrequest/archive/${encodeURIComponent("PRQ_code")}`, {
  method: "POST",
});
```
