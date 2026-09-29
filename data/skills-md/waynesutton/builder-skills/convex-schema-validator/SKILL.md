---
name: convex-schema-validator
description: Designs convex/schema.ts tables, validators, indexes, and relationships, and keeps the schema honest as data evolves. Use when creating tables, adding fields, choosing index fields, modeling relationships, or when a validator error appears at deploy time.
---

# Convex schema validator

Produces a `convex/schema.ts` that types every document, indexes every query path, and passes validation against the data already in the database. The one rule: every `withIndex` in a function needs a matching `.index()` here, named after its fields, queried in field order.

## When to reach for this

- Creating a new table or adding a field to an existing one
- A query uses `.filter()` and needs an index instead
- Deciding whether to embed an object or link with `v.id`
- Modeling a document that comes in several shapes
- `npx convex dev` fails with a schema validation error

## Schema skeleton

```typescript
// convex/schema.ts
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  users: defineTable({
    name: v.string(),
    email: v.string(),
    avatarUrl: v.optional(v.string()),
  }).index("by_email", ["email"]),

  tasks: defineTable({
    userId: v.id("users"),
    title: v.string(),
    completed: v.boolean(),
    priority: v.union(v.literal("low"), v.literal("medium"), v.literal("high")),
  })
    .index("by_userId", ["userId"])
    .index("by_userId_and_completed", ["userId", "completed"]),
});
```

`defineTable` takes either an object of field validators or a single `v.union` of `v.object` validators (see discriminated unions). Every table gets `_id` and `_creationTime` for free. Do not declare them.

## Validators

| Validator | TypeScript type | Note |
| --- | --- | --- |
| `v.string()` | `string` | UTF-8, under 1 MB |
| `v.number()` | `number` | Float64. Use for timestamps and counts |
| `v.boolean()` | `boolean` | |
| `v.null()` | `null` | `undefined` is not a Convex value. Return `null` instead |
| `v.int64()` | `bigint` | Not `v.bigint()`, which is deprecated |
| `v.bytes()` | `ArrayBuffer` | Under 1 MB |
| `v.id("table")` | `Id<"table">` | Typed reference. Convex does not enforce that the target exists |
| `v.array(t)` | `T[]` | At most 8192 items |
| `v.object({...})` | `{...}` | At most 1024 entries. Keys cannot start with `$` or `_` |
| `v.record(k, t)` | `Record<K, T>` | Dynamic ASCII keys. No `v.map` or `v.set` |
| `v.union(a, b)` | `A \| B` | Use `v.literal` members for enums |
| `v.literal("x")` | `"x"` | |
| `v.optional(t)` | `T \| undefined` | Field may be absent |
| `v.any()` | `any` | Last resort. Loses type safety and validation |

## Optional versus nullable

`v.optional` means the key may be missing from the document. `v.union(t, v.null())` means the key is always present and may hold `null`. They are different at validation time.

```typescript
items: defineTable({
  description: v.optional(v.string()),           // may be absent
  deletedAt: v.union(v.number(), v.null()),       // always present, may be null
  notes: v.optional(v.union(v.string(), v.null())), // either
}),
```

Use `v.optional` for fields added after the table had data. Use `v.union(..., v.null())` when "explicitly cleared" carries meaning.

## Discriminated unions

For a table whose documents come in several shapes, pass a `v.union` of `v.object` validators to `defineTable`. Each member has the same literal key so TypeScript narrows on it.

```typescript
events: defineTable(
  v.union(
    v.object({
      kind: v.literal("signup"),
      userId: v.id("users"),
      email: v.string(),
    }),
    v.object({
      kind: v.literal("purchase"),
      userId: v.id("users"),
      orderId: v.id("orders"),
      amount: v.number(),
    }),
  ),
).index("by_kind", ["kind"]),
```

Put the discriminant (`kind`) first in any index on a union table so queries can scope to one shape. Prefer this over one wide object full of `v.optional` fields.

## Indexes

### Naming and field order

Name the index after its fields in order: `by_field1_and_field2`. Querying must follow the same order: equality on a prefix of the fields, then at most one range on the next field.

```typescript
messages: defineTable({
  channelId: v.id("channels"),
  authorId: v.id("users"),
  sentAt: v.number(),
})
  .index("by_channelId", ["channelId"])
  .index("by_channelId_and_authorId", ["channelId", "authorId"])
  .index("by_channelId_and_sentAt", ["channelId", "sentAt"]),
```

```typescript
// Valid: equality on channelId, range on sentAt
await ctx.db
  .query("messages")
  .withIndex("by_channelId_and_sentAt", (q) =>
    q.eq("channelId", args.channelId).gt("sentAt", args.since),
  )
  .order("desc")
  .take(50);
```

