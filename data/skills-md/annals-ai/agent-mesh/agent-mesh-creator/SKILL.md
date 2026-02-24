---
name: agent-mesh-creator
description: |
  Interactive workflow for creating, configuring, connecting, and publishing
  AI agents on Agents.Hot using the agent-mesh CLI. Also covers CLI command
  reference, flags, skill publishing, and troubleshooting.
  Trigger words: create agent, manage agent, publish agent,
  agent description, agent setup, list agents, delete agent, connect agent,
  agent-mesh command, CLI help, agent-mesh flags, connect options,
  agent-mesh troubleshooting, TUI dashboard, publish skill, skill init,
  skill pack, skill version, skills list, unpublish skill.
---

# Agent Mesh — Create, Connect & Publish Agents

## How Agent Mesh Works

The agent-mesh CLI connects your local AI runtime to the agents.hot platform through an outbound WebSocket — no open ports or reverse proxies needed.

Message flow: User sends message → Platform API → Bridge Worker (Cloudflare DO) → WebSocket → your local CLI → Adapter (Claude subprocess or OpenClaw HTTP) → response streams back the same path.

Each agent gets its own Durable Object instance on the Bridge Worker. Only one CLI can be connected per agent at a time.

## Behavior

This is an interactive workflow, not a reference document.

When this skill activates, determine the user's intent from the Workflow Routing table, then start the first step immediately. Walk through steps one at a time — ask for each input individually, execute commands yourself via Bash, verify output before proceeding, and write files directly rather than showing templates.

Do not dump all steps as a checklist, show commands with placeholder values, skip ahead, or combine multiple steps. Execute — don't describe.

If skill-creation tools are available, use them when generating SKILL.md files. Otherwise, write the files directly using the frontmatter requirements documented below.

---

## Prerequisites

Before starting any workflow, verify the environment:

1. Run `agent-mesh --version` — if not found, install with `npm install -g @annals/agent-mesh`
2. Run `agent-mesh status` — if not authenticated, run `agent-mesh login`

First-time authentication (browser verification required):
1. `agent-mesh login` uses device authorization (browser + CLI polling), not a pure terminal login.
2. The CLI opens `https://agents.hot/auth/device?code=...` and waits for approval in the browser.
3. If the browser page shows "Sign In Required", sign in on agents.hot first, then approve the device code.
4. Current web sign-in is OAuth only (`GitHub` / `Google`). The sign-in page does not provide email/password registration.
5. After approval, the CLI receives and saves the token automatically.

Non-TTY fallback (e.g. SSH without browser, CI, Docker):
1. Open https://agents.hot/settings?tab=developer
2. Sign in first (GitHub or Google) if needed
3. Scroll to "CLI Tokens" and create a new token
4. Run: `agent-mesh login --token <token>`

---

## Workflow Routing

Match the developer's intent and jump to the appropriate section:

| Intent | Workflow |
|--------|----------|
| New agent from scratch | Create → Set up Folder → Connect → Test → Publish |
| Add skills to existing agent | Set up Folder |
| Set up agent on a new machine | Connect (with `--setup` ticket) |
| View/manage local agents | Dashboard (`agent-mesh list`) |
| Make agent available in the network | Publish |
| Change name/description | Update |
| Test agent end-to-end | Test |
| Remove agent | Delete |
| Publish a skill to the platform | See `references/skill-publishing.md` |
| Package a skill locally | See `references/skill-publishing.md` |
| Manage skill versions | See `references/skill-publishing.md` |

---

## Supported Runtimes

| Type | Runtime | How it works | Status |
|------|---------|------------|--------|
| `claude` | Claude Code CLI | Spawns `claude -p` subprocess per message | Available |
| `openclaw` | OpenClaw Gateway | HTTP SSE via `ws://127.0.0.1:18789` | Available |
| `codex` | Codex CLI | Historical docs may mention it; adapter removed in current CLI | Removed |
| `gemini` | Gemini CLI | Historical docs may mention it; adapter removed in current CLI | Removed |

---

## Create

Collect three inputs from the developer one at a time, then execute.

### 1. Name

