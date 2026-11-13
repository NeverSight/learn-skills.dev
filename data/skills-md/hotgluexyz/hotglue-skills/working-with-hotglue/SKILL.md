---
name: working-with-hotglue
description: Works on Hotglue integration workflows using the Hotglue CLI, public documentation MCP, Singer connectors, and ETL templates. Use for tasks involving Hotglue configuration, custom connectors, ETL scripts, or integration troubleshooting.
mcpServers:
  hotglue-docs:
    url: https://docs.hotglue.com/mcp
    transport: http
    includeTools:
      - search_hotglue_docs
      - query_docs_filesystem_hotglue_docs
---

# Working with Hotglue

Use the Hotglue Docs MCP as the source of truth for Hotglue product behavior and current examples. Search before relying on remembered API or CLI syntax.

## CLI

Confirm available commands with:

```bash
hotglue --help
```

For an unfamiliar API object or endpoint, use `hotglue <area> --help` and the Hotglue Docs MCP before creating or mutating it. Inspect the relevant existing entity and a real job artifact rather than inferring its contract from a similar connector.

Authenticate only when a task requires it. Prefer environment variables or local secret files for API keys — never put keys, tokens, or customer data in repository files, prompts, logs, or commits.

## Connector and ETL work

- Before a new connector, search `hotgluexyz` for `tap-<service>` or `target-<service>` and extend an existing connector when it matches the requested integration.
- Use `creating-taps`, `creating-targets` or `creating-hotglue-etl-scripts` for the relevant workflow.
- Use `managing-available-connectors` for environment definitions, linked entities, discovery, and field maps.
- Use `understanding-hotglue-jobs` for incremental sync, job settings, and snapshot traps.
- Use `running-hotglue-remote-jobs` to create and poll remote jobs over the client API.
- Treat `.secrets/` as the local location for config, catalogs, Singer streams, and job artifacts. This repository’s `.gitignore` must include `.secrets/`.
- Verify outputs semantically: inspect catalogs, Singer JSONL, and target state, rather than only checking process exit codes.

## v2 guardrails

- Record the topology before acting: write jobs are Source → ETL → Connector; read jobs are Connector → ETL → Target.
- Inspect existing available and linked entities before creating, deleting, or forking one. Fork the requested existing entity rather than creating a duplicate.
- Discover establishes the catalog of available streams; field selection is a separate linked-entity `field_map` update. Verify both independently.
- Retrigger a previous job for ETL-only changes, preserving the source sync output. Run a new job only when testing changed source data or configuration.
- Run one discover or job at a time, inspect its status and logs, then diagnose before retrying. Add structured ETL logs when the deployed result disagrees with a local replay.
- Require `externalId` in every ETL export and check the resulting target state mapping before declaring a direction complete.
- Use `--json` only with output filtering that excludes secrets; never echo full linked configuration or effective overrides.
