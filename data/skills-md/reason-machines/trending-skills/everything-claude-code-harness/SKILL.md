---
name: everything-claude-code-harness
description: Agent harness performance system for Claude Code and other AI coding agents — skills, instincts, memory, hooks, commands, and security scanning
triggers:
  - "set up everything claude code"
  - "optimize my claude code setup"
  - "install ecc plugin for claude code"
  - "configure ai agent harness performance"
  - "add skills and commands to claude code"
  - "set up hooks and memory for claude code"
  - "improve claude code with custom rules and agents"
  - "everything claude code getting started"
---

# Everything Claude Code (ECC) — Agent Harness Performance System

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Everything Claude Code (ECC) is a production-ready performance optimization system for AI agent harnesses. It provides specialized subagents, reusable skills, custom slash commands, memory-persisting hooks, security scanning, and language-specific rules — all evolved from 10+ months of daily real-world use. Works across Claude Code, Cursor, Codex, OpenCode, and Antigravity.

---

## Installation

### Option 1: Plugin Marketplace (Recommended)

```bash
# Inside Claude Code, run:
/plugin marketplace add affaan-m/everything-claude-code
/plugin install everything-claude-code@everything-claude-code
```

### Option 2: Manual Clone

```bash
git clone https://github.com/affaan-m/everything-claude-code.git
cd everything-claude-code

# Install rules for your language stack
./install.sh typescript
# Multiple languages:
./install.sh typescript python golang swift
# Target a specific IDE:
./install.sh --target cursor typescript
```

### Install Rules (Always Required)

Claude Code plugins cannot auto-distribute rules — install them manually via `./install.sh` or copy from `rules/` into your project's `.claude/rules/` directory.

---

## Directory Structure

```
everything-claude-code/
├── .claude-plugin/         # Plugin and marketplace manifests
│   ├── plugin.json
│   └── marketplace.json
├── agents/                 # Specialized subagents (planner, architect, etc.)
├── commands/               # Slash commands (/plan, /security-scan, etc.)
├── skills/                 # Reusable skill modules
├── hooks/                  # Lifecycle hooks (SessionStart, Stop, PostEdit, etc.)
├── rules/
│   ├── common/             # Language-agnostic rules
│   ├── typescript/
│   ├── python/
│   ├── golang/
│   └── swift/
├── scripts/                # Setup and utility scripts
└── install.sh              # Interactive installer
```

---

## Key Commands

After installation, use the namespaced form (plugin install) or short form (manual install):

```bash
# Planning & architecture
/everything-claude-code:plan "Add OAuth2 login flow"
/everything-claude-code:architect "Design a multi-tenant SaaS system"

# Research-first development
/everything-claude-code:research "Best approach for rate limiting in Node.js"

# Security
/everything-claude-code:security-scan
/everything-claude-code:harness-audit

# Agent loops and orchestration
/everything-claude-code:loop-start
/everything-claude-code:loop-status
/everything-claude-code:quality-gate
/everything-claude-code:model-route

# Multi-agent workflows
/everything-claude-code:multi-plan
/everything-claude-code:multi-execute
/everything-claude-code:multi-backend
/everything-claude-code:multi-frontend

# Session and memory
/everything-claude-code:sessions
/everything-claude-code:instinct-import

# PM2 orchestration
/everything-claude-code:pm2

# Package manager setup
/everything-claude-code:setup-pm
```

> With manual install, drop the `everything-claude-code:` prefix: `/plan`, `/sessions`, etc.

---

## Hook Runtime Controls

ECC hooks fire at agent lifecycle events. Control strictness at runtime without editing files:

```bash
# Set hook strictness profile
export ECC_HOOK_PROFILE=minimal    # Least intrusive
export ECC_HOOK_PROFILE=standard   # Default
export ECC_HOOK_PROFILE=strict     # Maximum enforcement

# Disable specific hooks by ID (comma-separated)
export ECC_DISABLED_HOOKS="pre:bash:tmux-reminder,post:edit:typecheck"
```