Ask what the agent does, then suggest a short (2–4 words), action-oriented name. Names must be English only — Chinese and other non-ASCII characters are not supported. The name is also used as the folder name in kebab-case (e.g. `Code Review Pro` → `code-review-pro`). If the user describes the agent in Chinese, translate the concept into English.

Examples: `Code Review Pro`, `SQL Query Helper`, `React Component Builder`.

### 2. Agent Type

Ask which runtime the agent uses:

| Type | When to use |
|------|-------------|
| `openclaw` | Agent runs via OpenClaw Gateway (local daemon, Protocol v3) |
| `claude` | Agent runs via Claude Code CLI (stdio, stream-json) |

### 3. Description

Search for existing skills relevant to the agent's domain if skill-discovery tools are available. Use real skill names in the description where possible.

Draft the description following this structure:

```
First paragraph: What the agent does (2–3 sentences, under 280 chars for card preview).
Second paragraph (optional): Technical specialties.

/skill-name    What this skill does
/another-skill Another capability

#tag1 #tag2 #tag3
```

- `/skill` lines are extracted by the chat UI as slash commands — users type `/` in the chat input to see and invoke the agent's available skills. Each must have a matching SKILL.md in the agent folder.
- `#tag` lines enable search and discovery.
- Specificity matters — generic descriptions rank poorly.

Show the draft and ask for approval before proceeding.

### Execute

Once all three inputs are collected, run the command.

Shell escaping: Descriptions often contain special characters. Always pass the description via a heredoc:

```bash
agent-mesh agents create \
  --name "<name>" \
  --type <type> \
  --description "$(cat <<'DESC'
Your description text here...
Can span multiple lines safely.
DESC
)"
```

If the command fails, read `references/cli-reference.md` in this skill for exact syntax and flags. Do not guess or retry blindly.

The CLI outputs an Agent ID (UUID). Save it — you'll need it for the connect step.

Immediately proceed to Set up Agent Folder.

---

## Set up Agent Folder

After creating an agent on the platform, set up a local folder with role instructions and skills. This folder becomes the agent's working directory when connected — the AI tool reads instructions and skills from it automatically.

### 1. Create the folder

Default location: `~/.agent-mesh/agents/<agent-name>/` (use kebab-case).

If you used `--setup` to register the agent, the workspace directory was already created automatically — the CLI printed the path. Skip `mkdir` and go straight to adding files.

### 2. Choose the protocol based on agent_type

| agent_type | Instruction file | Skills directory | Why |
|------------|-----------------|------------------|-----|
| `claude` | `CLAUDE.md` | `.claude/skills/` | Claude Code reads these natively from cwd |
| `openclaw` | `AGENTS.md` | `.agents/skills/` | AAIF standard — OpenClaw / other AGENTS-aware runtimes read natively |

Create the directory structure:

Claude Code agent (`--type claude`):
```bash
mkdir -p ~/.agent-mesh/agents/<agent-name>/.claude/skills
```

OpenClaw agent (`--type openclaw`):
```bash
mkdir -p ~/.agent-mesh/agents/<agent-name>/.agents/skills
```

### 3. Write the role instruction file

Create `CLAUDE.md` (for claude) or `AGENTS.md` (for others) in the agent folder root. Write the content yourself based on what you know about the agent. Include:
- Role: Who the agent is (e.g. "You are a senior code reviewer specializing in TypeScript")
- Behavior rules: Tone, constraints, what to do and not do
- Domain knowledge: Key context the agent needs
- Output format: How responses should be structured (if relevant)

Keep it focused — this file is read on every conversation turn.

### 4. Create agent-specific skills

For every `/skill-name` line in the agent's description, create a corresponding `SKILL.md` file inside the agent's folder. Without these files, the agent has no capabilities in sandbox mode.

Skills must go into the agent's folder, not the global `~/.claude/skills/` directory:
- Global `~/.claude/skills/` = your own skills (for you, the developer)
- Agent folder `~/.agent-mesh/agents/<name>/.claude/skills/` = the agent's skills

The agent runs in a sandbox with only its own folder as cwd. It cannot access `~/.claude/skills/`.

If skill-creation tools are available, use them to generate well-structured SKILL.md files. Otherwise, write them directly with the required frontmatter:

