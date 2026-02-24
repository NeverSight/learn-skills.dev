---
name: agent-worker
description: Create and manage AI agent sessions with multiple backends (SDK, Claude CLI, Codex, Cursor). Also supports multi-agent workflows with shared context, @mention coordination, and collaborative voting. Use for "start agent session", "create worker", "run agent", "multi-agent workflow", "agent collaboration", "test with tools", or when orchestrating AI conversations programmatically.
---

# Agent Worker

## Who You Are

You build AI-powered workflows—from simple Q&A to complex multi-agent collaboration.

**Two modes, one model**:
- **Agent Mode**: Run individual agents via CLI commands
- **Workflow Mode**: Orchestrate multiple agents via YAML

Both modes share the same context system: agents communicate through **channels** (@mentions) and **documents** (shared workspace). Everything is namespaced by `workflow:tag`.

---

## Quick Decision Guide

| I Want To... | Use This |
|-------------|----------|
| Chat with an AI agent | Agent Mode (CLI) |
| Test tools/prompts quickly | Agent Mode with `-b mock` |
| Run multiple agents manually | Workflow Mode (YAML) |
| Define structured multi-agent tasks | Workflow Mode (YAML) |
| Automate repeatable workflows | Workflow Mode (YAML) |

---

## 🤖 Agent Mode

**Run individual agents from the command line.**

### Quick Start

```bash
# Create an agent (auto-named: a0, a1, ...)
agent-worker new -m anthropic/claude-sonnet-4-5
# → a0

# Send a message
agent-worker send a0 "What is 2+2?"

# View conversation
agent-worker peek

# Create a second agent (shares channel)
agent-worker new coder
agent-worker send @global "@a0 @coder collaborate on this"

# Stop agents
agent-worker stop a0 coder
```

### Organizing Agents (workflow:tag)

Group agents into **workflows** using YAML definitions:

```yaml
# review.yaml
agents:
  reviewer:
    backend: claude
    system_prompt: You are a code reviewer.
  coder:
    backend: cursor
    system_prompt: You fix issues.
```

```bash
# Run workflow agents (workflow name from YAML)
agent-worker run review.yaml

# Send to specific agent in workflow
agent-worker send reviewer@review "Check this code"

# Multiple isolated instances (tags)
agent-worker run review.yaml --tag pr-123
agent-worker run review.yaml --tag pr-456

# Each tag has independent context
agent-worker send reviewer@review:pr-123 "LGTM"
agent-worker peek @review:pr-123  # Only sees pr-123 messages
```

**Note**: `agent-worker new` only creates standalone agents in the global workflow. Use YAML for workflow agents.

**Target syntax**:
- `alice` → standalone (`alice@global:main`)
- `alice@review` → agent in review workflow (`alice@review:main`)
- `alice@review:pr-123` → full specification
- `@review` → workflow reference (for broadcast/listing)
- `@review:pr-123` → specific workflow instance

**Context isolation**:
```
.workflow/
├── global/main/        # Standalone agents (default)
├── review/main/        # review workflow, default tag
└── review/pr-123/      # review workflow, pr-123 tag
```

### Agent Commands

```bash
# Lifecycle
agent-worker new [name] [options]        # Create standalone agent
agent-worker ls [target]                 # List agents (default: global)
agent-worker ls --all                    # List all agents from all workflows
agent-worker status <target>             # Check status
agent-worker stop <target>               # Stop agent
agent-worker stop @workflow:tag          # Stop all in workflow:tag

# Interaction
agent-worker send <target> <message>
agent-worker peek [target] [--all] [--find <text>]

# Per-agent operations
agent-worker stats <target>              # Statistics
agent-worker export <target>             # Export transcript
agent-worker clear <target>              # Clear history

# Scheduling (periodic wakeup)
agent-worker schedule <target> set <interval> [--prompt "..."]
agent-worker schedule <target> get
agent-worker schedule <target> clear

# Shared documents
agent-worker doc read <target>
agent-worker doc write <target> --content "..."
agent-worker doc append <target> --file notes.txt
```

### Backend Options

```bash
agent-worker new -m anthropic/claude-sonnet-4-5  # SDK (default)
agent-worker new -b claude                       # Claude CLI
agent-worker new -b cursor                       # Cursor Agent
agent-worker new -b mock                         # Testing (no API)
```

**Note**: Tool management (add, mock, import) only works with SDK backend.

### Examples

**Quick testing without API keys:**
```bash
agent-worker new -b mock
agent-worker send a0 "Hello"
```

**Scheduled monitoring agent:**
```bash
agent-worker new monitor --wakeup 30s --prompt "Check CI status"
```

