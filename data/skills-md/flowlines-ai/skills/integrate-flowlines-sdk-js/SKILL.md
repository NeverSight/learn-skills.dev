---
name: integrate-flowlines-sdk-js
description: Integrates the @flowlines/sdk into a Node.js/TypeScript codebase. Use when adding Flowlines observability to an AI/LLM application, setting up OpenTelemetry instrumentation for AI libraries, or when the user asks to add Flowlines monitoring.
---

# Flowlines SDK Integration Guide

This document helps AI coding agents integrate the `@flowlines/sdk` into a Node.js/TypeScript codebase.

## What is the Flowlines SDK?

`@flowlines/sdk` is a TypeScript SDK that provides OpenTelemetry-based observability for AI/LLM applications. It automatically instruments 13+ AI libraries (OpenAI, Anthropic, Cohere, AWS Bedrock, Google Vertex AI, LangChain, etc.), filters to only export LLM-relevant spans, and sends them to the Flowlines backend.

## Installation

```bash
npm install @flowlines/sdk
```

- Requires Node.js >= 20
- Requires ESM (`"type": "module"` in package.json)

## Public API

The SDK exports exactly 5 items:

```typescript
import { Flowlines, FlowlinesExporter, withContext } from "@flowlines/sdk";
import type { FlowlinesConfig, FlowlinesContext } from "@flowlines/sdk";
```

| Export | Kind | Purpose |
|---|---|---|
| `Flowlines` | Class | Main entry point. Initializes instrumentation and manages lifecycle. |
| `withContext` | Function | Attaches user/session/agent metadata to all LLM spans within a callback. |
| `FlowlinesExporter` | Class | Custom span exporter for advanced OpenTelemetry composition. |
| `FlowlinesConfig` | Type | Configuration interface for `Flowlines` constructor. |
| `FlowlinesContext` | Type | Context object passed to `withContext`. |

## Configuration

```typescript
interface FlowlinesConfig {
  apiKey: string;                        // Required. Flowlines API key.
  endpoint?: string;                     // Default: "https://ingest.flowlines.ai"
  hasExternalOtel?: boolean;             // Default: false. Set true to compose with your own NodeSDK.
  hasTraceloop?: boolean;                // Default: false. Set true for existing Traceloop setups.
  instrumentModules?: InstrumentModules; // Default: undefined (all libraries instrumented).
  exportIntervalMs?: number;             // Default: 5000
  maxQueueSize?: number;                 // Default: 2048
  maxExportBatchSize?: number;           // Default: 512
  debug?: boolean;                       // Default: false
}
```

**Validation rules:**
- `apiKey` must be a non-empty string
- `hasExternalOtel` and `hasTraceloop` are mutually exclusive
- `endpoint` must use HTTPS (HTTP is only allowed for localhost/127.0.0.1)

## Three Integration Modes

### 1. Standalone Mode (recommended for most apps)

Flowlines creates and manages its own OpenTelemetry `NodeSDK`. This is the simplest setup.

```typescript
import OpenAI from "openai";
import { Flowlines, withContext } from "@flowlines/sdk";

// CRITICAL: Initialize BEFORE creating any AI client instances.
// Use instrumentModules to pass the imported module for reliable ESM instrumentation.
const flowlines = new Flowlines({
  apiKey: process.env.FLOWLINES_API_KEY,
  instrumentModules: { openAI: OpenAI },
});

// Now create your AI clients — they will be automatically instrumented.
const openai = new OpenAI();

// Use withContext to attach user/session metadata to spans.
const response = await withContext({ userId: "user-123", sessionId: "sess-456" }, () =>
  openai.chat.completions.create({
    model: "gpt-4o",
    messages: [{ role: "user", content: "Hello" }],
  })
);

// Shutdown gracefully before process exit.
await flowlines.shutdown();
```

> **ESM note:** In ESM applications, all `import` statements are hoisted to the top of the module and executed before any other code. This means auto-instrumentation (without `instrumentModules`) may not patch modules in time. Always use `instrumentModules` to pass the imported modules explicitly — this guarantees reliable instrumentation regardless of import order.

### 2. External OpenTelemetry Mode