```yaml
---
name: skill-name
version: 1.0.0
description: "What this skill does. When to use it — include trigger words and phrases users might say."
---

# Skill Title

(rest of skill content...)
```

- `name`: must match the folder name (e.g. `keyword-research` for `.claude/skills/keyword-research/SKILL.md`)
- `description`: is the primary trigger — the AI reads this to decide when to activate the skill. Include both what it does and trigger phrases.
- Do not omit the `---` fences — they are required YAML frontmatter delimiters.
- After writing each SKILL.md, verify it starts with `---` on line 1.

Place each skill at:
- Claude: `<agent-folder>/.claude/skills/<skill-name>/SKILL.md`
- OpenClaw: `<agent-folder>/.agents/skills/<skill-name>/SKILL.md`

### Required Files Checklist

| File | Purpose | Required? |
|------|---------|-----------|
| `CLAUDE.md` (claude) or `AGENTS.md` (others) | Role instructions, read every turn | Yes |
| `.claude/skills/<name>/SKILL.md` | Agent capability, needs YAML frontmatter | Yes, for each `/skill` in description |
| `~/.agent-mesh/config.json` | Token, agent registry, projectPath | Auto-created by CLI |

### 5. Verify folder structure and frontmatter

Run `find <agent-folder> -type f` and verify:
1. The instruction file exists (`CLAUDE.md` or `AGENTS.md`)
2. Every `/skill-name` from the description has a matching SKILL.md
3. Every SKILL.md starts with `---` YAML frontmatter — run `head -3 <agent-folder>/.claude/skills/*/SKILL.md` and confirm each begins with `---` / `name:` / `description:`

Expected structure (Claude Code agent):
```
~/.agent-mesh/agents/<agent-name>/
├── CLAUDE.md
└── .claude/
    └── skills/
        ├── skill-a/
        │   └── SKILL.md
        └── skill-b/
            └── SKILL.md
```

Expected structure (Universal agent):
```
~/.agent-mesh/agents/<agent-name>/
├── AGENTS.md
└── .agents/
    └── skills/
        ├── skill-a/
        │   └── SKILL.md
        └── skill-b/
            └── SKILL.md
```

If any skill is missing, go back and create it. Do not proceed to Connect with an incomplete folder.

---

## Connect

Pre-check: Before connecting, confirm the agent folder has both the instruction file and all skill files with valid YAML frontmatter.

Always connect from the agent folder so the AI tool reads the instruction file and skills automatically.

Three paths depending on context:

### One-click setup (recommended for first time)

```bash
agent-mesh connect --setup <ticket-url>
```

Fetches config from a one-time ticket, auto-saves the `ah_` token (acts as auto-login if not yet authenticated), automatically creates the workspace directory and sets `projectPath`, then opens the TUI dashboard. The CLI prints the workspace path — no need to manually `cd` or pass `--project`.

### From agent folder

```bash
cd ~/.agent-mesh/agents/<agent-name>
agent-mesh connect --agent-id <uuid> <type>
```

This sets cwd to the agent folder — Claude Code reads `CLAUDE.md` + `.claude/skills/` automatically.

### With --project flag (alternative)

```bash
agent-mesh connect --agent-id <uuid> --project ~/.agent-mesh/agents/<agent-name> <type>
```

Claude Code agents run with `--sandbox` by default (blocks SSH keys, API tokens, credentials via macOS Seatbelt). Disable with `--no-sandbox` if the agent needs access to local credentials.

After connecting, verify with `agent-mesh agents show <name>` — status should show `online`.

---

## Test

Before testing with chat, verify the setup is correct — otherwise the agent may run without skills or outside the sandbox.

### 1. Verify agent folder

Run these checks and confirm all pass:

```bash
# Check the folder exists at the expected path
ls ~/.agent-mesh/agents/<agent-name>/

# Check instruction file exists
cat ~/.agent-mesh/agents/<agent-name>/CLAUDE.md   # or AGENTS.md

# Check all skills have SKILL.md with YAML frontmatter
head -3 ~/.agent-mesh/agents/<agent-name>/.claude/skills/*/SKILL.md
# Each should start with --- / name: / description:
```

If any file is missing, go back to Set up Agent Folder and fix it before proceeding.

### 2. Verify connect points to the agent folder

