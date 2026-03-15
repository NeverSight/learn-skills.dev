---
name: paystack-dedicated-accounts
description: >-
  Paystack Dedicated Virtual Accounts (DVA) API — create, assign, and manage unique
  virtual bank account numbers for customers. Supports Wema Bank and Access Bank providers
  in Nigeria and Ghana. Use this skill whenever implementing bank transfer payments via
  dedicated accounts, assigning virtual account numbers to customers, querying DVA
  transactions, splitting DVA payments with subaccounts, deactivating accounts, or
  fetching available bank providers. Also use when you see references to
  /dedicated_account endpoint, DVA, or virtual account numbers.
---

# Paystack Dedicated Virtual Accounts

The Dedicated Virtual Account API lets you create and manage unique payment account numbers for your customers. Available for Nigerian and Ghanaian merchants.

> Depends on: **paystack-setup** for the `paystackRequest` helper.  
> Related: **paystack-subaccounts** and **paystack-splits** for splitting DVA transactions.

## Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/dedicated_account` | Create DVA for existing customer |
| POST | `/dedicated_account/assign` | Create customer + assign DVA in one step |
| GET | `/dedicated_account` | List dedicated accounts |
| GET | `/dedicated_account/:id` | Fetch a dedicated account |
| GET | `/dedicated_account/requery` | Requery for new transactions |
| DELETE | `/dedicated_account/:id` | Deactivate a dedicated account |
| POST | `/dedicated_account/split` | Add split to DVA transactions |
| DELETE | `/dedicated_account/split` | Remove split from DVA |
| GET | `/dedicated_account/available_providers` | List available bank providers |

## Fetch Bank Providers

Always check available providers first:

```typescript
const providers = await paystackRequest<Array<{
  provider_slug: string;
  bank_id: number;
  bank_name: string;
}>>("/dedicated_account/available_providers");
// e.g. [{ provider_slug: "wema-bank", bank_id: 20, bank_name: "Wema Bank" }]
```

## Create DVA for Existing Customer

`POST /dedicated_account`

| Param | Type | Required | Description |
| --- | --- | --- | --- |
| `customer` | string | Yes | Customer ID or code |
| `preferred_bank` | string | No | Bank slug (e.g. `wema-bank`, `access-bank`) |
| `subaccount` | string | No | Subaccount code for split payments |
| `split_code` | string | No | Split code for multi-party splits |
| `first_name` | string | No | Customer first name |
| `last_name` | string | No | Customer last name |
| `phone` | string | No | Customer phone number |

```typescript
const dva = await paystackRequest<{
  bank: { name: string; slug: string };
  account_name: string;
  account_number: string;
  assigned: boolean;
  active: boolean;
}>("/dedicated_account", {
  method: "POST",
  body: JSON.stringify({
    customer: "CUS_dy1r7ts03zixbq5",
    preferred_bank: "wema-bank",
  }),
});
// dva.data.account_number → "9930000737"
```

## Assign DVA (Create Customer + DVA)

`POST /dedicated_account/assign` — creates the customer, validates, and assigns a DVA in one step.

| Param | Type | Required | Description |
| --- | --- | --- | --- |
| `email` | string | Yes | Customer email |
| `first_name` | string | Yes | First name |
| `last_name` | string | Yes | Last name |
| `phone` | string | Yes | Phone number |
| `preferred_bank` | string | Yes | Bank slug |
| `country` | string | Yes | `NG` or `GH` |
| `account_number` | string | No | Customer's account number |
| `bvn` | string | No | Bank Verification Number (Nigeria) |
| `bank_code` | string | No | Customer's bank code |
| `subaccount` | string | No | Subaccount code for split |
| `split_code` | string | No | Split code for multi-party split |

```typescript
await paystackRequest("/dedicated_account/assign", {
  method: "POST",
  body: JSON.stringify({
    email: "janedoe@test.com",
    first_name: "Jane",
    last_name: "Doe",
    phone: "+2348100000000",
    preferred_bank: "wema-bank",
    country: "NG",
  }),
});
// Response: { status: true, message: "Assign dedicated account in progress" }
```

## List Dedicated Accounts

`GET /dedicated_account`

| Param | Type | Required | Description |
| --- | --- | --- | --- |
| `active` | boolean | No | Filter by active status |
| `currency` | string | No | `NGN` or `GHS` |
| `provider_slug` | string | No | Bank slug filter |
| `bank_id` | string | No | Bank ID filter |
| `customer` | string | No | Customer ID filter |

```typescript
const accounts = await paystackRequest("/dedicated_account?active=true&currency=NGN");
```

## Fetch Dedicated Account

```typescript
const account = await paystackRequest(`/dedicated_account/${dedicatedAccountId}`);
```

## Requery for New Transactions

```typescript
await paystackRequest(
  `/dedicated_account/requery?account_number=9930000737&provider_slug=wema-bank&date=2024-01-15`
);
```

## Deactivate Dedicated Account

```typescript
await paystackRequest(`/dedicated_account/${dedicatedAccountId}`, {
  method: "DELETE",
});
```

## Split DVA Transactions

Add a split to DVA incoming payments:

```typescript
await paystackRequest("/dedicated_account/split", {
  method: "POST",
  body: JSON.stringify({
    customer: "CUS_dy1r7ts03zixbq5",
    split_code: "SPL_e7jnRLtzla",
    // OR use subaccount instead of split_code:
    // subaccount: "ACCT_6uujpqtzmnufzkw",
  }),
});
```

Remove a split:

```typescript
await paystackRequest("/dedicated_account/split", {
  method: "DELETE",
  body: JSON.stringify({
    account_number: "0033322211",
  }),
});
```

## Full DVA Flow

```typescript
// 1. Check available providers
const providers = await paystackRequest("/dedicated_account/available_providers");

// 2. Create customer first (or use existing)
const customer = await paystackRequest("/customer", {
  method: "POST",
  body: JSON.stringify({
    email: "user@example.com",
    first_name: "John",
    last_name: "Doe",
    phone: "+2348012345678",
  }),
});

// 3. Create DVA for the customer
const dva = await paystackRequest("/dedicated_account", {
  method: "POST",
  body: JSON.stringify({
    customer: customer.data.customer_code,
    preferred_bank: "wema-bank",
  }),
});

// 4. Display account details to user for bank transfer
console.log(`Pay to: ${dva.data.account_number} (${dva.data.bank.name})`);

// 5. Listen for charge.success webhook to confirm payment
// See paystack-webhooks skill for webhook handling
```
