---
name: claude-code-source-recovery
description: Skill for exploring and understanding the recovered Claude Code 2.1.88 TypeScript source code, including its CLI architecture, command system, MCP integration, and Ink/React terminal UI components.
triggers:
  - explore claude code source code
  - understand claude code architecture
  - how does claude code implement commands
  - claude code mcp integration source
  - claude code terminal ui components
  - recover source from source map
  - claude code cli internals
  - study claude code codebase structure
---

# Claude Code 2.1.88 Source Recovery

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

## What This Project Is

This repository contains the recovered TypeScript source code of `@anthropic-ai/claude-code` version 2.1.88. On 2026-03-31, Anthropic accidentally published a `cli.js.map` (57MB) source map to npm that contained the full `sourcesContent` of the bundled CLI. After extraction and reconstruction, the result is ~700,000 lines of TypeScript source code organized into a readable directory structure.

The project is useful for:
- Studying production CLI architecture patterns (Ink/React in terminal)
- Understanding how MCP (Model Context Protocol) is implemented in a real CLI
- Learning how Claude Code manages sessions, commands, authentication, and tool execution

---

## Repository Structure

```
src/
├── entrypoints/        # CLI bootstrap and initialization
├── commands/           # Command definitions (login, mcp, review, tasks, etc.)
├── components/         # Ink/React terminal UI components
├── services/           # Core business logic (sync, remote capabilities, policies)
├── hooks/              # Terminal state management hooks
├── utils/              # Auth, file ops, process management helpers
└── ink/                # Custom terminal rendering infrastructure
```

---

## Installing the Original 2.1.88 Package (Tencent Mirror Cache)

The official npm version was pulled. Use the Tencent mirror cache while available:

```bash
npm install -g https://mirrors.cloud.tencent.com/npm/@anthropic-ai/claude-code/-/claude-code-2.1.88.tgz
```

---

## Extracting Source from the Source Map

If you have the original `cli.js.map`, you can recover sources programmatically:

```typescript
import fs from "fs";
import path from "path";
import zlib from "zlib";

interface SourceMap {
  version: number;
  sources: string[];
  sourcesContent: (string | null)[];
  mappings: string;
}

async function extractSourceMap(mapPath: string, outDir: string) {
  const raw = fs.readFileSync(mapPath, "utf-8");
  const sourceMap: SourceMap = JSON.parse(raw);

  for (let i = 0; i < sourceMap.sources.length; i++) {
    const sourcePath = sourceMap.sources[i];
    const content = sourceMap.sourcesContent[i];

    if (!content) continue;

    // Normalize path: strip webpack/bundle prefixes
    const normalized = sourcePath
      .replace(/^webpack:\/\/\//, "")
      .replace(/^\.\//, "");

    const outPath = path.join(outDir, normalized);
    fs.mkdirSync(path.dirname(outPath), { recursive: true });
    fs.writeFileSync(outPath, content, "utf-8");
  }

  console.log(`Extracted ${sourceMap.sources.length} source files to ${outDir}`);
}

extractSourceMap("cli.js.map", "./recovered-src");
```

---

## Key Architectural Patterns

### 1. CLI Entrypoint Bootstrap

```typescript
// src/entrypoints/cli.ts (representative pattern)
import { render } from "ink";
import React from "react";
import { App } from "../components/App";
import { parseArgs } from "../utils/args";

async function main() {
  const args = parseArgs(process.argv.slice(2));

  if (args.command) {
    // Dispatch to named command handler
    const handler = await loadCommand(args.command);
    await handler.run(args);
  } else {
    // Default: launch interactive REPL via Ink
    render(React.createElement(App, { initialArgs: args }));
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
```

### 2. Command Loading System

Commands support built-in, dynamic skills, plugins, and MCP sources:

```typescript
// src/commands/loader.ts (representative pattern)
type CommandSource = "builtin" | "skill" | "plugin" | "mcp";

interface Command {
  name: string;
  source: CommandSource;
  description: string;
  run(args: ParsedArgs): Promise<void>;
}

async function loadCommand(name: string): Promise<Command> {
  // 1. Check built-in commands first
  const builtin = builtinCommands.get(name);
  if (builtin) return builtin;

  // 2. Check MCP-registered commands
  const mcpCmd = await mcpRegistry.resolve(name);
  if (mcpCmd) return mcpCmd;

  // 3. Dynamic skill loading
  const skill = await loadSkillCommand(name);
  if (skill) return skill;

  throw new Error(`Unknown command: ${name}`);
}
```

### 3. Ink/React Terminal UI Component Pattern

