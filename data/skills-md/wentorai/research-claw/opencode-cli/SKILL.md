---
name: opencode-cli
description: >
  Reference for using OpenCode CLI to handle complex coding tasks.
  Use when Research-Claw needs to delegate multi-file projects, code generation,
  or iterative debugging to a multi-provider AI coding tool.
  Trigger words: opencode, coding CLI, delegate coding, multi-provider agent.
---

# OpenCode CLI

Terminal-based AI coding agent supporting multiple LLM providers (OpenAI, Anthropic, Google, local models). Features a TUI for interactive use and `run` command for automation.

## Detect Installation

```bash
which opencode  # should return a path
opencode --version
```

## Install

```bash
# Recommended (automated)
curl -fsSL https://opencode.ai/install | bash

# npm
npm install -g opencode-ai

# Homebrew (macOS/Linux)
brew install anomalyco/tap/opencode

# pnpm
pnpm install -g opencode-ai
```

Requires API keys for your chosen LLM provider (configured via `/init` on first run).

## Non-Interactive Usage (run)

For programmatic invocation from Research-Claw, use `opencode run`:

```bash
# Basic non-interactive execution
opencode run "Refactor the auth module to use dependency injection"

# With model selection (provider/model format)
opencode run -m anthropic/claude-sonnet-4-20250514 "Fix all type errors"

# Attach files for context
opencode run -f src/config.ts -f README.md "Update the config schema"

# JSON output for parsing
opencode run --format json "List all exported functions"

# Continue a previous session
opencode run -c "Now add tests for what you just implemented"

# Continue a specific session
opencode run -s <session-id> "Fix the remaining issues"
```

## Key Flags

| Flag | Description |
|------|-------------|
| `-m, --model <provider/model>` | Model in `provider/model` format |
| `-f, --file <path>` | Attach file(s) to the message (repeatable) |
| `--format <fmt>` | Output format: `default` or `json` |
| `-c, --continue` | Continue last session |
| `-s, --session <id>` | Continue a specific session by ID |
| `--fork` | Fork session when continuing (new branch) |
| `--share` | Share the session |
| `--agent <name>` | Specify which agent to use |
| `--attach <url>` | Connect to running server (e.g. `http://localhost:4096`) |
| `--log-level <level>` | `DEBUG` / `INFO` / `WARN` / `ERROR` |

## Research-Claw exec Patterns

```bash
# Delegate a complex coding task
exec("opencode run -m anthropic/claude-sonnet-4-20250514 'Implement the feature described in TODO.md'")

# With file attachments for context
exec("opencode run -f README.md -f src/schema.ts 'Add validation based on the schema'")

# JSON output for structured results
exec("opencode run --format json 'List all API endpoints in this project'")

# Using persistent server for multiple tasks
exec("opencode run --attach http://localhost:4096 'Run the test suite and fix failures'")
```

## Docs

- CLI docs: https://opencode.ai/docs/cli/
- Getting started: https://opencode.ai/docs
