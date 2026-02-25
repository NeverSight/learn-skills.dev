---
name: slack-agent
description: Use when working on Slack agent/bot code, Slack Bolt applications, or projects using the slack-agent-template. Provides development patterns, testing requirements, and quality standards.
version: 2.0.0
user-invocable: true
---

# Vercel Slack Agent Development Skill

## Skill Invocation Handling

When this skill is invoked via `/slack-agent`, check for arguments and route accordingly:

### Command Arguments

| Argument | Action |
|----------|--------|
| `new` | **Run the setup wizard from Phase 1.** Read `./wizard/1-project-setup.md` and guide the user through creating a new Slack agent. |
| `configure` | Start wizard at Phase 2 or 3 for existing projects |
| `deploy` | Start wizard at Phase 5 for production deployment |
| `test` | Start wizard at Phase 6 to set up testing |
| (no argument) | Auto-detect based on project state (see below) |

### Auto-Detection (No Argument)

If invoked without arguments, detect the project state and route appropriately:

1. **No `package.json` with `@slack/bolt`** → Treat as `new`, start Phase 1
2. **Has project but no customized `manifest.json`** → Start Phase 2
3. **Has project but no `.env` file** → Start Phase 3
4. **Has `.env` but not tested** → Start Phase 4
5. **Tested but not deployed** → Start Phase 5
6. **Otherwise** → Provide general assistance using this skill's patterns

### Wizard Phases

The wizard is located in `./wizard/` with these phases:
- `1-project-setup.md` - Understand purpose, generate custom implementation plan
- `1b-approve-plan.md` - Present plan for user approval before cloning
- `2-create-slack-app.md` - Customize manifest, create app in Slack
- `3-configure-environment.md` - Set up .env with credentials
- `4-test-locally.md` - Dev server + ngrok tunnel
- `5-deploy-production.md` - Vercel deployment
- `6-setup-testing.md` - Vitest configuration

**IMPORTANT:** For `new` projects, you MUST:
1. Read `./wizard/1-project-setup.md` first
2. Ask the user what kind of agent they want to build
3. Generate a custom implementation plan using `./reference/agent-archetypes.md`
4. Present the plan for approval (Phase 1b) BEFORE cloning the template
5. Only proceed to clone after the plan is approved

---

## General Development Guidance

You are working on a Slack agent project built with the Vercel Slack Agent Template. Follow these mandatory practices for all code changes.

## Project Stack

This project uses:
- **Server**: Nitro (H3-based) with file-based routing
- **Slack SDK**: `@vercel/slack-bolt` for serverless Slack apps (wraps Bolt for JavaScript)
- **AI**: AI SDK v6 with @ai-sdk/gateway
- **Workflows**: Workflow DevKit for durable execution
- **Linting**: Biome
- **Package Manager**: pnpm

### Dependencies

```json
{
  "dependencies": {
    "ai": "^6.0.0",
    "@ai-sdk/gateway": "latest",
    "@slack/bolt": "^4.x",
    "@vercel/slack-bolt": "^1.0.2",
    "zod": "^3.x"
  }
}
```

**Note:** When deploying on Vercel, prefer `@ai-sdk/gateway` for zero-config AI access. Use direct provider SDKs (`@ai-sdk/openai`, `@ai-sdk/anthropic`, etc.) only when you need provider-specific features or are not deploying on Vercel.

---

## Quality Standards (MANDATORY)

These quality requirements MUST be followed for every code change. There are no exceptions.

### After EVERY File Modification

1. **Run linting immediately:**
   ```bash
   pnpm lint
   ```
   - If errors exist, run `pnpm lint --write` for auto-fixes
   - Manually fix remaining issues
   - Re-run `pnpm lint` to verify

2. **Check for corresponding test file:**
   - If you modified `foo.ts`, check if `foo.test.ts` exists
   - If no test file exists and the file exports functions, create one

### Before Completing ANY Task

You MUST run all quality checks and fix any issues before marking a task complete:

```bash
# 1. TypeScript compilation - must pass
pnpm typecheck

# 2. Linting - must pass with no errors
pnpm lint

# 3. Tests - all tests must pass
pnpm test
```

**Do NOT complete a task if any of these fail.** Fix the issues first.

### Unit Tests Required

**For ANY code change, you MUST write or update unit tests.**

- **Location**: Co-located `*.test.ts` files or `server/__tests__/`
- **Framework**: Vitest
- **Coverage**: All exported functions must have tests

