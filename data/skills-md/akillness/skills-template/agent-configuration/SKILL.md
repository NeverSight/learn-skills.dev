---
name: agent-configuration
description: AI agent configuration policy and security guide. Project description file writing, Hooks/Skills/Plugins setup, security policy, team shared workflow definition.
allowed-tools: Read Write Bash Grep Glob
metadata:
  tags: agent-configuration, superwork, spw, security, hooks, skills, plugins, multi-agent
  platforms: Claude, Gemini, ChatGPT, Codex
  version: 2.0.0
  source: Claude Code Complete Guide 70 Tips (ykdojo + Ado Kukic)
---


# AI Agent Configuration Policy (Configuration & Security)

## When to use this skill

- Build AI agent environment for new projects
- Write and optimize project description files
- Configure Hooks/Skills/Plugins
- Establish security policies
- Share team configurations

---

## 1. Project Description File Writing Policy

### Overview
Project description files (CLAUDE.md, README, etc.) are **project manuals for AI**. AI agents reference these files with top priority.

### Auto-generate (Claude Code)
```bash
/init  # Claude analyzes the codebase and generates a draft
```

### Required Section Structure

```markdown
# Project: [Project Name]

## Tech Stack
- **Frontend**: React + TypeScript
- **Backend**: Node.js + Express
- **Database**: PostgreSQL
- **ORM**: Drizzle

## Coding Standards
- Use TypeScript strict mode
- Prefer server components over client components
- Use `async/await` instead of `.then()`
- Always validate user input with Zod

## DO NOT
- Never commit `.env` files
- Never use `any` type in TypeScript
- Never bypass authentication checks
- Never expose API keys in client code

## Common Commands
- `npm run dev`: Start development server
- `npm run build`: Build for production
- `npm run test`: Run tests
```

### Writing Principles: The Art of Conciseness

**Bad (verbose):**
```markdown
Our authentication system is built using NextAuth.js, which is a
complete authentication solution for Next.js applications...
(5+ lines of explanation)
```

**Good (concise):**
```markdown
## Authentication
- NextAuth.js with Credentials provider
- JWT session strategy
- **DO NOT**: Bypass auth checks, expose session secrets
```

### Incremental Addition Principle
> "Start without a project description file. Add content when you find yourself repeating the same things."

---

## 2. Hooks Configuration Policy (Claude Code)

### Overview
Hooks are shell commands that run automatically on specific events. They act as **guardrails** for AI.

### Hook Event Types

| Hook | Trigger | Use Case |
|------|---------|----------|
| `PreToolUse` | Before tool execution | Block dangerous commands |
| `PostToolUse` | After tool execution | Log recording, send notifications |
| `PermissionRequest` | On permission request | Auto approve/deny |
| `Notification` | On notification | External system integration |
| `SubagentStart` | Subagent start | Monitoring |
| `SubagentStop` | Subagent stop | Result collection |

### Security Hooks Configuration

```json
// ~/.claude/settings.json
{
  "hooks": {
    "PreToolUse": [
      {
        "pattern": "rm -rf /",
        "action": "block",
        "message": "Block root directory deletion"
      },
      {
        "pattern": "rm -rf /*",
        "action": "block",
        "message": "Block dangerous deletion command"
      },
      {
        "pattern": "sudo rm",
        "action": "warn",
        "message": "Caution: sudo delete command"
      },
      {
        "pattern": "curl * | sh",
        "action": "block",
        "message": "Block piped script execution"
      },
      {
        "pattern": "chmod 777",
        "action": "warn",
        "message": "Caution: excessive permission setting"
      }
    ]
  }
}
```

---

## 3. Skills Configuration Policy

### Skills vs Other Settings Comparison

| Feature | Load Timing | Primary Users | Token Efficiency |
|---------|------------|--------------|-----------------|
| **Project Description File** | Always loaded | Project team | Low (always loaded) |
| **Skills** | Load on demand | AI auto | High (on-demand) |
| **Slash Commands** | On user call | Developers | Medium |
| **Plugins/MCP** | On install | Team/Community | Varies |

### Selection Guide
```
Rules that always apply → Project Description File
Knowledge needed only for specific tasks → Skills (token efficient)
Frequently used commands → Slash Commands
External service integration → Plugins / MCP
```

### Custom Skill Creation

