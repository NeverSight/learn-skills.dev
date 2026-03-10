---
name: agent-tool-selection
description: Guide for selecting appropriate VS Code Copilot tools when configuring agents, including environment-specific considerations.
---

# Agent Tool Selection Skill

## Purpose
Provides guidance for selecting the correct VS Code Copilot tools when creating or modifying agent definitions, with awareness of environment-specific tool availability.

## When to Use
- When configuring the `tools:` array in an agent's frontmatter
- When troubleshooting "tool not found" errors
- When adapting agents for both local (VS Code) and cloud (GitHub) environments

## Tool Awareness

You are always provided with a list of all available tools, even though you will not need to use many of them. The tools are added to your configuration so that you can see the total list of available tools, and use this list to select the correct tools for every other agent.

## Available VS Code Copilot Tools

For a complete reference of official tool IDs, consult the [VS Code Copilot Chat Tools documentation](https://code.visualstudio.com/docs/copilot/reference/copilot-vscode-features#_chat-tools).

**Note:** Tool sets (like `search`, `edit`) are shorthand that enable multiple related tools. For granular control, use the prefixed individual tools.

**Critical:** Never use snake_case names like `read_file` or `run_in_terminal` - VS Code silently ignores invalid tool names.

## Tool Usage by Environment

### Both Environments (Safe for All Contexts)
- `search` - Code and file search
- `web` - Web search for external information
- `github/*` - GitHub operations (repos, PRs, issues)
- `memory/*` - Memory storage (if configured)

### VS Code Only (Not Available in Cloud)
- `vscode` - VS Code-specific operations
- `execute` / `read` - Terminal execution and output reading
- `edit` - Direct file editing
- `todo` - VS Code TODO panel integration
- `copilot-container-tools/*` - Local Docker/container tools
- `io.github.chromedevtools/*` - Local browser DevTools

### Cloud Context Alternatives
- Instead of `edit` → Describe changes in PR or use GitHub API
- Instead of `execute` → Rely on GitHub Actions workflows
- Instead of `todo` → Track tasks in issue/PR description

## Best Practices

- **Verify tool names**: Always check tool names against your available tools list (case-sensitive)
- **Environment awareness**: When modifying agents intended for both environments, prefer tools available in both contexts
- **Conditional logic**: For environment-specific functionality, add conditional instructions in the agent definition
- **Avoid snake_case**: Tool names use camelCase or slash notation, never snake_case
- **Use tool sets**: For common combinations (e.g., `search`, `edit`), use the shorthand unless you need granular control

## Common Mistakes to Avoid

❌ Using snake_case: `read_file`, `run_in_terminal`
✅ Correct naming: `readFile`, `runInTerminal`

❌ Assuming all tools work in cloud: `execute`, `edit`
✅ Cloud-aware: Use conditional logic or stick to universal tools

❌ Hardcoding tool lists in instructions
✅ Dynamic lookup: Reference your own available tools list when configuring other agents
