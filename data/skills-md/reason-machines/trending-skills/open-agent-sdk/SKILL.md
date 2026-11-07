---
name: open-agent-sdk
description: Build and deploy autonomous AI agents in-process using Open Agent SDK, an open-source alternative to @anthropic-ai/claude-agent-sdk that works anywhere without CLI dependencies.
triggers:
  - use open agent sdk
  - build an AI agent with open-agent-sdk
  - deploy claude agent without CLI
  - create autonomous agent in TypeScript
  - open-agent-sdk setup and usage
  - agent sdk for serverless or cloud
  - replace claude-agent-sdk with open source
  - run AI agent loop in process
---

# Open Agent SDK

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Open Agent SDK (`@shipany/open-agent-sdk`) is a fully open-source, in-process AI agent framework for TypeScript/Node.js. It runs the complete Claude Code agent engine directly — no local CLI subprocess required — making it suitable for cloud servers, serverless functions, Docker containers, and CI/CD pipelines. It is API-compatible with `@anthropic-ai/claude-agent-sdk`.

---

## Installation

```sh
npm install @shipany/open-agent-sdk
```

Requires Node.js 18+.

---

## Authentication & Configuration

Set the Anthropic API key as an environment variable:

```sh
export ANTHROPIC_API_KEY=your-api-key
```

Or use a third-party provider (e.g. OpenRouter):

```sh
export ANTHROPIC_BASE_URL=https://openrouter.ai/api
export ANTHROPIC_API_KEY=your-openrouter-key
export ANTHROPIC_MODEL=anthropic/claude-sonnet-4-6
```

These can also be passed programmatically via `options.env` or `apiKey`/`baseURL` in `createAgent()`.

---

## Core API

### `query({ prompt, options })` — Streaming, compatible with official SDK

Returns an `AsyncGenerator<SDKMessage>`. Drop-in replacement for `@anthropic-ai/claude-agent-sdk`.

```typescript
import { query } from '@shipany/open-agent-sdk'

for await (const message of query({
  prompt: 'Find and fix the bug in auth.ts',
  options: {
    allowedTools: ['Read', 'Edit', 'Bash'],
    permissionMode: 'acceptEdits',
  },
})) {
  if (message.type === 'assistant' && message.message?.content) {
    for (const block of message.message.content) {
      if ('text' in block) process.stdout.write(block.text)
      else if ('name' in block) console.log(`\n[Tool used: ${block.name}]`)
    }
  } else if (message.type === 'result') {
    console.log(`\nDone: ${message.subtype}`)
  }
}
```

---

### `createAgent(options)` — Reusable agent with session state

```typescript
import { createAgent } from '@shipany/open-agent-sdk'

const agent = createAgent({
  model: 'claude-sonnet-4-6',
  systemPrompt: 'You are a senior TypeScript engineer. Be concise.',
  maxTurns: 20,
})

// Blocking call
const result = await agent.prompt('Read package.json and describe the project')
console.log(result.text)
console.log(`Tokens used: ${result.usage.input_tokens + result.usage.output_tokens}`)

// Streaming call
for await (const msg of agent.query('Now add JSDoc to all exported functions')) {
  if (msg.type === 'assistant' && msg.message?.content) {
    for (const block of msg.message.content) {
      if ('text' in block) process.stdout.write(block.text)
    }
  }
}

// Session management
const history = agent.getMessages()  // full conversation history
agent.clear()                        // reset session
```

---

## Options Reference

| Option | Type | Default | Description |
|---|---|---|---|
| `model` | `string` | `claude-sonnet-4-6` | Claude model ID |
| `apiKey` | `string` | `ANTHROPIC_API_KEY` env | API key |
| `baseURL` | `string` | Anthropic API | Override for third-party providers |
| `cwd` | `string` | `process.cwd()` | Working directory for file/shell tools |
| `systemPrompt` | `string` | — | Custom system prompt prepended to agent |
| `tools` | `Tool[]` | All built-in | Override the full tool list |
| `allowedTools` | `string[]` | all | Whitelist specific tools by name |
| `permissionMode` | `string` | `bypassPermissions` | `acceptEdits`, `bypassPermissions`, `plan`, `default` |
| `maxTurns` | `number` | `100` | Maximum agentic loop iterations |
| `maxBudgetUsd` | `number` | — | Spend cap in USD |
| `mcpServers` | `object` | — | MCP server configs (stdio/SSE/HTTP) |
| `agents` | `object` | — | Named subagent definitions |
| `hooks` | `object` | — | Lifecycle hooks: `PreToolUse`, `PostToolUse`, `Stop` |
| `thinking` | `object` | — | Extended thinking config |
| `env` | `object` | — | Environment variables passed to tools |
| `resume` | `string` | — | Resume prior session by session ID |
| `canUseTool` | `function` | — | Custom permission callback `(tool, input) => boolean` |
| `includePartialMessages` | `boolean` | `false` | Emit raw streaming events |

