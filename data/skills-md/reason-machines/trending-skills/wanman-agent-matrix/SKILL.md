---
name: wanman-agent-matrix
description: Expert skill for using wanman, the open-source local agent matrix runtime that coordinates multiple Claude Code or Codex agents on your machine.
triggers:
  - set up wanman agent matrix
  - run multiple claude code agents
  - coordinate agents with wanman
  - wanman takeover my repo
  - send messages between agents wanman
  - wanman task management
  - orchestrate codex agents locally
  - wanman supervisor setup
---

# wanman Agent Matrix Runtime

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

wanman is an open-source local agent matrix framework that runs a supervised network of Claude Code or Codex agents on your machine, coordinated through a JSON-RPC supervisor. Inspired by Japanese ワンマン電車 (one-man trains), it lets the human step back into an observer role while agents collaborate autonomously.

## Installation & Setup

### Prerequisites

- Node.js 20+
- pnpm 9+
- git
- A logged-in Claude Code or Codex CLI

### Install from Source

```bash
git clone git@github.com:chekusu/wanman.git wanman.dev
cd wanman.dev
pnpm install
pnpm build

# Run the CLI directly
pnpm --filter @wanman/cli exec wanman takeover /path/to/any/git/repo
```

### Single-file Bundle

```bash
pnpm --filter @wanman/cli standalone
node packages/cli/dist/wanman.mjs takeover /path/to/any/git/repo
```

### Add to PATH

After building, symlink or alias the CLI so you can run `wanman` from any project:

```bash
# Example: add to PATH via shell profile
export PATH="$PATH:/path/to/wanman.dev/packages/cli/dist"
# Then from inside any git repo:
wanman takeover .
```

## Key CLI Commands

| Command | Description |
|---------|-------------|
| `wanman takeover <path>` | Take over an existing git repo with the full agent matrix |
| `wanman run <goal>` | Start an agent matrix for a one-shot goal |
| `wanman send <agent> <msg>` | Send a message to an agent (`--steer` interrupts target) |
| `wanman recv [--agent <name>]` | Receive and mark pending messages as delivered |
| `wanman agents` | List registered agents and their current states |
| `wanman escalate <msg>` | Escalate a message to the CEO agent |
| `wanman watch` | Live-stream supervisor and agent activity |
| `wanman task create` | Create a task in the shared pool |
| `wanman task list` | List all tasks |
| `wanman task get <id>` | Get task details |
| `wanman task update <id>` | Update task status/fields |
| `wanman task done <id>` | Mark a task as complete |
| `wanman initiative create` | Create a long-lived initiative |
| `wanman initiative list` | List initiatives |
| `wanman capsule create` | Create a change capsule |
| `wanman capsule list` | List change capsules |
| `wanman capsule mine` | List capsules owned by current agent |
| `wanman artifact put` | Store a structured artifact |
| `wanman artifact list` | List stored artifacts |
| `wanman artifact get <id>` | Retrieve an artifact |
| `wanman hypothesis create` | Create a hypothesis to track |
| `wanman hypothesis list` | List hypotheses |
| `wanman hypothesis update <id>` | Update hypothesis status |
| `wanman context get <key>` | Read a shared context value |
| `wanman context set <key> <val>` | Write a shared context value |
| `wanman skill:check [path]` | Validate skill docs reference real CLI commands |

## Configuration

### Environment Variables

```bash
# Supervisor HTTP URL for the CLI (default: http://localhost:3120)
export WANMAN_URL=http://localhost:3120

# Identifies the current agent (set inside agent processes)
export WANMAN_AGENT_NAME=dev

# Select runtime: 'claude' (default) or 'codex'
export WANMAN_RUNTIME=claude

# Model overrides
export WANMAN_MODEL=claude-opus-4-5
export WANMAN_CODEX_MODEL=o4-mini
export WANMAN_CODEX_REASONING_EFFORT=high

# Bias Codex adapter toward lower-latency defaults
export WANMAN_CODEX_FAST=1

# Override where runtime materializes skill-activation snapshots
export WANMAN_SKILL_SNAPSHOTS_DIR=/tmp/my-skill-snapshots
```

### Agent Configuration File

Agent definitions live in a single JSON file (typically `.wanman/config.json`):

```json
{
  "agents": [
    {
      "name": "ceo",
      "lifecycle": "24/7",
      "model": "high",
      "systemPrompt": "You are the CEO agent. Coordinate all other agents, prioritize tasks, and escalate blockers."
    },
    {
      "name": "dev",
      "lifecycle": "on-demand",
      "model": "standard",
      "systemPrompt": "You are the dev agent. Implement features, fix bugs, and write tests."
    },
    {
      "name": "devops",
      "lifecycle": "on-demand",
      "model": "standard",
      "systemPrompt": "You are the devops agent. Manage CI/CD, infrastructure, and deployments."
    },
    {
      "name": "researcher",
      "lifecycle": "idle_cached",
      "model": "standard",
      "systemPrompt": "You are the research agent. Gather market data and synthesize findings."
    }
  ],
  "dbPath": ".wanman/wanman.db",
  "port": 3120,
  "workspaceRoot": ".wanman/agents"
}
```

