---
name: webpay-api
description: Integrate the Transbank Webpay Plus payment gateway using its REST API (HTTP). Use this skill whenever the user needs to implement Webpay Plus payments, create payment transactions, confirm payments, refund/reverse transactions, check transaction status, or capture deferred payments via the Webpay Plus API. Also use this skill when the user mentions Transbank, Webpay, Chilean payment processing, payment integration for Chile, or needs test credentials for Webpay Plus integration environment.
---

# Webpay Plus - REST API Integration Skill

This skill provides everything needed to integrate the Transbank Webpay Plus payment gateway using its REST API (HTTP). It covers the complete purchase cycle: creating transactions, confirming payments, checking status, refunding/reversing, and deferred capture.

> This skill covers **Webpay Plus** only (single-store). It does NOT cover Webpay Plus Mall (multi-store) or Oneclick.

## Table of Contents

1. [Environments and Credentials](#environments-and-credentials)
2. [Payment Flow Overview](#payment-flow-overview)
3. [API Endpoints](#api-endpoints)
   - [Create Transaction](#1-create-transaction)
   - [Confirm Transaction (Commit)](#2-confirm-transaction-commit)
   - [Get Transaction Status](#3-get-transaction-status)
   - [Refund / Reverse Transaction](#4-refund--reverse-transaction)
   - [Capture Transaction (Deferred)](#5-capture-transaction-deferred)
4. [Reference Tables](#reference-tables)
5. [Error Codes](#error-codes)
6. [Going to Production](#going-to-production)

---

## Environments and Credentials

The Webpay REST API is secured via TLSv1.2 and authenticated using two HTTP headers on every request:

| Header | Description |
|---|---|
| `Tbk-Api-Key-Id` | Commerce code (codigo de comercio) |
| `Tbk-Api-Key-Secret` | Secret key (llave secreta) |

All requests must also include `Content-Type: application/json`.

### Environments

| Environment | Base URL |
|---|---|
| **Integration (testing)** | `https://webpay3gint.transbank.cl` |
| **Production** | `https://webpay3g.transbank.cl` |

### Integration Test Credentials

Use these credentials freely for testing in the integration environment:

```
Tbk-Api-Key-Id: 597055555532
Tbk-Api-Key-Secret: 579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C
```

### Test Cards for Integration

For testing in the integration environment, use the test cards documented at https://www.transbankdevelopers.cl/documentacion/como_empezar#ambientes

Common test data for a successful transaction:
- **Card number**: `4051 8856 0044 6623`
- **Expiration date**: Any future date
- **CVV**: `123`
- **RUT**: `11.111.111-1`
- **Password**: `123`

To simulate a **rejected** transaction, use RUT `11.111.111-1` with password `123` but reject the payment in the Webpay form.

### Commerce Codes for Integration

| Product | Commerce Code |
|---|---|
| Webpay Plus | `597055555532` |
| Webpay Plus (Deferred Capture) | `597055555540` |

---

## Payment Flow Overview

The Webpay Plus payment cycle follows this sequence:

```
1. MERCHANT SERVER                    2. WEBPAY (Transbank)
   |                                     |
   |-- POST /transactions -------------->|  (Create transaction)
   |<-- { token, url } ------------------|
   |                                     |
   |-- Redirect user to url + token ---->|  (User pays on Webpay form)
   |                                     |
   |<-- Redirect to return_url ----------|  (Webpay sends token_ws via POST)
   |                                     |
   |-- PUT /transactions/{token} ------->|  (Confirm / Commit transaction)
   |<-- { transaction result } ----------|
   |                                     |
   |-- Show result to user              |
```

### Step-by-step:

1. **Create transaction**: Your server calls `POST /rswebpaytransaction/api/webpay/v1.2/transactions` with the order details. You receive a `token` and a `url`.

2. **Redirect to Webpay**: Redirect the user's browser to the returned `url`, passing the `token` via a form POST field called `token_ws`:
   ```html
   <form method="POST" action="{url}">
     <input type="hidden" name="token_ws" value="{token}">
     <input type="submit" value="Pagar">
   </form>
   ```

3. **User pays**: The user enters their card details on Transbank's secure form and authorizes the payment.

4. **Webpay redirects back**: After authorization (or rejection/abort), Webpay redirects the user back to your `return_url` via POST, sending:
   - `token_ws`: The transaction token (if the user completed the flow)
   - `TBK_TOKEN` + `TBK_ORDEN_COMPRA` + `TBK_ID_SESION`: Only if the user **aborted** the payment

5. **Confirm transaction**: Your server calls `PUT /rswebpaytransaction/api/webpay/v1.2/transactions/{token}` to confirm and get the result.

6. **Show result**: Display the payment result to the user.

### Handling Aborted Payments

If the user clicks "Anular" (cancel) on the Webpay form, the redirect to `return_url` will include `TBK_TOKEN`, `TBK_ORDEN_COMPRA`, and `TBK_ID_SESION` instead of `token_ws`. In this case, the transaction was NOT completed. Do not call commit; inform the user that payment was cancelled.

### Timeout Behavior

If the user does not complete the payment within the allowed time, two requests arrive at `return_url`:
1. First with `TBK_TOKEN`, `TBK_ORDEN_COMPRA`, `TBK_ID_SESION` (and empty `token_ws`)
2. A second request with just `TBK_TOKEN` (a POST from the user's browser)

Both indicate the transaction was abandoned. Do not confirm the transaction.

---

## API Endpoints

All endpoint paths are relative to the base URL for the chosen environment.

**Base path**: `/rswebpaytransaction/api/webpay/v1.2`

### 1. Create Transaction

Initialize a Webpay Plus payment. Returns a token and URL for the payment form.

**Endpoint**: `POST /rswebpaytransaction/api/webpay/v1.2/transactions`

**Request Headers**:
```
Tbk-Api-Key-Id: 597055555532
Tbk-Api-Key-Secret: 579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C
Content-Type: application/json
```

**Request Body**:
```json
{
  "buy_order": "ordenCompra12345678",
  "session_id": "sesion1234557545",
  "amount": 10000,
  "return_url": "http://www.comercio.cl/webpay/retorno"
}
```

**Request Parameters**:

| Parameter | Type | Description |
|---|---|---|
| `buy_order` | String | Unique order ID for this transaction. Max length: 26. Allowed chars: letters, numbers, and `\|_=&%.,~:/?[+!@()>-` |
| `session_id` | String | Session identifier, for internal use by the merchant. Returned at the end of the transaction. Max length: 61 |
| `amount` | Decimal | Transaction amount. Integer for CLP, max 2 decimals for USD. Max length: 17 |
| `return_url` | String | URL where Webpay redirects after authorization. Max length: 256 |

**Response** (200 OK):
```json
{
  "token": "e9d555262db0f989e49d724b4db0b0af367cc415cde41f500a776550fc5fddd3",
  "url": "https://webpay3gint.transbank.cl/webpayserver/initTransaction"
}
```

**Response Fields**:

| Field | Type | Description |
|---|---|---|
| `token` | String | Transaction token. Length: 64 |
| `url` | String | Webpay payment form URL. Max length: 255 |

---

### 2. Confirm Transaction (Commit)

After the user completes payment on Webpay and is redirected to `return_url`, confirm the transaction. This is mandatory to finalize the payment.

**Endpoint**: `PUT /rswebpaytransaction/api/webpay/v1.2/transactions/{token}`

**Request Headers**:
```
Tbk-Api-Key-Id: 597055555532
Tbk-Api-Key-Secret: 579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C
Content-Type: application/json
```

**URL Parameters**:

| Parameter | Type | Description |
|---|---|---|
| `token` | String | Transaction token (in the URL path, not body). Length: 64 |

**No request body** is needed.

**Response** (200 OK):
```json
{
  "vci": "TSY",
  "amount": 10000,
  "status": "AUTHORIZED",
  "buy_order": "ordenCompra12345678",
  "session_id": "sesion1234557545",
  "card_detail": {
    "card_number": "6623"
  },
  "accounting_date": "0522",
  "transaction_date": "2019-05-22T16:41:21.063Z",
  "authorization_code": "1213",
  "payment_type_code": "VN",
  "response_code": 0,
  "installments_number": 0
}
```

**Response Fields**:

| Field | Type | Description |
|---|---|---|
| `vci` | String | Cardholder authentication result. See [VCI Codes](#vci-codes) |
| `amount` | Decimal | Transaction amount. Max length: 17 |
| `status` | String | Transaction status. See [Transaction Statuses](#transaction-statuses) |
| `buy_order` | String | Order ID sent in create. Max length: 26 |
| `session_id` | String | Session ID sent in create. Max length: 61 |
| `card_detail` | Object | Card details object |
| `card_detail.card_number` | String | Last 4 digits of the card. Max length: 19 |
| `accounting_date` | String | Authorization date. Length: 4, format: MMDD |
| `transaction_date` | String | Authorization date/time. ISO 8601 format |
| `authorization_code` | String | Authorization code. Max length: 6 |
| `payment_type_code` | String | Payment type. See [Payment Type Codes](#payment-type-codes) |
| `response_code` | Number | Authorization response code. 0 = approved |
| `installments_amount` | Number | Installment amount. Max length: 17 |
| `installments_number` | Number | Number of installments. Max length: 2 |
| `balance` | Number | Remaining balance for a nullified detail. Max length: 17 |

### Validating a Successful Transaction

After calling commit, verify the transaction was successful by checking:
1. `response_code` equals `0`
2. `status` equals `"AUTHORIZED"`

If `response_code` is not `0`, the transaction was rejected.

---

### 3. Get Transaction Status

Query the state of a transaction at any time. Useful for error recovery or verifying a transaction's current state.

**Endpoint**: `GET /rswebpaytransaction/api/webpay/v1.2/transactions/{token}`

**Request Headers**:
```
Tbk-Api-Key-Id: 597055555532
Tbk-Api-Key-Secret: 579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C
Content-Type: application/json
```

**URL Parameters**:

| Parameter | Type | Description |
|---|---|---|
| `token` | String | Transaction token (in URL, not body). Length: 64 |

**Response**: Same structure as Commit response (see above).

---

### 4. Refund / Reverse Transaction

Refund all or part of a completed transaction. If called within the same day as the original transaction, it may result in a **reversal** (REVERSED). If called on a different day, it becomes a **nullification** (NULLIFIED).

**Endpoint**: `POST /rswebpaytransaction/api/webpay/v1.2/transactions/{token}/refunds`

**Request Headers**:
```
Tbk-Api-Key-Id: 597055555532
Tbk-Api-Key-Secret: 579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C
Content-Type: application/json
```

**URL Parameters**:

| Parameter | Type | Description |
|---|---|---|
| `token` | String | Transaction token (in URL, not body). Length: 64 |

**Request Body**:
```json
{
  "amount": 1000
}
```

**Request Parameters**:

| Parameter | Type | Description |
|---|---|---|
| `amount` | Decimal | Amount to refund/reverse. Integer for CLP, max 2 decimals for USD. Max length: 17 |

**Response** (200 OK) - Nullification:
```json
{
  "type": "NULLIFIED",
  "authorization_code": "123456",
  "authorization_date": "2019-03-20T20:18:20Z",
  "nullified_amount": 1000.00,
  "balance": 0.00,
  "response_code": 0
}
```

**Response** (200 OK) - Reversal:
```json
{
  "type": "REVERSED"
}
```

**Response Fields**:

| Field | Type | Description |
|---|---|---|
| `type` | String | Refund type: `REVERSED` or `NULLIFIED`. Max length: 10 |
| `authorization_code` | String | (NULLIFIED only) Authorization code. Max length: 6 |
| `authorization_date` | String | (NULLIFIED only) Authorization date/time |
| `balance` | Decimal | (NULLIFIED only) Updated balance. Max length: 17 |
| `nullified_amount` | Decimal | (NULLIFIED only) Amount nullified. Max length: 17 |
| `response_code` | Number | (NULLIFIED only) Result code. 0 = success. Max: 2 |

**Refund Error Codes**:

| Code | Description |
|---|---|
| 304 | Null input field validation |
| 245 | Commerce code does not exist |
| 22 | Commerce is not active |
| 316 | Commerce does not match certificate |
| 308 | Operation not allowed |
| 274 | Transaction not found |
| 16 | Transaction does not allow nullification |
| 292 | Transaction is not authorized |
| 284 | Nullification period exceeded |
| 310 | Transaction already nullified |
| 311 | Amount exceeds available balance to nullify |
| 312 | Generic nullification error |
| 315 | Authorizer error |
| 53 | Transaction does not allow partial nullification with installments |

---

### 5. Capture Transaction (Deferred)

For merchants configured with deferred capture, this endpoint captures a previously authorized transaction. Requires a specific commerce code for deferred capture.

**Integration commerce code for deferred capture**: `597055555540`

**Endpoint**: `PUT /rswebpaytransaction/api/webpay/v1.2/transactions/{token}/capture`

**Request Headers**:
```
Tbk-Api-Key-Id: 597055555540
Tbk-Api-Key-Secret: 579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C
Content-Type: application/json
```

**URL Parameters**:

| Parameter | Type | Description |
|---|---|---|
| `token` | String | Transaction token (in URL, not body). Length: 64 |

**Request Body**:
```json
{
  "buy_order": "415034240",
  "authorization_code": "12345",
  "capture_amount": 1000
}
```

**Request Parameters**:

| Parameter | Type | Description |
|---|---|---|
| `buy_order` | String | Order ID of the transaction to capture. Max length: 26 |
| `authorization_code` | String | Authorization code from the original transaction. Max length: 6 |
| `capture_amount` | Decimal | Amount to capture. Max length: 17 |

**Response** (200 OK):
```json
{
  "token": "e074d38c628122c63e5c0986368ece22974d6fee1440617d85873b7b4efa48a3",
  "authorization_code": "123456",
  "authorization_date": "2019-03-20T20:18:20Z",
  "captured_amount": 1000,
  "response_code": 0
}
```

**Response Fields**:

| Field | Type | Description |
|---|---|---|
| `token` | String | Transaction token. Max length: 64 |
| `authorization_code` | String | Deferred capture authorization code. Max length: 6 |
| `authorization_date` | String | Authorization date/time |
| `captured_amount` | Decimal | Captured amount. Max length: 6 |
| `response_code` | Number | Result code. 0 = success. Max: 2 |

**Capture Error Codes**:

| Code | Description |
|---|---|
| 304 | Null input field validation |
| 245 | Commerce code does not exist |
| 22 | Commerce is not active |
| 316 | Commerce does not match certificate |
| 308 | Operation not allowed |
| 274 | Transaction not found |
| 16 | Transaction is not deferred capture |
| 292 | Transaction is not authorized |
| 284 | Capture period exceeded |
| 310 | Transaction previously reversed |
| 309 | Transaction previously captured |
| 311 | Capture amount exceeds authorized amount |
| 315 | Authorizer error |

---

## Reference Tables

### Transaction Statuses

| Status | Description |
|---|---|
| `INITIALIZED` | Transaction has been created, waiting for user to complete payment |
| `AUTHORIZED` | Transaction was authorized successfully |
| `REVERSED` | Transaction was reversed (same-day refund) |
| `FAILED` | Transaction was rejected or failed |
| `NULLIFIED` | Transaction was nullified (refund after accounting date) |
| `PARTIALLY_NULLIFIED` | Transaction was partially nullified |
| `CAPTURED` | Transaction was captured (deferred capture) |

### Payment Type Codes

| Code | Description |
|---|---|
| `VD` | Debit Sale (Venta Debito) |
| `VN` | Normal Sale - Credit (Venta Normal) |
| `VC` | Installment Sale (Venta en Cuotas) |
| `SI` | 3 interest-free installments (3 Cuotas sin Interes) |
| `S2` | 2 interest-free installments (2 Cuotas sin Interes) |
| `NC` | N interest-free installments (N Cuotas sin Interes) |
| `VP` | Prepaid Sale (Venta Prepago) |

### VCI Codes

The `vci` field indicates cardholder authentication results. This is supplementary information to `response_code`. Merchants should NOT validate this field as new codes are constantly added.

**Domestic transactions**:

| Code | Description |
|---|---|
| `TSY` | Authentication successful |
| `TSN` | Authentication rejected |
| `NP` | Non-participating, no authentication |
| `U3` | Connection failure, authentication rejected |
| `INV` | Invalid data |
| `A` | Attempted |
| `CNP1` | Commerce does not participate |
| `EOP` | Operational error |
| `BNA` | BIN not enrolled |
| `ENA` | Issuer not enrolled |

**Foreign sale codes**:

| Code | Description |
|---|---|
| `TSYS` | Successful frictionless authentication |
| `TSAS` | Attempt, card not enrolled / issuer unavailable |
| `TSNS` | Failed, not authenticated, denied |
| `TSRS` | Authentication rejected, frictionless |
| `TSUS` | Authentication failed due to technical issue |
| `TSCF` | Challenge authentication (not accepted by commerce) |
| `TSYF` | Successful challenge authentication |
| `TSNF` | Not authenticated, denied with challenge |
| `TSUF` | Challenge authentication failed due to technical issue |
| `NPC` | Commerce does not participate |
| `NPB` | BIN does not participate |
| `NPCB` | Commerce and BIN do not participate |
| `SPCB` | Commerce and BIN participate, authorization incomplete |

---

## Error Codes

### HTTP Status Codes

| HTTP Code | Description |
|---|---|
| 200 | Operation executed successfully |
| 204 | DELETE operation executed successfully |
| 400 | Invalid JSON message (malformed or unexpected field) |
| 401 | Unauthorized. Invalid API Key and/or API Secret |
| 404 | Transaction not found |
| 405 | Method not allowed |
| 406 | Cannot process response in requested format |
| 415 | Message type not allowed |
| 422 | Request cannot be processed (data validation or business logic) |
| 500 | Unexpected error |

All errors return a JSON body:
```json
{
  "error_message": "token is required"
}
```

---

## Going to Production

To move from integration to production:

1. Complete the certification process with Transbank
2. Obtain your production commerce code and API secret
3. Change the base URL from `https://webpay3gint.transbank.cl` to `https://webpay3g.transbank.cl`
4. Replace the integration credentials with your production credentials

More details at https://www.transbankdevelopers.cl/documentacion/como_empezar#puesta-en-produccion

---

## Implementation Examples

### Node.js / Express Backend Example

```javascript
const express = require('express');
const axios = require('axios');

const app = express();
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Configuration
const WEBPAY_BASE_URL = 'https://webpay3gint.transbank.cl'; // Use production URL for prod
const API_KEY_ID = '597055555532';
const API_KEY_SECRET = '579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C';

const headers = {
  'Tbk-Api-Key-Id': API_KEY_ID,
  'Tbk-Api-Key-Secret': API_KEY_SECRET,
  'Content-Type': 'application/json'
};

// Step 1: Create transaction
app.post('/api/webpay/create', async (req, res) => {
  try {
    const { buy_order, session_id, amount, return_url } = req.body;

    const response = await axios.post(
      `${WEBPAY_BASE_URL}/rswebpaytransaction/api/webpay/v1.2/transactions`,
      { buy_order, session_id, amount, return_url },
      { headers }
    );

    // Return token and url to frontend
    res.json(response.data);
  } catch (error) {
    res.status(error.response?.status || 500).json({
      error: error.response?.data || 'Error creating transaction'
    });
  }
});

// Step 2: Confirm transaction (return_url handler)
app.post('/api/webpay/confirm', async (req, res) => {
  try {
    const token_ws = req.body.token_ws;

    // Check if payment was aborted
    if (!token_ws || req.body.TBK_TOKEN) {
      return res.redirect('/payment-cancelled');
    }

    const response = await axios.put(
      `${WEBPAY_BASE_URL}/rswebpaytransaction/api/webpay/v1.2/transactions/${token_ws}`,
      null,
      { headers }
    );

    const result = response.data;

    // Validate successful transaction
    if (result.response_code === 0 && result.status === 'AUTHORIZED') {
      // Payment successful - update your database
      res.redirect(`/payment-success?order=${result.buy_order}`);
    } else {
      // Payment rejected
      res.redirect(`/payment-rejected?order=${result.buy_order}`);
    }
  } catch (error) {
    res.redirect('/payment-error');
  }
});

// Check transaction status
app.get('/api/webpay/status/:token', async (req, res) => {
  try {
    const response = await axios.get(
      `${WEBPAY_BASE_URL}/rswebpaytransaction/api/webpay/v1.2/transactions/${req.params.token}`,
      { headers }
    );
    res.json(response.data);
  } catch (error) {
    res.status(error.response?.status || 500).json({
      error: error.response?.data || 'Error checking status'
    });
  }
});

// Refund transaction
app.post('/api/webpay/refund', async (req, res) => {
  try {
    const { token, amount } = req.body;

    const response = await axios.post(
      `${WEBPAY_BASE_URL}/rswebpaytransaction/api/webpay/v1.2/transactions/${token}/refunds`,
      { amount },
      { headers }
    );
    res.json(response.data);
  } catch (error) {
    res.status(error.response?.status || 500).json({
      error: error.response?.data || 'Error refunding transaction'
    });
  }
});
```

### Frontend Redirect Example

```html
<!-- After receiving token and url from your backend -->
<form id="webpay-form" method="POST" action="">
  <input type="hidden" name="token_ws" id="token_ws">
  <button type="submit">Pagar con Webpay</button>
</form>

<script>
async function initiatePayment(orderData) {
  const response = await fetch('/api/webpay/create', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      buy_order: orderData.orderId,
      session_id: orderData.sessionId,
      amount: orderData.amount,
      return_url: window.location.origin + '/api/webpay/confirm'
    })
  });

  const { token, url } = await response.json();

  // Redirect to Webpay payment form
  const form = document.getElementById('webpay-form');
  form.action = url;
  document.getElementById('token_ws').value = token;
  form.submit();
}
</script>
```

### cURL Examples

**Create transaction**:
```bash
curl -X POST "https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.2/transactions" \
  -H "Tbk-Api-Key-Id: 597055555532" \
  -H "Tbk-Api-Key-Secret: 579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C" \
  -H "Content-Type: application/json" \
  -d '{
    "buy_order": "order123",
    "session_id": "session456",
    "amount": 10000,
    "return_url": "http://localhost:3000/webpay/confirm"
  }'
```

**Confirm transaction**:
```bash
curl -X PUT "https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.2/transactions/{token}" \
  -H "Tbk-Api-Key-Id: 597055555532" \
  -H "Tbk-Api-Key-Secret: 579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C" \
  -H "Content-Type: application/json"
```

**Get transaction status**:
```bash
curl -X GET "https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.2/transactions/{token}" \
  -H "Tbk-Api-Key-Id: 597055555532" \
  -H "Tbk-Api-Key-Secret: 579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C" \
  -H "Content-Type: application/json"
```

**Refund**:
```bash
curl -X POST "https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.2/transactions/{token}/refunds" \
  -H "Tbk-Api-Key-Id: 597055555532" \
  -H "Tbk-Api-Key-Secret: 579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C" \
  -H "Content-Type: application/json" \
  -d '{"amount": 5000}'
```

**Capture (deferred)**:
```bash
curl -X PUT "https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.2/transactions/{token}/capture" \
  -H "Tbk-Api-Key-Id: 597055555540" \
  -H "Tbk-Api-Key-Secret: 579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C" \
  -H "Content-Type: application/json" \
  -d '{
    "buy_order": "order123",
    "authorization_code": "123456",
    "capture_amount": 10000
  }'
```

---

## Important Implementation Notes

1. **The `buy_order` must be unique** for each transaction. It cannot be reused.

2. **Always confirm (commit) the transaction** after receiving the redirect. If you don't call commit, the transaction remains in `INITIALIZED` state and the payment will not be processed.

3. **Commit has a time limit**: You must confirm the transaction within a few seconds after the user is redirected back. If too much time passes, the transaction may expire.

4. **Handle all redirect scenarios** at your `return_url`:
   - `token_ws` present: Normal flow, proceed to commit
   - `TBK_TOKEN` present (no `token_ws`): User aborted
   - Both present with empty `token_ws`: Timeout

5. **Refund vs Reversal**: The API automatically determines whether to reverse (same day, before accounting cutoff) or nullify (after accounting cutoff). You always call the same endpoint.

6. **Partial refunds** are supported: You can refund any amount up to the original transaction amount. Multiple partial refunds are allowed until the balance reaches zero.

7. **Deferred capture** requires a special commerce code and configuration with Transbank. Not all merchants have this feature enabled.

8. **The `vci` field** should NOT be used for business logic validation. Use `response_code` instead. The `vci` field is informational only and new values are added without documentation updates.

9. **The `response_code`** is the definitive indicator of whether a transaction was approved (0) or rejected (non-zero).
