---
name: checkout-integration
description: Guide for creating checkout sessions and payment flows with Dodo Payments - one-time, subscriptions, and overlay checkout.
---

# Dodo Payments Checkout Integration

**Reference: [docs.dodopayments.com/developer-resources/integration-guide](https://docs.dodopayments.com/developer-resources/integration-guide)**

Create seamless payment experiences with hosted checkout pages or overlay checkout modals.

---

## Checkout Methods

| Method | Best For | Integration |
|--------|----------|-------------|
| **Hosted Checkout** | Simple integration, full-page redirect | Server-side SDK |
| **Overlay Checkout** | Seamless UX, stays on your site | JavaScript SDK |
| **Payment Links** | No-code, shareable links | Dashboard |

---

## Hosted Checkout

### Basic Implementation

```typescript
import DodoPayments from 'dodopayments';

const client = new DodoPayments({
  bearerToken: process.env.DODO_PAYMENTS_API_KEY,
});

// Create checkout session
const session = await client.checkoutSessions.create({
  product_cart: [
    { product_id: 'prod_xxxxx', quantity: 1 }
  ],
  customer: {
    email: 'customer@example.com',
    name: 'John Doe',
  },
  return_url: 'https://yoursite.com/checkout/success',
});

// Redirect customer to checkout
// session.checkout_url
```

### With Multiple Products

```typescript
const session = await client.checkoutSessions.create({
  product_cart: [
    { product_id: 'prod_item_1', quantity: 2 },
    { product_id: 'prod_item_2', quantity: 1 },
  ],
  customer: {
    email: 'customer@example.com',
  },
  return_url: 'https://yoursite.com/success',
});
```

### With Customer ID (Existing Customer)

```typescript
const session = await client.checkoutSessions.create({
  product_cart: [
    { product_id: 'prod_xxxxx', quantity: 1 }
  ],
  customer_id: 'cust_existing_customer',
  return_url: 'https://yoursite.com/success',
});
```

### With Metadata

```typescript
const session = await client.checkoutSessions.create({
  product_cart: [
    { product_id: 'prod_xxxxx', quantity: 1 }
  ],
  customer: {
    email: 'customer@example.com',
  },
  metadata: {
    order_id: 'order_12345',
    referral_code: 'FRIEND20',
    user_id: 'internal_user_id',
  },
  return_url: 'https://yoursite.com/success',
});
```

---

## Next.js Implementation

### API Route

```typescript
// app/api/checkout/route.ts
import { NextRequest, NextResponse } from 'next/server';
import DodoPayments from 'dodopayments';

const client = new DodoPayments({
  bearerToken: process.env.DODO_PAYMENTS_API_KEY!,
});

export async function POST(req: NextRequest) {
  try {
    const { productId, quantity = 1, email, name, metadata } = await req.json();

    if (!productId || !email) {
      return NextResponse.json(
        { error: 'Missing required fields' },
        { status: 400 }
      );
    }

    const session = await client.checkoutSessions.create({
      product_cart: [{ product_id: productId, quantity }],
      customer: { email, name },
      metadata,
      return_url: `${process.env.NEXT_PUBLIC_APP_URL}/checkout/success`,
    });

    return NextResponse.json({ 
      checkoutUrl: session.checkout_url,
      sessionId: session.checkout_session_id,
    });
  } catch (error: any) {
    console.error('Checkout error:', error);
    return NextResponse.json(
      { error: error.message || 'Failed to create checkout' },
      { status: 500 }
    );
  }
}
```

### Client Component

```typescript
// components/CheckoutButton.tsx
'use client';

import { useState } from 'react';

interface CheckoutButtonProps {
  productId: string;
  email: string;
  name?: string;
  children: React.ReactNode;
}

export function CheckoutButton({ productId, email, name, children }: CheckoutButtonProps) {
  const [loading, setLoading] = useState(false);

  const handleCheckout = async () => {
    setLoading(true);
    
    try {
      const response = await fetch('/api/checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ productId, email, name }),
      });

      const data = await response.json();
      
      if (data.checkoutUrl) {
        window.location.href = data.checkoutUrl;
      } else {
        throw new Error(data.error || 'Failed to create checkout');
      }
    } catch (error) {
      console.error('Checkout error:', error);
      alert('Failed to start checkout. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <button onClick={handleCheckout} disabled={loading}>
      {loading ? 'Loading...' : children}
    </button>
  );
}
```

### Success Page

```typescript
// app/checkout/success/page.tsx
import { Suspense } from 'react';

function SuccessContent() {
  return (
    <div className="text-center py-20">
      <h1 className="text-3xl font-bold">Payment Successful!</h1>
      <p className="mt-4 text-gray-600">
        Thank you for your purchase. You will receive a confirmation email shortly.
      </p>
      <a href="/" className="mt-8 inline-block text-blue-600 hover:underline">
        Return to Home
      </a>
    </div>
  );
}

export default function SuccessPage() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <SuccessContent />
    </Suspense>
  );
}
```

---

## Overlay Checkout

Embed checkout directly on your page without redirects.

### Installation

```bash
npm install @dodopayments/checkout
```

### Basic Usage

```typescript
import { DodoCheckout } from '@dodopayments/checkout';

// Initialize
const checkout = new DodoCheckout({
  apiKey: 'your_publishable_key',
  environment: 'live', // or 'test'
});

// Open overlay
checkout.open({
  productId: 'prod_xxxxx',
  customer: {
    email: 'customer@example.com',
  },
  onSuccess: (result) => {
    console.log('Payment successful:', result);
    // Handle success
  },
  onClose: () => {
    console.log('Checkout closed');
  },
});
```

### React Component

```typescript
// components/OverlayCheckout.tsx
'use client';

import { useEffect, useRef } from 'react';
import { DodoCheckout } from '@dodopayments/checkout';

interface OverlayCheckoutProps {
  productId: string;
  email: string;
  onSuccess?: (result: any) => void;
  children: React.ReactNode;
}

export function OverlayCheckout({ 
  productId, 
  email, 
  onSuccess,
  children 
}: OverlayCheckoutProps) {
  const checkoutRef = useRef<DodoCheckout | null>(null);

  useEffect(() => {
    checkoutRef.current = new DodoCheckout({
      apiKey: process.env.NEXT_PUBLIC_DODO_PUBLISHABLE_KEY!,
      environment: process.env.NODE_ENV === 'production' ? 'live' : 'test',
    });

    return () => {
      checkoutRef.current?.close();
    };
  }, []);

  const handleClick = () => {
    checkoutRef.current?.open({
      productId,
      customer: { email },
      onSuccess: (result) => {
        onSuccess?.(result);
        // Optionally redirect
        window.location.href = '/checkout/success';
      },
      onClose: () => {
        console.log('Checkout closed');
      },
    });
  };

  return (
    <button onClick={handleClick}>
      {children}
    </button>
  );
}
```

### Customization

```typescript
checkout.open({
  productId: 'prod_xxxxx',
  customer: { email: 'customer@example.com' },
  theme: {
    primaryColor: '#0066FF',
    backgroundColor: '#FFFFFF',
    fontFamily: 'Inter, sans-serif',
  },
  locale: 'en',
});
```

---

## Express.js Implementation

```typescript
import express from 'express';
import DodoPayments from 'dodopayments';

const app = express();
app.use(express.json());

const client = new DodoPayments({
  bearerToken: process.env.DODO_PAYMENTS_API_KEY!,
});

app.post('/api/create-checkout', async (req, res) => {
  try {
    const { productId, email, name, quantity = 1 } = req.body;

    const session = await client.checkoutSessions.create({
      product_cart: [{ product_id: productId, quantity }],
      customer: { email, name },
      return_url: `${process.env.APP_URL}/success`,
    });

    res.json({ checkoutUrl: session.checkout_url });
  } catch (error: any) {
    res.status(500).json({ error: error.message });
  }
});

// Success page route
app.get('/success', (req, res) => {
  res.send('Payment successful!');
});
```

---

## Python Implementation

### FastAPI

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dodopayments import DodoPayments
import os

app = FastAPI()
client = DodoPayments(bearer_token=os.environ["DODO_PAYMENTS_API_KEY"])

class CheckoutRequest(BaseModel):
    product_id: str
    email: str
    name: str = None
    quantity: int = 1

@app.post("/api/checkout")
async def create_checkout(request: CheckoutRequest):
    try:
        session = client.checkout_sessions.create(
            product_cart=[{
                "product_id": request.product_id,
                "quantity": request.quantity
            }],
            customer={
                "email": request.email,
                "name": request.name
            },
            return_url=f"{os.environ['APP_URL']}/success"
        )
        
        return {"checkout_url": session.checkout_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Flask

```python
from flask import Flask, request, jsonify
from dodopayments import DodoPayments
import os

app = Flask(__name__)
client = DodoPayments(bearer_token=os.environ["DODO_PAYMENTS_API_KEY"])

@app.route('/api/checkout', methods=['POST'])
def create_checkout():
    data = request.json
    
    session = client.checkout_sessions.create(
        product_cart=[{
            "product_id": data['product_id'],
            "quantity": data.get('quantity', 1)
        }],
        customer={
            "email": data['email'],
            "name": data.get('name')
        },
        return_url=f"{os.environ['APP_URL']}/success"
    )
    
    return jsonify({"checkout_url": session.checkout_url})
```

---

## Go Implementation

```go
package main

import (
    "encoding/json"
    "net/http"
    "os"
    
    "github.com/dodopayments/dodopayments-go"
)

var client = dodopayments.NewClient(
    option.WithBearerToken(os.Getenv("DODO_PAYMENTS_API_KEY")),
)

type CheckoutRequest struct {
    ProductID string `json:"product_id"`
    Email     string `json:"email"`
    Name      string `json:"name"`
    Quantity  int    `json:"quantity"`
}

func createCheckout(w http.ResponseWriter, r *http.Request) {
    var req CheckoutRequest
    json.NewDecoder(r.Body).Decode(&req)
    
    if req.Quantity == 0 {
        req.Quantity = 1
    }
    
    session, err := client.CheckoutSessions.Create(r.Context(), &dodopayments.CheckoutSessionCreateParams{
        ProductCart: []dodopayments.CartItem{
            {ProductID: req.ProductID, Quantity: req.Quantity},
        },
        Customer: &dodopayments.Customer{
            Email: req.Email,
            Name:  req.Name,
        },
        ReturnURL: os.Getenv("APP_URL") + "/success",
    })
    
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }
    
    json.NewEncoder(w).Encode(map[string]string{
        "checkout_url": session.CheckoutURL,
    })
}
```

---

## Handling Success

### Query Parameters
The return URL receives these query parameters:
- `status=success` - Payment completed
- `session_id` - Checkout session ID

### Verify Payment Server-Side
Don't rely solely on the redirect. Always verify via webhook:

```typescript
// Webhook handler confirms payment
app.post('/webhook', async (req, res) => {
  const event = req.body;
  
  if (event.type === 'payment.succeeded') {
    // This is the source of truth
    await fulfillOrder(event.data);
  }
  
  res.json({ received: true });
});
```

---

## Advanced Options

### Prefill Customer Info
```typescript
const session = await client.checkoutSessions.create({
  product_cart: [{ product_id: 'prod_xxxxx', quantity: 1 }],
  customer: {
    email: 'customer@example.com',
    name: 'John Doe',
    phone: '+1234567890',
    address: {
      line1: '123 Main St',
      city: 'San Francisco',
      state: 'CA',
      postal_code: '94105',
      country: 'US',
    },
  },
  return_url: 'https://yoursite.com/success',
});
```

### Custom Success/Cancel URLs
```typescript
const session = await client.checkoutSessions.create({
  product_cart: [{ product_id: 'prod_xxxxx', quantity: 1 }],
  customer: { email: 'customer@example.com' },
  return_url: 'https://yoursite.com/checkout/success?session_id={CHECKOUT_SESSION_ID}',
});
```

### Subscription with Trial
```typescript
const session = await client.checkoutSessions.create({
  product_cart: [{ product_id: 'prod_subscription', quantity: 1 }],
  subscription_data: {
    trial_period_days: 14,
  },
  customer: { email: 'customer@example.com' },
  return_url: 'https://yoursite.com/success',
});
```

---

## Error Handling

```typescript
try {
  const session = await client.checkoutSessions.create({...});
} catch (error: any) {
  if (error.status === 400) {
    // Invalid parameters
    console.error('Invalid request:', error.message);
  } else if (error.status === 401) {
    // Invalid API key
    console.error('Authentication failed');
  } else if (error.status === 404) {
    // Product not found
    console.error('Product not found');
  } else {
    console.error('Checkout error:', error);
  }
}
```

---

## Resources

- [Integration Guide](https://docs.dodopayments.com/developer-resources/integration-guide)
- [Overlay Checkout](https://docs.dodopayments.com/developer-resources/overlay-checkout)
- [API Reference](https://docs.dodopayments.com/api-reference/checkout-sessions)