### Agent Lifecycle Options

- **`24/7`** — Continuous respawn loop; agent always running.
- **`on-demand`** — Idle until triggered by a message or task.
- **`idle_cached`** — Idle until triggered, but preserves Claude `session_id` across triggers via `claude --resume`. **Claude-only** — pairing with `codex` runtime is rejected at startup.

### Model Tiers

- **`high`** — Maps to highest-capability model for the selected runtime.
- **`standard`** — Maps to balanced default model; overridable via `WANMAN_MODEL` or `WANMAN_CODEX_MODEL`.

## Architecture Overview

```
+----------------+          +--------------------+          +-----------------+
|  wanman CLI    |  JSON    |  Supervisor        |  spawn   |  Agent process  |
|  (host shell)  | ---RPC-->|  (local process)   | -------> |  (Claude/Codex) |
|                |  /rpc    |  message/context/  |          |  per-agent $HOME|
|                |          |  task/artifact     |          |  per-agent wt   |
+----------------+          +--------------------+          +-----------------+
                                    |                              |
                                    v                              v
                           +--------------------+        +-----------------+
                           |  files + SQLite    |        |  worktree       |
                           +--------------------+        +-----------------+
```

- The CLI communicates with the Supervisor via **JSON-RPC 2.0** over HTTP.
- The Supervisor owns: message store, context store, task pool, artifact store, and spawns child agent processes.
- Each agent runs in an **isolated per-agent worktree** and **per-agent `$HOME`**, so agents never mutate your working directory or shell profile.

## Common Patterns & Workflows

### Pattern 1: Take Over an Existing Repo

```bash
# From inside the repo you want agents to work on:
cd /path/to/my-project
wanman takeover .

# Watch the agents coordinate in real time:
wanman watch
```

### Pattern 2: Send a Goal and Monitor Progress

```bash
# Launch agents against a specific goal
wanman run "Refactor the authentication module to use JWT tokens"

# In another terminal, watch activity stream
wanman watch

# Check agent states
wanman agents

# Escalate to CEO if blocked
wanman escalate "Dev agent is stuck on the JWT library choice, please decide"
```

### Pattern 3: Inter-Agent Messaging

```bash
# Send a normal message to the dev agent
wanman send dev "Please add unit tests for the UserService class"

# Send a steering (interrupt) message to the dev agent
wanman send dev --steer "STOP current task. Critical bug in auth — fix login endpoint first"

# Receive messages as the dev agent
WANMAN_AGENT_NAME=dev wanman recv

# Receive all pending messages for any agent
wanman recv
```

### Pattern 4: Task Pool Management

```bash
# Create a task with a dependency on task ID abc123
wanman task create \
  --title "Write integration tests" \
  --description "Cover all API endpoints with integration tests" \
  --agent dev \
  --after abc123

# List all tasks and their statuses
wanman task list

# Get details of a specific task
wanman task get <task-id>

# Update task status
wanman task update <task-id> --status in-progress

# Mark complete
wanman task done <task-id>
```

### Pattern 5: Shared Context Store

```bash
# Store shared context accessible to all agents
wanman context set api_base_url "https://api.example.com/v2"
wanman context set target_environment "staging"

# Read context values
wanman context get api_base_url

# Agents read context in their prompts automatically via the supervisor
```

### Pattern 6: Artifact Storage

```bash
# Store a structured artifact (e.g., research output)
wanman artifact put \
  --name "market-analysis-q2" \
  --type "report" \
  --content "$(cat analysis.md)"

# List artifacts
wanman artifact list

# Retrieve a specific artifact
wanman artifact get <artifact-id>
```

### Pattern 7: Hypothesis Tracking

```bash
# Create a hypothesis for agents to validate
wanman hypothesis create \
  --title "Switching to Bun runtime reduces build time by 40%" \
  --description "Based on benchmarks from similar TypeScript projects"

# List hypotheses and their validation status
wanman hypothesis list

# Update after validation
wanman hypothesis update <id> --status confirmed --evidence "Build time dropped from 45s to 26s"
```

### Pattern 8: Change Capsules

```bash
# Create a change capsule (bounded unit of work/change)
wanman capsule create \
  --title "Auth JWT migration" \
  --description "Migrate session-based auth to JWT"

# List all capsules
wanman capsule list

# List capsules owned by the current agent
WANMAN_AGENT_NAME=dev wanman capsule mine

# Get details
wanman capsule get <capsule-id>
```

