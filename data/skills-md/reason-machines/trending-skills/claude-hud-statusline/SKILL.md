---
name: claude-hud-statusline
description: A Claude Code plugin that displays a real-time HUD showing context usage, active tools, running agents, and todo progress in your terminal statusline.
triggers:
  - install claude hud plugin
  - show context usage in claude code
  - add statusline to claude code
  - track tool activity in claude
  - monitor agent progress claude code
  - configure claude hud display
  - claude code context window indicator
  - set up claude hud statusline
---

# Claude HUD

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Claude HUD is a Claude Code plugin that adds a persistent statusline to your terminal showing real-time context window usage, active tool calls, running subagents, and todo progress — always visible below your input prompt.

## What It Does

| Feature | Description |
|---------|-------------|
| **Context health** | Visual bar showing how full your context window is (green → yellow → red) |
| **Tool activity** | Live display of file reads, edits, and searches as they happen |
| **Agent tracking** | Shows which subagents are running and what they're doing |
| **Todo progress** | Real-time task completion tracking |
| **Usage limits** | Claude subscriber rate limit consumption |
| **Git status** | Current branch, dirty state, ahead/behind remote |

## Requirements

- Claude Code v1.0.80+
- Node.js 18+ or Bun

## Installation

Run these commands inside a Claude Code session:

**Step 1: Add the marketplace**
```
/plugin marketplace add jarrodwatts/claude-hud
```

**Step 2: Install the plugin**
```
/plugin install claude-hud
```

> **Linux users**: If you get `EXDEV: cross-device link not permitted`, set TMPDIR first:
> ```bash
> mkdir -p ~/.cache/tmp && TMPDIR=~/.cache/tmp claude
> ```

**Step 3: Configure the statusline**
```
/claude-hud:setup
```

> **Windows users**: If setup reports no JavaScript runtime, install Node.js LTS first:
> ```powershell
> winget install OpenJS.NodeJS.LTS
> ```

**Step 4: Restart Claude Code** to load the new `statusLine` config.

## What You See

### Default 2-line layout
```
[Opus] │ my-project git:(main*)
Context █████░░░░░ 45% │ Usage ██░░░░░░░░ 25% (1h 30m / 5h)
```

### With optional lines enabled
```
[Opus] │ my-project git:(main*)
Context █████░░░░░ 45% │ Usage ██░░░░░░░░ 25% (1h 30m / 5h)
◐ Edit: auth.ts | ✓ Read ×3 | ✓ Grep ×2
◐ explore [haiku]: Finding auth code (2m 15s)
▸ Fix authentication bug (2/5)
```

## Configuration

### Interactive configuration (recommended)
```
/claude-hud:configure
```

This opens a guided flow with preset options:

| Preset | Shows |
|--------|-------|
| **Full** | Everything — tools, agents, todos, git, usage, duration |
| **Essential** | Activity lines + git, minimal clutter |
| **Minimal** | Model name and context bar only |

### Manual configuration

Edit `~/.claude/plugins/claude-hud/config.json` directly:

```json
{
  "lineLayout": "expanded",
  "pathLevels": 2,
  "elementOrder": ["project", "context", "usage", "tools", "agents", "todos"],
  "gitStatus": {
    "enabled": true,
    "showDirty": true,
    "showAheadBehind": true,
    "showFileStats": false
  },
  "display": {
    "showModel": true,
    "showContextBar": true,
    "contextValue": "percent",
    "showUsage": true,
    "usageBarEnabled": true,
    "showTools": true,
    "showAgents": true,
    "showTodos": true,
    "showDuration": false,
    "showSpeed": false,
    "showConfigCounts": false,
    "showMemoryUsage": false,
    "showSessionName": false,
    "showClaudeCodeVersion": false,
    "sevenDayThreshold": 80,
    "showTokenBreakdown": true
  },
  "colors": {
    "context": "green",
    "usage": "brightBlue",
    "warning": "yellow",
    "usageWarning": "brightMagenta",
    "critical": "red",
    "model": "cyan",
    "project": "yellow",
    "git": "magenta",
    "gitBranch": "cyan",
    "label": "dim",
    "custom": "208"
  }
}
```

## Key Configuration Options

### Layout
```json
{
  "lineLayout": "expanded",   // "expanded" (multi-line) or "compact" (single line)
  "pathLevels": 1             // 1-3 directory levels in project path
}
```

Path level examples:
- `1` → `[Opus] │ my-project git:(main)`
- `2` → `[Opus] │ apps/my-project git:(main)`
- `3` → `[Opus] │ dev/apps/my-project git:(main)`

