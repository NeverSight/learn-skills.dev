---
name: stripe
description: |
  Use when the user mentions Stripe, Stripe Checkout, Stripe webhooks, payment intents,
  Stripe subscriptions, Stripe API, stripe CLI, payment processing, Stripe products/prices,
  or integrating payments into a web app.
tools: Read, Glob, Grep, Bash, WebFetch
version: 1.0.0
---

# Stripe Skill

Help users integrate Stripe for payments, subscriptions, and billing.

## When to Fetch Live Docs

Use `WebFetch` against `https://docs.stripe.com/...` when:
- User asks about specific API endpoints not covered inline
- Connect/marketplace payments
- Stripe Elements or Payment Element frontend integration
- Billing portal, invoices, or metered billing
- Regional payment methods (SEPA, iDEAL, etc.)

Useful doc URLs:
- API reference: `https://docs.stripe.com/api`
- Checkout quickstart: `https://docs.stripe.com/checkout/quickstart`
- Payment Intents: `https://docs.stripe.com/payments/payment-intents`
- Webhooks: `https://docs.stripe.com/webhooks`
- Subscriptions: `https://docs.stripe.com/billing/subscriptions/overview`
- Products & Prices: `https://docs.stripe.com/products-prices/overview`
- Stripe CLI: `https://docs.stripe.com/stripe-cli`
- Testing: `https://docs.stripe.com/testing`
- Payment Element: `https://docs.stripe.com/payments/payment-element`
- Customer portal: `https://docs.stripe.com/customer-management`
- Connect: `https://docs.stripe.com/connect`
- Idempotent requests: `https://docs.stripe.com/api/idempotent_requests`

---

## Client Setup

```ts
// Server-side (Node.js)
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);
// or
import Stripe from 'stripe';
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);
```

---

## Checkout Sessions

### One-Time Payment

```ts
const session = await stripe.checkout.sessions.create({
  mode: 'payment',
  line_items: [
    {
      price: 'price_xxxxx', // or use price_data for inline
      quantity: 1,
    },
  ],
  success_url: `${YOUR_DOMAIN}/success?session_id={CHECKOUT_SESSION_ID}`,
  cancel_url: `${YOUR_DOMAIN}/cancel`,
  metadata: { userId: '123' }, // passed to webhook
});

// Redirect client to session.url
res.redirect(303, session.url);
```

### Subscription

```ts
const session = await stripe.checkout.sessions.create({
  mode: 'subscription',
  line_items: [{ price: 'price_monthly_xxxxx', quantity: 1 }],
  success_url: `${YOUR_DOMAIN}/success?session_id={CHECKOUT_SESSION_ID}`,
  cancel_url: `${YOUR_DOMAIN}/cancel`,
  customer_email: 'user@example.com', // or customer: 'cus_xxxxx'
});
```

### Inline Price (no pre-created price)

```ts
const session = await stripe.checkout.sessions.create({
  mode: 'payment',
  line_items: [{
    price_data: {
      currency: 'usd',
      product_data: { name: 'Sway Score Lookup' },
      unit_amount: 99, // $0.99 in cents
    },
    quantity: 1,
  }],
  success_url: `${YOUR_DOMAIN}/success`,
  cancel_url: `${YOUR_DOMAIN}/cancel`,
});
```

---

## Webhooks

### Endpoint Handler (Node.js / Serverless)

```ts
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);
const endpointSecret = process.env.STRIPE_WEBHOOK_SECRET;

// CRITICAL: Use raw body, not parsed JSON
export const config = { api: { bodyParser: false } }; // Next.js
// For Vercel serverless: read raw body from request

export default async function handler(req, res) {
  const sig = req.headers['stripe-signature'];
  const rawBody = await getRawBody(req); // or req.body if raw

  let event;
  try {
    event = stripe.webhooks.constructEvent(rawBody, sig, endpointSecret);
  } catch (err) {
    console.error('Webhook signature verification failed:', err.message);
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }

  switch (event.type) {
    case 'checkout.session.completed':
      const session = event.data.object;
      // Fulfill order, update DB
      await handleCheckoutComplete(session);
      break;
    case 'invoice.paid':
      // Subscription payment succeeded
      break;
    case 'invoice.payment_failed':
      // Subscription payment failed
      break;
    case 'customer.subscription.updated':
      // Plan change, cancellation, etc.
      break;
    case 'customer.subscription.deleted':
      // Subscription ended
      break;
    default:
      console.log(`Unhandled event: ${event.type}`);
  }

  res.json({ received: true });
}
```

