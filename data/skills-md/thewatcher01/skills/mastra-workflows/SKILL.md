---
name: mastra-workflows
description: Build DAG workflows with Mastra 1.x (@mastra/core/workflows). Use when implementing workflow orchestration with directed acyclic graphs, step chaining, parallel execution, branching, loops, error handling, suspend/resume, or streaming. Triggers on tasks involving createStep, createWorkflow, .then(), .parallel(), .branch(), .foreach(), .dountil(), .dowhile(), .map(), workflow state management, or Mastra step composition.
---

# Mastra Workflows — DAG Orchestration

Build type-safe DAG workflows with `@mastra/core/workflows`.

## Quick Start

```typescript
import { createStep, createWorkflow } from "@mastra/core/workflows";
import { z } from "zod";

const stepA = createStep({
  id: "step-a",
  inputSchema: z.object({ value: z.string() }),
  outputSchema: z.object({ result: z.string() }),
  execute: async ({ inputData }) => ({ result: inputData.value.toUpperCase() }),
});

const workflow = createWorkflow({ id: "my-workflow", inputSchema: z.object({ value: z.string() }) })
  .then(stepA)
  .commit();

const run = workflow.createRun();
const result = await run.start({ inputData: { value: "hello" } });
// result.results["step-a"].output → { result: "HELLO" }
```

## Imports

Always import from `@mastra/core/workflows`, NOT from `@mastra/core`:

```typescript
import { createStep, createWorkflow } from "@mastra/core/workflows";
```

## Step Anatomy

```typescript
const step = createStep({
  id: "unique-step-id",           // Required: unique identifier
  inputSchema: z.object({...}),   // Required: Zod schema for input
  outputSchema: z.object({...}),  // Required: Zod schema for output
  execute: async (params) => {    // Required: execution function
    const { inputData, getStepResult, getInitData, suspend, mapiData } = params;
    // inputData: typed input from previous step or workflow
    // getStepResult: access results from earlier named steps
    // getInitData: access original workflow input
    // suspend: pause execution (see references/suspend-resume.md)
    return { /* matches outputSchema */ };
  },
});
```

## Control Flow

Chain steps with fluent API methods. Each returns the workflow for chaining.

| Method | Purpose | Output Shape |
|--------|---------|-------------|
| `.then(step)` | Sequential execution | Direct output |
| `.parallel([a, b])` | Run steps concurrently | `{ "step-a": {...}, "step-b": {...} }` keyed by step ID |
| `.branch([[cond, step], ...])` | Conditional routing | Output keyed by executed branch step ID (use `.optional()` in next inputSchema) |
| `.foreach(step, { concurrency })` | Iterate over arrays | Array of step outputs |
| `.dountil(step, condition)` | Loop until condition met | Last iteration output (has `iterationCount`) |
| `.dowhile(step, condition)` | Loop while condition true | Last iteration output (has `iterationCount`) |
| `.map(fn)` | Transform data between steps | Custom shape |
| `.commit()` | **Required** — finalize workflow definition | — |

**Critical**: Always call `.commit()` after the last control flow method.

For detailed patterns, examples, and advanced composition: See [references/control-flow.md](references/control-flow.md)

## Error Handling

```typescript
const step = createStep({
  id: "retry-step",
  retryConfig: { attempts: 3, delay: 1000 },  // Auto-retry
  execute: async ({ inputData, bail }) => {
    if (fatalError) bail("Unrecoverable");     // Skip retries, fail immediately
    return { result: "ok" };
  },
});
```

Lifecycle callbacks on workflow run:

```typescript
const result = await run.start({
  inputData: {...},
  onFinish: (result) => { /* always called */ },
  onError: (error) => { /* called on failure */ },
});
```

For retry strategies, bail patterns, conditional error branching: See [references/error-handling.md](references/error-handling.md)

## Suspend & Resume

Pause workflow execution for human input or external events:

```typescript
const humanStep = createStep({
  id: "approval",
  inputSchema: z.object({ request: z.string() }),
  outputSchema: z.object({ approved: z.boolean() }),
  resumeSchema: z.object({ decision: z.enum(["approve", "reject"]) }),
  execute: async ({ inputData, suspend, resumeData }) => {
    if (!resumeData) {
      await suspend({ request: inputData.request });
      return undefined as never;
    }
    return { approved: resumeData.decision === "approve" };
  },
});

// Resume later:
await run.resume({ step: humanStep, resumeData: { decision: "approve" } });
```

For suspend patterns, multi-step suspend, nested workflows: See [references/suspend-resume.md](references/suspend-resume.md)

## State & Streaming

**Workflow state** — shared mutable state across steps:

```typescript
const workflow = createWorkflow({
  id: "stateful",
  inputSchema: z.object({...}),
  stateSchema: z.object({ count: z.number() }),
});

// In step execute:
execute: async ({ state, setState }) => {
  setState({ ...state, count: state.count + 1 });
  return { result: state.count };
}
```

**Streaming** — real-time step events:

```typescript
const run = workflow.createRun();
const stream = run.stream({ inputData: {...} });
for await (const chunk of stream) {
  // chunk contains step progress, transitions, outputs
}
```

For state patterns, streaming events, nested state: See [references/state-streaming.md](references/state-streaming.md)

## Nested Workflows

Use a workflow as a step inside another workflow:

```typescript
const subWorkflow = createWorkflow({ id: "sub", inputSchema, outputSchema })
  .then(stepX)
  .then(stepY)
  .commit();

const mainWorkflow = createWorkflow({ id: "main", inputSchema })
  .then(subWorkflow)
  .commit();
```

## Agent Steps

Create steps from Mastra agents:

```typescript
import { Agent } from "@mastra/core/agents";

const agent = new Agent({ name: "analyzer", instructions: "...", model });
const agentStep = createStep(agent);
// or with structured output:
const typedAgentStep = createStep(agent, { structuredOutput: { schema: z.object({...}) } });
```

## Key Rules

1. **Import path**: `@mastra/core/workflows` — never `@mastra/core`
2. **Always `.commit()`** after the last chaining method
3. **Zod schemas required** on every step (input + output)
4. **Parallel output** is keyed by step ID — destructure accordingly
5. **Branch output** uses optional fields — next step must handle missing keys
6. **`getStepResult<typeof step>("step-id")`** for accessing earlier results (type-safe)
7. **Foreach** returns an array — next step receives `{ results: [...] }`
8. **Loop steps** receive `iterationCount` in their context
