---
name: free-code-claude-cli
description: Build and use free-code, the open-source fork of Claude Code CLI with telemetry removed, guardrails stripped, and all experimental features unlocked.
triggers:
  - set up free-code claude cli
  - install free-code terminal agent
  - use free-code with openai bedrock vertex
  - enable experimental features free-code
  - build free-code from source
  - configure free-code model provider
  - unlock ultrathink ultraplan features
  - strip telemetry from claude code
---

# free-code Claude CLI

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

free-code is a buildable fork of Anthropic's Claude Code CLI — a terminal-native AI coding agent. It removes all telemetry and phone-home callbacks, strips Anthropic's injected system-prompt guardrails, and unlocks 54 experimental feature flags that are disabled in the public npm release. It supports five model providers: Anthropic, OpenAI Codex, AWS Bedrock, Google Vertex AI, and Anthropic Foundry.

---

## Installation

### One-liner (recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/paoloanzn/free-code/main/install.sh | bash
```

This installs Bun if needed, clones the repo, builds with experimental features, and symlinks `free-code` on your `PATH`.

### Manual build

```bash
# Requires Bun >= 1.3.11
curl -fsSL https://bun.sh/install | bash

git clone https://github.com/paoloanzn/free-code.git
cd free-code
bun run build
./cli
```

---

## Key CLI Commands

```bash
# Start interactive REPL
free-code

# One-shot prompt
free-code -p "explain this codebase"

# Specify model
free-code --model claude-opus-4-6

# OAuth login (runs /login slash command)
free-code /login

# Run from source (slower, no build step)
bun run dev
```

### Slash commands inside the REPL

```
/login          Authenticate with your chosen provider
/help           List all available commands
/clear          Clear conversation context
/compact        Compact context window
/memory         View/edit memory files
```

---

## Build Variants

| Command | Output | Features |
|---|---|---|
| `bun run build` | `./cli` | VOICE_MODE only (production-like) |
| `bun run build:dev` | `./cli-dev` | VOICE_MODE only, dev stamp |
| `bun run build:dev:full` | `./cli-dev` | All 54 experimental flags unlocked |
| `bun run compile` | `./dist/cli` | Alternative output path |

### Enable specific feature flags

```bash
# Unlock ultrathink + ultraplan only
bun run ./scripts/build.ts --feature=ULTRATHINK --feature=ULTRAPLAN

# Dev build with bridge mode added
bun run ./scripts/build.ts --dev --feature=BRIDGE_MODE

# Full experimental unlock
bun run build:dev:full
```

---

## Model Provider Configuration

Switch providers entirely via environment variables — no code changes needed.

### Anthropic (default)

```bash
export ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY"
free-code --model claude-opus-4-6
```

Available models: `claude-opus-4-6`, `claude-sonnet-4-6`, `claude-haiku-4-5`

Override model defaults:

```bash
export ANTHROPIC_DEFAULT_OPUS_MODEL="claude-opus-4-6"
export ANTHROPIC_DEFAULT_SONNET_MODEL="claude-sonnet-4-6"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="claude-haiku-4-5"
export ANTHROPIC_BASE_URL="https://api.anthropic.com"  # custom endpoint
```

### OpenAI Codex

```bash
export CLAUDE_CODE_USE_OPENAI=1
free-code --model gpt-5.3-codex
```

Available models: `gpt-5.3-codex`, `gpt-5.4`, `gpt-5.4-mini`

### AWS Bedrock

```bash
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION="us-east-1"
# Uses standard AWS credential chain: env vars, ~/.aws/config, or IAM role
free-code
```

Additional Bedrock variables:

```bash
export ANTHROPIC_BEDROCK_BASE_URL="https://..."   # custom endpoint
export AWS_BEARER_TOKEN_BEDROCK="$TOKEN"           # bearer token auth
export CLAUDE_CODE_SKIP_BEDROCK_AUTH=1             # skip auth (testing only)
```

### Google Cloud Vertex AI

```bash
# Authenticate first
gcloud auth application-default login

export CLAUDE_CODE_USE_VERTEX=1
free-code
```

### Anthropic Foundry

```bash
export CLAUDE_CODE_USE_FOUNDRY=1
export ANTHROPIC_FOUNDRY_API_KEY="$ANTHROPIC_FOUNDRY_API_KEY"
free-code --model my-deployment-id
```

---

## Experimental Features Reference

Build with `bun run build:dev:full` to unlock all 54 flags, or pass `--feature=FLAG` individually.

### High-value flags

| Flag | What it does |
|---|---|
| `ULTRATHINK` | Type "ultrathink" in a prompt to boost reasoning depth |
| `ULTRAPLAN` | Remote multi-agent planning (Opus-class) via Claude Code web |
| `VOICE_MODE` | Push-to-talk voice input and dictation |
| `TOKEN_BUDGET` | Real-time token budget tracking and warnings |
| `HISTORY_PICKER` | Interactive prompt history picker |
| `EXTRACT_MEMORIES` | Auto-extracts memories after each query |
| `VERIFICATION_AGENT` | Validation agent that checks task completion |
| `AGENT_TRIGGERS` | Local cron/trigger tools for background automation |
| `BRIDGE_MODE` | IDE remote-control bridge (VS Code, JetBrains) |
| `BASH_CLASSIFIER` | AI-assisted bash permission decisions |
| `BUILTIN_EXPLORE_PLAN_AGENTS` | Preset explore/plan agent configs |
| `TEAMMEM` | Team-shared memory files with watcher hooks |
| `COMPACTION_REMINDERS` | Smart reminders around context window compaction |

---

## Environment Variables Quick Reference

```bash
# Authentication
ANTHROPIC_API_KEY              # Anthropic API key
ANTHROPIC_AUTH_TOKEN           # Alternative auth token
CLAUDE_CODE_OAUTH_TOKEN        # OAuth token via env (skips /login)

