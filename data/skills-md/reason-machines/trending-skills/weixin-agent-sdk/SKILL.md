---
name: weixin-agent-sdk
description: Bridge any AI agent backend to WeChat using the weixin-agent-sdk framework with simple Agent interface, login, and message loop.
triggers:
  - connect my AI agent to WeChat
  - integrate OpenAI with WeChat bot
  - weixin agent sdk setup
  - how to build a WeChat AI chatbot
  - bridge Claude or GPT to WeChat
  - weixin-agent-sdk usage
  - ACP agent WeChat integration
  - set up WeChat message loop with custom agent
---

# weixin-agent-sdk

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

`weixin-agent-sdk` is a TypeScript framework that bridges any AI backend to WeChat (微信) via the Clawbot channel. It uses long-polling to receive messages — no public server required — and exposes a minimal `Agent` interface so you can plug in OpenAI, Claude, or any custom logic in minutes.

---

## Installation

```bash
# npm
npm install weixin-agent-sdk

# pnpm (monorepo)
pnpm add weixin-agent-sdk
```

Node.js >= 22 required.

---

## Quick Start

### 1. Login (scan QR code once)

```typescript
import { login } from "weixin-agent-sdk";

await login();
// Credentials are persisted to ~/.openclaw/ — run once, then use start()
```

### 2. Implement the Agent interface

```typescript
import { login, start, type Agent } from "weixin-agent-sdk";

const echo: Agent = {
  async chat(req) {
    return { text: `You said: ${req.text}` };
  },
};

await login();
await start(echo);
```

---

## Core API

### `Agent` Interface

```typescript
interface Agent {
  chat(request: ChatRequest): Promise<ChatResponse>;
}

interface ChatRequest {
  conversationId: string;   // Unique user/conversation identifier
  text: string;             // Message text content
  media?: {
    type: "image" | "audio" | "video" | "file";
    filePath: string;       // Local path (already downloaded & decrypted)
    mimeType: string;
    fileName?: string;
  };
}

interface ChatResponse {
  text?: string;            // Markdown supported; auto-converted to plain text
  media?: {
    type: "image" | "video" | "file";
    url: string;            // Local path OR HTTPS URL (auto-downloaded)
    fileName?: string;
  };
}
```

### `login()`

Triggers QR code scan and persists session to `~/.openclaw/`. Only needs to run once.

### `start(agent)`

Starts the message loop. Blocks until process exits. Automatically reconnects on session expiry.

---

## Common Patterns

### Multi-turn Conversation with History

```typescript
import { login, start, type Agent } from "weixin-agent-sdk";

const conversations = new Map<string, string[]>();

const myAgent: Agent = {
  async chat(req) {
    const history = conversations.get(req.conversationId) ?? [];
    history.push(`user: ${req.text}`);

    const reply = await callMyAIService(history);

    history.push(`assistant: ${reply}`);
    conversations.set(req.conversationId, history);

    return { text: reply };
  },
};

await login();
await start(myAgent);
```

### OpenAI Agent (Full Example)

```typescript
import OpenAI from "openai";
import { login, start, type Agent, type ChatRequest } from "weixin-agent-sdk";
import * as fs from "fs";

const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
  baseURL: process.env.OPENAI_BASE_URL, // optional override
});

const model = process.env.OPENAI_MODEL ?? "gpt-4o";
const systemPrompt = process.env.SYSTEM_PROMPT ?? "You are a helpful assistant.";

type Message = OpenAI.Chat.ChatCompletionMessageParam;
const histories = new Map<string, Message[]>();

const openaiAgent: Agent = {
  async chat(req: ChatRequest) {
    const history = histories.get(req.conversationId) ?? [];

    // Build user message — support image input
    const content: OpenAI.Chat.ChatCompletionContentPart[] = [];

    if (req.text) {
      content.push({ type: "text", text: req.text });
    }

    if (req.media?.type === "image") {
      const imageData = fs.readFileSync(req.media.filePath).toString("base64");
      content.push({
        type: "image_url",
        image_url: {
          url: `data:${req.media.mimeType};base64,${imageData}`,
        },
      });
    }

    history.push({ role: "user", content });

    const response = await client.chat.completions.create({
      model,
      messages: [
        { role: "system", content: systemPrompt },
        ...history,
      ],
    });

    const reply = response.choices[0].message.content ?? "";
    history.push({ role: "assistant", content: reply });
    histories.set(req.conversationId, history);

    return { text: reply };
  },
};

await login();
await start(openaiAgent);
```

