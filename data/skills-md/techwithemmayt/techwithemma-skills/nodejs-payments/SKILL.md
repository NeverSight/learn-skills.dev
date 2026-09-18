---
name: nodejs-payments
description: Implement, review, or repair secure Node.js payment and subscription backends using Stripe, Polar, or Paddle, including checkout creation, customers, verified webhooks, idempotent processing, subscription state, entitlements, refunds, disputes, and billing portals. Use when a Node.js app needs payments, billing, subscriptions, payment-webhook security, or provider migration.
---

# Node.js Payments

Use one provider per requested integration. Do not install Stripe, Polar, and Paddle together unless the user explicitly requests multiple providers.

## Confirm before changing

Inspect read-only first. Before writing files, installing a provider SDK, changing schema/configuration, running migrations, or calling a provider API, show a proposal of no more than five short bullets covering the requested payment flow, provider, affected areas, durable state/webhooks, verification, and important exclusions. Wait for confirmation, then perform only the approved work. Do not repeat provider documentation or narrate routine steps unless asked.

## Inspect and choose the mode

Read the auth model, users or organizations, database schema, routes, existing provider code, product catalogue, and deployment environment. Determine whether the request is:

- one-time checkout;
- recurring subscription;
- usage or credit billing;
- customer portal;
- review or repair of an existing integration.

Ask for a provider only when it cannot be inferred. Then read the matching section in [references/providers.md](references/providers.md) and confirm current SDK/API signatures in the official docs before coding. Never fabricate package versions or event names.

## Enforce payment invariants

- The server maps an allowed product or price ID to price, currency, cadence, and entitlement. Never trust a client-supplied amount or access level.
- Associate the provider customer and checkout with the authenticated user or organization using stable server-owned IDs.
- Keep secret keys and webhook secrets server-only.
- Verify every webhook using the provider's official method and the unchanged raw request body before parsing or mutating it.
- Store provider event IDs with a unique constraint. Process retries idempotently and tolerate duplicate or out-of-order delivery.
- Use provider idempotency support for retryable create/update requests when available.
- Grant, change, or revoke access from verified server-side payment state. A success redirect is user experience, not proof of payment.
- Model pending, active, past-due, canceled, refunded, disputed, and expired states needed by the product.
- Record provider object IDs and a minimal audit trail; never log secrets, full payment details, or sensitive payloads.

## Design the integration

Keep provider calls behind a focused billing service rather than spreading SDK use across controllers. Separate:

1. checkout or portal endpoints;
2. webhook transport and signature verification;
3. durable event deduplication;
4. provider event-to-domain state transitions;
5. entitlement checks used by protected application features;
6. reconciliation jobs for missed or delayed events.

Return quickly from webhooks. If work is slow, persist the verified event and enqueue processing with retry and dead-letter visibility.

## Prevent payment misuse

Authenticate checkout creation, validate product eligibility, apply user- and identity-aware rate limits, and prevent arbitrary metadata from becoming authority. Review coupon, trial, credit, refund, portal, and organization ownership paths. Treat fraud products such as Stripe Radar as complementary; they do not replace application authorization, quotas, webhook verification, or monitoring.

## Test and verify

Use provider test or sandbox mode. Cover signature rejection, duplicate events, out-of-order state changes, unauthorized product IDs, retries, cancellation, refund/dispute behavior, and entitlement removal. Use provider CLI/test tools where available, but never point destructive tests at production.

Report the provider, supported flows, webhook events handled, database constraints, commands/tests run, required dashboard settings, required environment variable names, and remaining business decisions. Never print secret values.