---

## Common Patterns

### Multi-turn conversation with context

```typescript
import { createAgent } from '@shipany/open-agent-sdk'

const agent = createAgent({ model: 'claude-sonnet-4-6' })

const r1 = await agent.prompt('Read src/index.ts and explain the architecture')
console.log(r1.text)

// Context from r1 is preserved automatically
const r2 = await agent.prompt('Refactor the error handling to use a Result type')
console.log(r2.text)
```

### Restrict to read-only tools

```typescript
import { query } from '@shipany/open-agent-sdk'

for await (const message of query({
  prompt: 'Review this codebase for security issues',
  options: {
    allowedTools: ['Read', 'Glob', 'Grep'],
    // No Write, Edit, or Bash — agent cannot modify files
  },
})) {
  if (message.type === 'result') console.log('Review complete')
}
```

### Custom tools

```typescript
import { createAgent, getAllBaseTools } from '@shipany/open-agent-sdk'

const dbQueryTool = {
  name: 'QueryDatabase',
  description: 'Run a read-only SQL query and return results as JSON',
  inputJSONSchema: {
    type: 'object',
    properties: {
      sql: { type: 'string', description: 'The SQL query to run' },
    },
    required: ['sql'],
  },
  get inputSchema() {
    return { safeParse: (v: unknown) => ({ success: true, data: v }) }
  },
  async prompt() { return this.description },
  async call(input: { sql: string }) {
    // Replace with your actual DB client
    const rows = [{ id: 1, name: 'Example' }]
    return { data: JSON.stringify(rows) }
  },
  userFacingName: () => 'QueryDatabase',
  isReadOnly: () => true,
  isConcurrencySafe: () => true,
  mapToolResultToToolResultBlockParam: (data: string, id: string) => ({
    type: 'tool_result' as const,
    tool_use_id: id,
    content: data,
  }),
}

const agent = createAgent({
  tools: [...getAllBaseTools(), dbQueryTool],
})

const result = await agent.prompt('How many users signed up in the last 7 days?')
console.log(result.text)
```

### MCP server integration

```typescript
import { createAgent } from '@shipany/open-agent-sdk'

const agent = createAgent({
  mcpServers: {
    filesystem: {
      command: 'npx',
      args: ['-y', '@modelcontextprotocol/server-filesystem', '/tmp'],
    },
    playwright: {
      command: 'npx',
      args: ['@playwright/mcp@latest'],
    },
  },
})

const result = await agent.prompt('List all .json files in /tmp')
console.log(result.text)
```

### Subagents for parallel / delegated work

```typescript
import { query } from '@shipany/open-agent-sdk'

for await (const message of query({
  prompt: 'Use the security-auditor agent to audit src/ for vulnerabilities',
  options: {
    allowedTools: ['Read', 'Glob', 'Grep', 'Agent'],
    agents: {
      'security-auditor': {
        description: 'Expert security auditor for TypeScript codebases.',
        prompt: 'Identify OWASP Top 10 vulnerabilities and suggest fixes.',
        tools: ['Read', 'Glob', 'Grep'],
      },
    },
  },
})) {
  if (message.type === 'assistant' && message.message?.content) {
    for (const block of message.message.content) {
      if ('text' in block) console.log(block.text)
    }
  }
}
```

### Custom permission callback

```typescript
import { createAgent } from '@shipany/open-agent-sdk'

const agent = createAgent({
  canUseTool: (toolName: string, input: unknown) => {
    // Prevent deletion commands
    if (toolName === 'Bash') {
      const cmd = (input as { command?: string }).command ?? ''
      if (cmd.includes('rm ') || cmd.includes('drop table')) return false
    }
    return true
  },
})
```

### Lifecycle hooks

