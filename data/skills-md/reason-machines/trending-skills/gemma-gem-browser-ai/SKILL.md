---
name: gemma-gem-browser-ai
description: Build and extend Gemma Gem, an on-device AI browser assistant Chrome extension running Google's Gemma 4 model via WebGPU with no cloud dependencies.
triggers:
  - "add a tool to gemma gem"
  - "extend the gemma gem extension"
  - "how do I build the gemma gem chrome extension"
  - "gemma gem agent loop"
  - "add a new gemma gem tool"
  - "gemma 4 webgpu chrome extension"
  - "gemma gem content script tool"
  - "on-device llm browser extension"
---

# Gemma Gem Browser AI

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Gemma Gem is a Chrome extension that runs Google's Gemma 4 model entirely on-device via WebGPU. It injects a chat overlay into every page and exposes a tool-calling agent loop that can read pages, click elements, fill forms, execute JavaScript, and take screenshots — all without sending data to any server.

## Architecture Overview

```
Offscreen Document          Service Worker           Content Script
(Gemma 4 + Agent Loop)  <-> (Message Router)    <-> (Chat UI + DOM Tools)
       |                         |
  WebGPU inference          Screenshot capture
  Token streaming           JS execution
```

- **Offscreen document** (`offscreen/`): Loads the ONNX model via `@huggingface/transformers`, runs the agent loop, streams tokens.
- **Service worker** (`background/`): Routes messages, handles `take_screenshot` and `run_javascript`.
- **Content script** (`content/`): Injects shadow DOM chat UI, executes DOM tools.
- **`agent/`**: Zero-dependency module defining `ModelBackend` and `ToolExecutor` interfaces — extractable as a standalone library.

## Install & Build

```bash
# Prerequisites: Node.js 18+, pnpm
pnpm install

# Development build (logging active, source maps)
pnpm build

# Production build (errors only, minified)
pnpm build:prod
```

Load the extension:
1. Open `chrome://extensions`
2. Enable **Developer mode**
3. Click **Load unpacked** → select `.output/chrome-mv3-dev/`

**Model download** happens automatically on first chat open:
- `onnx-community/gemma-4-E2B-it-ONNX` — ~500 MB (default)
- `onnx-community/gemma-4-E4B-it-ONNX` — ~1.5 GB

Models are cached in the browser's cache storage after the first run.

## Key Interfaces (`agent/`)

### ModelBackend

```typescript
// agent/types.ts
export interface ModelBackend {
  generate(
    messages: ChatMessage[],
    tools: ToolDefinition[],
    options: GenerateOptions
  ): AsyncGenerator<StreamChunk>;
}

export interface ToolDefinition {
  name: string;
  description: string;
  parameters: JSONSchema;
}

export interface GenerateOptions {
  maxNewTokens?: number;
  thinking?: boolean;
}
```

### ToolExecutor

```typescript
// agent/types.ts
export interface ToolExecutor {
  execute(toolName: string, args: Record<string, unknown>): Promise<unknown>;
}
```

### Agent Loop

```typescript
// agent/loop.ts — simplified illustration
export async function* runAgentLoop(
  userMessage: string,
  history: ChatMessage[],
  model: ModelBackend,
  tools: ToolExecutor,
  toolDefs: ToolDefinition[],
  maxIterations: number
): AsyncGenerator<AgentEvent> {
  const messages = [...history, { role: "user", content: userMessage }];

  for (let i = 0; i < maxIterations; i++) {
    for await (const chunk of model.generate(messages, toolDefs, {})) {
      if (chunk.type === "token") yield { type: "token", token: chunk.token };
      if (chunk.type === "tool_call") {
        yield { type: "tool_start", name: chunk.name };
        const result = await tools.execute(chunk.name, chunk.args);
        yield { type: "tool_result", name: chunk.name, result };
        messages.push({ role: "tool", name: chunk.name, content: String(result) });
      }
      if (chunk.type === "done") return;
    }
  }
}
```

## Built-in Tools

| Tool | Location | Description |
|------|----------|-------------|
| `read_page_content` | Content script | Read page text/HTML or a CSS selector |
| `take_screenshot` | Service worker | Capture visible tab as PNG |
| `click_element` | Content script | Click by CSS selector |
| `type_text` | Content script | Type into input by CSS selector |
| `scroll_page` | Content script | Scroll by pixel amount |
| `run_javascript` | Service worker | Execute JS in page context |

