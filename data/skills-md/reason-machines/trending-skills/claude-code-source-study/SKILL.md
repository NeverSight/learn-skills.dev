---
name: claude-code-source-study
description: Deep dive into Claude Code source code to learn production-grade AI agent architecture patterns
triggers:
  - study claude code source
  - learn ai agent architecture
  - how does claude code work internally
  - implement agent like claude code
  - understand claude code system prompt
  - build production ai agent
  - claude code tool system design
  - multi agent orchestration patterns
---

# Claude Code Source Study

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

A 25-article deep-dive into Claude Code's ~1900-file source code, covering System Prompt engineering, multi-agent orchestration, tool systems, permission security, and terminal UI. Learn production-grade AI agent patterns from Anthropic's real CLI product.

## What This Project Is

This is a **Chinese-language source code analysis series** that dissects Claude Code (Anthropic's AI CLI coding assistant) module by module — with exact file references, line numbers, and code snippets. Each article extracts reusable design patterns for building your own AI agent applications.

**Tech stack covered:** Bun + TypeScript + Ink (React for terminals) + Anthropic API

## Repository Structure

```
claude-code-source-study/
├── docs/
│   ├── 00-目录与阅读指引.md      # Index and reading guide
│   ├── 01-项目全景.md             # Project overview
│   ├── 02-启动优化.md             # Startup optimization
│   ├── 03-状态管理.md             # State management
│   ├── 04-System-Prompt-工程.md  # System prompt engineering
│   ├── 05-对话循环.md             # Conversation loop
│   ├── 06-上下文管理.md           # Context management
│   ├── 07-Prompt-Cache.md        # Prompt caching
│   ├── 08-Thinking-与推理控制.md  # Thinking & reasoning
│   ├── 09-工具系统设计.md          # Tool system design
│   ├── 10-BashTool-深度剖析.md    # BashTool deep dive
│   ├── 11-命令系统.md             # Command system
│   ├── 12-Agent-系统.md           # Agent system
│   ├── 13-内置Agent设计模式.md    # Built-in agent patterns
│   ├── 14-任务系统.md             # Task system
│   ├── 15-MCP-协议实现.md         # MCP protocol
│   ├── 16-权限系统.md             # Permission system
│   ├── 17-Settings-系统.md       # Settings system
│   ├── 18-Hooks系统.md            # Hooks system
│   ├── 19-Feature-Flag与编译期优化.md
│   ├── 20-API调用与错误恢复.md    # API retry/recovery
│   ├── 21-Ink框架深度定制.md      # Ink UI customization
│   ├── 22-设计系统.md             # Design system
│   ├── 23-Memory系统.md           # Memory system
│   ├── 24-Skill-Plugin开发实战.md # Plugin development
│   └── 25-架构模式总结.md         # Architecture patterns summary
└── README.md
```

## Reading Routes

### ⚡ Quick Route (7 articles) — Global understanding
```
01 → 02 → 03 → 05 → 09 → 12 → 25
```

### 🤖 AI Engineering Route (9 articles) — Deep AI core
```
01 → 03 → 04 → 05 → 06 → 08 → 09 → 12 → 13
```

### 📚 Complete Route (25 articles)
Read docs/01 through docs/25 in order.

## Key Patterns Extracted from Claude Code

### 1. Tool Builder Pattern (`buildTool()`)

Claude Code registers tools using a builder with three-layer conditional registration:

```typescript
// Pattern extracted from docs/09-工具系统设计.md
const buildTool = <TInput, TOutput>(config: {
  name: string
  description: string
  inputSchema: ZodSchema<TInput>
  handler: (input: TInput, context: ToolContext) => Promise<TOutput>
  isEnabled?: (context: AppContext) => boolean
  requiresPermission?: PermissionLevel
}) => config

// Registration with conditions
const tools = [
  buildTool({ name: 'bash', ... }),
  buildTool({ name: 'read_file', ... }),
  buildTool({ name: 'write_file', ... }),
].filter(tool => tool.isEnabled?.(ctx) ?? true)
```

### 2. AsyncGenerator Conversation Loop (`docs/05`)

```typescript
// Pattern: state-machine conversation loop using AsyncGenerator
async function* conversationLoop(
  messages: Message[],
  tools: Tool[]
): AsyncGenerator<StreamEvent> {
  while (true) {
    const stream = await anthropic.messages.stream({
      model: 'claude-opus-4-5',
      messages,
      tools,
      system: buildSystemPrompt(),
    })

    for await (const event of stream) {
      yield event
    }

    const response = await stream.finalMessage()

    if (response.stop_reason === 'end_turn') break

    if (response.stop_reason === 'tool_use') {
      const toolResults = await executeTools(response.content)
      messages.push({ role: 'assistant', content: response.content })
      messages.push({ role: 'user', content: toolResults })
      // loop continues
    }
  }
}
```

### 3. 35-Line Minimal Store (React ↔ Non-React Bridge) (`docs/03`)

```typescript
// Pattern: tiny reactive store bridging React and imperative code
type Listener<T> = (state: T) => void

function createStore<T>(initialState: T) {
  let state = initialState
  const listeners = new Set<Listener<T>>()

  return {
    getState: () => state,
    setState: (updater: Partial<T> | ((s: T) => T)) => {
      state = typeof updater === 'function'
        ? updater(state)
        : { ...state, ...updater }
      listeners.forEach(l => l(state))
    },
    subscribe: (listener: Listener<T>) => {
      listeners.add(listener)
      return () => listeners.delete(listener)
    },
    // React hook integration
    useStore: () => {
      const [s, setS] = React.useState(state)
      React.useEffect(() => subscribe(setS), [])
      return s
    }
  }
}
```

### 4. System Prompt Segmented Construction (`docs/04`)

```typescript
// Pattern: build system prompt in segments with cache boundaries
function buildSystemPrompt(context: AppContext): SystemPrompt {
  return [
    // Static segment — cache this (never changes)
    { type: 'text', text: CORE_INSTRUCTIONS, cache_control: { type: 'ephemeral' } },

    // Semi-static segment — cache per project
    { type: 'text', text: buildProjectContext(context.project), cache_control: { type: 'ephemeral' } },

    // Dynamic segment — never cache (changes each turn)
    { type: 'text', text: buildDynamicContext(context.session) },
  ]
}
```

### 5. Context Auto-Compact with Token Budget (`docs/06`)

```typescript
// Pattern: token budget management with auto-compact
const TOKEN_BUDGET = {
  MAX_CONTEXT: 200_000,
  COMPACT_THRESHOLD: 0.85,  // compact at 85% full
  SUMMARY_RESERVE: 2_000,
}

async function maybeCompact(messages: Message[]): Promise<Message[]> {
  const tokenCount = await countTokens(messages)

  if (tokenCount < TOKEN_BUDGET.MAX_CONTEXT * TOKEN_BUDGET.COMPACT_THRESHOLD) {
    return messages
  }

  // Summarize older messages, keep recent ones verbatim
  const keepRecent = messages.slice(-20)
  const toSummarize = messages.slice(0, -20)

  const summary = await summarize(toSummarize)
  return [
    { role: 'user', content: `Previous conversation summary:\n${summary}` },
    { role: 'assistant', content: 'Understood.' },
    ...keepRecent,
  ]
}
```

### 6. Permission 7-Step Decision Pipeline (`docs/16`)

```typescript
// Pattern: layered permission evaluation
type PermissionMode = 'default' | 'acceptEdits' | 'bypassPermissions' | 'plan' | 'auto' | 'strict' | 'custom'

async function evaluatePermission(
  action: ToolAction,
  context: PermissionContext
): Promise<PermissionResult> {
  // Step 1: Check bypass mode
  if (context.mode === 'bypassPermissions') return { allowed: true }

  // Step 2: Check if action is always-safe
  if (isAlwaysSafe(action)) return { allowed: true }

  // Step 3: Check allowlist
  if (isAllowlisted(action, context.allowlist)) return { allowed: true }

  // Step 4: Check blocklist
  if (isBlocklisted(action, context.blocklist)) return { allowed: false, reason: 'blocklisted' }

  // Step 5: Check auto-approve rules
  if (matchesAutoApprove(action, context.rules)) return { allowed: true }

  // Step 6: Check session memory
  if (context.sessionMemory.has(actionKey(action))) return { allowed: true }

  // Step 7: Ask user
  const decision = await promptUser(action)
  if (decision.remember) context.sessionMemory.add(actionKey(action))
  return { allowed: decision.approved }
}
```

### 7. Multi-Agent Context Isolation (`docs/12`)

```typescript
// Pattern: sub-agent with isolated context
async function spawnSubAgent(task: AgentTask, parentContext: AgentContext) {
  const subContext: AgentContext = {
    // Isolated: sub-agent gets its own conversation
    messages: [],
    sessionId: generateId(),

    // Inherited: shares tools and permissions from parent
    tools: parentContext.tools,
    permissionMode: parentContext.permissionMode,

    // Scoped: limited working directory
    cwd: task.workingDir ?? parentContext.cwd,

    // Budget: prevent runaway sub-agents
    maxTurns: task.maxTurns ?? 10,
    tokenBudget: task.tokenBudget ?? 50_000,
  }

  return conversationLoop(
    [{ role: 'user', content: task.prompt }],
    subContext.tools,
    subContext
  )
}
```

### 8. withRetry for API Overload (`docs/20`)

```typescript
// Pattern: exponential backoff with overload handling
async function withRetry<T>(
  fn: () => Promise<T>,
  options = { maxAttempts: 3, baseDelay: 1000 }
): Promise<T> {
  for (let attempt = 1; attempt <= options.maxAttempts; attempt++) {
    try {
      return await fn()
    } catch (err) {
      if (attempt === options.maxAttempts) throw err

      // Handle Anthropic 529 overloaded
      if (isOverloadError(err)) {
        const delay = options.baseDelay * Math.pow(2, attempt - 1)
        await sleep(delay + Math.random() * 1000) // jitter
        continue
      }

      // Don't retry non-retriable errors
      if (isAuthError(err) || isInvalidRequestError(err)) throw err

      throw err
    }
  }
  throw new Error('unreachable')
}
```

## Applying These Patterns to Your Own Agent

### Minimal Agent Scaffold

```typescript
import Anthropic from '@anthropic-ai/sdk'

const anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY })

// 1. Define tools using builder pattern
const tools = [
  buildTool({
    name: 'read_file',
    description: 'Read a file from disk',
    inputSchema: z.object({ path: z.string() }),
    handler: async ({ path }) => fs.readFile(path, 'utf-8'),
  }),
]

// 2. Build system prompt with cache segments
const systemPrompt = buildSystemPrompt({ static: CORE_RULES, dynamic: '' })

// 3. Run conversation loop
for await (const event of conversationLoop(
  [{ role: 'user', content: userInput }],
  tools
)) {
  if (event.type === 'text') process.stdout.write(event.text)
}
```

### Thinking / Extended Reasoning Config (`docs/08`)

```typescript
// Control reasoning effort per request
type ThinkingConfig =
  | { type: 'disabled' }
  | { type: 'enabled'; budget_tokens: number }

// "ultrathink" = maximum budget
const EFFORT_LEVELS = {
  low:        { type: 'enabled', budget_tokens: 1_000 },
  medium:     { type: 'enabled', budget_tokens: 5_000 },
  high:       { type: 'enabled', budget_tokens: 10_000 },
  ultrathink: { type: 'enabled', budget_tokens: 32_000 },
} satisfies Record<string, ThinkingConfig>

const response = await anthropic.messages.create({
  model: 'claude-opus-4-5',
  thinking: EFFORT_LEVELS.ultrathink,
  messages,
})
```

## Troubleshooting

| Problem | Solution |
|---|---|
| Article links 404 | Clone the repo — all articles are in `docs/` locally |
| Code examples reference internal modules | They're illustrative patterns extracted from analysis, not runnable as-is |
| Need the actual Claude Code source | See [Anthropic's published CLI source](https://github.com/anthropics/claude-code) |
| Want to contribute an article | Open a PR to `docs/` following the existing article format |

## Start Here

```bash
git clone https://github.com/luyao618/Claude-Code-Source-Study
cd Claude-Code-Source-Study

# Quick route: global understanding (7 articles)
open docs/01-项目全景.md

# AI engineering deep dive (9 articles)  
open docs/04-System-Prompt-工程.md

# Architecture patterns summary (read last)
open docs/25-架构模式总结.md
```
