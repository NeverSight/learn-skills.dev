---
name: opencals-storefront-api
description: >-
  Ground-truth reference for building integrations on the Opencals hosted
  booking API with @opencals/storefront-sdk. Use whenever you are writing,
  reviewing or debugging code that talks to Opencals — availability, carts,
  appointments, checkout/payments, customer accounts (self-service), guests and
  attendees, custom durations, discounts (automatic / codes / balance credit),
  rescheduling and cancellation, addresses and marketing consent, or when you
  hit 429s / rate limits. Works alongside the `opencals-build-booking-site`
  skill (which scaffolds a whole site) but applies to ANY stack: a template, a
  from-scratch app, an embed on an existing site, or a v0/Lovable/Bolt build.
---

# Opencals Storefront API & SDK

You are integrating a real, revenue-carrying booking flow against the **Opencals
hosted API**. You do **not** implement availability maths, timezones, conflict
resolution, pricing or payments — the API owns all of that. Your job is to call
the right endpoints in the right order and render the results.

The SDK is `@opencals/storefront-sdk` (class-based, generated from the OpenAPI
spec). Every identifier in this skill's reference files is copied from that SDK —
**never invent method names, parameters or enum values.** If something you need
isn't documented here, read the generated types in
`node_modules/@opencals/storefront-sdk/dist` (or the source `src/client/*.gen.ts`)
rather than guessing.

## When to use this skill

Trigger on any Opencals API/SDK work: "book an appointment", "show available
slots", "apply a discount code", "let customers reschedule", "add a guest to a
booking", "collect a billing address at checkout", "why am I getting a 429",
"custom booking length", "customer login". If the task is "build me a whole
booking website from a template", start with the **`opencals-build-booking-site`**
skill and come back here for the exact call shapes.

## Setup (once)

Initialise the SDK a single time via a side-effect import, then import service
classes directly:

```ts
// lib/opencals.ts — imported once at the top of every server file that calls the API
import { setupOpencals } from '@opencals/storefront-sdk';

setupOpencals({
  baseUrl: process.env.OPENCALS_API_URL ?? 'https://api.opencals.com',
  apiKey: process.env.OPENCALS_API_KEY, // sfk_… storefront key, from the dashboard
  logging: process.env.NODE_ENV === 'development',
});
```

```ts
import { ProductService, CartService, AppointmentService } from '@opencals/storefront-sdk';
```

Full setup details, the complete service list, `X-Api-Version`, and the
`throwOnError` gotcha: **`references/setup.md`**.

## The core booking flow

1. **Availability** → `ProductService.getCurrentAvailabilities` (exact slots) or
   `getCurrentAvailabilitiesMerged` (calendar highlighting). → `references/availability.md`
2. **Cart** → `CartService.createOrGet`, persist the `X-Cart-Id`. → `references/cart-lifecycle.md`
3. **Appointment** → `AppointmentService.create` (slot + `cartId` + `numberOfAttendees` + optional guests/add-ons). → `references/guests-attendees.md`
4. **Checkout** → `CheckoutService.start → saveCustomer → saveAnswers → submit`. → `references/checkout.md`

## Reference files (load the one you need)

| File | Covers |
|------|--------|
| `references/setup.md` | `setupOpencals`, service classes, versioning header, `OpencalsApiError`, `throwOnError` |
| `references/availability.md` | `getCurrentAvailabilities` vs `getCurrentAvailabilitiesMerged`, `duration`, `excludeAppointmentId`, slot shape, grid fan-out |
| `references/custom-duration.md` | `allowCustomDuration` / `maxDuration`, quantity = duration-units pricing rule |
| `references/guests-attendees.md` | `numberOfAttendees`, `maxAttendees`/`attendees`, `addGuest` / `removeGuest` |
| `references/cart-lifecycle.md` | create/get, `X-Cart-Id`, `expiresAt`, `extendExpiration`, expiry countdown |
| `references/checkout.md` | `saveCustomer` timing, billing vs delivery address, marketing consent, checkout questions |
| `references/auth-self-service.md` | password + passwordless + OAuth login, sessions, `SelfService` (profile, appointments, consent) |
| `references/reschedule-cancel.md` | `reschedule` / `cancel`, `rescheduleGap` / `cancelGap`, excluding the moved appointment |
| `references/discounts.md` | automatic vs code (`applyCode`) vs balance credit (`valueType: 'time'`), error codes |
| `references/rate-limiting.md` | 429 handling, `withRateLimitRetry` backoff pattern, allowed origins, per-key throttling |
| `references/debugging.md` | reading `OpencalsApiError`, the top recurring mistakes and how to spot them |

## Resources

- [Opencals](https://opencals.com) — main site
- [Docs & API reference](https://opencals.com/docs)
- [@opencals/storefront-sdk on npm](https://www.npmjs.com/package/@opencals/storefront-sdk)
- [Dashboard](https://app.opencals.com) — create stores, manage storefront API keys

## Guardrails

- **Never invent SDK names.** Methods, params and enums must match the generated
  SDK. When unsure, read `references/*` or the SDK's `.d.ts` files.
- **Never hard-code services, prices, availability, staff or locations.** They
  come from the store via the API and are configured in the Opencals dashboard.
- **All slot dates/times are UTC.** Convert to the customer's timezone for
  display only; send `timezone` on availability queries so slots align to the
  local day.
- **Surface real errors.** The SDK throws `OpencalsApiError` with the backend
  status code and field-level detail — never swallow it into a generic 500.
- The SDK and the official templates are MIT-licensed; the hosted API is
  closed-source. You pay Opencals only for bookings.
