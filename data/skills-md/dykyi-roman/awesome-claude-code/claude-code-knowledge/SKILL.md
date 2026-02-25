---
name: claude-code-knowledge
description: Comprehensive knowledge base for Claude Code formats, patterns, and configuration. Use when creating, improving, or auditing commands, agents, skills, hooks, memory, plugins, or settings.
---

# Claude Code Knowledge Base

## Component Types Overview

| Type | Path | Invocation | Context Cost |
|------|------|------------|--------------|
| Command | `.claude/commands/name.md` | `/name args` | Loaded on invocation |
| Agent | `.claude/agents/name.md` | `Task(subagent_type)` | Loaded into subagent context |
| Skill | `.claude/skills/name/SKILL.md` | Auto or `/name` | Loaded by description match |
| Hook | `.claude/settings.json` | Automatic on event | Zero (shell script) |
| Rules | `.claude/rules/*.md` | Auto-loaded always | Always in system prompt |
| Memory | `CLAUDE.md` (various levels) | Auto-loaded always | Always in system prompt |

---

## Commands

**Path:** `.claude/commands/name.md`
**Invocation:** `/name` or `/name arguments`

```yaml
---
description: Required. What the command does.
allowed-tools: Optional. Restrict tools (comma-separated).
model: Optional. opus/sonnet/haiku — or alias from settings.
argument-hint: Optional. Hint shown in autocomplete.
---

Command instructions here.

Use $ARGUMENTS for full argument string.
Use $ARGUMENTS[0], $ARGUMENTS[1] for positional args.
Use $1, $2 as shorthand for $ARGUMENTS[N].
Use ${CLAUDE_SESSION_ID} for session identifier.
```

**Key rules:**
- Equivalent to `.claude/skills/name/SKILL.md` with `user-invocable: true`
- Commands in subdirectories: `.claude/commands/sub/name.md` → `/sub/name`
- Budget: `SLASH_COMMAND_TOOL_CHAR_BUDGET` (default 15000 chars)

---

## Agents (Subagents)

**Path:** `.claude/agents/name.md`
**Invocation:** `Task` tool with `subagent_type="name"`

```yaml
---
name: agent-name            # required, matches filename without .md
description: Required. When to use. "PROACTIVELY" for auto-invoke.
tools: Optional. All by default. Comma-separated.
disallowedTools: Optional. Denylist complement to tools.
model: Optional. opus | sonnet | haiku | inherit
permissionMode: Optional. default | acceptEdits | plan | dontAsk | delegate | bypassPermissions
skills: Optional. Auto-load skills (comma-separated inline list).
hooks: Optional. Lifecycle hooks scoped to this agent.
memory: Optional. user | project | local — CLAUDE.md scope to load.
---

Agent system prompt here.
```

**Permission modes:**
- `default` — ask user for each tool use
- `acceptEdits` — auto-allow file edits, ask for others
- `plan` — read-only exploration, no writes
- `dontAsk` — run without asking, within sandbox
- `delegate` — inherit parent permissions
- `bypassPermissions` — skip all permission checks (dangerous)

**Built-in subagent types:** Explore, Plan, general-purpose, Bash, statusline-setup, claude-code-guide

**Execution:** foreground (blocks) or background (`run_in_background: true`). Resume via agent ID.

**Scope priority:** CLI `--agents` flag > project `.claude/agents/` > user `~/.claude/agents/` > plugin agents

---

## Skills

**Path:** `.claude/skills/name/SKILL.md`
**Invocation:** `/name` (if user-invocable) or auto-loaded by agent/description match

```yaml
---
name: skill-name            # lowercase, hyphens, max 64 chars
description: Required. What and when. Max 1024 chars.
allowed-tools: Optional. Restrict tools.
model: Optional. Model override when skill is active.
context: Optional. "fork" for isolated subagent execution.
agent: Optional. Which subagent type to run in (Explore, Plan, etc).
hooks: Optional. Lifecycle hooks scoped to this skill.
disable-model-invocation: true   # only user can invoke
user-invocable: false            # only Claude can invoke
---

Skill instructions here.

Use $ARGUMENTS, $ARGUMENTS[N], $N for user input.
Use !`command` for dynamic context injection (shell output inserted).
```

**Folder structure:**
```
skill-name/
├── SKILL.md        # required, max 500 lines
├── references/     # large content extracted here
├── scripts/        # executable code
└── assets/         # templates, resources
```

**Invocation control matrix:**

| `disable-model-invocation` | `user-invocable` | Who can invoke |
|---------------------------|------------------|----------------|
| false (default) | true (default) | Both user and Claude |
| true | true | User only (via `/name`) |
| false | false | Claude only (auto-load) |
| true | false | Nobody (disabled) |

---

## Hooks

**Path:** `.claude/settings.json` (or agent/skill frontmatter `hooks:` field)

### Hook Events (12)

