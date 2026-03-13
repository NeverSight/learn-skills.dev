---
name: shopify-billing
description: Guide for implementing Shopify's Billing API in Remix apps using @shopify/shopify-app-remix. Covers subscriptions, one-time purchases, usage-based billing, discounts, and the project's billing implementation patterns.
---

# Shopify Billing Skill

The Billing API allows you to charge merchants for your app using recurring subscriptions or one-time purchases.

> [!IMPORTANT]
> **GraphQL Only**: The REST Billing API is deprecated. Always use the GraphQL Admin API for billing operations.

## Billing Overview

Shopify supports three billing models:

1. **Time-based subscriptions** - Recurring charges at set intervals (30 days or annual)
2. **Usage-based subscriptions** - Charges based on app usage during 30-day cycles
3. **One-time purchases** - Single charges for features or services

---

## Project Implementation Pattern

This project uses `@shopify/shopify-app-remix` (v3.8+) which provides a simplified billing helper. Here's how billing is structured:

```
app/config/plans.ts                    → Plan configurations (prices, limits, features)
app/enums/BillingPlans.ts              → Plan enum values
app/shopify.server.ts                  → Billing config generation
app/routes/billing.subscription.tsx    → Initiate subscription request
app/routes/billing.subscription-confirm.tsx → Handle Shopify confirmation callback
app/routes/app.billing.tsx             → Billing UI and cancellation
```

---

## 1. Plan Configuration (`app/config/plans.ts`)

Define your plans with pricing, intervals, and usage limits:

```typescript
import { BillingInterval } from "@shopify/shopify-app-remix/server";

export interface PlanLimit {
  taggerOperations: number | null; // null = unlimited
  bulkOperations: number | null;
  cleanerOperations: number | null;
  aiRuleGenerator: number | null;
}

export interface PlanConfig {
  id: BillingPlans | "Free";
  name: string;
  price: number;
  interval: BillingInterval | "Forever";
  currency: string;
  features: string[];
  limits: PlanLimit;
  isAnnual: boolean;
  label?: string;
}

export const PLANS: Record<string, PlanConfig> = {
  Free: {
    id: "Free",
    name: "Free",
    price: 0,
    interval: "Forever" as const,
    currency: "USD",
    features: ["200 Tagger tags/month", "500 Bulk Operations/month"],
    limits: { taggerOperations: 200, bulkOperations: 500, ... },
    isAnnual: false,
  },
  Basic: {
    id: BillingPlans.Basic,
    name: "Basic",
    price: 4.99,
    interval: BillingInterval.Every30Days,
    currency: "USD",
    features: ["2,000 Tagger tags/month", "Unlimited AI"],
    limits: { taggerOperations: 2000, aiRuleGenerator: null, ... },
    isAnnual: false,
  },
  Pro: {
    id: BillingPlans.Pro,
    name: "Pro",
    price: 14.99,
    interval: BillingInterval.Every30Days,
    currency: "USD",
    features: ["Everything unlimited", "Priority Support"],
    limits: { taggerOperations: null, bulkOperations: null, ... },
    isAnnual: false,
    label: "Best Value",
  },
};
```

---

## 2. Billing Config in `shopify.server.ts`

Generate billing config from PLANS for the Shopify app:

```typescript
import { PLANS } from "./config/plans";

// Generate billing config from PLANS
// Format compatible with @shopify/shopify-app-remix v3.8+ billing.request()
const billingConfig: any = {};
Object.values(PLANS).forEach((plan) => {
  if (plan.id !== "Free" && plan.interval !== "Forever") {
    billingConfig[plan.id] = {
      amount: plan.price,
      currencyCode: plan.currency,
      interval: plan.interval,
      trialDays: 7,  // Free trial for all paid plans
      // lineItems can be overridden during billing.request() for coupons/discounts
      lineItems: [
        {
          interval: plan.interval,
          amount: plan.price,
          currencyCode: plan.currency,
        },
      ],
    };
  }
});

const shopify = shopifyApp({
  // ... other config
  billing: billingConfig,
});
```

---

## 3. Initiate Subscription (`billing.subscription.tsx`)

Create a subscription request with optional coupon discounts:

