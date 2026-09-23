---
name: stripe
description: "Stripe — payment processing platform with APIs for accepting payments, managing subscriptions, handling payouts, and preventing fraud. Use when building with Stripe or asking about its APIs, configuration, patterns, webhooks, or integration. Fetch live documentation for up-to-date details."
---

# Stripe

> **CRITICAL: Your training data for Stripe is unreliable.** APIs change between versions and memorized patterns may be wrong or deprecated. Before writing any code, you MUST use `WebFetch` to read the live docs:
>
> **`WebFetch("https://docs.stripe.com/llms.txt")`**
>
> Do not proceed without fetching this URL first. Never assume an API exists — verify against current docs.

Stripe is a payment processing platform with APIs for accepting payments, managing subscriptions, handling payouts, Connect marketplaces, and fraud prevention.
## Best Practices

- **Use PaymentIntents, not Charges** — the Charges API and Sources API are legacy. Always use PaymentIntents (or Checkout Sessions) for new integrations. Agents default to Charges; this pattern is deprecated.
- **Use Payment Element, not Card Element** — the Payment Element is the current recommended frontend component. The Card Element is older and handles fewer payment methods. Agents often reach for Card Element.
- **Webhook signature verification is mandatory** — always verify webhooks with `stripe.webhooks.constructEvent(rawBody, sig, secret)`. Skipping verification means any attacker can send fake events. This is a security-critical step agents frequently omit.
- **Webhooks require the raw request body** — do not parse the body with `express.json()` or equivalent middleware before the webhook handler. The signature check needs the raw buffer, not a parsed object. Applying a body parser upstream silently breaks verification.
- **Add idempotency keys to mutations** — pass `{ idempotencyKey: 'unique-key' }` on PaymentIntent creation and other write operations to prevent duplicate charges on network retries. Agents almost never include these.
- **Never hardcode `payment_method_types`** — omit the parameter to let Stripe dynamically show the optimal payment methods for each customer's location and wallet. Hardcoding limits international acceptance unnecessarily.