# Provider selection
CLAUDE_CODE_USE_OPENAI=1       # Switch to OpenAI Codex
CLAUDE_CODE_USE_BEDROCK=1      # Switch to AWS Bedrock
CLAUDE_CODE_USE_VERTEX=1       # Switch to Google Vertex AI
CLAUDE_CODE_USE_FOUNDRY=1      # Switch to Anthropic Foundry

# Model overrides
ANTHROPIC_MODEL                # Override default model for session
ANTHROPIC_BASE_URL             # Custom API base URL

# Tuning
CLAUDE_CODE_API_KEY_HELPER_TTL_MS  # API key helper cache TTL in ms
```

---

## Project Structure

```
scripts/
  build.ts              # Build script — feature flag injection lives here

src/
  entrypoints/cli.tsx   # CLI entry — Commander.js setup, arg parsing
  commands.ts           # Slash command registry
  tools.ts              # Agent tool registry
  QueryEngine.ts        # Core LLM query orchestration
  screens/REPL.tsx      # Interactive terminal UI (React + Ink)

  commands/             # /slash command implementations
  tools/                # Agent tools: Bash, Read, Edit, Glob, Grep, etc.
  components/           # Ink/React terminal UI components
  services/
    api/                # Anthropic + Codex API clients
    oauth/              # OAuth flows (Anthropic, OpenAI)
  state/                # Global app state store
  utils/model/          # Model config, provider routing, validation
  bridge/               # IDE bridge (BRIDGE_MODE)
  voice/                # Voice input (VOICE_MODE)
  skills/               # Skill system
  plugins/              # Plugin system
  tasks/                # Background task management
```

---

## Common Patterns

### Use ultrathink for hard problems

After building with `--feature=ULTRATHINK`:

```
> ultrathink refactor this authentication module to use JWTs
```

The keyword `ultrathink` in your prompt triggers extended reasoning mode.

### Pipe files into one-shot mode

```bash
cat src/auth.ts | free-code -p "find security issues in this file"
free-code -p "write tests for $(cat src/utils.ts)"
```

### Run with a specific provider per session

```bash
# One-off Bedrock session without changing env permanently
CLAUDE_CODE_USE_BEDROCK=1 AWS_REGION=eu-west-1 free-code

# One-off Vertex session
CLAUDE_CODE_USE_VERTEX=1 free-code -p "review this PR diff"
```

### Custom build for CI with minimal features

```typescript
// scripts/build.ts accepts --feature flags
// Build only what you need for a headless CI agent:
// bun run ./scripts/build.ts --feature=VERIFICATION_AGENT --feature=AGENT_TRIGGERS
```

---

## Troubleshooting

### `bun: command not found`

```bash
curl -fsSL https://bun.sh/install | bash
source ~/.bashrc  # or ~/.zshrc
```

### `free-code: command not found` after install

The install script symlinks to your PATH. If it's missing:

```bash
cd free-code
ln -sf "$(pwd)/cli" /usr/local/bin/free-code
```

### Build fails on experimental flags

Some of the 88 flags don't compile cleanly. Use `build:dev:full` which only enables the 54 working flags. For broken flags, check `FEATURES.md` for reconstruction notes:

```bash
# Safe full-unlock build (54 working flags only)
bun run build:dev:full
```

### Authentication errors with Bedrock

Verify your AWS credential chain is working independently:

```bash
aws sts get-caller-identity
# If this fails, fix AWS credentials before setting CLAUDE_CODE_USE_BEDROCK=1
```

### Vertex AI auth errors

```bash
gcloud auth application-default login
gcloud auth application-default print-access-token  # verify it works
export CLAUDE_CODE_USE_VERTEX=1
free-code
```

### Context window fills up quickly

Enable compaction reminders and use the `/compact` command:

```bash
bun run ./scripts/build.ts --feature=COMPACTION_REMINDERS
# Inside REPL when warned:
/compact
```

---

## IPFS Fallback

If the GitHub repo is unavailable, the full source is permanently mirrored:

```
CID: bafybeiegvef3dt24n2znnnmzcud2vxat7y7rl5ikz7y7yoglxappim54bm
URL: https://w3s.link/ipfs/bafybeiegvef3dt24n2znnnmzcud2vxat7y7rl5ikz7y7yoglxappim54bm
```
