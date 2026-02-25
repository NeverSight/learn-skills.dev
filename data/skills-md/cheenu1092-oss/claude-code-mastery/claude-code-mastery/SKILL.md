---
name: claude-code-mastery
version: "1.4.3"
description: "Master Claude Code for coding tasks. Includes setup scripts, dev team subagents (starter pack or full team), self-improving learning system, diagnostics, and troubleshooting."
author: "Clawdbot Community"
license: "MIT"
metadata: {"openclaw":{"emoji":"🧑‍💻"}}
---

# Claude Code Mastery

Complete skill for setting up, optimizing, and mastering Claude Code with a full development team of subagents.

**Official Docs:** https://code.claude.com/docs

---

## ⚡ Quick Check: Is Setup Complete?

**Run this first:**
```bash
command -v claude >/dev/null && echo "✅ Claude Code installed - SKIP to 'Daily Use' section" || echo "❌ Not installed - follow 'First-Time Setup' below"
```

If Claude Code is already installed, **skip directly to the "Daily Use" section below.**

---

# 🔧 FIRST-TIME SETUP (Skip if already installed)

> **Note to bot:** Only follow this section if Claude Code is NOT installed. Check with the command above. Once setup is complete, this section can be ignored on future invocations.

## Setup Scripts

Run these in order:

```bash
cd ~/clawd/skills/claude-code-mastery/scripts

# 1. Check dependencies
./01-check-dependencies.sh

# 2. Install Claude Code
./02-install-claude-code.sh

# 3. Authenticate
./03-first-time-auth.sh

# 4. Install dev team subagents
./04-install-subagents.sh              # Starter pack (3 agents) - recommended
./04-install-subagents.sh --full-team  # All 11 agents

# 5. (Optional) Persistent memory - prompts y/N, default No
./05-setup-claude-mem.sh               # Interactive prompt
./05-setup-claude-mem.sh --skip        # Skip entirely
./05-setup-claude-mem.sh --yes         # Install without prompting
```

## Configuration

Edit `config.sh` to customize:
- `VALID_MODELS` — Add models as Anthropic releases them
- `HEARTBEAT_DIAGNOSTICS` — Enable/disable in heartbeat (default: false)
- `INSTALL_MODE` — Default to "starter" or "full"

## Setup Gotchas

| Issue | Solution |
|-------|----------|
| "Command not found" | Add `~/.local/bin` to PATH |
| Auth errors | Run `./03-first-time-auth.sh` |
| Slow startup | First run indexes codebase |
| Subagents not showing | Run `./04-install-subagents.sh` |

## Post-Setup: Add Heartbeat Task

After setup, add the maintenance task to your HEARTBEAT.md (see "Heartbeat Maintenance" in Daily Use section).

**Setup complete! Continue to Daily Use section.**

---

# 📘 DAILY USE (Always relevant)

This section covers ongoing usage - reference this for all coding tasks.

## Dev Team Subagents

Subagents are installed to `~/.claude/agents/`. Each has a **"Learn More"** section with curated links to deepen expertise.

### Starter Pack (Default) — 3 Core Agents

Most users only need these:

| Agent | Model | Purpose |
|-------|-------|---------|
| `senior-dev` | Sonnet | Architecture, complex code, code review |
| `project-manager` | Sonnet | Task breakdown, timelines, dependencies |
| `junior-dev` | **Haiku** | Quick fixes, simple tasks (fast & cheap) |

Install: `./04-install-subagents.sh` (or `--minimal`)

### Full Team (Optional) — All 10 Agents

For larger projects, install all 11 with `--full-team`:

| Agent | Model | Purpose |
|-------|-------|---------|
| `senior-dev` | Sonnet | Architecture, complex code, code review |
| `project-manager` | Sonnet | Task breakdown, timelines, dependencies |
| `junior-dev` | **Haiku** | Quick fixes, simple tasks (fast & cheap) |
| `frontend-dev` | Sonnet | React, UI, CSS, client-side |
| `backend-dev` | Sonnet | APIs, databases, server-side |
| `ai-engineer` | Sonnet | LLM apps, RAG, prompts, agents |
| `ml-engineer` | Sonnet | ML models, training, MLOps |
| `data-scientist` | Sonnet | SQL, analysis, statistics |
| `data-engineer` | Sonnet | Pipelines, ETL, data infrastructure |
| `product-manager` | Sonnet | Requirements, user stories, prioritization |
| `devops` | Sonnet | CI/CD, Docker, K8s, infrastructure, automation |

### Using Subagents

**Interactive mode:** Use the `/agent` slash command or natural language:
```
/agent senior-dev
Use the senior-dev agent to review this code
```

**Non-interactive mode (`-p`):** Use the `--agent` flag:
```bash
claude --agent senior-dev -p "review this code for security issues"
claude --agent project-manager -p "create a task breakdown for auth feature"
claude --agent junior-dev -p "fix the typo in README.md"
```

**Note:** Claude Code does NOT auto-delegate to subagents based on task type. You must explicitly specify which agent to use.

**Multi-agent handoff:** For tasks needing multiple specialists, use HANDOFF.md to pass context between agents. See `docs/workflows.md` for the full pattern.

---

## Quick Reference

### CLI Commands
```bash
claude              # Start interactive
claude -c           # Continue previous session
claude -p "prompt"  # Non-interactive mode
```

