---
name: vercel-workflow
description: Build durable workflows with Vercel Workflow DevKit using "use workflow" and "use step" directives. Use for long-running tasks, background jobs, AI agents, webhooks, scheduled tasks, retries, and workflow orchestration. Supports Next.js, Vite, Astro, Express, Fastify, Hono, Nitro, Nuxt, SvelteKit.
---

# Vercel Workflow DevKit

Build durable, resumable workflows that survive restarts, deployments, and failures using TypeScript directives.

## Quick Start (Next.js)

```bash
npm i workflow
```

```typescript
// next.config.ts
import { withWorkflow } from "workflow/next";
export default withWorkflow({});
```

```typescript
// workflows/signup.ts
import { sleep, FatalError } from "workflow";

export async function signupWorkflow(email: string) {
  "use workflow";

  const user = await createUser(email);
  await sendWelcome(user.id, email);
  await sleep("3d");
  await sendFollowUp(user.id);
  return { success: true };
}

async function createUser(email: string) {
  "use step";
  return { id: crypto.randomUUID(), email };
}

async function sendWelcome(userId: string, email: string) {
  "use step";
  const res = await fetch("https://api.email.com/send", {
    method: "POST",
    body: JSON.stringify({ to: email, template: "welcome" })
  });
  if (!res.ok) throw new Error("Failed"); // Auto-retried
}

async function sendFollowUp(userId: string) {
  "use step";
  // FatalError = no retry
  if (!userId) throw new FatalError("Missing userId");
  // ... send email
}
```

```typescript
// app/api/signup/route.ts
import { start } from "workflow/api";
import { signupWorkflow } from "@/workflows/signup";

export async function POST(request: Request) {
  const { email } = await request.json();
  const run = await start(signupWorkflow, [email]);
  return Response.json({ runId: run.id });
}
```

## Core Concepts

### The Two Directives

| Directive | Purpose | Rules |
|-----------|---------|-------|
| `"use workflow"` | Orchestrates steps, sleeps, suspends | **Deterministic**: No side effects, no Node.js modules, no global fetch |
| `"use step"` | Contains business logic, I/O, side effects | **Runs on separate request**: Auto-retries on failure |

### Why These Restrictions?