### Context display formats
```json
{
  "display": {
    "contextValue": "percent"    // "45%"
    // "contextValue": "tokens"  // "45k/200k"
    // "contextValue": "remaining" // "55% remaining"
    // "contextValue": "both"    // "45% (45k/200k)"
  }
}
```

### Element ordering (expanded layout)
```json
{
  "elementOrder": ["project", "context", "usage", "memory", "environment", "tools", "agents", "todos"]
}
```
Omit any entry from the array to hide it entirely.

### Git status options
```json
{
  "gitStatus": {
    "enabled": true,
    "showDirty": true,         // "main*" for uncommitted changes
    "showAheadBehind": true,   // "main ↑2 ↓1"
    "showFileStats": true      // "main* !3 +1 ?2" (modified/added/deleted/untracked)
  }
}
```

### Colors

Supported values: named colors (`dim`, `red`, `green`, `yellow`, `magenta`, `cyan`, `brightBlue`, `brightMagenta`), 256-color numbers (`0-255`), or hex (`#rrggbb`).

```json
{
  "colors": {
    "context": "#00FF88",
    "model": "208",
    "project": "#FF6600"
  }
}
```

## How It Works

Claude HUD uses Claude Code's native **statusline API** — no separate window, no tmux needed:

```
Claude Code → stdin JSON → claude-hud → stdout → terminal statusline
           ↘ transcript JSONL (tools, agents, todos parsed live)
```

- Token data comes directly from Claude Code (not estimated)
- Scales with reported context window size including 1M-context sessions
- Parses transcript for tool/agent activity
- Updates every ~300ms

## Common Patterns

### Minimal setup for focused work
```json
{
  "lineLayout": "compact",
  "display": {
    "showModel": true,
    "showContextBar": true,
    "contextValue": "percent",
    "showUsage": false,
    "showTools": false,
    "showAgents": false,
    "showTodos": false
  }
}
```

### Full monitoring setup
```json
{
  "lineLayout": "expanded",
  "pathLevels": 2,
  "gitStatus": {
    "enabled": true,
    "showDirty": true,
    "showAheadBehind": true,
    "showFileStats": true
  },
  "display": {
    "showTools": true,
    "showAgents": true,
    "showTodos": true,
    "showDuration": true,
    "showMemoryUsage": true,
    "showConfigCounts": true,
    "contextValue": "both",
    "showTokenBreakdown": true
  }
}
```

### Always show 7-day usage
```json
{
  "display": {
    "showUsage": true,
    "sevenDayThreshold": 0
  }
}
```
Output: `Context █████░░░░░ 45% │ Usage ██░░░░░░░░ 25% (1h 30m / 5h) | ██████████ 85% (2d / 7d)`

## Troubleshooting

**HUD not appearing after setup**
- Fully restart Claude Code (quit and re-run `claude` in terminal)
- On macOS, ensure you've fully quit the app, not just closed the window

**Config not applying**
- Check for JSON syntax errors — invalid JSON silently falls back to defaults
- Validate: `cat ~/.claude/plugins/claude-hud/config.json | node -e "JSON.parse(require('fs').readFileSync('/dev/stdin','utf8'))"`
- Delete config and run `/claude-hud:configure` to regenerate

**Git status missing**
- Verify you're in a git repository (`git status`)
- Ensure `gitStatus.enabled` is not `false` in config

**Tool/agent/todo lines not showing**
- These are hidden by default — enable with `showTools`, `showAgents`, `showTodos`
- Lines only render when there's active activity to display

**Usage limits not showing**
- Requires a Claude subscriber account (not API key only)
- AWS Bedrock users see `Bedrock` label; usage is managed in AWS console instead
- Usage data may be empty until after the first model response in a new session
- Older Claude Code versions that don't emit `rate_limits` won't show subscriber usage

**Linux cross-device error on install**
```bash
mkdir -p ~/.cache/tmp && TMPDIR=~/.cache/tmp claude
# Then run /plugin install claude-hud inside that session
```

**Windows: no JavaScript runtime found**
```powershell
winget install OpenJS.NodeJS.LTS
# Restart shell, then run /claude-hud:setup again
```

## Plugin Commands Reference

| Command | Description |
|---------|-------------|
| `/plugin marketplace add jarrodwatts/claude-hud` | Register the plugin source |
| `/plugin install claude-hud` | Install the plugin |
| `/claude-hud:setup` | Initial setup wizard, writes `statusLine` config |
| `/claude-hud:configure` | Interactive configuration with preview |

## Config File Location

```
~/.claude/plugins/claude-hud/config.json
```
