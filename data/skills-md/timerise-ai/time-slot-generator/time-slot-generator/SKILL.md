---
name: time-slot-generator
description: >
  Build a strategy-driven time-slot generator with availability in a Next.js App Router app: daily ranges,
  Nth-weekday-of-month rules, one-off slots and whole-day slots, authored in local wall-clock time and stored
  as UTC instants, with seats, bookings, blackouts, host busy time, shared resources and working hours
  subtracted, a listing route and a booking route that re-checks capacity in the write transaction. Use
  when: (1) an app needs appointment, class, rental or reservation slots generated from rules rather than
  stored one by one, (2) slot code gives wrong days around DST, wrong weekdays far from UTC, a week view
  with one day, or times that change with the server's time zone, (3) strategies must be validated, pinned
  to a zone, or moved off wall-clock-as-UTC storage, (4) two guests can book the last seat at once, (5)
  the user mentions: time slots, slot generator, availability, booking slots, opening hours, slot strategy,
  RANGE, PERIODICITY, DAY_RANGE, ONCE, slotInterval, slotDuration, slotsLimit, daysLimit, first Monday of
  the month, last Friday, overnight slots, lead time, booking window, timeOffset, IANA time zone, DST,
  fromZonedTime, storageVersion, slot ID, md5, overbooking, capacity check, book_slots,
  slot-no-longer-available, slot-has-not-enough-capacity. Carries a dependency-free engine on Intl with a
  23-test suite run under four process time zones, slot IDs that stay stable for existing bookings, one
  availability map for listing and booking, and a capacity re-check inside the booking transaction on both
  backends. Next.js App Router route handlers on the Node.js runtime; Firestore or Supabase/Postgres
  behind the SlotStore seam. Not a calendar UI, not RRULE or iCalendar recurrence, not payments or
  booking-flow screens.
---

# Time-Slot Generator

Slots are never stored. Strategies are stored, slots are regenerated from them on every read, and a booking
finds its slot again by a deterministic ID. Everything in this skill follows from that: the generator is
**a pure function of strategies, now and viewport whose output does not depend on the viewport, the
server's time zone or the day of the year**, so a slot that was on screen is still there when the guest
presses "book".

## When to use

- Generating bookable slots from rules: "Monday to Friday 09:00 to 17:00 every 30 min", "first and last
  Friday of each month 18:00 to 20:00", "whole days, weekends only", "this one Saturday 10:00 to 14:00".
- Showing availability: capacity per slot, minus bookings, blackouts, a host's other commitments, shared
  rooms or equipment, and outside working hours.
- Booking slots by ID with a capacity re-check that holds under concurrent requests.
- Fixing slot code with time-zone bugs, or moving one off wall-clock-as-UTC storage.

## When NOT to use

- **The booking screens or a kiosk flow**: `booking-kiosk`, which consumes the slots this skill produces.
- **Public scheduling links per host with calendar sync and e-mail**: `calendar-scheduling-links`.
- **Calendar recurrence (RRULE, iCalendar, Google or Outlook event series)**: `rrule` or the provider's
  API. Strategies describe bookable capacity, not events.
- **Payments, deposits, invoices**: `bookable-events`, `invoicing`.

## Architecture

```
 strategies (DB) --normalizeStrategy--> SlotStrategy[] --generateSlots(now, viewport)--> GeneratedSlot[]
                                                                                              |
 bookings, busy blocks, host bookings, resources, working hours --SlotStore--> buildAvailability
                                                                                              |
   GET /api/slots       listServiceSlots: toSlotOutput (UTC + local offset) <-----------------+
   POST /api/bookings   prepareBookingSlots(ids): one generation, then lookups <--------------+
                          |
                          v
                        book_slots / assertCapacityInTransaction: seats re-counted in the write
```

The engine (`lib/slots/`) is plain TypeScript with no Next.js import. The routes are the only files that
touch the framework, and `SlotStore` is the only one that touches the database.

### Adaptation contract

[adaptation.md](references/adaptation.md) holds the full contract, the rename table, the order of work and
the non-negotiables.

| Seam | The skill ships | The host supplies |
|---|---|---|
| Domain words | Service, Strategy, Booking, Host, Location, Resource, BusyBlock, project | Its names |
| Tenant and auth | `projectId` read from the stored service; a marked guard slot | Its guard before writes |
| Data access | `SlotStore` on Firestore and on Supabase | Its project and schema |
| Routes | Listing and booking route handlers on Supabase | Its URL scheme |
| Slot IDs | md5 via `node:crypto` | A pure md5 on the Edge runtime |
| Strings and UI | Error codes only, no screens | Its i18n and its slot picker |

## Critical facts

1. **Store instants in UTC, author in wall clock, pin the zone.** `start.time: "09:00"` means 09:00 in the
   strategy's `timeZone`, fixed at create time, so a later change to the project's zone does not move
   existing slots.
2. **Iterate local calendar dates, never `+24h`.** A DST day is 23 or 25 hours, and adding 24 hours to 23:30
   the evening before a spring-forward day lands two local days later.
3. **Emit chronologically before you stop early.** Generators stop at the first slot past a cutoff, so
   candidates produced weekday by weekday would end a week view after its first weekday.
4. **Limits count from the strategy start, never from the viewport.** Otherwise "the first 10 slots" depends
   on which week the client asks for, and a slot visible in one view is unbookable.
