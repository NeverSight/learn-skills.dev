---
name: agent-creator
description: Guide for creating custom Claude Code subagents. Use when user wants to create a new agent (or update an existing agent) that handles specific types of tasks with custom prompts, tool restrictions, and permissions. Triggers on requests to create agents, subagents, custom agents, or when user wants specialized AI assistants for specific workflows.
---

# Agent Creator

Create subagents as Markdown files with YAML frontmatter. Store in:
- `~/.claude/agents/` - User-level (all projects)
- `.claude/agents/` - Project-level (current project only)

## Subagent File Structure

```markdown
---
name: agent-name
description: When Claude should delegate to this agent
tools: Read, Grep, Glob
model: sonnet
---

System prompt instructions for the agent go here.
The agent receives only this prompt, not the full Claude Code system prompt.
```

## Required Fields

| Field | Description |
|-------|-------------|
| `name` | Unique identifier (lowercase, hyphens only) |
| `description` | When to delegate - Claude uses this to decide. Include "use proactively" for automatic delegation |

## Optional Fields

| Field | Default | Description |
|-------|---------|-------------|
| `tools` | All | Comma-separated tool names. See [configuration.md](references/configuration.md) for full list |
| `disallowedTools` | None | Tools to deny from inherited set |
| `model` | sonnet | `sonnet`, `opus`, `haiku`, or `inherit` |
| `permissionMode` | default | `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan` |
| `skills` | None | Skills to load into agent context at startup |
| `hooks` | None | Lifecycle hooks (`PreToolUse`, `PostToolUse`, `Stop`) |

For detailed options and all available tools, see [references/configuration.md](references/configuration.md).

## System Prompt Guidelines

- Be specific about what the agent should do when invoked
- Include a clear workflow (numbered steps)
- Define output format expectations
- Keep focused on one domain/task

## Examples

### Read-Only Reviewer

```markdown
---
name: code-reviewer
description: Reviews code for quality and security. Use proactively after code changes.
tools: Read, Grep, Glob, Bash
model: inherit
---

Review code and provide actionable feedback.

When invoked:
1. Run git diff to see recent changes
2. Focus on modified files
3. Check for: clarity, duplication, error handling, security, tests

Format feedback by priority:
- Critical (must fix)
- Warnings (should fix)
- Suggestions (consider)
```

### Read-Write Fixer

```markdown
---
name: debugger
description: Debug and fix errors, test failures, unexpected behavior. Use proactively for issues.
tools: Read, Edit, Bash, Grep, Glob
---

Debug issues with systematic root cause analysis.

When invoked:
1. Capture error message and stack trace
2. Identify reproduction steps
3. Isolate failure location
4. Implement minimal fix
5. Verify solution

Provide: root cause, evidence, code fix, prevention.
```

### Hook-Validated Agent

```markdown
---
name: db-reader
description: Execute read-only database queries for analysis and reports.
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly.sh"
---

Execute SELECT queries only. Explain that write access is unavailable if requested.
```

## Best Practices

1. **Focus agents narrowly** - One agent per domain/task
2. **Write clear descriptions** - Claude uses these for delegation decisions
3. **Limit tools appropriately** - Grant only what's needed
4. **Use hooks for validation** - When you need finer control than tool restrictions
5. **Test with real tasks** - Verify the agent behaves as expected
