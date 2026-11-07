---
name: codex-plugin-cc
description: Use OpenAI Codex from inside Claude Code for code reviews and delegated background tasks.
triggers:
  - "review my code with Codex"
  - "run a Codex review"
  - "delegate a task to Codex"
  - "use Codex to investigate a bug"
  - "set up the Codex plugin for Claude Code"
  - "run an adversarial review with Codex"
  - "check status of background Codex job"
  - "install codex plugin claude code"
---

# Codex Plugin for Claude Code

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

A Claude Code plugin that lets you run OpenAI Codex code reviews and delegate background tasks to Codex directly from your Claude Code session. Use it for read-only code reviews, adversarial design challenges, and handing off investigative or fix tasks to Codex as a subagent.

---

## What It Does

- `/codex:review` — Standard read-only Codex code review of uncommitted changes or a branch diff
- `/codex:adversarial-review` — Steerable review that challenges design decisions, tradeoffs, and assumptions
- `/codex:rescue` — Delegate a task (bug investigation, fix, etc.) to Codex as a background subagent
- `/codex:status` — Check progress of background Codex jobs
- `/codex:result` — Retrieve output from a finished job (includes Codex session ID for `codex resume`)
- `/codex:cancel` — Cancel an active background job
- `/codex:setup` — Verify Codex is installed and authenticated; optionally enable/disable the review gate

---

## Requirements

- Node.js 18.18 or later
- A ChatGPT subscription (Free tier works) **or** an OpenAI API key
- Claude Code with plugin support

---

## Installation

### 1. Add the marketplace and install the plugin

```bash
/plugin marketplace add openai/codex-plugin-cc
/plugin install codex@openai-codex
/reload-plugins
```

### 2. Verify setup

```bash
/codex:setup
```

If Codex CLI is missing, `/codex:setup` can install it for you via npm, or install manually:

```bash
npm install -g @openai/codex
```

### 3. Authenticate with Codex

```bash
!codex login
```

Supports ChatGPT account login or API key. Your existing Codex CLI authentication is reused automatically if already logged in.

---

## Key Commands

### `/codex:review`

Runs a standard read-only Codex review on your current work.

```bash
# Review uncommitted changes
/codex:review

# Review diff against a base branch
/codex:review --base main

# Run in the background (recommended for multi-file changes)
/codex:review --background

# Run and wait inline
/codex:review --wait
```

### `/codex:adversarial-review`

Challenges implementation decisions, tradeoffs, and hidden assumptions. Accepts optional free-text focus after flags.

```bash
# Basic adversarial review
/codex:adversarial-review

# Target a branch diff with a specific focus
/codex:adversarial-review --base main challenge whether this caching approach was correct

# Run in background, focus on race conditions
/codex:adversarial-review --background look for race conditions and question the retry design
```

### `/codex:rescue`

Hands off a task to Codex via the `codex:codex-rescue` subagent.

```bash
# Investigate a failing test
/codex:rescue investigate why the tests started failing

# Apply a minimal fix
/codex:rescue fix the failing test with the smallest safe patch

# Resume the most recent Codex session for this repo
/codex:rescue --resume apply the top fix from the last run

# Start fresh (ignore previous session)
/codex:rescue --fresh investigate the regression

# Use a specific model and effort level
/codex:rescue --model gpt-5.4-mini --effort medium investigate the flaky integration test

# Use the faster "spark" model (maps to gpt-5.3-codex-spark)
/codex:rescue --model spark fix the issue quickly

# Run in the background
/codex:rescue --background investigate why the build is failing in CI
```

You can also trigger rescue via natural language to Claude:

```text
Ask Codex to redesign the database connection to be more resilient.
```

### `/codex:status`

```bash
# List all running and recent jobs for this repo
/codex:status

# Check a specific job
/codex:status task-abc123
```

### `/codex:result`

```bash
# Get result of the most recent finished job
/codex:result

# Get result for a specific job
/codex:result task-abc123
```

Output includes a Codex session ID. Resume that session directly in Codex:

```bash
codex resume <session-id>
```

### `/codex:cancel`

```bash
# Cancel the most recent active job
/codex:cancel

# Cancel a specific job
/codex:cancel task-abc123
```

### `/codex:setup` — Review Gate

```bash
# Enable the stop hook review gate
/codex:setup --enable-review-gate

# Disable it
/codex:setup --disable-review-gate
```

> **Warning:** The review gate runs a Codex review on every Claude response and blocks the stop if issues are found. This can trigger long Claude/Codex loops and drain usage limits. Only enable it when actively monitoring the session.

---

## Configuration

The plugin uses the same `config.toml` as the Codex CLI. Configuration is layered:

| Location | Scope |
|---|---|
| `~/.codex/config.toml` | User-level defaults |
| `.codex/config.toml` (project root) | Project-level overrides (requires trusted project) |

### Example: Set default model and effort for a project

```toml
# .codex/config.toml
model = "gpt-5.4-mini"
model_reasoning_effort = "xhigh"
```

### Example: Point to a custom OpenAI-compatible endpoint

```toml
# ~/.codex/config.toml
openai_base_url = "https://your-custom-endpoint.example.com/v1"
```

API keys and authentication are managed via `codex login` — do not hardcode keys in config files. The CLI reads from the authenticated session or from the `OPENAI_API_KEY` environment variable.

---

## Common Patterns

### Review before shipping

```bash
/codex:review --base main
```

### Start a long-running review, check back later

```bash
/codex:adversarial-review --background look for auth and data-loss risks
/codex:status
/codex:result
```

### Delegate a bug investigation and resume in Codex

```bash
/codex:rescue --background investigate why the integration test is flaky
# ... later ...
/codex:result
# Copy session ID from output, then:
codex resume <session-id>
```

### Iterative rescue workflow

```bash
# First pass
/codex:rescue investigate the failing build

# Apply what Codex found, continuing the same thread
/codex:rescue --resume apply the recommended fix from the last run

# Start completely fresh
/codex:rescue --fresh re-investigate with a clean slate
```

### Use Claude to delegate naturally

```text
Ask Codex to refactor the authentication module to remove the global state.
```

Claude will invoke the `codex:codex-rescue` subagent automatically.

---

## Troubleshooting

### `/codex:setup` says Codex is not installed

```bash
npm install -g @openai/codex
# or let /codex:setup install it for you
```

### Codex is installed but not authenticated

```bash
!codex login
```

Supports ChatGPT account or API key. If using an API key directly:

```bash
export OPENAI_API_KEY=your-key-here
```

### Background job seems stuck

```bash
/codex:status
/codex:cancel task-abc123
```

### Plugin commands not appearing after install

```bash
/reload-plugins
```

### Project-level config not being picked up

Project config in `.codex/config.toml` only loads when the project is trusted by Codex. Run `codex` directly in the project directory to trust it, or check the [Codex advanced config docs](https://developers.openai.com/codex/config-advanced#project-config-files-codexconfigtoml).

### Review gate creating runaway loops

Disable it immediately:

```bash
/codex:setup --disable-review-gate
```

---

## How It Works Internally

- The plugin wraps the local `codex` binary and the [Codex app server](https://developers.openai.com/codex/app-server)
- All jobs run in your local environment against your local repository checkout
- Authentication, config, and model settings come from your existing Codex CLI setup
- Background jobs are tracked per-repository and can be resumed in Codex directly via session IDs
- The `codex:codex-rescue` subagent is registered in `/agents` and can be invoked by Claude automatically when you ask it to delegate work to Codex
