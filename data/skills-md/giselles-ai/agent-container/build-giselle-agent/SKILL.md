---
name: build-giselle-agent
description: >
  Build AI-agent-powered Next.js apps with Giselle Agent SDK. Use when developers want to
  (1) add an AI agent to a Next.js app,
  (2) create a browser-tool-powered agent that interacts with the page,
  (3) set up Giselle Agent SDK with useChat, streamText, and browser tools,
  (4) scaffold agent definition, chat route, and UI with data-browser-tool-id.
  Triggers on "giselle agent", "build agent", "add agent to my app",
  "AI agent in Next.js", "browser tool agent", "spreadsheet agent".
---

# Build a Giselle Agent

Scaffold an AI-agent-powered Next.js app using Giselle Agent SDK. This skill interviews the developer about their use case, then generates all necessary files.

## Critical: Read the bundled reference docs

Before generating any code, read the reference docs bundled with this skill:

```
reference/getting-started.md     — Full setup walkthrough (packages, config, route, UI)
reference/architecture.md        — How the system works (provider, sandbox, browser tools, relay)
reference/spreadsheet-agent.md   — Complete example: a spreadsheet agent with browser tools
```

**Always read `reference/getting-started.md` first** — it defines the canonical file structure and API usage.

## Workflow

### Phase 1: Hearing

Ask the developer the following questions **one at a time**, waiting for each answer before asking the next. Adapt your follow-up questions based on their answers.

**Q1 — App overview**
"What kind of app are you building? (e.g., spreadsheet, form, dashboard, todo list, quiz, configurator…)"

**Q2 — Agent behavior**
"What should the agent do? Describe the main task in one or two sentences. (e.g., 'Research topics and fill the spreadsheet', 'Help the user fill out a complex form step by step', 'Generate quiz questions and populate the UI')"

**Q3 — Interactive elements**
"What UI elements should the agent be able to see and interact with? List the key inputs, buttons, or selects. (e.g., 'A grid of text inputs for a 10x6 spreadsheet', 'Name, email, and plan select fields', 'Question text and four answer option inputs')"

**Q4 — Agent type**
"Which agent runtime? `gemini` (Gemini CLI) or `codex` (Codex CLI)? Default is `gemini`."

**Q5 — Additional constraints** (optional)
"Any specific tone, rules, or constraints for the agent? (e.g., 'Always respond in Japanese', 'Never modify header cells', 'Keep answers under 50 words'). Skip if none."

### Phase 2: Generate

After hearing is complete, generate the following files. Adapt each file based on the hearing answers.

#### 1. Install packages

If packages are not already installed, tell the developer to run:

```bash
pnpm add @giselles-ai/agent @giselles-ai/browser-tool @giselles-ai/giselle-provider ai @ai-sdk/react
```

#### 2. API key setup

Before generating code, make sure the developer has an API key. Walk them through:

