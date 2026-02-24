---
name: bullmq
description: "BullMQ queue system reference for Redis-backed job queues, workers, flows, and schedulers. Use when: (1) creating queues and workers with BullMQ, (2) adding jobs (delayed, prioritized, repeatable, deduplicated), (3) setting up FlowProducer parent-child job hierarchies, (4) configuring retry strategies, rate limiting, or concurrency, (5) implementing job schedulers with cron/interval patterns, (6) preparing BullMQ for production (graceful shutdown, Redis config, monitoring), or (7) debugging stalled jobs or connection issues"
---

# BullMQ

Redis-backed queue system for Node.js. Four core classes: `Queue`, `Worker`, `QueueEvents`, `FlowProducer`.

## Table of Contents

- [Install](#install)
- [Quick Start](#quick-start)
- [Connections](#connections)
- [Queue](#queue)
- [Worker](#worker)
- [TypeScript Generics](#typescript-generics)
- [Events](#events)
- [Job Lifecycle States](#job-lifecycle-states)
- [Advanced Topics](#advanced-topics)

## Install

`yarn add bullmq` — requires Redis 5.0+ with `maxmemory-policy=noeviction`.

## Quick Start

```ts
import { Queue, Worker, QueueEvents } from "bullmq";

// --- Producer ---
const queue = new Queue("my-queue", {
  connection: { host: "localhost", port: 6379 },
});

await queue.add("job-name", { foo: "bar" });

// --- Consumer ---
const worker = new Worker(
  "my-queue",
  async (job) => {
    // process job
    await job.updateProgress(50);
    return { result: "done" };
  },
  { connection: { host: "localhost", port: 6379 } },
);

worker.on("completed", (job, returnvalue) => {
  console.log(`${job.id} completed with`, returnvalue);
});

worker.on("failed", (job, err) => {
  console.error(`${job.id} failed with`, err.message);
});

// IMPORTANT: always attach an error handler
worker.on("error", (err) => {
  console.error(err);
});

// --- Global event listener (all workers) ---
const queueEvents = new QueueEvents("my-queue", {
  connection: { host: "localhost", port: 6379 },
});

queueEvents.on("completed", ({ jobId, returnvalue }) => {
  console.log(`Job ${jobId} completed`);
});

queueEvents.on("failed", ({ jobId, failedReason }) => {
  console.error(`Job ${jobId} failed: ${failedReason}`);
});
```

## Connections

BullMQ uses ioredis internally. Pass `connection` options or an existing ioredis instance.

```ts
import { Queue, Worker } from "bullmq";
import { Redis } from "ioredis";

// Option 1: connection config (new connection per instance)
const queue = new Queue("q", {
  connection: { host: "redis.example.com", port: 6379 },
});

// Option 2: reuse ioredis instance (Queue and multiple Queues can share)
const connection = new Redis();
const q1 = new Queue("q1", { connection });
const q2 = new Queue("q2", { connection });

// Option 3: reuse for Workers (BullMQ internally duplicates for blocking)
const workerConn = new Redis({ maxRetriesPerRequest: null });
const w1 = new Worker("q1", async (job) => {}, { connection: workerConn });
```

**Critical rules:**

- Workers REQUIRE `maxRetriesPerRequest: null` on the ioredis instance. BullMQ enforces this and will warn/throw if not set.
- Do NOT use ioredis `keyPrefix` option — use BullMQ's `prefix` option instead.
- `QueueEvents` cannot share connections (uses blocking Redis commands).
- Redis MUST have `maxmemory-policy=noeviction`.

## Queue

```ts
const queue = new Queue("paint", { connection });

// Add a job
await queue.add("job-name", { color: "red" });

// Add with options
await queue.add(
  "job-name",
  { color: "blue" },
  {
    delay: 5000, // wait 5s before processing
    priority: 1, // lower = higher priority (0 is highest, max 2^21)
    attempts: 3, // retry up to 3 times
    backoff: { type: "exponential", delay: 1000 },
    removeOnComplete: true, // or { count: 100 } to keep last 100
    removeOnFail: 1000, // keep last 1000 failed jobs
  },
);

// Add bulk
await queue.addBulk([
  { name: "job1", data: { x: 1 } },
  { name: "job2", data: { x: 2 }, opts: { priority: 1 } },
]);

// Queue operations
await queue.pause();
await queue.resume();
await queue.obliterate({ force: true }); // remove all data
await queue.close();
```

## Worker

```ts
const worker = new Worker<MyData, MyReturn>(
  "paint",
  async (job) => {
    await job.updateProgress(42);
    return { cost: 100 };
  },
  {
    connection,
    concurrency: 5, // process 5 jobs concurrently
    autorun: false, // don't start immediately
  },
);

worker.run(); // start when ready

// Update concurrency at runtime
worker.concurrency = 10;
```

**Processor receives 3 args:** `(job, token?, signal?)` — signal is an `AbortSignal` for cancellation support.

## TypeScript Generics

```ts
interface JobData {
  color: string;
}
interface JobReturn {
  cost: number;
}

const queue = new Queue<JobData, JobReturn>("paint");
const worker = new Worker<JobData, JobReturn>("paint", async (job) => {
  // job.data is typed as JobData
  return { cost: 100 }; // must match JobReturn
});
```

## Events

**Worker events** (local to that worker instance):

| Event       | Callback signature                   |
| ----------- | ------------------------------------ |
| `completed` | `(job, returnvalue)`                 |
| `failed`    | `(job \| undefined, error, prev)`    |
| `progress`  | `(job, progress: number \| object)`  |
| `drained`   | `()` — queue is empty                |
| `error`     | `(error)` — MUST attach this handler |

**QueueEvents** (global, all workers, uses Redis Streams):

| Event          | Callback signature                                |
| -------------- | ------------------------------------------------- |
| `completed`    | `({ jobId, returnvalue })`                        |
| `failed`       | `({ jobId, failedReason })`                       |
| `progress`     | `({ jobId, data })`                               |
| `waiting`      | `({ jobId })`                                     |
| `active`       | `({ jobId, prev })`                               |
| `delayed`      | `({ jobId, delay })`                              |
| `deduplicated` | `({ jobId, deduplicationId, deduplicatedJobId })` |

Event stream is auto-trimmed (~10,000 events). Configure via `streams.events.maxLen`.

## Job Lifecycle States

```
add() → wait / prioritized / delayed
         ↓
       active → completed
         ↓
       failed → (retry) → wait/delayed
```

With FlowProducer: jobs can also be in `waiting-children` state until all children complete.

## Advanced Topics

- **Job types and options** (delayed, prioritized, deduplication, repeatable): See [references/job-types-and-options.md](references/job-types-and-options.md)
- **Flows and schedulers** (FlowProducer, parent-child, job schedulers, cron): See [references/flows-and-schedulers.md](references/flows-and-schedulers.md)
- **Patterns** (step jobs, idempotent, throttle, manual rate-limit): See [references/patterns.md](references/patterns.md)
- **Production** (shutdown, Redis config, retries, backoff, monitoring): See [references/production.md](references/production.md)
