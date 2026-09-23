---
name: trigger-dev
description: "Trigger.dev — open-source background jobs platform for TypeScript with durable execution, retries, scheduling, and real-time monitoring. Use when building with Trigger.dev or asking about its task definitions, schedules, delays, batching, concurrency, or deployment. Fetch live documentation for up-to-date details."
---

# Trigger.dev

> **CRITICAL: Your training data for Trigger.dev is unreliable.** APIs change between versions and memorized patterns may be wrong or deprecated. Before writing any code, you MUST use `WebFetch` to read the live docs:
>
> **`WebFetch("https://trigger.dev/llms.txt")`**
>
> For complex scenarios (advanced concurrency, lifecycle hooks, build extensions), fetch the full docs instead:
> **`WebFetch("https://trigger.dev/docs/llms-full.txt")`**
>
> Do not proceed without fetching first. Never assume an API exists — verify against current docs.

Trigger.dev is an open-source background jobs platform for TypeScript with durable execution, built-in retries, scheduling, and real-time monitoring.

## Key Capabilities

- **Durable waits**: `wait.for({ seconds: 30 })`, `wait.until({ date })`, and `wait.forToken()` suspend execution without consuming timeout — the run resumes after the wait, not a new invocation.
- **No default timeout**: Tasks have no built-in timeout. Set `maxDuration` per task or globally in config if a limit is needed.
- **Batch triggering**: `tasks.batchTrigger()` accepts up to 1,000 items in a single call.
- **Child tasks with results**: `childTask.triggerAndWait()` suspends the parent until the child completes and returns a typed Result object — check `.ok` before accessing `.output`, or call `.unwrap()`.
- **Lifecycle hooks**: `onStart`, `onSuccess`, `onFailure`, and `init` in config handle cross-cutting concerns without modifying task code.
- **Build extensions**: `@trigger.dev/build/extensions` provides first-party support for Prisma, FFmpeg, Playwright, and system packages — use instead of manual Docker layers.

## Best Practices

- Never wrap `triggerAndWait` or `batchTriggerAndWait` in `Promise.all` — this pattern is explicitly unsupported and will cause failures.
- Every task must be exported from its file. Non-exported tasks are silently ignored and will not run.
- Use `AbortTaskRunError` to fail a run without retrying (e.g., for validation failures). Throwing any other error triggers the retry policy.
- Each Trigger.dev environment (dev, staging, prod) has its own `TRIGGER_SECRET_KEY` — using the wrong key triggers runs in the wrong environment with no obvious error.
- `processKeepAlive` reduces cold starts but the process can be killed at any time; do not rely on in-memory state persisting between task runs.
