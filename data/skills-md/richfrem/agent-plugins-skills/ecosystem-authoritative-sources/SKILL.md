---
name: ecosystem-authoritative-sources
description: Provides information about how to create, structure, install, and audit Agent Skills, Plugins, Antigravity Workflows, and Sub-agents. Trigger this when specifications, rules, or best practices for the ecosystem are required.
disable-model-invocation: false
allowed-tools: Bash, Read, Write
---
# Ecosystem Authoritative Sources

# Official Open Standard Recognition
**Important:** This reference library draws heavy inspiration and structural standards directly from the Anthropic Claude Plugins official repositories. Please refer to:
- **Foundational Specification**: `https://github.com/anthropics/claude-plugins-official/tree/main/plugins/plugin-dev`
- **L4 Interaction & Execution Patterns**: Derived from `https://github.com/anthropics/claude-knowledgework-plugins` (specifically the Legal and Bio-Research plugins).

# The Library
The following open standards are available for review:

This skill provides comprehensive information and reference guides about the conventions and constraints defining the extensibility ecosystem.

Because of the Progressive Disclosure architecture, you should selectively read the reference files below only when you need detailed information on that specific topic.

## Installation (`npx skills`)
This ecosystem uses the universal `npx skills` CLI to install, update, and manage plugins across all supported agents (Claude Code, Copilot, Gemini CLI, etc).

**Quick Reference:**
*   **Install from GitHub:** `npx skills add <user>/<repo>`
*   **Install Specific Skill:** `npx skills add <user>/<repo>/plugins/<plugin-name>`
*   **Update All Skills:** `npx skills update`
*   **Local Development Install:** `rm -rf .agents/ && npx skills add ./plugins/<plugin-name> --force`

*For full installation documentation and architecture rules, strictly refer to `references/skills.md`.*

## Table of Contents
To read any of the reference guides, use your file system tools to `cat` or `view` the relevant file.

*   **Agent Skills**: Definition, lifecycle, progressive disclosure, and constraints of `.claude/skills/` (and equivalents like `.agent/skills/` and `.github/skills/`). Custom agents deployed as Skills are stored here as `<plugin>-<agent>/SKILL.md`.
    *   [reference/skills.md](../../references/skills.md)
    *   [reference/diagrams/skill-execution-flow.mmd](../../references/diagrams/skill-execution-flow.mmd)
*   **Claude Plugins**: Specification for the `.claude-plugin` architecture, manifest setup, and distribution.
    *   [reference/plugins.md](../../references/plugins.md)
    *   [reference/diagrams/plugin-architecture.mmd](../../references/diagrams/plugin-architecture.mmd)
*   **Antigravity Workflows & Rules (and Legacy Commands)**: Specifications for global/workspace Rules, deterministic trajectory Workflows, and the critical distinction between deploying **Skills** vs. Legacy **Commands**.
    *   [reference/workflows.md](../../references/workflows.md)
*   **Sub-Agents**: Definition, setup, and orchestration of nested contextual LLM boundaries. Sub-Agents are deployed structurally as pure Skills (mapped to `skills/<agent-name>/SKILL.md`).
    *   [reference/sub-agents.md](../../references/sub-agents.md)
*   **GitHub Copilot Prompts (Models)**: Documentation on the exact YAML schema, dynamic variables, and exclusion logic (`exclude-targets`) used by GitHub Copilot chat environments.
    *   [reference/github-prompts.md](../../references/github-prompts.md)
*   **GitHub Agentic Workflows**: Documentation on the "Continuous AI" autonomous agents responding to CI/CD events.
    *   [reference/github-agentic-workflows.md](../../references/github-agentic-workflows.md)
*   **Hooks**: Lifecycle event integrations (e.g., `pre-commit`, `on-startup`).
    *   [reference/hooks.md](../../references/hooks.md)
*   **Azure AI Foundry Agents**: Documentation on how to map Open Agent-Skills to Azure Foundry Agent Service, including API payloads, constraints (e.g., 128-tool limits), and standard setups.
    *   [reference/azure-foundry-agents.md](../../references/azure-foundry-agents.md)
*   **Marketplace**: Registering registries and interacting with the `marketplace.json` distribution format.
    *   [reference/marketplace.md](../../references/marketplace.md)
*   **Installation & Management**: Universal CLI guidelines for `npx skills`, including remote installations, updates, and local development workarounds.
    *   [reference/npx-skills.md](../../references/npx-skills.md)

## Usage Instruction
Never guess the specifics of `SKILL.md` frontmatter, plugin directory limits, or workflow sizes. Read the exact specifications linked above before constructing new ecosystem extensions.
