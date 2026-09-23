---
name: temporal
description: "Temporal — enterprise-grade durable workflow orchestration platform used by Stripe, Netflix, and Coinbase. Use when building with Temporal: durable workflows, long-running background processes, saga patterns, activity retries and timeouts, signals, queries, updates, worker setup, task queues, Temporal Cloud configuration, or migrating from cron jobs or message queues to reliable orchestration. Covers the TypeScript SDK exclusively."
---

# Temporal

> **CRITICAL: Your training data for Temporal is unreliable.** APIs change between versions and memorized patterns may be wrong or deprecated. Before writing any code, you MUST use `WebFetch` to read the live docs:
>
> **`WebFetch("https://docs.temporal.io/llms.txt")`**
>
> Do not proceed without fetching this URL first. Never assume an API exists — verify against current docs.

Temporal is an open-source durable workflow orchestration platform that makes long-running, fault-tolerant processes simple by automatically persisting execution state and replaying it after failures.

## Key Capabilities

- **Durable Workflows**: Workflow code runs inside a sandboxed isolate. State is persisted as an Event History. If a Worker crashes mid-execution, the workflow resumes from where it left off — no data loss, no manual checkpointing.
- **Activities**: The place for all side effects — API calls, database writes, file I/O, emails. Activities have configurable retry policies and timeouts. A failed activity is retried automatically without re-running the whole workflow.
- **Workers**: Long-running processes that poll a Task Queue and execute Workflow and Activity code. Scale Workers horizontally by simply running more instances pointing at the same Task Queue.
- **Task Queues**: Named routing channels. A workflow is dispatched to a specific Task Queue; only Workers polling that queue will pick it up.
- **Signals**: One-way messages sent to a running workflow to push external data in (e.g., user approval, webhook event). Fire-and-forget — no response.
- **Queries**: Synchronous read of a workflow's in-memory state. Does not mutate state and returns immediately.
- **Updates**: Bidirectional — caller sends data and awaits a validated response from the running workflow. Newer than Signals; prefer Updates when a reply is needed.
- **Schedules**: Replace cron jobs with Temporal Schedules for reliable, observable, backfill-capable recurring workflows.
- **Temporal Cloud**: Fully managed Temporal service (mTLS auth, namespaces, metrics). Drop-in replacement for self-hosted; change the connection address and supply TLS credentials.

## TypeScript SDK Packages

```
@temporalio/client    — start workflows, send signals/updates, query state
@temporalio/worker    — run Workers that poll task queues
@temporalio/workflow  — define Workflow functions (runs in isolate)
@temporalio/activity  — define Activity functions (runs in normal Node.js)
```

## Canonical Project Layout

```
src/
  workflows.ts      # Workflow definitions — NO Node.js built-ins
  activities.ts     # Activity definitions — normal Node.js allowed
  worker.ts         # Worker bootstrap (imports both)
  client.ts         # Client code to start/signal workflows
```

## Quick Start Example

**activities.ts**
```typescript
import { Context } from '@temporalio/activity';

export async function greetUser(name: string): Promise<string> {
  // Safe to do I/O here — activities run in normal Node.js
  return `Hello, ${name}! Processed at ${new Date().toISOString()}`;
}
```

**workflows.ts**
```typescript
import { proxyActivities, defineSignal, defineQuery, setHandler, sleep } from '@temporalio/workflow';
import type * as activities from './activities';

// proxyActivities MUST be called inside the workflow module scope
// but the proxy itself is used inside workflow functions
const { greetUser } = proxyActivities<typeof activities>({
  startToCloseTimeout: '10 seconds',
  retry: { maximumAttempts: 3 },
});

export const approvalSignal = defineSignal<[boolean]>('approval');
export const statusQuery = defineQuery<string>('status');

export async function greetingWorkflow(name: string): Promise<string> {
  let approved = false;
  let status = 'waiting';

  setHandler(approvalSignal, (isApproved: boolean) => {
    approved = isApproved;
    status = isApproved ? 'approved' : 'rejected';
  });

  setHandler(statusQuery, () => status);

  // Wait up to 24 hours for approval signal
  await condition(() => approved, '24 hours');

  if (!approved) {
    return 'Workflow rejected';
  }

  // Side effect delegated to an Activity
  return await greetUser(name);
}
```