## Adding a New Tool

Tools live in two places: the **definition** (in the offscreen agent) and the **executor** (in content script or service worker).

### Step 1 — Define the tool schema

```typescript
// offscreen/tools/definitions.ts
export const MY_TOOL_DEFINITION: ToolDefinition = {
  name: "get_page_title",
  description: "Returns the document title of the current page.",
  parameters: {
    type: "object",
    properties: {},
    required: [],
  },
};
```

### Step 2 — Register in the tool list

```typescript
// offscreen/tools/index.ts
import { MY_TOOL_DEFINITION } from "./definitions";

export const ALL_TOOLS: ToolDefinition[] = [
  // ...existing tools
  MY_TOOL_DEFINITION,
];
```

### Step 3 — Implement execution in the content script

```typescript
// content/tools/executor.ts
export async function executeContentTool(
  name: string,
  args: Record<string, unknown>
): Promise<unknown> {
  switch (name) {
    case "get_page_title":
      return document.title;

    case "read_page_content": {
      const selector = args.selector as string | undefined;
      if (selector) {
        return document.querySelector(selector)?.textContent ?? "Not found";
      }
      return document.body.innerText;
    }

    case "click_element": {
      const el = document.querySelector(args.selector as string) as HTMLElement;
      if (!el) throw new Error(`Element not found: ${args.selector}`);
      el.click();
      return "clicked";
    }

    case "type_text": {
      const input = document.querySelector(args.selector as string) as HTMLInputElement;
      if (!input) throw new Error(`Input not found: ${args.selector}`);
      input.focus();
      input.value = args.text as string;
      input.dispatchEvent(new Event("input", { bubbles: true }));
      input.dispatchEvent(new Event("change", { bubbles: true }));
      return "typed";
    }

    default:
      throw new Error(`Unknown content tool: ${name}`);
  }
}
```

### Step 4 — Handle service-worker-side tools

```typescript
// background/tools.ts
export async function executeSwTool(
  name: string,
  args: Record<string, unknown>,
  tabId: number
): Promise<unknown> {
  switch (name) {
    case "take_screenshot": {
      const dataUrl = await chrome.tabs.captureVisibleTab({ format: "png" });
      return dataUrl;
    }

    case "run_javascript": {
      const results = await chrome.scripting.executeScript({
        target: { tabId },
        func: new Function(args.code as string) as () => unknown,
      });
      return results[0]?.result ?? null;
    }

    default:
      return null; // not a SW tool — forward to content script
  }
}
```

## Message Routing Pattern

The service worker acts as a message bus. All communication uses `chrome.runtime.sendMessage`.

```typescript
// Message types (shared/messages.ts)
export type ExtMessage =
  | { type: "TOOL_CALL"; name: string; args: Record<string, unknown>; tabId: number }
  | { type: "TOOL_RESULT"; name: string; result: unknown }
  | { type: "TOKEN"; token: string }
  | { type: "AGENT_DONE" }
  | { type: "AGENT_ERROR"; error: string };

// Offscreen → SW
chrome.runtime.sendMessage<ExtMessage>({
  type: "TOOL_CALL",
  name: "click_element",
  args: { selector: "#submit-btn" },
  tabId: currentTabId,
});

// SW → Content script
chrome.tabs.sendMessage<ExtMessage>(tabId, {
  type: "TOOL_CALL",
  name: "click_element",
  args: { selector: "#submit-btn" },
  tabId,
});
```

## Model Configuration

```typescript
// offscreen/model.ts — loading with transformers.js
import { pipeline, TextGenerationPipeline } from "@huggingface/transformers";

const MODEL_IDS = {
  E2B: "onnx-community/gemma-4-E2B-it-ONNX",
  E4B: "onnx-community/gemma-4-E4B-it-ONNX",
} as const;

export type ModelSize = keyof typeof MODEL_IDS;

export async function loadModel(
  size: ModelSize,
  onProgress: (progress: number) => void
): Promise<TextGenerationPipeline> {
  return pipeline("text-generation", MODEL_IDS[size], {
    dtype: "q4f16",
    device: "webgpu",
    progress_callback: (p: { progress: number }) => onProgress(p.progress),
  });
}
```

