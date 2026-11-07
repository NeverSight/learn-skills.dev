---
name: deepclaude-proxy
description: Use Claude Code's autonomous agent loop with DeepSeek V4 Pro, OpenRouter, or any Anthropic-compatible backend at up to 17x lower cost.
triggers:
  - set up deepclaude with deepseek
  - use claude code with deepseek backend
  - cheaper alternative to claude code
  - switch claude code to openrouter
  - proxy claude code api calls to deepseek
  - deepclaude installation and configuration
  - save money on claude code usage
  - live switch between anthropic and deepseek
---

# deepclaude

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

**deepclaude** routes Claude Code's API calls to DeepSeek V4 Pro, OpenRouter, Fireworks AI, or any Anthropic-compatible backend — keeping the full Claude Code UX (file editing, bash, subagents, git) while cutting costs by up to 17x.

## How it works

Claude Code reads specific environment variables to determine its API endpoint and model names. `deepclaude` sets these per-session (not permanently), launches Claude Code, then restores originals on exit.

```
Your terminal
  └── Claude Code CLI (tool loop, file editing, bash, git — unchanged)
        └── API calls → DeepSeek V4 Pro ($0.87/M) instead of Anthropic ($15/M)
```

Key environment variables Claude Code uses:

| Variable | Purpose |
|---|---|
| `ANTHROPIC_BASE_URL` | API endpoint override |
| `ANTHROPIC_AUTH_TOKEN` | API key for the backend |
| `ANTHROPIC_DEFAULT_OPUS_MODEL` | Model for Opus-tier tasks |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | Model for Sonnet-tier tasks |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL` | Model for Haiku-tier / subagents |
| `CLAUDE_CODE_SUBAGENT_MODEL` | Model for spawned subagents |

## Installation

### Prerequisites
- Claude Code CLI installed (`npm install -g @anthropic-ai/claude-code`)
- Node.js 18+ (for the proxy server)
- API key for at least one backend

### 1. Clone the repo

```bash
git clone https://github.com/aattaran/deepclaude.git
cd deepclaude
```

### 2. Set API keys

**macOS/Linux:**
```bash
# DeepSeek (default backend — get key at platform.deepseek.com)
echo 'export DEEPSEEK_API_KEY="$DEEPSEEK_API_KEY"' >> ~/.bashrc

# OpenRouter (optional — cheapest US latency)
echo 'export OPENROUTER_API_KEY="$OPENROUTER_API_KEY"' >> ~/.bashrc

# Fireworks AI (optional — fastest inference)
echo 'export FIREWORKS_API_KEY="$FIREWORKS_API_KEY"' >> ~/.bashrc

source ~/.bashrc
```

**Windows (PowerShell):**
```powershell
setx DEEPSEEK_API_KEY $env:DEEPSEEK_API_KEY
setx OPENROUTER_API_KEY $env:OPENROUTER_API_KEY
setx FIREWORKS_API_KEY $env:FIREWORKS_API_KEY
```

### 3. Install the CLI

**macOS/Linux:**
```bash
chmod +x deepclaude.sh
sudo ln -s "$(pwd)/deepclaude.sh" /usr/local/bin/deepclaude
```

**Windows (PowerShell):**
```powershell
Copy-Item deepclaude.ps1 "$env:USERPROFILE\.local\bin\deepclaude.ps1"
# Or add repo directory to PATH:
setx PATH "$env:PATH;C:\path\to\deepclaude"
```

## Key CLI commands

```bash
# Launch Claude Code with DeepSeek V4 Pro (default)
deepclaude

# Show available backends and configured API keys
deepclaude --status

# Select a specific backend
deepclaude --backend ds          # DeepSeek (default)
deepclaude --backend or          # OpenRouter
deepclaude --backend fw          # Fireworks AI
deepclaude --backend anthropic   # Normal Claude Opus

# Show pricing comparison
deepclaude --cost

# Latency benchmark across all configured providers
deepclaude --benchmark

# Switch backend mid-session (proxy must be running)
deepclaude --switch ds
deepclaude --switch or
deepclaude --switch anthropic

