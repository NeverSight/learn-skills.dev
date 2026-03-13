---
name: paystack-charges
description: >-
  Paystack Charge API — initiate direct charges via card, bank account, USSD, mobile
  money, QR, EFT, Capitec Pay, and bank transfer channels. Handle multi-step
  authentication with Submit PIN, Submit OTP, Submit Phone, Submit Birthday, and Submit
  Address endpoints. Check pending charge status. Use this skill whenever building a
  custom payment flow that needs direct channel control instead of the standard checkout,
  implementing bank debit or USSD payments, handling card PIN/OTP verification flows,
  processing mobile money payments in Ghana/Kenya, or checking the status of a pending
  charge. Also use when you see references to /charge, submit_pin, submit_otp, or
  send_birthday in Paystack code.
---

# Paystack Charges

The Charge API gives you direct control over which payment channel to use, bypassing the standard Paystack checkout. It supports card, bank, USSD, mobile money, QR, EFT, Capitec Pay, and bank transfers.

> Depends on: **paystack-setup** for the `paystackRequest` helper and environment config.

## Charge Flow

The Charge API follows a multi-step flow. After creating a charge, Paystack may request additional authentication:

```
Create Charge → Check status → If "send_pin"    → Submit PIN    → Check status
                              → If "send_otp"    → Submit OTP    → Check status
                              → If "send_phone"  → Submit Phone  → Check status
                              → If "send_birthday"→ Submit Birthday→ Check status
                              → If "send_address"→ Submit Address → Check status
                              → If "pending"     → Wait 10s      → Check Pending
                              → If "success"     → Done ✓
```

## Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/charge` | Create a charge |
| POST | `/charge/submit_pin` | Submit PIN for verification |
| POST | `/charge/submit_otp` | Submit OTP for verification |
| POST | `/charge/submit_phone` | Submit phone number |
| POST | `/charge/submit_birthday` | Submit birthday |
| POST | `/charge/submit_address` | Submit address (AVS) |
| GET | `/charge/:reference` | Check pending charge status |

## Create Charge

`POST /charge`

### Core Parameters (Body)

| Param | Type | Required | Description |
| --- | --- | --- | --- |
| `email` | string | Yes | Customer's email address |
| `amount` | string | Yes | Amount in subunits |
| `reference` | string | No | Unique transaction reference |
| `metadata` | object | No | Custom data for post-payment processing |

### Channel-Specific Parameters

Send ONE of these objects to select the payment channel:

#### Bank Account (Nigeria)

```typescript
const result = await paystackRequest("/charge", {
  method: "POST",
  body: JSON.stringify({
    email: "customer@email.com",
    amount: "10000",
    bank: {
      code: "057",           // Bank code (get from List Banks endpoint)
      account_number: "0000000000",
    },
    birthday: "1995-12-23",  // Required for some banks
  }),
});
```

#### Bank Account (Kuda Bank)

```typescript
{
  email: "customer@email.com",
  amount: "10000",
  bank: {
    code: "50211",
    account_number: "0000000000",
    phone: "08012345678",    // Required for Kuda
    token: "123456",         // 6-digit code from Kuda app
  }
}
```

#### USSD (Nigeria only)

```typescript
{
  email: "customer@email.com",
  amount: "10000",
  ussd: { type: "737" }     // 737 (GTBank) — currently only supported type
}
```

#### Mobile Money (Ghana, Kenya, Côte d'Ivoire)

```typescript
// MTN Ghana
{
  email: "customer@email.com",
  amount: "10000",
  mobile_money: {
    phone: "0551234987",
    provider: "mtn"          // mtn | atl | vod (Ghana), mpesa (Kenya), orange | wave (CIV)
  }
}

// M-Pesa Kenya (till number)
{
  email: "customer@email.com",
  amount: "10000",
  mobile_money: {
    account: "TILL_NUMBER",  // Use account instead of phone for M-Pesa till
    provider: "mptill"       // or "mpesa" for phone-based, "mpesa_offline"
  }
}
```

#### QR Code (South Africa)

```typescript
{
  email: "customer@email.com",
  amount: "10000",
  qr: { provider: "scan-to-pay" }
}
```

#### EFT (South Africa)

```typescript
{
  email: "customer@email.com",
  amount: "10000",
  eft: { provider: "ozow" }
}
```

#### Capitec Pay (South Africa)

```typescript
{
  email: "customer@email.com",
  amount: "10000",
  capitec_pay: {
    identifier_key: "CELLPHONE",    // CELLPHONE | IDNUMBER | ACCOUNTNUMBER
    identifier_value: "0712345678"
  }
}
```

#### Bank Transfer (Pay with Transfer)

```typescript
{
  email: "customer@email.com",
  amount: "10000",
  bank_transfer: {
    account_expires_at: "2024-12-31T23:59:59.000Z"  // Expiry for generated account
  }
}
```

#### Card (with authorization code)