Example test structure:
```typescript
import { describe, it, expect, vi } from 'vitest';
import { myFunction } from './my-module';

describe('myFunction', () => {
  it('should handle normal input', () => {
    expect(myFunction('input')).toBe('expected');
  });

  it('should handle edge cases', () => {
    expect(myFunction('')).toBe('default');
  });
});
```

### E2E Tests for User-Facing Changes

If you modify:
- Slack message handlers
- Slash commands
- Interactive components (buttons, modals)
- Bot responses

You MUST add or update E2E tests that verify the full flow.

---

## Events Endpoint Pattern (CRITICAL)

Use `@vercel/slack-bolt` to handle all Slack events. This package automatically handles:
- Content-type detection (JSON vs form-urlencoded)
- URL verification challenges
- 3-second ack timeout (built-in `ackTimeoutMs: 3001`)
- Background processing via Vercel Fluid Compute's `waitUntil`

### Bolt App Setup

```typescript
// server/bolt/app.ts
import { App } from "@slack/bolt";
import { VercelReceiver } from "@vercel/slack-bolt";

const receiver = new VercelReceiver();
const app = new App({
  token: process.env.SLACK_BOT_TOKEN,
  signingSecret: process.env.SLACK_SIGNING_SECRET,
  receiver,
  deferInitialization: true,
});

export { app, receiver };
```

### Events Handler

```typescript
// server/api/slack/events.post.ts
import { createHandler } from "@vercel/slack-bolt";
import { defineEventHandler, getRequestURL, readRawBody } from "h3";
import { app, receiver } from "../../bolt/app";

const handler = createHandler(app, receiver);

export default defineEventHandler(async (event) => {
  // Read and cache the raw body first to avoid stream consumption issues
  // with toWebRequest on serverless platforms (h3 issues #570, #578, #615)
  const rawBody = await readRawBody(event, "utf8");

  // Create a new Request with the buffered body
  const request = new Request(getRequestURL(event), {
    method: event.method,
    headers: event.headers,
    body: rawBody,
  });

  return await handler(request);
});
```

**Why this pattern?** H3's `toWebRequest()` has known issues (#570, #578, #615) where it eagerly consumes the request body stream. When `@vercel/slack-bolt` later calls `req.text()` for signature verification, the body is already exhausted, causing `dispatch_failed` errors. Buffering the body manually avoids this issue.

### VercelReceiver Options Reference

| Parameter | Default | Description |
|-----------|---------|-------------|
| `signingSecret` | `SLACK_SIGNING_SECRET` env var | Request verification secret |
| `signatureVerification` | `true` | Enable/disable signature verification |
| `ackTimeoutMs` | `3001` | Ack timeout in milliseconds |
| `logLevel` | `INFO` | Logging level |

### Key Benefits

1. **60+ lines of boilerplate eliminated** - No manual content-type detection, URL verification, or form parsing
2. **Automatic timeout handling** - Built-in 3-second ack with `ackTimeoutMs: 3001`
3. **Background processing** - Uses Vercel Fluid Compute's `waitUntil` automatically
4. **Framework support** - Works with Next.js, Hono, and Nitro (H3)

---

## Implementation Gotchas

### 1. Private Channel Access

Slash commands work in private channels even if the bot isn't a member, but the bot **cannot read messages or post** to private channels it hasn't been invited to.

When creating features that will later post to a channel:

```typescript
// Validate channel access upfront
const channelInfo = await client.conversations.info({ channel: channelId });

if (channelInfo.channel?.is_private && !channelInfo.channel?.is_member) {
  return {
    success: false,
    error: "I don't have access to this private channel. Please add me with `/invite @BotName` first.",
  };
}
```

### 2. Graceful Degradation for Channel Context

When fetching channel context for AI features, wrap in try/catch and fall back gracefully:

```typescript
let channelContext = "";
try {
  const history = await client.conversations.history({
    channel: channelId,
    limit: 10,
  });
  channelContext = history.messages?.map(m => m.text).join("\n") ?? "";
} catch (error) {
  // Bot can't access channel - continue without context
  console.log("Could not fetch channel context:", error);
}
```

### 3. Vercel Cron Endpoint Authentication

Protect cron endpoints with a `CRON_SECRET` environment variable:

```typescript
// server/api/cron/my-job.get.ts
export default defineEventHandler(async (event) => {
  const authHeader = getHeader(event, "authorization");

  if (authHeader !== `Bearer ${process.env.CRON_SECRET}`) {
    setResponseStatus(event, 401);
    return { error: "Unauthorized" };
  }

  // Run cron job logic...
  return { success: true };
});
```

