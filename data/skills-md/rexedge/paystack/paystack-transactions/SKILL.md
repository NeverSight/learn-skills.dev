---
name: paystack-transactions
description: >-
  Paystack Transactions API — initialize payments, verify transactions, list/fetch
  transaction history, charge saved authorizations, view timelines, get totals, export
  data, and perform partial debits. Use this skill whenever building a checkout flow,
  verifying payment status, recharging a returning customer's saved card, pulling
  transaction reports or analytics, exporting transaction CSVs, or handling any
  transaction-related Paystack endpoint. Also use when you see references to
  /transaction/initialize, /transaction/verify, authorization_url, access_code, or
  charge_authorization in Paystack integrations.
---

# Paystack Transactions

The Transactions API lets you create and manage payments on your integration. This covers the entire transaction lifecycle from initialization through verification.

> Depends on: **paystack-setup** for the `paystackRequest` helper and environment config.

## Transaction Lifecycle

```
Initialize (server) → Complete (client/redirect) → Verify (server) + Webhook
```

## Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/transaction/initialize` | Initialize a transaction |
| GET | `/transaction/verify/:reference` | Verify a transaction |
| GET | `/transaction` | List transactions |
| GET | `/transaction/:id` | Fetch a transaction |
| POST | `/transaction/charge_authorization` | Charge a saved authorization |
| GET | `/transaction/timeline/:id_or_reference` | View transaction timeline |
| GET | `/transaction/totals` | Get transaction totals |
| GET | `/transaction/export` | Export transactions as CSV |
| POST | `/transaction/partial_debit` | Partial debit on an authorization |

## Initialize Transaction

`POST /transaction/initialize`

Creates a payment and returns an `authorization_url` (for redirect) and `access_code` (for Popup/InlineJS).

### Parameters (Body)

| Param | Type | Required | Description |
| --- | --- | --- | --- |
| `amount` | string | Yes | Amount in **subunits** (kobo). `"50000"` = NGN 500 |
| `email` | string | Yes | Customer's email address |
| `reference` | string | No | Unique ref. Alphanumeric + `-` `.` `=` only |
| `currency` | string | No | `NGN`, `USD`, `GHS`, `ZAR`, `KES`. Defaults to integration currency |
| `callback_url` | string | No | Override the dashboard callback URL |
| `channels` | array | No | `["card","bank","ussd","qr","mobile_money","bank_transfer","eft","apple_pay"]` |
| `plan` | string | No | Plan code for subscription-based payment |
| `invoice_limit` | integer | No | Max charges for subscription |
| `metadata` | string | No | Stringified JSON with `custom_fields` array |
| `subaccount` | string | No | Subaccount code e.g. `ACCT_8f4s1eq7ml6rlzj` |
| `split_code` | string | No | Split code e.g. `SPL_98WF13Eb3w` |
| `transaction_charge` | integer | No | Flat fee override for split (in subunits) |
| `bearer` | string | No | `"account"` or `"subaccount"` — who pays Paystack fees |

### Response

```json
{
  "status": true,
  "message": "Authorization URL created",
  "data": {
    "authorization_url": "https://checkout.paystack.com/3ni8kdavz62431k",
    "access_code": "3ni8kdavz62431k",
    "reference": "re4lyvq3s3"
  }
}
```

### Server Action Example (Next.js)

```typescript
"use server";
import { paystackRequest } from "@/lib/paystack";

export async function initializePayment(email: string, amountInNaira: number) {
  const result = await paystackRequest<{
    authorization_url: string;
    access_code: string;
    reference: string;
  }>("/transaction/initialize", {
    method: "POST",
    body: JSON.stringify({
      email,
      amount: Math.round(amountInNaira * 100).toString(),
      callback_url: `${process.env.NEXT_PUBLIC_APP_URL}/payment/callback`,
    }),
  });
  return result.data;
}
```

### Client-Side Popup (InlineJS)

```typescript
"use client";
import PaystackInline from "@paystack/inline-js";

function PayButton({ email, amount }: { email: string; amount: number }) {
  const handlePay = async () => {
    // 1. Initialize on server
    const { access_code } = await initializePayment(email, amount);

    // 2. Open Popup with access_code
    const popup = new PaystackInline();
    popup.openIframe({
      accessCode: access_code,
      onSuccess: (response) => {
        // 3. Verify on server — NEVER trust this alone
        verifyTransaction(response.reference);
      },
      onClose: () => console.log("Payment window closed"),
    });
  };

  return <button onClick={handlePay}>Pay ₦{amount}</button>;
}
```

### Redirect Method

After initializing, redirect the user to `authorization_url`. Paystack redirects back to your `callback_url` with `?trxref=REFERENCE&reference=REFERENCE` in the query string. Verify server-side immediately.

```typescript
// app/payment/callback/page.tsx
import { paystackRequest } from "@/lib/paystack";

export default async function PaymentCallback({
  searchParams,
}: {
  searchParams: Promise<{ reference?: string }>;
}) {
  const { reference } = await searchParams;
  if (!reference) return <p>No reference provided</p>;

  const result = await paystackRequest<{ status: string; amount: number }>(
    `/transaction/verify/${encodeURIComponent(reference)}`
  );

  if (result.data.status === "success") {
    return <p>Payment successful!</p>;
  }
  return <p>Payment failed: {result.data.status}</p>;
}
```

