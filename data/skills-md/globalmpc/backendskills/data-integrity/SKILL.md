---
name: data-integrity
description: Rules for code that writes to the database where two requests, retries or jobs can run at once. Use for anything that changes money, stock, balances, counters or statuses, creates rows that must be unique, or calls a payment provider, email or other outside service. Applies in endpoints, webhooks and background jobs.
---

# Data integrity

Examples are TypeScript with `pg`. The rules apply to any stack. Assume every write can run twice at the
same time: two clicks, a client retry, two servers picking up the same job.

## 1. Read-then-write is one conditional statement, or one transaction with a lock

Why: two requests at once both read "1 seat left", both book it. Counts go negative and money gets created.

```ts
// Bad: check and write are separate; a concurrent request slips in between
const { rows: [e] } = await pool.query("select seats_left from events where id = $1", [id]);
if (e.seats_left < seats) return sendError(res, 409, "sold_out", "Not enough seats");
await pool.query("update events set seats_left = seats_left - $1 where id = $2", [seats, id]);

// Good: the check is part of the write
const { rowCount } = await client.query(
  "update events set seats_left = seats_left - $1 where id = $2 and seats_left >= $1", [seats, id]);
if (rowCount === 0) throw new HttpError(409, "sold_out", "Not enough seats");
```

When several rows must change together (every line of a booking, both accounts in a payment), do it in one
transaction. Put a database CHECK behind it (`seats_left >= 0`, `balance_cents >= 0`) as the last line of
defence.

## 2. Uniqueness is a UNIQUE constraint, not a check before the insert

Why: two requests both find "no row yet" and both insert. You get two accounts per email or two reviews
per user.

```ts
// Bad: a concurrent request inserts between the select and the insert
const { rows } = await pool.query("select 1 from memberships where team_id = $1 and user_id = $2", [team, user]);
if (rows.length) return sendError(res, 409, "already_member", "Already a member");
await pool.query("insert into memberships (team_id, user_id) values ($1, $2)", [team, user]);

// Good: unique (team_id, user_id) in the schema; the database decides who was first
const { rowCount } = await pool.query(
  "insert into memberships (team_id, user_id) values ($1, $2) on conflict do nothing", [team, user]);
if (rowCount === 0) return sendError(res, 409, "already_member", "Already a member");
```

## 3. Lock rows in a fixed order

Why: request A locks row 1 then row 2 while request B locks 2 then 1, and Postgres kills one of them with a
deadlock. Two payments between the same two accounts, in opposite directions, are enough to cause it.

```ts
// Bad: lock order follows the request (payer first, lines in the order given)
for (const id of [payerId, payeeId]) await client.query("select ... where id = $1 for update", [id]);

// Good: always lowest id first, in one statement
await client.query("select id, balance_cents from accounts where id = any($1) order by id for update",
  [[payerId, payeeId]]);
```

## 4. Never call an outside service inside a transaction

Why: the payment provider, HTTP, email all take tens of milliseconds to seconds. During that wait the
transaction holds its row locks and a pool connection. Under load every connection is held and the app
hangs. This is worse still if the client library uses the same pool.

```ts
// Bad: charge while the seat rows are locked
await client.query("begin");
await holdSeats(client, seats);
const { paymentId } = await payments.charge({ amountCents: total });
await client.query("commit");

// Good: short write, call, short write
const bookingId = await tx(async (c) => { await holdSeats(c, seats); return createBooking(c, "pending"); });
try {
  const { paymentId } = await payments.charge({ amountCents: total, idempotencyKey: `booking-${bookingId}` });
  await pool.query("update bookings set status = 'paid', payment_id = $2 where id = $1", [bookingId, paymentId]);
} catch (err) {
  await tx(async (c) => { await releaseSeats(c, seats); await markBooking(c, bookingId, "failed"); });
  return sendError(res, 502, "payment_failed", "Payment failed");
}
```

## 5. Anything that charges, refunds or sends gets an idempotency key

Why: a retry (by the client, a proxy, or your own code after a timeout) charges the customer twice.

- Pass a key derived from your own record (`booking-<id>`, `refund-<bookingId>`), not a random one per attempt.
- Change state only from the state you expect (`update bookings set status = 'cancelled' where id = $1 and
  status = 'paid'`), and act only if a row changed. Two cancellations at once must not both refund.
- Events can arrive twice or out of order (webhooks, queue messages). Handling one must not move a record
  back to an earlier state.

## 6. Test it with requests at once

Why: every bug above passes a test that sends one request at a time.

Send the same write 10–20 times in parallel (`Promise.all`) and check the end state: counts never below 0,
money neither created nor lost, one charge per order, no deadlock errors.

## Make it yours

Your team's choices. Until you change a line, it's the default.

- **Transactions:** `pool.connect()` + `begin`/`commit`/`rollback`, or the repo's transaction helper if it has one.
- **Payment and email clients:** take an `idempotencyKey` argument; check the client in the repo for its name.