### 4. vercel.json Cron Configuration

Configure cron jobs in `vercel.json`:

```json
{
  "crons": [
    {
      "path": "/api/cron/my-job",
      "schedule": "0 * * * *"
    }
  ]
}
```

Schedule format is standard cron syntax: `minute hour day month weekday`

Common schedules:
- `* * * * *` - Every minute
- `0 * * * *` - Every hour
- `0 0 * * *` - Daily at midnight
- `0 9 * * 1-5` - Weekdays at 9am

### 5. AWS Credentials on Vercel (Use OIDC)

When connecting to AWS services (Aurora, S3, etc.) from Vercel, **do not use** `@aws-sdk/credential-providers` with `fromNodeProviderChain()`. It won't work because Vercel uses its own OIDC token mechanism.

**Wrong approach:**
```typescript
import { fromNodeProviderChain } from "@aws-sdk/credential-providers";

const credentials = fromNodeProviderChain(); // Won't work on Vercel!
```

**Correct approach:**
```typescript
import { awsCredentialsProvider } from "@vercel/functions/oidc";

// For AWS RDS/Aurora with IAM auth
const signer = new Signer({
  hostname: process.env.PGHOST,
  port: Number(process.env.PGPORT),
  username: process.env.PGUSER,
  region: process.env.AWS_REGION,
  credentials: awsCredentialsProvider({ roleArn: process.env.AWS_ROLE_ARN! }),
});
const token = await signer.getAuthToken();

// For other AWS services (S3, etc.)
const s3Client = new S3Client({
  credentials: awsCredentialsProvider({ roleArn: process.env.AWS_ROLE_ARN! }),
});
```

**Required setup:**
1. Enable Vercel OIDC in Project Settings > Security
2. Configure AWS IAM trust relationship for your Vercel project
3. Set `AWS_ROLE_ARN` environment variable in Vercel