```typescript
import type { LoaderFunctionArgs } from '@remix-run/node';
import { redirect } from '@remix-run/node';
import { BillingInterval } from '@shopify/shopify-app-remix/server';
import { authenticate, BillingPlans } from '~/shopify.server';
import { getMyshopify } from '~/utils/get-myshopify';

// Coupon configuration
const COUPONS = {
  FIRST50: {
    discountPercentage: 0.5,  // 50% off
    durationLimitInIntervals: 1,  // 1 billing cycle
    oneTimeUse: true,
  },
  WELCOME30: {
    discountPercentage: 0.3,  // 30% off
    durationLimitInIntervals: 2,  // 2 billing cycles
    oneTimeUse: true,
  },
} as const;

export const loader = async ({ request }: LoaderFunctionArgs) => {
  const { billing, session } = await authenticate.admin(request);
  const myshopify = getMyshopify(session.shop);
  const url = new URL(request.url);
  const plan = url.searchParams.get('plan') as BillingPlans;
  const couponCode = url.searchParams.get('coupon')?.toUpperCase();

  // Validate plan
  const planConfig = PLANS[plan];
  if (!planConfig || planConfig.id === 'Free') {
    return { status: 0 };
  }

  // Check coupon usage
  let couponApplied = false;
  let appliedCoupon: typeof COUPONS[keyof typeof COUPONS] | null = null;

  if (couponCode && couponCode in COUPONS) {
    const coupon = COUPONS[couponCode as keyof typeof COUPONS];

    if (coupon.oneTimeUse) {
      const settings = await Settings.findOne({ shop: session.shop });
      const alreadyUsed = settings?.usedCoupons?.some(
        (c: { code: string }) => c.code === couponCode
      );

      if (alreadyUsed) {
        return redirect(`/app/billing?error=coupon_already_used&code=${couponCode}`);
      }
    }

    appliedCoupon = coupon;
    couponApplied = true;
  }

  // Build billing request
  const billingOptions: Parameters<typeof billing.request>[0] = {
    plan: plan,
    isTest: process.env.NODE_ENV !== 'production',
    returnUrl: `https://admin.shopify.com/store/${myshopify}/apps/${process.env.SHOPIFY_API_KEY}/billing/subscription-confirm?plan=${plan}${couponApplied ? `&coupon=${couponCode}` : ''}`,
    // Use STANDARD for smart replacement behavior
    // - Immediate for upgrades
    // - Deferred for downgrades
    replacementBehavior: 'STANDARD',
  };

  // Apply coupon discount via lineItems override
  if (couponApplied && appliedCoupon && couponCode) {
    if (planConfig.interval === BillingInterval.Every30Days ||
        planConfig.interval === BillingInterval.Annual) {
      billingOptions.lineItems = [
        {
          interval: planConfig.interval,
          discount: {
            durationLimitInIntervals: appliedCoupon.durationLimitInIntervals,
            value: {
              percentage: appliedCoupon.discountPercentage,
            },
          },
        },
      ];
    }
  }

  await billing.request(billingOptions);

  // Log activity
  await ActivityService.createLog({
    shop: session.shop,
    resourceType: "Billing",
    resourceId: plan,
    action: "Billing Request",
    detail: `${plan} plan subscription requested${couponApplied && appliedCoupon ? ` with coupon ${couponCode} (${appliedCoupon.discountPercentage * 100}% off)` : ''}`,
    status: "Success",
  });

  return null;
};
```

---

## 4. Confirm Subscription (`billing.subscription-confirm.tsx`)

Handle the callback after merchant approves the charge:

```typescript
export const loader = async ({ request }: LoaderFunctionArgs) => {
  const { session, billing } = await authenticate.admin(request);
  const url = new URL(request.url);
  const plan = url.searchParams.get('plan') as BillingPlans;
  const couponCode = url.searchParams.get('coupon')?.toUpperCase();

  try {
    // Verify subscription is active
    const billingCheck = await billing.check({
      plans: [plan],
      isTest: process.env.NODE_ENV !== 'production',
    });

    if (billingCheck.hasActivePayment) {
      // Update shop's plan in database
      await shopService.updateApp(session.shop, APP_ID, {
        plan: plan,
        accessToken: session.accessToken,
      });

      // Record coupon usage
      if (couponCode) {
        await Settings.findOneAndUpdate(
          { shop: session.shop },
          {
            $push: {
              usedCoupons: {
                code: couponCode,
                usedAt: new Date(),
                plan: plan,
              },
            },
          },
          { upsert: true }
        );
      }

      await ActivityService.createLog({
        shop: session.shop,
        resourceType: "Billing",
        resourceId: plan,
        action: "Billing Confirmed",
        detail: `${plan} plan subscription confirmed and activated${couponCode ? ` with coupon ${couponCode}` : ''}`,
        status: "Success",
      });

      // Log subscription ID for tracking
      if (billingCheck.appSubscriptions?.[0]?.id) {
        console.log(`[Billing] Subscription activated: ${billingCheck.appSubscriptions[0].id} for ${session.shop}`);
      }
    }

    return redirect('/app/billing');
  } catch (error) {
    console.error("Error verifying billing:", error);
    return redirect('/app/billing');
  }
};
```

---

## 5. Check Subscription Status

### Using `billing.check()` (Non-blocking)

```typescript
export const loader = async ({ request }) => {
  const { billing, session } = await authenticate.admin(request);

  const billingCheck = await billing.check({
    plans: ["Basic", "Pro"],
    isTest: true,
  });

  if (billingCheck.hasActivePayment) {
    const subscription = billingCheck.appSubscriptions[0];
    // Access subscription details
  }

  return { hasActivePayment: billingCheck.hasActivePayment };
};
```

### Using `billing.require()` (Blocking)

```typescript
export const loader = async ({ request }) => {
  const { billing, session } = await authenticate.admin(request);

  const billingCheck = await billing.require({
    plans: ["Basic", "Pro"],
    isTest: true,
    onFailure: async () => {
      // Redirect to billing page or show upgrade prompt
      return redirect('/app/billing?prompt=upgrade');
    },
  });

  // If we reach here, shop has active subscription
  const subscription = billingCheck.appSubscriptions[0];
  return { subscription };
};
```

---

## 6. Cancel Subscription

```typescript
export const action = async ({ request }) => {
  const { billing, session } = await authenticate.admin(request);
  const formData = await request.formData();
  const plan = formData.get("plan") as BillingPlans;

  if (request.method === 'DELETE') {
    try {
      const billingCheck = await billing.require({
        plans: [plan],
        onFailure: async () => {
          throw new Error('No plan active');
        },
      });

      const subscription = billingCheck.appSubscriptions[0];
      console.log(`[Billing] Cancelling subscription ${subscription.id} for ${session.shop}`);

      await billing.cancel({
        subscriptionId: subscription.id,
        isTest: process.env.NODE_ENV !== 'production',
        prorate: true, // Issue prorated credit for unused portion
      });

      // Update shop to free plan
      await shopService.updateApp(session.shop, APP_ID, {
        plan: "free",
      });

      await ActivityService.createLog({
        shop: session.shop,
        resourceType: "Billing",
        resourceId: plan,
        action: "Billing Cancelled",
        detail: `${plan} plan subscription cancelled`,
        status: "Success",
      });

      return redirect('/app/billing');
    } catch (error) {
      throw error;
    }
  }
};
```

---

## 7. Billing UI Example (`app.billing.tsx`)

Key patterns for the billing interface:

```typescript
export const loader = async ({ request }) => {
  const { session } = await authenticate.admin(request);

  // Get current usage and plan
  const [usage, plan, settings] = await Promise.all([
    UsageService.getCurrentUsage(session.shop),
    UsageService.getPlanType(session.shop),
    Settings.findOne({ shop: session.shop })
  ]);

  const planConfig = PLANS[plan] || PLANS.Free;
  const limits = planConfig.limits;

  return json({ usage, plan, limits });
};