```bash
# Create skill directory
mkdir -p ~/.claude/skills/my-skill

# Write SKILL.md
cat > ~/.claude/skills/my-skill/SKILL.md << 'EOF'
---
name: my-skill
description: My custom skill
platforms: [Claude, Gemini, ChatGPT]
---

# My Skill

## When to use
- When needed for specific tasks

## Instructions
1. First step
2. Second step
EOF
```

---

## 4. Security Policy

### Prohibited Actions (DO NOT)

#### Absolutely Forbidden
- Using unrestricted permission mode on host systems
- Auto-approving root directory deletion commands
- Committing secret files like `.env`, `credentials.json`
- Hardcoding API keys

#### Requires Caution
- Indiscriminate approval of `sudo` commands
- Running scripts in `curl | sh` format
- Setting excessive permissions with `chmod 777`
- Connecting to unknown MCP servers

### Approved Command Audit

```bash
# Check for dangerous commands with cc-safe tool
npx cc-safe .
npx cc-safe ~/projects

# Detection targets:
# - sudo, rm -rf, chmod 777
# - curl | sh, wget | bash
# - git reset --hard, git push --force
# - npm publish, docker run --privileged
```

### Safe Auto-approval (Claude Code)

```bash
# Auto-approve only safe commands
/sandbox "npm test"
/sandbox "npm run lint"
/sandbox "git status"
/sandbox "git diff"

# Pattern approval
/sandbox "git *"       # All git commands
/sandbox "npm test *"  # npm test related

# MCP tool patterns
/sandbox "mcp__server__*"
```

---

## 5. Team Configuration Sharing

### Project Configuration Structure

```
project/
├── .claude/                    # Claude Code settings
│   ├── team-settings.json
│   ├── hooks/
│   └── skills/
├── .agent-skills/              # Universal skills
│   ├── backend/
│   ├── frontend/
│   └── ...
├── CLAUDE.md                   # Project description for Claude
├── .cursorrules               # Cursor settings
└── ...
```

### team-settings.json Example

```json
{
  "permissions": {
    "allow": [
      "Read(src/)",
      "Write(src/)",
      "Bash(npm test)",
      "Bash(npm run lint)"
    ],
    "deny": [
      "Bash(rm -rf /)",
      "Bash(sudo *)"
    ]
  },
  "hooks": {
    "PreToolUse": {
      "command": "bash",
      "args": ["-c", "echo 'Team hook: validating...'"]
    }
  },
  "mcpServers": {
    "company-db": {
      "command": "npx",
      "args": ["@company/db-mcp"]
    }
  }
}
```

### Team Sharing Workflow
```
Commit .claude/ folder → Team members Clone → Same settings automatically applied → Team standards maintained
```

---

## 6. Multi-Agent Configuration

### Per-Agent Configuration Files

| Agent | Config File | Location |
|-------|------------|---------|
| Claude Code | CLAUDE.md, settings.json | Project root, ~/.claude/ |
| Gemini CLI | .geminirc | Project root, ~/ |
| Cursor | .cursorrules | Project root |
| ChatGPT | Custom Instructions | UI settings |

### Shared Skills Directory
```
.agent-skills/
├── backend/
├── frontend/
├── code-quality/
├── infrastructure/
├── documentation/
├── project-management/
├── search-analysis/
└── utilities/
```

---

## 7. Environment Configuration Checklist

### Initial Setup

- [ ] Create project description file (`/init` or manual)
- [ ] Set up terminal aliases (`c`, `cc`, `g`, `cx`)
- [ ] Configure external editor (`export EDITOR=vim`)
- [ ] Connect MCP servers (if needed)

### Security Setup

- [ ] Configure Hooks for dangerous commands
- [ ] Review approved command list (`cc-safe`)
- [ ] Verify .env file in .gitignore
- [ ] Prepare container environment (for experimentation)

### Team Setup

- [ ] Commit .claude/ folder to Git
- [ ] Write team-settings.json
- [ ] Team standard project description file template

---

## Quick Reference

### Configuration File Locations
```
~/.claude/settings.json     # Global settings
~/.claude/skills/           # Global skills
.claude/settings.json       # Project settings
.claude/skills/             # Project skills
.agent-skills/              # Universal skills
CLAUDE.md                   # Project AI manual
```

### Security Priority
```
1. Block dangerous commands with Hooks
2. Auto-approve only safe commands with /sandbox
3. Regular audit with cc-safe
4. Experiment mode in containers only
```

### Token Efficiency
```
Project Description File: Always loaded (keep concise)
Skills: Load on demand (token efficient)
.toon mode: 95% token savings
```