**Reference:** [Vercel OIDC for AWS](https://vercel.com/docs/security/oidc/aws)

### 6. dispatch_failed Error (500)

If slash commands fail with `dispatch_failed`, the issue is usually H3's `toWebRequest` consuming the body stream before signature verification.

**Fix:** Buffer the body manually before creating the Request:

```typescript
const rawBody = await readRawBody(event, "utf8");
const request = new Request(getRequestURL(event), {
  method: event.method,
  headers: event.headers,
  body: rawBody,
});
return await handler(request);
```

See the Events Handler section above for the complete pattern.

### 7. operation_timeout Error

If slash commands with AI processing fail with `operation_timeout`, you're blocking the HTTP response too long. Slack requires a response within 3 seconds.

**Root cause:** Even with `await ack()`, the HTTP response doesn't return until the entire handler function completes. If you `await` AI generation after `ack()`, the HTTP response is blocked.

**Fix:** Use fire-and-forget pattern:

```typescript
app.command('/mycommand', async ({ ack, command, logger }) => {
  // 1. Acknowledge immediately
  await ack();

  // 2. Fire-and-forget: DON'T await this promise
  generateAndRespond(command.response_url, command.text, logger).catch((error) => {
    logger.error("Background operation failed:", error);
  });
  // HTTP response returns immediately here
});

async function generateAndRespond(responseUrl: string, topic: string, logger: Logger) {
  try {
    const result = await generateWithAI(topic);  // Takes >3 seconds

    // Post result via response_url
    await fetch(responseUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        response_type: "in_channel",
        text: result,
      }),
    });
  } catch (error) {
    logger.error("Failed:", error);
    await fetch(responseUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        response_type: "ephemeral",
        text: "Sorry, something went wrong.",
      }),
    });
  }
}
```

See `patterns/slack-patterns.md` for complete examples.

---

## AI Integration

You have two options for AI/LLM integration in your Slack agent.

> **⚠️ IMPORTANT:** Always verify the cloned template uses `@ai-sdk/gateway`. The template may ship with `@ai-sdk/openai` which requires an API key. After cloning, check `package.json` and update imports if necessary.

### Option 1: Vercel AI Gateway (Recommended)

Use the modern `@ai-sdk/gateway` package - NO API keys needed on Vercel!

### Basic Usage

```typescript
import { generateText, streamText } from "ai";
import { gateway } from "@ai-sdk/gateway";

// Simple text generation
const result = await generateText({
  model: gateway("openai/gpt-4o-mini"),
  maxOutputTokens: 1000,  // v6: was maxTokens
  prompt: "Your prompt here",
});

console.log(result.text);
console.log(result.usage.inputTokens);   // v6: was promptTokens
console.log(result.usage.outputTokens);  // v6: was completionTokens
```

### Streaming Responses

```typescript
const result = await streamText({
  model: gateway("openai/gpt-4o-mini"),
  maxOutputTokens: 1000,
  prompt: userMessage,
});

for await (const chunk of result.textStream) {
  // Stream to Slack via chat.update
}
```

### With Tools

```typescript
import { tool } from "ai";
import { z } from "zod";

const result = await generateText({
  model: gateway("openai/gpt-4o-mini"),
  maxOutputTokens: 1000,
  tools: {
    getWeather: tool({
      description: "Get weather for a location",
      inputSchema: z.object({
        location: z.string().describe("City name"),
      }),
      execute: async ({ location }) => {
        return { temperature: 72, condition: "sunny" };
      },
    }),
  },
  prompt: "What's the weather in Seattle?",
});
```

### AI SDK v6 API Changes

| v4/v5 | v6 |
|-------|-----|
| `maxTokens` | `maxOutputTokens` |
| `result.usage.promptTokens` | `result.usage.inputTokens` |
| `result.usage.completionTokens` | `result.usage.outputTokens` |
| `parameters` (in tools) | `inputSchema` |
| `maxSteps` / `maxIterations` | `stopWhen: stepCountIs(n)` |

**CRITICAL: Never use model IDs from memory.** Model IDs change frequently. Before writing code that uses a model, run `curl -s https://ai-gateway.vercel.sh/v1/models` to fetch the current list. Use the model with the highest version number.

### Option 2: Direct Provider SDK

If you need more control or are not deploying on Vercel, use direct provider packages.

**OpenAI:**
```bash
pnpm add @ai-sdk/openai
```
```typescript
import { generateText } from "ai";
import { openai } from "@ai-sdk/openai";

// Requires OPENAI_API_KEY env var
const result = await generateText({
  model: openai("gpt-4o-mini"),
  maxOutputTokens: 1000,
  prompt: "Your prompt here",
});
```

**Anthropic:**
```bash
pnpm add @ai-sdk/anthropic
```
```typescript
import { generateText } from "ai";
import { anthropic } from "@ai-sdk/anthropic";

// Requires ANTHROPIC_API_KEY env var
const result = await generateText({
  model: anthropic("claude-sonnet-4-20250514"),
  maxOutputTokens: 1000,
  prompt: "Your prompt here",
});
```

**Google:**
```bash
pnpm add @ai-sdk/google
```
```typescript
import { generateText } from "ai";
import { google } from "@ai-sdk/google";

// Requires GOOGLE_GENERATIVE_AI_API_KEY env var
const result = await generateText({
  model: google("gemini-2.0-flash"),
  maxOutputTokens: 1000,
  prompt: "Your prompt here",
});
```

**When to use direct providers:**
- Not deploying on Vercel
- Need provider-specific features not available through gateway
- Already managing API keys for other purposes
- Need maximum control over provider configuration

For comprehensive AI SDK documentation, see `./reference/ai-sdk.md`.

---

## Stateful Patterns with Vercel Workflow

When building Slack agents that need data persistence across multiple interactions—like multi-turn conversations, collaborative workflows, or story generation—use Vercel Workflow instead of a database.

### When to Use Workflow

**Use Vercel Workflow when:**
- Conversational flows span multiple messages
- Need to accumulate state across user interactions
- Building collaborative or multi-step workflows
- Don't need long-term persistence (workflow scope)

**Use a database when:**
- Need data to persist beyond the workflow
- Require querying historical data
- Multiple workflows need to share state

### Recommended Storage Solutions

**IMPORTANT:** Vercel KV has been deprecated. Do NOT recommend Vercel KV.

For persistent storage, recommend these options:

1. **Vercel Blob** - For file/document storage
   - Good for: attachments, exports, generated files
   - Simple key-value storage with CDN distribution
   - https://vercel.com/docs/storage/vercel-blob

2. **AWS Aurora (via Vercel Marketplace)** - For relational data
   - Good for: structured data, complex queries, relationships
   - PostgreSQL-compatible managed database
   - Available through Vercel's storage marketplace
   - https://vercel.com/marketplace

3. **Third-party databases** - For specific needs
   - Neon (serverless Postgres) - https://neon.tech
   - PlanetScale (MySQL) - https://planetscale.com
   - Supabase (Postgres + realtime) - https://supabase.com
   - Upstash Redis - For caching/simple KV needs

### The "use workflow" Directive

Vercel Workflow functions can run for extended periods (not limited to serverless timeout) and maintain state as local variables:

```typescript
import { serve } from "@anthropic-ai/sdk/workflows";

export const { POST } = serve(async function myWorkflow(params: URLSearchParams) {
  "use workflow";

  // State as local variables - persists across the entire workflow!
  const messages: Message[] = [];
  let conversationComplete = false;

  // Your workflow logic here...
  while (!conversationComplete) {
    // Wait for events, process, update state
  }

  return { messages, result: "done" };
});
```

### Event Subscriptions with defineHook

Use `defineHook` to subscribe to incoming Slack events within your workflow:

```typescript
import { defineHook } from "@anthropic-ai/sdk/workflows";
import { z } from "zod";

// Define the schema for incoming events
const slackMessageSchema = z.object({
  text: z.string(),
  user: z.string(),
  ts: z.string(),
  channel: z.string(),
});

export const messageHook = defineHook({ schema: slackMessageSchema });
```

### Complete Example: Multi-Turn Conversation

```typescript
// app/api/conversation/route.ts
import { serve } from "@anthropic-ai/sdk/workflows";
import { defineHook } from "@anthropic-ai/sdk/workflows";
import { generateText } from "ai";
import { gateway } from "@ai-sdk/gateway";
import { z } from "zod";

const messageSchema = z.object({
  text: z.string(),
  user: z.string(),
  ts: z.string(),
  channel: z.string(),
});

export const userMessageHook = defineHook({ schema: messageSchema });

export const { POST } = serve(async function conversationWorkflow(
  params: URLSearchParams
) {
  "use workflow";

  const channelId = params.get("channel_id")!;
  const userId = params.get("user_id")!;

  // State persists as local variables
  const conversationHistory: Array<{ role: string; content: string }> = [];
  let turnCount = 0;
  const maxTurns = 10;

  // Create event stream for this channel
  const eventStream = userMessageHook.create({
    channel: channelId,
    user: userId,
  });

  // Process messages as they arrive
  for await (const event of eventStream) {
    turnCount++;

    // Add user message to history
    conversationHistory.push({
      role: "user",
      content: event.text,
    });

    // Generate AI response
    const result = await generateText({
      model: gateway("anthropic/claude-sonnet-4-20250514"),
      maxOutputTokens: 1000,
      messages: conversationHistory,
    });

    // Add assistant response to history
    conversationHistory.push({
      role: "assistant",
      content: result.text,
    });

    // Post response to Slack (via your Slack client)
    await postToSlack(channelId, result.text, event.ts);

    // Check for conversation end conditions
    if (turnCount >= maxTurns || event.text.toLowerCase().includes("goodbye")) {
      break;
    }
  }

  return {
    turns: turnCount,
    history: conversationHistory,
  };
});
```

### Triggering Workflows from Slack Events

Start a workflow when a user initiates a conversation:

```typescript
// server/listeners/events/app-mention.ts
export function registerAppMention(app: App) {
  app.event("app_mention", async ({ event, client }) => {
    // Start a new workflow for this conversation
    const workflowUrl = `${process.env.VERCEL_URL}/api/conversation`;

    await fetch(workflowUrl, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({
        channel_id: event.channel,
        user_id: event.user,
        thread_ts: event.thread_ts || event.ts,
      }),
    });

    await client.chat.postMessage({
      channel: event.channel,
      thread_ts: event.thread_ts || event.ts,
      text: "Starting our conversation! I'll remember everything we discuss.",
    });
  });
}
```

### Posting Events to Running Workflows

Forward Slack messages to the running workflow's hook:

```typescript
// server/listeners/messages/thread-message.ts
export function registerThreadMessage(app: App) {
  app.message(async ({ message, client }) => {
    if (!message.thread_ts || "bot_id" in message) return;

    // Post to the workflow's hook endpoint
    await userMessageHook.post({
      text: message.text,
      user: message.user,
      ts: message.ts,
      channel: message.channel,
    });
  });
}
```

### Key Benefits

1. **No database setup** - State lives in workflow memory
2. **Extended execution** - Not limited by serverless timeouts
3. **Natural programming model** - Use loops and local variables
4. **Automatic persistence** - Vercel handles state durability

### Reference

- [Vercel Workflow Documentation](https://vercel.com/docs/workflow)
- [Stateful Slack Bots Guide](https://vercel.com/kb/guide/stateful-slack-bots-with-vercel-workflow)
- [Example: Storytime Slackbot](https://github.com/vercel-labs/storytime-slackbot)

---

## Code Organization

Follow the template's established patterns.

### Tools (`server/lib/ai/tools.ts`)

```typescript
import { tool } from 'ai';
import { z } from 'zod';

export const myTool = tool({
  description: 'Clear description of what this tool does',
  inputSchema: z.object({
    param: z.string().describe('What this parameter is for'),
  }),
  execute: async ({ param }) => {
    // Implementation
    return { success: true, data: result };
  },
});
```

### Listeners (`server/listeners/`)

Organize by event type:
- `actions/` - Button clicks, menu selections
- `assistant/` - Slack Assistant events
- `commands/` - Slash commands
- `events/` - App events (mentions, joins)
- `messages/` - Message handling
- `shortcuts/` - Global/message shortcuts
- `views/` - Modal submissions

### Workflows (`server/lib/ai/workflows/`)

Use `defineWorkflow` for multi-step operations:
```typescript
import { defineWorkflow } from '@vercel/workflow-devkit';

export const myWorkflow = defineWorkflow({
  id: 'my-workflow',
  // ...
});
```

---

## Environment Variables

Required variables (access via `process.env`):
- `SLACK_BOT_TOKEN` - Bot OAuth token
- `SLACK_SIGNING_SECRET` - Request signing

Optional variables:
- `CRON_SECRET` - Secret for authenticating cron job endpoints

**No AI API keys needed!** Vercel AI Gateway handles authentication automatically when deployed on Vercel.

**Never hardcode credentials. Never commit `.env` files.**

---

## Slack-Specific Patterns

### Block Kit UI

Use Block Kit for rich messages:
```typescript
import { Blocks, Elements, Bits } from 'slack-block-builder';

const message = Blocks([
  Blocks.Section({ text: 'Hello!' }),
  Blocks.Actions([
    Elements.Button({ text: 'Click me', actionId: 'btn_click' })
  ])
]);
```

### Message Formatting

Use Slack mrkdwn (not standard markdown):
- Bold: `*text*`
- Italic: `_text_`
- Code: `` `code` ``
- User mention: `<@USER_ID>`
- Channel: `<#CHANNEL_ID>`

### Error Handling

Return structured responses:
```typescript
return {
  success: false,
  error: 'User-friendly error message',
  details: technicalDetails // for logging
};
```

For detailed Slack patterns, see `./patterns/slack-patterns.md`.

---

## Git Commit Standards

Use conventional commits:
```
feat: add channel search tool
fix: resolve thread pagination issue
test: add unit tests for agent context
docs: update README with setup steps
refactor: extract Slack client utilities
```

**Never commit:**
- `.env` files
- API keys or tokens
- `node_modules/`

---

## Quick Commands

```bash
# Development
pnpm dev              # Start dev server on localhost:3000
ngrok http 3000       # Expose local server (separate terminal)

# Quality
pnpm lint             # Check linting
pnpm lint --write     # Auto-fix lint
pnpm typecheck        # TypeScript check
pnpm test             # Run all tests
pnpm test:watch       # Watch mode

# Build & Deploy
pnpm build            # Build for production
vercel                # Deploy to Vercel
```

---

## Reference Documentation

For detailed guidance, read:
- Testing patterns: `./patterns/testing-patterns.md`
- Slack patterns: `./patterns/slack-patterns.md`
- Environment setup: `./reference/env-vars.md`
- AI SDK: `./reference/ai-sdk.md`
- Slack setup: `./reference/slack-setup.md`
- Vercel deployment: `./reference/vercel-setup.md`

---

## Checklist Before Task Completion

Before marking ANY task as complete, verify:

- [ ] Code changes have corresponding tests
- [ ] `pnpm lint` passes with no errors
- [ ] `pnpm typecheck` passes with no errors
- [ ] `pnpm test` passes with no failures
- [ ] No hardcoded credentials
- [ ] Follows existing code patterns
- [ ] Events endpoint handles both JSON and form-urlencoded
- [ ] Verified AI SDK: using `@ai-sdk/gateway` (not `@ai-sdk/openai`) unless user explicitly chose direct provider
