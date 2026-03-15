---
name: paystack-customers
description: >-
  Paystack Customers API — create, list, fetch, update, validate identity, whitelist/blacklist,
  manage authorizations, and direct debit operations. Use this skill whenever creating or
  managing customer records on Paystack, validating customer identity with BVN or bank account,
  whitelisting or blacklisting customers by risk action, deactivating saved card authorizations,
  setting up direct debit mandates, or building customer management dashboards. Also use when
  you see references to customer_code, CUS_ prefixed codes, risk_action, or
  /customer/authorization endpoints.
---

# Paystack Customers

The Customers API lets you create and manage customer records on your integration. Customers are automatically created on first charge, but you can also create them explicitly.

> Depends on: **paystack-setup** for the `paystackRequest` helper and environment config.

## Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/customer` | Create a customer |
| GET | `/customer` | List customers |
| GET | `/customer/:email_or_code` | Fetch a customer |
| PUT | `/customer/:code` | Update a customer |
| POST | `/customer/:code/identification` | Validate customer identity |
| POST | `/customer/set_risk_action` | Whitelist/Blacklist a customer |
| POST | `/customer/authorization/initialize` | Initialize authorization |
| GET | `/customer/authorization/verify/:reference` | Verify authorization |
| POST | `/customer/:id/initialize-direct-debit` | Initialize direct debit |
| PUT | `/customer/:id/directdebit-activation-charge` | Activate direct debit |
| GET | `/customer/:id/directdebit-mandate-authorizations` | Fetch mandate authorizations |
| POST | `/customer/authorization/deactivate` | Deactivate an authorization |

## Create Customer

`POST /customer`

| Param | Type | Required | Description |
| --- | --- | --- | --- |
| `email` | string | Yes | Customer's email address |
| `first_name` | string | No | Customer's first name |
| `last_name` | string | No | Customer's last name |
| `phone` | string | No | Customer's phone number |
| `metadata` | object | No | Key/value pairs for additional info |

> **Note:** `first_name`, `last_name`, and `phone` become **required** when assigning a Dedicated Virtual Account to customers in Betting, Financial Services, or General Service business categories.

```typescript
const customer = await paystackRequest<{
  email: string;
  customer_code: string;
  id: number;
}>("/customer", {
  method: "POST",
  body: JSON.stringify({
    email: "customer@example.com",
    first_name: "Zero",
    last_name: "Sum",
    phone: "+2348123456789",
  }),
});
// customer.data.customer_code → "CUS_xnxdt6s1zg1f4nx"
```

## List Customers

`GET /customer`

| Param | Type | Required | Description |
| --- | --- | --- | --- |
| `perPage` | integer | No | Records per page (default: 50) |
| `page` | integer | No | Page number (default: 1) |
| `from` | datetime | No | Start date e.g. `2016-09-24T00:00:05.000Z` |
| `to` | datetime | No | End date |

```typescript
const customers = await paystackRequest("/customer?perPage=20&page=1");
```

## Fetch Customer

`GET /customer/:email_or_code`

Returns full customer details including `transactions`, `subscriptions`, and `authorizations` arrays.

```typescript
const customer = await paystackRequest(
  `/customer/${encodeURIComponent("CUS_xnxdt6s1zg1f4nx")}`
);
// Includes: customer.data.authorizations[].authorization_code
```

## Update Customer

`PUT /customer/:code`

```typescript
await paystackRequest(`/customer/${encodeURIComponent("CUS_xnxdt6s1zg1f4nx")}`, {
  method: "PUT",
  body: JSON.stringify({
    first_name: "BoJack",
    last_name: "Horseman",
  }),
});
```

## Validate Customer Identity

`POST /customer/:code/identification`

Validates a customer's identity via bank account verification. Returns `202 Accepted` — validation happens asynchronously. Listen for `customeridentification.success` or `customeridentification.failed` webhooks.

