---
name: subscription-integration
description: Guide for implementing subscription billing with Dodo Payments - trials, upgrades, downgrades, and on-demand billing.
---

# Dodo Payments Subscription Integration

**Reference: [docs.dodopayments.com/developer-resources/subscription-integration-guide](https://docs.dodopayments.com/developer-resources/subscription-integration-guide)**

Implement recurring billing with trials, plan changes, and usage-based pricing.

---

## Quick Start

### 1. Create Subscription Product
In the dashboard (Products → Create Product):
- Select "Subscription" type
- Set billing interval (monthly, yearly, etc.)
- Configure pricing

### 2. Create Checkout Session

```typescript
import DodoPayments from 'dodopayments';

const client = new DodoPayments({
  bearerToken: process.env.DODO_PAYMENTS_API_KEY,
});

const session = await client.checkoutSessions.create({
  product_cart: [
    { product_id: 'prod_monthly_plan', quantity: 1 }
  ],
  subscription_data: {
    trial_period_days: 14, // Optional trial
  },
  customer: {
    email: 'subscriber@example.com',
    name: 'Jane Doe',
  },
  return_url: 'https://yoursite.com/success',
});

// Redirect to session.checkout_url
```

### 3. Handle Webhook Events
```typescript
// subscription.active - Grant access
// subscription.cancelled - Schedule access revocation
// subscription.renewed - Log renewal
// payment.succeeded - Track payments
```

---

## Subscription Lifecycle

```
┌─────────────┐     ┌─────────┐     ┌────────┐
│   Created   │ ──▶ │  Trial  │ ──▶ │ Active │
└─────────────┘     └─────────┘     └────────┘
                                         │
                    ┌────────────────────┼────────────────────┐
                    ▼                    ▼                    ▼
              ┌──────────┐        ┌───────────┐        ┌───────────┐
              │ On Hold  │        │ Cancelled │        │  Renewed  │
              └──────────┘        └───────────┘        └───────────┘
                    │                    │
                    ▼                    ▼
              ┌──────────┐        ┌───────────┐
              │  Failed  │        │  Expired  │
              └──────────┘        └───────────┘
```

---

## Webhook Events

| Event | When | Action |
|-------|------|--------|
| `subscription.active` | Subscription starts | Grant access |
| `subscription.updated` | Any field changes | Sync state |
| `subscription.on_hold` | Payment fails | Notify user, retry |
| `subscription.renewed` | Successful renewal | Log, send receipt |
| `subscription.plan_changed` | Upgrade/downgrade | Update entitlements |
| `subscription.cancelled` | User cancels | Schedule end of access |
| `subscription.failed` | Mandate creation fails | Notify, retry options |
| `subscription.expired` | Term ends | Revoke access |

---

## Implementation Examples

### Full Subscription Handler

```typescript
// app/api/webhooks/subscription/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';

export async function POST(req: NextRequest) {
  const event = await req.json();
  const data = event.data;

  switch (event.type) {
    case 'subscription.active':
      await handleSubscriptionActive(data);
      break;
    case 'subscription.cancelled':
      await handleSubscriptionCancelled(data);
      break;
    case 'subscription.on_hold':
      await handleSubscriptionOnHold(data);
      break;
    case 'subscription.renewed':
      await handleSubscriptionRenewed(data);
      break;
    case 'subscription.plan_changed':
      await handlePlanChanged(data);
      break;
    case 'subscription.expired':
      await handleSubscriptionExpired(data);
      break;
  }

  return NextResponse.json({ received: true });
}

async function handleSubscriptionActive(data: any) {
  const {
    subscription_id,
    customer,
    product_id,
    next_billing_date,
    recurring_pre_tax_amount,
    payment_frequency_interval,
  } = data;

  // Create or update user subscription
  await prisma.subscription.upsert({
    where: { externalId: subscription_id },
    create: {
      externalId: subscription_id,
      userId: customer.customer_id,
      email: customer.email,
      productId: product_id,
      status: 'active',
      currentPeriodEnd: new Date(next_billing_date),
      amount: recurring_pre_tax_amount,
      interval: payment_frequency_interval,
    },
    update: {
      status: 'active',
      currentPeriodEnd: new Date(next_billing_date),
    },
  });

  // Grant access
  await prisma.user.update({
    where: { id: customer.customer_id },
    data: { 
      subscriptionStatus: 'active',
      plan: product_id,
    },
  });

  // Send welcome email
  await sendWelcomeEmail(customer.email, product_id);
}

async function handleSubscriptionCancelled(data: any) {
  const { subscription_id, customer, cancelled_at, cancel_at_next_billing_date } = data;

  await prisma.subscription.update({
    where: { externalId: subscription_id },
    data: {
      status: 'cancelled',
      cancelledAt: new Date(cancelled_at),
      // Keep access until end of billing period if cancel_at_next_billing_date
      accessEndsAt: cancel_at_next_billing_date 
        ? new Date(data.next_billing_date) 
        : new Date(),
    },
  });

  // Send cancellation email
  await sendCancellationEmail(customer.email, cancel_at_next_billing_date);
}

async function handleSubscriptionOnHold(data: any) {
  const { subscription_id, customer } = data;

  await prisma.subscription.update({
    where: { externalId: subscription_id },
    data: { status: 'on_hold' },
  });

  // Notify user about payment issue
  await sendPaymentFailedEmail(customer.email);
}

async function handleSubscriptionRenewed(data: any) {
  const { subscription_id, next_billing_date } = data;

  await prisma.subscription.update({
    where: { externalId: subscription_id },
    data: {
      status: 'active',
      currentPeriodEnd: new Date(next_billing_date),
    },
  });
}

async function handlePlanChanged(data: any) {
  const { subscription_id, product_id, recurring_pre_tax_amount } = data;

  await prisma.subscription.update({
    where: { externalId: subscription_id },
    data: {
      productId: product_id,
      amount: recurring_pre_tax_amount,
    },
  });

  // Update user entitlements based on new plan
  await updateUserEntitlements(subscription_id, product_id);
}

async function handleSubscriptionExpired(data: any) {
  const { subscription_id, customer } = data;

  await prisma.subscription.update({
    where: { externalId: subscription_id },
    data: { status: 'expired' },
  });

  // Revoke access
  await prisma.user.update({
    where: { id: customer.customer_id },
    data: { 
      subscriptionStatus: 'expired',
      plan: null,
    },
  });
}
```

### Subscription with Trial

```typescript
const session = await client.checkoutSessions.create({
  product_cart: [
    { product_id: 'prod_pro_monthly', quantity: 1 }
  ],
  subscription_data: {
    trial_period_days: 14,
  },
  customer: {
    email: 'user@example.com',
    name: 'John Doe',
  },
  return_url: 'https://yoursite.com/welcome',
});
```

### Customer Portal for Self-Service

Allow customers to manage their subscription:

```typescript
// Create portal session
const portal = await client.customers.createPortalSession({
  customer_id: 'cust_xxxxx',
  return_url: 'https://yoursite.com/account',
});

// Redirect to portal.url
```

Portal features:
- View subscription details
- Update payment method
- Cancel subscription
- View billing history

---

## On-Demand (Usage-Based) Subscriptions

For metered/usage-based billing:

### Create Subscription with Mandate

```typescript
const session = await client.checkoutSessions.create({
  product_cart: [
    { product_id: 'prod_usage_based', quantity: 1 }
  ],
  customer: { email: 'user@example.com' },
  return_url: 'https://yoursite.com/success',
});
```

### Charge for Usage

```typescript
// When usage occurs, create a charge
const charge = await client.subscriptions.charge({
  subscription_id: 'sub_xxxxx',
  amount: 1500, // $15.00 in cents
  description: 'API calls for January 2025',
});
```

### Track Usage Events

```typescript
// payment.succeeded - Charge succeeded
// payment.failed - Charge failed, implement retry logic
```

---

## Plan Changes

### Upgrade/Downgrade Flow

```typescript
// Get available plans
const plans = await client.products.list({
  type: 'subscription',
});

// Change plan
await client.subscriptions.update({
  subscription_id: 'sub_xxxxx',
  product_id: 'prod_new_plan',
  proration_behavior: 'create_prorations', // or 'none'
});
```

### Handling `subscription.plan_changed`

```typescript
async function handlePlanChanged(data: any) {
  const { subscription_id, product_id, customer } = data;
  
  // Map product to features/limits
  const planFeatures = getPlanFeatures(product_id);
  
  await prisma.user.update({
    where: { externalId: customer.customer_id },
    data: {
      plan: product_id,
      features: planFeatures,
      apiLimit: planFeatures.apiLimit,
      storageLimit: planFeatures.storageLimit,
    },
  });
}
```

---

## Access Control Pattern

### Middleware Example (Next.js)

```typescript
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export async function middleware(request: NextRequest) {
  // Check subscription status
  const session = await getSession(request);
  
  if (!session?.user) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  const subscription = await getSubscription(session.user.id);

  // Check if accessing premium feature
  if (request.nextUrl.pathname.startsWith('/dashboard/pro')) {
    if (!subscription || subscription.status !== 'active') {
      return NextResponse.redirect(new URL('/pricing', request.url));
    }
    
    // Check if plan includes this feature
    if (!subscription.features.includes('pro')) {
      return NextResponse.redirect(new URL('/upgrade', request.url));
    }
  }

  return NextResponse.next();
}
```

### React Hook for Subscription State

```typescript
// hooks/useSubscription.ts
import useSWR from 'swr';

export function useSubscription() {
  const { data, error, mutate } = useSWR('/api/subscription', fetcher);

  return {
    subscription: data,
    isLoading: !error && !data,
    isError: error,
    isActive: data?.status === 'active',
    isPro: data?.plan?.includes('pro'),
    refresh: mutate,
  };
}

// Usage in component
function PremiumFeature() {
  const { isActive, isPro } = useSubscription();

  if (!isActive) {
    return <UpgradePrompt />;
  }

  if (!isPro) {
    return <ProUpgradePrompt />;
  }

  return <ActualFeature />;
}
```

---

## Common Patterns

### Grace Period for Failed Payments

```typescript
async function handleSubscriptionOnHold(data: any) {
  const gracePeriodDays = 7;
  
  await prisma.subscription.update({
    where: { externalId: data.subscription_id },
    data: {
      status: 'on_hold',
      gracePeriodEnds: new Date(Date.now() + gracePeriodDays * 24 * 60 * 60 * 1000),
    },
  });

  // Schedule job to revoke access after grace period
  await scheduleAccessRevocation(data.subscription_id, gracePeriodDays);
}
```

### Prorated Upgrades

When upgrading mid-cycle:
```typescript
// Dodo handles proration automatically
// Customer pays difference for remaining days
await client.subscriptions.update({
  subscription_id: 'sub_xxxxx',
  product_id: 'prod_higher_plan',
  proration_behavior: 'create_prorations',
});
```

### Cancellation with End-of-Period Access

```typescript
// subscription.cancelled event includes:
// - cancel_at_next_billing_date: boolean
// - next_billing_date: string (when access should end)

if (data.cancel_at_next_billing_date) {
  // Keep access until next_billing_date
  await scheduleAccessRevocation(
    data.subscription_id, 
    new Date(data.next_billing_date)
  );
}
```

---

## Testing

### Test Scenarios
1. New subscription → `subscription.active`
2. Renewal success → `subscription.renewed` + `payment.succeeded`
3. Renewal failure → `subscription.on_hold` + `payment.failed`
4. Plan upgrade → `subscription.plan_changed`
5. Cancellation → `subscription.cancelled`
6. Expiration → `subscription.expired`

### Test in Dashboard
Use test mode and trigger events manually from the webhook settings.

---

## Resources

- [Subscription Guide](https://docs.dodopayments.com/developer-resources/subscription-integration-guide)
- [On-Demand Subscriptions](https://docs.dodopayments.com/developer-resources/ondemand-subscriptions)
- [Webhook Events](https://docs.dodopayments.com/developer-resources/webhooks/intents/subscription)
- [Customer Portal](https://docs.dodopayments.com/developer-resources/customer-portal)