### Send Image Response

```typescript
const imageAgent: Agent = {
  async chat(req) {
    return {
      text: "Here is your image:",
      media: {
        type: "image",
        url: "/tmp/output.png",       // local path
        // or: url: "https://example.com/image.png"  — auto-downloaded
      },
    };
  },
};
```

### Send File Response

```typescript
const fileAgent: Agent = {
  async chat(req) {
    return {
      media: {
        type: "file",
        url: "/tmp/report.pdf",
        fileName: "monthly-report.pdf",
      },
    };
  },
};
```

---

## ACP (Agent Client Protocol) Integration

If you have an ACP-compatible agent (Claude Code, Codex, kimi-cli, etc.), use the `weixin-acp` package — no code needed.

```bash
# Claude Code
npx weixin-acp claude-code

# Codex
npx weixin-acp codex

# Any ACP-compatible agent (e.g. kimi-cli)
npx weixin-acp start -- kimi acp
```

`weixin-acp` launches your agent as a subprocess and communicates via JSON-RPC over stdio.

---

## Environment Variables (OpenAI Example)

| Variable | Required | Description |
|---|---|---|
| `OPENAI_API_KEY` | Yes | OpenAI API key |
| `OPENAI_BASE_URL` | No | Custom API base URL (OpenAI-compatible services) |
| `OPENAI_MODEL` | No | Model name, default `gpt-5.4` |
| `SYSTEM_PROMPT` | No | System prompt for the assistant |

---

## Built-in Slash Commands

Send these in WeChat chat to control the bot:

| Command | Description |
|---|---|
| `/echo <message>` | Echoes back directly (bypasses Agent), shows channel latency |
| `/toggle-debug` | Toggles debug mode — appends full latency stats to each reply |

---

## Supported Message Types

### Incoming (WeChat → Agent)

| Type | `media.type` | Notes |
|---|---|---|
| Text | — | Plain text in `request.text` |
| Image | `image` | Downloaded & decrypted, `filePath` = local file |
| Voice | `audio` | SILK auto-converted to WAV (requires `silk-wasm`) |
| Video | `video` | Downloaded & decrypted |
| File | `file` | Downloaded & decrypted, original filename preserved |
| Quoted message | — | Quoted text appended to `request.text`, quoted media as `media` |
| Voice-to-text | — | WeChat transcription delivered as `request.text` |

### Outgoing (Agent → WeChat)

| Type | Usage |
|---|---|
| Text | Return `{ text: "..." }` |
| Image | Return `{ media: { type: "image", url: "..." } }` |
| Video | Return `{ media: { type: "video", url: "..." } }` |
| File | Return `{ media: { type: "file", url: "...", fileName: "..." } }` |
| Text + Media | Return both `text` and `media` together |
| Remote image | Set `url` to an HTTPS link — SDK auto-downloads and uploads to WeChat CDN |

---

## Monorepo / pnpm Setup

```bash
git clone https://github.com/wong2/weixin-agent-sdk
cd weixin-agent-sdk
pnpm install

# Login (scan QR code)
pnpm run login -w packages/example-openai

# Start the OpenAI bot
OPENAI_API_KEY=$OPENAI_API_KEY pnpm run start -w packages/example-openai
```

---

## Troubleshooting

**Session expired (`errcode -14`)**
The SDK automatically enters a 1-hour cooldown and then reconnects. No manual intervention needed.

**Audio not converting from SILK to WAV**
Install the optional dependency: `npm install silk-wasm`

**Bot not receiving messages after restart**
State is persisted in `~/.openclaw/get_updates_buf`. The bot resumes from the last position automatically.

**Remote image URL not sending**
Ensure the URL is HTTPS and publicly accessible. The SDK downloads it before uploading to WeChat CDN.

**`login()` QR code not appearing**
Ensure your terminal supports rendering QR codes, or check `~/.openclaw/` for the raw QR data.