**Multi-agent code review (using YAML workflow):**
```yaml
# review.yaml
agents:
  reviewer:
    backend: claude
    system_prompt: You are a code reviewer.
  coder:
    backend: cursor
    system_prompt: You fix issues.
```

```bash
# Run workflow (workflow name from YAML)
agent-worker run review.yaml --tag pr-123

# Interact with agents
agent-worker send reviewer@review:pr-123 "Review recent changes"
agent-worker peek @review:pr-123
```

---

## 📋 Workflow Mode

**Define multi-agent collaboration via YAML.**

### Quick Start

```yaml
# review.yaml
agents:
  reviewer:
    backend: claude
    system_prompt: You are a code reviewer. Provide constructive feedback.

  coder:
    backend: cursor
    model: sonnet-4.5
    system_prompt: You implement code changes based on feedback.

kickoff: |
  @reviewer Review the recent changes and provide feedback.
  @coder Implement the suggested improvements.
```

```bash
# Run once and exit
agent-worker run review.yaml

# Keep agents alive
agent-worker start review.yaml

# With specific tag
agent-worker run review.yaml --tag pr-123
```

### Workflow Structure

```yaml
# Full workflow file structure
name: code-review  # Optional (defaults to filename)

# Agent definitions
agents:
  alice:
    backend: sdk | claude | cursor | codex | mock
    model: anthropic/claude-sonnet-4-5  # Required for SDK backend
    system_prompt: |
      You are Alice, a senior code reviewer.
    # OR
    system_prompt_file: ./prompts/alice.txt

    tools: [bash, read, write]  # CLI backend tool names
    max_tokens: 8000
    max_steps: 20

  bob:
    backend: claude
    system_prompt: You are Bob, a helpful coder.

# Context configuration (shared channel + documents)
context:
  provider: file
  config:
    # Ephemeral (default) - cleared on shutdown
    dir: ./.workflow/${{ workflow.name }}/${{ workflow.tag }}/

    # OR persistent - survives shutdown
    bind: ./data/${{ workflow.tag }}/

# Setup commands (run before kickoff)
setup:
  - shell: git log --oneline -10
    as: recent_commits  # Store output in variable

  - shell: git diff main...HEAD
    as: changes

# Kickoff message (starts the workflow)
kickoff: |
  @alice Review these changes:

  Recent commits:
  ${{ recent_commits }}

  Diff:
  ${{ changes }}

  @bob Stand by for implementation.
```

### Variable Interpolation

Use `${{ variable }}` syntax in kickoff and setup:

```yaml
setup:
  - shell: echo "pr-${{ env.PR_NUMBER }}"
    as: branch_name

kickoff: |
  Workflow: ${{ workflow.name }}
  Tag: ${{ workflow.tag }}
  Branch: ${{ branch_name }}
```

**Available variables**:
- `${{ workflow.name }}` - Workflow name
- `${{ workflow.tag }}` - Instance tag
- `${{ env.VAR }}` - Environment variable
- `${{ task_output }}` - Setup task output (via `as:`)

### Coordination Patterns

**Sequential handoff:**
```yaml
kickoff: |
  @alice Start the task.
```
Alice finishes and mentions: "@bob your turn"

**Parallel execution:**
```yaml
kickoff: |
  @alice @bob @charlie All review this code.
```

**Document-based collaboration:**
```yaml
agents:
  researcher:
    system_prompt: Research and write findings to the shared document.

  summarizer:
    system_prompt: Read the document and create a concise summary.

context:
  provider: file
  config:
    bind: ./results/  # Persistent across runs
```

### Workflow Examples

**PR Review Workflow:**
```yaml
# review.yaml
agents:
  reviewer:
    backend: claude
    system_prompt: |
      Review code for:
      - Bugs and logic errors
      - Code style and readability
      - Performance issues

setup:
  - shell: gh pr diff ${{ env.PR_NUMBER }}
    as: diff

kickoff: |
  @reviewer Review this PR:

  ${{ diff }}

  Provide clear, actionable feedback.
```

```bash
PR_NUMBER=123 agent-worker run review.yaml --tag pr-123
```

**Research & Summarize:**
```yaml
# research.yaml
agents:
  researcher:
    backend: sdk
    model: anthropic/claude-sonnet-4-5
    system_prompt: |
      Research topics thoroughly.
      Write detailed findings to the shared document.

  summarizer:
    backend: sdk
    model: anthropic/claude-haiku-4-5
    system_prompt: |
      Read the document and create:
      - Executive summary (3-5 bullet points)
      - Key findings
      - Recommendations

context:
  provider: file
  config:
    bind: ./research-output/

kickoff: |
  @researcher Research "${{ env.TOPIC }}" and document findings.
  @summarizer Wait for research to complete, then create summary.
```

```bash
TOPIC="AI agent frameworks" agent-worker run research.yaml
```

