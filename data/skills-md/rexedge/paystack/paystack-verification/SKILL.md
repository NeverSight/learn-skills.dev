---
name: paystack-verification
description: >-
  Paystack Verification API — KYC verification tools for resolving bank accounts,
  validating account ownership, and looking up card BIN information. Use this skill
  whenever verifying bank account details before transfers, confirming account holder
  names, validating customer identity for compliance, looking up card brand/type/bank
  from BIN, or implementing KYC flows. Also use when you see references to /bank/resolve,
  /bank/validate, /decision/bin endpoints, or need to match account numbers to names.
---

# Paystack Verification

The Verification API provides KYC tools for account resolution, validation, and card BIN lookups.

> Depends on: **paystack-setup** for the `paystackRequest` helper.  
> Related: **paystack-miscellaneous** for fetching bank codes.

## Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/bank/resolve` | Resolve account number to name |
| POST | `/bank/validate` | Validate account ownership |
| GET | `/decision/bin/:bin` | Resolve card BIN |

## Resolve Account Number

Confirm an account belongs to the right customer. Returns the account holder's name.

| Param | Type | Required | Description |
| --- | --- | --- | --- |
| `account_number` | string | Yes | Bank account number |
| `bank_code` | string | Yes | Bank code (from List Banks endpoint) |

```typescript
const resolved = await paystackRequest<{
  account_number: string;
  account_name: string;
}>("/bank/resolve?account_number=0022728151&bank_code=063");
// resolved.data.account_name → "WES GIBBONS"
```

### Verify Before Transfer Pattern

```typescript
async function verifyAccountBeforeTransfer(
  accountNumber: string,
  bankCode: string,
  expectedName: string
) {
  const resolved = await paystackRequest<{
    account_number: string;
    account_name: string;
  }>(`/bank/resolve?account_number=${accountNumber}&bank_code=${bankCode}`);

  const resolvedName = resolved.data.account_name.toLowerCase();
  const expected = expectedName.toLowerCase();

  if (!resolvedName.includes(expected)) {
    throw new Error(
      `Account name mismatch: "${resolved.data.account_name}" does not match "${expectedName}"`
    );
  }

  return resolved.data;
}
```

## Validate Account

Full account validation with identity document verification. Use before sending money.

| Param | Type | Required | Description |
| --- | --- | --- | --- |
| `account_name` | string | Yes | Customer's first and last name |
| `account_number` | string | Yes | Account number |
| `account_type` | string | Yes | `personal` or `business` |
| `bank_code` | string | Yes | Bank code |
| `country_code` | string | Yes | Two-letter ISO code (e.g. `NG`, `ZA`, `GH`) |
| `document_type` | string | Yes | `identityNumber`, `passportNumber`, or `businessRegistrationNumber` |
| `document_number` | string | No | Identity document number |

```typescript
const validation = await paystackRequest<{
  verified: boolean;
  verificationMessage: string;
  accountAcceptsDebits: boolean;
  accountAcceptsCredits: boolean;
  accountHolderMatch: boolean;
  accountOpen: boolean;
}>("/bank/validate", {
  method: "POST",
  body: JSON.stringify({
    bank_code: "632005",
    country_code: "ZA",
    account_number: "0123456789",
    account_name: "Ann Bron",
    account_type: "personal",
    document_type: "identityNumber",
    document_number: "1234567890123",
  }),
});
// validation.data.verified → true
// validation.data.verificationMessage → "Account is verified successfully"
```

## Resolve Card BIN

Get card brand, type, and issuing bank from the first 6 digits of a card number:

```typescript
const card = await paystackRequest<{
  bin: string;
  brand: string;
  sub_brand: string;
  country_code: string;
  country_name: string;
  card_type: string; // "DEBIT" | "CREDIT"
  bank: string;
}>("/decision/bin/539983");
// card.data.brand → "Mastercard"
// card.data.card_type → "DEBIT"
// card.data.bank → "Guaranty Trust Bank"
```
