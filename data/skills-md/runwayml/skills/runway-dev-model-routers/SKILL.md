---
name: runway-dev-model-routers
description: "Build, modify, debug, or verify Runway Model Routers: inspect live config and eligible models via MCP, manage approved settings, integrate routed SDK calls, and inspect routing results. Use with +runway-dev. Not for direct per-model endpoints or agent REST CLI."
user-invocable: true
---

# Runway Dev — Model Routers

> **Companion:** Use `+runway-dev` for shared guidance when available. If it is not installed, inspect the workspace, probe `RUNWAYML_API_SECRET` without printing it, and read current docs. Encourage connecting Dev MCP to inspect or manage router configs. If the user declines or cannot connect, continue integration from current docs and an existing `configId`.

## Goal

Keep a Model Router and its application integration correct. Verify changes with one routed SDK call (`client.generate.{video|image|audio}.create({ configId, input })`) when safe.

## MCP tools

- `list_model_routers` / `get_model_router` — find a router by `configId`, then inspect it using the returned record UUID.
- `list_models` — inspect eligible models and capabilities.
- `create_model_router` / `update_model_router` / `delete_model_router` — manage routers after user approval; updates replace the full configuration.
- `get_credit_balance` — check budget before proposing credit ceilings or testing.
- `get_task_routing` — explain which model handled an existing routed task.

## New router

1. `list_models` across relevant endpoints — do not guess eligible models or capabilities.
2. `get_credit_balance` — understand budget before proposing credit ceilings.
3. Propose: name, immutable `configId` slug, description, routing preference, model-list policy, capacity fallback, optional credit caps. **Wait for user approval** unless they supplied all fields.
4. `create_model_router`, then `update_model_router` for settings if needed.
5. Validate the intended payload with HTTP `dryRun: true` before a billable generation; the SDK does not currently support dry runs.
6. When billable verification is appropriate, make one routed SDK call with the wait helper chained directly from `create()`, then use `get_task_routing` to explain which model ran.

## Existing router

1. Use `list_model_routers` to resolve the application's `configId` slug to a router record, then call `get_model_router` with its UUID.
2. Clarify integration goal (wire into app vs test call).
3. Implement the routed generate call behind the application's server boundary per https://docs.dev.runwayml.com/model-routers.md, chaining the SDK wait helper directly from `create()`.
4. Validate the same payload with HTTP `dryRun: true` before any billable verification.
5. After an approved live test, use `get_task_routing` to confirm which model ran.

## Terminology

- Router record **id** (UUID) ≠ **configId** (immutable slug used in SDK `configId` field).

## Docs

- https://docs.dev.runwayml.com/llms.txt (model routers section)
- https://docs.dev.runwayml.com/model-routers.md
