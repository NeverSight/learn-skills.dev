---
name: opencode-command-creator
description: Create custom OpenCode commands with proper structure and configuration
tags: [opencode, command, cli, automation]
version: 1.0.0
---

# OpenCode Command Creator

Use this skill when creating OpenCode custom commands that allow users to define reusable prompts and workflows.

## When to Use

Use this skill when the user wants to:
- Create new OpenCode custom commands
- Define command templates with arguments
- Set up command configurations
- Override or extend built-in commands

## Command Structure

OpenCode commands can be defined in two ways:

### 1. Markdown Files (Recommended)

Create `.md` files in:
- **Global**: `~/.config/opencode/commands/`
- **Per-project**: `.opencode/commands/`

**Format:**
```markdown
---
description: Brief description of command
agent: agent-name (optional)
model: model-identifier (optional)
subtask: true/false (optional)
---

Command template with $ARGUMENTS placeholder
and other prompt content.
```

**Example:**
```markdown
---
description: Run tests with coverage
agent: build
model: anthropic/claude-3-5-sonnet-20241022
---

Run the full test suite with coverage report and show any failures.
Focus on the failing tests and suggest fixes.
```

### 2. JSON Configuration

Add to `opencode.jsonc`:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "command": {
    "command-name": {
      "template": "Prompt template text",
      "description": "Brief description",
      "agent": "agent-name",
      "model": "model-identifier",
      "subtask": false
    }
  }
}
```

## Configuration Options

### Required
- **`template`**: The prompt sent to the LLM when command executes

### Optional
- **`description`**: Brief description shown in TUI
- **`agent`**: Which agent should execute the command
- **`subtask`**: Boolean to force subagent invocation
- **`model`**: Override default model for this command

## Template Features

### Arguments
Use placeholders in templates:
- `$ARGUMENTS` - All arguments as single string
- `$1`, `$2`, `$3`, etc. - Individual positional arguments

**Example:**
```markdown
Create a React component named $ARGUMENTS with TypeScript support.
```

Usage: `/component Button`

### Shell Output
Inject bash command output with `` !`command` ``:

```markdown
Here are the current test results:
!`npm test`

Based on these results, suggest improvements.
```

### File References
Include file content with `@filename`:

```markdown
Review the component in @src/components/Button.tsx.
Check for performance issues.
```

## Examples

### Simple Command
```markdown
---
description: Format all files
---

Run the code formatter on all source files and report any changes.
```

### Command with Arguments
```markdown
---
description: Create new feature
agent: code
---

Create a new feature for $ARGUMENTS.
Include tests and documentation.
```

### Command with Shell Output
```markdown
---
description: Analyze git changes
---

Recent commits:
!`git log --oneline -10`

Review these changes and suggest improvements.
```

### Complex Command
```markdown
---
description: Full code review
agent: reviewer
model: anthropic/claude-sonnet-4-5
subtask: true
---

Review the following files: $ARGUMENTS

Check for:
1. Code quality issues
2. Security vulnerabilities
3. Performance problems

Current test status:
!`npm test`
```

## Best Practices

1. **Use descriptive names**: Command names should be clear and memorable
2. **Add descriptions**: Always include descriptions for TUI display
3. **Choose file location wisely**:
   - Use global commands for general-purpose utilities
   - Use project commands for project-specific workflows
4. **Leverage arguments**: Make commands flexible with `$ARGUMENTS` and positional params
5. **Use appropriate agents**: Match commands to the right agent for the task
6. **Consider subtasks**: Use `subtask: true` to keep primary context clean
7. **Test commands**: Try commands with different arguments before committing

## Implementation Steps

When creating a command:

1. **Determine scope**: Global or project-specific?
2. **Choose format**: Markdown (preferred) or JSON config?
3. **Define structure**:
   - Required: template
   - Optional: description, agent, model, subtask
4. **Add template features** as needed:
   - Arguments placeholders
   - Shell command outputs
   - File references
5. **Test the command**: Run in TUI with various inputs
6. **Document usage**: Add to project docs if project-specific

## Notes

- Custom commands can override built-in commands (`/init`, `/undo`, `/redo`, etc.)
- Commands run in the project's root directory
- Shell commands use bash syntax
- File references automatically include content in the prompt
- Markdown filename becomes command name (e.g., `test.md` → `/test`)