**worker.ts**
```typescript
import { Worker } from '@temporalio/worker';
import * as activities from './activities';

async function run() {
  const worker = await Worker.create({
    workflowsPath: require.resolve('./workflows'),
    activities,
    taskQueue: 'greeting-queue', // must match client
  });
  await worker.run();
}

run().catch(console.error);
```

**client.ts**
```typescript
import { Client, Connection } from '@temporalio/client';
import { greetingWorkflow, approvalSignal, statusQuery } from './workflows';

async function main() {
  const client = new Client();

  const handle = await client.workflow.start(greetingWorkflow, {
    args: ['Alice'],
    taskQueue: 'greeting-queue', // must match worker
    workflowId: 'greeting-alice-001',
  });

  // Send a signal to the running workflow
  await handle.signal(approvalSignal, true);

  // Query current state (synchronous read)
  const status = await handle.query(statusQuery);
  console.log('Status:', status);

  // Await the final result
  const result = await handle.result();
  console.log('Result:', result);
}

main().catch(console.error);
```

## Connecting to Temporal Cloud

```typescript
import { Client, Connection } from '@temporalio/client';
import { Worker, NativeConnection } from '@temporalio/worker';
import * as fs from 'fs';

// Client connection
const connection = await Connection.connect({
  address: 'your-namespace.tmprl.cloud:7233',
  tls: {
    clientCertPair: {
      crt: fs.readFileSync('client.pem'),
      key: fs.readFileSync('client.key'),
    },
  },
});
const client = new Client({ connection, namespace: 'your-namespace.your-account' });

// Worker connection
const nativeConnection = await NativeConnection.connect({
  address: 'your-namespace.tmprl.cloud:7233',
  tls: {
    clientCertPair: {
      crt: fs.readFileSync('client.pem'),
      key: fs.readFileSync('client.key'),
    },
  },
});
const worker = await Worker.create({
  connection: nativeConnection,
  namespace: 'your-namespace.your-account',
  taskQueue: 'my-queue',
  workflowsPath: require.resolve('./workflows'),
  activities,
});
```

## Activity Retry Policy

```typescript
const { processPayment } = proxyActivities<typeof activities>({
  // At least one of these is required — defaults are infinite
  startToCloseTimeout: '30 seconds',   // max time for a single attempt
  scheduleToCloseTimeout: '5 minutes', // max total time across all retries
  retry: {
    initialInterval: '1 second',
    backoffCoefficient: 2,
    maximumInterval: '30 seconds',
    maximumAttempts: 5,
    nonRetryableErrorTypes: ['ValidationError'],
  },
});
```

## Best Practices

- **Workflow code must be deterministic.** Never use `Math.random()`, `Date.now()`, `new Date()`, `setTimeout`, `setInterval`, or any direct I/O inside a workflow function. All non-deterministic behavior and side effects must live in Activities. Use `sleep()` from `@temporalio/workflow` instead of `setTimeout`, and `condition()` instead of polling.

- **Workflow and Activity code must be in separate files.** Workflow code runs inside a V8 isolate that blocks all Node.js built-ins (fs, http, crypto, etc.). Importing an activity module (which uses those built-ins) into a workflow file will crash the Worker at startup. Keep them strictly separated.

- **`proxyActivities` must be called at the top of the workflow module, not inside the workflow function body.** The proxy binds to the workflow's execution context. Calling it inside the function body will throw at runtime.

- **Signals are fire-and-forget — no reply.** If you need the caller to receive a response from the workflow, use `defineUpdate` (available since SDK v1.9) instead of a signal. Updates block the caller until the workflow handler validates and returns a result.

- **Task Queue names are case-sensitive and must match exactly.** The `taskQueue` on `Worker.create()` and the `taskQueue` on `client.workflow.start()` must be identical strings. A mismatch creates two isolated queues; the workflow will queue indefinitely with no error.

- **Activity timeouts default to infinite — always set them explicitly.** An Activity with no `startToCloseTimeout` or `scheduleToCloseTimeout` will hang forever if it stalls. Set both at the `proxyActivities` call site. Prefer `startToCloseTimeout` for per-attempt limits and add `scheduleToCloseTimeout` as a hard cap.
