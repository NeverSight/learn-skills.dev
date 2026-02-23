---
name: agent-sdk
description: Guide for Claude Agent SDK - build custom AI agents powered by Claude. Covers installation, authentication providers, tool permissions, file-based configuration, TypeScript/Python code examples, and project scaffolding templates.
---

# Claude Agent SDK Guide

Build custom AI agents powered by Claude. Same infrastructure as Claude Code.

## Installation

### TypeScript

```bash
npm install @anthropic-ai/claude-agent-sdk
```

### Python

```bash
pip install claude-agent-sdk
```

## Core Features

### Context Management

Automatic compaction ensures your agent doesn't run out of context during extended operations.

### Tool Ecosystem

Built-in capabilities:
- **File operations** - Read, write, edit files
- **Code execution** - Run bash commands safely
- **Web search** - Access real-time information
- **MCP extensibility** - Add custom tools via Model Context Protocol

### Permission Controls

```typescript
{
  allowedTools: ['Read', 'Write', 'Bash'],  // Explicit allowlist
  disallowedTools: ['WebSearch'],            // Explicit blocklist
  permissionMode: 'default' | 'strict'       // Overall strategy
}
```

## Authentication Providers

### Anthropic API (Default)

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

### Amazon Bedrock

```bash
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export AWS_REGION=us-east-1
```

### Google Vertex AI

```bash
export CLAUDE_CODE_USE_VERTEX=1
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
export VERTEX_REGION=us-central1
export VERTEX_PROJECT_ID=your-project
```

### Microsoft Foundry

```bash
export CLAUDE_CODE_USE_FOUNDRY=1
# Azure credentials configuration
```

## File-Based Configuration

| Directory | Purpose |
|-----------|---------|
| `.claude/agents/` | Subagent definitions (Markdown) |
| `.claude/skills/` | Skill files (`SKILL.md`) |
| `.claude/commands/` | Slash commands (Markdown) |
| `.claude/settings.json` | Hooks configuration |
| `CLAUDE.md` | Project memory/context |

Enable project settings:

```typescript
{
  settingSources: ['project']
}
```

## Code Examples

### TypeScript: Basic Agent

```typescript
import { Agent } from '@anthropic-ai/claude-agent-sdk';

const agent = new Agent({
  model: 'claude-sonnet-4-20250514',
  allowedTools: ['Read', 'Write', 'Bash'],
  systemPrompt: `You are a code review assistant.
    Analyze code for bugs, security issues, and best practices.`,
});

const result = await agent.run({
  prompt: 'Review the code in src/auth.ts for security issues',
});

console.log(result.output);
```

### TypeScript: Agent with MCP Tools

```typescript
import { Agent } from '@anthropic-ai/claude-agent-sdk';

const agent = new Agent({
  model: 'claude-sonnet-4-20250514',
  mcpServers: {
    database: {
      command: 'npx',
      args: ['-y', '@modelcontextprotocol/server-postgres'],
      env: { DATABASE_URL: process.env.DATABASE_URL },
    },
  },
});

const result = await agent.run({
  prompt: 'List all users who signed up in the last 24 hours',
});
```

### Python: Basic Agent

```python
from claude_agent_sdk import Agent

agent = Agent(
    model="claude-sonnet-4-20250514",
    allowed_tools=["Read", "Write", "Bash"],
    system_prompt="""You are a code review assistant.
    Analyze code for bugs, security issues, and best practices.""",
)

result = agent.run(
    prompt="Review the code in src/auth.py for security issues"
)

print(result.output)
```

### Python: Agent with Custom Permissions

```python
from claude_agent_sdk import Agent, PermissionMode

agent = Agent(
    model="claude-sonnet-4-20250514",
    permission_mode=PermissionMode.STRICT,
    allowed_tools=["Read", "Grep", "Glob"],
    disallowed_tools=["Bash"],  # Extra safety
)

result = agent.run(
    prompt="Find all TODO comments in the codebase"
)
```

## Agent Types & Use Cases

### Coding Agents

- **SRE Diagnostics** - Analyze logs, identify issues, suggest fixes
- **Security Auditing** - Scan for vulnerabilities, check dependencies
- **Incident Triage** - Correlate alerts, gather context, draft runbooks
- **Code Review** - Enforce standards, catch bugs, suggest improvements

### Business Agents

- **Legal Review** - Analyze contracts, flag risks, summarize terms
- **Financial Analysis** - Process reports, identify anomalies, forecast
- **Customer Support** - Handle tickets, route issues, draft responses
- **Content Creation** - Generate docs, edit copy, ensure consistency

## Best Practices

### Start Simple

Begin with minimal tool access and expand as needed:

```typescript
// Start here
allowedTools: ['Read']

// Then add as required
allowedTools: ['Read', 'Grep', 'Glob']

// Only if truly needed
allowedTools: ['Read', 'Write', 'Bash']
```

### Use Subagents for Complex Tasks

Break large tasks into specialized subagents:

```
.claude/agents/
├── code-reviewer.md      # Reviews code changes
├── test-writer.md        # Generates tests
└── doc-generator.md      # Creates documentation
```

### Handle Errors Gracefully

```typescript
try {
  const result = await agent.run({ prompt });
  if (result.error) {
    console.error('Agent error:', result.error);
  }
} catch (error) {
  console.error('SDK error:', error);
}
```

### Monitor Agent Behavior

```typescript
const agent = new Agent({
  onToolUse: (tool, input) => {
    console.log(`Tool: ${tool}, Input: ${JSON.stringify(input)}`);
  },
  onThinking: (thought) => {
    console.log(`Thinking: ${thought}`);
  },
});
```

## Project Scaffolding

Use `/agent-sdk:agent-scaffold` command to generate a new project.

### Template Files

| Template | Purpose |
|----------|---------|
| `assets/typescript/package.json` | Node.js package config |
| `scripts/typescript/agent.ts` | TypeScript agent entry |
| `assets/python/pyproject.toml` | Python package config |
| `scripts/python/agent.py` | Python agent entry |
| `assets/env-*.example` | Provider config templates |
| `references/claude/*.md` | Subagent/skill/command templates |

### Tool Mapping

| User Selection | SDK Tools |
|----------------|-----------|
| File Operations | Read, Write, Edit, Glob, Grep |
| Code Execution | Bash |
| Web Search | WebSearch, WebFetch |
| MCP Tools | (configured via mcpServers) |

### System Prompts

**Coding Agent:**
```
You are a coding assistant that helps developers write better code.
Analyze code for bugs, security issues, and best practices.
```

**Business Agent:**
```
You are a business analyst assistant.
Help with document analysis, data extraction, and report generation.
```

## Resources

- **TypeScript**: [anthropics/claude-agent-sdk-typescript](https://github.com/anthropics/claude-agent-sdk-typescript)
- **Python**: [anthropics/claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python)
- **Docs**: [platform.claude.com/docs/en/agent-sdk/overview](https://platform.claude.com/docs/en/agent-sdk/overview)