```typescript
// src/components/ChatView.tsx (representative pattern)
import React, { useState, useEffect } from "react";
import { Box, Text, useInput } from "ink";
import { useConversation } from "../hooks/useConversation";

interface ChatViewProps {
  sessionId: string;
}

export function ChatView({ sessionId }: ChatViewProps) {
  const { messages, sendMessage, isStreaming } = useConversation(sessionId);
  const [input, setInput] = useState("");

  useInput((char, key) => {
    if (key.return) {
      sendMessage(input);
      setInput("");
    } else if (key.backspace) {
      setInput((prev) => prev.slice(0, -1));
    } else {
      setInput((prev) => prev + char);
    }
  });

  return (
    <Box flexDirection="column" height="100%">
      <Box flexDirection="column" flexGrow={1} overflowY="hidden">
        {messages.map((msg, i) => (
          <Box key={i} marginBottom={1}>
            <Text color={msg.role === "assistant" ? "cyan" : "white"}>
              {msg.role === "assistant" ? "Claude: " : "You: "}
            </Text>
            <Text>{msg.content}</Text>
          </Box>
        ))}
        {isStreaming && <Text color="gray">▋</Text>}
      </Box>
      <Box borderStyle="single" paddingX={1}>
        <Text>{">"} </Text>
        <Text>{input}</Text>
      </Box>
    </Box>
  );
}
```

### 4. MCP (Model Context Protocol) Integration

```typescript
// src/services/mcpClient.ts (representative pattern)
import { McpClient, Transport } from "@anthropic-ai/mcp";

interface McpServerConfig {
  name: string;
  command: string;
  args: string[];
  env?: Record<string, string>;
}

class McpRegistry {
  private clients = new Map<string, McpClient>();

  async connect(config: McpServerConfig): Promise<void> {
    const transport = new StdioTransport({
      command: config.command,
      args: config.args,
      env: { ...process.env, ...config.env },
    });

    const client = new McpClient({ name: "claude-code", version: "2.1.88" });
    await client.connect(transport);

    // Discover tools exposed by this MCP server
    const { tools } = await client.listTools();
    for (const tool of tools) {
      this.registerTool(config.name, tool);
    }

    this.clients.set(config.name, client);
  }

  async callTool(serverName: string, toolName: string, args: unknown) {
    const client = this.clients.get(serverName);
    if (!client) throw new Error(`MCP server not connected: ${serverName}`);
    return client.callTool({ name: toolName, arguments: args as Record<string, unknown> });
  }

  async resolve(commandName: string): Promise<Command | null> {
    // Map MCP tool names to CLI commands
    for (const [server, tools] of this.toolRegistry) {
      const tool = tools.find((t) => t.name === commandName);
      if (tool) {
        return {
          name: commandName,
          source: "mcp",
          description: tool.description ?? "",
          run: async (args) => {
            const result = await this.callTool(server, commandName, args);
            console.log(result.content);
          },
        };
      }
    }
    return null;
  }

  private toolRegistry = new Map<string, Array<{ name: string; description?: string }>>();

  private registerTool(server: string, tool: { name: string; description?: string }) {
    const existing = this.toolRegistry.get(server) ?? [];
    this.toolRegistry.set(server, [...existing, tool]);
  }
}

export const mcpRegistry = new McpRegistry();
```

### 5. Authentication Utilities

```typescript
// src/utils/auth.ts (representative pattern)
import fs from "fs";
import path from "path";
import os from "os";

const CONFIG_DIR = path.join(os.homedir(), ".claude");
const CREDENTIALS_FILE = path.join(CONFIG_DIR, "credentials.json");

interface Credentials {
  apiKey?: string;
  sessionToken?: string;
  expiresAt?: string;
}

export function loadCredentials(): Credentials {
  if (!fs.existsSync(CREDENTIALS_FILE)) return {};
  return JSON.parse(fs.readFileSync(CREDENTIALS_FILE, "utf-8"));
}

export function saveCredentials(creds: Credentials): void {
  fs.mkdirSync(CONFIG_DIR, { recursive: true });
  fs.writeFileSync(CREDENTIALS_FILE, JSON.stringify(creds, null, 2), {
    mode: 0o600, // owner read/write only
  });
}

export function getApiKey(): string {
  // Priority: env var > credentials file
  if (process.env.ANTHROPIC_API_KEY) {
    return process.env.ANTHROPIC_API_KEY;
  }
  const creds = loadCredentials();
  if (creds.apiKey) return creds.apiKey;
  throw new Error("No API key found. Run `claude login` or set ANTHROPIC_API_KEY.");
}
```

### 6. Feature Flags Pattern

