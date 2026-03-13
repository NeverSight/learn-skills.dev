---
name: tanstack-ai
description: Build AI-powered chat applications with TanStack AI and React. Use when working with @tanstack/ai, @tanstack/ai-react, @tanstack/ai-client, or any TanStack AI packages. Covers useChat hook, streaming, tools (server/client/hybrid), tool approval, structured outputs, multimodal content, adapters (OpenAI, Anthropic, Gemini, Ollama, Grok), agentic cycles, devtools, and type safety patterns. Triggers on AI chat UI, function calling, LLM integration, or streaming response tasks using TanStack AI.
---

# TanStack AI (React)

AI chat framework with isomorphic tools, streaming, and full type safety.

## Packages

- `@tanstack/ai` — core: `chat()`, `toolDefinition()`, `toServerSentEventsResponse()`, `maxIterations()`
- `@tanstack/ai-react` — React: `useChat()` hook, re-exports connection adapters
- `@tanstack/ai-client` — headless: `ChatClient`, `clientTools()`, `createChatClientOptions()`, `InferChatMessages`
- `@tanstack/ai-{openai,anthropic,gemini,ollama,grok,openrouter,fal}` — adapter packages

## Quick Start

### Install

```bash
npm install @tanstack/ai @tanstack/ai-react @tanstack/ai-openai
```

### Server (Next.js API Route)

```typescript
import { chat, toServerSentEventsResponse } from "@tanstack/ai";
import { openaiText } from "@tanstack/ai-openai";

export async function POST(request: Request) {
  const { messages } = await request.json();
  const stream = chat({
    adapter: openaiText("gpt-5.2"),
    messages,
  });
  return toServerSentEventsResponse(stream);
}
```

### Client (React)

```typescript
import { useState } from "react";
import { useChat, fetchServerSentEvents } from "@tanstack/ai-react";

export function Chat() {
  const [input, setInput] = useState("");
  const { messages, sendMessage, isLoading } = useChat({
    connection: fetchServerSentEvents("/api/chat"),
  });

  return (
    <div>
      {messages.map((message) => (
        <div key={message.id}>
          <strong>{message.role}:</strong>
          {message.parts.map((part, idx) => {
            if (part.type === "text") return <span key={idx}>{part.content}</span>;
            if (part.type === "thinking") return <em key={idx}>{part.content}</em>;
            return null;
          })}
        </div>
      ))}
      <form onSubmit={(e) => { e.preventDefault(); sendMessage(input); setInput(""); }}>
        <input value={input} onChange={(e) => setInput(e.target.value)} disabled={isLoading} />
        <button type="submit" disabled={isLoading}>Send</button>
      </form>
    </div>
  );
}
```

## useChat Hook

```typescript
const {
  messages,          // UIMessage[] — current messages
  sendMessage,       // (content: string | MultimodalContent) => Promise<void>
  append,            // (message: ModelMessage | UIMessage) => Promise<void>
  isLoading,         // boolean
  error,             // Error | undefined
  stop,              // () => void — cancel current stream
  reload,            // () => Promise<void> — regenerate last response
  clear,             // () => void — clear all messages
  setMessages,       // (messages: UIMessage[]) => void
  addToolResult,     // (result: { toolCallId, tool, output, state? }) => Promise<void>
  addToolApprovalResponse, // (response: { id, approved }) => Promise<void>
} = useChat({
  connection: fetchServerSentEvents("/api/chat"),
  tools?,             // client tool implementations
  initialMessages?,   // UIMessage[]
  id?,                // string — unique chat instance id
  body?,              // additional body params sent with every request
  onResponse?,        // (response) => void
  onChunk?,           // (chunk) => void
  onFinish?,          // (message) => void
  onError?,           // (error) => void
});
```

## Message Structure

Messages use `UIMessage` with a `parts` array:

```typescript
interface UIMessage {
  id: string;
  role: "user" | "assistant";
  parts: (TextPart | ThinkingPart | ToolCallPart | ToolResultPart)[];
}
```