```typescript
{
  email: "customer@email.com",
  amount: "10000",
  authorization_code: "AUTH_72btv547",  // From a previous successful charge
  pin: "1234"                           // Only for non-reusable auth codes
}
```

### Split Payment Parameters

| Param | Type | Description |
| --- | --- | --- |
| `split_code` | string | Split code e.g. `SPL_98WF13Eb3w` |
| `subaccount` | string | Subaccount code e.g. `ACCT_8f4s1eq7ml6rlzj` |
| `transaction_charge` | integer | Override split amount (subunits) |
| `bearer` | string | `"account"` or `"subaccount"` — who pays fees |

## Submit PIN

`POST /charge/submit_pin`

When `data.status === "send_pin"` in the charge response:

```typescript
const result = await paystackRequest("/charge/submit_pin", {
  method: "POST",
  body: JSON.stringify({
    pin: "1234",
    reference: "5bwib5v6anhe9xa",
  }),
});
```

## Submit OTP

`POST /charge/submit_otp`

When `data.status === "send_otp"`:

```typescript
const result = await paystackRequest("/charge/submit_otp", {
  method: "POST",
  body: JSON.stringify({
    otp: "123456",
    reference: "5bwib5v6anhe9xa",
  }),
});
```

## Submit Phone

`POST /charge/submit_phone`

When `data.status === "send_phone"`:

```typescript
const result = await paystackRequest("/charge/submit_phone", {
  method: "POST",
  body: JSON.stringify({
    phone: "08012345678",
    reference: "5bwib5v6anhe9xa",
  }),
});
```

## Submit Birthday

`POST /charge/submit_birthday`

When `data.status === "send_birthday"`:

```typescript
const result = await paystackRequest("/charge/submit_birthday", {
  method: "POST",
  body: JSON.stringify({
    birthday: "1995-12-23",
    reference: "5bwib5v6anhe9xa",
  }),
});
```

## Submit Address

`POST /charge/submit_address`

When `data.status === "send_address"` (AVS — Address Verification System):

```typescript
const result = await paystackRequest("/charge/submit_address", {
  method: "POST",
  body: JSON.stringify({
    reference: "7c7rpkqpc0tijs8",
    address: "140 N 2ND ST",
    city: "Stroudsburg",
    state: "PA",
    zipcode: "18360",
  }),
});
```

## Check Pending Charge

`GET /charge/:reference`

When status is `"pending"`, wait at least **10 seconds** before checking:

```typescript
const result = await paystackRequest<{
  status: string;
  reference: string;
  amount: number;
}>(`/charge/${encodeURIComponent(reference)}`);

// result.data.status: "success" | "failed" | "pending"
```

## Full Charge Flow Example

```typescript
async function processDirectCharge(chargeData: any) {
  let result = await paystackRequest<any>("/charge", {
    method: "POST",
    body: JSON.stringify(chargeData),
  });

  // Handle multi-step authentication
  while (result.data.status !== "success" && result.data.status !== "failed") {
    switch (result.data.status) {
      case "send_pin":
        const pin = await promptUserForPIN();
        result = await paystackRequest("/charge/submit_pin", {
          method: "POST",
          body: JSON.stringify({ pin, reference: result.data.reference }),
        });
        break;
      case "send_otp":
        const otp = await promptUserForOTP();
        result = await paystackRequest("/charge/submit_otp", {
          method: "POST",
          body: JSON.stringify({ otp, reference: result.data.reference }),
        });
        break;
      case "send_phone":
        const phone = await promptUserForPhone();
        result = await paystackRequest("/charge/submit_phone", {
          method: "POST",
          body: JSON.stringify({ phone, reference: result.data.reference }),
        });
        break;
      case "send_birthday":
        const birthday = await promptUserForBirthday();
        result = await paystackRequest("/charge/submit_birthday", {
          method: "POST",
          body: JSON.stringify({ birthday, reference: result.data.reference }),
        });
        break;
      case "send_address":
        const address = await promptUserForAddress();
        result = await paystackRequest("/charge/submit_address", {
          method: "POST",
          body: JSON.stringify({ ...address, reference: result.data.reference }),
        });
        break;
      case "pending":
        await new Promise((r) => setTimeout(r, 10000)); // Wait 10 seconds
        result = await paystackRequest(`/charge/${result.data.reference}`);
        break;
      default:
        throw new Error(`Unknown charge status: ${result.data.status}`);
    }
  }

  return result.data;
}
```

## Important Notes

- The Charge API is more complex than the standard checkout — only use it when you need direct control over payment channels
- Some bank charges require `birthday` as part of the initial request
- For `pending` status, wait at least 10 seconds before polling to avoid rate limiting
- Mobile money providers vary by country: `mtn`, `atl`, `vod` for Ghana; `mpesa` for Kenya; `orange`, `wave` for Côte d'Ivoire
- USSD currently only supports `737` (GTBank) in Nigeria
- PIN and OTP submissions must happen server-side — never collect or transmit these on the client
