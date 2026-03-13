---
name: claude-agent-sdk
description: |
  Expert guide for building AI agents with the Claude Agent SDK (Python & TypeScript).
  Use this skill PROACTIVELY whenever:
  - Building or configuring AI agents with `claude_agent_sdk` or `@anthropic-ai/claude-agent-sdk`
  - Working with `query()`, `ClaudeAgentOptions`, `AgentDefinition`, hooks, sessions, subagents, MCP, or custom tools
  - User asks how to automate tasks, build pipelines, or orchestrate multi-agent workflows with Claude
  - Implementing permission controls, `canUseTool` callbacks, or tool restrictions
  - Connecting external services (databases, APIs, browsers) to a Claude agent via MCP
  - Debugging or optimizing agent behavior, streaming, sessions, or hooks
  - Any mention of "Claude agent", "agent SDK", "agentic loop", or autonomous Claude workflows
  Covers the full SDK: query API, built-in tools, hooks lifecycle, session management, subagents,
  MCP servers, custom in-process tools, permission modes, user input flows, structured outputs,
  thinking config, effort levels, V2 preview API, session discovery, error handling, and authentication.
---

# Claude Agent SDK — Complete Guide

The Claude Agent SDK lets you build AI agents that autonomously read files, run commands, search the web, edit code, and more — using the same tools and agent loop that power Claude Code.

**Languages:** Python (`claude-agent-sdk`) and TypeScript (`@anthropic-ai/claude-agent-sdk`)

## Quick Reference

