---
name: herobrine
description: Create, list, remove, and run scheduled autonomous Claude Code agents. Agents run on a timer via macOS launchd, execute any prompt headlessly, and deliver results via Beeper messages and macOS notifications. Use for recurring research, monitoring, overnight builds, or any task you want Claude to do on autopilot.
disable-model-invocation: false
user-invocable: true
argument-hint: "[create|list|remove|run-now|logs]"
allowed-tools: Bash(bash */.claude/agents/*), AskUserQuestion
---

# Scheduled Autonomous Agents

Run Claude Code on autopilot. Create agents that execute any prompt on a schedule — morning briefings, overnight builds, recurring research — delivered straight to your Beeper.

> Claude Code isn't just interactive. It's a daemon.

---

## HOW IT WORKS

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────────┐
│  /herobrine │────▶│  macOS       │────▶│  claude -p      │
│  create          │     │  launchd     │     │  (headless)     │
└─────────────────┘     └──────────────┘     └────────┬────────┘
                                                       │
                                              ┌────────▼────────┐
                                              │  Deliver via     │
                                              │  Beeper + notif  │
                                              └─────────────────┘
```

1. You define an agent: a name, a prompt, and a schedule
2. A macOS launchd plist is created to trigger it on time
3. The runner executes `claude -p` with `--dangerously-skip-permissions` (fully autonomous)
4. Results are sent to your Beeper chat and saved to local logs
5. macOS notification confirms completion

---

## SETUP

### 1. Install the scripts

Copy the runner and manager scripts to `~/.claude/agents/`:

```bash
mkdir -p ~/.claude/agents/schedules ~/.claude/agents/logs
cp scripts/run-agent.sh ~/.claude/agents/run-agent.sh
cp scripts/manage-agent.sh ~/.claude/agents/manage-agent.sh
chmod +x ~/.claude/agents/run-agent.sh ~/.claude/agents/manage-agent.sh
```

### 2. Configure Beeper delivery (optional)

Find your Beeper "Note to Self" chat ID and update the default `DELIVERY_CHAT` in `manage-agent.sh`. The agent will send full results as a formatted Beeper message after each run.

If you don't use Beeper, results are still saved to `~/.claude/agents/logs/` and delivered via macOS notification.

---

## ACTIONS

### Determine the action

If `$ARGUMENTS` contains an action keyword (create, list, remove, run-now, logs), use that. Otherwise, ask the user with AskUserQuestion:
- **Create** a new scheduled agent
- **List** all scheduled agents
- **Remove** a scheduled agent
- **Run now** — trigger an agent immediately
- **View logs** of past agent runs

---

### Action: Create

Gather from the user (via AskUserQuestion or arguments):

1. **Agent name** — short identifier, lowercase with hyphens (e.g., `stock-news`, `nightly-review`)
2. **Prompt** — the full prompt sent to Claude. Be detailed. Can include skill invocations like `/steve` or `/gsd:execute-plan`
3. **Schedule** — friendly options:
   - Every morning at 8am → `0 8 * * *`
   - Every evening at 6pm → `0 18 * * *`
   - Every hour → `every-1h`
   - Every 30 minutes → `every-30m`
   - Weekday mornings at 9am → `0 9 * * 1-5`
   - Custom cron or interval
4. **Model** — `opus`, `sonnet` (default), or `haiku`
5. **Max turns** — default: `50`

Then run:
```bash
bash ~/.claude/agents/manage-agent.sh create "<name>" "<prompt>" "<schedule>" "$HOME" "<model>" <max_turns>
```

### Action: List

```bash
bash ~/.claude/agents/manage-agent.sh list
```

### Action: Remove

If no agent name given, list first, then ask which to remove.
```bash
bash ~/.claude/agents/manage-agent.sh remove "<name>"
```

### Action: Run Now

```bash
bash ~/.claude/agents/manage-agent.sh run-now "<name>"
```

### Action: Logs

```bash
bash ~/.claude/agents/manage-agent.sh logs [agent-name]
```

---

## USE CASES

| Agent | Prompt | Schedule |
|-------|--------|----------|
| `stock-news` | Research today's top stock market movements and tech earnings. Summarize the 5 most important things. | `0 8 * * 1-5` |
| `pr-digest` | Review all open PRs in my-org/my-repo. Summarize changes, flag concerns, note approvals needed. | `0 9 * * 1-5` |
| `overnight-build` | Use /steve to implement the next phase in /path/to/project | `0 2 * * *` |
| `security-scan` | Audit /path/to/repo for OWASP top 10 vulnerabilities. Report findings with severity. | `0 6 * * 1` |
| `dep-updater` | Check for outdated dependencies in /path/to/project. Create a PR with safe updates. | `0 3 * * 0` |

---

## FILE STRUCTURE

```
~/.claude/agents/
├── run-agent.sh              # Executes claude -p, delivers results
├── manage-agent.sh           # Create/list/remove/run-now/logs
├── schedules/                # Agent configs (JSON)
│   └── stock-news.json
└── logs/                     # Execution logs
    ├── stock-news_20260211_080000.log
    └── stock-news_launchd.log

~/Library/LaunchAgents/
└── com.claude.agent.stock-news.plist   # macOS scheduler
```

---

## KEY DETAILS

- Agents run with `--dangerously-skip-permissions` — fully autonomous, no prompts
- Each agent gets its own launchd plist for reliable scheduling
- The Beeper delivery instruction is injected into the prompt, so the spawned Claude instance handles delivery itself via MCP
- Logs capture full output for every run with timestamps
- Agents can invoke other skills (`/steve`, `/rnv`, `/gsd:execute-plan`) — it's a full Claude Code instance