| Param | Type | Required | Description |
| --- | --- | --- | --- |
| `country` | string | Yes | 2-letter country code (e.g. `NG`) |
| `type` | string | Yes | `bank_account` (only supported type) |
| `account_number` | string | Yes | Customer's bank account number |
| `bvn` | string | Yes | Bank Verification Number |
| `bank_code` | string | Yes | Bank code (from List Banks endpoint) |
| `first_name` | string | Yes | Customer's first name |
| `last_name` | string | Yes | Customer's last name |
| `middle_name` | string | No | Customer's middle name |

```typescript
await paystackRequest(
  `/customer/${encodeURIComponent("CUS_xnxdt6s1zg1f4nx")}/identification`,
  {
    method: "POST",
    body: JSON.stringify({
      country: "NG",
      type: "bank_account",
      account_number: "0123456789",
      bvn: "20012345677",
      bank_code: "007",
      first_name: "Asta",
      last_name: "Lavista",
    }),
  }
);
// Returns: { status: true, message: "Customer Identification in progress" }
```

## Whitelist / Blacklist Customer

`POST /customer/set_risk_action`

| Param | Type | Required | Description |
| --- | --- | --- | --- |
| `customer` | string | Yes | Customer code or email |
| `risk_action` | string | No | `default`, `allow` (whitelist), or `deny` (blacklist) |

```typescript
await paystackRequest("/customer/set_risk_action", {
  method: "POST",
  body: JSON.stringify({
    customer: "CUS_xr58yrr2ujlft9k",
    risk_action: "deny", // Blacklist this customer
  }),
});
```

## Initialize Authorization

`POST /customer/authorization/initialize`

Create a reusable authorization code for recurring direct debit transactions.

| Param | Type | Required | Description |
| --- | --- | --- | --- |
| `email` | string | Yes | Customer's email |
| `channel` | string | Yes | `direct_debit` (only supported option) |
| `callback_url` | string | No | URL to redirect customer after authorization |
| `account` | object | No | `{ number, bank_code }` for bank account details |
| `address` | object | No | `{ street, city, state }` for customer address |

```typescript
const auth = await paystackRequest<{
  redirect_url: string;
  access_code: string;
  reference: string;
}>("/customer/authorization/initialize", {
  method: "POST",
  body: JSON.stringify({
    email: "customer@email.com",
    channel: "direct_debit",
    callback_url: "https://example.com/callback",
  }),
});
// Redirect customer to auth.data.redirect_url
```

## Verify Authorization

`GET /customer/authorization/verify/:reference`

```typescript
const result = await paystackRequest(
  `/customer/authorization/verify/${encodeURIComponent(reference)}`
);
// result.data.authorization_code, result.data.active
```

## Initialize Direct Debit

`POST /customer/:id/initialize-direct-debit`

Link a bank account to a customer for direct debit transactions.

```typescript
const result = await paystackRequest(
  `/customer/${customerId}/initialize-direct-debit`,
  {
    method: "POST",
    body: JSON.stringify({
      account: { number: "0123456789", bank_code: "058" },
      address: { street: "Some Where", city: "Ikeja", state: "Lagos" },
    }),
  }
);
// Redirect customer to result.data.redirect_url
```

## Direct Debit Activation Charge

`PUT /customer/:id/directdebit-activation-charge`

Trigger an activation charge on an inactive mandate.

```typescript
await paystackRequest(`/customer/${customerId}/directdebit-activation-charge`, {
  method: "PUT",
  body: JSON.stringify({ authorization_id: 1069309917 }),
});
```

## Fetch Mandate Authorizations

`GET /customer/:id/directdebit-mandate-authorizations`

```typescript
const mandates = await paystackRequest(
  `/customer/${customerId}/directdebit-mandate-authorizations`
);
// mandates.data[].status, mandates.data[].authorization_code
```

## Deactivate Authorization

`POST /customer/authorization/deactivate`

Permanently deactivate a saved card/authorization so it can no longer be used for charges.

```typescript
await paystackRequest("/customer/authorization/deactivate", {
  method: "POST",
  body: JSON.stringify({
    authorization_code: "AUTH_xxxIjkZVj5",
  }),
});
```
