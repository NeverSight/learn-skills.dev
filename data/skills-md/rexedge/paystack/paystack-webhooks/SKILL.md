---
name: paystack-webhooks
description: >-
  Paystack webhook integration — signature validation with HMAC SHA512, event parsing,
  IP whitelisting, retry policy, and all supported event types. Use this skill whenever
  setting up a webhook endpoint for Paystack, validating x-paystack-signature headers,
  handling charge.success or transfer.success events, debugging webhook delivery
  failures, implementing idempotent event processing, or building any server-side
  Paystack event listener. Also use when encountering webhook timeout issues or needing
  the list of Paystack webhook IP addresses.
---

# Paystack Webhooks

Webhooks let Paystack push real-time event notifications to your server. They are the recommended way to confirm payment status — more reliable than client-side callbacks or polling.

> Depends on: **paystack-setup** for environment configuration.

## How Webhooks Work

```
Customer pays → Paystack processes → Paystack POSTs event JSON to your webhook URL
                                   → Your server validates signature
                                   → Returns 200 OK immediately
                                   → Then processes the event asynchronously
```

## Endpoints

Your webhook URL is a `POST` endpoint you create on your server. Register it on the [Paystack Dashboard](https://dashboard.paystack.com/#/settings/developer) under Settings → API Keys & Webhooks.

## Signature Validation

Every webhook request includes an `x-paystack-signature` header containing an HMAC SHA512 hash of the request body, signed with your secret key. Always validate this before processing.

### Next.js App Router (Route Handler)

```typescript
// app/api/webhooks/paystack/route.ts
import crypto from "crypto";
import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  const body = await req.text();
  const signature = req.headers.get("x-paystack-signature");
  
  const hash = crypto
    .createHmac("sha512", process.env.PAYSTACK_SECRET_KEY!)
    .update(body)
    .digest("hex");

  if (hash !== signature) {
    return NextResponse.json({ error: "Invalid signature" }, { status: 401 });
  }

  // Return 200 immediately — process event asynchronously
  const event = JSON.parse(body);

  // Handle event based on type
  switch (event.event) {
    case "charge.success":
      await handleChargeSuccess(event.data);
      break;
    case "transfer.success":
      await handleTransferSuccess(event.data);
      break;
    case "transfer.failed":
      await handleTransferFailed(event.data);
      break;
    // ... handle other events
  }

  return NextResponse.json({ received: true }, { status: 200 });
}

async function handleChargeSuccess(data: any) {
  const { reference, amount, customer, metadata } = data;
  // Verify the transaction server-side as an extra check
  // Update your database, fulfill the order, etc.
}

async function handleTransferSuccess(data: any) {
  const { reference, amount, recipient } = data;
  // Mark transfer as completed in your database
}

async function handleTransferFailed(data: any) {
  const { reference, amount } = data;
  // Mark transfer as failed, notify admin, retry if needed
}
```

### Express.js

```typescript
import crypto from "crypto";
import express from "express";

const app = express();
app.use(express.json());

app.post("/webhooks/paystack", (req, res) => {
  const hash = crypto
    .createHmac("sha512", process.env.PAYSTACK_SECRET_KEY!)
    .update(JSON.stringify(req.body))
    .digest("hex");

  if (hash !== req.headers["x-paystack-signature"]) {
    return res.status(401).send("Invalid signature");
  }

  // Return 200 immediately
  res.sendStatus(200);

  // Process event asynchronously
  const event = req.body;
  processEvent(event).catch(console.error);
});
```

## IP Whitelisting

As an additional security layer, only allow requests from Paystack's IP addresses:

```
52.31.139.75
52.49.173.169
52.214.14.220
```

These IPs apply to both test and live environments.

```typescript
const PAYSTACK_IPS = ["52.31.139.75", "52.49.173.169", "52.214.14.220"];

function isPaystackIP(ip: string): boolean {
  // Handle x-forwarded-for if behind a proxy/load balancer
  const clientIP = ip.split(",")[0].trim();
  return PAYSTACK_IPS.includes(clientIP);
}
```

## Retry Policy

If your webhook endpoint doesn't return a `200 OK` status, Paystack retries:

| Mode | Retry Schedule | Duration |
| --- | --- | --- |
| **Live** | Every 3 minutes for first 4 tries, then hourly | Up to 72 hours |
| **Test** | Hourly | Up to 10 hours |

Request timeout is **30 seconds** in test mode. Return `200 OK` immediately and process events asynchronously to avoid timeouts.

## Idempotency

Webhook events may be sent more than once. Make your handler idempotent:

```typescript
async function handleChargeSuccess(data: any) {
  const { reference } = data;

  // Check if already processed
  const existing = await db.transaction.findUnique({ where: { reference } });
  if (existing?.status === "completed") {
    return; // Already processed, skip
  }

  // Process and mark as completed atomically
  await db.transaction.upsert({
    where: { reference },
    update: { status: "completed", paidAt: new Date() },
    create: { reference, status: "completed", amount: data.amount, paidAt: new Date() },
  });
}
```

## Supported Event Types

| Event | Description |
| --- | --- |
| `charge.success` | A successful charge/payment was made |
| `charge.dispute.create` | A dispute was logged against your business |
| `charge.dispute.remind` | A logged dispute hasn't been resolved |
| `charge.dispute.resolve` | A dispute has been resolved |
| `customeridentification.failed` | Customer ID validation failed |
| `customeridentification.success` | Customer ID validation succeeded |
| `dedicatedaccount.assign.failed` | DVA couldn't be created/assigned |
| `dedicatedaccount.assign.success` | DVA successfully created/assigned |
| `invoice.create` | Invoice created for a subscription (3 days before due) |
| `invoice.payment_failed` | Invoice payment failed |
| `invoice.update` | Invoice updated (usually after successful charge) |
| `paymentrequest.pending` | Payment request sent to customer |
| `paymentrequest.success` | Payment request paid |
| `refund.failed` | Refund failed — account credited with refund amount |
| `refund.pending` | Refund initiated, awaiting processor |
| `refund.processed` | Refund successfully processed |
| `refund.processing` | Refund received by processor |
| `subscription.create` | Subscription created |
| `subscription.disable` | Subscription disabled |
| `subscription.expiring_cards` | Monthly notice of subscriptions with expiring cards |
| `subscription.not_renew` | Subscription set to non-renewing |
| `transfer.success` | Transfer completed successfully |
| `transfer.failed` | Transfer failed |
| `transfer.reversed` | Transfer reversed |

## Event Payload Structure

Every webhook event follows this structure:

```json
{
  "event": "charge.success",
  "data": {
    "id": 4099260516,
    "domain": "live",
    "status": "success",
    "reference": "re4lyvq3s3",
    "amount": 50000,
    "currency": "NGN",
    "channel": "card",
    "customer": {
      "id": 82796315,
      "email": "customer@email.com",
      "customer_code": "CUS_xxxxx"
    },
    "authorization": {
      "authorization_code": "AUTH_xxxxx",
      "card_type": "visa",
      "last4": "4081",
      "reusable": true
    },
    "metadata": {}
  }
}
```

## Go-Live Checklist

1. Add the webhook URL on your Paystack dashboard (Settings → API Keys & Webhooks)
2. Ensure the URL is publicly accessible (localhost won't receive events)
3. If using `.htaccess`, add a trailing `/` to the URL
4. Validate signature on every request using `x-paystack-signature`
5. Return `200 OK` immediately before processing long-running tasks
6. Make handlers idempotent — events can be sent more than once
7. Test with Paystack's test mode before going live
