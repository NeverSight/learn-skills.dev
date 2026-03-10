---
name: agent-file-structure
description: Standard structure and key principles for agent definition markdown files.
---

# Agent File Structure Skill

## Purpose
Defines the required structure and best practices for creating agent definition files in `.github/agents/*.agent.md`.

## When to Use
- When creating a new agent definition file
- When reviewing or refactoring existing agent definitions
- When ensuring consistency across the agent ecosystem

## Required Structure

All agents must follow this structure:

```markdown
---
description: Brief, specific description (≤100 chars)
name: Workflow Engineer (coding agent)
model: <model name>
---

# Agent Name Agent

You are the **Agent Name** agent for this project...

## Your Goal
Single, clear goal statement.

## Boundaries
✅ Always Do: ...
⚠️ Ask First: ...
🚫 Never Do: ...

## Context to Read
- Relevant docs with links

## Workflow
Step-by-step numbered approach

## Output
What this agent produces
```

## Key Principles

- **Specific over general** - "Write unit tests for React components" beats "Help with testing"
- **Commands over descriptions** - Include exact commands: `npm test`, `dotnet build`
- **Examples over explanations** - Show real code examples, not abstract descriptions
- **Boundaries first** - Clear rules prevent mistakes

## Frontmatter Requirements

The YAML frontmatter at the top of each agent file must include:
- `description`: Brief description (100 characters or less) that explains the agent's purpose
- `name`: The agent's display name (include "(coding agent)" or local agent type)
- `model`: **VS Code agents only** — The language model assigned to this agent (must exist in docs/ai-model-reference.md)

> ⚠️ **Coding agents (`*-coding-agent.agent.md`) must NOT include `model:` in frontmatter.**
> The `model:` property is not supported on GitHub.com coding agents and causes a hard
> `CAPIError: 400 The requested model is not supported` error, preventing the agent from running.
> VS Code agents (without the `-coding-agent` suffix) should always include `model:` for LLM selection.
> See [docs/ai-model-reference.md](../../docs/ai-model-reference.md) for details.

## Section Guidelines

### Your Goal
- One clear sentence describing what the agent accomplishes
- Focus on outcomes, not process
- Example: "Implement features and tests according to specifications"

### Boundaries
- **✅ Always Do**: Mandatory actions the agent must take (use specific commands)
- **⚠️ Ask First**: Situations requiring maintainer approval before proceeding
- **🚫 Never Do**: Actions that are explicitly forbidden or outside agent scope

### Context to Read
- List of documentation files the agent should review before starting work
- Use relative paths with links (e.g., `[docs/spec.md](../../docs/spec.md)`)

### Workflow
- Numbered steps in logical sequence
- Include exact commands where applicable
- Specify decision points and branching logic

### Output
- List of artifacts the agent produces
- Include file locations and formats
- Clarify deliverables vs intermediate work

## Best Practices

- **Be specific**: Include exact file paths, command syntax, and expected outputs
- **Use examples**: Show don't tell - include code snippets and command examples
- **Keep it actionable**: Every instruction should be something the agent can execute
- **Avoid ambiguity**: Use precise language and avoid vague terms like "usually" or "might"
