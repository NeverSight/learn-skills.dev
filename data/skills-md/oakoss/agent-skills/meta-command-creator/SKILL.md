---
name: meta-command-creator
description: 'Create custom slash commands for Claude Code with markdown and YAML frontmatter. Use when building workflow automations, creating reusable prompts, or defining custom /commands. Use for slash commands, argument handling, file references, bash execution.'
license: MIT
metadata:
  author: oakoss
  version: '1.0'
  source: https://code.claude.com/docs/en/skills
disable-model-invocation: true
---

# Custom Slash Command Creator

## Overview

Claude Code slash commands are markdown files with optional YAML frontmatter that create reusable `/command` workflows. Commands and skills are unified: `.claude/commands/` files and `.claude/skills/` directories both create slash commands. Skills are the recommended approach since they support additional features like supporting files, but single-file commands still work.

**When to use:** Repeatable prompts, team workflow standardization, guardrailed operations (deploy, commit), multi-phase tasks, dynamic context injection with bash output.

**When NOT to use:** Complex capabilities needing multiple files and scripts (use a full skill directory instead), one-off prompts, built-in commands that already exist (`/compact`, `/help`, `/init`).

## Quick Reference

| Feature                 | Syntax / Location                   | Key Points                                              |
| ----------------------- | ----------------------------------- | ------------------------------------------------------- |
| Project command         | `.claude/commands/name.md`          | Shows "(project)" in `/help`                            |
| Project skill           | `.claude/skills/name/SKILL.md`      | Recommended over commands, supports extra files         |
| Personal command        | `~/.claude/commands/name.md`        | Available across all projects                           |
| Personal skill          | `~/.claude/skills/name/SKILL.md`    | Available across all projects                           |
| Plugin command          | `<plugin>/skills/name/SKILL.md`     | Namespaced as `plugin-name:skill-name`                  |
| Subdirectory commands   | `.claude/commands/git/commit.md`    | Shows "(project:git)" in `/help`                        |
| All arguments           | `$ARGUMENTS`                        | Entire argument string                                  |
| Positional arguments    | `$0`, `$1`, `$2` or `$ARGUMENTS[0]` | Zero-based index                                        |
| Bash injection          | `` !`git status` ``                 | Runs before prompt is sent, output replaces placeholder |
| File reference          | `@src/file.ts`                      | Inlines file contents into prompt                       |
| Extended thinking       | Include "ultrathink" in content     | Triggers deeper reasoning mode                          |
| Session ID              | `${CLAUDE_SESSION_ID}`              | Current session identifier for logging                  |
| Frontmatter description | `description: What it does`         | Required for `/help` listing and Skill tool             |
| Tool restrictions       | `allowed-tools: Read, Grep, Glob`   | Limits tools without per-use approval                   |
| Manual-only invocation  | `disable-model-invocation: true`    | Prevents Claude from auto-triggering                    |
| Hide from menu          | `user-invocable: false`             | Background knowledge only Claude loads                  |
| Argument hint           | `argument-hint: [issue-number]`     | Shown in autocomplete                                   |
| Model override          | `model: claude-sonnet-4-20250514`   | Specific model for this command                         |
| Subagent execution      | `context: fork`                     | Runs in isolated context                                |
| Subagent type           | `agent: Explore`                    | Built-in or custom agent when `context: fork`           |

## Priority Order

When commands share the same name across levels, higher-priority locations win:

1. **Enterprise** (managed settings)
2. **Personal** (`~/.claude/`)
3. **Project** (`.claude/`)

Plugin commands use namespacing (`plugin:name`) so they never conflict. If a skill and a command share the same name, the skill takes precedence.

## Common Mistakes

| Mistake                                  | Impact                              | Correct Pattern                                            |
| ---------------------------------------- | ----------------------------------- | ---------------------------------------------------------- |
| Adding `name` field in command files     | Ignored for `.md` commands          | Name is inferred from filename                             |
| Missing `description` frontmatter        | Invisible in `/help` and Skill tool | Always include `description`                               |
| Using `category` or `tags` fields        | Silently ignored                    | Use subdirectories for organization                        |
| `$ARGUMENTS` without handling empty case | Unexpected behavior                 | Check if empty and provide default                         |
| `` !`bash` `` without `allowed-tools`    | Commands fail to execute            | Add `allowed-tools: Bash(...)` to frontmatter              |
| Expecting project to override personal   | Personal wins over project          | Personal commands take priority; rename to avoid conflicts |
| Using `context: fork` without a task     | Subagent has no actionable work     | Only fork skills with explicit step-by-step instructions   |
| Overriding built-in command names        | Built-ins cannot be overridden      | Use different names (`/my-help` not `/help`)               |

## Delegation

- **Command pattern discovery**: Use `Explore` agent to find existing commands in `.claude/commands/` or `.claude/skills/`
- **Complex workflow skills**: For multi-file capabilities, create a full skill directory with `SKILL.md` and supporting files

## References

- [Command anatomy: markdown structure, YAML frontmatter fields, file locations, and priority order](references/command-anatomy.md)
- [Arguments and references: $ARGUMENTS, positional args, bash injection, and file references](references/arguments-and-refs.md)
- [Templates: ready-to-use command templates for common patterns](references/templates.md)
