---
name: booking-kiosk
description: >
  Build a self-service touchscreen booking kiosk for a venue: a stepped walk-up
  flow from service, date and time slot through stations and participant names,
  equipment and consumables, to summary and confirmation, with an on-screen
  keyboard, inactivity auto-reset, pay-at-counter or pay-by-QR, live
  availability refresh and a find-my-booking edit flow. Use when: (1) a venue
  (gym, karting, bowling, climbing, escape room, clinic) wants an unattended
  booking terminal, (2) an app that already books online needs a kiosk mode,
  (3) an existing kiosk needs auditing against the hard rules, (4) the user
  mentions: kiosk mode, self-service kiosk, touch screen booking, walk-up
  terminal, on-screen keyboard, inputMode none, inactivity reset, counter
  payment, PENDING_COUNTER_PAYMENT, x-kiosk-api-key, SET_SLOT, REFRESH_SLOT,
  PROMO_INVALID, stock lock. Carries the session reducer with its 14-test suite,
  the screen contract and dictionary key tree, a server-priced idempotent API
  contract with guard tables, stock locks released on every failure path, and
  offline failover against a LAN server. Next.js App Router with React context;
  the KioskBackend interface is the seam, so the booking store, payment provider
  and realtime channel are the host's. Not a staff POS, not digital signage and
  not the on-prem fallback server itself.
---

# Self-Service Booking Kiosk

A kiosk is a booking website with the trust model inverted: the client is
unauthenticated by design and physically shared, so **all trust lives on the
server** (prices, capacity, idempotency) and **all state is disposable**
(in-memory, auto-reset, never persisted). Everything in this skill follows
from those two facts.

## When to use

- Building a walk-up booking terminal for slot-based capacity (stations by
  time windows) with optional equipment and consumable add-ons.
- Adding kiosk mode to an app that already has online booking.
- Auditing an existing kiosk against the hard rules below;
  [provenance.md](references/provenance.md) records the reason behind each.

## When NOT to use

- **On-prem offline fallback server**: that is the sibling
  `island-mode-server` skill; this skill only defines the kiosk's client-side
  failover contract.
- **Digital signage / display screens**: different capability (playback, no
  input), different skill.
- **Staff-facing POS or admin booking tools**: staff are authenticated and
  trusted; this skill's trust model is wrong for them.
- **A plain booking website**: take the backend seam if useful, but the
  kiosk machinery (keyboard, timers, touch hardening) is dead weight there.

## Architecture

```
 KioskProvider (pure reducer: steps, selections, cart, sessionId)
   | props: dictionary slices        hooks: pricing, equipment, availability
 screens: service->date->time->participants->equipment->summary->confirmation
   |                         +- side flow: booking-lookup -> booking-edit
   v one fetch wrapper (device key + offline base-URL failover)
 /api/kiosk/booking/{create,lookup,add-items,edit}     <- all trust decisions
   v KioskBackend seam: server pricing, promo, stock locks (TTL 15 min)
     transactional capacity re-check, counter/online payment, webhook
 realtime: location.lastBookingChangeAt -> silent refetch -> REFRESH_SLOT
```

## Critical facts

1. **User taps navigate; background refreshes never do.** `SET_SLOT` vs
   `REFRESH_SLOT` is the difference between live availability and teleporting
   a customer off the summary screen mid-purchase.
2. **The server prices everything.** Nothing money-shaped crosses the wire
   inbound; the client total is a preview.
3. **Counter payment is the resilience path**: a booking confirms with
   `PENDING_COUNTER_PAYMENT`, no payment integration in the loop; online
   payment on a kiosk means a QR the customer scans, never navigating the
   kiosk away.
4. **Every text input opens the on-screen keyboard** and sets
   `inputMode="none"`. One without the other is an unusable screen.
5. **Stock locks are TTL-reserved (15 min) and released on every failure
   path.** The sweep job is the safety net, not the mechanism.
6. **The client sessionId is the idempotency key.** Double-tap, retry, lost
   response: at most one booking.

## Hard rules

> **Never persist kiosk session state.** The next customer must not see the
> previous one's name. In-memory + 120 s inactivity reset + 30 s
> confirmation reset, verified on hardware.

> **Never trust the client for prices, capacity, or promo validity.** The
> server computes every amount and answers an invalid promo with
> `PROMO_INVALID`; a customer at a kiosk has no way to check the amount.