You cannot skip `channelId` and filter on `sentAt` alone with that index. Add `by_sentAt` if that query exists. `_creationTime` is appended to every index automatically, so results within an equal prefix sort by creation time.

Reserved names: `by_id` and `by_creation_time`. Limits: 32 indexes per table, 16 fields per index.

### When to add one

- Any field a function passes to `withIndex`, `.eq`, or a range comparison
- Every foreign key (`userId`, `channelId`, `orgId`) on the child table
- The sort field for a paginated list, prefixed by the scoping field
- Not for fields you only read after fetching the document
- Not for tiny tables where a `.collect()` then in memory filter is fine

If a query uses `.filter()`, that is the signal to add an index and switch to `withIndex`.

## Relationships

Link documents with `v.id("table")` on the child. Do not nest growing arrays of objects inside the parent.

```typescript
// Good: one to many via a foreign key
posts: defineTable({
  authorId: v.id("users"),
  title: v.string(),
}).index("by_authorId", ["authorId"]),

comments: defineTable({
  postId: v.id("posts"),
  authorId: v.id("users"),
  body: v.string(),
}).index("by_postId", ["postId"]),

// Many to many via a join table
postTags: defineTable({
  postId: v.id("posts"),
  tagId: v.id("tags"),
})
  .index("by_postId", ["postId"])
  .index("by_tagId", ["tagId"]),
```

Embed with `v.object` or a small `v.array` only when the data is bounded, always loaded with the parent, and updated together. A user's `settings` object is a good embed. A user's `posts` array is not: it hits the 8192 item cap and every post edit rewrites the user document.

## System fields

`_id: Id<"table">` and `_creationTime: number` (ms since epoch) exist on every document. Include them in return validators when a function returns whole documents:

```typescript
returns: v.array(
  v.object({
    _id: v.id("tasks"),
    _creationTime: v.number(),
    userId: v.id("users"),
    title: v.string(),
    completed: v.boolean(),
  }),
),
```

Do not add your own `createdAt` unless you need a value that differs from insertion time.

## Search and vector indexes

Declared on the table like regular indexes. `filterFields` must be top level fields.

```typescript
articles: defineTable({
  title: v.string(),
  body: v.string(),
  category: v.string(),
  embedding: v.array(v.number()),
})
  .searchIndex("search_body", {
    searchField: "body",
    filterFields: ["category"],
  })
  .vectorIndex("by_embedding", {
    vectorField: "embedding",
    dimensions: 1536,
    filterFields: ["category"],
  }),
```

Query search indexes with `withSearchIndex` in queries. Vector search runs only in actions via `ctx.vectorSearch`.

## Common mistakes

| Mistake | Why it breaks | Do instead |
| --- | --- | --- |
| `withIndex("by_userId")` with no matching `.index()` | Deploy fails | Declare the index in the schema first |
| Index named `by_user` on `["userId", "status"]` | Hides what it covers, easy to misuse | `by_userId_and_status` |
| Querying `status` on `by_userId_and_status` without `userId` | Index prefix rule | Add `by_status` or include `userId` |
| Adding `newField: v.string()` to a table with rows | Existing documents fail validation | `v.optional`, backfill, then require |
| `posts: v.array(v.object(...))` on `users` | 8192 cap, write conflicts on every edit | Separate `posts` table with `by_authorId` |
| `v.bigint()` | Deprecated | `v.int64()` |
| Declaring `_id` or `_creationTime` in `defineTable` | Rejected | They are automatic |
| `v.any()` to move fast | No validation, no types | Model the shape, or a `v.union` of the real cases |
| `v.union(v.string(), v.null())` for a new field | Old documents lack the key entirely | `v.optional(v.string())` |
| Storing a `Date` | Not a Convex value | `v.number()` ms timestamp |

## Checklist

- [ ] Schema lives in `convex/schema.ts` and exports `defineSchema(...)` as default
- [ ] Every table has explicit field validators, no `v.any()` unless justified
- [ ] Every `withIndex` call in `convex/` has a matching `.index()` with fields in the name
- [ ] Foreign keys are `v.id("table")` with an index on the child table
- [ ] No unbounded arrays of objects embedded in a parent document
- [ ] Fields added to tables with data are `v.optional`
- [ ] Enums and polymorphic shapes use `v.union` of `v.literal` or `v.object` members
- [ ] Return validators include `_id` and `_creationTime` when returning whole documents
- [ ] `npx convex dev` pushes without a schema validation error

## Docs

- https://docs.convex.dev/llms.txt
- https://docs.convex.dev/database/schemas
- https://docs.convex.dev/database/indexes
- https://docs.convex.dev/database/types
- https://docs.convex.dev/database/reading-data