Hook events covered: `SessionStart`, `Stop`, `PostEdit`, `PreBash`, `PostBash`, and more.

---

## Package Manager Detection

ECC auto-detects your package manager with this priority chain:

1. `CLAUDE_PACKAGE_MANAGER` environment variable
2. `.claude/package-manager.json` (project-level)
3. `package.json` → `packageManager` field
4. Lock file detection (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `bun.lockb`)
5. `~/.claude/package-manager.json` (global)
6. First available manager as fallback

```bash
# Set via environment
export CLAUDE_PACKAGE_MANAGER=pnpm

# Set globally
node scripts/setup-package-manager.js --global pnpm

# Set per-project
node scripts/setup-package-manager.js --project bun

# Detect current setting
node scripts/setup-package-manager.js --detect
```

---

## Skills System

Skills are markdown modules the agent loads to gain domain expertise. Install individually or in bulk.

### Using a Skill

```bash
# Reference a skill explicitly in your prompt
"Use the search-first skill to find the right caching approach before implementing"

# Or trigger via slash command
/everything-claude-code:research "content hashing strategies for API responses"
```

### Notable Built-in Skills

| Skill | Purpose |
|---|---|
| `search-first` | Research before coding — avoids hallucinated APIs |
| `cost-aware-llm-pipeline` | Optimizes token spend across model calls |
| `content-hash-cache-pattern` | Cache invalidation via content hashing |
| `skill-stocktake` | Audits which skills are loaded and active |
| `frontend-slides` | Zero-dependency HTML presentation builder |
| `configure-ecc` | Guided interactive ECC setup wizard |
| `swift-actor-persistence` | Swift concurrency + persistence patterns |
| `regex-vs-llm-structured-text` | Decides when to use regex vs LLM parsing |

### Writing a Custom Skill

Create `skills/my-skill.md`:

```markdown
---
name: my-skill
description: What this skill does
triggers:
  - "phrase that activates this skill"
---

# My Skill

## When to Use
...

## Pattern
\`\`\`typescript
// concrete example
\`\`\`

## Rules
- Rule one
- Rule two
```

---

## Instincts System (Continuous Learning)

Instincts are session-extracted patterns saved for reuse. They carry confidence scores and evolve over time.

### Export an Instinct

```bash
/everything-claude-code:instinct-import
```

### Instinct File Format

```markdown
---
name: prefer-zod-for-validation
confidence: 0.92
extracted_from: session-2026-02-14
---

# Action
Always use Zod for runtime schema validation in TypeScript projects.

# Evidence
Caught 3 runtime type errors that TypeScript alone missed during session.

# Examples
\`\`\`typescript
import { z } from 'zod'

const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  role: z.enum(['admin', 'user'])
})

type User = z.infer<typeof UserSchema>
\`\`\`
```

---

## Rules Architecture

Rules enforce coding standards per language. Install only what your stack needs.

```bash
# TypeScript + Python
./install.sh typescript python

# Check what's installed
ls .claude/rules/
```

### Rule Directory Layout

```
rules/
├── common/         # Applies to all languages
│   ├── research-first.md
│   ├── security-baseline.md
│   └── verification-loops.md
├── typescript/
│   ├── no-any.md
│   ├── zod-validation.md
│   └── strict-mode.md
├── python/
│   ├── type-hints.md
│   └── django-patterns.md
└── golang/
    └── error-wrapping.md
```

---

## Agents (Subagent Delegation)

Agents are specialized personas the orchestrator delegates to:

```bash
# In your prompt, reference an agent explicitly
"Delegate architecture decisions to the architect agent"
"Use the planner agent to break this feature into tasks"
```

Available agents include: `planner`, `architect`, `researcher`, `verifier`, `security-auditor`, and more. Each lives in `agents/<name>.md` with its own system prompt, tools list, and constraints.

---

## AgentShield Security Scanning

Run security scans directly from Claude Code:

```bash
/everything-claude-code:security-scan
```

