---
name: edge-functions-and-webhooks
description: >-
  Use when adding Supabase Edge Functions, Stripe/webhook handlers, server-side
  secrets, or API routes that must not run in the browser. Not for client-only
  UI, CSS, or simple CRUD that RLS + client can handle safely.
---

# Edge functions and webhooks

Secrets and trusted third-party callbacks belong in **Supabase Edge Functions** (or equivalent server), never in the Vite client bundle.

## When to use an edge function

- Webhook signature verification (Stripe, etc.).
- Operations requiring **service role** or private API keys.
- Sending email with provider API keys.
- Complex server logic that must not be tampered with client-side.

## Structure

```
supabase/functions/
  stripe-webhook/
    index.ts
  send-email/
    index.ts
```

- Read secrets from `Deno.env.get("STRIPE_WEBHOOK_SECRET")` etc. — set in Supabase dashboard, not in repo.
- Return proper HTTP status: `400` invalid payload, `401` bad signature, `200` success.
- Make webhook handlers **idempotent** (store processed event IDs).

## Stripe webhook pattern

1. Verify signature with raw body + secret.
2. Switch on `event.type`; update DB with service client.
3. Respond quickly; heavy work async if needed.

For full Stripe event matrix, idempotency, and testing, use **`stripe-payment-webhooks`**, **`payment-webhook-idempotency`**, and **`payment-webhook-testing`**.

## Client invocation

- Use `supabase.functions.invoke("send-email", { body: { ... } })` only for operations safe for authenticated users.
- Pass JWT; validate `auth.getUser()` inside the function for user-triggered calls.

## Avoid

- `VITE_STRIPE_SECRET_KEY`, `VITE_SERVICE_ROLE`, or webhook secrets in frontend.
- Trusting client-sent payment status without webhook confirmation.
- Logging full webhook payloads with PII in production.

## Required companion skills

For any non-trivial edge function, also apply:

- `server-input-validation` — Zod on every body
- `api-error-handling` — consistent JSON errors and status codes

## Checklist

- [ ] CORS configured only if browser calls the function.
- [ ] Auth or signature verified on every entry point.
- [ ] Body validated with Zod (`server-input-validation`).
- [ ] Errors returned as JSON with stable codes (`api-error-handling`).
- [ ] Secrets via `Deno.env.get(...)`; never logged.