## Verify Transaction

`GET /transaction/verify/:reference`

Always verify server-side after payment. The `reference` is in the callback URL query params or returned from Popup's `onSuccess`.

```typescript
const result = await paystackRequest<{
  id: number;
  status: "success" | "failed" | "abandoned";
  reference: string;
  amount: number;
  currency: string;
  channel: string;
  paid_at: string;
  authorization: {
    authorization_code: string;
    reusable: boolean;
    card_type: string;
    last4: string;
    bank: string;
  };
  customer: { email: string; id: number };
}>(`/transaction/verify/${encodeURIComponent(reference)}`);
```

Check `result.data.status === "success"` and validate `result.data.amount` matches expected amount before fulfilling the order.

## List Transactions

`GET /transaction`

### Query Parameters

| Param | Type | Description |
| --- | --- | --- |
| `perPage` | integer | Records per page (default 50) |
| `page` | integer | Page number (default 1) |
| `customer` | integer | Filter by customer ID |
| `terminalid` | string | Filter by Terminal ID |
| `status` | string | `"success"`, `"failed"`, or `"abandoned"` |
| `from` | datetime | Start date e.g. `2024-01-01T00:00:00.000Z` |
| `to` | datetime | End date |
| `amount` | integer | Filter by amount (in subunits) |

```typescript
const params = new URLSearchParams({ status: "success", perPage: "20" });
const result = await paystackRequest<Transaction[]>(`/transaction?${params}`);
```

## Fetch Transaction

`GET /transaction/:id`

Fetch a single transaction by its numeric ID.

```typescript
const result = await paystackRequest<Transaction>(`/transaction/${transactionId}`);
```

## Charge Authorization

`POST /transaction/charge_authorization`

Charge a customer's previously saved card (where `authorization.reusable === true`).

| Param | Type | Required | Description |
| --- | --- | --- | --- |
| `amount` | string | Yes | Amount in subunits |
| `email` | string | Yes | Customer's email |
| `authorization_code` | string | Yes | e.g. `AUTH_72btv547` |
| `reference` | string | No | Unique transaction reference |
| `currency` | string | No | Currency code |
| `queue` | boolean | No | Set `true` for scheduled/bulk charges |

```typescript
const result = await paystackRequest<Transaction>(
  "/transaction/charge_authorization",
  {
    method: "POST",
    body: JSON.stringify({
      authorization_code: "AUTH_72btv547",
      email: "customer@email.com",
      amount: "20000",
    }),
  }
);
```

## Transaction Timeline

`GET /transaction/timeline/:id_or_reference`

Returns a step-by-step history of the transaction (attempted payment method, success/failure, time spent).

```typescript
const result = await paystackRequest<{
  start_time: number;
  time_spent: number;
  attempts: number;
  errors: number;
  success: boolean;
  history: Array<{ type: string; message: string; time: number }>;
}>(`/transaction/timeline/${reference}`);
```

## Transaction Totals

`GET /transaction/totals`

Returns aggregate volume and count. Supports `from`, `to`, `perPage`, `page` query params.

```typescript
const result = await paystackRequest<{
  total_transactions: number;
  total_volume: number;
  total_volume_by_currency: Array<{ currency: string; amount: number }>;
  pending_transfers: number;
}>("/transaction/totals");
```

## Export Transactions

`GET /transaction/export`

Returns a CSV download link. Supports all list filters plus `settled`, `settlement`, `payment_page`.

```typescript
const params = new URLSearchParams({ from: "2024-01-01", status: "success" });
const result = await paystackRequest<{ path: string }>(
  `/transaction/export?${params}`
);
// result.data.path is a time-limited S3 URL to the CSV
```

## Partial Debit

`POST /transaction/partial_debit`

Debit a portion of a customer's available balance on an authorization. Useful for metered billing.

| Param | Type | Required | Description |
| --- | --- | --- | --- |
| `authorization_code` | string | Yes | Auth code from previous transaction |
| `currency` | string | Yes | `NGN` or `GHS` |
| `amount` | string | Yes | Amount in subunits |
| `email` | string | Yes | Customer email tied to the auth code |
| `reference` | string | No | Unique reference |
| `at_least` | string | No | Minimum amount to charge if full amount fails |

```typescript
const result = await paystackRequest<Transaction>(
  "/transaction/partial_debit",
  {
    method: "POST",
    body: JSON.stringify({
      authorization_code: "AUTH_72btv547",
      currency: "NGN",
      amount: "20000",
      email: "customer@email.com",
      at_least: "10000",
    }),
  }
);
```

## Important Notes

- **Transaction IDs** are unsigned 64-bit integers — store as `string` in TypeScript to avoid precision loss
- **Always verify server-side** after payment — never trust client-side callbacks alone
- **Amount validation**: always confirm `result.data.amount` matches your expected amount after verification
- The `authorization_code` from a successful transaction can be saved and reused for future charges if `authorization.reusable === true`
- Metadata supports `custom_fields` for dashboard display — stringify the JSON before sending
