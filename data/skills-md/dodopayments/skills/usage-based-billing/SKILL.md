---
name: usage-based-billing
description: Guide for implementing usage-based billing with Dodo Payments - meters, events, pricing per unit, and metered subscriptions.
---

# Dodo Payments Usage-Based Billing

**Reference: [docs.dodopayments.com/features/usage-based-billing](https://docs.dodopayments.com/features/usage-based-billing/introduction)**

Charge customers for what they actually use—API calls, storage, AI tokens, or any metric you define.

---

## Overview

Usage-based billing is perfect for:
- **APIs**: Charge per request or operation
- **AI Services**: Bill per token, generation, or inference
- **Infrastructure**: Charge for compute, storage, bandwidth
- **SaaS**: Metered features alongside subscriptions

---

## Core Concepts

### Events
Usage actions sent from your application:
```json
{
  "event_id": "evt_unique_123",
  "customer_id": "cus_abc123",
  "event_name": "api.call",
  "timestamp": "2025-01-21T10:30:00Z",
  "metadata": { "endpoint": "/v1/users", "tokens": 150 }
}
```

### Meters
Aggregate events into billable quantities:
| Aggregation | Use Case | Example |
|-------------|----------|---------|
| **Count** | Total events | API calls, image generations |
| **Sum** | Add values | Tokens used, bytes transferred |
| **Max** | Highest value | Peak concurrent users |
| **Last** | Most recent | Current storage used |

### Products with Usage Pricing
- Price per unit (e.g., $0.001 per API call)
- Free threshold (e.g., 1,000 free calls)
- Automatic billing each cycle

**Billing Example**: 2,500 calls - 1,000 free = 1,500 × $0.02 = $30.00

---

## Quick Start

### 1. Create a Meter

In Dashboard → Meters → Create Meter:

1. **Name**: "API Requests"
2. **Event Name**: `api.call` (exact match, case-sensitive)
3. **Aggregation**: Count
4. **Unit**: "calls"

### 2. Create Usage-Based Product

In Dashboard → Products → Create Product:

1. Select **Usage-Based** type
2. Connect your meter
3. Set pricing:
   - **Price Per Unit**: $0.001
   - **Free Threshold**: 1000

### 3. Send Events

```typescript
import DodoPayments from 'dodopayments';

const client = new DodoPayments({
  bearerToken: process.env.DODO_PAYMENTS_API_KEY,
});

await client.usageEvents.ingest({
  events: [{
    event_id: `api_${Date.now()}_${Math.random()}`,
    customer_id: 'cus_abc123',
    event_name: 'api.call',
    timestamp: new Date().toISOString(),
    metadata: {
      endpoint: '/v1/users',
      method: 'GET',
    }
  }]
});
```

---

## Implementation Examples

### TypeScript/Node.js

```typescript
import DodoPayments from 'dodopayments';

const client = new DodoPayments({
  bearerToken: process.env.DODO_PAYMENTS_API_KEY!,
});

// Track single event
async function trackUsage(
  customerId: string,
  eventName: string,
  metadata: Record<string, string>
) {
  await client.usageEvents.ingest({
    events: [{
      event_id: `${eventName}_${Date.now()}_${crypto.randomUUID()}`,
      customer_id: customerId,
      event_name: eventName,
      timestamp: new Date().toISOString(),
      metadata,
    }]
  });
}

// Track API call
await trackUsage('cus_abc123', 'api.call', {
  endpoint: '/v1/generate',
  method: 'POST',
});

// Track token usage (for Sum aggregation)
await trackUsage('cus_abc123', 'token.usage', {
  tokens: '1500',
  model: 'gpt-4',
});
```

### Batch Event Ingestion

Send multiple events efficiently (max 1000 per request):

```typescript
async function trackBatchUsage(
  events: Array<{
    customerId: string;
    eventName: string;
    metadata: Record<string, string>;
    timestamp?: string;
  }>
) {
  const formattedEvents = events.map((e, i) => ({
    event_id: `batch_${Date.now()}_${i}_${crypto.randomUUID()}`,
    customer_id: e.customerId,
    event_name: e.eventName,
    timestamp: e.timestamp || new Date().toISOString(),
    metadata: e.metadata,
  }));

  await client.usageEvents.ingest({ events: formattedEvents });
}

// Batch track multiple API calls
await trackBatchUsage([
  { customerId: 'cus_abc', eventName: 'api.call', metadata: { endpoint: '/v1/users' } },
  { customerId: 'cus_abc', eventName: 'api.call', metadata: { endpoint: '/v1/orders' } },
  { customerId: 'cus_xyz', eventName: 'api.call', metadata: { endpoint: '/v1/products' } },
]);
```

### Python

```python
from dodopayments import DodoPayments
import uuid
from datetime import datetime

client = DodoPayments(bearer_token=os.environ["DODO_PAYMENTS_API_KEY"])

def track_usage(customer_id: str, event_name: str, metadata: dict):
    client.usage_events.ingest(events=[{
        "event_id": f"{event_name}_{datetime.now().timestamp()}_{uuid.uuid4()}",
        "customer_id": customer_id,
        "event_name": event_name,
        "timestamp": datetime.now().isoformat(),
        "metadata": metadata
    }])

# Track AI token usage
track_usage("cus_abc123", "ai.tokens", {
    "tokens": "2500",
    "model": "claude-3",
    "operation": "completion"
})

# Track image generation
track_usage("cus_abc123", "image.generated", {
    "size": "1024x1024",
    "model": "dall-e-3"
})
```

### Go

```go
package main

import (
    "context"
    "fmt"
    "os"
    "time"

    "github.com/dodopayments/dodopayments-go"
    "github.com/google/uuid"
)

func main() {
    client := dodopayments.NewClient(
        option.WithBearerToken(os.Getenv("DODO_PAYMENTS_API_KEY")),
    )

    ctx := context.Background()

    _, err := client.UsageEvents.Ingest(ctx, &dodopayments.UsageEventIngestParams{
        Events: []dodopayments.UsageEvent{{
            EventID:    fmt.Sprintf("api_%d_%s", time.Now().Unix(), uuid.New().String()),
            CustomerID: "cus_abc123",
            EventName:  "api.call",
            Timestamp:  time.Now().Format(time.RFC3339),
            Metadata: map[string]string{
                "endpoint": "/v1/users",
                "method":   "GET",
            },
        }},
    })

    if err != nil {
        panic(err)
    }
}
```

---

## Meter Configuration

### Aggregation Types

#### Count (API Calls, Requests)
```
Meter: API Requests
Event Name: api.call
Aggregation: Count
Unit: calls
```

#### Sum (Tokens, Bytes)
```
Meter: Token Usage
Event Name: token.usage
Aggregation: Sum
Over Property: tokens
Unit: tokens
```

Events must include the property in metadata:
```typescript
await client.usageEvents.ingest({
  events: [{
    event_id: 'token_123',
    customer_id: 'cus_abc',
    event_name: 'token.usage',
    metadata: { tokens: '1500' } // This value gets summed
  }]
});
```

#### Max (Peak Concurrent Users)
```
Meter: Peak Users
Event Name: concurrent.users
Aggregation: Max
Over Property: count
Unit: users
```

#### Last (Current Storage)
```
Meter: Storage Used
Event Name: storage.snapshot
Aggregation: Last
Over Property: bytes
Unit: GB
```

### Event Filtering

Filter which events count toward the meter:

```
Filter Logic: AND
Conditions:
  - Property: tier, Equals: "premium"
  - Property: status, Equals: "success"
```

Only events matching ALL conditions are counted.

---

## Common Use Cases

### AI Token Billing

```typescript
// Meter: AI Tokens (Sum aggregation over "tokens" property)

async function trackAIUsage(
  customerId: string,
  promptTokens: number,
  completionTokens: number,
  model: string
) {
  const totalTokens = promptTokens + completionTokens;

  await client.usageEvents.ingest({
    events: [{
      event_id: `ai_${Date.now()}_${crypto.randomUUID()}`,
      customer_id: customerId,
      event_name: 'ai.tokens',
      timestamp: new Date().toISOString(),
      metadata: {
        tokens: totalTokens.toString(),
        prompt_tokens: promptTokens.toString(),
        completion_tokens: completionTokens.toString(),
        model,
      }
    }]
  });
}

// After AI completion
await trackAIUsage('cus_abc', 500, 1200, 'gpt-4');
```

### Image Generation

```typescript
// Meter: Images Generated (Count aggregation)

async function trackImageGeneration(
  customerId: string,
  imageSize: string,
  model: string
) {
  await client.usageEvents.ingest({
    events: [{
      event_id: `img_${Date.now()}_${crypto.randomUUID()}`,
      customer_id: customerId,
      event_name: 'image.generated',
      timestamp: new Date().toISOString(),
      metadata: {
        size: imageSize,
        model,
      }
    }]
  });
}
```

### API Rate Tracking

```typescript
// Middleware for Express/Next.js

async function trackAPIUsage(
  req: Request,
  customerId: string
) {
  await client.usageEvents.ingest({
    events: [{
      event_id: `api_${Date.now()}_${crypto.randomUUID()}`,
      customer_id: customerId,
      event_name: 'api.call',
      timestamp: new Date().toISOString(),
      metadata: {
        endpoint: req.url,
        method: req.method,
        user_agent: req.headers['user-agent'] || 'unknown',
      }
    }]
  });
}
```

### Storage Billing

```typescript
// Meter: Storage (Last aggregation - snapshot of current usage)

async function updateStorageUsage(customerId: string, bytesUsed: number) {
  await client.usageEvents.ingest({
    events: [{
      event_id: `storage_${Date.now()}_${customerId}`,
      customer_id: customerId,
      event_name: 'storage.snapshot',
      timestamp: new Date().toISOString(),
      metadata: {
        bytes: bytesUsed.toString(),
        gb: (bytesUsed / 1024 / 1024 / 1024).toFixed(2),
      }
    }]
  });
}

// Call periodically or after storage changes
await updateStorageUsage('cus_abc', 5368709120); // 5GB
```

---

## Next.js Integration

### API Route for Usage Tracking

```typescript
// app/api/track-usage/route.ts
import { NextRequest, NextResponse } from 'next/server';
import DodoPayments from 'dodopayments';

const client = new DodoPayments({
  bearerToken: process.env.DODO_PAYMENTS_API_KEY!,
});

export async function POST(req: NextRequest) {
  const { customerId, eventName, metadata } = await req.json();

  try {
    await client.usageEvents.ingest({
      events: [{
        event_id: `${eventName}_${Date.now()}_${crypto.randomUUID()}`,
        customer_id: customerId,
        event_name: eventName,
        timestamp: new Date().toISOString(),
        metadata,
      }]
    });

    return NextResponse.json({ success: true });
  } catch (error: any) {
    return NextResponse.json(
      { error: error.message },
      { status: 500 }
    );
  }
}
```

### Usage Tracking Hook

```typescript
// hooks/useUsageTracking.ts
import { useCallback } from 'react';

export function useUsageTracking(customerId: string) {
  const trackUsage = useCallback(async (
    eventName: string,
    metadata: Record<string, string>
  ) => {
    await fetch('/api/track-usage', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ customerId, eventName, metadata }),
    });
  }, [customerId]);

  return { trackUsage };
}

// Usage in component
function AIChat() {
  const { trackUsage } = useUsageTracking('cus_abc123');

  const handleGenerate = async () => {
    const result = await generateAIResponse(prompt);
    
    // Track token usage
    await trackUsage('ai.tokens', {
      tokens: result.totalTokens.toString(),
      model: 'gpt-4',
    });
  };
}
```

---

## Hybrid Billing

Combine usage-based with subscriptions:

### Subscription + Usage Overage

```typescript
// 1. Customer subscribes to plan with included usage
// Product: Pro Plan - $49/month + $0.01/call after 10,000 free

// 2. Track all usage events
await trackUsage('cus_abc', 'api.call', { endpoint: '/v1/generate' });

// 3. Dodo automatically:
//    - Applies free threshold (10,000 calls)
//    - Charges overage at $0.01/call
//    - Combines with subscription fee
```

### Multiple Meters per Product

Attach up to 10 meters to a single product:

```
Product: AI Platform
├── Meter: API Calls ($0.001/call, 1000 free)
├── Meter: Token Usage ($0.01/1000 tokens)
├── Meter: Image Generations ($0.05/image, 10 free)
└── Meter: Storage ($0.10/GB)
```

---

## Best Practices

### 1. Unique Event IDs
Always generate unique IDs for idempotency:
```typescript
const eventId = `${eventName}_${Date.now()}_${crypto.randomUUID()}`;
```

### 2. Batch Events
For high-volume, batch events (max 1000/request):
```typescript
// Queue events and send in batches
const eventQueue: Event[] = [];

function queueEvent(event: Event) {
  eventQueue.push(event);
  if (eventQueue.length >= 100) {
    flushEvents();
  }
}

async function flushEvents() {
  if (eventQueue.length === 0) return;
  const batch = eventQueue.splice(0, 1000);
  await client.usageEvents.ingest({ events: batch });
}

// Flush periodically
setInterval(flushEvents, 5000);
```

### 3. Handle Failures Gracefully
Implement retry logic for event ingestion:
```typescript
async function trackWithRetry(event: Event, retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      await client.usageEvents.ingest({ events: [event] });
      return;
    } catch (error) {
      if (i === retries - 1) throw error;
      await sleep(1000 * Math.pow(2, i)); // Exponential backoff
    }
  }
}
```

### 4. Include Relevant Metadata
Add context for debugging and filtering:
```typescript
metadata: {
  endpoint: '/v1/generate',
  method: 'POST',
  model: 'gpt-4',
  user_id: 'internal_user_123',
  request_id: requestId,
}
```

### 5. Monitor in Dashboard
Check Meters dashboard for:
- Event volume and trends
- Usage per customer
- Aggregated quantities

---

## Pricing Examples

### API Service
```
Meter: API Calls (Count)
Price: $0.001 per call
Free Threshold: 1,000 calls/month

Customer uses 15,000 calls:
(15,000 - 1,000) × $0.001 = $14.00
```

### AI Token Service
```
Meter: Tokens (Sum over "tokens")
Price: $0.00001 per token ($0.01 per 1,000)
Free Threshold: 10,000 tokens

Customer uses 50,000 tokens:
(50,000 - 10,000) × $0.00001 = $0.40
```

### Image Generation
```
Meter: Images (Count)
Price: $0.05 per image
Free Threshold: 10 images

Customer generates 100 images:
(100 - 10) × $0.05 = $4.50
```

---

## Resources

- [Usage-Based Billing Guide](https://docs.dodopayments.com/features/usage-based-billing/introduction)
- [Meters Documentation](https://docs.dodopayments.com/features/usage-based-billing/meters)
- [Event Ingestion](https://docs.dodopayments.com/features/usage-based-billing/event-ingestion)
- [AI Chat App Tutorial](https://docs.dodopayments.com/developer-resources/build-an-ai-chat-app-with-usage-based-billing)
- [Hybrid Billing Models](https://docs.dodopayments.com/features/hybrid-billing)
