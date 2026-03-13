---
name: paystack-subaccounts
description: >-
  Paystack Subaccounts API — create and manage subaccounts for split payments between
  your main account and sub-merchants. Configure percentage charges, settlement banks,
  settlement schedules, and contact details. Use this skill whenever building a
  marketplace, implementing split payments, onboarding sub-merchants, configuring
  payout schedules (auto/weekly/monthly/manual), or managing multi-vendor payment
  flows. Also use when you see references to subaccount_code, ACCT_ prefixed codes,
  percentage_charge, or the /subaccount endpoint.
---

# Paystack Subaccounts

The Subaccounts API lets you create and manage subaccounts for split payments. Subaccounts represent sub-merchants/vendors who receive a portion of each payment.

> Depends on: **paystack-setup** for the `paystackRequest` helper.  
> Related: **paystack-splits** for multi-party split configurations.

## Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/subaccount` | Create a subaccount |
| GET | `/subaccount` | List subaccounts |
| GET | `/subaccount/:id_or_code` | Fetch a subaccount |
| PUT | `/subaccount/:id_or_code` | Update a subaccount |

## Create Subaccount

`POST /subaccount`

| Param | Type | Required | Description |
| --- | --- | --- | --- |
| `business_name` | string | Yes | Name of the sub-merchant business |
| `bank_code` | string | Yes | Bank code (from List Banks endpoint) |
| `account_number` | string | Yes | Bank account number for settlements |
| `percentage_charge` | float | Yes | Percentage the **main account** receives from each payment |
| `description` | string | No | Description of the subaccount |
| `primary_contact_email` | string | No | Contact email |
| `primary_contact_name` | string | No | Contact person name |
| `primary_contact_phone` | string | No | Contact phone number |
| `metadata` | string | No | Stringified JSON with custom fields |

```typescript
const subaccount = await paystackRequest<{
  subaccount_code: string;
  business_name: string;
  percentage_charge: number;
}>("/subaccount", {
  method: "POST",
  body: JSON.stringify({
    business_name: "Vendor Store",
    settlement_bank: "058",        // GTBank
    account_number: "0123456047",
    percentage_charge: 20,         // Main account gets 20%, subaccount gets 80%
    description: "Electronics vendor",
    primary_contact_email: "vendor@store.com",
  }),
});
// subaccount.data.subaccount_code → "ACCT_6uujpqtzmnufzkw"
```

## List Subaccounts

`GET /subaccount`

| Param | Type | Required | Description |
| --- | --- | --- | --- |
| `perPage` | integer | No | Records per page (default: 50) |
| `page` | integer | No | Page number (default: 1) |
| `from` | datetime | No | Start date |
| `to` | datetime | No | End date |

```typescript
const subaccounts = await paystackRequest("/subaccount?perPage=20&page=1");
```

## Fetch Subaccount

`GET /subaccount/:id_or_code`

```typescript
const sub = await paystackRequest(
  `/subaccount/${encodeURIComponent("ACCT_6uujpqtzmnufzkw")}`
);
```

## Update Subaccount

`PUT /subaccount/:id_or_code`

| Param | Type | Required | Description |
| --- | --- | --- | --- |
| `business_name` | string | Yes | Business name |
| `description` | string | Yes | Description |
| `bank_code` | string | No | New bank code |
| `account_number` | string | No | New account number |
| `active` | boolean | No | `true` to activate, `false` to deactivate |
| `percentage_charge` | float | No | Updated percentage |
| `settlement_schedule` | string | No | `auto` (T+1), `weekly`, `monthly`, or `manual` |
| `primary_contact_email` | string | No | Updated contact email |
| `primary_contact_name` | string | No | Updated contact name |
| `primary_contact_phone` | string | No | Updated contact phone |
| `metadata` | string | No | Stringified JSON |

```typescript
await paystackRequest(
  `/subaccount/${encodeURIComponent("ACCT_6uujpqtzmnufzkw")}`,
  {
    method: "PUT",
    body: JSON.stringify({
      business_name: "Vendor Store Global",
      description: "International electronics vendor",
      settlement_schedule: "weekly",
      percentage_charge: 15,
    }),
  }
);
```

## Settlement Schedules

| Schedule | Description |
| --- | --- |
| `auto` | Payout is T+1 (next business day) — **default** |
| `weekly` | Payout every week |
| `monthly` | Payout every month |
| `manual` | Payout only when requested |

## Using Subaccounts in Transactions

Pass the `subaccount` code when initializing a transaction:

```typescript
// Initialize transaction with subaccount split
const tx = await paystackRequest("/transaction/initialize", {
  method: "POST",
  body: JSON.stringify({
    email: "customer@email.com",
    amount: 500000,
    subaccount: "ACCT_6uujpqtzmnufzkw",
    // Optional overrides:
    // transaction_charge: 10000,  // Fixed charge in subunits (overrides percentage)
    // bearer: "subaccount",       // Who bears Paystack fees: "account" or "subaccount"
  }),
});
```

## Marketplace Pattern

```typescript
// 1. Onboard vendor → create subaccount
const vendor = await paystackRequest("/subaccount", {
  method: "POST",
  body: JSON.stringify({
    business_name: "Vendor A",
    settlement_bank: "058",
    account_number: "0123456789",
    percentage_charge: 10, // Platform takes 10%
  }),
});

// 2. Customer buys from vendor → charge with subaccount
await paystackRequest("/transaction/initialize", {
  method: "POST",
  body: JSON.stringify({
    email: "buyer@email.com",
    amount: 100000,
    subaccount: vendor.data.subaccount_code,
    bearer: "subaccount", // Vendor bears Paystack fees
  }),
});
// Platform gets 10%, Vendor gets 90% minus Paystack fees
```
