---
name: agent-conventions
description: >-
  Agent definition conventions. Use when creating or modifying agents at any
  level (~/.claude/agents/, .claude/agents/, or project-local). Validate
  frontmatter, update README.md index. NOT for creating skills, MCP servers,
  or modifying CLAUDE.md.
user-invocable: false
disable-model-invocation: false
license: MIT
metadata:
  author: wyattowalsh
  version: "1.0.0"
---

# Agent Conventions

Apply these conventions when creating or modifying AI agent definitions.

## Dispatch

| $ARGUMENTS | Action |
|------------|--------|
| Active (auto-invoked when working on agent files) | Apply all conventions below |
| Empty | Display convention summary |
| `check` | Run validation checks only |

## References

| File | Purpose |
|------|---------|
| `references/readme-template.md` | Template for agent README.md index entries |

## Conventions

### Required Frontmatter

Every agent file must include these fields in YAML frontmatter:

- `name` -- kebab-case, must match filename without `.md`
- `description` -- non-empty, describes the agent's purpose

### Optional Frontmatter

- `tools` -- comma-separated tool allowlist (default: all)
- `disallowedTools` -- comma-separated tool denylist
- `model` -- `sonnet` | `opus` | `haiku` | `inherit` (default: `inherit`)
- `permissionMode` -- `default` | `acceptEdits` | `delegate` | `dontAsk` | `bypassPermissions` | `plan`
- `maxTurns` -- integer cap on agentic turns
- `skills` -- list of skills preloaded into agent context
- `mcpServers` -- list of MCP servers available to this agent
- `memory` -- `user` | `project` | `local`
- `hooks` -- lifecycle hooks scoped to this agent

**Memory field conventions:**
- Choose the narrowest memory scope: `local` for temporary insights, `project` for shared patterns, `user` for cross-project preferences
- Keep memory entrypoint files under 200 lines — content beyond this is truncated at load time
- Organize memory by topic (e.g., `debugging.md`, `api-patterns.md`), not chronologically
- Use MEMORY.md as the index file; create separate topic files for detailed notes

### Naming

- All agent names use kebab-case: `^[a-z0-9][a-z0-9-]*$`
- Filename (without `.md`) must match the `name` frontmatter field exactly
- No consecutive hyphens, no leading/trailing hyphens

### README Index Requirement

When defining a new agent at **any** level:

- `~/.claude/agents/`
- `.claude/agents/` (project-level)
- Project-local agent directories

Update the corresponding `README.md` index in the same directory:

1. Add a row to the index table with agent name, description, and key fields
2. Add a description section with usage details
3. Keep the table sorted alphabetically by name

### Body Content

- Write the system prompt in imperative voice ("Check the logs" not "Checks the logs")
- Keep agent definitions focused on a single responsibility
- Reference skills by name rather than inlining their content

## Critical Rules

1. Always update the README.md index when adding or modifying an agent
2. Name every agent in kebab-case matching its filename exactly
3. Include both `name` and `description` in frontmatter -- they are required
4. Never duplicate agent functionality -- check existing agents first
5. Keep agent system prompts under 500 lines for maintainability
6. Run `wagents validate` after any agent frontmatter change
7. Use imperative voice throughout the agent body text

**Canonical terms** (use these exactly):
- `agent` -- an AI agent definition file in `agents/` directory
- `frontmatter` -- YAML metadata between `---` delimiters
- `system prompt` -- the markdown body after frontmatter
- `index table` -- the markdown table in README.md listing all agents
- `kebab-case` -- lowercase words separated by hyphens
