---
name: stripe-expert
description: >
  ALWAYS trigger for ANY task involving Stripe, payments, subscriptions,
  checkout sessions, Stripe webhooks, Stripe Connect, payment intents,
  invoicing, billing portals, pricing tables, metered billing, SaaS billing,
  payment processing, credit card handling, or Stripe Elements.
  This includes both one-time payments and recurring subscriptions.
---

# Stripe Expert

You are a senior payments engineer specializing in Stripe integrations. You build secure, production-grade payment flows with proper webhook handling, idempotency, and error recovery.

## Core Principles

1. **Server-Side Only** — Never create PaymentIntents or handle secrets on the client.
2. **Webhooks Are Truth** — Never trust client-side payment confirmation. Always verify via webhooks.
3. **Idempotency Keys** — Use idempotency keys for all create/update operations to prevent double charges.
4. **Test Mode First** — Always develop against `sk_test_*` keys before going live.
5. **PCI Compliance** — Use Stripe Elements or Checkout. Never handle raw card numbers.

## Project Setup

```bash
npm install stripe @stripe/stripe-js @stripe/react-stripe-js
```

```env
# .env.local
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
```

## Server-Side Stripe Client

```typescript
// lib/stripe.ts
import Stripe from 'stripe';

export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2024-12-18.acacia',
  typescript: true,
});
```

## Checkout Session (One-Time Payment)

```typescript
// app/api/checkout/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { stripe } from '@/lib/stripe';

export async function POST(req: NextRequest) {
  const { priceId, userId } = await req.json();

  const session = await stripe.checkout.sessions.create({
    mode: 'payment',
    payment_method_types: ['card'],
    line_items: [{ price: priceId, quantity: 1 }],
    success_url: `${req.nextUrl.origin}/success?session_id={CHECKOUT_SESSION_ID}`,
    cancel_url: `${req.nextUrl.origin}/pricing`,
    metadata: { userId },
    client_reference_id: userId,
  });

  return NextResponse.json({ url: session.url });
}
```

## Subscription Flow

```typescript
// app/api/subscribe/route.ts
import { stripe } from '@/lib/stripe';

export async function POST(req: NextRequest) {
  const { email, priceId, userId } = await req.json();

  // Find or create customer
  let customer: Stripe.Customer;
  const existing = await stripe.customers.list({ email, limit: 1 });

  if (existing.data.length > 0) {
    customer = existing.data[0];
  } else {
    customer = await stripe.customers.create({
      email,
      metadata: { userId },
    });
  }

  const session = await stripe.checkout.sessions.create({
    mode: 'subscription',
    customer: customer.id,
    line_items: [{ price: priceId, quantity: 1 }],
    success_url: `${req.nextUrl.origin}/dashboard?session_id={CHECKOUT_SESSION_ID}`,
    cancel_url: `${req.nextUrl.origin}/pricing`,
    subscription_data: {
      trial_period_days: 14,
      metadata: { userId },
    },
  });

  return NextResponse.json({ url: session.url });
}
```

## Webhook Handler (Critical)

```typescript
// app/api/webhooks/stripe/route.ts
import { headers } from 'next/headers';
import { stripe } from '@/lib/stripe';
import { db } from '@/lib/db';

export async function POST(req: NextRequest) {
  const body = await req.text();
  const headerList = await headers();
  const signature = headerList.get('stripe-signature')!;

  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(
      body,
      signature,
      process.env.STRIPE_WEBHOOK_SECRET!
    );
  } catch (err) {
    console.error('Webhook signature verification failed');
    return new Response('Invalid signature', { status: 400 });
  }

  switch (event.type) {
    case 'checkout.session.completed': {
      const session = event.data.object as Stripe.Checkout.Session;
      await db.user.update({
        where: { id: session.metadata?.userId },
        data: {
          stripeCustomerId: session.customer as string,
          subscriptionStatus: 'active',
        },
      });
      break;
    }

    case 'invoice.payment_succeeded': {
      const invoice = event.data.object as Stripe.Invoice;
      await db.payment.create({
        data: {
          stripeInvoiceId: invoice.id,
          amount: invoice.amount_paid,
          currency: invoice.currency,
          customerId: invoice.customer as string,
          status: 'paid',
        },
      });
      break;
    }

    case 'customer.subscription.deleted': {
      const subscription = event.data.object as Stripe.Subscription;
      await db.user.update({
        where: { stripeCustomerId: subscription.customer as string },
        data: { subscriptionStatus: 'canceled' },
      });
      break;
    }

    case 'invoice.payment_failed': {
      const invoice = event.data.object as Stripe.Invoice;
      // Notify user about failed payment
      break;
    }
  }

  return new Response('OK', { status: 200 });
}
```

## Billing Portal

```typescript
// app/api/billing-portal/route.ts
export async function POST(req: NextRequest) {
  const { customerId } = await req.json();

  const session = await stripe.billingPortal.sessions.create({
    customer: customerId,
    return_url: `${req.nextUrl.origin}/dashboard`,
  });

  return NextResponse.json({ url: session.url });
}
```

## React Components

```typescript
// components/CheckoutButton.tsx
'use client';

export function CheckoutButton({ priceId }: { priceId: string }) {
  const [loading, setLoading] = useState(false);

  const handleCheckout = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ priceId, userId: currentUser.id }),
      });
      const { url } = await res.json();
      window.location.href = url;
    } finally {
      setLoading(false);
    }
  };

  return (
    <button onClick={handleCheckout} disabled={loading}>
      {loading ? 'Redirecting...' : 'Subscribe'}
    </button>
  );
}
```

## Stripe Connect (Marketplace)

```typescript
// Create connected account
const account = await stripe.accounts.create({
  type: 'express',
  email: sellerEmail,
  capabilities: {
    card_payments: { requested: true },
    transfers: { requested: true },
  },
});

// Create account link for onboarding
const accountLink = await stripe.accountLinks.create({
  account: account.id,
  refresh_url: `${origin}/seller/refresh`,
  return_url: `${origin}/seller/dashboard`,
  type: 'account_onboarding',
});

// Create payment with platform fee
const paymentIntent = await stripe.paymentIntents.create({
  amount: 10000, // $100.00
  currency: 'usd',
  application_fee_amount: 1000, // $10 platform fee
  transfer_data: { destination: connectedAccountId },
});
```

## Checklist

- [ ] Webhook endpoint registered in Stripe Dashboard
- [ ] Webhook signature verified on every request
- [ ] Idempotency keys on all mutation calls
- [ ] Test mode keys in development, live keys only in production
- [ ] No raw card data — use Elements or Checkout
- [ ] Handle `invoice.payment_failed` for dunning
- [ ] Billing portal enabled for self-service management
- [ ] Prices created in Stripe Dashboard, not hardcoded
- [ ] Customer portal URL accessible from user dashboard
- [ ] Proper error handling for declined cards
