---
name: paystack-settlements
description: >-
  Paystack Settlements API — view and track payouts from Paystack to your bank account.
  List settlements with status filters, view individual settlement transactions, and
  monitor settlement timelines. Use this skill whenever tracking payouts, reconciling
  bank deposits with Paystack transactions, monitoring settlement status
  (success/processing/pending/failed), filtering settlements by subaccount, or building
  financial reconciliation tools. Also use when you see references to /settlement
  endpoint or need to understand when funds will reach your bank account.
---

# Paystack Settlements

The Settlements API lets you track payouts from Paystack to your bank account.

> Depends on: **paystack-setup** for the `paystackRequest` helper.

## Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/settlement` | List settlements |
| GET | `/settlement/:id/transactions` | List transactions in a settlement |

## Settlement Statuses

| Status | Description |
| --- | --- |
| `success` | Funds successfully deposited |
| `processing` | Settlement is being processed |
| `pending` | Settlement is queued |
| `failed` | Settlement failed |

## List Settlements

| Param | Type | Required | Description |
| --- | --- | --- | --- |
| `perPage` | integer | No | Records per page (default: 50) |
| `page` | integer | No | Page number (default: 1) |
| `status` | string | No | `success`, `processing`, `pending`, or `failed` |
| `subaccount` | string | No | Subaccount ID, or `none` for main account only |
| `from` | datetime | No | Start date |
| `to` | datetime | No | End date |

```typescript
// All successful settlements
const settlements = await paystackRequest(
  "/settlement?status=success&from=2024-01-01&to=2024-01-31"
);

// settlements.data[0]:
// {
//   id: 3090024,
//   status: "success",
//   currency: "NGN",
//   total_amount: 995,       // Amount settled (subunits)
//   effective_amount: 995,   // Amount after deductions
//   total_fees: 5,           // Paystack fees
//   total_processed: 1000,   // Gross transaction amount
//   settlement_date: "2022-11-09T00:00:00.000Z"
// }

// Main account settlements only (exclude subaccounts)
await paystackRequest("/settlement?subaccount=none");

// Specific subaccount settlements
await paystackRequest("/settlement?subaccount=ACCT_6uujpqtzmnufzkw");
```

## List Settlement Transactions

Get the individual transactions that make up a settlement:

```typescript
const txs = await paystackRequest(
  `/settlement/${settlementId}/transactions?perPage=50&page=1`
);

// txs.data[0]:
// {
//   id: 2067030515,       // Store as unsigned 64-bit integer
//   status: "success",
//   reference: "da8ed5u8sz6yn95",
//   amount: 10000,
//   channel: "card",
//   currency: "NGN",
//   paid_at: "2022-09-01T10:36:37.000Z"
// }
```

> **Important**: Transaction IDs should be stored as unsigned 64-bit integers.

## Reconciliation Pattern

```typescript
async function reconcileSettlements(from: string, to: string) {
  const settlements = await paystackRequest(
    `/settlement?status=success&from=${from}&to=${to}`
  );

  for (const settlement of settlements.data) {
    const txs = await paystackRequest(
      `/settlement/${settlement.id}/transactions`
    );

    console.log(
      `Settlement #${settlement.id}: ` +
      `₦${(settlement.total_processed / 100).toFixed(2)} gross → ` +
      `₦${(settlement.effective_amount / 100).toFixed(2)} net ` +
      `(${txs.data.length} transactions)`
    );
  }
}
```
