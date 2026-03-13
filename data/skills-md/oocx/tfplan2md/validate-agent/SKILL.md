---
name: validate-agent
description: Validate agent definitions for consistency, model availability, handoff integrity, and tool existence. Use this when creating or modifying agents.
---

# Validate Agent Skill

## Purpose
Ensure that agent definitions are technically sound, follow project standards, and are compatible with the current environment and other agents.

## When to Use
- After creating a new agent.
- After modifying an existing agent's frontmatter (model, tools, handoffs).
- When troubleshooting "dead-end" handoffs or tool execution failures.

## Workflow

### 1. Run Automated Validation
Execute the validation script to check for common errors in frontmatter and structure:

```bash
./scripts/validate-agents.py
```

This script checks:
- **Model Availability**: Verifies the model exists in `docs/ai-model-reference.md`.
- **Handoff Integrity**: Verifies that handoff targets exist.
- **Required Sections**: Ensures all mandatory headers are present.
- **Snake Case Tools**: Warns about potential invalid tool names.

### 2. Validate Tool Existence
As the **Workflow Engineer**, you have access to all available tools in the workspace. You must manually verify that every tool listed in an agent's `tools:` array exists in your own tool list.

- **Check**: Compare the agent's `tools:` list against your own available tools.
- **Wildcards**: If an agent uses a wildcard (e.g., `github/*`), ensure you have tools with that prefix.
- **Naming**: Ensure the tool IDs match exactly (case-sensitive). VS Code tools typically use `category/toolName` or `publisher.extension/toolName` format.

### 3. Verify Boundary Consistency
Check that the agent's boundaries (✅ Always Do, ⚠️ Ask First, 🚫 Never Do) are:
- **Specific**: Use concrete commands and file paths.
- **Actionable**: The agent can actually perform the "Always Do" actions with its tools.
- **Consistent**: They do not contradict project-wide instructions in `.github/copilot-instructions.md`.

### 4. Check Handoff Logic
Verify that the `handoffs:` section makes sense for the agent's role:
- Does the `prompt` provide enough context for the next agent?
- Is `send: false` used for handoffs that require user review before proceeding? (Standard for this project).

## Output
- A summary of validation results.
- Fixes for any identified issues.
- Confirmation that the agent is ready for use.