// In your component:
// - Display usage progress bars
// - Show plan comparison with monthly/annual toggle
// - Include coupon input field
// - Handle upgrade/downgrade actions
```

**Subscription URL Pattern:**
```typescript
// Build subscription URL with coupon
const subscriptionUrl = couponCode
  ? `/billing/subscription?plan=${planConfig.id}&coupon=${encodeURIComponent(couponCode)}`
  : `/billing/subscription?plan=${planConfig.id}`;

// Button links to subscription URL
<Button url={subscriptionUrl}>Upgrade</Button>
```

---

## 8. Billing Helper API Reference

### `billing.request(options)`

Initiates a subscription charge. Returns a confirmation URL.

```typescript
await billing.request({
  plan: string,                    // Plan ID from billingConfig
  isTest: boolean,                 // Enable test mode
  returnUrl: string,               // Merchant redirect after approval
  replacementBehavior?: 'STANDARD' | 'APPLY_IMMEDIATELY' | 'APPLY_ON_NEXT_BILLING_CYCLE',
  lineItems?: Array<{             // Optional: override for discounts
    interval: BillingInterval,
    discount?: {
      durationLimitInIntervals: number,
      value: {
        percentage: number,        // 0.5 = 50%
        amount?: { amount: number, currencyCode: string }
      }
    }
  }>
});
```

### `billing.check(options)`

Checks if shop has active subscription (non-blocking).

```typescript
const result = await billing.check({
  plans: string[],                 // Plan IDs to check
  isTest: boolean,
});

// Returns: { hasActivePayment: boolean, appSubscriptions: [...] }
```

### `billing.require(options)`

Checks subscription and throws if not active (blocking).

```typescript
const result = await billing.require({
  plans: string[],
  isTest: boolean,
  onFailure: async () => {
    // Called when no active subscription
    // Return redirect or throw error
  }
});
```

### `billing.cancel(options)`

Cancels an active subscription.

```typescript
await billing.cancel({
  subscriptionId: string,
  isTest: boolean,
  prorate: boolean,                // Credit merchant for unused time
});
```

---

## 9. Replacement Behaviors

Control how new subscriptions interact with existing ones:

| Behavior | Description |
|----------|-------------|
| `STANDARD` | Smart default: immediate for upgrades, deferred for downgrades |
| `APPLY_IMMEDIATELY` | Cancel current subscription immediately |
| `APPLY_ON_NEXT_BILLING_CYCLE` | Wait until current cycle ends |

**Example:**
```typescript
// For plan upgrades/downgrades
billingOptions.replacementBehavior = 'STANDARD';