> **One fetch wrapper for every kiosk request.** The wrapper carries the
> device header, the error envelope and the failover base URL, so auth,
> errors and offline failover apply to every request at once.

> **If the device key is configured, a missing header is a 401.** Reject-only-
> on-wrong-key is the same as no auth.

> **Release stock locks on every failure path after acquiring them.** A 409
> that keeps the reservation freezes stock for the full TTL.

## Quick start

1. Copy every template to the path on its first `// file:` line, renamed only
   through the vocabulary table in [state-machine.md](references/state-machine.md).
   Never rewrite, harden or restructure a template: a defect you find in one
   goes in the handover, not into the code.
2. Install vitest (`npm i -D vitest`; the package registry is not an external
   service), set `"test": "vitest run"` and run the 14 reducer tests unchanged:
   no other runner, no `expect` shim, no edited assertion.
3. Build screens against the contract in [screens.md](references/screens.md)
   with the host's design system: keyboard, timers, touch hardening.
4. Implement the routes from [api-contract.md](references/api-contract.md) over
   the [booking-backend.md](references/booking-backend.md) seam, send every kiosk
   request through its one `createKioskFetch` wrapper, and wire freshness +
   offline per [realtime-offline.md](references/realtime-offline.md).
5. Configure per [operations.md](references/operations.md): a tracked
   `.env.example` lists `KIOSK_API_KEY`, `KIOSK_PUBLIC_BASE_URL` and
   `KIOSK_LAN_FALLBACK_URL`, all empty.
6. Hand over: name the variables in `.env.example`, and tell the operator that
   with `KIOSK_API_KEY` unset the kiosk API is open to anyone who can reach it,
   that the boot URL must carry `?locationId=`, and which `KioskBackend` is
   wired (a demo store must be replaced before real sales).

## Adaptation Contract

This skill keeps its seam contract here rather than in a `references/adaptation.md`: the
table is the full boundary of what the host supplies, and the rename table sits in
[state-machine.md](references/state-machine.md).

| Seam | This skill ships | The host supplies |
|---|---|---|
| Domain entities | service/station/equipment/consumable + rename table | its vocabulary (court, kart, bay) |
| Tenant scope | `locationId` in the kiosk URL, server-verified | its location/site model |
| Device auth | `x-kiosk-api-key` contract | key management; optional per-device tokens |
| Data access | `KioskBackend` interface; Firestore reference + SQL sketch | its ORM/SDK, exported as `backend` from `lib/kiosk/server/instance.ts` |
| Payments | counter status + checkout-session/webhook contract | Stripe or equivalent |
| Realtime | `SubscribeFreshness` interface | Firestore/Supabase/SSE/polling |
| Offline | `NetworkStatus` contract | LAN server (`island-mode-server`) or none |
| UI primitives | structure, states, interaction rules | buttons, dialog, spinner, look |
| Styling | layout intent, touch targets, one `--primary` token | its design system |
| Strings | dictionary key tree, all keys required | its i18n files, all locales |
| Validation | dependency-free guards | its schema library, if any |

## Reference directory

| Scenario | Trigger keywords | Reference |
|---|---|---|
| State, steps, reducer, session, tests | step, reducer, GO_BACK, REFRESH_SLOT, sessionId, reset, vitest | [state-machine.md](references/state-machine.md) |
| Screens, keyboard, timers, touch, i18n keys | on-screen keyboard, inactivity, countdown, QR, touch target, dictionary | [screens.md](references/screens.md) |
| Routes, auth, validation, idempotency, errors | x-kiosk-api-key, 401, 409, idempotency, PROMO_INVALID, lookup, PII, createKioskFetch, fetch wrapper | [api-contract.md](references/api-contract.md) |
| Capacity, stock, payments, webhook, crons | transaction, stock lock, TTL, PENDING_COUNTER_PAYMENT, webhook, refund | [booking-backend.md](references/booking-backend.md) |
| Live refresh, caching, offline failover | lastBookingChangeAt, onSnapshot, s-maxage, offline banner, LAN, health poll | [realtime-offline.md](references/realtime-offline.md) |
| Deploying, gating, operator surface | Edge --kiosk, assigned access, heartbeat, feature gate, env vars, .env.example, smoke test | [operations.md](references/operations.md) |
| Why the templates differ from the earlier implementation | audit, ledger, kept deliberately, added | [provenance.md](references/provenance.md) |

Part of the [Timerise Skills](https://github.com/timerise-ai/skills) index, which lists the sibling skills.
