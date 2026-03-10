---
name: mercadopago-subscriptions
description: Implements MercadoPago recurring subscriptions with preapproval plans in a React + Supabase Edge Functions stack. Covers the full lifecycle — creation, cancellation, plan changes, payment method changes, pause/reactivate, webhooks, and CRON sync. Use when building or modifying subscription billing, payment forms, edge functions for MercadoPago, or webhook handlers.
---

# MercadoPago Subscriptions

## Architecture overview

```
Frontend (React + Vite)          Edge Functions (Deno)            MercadoPago API
─────────────────────────        ─────────────────────            ──────────────
CardForm (Secure Fields)    →    mp-create-subscription      →   POST /preapproval
  ↓ card token                   mp-manage-subscription      →   PUT  /preapproval/{id}
SubscriptionPage / Settings →    mp-get-subscription-status  →   GET  /preapproval/{id}
                                 webhook-mercadopago         ←   Webhook notifications
                                 cron-check-subscriptions    →   GET  /preapproval/{id}
```

**Key principle**: Frontend only tokenizes cards (Secure Fields). All MercadoPago API calls happen server-side in Supabase Edge Functions.

## Subscription lifecycle

| Action | Edge Function | MP API | DB Effect |
|---|---|---|---|
| Create | `mp-create-subscription` | `POST /preapproval` (status=authorized) | Insert subscription, update company |
| Cancel | `mp-manage-subscription` (action=cancel) | `PUT /preapproval/{id}` (status=cancelled) | Set cancelled, keep access until period end |
| Change plan | `mp-manage-subscription` (action=change_plan) | `PUT /preapproval/{id}` (transaction_amount) | Update plan_key, amount |
| Change card | `mp-manage-subscription` (action=change_card) | `PUT /preapproval/{id}` (card_token_id) | No DB card storage (MP stores it) |
| Pause | `mp-manage-subscription` (action=pause) | `PUT /preapproval/{id}` (status=paused) | Set suspended |
| Reactivate | `mp-manage-subscription` (action=reactivate) | `PUT /preapproval/{id}` (status=authorized) | Set active |

## Quick reference

### Creating a subscription (happy path)

**Frontend**: Generate card token via Secure Fields → call edge function.

```typescript
// 1. Tokenize card (CardForm component)
const tokenResponse = await mp.fields.createCardToken({
  cardholderName, identificationType, identificationNumber
});

// 2. Call edge function
const result = await api.mpCreateSubscription({
  planKey: 'basic',
  companyId,
  cardTokenId: tokenResponse.id,
  payerEmail: email
});
```

**Edge function**: Create preapproval with `status: 'authorized'` (triggers immediate charge).

```typescript
const preapproval = await mpFetch<MpPreapproval>(
  `${mpConfig.apiBase}/preapproval`,
  {
    method: 'POST',
    headers: getMpHeaders({ 'X-Idempotency-Key': `mp-sub-${companyId}-${planKey}-${Date.now()}` }),
    body: JSON.stringify({
      preapproval_plan_id: mpPlanId,
      payer_email: payerEmail,
      card_token_id: cardTokenId,
      auto_recurring: {
        frequency: 1, frequency_type: 'months',
        transaction_amount: planMeta.amount,
        currency_id: 'ARS'
      },
      status: 'authorized',
      back_url: `${Deno.env.get('APP_URL')}/settings`
    }),
  }
);
```

### Managing a subscription

All management goes through a single `mp-manage-subscription` edge function dispatching on `action`:

```typescript
await api.mpManageSubscription({
  action: 'cancel',          // or 'change_plan' | 'change_card' | 'pause' | 'reactivate'
  mpPreapprovalId: subscription.mpPreapprovalId,
  newPlanKey: 'premium',     // only for change_plan
  cardTokenId: token,        // only for change_card
  reason: 'User requested',  // optional
});
```

## Detailed references

- **Frontend patterns** (CardForm, hooks, API service): See [FRONTEND.md](FRONTEND.md)
- **Edge function patterns** (create, manage, status, CRON): See [EDGE_FUNCTIONS.md](EDGE_FUNCTIONS.md)
- **Webhook handling** (signature validation, event processing): See [WEBHOOK.md](WEBHOOK.md)
- **Type definitions & DB schema**: See [TYPES.md](TYPES.md)
- **Email notifications**: See [EMAIL_TEMPLATES.md](EMAIL_TEMPLATES.md)

## Environment variables

### Frontend (.env)
```
VITE_MP_PUBLIC_KEY=<mercadopago-public-key>
```

### Edge Functions (Supabase Secrets)
```
MP_MODE=sandbox|production
MP_ACCESS_TOKEN=<mercadopago-access-token>
MP_WEBHOOK_SECRET=<webhook-signing-secret>
MP_PLAN_ID_BASIC=<preapproval-plan-id>
MP_PLAN_ID_STANDARD=<preapproval-plan-id>
MP_PLAN_ID_PREMIUM=<preapproval-plan-id>
RESEND_API_KEY=<for-email-notifications>
```

## Plans configuration

Plans are defined in `supabase/functions/_shared/mp-plans.ts`:

```typescript
const MP_PLAN_METADATA = {
  basic:    { name: 'Básico',   amount: 25000, features: [...] },
  standard: { name: 'Estándar', amount: 49000, features: [...] },
  premium:  { name: 'Premium',  amount: 89000, features: [...] },
};
```

Each plan has a corresponding MercadoPago preapproval plan ID stored in env vars (`MP_PLAN_ID_BASIC`, etc.). These plans are created once in the MP dashboard and referenced by ID.

## Critical rules

1. **Never store raw card data**. Use MercadoPago Secure Fields for tokenization only.
2. **Always use `status: 'authorized'`** when creating subscriptions (triggers immediate charge).
3. **Always send `X-Idempotency-Key`** on MP API calls to prevent duplicate operations.
4. **Webhooks must return 200 within 22 seconds** — MP retries on failure.
5. **Webhook signature validation is mandatory** — use HMAC-SHA256 with `MP_WEBHOOK_SECRET`.
6. **Grace period**: Cancelled subscriptions keep access until `current_period_end`.
7. **Use `mpFetch` wrapper** for all MP API calls — handles retries (3x for 5xx/429) with exponential backoff.
8. **Use admin Supabase client** (service role) for cross-user DB updates in edge functions.
