---
name: billing-sdk
description: Guide for using BillingSDK - open-source React components for pricing tables, subscription management, and billing UI with Dodo Payments.
---

# BillingSDK Integration

**Reference: [docs.dodopayments.com/developer-resources/billingsdk](https://docs.dodopayments.com/developer-resources/billingsdk) | [billingsdk.com](https://billingsdk.com)**

BillingSDK provides open-source, customizable React components for billing interfaces - pricing tables, subscription management, usage meters, and more.

---

## Overview

BillingSDK offers:
- **React Components**: Pre-built, customizable billing components
- **CLI Tooling**: Project initialization and component management
- **Framework Support**: Next.js, Express.js, Hono, Fastify, React
- **Payment Provider**: Full integration with Dodo Payments

---

## Quick Start Options

### Option 1: New Project (Recommended)
Complete project setup with framework configuration and API routes:

```bash
npx @billingsdk/cli init
```

The CLI will:
- Configure your framework (Next.js App Router)
- Set up Dodo Payments integration
- Generate API routes for checkout, customers, webhooks
- Install dependencies
- Create configuration files

### Option 2: Add to Existing Project
Add individual components using the CLI:

```bash
npx @billingsdk/cli add pricing-table-one
npx @billingsdk/cli add subscription-management
npx @billingsdk/cli add usage-meter-circle
```

### Option 3: Manual via shadcn/ui
Install directly using shadcn registry:

```bash
npx shadcn@latest add @billingsdk/pricing-table-one
```

---

## CLI Reference

### Initialize Project

```bash
npx @billingsdk/cli init
```

Interactive setup prompts:
1. Select framework (Next.js, Express.js, Hono, Fastify, React)
2. Select payment provider (Dodo Payments)
3. Configure project settings

### Add Components

```bash
npx @billingsdk/cli add <component-name>
```

**Available components:**
- `pricing-table-one` - Simple pricing table
- `pricing-table-two` - Feature-rich pricing table
- `subscription-management` - Manage active subscriptions
- `usage-meter-circle` - Circular usage visualization
- More components available...

### What happens when adding:
1. Downloads component from registry
2. Installs files to `components/billingsdk/`
3. Updates project configuration
4. Installs additional dependencies

---

## Components

### Pricing Table One

Simple, clean pricing table for displaying plans.

**Installation:**
```bash
npx @billingsdk/cli add pricing-table-one
# or
npx shadcn@latest add @billingsdk/pricing-table-one
```

**Usage:**
```tsx
import { PricingTableOne } from "@/components/billingsdk/pricing-table-one";

const plans = [
  {
    id: 'prod_free',
    name: 'Free',
    price: 0,
    interval: 'month',
    features: ['5 projects', 'Basic support'],
  },
  {
    id: 'prod_pro',
    name: 'Pro',
    price: 29,
    interval: 'month',
    features: ['Unlimited projects', 'Priority support', 'API access'],
    popular: true,
  },
  {
    id: 'prod_enterprise',
    name: 'Enterprise',
    price: 99,
    interval: 'month',
    features: ['Everything in Pro', 'Custom integrations', 'Dedicated support'],
  },
];

export function PricingPage() {
  const handleSelectPlan = async (planId: string) => {
    // Create checkout session
    const response = await fetch('/api/checkout', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ productId: planId }),
    });
    
    const { checkoutUrl } = await response.json();
    window.location.href = checkoutUrl;
  };

  return (
    <PricingTableOne 
      plans={plans}
      onSelectPlan={handleSelectPlan}
    />
  );
}
```

### Pricing Table Two

Feature-comparison pricing table with toggle for monthly/yearly.

**Installation:**
```bash
npx @billingsdk/cli add pricing-table-two
```

**Usage:**
```tsx
import { PricingTableTwo } from "@/components/billingsdk/pricing-table-two";

const plans = [
  {
    id: 'prod_starter_monthly',
    yearlyId: 'prod_starter_yearly',
    name: 'Starter',
    monthlyPrice: 19,
    yearlyPrice: 190,
    features: [
      { name: 'Projects', value: '10' },
      { name: 'Storage', value: '5 GB' },
      { name: 'Support', value: 'Email' },
    ],
  },
  {
    id: 'prod_pro_monthly',
    yearlyId: 'prod_pro_yearly',
    name: 'Pro',
    monthlyPrice: 49,
    yearlyPrice: 490,
    popular: true,
    features: [
      { name: 'Projects', value: 'Unlimited' },
      { name: 'Storage', value: '50 GB' },
      { name: 'Support', value: 'Priority' },
    ],
  },
];

export function PricingPage() {
  return (
    <PricingTableTwo 
      plans={plans}
      onSelectPlan={(planId, billingInterval) => {
        console.log(`Selected: ${planId}, Interval: ${billingInterval}`);
      }}
    />
  );
}
```

### Subscription Management

Allow users to view and manage their subscription.

**Installation:**
```bash
npx @billingsdk/cli add subscription-management
```

**Usage:**
```tsx
import { SubscriptionManagement } from "@/components/billingsdk/subscription-management";

export function AccountPage() {
  const subscription = {
    plan: 'Pro',
    status: 'active',
    currentPeriodEnd: '2025-02-21',
    amount: 49,
    interval: 'month',
  };

  return (
    <SubscriptionManagement 
      subscription={subscription}
      onManageBilling={async () => {
        // Open customer portal
        const response = await fetch('/api/portal', { method: 'POST' });
        const { url } = await response.json();
        window.location.href = url;
      }}
      onCancelSubscription={async () => {
        if (confirm('Are you sure you want to cancel?')) {
          await fetch('/api/subscription/cancel', { method: 'POST' });
        }
      }}
    />
  );
}
```

### Usage Meter

Display usage-based billing metrics.

**Installation:**
```bash
npx @billingsdk/cli add usage-meter-circle
```

**Usage:**
```tsx
import { UsageMeterCircle } from "@/components/billingsdk/usage-meter-circle";

export function UsageDashboard() {
  return (
    <div className="grid grid-cols-3 gap-4">
      <UsageMeterCircle 
        label="API Calls"
        current={8500}
        limit={10000}
        unit="calls"
      />
      <UsageMeterCircle 
        label="Storage"
        current={3.2}
        limit={5}
        unit="GB"
      />
      <UsageMeterCircle 
        label="Bandwidth"
        current={45}
        limit={100}
        unit="GB"
      />
    </div>
  );
}
```

---

## Next.js Integration

### Project Structure (after `init`)

```
your-project/
├── app/
│   ├── api/
│   │   ├── checkout/
│   │   │   └── route.ts
│   │   ├── portal/
│   │   │   └── route.ts
│   │   └── webhooks/
│   │       └── dodo/
│   │           └── route.ts
│   └── pricing/
│       └── page.tsx
├── components/
│   └── billingsdk/
│       ├── pricing-table-one.tsx
│       └── subscription-management.tsx
├── lib/
│   ├── dodo.ts
│   └── billingsdk-config.ts
└── .env.local
```

### Generated API Routes

**Checkout Route (`app/api/checkout/route.ts`):**
```typescript
import { NextRequest, NextResponse } from 'next/server';
import { dodo } from '@/lib/dodo';

export async function POST(req: NextRequest) {
  const { productId, email } = await req.json();

  const session = await dodo.checkoutSessions.create({
    product_cart: [{ product_id: productId, quantity: 1 }],
    customer: { email },
    return_url: `${process.env.NEXT_PUBLIC_APP_URL}/success`,
  });

  return NextResponse.json({ checkoutUrl: session.checkout_url });
}
```

**Portal Route (`app/api/portal/route.ts`):**
```typescript
import { NextRequest, NextResponse } from 'next/server';
import { dodo } from '@/lib/dodo';
import { getSession } from '@/lib/auth';

export async function POST(req: NextRequest) {
  const session = await getSession();
  
  const portal = await dodo.customers.createPortalSession({
    customer_id: session.user.customerId,
    return_url: `${process.env.NEXT_PUBLIC_APP_URL}/account`,
  });

  return NextResponse.json({ url: portal.url });
}
```

### Configuration File

**`lib/billingsdk-config.ts`:**
```typescript
export const plans = [
  {
    id: process.env.NEXT_PUBLIC_PLAN_FREE_ID!,
    name: 'Free',
    description: 'Perfect for trying out',
    price: 0,
    interval: 'month' as const,
    features: [
      '5 projects',
      '1 GB storage',
      'Community support',
    ],
  },
  {
    id: process.env.NEXT_PUBLIC_PLAN_PRO_ID!,
    name: 'Pro',
    description: 'For professionals',
    price: 29,
    interval: 'month' as const,
    popular: true,
    features: [
      'Unlimited projects',
      '50 GB storage',
      'Priority support',
      'API access',
    ],
  },
];

export const config = {
  returnUrl: process.env.NEXT_PUBLIC_APP_URL + '/success',
  portalReturnUrl: process.env.NEXT_PUBLIC_APP_URL + '/account',
};
```

---

## Customization

### Styling with Tailwind

Components use Tailwind CSS and shadcn/ui patterns. Customize via:

1. **Theme variables** in `globals.css`
2. **Direct class overrides** on components
3. **Component source modification** (files are local)

**Example - Custom colors:**
```css
/* globals.css */
@layer base {
  :root {
    --primary: 220 90% 56%;
    --primary-foreground: 0 0% 100%;
  }
}
```

### Component Props

Most components accept standard styling props:

```tsx
<PricingTableOne 
  plans={plans}
  onSelectPlan={handleSelect}
  className="max-w-4xl mx-auto"
  containerClassName="gap-8"
  cardClassName="border-2"
/>
```

---

## Environment Variables

```bash
# .env.local

# Dodo Payments
DODO_PAYMENTS_API_KEY=sk_live_xxxxx
DODO_PAYMENTS_WEBHOOK_SECRET=whsec_xxxxx

# Product IDs (from dashboard)
NEXT_PUBLIC_PLAN_FREE_ID=prod_xxxxx
NEXT_PUBLIC_PLAN_PRO_ID=prod_xxxxx
NEXT_PUBLIC_PLAN_ENTERPRISE_ID=prod_xxxxx

# App
NEXT_PUBLIC_APP_URL=https://yoursite.com
```

---

## Best Practices

### 1. Use Product IDs from Environment
Keep product IDs in environment variables for easy staging/production switching.

### 2. Handle Loading States
Components should show loading states during checkout:

```tsx
const [loading, setLoading] = useState(false);

const handleSelect = async (planId: string) => {
  setLoading(true);
  try {
    const response = await fetch('/api/checkout', {...});
    const { checkoutUrl } = await response.json();
    window.location.href = checkoutUrl;
  } finally {
    setLoading(false);
  }
};
```

### 3. Server-Side Data Fetching
Fetch subscription data server-side when possible:

```tsx
// app/account/page.tsx
import { getSubscription } from '@/lib/subscription';

export default async function AccountPage() {
  const subscription = await getSubscription();
  
  return <SubscriptionManagement subscription={subscription} />;
}
```

### 4. Implement Webhooks
Always use webhooks as source of truth for subscription status, not client-side data.

---

## Resources

- [BillingSDK Documentation](https://billingsdk.com/docs)
- [Dodo Payments Integration](https://docs.dodopayments.com/developer-resources/billingsdk)
- [Component Gallery](https://billingsdk.com/docs/components)
- [GitHub Repository](https://github.com/dodopayments/billingsdk)
