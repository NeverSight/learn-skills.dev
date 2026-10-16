---
name: calendar-scheduling-links
description: >
  Build self-hosted scheduling links in a Next.js App Router app: a public booking page per host and event
  type, weekly availability with date overrides, buffers, minimum notice, daily limits and a rolling horizon,
  one-on-one and group event types, Google Calendar and Microsoft 365 busy-time sync and event write-back,
  confirmation e-mails with an ICS invite, reminders, reschedule and cancel by a private link, signed
  webhooks and an embeddable widget. Use when: (1) a team wants its own Calendly-style booking pages instead
  of a per-seat subscription, (2) an app needs "book a time with me" links for coaches, advisors, sales or
  support, (3) an existing scheduling module double-books, drifts across DST, sends stale reminders or
  duplicates calendar events, (4) the user mentions: scheduling link, booking page, Calendly alternative,
  Calendly clone, Cal.com alternative, event types, availability rules, date overrides, buffer time, minimum
  notice, daily limit, round robin, time slots, free busy, freeBusy, calendarView, Google Calendar sync,
  Outlook sync, Microsoft Graph subscription, watch channel, ICS invite, METHOD:REQUEST, SEQUENCE,
  reschedule link, cancel link, embed widget, booking webhook, double booking, DST, exclusion constraint,
  btree_gist, pg_cron. Carries one pure slot engine that the page and the write both call, a per-host lock
  with a Postgres exclusion constraint, side effects as leased idempotent jobs, sealed OAuth tokens, signed
  state and channel tokens, and 53 unit tests plus a store contract run on Supabase and the Firestore
  emulator. Next.js App Router on Vercel; Supabase by default, Firestore behind the same SchedulingStore
  seam. Not payments, not team round robin in this release, not a video meeting service.
---

# Calendar Scheduling Links

A scheduling page is a list of free times and a button. The hard part is the write: two people on one page,
a calendar that changed a minute ago, a DST night, a reminder for a booking that moved. This skill computes
slots with **one pure function that the page lists and the booking route calls again for the requested
start**, writes the booking **under one lock per host with an exclusion constraint as the backstop**, and
turns every side effect into **a leased, idempotent job written in the same transaction**.

## When to use

- Public booking pages for one or many hosts, each with their own event types and availability.
- One-on-one meetings and group sessions with seats.
- Avoiding the host's Google or Microsoft calendar, and writing bookings into it.
- Auditing or rebuilding a scheduling module: [provenance.md](references/provenance.md) has the audit
  ledger and the fix order.

## When NOT to use

- **Taking payment for a booking, deposits, no-show holds**: the sibling `bookable-events` skill, or
  `stripe-connect-subscriptions` for a marketplace. [extensions.md](references/extensions.md) shows the join.
- **Capacity-limited events with tickets (a workshop on one date)**: `bookable-events`.
- **A walk-up touchscreen terminal**: `booking-kiosk`, which can call this module's service.
- **Round robin, collective and routing forms**: described in [extensions.md](references/extensions.md),
  with no templates in this release.
- **Video meetings themselves**: the module creates Google Meet or Teams links through the calendar APIs.

## Architecture

```
 public page /[handle]/[event]     widget: slots by the visitor's zone, form, 409 means "just taken"
   |  GET /api/scheduling/slots                    POST /api/scheduling/bookings
   v                                                 v
 computeSlots(rules, overrides, bookings, busy) <-- createBooking: same engine for the one start
   ^                                                 |  store.book: per-host lock, seats, daily limit,
   | busy_blocks (mirrored)                          |  exclusion constraint, booking + jobs in one tx
   |                                                 v
 calendar sync <-- push notice / cron        jobs: e-mail + ICS, host e-mail, calendar upsert,
   Google, Microsoft (OAuth, sealed tokens)        reminders, signed webhooks; leased, retried
                                                     ^
 manage page /booking/[token]  reschedule, cancel ---+   cron every 5 min: jobs, watches, sync
```

### Adaptation contract

[adaptation.md](references/adaptation.md) has the full contract, the host prerequisites and the order of
work. The rename table is in [data-model.md](references/data-model.md).

| Seam | This skill ships | The host supplies |
|---|---|---|
| Auth | `currentHostId()` for Supabase Auth | Its session lookup |
| Data | `SchedulingStore` on Supabase and Firestore, `CalendarStore` on Supabase | Its project |
| E-mail | `Mailer` with SendGrid | Its provider and wording |
| UI | Structure, behaviour, ARIA; no styling | Its components and tokens |
| Scheduler | One cron route | Vercel Cron (Pro) or Supabase `pg_cron` |

## Critical facts

1. **A slot is never stored.** It is `computeSlots` output; a booking stores the start, the blocked range and
   a `slotKey` that seats of one group slot share.
2. **Availability is per host, across event types.** A booking of any event type blocks the host.
3. **Buffers add up.** Each booking freezes its own blocked range; two 15-minute buffers need a 30-minute gap.
4. **Days are local dates.** The engine iterates dates in the schedule's zone; the widget groups by the
   visitor's zone.
5. **The manage token is HMAC(secret, booking id)** and only its SHA-256 is stored, so a job can rebuild the
   link and a leaked table cancels nothing.
6. **A reschedule is a new booking on the same chain.** The chain id gives one calendar event and one ICS UID;
   `sequence` rises with every change.
7. **Busy time is mirrored into `busy_blocks`.** Push notices and the cron refresh it; slot queries never call
   a provider.
