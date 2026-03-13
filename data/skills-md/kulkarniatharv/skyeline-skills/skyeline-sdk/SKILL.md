---
name: skyeline-sdk
description: Use this skill when working with Skyeline or @skyeline/sdk. It teaches the agent how to install the SDK, configure SkyelineClient, use application-scoped prompt workflows, approvals, chat completions, structured output, webhook verification, template utilities, and Skyeline-specific error handling.
---

# Skyeline SDK

Use this skill when the user wants to integrate Skyeline, manage prompts, run chat completions through Skyeline, verify webhook events, teach another coding agent how to use the SDK, or update code that already imports `@skyeline/sdk`.

## When to use this skill

- The codebase already uses Skyeline.
- The user asks to install or initialize `@skyeline/sdk`.
- The user needs prompt CRUD, versioning, rendering, approvals, or chat completions.
- The user wants to verify Skyeline webhook events.
- The user wants OpenAI-compatible examples and has not explicitly asked for raw HTTP.
- A coding agent needs concrete Skyeline conventions rather than generic SDK guesses.

## Installation and setup

```typescript
import { SkyelineClient } from "@skyeline/sdk";

const client = new SkyelineClient({
  baseUrl: process.env.SKYELINE_BASE_URL ?? "https://api.skyeline.dev",
  apiKey: process.env.SKYELINE_API_KEY,
  // Optional:
  headers: { "X-Custom": "value" },   // additional headers for all requests
  timeoutMs: 600_000,                  // default request timeout (10 min)
  maxRetries: 2,                       // default retry count (3 total attempts)
  fetchApi: customFetch,               // custom fetch implementation
});

const app = client.app("my-app");
```

`baseUrl` and `apiKey` accept `string | undefined` — pass env vars directly; the constructor throws a descriptive error if either is missing. Use `client.app("my-app")` as the default entry point for app-scoped prompt and approval work, especially when you want to treat prompts as SDK-managed assets in apps, CI, or agents.

## Prompt management

```typescript
const app = client.app("my-app");

// List and fetch
const prompts = await app.prompts.list();
const filtered = await app.prompts.list({ status: "active" });
const prompt = await app.prompts.getLatest("support-reply");
const version = await app.prompts.getVersion("support-reply", "v2");
const versions = await app.prompts.listVersions("support-reply");

// Render with variable validation
const rendered = await app.prompts.populatePrompt("support-reply", {
  customerName: "Ava",
  issue: "billing",
});
// rendered.content = interpolated string
// rendered.prompt  = original PromptVersion

// Render a specific version
const v2Rendered = await app.prompts.populatePrompt(
  "support-reply",
  { customerName: "Ava", issue: "billing" },
  { version: "v2" },
);

// Push a new version
const updated = await app.prompts.push({
  slug: "support-reply",
  content: "Hi {{customerName}}, I can help with {{issue}}.",
  tags: ["production"],
});

// Lifecycle
await app.prompts.activate("support-reply", updated.version);
await app.prompts.promote("support-reply", "v3"); // alias for activate
await app.prompts.archive("support-reply", "v1");
await app.prompts.rollback("support-reply");
await app.prompts.delete("support-reply");

// Tags
const tags = await app.prompts.listTags();
await app.prompts.updateTags("support-reply", {
  tags: ["production", "v2"],
});
```

Use `populatePrompt` when variables matter. It validates required `{{variables}}` before interpolation and throws `MissingVariablesError` instead of silently producing a broken prompt.

## Approval workflows

```typescript
const chain = (await app.approvals.listChains())[0];

if (!chain) {
  throw new Error("Create an approval chain in the dashboard before requesting approval.");
}

// Request approval by prompt slug
const request = await app.approvals.requestBySlug("support-reply", {
  chainId: chain.id,
  comments: "Ready for review",
});

// Or request a specific version explicitly
const pinnedRequest = await app.approvals.requestBySlug(
  "support-reply",
  { chainId: chain.id },
  { version: "v2" },
);

// Store request.id so webhook events can resume the workflow later
const requestId = request.id;

// Poll only if webhook delivery is unavailable
const latestStatus = await app.approvals.get(requestId);

// Cancel your own pending request if the rollout changes
await app.approvals.cancel(requestId);

// Numeric-ID methods are still available when you already have promptId
await app.approvals.request(promptId, { chainId: chain.id });
```

`app().approvals` is the approval workflow for apps, agents, and CI. Application keys can discover chains, create approval requests, fetch request status, and cancel their own pending requests. Approvers review requests in the Skyeline dashboard. Use outbound webhooks when your workflow needs to react automatically after a request is completed. Use `requestBySlug` unless you already have a numeric prompt version ID.

## Chat and streaming

