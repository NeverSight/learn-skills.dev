---
name: convex-functions
description: Writes Convex queries, mutations, actions, and internal functions in the object form with args and returns validators, correct ctx usage, runtime boundaries, and error handling. Use when adding or changing anything in convex/*.ts that exports a function, or when deciding between query, mutation, and action.
---

# Convex functions

Every exported function in `convex/` uses the object form with `args` and `returns` validators. Pick the type by what the handler touches: queries read, mutations write, actions call out.

## Pick the function type

| Type | Database | External calls | Callable by | Use for |
| --- | --- | --- | --- | --- |
| `query` | Read | No | Clients, other functions | Reads. Cached and reactive. |
| `mutation` | Read and write | No | Clients, other functions | Writes. One transaction. |
| `action` | Only via `runQuery` and `runMutation` | Yes | Clients, scheduler, other actions | `fetch`, third party SDKs, Node APIs |
| `internalQuery`, `internalMutation`, `internalAction` | Same as the public form | Same | Only other Convex functions | Scheduled work, crons, privileged writes |
| `httpAction` | Only via `runQuery` and `runMutation` | Yes | HTTP requests in `convex/http.ts` | Webhooks, REST endpoints |

Default to query or mutation. Reach for an action only when the handler must talk to something outside Convex.

## The object form

Declare `args` and `returns` on every function. A function that returns nothing declares `returns: v.null()` and returns `null`. Hoist a shared document validator when several functions return the same shape.

```typescript
// convex/tasks.ts
import { query, mutation } from "./_generated/server";
import { v } from "convex/values";

const taskValidator = v.object({
  _id: v.id("tasks"),
  _creationTime: v.number(),
  userId: v.id("users"),
  title: v.string(),
  completed: v.boolean(),
});

export const get = query({
  args: { taskId: v.id("tasks") },
  returns: v.union(taskValidator, v.null()),
  handler: async (ctx, args) => {
    return await ctx.db.get(args.taskId);
  },
});

export const remove = mutation({
  args: { taskId: v.id("tasks") },
  returns: v.null(),
  handler: async (ctx, args) => {
    await ctx.db.delete(args.taskId);
    return null;
  },
});
```

## Reading data

Use `ctx.db.get(id)` for one document by id. For everything else use `withIndex` against an index defined in `convex/schema.ts`. Never call `.filter()` on a table query; it scans the whole table.

```typescript
export const listByUser = query({
  args: { userId: v.id("users") },
  returns: v.array(taskValidator),
  handler: async (ctx, args) => {
    return await ctx.db
      .query("tasks")
      .withIndex("by_user", (q) => q.eq("userId", args.userId))
      .order("desc")
      .take(50);
  },
});
```

Pick the terminal method by how many documents you expect:

| Method | Returns | Use when |
| --- | --- | --- |
| `.unique()` | One doc or null, throws on more than one | The index guarantees at most one match |
| `.first()` | First doc or null | You want the newest or oldest match |
| `.take(n)` | Up to n docs | A bounded list such as a recent feed |
| `.collect()` | Every match | The result set is small and stays small |
| `.paginate(opts)` | A page plus cursor | The table is unbounded |

Paginated queries take `paginationOpts: paginationOptsValidator` (from `convex/server`) as an argument.

## Writing data

| Method | What it does |
| --- | --- |
| `ctx.db.insert("tasks", doc)` | Inserts and returns the new id |
| `ctx.db.patch(id, fields)` | Shallow merges fields. Throws if the doc is missing |
| `ctx.db.replace(id, doc)` | Replaces the whole doc. Throws if missing |
| `ctx.db.delete(id)` | Deletes the doc |

Patch directly when you do not need the old value. Reading first widens the window for write conflicts. Make mutations safe to retry.

```typescript
export const rename = mutation({
  args: { taskId: v.id("tasks"), title: v.string() },
  returns: v.null(),
  handler: async (ctx, args) => {
    await ctx.db.patch(args.taskId, { title: args.title });
    return null;
  },
});
```

## Internal functions and references

`query`, `mutation`, and `action` are public. Anyone with the deployment URL can call them. Use `internalQuery`, `internalMutation`, and `internalAction` for code that should only run from other Convex code: scheduled jobs, crons, webhook handlers, privileged writes.

Reference functions through the generated objects in `./_generated/api`:

- `api.tasks.get` points at a public function in `convex/tasks.ts`
- `internal.tasks.markPaid` points at an internal function in the same file
- Folders map to paths: `convex/billing/invoices.ts` gives `api.billing.invoices.list`

Always schedule `internal.*`. Scheduled functions and crons run without a client, so a public reference there skips the auth checks a client call would hit.

```typescript
// convex/messages.ts
import { mutation, internalMutation } from "./_generated/server";
import { internal } from "./_generated/api";
import { v } from "convex/values";

export const send = mutation({
  args: { channelId: v.id("channels"), content: v.string() },
  returns: v.id("messages"),
  handler: async (ctx, args) => {
    const messageId = await ctx.db.insert("messages", args);
    await ctx.scheduler.runAfter(0, internal.messages.notifySubscribers, {
      channelId: args.channelId,
      messageId,
    });
    return messageId;
  },
});

export const notifySubscribers = internalMutation({
  args: { channelId: v.id("channels"), messageId: v.id("messages") },
  returns: v.null(),
  handler: async (ctx, args) => {
    const subs = await ctx.db
      .query("subscriptions")
      .withIndex("by_channel", (q) => q.eq("channelId", args.channelId))
      .collect();
    await Promise.all(
      subs.map((sub) =>
        ctx.db.insert("notifications", {
          userId: sub.userId,
          messageId: args.messageId,
          read: false,
        }),
      ),
    );
    return null;
  },
});
```

## Actions and runtime boundaries

Actions have no `ctx.db`. They read through `ctx.runQuery` and write through `ctx.runMutation`. Each call is its own transaction, so keep the count low and do related reads and writes inside one mutation.

`fetch` works in the default runtime. Add `"use node";` as the first line of a file only when an action needs Node built ins or a Node only SDK. A `"use node"` file can export actions only; queries and mutations go in a separate file.

```typescript
// convex/orders.ts (default runtime)
import { action } from "./_generated/server";
import { internal } from "./_generated/api";
import { v, ConvexError } from "convex/values";
import { Doc } from "./_generated/dataModel";

export const charge = action({
  args: { orderId: v.id("orders") },
  returns: v.null(),
  handler: async (ctx, args) => {
    // Same file call: annotate the result so TypeScript does not hit a circular type
    const order: Doc<"orders"> | null = await ctx.runQuery(
      internal.orders.getForCharge,
      { orderId: args.orderId },
    );
    if (!order) {
      throw new ConvexError("Order not found");
    }
    const res = await fetch("https://api.payments.example/charge", {
      method: "POST",
      body: JSON.stringify({ amount: order.total }),
    });
    await ctx.runMutation(internal.orders.setStatus, {
      orderId: args.orderId,
      status: res.ok ? "paid" : "failed",
    });
    return null;
  },
});
```

`Doc` and `Id` come from `./_generated/dataModel`. The annotation is only needed when the called function lives in the same file.

## Errors

Throw `ConvexError` from `convex/values` for anything a client should read. Its `data` reaches the client; a plain `Error` message is redacted in production. Return `null` for expected absences such as a lookup that finds nothing. Throw for real failures: not authenticated, not authorized, invalid input.

```typescript
import { ConvexError } from "convex/values";

throw new ConvexError({ code: "NOT_FOUND", message: "Task not found" });
```

## Thin wrappers

Keep handlers short. Put auth lookups, validation, and business logic in plain async functions that take `ctx` first, then call them from the wrapper. Plain helpers are testable and shared between queries and mutations without a `ctx.runQuery` hop.

```typescript
import { QueryCtx, MutationCtx } from "./_generated/server";
import { ConvexError } from "convex/values";

export async function getCurrentUser(ctx: QueryCtx | MutationCtx) {
  const identity = await ctx.auth.getUserIdentity();
  if (!identity) {
    throw new ConvexError("Not authenticated");
  }
  const user = await ctx.db
    .query("users")
    .withIndex("by_token", (q) =>
      q.eq("tokenIdentifier", identity.tokenIdentifier),
    )
    .unique();
  if (!user) {
    throw new ConvexError("User not found");
  }
  return user;
}
```

From a query or mutation, call the helper directly. `ctx.runQuery` and `ctx.runMutation` are for actions and component boundaries.

## Common mistakes

| Mistake | Why it breaks | Do instead |
| --- | --- | --- |
| No `returns` validator | Return shape drifts and client types lie | Declare `returns`, use `v.null()` for nothing |
| `.filter()` on a table query | Full table scan | Add an index, use `withIndex` |
| `ctx.db` inside an action | Actions have no database handle | `ctx.runQuery` and `ctx.runMutation` |
| `fetch` inside a query or mutation | Transactions must be deterministic | Move it to an action |
| Scheduling `api.*` | Runs public code without a client, skips auth | Schedule `internal.*` |
| `"use node"` in a file with queries | Bundler rejects the file | Split actions into their own file |
| `Date.now()` in a query | Breaks caching and reactivity | Pass time as an arg or store a status field |
| Many `runQuery` calls from one action | Each is a separate transaction, races appear | One mutation that does the related work |
| Plain `Error` for user messages | Message is hidden in production | `ConvexError` |
| Missing `await` on `ctx.db` or scheduler | Write may not commit | Await every `ctx` call |

## Checklist

- [ ] Object form with `args` and `returns` on every exported function
- [ ] `returns: v.null()` and `return null` when there is nothing to return
- [ ] Reads use `ctx.db.get(id)` or `withIndex`, never `.filter()`
- [ ] Unbounded tables use `.paginate()` or `.take(n)`, not `.collect()`
- [ ] Mutations patch directly and are safe to retry
- [ ] Scheduled and cron targets are `internal.*`
- [ ] Actions never touch `ctx.db`
- [ ] `"use node"` only in files that export actions and need Node
- [ ] Same file `runQuery` and `runMutation` results have a type annotation
- [ ] Client visible errors are `ConvexError`
- [ ] Every `ctx.*` promise is awaited

## Docs

- https://docs.convex.dev/llms.txt
- https://docs.convex.dev/functions
- https://docs.convex.dev/functions/validation
- https://docs.convex.dev/functions/actions
- https://docs.convex.dev/functions/error-handling
