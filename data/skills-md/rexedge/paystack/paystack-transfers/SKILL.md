---
name: paystack-transfers
description: >-
  Paystack Transfers API — send money to bank accounts and mobile wallets. Initiate
  single and bulk transfers, finalize OTP-verified transfers, list, fetch, and verify
  transfer status. Use this skill whenever implementing payouts, disbursements, vendor
  payments, withdrawal flows, or any feature that sends money from your Paystack balance
  to recipients. Also use when you see references to transfer_code, TRF_ prefixed codes,
  the /transfer endpoint, or need to handle transfer OTP verification.
---

# Paystack Transfers

The Transfers API lets you send money from your Paystack balance to bank accounts and mobile wallets. Transfers require a pre-created transfer recipient.

> Depends on: **paystack-setup** for the `paystackRequest` helper.  
> Related: **paystack-transfer-recipients** for creating recipients before transfers.

## Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/transfer` | Initiate a transfer |
| POST | `/transfer/finalize_transfer` | Finalize transfer (OTP) |
| POST | `/transfer/bulk` | Initiate bulk transfer |
| GET | `/transfer` | List transfers |
| GET | `/transfer/:id_or_code` | Fetch a transfer |
| GET | `/transfer/verify/:reference` | Verify a transfer |

## Initiate Transfer

`POST /transfer`

Returns status `pending` if OTP is disabled on your account, or `otp` if OTP is required.

| Param | Type | Required | Description |
| --- | --- | --- | --- |
| `source` | string | Yes | `balance` (only option) |
| `amount` | integer | Yes | Amount in subunits (kobo/pesewas) |
| `recipient` | string | Yes | Recipient code (e.g. `RCP_gd9vgag7n5lr5ix`) |
| `reference` | string | Yes | Unique identifier (16-50 chars, lowercase a-z, 0-9, `-`, `_`) |
| `reason` | string | No | Reason for transfer (shows in customer's credit notification) |
| `currency` | string | No | Currency code (defaults to `NGN`) |
| `account_reference` | string | No | Required in Kenya for MPESA Paybill and Till transfers |

```typescript
const transfer = await paystackRequest<{
  transfer_code: string;
  status: string;
  reference: string;
  amount: number;
}>("/transfer", {
  method: "POST",
  body: JSON.stringify({
    source: "balance",
    amount: 100000,          // ₦1,000
    recipient: "RCP_gd9vgag7n5lr5ix",
    reference: `txf_${crypto.randomUUID()}`,
    reason: "Vendor payment for January",
  }),
});
// transfer.data.status → "pending" or "otp"
// transfer.data.transfer_code → "TRF_v5tip3zx8nna9o78"
```

## Finalize Transfer

`POST /transfer/finalize_transfer`

Required when transfer status is `otp`. Submit the OTP sent to your business phone.

| Param | Type | Required | Description |
| --- | --- | --- | --- |
| `transfer_code` | string | Yes | Transfer code from initiate response |
| `otp` | string | Yes | OTP sent to business phone |

```typescript
await paystackRequest("/transfer/finalize_transfer", {
  method: "POST",
  body: JSON.stringify({
    transfer_code: "TRF_v5tip3zx8nna9o78",
    otp: "928783",
  }),
});
```

## Initiate Bulk Transfer

`POST /transfer/bulk`

Batch multiple transfers in a single request. **OTP must be disabled** on your account to use this endpoint.

| Param | Type | Required | Description |
| --- | --- | --- | --- |
| `source` | string | Yes | `balance` |
| `transfers` | array | Yes | Array of transfer objects |

Each transfer object:

| Param | Type | Required | Description |
| --- | --- | --- | --- |
| `amount` | integer | Yes | Amount in subunits |
| `recipient` | string | Yes | Recipient code |
| `reference` | string | Yes | Unique reference (16-50 chars) |
| `reason` | string | No | Transfer reason |

```typescript
const result = await paystackRequest("/transfer/bulk", {
  method: "POST",
  body: JSON.stringify({
    source: "balance",
    currency: "NGN",
    transfers: [
      {
        amount: 20000,
        recipient: "RCP_gd9vgag7n5lr5ix",
        reference: `txf_${crypto.randomUUID()}`,
        reason: "Bonus for the week",
      },
      {
        amount: 35000,
        recipient: "RCP_m7ljkv8leesep7p",
        reference: `txf_${crypto.randomUUID()}`,
        reason: "January salary",
      },
    ],
  }),
});
// result.message → "2 transfers queued."
```

## List Transfers

`GET /transfer`

| Param | Type | Required | Description |
| --- | --- | --- | --- |
| `perPage` | integer | No | Records per page (default: 50) |
| `page` | integer | No | Page number (default: 1) |
| `recipient` | integer | No | Filter by recipient ID |
| `from` | datetime | No | Start date |
| `to` | datetime | No | End date |

```typescript
const transfers = await paystackRequest("/transfer?perPage=20&page=1");
```

## Fetch Transfer

`GET /transfer/:id_or_code`

```typescript
const transfer = await paystackRequest(
  `/transfer/${encodeURIComponent("TRF_v5tip3zx8nna9o78")}`
);
```

## Verify Transfer

`GET /transfer/verify/:reference`

Verify the status of a transfer using its reference.

```typescript
const result = await paystackRequest(
  `/transfer/verify/${encodeURIComponent(reference)}`
);
// result.data.status → "success" | "failed" | "pending" | "reversed"
```

## Transfer Flow

```typescript
// 1. Create recipient (see paystack-transfer-recipients skill)
// 2. Initiate transfer
const transfer = await paystackRequest("/transfer", {
  method: "POST",
  body: JSON.stringify({
    source: "balance",
    amount: 500000,
    recipient: "RCP_gd9vgag7n5lr5ix",
    reference: `txf_${crypto.randomUUID()}`,
  }),
});

// 3. If OTP required, finalize
if (transfer.data.status === "otp") {
  const otp = await getOTPFromUser();
  await paystackRequest("/transfer/finalize_transfer", {
    method: "POST",
    body: JSON.stringify({
      transfer_code: transfer.data.transfer_code,
      otp,
    }),
  });
}

// 4. Listen for webhooks: transfer.success, transfer.failed, transfer.reversed
```

## Important Notes

- You can only transfer from `balance` — ensure your Paystack balance has sufficient funds
- Bulk transfers require OTP to be disabled (Dashboard → Settings → Preferences)
- Transfer references must be unique, 16-50 characters, lowercase with `-` and `_` only
- For Kenya MPESA Paybill/Till, include `account_reference` in the transfer
- Always verify transfer status via webhook (`transfer.success`, `transfer.failed`) rather than polling
