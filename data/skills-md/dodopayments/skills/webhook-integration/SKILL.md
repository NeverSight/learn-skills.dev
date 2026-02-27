---
name: webhook-integration
description: Complete guide for setting up and handling Dodo Payments webhooks for real-time payment event notifications.
---

# Dodo Payments Webhook Integration

**Reference: [docs.dodopayments.com/developer-resources/webhooks](https://docs.dodopayments.com/developer-resources/webhooks)**

Webhooks provide real-time notifications when payment events occur. Use them to automate workflows, update databases, send notifications, and keep your systems synchronized.

---

## Quick Setup

### 1. Configure Webhook in Dashboard
1. Go to Dashboard → Developer → Webhooks
2. Click "Create Webhook"
3. Enter your endpoint URL
4. Select events to subscribe to
5. Copy the webhook secret

### 2. Environment Variables
```bash
DODO_PAYMENTS_WEBHOOK_SECRET=your_webhook_secret_here
```

---

## Webhook Events

### Payment Events
| Event | Description |
|-------|-------------|
| `payment.succeeded` | Payment completed successfully |
| `payment.failed` | Payment attempt failed |
| `payment.processing` | Payment is being processed |
| `payment.cancelled` | Payment was cancelled |

### Subscription Events
| Event | Description |
|-------|-------------|
| `subscription.active` | Subscription is now active |
| `subscription.updated` | Subscription details changed |
| `subscription.on_hold` | Subscription on hold (failed renewal) |
| `subscription.renewed` | Subscription renewed successfully |
| `subscription.plan_changed` | Plan upgraded/downgraded |
| `subscription.cancelled` | Subscription cancelled |
| `subscription.failed` | Subscription creation failed |
| `subscription.expired` | Subscription term ended |

### Other Events
| Event | Description |
|-------|-------------|
| `refund.succeeded` | Refund processed successfully |
| `dispute.opened` | New dispute received |
| `license_key.created` | License key generated |

---

## Webhook Payload Structure

### Request Headers
```http
POST /your-webhook-url
Content-Type: application/json
webhook-id: evt_xxxxx
webhook-signature: v1,signature_here
webhook-timestamp: 1234567890
```

### Payload Format
```json
{
  "business_id": "bus_xxxxx",
  "type": "payment.succeeded",
  "timestamp": "2024-01-01T12:00:00Z",
  "data": {
    "payload_type": "Payment",
    "payment_id": "pay_xxxxx",
    "total_amount": 2999,
    "currency": "USD",
    "customer": {
      "customer_id": "cust_xxxxx",
      "email": "customer@example.com",
      "name": "John Doe"
    }
    // ... additional event-specific fields
  }
}
```

---

## Implementation Examples

### Next.js (App Router)

```typescript
// app/api/webhooks/dodo/route.ts
import { NextRequest, NextResponse } from 'next/server';
import crypto from 'crypto';

const WEBHOOK_SECRET = process.env.DODO_PAYMENTS_WEBHOOK_SECRET!;

function verifySignature(payload: string, signature: string, timestamp: string): boolean {
  const signedPayload = `${timestamp}.${payload}`;
  const expectedSignature = crypto
    .createHmac('sha256', WEBHOOK_SECRET)
    .update(signedPayload)
    .digest('base64');
  
  // Extract signature from "v1,signature" format
  const providedSig = signature.split(',')[1];
  
  return crypto.timingSafeEqual(
    Buffer.from(expectedSignature),
    Buffer.from(providedSig || '')
  );
}

export async function POST(req: NextRequest) {
  const body = await req.text();
  const signature = req.headers.get('webhook-signature') || '';
  const timestamp = req.headers.get('webhook-timestamp') || '';
  const webhookId = req.headers.get('webhook-id');

  // Verify signature
  if (!verifySignature(body, signature, timestamp)) {
    return NextResponse.json({ error: 'Invalid signature' }, { status: 401 });
  }

  // Check timestamp to prevent replay attacks (5 minute tolerance)
  const eventTime = parseInt(timestamp) * 1000;
  if (Math.abs(Date.now() - eventTime) > 300000) {
    return NextResponse.json({ error: 'Timestamp too old' }, { status: 401 });
  }

  const event = JSON.parse(body);

  // Handle events
  switch (event.type) {
    case 'payment.succeeded':
      await handlePaymentSucceeded(event.data);
      break;
    case 'payment.failed':
      await handlePaymentFailed(event.data);
      break;
    case 'subscription.active':
      await handleSubscriptionActive(event.data);
      break;
    case 'subscription.cancelled':
      await handleSubscriptionCancelled(event.data);
      break;
    case 'refund.succeeded':
      await handleRefundSucceeded(event.data);
      break;
    case 'dispute.opened':
      await handleDisputeOpened(event.data);
      break;
    case 'license_key.created':
      await handleLicenseKeyCreated(event.data);
      break;
    default:
      console.log(`Unhandled event type: ${event.type}`);
  }

  return NextResponse.json({ received: true });
}

async function handlePaymentSucceeded(data: any) {
  const { payment_id, customer, total_amount, product_id, subscription_id } = data;
  
  // Update database
  // Send confirmation email
  // Grant access to product
  console.log(`Payment ${payment_id} succeeded for ${customer.email}`);
}

async function handlePaymentFailed(data: any) {
  const { payment_id, customer, error_message } = data;
  
  // Log failure
  // Notify customer
  // Update UI state
  console.log(`Payment ${payment_id} failed: ${error_message}`);
}

async function handleSubscriptionActive(data: any) {
  const { subscription_id, customer, product_id, next_billing_date } = data;
  
  // Grant subscription access
  // Update user record
  // Send welcome email
  console.log(`Subscription ${subscription_id} activated for ${customer.email}`);
}

async function handleSubscriptionCancelled(data: any) {
  const { subscription_id, customer, cancelled_at, cancel_at_next_billing_date } = data;
  
  // Schedule access revocation
  // Send cancellation confirmation
  console.log(`Subscription ${subscription_id} cancelled`);
}

async function handleRefundSucceeded(data: any) {
  const { refund_id, payment_id, amount } = data;
  
  // Update order status
  // Revoke access if needed
  console.log(`Refund ${refund_id} processed for payment ${payment_id}`);
}

async function handleDisputeOpened(data: any) {
  const { dispute_id, payment_id, amount, dispute_status } = data;
  
  // Alert team
  // Prepare evidence
  console.log(`Dispute ${dispute_id} opened for payment ${payment_id}`);
}

async function handleLicenseKeyCreated(data: any) {
  const { id, key, product_id, customer_id, expires_at } = data;
  
  // Store license key
  // Send to customer
  console.log(`License key created: ${key.substring(0, 8)}...`);
}
```

### Express.js

```typescript
import express from 'express';
import crypto from 'crypto';

const app = express();
const WEBHOOK_SECRET = process.env.DODO_PAYMENTS_WEBHOOK_SECRET!;

// Use raw body for signature verification
app.post('/webhooks/dodo', 
  express.raw({ type: 'application/json' }),
  async (req, res) => {
    const signature = req.headers['webhook-signature'] as string;
    const timestamp = req.headers['webhook-timestamp'] as string;
    const payload = req.body.toString();

    // Verify signature
    const signedPayload = `${timestamp}.${payload}`;
    const expectedSig = crypto
      .createHmac('sha256', WEBHOOK_SECRET)
      .update(signedPayload)
      .digest('base64');
    
    const providedSig = signature?.split(',')[1];
    
    if (!providedSig || !crypto.timingSafeEqual(
      Buffer.from(expectedSig),
      Buffer.from(providedSig)
    )) {
      return res.status(401).json({ error: 'Invalid signature' });
    }

    const event = JSON.parse(payload);

    // Process event
    try {
      switch (event.type) {
        case 'payment.succeeded':
          await processPayment(event.data);
          break;
        case 'subscription.active':
          await activateSubscription(event.data);
          break;
        // ... handle other events
      }
      res.json({ received: true });
    } catch (error) {
      console.error('Webhook processing error:', error);
      res.status(500).json({ error: 'Processing failed' });
    }
  }
);
```

### Python (FastAPI)

```python
from fastapi import FastAPI, Request, HTTPException
import hmac
import hashlib
import base64
import time

app = FastAPI()
WEBHOOK_SECRET = os.environ["DODO_PAYMENTS_WEBHOOK_SECRET"]

def verify_signature(payload: bytes, signature: str, timestamp: str) -> bool:
    signed_payload = f"{timestamp}.{payload.decode()}"
    expected_sig = base64.b64encode(
        hmac.new(
            WEBHOOK_SECRET.encode(),
            signed_payload.encode(),
            hashlib.sha256
        ).digest()
    ).decode()
    
    provided_sig = signature.split(',')[1] if ',' in signature else ''
    return hmac.compare_digest(expected_sig, provided_sig)

@app.post("/webhooks/dodo")
async def handle_webhook(request: Request):
    body = await request.body()
    signature = request.headers.get("webhook-signature", "")
    timestamp = request.headers.get("webhook-timestamp", "")
    
    if not verify_signature(body, signature, timestamp):
        raise HTTPException(status_code=401, detail="Invalid signature")
    
    # Check timestamp freshness
    event_time = int(timestamp)
    if abs(time.time() - event_time) > 300:
        raise HTTPException(status_code=401, detail="Timestamp too old")
    
    event = json.loads(body)
    
    if event["type"] == "payment.succeeded":
        await handle_payment_succeeded(event["data"])
    elif event["type"] == "subscription.active":
        await handle_subscription_active(event["data"])
    # ... handle other events
    
    return {"received": True}
```

### Go

```go
package main

import (
    "crypto/hmac"
    "crypto/sha256"
    "encoding/base64"
    "encoding/json"
    "io"
    "net/http"
    "os"
    "strconv"
    "strings"
    "time"
)

var webhookSecret = os.Getenv("DODO_PAYMENTS_WEBHOOK_SECRET")

func verifySignature(payload []byte, signature, timestamp string) bool {
    signedPayload := timestamp + "." + string(payload)
    
    mac := hmac.New(sha256.New, []byte(webhookSecret))
    mac.Write([]byte(signedPayload))
    expectedSig := base64.StdEncoding.EncodeToString(mac.Sum(nil))
    
    parts := strings.Split(signature, ",")
    if len(parts) < 2 {
        return false
    }
    
    return hmac.Equal([]byte(expectedSig), []byte(parts[1]))
}

func webhookHandler(w http.ResponseWriter, r *http.Request) {
    body, _ := io.ReadAll(r.Body)
    signature := r.Header.Get("webhook-signature")
    timestamp := r.Header.Get("webhook-timestamp")
    
    if !verifySignature(body, signature, timestamp) {
        http.Error(w, "Invalid signature", http.StatusUnauthorized)
        return
    }
    
    // Check timestamp
    ts, _ := strconv.ParseInt(timestamp, 10, 64)
    if time.Since(time.Unix(ts, 0)) > 5*time.Minute {
        http.Error(w, "Timestamp too old", http.StatusUnauthorized)
        return
    }
    
    var event map[string]interface{}
    json.Unmarshal(body, &event)
    
    switch event["type"] {
    case "payment.succeeded":
        handlePaymentSucceeded(event["data"].(map[string]interface{}))
    case "subscription.active":
        handleSubscriptionActive(event["data"].(map[string]interface{}))
    }
    
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(map[string]bool{"received": true})
}
```

---

## Best Practices

### 1. Always Verify Signatures
Never process webhooks without signature verification to prevent spoofing.

### 2. Implement Idempotency
Use `webhook-id` header to prevent duplicate processing:
```typescript
const processedIds = new Set<string>();

if (processedIds.has(webhookId)) {
  return NextResponse.json({ received: true }); // Already processed
}
processedIds.add(webhookId);
```

### 3. Respond Quickly
Return 200 immediately, process asynchronously if needed:
```typescript
// Queue for async processing
await queue.add('process-webhook', event);
return NextResponse.json({ received: true });
```

### 4. Handle Retries
Dodo Payments retries failed webhooks. Design handlers to be idempotent.

### 5. Log Everything
Keep detailed logs for debugging:
```typescript
console.log(`[Webhook] ${event.type} - ${webhookId}`, {
  timestamp: event.timestamp,
  data: event.data
});
```

---

## Local Development

### Using ngrok
```bash
# Start ngrok tunnel
ngrok http 3000

# Use the ngrok URL as your webhook endpoint
# https://xxxx.ngrok.io/api/webhooks/dodo
```

### Testing Webhooks
You can trigger test webhooks from the Dodo Payments dashboard:
1. Go to Developer → Webhooks
2. Select your webhook
3. Click "Send Test Event"

---

## Troubleshooting

### Signature Verification Failing
- Ensure you're using the raw request body
- Check webhook secret is correct
- Verify timestamp format (Unix seconds)

### Not Receiving Webhooks
- Check endpoint is publicly accessible
- Verify webhook is enabled in dashboard
- Check server logs for errors

### Duplicate Events
- Implement idempotency using webhook-id
- Store processed event IDs in database

---

## Resources

- [Webhook Documentation](https://docs.dodopayments.com/developer-resources/webhooks)
- [Event Reference](https://docs.dodopayments.com/developer-resources/webhooks/intents/webhook-events-guide)
- [Standard Webhooks Spec](https://standardwebhooks.com/)