| Goal | Go to |
|------|-------|
| First agent | [Setup & Installation](#setup--installation) |
| Configure tools/permissions | [Core Options (ClaudeAgentOptions)](#core-options-claudeagentoptions) |
| React to tool calls | [Hooks](#hooks) |
| Multi-turn memory | [Sessions](#sessions) |
| Delegate to specialists | [Subagents](#subagents) |
| Connect external APIs/DBs | [MCP Servers](#mcp-servers) |
| Build in-process tools | [Custom Tools](#custom-tools) |
| Load skills & plugins | [Skills & Plugins](#skills--plugins) |
| Control tool approvals | [Permissions & User Input](#permissions--user-input) |
| Customize system prompt | [System Prompts & CLAUDE.md](#system-prompts--claudemd) |
| Track costs & usage | [Cost Tracking](#cost-tracking) |
| Undo file changes | [File Checkpointing](#file-checkpointing) |
| Interrupt / stop agent | [Interrupt & Stop Reasons](#interrupt--stop-reasons) |
| Multi-turn client | [ClaudeSDKClient](#claudesdkclient-multi-turn-client) |
| Structured output | [Structured Outputs](#structured-outputs) |
| Thinking & effort | [Thinking & Effort](#thinking--effort) |
| Sandbox & secure deploy | [Sandbox & Secure Deployment](#sandbox--secure-deployment) |
| SDK internals & IPC | [SDK Internal Architecture](#sdk-internal-architecture) |
| Deploy to production | [Authentication & Hosting](#authentication--hosting) |
| Use Pro/Max subscription | [Using Pro/Max Subscription with the SDK](#using-promax-subscription-with-the-sdk) |
| Session discovery | [Session Discovery](#session-discovery) |
| V2 Preview API (TS) | [TypeScript V2 Preview](#typescript-v2-preview) |
| Query object methods (TS) | [Query Object Methods (TS)](#query-object-methods-ts) |
| Error handling | [Error Types](#error-types) |
| Advanced reference | `references/` directory |

---

## Setup & Installation

```bash
# TypeScript
npm install @anthropic-ai/claude-agent-sdk

# Python (pip)
pip install claude-agent-sdk

# Python (uv — recommended)
uv add claude-agent-sdk
```

Set your API key:
```bash
export ANTHROPIC_API_KEY=your-api-key
```

**Minimal working agent:**

```python
# Python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    async for message in query(
        prompt="What files are in this directory?",
        options=ClaudeAgentOptions(allowed_tools=["Bash", "Glob"]),
    ):
        if hasattr(message, "result"):
            print(message.result)

asyncio.run(main())
```

```typescript
// TypeScript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "What files are in this directory?",
  options: { allowedTools: ["Bash", "Glob"] }
})) {
  if ("result" in message) console.log(message.result);
}
```

---

## Core Options (ClaudeAgentOptions)

All options for `query()` — Python uses `snake_case`, TypeScript uses `camelCase`.

| Option (Python / TS) | Type | Description |
|---|---|---|
| `allowed_tools` / `allowedTools` | `string[]` | Whitelist of tools Claude can use |
| `disallowed_tools` / `disallowedTools` | `string[]` | Blacklist of tools |
| `tools` | `string[] \| ToolsPreset` | Alternative to `allowed_tools`; also accepts presets |
| `permission_mode` / `permissionMode` | `string` | `"default"`, `"acceptEdits"`, `"bypassPermissions"`, `"plan"`, `"dontAsk"` |
| `system_prompt` / `systemPrompt` | `string \| object` | Custom string or preset object (see [System Prompts](#system-prompts--claudemd)) |
| `model` | `string` | Model ID or shorthand (`"sonnet"`, `"opus"`, `"haiku"`) |
| `fallback_model` / `fallbackModel` | `string` | Fallback model if primary is unavailable |
| `max_turns` / `maxTurns` | `number` | Maximum agentic turns |
| `max_budget_usd` / `maxBudgetUsd` | `float` | Maximum spend in USD per query (triggers `error_max_budget_usd` on exceed) |
| `thinking` | `object` | Thinking config: `{type:"adaptive"}`, `{type:"enabled",budget_tokens:N}`, `{type:"disabled"}` |
| `effort` | `string` | Thinking depth: `"low"`, `"medium"`, `"high"`, `"max"` |
| `max_thinking_tokens` / `maxThinkingTokens` | `number` | **Deprecated** — use `thinking` instead |
| `output_format` / `outputFormat` | `object` | Structured output schema: `{type:"json_schema", schema:{...}}` |
| `resume` | `string` | Session ID to resume |
| `fork_session` / `forkSession` | `boolean` | Fork session instead of continuing |
| `continue_conversation` / `continue` | `boolean` | Continue most recent conversation |
| `mcp_servers` / `mcpServers` | `object \| string` | MCP server configurations (inline object or path to `.mcp.json`) |
| `agents` | `object` | Subagent definitions (keyed by name) |
| `hooks` | `object` | Hook event callbacks |
| `can_use_tool` / `canUseTool` | `function` | Callback for runtime tool approval |
| `setting_sources` / `settingSources` | `string[]` | Load from filesystem (`["user"`, `"project"`, `"local"]`) |
| `cwd` | `string` | Working directory for the agent |
| `env` | `object` | Environment variables to pass |
| `plugins` | `array` | Programmatic plugins (slash commands, agents, MCP) |
| `sandbox` | `object` | Sandbox settings (see [Sandbox](#sandbox--secure-deployment)) |
| `enable_file_checkpointing` / `enableFileCheckpointing` | `boolean` | Enable file change tracking for rewind |
| `extra_args` / `extraArgs` | `object` | Additional CLI arguments to pass |
| `betas` | `string[]` | Beta features (e.g., `["context-1m-2025-08-07"]` for 1M context window) |
| `add_dirs` / `additionalDirectories` | `string[]` | Additional directories Claude can access |
| `user` | `string` | User identifier (for logging/tracking) |
| `cli_path` / `cliPath` | `string` | Custom path to Claude CLI binary |
| `include_partial_messages` / `includePartialMessages` | `boolean` | Include partial streaming messages |
| `stderr` | `function` | Custom stderr handler callback |

**TypeScript-only options:**

| Option (TS only) | Type | Description |
|---|---|---|
| `sessionId` | `string` | Use a specific UUID for the session |
| `persistSession` | `boolean` | Disable disk persistence (`false` to skip saving) |
| `resumeSessionAt` | `string` | Resume at a specific message UUID |
| `promptSuggestions` | `boolean` | Enable `SDKPromptSuggestionMessage` after each turn |
| `abortController` | `AbortController` | For cancelling operations externally |
| `agent` | `string` | Agent name for the main thread |
| `debug` / `debugFile` | `boolean` / `string` | Enable debug mode / write debug logs to file |
| `spawnClaudeCodeProcess` | `function` | Custom process spawning (VMs, containers, remote) |
| `allowDangerouslySkipPermissions` | `boolean` | Required when using `bypassPermissions` |
| `strictMcpConfig` | `boolean` | Enforce strict MCP server validation |
| `executable` / `executableArgs` | `string` / `string[]` | JS runtime (`"bun"`, `"deno"`, `"node"`) and args |

### Built-in Tools Reference

| Tool | Purpose |
|------|---------|
| `Read` | Read any file (text, image, PDF, Jupyter notebooks) |
| `Write` | Create new files |
| `Edit` | Precise string replacements in existing files |
| `Bash` | Run terminal commands, scripts, git (supports background execution) |
| `Glob` | Find files by pattern (`**/*.ts`) |
| `Grep` | Search file contents with regex (ripgrep-based) |
| `WebSearch` | Search the web |
| `WebFetch` | Fetch and parse web pages |
| `AskUserQuestion` | Ask user clarifying questions (multiple choice) |
| `Task` | Invoke subagents (required when using `agents`) |
| `TaskOutput` | Retrieve output from background tasks |
| `TaskStop` | Stop a running background task |
| `Skill` | Invoke installed skills (requires `setting_sources`) |
| `TodoWrite` | Create/manage structured task lists for progress tracking |
| `NotebookEdit` | Edit Jupyter notebook cells (`.ipynb` files) |
| `Config` | Get/set agent configuration values |
| `ExitPlanMode` | Exit planning mode with optional allowed prompts |
| `EnterWorktree` | Create and enter a git worktree for isolated work |
| `ListMcpResources` | List available resources from configured MCP servers |
| `ReadMcpResource` | Read a specific resource from an MCP server by URI |

**Common tool combinations:**
- Read-only: `["Read", "Glob", "Grep"]`
- Code editing: `["Read", "Edit", "Write", "Glob", "Grep"]`
- Full automation: `["Read", "Edit", "Write", "Bash", "Glob", "Grep"]`
- Web research: `["WebSearch", "WebFetch", "Read"]`
- With subagents: add `"Task"` to any combination
- With skills: add `"Skill"` and configure `setting_sources`

---

## Message Types

The `query()` async iterator yields typed messages:

```python
# Python — check message type
from claude_agent_sdk import AssistantMessage, ResultMessage, SystemMessage

async for message in query(prompt="...", options=...):
    if isinstance(message, SystemMessage) and message.subtype == "init":
        session_id = message.data.get("session_id")
    elif isinstance(message, AssistantMessage):
        for block in message.content:
            if hasattr(block, "text"):
                print(block.text)          # Claude's reasoning
            elif hasattr(block, "name"):
                print(f"Tool: {block.name}")  # Tool call
    elif isinstance(message, ResultMessage):
        print(f"Done ({message.subtype}): {message.result}")
```

```typescript
// TypeScript — check message type
for await (const message of query({ prompt: "..." })) {
  if (message.type === "system" && message.subtype === "init") {
    const sessionId = message.session_id;
  } else if (message.type === "assistant") {
    for (const block of message.message.content) {
      if ("text" in block) console.log(block.text);
      else if ("name" in block) console.log(`Tool: ${block.name}`);
    }
  } else if (message.type === "result") {
    console.log(`Done (${message.subtype}): ${message.result}`);
  }
}
```

**Result subtypes:** `"success"` | `"error_during_execution"` | `"error_max_turns"` | `"error_max_budget_usd"` | `"error_max_structured_output_retries"`

**ResultMessage extended fields:**
- `result` — Final text output
- `stop_reason` — `"end_turn"` or `"tool_use"`
- `num_turns`, `duration_ms`, `total_cost_usd`
- `session_id` — For session resumption
- `structured_output` — Parsed JSON when using `output_format`
- `permission_denials` — Array of `{tool_name, tool_use_id, tool_input}` for denied tools
- `modelUsage` — Per-model usage breakdown: `{inputTokens, outputTokens, cacheReadInputTokens, cacheCreationInputTokens, webSearchRequests, costUSD, contextWindow, maxOutputTokens}`

### Additional Message Types (TypeScript)

TypeScript exposes additional message types beyond the core four:

| Message Type | Description |
|---|---|
| `SDKPartialAssistantMessage` | Partial streaming message (requires `includePartialMessages`) |
| `SDKStatusMessage` | Status updates (compacting, permission mode changes) |
| `SDKCompactBoundaryMessage` | Marks conversation compaction boundary |
| `SDKRateLimitEvent` | Rate limit info: `status` ("allowed" / "allowed_warning" / "rejected"), `resetsAt`, `utilization` |
| `SDKPromptSuggestionMessage` | Prompt suggestions (requires `promptSuggestions: true`) |
| `SDKFilesPersistedEvent` | Files persisted to disk with `files[]` and `failed[]` |
| `SDKHookStartedMessage` / `SDKHookProgressMessage` / `SDKHookResponseMessage` | Hook execution lifecycle |
| `SDKToolProgressMessage` / `SDKToolUseSummaryMessage` | Tool execution progress and summaries |
| `SDKTaskStartedMessage` / `SDKTaskProgressMessage` / `SDKTaskNotificationMessage` | Background task lifecycle |
| `SDKAuthStatusMessage` | Authentication status updates |

---

## Hooks

Hooks are callback functions that intercept agent events. Use them to block/allow tools, log operations, inject context, or notify external systems.

### Hook Events

| Event | Trigger | Python | TypeScript |
|-------|---------|--------|------------|
| `PreToolUse` | Before tool call (can block/modify) | ✅ | ✅ |
| `PostToolUse` | After tool result | ✅ | ✅ |
| `PostToolUseFailure` | On tool error | ✅ | ✅ |
| `UserPromptSubmit` | On user prompt | ✅ | ✅ |
| `Stop` | Agent stops | ✅ | ✅ |
| `SubagentStart` | Subagent spawned | ✅ | ✅ |
| `SubagentStop` | Subagent finishes | ✅ | ✅ |
| `Notification` | Agent status message | ✅ | ✅ |
| `PreCompact` | Before conversation compaction | ✅ | ✅ |
| `PermissionRequest` | Permission dialog | ✅ | ✅ |
| `SessionStart` / `SessionEnd` | Session lifecycle | ❌ | ✅ |
| `Setup`, `TeammateIdle`, `TaskCompleted` | Advanced lifecycle | ❌ | ✅ |
| `WorktreeCreate` / `WorktreeRemove` | Git worktree events | ❌ | ✅ |
| `ConfigChange` | Config file changes | ❌ | ✅ |

### Hook Configuration

```python
# Python
from claude_agent_sdk import query, ClaudeAgentOptions, HookMatcher

async def my_hook(input_data, tool_use_id, context):
    # input_data has: hook_event_name, tool_name, tool_input, session_id, cwd
    file_path = input_data.get("tool_input", {}).get("file_path", "")
    if ".env" in file_path:
        return {
            "hookSpecificOutput": {
                "hookEventName": input_data["hook_event_name"],
                "permissionDecision": "deny",
                "permissionDecisionReason": "Cannot modify .env files",
            }
        }
    return {}  # Empty = allow

options = ClaudeAgentOptions(
    hooks={
        "PreToolUse": [
            HookMatcher(matcher="Write|Edit", hooks=[my_hook])
        ]
    }
)
```

```typescript
// TypeScript
import { query, HookCallback, PreToolUseHookInput } from "@anthropic-ai/claude-agent-sdk";

const myHook: HookCallback = async (input, toolUseID, { signal }) => {
  const preInput = input as PreToolUseHookInput;
  const toolInput = preInput.tool_input as Record<string, unknown>;
  const filePath = toolInput?.file_path as string;

  if (filePath?.includes(".env")) {
    return {
      hookSpecificOutput: {
        hookEventName: preInput.hook_event_name,
        permissionDecision: "deny",
        permissionDecisionReason: "Cannot modify .env files"
      }
    };
  }
  return {}; // Empty = allow
};

// Usage
const options = {
  hooks: {
    PreToolUse: [{ matcher: "Write|Edit", hooks: [myHook] }]
  }
};
```

### Hook Output Fields

**Top-level fields** (affect conversation):
- `systemMessage: string` — inject context Claude can see
- `continue` (`continue_` in Python): `boolean` — whether agent keeps running

**`hookSpecificOutput`** fields (affect the current operation):
- `permissionDecision`: `"allow"` | `"deny"` | `"ask"`
- `permissionDecisionReason`: `string` — shown to Claude on deny
- `updatedInput`: `object` — modified tool input (requires `permissionDecision: "allow"`)
- `additionalContext`: `string` — append to tool result (PostToolUse only)

**Async output** (fire-and-forget, for logging/webhooks):
```python
return {"async_": True, "asyncTimeout": 30000}   # Python
```
```typescript
return { async: true, asyncTimeout: 30000 };      // TypeScript
```

For detailed examples (audit logging, sandbox redirection, Slack notifications): see [references/hooks.md](references/hooks.md)

---

## Sessions

Sessions maintain full context (files read, analysis, conversation) across multiple queries.

```python
# Python — capture and resume session
session_id = None

# First query
async for message in query(prompt="Read the auth module", options=ClaudeAgentOptions(allowed_tools=["Read", "Glob"])):
    if hasattr(message, "subtype") and message.subtype == "init":
        session_id = message.data.get("session_id")

# Resume with full context
async for message in query(
    prompt="Now find all callers of it",  # "it" = auth module from previous query
    options=ClaudeAgentOptions(resume=session_id),
):
    if hasattr(message, "result"):
        print(message.result)
```

```typescript
// TypeScript
let sessionId: string | undefined;

// First query
for await (const message of query({ prompt: "Read the auth module", options: { allowedTools: ["Read", "Glob"] } })) {
  if (message.type === "system" && message.subtype === "init") {
    sessionId = message.session_id;
  }
}

// Resume
for await (const message of query({ prompt: "Now find all callers", options: { resume: sessionId } })) {
  if ("result" in message) console.log(message.result);
}
```

### Fork a Session

Create a new branch from a session without modifying the original:

```python
# Python
options = ClaudeAgentOptions(resume=session_id, fork_session=True)
```
```typescript
// TypeScript
const options = { resume: sessionId, forkSession: true };
```

| | `forkSession: false` (default) | `forkSession: true` |
|--|--|--|
| Session ID | Same as original | New ID generated |
| Original | Modified | Preserved |
| Use case | Continue conversation | Explore alternatives |

For multi-turn patterns and session persistence details: see [references/sessions.md](references/sessions.md)

---

## Subagents

Subagents are specialized agent instances the main agent can delegate to. Benefits: isolated context, parallel execution, specialized tools/prompts.

**Key requirement:** Include `"Task"` in `allowedTools` — subagents are invoked via the Task tool.

```python
# Python
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition

async for message in query(
    prompt="Use the code-reviewer agent to review auth.py",
    options=ClaudeAgentOptions(
        allowed_tools=["Read", "Glob", "Grep", "Task"],
        agents={
            "code-reviewer": AgentDefinition(
                description="Expert code reviewer. Use for quality, security, and maintainability reviews.",
                prompt="You are a security-focused code reviewer. Identify vulnerabilities and suggest fixes.",
                tools=["Read", "Glob", "Grep"],  # Read-only
                model="sonnet",  # Override model for this subagent
            )
        },
    ),
):
    if hasattr(message, "result"):
        print(message.result)
```

```typescript
// TypeScript
for await (const message of query({
  prompt: "Use the code-reviewer agent to review auth.py",
  options: {
    allowedTools: ["Read", "Glob", "Grep", "Task"],
    agents: {
      "code-reviewer": {
        description: "Expert code reviewer. Use for quality, security, and maintainability reviews.",
        prompt: "You are a security-focused code reviewer. Identify vulnerabilities and suggest fixes.",
        tools: ["Read", "Glob", "Grep"],
        model: "sonnet"
      }
    }
  }
})) {
  if ("result" in message) console.log(message.result);
}
```

### AgentDefinition Fields

| Field | Required | Python / TS | Description |
|-------|----------|-------------|-------------|
| `description` | ✅ | Both | When to use this agent (determines auto-invocation) |
| `prompt` | ✅ | Both | Subagent's system prompt / expertise |
| `tools` | ❌ | Both | Allowed tools (omit to inherit all) |
| `model` | ❌ | Both | `"sonnet"`, `"opus"`, `"haiku"`, `"inherit"`, or model ID |
| `disallowed_tools` / `disallowedTools` | ❌ | TS | Blacklist tools for this subagent |
| `mcp_servers` / `mcpServers` | ❌ | TS | Subagent-specific MCP servers |
| `skills` | ❌ | TS | Skills this subagent can access |
| `max_turns` / `maxTurns` | ❌ | TS | Turn limit for this subagent |

### Task Tool Extended Input (TS)

When invoking subagents via the `Task` tool, TypeScript supports additional parameters:

```typescript
// Task tool input supports these fields:
{
  description: "Short task description",
  prompt: "Detailed task instructions",
  subagent_type: "code-reviewer",    // Agent name
  model: "sonnet",                    // Override model
  run_in_background: true,            // Run as background task
  resume: "agent-session-id",         // Resume a previous subagent
  max_turns: 10,                      // Limit turns
  isolation: "worktree",              // Run in isolated git worktree
  name: "review-task-1",             // Task identifier
  team_name: "reviewers",            // Team grouping
}
```

**Notes:**
- Subagents cannot spawn their own subagents (don't add `"Task"` to subagent tools)
- Use explicit naming in prompt to guarantee a specific subagent: `"Use the X agent to..."`
- Messages from subagent context have `parent_tool_use_id` set

For subagent resumption and parallel patterns: see [references/subagents.md](references/subagents.md)

---

## MCP Servers

Connect your agent to databases, browsers, APIs, and hundreds of external tools via the Model Context Protocol.

### MCP Tool Naming
MCP tools follow: `mcp__<server-name>__<tool-name>`
Example: server `"github"` + tool `list_issues` → `mcp__github__list_issues`

### Add MCP Servers

```python
# Python — connect to GitHub MCP server
from claude_agent_sdk import query, ClaudeAgentOptions
import os

options = ClaudeAgentOptions(
    mcp_servers={
        "github": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-github"],
            "env": {"GITHUB_TOKEN": os.environ["GITHUB_TOKEN"]},
        }
    },
    allowed_tools=["mcp__github__list_issues", "mcp__github__search_issues"],
)
```

```typescript
// TypeScript
const options = {
  mcpServers: {
    github: {
      command: "npx",
      args: ["-y", "@modelcontextprotocol/server-github"],
      env: { GITHUB_TOKEN: process.env.GITHUB_TOKEN }
    }
  },
  allowedTools: ["mcp__github__list_issues", "mcp__github__search_issues"]
};
```

### Transport Types

| Type | When to use | Config |
|------|-------------|--------|
| **stdio** | Local CLI tools (`npx`, `uvx`) | `command`, `args`, `env` |
| **HTTP** | Remote REST APIs | `type: "http"`, `url`, `headers` |
| **SSE** | Remote streaming APIs | `type: "sse"`, `url`, `headers` |
| **SDK MCP** | In-process custom tools | See [Custom Tools](#custom-tools) |
| **claudeai-proxy** (TS) | Claude.ai proxy servers | `type: "claudeai-proxy"`, `url`, `id` |

```python
# Remote SSE server with auth
mcp_servers = {
    "remote-api": {
        "type": "sse",
        "url": "https://api.example.com/mcp/sse",
        "headers": {"Authorization": f"Bearer {os.environ['API_TOKEN']}"},
    }
}
```

### Wildcard Tool Access
```python
allowed_tools=["mcp__github__*"]   # All tools from github server
```

### MCP Tool Search (large tool sets)
When tools exceed 10% of context window, auto-activates to load tools on-demand:
```python
env={"ENABLE_TOOL_SEARCH": "auto"}    # default
env={"ENABLE_TOOL_SEARCH": "auto:5"}  # activate at 5% threshold
env={"ENABLE_TOOL_SEARCH": "true"}    # always on
env={"ENABLE_TOOL_SEARCH": "false"}   # always load all upfront
```
*Requires: claude-sonnet-4 or claude-opus-4+. Not available on Haiku.*

### Dynamic MCP Management (TypeScript)

The TypeScript `Query` object supports runtime MCP server control:

```typescript
const q = query({ prompt: "...", options });

// Replace all MCP servers dynamically
const result = await q.setMcpServers({
  "new-server": { command: "npx", args: ["-y", "some-mcp-server"] }
});
// result: { added: ["new-server"], removed: ["old-server"], errors: [] }

// Reconnect a failed server
await q.reconnectMcpServer("github");

// Enable/disable a server
await q.toggleMcpServer("github", false);  // disable
await q.toggleMcpServer("github", true);   // re-enable
```

For .mcp.json config files and error handling patterns: see [references/mcp.md](references/mcp.md)

---

## Custom Tools

Define in-process MCP servers to give Claude custom capabilities without running a separate process.

```python
# Python
from claude_agent_sdk import tool, create_sdk_mcp_server, ClaudeSDKClient, ClaudeAgentOptions
import aiohttp, asyncio
from typing import Any

@tool("get_weather", "Get temperature for coordinates", {"latitude": float, "longitude": float})
async def get_weather(args: dict[str, Any]) -> dict[str, Any]:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://api.open-meteo.com/v1/forecast?latitude={args['latitude']}&longitude={args['longitude']}&current=temperature_2m"
        ) as response:
            data = await response.json()
    return {"content": [{"type": "text", "text": f"Temp: {data['current']['temperature_2m']}°C"}]}

custom_server = create_sdk_mcp_server(name="weather-tools", version="1.0.0", tools=[get_weather])

async def main():
    options = ClaudeAgentOptions(
        mcp_servers={"weather-tools": custom_server},
        allowed_tools=["mcp__weather-tools__get_weather"],
    )
    async with ClaudeSDKClient(options=options) as client:
        await client.query("What's the weather in Paris (48.85, 2.35)?")
        async for msg in client.receive_response():
            print(msg)

asyncio.run(main())
```

```typescript
// TypeScript
import { query, tool, createSdkMcpServer } from "@anthropic-ai/claude-agent-sdk";
import { z } from "zod";

const customServer = createSdkMcpServer({
  name: "weather-tools",
  version: "1.0.0",
  tools: [
    tool("get_weather", "Get temperature for coordinates",
      { latitude: z.number(), longitude: z.number() },
      async (args) => {
        const res = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${args.latitude}&longitude=${args.longitude}&current=temperature_2m`);
        const data = await res.json();
        return { content: [{ type: "text", text: `Temp: ${data.current.temperature_2m}°C` }] };
      }
    )
  ]
});

// Important: use async generator for prompt when using SDK MCP servers
async function* messages() {
  yield { type: "user" as const, message: { role: "user" as const, content: "Weather in Paris (48.85, 2.35)?" } };
}

for await (const message of query({
  prompt: messages(),
  options: {
    mcpServers: { "weather-tools": customServer },
    allowedTools: ["mcp__weather-tools__get_weather"]
  }
})) {
  if (message.type === "result") console.log(message.result);
}
```

**Important:** Custom MCP tools require streaming/async generator input in TypeScript.

For complex schema patterns, error handling, and database/API gateway examples: see [references/custom-tools.md](references/custom-tools.md)

---

## Skills & Plugins

Skills are reusable capability packages (`SKILL.md` files) that Claude loads on-demand based on context. The SDK can load skills from the filesystem and invoke them via the `Skill` built-in tool.

### Loading Skills from Filesystem

By default, the SDK does **not** load any filesystem settings (including skills). You must explicitly configure `setting_sources` to enable skill discovery.

```python
# Python — enable skills from user and project directories
from claude_agent_sdk import query, ClaudeAgentOptions

options = ClaudeAgentOptions(
    cwd="/path/to/project",                    # Project with .claude/skills/
    setting_sources=["user", "project"],       # Load skills from filesystem
    allowed_tools=["Skill", "Read", "Write", "Bash"],  # Enable Skill tool
)

async for message in query(prompt="Help me process this PDF document", options=options):
    print(message)
```

```typescript
// TypeScript — enable skills from user and project directories
for await (const message of query({
  prompt: "Help me process this PDF document",
  options: {
    cwd: "/path/to/project",                   // Project with .claude/skills/
    settingSources: ["user", "project"],        // Load skills from filesystem
    allowedTools: ["Skill", "Read", "Write", "Bash"]  // Enable Skill tool
  }
})) {
  console.log(message);
}
```

### How Skills Work in the SDK

1. **Filesystem artifacts**: Skills are `SKILL.md` files in `.claude/skills/` directories
2. **Auto-discovered**: Skill metadata (name + description) is loaded at startup
3. **Model-invoked**: Claude autonomously decides when to activate a skill based on context
4. **On-demand loading**: Full skill content is loaded only when triggered (saves context)

### Skill Discovery Locations

| `setting_sources` value | Skills loaded from |
|-------------------------|-------------------|
| `"user"` | `~/.claude/skills/` |
| `"project"` | `.claude/skills/` in `cwd` |
| `"local"` | `.claude/settings.local.json` |

### Discovering Available Skills

```python
# List all skills available to the agent
options = ClaudeAgentOptions(
    setting_sources=["user", "project"],
    allowed_tools=["Skill"],
)

async for message in query(prompt="What Skills are available?", options=options):
    print(message)
```

### Loading Plugins Programmatically

Plugins provide skills, slash commands, and agents from local directories — without requiring them to be in `.claude/skills/`.

```python
# Python — load plugins from local paths
async for message in query(
    prompt="Hello",
    options={
        "plugins": [
            {"type": "local", "path": "./my-plugin"},
            {"type": "local", "path": "/absolute/path/to/another-plugin"},
        ]
    },
):
    print(message)
```

```typescript
// TypeScript — load plugins from local paths
for await (const message of query({
  prompt: "Hello",
  options: {
    plugins: [
      { type: "local", path: "./my-plugin" },
      { type: "local", path: "/absolute/path/to/another-plugin" }
    ]
  }
})) {
  console.log(message);
}
```

**Key differences between Skills and Plugins:**
- Skills must be filesystem artifacts (`SKILL.md` files) — no programmatic registration API
- Plugins load from any local path via the `plugins` array
- Both require `"Skill"` in `allowed_tools` to be invokable
- Programmatic options (`agents`, `allowed_tools`) always override filesystem settings

---

## Permissions & User Input

### Permission Modes

| Mode | Behavior | Best for |
|------|----------|---------|
| `"default"` | No auto-approvals; uses `canUseTool` callback | Interactive apps |
| `"acceptEdits"` | Auto-approves file edits + mkdir/rm/mv/cp | Trusted dev workflows |
| `"bypassPermissions"` | All tools run without prompts | CI/CD, automation |
| `"plan"` | No tool execution; Claude plans only | Pre-approval review |
| `"dontAsk"` | Auto-approve all tools without prompting | Fully autonomous agents |

```python
# Dynamic permission mode change mid-session
q = query(prompt="...", options=ClaudeAgentOptions(permission_mode="default"))
await q.set_permission_mode("acceptEdits")  # Switch after review
async for message in q: ...
```

### canUseTool Callback

Handle interactive tool approvals and `AskUserQuestion` responses:

```python
# Python
from claude_agent_sdk.types import PermissionResultAllow, PermissionResultDeny

async def can_use_tool(tool_name: str, input_data: dict, context):
    if tool_name == "AskUserQuestion":
        # Claude is asking the user a question
        answers = {}
        for q in input_data.get("questions", []):
            print(f"\n{q['question']}")
            for i, opt in enumerate(q["options"]):
                print(f"  {i+1}. {opt['label']} — {opt['description']}")
            choice = input("Your choice: ")
            answers[q["question"]] = q["options"][int(choice)-1]["label"]
        return PermissionResultAllow(updated_input={"questions": input_data["questions"], "answers": answers})

    # For other tools
    print(f"Claude wants to use {tool_name}: {input_data}")
    response = input("Allow? (y/n): ")
    if response.lower() == "y":
        return PermissionResultAllow(updated_input=input_data)
    return PermissionResultDeny(message="User denied")

# NOTE: Python requires streaming input + dummy PreToolUse hook for canUseTool to work
async def dummy_hook(input_data, tool_use_id, context):
    return {"continue_": True}

async def prompt_stream():
    yield {"type": "user", "message": {"role": "user", "content": "Your task here"}}

options = ClaudeAgentOptions(
    can_use_tool=can_use_tool,
    hooks={"PreToolUse": [HookMatcher(matcher=None, hooks=[dummy_hook])]},
)
```

```typescript
// TypeScript
const options = {
  canUseTool: async (toolName: string, input: any) => {
    if (toolName === "AskUserQuestion") {
      const answers: Record<string, string> = {};
      for (const q of input.questions) {
        console.log(`\n${q.question}`);
        q.options.forEach((opt: any, i: number) => console.log(`  ${i+1}. ${opt.label}`));
        const choice = parseInt(await prompt("Choice: ")) - 1;
        answers[q.question] = q.options[choice].label;
      }
      return { behavior: "allow", updatedInput: { questions: input.questions, answers } };
    }
    console.log(`Tool: ${toolName}`, input);
    const approved = (await prompt("Allow? (y/n): ")).toLowerCase() === "y";
    return approved
      ? { behavior: "allow", updatedInput: input }
      : { behavior: "deny", message: "User denied" };
  }
};
```

### Permission Updates via canUseTool (TypeScript)

The `canUseTool` callback can return `updatedPermissions` to dynamically modify permission rules:

```typescript
const options = {
  canUseTool: async (toolName: string, input: any) => {
    return {
      behavior: "allow",
      updatedInput: input,
      updatedPermissions: {
        // Add new permission rules
        addRules: [{ tool: "Bash(*)", permission: "allow" }],
        // Replace all rules
        replaceRules: [{ tool: "Read(*)", permission: "allow" }],
        // Remove specific rules
        removeRules: [{ tool: "Write(/tmp/*)" }],
        // Change permission mode
        setMode: "acceptEdits",
        // Add/remove accessible directories
        addDirectories: ["/new/path"],
        removeDirectories: ["/old/path"],
      }
    };
  }
};
```

Permission update destinations: `"userSettings"`, `"projectSettings"`, `"localSettings"`, `"session"`, `"cliArg"` (TS).

For declarative permission rules (settings.json), plan mode patterns, and input modification: see [references/permissions.md](references/permissions.md)

---

## System Prompts & CLAUDE.md

### System Prompt Types

The `system_prompt` option accepts either a plain string or a **preset object**:

```python
# Plain string — replaces the default system prompt entirely
options = ClaudeAgentOptions(system_prompt="You are a security auditor.")

# Preset — uses Claude Code's full system prompt + your additions
options = ClaudeAgentOptions(
    system_prompt={
        "type": "preset",
        "preset": "claude_code",
        "append": "Always include detailed docstrings and type hints.",
    }
)
```

```typescript
// TypeScript preset
const options = {
  systemPrompt: {
    type: "preset",
    preset: "claude_code",
    append: "Always include detailed docstrings and type hints."
  }
};
```

The preset approach preserves all built-in Claude Code functionality (tool usage, safety, formatting) while adding domain-specific instructions. Use `append` to add requirements without losing defaults.

### CLAUDE.md Files

CLAUDE.md files provide persistent project-level instructions. The SDK loads them only when `setting_sources` includes `"project"`:

```python
# Required: setting_sources=["project"] to load CLAUDE.md
options = ClaudeAgentOptions(
    system_prompt={"type": "preset", "preset": "claude_code"},
    setting_sources=["project"],  # Loads CLAUDE.md from cwd
)
```

CLAUDE.md is a markdown file in the project root with guidelines, code style, commands, etc. — Claude follows these instructions automatically.

### Output Styles

Output styles are reusable prompt profiles stored in `.claude/output-styles/`:

```python
# Output styles are auto-loaded when setting_sources includes "user" or "project"
options = ClaudeAgentOptions(
    setting_sources=["user", "project"],  # Loads output styles
)
```

Create a style file at `~/.claude/output-styles/code-reviewer.md`:
```markdown
---
name: Code Reviewer
description: Thorough code review assistant
---

You are an expert code reviewer. For every submission:
1. Check for bugs and security issues
2. Evaluate performance
3. Suggest improvements
```

### Settings Precedence

When multiple sources are loaded, settings merge (highest to lowest priority):
1. Programmatic options (`agents`, `allowed_tools`) — always win
2. Local settings (`.claude/settings.local.json`)
3. Project settings (`.claude/settings.json`)
4. User settings (`~/.claude/settings.json`)

---

## Cost Tracking

The SDK provides per-message and cumulative cost/usage information.

### Usage Fields

| Field | Type | Description |
|-------|------|-------------|
| `input_tokens` | `number` | Base input tokens processed |
| `output_tokens` | `number` | Tokens generated in response |
| `cache_creation_input_tokens` | `number` | Tokens used to create cache |
| `cache_read_input_tokens` | `number` | Tokens read from cache |
| `total_cost_usd` | `float` | Total cost (only on `ResultMessage`) |

### Tracking Costs

```python
# Python — cost tracking
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, ResultMessage

async for message in query(prompt="Refactor auth.py", options=ClaudeAgentOptions()):
    if isinstance(message, AssistantMessage) and hasattr(message, "usage"):
        print(f"Step tokens: in={message.usage.get('input_tokens')}, out={message.usage.get('output_tokens')}")
    elif isinstance(message, ResultMessage):
        print(f"Total: {message.num_turns} turns, {message.duration_ms}ms")
        if message.total_cost_usd:
            print(f"Cost: ${message.total_cost_usd:.4f}")
```

```typescript
// TypeScript — cost tracking
for await (const message of query({ prompt: "Refactor auth.py" })) {
  if (message.type === "assistant" && message.message.usage) {
    console.log("Step tokens:", message.message.usage);
  }
  if (message.type === "result") {
    console.log(`Total: ${message.num_turns} turns, ${message.duration_ms}ms`);
    console.log(`Cost: $${message.usage?.total_cost_usd}`);
  }
}
```

### Subagent Costs

The `Task` tool output includes usage stats for each subagent:
```python
# Task tool output
{
    "result": str,
    "usage": {"input_tokens": int, "output_tokens": int, ...},
    "total_cost_usd": float,
    "duration_ms": int,
}
```

---

## Structured Outputs

Force Claude to return structured JSON matching a schema. The result appears in `ResultMessage.structured_output`.

```python
# Python — JSON Schema
options = ClaudeAgentOptions(
    output_format={
        "type": "json_schema",
        "schema": {
            "type": "object",
            "properties": {
                "summary": {"type": "string"},
                "issues": {"type": "array", "items": {"type": "object", "properties": {
                    "severity": {"type": "string", "enum": ["low", "medium", "high", "critical"]},
                    "description": {"type": "string"},
                    "file": {"type": "string"},
                    "line": {"type": "integer"},
                }, "required": ["severity", "description"]}},
            },
            "required": ["summary", "issues"],
        }
    },
    allowed_tools=["Read", "Glob", "Grep"],
)

async for message in query(prompt="Analyze auth.py for security issues", options=options):
    if hasattr(message, "structured_output") and message.structured_output:
        import json
        result = json.loads(message.structured_output)
        for issue in result["issues"]:
            print(f"[{issue['severity']}] {issue['description']}")
```

```typescript
// TypeScript — Zod schema (also supports raw JSON Schema)
import { z } from "zod";

const options = {
  outputFormat: {
    type: "json_schema" as const,
    schema: z.object({
      summary: z.string(),
      issues: z.array(z.object({
        severity: z.enum(["low", "medium", "high", "critical"]),
        description: z.string(),
        file: z.string().optional(),
        line: z.number().optional(),
      })),
    })
  },
  allowedTools: ["Read", "Glob", "Grep"]
};

for await (const msg of query({ prompt: "Analyze auth.py", options })) {
  if (msg.type === "result" && msg.structured_output) {
    const result = JSON.parse(msg.structured_output);
    console.log(result.issues);
  }
}
```

If Claude can't match the schema after retries, the result subtype is `"error_max_structured_output_retries"`.

---

## Thinking & Effort

Control Claude's extended thinking behavior. The `thinking` option replaces the deprecated `max_thinking_tokens`.

### Thinking Config

```python
# Adaptive (default) — Claude decides when to think
options = ClaudeAgentOptions(thinking={"type": "adaptive"})

# Fixed budget — always think with N tokens
options = ClaudeAgentOptions(thinking={"type": "enabled", "budget_tokens": 10000})

# Disabled — no extended thinking
options = ClaudeAgentOptions(thinking={"type": "disabled"})
```

```typescript
const options = { thinking: { type: "adaptive" as const } };
const options2 = { thinking: { type: "enabled" as const, budget_tokens: 10000 } };
const options3 = { thinking: { type: "disabled" as const } };
```

### Effort Levels

A simpler alternative to thinking config — controls thinking depth:

```python
options = ClaudeAgentOptions(effort="high")   # "low", "medium", "high", "max"
```

```typescript
const options = { effort: "high" as const };  // "low" | "medium" | "high" | "max"
```

### Betas

Enable experimental SDK features:

```python
# 1M token context window (compatible with Opus 4.6, Sonnet 4.5, Sonnet 4)
options = ClaudeAgentOptions(betas=["context-1m-2025-08-07"])
```

---

## File Checkpointing

File checkpointing tracks file changes and allows rewinding to a previous state — useful for undoing agent modifications.

### Setup

```python
import os
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, UserMessage, ResultMessage

options = ClaudeAgentOptions(
    enable_file_checkpointing=True,
    permission_mode="acceptEdits",
    extra_args={"replay-user-messages": None},  # Required for checkpoint UUIDs
    env={**os.environ, "CLAUDE_CODE_ENABLE_SDK_FILE_CHECKPOINTING": "1"},
)
```

```typescript
const opts = {
  enableFileCheckpointing: true,
  permissionMode: "acceptEdits" as const,
  extraArgs: { "replay-user-messages": null },
  env: { ...process.env, CLAUDE_CODE_ENABLE_SDK_FILE_CHECKPOINTING: "1" }
};
```

### Capture Checkpoint and Rewind

```python
checkpoint_id = None
session_id = None

async with ClaudeSDKClient(options) as client:
    await client.query("Refactor the authentication module")
    async for message in client.receive_response():
        # Capture first user message UUID as restore point
        if isinstance(message, UserMessage) and message.uuid and not checkpoint_id:
            checkpoint_id = message.uuid
        if isinstance(message, ResultMessage):
            session_id = message.session_id

# Later — rewind all file changes
if checkpoint_id and session_id:
    async with ClaudeSDKClient(
        ClaudeAgentOptions(enable_file_checkpointing=True, resume=session_id)
    ) as client:
        await client.query("")  # Empty prompt opens connection
        async for message in client.receive_response():
            await client.rewind_files(checkpoint_id)
            break
```

```typescript
// TypeScript — rewind
const rewindQuery = query({
  prompt: "",
  options: { ...opts, resume: sessionId }
});
for await (const msg of rewindQuery) {
  await rewindQuery.rewindFiles(checkpointId);
  break;
}
```

---

## Interrupt & Stop Reasons

### Interrupting a Running Task

Use `client.interrupt()` to stop a long-running task mid-execution:

```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
import asyncio

async def main():
    options = ClaudeAgentOptions(allowed_tools=["Bash"], permission_mode="acceptEdits")

    async with ClaudeSDKClient(options=options) as client:
        await client.query("Count from 1 to 100 slowly")
        await asyncio.sleep(2)

        await client.interrupt()  # Stop current task
        print("Task interrupted!")

        await client.query("Just say hello instead")  # Send new command
        async for message in client.receive_response():
            pass

asyncio.run(main())
```

### Stop Reasons

The `ResultMessage` includes a `stop_reason` field indicating why the agent stopped:

| `subtype` | `stop_reason` | Meaning |
|-----------|---------------|---------|
| `"success"` | `"end_turn"` | Agent completed normally |
| `"error_during_execution"` | varies | An error occurred |
| `"error_max_turns"` | `"end_turn"` or `"tool_use"` | Hit `max_turns` limit |
| `"error_max_budget_usd"` | varies | Hit `max_budget_usd` spend cap |
| `"error_max_structured_output_retries"` | varies | Failed to match `output_format` schema |

```python
from claude_agent_sdk import ResultMessage

async for message in query(prompt="...", options=ClaudeAgentOptions(max_turns=3)):
    if isinstance(message, ResultMessage):
        if message.subtype == "error_max_turns":
            print(f"Hit turn limit. Last stop reason: {message.stop_reason}")
```

---

## ClaudeSDKClient (Multi-Turn Client)

`ClaudeSDKClient` provides a persistent connection for multi-turn conversations, dynamic control, and advanced operations like interrupt and rewind.

### Constructor

```python
# Python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions

client = ClaudeSDKClient(
    options=ClaudeAgentOptions(...),
    transport=None,  # Optional custom Transport for IPC
)
```

```typescript
// TypeScript
import { ClaudeSDKClient } from "@anthropic-ai/claude-agent-sdk";

const client = new ClaudeSDKClient({
  options: { ... },
  transport: undefined  // Optional custom Transport
});
```

The optional `transport` parameter allows a custom IPC transport (e.g., for embedding the SDK in a larger system). When omitted, the default process-based transport is used.

### Method Reference

| Method | Description |
|--------|-------------|
| `connect(prompt?)` | Initialize connection (optionally with first prompt) |
| `query(prompt, session_id?)` | Send a prompt (starts or resumes a session) |
| `receive_messages()` | Async iterator of all messages from current query |
| `receive_response()` | Async iterator (alias for receive_messages) |
| `interrupt()` | Cancel the current running task |
| `set_permission_mode(mode)` | Change permission mode dynamically |
| `set_model(model)` | Change model dynamically (`"sonnet"`, `"opus"`, `"haiku"`, or `None` for default) |
| `get_mcp_status()` | Get status of all connected MCP servers |
| `get_server_info()` | Get agent server metadata |
| `rewind_files(user_message_id)` | Undo file changes to a checkpoint (requires `enable_file_checkpointing`) |
| `disconnect()` | Close the connection and clean up |

### Usage with Context Manager

```python
# Python — recommended: use as async context manager
async with ClaudeSDKClient(options=options) as client:
    await client.query("Analyze this codebase")
    async for message in client.receive_response():
        print(message)

    # Dynamic control mid-session
    await client.set_model("haiku")       # Switch to faster model
    await client.set_permission_mode("acceptEdits")  # Relax permissions

    await client.query("Now fix the top 3 issues")
    async for message in client.receive_response():
        print(message)

    # Inspect MCP server health
    status = await client.get_mcp_status()
    print(status)  # {"server_name": {"status": "connected", ...}, ...}

    # Get server info
    info = await client.get_server_info()
    print(info)  # {"version": "...", ...}
```

```typescript
// TypeScript
const client = new ClaudeSDKClient({ options });
await client.connect("Analyze this codebase");

for await (const msg of client.receiveMessages()) {
  console.log(msg);
}

// Dynamic control
await client.setModel("haiku");
await client.setPermissionMode("acceptEdits");

await client.query("Now fix the top 3 issues");
for await (const msg of client.receiveMessages()) {
  console.log(msg);
}

await client.disconnect();
```

### Dynamic Permission Mode on Query

You can also change the permission mode on the `query()` async generator directly:

```python
q = query(prompt="...", options=ClaudeAgentOptions(permission_mode="default"))
await q.set_permission_mode("acceptEdits")  # Change before iterating
async for message in q:
    print(message)
```

```typescript
const q = query({ prompt: "...", options: { permissionMode: "default" } });
await q.setPermissionMode("acceptEdits");
for await (const msg of q) {
  console.log(msg);
}
```

---

## Sandbox & Secure Deployment

### Sandbox Settings

Run the agent in a sandboxed environment with restricted capabilities:

```python
from claude_agent_sdk import query, ClaudeAgentOptions

options = ClaudeAgentOptions(
    sandbox={
        "enabled": True,
        "autoAllowBashIfSandboxed": True,
        "network": {
            "allowLocalBinding": True,
            "allowedDomains": ["api.example.com"],
            "allowManagedDomainsOnly": False,
        },
        "filesystem": {
            "allowWrite": ["/workspace"],
            "denyWrite": ["/etc", "/usr"],
            "denyRead": ["/secrets"],
        },
    }
)

async for message in query(prompt="Build and test my project", options=options):
    print(message)
```

```typescript
const options = {
  sandbox: {
    enabled: true,
    autoAllowBashIfSandboxed: true,
    excludedCommands: ["rm -rf /"],           // Block specific commands
    network: {
      allowLocalBinding: true,
      allowedDomains: ["api.example.com"],
      allowUnixSockets: false,
    },
    filesystem: {
      allowWrite: ["/workspace"],
      denyWrite: ["/etc", "/usr"],
      denyRead: ["/secrets"],
    },
  }
};
```

**Sandbox settings:**
| Field | Description |
|---|---|
| `enabled` | Enable sandbox |
| `autoAllowBashIfSandboxed` | Auto-approve Bash when sandboxed |
| `excludedCommands` | Block specific bash commands |
| `network.allowLocalBinding` | Allow binding local ports |
| `network.allowedDomains` | Whitelist of allowed domains |
| `network.allowManagedDomainsOnly` | Only allow managed domains |
| `network.allowUnixSockets` / `allowAllUnixSockets` | Unix socket access |
| `filesystem.allowWrite` | Writable paths |
| `filesystem.denyWrite` | Read-only paths |
| `filesystem.denyRead` | Inaccessible paths |

### Docker Security Hardening

For production deployments, run agents in hardened containers:

```bash
docker run \
  --cap-drop ALL \
  --security-opt no-new-privileges \
  --read-only \
  --tmpfs /tmp:rw,noexec,nosuid,size=100m \
  --tmpfs /home/agent:rw,noexec,nosuid,size=500m \
  --network none \
  --memory 2g --cpus 2 --pids-limit 100 \
  --user 1000:1000 \
  -v /path/to/code:/workspace:ro \
  agent-image
```

Key security measures:
- `--cap-drop ALL` — remove all Linux capabilities
- `--read-only` — immutable root filesystem
- `--network none` — no network access (use Unix socket for API)
- `--user 1000:1000` — non-root execution
- Resource limits (`--memory`, `--cpus`, `--pids-limit`)

---

## SDK Internal Architecture

The SDK **never calls the Anthropic API directly**. It spawns the `claude` CLI as a child subprocess and communicates via **stdin/stdout using newline-delimited JSON (NDJSON)**:

```
┌─────────────────────┐    stdin (NDJSON)          ┌──────────────────┐
│   Your Application  │ ──────────────────────────> │                  │
│   (Python / TS)     │                             │  claude CLI      │
│                     │ <────────────────────────── │  (Node.js)       │
│   SDK (Transport)   │    stdout (NDJSON)          │                  │
│                     │                             │  Calls Anthropic │
│                     │    stderr (debug/logs)      │  API internally  │
└─────────────────────┘ <────────────────────────── └──────────────────┘
```

### Process Spawning

**Python** — resolves the `claude` binary in order: bundled CLI (`_bundled/`), `shutil.which("claude")`, common locations (`~/.npm-global/bin/`, `/usr/local/bin/`, etc.). Spawns via `anyio.open_process()`.

**TypeScript** — resolves bundled `cli.js` (in the npm package) or `pathToClaudeCodeExecutable`. If the path is a JS file, prepends `node`/`bun` as runtime. Spawns via `child_process.spawn()`.

Both SDKs always pass these base CLI flags:
```
["--output-format", "stream-json", "--verbose", "--input-format", "stream-json"]
```

### Environment Inheritance

Both SDKs **inherit all environment variables** from the parent process and add SDK-specific ones:

```python
# Python (subprocess_cli.py)
process_env = {
    **os.environ,                           # Inherit ALL system env vars
    **self._options.env,                    # User-provided overrides
    "CLAUDE_CODE_ENTRYPOINT": "sdk-py",
    "CLAUDE_AGENT_SDK_VERSION": __version__,
}
```

```typescript
// TypeScript
let env = { ...process.env };              // Inherit ALL system env vars
// User env vars spread via options.env
env.CLAUDE_CODE_ENTRYPOINT = "sdk-ts";
env.CLAUDE_AGENT_SDK_VERSION = "0.2.66";
```

This means the `claude` child process receives **every auth-related variable** already set in your shell (`ANTHROPIC_API_KEY`, `CLAUDE_CODE_OAUTH_TOKEN`, AWS/GCP/Azure credentials, etc.).

### IPC Protocol (stream-json)

The SDK and CLI communicate using **bidirectional NDJSON** (one JSON object per line):

**Message types (CLI → SDK via stdout):**

| Type | Purpose |
|---|---|
| `{"type": "system", "subtype": "init"}` | Session initialization (returns `session_id`) |
| `{"type": "assistant", "message": {...}}` | Claude's responses |
| `{"type": "user", "message": {...}}` | Tool results |
| `{"type": "result", "subtype": "success"}` | Final result with cost/usage |
| `{"type": "control_request", ...}` | Permission/hook/MCP requests from CLI |

**Control messages (SDK → CLI via stdin):**

| Type | Purpose |
|---|---|
| `{"type": "user", "message": {...}}` | User prompts |
| `{"type": "control_request", "request": {"subtype": "initialize"}}` | Handshake (register hooks, agents) |
| `{"type": "control_request", "request": {"subtype": "interrupt"}}` | Interrupt processing |
| `{"type": "control_response", ...}` | Responses to permission/hook/MCP requests |

**Initialize handshake** (first message after spawn):
```json
{"type": "control_request", "request_id": "req_1", "request": {
  "subtype": "initialize",
  "hooks": {"PreToolUse": [{"matcher": "Edit", "hookCallbackIds": ["h0"]}]},
  "agents": {"reviewer": {"prompt": "Review code", "tools": ["Read"]}}
}}
```

**Permission request** (CLI asks SDK to approve a tool):
```json
{"type": "control_request", "request_id": "req_42", "request": {
  "subtype": "can_use_tool", "tool_name": "Bash",
  "input": {"command": "rm -rf /tmp/test"}
}}
```

**Permission response** (SDK approves/denies):
```json
{"type": "control_response", "response": {
  "request_id": "req_42", "subtype": "success",
  "response": {"behavior": "allow"}
}}
```

**Other control request subtypes (SDK → CLI):**
`set_permission_mode`, `set_model`, `rewind_files`, `mcp_status`, `mcp_reconnect`, `mcp_toggle`, `mcp_set_servers` (TS), `stop_task`

---

## Authentication & Hosting

### API Providers

```bash
# Anthropic (default)
export ANTHROPIC_API_KEY=your-key

# Amazon Bedrock
export CLAUDE_CODE_USE_BEDROCK=1
# Configure AWS credentials (aws configure or env vars)

# Google Vertex AI
export CLAUDE_CODE_USE_VERTEX=1
# Configure Google Cloud credentials

# Microsoft Azure AI Foundry
export CLAUDE_CODE_USE_FOUNDRY=1
# Configure Azure credentials
```

### Authentication Resolution Order

The `claude` child process resolves authentication in this priority:

| Priority | Variable | Billing |
|---|---|---|
| 1 | `ANTHROPIC_API_KEY` | Pay-per-use (API credits) |
| 2 | `CLAUDE_CODE_OAUTH_TOKEN` | Subscription quota (Pro/Max/Team) |
| 3 | `CLAUDE_CODE_USE_BEDROCK=1` | AWS Bedrock pricing |
| 4 | `CLAUDE_CODE_USE_VERTEX=1` | Google Vertex pricing |
| 5 | `CLAUDE_CODE_USE_FOUNDRY=1` | Azure AI Foundry pricing |

### SDK vs CLI Authentication (Official)

Anthropic's official position: the SDK is designed for API key authentication. OAuth/subscription login is **not officially supported** for the Agent SDK.

| | Interactive CLI (`claude`) | Agent SDK (official) |
|---|---|---|
| API key | ✅ | ✅ |
| OAuth / subscription login | ✅ | ❌ Not officially supported |
| Bedrock / Vertex / Foundry | ✅ | ✅ |

### Using Pro/Max Subscription with the SDK

Since the SDK spawns the `claude` CLI as a child process and **inherits all environment variables** (see [SDK Internal Architecture](#sdk-internal-architecture)), if `CLAUDE_CODE_OAUTH_TOKEN` is set in your shell and `ANTHROPIC_API_KEY` is **not** set, the child process will use your subscription quota.

> **Warning:** This is **not officially supported** by Anthropic. It works due to the SDK's process-spawning architecture but may break in future updates. Anthropic's ToS prohibit using OAuth tokens in third-party products. Use for personal/local development only.

**Step 1: Obtain your OAuth token**
```bash
# Login to Claude (if not already authenticated)
claude login

# Or explicitly set up the token
claude setup-token
# Opens browser → authenticate → token is stored
```

**Step 2: Ensure no API key overrides it**
```bash
# IMPORTANT: ANTHROPIC_API_KEY takes priority over OAuth token
# Make sure it's NOT set, or the SDK will use API billing instead
unset ANTHROPIC_API_KEY

# Verify OAuth token is available
echo $CLAUDE_CODE_OAUTH_TOKEN
```

**Step 3: Use the SDK normally**
```python
import os
from claude_agent_sdk import query, ClaudeAgentOptions

# Option A: OAuth token already in environment (from `claude login`)
# The SDK inherits it automatically — nothing special needed
async for msg in query(prompt="Hello", options=ClaudeAgentOptions()):
    print(msg)
```

```python
# Option B: Explicitly pass the OAuth token (useful when ANTHROPIC_API_KEY is also set)
options = ClaudeAgentOptions(
    env={
        "CLAUDE_CODE_OAUTH_TOKEN": os.environ["CLAUDE_CODE_OAUTH_TOKEN"],
        # Omit ANTHROPIC_API_KEY to force OAuth usage
    },
)
async for msg in query(prompt="Hello", options=options):
    print(msg)
```

```python
# Option C: Remove API key at runtime to force OAuth
import os
os.environ.pop("ANTHROPIC_API_KEY", None)  # Remove if present

async for msg in query(prompt="Hello", options=ClaudeAgentOptions()):
    print(msg)
```

```typescript
// TypeScript — same principle
import { query } from "@anthropic-ai/claude-agent-sdk";

// Ensure ANTHROPIC_API_KEY is not set; CLAUDE_CODE_OAUTH_TOKEN will be inherited
delete process.env.ANTHROPIC_API_KEY;

for await (const msg of query({ prompt: "Hello" })) {
  console.log(msg);
}
```

**Why it works:** The SDK's `SubprocessCLITransport` (Python) / `ProcessTransport` (TypeScript) builds the child environment as `{...os.environ, ...options.env}`. The `claude` process receives `CLAUDE_CODE_OAUTH_TOKEN` and, with no `ANTHROPIC_API_KEY` present, authenticates via your subscription.

### Recommended Authentication for Production

| Use Case | Recommended Auth |
|---|---|
| Personal/local development | API key or OAuth token (see above) |
| CI/CD pipelines | `ANTHROPIC_API_KEY` or Bedrock/Vertex |
| Commercial products | `ANTHROPIC_API_KEY` (pay-per-use) |
| Enterprise / cloud-native | Bedrock, Vertex, or Foundry |

**Dynamic API key rotation** (for vaults/secret managers):
```python
# In .claude/settings.json or via setting_sources
# "apiKeyHelper": "my-script-that-returns-api-key"
# CLAUDE_CODE_API_KEY_HELPER_TTL_MS controls refresh interval
```

### Docker Deployment

```dockerfile
FROM node:18-slim
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
ENV ANTHROPIC_API_KEY=""
CMD ["node", "agent.js"]
```

### Filesystem Configuration

Load Claude Code settings (CLAUDE.md, slash commands, skills, agents from `.claude/agents/`):
```python
options = ClaudeAgentOptions(setting_sources=["project"])
```

Available setting sources: `"project"` (`.claude/`), `"user"` (~/.claude/), `"mcpServers"`

---

## Session Discovery

TypeScript provides functions to list past sessions and read their transcripts:

```typescript
import { listSessions, getSessionMessages } from "@anthropic-ai/claude-agent-sdk";

// List past sessions with metadata
const sessions = await listSessions({ dir: "/path/to/project", limit: 10 });
for (const session of sessions) {
  console.log(`${session.sessionId}: ${session.summary}`);
  console.log(`  Branch: ${session.gitBranch}, Last modified: ${session.lastModified}`);
}

// Read session transcript with pagination
const messages = await getSessionMessages(sessions[0].sessionId, {
  limit: 50,
  offset: 0,
});
for (const msg of messages) {
  console.log(msg);
}
```

**`SDKSessionInfo` fields:** `sessionId`, `summary`, `lastModified`, `fileSize`, `customTitle?`, `firstPrompt?`, `gitBranch?`, `cwd?`

---

## TypeScript V2 Preview

The V2 API provides a simpler session-based interface (unstable — may change):

```typescript
import {
  unstable_v2_createSession,
  unstable_v2_resumeSession,
  unstable_v2_prompt,
} from "@anthropic-ai/claude-agent-sdk";

// Create a session
const session = await unstable_v2_createSession({
  allowedTools: ["Read", "Glob"],
  permissionMode: "bypassPermissions",
});

// Send messages and stream responses
session.send("What files are in this directory?");
for await (const msg of session.stream()) {
  if (msg.type === "result") console.log(msg.result);
}

// Resume later
const resumed = await unstable_v2_resumeSession(session.sessionId, {
  allowedTools: ["Read", "Glob"],
});
resumed.send("Now count the TypeScript files");
for await (const msg of resumed.stream()) {
  if (msg.type === "result") console.log(msg.result);
}

// Close (also supports `await using` for auto-cleanup)
await session.close();

// One-shot convenience function (returns ResultMessage directly)
const result = await unstable_v2_prompt("Hello!", {
  allowedTools: ["Read"],
  permissionMode: "bypassPermissions",
});
console.log(result.result);
```

---

## Query Object Methods (TS)

The TypeScript `Query` object (returned by `query()`) exposes additional methods beyond streaming:

| Method | Returns | Description |
|--------|---------|-------------|
| `interrupt()` | `void` | Cancel the current running task |
| `rewindFiles(userMessageId, opts?)` | `RewindFilesResult` | Restore files to checkpoint (`canRewind`, `filesChanged`, `insertions`, `deletions`) |
| `setPermissionMode(mode)` | `void` | Change permission mode dynamically |
| `setModel(model?)` | `void` | Change model (`null` to reset to default) |
| `initializationResult()` | `SDKControlInitializeResponse` | Returns init data: `commands`, `agents`, `output_style`, `available_output_styles`, `models`, `account` |
| `supportedCommands()` | `SlashCommand[]` | List of available slash commands (`name`, `description`, `argumentHint`) |
| `supportedModels()` | `ModelInfo[]` | Available models with `displayName`, `supportsEffort`, `supportedEffortLevels`, `supportsAdaptiveThinking` |
| `supportedAgents()` | `AgentInfo[]` | Available agents with `name`, `description`, `model?` |
| `accountInfo()` | `AccountInfo` | Account details: `email?`, `organization?`, `subscriptionType?`, `apiKeySource?` |
| `mcpServerStatus()` | `McpServerStatus[]` | Status of all MCP servers (name, status, tools, errors) |
| `setMcpServers(servers)` | `McpSetServersResult` | Dynamically replace MCP servers (`added`, `removed`, `errors`) |
| `reconnectMcpServer(name)` | `void` | Reconnect a failed MCP server |
| `toggleMcpServer(name, enabled)` | `void` | Enable/disable an MCP server |
| `stopTask(taskId)` | `void` | Stop a running background task |
| `streamInput(stream)` | `void` | Stream input messages for multi-turn conversations |
| `close()` | `void` | Forcefully terminate and clean up |

**MCP Server Status values:** `"connected"` | `"failed"` | `"needs-auth"` | `"pending"` | `"disabled"`

---

## Error Types

The SDK provides typed error classes for error handling:

### Python Errors

```python
from claude_agent_sdk import (
    ClaudeSDKError,         # Base error class
    CLIConnectionError,     # Connection to CLI failed
    CLINotFoundError,       # CLI binary not found (has cli_path attribute)
    ProcessError,           # Process failure (has exit_code, stderr attributes)
    CLIJSONDecodeError,     # JSON parse failure (has line, original_error attributes)
)

try:
    async for msg in query(prompt="...", options=options):
        pass
except CLINotFoundError as e:
    print(f"CLI not found at: {e.cli_path}")
except ProcessError as e:
    print(f"Process exited with code {e.exit_code}: {e.stderr}")
except CLIConnectionError as e:
    print(f"Connection failed: {e}")
except CLIJSONDecodeError as e:
    print(f"JSON parse error on line {e.line}: {e.original_error}")
except ClaudeSDKError as e:
    print(f"SDK error: {e}")
```

### TypeScript Errors

```typescript
import { AbortError } from "@anthropic-ai/claude-agent-sdk";

try {
  for await (const msg of query({ prompt: "...", options })) { /* ... */ }
} catch (e) {
  if (e instanceof AbortError) {
    console.log("Query was aborted");
  }
}
```

### AssistantMessage Error Types

When an `AssistantMessage` contains an error, the `error` field has a `type`:
`"authentication_failed"` | `"billing_error"` | `"rate_limit"` | `"invalid_request"` | `"server_error"` | `"unknown"`

---

## Transport & Custom Process Spawning

The SDK abstracts communication with the `claude` CLI through the Transport layer. By default, it uses a subprocess-based transport (see [SDK Internal Architecture](#sdk-internal-architecture) for the IPC protocol). You can replace or customize this.

### Default Transports

| SDK | Default Transport | Mechanism |
|---|---|---|
| Python | `SubprocessCLITransport` | `anyio.open_process()` → stdin/stdout NDJSON |
| TypeScript | `ProcessTransport` | `child_process.spawn()` → stdin/stdout NDJSON |

Both read stdout line-by-line: TypeScript uses `readline.createInterface()`, Python uses `anyio.TextReceiveStream` with a 1MB JSON buffer.

### Custom Transport (Python)

The `Transport` abstract class enables custom IPC (inter-process communication):

```python
from claude_agent_sdk import Transport

class MyTransport(Transport):
    async def connect(self): ...
    async def write(self, data: str): ...
    async def read_messages(self): ...    # Async iterator
    async def close(self): ...
    def is_ready(self) -> bool: ...
    async def end_input(self): ...

client = ClaudeSDKClient(options=options, transport=MyTransport())
```

### DirectConnectTransport (TypeScript)

Connect to a running `claude server` via WebSocket:

```typescript
import { DirectConnectTransport } from "@anthropic-ai/claude-agent-sdk";

const transport = new DirectConnectTransport("ws://localhost:8080");
const q = query({ prompt: "Hello", options, transport });
```

### Custom Process Spawning (TypeScript)

Customize how the `claude` process is launched (VMs, containers, remote machines) while keeping the SDK's NDJSON protocol handling:

```typescript
const options = {
  spawnClaudeCodeProcess: (spawnOptions) => {
    // spawnOptions: { command, args, env, cwd, signal }
    const child = spawn("docker", ["run", "--rm", "-i", "agent-image", ...spawnOptions.args], {
      env: spawnOptions.env,
      cwd: spawnOptions.cwd,
      signal: spawnOptions.signal,
    });
    return {
      stdin: child.stdin,
      stdout: child.stdout,
      stderr: child.stderr,
      exitCode: new Promise(resolve => child.on("exit", resolve)),
      kill: () => child.kill(),
    };
  }
};
```

---

## Common Patterns

### Read-Only Analysis Agent
```python
options = ClaudeAgentOptions(
    allowed_tools=["Read", "Glob", "Grep"],
    permission_mode="bypassPermissions",
    system_prompt="You are a code analyst. Never modify files.",
)
```

### CI/CD Automation Agent
```python
options = ClaudeAgentOptions(
    allowed_tools=["Read", "Edit", "Write", "Bash", "Glob", "Grep"],
    permission_mode="bypassPermissions",
    max_turns=20,
)
```

### Multi-Agent Parallel Workflow
```python
# Main agent delegates to specialists
options = ClaudeAgentOptions(
    allowed_tools=["Read", "Glob", "Grep", "Task"],
    agents={
        "security-scanner": AgentDefinition(
            description="Security vulnerability scanner",
            prompt="Find security issues. Report CVEs and OWASP violations.",
            tools=["Read", "Grep", "Glob"],
        ),
        "test-runner": AgentDefinition(
            description="Test execution and analysis specialist",
            prompt="Run tests and analyze failures.",
            tools=["Bash", "Read", "Grep"],
        ),
    },
)
```

### Audit Logging Hook
```python
async def audit_logger(input_data, tool_use_id, context):
    with open("audit.log", "a") as f:
        f.write(f"{datetime.now()}: {input_data['tool_name']} — {input_data.get('tool_input', {})}\n")
    return {}

options = ClaudeAgentOptions(
    hooks={"PostToolUse": [HookMatcher(hooks=[audit_logger])]}
)
```

### Skills-Enabled Agent
```python
# Agent that can use installed skills (PDF, XLSX, etc.)
options = ClaudeAgentOptions(
    cwd="/path/to/project",
    setting_sources=["user", "project"],  # Load skills from filesystem
    allowed_tools=["Skill", "Read", "Write", "Edit", "Bash", "Glob"],
)
```

### Todo Progress Tracking
```python
# Monitor TodoWrite tool calls to track agent progress in real-time
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage

async for message in query(prompt="Refactor the auth module", options=ClaudeAgentOptions(
    allowed_tools=["Read", "Edit", "Write", "Glob", "Grep", "TodoWrite"],
)):
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if hasattr(block, "name") and block.name == "TodoWrite":
                todos = block.input.get("todos", [])
                for todo in todos:
                    status = todo.get("status", "")
                    label = todo.get("content", "")
                    if status == "in_progress":
                        print(f"  ▶ {todo.get('activeForm', label)}")
                    elif status == "completed":
                        print(f"  ✓ {label}")
```

### Session-Based Multi-Turn Workflow
```python
session_id = None
prompts = ["Read auth.py", "Find security issues", "Fix the top 3 issues"]

for prompt_text in prompts:
    opts = ClaudeAgentOptions(
        allowed_tools=["Read", "Edit", "Glob"],
        resume=session_id,
    )
    async for message in query(prompt=prompt_text, options=opts):
        if hasattr(message, "subtype") and message.subtype == "init":
            session_id = message.data.get("session_id")
        if hasattr(message, "result"):
            print(message.result)
```

---

## Reference Files

For detailed coverage of each topic, read the appropriate reference:

- [references/hooks.md](references/hooks.md) — All hook events, input/output schemas, full examples
- [references/sessions.md](references/sessions.md) — Session lifecycle, forking, file checkpointing
- [references/subagents.md](references/subagents.md) — Subagent patterns, resumption, parallel workflows
- [references/mcp.md](references/mcp.md) — MCP transports, auth, .mcp.json, error handling
- [references/custom-tools.md](references/custom-tools.md) — In-process tools, Zod schemas, type safety
- [references/permissions.md](references/permissions.md) — Permission modes, declarative rules, canUseTool
- [references/streaming.md](references/streaming.md) — Streaming vs single-turn, input streaming, interrupts
