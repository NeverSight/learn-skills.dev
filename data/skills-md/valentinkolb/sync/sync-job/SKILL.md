---
name: sync-job
description: "Use this skill when implementing durable background jobs with @valentinkolb/sync job: defining typed process handlers with ctx.step/ctx.heartbeat/ctx.signal, submit/join/cancel flows, idempotent submission via key, retries with exponential backoff, lease timeouts, and per-job event streams for audit. Also use when choosing between job (durable execution with state) vs queue (simple work distribution)."
---

# Sync Job

Durable async execution: submit, process (with retries), join for result, cancel cooperatively. Built on top of `queue` and `topic` internally.

## Decision Guide: job vs queue

- **job**: full lifecycle (submitted → running → completed/failed/cancelled). Has state, retries, backoff, `join()`, `cancel()`, event audit stream. Best for background tasks where you need to track outcome.
- **queue**: raw work distribution with ack/nack. No state machine, no join. Best for fire-and-forget pipelines. See `sync-queue` skill.

## Handler Pattern

```ts
process: async ({ ctx, input }) => {
  // 1. Check cancellation
  if (ctx.signal.aborted) return;

  // 2. Use step() for resumable sub-tasks
  await ctx.step({ id: "fetch", run: () => fetchData(input) });

  // 3. Heartbeat for long work (extends queue lease)
  await ctx.heartbeat();

  // 4. Return result (stored in terminal state)
  return { success: true };
}
```

## Gotchas

- `submit()` auto-starts the worker loop on the calling process. No separate `start()` needed.
- `key` on submit is the idempotency key. Same key returns same job ID. Use for retry-safe submissions.
- `maxAttempts` default is `1` (no retry). Set explicitly for retryable jobs.
- `join()` with no `timeoutMs` still returns eventually — as `{ status: "timed_out", error.code: "JOIN_TIMEOUT" }`.
- `cancel()` is cooperative: it sets state to `cancelled` only if non-terminal. The handler must check `ctx.signal.aborted`.
- `ctx.heartbeat()` extends the underlying queue lease. Call it in long-running handlers to prevent lease expiry and re-delivery.
- State is retained for 7 days (`DEFAULT_STATE_RETENTION_MS`). After that, `join()` cannot find the result.
- Worker receive loop auto-retries transient transport errors — survives brief Redis outages.

## API Reference

Read full API/types/config/defaults in [references/api.md](references/api.md).
