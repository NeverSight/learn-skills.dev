---
name: meta-plugin-creator
description: 'Create plugins for Claude Code that bundle skills, agents, commands, hooks, and MCP servers. Use when packaging reusable tooling, distributing agent capabilities, or building plugin manifests. Use for plugin creation, manifest configuration, component bundling.'
license: MIT
metadata:
  author: oakoss
  version: '1.0'
  source: 'https://code.claude.com/docs/en/plugins-reference'
disable-model-invocation: true
---

# Plugin Creator

## Overview

Plugins are shareable packages that bundle skills, agents, commands, hooks, MCP servers, and LSP servers into installable units for Claude Code. A plugin requires only a `.claude-plugin/plugin.json` manifest at minimum; all other components are optional and auto-discovered from conventional directories at the plugin root.

**When to use:** Sharing functionality across projects or teams, distributing through marketplaces, versioning reusable agent capabilities, bundling MCP servers with skills.

**When NOT to use:** Single-project customizations (use `.claude/` directory instead), quick experiments before packaging, personal workflows that do not need distribution.

## Quick Reference

| Component      | Location                       | Format          | Discovery           |
| -------------- | ------------------------------ | --------------- | ------------------- |
| Manifest       | `.claude-plugin/plugin.json`   | JSON            | Required            |
| Skills         | `skills/*/SKILL.md`            | Markdown + YAML | Auto by context     |
| Commands       | `commands/*.md`                | Markdown + YAML | Auto, namespaced    |
| Agents         | `agents/*.md`                  | Markdown + YAML | Auto, `/agents` UI  |
| Hooks          | `hooks/hooks.json`             | JSON            | Auto on events      |
| MCP servers    | `.mcp.json`                    | JSON            | Auto on enable      |
| LSP servers    | `.lsp.json`                    | JSON            | Auto on enable      |
| Output styles  | Custom path                    | Per config      | Via manifest        |
| Plugin env var | `${CLAUDE_PLUGIN_ROOT}`        | Absolute path   | All configs/scripts |
| Project env    | `${CLAUDE_PROJECT_DIR}`        | Absolute path   | All configs/scripts |
| CLI test flag  | `--plugin-dir ./my-plugin`     | Local dev       | Manual load         |
| CLI validate   | `claude plugin validate .`     | Local dev       | Manual check        |
| Install scope  | `--scope user\|project\|local` | CLI flag        | Per install         |

## Common Mistakes

| Mistake                                     | Correct Pattern                                                         |
| ------------------------------------------- | ----------------------------------------------------------------------- |
| Placing components inside `.claude-plugin/` | Only `plugin.json` goes in `.claude-plugin/`; components at plugin root |
| Using absolute paths in configs             | Use `${CLAUDE_PLUGIN_ROOT}` for all plugin file references              |
| Missing `plugin.json` manifest              | Create `.claude-plugin/plugin.json` with at least a `name` field        |
| Path traversal with `../`                   | Keep all files inside the plugin directory                              |
| Non-executable hook scripts                 | Run `chmod +x` on all scripts referenced by hooks                       |
| Forgetting namespacing                      | Plugin skills are invoked as `/plugin-name:skill-name`                  |
| Inline hooks missing event casing           | Event names are case-sensitive: `PostToolUse`, not `postToolUse`        |
| Expecting custom paths to replace defaults  | Custom component paths supplement default directories, not replace them |

## Delegation

- **Plugin component creation**: Build skills, agents, and commands following their respective standards
- **Pattern discovery**: Use `Explore` agent to find existing plugin patterns in the codebase
- **Code review**: Use `Task` agent for plugin structure validation

> If the `meta-skill-creator` skill is available, delegate skill authoring within plugins to it.
> Otherwise, recommend: `npx skills add oakoss/agent-skills --skill meta-skill-creator`

## References

- [Plugin manifest schema, directory structure, and component paths](references/plugin-anatomy.md)
- [Skills, agents, commands, hooks, MCP servers, and LSP servers in plugins](references/components.md)
- [Installation scopes, environment variables, and publishing](references/distribution.md)