Render parts by type:
- `part.type === "text"` — `part.content` (string)
- `part.type === "thinking"` — `part.content` (model reasoning, UI-only, not sent back)
- `part.type === "tool-call"` — `part.name`, `part.input`, `part.output`, `part.state`
- `part.type === "tool-result"` — `part.output`, `part.state`

## Connection Adapters

```typescript
import { fetchServerSentEvents, fetchHttpStream, stream } from "@tanstack/ai-react";

// SSE (recommended — auto-reconnection)
fetchServerSentEvents("/api/chat", { headers: { Authorization: "Bearer token" } })

// HTTP stream (NDJSON)
fetchHttpStream("/api/chat")

// Custom
stream(async (messages, data, signal) => { /* return async iterable */ })
```

## Adapters

Model passed to adapter factory — one function per activity for tree-shaking:

```typescript
import { openaiText } from "@tanstack/ai-openai";       // openaiText('gpt-5.2')
import { anthropicText } from "@tanstack/ai-anthropic";  // anthropicText('claude-sonnet-4-5')
import { geminiText } from "@tanstack/ai-gemini";        // geminiText('gemini-2.5-pro')
import { ollamaText } from "@tanstack/ai-ollama";        // ollamaText('llama3')
import { grokText } from "@tanstack/ai-grok";            // grokText('grok-4')
import { openRouterText } from "@tanstack/ai-openrouter"; // openRouterText('openai/gpt-5')
```

## Tools Overview

Two-step process: define schema with `toolDefinition()`, then implement with `.server()` or `.client()`.

```typescript
import { toolDefinition } from "@tanstack/ai";
import { z } from "zod";

const getWeatherDef = toolDefinition({
  name: "get_weather",
  description: "Get current weather for a location",
  inputSchema: z.object({ location: z.string() }),
  outputSchema: z.object({ temperature: z.number(), conditions: z.string() }),
  needsApproval: false, // optional
});

// Server implementation — runs on server with DB/API access
const getWeather = getWeatherDef.server(async ({ location }) => {
  const data = await fetchWeather(location);
  return { temperature: data.temp, conditions: data.conditions };
});

// Client implementation — runs in browser for UI/localStorage
const getWeatherClient = getWeatherDef.client((input) => {
  return { temperature: 72, conditions: "cached" };
});
```

For detailed tool patterns (server, client, hybrid, approval, agentic cycle), see [references/tools.md](references/tools.md).

## Type Safety

Use `clientTools()` + `createChatClientOptions()` + `InferChatMessages` for full type inference:

```typescript
import { clientTools, createChatClientOptions, type InferChatMessages } from "@tanstack/ai-client";

const tools = clientTools(updateUI, saveToStorage); // no 'as const' needed
const chatOptions = createChatClientOptions({
  connection: fetchServerSentEvents("/api/chat"),
  tools,
});
type ChatMessages = InferChatMessages<typeof chatOptions>;

// In component:
const { messages } = useChat(chatOptions);
// messages typed — part.name is discriminated union, part.input/output typed from Zod schemas
```

## Devtools

```bash
npm install -D @tanstack/react-ai-devtools @tanstack/react-devtools
```

```tsx
import { TanStackDevtools } from "@tanstack/react-devtools";
import { aiDevtoolsPlugin } from "@tanstack/react-ai-devtools";

<TanStackDevtools
  plugins={[aiDevtoolsPlugin()]}
  eventBusConfig={{ connectToServerBus: true }}
/>
```

## Additional Guides

- **Server setup patterns** (Next.js, TanStack Start): see [references/server-setup.md](references/server-setup.md)
- **Tool system** (server, client, hybrid, approval, agentic cycle): see [references/tools.md](references/tools.md)
- **Advanced features** (multimodal, structured outputs, runtime adapter switching): see [references/advanced.md](references/advanced.md)
