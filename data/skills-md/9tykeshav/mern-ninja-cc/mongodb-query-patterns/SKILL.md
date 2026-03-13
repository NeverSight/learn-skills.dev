---
name: mongodb-query-patterns
description: Use when writing ANY Mongoose query (.find, .findOne, .findById, .aggregate, .populate), adding database operations to services or controllers, wiring data between services, building endpoints that read or write to MongoDB, or reviewing code that chains service calls. TRIGGER especially when about to write a new findById or pass an ID where a document could be passed instead.
---

# MongoDB Query Patterns

## Overview

The best query is the one you never make. The second best is the one that fetches only what it needs in a single round-trip.

Before writing any database call, ask: **does this data already exist somewhere in the current request chain?** If a controller fetched a document and then calls three services, those services should receive the document — not re-fetch it. Pass documents, not IDs.

**Think in data flow, not individual queries.** Trace how data moves through the request (controller → services → response) and ensure each document makes that journey exactly once.

## When to Use

- Adding any new database operation to a service or controller
- Building a new endpoint that reads or writes data
- Wiring service calls together in a controller or orchestration function
- Adding or modifying Mongoose schemas
- Reviewing code that chains multiple service calls

## Data Flow Principles

### 1. Trace the Request Chain First

Before writing code, map the data flow:

```
Request → Controller → Service A → Service B → Service C → Response
                          ↓            ↓            ↓
                        needs        needs        needs
                       doc X        doc X        doc X
```

If multiple stops need the same document, fetch it **once** at the top and pass it down. Don't let each service independently query for what the caller already has.

### 2. Fetch Wide at the Top, Narrow Below

The first service in the chain may need a broader projection. Downstream services should accept the already-fetched document rather than re-querying with their own narrower projection. A few extra fields in memory cost nothing compared to an extra database round-trip.

### 3. Every Query Must Justify Its Existence

When you're about to write a `findById` or `findOne`, ask:

- Is this document already available from the caller? → **Accept it as a parameter**
- Is this the same document another branch of the code fetches? → **Hoist it above the branch**
- Am I querying N documents one at a time in a loop? → **Batch with `$in`**
- Am I querying just to count or aggregate? → **Can I derive it from data I already have?**

If none of these apply, the query is justified — write it efficiently.

## Query Efficiency Rules

When a query *is* justified, make it lean:

| Rule | How | Why |
|---|---|---|
| Project only needed fields | `.select('name email status')` | Full documents carry every field — list exactly what the caller needs, never widen "just in case" |
| Return plain objects for reads | `.lean()` | Skips Mongoose hydration — 2-5x faster for read-only paths |
| Ensure filter fields are indexed | `schema.index({ field: 1 })` | Without an index, MongoDB scans every document (COLLSCAN) |
| Batch related reads | `.find({ _id: { $in: ids } })` + Map | N round-trips collapse to 1 |
| Batch related writes | `Model.bulkWrite([...])` | N sequential updates collapse to 1 |

## Patterns

### Pass Data Through Service Boundaries

The most common source of waste: services that re-fetch documents the caller already has.

```typescript
// WRONG — each service queries the same document independently
async function checkout(orderId: string) {
  const order = await Order.findById(orderId).lean();
  await validateInventory(orderId);    // fetches order again
  await calculateTax(orderId);         // fetches order again
  await processPayment(orderId);       // fetches order again
}

// RIGHT — fetch once, pass through, always provide DB fallback
async function validateInventory(orderId: string, prefetched?: IOrder) {
  const order = prefetched
    || await Order.findById(orderId).select('items quantities').lean();
  // ...
}

async function checkout(orderId: string) {
  const order = await Order.findById(orderId).lean();
  await validateInventory(orderId, order);
  await calculateTax(orderId, order);
  await processPayment(orderId, order);
}
```

**Always keep the DB fallback.** Some callers (webhooks, cron jobs, background workers) won't have pre-fetched data.

### Batch Instead of Loop

When you need related data for a list of items, fetch everything in one query and index with a Map.

```typescript
// WRONG — N+1: one query per item
for (const order of orders) {
  const product = await Product.findById(order.productId);
  // ...
}

// RIGHT — 1 query + O(1) lookups
const productIds = orders.map(o => o.productId);
const products = await Product.find({ _id: { $in: productIds } })
  .select('name price image')
  .lean();
const productMap = new Map(products.map(p => [p._id.toString(), p]));

for (const order of orders) {
  const product = productMap.get(order.productId.toString());
  // ...
}
```

**Always use a Map for lookups** — never `array.find()` inside a loop (O(n²)).

### Hoist Common Queries

When the same query appears in multiple code branches, it should execute once before the branch.

```typescript
// WRONG — identical query in both branches
if (userProvidedId) {
  const doc = await Order.findById(orderId).select('status').lean();
  // validate...
} else {
  const doc = await Order.findById(orderId).select('status').lean();
  // use directly...
}

// RIGHT — query once
const doc = await Order.findById(orderId).select('status').lean();
if (userProvidedId) { /* validate */ } else { /* use */ }
```

### Consolidate Same-Collection Queries

If you need multiple aggregates from the same collection, fetch the data once and compute in memory.

```typescript
// WRONG — two round-trips to the same collection
const totalCount = await Booking.countDocuments({ eventId });
const perTypeCount = await Booking.aggregate([
  { $match: { eventId } },
  { $group: { _id: '$ticketType', count: { $sum: 1 } } },
]);

// RIGHT — one fetch, derive both
const bookings = await Booking.find({ eventId })
  .select('ticketType')
  .lean();
const totalCount = bookings.length;
const perTypeCount = new Map();
for (const b of bookings) {
  perTypeCount.set(b.ticketType, (perTypeCount.get(b.ticketType) || 0) + 1);
}
```