// For immediate plan changes (e.g., merchant request)
billingOptions.replacementBehavior = 'APPLY_IMMEDIATELY';

// To avoid mid-cycle charges
billingOptions.replacementBehavior = 'APPLY_ON_NEXT_BILLING_CYCLE';
```

---

## 10. Webhooks

Subscribe to these webhook topics to monitor billing events:

| Webhook Topic | Description |
|---------------|-------------|
| `APP_SUBSCRIPTIONS_UPDATE` | Subscription status changes (activated, cancelled, etc.) |
| `APP_PURCHASES_ONE_TIME_UPDATE` | One-time purchase status changes |
| `APP_SUBSCRIPTIONS_APPROACHING_CAPPED_AMOUNT` | Usage reaches 90% of cap |

### Webhook Handler Example

```typescript
// app/routes/webhooks.appSubscriptionsUpdate.tsx
export const action = async ({ request }) => {
  const { topic, shop, payload } = await authenticate.webhook(request);

  if (topic === "APP_SUBSCRIPTIONS_UPDATE") {
    const subscription = payload.appSubscription;

    if (subscription.status === "CANCELLED") {
      // Handle cancellation - revoke access
      await shopService.updateApp(shop, APP_ID, { plan: "free" });
    } else if (subscription.status === "ACTIVE") {
      // Grant access to features
      console.log(`Subscription activated for shop ${shop}`);
    }
  }

  return new Response(JSON.stringify({ success: true }));
};
```

---

## 11. Best Practices

### Test Mode
```typescript
// Always use test mode in development
isTest: process.env.NODE_ENV !== 'production' || session.shop === process.env.SHOP_ADMIN
```

### Confirmation URL
- **MUST redirect** merchant to confirmation URL
- Charge is NOT active until merchant approves
- After approval, merchant redirects to your `returnUrl`

### Coupon System
- Store used coupons in database for one-time use
- Check usage before applying discount
- Log coupon usage for analytics

### Subscription Management
- An app can have only **one active subscription** per merchant
- Creating a new subscription replaces the existing one
- Use `replacementBehavior` to control timing
- Handle `APP_SUBSCRIPTIONS_UPDATE` webhook for cancellations

### Proration
```typescript
// Always prorate when cancelling for better UX
await billing.cancel({
  subscriptionId: subscription.id,
  prorate: true,  // Issue credit for unused time
});
```

### Error Handling
- Always check `userErrors` in mutation responses
- Handle declined charges gracefully
- Provide clear messaging about billing status
- Log all billing events for debugging

---

## 12. Common Patterns

### Plan Upgrade with Discount
```typescript
// /billing/subscription?plan=Pro&coupon=WELCOME30
// → 30% off for 2 billing cycles
```

### Switch Billing Cycle
```typescript
// From Monthly to Annual
billing.request({
  plan: "ProAnnual",
  replacementBehavior: 'STANDARD',  // Shopify will handle timing
});
```

### Downgrade to Free
```typescript
// Cancel paid subscription
await billing.cancel({
  subscriptionId: subscription.id,
  prorate: true,
});
// Then update shop to free plan
```

---

## 13. Project-Specific Notes

- **Trial Days**: All paid plans get 7-day free trial
- **Test Mode**: Automatically enabled in non-production
- **Proration**: Enabled for all cancellations
- **Coupon Storage**: `Settings.usedCoupons` array
- **Plan Storage**: `shops.app[].plan` field
- **VIP Status**: Separate system for gifted plans

---

## Resources

- [Shopify Billing Overview](https://shopify.dev/docs/apps/launch/billing)
- [Time-Based Subscriptions](https://shopify.dev/docs/apps/launch/billing/subscription-billing/create-time-based-subscriptions)
- [Usage-Based Subscriptions](https://shopify.dev/docs/apps/launch/billing/subscription-billing/create-usage-based-subscriptions)
- [One-Time Purchases](https://shopify.dev/docs/apps/launch/billing/support-one-time-purchases)
- [Subscription Discounts](https://shopify.dev/docs/apps/launch/billing/subscription-billing/offer-subscription-discounts)
- [Shopify App Remix Billing](https://github.com/Shopify/shopify-app-template-remix/tree/main/app%2Froutes)
