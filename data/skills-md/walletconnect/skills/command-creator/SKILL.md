---
name: command-creator
description: Guide for creating custom Claude Code slash commands. Use when user wants to create a new command (or update an existing command) that provides a reusable prompt snippet, workflow, or automation. Triggers on requests to create /commands, slash commands, custom commands, or when user wants to define frequently-used prompts as reusable commands.
---

# Command Creator

Create custom slash commands for Claude Code. Commands are Markdown files that define reusable prompts with support for arguments, bash execution, file references, and tool permissions.

## Command Locations

| Type | Location | Scope |
|------|----------|-------|
| Project | `.claude/commands/` | Shared with team via git |
| Personal | `~/.claude/commands/` | Available across all projects |

Project commands take precedence over personal commands with the same name.

## Basic Structure

```markdown
---
description: Brief description shown in /help
---

Your prompt instructions here.
```

Filename becomes the command name: `review.md` → `/review`

## Frontmatter Options

| Field | Purpose | Default |
|-------|---------|---------|
| `description` | Brief description for /help | First line of prompt |
| `allowed-tools` | Tools the command can use | Inherits from conversation |
| `argument-hint` | Shows usage hint in autocomplete | None |
| `model` | Specific model to use | Inherits from conversation |
| `disable-model-invocation` | Prevent Skill tool from calling this | false |
| `hooks` | Command-scoped hooks (PreToolUse, PostToolUse, Stop) | None |

## Arguments

### All arguments: `$ARGUMENTS`

```markdown
---
description: Fix an issue
---
Fix issue #$ARGUMENTS following our coding standards
```

Usage: `/fix-issue 123 high-priority` → `$ARGUMENTS` = "123 high-priority"

### Positional: `$1`, `$2`, etc.

```markdown
---
argument-hint: [pr-number] [priority] [assignee]
description: Review pull request
---
Review PR #$1 with priority $2 and assign to $3.
```

Usage: `/review-pr 456 high alice`

## Bash Execution

Execute bash before the command runs using the exclamation mark prefix. Output is included in context.

```markdown
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
description: Create a git commit
---

## Context
- Current git status: !\`git status\`
- Current git diff: !\`git diff HEAD\`
- Current branch: !\`git branch --show-current\`
- Recent commits: !\`git log --oneline -10\`

## Task
Create a git commit based on the above changes.
```

**Required**: Include `allowed-tools` with the Bash tool when using bang execution (the exclamation mark prefix).

## File References

Include file contents using the `@` prefix:

```markdown
Review the implementation in @src/utils/helpers.js
Compare @src/old-version.js with @src/new-version.js
```

## Namespacing

Subdirectories group related commands. The subdirectory appears in the description:

- `.claude/commands/frontend/component.md` → `/component` (project:frontend)
- `.claude/commands/backend/test.md` → `/test` (project:backend)

Commands in different subdirectories can share names.

## Example: Complete Command

~~~markdown
---
allowed-tools: Bash(npm:*), Bash(git:*), Read, Edit, Write
argument-hint: [component-name]
description: Create a new React component with tests
model: claude-sonnet-4-20250514
---

## Context
- Existing components: !\`ls src/components/\`
- Project structure: !\`ls -la src/\`

## Task
Create a new React component named $1:
1. Create component file at @src/components/$1.tsx
2. Create test file at @src/components/$1.test.tsx
3. Export from @src/components/index.ts
4. Follow patterns in existing components
~~~

## Hooks in Commands

Define command-scoped hooks that run during execution:

```markdown
---
description: Deploy with validation
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh"
          once: true
---

Deploy to staging environment.
```

The `once: true` option runs the hook only once per session.

## Best Practices

1. **Keep prompts concise** - Claude is smart; don't over-explain
2. **Use bash execution for context** - Gather relevant state before the task
3. **Specify allowed-tools** - Limit to what the command needs
4. **Add argument-hint** - Help users understand expected arguments
5. **Use file references** - Point to relevant files with `@`
6. **Namespace related commands** - Use subdirectories for organization
