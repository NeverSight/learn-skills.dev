---
name: paystack-splits
description: >-
  Paystack Transaction Splits API — create, update, and manage multi-party payment splits
  across subaccounts. Configure percentage or flat-amount splits with flexible bearer
  types (subaccount, account, all-proportional, all). Add or remove subaccounts from
  split groups. Use this skill whenever implementing revenue sharing between multiple
  parties, marketplace commission structures, multi-vendor payment distribution, or any
  flow that divides a single payment among multiple recipients. Also use when you see
  references to split_code, SPL_ prefixed codes, bearer_type, or the /split endpoint.
---

# Paystack Transaction Splits

The Transaction Splits API lets you split payment settlements across your main account and one or more subaccounts. More flexible than simple subaccount splits.

> Depends on: **paystack-setup** for the `paystackRequest` helper.  
> Related: **paystack-subaccounts** for creating subaccounts used in splits.

## Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/split` | Create a split |
| GET | `/split` | List splits |
| GET | `/split/:id` | Fetch a split |
| PUT | `/split/:id` | Update a split |
| POST | `/split/:id/subaccount/add` | Add/update subaccount in split |
| POST | `/split/:id/subaccount/remove` | Remove subaccount from split |

## Create Split

`POST /split`

| Param | Type | Required | Description |
| --- | --- | --- | --- |
| `name` | string | Yes | Name of the split |
| `type` | string | Yes | `percentage` or `flat` |
| `currency` | string | Yes | Currency code (e.g. `NGN`) |
| `subaccounts` | array | Yes | Array of `{ subaccount, share }` objects |
| `bearer_type` | string | Yes | Who bears Paystack fees (see table below) |
| `bearer_subaccount` | string | No | Subaccount code (required if bearer_type is `subaccount`) |

### Bearer Types

| Type | Description |
| --- | --- |
| `subaccount` | A specific subaccount bears fees |
| `account` | The main account bears all fees |
| `all-proportional` | Fees are split proportionally among all parties |
| `all` | Each party bears fees on their share |

### Percentage Split

```typescript
const split = await paystackRequest<{
  split_code: string;
  name: string;
  type: string;
}>("/split", {
  method: "POST",
  body: JSON.stringify({
    name: "Marketplace 70-30",
    type: "percentage",
    currency: "NGN",
    subaccounts: [
      { subaccount: "ACCT_6uujpqtzmnufzkw", share: 70 },
    ],
    bearer_type: "all-proportional",
    // Main account gets remaining 30%
  }),
});
// split.data.split_code → "SPL_RcScyW5jp2"
```

### Flat Split

```typescript
await paystackRequest("/split", {
  method: "POST",
  body: JSON.stringify({
    name: "Fixed Distribution",
    type: "flat",
    currency: "NGN",
    subaccounts: [
      { subaccount: "ACCT_6uujpqtzmnufzkw", share: 50000 },  // ₦500 flat
      { subaccount: "ACCT_eg4sob4590pq9vb", share: 30000 },  // ₦300 flat
    ],
    bearer_type: "account",
  }),
});
```

## List Splits

`GET /split`

| Param | Type | Required | Description |
| --- | --- | --- | --- |
| `name` | string | No | Filter by split name |
| `active` | boolean | No | Filter active/inactive |
| `sort_by` | string | No | Sort field (default: `createdAt`) |
| `perPage` | integer | No | Records per page (default: 50) |
| `page` | integer | No | Page number (default: 1) |
| `from` | datetime | No | Start date |
| `to` | datetime | No | End date |

```typescript
const splits = await paystackRequest("/split?active=true");
```

## Fetch Split

`GET /split/:id`

```typescript
const split = await paystackRequest(`/split/${splitId}`);
```

## Update Split

`PUT /split/:id`

| Param | Type | Required | Description |
| --- | --- | --- | --- |
| `name` | string | Yes | Updated split name |
| `active` | boolean | Yes | Enable or disable |
| `bearer_type` | string | No | Updated bearer type |
| `bearer_subaccount` | string | No | Updated bearer subaccount |

```typescript
await paystackRequest(`/split/${splitId}`, {
  method: "PUT",
  body: JSON.stringify({
    name: "Updated Marketplace Split",
    active: true,
    bearer_type: "all-proportional",
  }),
});
```

## Add/Update Subaccount in Split

`POST /split/:id/subaccount/add`

Add a new subaccount or update the share of an existing one.

| Param | Type | Required | Description |
| --- | --- | --- | --- |
| `subaccount` | string | Yes | Subaccount code |
| `share` | integer | Yes | Share amount (percentage or flat depending on split type) |

```typescript
await paystackRequest(`/split/${splitId}/subaccount/add`, {
  method: "POST",
  body: JSON.stringify({
    subaccount: "ACCT_eg4sob4590pq9vb",
    share: 20,
  }),
});
```

## Remove Subaccount from Split

`POST /split/:id/subaccount/remove`

```typescript
await paystackRequest(`/split/${splitId}/subaccount/remove`, {
  method: "POST",
  body: JSON.stringify({
    subaccount: "ACCT_eg4sob4590pq9vb",
  }),
});
```

## Using Splits in Transactions

Pass the `split_code` when initializing a transaction:

```typescript
await paystackRequest("/transaction/initialize", {
  method: "POST",
  body: JSON.stringify({
    email: "customer@email.com",
    amount: 500000,
    split_code: "SPL_RcScyW5jp2",
  }),
});
```
