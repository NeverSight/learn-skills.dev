---
name: paystack-integration
description: >-
  Paystack Integration API — manage integration-level settings like payment session
  timeouts. Use this skill whenever configuring Paystack integration settings,
  adjusting payment session timeout durations, or building admin panels that control
  payment session behavior. Also use when you see references to
  /integration/payment_session_timeout endpoint.
---

# Paystack Integration

The Integration API lets you manage settings on your Paystack integration.

> Depends on: **paystack-setup** for the `paystackRequest` helper.

## Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/integration/payment_session_timeout` | Get current timeout |
| PUT | `/integration/payment_session_timeout` | Update timeout |

## Fetch Payment Session Timeout

```typescript
const timeout = await paystackRequest<{
  payment_session_timeout: number;
}>("/integration/payment_session_timeout");
// timeout.data.payment_session_timeout → 30 (seconds)
```

## Update Payment Session Timeout

Set how long (in seconds) before a payment session expires. Set to `0` to disable.

```typescript
await paystackRequest("/integration/payment_session_timeout", {
  method: "PUT",
  body: JSON.stringify({ timeout: 30 }),
});
```