# Remote control — open session in any browser
deepclaude --remote
deepclaude --remote --backend or
deepclaude --remote --backend anthropic
```

## Supported backends

| Backend | Flag | Input/M | Output/M | Notes |
|---|---|---|---|---|
| DeepSeek | `ds` | $0.44 | $0.87 | Auto context caching (120x cheaper on repeat turns) |
| OpenRouter | `or` | $0.44 | $0.87 | Lowest latency from US/EU |
| Fireworks AI | `fw` | $1.74 | $3.48 | Fastest inference, US servers |
| Anthropic | `anthropic` | $3.00 | $15.00 | Original Claude Opus |

## Live backend switching (no restart)

A local proxy runs on `localhost:3200` and intercepts all API calls. Switch backends instantly without restarting Claude Code.

### Proxy control endpoints

```bash
# Switch backend
curl -sX POST http://127.0.0.1:3200/_proxy/mode -d "backend=deepseek"
curl -sX POST http://127.0.0.1:3200/_proxy/mode -d "backend=openrouter"
curl -sX POST http://127.0.0.1:3200/_proxy/mode -d "backend=anthropic"

# Check current backend + uptime
curl -s http://127.0.0.1:3200/_proxy/status

# Token usage and cost savings vs Anthropic
curl -s http://127.0.0.1:3200/_proxy/cost
```

Cost endpoint response shape:
```json
{
  "backends": {
    "deepseek": {
      "input_tokens": 125000,
      "output_tokens": 45000,
      "requests": 12,
      "cost": 0.0941,
      "anthropic_equivalent": 1.05
    }
  },
  "total_cost": 0.0941,
  "anthropic_equivalent": 1.05,
  "savings": 0.9559
}
```

### Slash commands (recommended UX)

Create files in `~/.claude/commands/` to switch backends from inside any Claude Code session:

**`~/.claude/commands/deepseek.md`:**
```markdown
Switch the model proxy to DeepSeek. Run this command silently and report the result:
curl -sX POST http://127.0.0.1:3200/_proxy/mode -d "backend=deepseek"
If successful, say: "Switched to DeepSeek."
```

**`~/.claude/commands/anthropic.md`:**
```markdown
Switch the model proxy back to Anthropic. Run this command silently and report the result:
curl -sX POST http://127.0.0.1:3200/_proxy/mode -d "backend=anthropic"
If successful, say: "Switched to Anthropic."
```

**`~/.claude/commands/openrouter.md`:**
```markdown
Switch the model proxy to OpenRouter. Run this command silently and report the result:
curl -sX POST http://127.0.0.1:3200/_proxy/mode -d "backend=openrouter"
If successful, say: "Switched to OpenRouter."
```

Then type `/deepseek`, `/anthropic`, or `/openrouter` in any Claude Code session.

### VS Code keyboard shortcuts

**`.vscode/tasks.json`:**
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Proxy: Switch to DeepSeek",
      "type": "shell",
      "command": "curl -sX POST http://127.0.0.1:3200/_proxy/mode -d 'backend=deepseek'",
      "presentation": { "reveal": "always" },
      "problemMatcher": []
    },
    {
      "label": "Proxy: Switch to Anthropic",
      "type": "shell",
      "command": "curl -sX POST http://127.0.0.1:3200/_proxy/mode -d 'backend=anthropic'",
      "presentation": { "reveal": "always" },
      "problemMatcher": []
    },
    {
      "label": "Proxy: Switch to OpenRouter",
      "type": "shell",
      "command": "curl -sX POST http://127.0.0.1:3200/_proxy/mode -d 'backend=openrouter'",
      "presentation": { "reveal": "always" },
      "problemMatcher": []
    }
  ]
}
```

**`keybindings.json`:**
```json
[
  { "key": "ctrl+alt+d", "command": "workbench.action.tasks.runTask", "args": "Proxy: Switch to DeepSeek" },
  { "key": "ctrl+alt+a", "command": "workbench.action.tasks.runTask", "args": "Proxy: Switch to Anthropic" },
  { "key": "ctrl+alt+o", "command": "workbench.action.tasks.runTask", "args": "Proxy: Switch to OpenRouter" }
]
```

## VS Code / Cursor terminal profiles

**`settings.json` on macOS/Linux:**
```json
{
  "terminal.integrated.profiles.linux": {
    "DeepSeek Agent": {
      "path": "/usr/local/bin/deepclaude"
    },
    "DeepSeek (OpenRouter)": {
      "path": "/usr/local/bin/deepclaude",
      "args": ["--backend", "or"]
    }
  },
  "terminal.integrated.defaultProfile.linux": "DeepSeek Agent"
}
```

**`settings.json` on Windows:**
```json
{
  "terminal.integrated.profiles.windows": {
    "DeepSeek Agent": {
      "path": "powershell.exe",
      "args": ["-ExecutionPolicy", "Bypass", "-NoExit", "-File", "C:\\path\\to\\deepclaude.ps1"]
    }
  }
}
```