This invokes the AgentShield scanner (1282 tests, 102 rules) against your codebase and surfaces:
- Hardcoded secrets
- Injection vulnerabilities
- Insecure dependencies
- Agent prompt injection patterns

---

## Memory Persistence Hooks

ECC hooks automatically save and restore session context:

```javascript
// hooks/session-start.js — loads prior context on new session
const fs = require('fs')
const path = require('path')

const memoryPath = path.join(process.env.HOME, '.claude', 'session-memory.json')

if (fs.existsSync(memoryPath)) {
  const memory = JSON.parse(fs.readFileSync(memoryPath, 'utf8'))
  console.log('Restored session context:', memory.summary)
}
```

```javascript
// hooks/stop.js — saves session summary on exit
const summary = {
  timestamp: new Date().toISOString(),
  summary: process.env.ECC_SESSION_SUMMARY || '',
  skills_used: (process.env.ECC_SKILLS_USED || '').split(',')
}

fs.writeFileSync(memoryPath, JSON.stringify(summary, null, 2))
```

---

## Cross-Platform Support

| Platform | Support |
|---|---|
| Claude Code | Full (agents, commands, skills, hooks, rules) |
| Cursor | Full (via `--target cursor` installer flag) |
| OpenCode | Full (plugin system, 20+ hook event types, 3 native tools) |
| Codex CLI | Full (`codex.md` generated via `/codex-setup`) |
| Codex App | Full (`AGENTS.md`-based) |
| Antigravity | Full (via `--target antigravity` installer flag) |

---

## Common Patterns

### Research-First Development

```
"Before implementing the payment webhook handler, use the search-first skill to 
verify current Stripe webhook verification best practices."
```

### Token Optimization

```bash
# Route to cheaper model for simple tasks
/everything-claude-code:model-route "Write a unit test for this pure function"

# Use background processes for long analysis
/everything-claude-code:harness-audit
```

### Parallelization with Git Worktrees

```bash
# Create isolated worktrees for parallel agent tasks
git worktree add ../feature-auth -b feature/auth
git worktree add ../feature-payments -b feature/payments

# Each Claude Code session operates in its own worktree
# Merge when both complete
```

### Verification Loop

```bash
/everything-claude-code:loop-start    # Begin tracked loop
# ... agent does work ...
/everything-claude-code:loop-status   # Check progress
/everything-claude-code:quality-gate  # Enforce pass criteria before merge
```

---

## Troubleshooting

**Plugin commands not found after install**
```bash
/plugin list everything-claude-code@everything-claude-code
# If empty, re-run: /plugin install everything-claude-code@everything-claude-code
```

**Rules not applied**
```bash
# Rules require manual install — plugin system cannot distribute them
cd everything-claude-code && ./install.sh typescript
# Verify:
ls ~/.claude/rules/   # or .claude/rules/ in project root
```

**Hooks not firing**
```bash
# Check profile setting
echo $ECC_HOOK_PROFILE
# Check disabled list
echo $ECC_DISABLED_HOOKS
# Reset to defaults
unset ECC_HOOK_PROFILE
unset ECC_DISABLED_HOOKS
```

**Instinct import drops content**
Ensure you're on v1.4.1+. Earlier versions had a bug where `parse_instinct_file()` silently dropped Action/Evidence/Examples sections. Pull latest and re-run.

**Wrong package manager used**
```bash
node scripts/setup-package-manager.js --detect
export CLAUDE_PACKAGE_MANAGER=pnpm   # Override explicitly
```

---

## Resources

- Homepage: https://ecc.tools
- GitHub: https://github.com/affaan-m/everything-claude-code
- GitHub App (Marketplace): https://github.com/marketplace/ecc-tools
- npm (universal): `ecc-universal`
- npm (security): `ecc-agentshield`
- Shorthand Guide: https://x.com/affaanmustafa/status/2012378465664745795
- Longform Guide: https://x.com/affaanmustafa/status/2014040193557471352
