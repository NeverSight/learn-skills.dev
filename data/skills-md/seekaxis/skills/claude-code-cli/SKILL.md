---
name: claude-code-cli
description: "Run Claude Code programmatically from scripts, CI/CD pipelines, and other AI agents. Covers the CLI print mode (`claude -p`), the Agent SDK (Python and TypeScript), structured/streaming output, session management, subagents, agent teams, and common automation patterns. Use when the user wants to: (1) automate tasks with Claude Code, (2) integrate Claude Code into scripts or pipelines, (3) use the Agent SDK from Python or TypeScript, (4) orchestrate multiple Claude Code sessions, (5) get structured JSON output from Claude Code, or (6) build agents on top of Claude Code."
---

# Claude Code CLI — Programmatic Usage

Use Claude Code as a programmable agent from shell scripts, CI/CD pipelines, Python, or TypeScript. The CLI's `-p` (print) flag runs non-interactively; the Agent SDK gives full programmatic control.

## Quick Start

### One-shot task (CLI)

```bash
claude -p "Find and fix the bug in auth.py" --allowedTools "Read,Edit,Bash"
```

### Python SDK

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    async for message in query(
        prompt="Find and fix the bug in auth.py",
        options=ClaudeAgentOptions(allowed_tools=["Read", "Edit", "Bash"])
    ):
        if hasattr(message, "result"):
            print(message.result)

asyncio.run(main())
```

### TypeScript SDK

```typescript
import { query, ClaudeAgentOptions } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Find and fix the bug in auth.py",
  options: { allowedTools: ["Read", "Edit", "Bash"] },
})) {
  if (message.result) console.log(message.result);
}
```

## Core Concepts

### Print Mode (`-p`)

The `-p` flag runs Claude non-interactively. All CLI flags work with `-p`:

```bash
claude -p "What does the auth module do?"
```

Key flags for programmatic use:

| Flag | Purpose |
|------|---------|
| `-p "prompt"` | Run non-interactively, print result |
| `--output-format json` | Structured JSON with session ID and metadata |
| `--output-format stream-json` | Newline-delimited JSON for streaming |
| `--allowedTools "Read,Edit,Bash"` | Auto-approve specific tools |
| `--max-turns 5` | Limit agentic turns |
| `--max-budget-usd 2.00` | Cap API spend |
| `--model sonnet` | Select model (`sonnet`, `opus`, `haiku`) |
| `--continue` | Continue most recent conversation |
| `--resume <id>` | Resume specific session by ID |
| `--json-schema '{...}'` | Validate output against JSON Schema |

### Structured Output

Get JSON responses with metadata:

```bash
claude -p "Summarize this project" --output-format json
```

Response includes `result` (text), `session_id`, and usage metadata.

For schema-validated output, add `--json-schema`:

```bash
claude -p "Extract function names from auth.py" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}'
```

Structured result is in the `structured_output` field. Parse with `jq`:

```bash
claude -p "Summarize this project" --output-format json | jq -r '.result'
```

### Streaming Output

Stream tokens as they arrive:

```bash
claude -p "Explain recursion" \
  --output-format stream-json --verbose --include-partial-messages
```

Filter for text deltas with `jq`:

```bash
claude -p "Write a poem" \
  --output-format stream-json --verbose --include-partial-messages | \
  jq -rj 'select(.type == "stream_event" and .event.delta.type? == "text_delta") | .event.delta.text'
```

### Auto-Approve Tools

Skip permission prompts for specific tools:

```bash
claude -p "Run tests and fix failures" --allowedTools "Bash,Read,Edit"
```

Use permission rule syntax with prefix matching (`*` after a space):

```bash
claude -p "Create a commit" \
  --allowedTools "Bash(git diff *),Bash(git log *),Bash(git status *),Bash(git commit *)"
```

Skip ALL permission prompts (use with caution):

```bash
claude -p "Fix all lint errors" --dangerously-skip-permissions
```

### Session Management

Continue the most recent conversation:

```bash
claude -p "Review this codebase for issues"
claude -p "Now focus on database queries" --continue
claude -p "Generate a summary" --continue
```

Capture and resume by session ID:

```bash
session_id=$(claude -p "Start review" --output-format json | jq -r '.session_id')
claude -p "Continue that review" --resume "$session_id"
```

### System Prompt Customization

Append to default prompt (recommended — preserves built-in capabilities):

```bash
claude -p "Review this PR" \
  --append-system-prompt "You are a security engineer. Focus on vulnerabilities."
```

Replace entire prompt:

```bash
claude -p "Analyze this code" \
  --system-prompt "You are a Python expert who only writes type-annotated code"
```

Load prompts from files (print mode only):

```bash
claude -p "Review this PR" --append-system-prompt-file ./prompts/security-rules.txt
claude -p "Analyze code" --system-prompt-file ./prompts/custom-prompt.txt
```

### Piping Input

Pipe content to Claude via stdin:

```bash
cat error.log | claude -p "Explain these errors"
gh pr diff 123 | claude -p "Review this diff for security issues"
git diff --staged | claude -p "Write a commit message for these changes"
```

## Subagents

Define custom subagents inline via `--agents` JSON:

```bash
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use proactively after code changes.",
    "prompt": "You are a senior code reviewer. Focus on quality, security, and best practices.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  },
  "debugger": {
    "description": "Debugging specialist for errors and test failures.",
    "prompt": "You are an expert debugger. Analyze errors, identify root causes, and provide fixes."
  }
}'
```

Subagent fields: `description` (required), `prompt` (required), `tools`, `disallowedTools`, `model` (`sonnet`/`opus`/`haiku`/`inherit`), `skills`, `mcpServers`, `maxTurns`, `permissionMode`.

File-based subagents go in `.claude/agents/` (project) or `~/.claude/agents/` (personal):

```markdown
---
name: code-reviewer
description: Reviews code for quality and best practices
tools: Read, Glob, Grep
model: sonnet
---
You are a code reviewer. Analyze code and provide specific,
actionable feedback on quality, security, and best practices.
```

## Agent Teams (Experimental)

Coordinate multiple Claude Code instances working in parallel:

```bash
# Enable first
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1

# Then ask Claude to create a team
claude "Create an agent team: one on security, one on performance, one on test coverage to review PR #142"
```

Teams have a lead (coordinator) and teammates (workers). Each teammate has its own context window. Communication is via shared task lists and direct messaging.

## Additional Resources

- For the complete CLI flags reference, see [cli-reference.md](cli-reference.md)
- For Python and TypeScript Agent SDK details, see [agent-sdk.md](agent-sdk.md)
- For common automation patterns and CI/CD recipes, see [patterns.md](patterns.md)

## Source Documentation

- [Claude Code CLI Reference](https://code.claude.com/docs/en/cli-reference)
- [Programmatic Usage (Headless)](https://code.claude.com/docs/en/headless)
- [Agent SDK Overview](https://platform.claude.com/docs/en/agent-sdk/overview)
- [Subagents](https://code.claude.com/docs/en/sub-agents)
- [Agent Teams](https://code.claude.com/docs/en/agent-teams)
