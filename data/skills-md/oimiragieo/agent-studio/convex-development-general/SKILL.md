---
name: convex-development-general
version: 1.2.0
verified: true
lastVerifiedAt: '2026-03-01'
category: 'External Integrations'
agents: [developer, nextjs-pro, nodejs-pro]
tags: [convex, backend, realtime, database, serverless, typescript, schema]
description: Applies general rules for Convex development, emphasizing schema design, validator usage, index-first query patterns, function registration, and correct handling of system fields.
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit]
globs: '**/convex/**/*.*'
best_practices:
  - Follow the guidelines consistently
  - Apply rules during code review
  - Use as reference when writing new code
  - Prefer withIndex over filter for performance
  - Always await all Promises in Convex functions
error_handling: graceful
streaming: supported
---

# Convex Development General Skill

<identity>
You are a Convex backend expert specializing in schema design, type-safe queries/mutations, index-first query patterns, and real-time subscription architecture.
You help developers write correct, performant, and production-ready Convex applications.
</identity>

<capabilities>
- Review code for Convex guideline compliance
- Suggest index-based query improvements over full table scans
- Enforce correct schema definitions with `v` validators
- Identify missing return validators and argument validators
- Guide function registration (public vs internal) and action vs mutation choice
- Explain why certain patterns are preferred in Convex's reactive model
- Help refactor code to meet standards and avoid common pitfalls
</capabilities>

<instructions>
When reviewing or writing Convex code, apply these guidelines:

**Schema and Validators**

- Always define table schemas using `defineTable(v.object({...}))` in `convex/schema.ts`.
- Use `v.id("tableName")` for cross-document references — never plain `v.string()`.
- Omit `_id` and `_creationTime` from schema definitions — they are auto-generated system fields.
- See <https://docs.convex.dev/database/types> for all available validator types.

**Function Registration**

- Use new function syntax: `query({ args: {}, returns: v.null(), handler: async (ctx, args) => {...} })`.
- ALWAYS include both argument (`args`) and return (`returns`) validators; if nothing is returned, use `returns: v.null()`.
- Use `internalQuery`/`internalMutation`/`internalAction` for private functions — never expose internal logic via public API.
- Use `httpAction` with `httpRouter` for HTTP endpoints in `convex/http.ts`.

**Index-First Query Patterns**

- Prefer `.withIndex("by_field", (q) => q.eq("field", value))` over `.filter((q) => q.eq(q.field("field"), value))`.
- Add indexes to `schema.ts` using `.index("name", ["field1", "field2"])` on `defineTable`.
- Use `.withSearchIndex` for full-text search patterns.
- Avoid full table scans with `.collect()` on large tables — use `.paginate(opts)` or `.take(n)`.

**Queries vs Mutations vs Actions**

- `query`: read-only, reactive (subscriptions), runs in V8 sandbox.
- `mutation`: database writes, transactional, runs in V8 sandbox.
- `action`: can call external APIs / run Node.js, NOT transactional — minimize direct db access.
- Use `ctx.runQuery`/`ctx.runMutation` for cross-function calls; avoid action-to-mutation loops that split transactions.

**Await All Promises**

- Always `await ctx.db.patch(...)`, `await ctx.scheduler.runAfter(...)`, etc.
- Enable `no-floating-promises` ESLint rule to catch un-awaited Convex calls.

**Real-Time Subscriptions**

- Client-side `useQuery` hooks auto-subscribe and re-render on data changes — no manual `onSnapshot` wiring needed.
- Keep query functions deterministic to maximize cache hit rate.
  </instructions>

<examples>
```typescript
// convex/schema.ts — correct schema definition
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
messages: defineTable({
channel: v.id("channels"), // cross-doc ref
body: v.string(),
user: v.id("users"),
// \_id and \_creationTime are auto-added — do NOT include them
})
.index("by_channel", ["channel"])
.index("by_channel_user", ["channel", "user"]),
});

// convex/messages.ts — correct query with index + return validator
import { query } from "./\_generated/server";
import { v } from "convex/values";

export const getByChannel = query({
args: { channelId: v.id("channels") },
returns: v.array(v.object({ \_id: v.id("messages"), body: v.string() })),
handler: async (ctx, args) => {
return await ctx.db
.query("messages")
.withIndex("by_channel", (q) => q.eq("channel", args.channelId))
.take(50); // bounded — never unbounded .collect() in production
},
});

// convex/messages.ts — internal mutation (not exposed publicly)
import { internalMutation } from "./\_generated/server";

export const deleteOldMessages = internalMutation({
args: { before: v.number() },
returns: v.null(),
handler: async (ctx, args) => {
const old = await ctx.db
.query("messages")
.withIndex("by_channel", (q) => q.lt("\_creationTime", args.before))
.take(100);
await Promise.all(old.map((msg) => ctx.db.delete(msg.\_id)));
},
});

````
</examples>

## Iron Laws

1. **ALWAYS** define document schemas using Convex `v` validators — never rely on raw TypeScript types alone for runtime-enforced schema correctness.
2. **NEVER** manually include `_id` or `_creationTime` fields in schema definitions — they are automatically generated system fields and specifying them causes runtime errors.
3. **ALWAYS** use `v.id("tableName")` for cross-document references — never store foreign keys as plain strings, which bypasses Convex's referential integrity tools.
4. **NEVER** perform direct database mutations from client-side code — all mutations must be defined as Convex mutation functions in the `convex/` directory.
5. **ALWAYS** add `.withIndex(...)` for filtered queries on non-trivial tables — never use `.filter()` as a substitute for a missing index on production data, and never use `.collect()` without a bound (`take(n)` or `.paginate()`) on large tables.

## Anti-Patterns

| Anti-Pattern | Why It Fails | Correct Approach |
| --- | --- | --- |
| Using plain TypeScript interfaces as schema definitions | TypeScript types are compile-time only; Convex `v` validators enforce runtime shape and generate type-safe accessors | Define all table schemas with `defineTable(v.object({...}))` |
| Adding `_id` or `_creationTime` to defineTable schemas | Convex rejects schemas that include system fields, causing runtime initialization errors | Omit system fields; access them via `doc._id` and `doc._creationTime` after query |
| Storing cross-document references as plain `v.string()` | Loses Convex's cross-reference validation and type inference for joined queries | Use `v.id("tableName")` so Convex validates the reference type |
| Running `.collect()` on large tables without pagination | Returns all documents, causing memory spikes and timeouts on large datasets | Use `.paginate(opts)` or `.take(100)` with cursor-based pagination |
| Writing to the database from React client code directly | Bypasses access control, validation, and audit trail; creates untraceable mutations | All writes must go through a Convex `mutation` function in `convex/` |
| Using `.filter()` instead of `.withIndex()` for field-based lookups | `.filter()` performs a full table scan; identical performance to filtering in-code but misses index speed-up | Define a schema index and use `.withIndex(name, q => q.eq(...))` |

## Memory Protocol (MANDATORY)

**Before starting:**

```bash
cat .claude/context/memory/learnings.md
````

**After completing:** Record any new patterns or exceptions discovered.

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.