**Test Generation:**
```yaml
# test-gen.yaml
agents:
  analyzer:
    model: anthropic/claude-sonnet-4-5
    system_prompt: Analyze code and identify test cases.

  generator:
    model: anthropic/claude-sonnet-4-5
    system_prompt: Generate test code based on identified cases.

setup:
  - shell: cat src/main.ts
    as: code

kickoff: |
  @analyzer Analyze this code and identify test cases:
  ${{ code }}

  @generator Generate comprehensive tests based on the analysis.
```

**Consensus Decision:**
```yaml
# consensus.yaml
agents:
  alice:
    system_prompt: You are a cautious reviewer.

  bob:
    system_prompt: You are an optimistic reviewer.

  charlie:
    system_prompt: You balance caution and optimism.

setup:
  - shell: git diff
    as: changes

kickoff: |
  @alice @bob @charlie Review these changes:
  ${{ changes }}

  Each provide your assessment. Use proposal tools to vote on merging.
```

---

## Core Concepts

### Channels (Communication)

All agents in a workflow share a channel. Messages route via `@mentions`:

```bash
# Route to specific agent
agent-worker send alice "analyze this"

# Route to multiple agents (workflow broadcast with @mentions)
agent-worker send @review "@alice @bob collaborate on this"

# Broadcast to workflow (no @mention)
agent-worker send @review "Status update"
```