```typescript
// Non-streaming
const response = await client.chat.create({
  model: "openai/gpt-5-mini",
  messages: [{ role: "user", content: "Summarize this ticket." }],
});
console.log(response.content);      // text response
console.log(response.finishReason); // "stop" | "length" | "tool_calls" | ...
console.log(response.usage);        // { inputTokens, outputTokens, totalTokens }

// Streaming
for await (const event of client.chat.stream({
  model: "openai/gpt-5-mini",
  messages: [{ role: "user", content: "Stream a short answer." }],
})) {
  if (event.type === "text-delta") {
    process.stdout.write(event.delta);
  }
}

// Tool calls
const toolResponse = await client.chat.create({
  model: "openai/gpt-5",
  messages: [{ role: "user", content: "What is the weather in SF?" }],
  tools: [
    {
      name: "get_weather",
      description: "Get weather for a city",
      parameters: {
        type: "object",
        properties: { city: { type: "string" } },
        required: ["city"],
      },
    },
  ],
});

for (const call of toolResponse.toolCalls) {
  console.log(call.name, call.arguments);
}

// Per-request overrides (timeout, retries, headers)
await client.chat.create(
  { model: "openai/gpt-5-mini", messages: [{ role: "user", content: "Hi" }] },
  { timeoutMs: 5000, maxRetries: 0, headers: { "X-Trace-Id": "trace-123" } },
);
```

Use `client.chat.create` for standard responses and `client.chat.stream` when the UI or CLI should render incremental tokens. Stream events are typed: `text-delta`, `tool-call`, `tool-result`, `finish`, `error`.

## Structured output

```typescript
import { z } from "zod";

// object — returns inferred Zod type
const classification = await client.chat.createStructured({
  model: "openai/gpt-5-mini",
  messages: [{ role: "user", content: "Classify this support issue." }],
  output: {
    type: "object",
    name: "support_classification",
    schema: z.object({
      priority: z.enum(["low", "medium", "high"]),
      team: z.enum(["billing", "support", "sales"]),
    }),
  },
});

// array — returns inferred Zod type[]
const items = await client.chat.createStructured({
  model: "openai/gpt-5-mini",
  messages: [{ role: "user", content: "Return 3 tags for: distributed tracing" }],
  output: {
    type: "array",
    elementSchema: z.object({ tag: z.string() }),
  },
});

// choice — returns one of the string options
const route = await client.chat.createStructured({
  model: "openai/gpt-5-mini",
  messages: [{ role: "user", content: "Route to: sales, support, or engineering?" }],
  output: {
    type: "choice",
    options: ["sales", "support", "engineering"],
  },
});

// json — returns unknown (untyped JSON)
const freeform = await client.chat.createStructured({
  model: "openai/gpt-5-mini",
  messages: [{ role: "user", content: "Return a JSON summary." }],
  output: { type: "json" },
});
```

`createStructured` is non-streaming only. The SDK validates Zod-backed `object` and `array` outputs, plus `choice` outputs, before returning them. Catch `SkyelineStructuredOutputValidationError` when typed structured output does not match the declared contract. Plain JSON Schema `object` / `array` definitions and `json` outputs remain unvalidated and return `unknown`.

## Webhook verification

```typescript
import {
  SkyelineClient,
  SkyelineWebhookVerificationError,
} from "@skyeline/sdk";

export async function handleWebhook(request: Request) {
  const rawBody = await request.text();

  try {
    const event = client.webhooks.constructEvent(
      rawBody,
      request.headers,
      process.env.SKYELINE_WEBHOOK_SECRET!,
    );

    switch (event.type) {
      case "approval.requested":
        console.log(event.data.promptSlug, event.data.requester);
        break;
      case "approval.updated":
        console.log(event.data.action, event.data.actor);
        break;
      case "approval.completed":
        console.log(event.data.status, event.data.promptVersion);
        break;
    }
  } catch (error) {
    if (error instanceof SkyelineWebhookVerificationError) {
      return new Response(`Invalid webhook: ${error.code}`, { status: 400 });
    }
    return new Response("Unexpected error", { status: 500 });
  }

  return new Response("ok", { status: 200 });
}
```

`constructEvent` verifies `X-Skyeline-Signature` / `X-Skyeline-Timestamp` headers and parses a typed event. Use `verifySignature` if you only need signature verification without payload parsing. Webhook event types: `approval.requested`, `approval.updated`, `approval.completed`.

## Offline template utilities

```typescript
import { extractVariables, renderTemplate } from "@skyeline/sdk";

const variables = extractVariables("Hi {{customerName}}, issue: {{issue}}");
const content = renderTemplate("Hi {{customerName}}", {
  customerName: "Ava",
});
```

Use these utilities when you need local validation or rendering without an API call.

## Error handling

HTTP responses map to `SkyelineApiError` subclasses, while client-side helpers such as structured-output validation, webhook verification, and prompt templating expose their own typed errors.

