---
name: rowset
description: Use when an authenticated agent needs to discover Rowset capabilities or manage Rowset projects, datasets, relationships, rows, exports, and public previews.
---

# Rowset

## Purpose

Use Rowset as a stable backend for user-owned structured datasets. Rowset can be
used through MCP, the Rowset CLI, or the REST API. Treat these as peer
interfaces over the same account and data. During setup, prefer native remote
MCP only with private bearer-secret configuration, fall back to the CLI for
trusted terminal or local-file workflows, and use REST for code-only or
HTTP-only runtimes.

This skill is the durable guide for working with Rowset after access has been
configured. Use `rowset-setup` when the agent still needs to inspect its runtime,
select and configure an interface, store credentials, verify authentication, or
complete first-run activation.

Rowset evolves quickly, so do not treat static examples as a complete feature
or command reference. Use live capabilities and interface documentation for
current schemas, commands, endpoints, and workflows.

## Current Capability Discovery

Discovery is task-driven, not a startup checklist. Do not load capabilities or
list datasets merely because a session started. Use the current live resources
only when the task needs them rather than maintaining a static feature catalog:

- MCP: use live tool schemas for exact inputs. Call `get_rowset_capabilities`
  for the compact topic index only when a feature is unfamiliar or setup is
  failing, then request only relevant `topics`.
- CLI: inspect command help for the operation at hand. Use bare
  `rowset capabilities` and repeat `--topic` only when broader workflow guidance
  is needed.
- REST: consult generated API docs for the endpoint at hand. Read
  `/api/capabilities` and request details with `?topics=...` only when broader
  workflow guidance is needed.
- Across interfaces, use cases are opt-in and full mode retrieves the complete
  guide without topic filtering.
- Any interface: use Rowset `llms.txt` to find current docs, guides, skills,
  use cases, and release-oriented resources.
- Use the Rowset docs and blog indexes for current product guidance, examples,
  decision guides, and evolving workflow recommendations.

When the user supplies a dataset key or URL, inspect that dataset directly. MCP
`get_dataset` accepts either value. For CLI or REST, extract the dataset key from
the URL before using `rowset dataset get` or `/api/datasets/{dataset_key}`. If the
relevant dataset is unknown, search with an explicit limit of 3, select one, then
inspect its current schema, instructions, metadata, relationships, and index
semantics. Search before creating duplicates. If no stable business key exists
for a new dataset, use Rowset's current generated-ID path documented by the live
capability guide.

## Working With Rowset

- Reuse the interface already configured for this user. If it is no longer
  supported by the runtime, rerun the `rowset-setup` selection process.
- Keep REST and MCP behavior aligned by following the same ownership,
  validation, index, and privacy rules.
- Treat dataset instructions, metadata, semantic schema, relationships, and
  index settings as durable operating context, not decoration.
- Keep index columns stable, unique, and explicit. Use Rowset's generated-ID
  path when the source has no reliable business key.
- Search existing projects and datasets with an explicit limit of 3 before creating new
  ones; do not enumerate unrelated resources.
- Inspect a dataset's current detail before reading or changing its rows.
- Ask before destructive actions and before changing public sharing state.

## Safety Rules

- Keep authenticated datasets private by default.
- Access only the Rowset resources needed for the user's task.
- Ask before destructive actions such as deleting rows or datasets, archiving
  resources, clearing preview passwords, or replacing meaningful data.
- Ask before enabling or changing any public preview.
- Do not expose API keys, OAuth tokens, raw secrets, or private dataset contents.
- Public previews are read-only sharing surfaces, not authentication and not a
  replacement for private MCP, CLI, or REST access.
- Prefer programmatic Rowset interfaces over browser automation for agent work.
- Do not claim a capability exists unless a current Rowset resource exposes it.

## Companion Skills

- `rowset-setup` configures access, verifies authentication, and completes the
  first-run activation handoff.
- `rowset-features` helps interpret the current capability surface.
- `rowset-use-cases` provides example dataset patterns. Verify every example
  against current Rowset capabilities before implementing it.