5. **The server's time zone does not matter.** `new Date('2026-03-29T09:00')` is parsed in the process zone
   and `getUTCDay()` on a shifted Date is right only in a UTC process, so the engine uses the Intl helpers.
6. **One generation per booking, then lookups.** Regenerating per requested slot multiplies the work by the
   number of slots in the booking.
7. **Generation is stale by the time you write.** Two guests can both have seen the last seat, so seats are
   re-counted inside the booking transaction.

## Hard rules

1. **Never change the slot ID input.** `md5("<utcStartISO>;<duration>;<strategyId>")` is the identity every
   client and every booking holds; a different input orphans them all.
2. **Never infer "overnight" from end before start.** A reversed range is far more often a typo than a night
   shift, so an overnight window needs `overnight: true`.
3. **Never generate without a horizon.** `maxHorizonDays` and `maxSlots` cap every strategy, since one with
   no end would otherwise generate until 2038.
4. **Never filter availability in the listing only.** The listing and the booking path read one
   `buildAvailability` map, so an ID cannot book what the listing hides.
5. **Never count a host's booking of this service as host busy time.** It already subtracts seats as a
   `BOOKING`; blocking on it as well hides a slot that still has room.

## Quick start

Copy the code blocks with this command from the app root, `S` set to this skill's folder; never retype them,
retyped files drift. It writes each `ts` block to the path on its first line and the schema to
`supabase/schema.sql`. On Firestore, name `firestore-backend` in place of the last two references.

```bash
node -e 'const fs = require("fs"), path = require("path"), put = (out, body) =>
  (fs.mkdirSync(path.dirname(out), { recursive: true }), fs.writeFileSync(out, body));
for (const text of process.argv.slice(1).map(file => fs.readFileSync(file, "utf8"))) {
  for (const m of text.matchAll(/\x60{3}ts\n(\/\/ ((?:lib|app)\/[^:\s]+):[\s\S]*?)\x60{3}/g)) put(m[2], m[1]);
  for (const m of text.matchAll(/\x60{3}sql\n([\s\S]*?)\x60{3}/g)) put("supabase/schema.sql", m[1]);
}' "$S"/references/{strategy-model,timezones,generators,availability,testing,supabase-backend,nextjs-routes}.md
```

The only edits after it are the rename table, the guard at the marked line, and `book_slots` extended with
the host's booking columns. A template that looks wrong is named in the handover, never patched.

1. Read the host and fill the seam contract and the rename table: [adaptation.md](references/adaptation.md).
2. Run the command, then read what it wrote: the model in [strategy-model.md](references/strategy-model.md),
   zones in [timezones.md](references/timezones.md), the engine in [generators.md](references/generators.md),
   availability in [availability.md](references/availability.md).
3. `npm i -D vitest`, change only the suite's `node:test` import, wire `npm test` to the four-`TZ` loop and
   run it: [testing.md](references/testing.md). Your own tests go in a separate file.
4. `npm i` the backend SDK (`@supabase/supabase-js` or `firebase-admin`), never a hand-written client:
   [supabase-backend.md](references/supabase-backend.md) or
   [firestore-backend.md](references/firestore-backend.md). The package registry is not an external service.
5. Serve it from route handlers: [nextjs-routes.md](references/nextjs-routes.md).
6. Rebuilding an existing engine? [provenance.md](references/provenance.md) has the ledger and the fix
   order, and [testing.md](references/testing.md) the differential check.

Hand over, every time: the schema file or indexes to apply; `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY`
(server only); the file and line where the host's guard goes, and that bookings are public until it does;
"23 shipped tests pass under four zones", with any tests of your own counted apart.

## Reference directory

| Scenario | Trigger keywords | Reference |
|---|---|---|
| Seams, renaming, order of work | adapt, host, rename, tenant, auth guard, non-negotiables | [adaptation.md](references/adaptation.md) |
| Strategy shape, fields, validation | RANGE, PERIODICITY, ONCE, DAY_RANGE, tendency, timeOffset, slotsLimit, overnight, strategy-bounds-invalid | [strategy-model.md](references/strategy-model.md) |
| Time zones and DST | IANA, wall clock, UTC, DST gap, overlap, fromZonedTime, offset, storageVersion, legacy | [timezones.md](references/timezones.md) |
| Producing slots | generateSlots, horizon, maxSlots, truncated, slot ID, md5, chronological, viewport | [generators.md](references/generators.md) |
| What is still free | availability, seats, BOOKING, BLOCK, working hours, resource, capacity, overbooking, prepareBookingSlots | [availability.md](references/availability.md) |
| Supabase and Postgres | timestamptz, jsonb, RLS, with check, gin index, book_slots, advisory lock | [supabase-backend.md](references/supabase-backend.md) |
| Firestore | firebase-admin, Timestamp, composite index, array-contains-any, onSnapshot, runTransaction | [firestore-backend.md](references/firestore-backend.md) |
| Route handlers | app/api/slots, app/api/bookings, route.ts, Node.js runtime, 409, SUPABASE_SERVICE_ROLE_KEY | [nextjs-routes.md](references/nextjs-routes.md) |
| Proving it | node:test, vitest, npm test, TZ=, DST regression, Lord Howe, Auckland, differential check | [testing.md](references/testing.md) |
| Why it is built this way | provenance, audit, kept deliberately, fix order | [provenance.md](references/provenance.md) |

Part of the [Timerise Skills](https://github.com/timerise-ai/skills) index, which lists the sibling skills.