## Remote control (browser UI)

Open a Claude Code session in any browser with DeepSeek as the backend:

```bash
deepclaude --remote                  # DeepSeek backend
deepclaude --remote --backend or     # OpenRouter backend
deepclaude --remote --backend anthropic  # Normal Anthropic
```

Traffic split:
```
claude remote-control
  ├── Bridge WebSocket → wss://bridge.claudeusercontent.com (Anthropic, required)
  └── Model API calls  → http://localhost:3200 (proxy)
                          ├── /v1/messages → active backend (DeepSeek/OR/etc.)
                          └── everything else → Anthropic (passthrough)
```

**Requirements for remote control:**
- Must be logged in: `claude auth login`
- Must have a claude.ai subscription (bridge is Anthropic infrastructure)

## Manually setting environment variables (without the CLI wrapper)

If you want to wire up the backend yourself without using the `deepclaude` wrapper script:

```bash
# DeepSeek
export ANTHROPIC_BASE_URL="https://api.deepseek.com/v1"
export ANTHROPIC_AUTH_TOKEN="$DEEPSEEK_API_KEY"
export ANTHROPIC_DEFAULT_OPUS_MODEL="deepseek-chat"
export ANTHROPIC_DEFAULT_SONNET_MODEL="deepseek-chat"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="deepseek-chat"
export CLAUDE_CODE_SUBAGENT_MODEL="deepseek-chat"
claude  # launch normally

# OpenRouter
export ANTHROPIC_BASE_URL="https://openrouter.ai/api/v1"
export ANTHROPIC_AUTH_TOKEN="$OPENROUTER_API_KEY"
export ANTHROPIC_DEFAULT_OPUS_MODEL="deepseek/deepseek-chat-v3-0324"
export ANTHROPIC_DEFAULT_SONNET_MODEL="deepseek/deepseek-chat-v3-0324"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="deepseek/deepseek-chat-v3-0324"
export CLAUDE_CODE_SUBAGENT_MODEL="deepseek/deepseek-chat-v3-0324"
claude
```

## What works and what doesn't

### ✅ Fully supported
- File reading, writing, editing (`Read`/`Write`/`Edit` tools)
- Bash / PowerShell execution
- Glob and Grep search
- Multi-step autonomous tool loops
- Subagent spawning
- Git operations
- Project initialization (`/init`)
- Thinking mode (enabled by default)

### ⚠️ Not supported or degraded

| Feature | Reason |
|---|---|
| Image / vision input | DeepSeek's Anthropic-compat endpoint doesn't support images |
| MCP server tools | Not supported through compatibility layer |
| Anthropic prompt caching (`cache_control`) | Ignored; DeepSeek uses its own automatic caching |
| Parallel tool use | DeepSeek supports up to 128/call but Claude Code sends sequentially |

## Choosing the right backend

| Task type | Recommendation |
|---|---|
| Routine coding, refactoring, CRUD | DeepSeek (default) — 90% cost savings |
| US/EU latency sensitive | OpenRouter |
| Highest throughput / speed | Fireworks AI |
| Complex multi-step reasoning, architecture | Switch to `--backend anthropic` |

Use `/deepseek` for most work, `/anthropic` for the hard 20% — then switch back.

## Troubleshooting

**`DEEPSEEK_API_KEY` not found:**
```bash
# Verify the var is set in current shell
echo $DEEPSEEK_API_KEY
# If blank, re-source your profile
source ~/.bashrc   # or ~/.zshrc
```

**`deepclaude: command not found`:**
```bash
# Check symlink
ls -la /usr/local/bin/deepclaude
# Re-create if missing
sudo ln -sf "$(pwd)/deepclaude.sh" /usr/local/bin/deepclaude
```

**Proxy not responding on port 3200:**
```bash
# Check if proxy process is running
lsof -i :3200
# Restart deepclaude — proxy starts automatically
deepclaude
```

**`curl` not available on Windows for slash commands:**
```powershell
# Use PowerShell equivalent in the .md command files:
Invoke-RestMethod -Uri http://127.0.0.1:3200/_proxy/mode -Method Post -Body 'backend=deepseek'
```

**Image inputs fail with DeepSeek:**
- Switch to Anthropic for that session: `deepclaude --switch anthropic`
- Or launch with: `deepclaude --backend anthropic`

**Remote control fails:**
```bash
# Ensure you're authenticated
claude auth login
# Verify subscription at claude.ai — bridge requires it
```
