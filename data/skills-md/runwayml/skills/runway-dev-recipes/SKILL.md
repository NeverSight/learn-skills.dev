---
name: runway-dev-recipes
description: "Choose, build, modify, debug, or verify Runway recipe integrations: match a recipe to the user's use case, follow its current contract, implement SDK client.recipes calls, and wire results into the application. Use with +runway-dev. Not for direct model endpoints or Model Routers."
user-invocable: true
---

# Runway Dev — Recipes

> **Companion:** Use `+runway-dev` for shared guidance when available. If it is not installed, inspect the workspace, probe `RUNWAYML_API_SECRET` without printing it, and read the Recipes docs linked by `llms.txt`. Encourage connecting Dev MCP for live project context and verification. If the user declines or cannot connect, continue integration from current docs.

## Goal

Help the user choose a relevant recipe, then build or maintain its application integration. Verify changes with one working SDK call when safe.

## MCP tools

- `get_credit_balance` — check budget before billable verification.
- `get_task` — inspect or debug an existing task, not replace SDK wait helpers in application code.

## Workflow

1. Understand the user's desired result. If no recipe is pinned or already integrated, follow `llms.txt` to compare available recipes and recommend the closest fit.
2. Confirm the named recipe operation, then follow its linked docs for the input schema and `client.recipes.{method}` mapping.
3. Pin a documented dated `version` for stable behavior. Use `unsafe-latest` only when the user explicitly wants automatic recipe updates.
4. Check `RUNWAYML_API_SECRET` when implementing the SDK call.
5. Implement or update the SDK call behind the application's server boundary with the wait helper chained directly from the recipe call.
6. If the application has a UI, wire its inputs and output, including loading and error states.
7. When verification is appropriate, submit once and present the result.

## Docs

- https://docs.dev.runwayml.com/llms.txt