### Common Events

| Event | When |
|---|---|
| `checkout.session.completed` | Customer finishes Checkout |
| `invoice.paid` | Subscription payment succeeds |
| `invoice.payment_failed` | Subscription payment fails |
| `customer.subscription.created` | New subscription starts |
| `customer.subscription.updated` | Plan changed, renewed, etc. |
| `customer.subscription.deleted` | Subscription canceled/expired |
| `payment_intent.succeeded` | Payment Intent completes |
| `payment_intent.payment_failed` | Payment Intent fails |
| `charge.refunded` | Refund processed |

### Retry Behavior

- **Live mode:** Retries up to 3 days with exponential backoff
- **Sandbox:** Retries 3 times over a few hours
- Return `2xx` quickly — do heavy processing async
- Log `event.id` to deduplicate retries

---

## Products & Prices

```ts
// Create a product
const product = await stripe.products.create({
  name: 'Sway Score Lookup',
  description: 'One-time influence score check',
});

// Create a one-time price
const price = await stripe.prices.create({
  product: product.id,
  unit_amount: 99,     // cents
  currency: 'usd',
});

// Create a recurring price
const monthlyPrice = await stripe.prices.create({
  product: product.id,
  unit_amount: 999,
  currency: 'usd',
  recurring: { interval: 'month' },
});
```

**Sandbox vs Production:** Price IDs differ between modes. Use environment variables:
```bash
STRIPE_PRICE_LOOKUP=price_test_xxx    # sandbox
STRIPE_PRICE_LOOKUP=price_live_xxx    # production
```

---

## Customer Management

```ts
// Create customer
const customer = await stripe.customers.create({
  email: 'user@example.com',
  metadata: { userId: '123' },
});

// Retrieve
const customer = await stripe.customers.retrieve('cus_xxxxx');

// List
const customers = await stripe.customers.list({ limit: 10 });
```

---

## Subscriptions

```ts
// Create (if not using Checkout)
const subscription = await stripe.subscriptions.create({
  customer: 'cus_xxxxx',
  items: [{ price: 'price_xxxxx' }],
  trial_period_days: 14,
});

// Cancel at period end
await stripe.subscriptions.update('sub_xxxxx', {
  cancel_at_period_end: true,
});

// Cancel immediately
await stripe.subscriptions.cancel('sub_xxxxx');

// Change plan
await stripe.subscriptions.update('sub_xxxxx', {
  items: [{
    id: 'si_xxxxx', // subscription item ID
    price: 'price_new_xxxxx',
  }],
  proration_behavior: 'create_prorations',
});
```

---

## Stripe CLI

```bash
# Install (macOS)
brew install stripe/stripe-cli/stripe

# Login
stripe login

# Listen for webhooks locally
stripe listen --forward-to localhost:3000/api/webhooks/stripe

# Trigger test events
stripe trigger checkout.session.completed
stripe trigger payment_intent.succeeded
stripe trigger customer.subscription.created

# View recent events
stripe events list --limit 10

# View logs
stripe logs tail

# Create test resources
stripe products create --name="Test Product"
stripe prices create --product=prod_xxx --unit-amount=999 --currency=usd
```

---

## Testing

### Test Card Numbers

| Card | Behavior |
|---|---|
| `4242 4242 4242 4242` | Succeeds |
| `4000 0000 0000 3220` | 3D Secure required |
| `4000 0000 0000 9995` | Declined (insufficient funds) |
| `4000 0000 0000 0002` | Declined (generic) |
| `4000 0025 0000 3155` | Requires authentication |

Use any future expiry date, any 3-digit CVC, any postal code.

---

## Environment Variables

```bash
STRIPE_SECRET_KEY=sk_test_...          # Server-side only
STRIPE_PUBLISHABLE_KEY=pk_test_...     # Client-side safe
STRIPE_WEBHOOK_SECRET=whsec_...        # For webhook verification
```

---

## Common Gotchas

- **Raw body required:** Webhook signature verification needs the raw request body, not parsed JSON. In Next.js: `export const config = { api: { bodyParser: false } }`. In Vercel serverless: read `req.body` as buffer.
- **Idempotency keys:** Use for POST requests to prevent duplicate charges: `stripe.paymentIntents.create({...}, { idempotencyKey: 'unique-key' })`
- **Sandbox vs live:** All test resources use `_test_` in keys. Switch by changing API key.
- **Webhook timing:** Don't rely on redirect success URL for fulfillment — always use webhooks.
- **Amount in cents:** `unit_amount: 999` = $9.99, not $999.