## TypeScript Integration (Host SDK)

Embed wanman into your own tools using the `@wanman/host-sdk` package:

```typescript
import { WanmanClient } from '@wanman/host-sdk';

// Connect to a running supervisor
const client = new WanmanClient({
  url: process.env.WANMAN_URL ?? 'http://localhost:3120',
});

// Send a message programmatically
await client.send({
  agent: 'dev',
  message: 'Please review the PR and add inline comments',
  steer: false,
});

// Create a task
const task = await client.task.create({
  title: 'Fix flaky tests',
  description: 'Tests in auth.test.ts fail intermittently under CI',
  agent: 'dev',
});

// Poll for agent status
const agents = await client.agents.list();
for (const agent of agents) {
  console.log(`${agent.name}: ${agent.state}`);
}

// Store an artifact
await client.artifact.put({
  name: 'perf-baseline',
  type: 'benchmark',
  content: JSON.stringify(perfResults),
});

// Read shared context
const env = await client.context.get('target_environment');
```

## Project Structure

```
wanman.dev/
  packages/
    cli/          # wanman CLI (send/recv/task/artifact/run/takeover/...)
    core/         # Shared types, JSON-RPC protocol, skills (core/skills/)
    host-sdk/     # Host-side SDK for embedding wanman into other tools
    runtime/      # Supervisor, agent process manager, SQLite stores, adapters
  docs/
    quickstart.md
    architecture.md
  CONTRIBUTING.md
```

### Built-in Shared Skills (`packages/core/skills/`)

Skills are auto-discovered by agents at `~/.claude/skills/`:

- **`artifact-naming`** — Conventions for naming agent-produced artifacts.
- **`artifact-quality`** — Quality standards for artifacts.
- **`cross-validation`** — CEO consistency checks across agent outputs.
- **`research-methodology`** — Market/data research methodology.
- **`wanman-cli`** — CLI command reference consumed by agents at runtime.
- **`workspace-conventions`** — File-system conventions inside agent workspaces.

### Validate Skills

```bash
# Check that skill docs only reference real CLI commands
wanman skill:check
wanman skill:check packages/core/skills/wanman-cli.md
```

## Testing

```bash
# Type checking
pnpm typecheck

# Run all tests
pnpm test

# Run tests with coverage (target: 90%+ line coverage)
pnpm exec vitest run \
  --coverage \
  --coverage.reporter=text-summary \
  --coverage.reporter=json-summary \
  --coverage.exclude='**/dist/**'

# Coverage summary written to: coverage/coverage-summary.json
```

## Troubleshooting

### Supervisor Not Reachable

```bash
# Check if supervisor is running on expected port
curl http://localhost:3120/rpc

# Override URL if running on a non-default port
export WANMAN_URL=http://localhost:4000
wanman agents
```

### Agent Stuck / Not Responding

```bash
# Check agent states
wanman agents

# Send a steer message to interrupt and redirect
wanman send <agent-name> --steer "Reset and await new instructions"

# Escalate to CEO for intervention
wanman escalate "Agent 'dev' appears stuck on task <task-id>, please reassign"

# Watch live activity to diagnose
wanman watch
```

### `idle_cached` Lifecycle with Wrong Runtime

```
Error: idle_cached lifecycle requires Claude runtime; codex has no resume mechanism
```

**Fix:** Only use `lifecycle: "idle_cached"` when `WANMAN_RUNTIME=claude` (or unset, as Claude is the default). Switch lifecycle to `on-demand` for Codex agents.

### Agents Mutating Wrong Directory

Each agent runs in its own **git worktree** under `workspaceRoot` (default: `.wanman/agents/`). If an agent appears to be modifying wrong files, check `workspaceRoot` in your config and ensure `WANMAN_AGENT_NAME` is set correctly in agent subprocesses.

### SQLite Lock Errors

If the supervisor crashes mid-run, the SQLite file at `dbPath` may be locked:

```bash
# Stop all wanman processes
pkill -f wanman

# Remove WAL files if present
rm .wanman/wanman.db-wal .wanman/wanman.db-shm

# Restart supervisor
wanman takeover .
```

### Skill Validation Failures

```bash
# Run skill:check to find references to non-existent commands
wanman skill:check

# Output will show which skill files reference invalid commands
# Update the skill markdown to use only real wanman CLI commands
```

## Further Reading

- [Quickstart Guide](docs/quickstart.md) — First-run walkthrough against any git repo.
- [Architecture Deep Dive](docs/architecture.md) — Agent lifecycle, JSON-RPC, stores, adapters, brain/persistence.
- [Contributing Guide](CONTRIBUTING.md) — Tests, typecheck, commit conventions.
- [wanman.ai](https://wanman.ai) — Hosted 24/7 sandbox edition with dynamic roles and global search.