## Settings & Persistence

Settings are stored via `chrome.storage.sync`:

```typescript
export interface GemmaGemSettings {
  modelSize: "E2B" | "E4B";
  thinking: boolean;
  maxIterations: number;
  disabledHosts: string[];
}

const DEFAULT_SETTINGS: GemmaGemSettings = {
  modelSize: "E2B",
  thinking: false,
  maxIterations: 10,
  disabledHosts: [],
};

export async function getSettings(): Promise<GemmaGemSettings> {
  const stored = await chrome.storage.sync.get("settings");
  return { ...DEFAULT_SETTINGS, ...(stored.settings ?? {}) };
}

export async function saveSettings(patch: Partial<GemmaGemSettings>): Promise<void> {
  const current = await getSettings();
  await chrome.storage.sync.set({ settings: { ...current, ...patch } });
}

// Disable extension on current host
async function disableOnCurrentSite() {
  const host = new URL(location.href).hostname;
  const settings = await getSettings();
  if (!settings.disabledHosts.includes(host)) {
    await saveSettings({ disabledHosts: [...settings.disabledHosts, host] });
  }
}
```

## Shadow DOM Chat UI Pattern

The content script injects a shadow DOM to isolate styles:

```typescript
// content/ui.ts
export function injectChatOverlay(): ShadowRoot {
  const host = document.createElement("div");
  host.id = "gemma-gem-host";
  // Prevent page styles from leaking in
  const shadow = host.attachShadow({ mode: "closed" });

  // Inject styles
  const style = document.createElement("style");
  style.textContent = CHAT_STYLES; // imported CSS string
  shadow.appendChild(style);

  // Inject chat container
  const container = document.createElement("div");
  container.id = "gemma-gem-container";
  shadow.appendChild(container);

  document.body.appendChild(host);
  return shadow;
}
```

## Debugging

All logs use `[Gemma Gem]` prefix. Development builds log info/debug/warn; production only logs errors.

```
# Service worker logs
chrome://extensions → Gemma Gem → "Inspect views: service worker"

# Offscreen document (most useful: model loading, prompts, tool calls)
chrome://extensions → Gemma Gem → "Inspect views: offscreen.html"

# Content script logs
DevTools on any page → Console (filter: [Gemma Gem])

# All extension contexts
chrome://inspect#other
```

Key things to check in offscreen document logs:
- Model download progress
- Full prompt construction
- Token counts per turn
- Raw model output (before tool call parsing)
- Tool execution results

## Common Patterns & Gotchas

**WebGPU availability check:**
```typescript
if (!navigator.gpu) {
  throw new Error("WebGPU not supported. Use Chrome 113+ with hardware acceleration enabled.");
}
const adapter = await navigator.gpu.requestAdapter();
if (!adapter) throw new Error("No WebGPU adapter found.");
```

**Offscreen document lifecycle** — Chrome may suspend the offscreen document. Ping it before sending messages:
```typescript
async function ensureOffscreen() {
  const existing = await chrome.offscreen.hasDocument();
  if (!existing) {
    await chrome.offscreen.createDocument({
      url: "offscreen.html",
      reasons: [chrome.offscreen.Reason.WORKERS],
      justification: "Run Gemma 4 inference via WebGPU",
    });
  }
}
```

**Context window management** — Gemma 4 supports 128K tokens but inference slows with long contexts. Clear history per-page with `clear_context` or limit stored turns:
```typescript
const MAX_HISTORY_TURNS = 20;
function trimHistory(messages: ChatMessage[]): ChatMessage[] {
  if (messages.length <= MAX_HISTORY_TURNS * 2) return messages;
  return messages.slice(-MAX_HISTORY_TURNS * 2);
}
```

**Tool call parsing** — Gemma 4 emits tool calls in a structured format. If adding custom parsing, guard against partial/streamed JSON:
```typescript
function safeParseToolCall(raw: string): { name: string; args: Record<string, unknown> } | null {
  try {
    return JSON.parse(raw);
  } catch {
    return null; // still streaming
  }
}
```

**CSS selector safety for DOM tools:**
```typescript
function safeQuerySelector(selector: string): Element | null {
  try {
    return document.querySelector(selector);
  } catch {
    return null; // invalid selector from model
  }
}
```