Workflow DevKit uses **event sourcing** - state changes are stored as events and replayed to reconstruct state. Workflows must be deterministic so replays produce identical step sequences. Steps run on separate requests, so data passes by value (mutations don't affect workflow variables).

### Data Flow: Pass-by-Value

```typescript
// WRONG - mutations lost
async function workflow() {
  "use workflow";
  const user = { name: "Alice" };
  await updateUser(user);
  console.log(user.name); // Still "Alice"!
}

// CORRECT - return modified data
async function workflow() {
  "use workflow";
  let user = { name: "Alice" };
  user = await updateUser(user);
  console.log(user.name); // "Bob"
}

async function updateUser(user: User) {
  "use step";
  user.name = "Bob";
  return user; // Must return!
}
```

## API Quick Reference

### workflow package

```typescript
import {
  sleep,              // Suspend for duration/until date
  fetch,              // HTTP with auto-retry (use in workflows)
  FatalError,         // Non-retryable error
  RetryableError,     // Explicit retry with delay
  createHook,         // Receive external payloads
  createWebhook,      // Receive HTTP requests
  defineHook,         // Type-safe hooks with validation
  getWritable,        // Stream output
  getWorkflowMetadata,// { workflowRunId, workflowStartedAt, url }
  getStepMetadata     // { stepId } - use for idempotency keys
} from "workflow";
```

### workflow/api package

```typescript
import {
  start,          // Start workflow run
  getRun,         // Get run status
  resumeHook,     // Resume via hook token
  resumeWebhook,  // Resume via webhook token
  getHookByToken  // Get hook details
} from "workflow/api";
```

## Sleep & Scheduling

```typescript
await sleep("10s");   // seconds
await sleep("5m");    // minutes
await sleep("2h");    // hours
await sleep("1d");    // days
await sleep("2w");    // weeks
await sleep(5000);    // milliseconds
await sleep(new Date("2025-12-25")); // until date
```

## Error Handling

```typescript
import { FatalError, RetryableError } from "workflow";

async function processPayment(amount: number) {
  "use step";

  try {
    return await paymentAPI.charge(amount);
  } catch (error) {
    // Don't retry invalid requests
    if (error.code === "INVALID_CARD") {
      throw new FatalError("Invalid card");
    }
    // Explicit retry with delay
    if (error.code === "RATE_LIMITED") {
      throw new RetryableError("Rate limited", { retryAfter: "5m" });
    }
    // Other errors auto-retry with default backoff
    throw error;
  }
}
```

## Hooks (External Events)

```typescript
import { createHook, defineHook } from "workflow";
import { resumeHook } from "workflow/api";
import { z } from "zod";

// In workflow - create hook and wait
export async function approvalWorkflow(orderId: string) {
  "use workflow";

  const hook = createHook<{ approved: boolean; comment: string }>({
    token: `approval:${orderId}` // Custom token for deterministic recovery
  });

  await notifyReviewer(orderId, hook.token);
  const result = await hook; // Suspends until resumed

  if (result.approved) await processOrder(orderId);
}

// In API route - resume with payload
export async function POST(request: Request) {
  const { token, approved, comment } = await request.json();
  await resumeHook(token, { approved, comment });
  return Response.json({ success: true });
}

// Type-safe hooks with validation
const approvalHook = defineHook(z.object({
  approved: z.boolean(),
  comment: z.string().max(500)
}));

// Use: approvalHook.create(), approvalHook.resume(token, payload)
```

## Idempotency

Use `stepId` for idempotency keys - stable across retries, unique per step:

```typescript
import { getStepMetadata } from "workflow";

async function chargeCustomer(customerId: string, amount: number) {
  "use step";
  const { stepId } = getStepMetadata();

  return stripe.charges.create({
    customer: customerId,
    amount,
    idempotency_key: `charge:${stepId}`
  });
}
```

## Streaming

```typescript
import { getWritable } from "workflow";

export async function streamingWorkflow() {
  "use workflow";
  const writable = getWritable<{ progress: number }>();
  await streamProgress(writable);
  await closeStream(writable);
}

// IMPORTANT: All stream operations must happen in steps
async function streamProgress(writable: WritableStream) {
  "use step";
  const writer = writable.getWriter();
  try {
    for (let i = 0; i <= 100; i += 10) {
      await writer.write({ progress: i });
    }
  } finally {
    writer.releaseLock(); // Always release!
  }
}

async function closeStream(writable: WritableStream) {
  "use step";
  await writable.close();
}

// Consume in API route
export async function GET() {
  const run = await start(streamingWorkflow);
  return new Response(run.readable);
}

// Namespaced streams
const dataStream = getWritable({ namespace: "data" });
const logsStream = getWritable({ namespace: "logs" });
```

## AI Agents with @workflow/ai

```typescript
import { DurableAgent } from "@workflow/ai";
import { fetch, getWritable } from "workflow";
import { z } from "zod";

export async function chatWorkflow(messages: UIMessage[]) {
  "use workflow";

  // CRITICAL: Enable fetch for AI SDK
  globalThis.fetch = fetch;

  const writable = getWritable<UIMessageChunk>();

  const agent = new DurableAgent({
    model: "anthropic/claude-haiku-4.5",
    system: "You are a helpful assistant.",
    tools: {
      searchWeb: {
        description: "Search the web",
        parameters: z.object({ query: z.string() }),
        execute: async ({ query }) => {
          "use step";
          return await searchAPI(query);
        }
      }
    }
  });

  const result = await agent.stream({
    messages,
    writable,
    maxSteps: 10
  });

  return result.messages;
}
```

## Observability & Debugging

```bash
npx workflow web              # Visual web UI
npx workflow inspect runs     # List recent runs
npx workflow inspect run <id> # Detailed run info
npx workflow inspect steps <id> # List steps

# Production (Vercel)
npx workflow inspect runs --backend vercel --env production
```

## Deployment

**Vercel (recommended):** `vercel deploy` - no config needed

**Other backends:** Set `WORKFLOW_TARGET_WORLD`:
- `@workflow/world-local` (default dev)
- `@workflow-worlds/postgres`
- `@workflow-worlds/turso`
- `@workflow-worlds/mongodb`
- `@workflow-worlds/redis`

## Common Patterns

See `references/patterns.md` for:
- Parallel execution (Promise.all)
- Saga pattern (compensating transactions)
- Circuit breaker
- Scheduled/recurring workflows
- Human-in-the-loop
- Single vs multi-turn chat sessions

## Debugging & Errors

See `references/debugging.md` for:
- All error types and solutions
- Logging best practices
- Testing strategies
- Performance tips
- Middleware configuration
