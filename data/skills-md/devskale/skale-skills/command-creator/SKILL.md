---
name: command-creator
description: Create custom commands for Pi (prompt templates) or OpenCode. Define command prompts, arguments, shell output injection, file references, and configure agents, models, and descriptions.
license: MIT
compatibility: opencode, pi
disable-model-invocation: true
metadata:
  version: "2.0.0"
---

# Command Creator

Create custom commands to automate repetitive tasks. This skill supports:

- **Pi prompt templates** - Markdown snippets invoked via `/name` in the editor (simpler, no configuration)
- **OpenCode commands** - Custom commands with advanced configuration (agents, models, shell injection)

When asked to create a command, first ask the user which system they're targeting.

## Pi Prompt Templates

Pi prompt templates are simple Markdown files that expand in the editor when invoked.

### Locations

| Scope | Path |
|-------|------|
| Global | `~/.pi/agent/prompts/*.md` |
| Project | `.pi/prompts/*.md` |

### Format

```markdown
---
description: Review staged git changes
---
Review the staged changes (`git diff --cached`). Focus on:
- Bugs and logic errors
- Security issues
- Error handling gaps
```

**Key points:**
- Filename becomes command name: `review.md` → `/review`
- `description` in frontmatter is optional (defaults to first line)
- No special configuration required

### Arguments

Supports positional arguments and slicing:

| Placeholder | Description |
|-------------|-------------|
| `$1`, `$2`, ... | Individual positional arguments |
| `$@`, `$ARGUMENTS` | All arguments joined |
| `${@:N}` | Args from position N (1-indexed) |
| `${@:N:L}` | L args starting at position N |

Example:
```markdown
---
description: Create a React component
---
Create a React component named $1 with TypeScript and features: $@
```

Usage: `/component Button "onClick handler" "disabled support"`

### Loading

- Discovery is non-recursive (no subdirectory scanning)
- Add via `prompts` array in settings if needed
- Disable with `--no-prompt-templates`

### Example Pi Templates

**Git review template** (`.pi/prompts/review.md`):
```markdown
---
description: Review staged changes
---
Review the staged changes (`git diff --cached`). Check for:
- Bugs and logic errors
- Security vulnerabilities
- Performance issues
- Code style inconsistencies
```

**Component creation** (`.pi/prompts/component.md`):
```markdown
---
description: Create React component
---
Create a React component named $1 with TypeScript:
- Use functional components with hooks
- Export as default module
- Include PropTypes or TypeScript interface
$@
```

Usage: `/component Button`

---

## OpenCode Commands

OpenCode commands are more powerful with JSON configuration, agent/model selection, and shell injection.

### Quick Start

**Markdown format** (`.opencode/commands/test.md`):
```yaml
---
description: Run tests with coverage
agent: build
model: anthropic/claude-3-5-sonnet-20241022
---
Run the full test suite with coverage report and show any failures.
```

**JSON format** (`opencode.jsonc`):
```json
{
  "command": {
    "test": {
      "template": "Run the full test suite with coverage report and show any failures.",
      "description": "Run tests with coverage",
      "agent": "build",
      "model": "anthropic/claude-3-5-sonnet-20241022"
    }
  }
}
```

### Locations

| Scope | Path |
|-------|------|
| Global | `~/.config/opencode/commands/` |
| Project | `.opencode/commands/` |

### Arguments

Same placeholders as Pi, plus OpenCode-specific features:

| Placeholder | Description |
|-------------|-------------|
| `$ARGUMENTS` | All arguments passed to command |
| `$1`, `$2`, `$3` | Individual positional arguments |

### Shell Output Injection

Use backticks to inject bash command output (OpenCode only):

```yaml
---
description: Analyze coverage
---
Current test results:
!`npm test`
Suggest improvements based on these results.
```

### File References

Include file contents using `@`:

```yaml
---
description: Review component
---
Review @src/components/Button.tsx for performance issues.
```

### Options Reference

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `template` | string | Yes | Prompt sent to LLM |
| `description` | string | Yes | Shown in TUI command list |
| `agent` | string | No | Agent to use (defaults to current) |
| `subtask` | boolean | No | Force subagent invocation |
| `model` | string | No | Override default model |

### Built-in Commands

OpenCode includes: `/init`, `/undo`, `/redo`, `/share`, `/help`. Custom commands with the same name override built-ins.

---

## Comparison: Pi vs OpenCode

| Feature | Pi Prompts | OpenCode Commands |
|---------|------------|-------------------|
| File format | Markdown | Markdown or JSON |
| Configuration | None | agent, model, etc. |
| Shell injection | ❌ No | ✅ Yes |
| File references | ❌ No | ✅ Yes |
| Complexity | Simple | Advanced |
| Best for | Quick shortcuts | Complex workflows |

---

## Best Practices

1. **Use descriptive names** that don't conflict with built-ins
2. **Keep prompts focused and specific** - one task per template/command
3. **Use arguments** for reusable templates (Pi) and commands (OpenCode)
4. **Include descriptions** for autocomplete suggestions
5. **For Pi**: Keep it simple - no shell code or complex logic
6. **For OpenCode**: Leverage shell output for dynamic context
7. **Include file references** (`@`) for context-aware commands (OpenCode only)
8. **Test your templates/commands** after creating them