---
name: sync-scheduler
description: "Use this skill when implementing distributed cron scheduling with @valentinkolb/sync scheduler: registering idempotent schedules across pods, leader-fenced dispatch via job.submit, misfire policy (skip/catch_up_one/catch_up_all), triggerNow for manual dispatch, unregister, metrics/health, and multi-pod leader election. Depends on sync-job for execution and sync-mutex for leader lock."
---

# Sync Scheduler

Distributed cron with durable dispatch. Leader election across pods via mutex. Dispatch goes through the `job` system for at-least-once execution.

**Dependencies**: requires `sync-job` handles for execution. Uses `sync-mutex` internally for leader election. Read those skills for deeper semantics if needed.

## Setup Pattern

```ts
// 1. Define jobs first
const cleanupJob = job({ id: "cleanup", schema, process: handler });

// 2. Create scheduler
const sched = scheduler({ id: "platform", onMetric: console.log });

// 3. Start on every pod
sched.start();

// 4. Register schedules (idempotent — safe to call on every startup)
await sched.register({
  id: "cleanup-hourly", cron: "0 * * * *", tz: "Europe/Berlin",
  job: cleanupJob, input: { scope: "temp" }, misfire: "skip",
});

// 5. Graceful shutdown
await sched.stop();
```

## Misfire Policies

- `skip` (default): ignore missed slots, jump to next future cron time.
- `catch_up_one`: submit one overdue slot, then jump to next.
- `catch_up_all`: submit all overdue slots up to `maxCatchUpRuns` (default 100).

## Gotchas

- `register()` is idempotent by schedule `id`. If cron/tz change, `nextRunAt` is recalculated; otherwise preserved.
- `triggerNow({ id })` submits immediately through `job.submit()`. It reuses stored schedule input — use `job.submit()` directly for custom per-run input.
- `triggerNow()` does NOT require `start()` and does NOT alter cron dispatch state.
- `key` in `triggerNow()` is recommended for retry-safe manual triggers.
- `strictHandlers: true` (default): dispatch fails if no job handler is registered. Set to `false` to skip silently.
- Leader lease is 5s by default. Any pod can become leader. Epoch-based CAS prevents stale leaders from dispatching.
- Dispatch uses deterministic submit keys `${scheduleId}:${slotTs}` — the job system deduplicates naturally.
- After `maxConsecutiveDispatchFailures` (default 5), the schedule slot is advanced and failure is logged to DLQ.
- `onMetric` callback is best-effort — errors in the callback are swallowed.

## API Reference

Read full API/types/config/defaults in [references/api.md](references/api.md).