Use when the app already has its own `NodeSDK` setup and you want to add Flowlines to the existing pipeline.

```typescript
import { Flowlines, withContext } from "@flowlines/sdk";
import { NodeSDK } from "@opentelemetry/sdk-node";

const flowlines = new Flowlines({
  apiKey: process.env.FLOWLINES_API_KEY,
  hasExternalOtel: true,
});

const sdk = new NodeSDK({
  spanProcessors: [flowlines.createSpanProcessor()],
  instrumentations: flowlines.getInstrumentations(),
});
sdk.start();

// ... use withContext as usual ...

await flowlines.shutdown();
await sdk.shutdown();
```

### 3. Traceloop Mode

Use when the app already has Traceloop initialized.

```typescript
import { Flowlines } from "@flowlines/sdk";

const flowlines = new Flowlines({
  apiKey: process.env.FLOWLINES_API_KEY,
  hasTraceloop: true,
});

// Add flowlines.createSpanProcessor() to your Traceloop configuration.
```

## Using `withContext()`

`withContext` attaches `flowlines.user_id`, `flowlines.session_id`, and `flowlines.agent_id` attributes to all LLM spans created within its callback. This is how Flowlines associates traces with users, sessions, and agents.

```typescript
interface FlowlinesContext {
  userId: string;
  sessionId?: string;
  agentId?: string;
}

function withContext<T>(ctx: FlowlinesContext, fn: () => T): T;
```

- `userId` is required (string)
- `sessionId` is optional (omit to skip)
- `agentId` is optional (omit to skip)
- `fn` can be sync or async — the return value (or Promise) is forwarded
- Supports nesting: inner calls override outer values
- Must wrap every AI/LLM call that should carry user context

```typescript
// Async usage with session and agent
const result = await withContext(
  { userId: "user-123", sessionId: "sess-456", agentId: "agent-1" },
  async () => {
    return await openai.chat.completions.create({ /* ... */ });
  }
);

// Without session or agent ID
await withContext({ userId: "user-123" }, async () => {
  await anthropic.messages.create({ /* ... */ });
});

// Nested contexts (inner overrides outer)
await withContext({ userId: "user-A", sessionId: "sess-1" }, async () => {
  // spans here have user_id="user-A", session_id="sess-1"
  await withContext({ userId: "user-B", sessionId: "sess-2" }, async () => {
    // spans here have user_id="user-B", session_id="sess-2"
  });
});
```

## Context integration guidance

When integrating `withContext`, you MUST wrap LLM calls with context. Follow these steps:

1. **Identify existing data** in the codebase that maps to `userId`, `sessionId`, and `agentId`:
   - `userId`: the end-user making the request (e.g., authenticated user ID, email, API key owner)
   - `sessionId`: the conversation or session grouping multiple interactions (e.g., chat thread ID, session token, conversation UUID)
   - `agentId`: the AI agent or assistant handling the request (e.g., agent name, bot identifier, assistant ID)

2. **If obvious mappings exist**, use them directly. For example, if the app has `req.user.id` and a `threadId`, wire them in:
   ```typescript
   await withContext({ userId: req.user.id, sessionId: threadId }, async () => { ... });
   ```

3. **If mappings are unclear**, ask the user which variables or fields should be used for `userId`, `sessionId`, and `agentId`.

4. **If no data is available yet**, propose using placeholder values with TODO comments so the integration is functional and easy to complete later:
   ```typescript
   await withContext(
     {
       userId: "anonymous", // TODO: replace with actual user identifier
       sessionId: `sess-${Date.now()}`, // TODO: replace with actual session/conversation ID
       agentId: "my-agent", // TODO: replace with actual agent identifier
     },
     async () => { ... }
   );
   ```
   Only include fields that are relevant. `sessionId` and `agentId` can be omitted entirely if not applicable.

## Selective Instrumentation with `instrumentModules`

By default, all 13+ supported libraries are instrumented. To instrument only specific libraries, pass `instrumentModules` with the imported modules. **The required import style varies by library:**

**OpenAI — use the default import:**

```typescript
import OpenAI from "openai";

const flowlines = new Flowlines({
  apiKey: process.env.FLOWLINES_API_KEY,
  instrumentModules: { openAI: OpenAI },
});
```