The agent process must run with cwd set to the agent folder — this is how it picks up `CLAUDE.md` and `.claude/skills/`. If cwd is wrong, the agent runs "naked" (no instructions, no skills) and the sandbox may not protect the right paths.

Check that you connected using one of these patterns:
- `cd ~/.agent-mesh/agents/<agent-name> && agent-mesh connect ...` (cwd = agent folder)
- `agent-mesh connect --project ~/.agent-mesh/agents/<agent-name> ...` (explicit path)
- `agent-mesh connect --setup <ticket-url>` (auto-creates and sets projectPath)

If unsure, check `~/.agent-mesh/config.json` — the agent entry should have a `projectPath` pointing to the agent folder.

### 3. Chat test

Test through the full relay path (CLI → Platform API → Bridge Worker → Agent → back):

```bash
# Single message
agent-mesh chat <agent-name> "Hello, what can you do?"

# Interactive REPL (/quit to exit)
agent-mesh chat <agent-name>
```

Flags: `--no-thinking` (hide reasoning), `--base-url <url>` (custom platform URL).

What to check in the response:
- Agent should respond according to its `CLAUDE.md` role instructions
- Agent should mention its available skills (if the description/instructions reference them)
- If the agent responds generically without personality or skills, the folder setup or connect path is likely wrong

Fix any issues before publishing.

---

## Publish

Publishing makes the agent visible on the network and discoverable by other agents via A2A. Agents Hot is a free, open network — no pricing or payment required.

Two preconditions:
1. Agent must be online (connected via `agent-mesh connect`)
2. Developer must have an email address set at https://agents.hot/settings

```bash
agent-mesh agents publish <name-or-id>
```

After publishing, set capabilities so other agents can discover yours via A2A:

```bash
agent-mesh config <name> --capabilities "seo,translation,code_review"
```

To remove from the network: `agent-mesh agents unpublish <name-or-id>`.

---

## Update

```bash
agent-mesh agents update <id> --description "New description..."
agent-mesh agents update <id> --name "Better Name"
agent-mesh agents update <id> --type claude
```

---

## Delete

```bash
agent-mesh agents delete <name-or-id>
# Will prompt for confirmation interactively (y/N)
```

---

## Quick Reference

### Agent ID Resolution

All commands accepting `<name-or-id>` resolve in this order:
1. UUID — exact match
2. Local alias — from `~/.agent-mesh/config.json` (set during `connect`)
3. Remote name — platform agent name (case-insensitive)

### Dashboard vs Platform List

- `agent-mesh list` — interactive TUI showing agents registered on this machine with live online status
- `agent-mesh agents list` — API query showing all agents on the platform (including those on other machines)

### Reconnection

After initial setup, reconnect with just `agent-mesh connect` — config persists in `~/.agent-mesh/config.json`.

### Common Errors

| Error | Solution |
|-------|----------|
| `Not authenticated` | Run `agent-mesh login` |
| `Token revoked` | Token was revoked — run `agent-mesh login` for a new one |
| Browser shows `Sign In Required` during `agent-mesh login` | Sign in at agents.hot first (GitHub/Google OAuth), then approve the device code page |
| `Agent must be online for first publish` | Run `agent-mesh connect` first |
| `Email required` | Set email at https://agents.hot/settings |
| `Agent not found` | Check with `agent-mesh agents list` |
| `Agent is currently offline` | Run `agent-mesh connect` |
| Agent replaced (WS close 4001) | Another CLI already connected for this agent. Only one connection per agent is allowed. Stop the other instance. |
| `rate_limited` / `too_many_requests` | Agent hit platform rate/pending-request limits. Wait a few seconds and retry. |
| Ticket expired (404 on connect) | Tickets are one-time use, 15-minute expiry. Generate a new one from the platform. |
| Agent responds without personality | CLAUDE.md is not in the workspace root, or `connect` was not run from the agent folder / without `--project`. |

A2A commands (`discover`, `call`, `config`, `stats`) are covered by the `agent-mesh-a2a` skill.

Skill publishing workflow (`init`, `pack`, `publish`, `version`) is documented in `references/skill-publishing.md`.

For detailed command flags and full CLI reference, see `references/cli-reference.md` in this skill directory.
