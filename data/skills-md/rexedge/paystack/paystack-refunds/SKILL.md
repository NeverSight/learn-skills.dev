---
name: paystack-refunds
description: >-
  Paystack Refunds API — create full or partial refunds, retry failed refunds with
  customer bank details, list and fetch refund records. Use this skill whenever
  implementing refund functionality, processing customer refund requests, handling
  partial refunds, retrying refunds that need attention, or tracking refund status.
  Also use when you see references to refund.processed, refund.failed, refund.pending
  webhook events, or the /refund endpoint.
---

# Paystack Refunds

The Refunds API lets you create and manage refunds for transactions. Supports full and partial refunds.

> Depends on: **paystack-setup** for the `paystackRequest` helper.  
> Related: **paystack-webhooks** for `refund.processed`, `refund.failed`, `refund.pending` events.

## Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/refund` | Create a refund |
| POST | `/refund/retry_with_customer_details/:id` | Retry a failed refund |
| GET | `/refund` | List refunds |
| GET | `/refund/:id` | Fetch a refund |

## Create Refund

`POST /refund`

| Param | Type | Required | Description |
| --- | --- | --- | --- |
| `transaction` | string | Yes | Transaction reference or ID |
| `amount` | integer | No | Amount in subunits (defaults to full transaction amount) |
| `currency` | string | No | Currency code |
| `customer_note` | string | No | Reason shown to customer |
| `merchant_note` | string | No | Internal reason for merchant |

### Full Refund

```typescript
const refund = await paystackRequest<{
  status: string;
  amount: number;
  transaction: { reference: string; amount: number };
}>("/refund", {
  method: "POST",
  body: JSON.stringify({
    transaction: "T685312322670591",  // Transaction reference or ID
  }),
});
// refund.message → "Refund has been queued for processing"
```

### Partial Refund

```typescript
await paystackRequest("/refund", {
  method: "POST",
  body: JSON.stringify({
    transaction: "T685312322670591",
    amount: 5000,                        // Refund ₦50 of a larger transaction
    customer_note: "Partial refund for damaged item",
    merchant_note: "Customer reported damage on item #3",
  }),
});
```

## Retry Refund

`POST /refund/retry_with_customer_details/:id`

Retry a refund with `needs-attention` status by providing the customer's bank account details.

| Param | Type | Required | Description |
| --- | --- | --- | --- |
| `refund_account_details` | object | Yes | Customer's bank account details |
| `refund_account_details.currency` | string | Yes | Currency (same as original payment) |
| `refund_account_details.account_number` | string | Yes | Customer's bank account number |
| `refund_account_details.bank_id` | string | Yes | Bank ID (from List Banks endpoint) |

```typescript
await paystackRequest(`/refund/retry_with_customer_details/${refundId}`, {
  method: "POST",
  body: JSON.stringify({
    refund_account_details: {
      currency: "NGN",
      account_number: "1234567890",
      bank_id: "9",
    },
  }),
});
```

## List Refunds

`GET /refund`

| Param | Type | Required | Description |
| --- | --- | --- | --- |
| `transaction` | string | No | Filter by transaction ID |
| `currency` | string | No | Filter by currency |
| `from` | date | No | Start date e.g. `2016-09-21` |
| `to` | date | No | End date |
| `perPage` | integer | No | Records per page (default: 50) |
| `page` | integer | No | Page number (default: 1) |

```typescript
const refunds = await paystackRequest("/refund?perPage=20&page=1");
```

## Fetch Refund

`GET /refund/:id`

```typescript
const refund = await paystackRequest(`/refund/${refundId}`);
// refund.data.status → "pending" | "processing" | "processed" | "failed"
```

## Refund Statuses

| Status | Description |
| --- | --- |
| `pending` | Refund initiated, awaiting processor |
| `processing` | Refund received by processor |
| `processed` | Refund successfully completed |
| `failed` | Refund failed — your account is credited back |
| `needs-attention` | Refund needs manual intervention (retry with customer details) |

## Webhook Events

Listen for these events to track refund lifecycle:

- `refund.pending` — Refund initiated
- `refund.processing` — Refund being processed
- `refund.processed` — Refund completed successfully
- `refund.failed` — Refund failed (amount credited back to your account)

## Important Notes

- Refund amount cannot exceed the original transaction amount
- If `amount` is omitted, the full transaction amount is refunded
- Partial refunds are supported — you can refund a portion of a transaction
- Failed refunds credit the refund amount back to your Paystack balance
- For `needs-attention` status, retry with customer's bank account details
- Always listen for webhook events rather than polling for refund status
