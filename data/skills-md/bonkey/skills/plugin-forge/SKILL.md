---
name: plugin-forge
description: "Create Claude Code plugins, skills, commands, agents, hooks, MCP servers, and marketplace files. Use when building a plugin, packaging skills for sharing, creating a marketplace, converting standalone config to a plugin, or deciding between plugin vs skill vs MCP vs standalone."
---

# Plugin Forge

Guide for creating Claude Code plugins. For full reference, see `references/plugins-reference.md`.

## Step 1: Decide What to Build

Ask the user these questions to determine the right approach:

**Q1: Will this be used in one project or shared across projects/team?**
- One project → standalone (`.claude/` directory) or skill
- Shared → plugin

**Q2: Should Claude use it automatically or should the user invoke it explicitly?**
- Automatically (context-based) → skill (SKILL.md)
- Explicitly (`/command`) → command (markdown file)

**Q3: Does it need to connect to external services/APIs?**
- Yes → MCP server (standalone or inside plugin)
- No → skill or command

**Q4: Should it run code automatically on events (file save, tool use, etc.)?**
- Yes → hook
- No → skill or command

**Q5: Does it need a specialized AI agent with its own system prompt?**
- Yes → agent
- No → skill or command

### Decision Summary

| Need | Solution | Location |
|------|----------|----------|
| Personal, one project, auto-triggered | Standalone skill | `.claude/skills/<name>/SKILL.md` |
| Personal, one project, user-invoked | Standalone command | `.claude/commands/<name>.md` |
| Shared, auto-triggered | Plugin with skill | `plugin/skills/<name>/SKILL.md` |
| Shared, user-invoked | Plugin with command | `plugin/commands/<name>.md` |
| External API access | MCP server | `.mcp.json` (standalone or plugin) |
| Event automation | Hook | `hooks/hooks.json` (standalone or plugin) |
| Specialized AI role | Agent | `agents/<name>.md` |
| Multiple of the above | Plugin combining components | See plugin structure below |

### Scope: Who Can Access It?

| Scope | File | Visibility |
|-------|------|------------|
| `user` | `~/.claude/settings.json` | You only, all projects |
| `project` | `.claude/settings.json` | Team via git, this project |
| `local` | `.claude/settings.local.json` | You only, this project (gitignored) |
| `managed` | Admin-controlled | Org-wide, read-only |

## Step 2: Create the Plugin

### Directory Structure

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json           # Only this file goes here
├── skills/                   # Auto-triggered by context
│   └── skill-name/
│       └── SKILL.md
├── commands/                 # User-invoked via /plugin:command
│   └── command-name.md
├── agents/                   # Specialized subagents
│   └── agent-name.md
├── hooks/
│   └── hooks.json            # Event handlers
├── bin/                      # Executables added to PATH
├── settings.json             # Default settings
├── .mcp.json                 # MCP server configs
└── .lsp.json                 # LSP server configs
```

**Critical rules:**
- Components go at plugin root, NOT inside `.claude-plugin/`
- Plugin name must be kebab-case
- Skills must use `SKILL.md` (exact case)

### plugin.json (minimal)

```json
{
  "name": "my-plugin",
  "description": "What the plugin does",
  "version": "1.0.0"
}
```

### plugin.json (full)

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "What the plugin does",
  "author": { "name": "Name", "email": "email@example.com" },
  "homepage": "https://docs.example.com",
  "repository": "https://github.com/user/plugin",
  "license": "MIT",
  "keywords": ["keyword1"],
  "userConfig": {
    "api_key": { "description": "API key", "sensitive": true }
  }
}
```

User config values available as `${user_config.KEY}` in configs and `CLAUDE_PLUGIN_OPTION_<KEY>` env vars.

### Skill (SKILL.md)

```yaml
---
name: skill-name
description: What it does. Use when [trigger phrases].
---

Instructions for Claude.
```

### Command (commands/name.md)

```yaml
---
description: What it does
disable-model-invocation: true
---

Instructions. User input: $ARGUMENTS
```

### Agent (agents/name.md)

```yaml
---
name: agent-name
description: What it specializes in
model: sonnet
maxTurns: 20
---

System prompt here.
```

### Hook (hooks/hooks.json)

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{ "type": "command", "command": "${CLAUDE_PLUGIN_ROOT}/scripts/lint.sh" }]
    }]
  }
}
```

### MCP Server (.mcp.json)

```json
{
  "mcpServers": {
    "server-name": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"]
    }
  }
}
```

## Step 3: Test

```bash
claude --plugin-dir ./my-plugin
```

Inside session: `/reload-plugins` after changes. Validate: `claude plugin validate .`

## Step 4: Distribute

### Option A: Marketplace (for team/community)

Create `.claude-plugin/marketplace.json` in marketplace repo:

```json
{
  "name": "marketplace-name",
  "owner": { "name": "Team Name" },
  "plugins": [
    {
      "name": "plugin-name",
      "source": "./plugins/plugin-name",
      "description": "What it does",
      "version": "1.0.0"
    }
  ]
}
```

Plugin sources can be: relative path (`"./plugins/x"`), GitHub (`{ "source": "github", "repo": "owner/repo" }`), git URL, git subdirectory, or npm package.

Host on GitHub, add with: `/plugin marketplace add owner/repo`

### Option B: Direct sharing

Host plugin directory on GitHub. Users install with `--plugin-dir` or add to their `.claude/` config.

### Option C: Team auto-install

Add to project `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "team-tools": { "source": { "source": "github", "repo": "org/plugins" } }
  },
  "enabledPlugins": { "my-plugin@team-tools": true }
}
```

### Option D: Official marketplace

Submit at claude.ai/settings/plugins/submit or platform.claude.com/plugins/submit.

## Converting Standalone to Plugin

1. `mkdir -p my-plugin/.claude-plugin`
2. Create `plugin.json` with name
3. Copy `.claude/commands/` → `my-plugin/commands/`
4. Copy `.claude/skills/` → `my-plugin/skills/`
5. Copy `.claude/agents/` → `my-plugin/agents/`
6. Move hooks from settings.json → `my-plugin/hooks/hooks.json`
7. Test: `claude --plugin-dir ./my-plugin`

## Environment Variables in Plugins

- `${CLAUDE_PLUGIN_ROOT}` — plugin install path (changes on update)
- `${CLAUDE_PLUGIN_DATA}` — persistent data path (survives updates)