8. **Vercel Hobby runs crons once a day.** Use Supabase `pg_cron`: [operations.md](references/operations.md).

## Hard rules

> **1. The write recomputes the slot with the engine that listed it.** A start is booked only if
> `computeSlots` offers it at write time.

> **2. Every booking write is atomic per host.** Seats, the daily limit and overlap are checked under one lock
> per host, with the overlap constraint as the backstop.

> **3. Side effects are jobs, written with the change and run after it.** No e-mail, calendar call or webhook
> inside the transaction; every job idempotent and re-checking the booking.

> **4. Instants in storage, zones only at the edges.** Store UTC instants; convert with an explicit IANA zone,
> iterate local dates, never add 24 hours.

> **5. Secrets stay sealed and links stay unforgeable.** Manage tokens stored as hashes, OAuth tokens and
> webhook secrets encrypted, OAuth state and channel tokens signed, cron auth failing closed.

## Quick start

1. Probe the host and fill the seam table and rename table: [adaptation.md](references/adaptation.md),
   [data-model.md](references/data-model.md).
2. Copy the time helpers and the engine, run their suites: [time-and-slots.md](references/time-and-slots.md),
   [testing.md](references/testing.md); flow suites in [testing-flows.md](references/testing-flows.md).
3. Apply the migration and copy the stores: [supabase.md](references/supabase.md) and
   [supabase-stores.md](references/supabase-stores.md), or [firestore.md](references/firestore.md).
4. Copy the service, tokens and validation, run the booking suite:
   [booking-flow.md](references/booking-flow.md).
5. Copy jobs, e-mail, ICS and webhooks: [jobs-and-notifications.md](references/jobs-and-notifications.md),
   [webhooks.md](references/webhooks.md).
6. Copy the routes, `runtime.ts` and `host.ts`; on Supabase Auth `host.ts` is used unchanged:
   [api-routes.md](references/api-routes.md).
7. Build the pages and dashboard with the host's components:
   [booking-page-ui.md](references/booking-page-ui.md).
8. Add calendar sync: [calendar-sync.md](references/calendar-sync.md),
   [calendar-providers.md](references/calendar-providers.md).
9. Set the environment by the exact names in [operations.md](references/operations.md), and an `.env.example`
   with all of them, empty; then the cron, and deploy.
10. Extend only along [extensions.md](references/extensions.md). Before changing a template, read
    [provenance.md](references/provenance.md).

Copy the templates and the suites as written, the lines a reference calls odd on purpose too; what you add
goes in new files. The final message itself names every variable, then what is left to set up: the migration,
the cron, the e-mail sender, and each OAuth app with its redirect URI.

## Reference directory

| Scenario | Trigger keywords | Reference |
|---|---|---|
| Vocabulary, fields, renaming | event type, schedule, booking, invitee, chainId, slotKey, rename | [data-model.md](references/data-model.md) |
| Computing free times | slots, availability, override, buffer, notice, horizon, daily limit, DST, time zone | [time-and-slots.md](references/time-and-slots.md) |
| Booking, reschedule, cancel | createBooking, double booking, 409, manage token, reschedule, cancel | [booking-flow.md](references/booking-flow.md) |
| Postgres and Supabase | migration, RLS, service_role, exclusion constraint, btree_gist, advisory lock | [supabase.md](references/supabase.md) |
| Supabase store code | supabaseStore, supabaseCalendarStore, rpc, row mapping, PostgREST | [supabase-stores.md](references/supabase-stores.md) |
| Firestore | firebase-admin, transaction, lock document, indexes, emulator | [firestore.md](references/firestore.md) |
| E-mail, ICS, reminders | jobs, outbox, retry, backoff, lease, SendGrid, ICS, UID, SEQUENCE, METHOD | [jobs-and-notifications.md](references/jobs-and-notifications.md) |
| Outgoing webhooks | webhook, HMAC, Scheduling-Signature, SSRF, private address, BlockList, ::ffff, DNS rebinding, redirect | [webhooks.md](references/webhooks.md) |
| Calendar connection and sync | OAuth, PKCE, signed state, refresh token, invalid_grant, busy_blocks, watch renewal, disconnect | [calendar-sync.md](references/calendar-sync.md) |
| Google and Microsoft APIs | events.list, calendarView, events.insert, transactionId, subscription, clientState, showAs | [calendar-providers.md](references/calendar-providers.md) |
| Routes and secrets | route handler, after(), CRON_SECRET, AES-GCM, currentHostId | [api-routes.md](references/api-routes.md) |
| Pages, widget, embed, dashboard | booking page, iframe, postMessage, manage page, aria | [booking-page-ui.md](references/booking-page-ui.md) |
| Environment, cron, provider setup, deploy | env, vercel.ts, pg_cron, Google verification, Entra, monitoring | [operations.md](references/operations.md) |
| Round robin, routing, payments | round robin, collective, routing form, Stripe, polls, SMS | [extensions.md](references/extensions.md) |
| Tests: setup, time, engine | vitest, fixtures, DST tests, emulator, local Supabase | [testing.md](references/testing.md) |
| Tests: booking, edges, contract | concurrency, reschedule, ICS, signature, store contract | [testing-flows.md](references/testing-flows.md) |
| Seams and order of work | adapt, host probe, non-negotiables | [adaptation.md](references/adaptation.md) |
| Why it is built this way | audit, defect, kept deliberately, added | [provenance.md](references/provenance.md) |

Part of the [Timerise Skills](https://github.com/timerise-ai/skills) index, which lists the sibling skills.
