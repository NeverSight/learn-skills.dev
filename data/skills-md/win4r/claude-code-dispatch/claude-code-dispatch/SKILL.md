---
name: claude-code-dispatch
description: >
  Dispatch development tasks to Claude Code with automatic callback on completion.
  Supports Agent Teams (multi-agent parallel dev with dedicated Testing Agent),
  cost controls (--max-budget-usd), model fallback, git worktree isolation,
  custom subagents via --agents JSON, and MCP server integration.
  Use when: (1) dispatching a coding task to Claude Code and wanting automatic
  Telegram notification on completion, (2) running Agent Teams for parallel
  dev+test workflows, (3) needing zero-polling task execution with Stop Hook
  callback, (4) the user says 'use Claude Code to build/develop/create X',
  (5) the user asks to dispatch or run a Claude Code task.
  THIS IS THE DEFAULT for any 'build/develop/create a project' request —
  prefer this over claude-code-clawdbot for anything that takes >2 min or
  needs background execution.
---

# Claude Code Dispatch Skill

Dispatch development tasks to Claude Code with automatic notification on
completion. Zero polling, zero token waste.

## Architecture

```
dispatch.sh
  → write task-meta.json
  → launch Claude Code via claude_code_run.py (PTY wrapper)
  → [Agent Teams: --agents JSON defines Testing Agent + custom subagents]
  → Claude Code finishes → Stop/TaskCompleted hook fires automatically
    → notify-agi.sh reads meta + output
    → writes latest.json
    → sends Telegram notification (group + callback)
    → writes pending-wake.json (heartbeat fallback)
```

## Quick Reference

### Basic dispatch

⚠️ **Always use `nohup` + background (`&`)** — dispatch runs until done.

```bash
nohup bash scripts/dispatch.sh \
  -p "Build a Python REST API with FastAPI" \
  -n "my-api" \
  -g "-5006066016" \
  --permission-mode bypassPermissions \
  --workdir /home/ubuntu/projects/my-api \
  > /tmp/dispatch-my-api.log 2>&1 &
```

### With Agent Teams

```bash
nohup bash scripts/dispatch.sh \
  -p "Build a full-stack app with React + Express" \
  -n "fullstack-app" \
  --agent-teams \
  --permission-mode bypassPermissions \
  --workdir /home/ubuntu/projects/fullstack-app \
  > /tmp/dispatch-fullstack.log 2>&1 &
```

When `--agent-teams` is passed without `--agents-json`, a default Testing Agent
is auto-defined via the `--agents` CLI flag (structured JSON, not prompt injection).

### With cost controls

```bash
nohup bash scripts/dispatch.sh \
  -p "Refactor the database layer" \
  -n "db-refactor" \
  --max-budget-usd 5.00 \
  --max-turns 50 \
  --fallback-model sonnet \
  --permission-mode bypassPermissions \
  --workdir /home/ubuntu/projects/my-app \
  > /tmp/dispatch-refactor.log 2>&1 &
```

### With custom subagents

```bash
nohup bash scripts/dispatch.sh \
  -p "Build CLI tool" \
  -n "cli-tool" \
  --agent-teams \
  --agents-json '{"security-reviewer":{"description":"Security expert","prompt":"Review for vulnerabilities","tools":["Read","Grep","Glob"],"model":"opus"}}' \
  --permission-mode bypassPermissions \
  --workdir /home/ubuntu/projects/cli-tool \
  > /tmp/dispatch-cli.log 2>&1 &
```

### With git worktree isolation

```bash
nohup bash scripts/dispatch.sh \
  -p "Implement feature X" \
  -n "feature-x" \
  --worktree feature-x \
  --permission-mode bypassPermissions \
  --workdir /home/ubuntu/projects/my-app \
  > /tmp/dispatch-feature.log 2>&1 &
```

## All Parameters

| Param | Short | Description |
|-------|-------|-------------|
| `--prompt` | `-p` | Task description (required*) |
| `--prompt-file` | | Read prompt from file (required*) |
| `--name` | `-n` | Task name for tracking |
| `--group` | `-g` | Telegram group ID for notifications |
| `--workdir` | `-w` | Working directory |
| `--agent-teams` | | Enable Agent Teams mode |
| `--agents-json` | | Custom subagent definitions (JSON) |
| `--teammate-mode` | | Display: `auto` / `in-process` / `tmux` |
| `--permission-mode` | | `bypassPermissions` / `plan` / `acceptEdits` / `default` |
| `--allowed-tools` | | Tool allowlist |
| `--disallowed-tools` | | Tool denylist |
| `--model` | | Model override (sonnet/opus/haiku/full name) |
| `--fallback-model` | | Auto-fallback when primary is overloaded |
| `--max-budget-usd` | | Maximum dollar spend before stopping |
| `--max-turns` | | Maximum agentic turns |
| `--worktree` | | Git worktree name for isolation |
| `--no-session-persistence` | | Don't save session to disk |
| `--append-system-prompt` | | Append text to system prompt |
| `--append-system-prompt-file` | | Append system prompt from file |
| `--mcp-config` | | Load MCP servers from JSON file |
| `--verbose` | | Enable verbose logging |
| `--callback-group` | | Callback to dispatching agent's group |
| `--callback-dm` | | DM callback user ID |
| `--callback-account` | | DM callback bot account |
| `--session` | `-s` | Callback session key |

\* One of `--prompt` or `--prompt-file` is required.

## Hook Setup

See [references/hook-setup.md](references/hook-setup.md) for full hook
configuration. The skill uses Stop, TaskCompleted, and SessionEnd hooks with
the `notify-agi.sh` script. HTTP hooks are also supported as an alternative.

## Prompt Tips

See [references/prompt-guide.md](references/prompt-guide.md) for examples
and best practices, including cost control, Agent Teams, worktree isolation,
custom subagents, and MCP integration.

## Debugging

```bash
# Watch hook log
tail -f data/claude-code-results/hook.log

# Check latest result
cat data/claude-code-results/latest.json | jq .

# Check task metadata
cat data/claude-code-results/task-meta.json | jq .

# Test Telegram delivery
openclaw message send --channel telegram --target "-5006066016" --message "test"

# Check dispatch log
tail -f /tmp/dispatch-*.log
```

## Gotchas

1. **Must use PTY wrapper** — Direct `claude -p` can hang in exec environments
2. **Hook fires twice** — Stop + SessionEnd both trigger; `.hook-lock` deduplicates (30s window)
3. **Hook stdin is empty in PTY** — Output read from `task-output.txt`, not stdin
4. **tee pipe race** — Hook sleeps 1s for pipe flush before reading output
5. **Meta freshness** — Hook validates meta age (<2h) and session ID
6. **Agent Teams cost** — Use `--max-budget-usd` to cap spend on multi-agent tasks
7. **Rate limits** — Claude Code has daily rate limits resetting at 11:00 UTC; check hook.log for "limit" messages