```typescript
import {
  SkyelineApiError,
  SkyelineAuthError,
  SkyelineNotFoundError,
  SkyelineRateLimitError,
  SkyelineStructuredOutputValidationError,
  SkyelineValidationError,
  SkyelineWebhookVerificationError,
  MissingVariablesError,
} from "@skyeline/sdk";

try {
  await client.chat.createStructured({
    model: "openai/gpt-5-mini",
    messages: [{ role: "user", content: "Route this to support." }],
    output: {
      type: "choice",
      options: ["sales", "support", "engineering"],
    },
  });
} catch (error) {
  if (error instanceof SkyelineStructuredOutputValidationError) {
    console.error(error.outputType, error.rawOutput, error.issues);
  }
}

try {
  await app.prompts.getLatest("nonexistent");
} catch (error) {
  if (error instanceof SkyelineNotFoundError) {
    // 404 — resource does not exist
    console.error(error.message, error.status, error.code);
  }

  if (error instanceof SkyelineAuthError) {
    // 401 or 403 — invalid/expired API key or insufficient permissions
  }

  if (error instanceof SkyelineRateLimitError) {
    // 429 — too many requests; use retryAfterMs for backoff
    console.error(error.retryAfterMs);
  }

  if (error instanceof SkyelineValidationError) {
    // 400 or 422 — invalid request parameters
  }

  if (error instanceof SkyelineApiError) {
    // Catch-all for API errors only
    console.error(error.message, error.status, error.code, error.type);
  }
}

// Template-specific error
try {
  await app.prompts.populatePrompt("support-reply", {});
} catch (error) {
  if (error instanceof MissingVariablesError) {
    console.error(error.missingVariables); // ["customerName", "issue"]
  }
}
```

| Error Class | HTTP Status | When |
|---|---|---|
| `SkyelineAuthError` | 401, 403 | Invalid API key or insufficient permissions |
| `SkyelineNotFoundError` | 404 | Resource does not exist |
| `SkyelineRateLimitError` | 429 | Too many requests (`retryAfterMs` for backoff) |
| `SkyelineStructuredOutputValidationError` | 500 (client-side) | `createStructured` returned data that failed Zod or choice validation |
| `SkyelineValidationError` | 400, 422 | Invalid request parameters |
| `SkyelineApiError` | Any other | Server errors, unexpected failures (catch-all base) |
| `SkyelineWebhookVerificationError` | — | Invalid webhook signature, timestamp, or payload |
| `MissingVariablesError` | — | `populatePrompt` called without required variables |

## OpenAI compatibility

Skyeline exposes OpenAI-compatible endpoints for drop-in OpenAI client migrations. This is separate from the Skyeline SDK.

For new OpenAI-style integrations, prefer the Responses API. Chat Completions remains available for older code and incremental migrations.
Use `@skyeline/sdk` when you want multi-provider model calls, provider/model strings, structured output helpers, or prompt workflows.
Use the OpenAI SDK directly only when you need to preserve existing OpenAI client code.

```typescript
import OpenAI from "openai";

const openai = new OpenAI({
  apiKey: process.env.SKYELINE_API_KEY,
  baseURL: "https://api.skyeline.dev/v1",
});

const response = await openai.responses.create({
  model: "gpt-5-mini",
  instructions: "Write concise release notes.",
  input: "Summarize the latest deployment in one paragraph.",
  store: true,
});

console.log(response.output_text);
```

Chat Completions is also supported:

```typescript
import OpenAI from "openai";

const openai = new OpenAI({
  apiKey: process.env.SKYELINE_API_KEY,
  baseURL: "https://api.skyeline.dev/v1",
});

const completion = await openai.chat.completions.create({
  model: "gpt-5-mini",
  messages: [{ role: "user", content: "Hello!" }],
});
```

## Guardrails

- Install `@skyeline/sdk@beta`.
- Prefer the SDK over raw HTTP unless the user explicitly asks for cURL or fetch examples.
- Use `client.chat.create`, `client.chat.stream`, and `client.chat.createStructured` for OpenAI, Anthropic, Google, and Groq model calls.
- Use OpenAI compatibility only for existing OpenAI SDK integrations or migrations.
- Prefer `openai.responses.create` over `openai.chat.completions.create` for new OpenAI-compatible integrations.
- Prefer `client.app("my-app")` for prompt work and approval requests.
- Use `populatePrompt` instead of hand-rolling template substitution for remote prompts.
- Use `client.chat.createStructured` for typed JSON outputs — supports `object`, `array`, `choice`, and `json` types.
- Catch `SkyelineStructuredOutputValidationError` when Zod-backed object/array outputs or choice results must match a strict contract.
- Handle `text-delta` events when consuming stream output.
- Catch `SkyelineRateLimitError` and use `retryAfterMs` for backoff when building resilient integrations.
- Use `client.webhooks.constructEvent` for webhook verification — never manually parse or verify signatures.
- Do not invent unsupported SDK methods. The complete method surface is documented in the sections above.

## Reference

- Docs: https://skyeline.dev/docs/sdk
- Agent skills docs: https://skyeline.dev/docs/agent-skills
