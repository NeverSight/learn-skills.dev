---
name: meta-agent-creator
description: |
  Creates custom subagents for Claude Code with YAML frontmatter configuration in Markdown files. Covers agent scoping (project, user, CLI, plugin), tool access control, model selection, permission modes, skill preloading, and lifecycle hooks.

  Use when building specialized subagents, configuring tool access, selecting models, setting permission modes, or designing delegation patterns. Use for agent creation, subagent configuration, custom agent setup.
license: MIT
metadata:
  author: oakoss
  version: '1.0'
  source: https://code.claude.com/docs/en/sub-agents
disable-model-invocation: true
---

# Custom Agent Creator

## Overview

Subagents are specialized AI assistants defined as Markdown files with YAML frontmatter. Each subagent runs in its own context window with a custom system prompt, specific tool access, and independent permissions. When a task matches a subagent's description, the parent conversation delegates to it automatically, preserving main context while enforcing constraints.

**When to use:** Isolating high-volume operations (tests, logs), enforcing read-only access for reviewers, routing simple tasks to cheaper models, running parallel research, creating reusable team workflows.

**When NOT to use:** Tasks requiring frequent back-and-forth, quick targeted changes, workflows needing nested delegation (subagents cannot spawn subagents), latency-sensitive operations where fresh context gathering is costly.

## Quick Reference

| Pattern                 | Configuration                  | Key Points                                              |
| ----------------------- | ------------------------------ | ------------------------------------------------------- |
| File location (project) | `.claude/agents/name.md`       | Shared via version control, priority 2                  |
| File location (user)    | `~/.claude/agents/name.md`     | Available across all projects, priority 3               |
| Required fields         | `name`, `description`          | Only two fields are mandatory                           |
| Tool restriction        | `tools: Read, Grep, Glob`      | Allowlist; inherits all if omitted                      |
| Tool denial             | `disallowedTools: Write, Edit` | Denylist; removed from inherited set                    |
| Model selection         | `model: haiku`                 | Options: `sonnet`, `opus`, `haiku`, `inherit` (default) |
| Permission mode         | `permissionMode: dontAsk`      | Controls permission prompt behavior                     |
| Skill preloading        | `skills: [auth, api-patterns]` | Injected at startup; no inheritance from parent         |
| Lifecycle hooks         | `hooks: { PreToolUse: [...] }` | Validate or block tool usage conditionally              |
| CLI-defined agent       | `claude --agents '{...}'`      | Session-only, highest priority, JSON format             |
| Interactive creation    | `/agents` command              | Guided setup with Claude generation                     |
| Proactive triggers      | `"Use proactively after..."`   | Include in description for auto-delegation              |

## Common Mistakes

| Mistake                                         | Correct Pattern                                                  |
| ----------------------------------------------- | ---------------------------------------------------------------- |
| Using opus for simple checklist reviews         | Use haiku for read-only reviews and style checks                 |
| Omitting output format in system prompt         | Include structured output template for consistent results        |
| Listing tools explicitly when all are needed    | Omit `tools` field to inherit all tools including MCP            |
| Expecting skills from parent conversation       | Explicitly list skills in the `skills` field                     |
| Generic description without triggers            | Include specific trigger phrases like "Use proactively when..."  |
| Giving a single agent too many responsibilities | Design focused agents with one clear purpose each                |
| Using `bypassPermissions` without caution       | Prefer `acceptEdits` or `dontAsk` for safer automation           |
| Creating deeply nested agent workflows          | Chain subagents from main conversation; nesting is not supported |

## Delegation

- **Agent pattern discovery**: Use `Explore` agent to find existing agents in `.claude/agents/`
- **Interactive creation**: Use `/agents` command for guided setup with Claude generation
- **Code review of agent files**: Use `Task` agent to validate system prompts and configuration

## References

- [Agent configuration: YAML fields, file locations, and priority order](references/agent-configuration.md)
- [Tool selection: access patterns, common combinations, and model guide](references/tool-selection.md)
- [Templates: ready-to-use agent patterns for common workflows](references/templates.md)
