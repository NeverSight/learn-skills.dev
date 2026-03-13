---
name: umbraco-mcp-dev-ops-headless
description: Guide to perform headless Umbraco dev/ops tasks via MCP tools safely.
---

# Umbraco MCP Dev Ops Headless

## Purpose

Guide to perform Umbraco developer and operational tasks for headless deployments efficiently and safely using the MCP tool collections.

## Scope

- Included: document/data type management, models builder, search/indexing, webhooks, health/logs, server diagnostics.
- Optional: templates and partials for preview-only flows.
- Excluded by default: editorial content authoring and bulk publishing workflows.

## When to Use

- Maintaining headless content models and delivery readiness.
- Managing indexing and search for API consumers.
- Operating webhooks for downstream sync and integrations.

## When Not to Use

- Content authoring or localization tasks.
- Media uploads and editorial workflows.

## Tool Collection Strategy

- Always request the smallest set of tool collections needed for the task.
- See `references/tool-collections.md` for task-to-collection mapping.

## Execution Policy

- Read before write: fetch configuration or scaffolds first.
- Validate before mutate: use validation endpoints when available.
- Prefer search and by-id-array endpoints to reduce calls.
- Paginate large lists and batch changes with clear progress.

## Safety Rules

- Require confirmation for destructive actions (delete, remove folders).
- Require confirmation for breaking API changes (renames, removals, type changes).
- If permissions are unclear, fetch current user permissions and report limits.

## Response Format

- Summarize actions taken and list affected assets.
- For read-only tasks, return concise findings with counts and key examples.
- Include next steps only when useful (e.g., rebuild models, notify clients).

## Examples

- Create a new headless Document Type and run Models Builder.
- Update a Data Type configuration used by API clients.
- Rebuild an external index and report status.
- Create a webhook for Content.Published events to sync downstream.
- Run health checks when API delivery latency spikes.