1. **Create an account** at [studio.giselles.ai](https://studio.giselles.ai)
2. **Navigate to API keys** — go to Settings → API Keys (or the API key management page)
3. **Generate a new API key** — click "Create API Key", give it a name (e.g., the project name), and copy the key
4. **Create `.env.local`** in the project root:

```env
GISELLE_AGENT_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx
```

> **Important:** The key starts with `gsk_`. If the developer doesn't have an account yet, they need to sign up first. The Cloud API at `studio.giselles.ai` is the default — no additional URL configuration is needed.

If the developer already has a key or `.env.local`, confirm and move on.

#### 3. `lib/agent.ts` — Agent definition

Generate the `agentMd` based on the hearing answers. The agent prompt MUST include:

- **Role description** — Who the agent is, in the context of this specific app.
- **Page Structure** — What UI elements exist and how they're laid out. Reference the `data-browser-tool-id` naming convention used in the UI.
- **How to Work** — Step-by-step workflow: understand → plan → snapshot → fill/interact → verify.
- **Important** — Constraints and rules (always act, don't just describe; keep labels short; etc.).

Use `defineAgent()` from `@giselles-ai/agent`:

```ts
import { defineAgent } from "@giselles-ai/agent";

const agentMd = `
<generated from hearing>
`;

export const agent = defineAgent({
  agentType: "<gemini or codex>",
  agentMd,
});
```

**Key principle for agentMd:** The agent runs in a cloud sandbox and cannot see the UI directly. The prompt must describe the page structure precisely — what elements exist, their `data-browser-tool-id` patterns, and what the agent should do with them. Think of it as briefing a remote contractor who can only interact through `getFormSnapshot` and `executeFormActions`.

#### 4. `next.config.ts` — Wrap with plugin

If the project already has a `next.config.ts`, wrap the existing export:

```ts
import { withGiselleAgent } from "@giselles-ai/agent/next";
import type { NextConfig } from "next";
import { agent } from "./lib/agent";

const nextConfig: NextConfig = {
  /* existing config */
};

export default withGiselleAgent(nextConfig, agent);
```

#### 5. `app/chat/route.ts` — Chat API route

This is mostly boilerplate. Generate it as-is:

```ts
import { type BrowserTools, browserTools } from "@giselles-ai/browser-tool";
import { giselle } from "@giselles-ai/giselle-provider";
import {
  consumeStream,
  convertToModelMessages,
  type InferUITools,
  streamText,
  type UIMessage,
  validateUIMessages,
} from "ai";
import { agent } from "../../lib/agent";

export async function POST(request: Request): Promise<Response> {
  const body = await request.json();
  const sessionId = body.id ?? crypto.randomUUID();

  const messages = await validateUIMessages<
    UIMessage<never, never, InferUITools<BrowserTools>>
  >({
    messages: body.messages,
    tools: browserTools,
  });

  const result = streamText({
    model: giselle({ agent }),
    messages: await convertToModelMessages(messages),
    tools: browserTools,
    providerOptions: {
      giselle: { sessionId },
    },
    abortSignal: request.signal,
  });

  return result.toUIMessageStreamResponse({
    headers: { "x-giselle-session-id": sessionId },
    consumeSseStream: consumeStream,
  });
}
```

#### 6. `app/page.tsx` — UI with browser tools

Generate a page that includes:

1. **Interactive elements with `data-browser-tool-id`** — Every element the agent should interact with MUST have this attribute. Use a predictable naming convention (e.g., `header-{i}`, `cell-{row}-{col}`, `field-name`, `submit-btn`).
2. **`useBrowserToolHandler`** — From `@giselles-ai/browser-tool/react`.
3. **`useChat`** — From `@ai-sdk/react`, configured with:
   - `transport: new DefaultChatTransport({ api: "/chat" })`
   - `sendAutomaticallyWhen: lastAssistantMessageIsCompleteWithToolCalls`
   - `...browserTool` spread
4. **`browserTool.connect(addToolOutput)`** — Bridges tool calls to the DOM.
5. **Chat message rendering** — Show text parts and tool call status with `isToolUIPart`.

```tsx
"use client";

import { useChat } from "@ai-sdk/react";
import { useBrowserToolHandler } from "@giselles-ai/browser-tool/react";
import {
  DefaultChatTransport,
  isToolUIPart,
  lastAssistantMessageIsCompleteWithToolCalls,
} from "ai";
import { useState } from "react";

export default function Home() {
  const browserTool = useBrowserToolHandler();

  const { status, messages, sendMessage, addToolOutput } = useChat({
    transport: new DefaultChatTransport({ api: "/chat" }),
    sendAutomaticallyWhen: lastAssistantMessageIsCompleteWithToolCalls,
    ...browserTool,
  });

  browserTool.connect(addToolOutput);

  const isBusy = status === "submitted" || status === "streaming";

  // ... render interactive UI with data-browser-tool-id attributes
  // ... render chat panel with messages
}
```

Adapt the UI structure to match the developer's app description from the hearing. For example:
- **Spreadsheet app** → grid of `<input>` elements with `cell-{row}-{col}` IDs
- **Form app** → labeled `<input>` and `<select>` elements with descriptive IDs like `field-name`, `field-email`
- **Quiz app** → question display + answer `<input>` elements with `question-{i}`, `answer-{i}-{j}` IDs

### Phase 3: Verify

After generating all files, tell the developer to:

1. Run `pnpm dev`
2. Confirm they see the Giselle Agent build output:
   ```
   ✦ Giselle Agent
   ✓ Authenticated
   ✓ Building...
   ✓ Ready
   ```
3. Open the app and send a test message to the agent.

## Important rules

- **Never skip the hearing phase.** Even if the developer says "just build a spreadsheet agent", ask the questions to confirm details and customize the agentMd.
- **The agentMd is the most important output.** Spend effort making it specific and actionable. A vague prompt like "You are a helpful assistant" will produce a bad agent. Reference the spreadsheet example in `reference/spreadsheet-agent.md` for the quality bar.
- **Always use `data-browser-tool-id`.** Elements without this attribute are invisible to the agent. Make sure the naming convention is predictable and documented in the agentMd.
- **Match the project's existing style.** Check if the project uses Tailwind, CSS modules, or plain CSS. Check the existing `next.config.ts` structure before modifying it.