*For bounded collections (e.g., bookings per event) this is safe. For unbounded collections, keep aggregation server-side.*

### Bulk Writes Over Loops

```typescript
// WRONG — N sequential round-trips
for (const item of items) {
  await Item.findByIdAndUpdate(item._id, { $set: { archived: true } });
}

// RIGHT — 1 round-trip
await Item.bulkWrite(
  items.map(i => ({
    updateOne: {
      filter: { _id: i._id },
      update: { $set: { archived: true } },
    },
  }))
);
```

### Avoid Hidden N+1 from `.populate()`

`.populate()` fires a separate query per populated path. Nested or chained populates on lists are silent N+1 bombs.

```typescript
// WRONG — if orders has 50 items, this fires 50+ hidden queries
const orders = await Order.find({ userId })
  .populate('product')
  .populate('seller')
  .populate('reviews');

// RIGHT — batch manually
const orders = await Order.find({ userId }).select('product seller').lean();
const productIds = orders.map(o => o.product);
const sellerIds = orders.map(o => o.seller);

const [products, sellers] = await Promise.all([
  Product.find({ _id: { $in: productIds } }).select('name price').lean(),
  Seller.find({ _id: { $in: sellerIds } }).select('name rating').lean(),
]);
const productMap = new Map(products.map(p => [p._id.toString(), p]));
const sellerMap = new Map(sellers.map(s => [s._id.toString(), s]));
```

`.populate()` is fine for single-document lookups. Avoid it when populating across a list.

### Update Directly — Don't Fetch to Modify

When updating a field, don't fetch the whole document just to change it and save it back.

```typescript
// WRONG — 2 round-trips, fetches entire document
const user = await User.findById(userId);
user.lastLogin = new Date();
await user.save();

// RIGHT — 1 round-trip, touches only the field
await User.updateOne(
  { _id: userId },
  { $set: { lastLogin: new Date() } }
);
```

Use `findById` + `.save()` only when you need validation, middleware hooks, or optimistic concurrency.

### Run Independent Queries Concurrently

When you need data from multiple collections and the queries don't depend on each other, run them in parallel.

```typescript
// WRONG — sequential, each waits for the previous
const users = await User.find({ _id: { $in: userIds } }).select('name email').lean();
const responses = await FormResponse.find({ eventId }).select('userId answers').lean();
const reviews = await Review.find({ eventId }).select('userId rating').lean();

// RIGHT — concurrent, all fire at once
const [users, responses, reviews] = await Promise.all([
  User.find({ _id: { $in: userIds } }).select('name email').lean(),
  FormResponse.find({ eventId }).select('userId answers').lean(),
  Review.find({ eventId }).select('userId rating').lean(),
]);
```

Use `Promise.all` whenever queries don't depend on each other's results. Three 100ms queries run concurrently take 100ms total, not 300ms.

### Index Every Filter Field

```typescript
schema.index({ order_id: 1 });                 // single field
schema.index({ userId: 1, status: 1 });         // compound — high-selectivity field first
schema.index({ event_id: 1, type: 1 });         // compound for filtered aggregations
```

- Mongoose auto-creates indexes on connection (`autoIndex: true`)
- `createIndex()` is idempotent — safe to define even if the index exists
- Verify with `explain('executionStats')` — look for `IXSCAN`, not `COLLSCAN`
- Don't index write-only fields — indexes slow inserts and updates

## Checklist

Before committing any code that touches the database:

```
[ ] Traced the request chain — no document is fetched more than once across the call stack
[ ] Services accept pre-fetched documents as optional params with DB fallback
[ ] Passing documents between functions, not just IDs
[ ] No query executes inside a loop — batched with $in where needed
[ ] No .populate() on a list of documents — batch manually with $in + Map
[ ] Every read query has .select() with only needed fields
[ ] Every read-only query has .lean()
[ ] Updates that don't need hooks use updateOne/bulkWrite, not findById + save
[ ] Filter fields have corresponding schema.index() definitions
[ ] Multiple writes use bulkWrite, not a loop
[ ] Independent queries run concurrently with Promise.all
[ ] Same query doesn't appear in multiple code branches — hoisted above
[ ] .select() lists exactly the fields needed — not widened "just in case"
```

## Common Mistakes

| Mistake | Why It Breaks |
|---|---|
| Passing IDs between services instead of documents | Forces every downstream service to re-query — pass the document |
| `.populate()` on a list of documents | Each populate fires a separate query per document — silent N+1 |
| `findById` + modify + `.save()` for simple field update | 2 round-trips + full document fetch — use `updateOne` directly |
| `.select()` without `.lean()` | Still returns Mongoose document with full change tracking overhead |
| `.lean()` then calling `.save()` | `.lean()` returns plain objects — no Mongoose methods available |
| Batch `$in` + `array.find()` for lookup | O(n²) — always use a Map for O(1) lookups |
| Prefetch param without DB fallback | Breaks webhook/cron callers that don't have the pre-fetched data |
| Sequential independent queries | Use `Promise.all` — 3 queries at 100ms each take 100ms, not 300ms |
| Widening `.select()` "just in case" | Fetch only what the caller actually uses — extra fields waste bandwidth |
| Unbounded `.find()` without limit | Risk of loading entire collection into memory |
| Index on rarely-queried field | Indexes slow every write for no read benefit |
