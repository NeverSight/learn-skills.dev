---
name: bookable-events
description: >
  Build bookable events with Stripe payments and an anti-no-show card hold:
  capacity-limited registration for free and paid events, Stripe Checkout
  tickets, refundable deposits on free events that are released when the
  guest checks in and captured when they don't show, staff check-in, refunds
  and event cancellation. Use when: (1) a venue, club, studio, school or
  community runs classes, workshops, tournaments, meetups or open days with
  limited seats, (2) free events suffer no-shows and need a deposit or card
  hold, (3) an existing event-registration or ticketing module needs auditing,
  (4) the user mentions: event registration, ticketed events, RSVP with
  deposit, no-show fee, no-show deposit, card hold, hold funds, authorize and
  capture later, capture_method manual, uncaptured payment, capture_before,
  SetupIntent, off_session, checkout.session.expired, "release the deposit on
  check-in", "charge no-shows", escrow for attendance, Stripe Checkout
  tickets, refund on cancel, cancel event and refund everyone. Carries a pure
  participant state machine, the hold timing that survives Visa's shorter
  merchant-initiated window, any ISO currency with USD by default, refunds of
  the amount frozen at registration, and 50 tests that hold each rule.
  Next.js App Router; Firestore or Postgres behind an EventStore seam. Not a
  marketplace payout skill, not subscriptions, not seat maps or resale.
---

# Bookable Events with No-Show Deposits

Events are the easy half. The hard half is money that moves while seats are scarce: a seat taken before
payment, a payment that arrives after the seat expired, a hold that lapses before the no-show can be charged.
This skill runs every change through **one pure state machine inside a transaction, and calls Stripe only
after commit**, leaving a durable intent a single cron retries until Stripe confirms.

## When to use

- Capacity-limited events (free or paid) with online registration and payment.
- Free events that need a refundable deposit to stop no-shows.
- Staff check-in at the door that must drive money (release or capture).
- Auditing or upgrading an existing event-registration module:
  [provenance.md](references/provenance.md) has the audit ledger and the order of work.

## When NOT to use

- **Splitting payments between sellers, payouts, marketplace escrow, recurring memberships or
  subscriptions**: use the sibling `stripe-connect-subscriptions` skill.
- **Time-slot resource booking (lanes, courts, rooms by the hour)**: a booking
  engine's job; this skill only notes where events block such slots.
- **Walk-up touchscreen registration**: the sibling `booking-kiosk` skill owns
  the unattended-terminal flow; it can call this engine.
- **Seated venues with seat maps, or ticket resale**: a different domain.

## Architecture

```
 routes: register, status/cancel/resume, staff check-in/no-show/waive/cancel, admin CRUD/cancel
   |  parse, authorize (host.ts: session, staff + locationId), call the engine
   v
 engine.transition --- store.mutateParticipant (ONE tx) --- applyAction (pure) --- seatDelta
   |  commit
   v
 effectsOf(before, after) --> Stripe: expire, cancel hold, capture, refund; email
   ^                            success: confirming action; failure: RETRY_*
   |
 webhook (claim evt id)
 tick every 5 min: nextActionAt <= now --> EXPIRE_PENDING, PLACE_HOLD, SETTLE, RETRY_*
```

Routes parse and authorize, then hand one action to the engine. The engine
applies it to the participant through the pure machine inside one store
transaction, adjusts the seat counter by `seatDelta`, and only after commit
runs the effects the state change implies. Webhooks and the tick are two more
sources of actions into the same path.

### Adaptation contract

The seam lives here rather than in a separate `references/adaptation.md`. The
rename table is in [data-model.md](references/data-model.md).

| Seam | This skill ships | The host supplies |
|---|---|---|
| Domain entities | event, participant, ticket, deposit, and a rename table | its vocabulary (class, session, attendee, and so on) |
| Tenant scope | `locationId` on events and participants, checked per route | its venue, site or workspace model |
| Auth | `getCustomer`, `getStaff`, `canAccessLocation` in `host.ts` | Clerk, NextAuth, Supabase, Firebase, or its own; with none, `getCustomer` and `getStaff` return `null`, never identity from headers, query, body or a shared key |
| Data access | `EventStore` port; Firestore and Postgres implementations | its SDK or ORM |
| Payments | `StripeGateway` behind `PaymentGateway`; webhook handler | Stripe keys; optional shared webhook |
| Stored credit | optional `BalanceLedger` port | its wallet (the sibling `ledger-wallet` skill implements the port), or `null` |
| Notifications | `Notifier` port, 11 notification kinds | its email or SMS provider and templates |
| Background work | one tick, every 5 minutes | its cron or scheduler |
| Currency | any ISO-4217, `usd` default, optional allow-list | its default and restriction |
| UI primitives | structure, states, copy rules | buttons, dialogs, tables, toasts |
| Styling | layout intent only | its design system |
| Strings | `events.*` keys and error codes | its i18n files, every locale |
| Validation | dependency-free parsers | its schema library, if preferred |

## Critical facts