**Anthropic — use a namespace import:**

```typescript
import * as AnthropicModule from "@anthropic-ai/sdk";

const flowlines = new Flowlines({
  apiKey: process.env.FLOWLINES_API_KEY,
  instrumentModules: { anthropic: AnthropicModule },
});
```

**Both together:**

```typescript
import OpenAI from "openai";
import * as AnthropicModule from "@anthropic-ai/sdk";

const flowlines = new Flowlines({
  apiKey: process.env.FLOWLINES_API_KEY,
  instrumentModules: {
    openAI: OpenAI,
    anthropic: AnthropicModule,
  },
});
```

Supported keys: `openAI`, `anthropic`, `cohere`, `bedrock`, `google_vertexai`, `google_aiplatform`, `google_generativeai`, `pinecone`, `together`, `chromadb`, `qdrant`, `langchain`, `llamaIndex`, `mcp`.

**Important:** The import style required depends on the library. OpenAI requires the **default import** (the class itself). Anthropic and most other libraries require a **namespace import** (`import * as X from "..."`). Using the wrong import style will cause instrumentation to silently fail or throw errors.

## Critical Integration Rules

1. **Initialize Flowlines BEFORE creating AI client instances.** The SDK uses monkey-patching via OpenTelemetry instrumentation. Clients created before `new Flowlines(...)` will not be instrumented.

2. **Only one standalone Flowlines instance can exist at a time.** Creating a second standalone instance throws an error. Call `shutdown()` first, or use `hasExternalOtel`/`hasTraceloop` for composition.

3. **Always call `shutdown()` before process exit.** This flushes any pending spans to the backend. Without it, the last batch of traces may be lost.

4. **Wrap LLM calls with `withContext()` to associate traces with users.** Without `withContext`, spans are still exported but lack user/session/agent metadata.

5. **The SDK only exports LLM-related spans.** It filters for spans with `gen_ai.*` or `ai.*` attribute prefixes. Non-LLM OpenTelemetry spans (HTTP, DB, etc.) are discarded by the Flowlines exporter.

## Graceful Shutdown Pattern

```typescript
const flowlines = new Flowlines({ apiKey: "..." });

// Handle process signals
process.on("SIGINT", async () => {
  await flowlines.shutdown();
  process.exit(0);
});

process.on("SIGTERM", async () => {
  await flowlines.shutdown();
  process.exit(0);
});
```

## Known Limitations

- **OpenAI `responses.create` is not instrumented.** The underlying OpenTelemetry instrumentation only patches `chat.completions.create`. Calls to the newer `responses.create` API will not produce traces. Use `chat.completions.create` for traced interactions.

## Common Errors

| Error | Cause | Fix |
|---|---|---|
| `Flowlines API key is required` | Empty or missing `apiKey` | Provide a valid API key |
| `Cannot set both hasExternalOtel and hasTraceloop` | Both flags set to true | Use only one mode flag |
| `A standalone Flowlines instance is already active` | Creating a second standalone instance | Call `shutdown()` on the first, or use `hasExternalOtel: true` |
| `Invalid Flowlines endpoint URL` | Malformed URL in `endpoint` | Provide a valid URL |
| `Insecure Flowlines endpoint` | HTTP endpoint that is not localhost | Use HTTPS, or use localhost for development |

## Full Example: Anthropic Chat with Tools

```typescript
import * as AnthropicModule from "@anthropic-ai/sdk";
import Anthropic from "@anthropic-ai/sdk";
import { Flowlines, withContext } from "@flowlines/sdk";

// 1. Init Flowlines FIRST
const flowlines = new Flowlines({
  apiKey: process.env.FLOWLINES_API_KEY,
  instrumentModules: { anthropic: AnthropicModule },
});

// 2. Then create the AI client
const client = new Anthropic();

// 3. Wrap calls with withContext
const sessionId = `sess-${Date.now()}`;
const reply = await withContext({ userId: "user-123", sessionId }, () =>
  client.messages.create({
    model: "claude-sonnet-4-20250514",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello!" }],
  })
);

// 4. Shutdown before exit
await flowlines.shutdown();
```
