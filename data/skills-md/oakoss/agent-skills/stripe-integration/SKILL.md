---
name: stripe-integration
description: |
  Stripe payment integration with Node.js SDK. Covers Checkout Sessions, Payment Intents, Subscriptions, Customer Portal, webhooks, and Stripe Elements.

  Use when implementing checkout flows, payment processing, subscription billing, webhook handlers, or payment forms with Stripe Elements.

  Use for stripe, payments, checkout, subscriptions, billing, webhooks, payment intents, stripe elements.
license: MIT
metadata:
  author: oakoss
  version: '1.0'
  source: https://docs.stripe.com
user-invocable: false
---

# Stripe Integration

## Overview

Stripe provides a complete payments platform with server-side SDKs (Node.js) and client-side libraries (Stripe.js, React Stripe.js). The Node.js SDK handles server operations like creating Payment Intents, managing Subscriptions, and verifying webhooks. The React Stripe.js library provides pre-built UI components (PaymentElement, Elements provider) for secure client-side payment collection.

**When to use:** One-time payments, recurring subscriptions, usage-based billing, marketplace payouts, hosted checkout pages, custom payment forms, webhook-driven fulfillment.

**When NOT to use:** Cryptocurrency payments (not supported), regions where Stripe is unavailable, simple static product sales without payment processing (use a hosted storefront).

## Quick Reference

| Pattern             | API                                                   | Key Points                                                            |
| ------------------- | ----------------------------------------------------- | --------------------------------------------------------------------- |
| Hosted checkout     | `stripe.checkout.sessions.create()`                   | Stripe-hosted page, supports `payment`, `subscription`, `setup` modes |
| Payment Intent      | `stripe.paymentIntents.create()`                      | Server-side, returns `client_secret` for client confirmation          |
| Confirm payment     | `stripe.confirmPayment({ elements, clientSecret })`   | Client-side, requires Elements instance                               |
| Create subscription | `stripe.subscriptions.create()`                       | Use `payment_behavior: 'default_incomplete'` for SCA                  |
| Update subscription | `stripe.subscriptions.update()`                       | Set `proration_behavior` explicitly                                   |
| Cancel subscription | `stripe.subscriptions.cancel()`                       | Use `prorate: true` to credit unused time                             |
| Customer Portal     | `stripe.billingPortal.sessions.create()`              | Self-service billing management, returns short-lived URL              |
| Webhook verify      | `stripe.webhooks.constructEvent()`                    | Requires raw body, signature header, and endpoint secret              |
| Elements provider   | `<Elements stripe={stripePromise} options={options}>` | Wraps payment components, pass `clientSecret` or `mode`               |
| PaymentElement      | `<PaymentElement />`                                  | Renders all supported payment methods automatically                   |
| Retrieve + expand   | `stripe.checkout.sessions.retrieve(id, { expand })`   | Expand nested objects to reduce API calls                             |
| Search              | `stripe.paymentIntents.search({ query })`             | Stripe Query Language for filtering                                   |

## Common Mistakes

| Mistake                                           | Correct Pattern                                                                                     |
| ------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| Parsing webhook body as JSON before verification  | Use `express.raw({ type: 'application/json' })` to pass raw body to `constructEvent`                |
| Hardcoding payment method types                   | Use `automatic_payment_methods` or let Checkout choose based on currency and region                 |
| Creating PaymentIntent client-side                | Create on server, pass only `client_secret` to client                                               |
| Not awaiting `elements.submit()` before confirm   | Call `elements.submit()` first to trigger validation, then `confirmPayment`                         |
| Missing `return_url` in `confirmPayment`          | Always provide `return_url` for redirect-based payment methods                                      |
| Using test keys in production                     | Store keys in environment variables, validate `STRIPE_SECRET_KEY` prefix (`sk_live_` vs `sk_test_`) |
| Not handling `requires_action` status             | Check PaymentIntent status after confirmation, handle 3D Secure or other authentication             |
| Creating Customer Portal session without settings | Save portal settings in Dashboard first, otherwise API returns an error                             |
| Not expanding related objects                     | Use `expand` parameter to include nested objects like `latest_invoice.payment_intent`               |
| Ignoring webhook idempotency                      | Use `event.id` to deduplicate, webhook events can be delivered more than once                       |

## Delegation

- **Payment flow architecture**: Use `Explore` agent to discover integration patterns
- **Webhook debugging**: Use `Task` agent for end-to-end event tracing
- **Code review**: Delegate to `code-reviewer` agent for security review of payment handlers

## References

- [Checkout Sessions, Payment Intents, and one-time payments](references/checkout-and-payments.md)
- [Subscription lifecycle, pricing models, trials, and Customer Portal](references/subscriptions.md)
- [Webhook endpoints, signature verification, and event handling](references/webhooks.md)
- [React Stripe.js, Elements provider, PaymentElement, and custom forms](references/stripe-elements.md)
