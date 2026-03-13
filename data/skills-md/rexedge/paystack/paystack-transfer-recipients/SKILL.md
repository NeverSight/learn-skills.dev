---
name: paystack-transfer-recipients
description: >-
  Paystack Transfer Recipients API — create, list, fetch, update, and delete transfer
  recipients (beneficiaries) for payouts. Supports NUBAN (Nigeria), GHIPSS (Ghana),
  Mobile Money, BASA (South Africa), and authorization-based recipients. Use this skill
  whenever adding bank accounts or mobile wallets as payout destinations, creating
  transfer recipients before initiating transfers, managing beneficiary lists, or doing
  bulk recipient creation. Also use when you see references to recipient_code,
  RCP_ prefixed codes, or the /transferrecipient endpoint.
---

# Paystack Transfer Recipients

The Transfer Recipients API lets you create and manage beneficiaries that receive money via transfers. You must create a recipient before initiating a transfer.

> Depends on: **paystack-setup** for the `paystackRequest` helper.  
> Related: **paystack-transfers** for sending money to recipients.

## Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/transferrecipient` | Create a recipient |
| POST | `/transferrecipient/bulk` | Bulk create recipients |
| GET | `/transferrecipient` | List recipients |
| GET | `/transferrecipient/:id_or_code` | Fetch a recipient |
| PUT | `/transferrecipient/:id_or_code` | Update a recipient |
| DELETE | `/transferrecipient/:id_or_code` | Delete (deactivate) a recipient |

## Recipient Types

| Type | Description | Countries |
| --- | --- | --- |
| `nuban` | Nigerian bank accounts (NUBAN) | Nigeria |
| `ghipss` | Ghana Interbank Payment & Settlement | Ghana |
| `mobile_money` | Mobile money wallets | Ghana, Kenya |
| `basa` | South African bank accounts | South Africa |
| `authorization` | Use a previous charge authorization | All |

## Create Transfer Recipient

`POST /transferrecipient`

A duplicate account number returns the existing record instead of creating a new one.

| Param | Type | Required | Description |
| --- | --- | --- | --- |
| `type` | string | Yes | `nuban`, `ghipss`, `mobile_money`, or `basa` |
| `name` | string | Yes | Recipient name (as registered on their account) |
| `account_number` | string | Yes* | Bank account / mobile number (* Not required for `authorization` type) |
| `bank_code` | string | Yes* | Bank code from List Banks endpoint (* Not required for `authorization` type) |
| `description` | string | No | Description for this recipient |
| `currency` | string | No | Currency code (e.g. `NGN`, `GHS`, `ZAR`) |
| `authorization_code` | string | No | Auth code from a previous transaction |
| `metadata` | object | No | Additional structured data |

### Nigerian Bank Account (NUBAN)

```typescript
const recipient = await paystackRequest<{
  recipient_code: string;
  name: string;
  type: string;
}>("/transferrecipient", {
  method: "POST",
  body: JSON.stringify({
    type: "nuban",
    name: "Tolu Robert",
    account_number: "0123456789",
    bank_code: "058",    // GTBank — get codes from List Banks endpoint
    currency: "NGN",
  }),
});
// recipient.data.recipient_code → "RCP_m7ljkv8leesep7p"
```

### Ghana Bank Account (GHIPSS)

```typescript
await paystackRequest("/transferrecipient", {
  method: "POST",
  body: JSON.stringify({
    type: "ghipss",
    name: "Kwame Asante",
    account_number: "0551234987",
    bank_code: "GH010100",
    currency: "GHS",
  }),
});
```

### Mobile Money

```typescript
await paystackRequest("/transferrecipient", {
  method: "POST",
  body: JSON.stringify({
    type: "mobile_money",
    name: "Ama Serwah",
    account_number: "0551234987",
    bank_code: "MTN",      // Mobile money provider code
    currency: "GHS",
  }),
});
```

### Authorization-Based

```typescript
await paystackRequest("/transferrecipient", {
  method: "POST",
  body: JSON.stringify({
    type: "authorization",
    name: "Customer Refund",
    authorization_code: "AUTH_ekk8t49ogj",
  }),
});
```

## Bulk Create Transfer Recipients

`POST /transferrecipient/bulk`

| Param | Type | Required | Description |
| --- | --- | --- | --- |
| `batch` | array | Yes | Array of recipient objects (same params as Create) |

```typescript
const result = await paystackRequest("/transferrecipient/bulk", {
  method: "POST",
  body: JSON.stringify({
    batch: [
      {
        type: "nuban",
        name: "Habenero Mundane",
        account_number: "0123456789",
        bank_code: "033",
        currency: "NGN",
      },
      {
        type: "nuban",
        name: "Soft Merry",
        account_number: "9876543210",
        bank_code: "50211",
        currency: "NGN",
      },
    ],
  }),
});
// result.data.success[] — successfully created recipients
// result.data.errors[] — failed recipients
```

## List Transfer Recipients

`GET /transferrecipient`

| Param | Type | Required | Description |
| --- | --- | --- | --- |
| `perPage` | integer | No | Records per page (default: 50) |
| `page` | integer | No | Page number (default: 1) |
| `from` | datetime | No | Start date |
| `to` | datetime | No | End date |

```typescript
const recipients = await paystackRequest("/transferrecipient?perPage=20&page=1");
```

## Fetch Transfer Recipient

`GET /transferrecipient/:id_or_code`

```typescript
const recipient = await paystackRequest(
  `/transferrecipient/${encodeURIComponent("RCP_m7ljkv8leesep7p")}`
);
```

## Update Transfer Recipient

`PUT /transferrecipient/:id_or_code`

| Param | Type | Required | Description |
| --- | --- | --- | --- |
| `name` | string | Yes | Updated recipient name |
| `email` | string | No | Updated recipient email |

```typescript
await paystackRequest(
  `/transferrecipient/${encodeURIComponent("RCP_m7ljkv8leesep7p")}`,
  {
    method: "PUT",
    body: JSON.stringify({ name: "Rick Sanchez" }),
  }
);
```

## Delete Transfer Recipient

`DELETE /transferrecipient/:id_or_code`

Sets the recipient to inactive (soft delete).

```typescript
await paystackRequest(
  `/transferrecipient/${encodeURIComponent("RCP_m7ljkv8leesep7p")}`,
  { method: "DELETE" }
);
```