```typescript
// src/utils/featureFlags.ts (representative pattern)
// Feature flags are resolved at build time via bun:bundle macros
// and at runtime via environment variables

type FeatureFlag =
  | "ENABLE_MCP_STREAMING"
  | "ENABLE_TASKS_COMMAND"
  | "ENABLE_REVIEW_COMMAND"
  | "ENABLE_REMOTE_CAPABILITIES";

const RUNTIME_FLAGS: Record<FeatureFlag, boolean> = {
  ENABLE_MCP_STREAMING: process.env.CLAUDE_FF_MCP_STREAMING === "1",
  ENABLE_TASKS_COMMAND: process.env.CLAUDE_FF_TASKS === "1",
  ENABLE_REVIEW_COMMAND: process.env.CLAUDE_FF_REVIEW === "1",
  ENABLE_REMOTE_CAPABILITIES: process.env.CLAUDE_FF_REMOTE === "1",
};

export function isEnabled(flag: FeatureFlag): boolean {
  return RUNTIME_FLAGS[flag] ?? false;
}

// Usage in command loader:
// if (isEnabled("ENABLE_TASKS_COMMAND")) {
//   registerCommand(tasksCommand);
// }
```

---

## Commands Documented in Source

| Command | Description |
|---------|-------------|
| `claude login` | OAuth/API key authentication flow |
| `claude mcp` | Manage MCP server connections |
| `claude review` | Code review workflow |
| `claude tasks` | Task/todo management |
| `claude config` | View and edit configuration |

---

## Hooks: Terminal State Management

```typescript
// src/hooks/useConversation.ts (representative pattern)
import { useState, useCallback, useRef } from "react";
import Anthropic from "@anthropic-ai/sdk";

export function useConversation(sessionId: string) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);
  const clientRef = useRef(new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY }));

  const sendMessage = useCallback(async (content: string) => {
    const userMessage: Message = { role: "user", content };
    setMessages((prev) => [...prev, userMessage]);
    setIsStreaming(true);

    let assistantContent = "";

    try {
      const stream = await clientRef.current.messages.stream({
        model: "claude-opus-4-5",
        max_tokens: 8096,
        messages: [...messages, userMessage].map((m) => ({
          role: m.role,
          content: m.content,
        })),
      });

      for await (const chunk of stream) {
        if (
          chunk.type === "content_block_delta" &&
          chunk.delta.type === "text_delta"
        ) {
          assistantContent += chunk.delta.text;
          setMessages((prev) => {
            const next = [...prev];
            const last = next[next.length - 1];
            if (last?.role === "assistant") {
              next[next.length - 1] = { ...last, content: assistantContent };
            } else {
              next.push({ role: "assistant", content: assistantContent });
            }
            return next;
          });
        }
      }
    } finally {
      setIsStreaming(false);
    }
  }, [messages]);

  return { messages, sendMessage, isStreaming };
}
```

---

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `ANTHROPIC_API_KEY` | Primary API key for Claude API calls |
| `CLAUDE_FF_MCP_STREAMING` | Enable MCP streaming feature flag (`1`/`0`) |
| `CLAUDE_FF_TASKS` | Enable tasks command feature flag |
| `CLAUDE_FF_REVIEW` | Enable review command feature flag |
| `CLAUDE_FF_REMOTE` | Enable remote capabilities feature flag |
| `CLAUDE_CONFIG_DIR` | Override default `~/.claude` config directory |

---

## Attempting to Run the Recovered Source

```bash
# 1. Clone the repo
git clone https://github.com/ponponon/claude_code_src
cd claude_code_src

# 2. Add a package.json (not included — must be reconstructed)
cat > package.json << 'EOF'
{
  "name": "claude-code-recovered",
  "version": "2.1.88",
  "type": "module",
  "dependencies": {
    "@anthropic-ai/sdk": "^0.51.0",
    "ink": "^5.0.0",
    "react": "^18.0.0",
    "commander": "^12.0.0"
  },
  "devDependencies": {
    "typescript": "^5.0.0",
    "@types/react": "^18.0.0",
    "@types/node": "^22.0.0"
  }
}
EOF

# 3. Install deps
npm install

# 4. Set your API key
export ANTHROPIC_API_KEY=your_key_here

# 5. Compile (bun:bundle macros will need stubs)
npx tsc --noEmit  # type-check only
```

> **Note**: The source uses `bun:bundle` macros for feature flag tree-shaking. You'll need to stub these or use Bun to build.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `bun:bundle` import errors | Replace with runtime flag checks or use Bun as the build tool |
| Missing `package.json` | Reconstruct from `node_modules` references in source imports |
| `cli.js.map` too large to parse in-memory | Stream-parse with `stream-json` npm package |
| Tencent mirror link broken | Check archive.org or other npm mirror caches |
| TypeScript path aliases unresolved | Add `paths` to `tsconfig.json` matching the original bundle's alias structure |

---

## Legal Notes

- This repository is **not affiliated with Anthropic**.
- Original code copyright belongs to **Anthropic**.
- This project is for **archival and research purposes only**.
- Do not use recovered code in production or commercial products without proper licensing.