| Event | When | Matcher | Can Block |
|-------|------|---------|-----------|
| `PreToolUse` | Before tool execution | Tool name | Yes |
| `PostToolUse` | After tool execution | Tool name | No |
| `Notification` | On notification | — | No |
| `Stop` | Agent stops | — | No |
| `SubagentStop` | Subagent completes | Agent name | No |
| `PreCompact` | Before context compaction | — | No |
| `PostCompact` | After context compaction | — | No |
| `ToolError` | Tool execution error | Tool name | No |
| `PreUserInput` | Before user message processed | — | No |
| `PostUserInput` | After user message processed | — | No |
| `SessionStart` | Session begins | — | No |
| `SessionEnd` | Session ends | — | No |

### Hook Types (3)

```json
{"type": "command", "command": "./script.sh"}
{"type": "prompt", "prompt": "Check if output is safe"}
{"type": "agent", "agent": "validator-agent"}
```

### Exit Codes

| Code | Behavior |
|------|----------|
| 0 | Allow (continue) |
| 2 | Block (deny tool use, PreToolUse only) |
| Other | Log warning, continue |

### Hook Configuration

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {"type": "command", "command": "php -l $CLAUDE_FILE_PATH", "async": false}
        ]
      }
    ]
  }
}
```

**Matcher patterns:** exact name, `|` OR, regex. MCP tools: `mcp__server__tool`.

For comprehensive hooks reference see [references/hooks-reference.md](references/hooks-reference.md).

---

## Memory & CLAUDE.md

### Hierarchy (top to bottom, higher = higher priority)

| Level | Location | Scope |
|-------|----------|-------|
| Managed | System dirs (enterprise) | Organization-wide |
| User | `~/.claude/CLAUDE.md` | All user projects |
| User rules | `~/.claude/rules/*.md` | All user projects |
| Project | `CLAUDE.md` (project root) | This project |
| Project rules | `.claude/rules/*.md` | This project |
| Local | `CLAUDE.local.md` (project root, auto-gitignored) | This machine only |
| Nested | `src/CLAUDE.md`, `tests/CLAUDE.md` | Subdirectory context |

### Rules Files

`.claude/rules/*.md` — modular rules, always loaded into system prompt.

**Path-specific rules** via `paths` frontmatter:
```yaml
---
paths:
  - src/Domain/**
  - src/Application/**
---
These rules apply only when working with files matching the glob patterns above.
```

### Import Syntax

```markdown
@path/to/file.md      # relative to current file
@/absolute/path.md    # absolute path
@~/user/path.md       # home directory
```

Import recursion limit: 5 hops max.

### Commands

- `/memory` — view and edit memory files
- `/init` — generate initial CLAUDE.md from project analysis

For full reference see [references/memory-and-rules.md](references/memory-and-rules.md).

---

## Plugins

**Path:** `.claude-plugin/plugin.json` (plugin root)

```json
{
  "name": "my-plugin",
  "description": "What this plugin provides",
  "version": "1.0.0",
  "author": "Name",
  "repository": "https://github.com/user/repo"
}
```

**Plugin structure:**
```
.claude-plugin/
├── plugin.json         # manifest (required)
├── commands/           # namespaced as /plugin:command
├── agents/             # available as subagent_type
├── skills/             # namespaced as /plugin:skill
├── hooks/hooks.json    # plugin-scoped hooks
├── .mcp.json           # MCP server config
└── .lsp.json           # LSP server config
```

**Namespaced invocation:** `/plugin-name:skill-name`

**Installation sources:** GitHub, Git URL, NPM, File path, Directory.

For full reference see [references/plugins-reference.md](references/plugins-reference.md).

---

## Permissions

### Rule Syntax

```json
{
  "permissions": {
    "allow": ["Read", "Glob", "Grep"],
    "deny": ["Bash(rm *)"],
    "ask": ["Write", "Edit"]
  }
}
```

**Specifier patterns:**

| Pattern | Example | Matches |
|---------|---------|---------|
| `Tool` | `Read` | All Read calls |
| `Tool(literal)` | `Bash(npm test)` | Exact command |
| `Tool(glob)` | `Read(src/**)` | Gitignore-style glob |
| `Tool(domain:)` | `WebFetch(domain:api.example.com)` | Domain filter |
| `mcp__server__tool` | `mcp__github__create_issue` | MCP tool |
| `Task(agent)` | `Task(ddd-auditor)` | Specific subagent |

**Evaluation order:** deny → ask → allow (deny wins over allow)

For full reference see [references/settings-and-permissions.md](references/settings-and-permissions.md).

---

## MCP (Model Context Protocol)

**Config:** `.mcp.json` (project root) or in `settings.json`

```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-name"],
      "env": {"API_KEY": "..."}
    }
  }
}
```

**Tool naming:** `mcp__servername__toolname`

**Scope hierarchy:** project `.mcp.json` > user settings > plugin `.mcp.json`

**Permission:** `enableAllProjectMcpServers`, `allowedMcpServers`, `deniedMcpServers` in settings.

---

## Settings

**Hierarchy:** managed > CLI args > local > project > user

| Level | Location |
|-------|----------|
| User | `~/.claude/settings.json` |
| Project | `.claude/settings.json` |
| Local | `.claude/settings.local.json` (gitignored) |
| Managed | Enterprise system dirs |

**Key settings areas:** permissions, hooks, sandbox, MCP, model config, context management, attribution.

For full schema reference see [references/settings-and-permissions.md](references/settings-and-permissions.md).

---

## Decision Framework

When to use which component type:

| Goal | Best Component | Reason |
|------|---------------|--------|
| Reusable saved prompt | **Command** | User invokes, low context cost |
| Complex analysis in isolation | **Agent** | Separate context window |
| Knowledge base / templates | **Skill** | Auto-loaded, shared across agents |
| Auto-trigger on events | **Hook** | Zero context cost, shell execution |
| Project-wide instructions | **CLAUDE.md** | Always in context |
| Path-specific rules | **Rules** (`.claude/rules/`) | Conditional loading |
| Distributable extension | **Plugin** | Namespaced, installable |
| External tool integration | **MCP** | Standardized protocol |

### Context Cost Awareness

| Component | Context Budget Impact |
|-----------|---------------------|
| CLAUDE.md + rules | Always loaded (~500 lines recommended max) |
| Skills (auto-loaded) | Loaded when description matches (~15K chars budget) |
| Skills (by agent) | Loaded into agent's context window |
| Agents | Separate context window (no parent cost) |
| Hooks (command type) | Zero context cost (shell execution) |
| Hooks (prompt/agent type) | Uses context for LLM evaluation |
| MCP tools | Tool descriptions always in context |
| Plugins | Components loaded per their type rules |

---

## Patterns

### Parallel Agents
```
Run in parallel:
1. Task: researcher — study architecture
2. Task: security-scanner — check security
3. Task: performance-analyzer — check performance

Wait for all and combine results.
```

### Progressive Disclosure
```
SKILL.md — brief instructions (max 500 lines)
references/ — details loaded when needed
scripts/ — execute without reading into context
```

### Chained Agents
```
1. researcher → studies the task
2. planner → creates plan based on research
3. implementer → implements the plan
4. reviewer → reviews implementation
```

### Agent Teams (Coordinator Pattern)
```
coordinator (opus) → delegates via Task tool
├── auditor-1 (sonnet, parallel)
├── auditor-2 (sonnet, parallel)
└── generator (sonnet, sequential after audit)

Coordinator uses TaskCreate/TaskUpdate for progress tracking.
```

### Plugin Distribution
```
Package as .claude-plugin/ → publish to GitHub/NPM
Users install: enabledPlugins in settings
Skills namespaced: /plugin-name:skill-name
```

---

## Validation Checklists

### Commands
- [ ] `description` is filled and specific
- [ ] Path: `.claude/commands/*.md`
- [ ] `$ARGUMENTS` used if `argument-hint` defined
- [ ] `model` specified consciously (opus for complex, haiku for fast)
- [ ] Instructions are clear and step-by-step

### Agents
- [ ] `name` and `description` are filled
- [ ] `name` matches filename (without `.md`)
- [ ] `tools` are minimally necessary
- [ ] `disallowedTools` used if most tools needed except few
- [ ] `model` chosen consciously
- [ ] `permissionMode` appropriate for task
- [ ] `skills:` is comma-separated inline list (not YAML array)
- [ ] Coordinators have `TaskCreate, TaskUpdate` in tools
- [ ] Coordinators have `task-progress-knowledge` in skills

### Skills
- [ ] `name` is lowercase with hyphens, matches folder name
- [ ] `description` < 1024 characters, explains "when to use"
- [ ] `SKILL.md` < 500 lines
- [ ] Large content extracted to `references/`
- [ ] `context: fork` if needs isolated execution
- [ ] Path: `.claude/skills/name/SKILL.md`

### Hooks
- [ ] JSON is valid
- [ ] Event name is one of 12 valid events
- [ ] `matcher` is correct tool/agent name or pattern
- [ ] `command` script exists and is executable
- [ ] Exit codes handled properly (0=allow, 2=block)
- [ ] `async: true` only for non-blocking operations

### Memory/Rules
- [ ] `CLAUDE.md` < 500 lines (recommended)
- [ ] `.claude/rules/*.md` for modular rules
- [ ] `CLAUDE.local.md` in `.gitignore`
- [ ] `@imports` resolve (max 5 hops)
- [ ] `paths` frontmatter uses valid glob patterns

### Settings
- [ ] Valid JSON in `settings.json`
- [ ] Permission rules follow deny → ask → allow order
- [ ] `settings.local.json` is gitignored
- [ ] Sandbox configured if auto-allowing Bash
- [ ] MCP servers explicitly allowed/denied

---

## Reference Files

Detailed documentation for specific areas:

- [Hooks Reference](references/hooks-reference.md) — all 12 events, 3 types, matchers, I/O, exit codes
- [Skills Advanced](references/skills-advanced.md) — context:fork, agent, hooks, model, invocation control
- [Subagents Advanced](references/subagents-advanced.md) — memory, hooks, disallowedTools, background, resume
- [Memory and Rules](references/memory-and-rules.md) — CLAUDE.md hierarchy, rules/, @imports, paths
- [Plugins Reference](references/plugins-reference.md) — plugin structure, manifest, marketplace, migration
- [Settings and Permissions](references/settings-and-permissions.md) — full schema, sandbox, permissions, env vars
