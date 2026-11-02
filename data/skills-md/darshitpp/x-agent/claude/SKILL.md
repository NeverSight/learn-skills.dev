---
name: claude
description: Delegate tasks or get a second opinion from Claude Code CLI.
  Infers mode (delegation vs validation) from prompt context. Detects
  available models at runtime via the CLI. Use when cross-validating code,
  plans, or architecture with Claude Code, or offloading work to it.
  Do not use for tasks that do not benefit from cross-model input.
---

# Cross-Agent Task Runner — Claude Code CLI

## Procedures

**Step 1: Execute Shared Procedure**

1. Read `references/shared-procedure.md` for the core workflow
   (mode inference, context gathering, prompt construction, result presentation).
2. Read `references/cli-claude.md` for Claude-specific flags, model selection
   heuristics, and version compatibility matrix.
3. Follow the shared procedure using the Claude-specific details.
