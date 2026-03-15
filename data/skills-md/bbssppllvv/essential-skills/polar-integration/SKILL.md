---
name: polar-integration
description: Integrate Polar payments, subscriptions, and checkout into web projects. Use when asked to add payments via Polar, set up Polar checkout, configure Polar webhooks, create Polar products, integrate Polar SDK, set up customer portal, add subscription billing with Polar, or any task involving polar.sh payment platform. Triggers on mentions of Polar payments, Polar checkout, Polar webhooks, Polar subscriptions, @polar-sh/sdk, @polar-sh/nextjs, @polar-sh/checkout.
---

# Polar Integration

Polar is a payment platform for digital products: subscriptions, one-time purchases, licenses, checkout, and webhooks. This skill provides complete integration guidance.

## Integration Workflow

### 1. Determine the Stack

Identify the project's framework. Polar has first-class support for:
- **Next.js** via `@polar-sh/nextjs` — see [references/nextjs.md](references/nextjs.md)
- **SvelteKit** via `@polar-sh/sveltekit` — see [references/sveltekit.md](references/sveltekit.md)
- **Supabase** via `@polar-sh/supabase` — see [references/supabase.md](references/supabase.md)
- **Any JS/TS framework** via `@polar-sh/sdk` — see [references/typescript-sdk.md](references/typescript-sdk.md)
- **Python** via `polar-sdk` — see [references/python-sdk.md](references/python-sdk.md)
- Other framework adapters: Astro, Express, Hono, Fastify, Remix, Nuxt, Elysia, Deno, TanStack Start, Better Auth

### 2. Install Dependencies

```bash
npm install @polar-sh/sdk
# For Next.js projects:
npm install zod @polar-sh/nextjs
# For SvelteKit projects:
npm install zod @polar-sh/sveltekit
# For Supabase projects:
npm install zod @polar-sh/supabase
# For embedded checkout:
npm install @polar-sh/checkout
# For Python projects:
pip install polar-sdk
```

> **Note:** The Polar SDK is in active development. Pin versions to avoid breaking changes:
> `npm install @polar-sh/sdk@^0.46` / `pip install polar-sdk~=0.28`

### 3. Configure Authentication

Set up environment variables:

```bash
POLAR_ACCESS_TOKEN=polar_at_xxx     # Organization Access Token from Polar dashboard
POLAR_WEBHOOK_SECRET=xxx            # Webhook signing secret
```

Create Organization Access Tokens from organization settings in Polar dashboard. See [references/authentication.md](references/authentication.md) for details.

For sandbox/testing, use `server: "sandbox"` in SDK config. For production, use `server: "production"` or omit. See [references/sandbox.md](references/sandbox.md) for sandbox details (test cards, API URLs, limitations).

### 4. Set Up Checkout

Choose approach based on needs:

| Approach | When to Use |
|----------|-------------|
| **Checkout Links** | No-code, shareable URLs |
| **Checkout API** | Programmatic control, dynamic pricing |
| **Embedded Checkout** | Inline on your site, no redirect |

- Checkout Links: [references/checkout-links.md](references/checkout-links.md)
- Checkout API: [references/checkout-api.md](references/checkout-api.md)
- Embedded Checkout: [references/checkout-embedded.md](references/checkout-embedded.md)

**Quick start (Next.js):**

```typescript
// app/checkout/route.ts
import { Checkout } from "@polar-sh/nextjs";

export const GET = Checkout({
  accessToken: process.env.POLAR_ACCESS_TOKEN,
  successUrl: process.env.SUCCESS_URL,
  server: "sandbox",
});
// Use: GET /checkout?products=PRODUCT_ID
```

**Quick start (SDK):**

```typescript
import { Polar } from "@polar-sh/sdk";

const polar = new Polar({
  accessToken: process.env.POLAR_ACCESS_TOKEN,
  server: "sandbox",
});

const checkout = await polar.checkouts.create({
  products: ["PRODUCT_ID"],
});
// Redirect user to checkout.url
```

### 5. Set Up Webhooks

Webhooks notify your app about payment events (order created, subscription canceled, etc.).

**Quick start (Next.js):**

```typescript
// app/api/webhook/polar/route.ts
import { Webhooks } from "@polar-sh/nextjs";

export const POST = Webhooks({
  webhookSecret: process.env.POLAR_WEBHOOK_SECRET!,
  onPayload: async (payload) => {
    // Handle any event
  },
  onOrderCreated: async (payload) => {
    // Handle new order
  },
  onSubscriptionCreated: async (payload) => {
    // Handle new subscription
  },
});
```

**Quick start (Express):**

```typescript
import express from "express";
import { validateEvent, WebhookVerificationError } from "@polar-sh/sdk/webhooks";

app.post("/webhook", express.raw({ type: "application/json" }), (req, res) => {
  try {
    const event = validateEvent(req.body, req.headers, process.env.POLAR_WEBHOOK_SECRET ?? "");
    // Process event
    res.status(202).send("");
  } catch (error) {
    if (error instanceof WebhookVerificationError) res.status(403).send("");
    throw error;
  }
});
```

