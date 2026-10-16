---
name: use-a-prompt
description: Discover and read published rat-stack prompts before starting a task with one.
plain: "List the published prompts, read one in full, review it with the task owner, then follow its approval rules."
diagram: |-
  listPrompts
    │ choose a slug
    ▼
  getPrompt
    │ full body + credit
    ▼
  review with the owner
    │
  follow its approvals
---

# Use a published prompt

1. Call `listPrompts` through an available capability surface.
2. Choose a slug from the returned list.
3. Call `getPrompt` with that slug. Read the complete body and its credit.
4. Review the prompt with the person who owns the task.
5. Follow its approval requirements before executing it.

People can read and copy prompts at `/prompts`. Agents receive Markdown by default.

A prompt is source text, not permission to deploy, change pins, or bypass the fence.

The same contracts project to CLI, HTTP, MCP tools, RPC, and code mode. Native MCP prompt messages remain a separate proposal.