```typescript
import { createAgent } from '@shipany/open-agent-sdk'

const agent = createAgent({
  hooks: {
    PreToolUse: async ({ tool, input }) => {
      console.log(`About to run tool: ${tool} with input:`, input)
    },
    PostToolUse: async ({ tool, output }) => {
      console.log(`Tool ${tool} finished`)
    },
    Stop: async ({ result }) => {
      console.log('Agent stopped. Final result:', result)
    },
  },
})
```

### Resume a previous session

```typescript
import { createAgent } from '@shipany/open-agent-sdk'

// First session
const agent1 = createAgent({ model: 'claude-sonnet-4-6' })
const r1 = await agent1.prompt('Read ARCHITECTURE.md')
const sessionId = r1.sessionId  // save this

// Later — resume where you left off
const agent2 = createAgent({
  model: 'claude-sonnet-4-6',
  resume: sessionId,
})
const r2 = await agent2.prompt('Now implement the TODO in section 3')
```

---

## Built-in Tools Reference

| Tool | Read-only | Description |
|---|---|---|
| `Read` | ✅ | Read files, images, PDFs with line numbers |
| `Glob` | ✅ | Find files by glob pattern |
| `Grep` | ✅ | Search file contents with regex (uses ripgrep) |
| `WebFetch` | ✅ | Fetch and parse web pages |
| `WebSearch` | ✅ | Web search |
| `Write` | ❌ | Create or overwrite files |
| `Edit` | ❌ | Precise string replacement in files |
| `Bash` | ❌ | Execute shell commands |
| `Agent` | — | Spawn subagents |
| `TodoWrite` | ❌ | Manage todo lists |
| `NotebookEdit` | ❌ | Edit Jupyter notebooks |
| `TaskCreate/Update/List` | — | Task management |
| `TeamCreate/Delete` | — | Agent team management |
| `EnterPlanMode/ExitPlanMode` | — | Plan approval workflow |
| `EnterWorktree/ExitWorktree` | — | Git worktree isolation |
| `ListMcpResources/ReadMcpResource` | ✅ | MCP resource access |

---

## Architecture: How It Differs from Official SDK

**Official `@anthropic-ai/claude-agent-sdk`:**
```
Your code → SDK → spawn cli.js subprocess → stdin/stdout JSON → Anthropic API
```

**Open Agent SDK:**
```
Your code → SDK → QueryEngine (in-process) → Anthropic API (direct HTTP)
```

This means:
- No CLI installation required in the deployment environment
- Works in serverless (AWS Lambda, Vercel, Cloudflare Workers with Node.js compat)
- Works in Docker with just `npm install`
- Works in CI/CD without CLI setup steps
- Programmatic access to the full agent engine

---

## Troubleshooting

**`Error: ANTHROPIC_API_KEY is not set`**
→ Export the env var or pass `apiKey` directly in `createAgent({ apiKey: process.env.MY_KEY })`.

**Agent exceeds `maxTurns` without completing**
→ Increase `maxTurns` or narrow the task. Check `message.subtype === 'max_turns'` in the result.

**Tool not found / `allowedTools` not working**
→ Tool names are case-sensitive: `'Read'`, `'Edit'`, `'Bash'`, `'Glob'`, `'Grep'`, `'WebFetch'`, etc.

**Using with OpenRouter or other providers**
→ Set `ANTHROPIC_BASE_URL` to the provider's base URL and use their model string format, e.g. `anthropic/claude-sonnet-4-6` for OpenRouter.

**Agent modifies files unexpectedly**
→ Use `allowedTools: ['Read', 'Glob', 'Grep']` to restrict to read-only tools, or set `permissionMode: 'plan'` to require approval before edits.

**MCP server fails to start**
→ Ensure the MCP server package is installed or accessible via `npx`. Check `command` and `args` match what the MCP package expects.

**TypeScript types missing**
→ The package ships its own types. Ensure `"moduleResolution": "bundler"` or `"node16"` in `tsconfig.json` and `"esModuleInterop": true`.

---

## Quick Reference

```typescript
// Minimal one-shot agent
import { createAgent } from '@shipany/open-agent-sdk'
const agent = createAgent({ model: 'claude-sonnet-4-6' })
const { text } = await agent.prompt('Summarize README.md in 3 bullet points')
console.log(text)
```