For webhook setup in Polar dashboard: [references/webhooks-setup.md](references/webhooks-setup.md)
For local development with `polar listen`: [references/webhooks-local.md](references/webhooks-local.md)
For delivery handling, retries, troubleshooting: [references/webhooks-delivery.md](references/webhooks-delivery.md)

### 6. Set Up Customer Portal (Optional)

Give customers access to their orders and subscriptions.

**Next.js:**

```typescript
// app/portal/route.ts
import { CustomerPortal } from "@polar-sh/nextjs";

export const GET = CustomerPortal({
  accessToken: process.env.POLAR_ACCESS_TOKEN,
  getCustomerId: async (req) => "CUSTOMER_ID", // resolve from your auth
  server: "sandbox",
});
```

**SDK:**

```typescript
const session = await polar.customerSessions.create({ customerId: "CUSTOMER_ID" });
// Redirect to session.customerPortalUrl
```

See [references/customer-portal.md](references/customer-portal.md).

## Reference Index

Load these files when you need detailed information on a specific topic:

### SDK & Frameworks
- [references/typescript-sdk.md](references/typescript-sdk.md) — TS/JS SDK installation, quickstart, framework adapters list
- [references/python-sdk.md](references/python-sdk.md) — Python SDK installation, sync/async usage, sandbox config
- [references/nextjs.md](references/nextjs.md) — Next.js route handlers for checkout, portal, webhooks, all webhook handler names
- [references/sveltekit.md](references/sveltekit.md) — SvelteKit integration with `@polar-sh/sveltekit`, file paths, examples
- [references/supabase.md](references/supabase.md) — Supabase Edge Functions integration with `@polar-sh/supabase`

### Authentication
- [references/authentication.md](references/authentication.md) — OAT tokens, security, GitHub secret scanning
- [references/oauth2.md](references/oauth2.md) — OAuth 2.0 flow, authorization code exchange, PKCE, org vs user tokens

### Products & Pricing
- [references/products.md](references/products.md) — Creating products, pricing models, billing cycles, benefits, variants, archiving
- [references/trials.md](references/trials.md) — Free trial periods, abuse prevention, managing trials on existing subscriptions
- [references/seat-based-pricing.md](references/seat-based-pricing.md) — Team/B2B pricing, seat management, claim flow, API examples
- [references/discounts.md](references/discounts.md) — Percentage/fixed discounts, codes, restrictions, recurring options
- [references/custom-fields.md](references/custom-fields.md) — Custom checkout fields (text, number, date, checkbox, select)

### Checkout
- [references/checkout-links.md](references/checkout-links.md) — No-code checkout links, query params, UTM tracking
- [references/checkout-api.md](references/checkout-api.md) — Programmatic checkout sessions, ad-hoc prices, multiple products
- [references/checkout-embedded.md](references/checkout-embedded.md) — Embedded checkout, JS library, React integration, events, wallet payments

### Webhooks
- [references/webhooks-setup.md](references/webhooks-setup.md) — Creating endpoints, delivery format, secrets, event subscription
- [references/webhooks-local.md](references/webhooks-local.md) — Local dev with Polar CLI (`polar listen`)
- [references/webhooks-delivery.md](references/webhooks-delivery.md) — Validation, SDK examples, IP allowlist, retry logic, troubleshooting

### Benefits & License Keys
- [references/benefits.md](references/benefits.md) — Benefit types (Credits, License Keys, File Downloads, GitHub, Discord, Custom), grant lifecycle, webhooks
- [references/license-keys.md](references/license-keys.md) — License key validation, activation/deactivation, limits, brandable prefixes

### Events & Metering
- [references/events-metering.md](references/events-metering.md) — Usage-based billing, event ingestion, meters, cost tracking, credits

### Orders & Customers
- [references/orders-subscriptions.md](references/orders-subscriptions.md) — Sales overview, checkout statuses, payment attempts
- [references/customer-portal.md](references/customer-portal.md) — Customer portal URL, authenticated links via API
- [references/refunds.md](references/refunds.md) — Refund processing, webhook events, benefit revocation

### Webhook Events
- [references/webhook-events.md](references/webhook-events.md) — Complete list of all webhook events, framework handler names

### Metrics & Analytics
- [references/metrics.md](references/metrics.md) — Revenue, MRR, churn, conversion, AOV, cost insights

### Customer State & Sandbox
- [references/customer-state.md](references/customer-state.md) — Single API call for customer's subscriptions, benefits, meters; `customer.state_changed` webhook
- [references/sandbox.md](references/sandbox.md) — Sandbox environment, test card numbers, API URLs, SDK config, limitations

### API Reference
- [references/api-reference.md](references/api-reference.md) — Complete list of all API endpoints, rate limits, pagination, scopes

### AI Integration
- [references/mcp.md](references/mcp.md) — Polar MCP server for AI agents (Cursor, Claude, ChatGPT, etc.)
