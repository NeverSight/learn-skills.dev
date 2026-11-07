---
name: open-multi-agent-orchestration
description: Expertise in using open-multi-agent, a TypeScript framework for building production-grade multi-agent AI teams with task scheduling, dependency graphs, and inter-agent communication.
triggers:
  - set up a multi-agent AI team
  - orchestrate multiple AI agents
  - build agents that collaborate
  - create a task pipeline with dependencies
  - use open-multi-agent framework
  - run agents in parallel with task scheduling
  - mix Claude and GPT in one workflow
  - define custom tools for AI agents
---

# Open Multi-Agent Orchestration

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

`open-multi-agent` is a TypeScript framework for building AI agent teams where agents with different roles, models, and tools collaborate on complex goals. The framework handles task dependency resolution (DAG scheduling), parallel execution, shared memory, and inter-agent communication — all in-process with no subprocess overhead.

## Installation

```bash
npm install @jackchen_me/open-multi-agent
# or
pnpm add @jackchen_me/open-multi-agent
```

Set environment variables:

```bash
export ANTHROPIC_API_KEY=your_key_here
export OPENAI_API_KEY=your_key_here   # optional, only if using OpenAI models
```

## Core Concepts

| Concept | Description |
|---------|-------------|
| `OpenMultiAgent` | Top-level orchestrator — entry point for all operations |
| `Team` | A named group of agents sharing a message bus, task queue, and optional shared memory |
| `AgentConfig` | Defines an agent's name, model, provider, system prompt, and allowed tools |
| `Task` | A unit of work with a title, description, assignee, and optional `dependsOn` list |
| `LLMAdapter` | Pluggable interface — built-in adapters for Anthropic and OpenAI |
| `ToolRegistry` | Registry of available tools; built-ins + custom tools via `defineTool()` |

## Quick Start — Single Agent

```typescript
import { OpenMultiAgent } from '@jackchen_me/open-multi-agent'

const orchestrator = new OpenMultiAgent({ defaultModel: 'claude-sonnet-4-6' })

const result = await orchestrator.runAgent(
  {
    name: 'coder',
    model: 'claude-sonnet-4-6',
    tools: ['bash', 'file_write'],
  },
  'Write a TypeScript function that reverses a string, save it to /tmp/reverse.ts, and run it.',
)

console.log(result.output)
```

## Multi-Agent Team

```typescript
import { OpenMultiAgent } from '@jackchen_me/open-multi-agent'
import type { AgentConfig } from '@jackchen_me/open-multi-agent'

const architect: AgentConfig = {
  name: 'architect',
  model: 'claude-sonnet-4-6',
  systemPrompt: 'You design clean API contracts and file structures.',
  tools: ['file_write'],
}

const developer: AgentConfig = {
  name: 'developer',
  model: 'claude-sonnet-4-6',
  systemPrompt: 'You implement what the architect designs.',
  tools: ['bash', 'file_read', 'file_write', 'file_edit'],
}

const reviewer: AgentConfig = {
  name: 'reviewer',
  model: 'claude-sonnet-4-6',
  systemPrompt: 'You review code for correctness and clarity.',
  tools: ['file_read', 'grep'],
}

const orchestrator = new OpenMultiAgent({
  defaultModel: 'claude-sonnet-4-6',
  onProgress: (event) => console.log(event.type, event.agent ?? event.task ?? ''),
})

const team = orchestrator.createTeam('api-team', {
  name: 'api-team',
  agents: [architect, developer, reviewer],
  sharedMemory: true,
})

const result = await orchestrator.runTeam(
  team,
  'Create a REST API for a todo list in /tmp/todo-api/',
)

console.log(`Success: ${result.success}`)
console.log(`Output tokens: ${result.totalTokenUsage.output_tokens}`)
```

## Task Pipeline — Explicit DAG Control

Use `runTasks()` when you need precise control over task ordering, assignments, and parallelism:

```typescript
const result = await orchestrator.runTasks(team, [
  {
    title: 'Design the data model',
    description: 'Write a TypeScript interface spec to /tmp/spec.md',
    assignee: 'architect',
  },
  {
    title: 'Implement the module',
    description: 'Read /tmp/spec.md and implement the module in /tmp/src/',
    assignee: 'developer',
    dependsOn: ['Design the data model'], // blocked until design completes
  },
  {
    title: 'Write tests',
    description: 'Read the implementation and write Vitest tests.',
    assignee: 'developer',
    dependsOn: ['Implement the module'],
  },
  {
    title: 'Review code',
    description: 'Review /tmp/src/ and produce a structured code review.',
    assignee: 'reviewer',
    dependsOn: ['Implement the module'], // runs in parallel with "Write tests"
  },
])
```

Tasks with no unresolved `dependsOn` entries run in parallel automatically. The framework cascades failures — if a task fails, dependent tasks are skipped.

## Multi-Model Teams (Claude + GPT)

```typescript
const claudeAgent: AgentConfig = {
  name: 'strategist',
  model: 'claude-opus-4-6',
  provider: 'anthropic',
  systemPrompt: 'You plan high-level approaches.',
  tools: ['file_write'],
}

const gptAgent: AgentConfig = {
  name: 'implementer',
  model: 'gpt-5.4',
  provider: 'openai',
  systemPrompt: 'You implement plans as working code.',
  tools: ['bash', 'file_read', 'file_write'],
}

const team = orchestrator.createTeam('mixed-team', {
  name: 'mixed-team',
  agents: [claudeAgent, gptAgent],
  sharedMemory: true,
})

const result = await orchestrator.runTeam(team, 'Build a CLI tool that converts JSON to CSV.')
```

## Custom Tools with Zod Schemas

```typescript
import { z } from 'zod'
import {
  defineTool,
  Agent,
  ToolRegistry,
  ToolExecutor,
  registerBuiltInTools,
} from '@jackchen_me/open-multi-agent'

// Define the tool
const weatherTool = defineTool({
  name: 'get_weather',
  description: 'Get current weather for a city.',
  inputSchema: z.object({
    city: z.string().describe('The city name.'),
    units: z.enum(['celsius', 'fahrenheit']).optional().describe('Temperature units.'),
  }),
  execute: async ({ city, units = 'celsius' }) => {
    // Replace with your actual weather API call
    const data = await fetchWeatherAPI(city, units)
    return { data: JSON.stringify(data), isError: false }
  },
})

// Wire up registry
const registry = new ToolRegistry()
registerBuiltInTools(registry)        // adds bash, file_read, file_write, file_edit, grep
registry.register(weatherTool)        // add your custom tool

const executor = new ToolExecutor(registry)
const agent = new Agent(
  {
    name: 'weather-agent',
    model: 'claude-sonnet-4-6',
    tools: ['get_weather', 'file_write'],
  },
  registry,
  executor,
)

const result = await agent.run('Get the weather for Tokyo and save a report to /tmp/weather.txt')
```

## Streaming Output

```typescript
import { Agent, ToolRegistry, ToolExecutor, registerBuiltInTools } from '@jackchen_me/open-multi-agent'

const registry = new ToolRegistry()
registerBuiltInTools(registry)
const executor = new ToolExecutor(registry)

const agent = new Agent(
  { name: 'writer', model: 'claude-sonnet-4-6', maxTurns: 3 },
  registry,
  executor,
)

for await (const event of agent.stream('Explain dependency injection in two paragraphs.')) {
  if (event.type === 'text' && typeof event.data === 'string') {
    process.stdout.write(event.data)
  }
}
```

## Progress Monitoring

```typescript
const orchestrator = new OpenMultiAgent({
  defaultModel: 'claude-sonnet-4-6',
  onProgress: (event) => {
    switch (event.type) {
      case 'task:start':
        console.log(`▶ Task started: ${event.task}`)
        break
      case 'task:complete':
        console.log(`✓ Task done: ${event.task}`)
        break
      case 'task:failed':
        console.error(`✗ Task failed: ${event.task}`)
        break
      case 'agent:thinking':
        console.log(`  [${event.agent}] thinking...`)
        break
      case 'agent:tool_use':
        console.log(`  [${event.agent}] using tool: ${event.tool}`)
        break
    }
  },
})
```

## Built-in Tools Reference

