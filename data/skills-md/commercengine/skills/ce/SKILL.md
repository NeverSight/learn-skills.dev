---
name: ce
description: Commerce Engine router. Use when user asks about building a storefront, setting up the SDK, authentication, products, cart, checkout, orders, webhooks, or Next.js e-commerce patterns. Automatically routes to the specific skill based on their task.
---

> **LLM Docs Header**: All requests to `https://llm-docs.commercengine.io` **must** include the `Accept: text/markdown` header (or append `.md` to the URL path). Without it, responses return HTML instead of parseable markdown.

# Commerce Engine Skills Router

These skills cover **B2C storefronts**. B2B storefronts share ~95% of the same patterns — the main difference is customer group pricing (see `ce-catalog` § "Customer Groups & Pricing" and `ce-setup` § "Default Headers").

Based on what you're trying to do, here's the right skill to use:

## By Task

**Setting up the SDK** → Use `ce-setup`
- Framework detection and SDK install
- Token storage selection
- Environment variables (`CE_STORE_ID`, `CE_API_KEY`)

**Authentication & login** → Use `ce-auth`
- Anonymous auth (always required)
- OTP login (email/phone/WhatsApp), password auth, token refresh
- **Note**: If using Hosted Checkout, login is handled inside the checkout drawer. Only build custom login UI if your app needs logged-in state outside of checkout (account pages, order history, etc.)

**Products & catalog** → Use `ce-catalog`
- Products, variants, SKUs
- Categories, faceted search
- Reviews, recommendations

**Cart & checkout** → Use `ce-cart-checkout`
- **Hosted Checkout (recommended)** — pre-built, embeddable, saves 2-3 months
- Custom checkout (advanced) — Cart CRUD, fulfillment, payment gateways
- Coupons, loyalty points

**Orders & returns** → Use `ce-orders`
- Create orders from cart
- Shipment tracking, payment status
- Cancellation, returns flow

**Webhooks & events** → Use `ce-webhooks`
- 14 event types (order, payment, refund, shipment)
- Signature verification
- Async processing patterns

**Next.js patterns** → Use `ce-nextjs-patterns`
- `storefront()` universal function
- `CookieTokenStorage` for SSR
- Server Actions, SSG, ISR

## Storefront Pages

Canonical pages for a CE storefront and the skills/methods each needs:

| Page | Example Route | Skills | Key SDK Methods |
|------|---------------|--------|-----------------|
| Home | `/` | catalog | `listProducts`, `listCategories`, recommendations (`listSimilarProducts`, etc.) |
| Product Listing (PLP) | `/products`, `/categories/[slug]` | catalog | `searchProducts({ query, filters })` for filtered/search PLPs; `listProducts` for simple grids |
| Product Detail (PDP) | `/products/[slug]` | catalog | `getProductDetail`, `listProductVariants` (if `has_variant`), `listProductReviews` |
| Cart | Hosted Checkout drawer | cart-checkout | `useCheckout().openCart()`, `useCheckout().addToCart()` |
| Checkout | Hosted Checkout drawer | cart-checkout | `useCheckout().openCheckout()` |
| Login | `/login` | auth | `loginWithEmail` / `loginWithPhone`, `verifyOtp` |
| Account | `/account` | auth | `getUserDetails`, `updateUserDetails`, `changePassword` |
| Orders | `/account/orders` | orders | `listOrders` |
| Order Detail | `/account/orders/[id]` | orders | `getOrderDetails`, `listOrderShipments`, `listOrderPayments` |

> **Cart & Checkout routes**: With Hosted Checkout (recommended), cart and checkout are drawers — no dedicated pages needed. With custom checkout, add `/cart` and `/checkout` as separate pages (see `ce-cart-checkout`).

> **Building a new storefront?** Start with `ce-setup`, then build pages in this order: Home → PLP → PDP → Cart/Checkout → Login → Account → Orders.
>
> **Converting an existing project?** Follow the migration checklist below.

## Converting an Existing Project

Step-by-step for replacing an existing backend (or mock data) with Commerce Engine:

1. **Install SDK** — Follow `ce-setup`. Detect framework, install packages, set env vars, choose token storage.
2. **Add anonymous auth** — Call `sdk.auth.getAnonymousToken()` at app startup. Every visitor needs this before any API call works.
3. **Replace catalog data** — Swap mock/existing product data with `sdk.catalog.*` calls. Start here because catalog is read-only and low-risk.
   - Product lists → `searchProducts` or `listProducts`
   - Product detail → `getProductDetail` + `listProductVariants`
   - Categories → `listCategories`
4. **Add auth** — Replace existing login with CE auth (`ce-auth`). Use `loginWithEmail`/`loginWithPhone` + `verifyOtp`.
5. **Add cart + checkout** — Install Hosted Checkout (`ce-cart-checkout`). Replace existing cart UI with `useCheckout()` hooks. Wire `authMode: "provided"` with two-way token sync.
6. **Add orders** — Replace order history with `listOrders` / `getOrderDetails` (`ce-orders`).
7. **Add SEO metadata** — Map CE product fields to meta tags (`ce-nextjs-patterns` § "SEO Metadata" for Next.js).

> **Key principle**: Replace one data source at a time. Keep existing UI components — only swap the data layer underneath.

## Decision Tree

```
User Request
    │
    ├─ "Set up SDK" / "Add Commerce Engine"  → ce-setup
    ├─ "Login" / "Auth" / "OTP"              → ce-auth
    ├─ "Products" / "Categories" / "Search"  → ce-catalog
    ├─ "Cart" / "Checkout" / "Payments"      → ce-cart-checkout
    ├─ "Orders" / "Returns" / "Shipments"    → ce-orders
    ├─ "Webhooks" / "Events" / "Sync"        → ce-webhooks
    └─ "Next.js" / "SSR" / "Server Actions"  → ce-nextjs-patterns
```

## Quick Navigation

If you know your task, you can directly access:
- `/ce-setup` - SDK setup & framework detection
- `/ce-auth` - Authentication & user management
- `/ce-catalog` - Products & categories
- `/ce-cart-checkout` - Cart, checkout & payments
- `/ce-orders` - Order management
- `/ce-webhooks` - Webhook events & syncing
- `/ce-nextjs-patterns` - Next.js patterns

Or describe what you need and I'll recommend the right one.