1. **Holds expire.** About 7 days when the customer authorizes in Checkout, only **about 4 days 18 hours for a
   Visa hold the server places later**. Events settling within 6 days hold in Checkout; later ones save the
   card and the tick holds 4 days before settlement.
2. **`payment_intent.payment_failed` is not the end.** Checkout stays open
   after a decline; only `checkout.session.expired` ends a pending seat.
3. **Free means free in every currency.** A missing or zero price in the
   chosen currency on a paid event is a refusal, never a free ticket.
4. **Refunds use the amount frozen at registration**, never today's price.
5. **Money that arrives for a released seat goes back.** The seat is never
   resurrected, because it may already be resold.
6. **A repeated action returns the same object.** That single rule makes
   webhooks, double taps and cron retries safe.

## Hard rules

1. **Transaction first, Stripe second.** Never call Stripe inside a database transaction, and never write
   state after a Stripe call without a durable intent first. Transaction callbacks re-run, and a failed write
   after a capture loses the record of money moved.
2. **Identity never comes from the request body.** Customers from the session,
   guests by HMAC manage link, staff by the host guard with location scope on
   every `[eventId]` route.
3. **Never capture before settlement.** Check-in must be possible first; a hold
   that would lapse is renewed or released, never captured early.
4. **Cancelling an event is an action, not a status.** It refunds and releases
   everyone; a status flip would leave every participant charged.
5. **A webhook error is a 500.** Release the claim, answer 500 and let Stripe
   retry; a swallowed error is a payment nobody records.

## Quick start

Copy every block to the path on its first line, verbatim; edit only `lib/events/host.ts` (`HOST:` bodies,
store line). `test/fixtures.ts` and the three suites run as written, under Vitest. A template you think is
wrong stays as shipped: [provenance.md](references/provenance.md) may say why; if not, say so in the handover.

1. Model: [data-model.md](references/data-model.md), [money-and-time.md](references/money-and-time.md),
   [participant-lifecycle.md](references/participant-lifecycle.md).
2. Store: [firestore.md](references/firestore.md) or [postgres.md](references/postgres.md).
3. Engine and flows: [engine.md](references/engine.md), [registration.md](references/registration.md).
4. Stripe: [stripe.md](references/stripe.md); deposits: [no-show-deposits.md](references/no-show-deposits.md).
5. Routes: [api-routes.md](references/api-routes.md); screens: [ui.md](references/ui.md); tests:
   [testing.md](references/testing.md), [testing-lifecycles.md](references/testing-lifecycles.md).
6. Go live: [operations.md](references/operations.md). `.env.example` lists its five variables, empty, and
   the templates read them as shipped: no fallback, no other name, no extra check. Your final message names
   those five, the webhook endpoint and its eight event types, the 5-minute tick, that emails only log until
   the `Notifier` is wired, and, in an app without login, that staff routes answer 401 until `getStaff` is.

## Reference directory

| Scenario | Trigger keywords | Reference |
|---|---|---|
| Types, rename, seat counting | Event, Participant, seatsTaken, capacity, rename | [data-model.md](references/data-model.md) |
| Currencies, prices, time zones | ISO-4217, zero-decimal, ISK, KWD, USD default, DST, IANA, todayIn | [money-and-time.md](references/money-and-time.md) |
| States, actions, effects, due work | applyAction, PENDING, HELD, RELEASING, CAPTURING, nextActionAt | [participant-lifecycle.md](references/participant-lifecycle.md) |
| Deposits, holds, settlement, tick | no-show, capture_before, manual capture, off_session, SetupIntent, waive | [no-show-deposits.md](references/no-show-deposits.md) |
| Checkout, webhooks, test cards | checkout.session.completed, expired, charge.refunded, idempotency, whsec | [stripe.md](references/stripe.md) |
| Register, cancel, refund flows | register, capacity, guest link, late cancel, refund, cancel event | [registration.md](references/registration.md) |
| Engine wiring and ports | createEventsEngine, EventStore, BalanceLedger, Notifier | [engine.md](references/engine.md) |
| Firestore store | collection group, transaction, rules, indexes | [firestore.md](references/firestore.md) |
| Postgres store | schema, FOR UPDATE, jsonb, RLS, Supabase | [postgres.md](references/postgres.md) |
| Routes, auth, errors | route handler, requireStaffForEvent, CRON_SECRET, 409 | [api-routes.md](references/api-routes.md) |
| Screens | registration dialog, check-in screen, admin form, manage page | [ui.md](references/ui.md) |
| Core and state-machine tests | vitest, fixtures, fake gateway, in-memory store | [testing.md](references/testing.md) |
| Lifecycle tests | end-to-end, regression, redelivered webhook, late payment, capacity | [testing-lifecycles.md](references/testing-lifecycles.md) |
| Env, cron, monitoring, emails | env vars, vercel cron, reconciliation, go-live | [operations.md](references/operations.md) |
| What the audit changed and why | audit, provenance, kept deliberately, order of work | [provenance.md](references/provenance.md) |

Part of the [Timerise Skills](https://github.com/timerise-ai/skills) index, which lists the sibling skills.