### Slash Commands
```
/agents   - Manage subagents
/clear    - Clear conversation (use between tasks!)
/compact  - Compress context
/model    - Change model
/help     - All commands
```

### Keyboard Shortcuts
```
Shift+Tab - Toggle Plan mode (read-only exploration)
Ctrl+C    - Cancel operation
Ctrl+B    - Background task
```

---

## Context Management (Critical!)

| Command | What it does | When to use |
|---------|--------------|-------------|
| `/clear` | Clear conversation, start fresh | Between unrelated tasks |
| `/compact` | Summarize and compress context | When context getting full |
| `Shift+Tab` | Toggle Plan mode (read-only) | Exploration before implementing |

**Best practices:**
1. `/clear` between unrelated tasks
2. Use Plan mode for exploration before implementing
3. Subagents isolate verbose operations
4. Create HANDOFF.md for session continuity

---

## Project Configuration

### settings.json

Create `.claude/settings.json` in your project:

```json
{
  "model": "sonnet",
  "permissions": {
    "allow": ["Bash(npm:*)", "Bash(git:*)", "Read", "Write", "Edit"],
    "deny": ["Bash(rm -rf:*)", "Bash(sudo:*)"]
  }
}
```

### CLAUDE.md

Create `CLAUDE.md` in your project root (Claude reads this automatically):

```markdown
# Project: MyApp

## Tech Stack
- Frontend: React, TypeScript, Tailwind
- Backend: Node.js, PostgreSQL

## Commands
- `npm run dev` - Start dev server
- `npm test` - Run tests
```

See `examples/CLAUDE-template.md` for a full template.

---

## Claude-Mem (If Installed)

Check status:
```bash
pgrep -f "worker-service" >/dev/null && echo "running" || echo "stopped"
```

Start if stopped:
```bash
cd ~/.claude/plugins/marketplaces/thedotmack && bun plugin/scripts/worker-service.cjs start
```

Web UI: http://localhost:37777

---

## Diagnostics & Troubleshooting

**Quick diagnostics:**
```bash
~/clawd/skills/claude-code-mastery/scripts/06-diagnostics.sh
```

**Full troubleshooting (if issues found):**
```bash
~/clawd/skills/claude-code-mastery/scripts/08-troubleshoot.sh
```

**Common issues guide:** See `docs/troubleshooting.md` for solutions to:
- Authentication problems (API key, OAuth, logout bugs)
- Installation issues (PATH, WSL, Node.js version)
- Network errors (firewalls, VPNs, proxies)
- Performance problems (high CPU, hangs, slow search)

---

## Heartbeat Maintenance

Add to your HEARTBEAT.md for automatic maintenance:

```markdown
## Claude Code Maintenance

**Last Health Check:** [timestamp]
**Last Learning Session:** [timestamp]

### Every Heartbeat (if coding tasks active):
1. Quick claude-mem check (if installed):
   `pgrep -f "worker-service" >/dev/null && echo "running" || echo "stopped"`
   - Only restart if stopped
   - Note: pgrep saves ~500 tokens vs full status command

### Daily (morning):
1. Quick health check: `command -v claude && pgrep -f "worker-service"`
2. Only run full diagnostics if quick check fails

### Weekly (Sunday):
1. Run: `~/clawd/skills/claude-code-mastery/scripts/07-weekly-improvement-cron.sh`
2. Propose improvements (require human approval)

### Weekly Learning & Skill Improvement (rotate through agents):
1. Pick ONE agent file from the skill's `agents/` folder (rotate weekly)
2. Read the "Learn More" section
3. Visit 2-3 links that are relevant to current projects
4. Internalize key concepts and update your workflows
5. **Improve the skill itself:**
   - Found a better resource? Add it to "Learn More"
   - Discovered a new best practice? Update the agent's guidelines
   - Link broken or outdated? Remove or replace it
   - New tool or framework worth mentioning? Add it
6. Commit changes locally with clear commit messages
7. **Don't push directly to shared repos** — propose changes as a PR or request human review first
8. Note learnings in your memory files

**Rotation schedule:**
- Week 1: senior-dev, junior-dev
- Week 2: frontend-dev, backend-dev
- Week 3: ai-engineer, ml-engineer
- Week 4: data-scientist, data-engineer
- Week 5: project-manager, product-manager
- Week 6: devops

**What to update:**
- `agents/*.md` — Add new links, update best practices, fix outdated info
- `SKILL.md` — Improve documentation, add tips discovered
- `docs/*.md` — Enhance guides based on real usage
```

**Why this matters:**
- Skill improves over time through actual use
- Links stay current (broken ones get fixed)
- Best practices evolve with the ecosystem
- Each Clawdbot contributes back to the skill

---

## Scripts Reference

| Script | Purpose | When to use |
|--------|---------|-------------|
| `06-diagnostics.sh` | Health check and status report | When issues occur |
| `07-weekly-improvement-cron.sh` | Generate improvement report | Weekly (Sunday) |
| `08-troubleshoot.sh` | Comprehensive troubleshooting | When 06 finds issues |

---

## Summary

**For coding tasks:**
1. Use appropriate subagent for the task
2. Manage context with `/clear` and Plan mode
3. Run diagnostics if something breaks

**Heartbeat handles:**
- claude-mem health checks
- Daily quick diagnostics
- Weekly improvement research

The dev team subagents turn Claude Code into a full development organization.
