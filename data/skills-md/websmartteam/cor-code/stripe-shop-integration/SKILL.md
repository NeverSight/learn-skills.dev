---
name: stripe-shop-integration
description: Comprehensive Stripe e-commerce integration for React shops (Vite OR Next.js). Use when building online shops, payment systems, checkout flows, or integrating Stripe payments. Covers client-side setup, server-side APIs, webhooks, cart systems, and UK GBP configuration.
allowed-tools: Read, Write, Edit, MultiEdit, Bash, Glob, Grep
---

# Stripe E-Commerce Shop Integration

Production-tested patterns for integrating Stripe payments into React e-commerce applications with Supabase backend. Supports **both Vite and Next.js**. All examples use **UK GBP currency** and follow enterprise security standards.

## Framework Support

| Framework | API Routes | Environment Variables | Server Components |
|-----------|------------|----------------------|-------------------|
| **Vite + Vercel** | `api/*.ts` (Vercel functions) | `import.meta.env.VITE_*` | No (CSR only) |
| **Next.js App Router** | `app/api/*/route.ts` | `process.env.*` | Yes (RSC) |
| **Next.js Pages Router** | `pages/api/*.ts` | `process.env.*` | No |

## Quick Start Checklist

1. **Install Dependencies**: `npm install @stripe/stripe-js @stripe/react-stripe-js stripe`
2. **Environment Variables**: Set up `.env` with Stripe keys
3. **Create Client Library**: `src/lib/stripe.ts`
4. **Create Server Library**: `src/lib/stripe-server.ts`
5. **Create API Endpoints**: `api/stripe/` directory
6. **Create Types**: `src/types/stripe.ts`
7. **Set Up Webhook**: Configure in Stripe Dashboard

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CLIENT (React/Vite)                          │
├─────────────────────────────────────────────────────────────────────┤
│  CartContext.tsx → Checkout.tsx → Payment.tsx → StripeCheckout.tsx  │
│         ↓              ↓             ↓              ↓                │
│    Add Items     Create Order   Get Secret    PaymentElement         │
└────────────────────────────────┬────────────────────────────────────┘
                                 │ API Calls
┌────────────────────────────────▼────────────────────────────────────┐
│                      SERVER (Vercel API Routes)                      │
├─────────────────────────────────────────────────────────────────────┤
│  /api/stripe/create-payment-intent  →  Stripe API                   │
│  /api/stripe/create-checkout-session →  Stripe API                  │
│  /api/stripe/webhook               ←  Stripe Webhooks               │
└─────────────────────────────────────────────────────────────────────┘
```

## Detailed Implementation

For complete code examples, see:
- [ENVIRONMENT.md](ENVIRONMENT.md) - Environment variables configuration
- [CLIENT.md](CLIENT.md) - Client-side Stripe setup (Vite examples)
- [SERVER.md](SERVER.md) - Server-side Stripe setup and API endpoints (Vite/Vercel)
- [NEXTJS.md](NEXTJS.md) - **Next.js App Router specific patterns**
- [TYPES.md](TYPES.md) - TypeScript interfaces
- [FLOW.md](FLOW.md) - Complete checkout flow implementation
- [WEBHOOKS.md](WEBHOOKS.md) - Webhook handling for payment events
- [DATABASE.md](DATABASE.md) - Required Supabase database tables
- [STRIPE-CLI.md](STRIPE-CLI.md) - **Stripe CLI for dashboard configuration & testing**

## Stripe MCP Server (AI Agent Integration)

For AI-assisted Stripe management, use the official Stripe MCP server:

### Installation

```bash
# Add to Claude Code MCP config (~/.claude.json)
claude mcp add --scope user stripe -- npx -y @stripe/mcp --tools=all --api-key=sk_test_YOUR_KEY
```

### Manual Configuration

```json
{
  "mcpServers": {
    "stripe": {
      "command": "npx",
      "args": [
        "-y",
        "@stripe/mcp",
        "--tools=all",
        "--api-key=sk_test_YOUR_STRIPE_SECRET_KEY"
      ]
    }
  }
}
```

### MCP Capabilities

The Stripe MCP enables natural language interactions:
- Create and manage products/prices
- Handle customer operations
- Process payments and refunds
- Search Stripe documentation
- Debug webhook issues
- Manage subscriptions

**Documentation**: https://docs.stripe.com/mcp

## Key Principles

### Security First
- **NEVER** expose secret keys on the client
- **ALWAYS** validate amounts server-side against database
- **ALWAYS** use webhook signature validation
- **ALWAYS** store payment records in database

### UK/GBP Configuration
- Currency: `'gbp'`
- Country: `'GB'`
- Amounts in **pence** for Stripe API (multiply pounds by 100)

### Two Payment Methods

1. **Payment Intent** (Embedded Form)
   - Payment form stays on your site
   - More control over UI/UX
   - Use `PaymentElement` component

2. **Checkout Session** (Stripe Hosted)
   - Redirects to Stripe's hosted page
   - Easier to implement
   - Built-in address collection

## Common Commands

```bash
# Install Stripe packages
npm install @stripe/stripe-js @stripe/react-stripe-js stripe

# Install Stripe CLI (macOS)
brew install stripe/stripe-cli/stripe

# Login to Stripe CLI
stripe login

# Generate TypeScript types from Supabase (if using)
npx supabase gen types typescript --project-id YOUR_PROJECT_ID > src/types/supabase.ts
```

## Testing

- Use Stripe test mode keys (start with `pk_test_` and `sk_test_`)
- Test card number: `4242 4242 4242 4242`
- Any future expiry date and any 3-digit CVC
- Use Stripe CLI for webhook testing: `stripe listen --forward-to localhost:3000/api/stripe/webhook`

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Invalid API key" | Check environment variable is set and correct |
| Amount mismatch | Ensure you're converting pounds to pence (x100) |
| Webhook fails | Check signature, ensure raw body parsing disabled |
| CORS errors | Add origin to allowed origins list in API |
| Stripe CLI not working | Run `stripe login` to authenticate |
| MCP not connecting | Restart Claude Code after adding MCP config |