**Available tools** (in agent's system prompt):
- `channel_send` - Send message to channel
- `channel_read` - Read recent messages
- `inbox_read` - Read own @mentions

### Documents (Shared State)

Agents can read/write to a shared document:

```bash
# Manual document management
agent-worker doc read @review:pr-123
agent-worker doc write @review:pr-123 --content "Analysis complete"
agent-worker doc append @review:pr-123 --file results.txt
```

**Available tools** (in agent's system prompt):
- `document_read` - Read current document
- `document_write` - Overwrite document
- `document_append` - Append to document

### Proposals & Voting

For collaborative decisions:

**Available tools**:
- `proposal_create` - Create proposal (election, decision, approval)
- `vote` - Cast vote on proposal
- `proposal_status` - Check results

**Resolution types**:
- `plurality` - Most votes wins
- `majority` - >50% required
- `unanimous` - All votes must agree

Example usage in agent's tool calls:
```json
{
  "name": "proposal_create",
  "arguments": {
    "title": "Merge PR #123",
    "type": "approval",
    "resolution": "majority"
  }
}
```

---

## Scheduling (Periodic Wakeup)

Agents can wake up periodically when idle:

| Mode | Format | Behavior |
|------|--------|----------|
| **Interval** | `60000`, `30s`, `5m`, `2h` | Fires after idle. Resets on activity. |
| **Cron** | `0 */2 * * *` | Fixed schedule. NOT reset by activity. |

```bash
# At creation
agent-worker new --wakeup 5m
agent-worker new --wakeup "0 */2 * * *" --wakeup-prompt "Check for updates"

# Runtime management
agent-worker schedule <target> set 5m
agent-worker schedule <target> set "0 */2 * * *" -p "Health check"
agent-worker schedule <target> get
agent-worker schedule <target> clear
```

---

## Tool Management (SDK Backend Only)

### Specifying Tools at Creation

Tools are specified when creating an agent using the `--tool` parameter:

```bash
# Create agent with custom tools
agent-worker new alice --tool ./my-tools.ts

# Combine with skills
agent-worker new alice --skill ./skills --tool ./tools.ts
```

### Tool File Format

```typescript
// my-tools.ts
export default [
  {
    name: 'search_docs',
    description: 'Search documentation',
    parameters: {
      type: 'object',
      properties: {
        query: { type: 'string', description: 'Search query' }
      },
      required: ['query']
    },
    needsApproval: false,  // Optional: require approval before execution
    execute: async (args) => {
      return { results: ['doc1', 'doc2'] }
    }
  }
]
```

### Mocking Tools (Testing)

```bash
# Mock tool response for testing
agent-worker mock tool get_weather '{"temp": 72, "condition": "sunny"}'

# View agent feedback/observations
agent-worker feedback alice
```

### Approval Workflow

For tools marked `needsApproval`:

```bash
agent-worker send a0 "Delete /tmp/test.txt"
agent-worker pending
agent-worker approve <id>
agent-worker deny <id> -r "Path not allowed"
```

---

## Model Formats

SDK backend supports multiple formats:

```bash
# Gateway format (recommended)
agent-worker new -m openai/gpt-4.5
agent-worker new -m anthropic/claude-sonnet-4-5

# Provider-only (uses frontier model)
agent-worker new -m openai
agent-worker new -m anthropic

# Direct provider format
agent-worker new -m deepseek:deepseek-chat
```

Check available providers:
```bash
agent-worker providers
```

---

## Programmatic Usage (SDK)

For TypeScript/JavaScript integration:

```typescript
import { AgentSession } from 'agent-worker'

const session = new AgentSession({
  model: 'anthropic/claude-sonnet-4-5',
  system: 'You are a helpful assistant.',
  tools: [/* your tools */]
})

// Send message
const response = await session.send('Hello')
console.log(response.content)
console.log(response.toolCalls)
console.log(response.usage)

// Stream response
for await (const chunk of session.sendStream('Tell me a story')) {
  process.stdout.write(chunk)
}

// State management
const state = session.getState()
// Later: restore from state
```

### With Skills

```typescript
import { AgentSession, SkillsProvider, createSkillsTool } from 'agent-worker'

const skillsProvider = new SkillsProvider()
await skillsProvider.scanDirectory('.agents/skills')

const session = new AgentSession({
  model: 'anthropic/claude-sonnet-4-5',
  system: 'You are a helpful assistant.',
  tools: [createSkillsTool(skillsProvider)]
})
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "No active agent" | Run `agent-worker new` first |
| "Agent not found" | Check `agent-worker ls` |
| "Tool management not supported" | Use SDK backend (default) |
| "Provider not loaded" | Check API key: `agent-worker providers` |
| Agent not responding | Check status: `agent-worker status <target>` |
| No response in peek | Agent still processing. Wait and retry. |
| Workflow file errors | Validate YAML syntax |

---

## Command Reference

```
# Agent Management
agent-worker new [name]              Create agent (auto-names if omitted)
  -m, --model <model>                Model (SDK backend)
  -b, --backend <type>               Backend: sdk, claude, cursor, codex, mock
  -s, --system <prompt>              System prompt
  -f, --system-file <path>           System prompt from file
  --tool <file>                      Import MCP tools from file (SDK backend)
  --wakeup <interval|cron>           Periodic wakeup schedule
  --wakeup-prompt <text>             Prompt for wakeup
  --idle-timeout <ms>                Idle timeout (0 = no timeout)

agent-worker ls [target]             List agents (default: global)
  --all                              Show agents from all workflows

agent-worker status <target>         Check agent status
agent-worker stop <target>           Stop agent
  --all                              Stop all agents
  Target: agent, agent@workflow:tag, or @workflow:tag

# Communication
agent-worker send <target> <message> Send to agent or workflow
  Target examples:
    alice                            Send to alice@global:main
    alice@review                     Send to alice@review:main
    alice@review:pr-123              Send to specific workflow:tag
    @review                          Broadcast to review workflow
    @review:pr-123                   Broadcast to workflow:tag

agent-worker peek [target]           View channel messages
  Target: agent@workflow:tag or @workflow:tag (default: @global)
  --all                              Show all messages
  -n, --last <count>                 Show last N messages
  --find <text>                      Search messages

# Per-agent Operations
agent-worker stats <target>          Show statistics
agent-worker export <target>         Export transcript
agent-worker clear <target>          Clear history

# Scheduling
agent-worker schedule <target> set <interval> [options]
agent-worker schedule <target> get
agent-worker schedule <target> clear

# Documents
agent-worker doc read <target>
agent-worker doc write <target> --content <text>
agent-worker doc append <target> --file <path>
  Target: @workflow:tag (e.g., @review:pr-123)

# Testing & Debugging
agent-worker mock tool <name> <response>  Mock tool response (SDK backend)
agent-worker feedback [target]            View agent feedback/observations

# Approvals
agent-worker pending                 List pending approvals
agent-worker approve <id>            Approve tool call
agent-worker deny <id> -r <reason>   Deny tool call

# Workflows (YAML)
agent-worker run <file>              Run workflow (exit on complete)
  --tag <tag>                        Workflow instance tag (default: main)
  --json                             JSON output
  --debug                            Show debug logs
  --feedback                         Enable feedback tool
  Note: Workflow name inferred from YAML 'name' field or filename

agent-worker start <file>            Start workflow (keep running)
  --tag <tag>                        Workflow instance tag (default: main)
  --background                       Run in background
  Note: Workflow name inferred from YAML 'name' field or filename

# Utilities
agent-worker providers               Check SDK providers
agent-worker backends                Check available backends
```

---

## Remember

**Two modes, same model**:
- **Agent Mode**: Manual CLI control, perfect for exploration
- **Workflow Mode**: Declarative YAML, perfect for automation

Both use:
- **workflow:tag** for namespacing and isolation
- **Channels** for @mention-based communication
- **Documents** for shared state
- **Proposals** for collaborative decisions

Choose the mode that fits your task. Mix and match as needed.