| Tool | Key Options | Notes |
|------|-------------|-------|
| `bash` | `command`, `timeout`, `cwd` | Returns stdout + stderr |
| `file_read` | `path`, `offset`, `limit` | Use offset/limit for large files |
| `file_write` | `path`, `content` | Auto-creates parent directories |
| `file_edit` | `path`, `old_string`, `new_string` | Exact string match replacement |
| `grep` | `pattern`, `path`, `flags` | Uses ripgrep if available, falls back to Node.js |

## AgentConfig Options

```typescript
interface AgentConfig {
  name: string                    // unique within a team
  model: string                   // e.g. 'claude-sonnet-4-6', 'gpt-5.4'
  provider?: 'anthropic' | 'openai'  // inferred from model name if omitted
  systemPrompt?: string           // agent's persona and instructions
  tools?: string[]                // names of tools the agent can use
  maxTurns?: number               // max conversation turns (default: unlimited)
}
```

## Custom LLM Adapter

Implement two methods to add any LLM provider:

```typescript
import type { LLMAdapter, ChatMessage, ChatResponse } from '@jackchen_me/open-multi-agent'

class OllamaAdapter implements LLMAdapter {
  async chat(messages: ChatMessage[], options?: ChatOptions): Promise<ChatResponse> {
    const response = await fetch('http://localhost:11434/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ model: options?.model ?? 'llama3', messages }),
    })
    const data = await response.json()
    return {
      content: data.message.content,
      usage: { input_tokens: 0, output_tokens: 0 },
    }
  }

  async *stream(messages: ChatMessage[], options?: ChatOptions): AsyncIterable<StreamEvent> {
    // implement streaming from Ollama's /api/chat with stream:true
  }
}
```

## Common Patterns

### Pattern: Research → Write → Review pipeline

```typescript
const team = orchestrator.createTeam('content-team', {
  name: 'content-team',
  agents: [
    { name: 'researcher', model: 'claude-sonnet-4-6', tools: ['bash', 'file_write'] },
    { name: 'writer', model: 'claude-sonnet-4-6', tools: ['file_read', 'file_write'] },
    { name: 'editor', model: 'claude-sonnet-4-6', tools: ['file_read', 'file_edit'] },
  ],
  sharedMemory: true,
})

await orchestrator.runTasks(team, [
  {
    title: 'Research topic',
    description: 'Research TypeScript 5.6 features, save findings to /tmp/research.md',
    assignee: 'researcher',
  },
  {
    title: 'Write article',
    description: 'Read /tmp/research.md and write a blog post to /tmp/article.md',
    assignee: 'writer',
    dependsOn: ['Research topic'],
  },
  {
    title: 'Edit article',
    description: 'Read /tmp/article.md and improve clarity and tone in-place',
    assignee: 'editor',
    dependsOn: ['Write article'],
  },
])
```

### Pattern: Fan-out then merge

```typescript
// Three agents work on separate modules in parallel, then one integrates
await orchestrator.runTasks(team, [
  { title: 'Build auth module', assignee: 'dev-1', description: '...' },
  { title: 'Build data module', assignee: 'dev-2', description: '...' },
  { title: 'Build api module',  assignee: 'dev-3', description: '...' },
  {
    title: 'Integrate modules',
    assignee: 'architect',
    description: 'Wire auth, data, and api modules together.',
    dependsOn: ['Build auth module', 'Build data module', 'Build api module'],
  },
])
```

## Troubleshooting

**`ANTHROPIC_API_KEY` not found**
Ensure the env var is exported in the shell running your script, or use a `.env` loader like `dotenv` before importing from the framework.

**Tasks not running in parallel**
Check that tasks don't share a circular `dependsOn` chain. Only tasks with all dependencies resolved become eligible for parallel execution.

**Agent exceeds token limit**
Set `maxTurns` on the `AgentConfig` to cap conversation length. For large file operations, use `file_read` with `offset`/`limit` instead of reading entire files.

**Tool not found error**
Ensure the tool name in `AgentConfig.tools[]` exactly matches the name registered in `ToolRegistry`. Built-in tools are registered via `registerBuiltInTools(registry)`.

**OpenAI adapter not initializing**
`OPENAI_API_KEY` must be set when any agent uses `provider: 'openai'`. The framework initializes the adapter lazily but will throw if the key is missing at first use.

**Type errors with `defineTool`**
Ensure `zod` is installed as a direct dependency (`npm install zod`) — the framework uses Zod for schema validation but doesn't re-export it.
