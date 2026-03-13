---
name: mom-factura-webhooks
description: Implement webhook-based payment confirmation for Mom Factura API. Webhooks work for both Bank Reference and E-kwanza, sending two sequential events (payment.confirmed + invoice.created). Use when building payment confirmation flows, receiving webhook notifications, or handling order state transitions from OPEN to PAID. Status polling endpoints available as fallback.
license: MIT
metadata:
  author: mom-factura
  version: "3.0"
  language: pt
---

# Mom Factura Webhooks & Status

Receive payment confirmations for deferred payments (Bank Reference and E-kwanza) via webhook with two sequential events. Status polling endpoints available as fallback.

**Base URL:** `https://api.momenu.online`
**Auth:** `x-api-key` header required on all requests.

## How It Works

1. Login at [momenu.toquemedia.net](https://momenu.toquemedia.net)
2. Go to the **Desenvolvedores** menu
3. Add your webhook URL
4. Save the configuration

When a payment is confirmed, the API sends **two sequential webhook events** to your URL:

1. **`payment.confirmed`** — Sent immediately after the order status is updated to PAID (before invoice generation). Use this to update the order state in your system.
2. **`invoice.created`** — Sent after the invoice PDF is generated and uploaded. Includes the `invoiceUrl` field with the download link.

Non-paid events (cancelled, failed, error) are sent as a single event without the `event` field, maintaining backward compatibility.

## Webhook Payloads

### Event 1: payment.confirmed

```json
{
  "event": "payment.confirmed",
  "merchantTransactionId": "abc123...",
  "ekwanzaTransactionId": "EKZ456...",
  "operationStatus": "1",
  "operationData": { ... }
}
```

### Event 2: invoice.created

```json
{
  "event": "invoice.created",
  "merchantTransactionId": "abc123...",
  "ekwanzaTransactionId": "EKZ456...",
  "operationStatus": "1",
  "operationData": { ... },
  "invoiceUrl": "https://invoice-momenu.toquemedia.net/invoices/..."
}
```

### Non-paid events (no `event` field)

```json
{
  "merchantTransactionId": "abc123...",
  "ekwanzaTransactionId": "EKZ456...",
  "operationStatus": "3",
  "operationData": { ... }
}
```

**operationStatus values:** `"1"` Paid · `"3"` Cancelled/Expired · `"4"` Failed/Refused · `"5"` Error

## Webhook Server Example - Node.js / Express

```javascript
const express = require("express");
const app = express();

app.use(express.json());

app.post("/webhook/meu-webhook", (req, res) => {
  const { event, merchantTransactionId, operationStatus, invoiceUrl } = req.body;

  switch (event) {
    case "payment.confirmed":
      console.log("Payment confirmed:", merchantTransactionId);
      // Update order state in your system
      break;

    case "invoice.created":
      console.log("Invoice ready:", invoiceUrl);
      // Save invoice URL, send to customer
      break;

    default:
      // Events without "event" field (cancelled, failed, error)
      if (["3", "4", "5"].includes(operationStatus)) {
        console.log("Payment failed:", operationStatus);
      }
  }

  res.status(200).json({ received: true });
});

app.listen(3000);
```

## Webhook Server Example - Python / Flask

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/webhook/meu-webhook", methods=["POST"])
def momenu_webhook():
    data = request.json
    event = data.get("event")
    transaction_id = data.get("merchantTransactionId")
    status = data.get("operationStatus")

    if event == "payment.confirmed":
        print(f"Payment confirmed: {transaction_id}")
        # Update order state

    elif event == "invoice.created":
        invoice_url = data.get("invoiceUrl")
        print(f"Invoice ready: {invoice_url}")
        # Save invoice URL

    elif status in ["3", "4", "5"]:
        print(f"Payment failed: {status}")

    return jsonify({"received": True}), 200
```

## Fallback: Status Polling

If webhook delivery fails, use status endpoints as fallback:

**E-kwanza:** GET `/api/payment/ekwanza/status/:code`
**Reference:** GET `/api/payment/reference/status/:operationId`

When paid, both return `invoiceUrl`.

```javascript
async function checkEkwanzaStatus(code) {
  const response = await fetch(
    `https://api.momenu.online/api/payment/ekwanza/status/${code}`,
    { headers: { "x-api-key": "YOUR_API_KEY" } }
  );

  const data = await response.json();

  if (data.status === "paid") {
    console.log("Paid! Invoice:", data.invoiceUrl);
  }

  return data;
}
```

## Notes

- Webhook works for both Bank Reference and E-kwanza
- Webhook delivery is fire-and-forget (no retries) — implement status endpoints as fallback
- Your webhook endpoint must return HTTP 2xx to acknowledge receipt
- MCX payments are immediate and do not use webhooks or polling
- Rate limiting: 100 req/min general, minimum 5s interval for E-kwanza polling, 30s for Reference polling
