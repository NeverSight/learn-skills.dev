---
name: apple-dash-docsets
description: Manage Dash docsets and cheatsheets on macOS. Use when tasks involve Dash search and discovery, installing missing docsets, or generating guidance when a docset is unavailable.
---

# Apple Dash Docsets

## Purpose

Manage Dash docsets and cheatsheets on macOS with one top-level entry point. `scripts/run_workflow.py` is the authoritative runtime path for stage selection, fallback order, source priority, approval gating, and structured generation guidance; it does not replace the agent's own Dash access methods.

## When To Use

- Use this skill for Dash search and discovery requests.
- Use this skill for Dash installation requests after search has identified a missing docset.
- Use this skill for Dash generation guidance when installation cannot complete.
- Use this skill when the user needs the exact fallback path between agent-side Dash MCP usage, local HTTP, and URL or Service integration.
- Recommend `apple-xcode-workflow` when the user needs Apple or Swift execution, diagnostics, build or test work, or Apple docs reasoning outside Dash management.
- Recommend `apple-swift-package-bootstrap` when the user is starting a brand new Swift package rather than managing Dash content.

## Single-Path Workflow

1. Classify the request into one stage:
   - `search`
   - `install`
   - `generate`
2. If no stage is explicit, start at `search`.
3. Run `scripts/run_workflow.py` with the selected stage:
   - `search`: applies configured fallback order and returns a structured access-path decision
   - `install`: applies configured source priority and approval gating
   - `generate`: returns structured automation-first guidance
4. If the selected stage cannot complete, hand off forward through `references/stage-handoff-contract.md`:
   - `search -> install`
   - `install -> generate`
5. Return one status, one `path_type`, and one output contract for the stage that ran.

## Inputs

- `stage`: `search`, `install`, or `generate`
- `query`: required for `search`
- `docset_identifiers`: optional for `search`; use installed identifiers only
- `docset_request`: required for `install` and `generate`
- `approval`: required before side-effectful install actions
- Defaults:
  - runtime entrypoint: `python3 scripts/run_workflow.py`
  - `search` access order is `mcp -> http -> url-service`
  - install source priority is `built-in,user-contributed,cheatsheet`
  - default search result limit is `20`
  - default search snippets setting is `true`

## Outputs

- `status`
  - `success`: the selected stage completed on its primary or fallback path
  - `blocked`: prerequisites, approval, or usable access paths are missing
  - `handoff`: the current stage is handing off to the next Dash stage
- `path_type`
  - `primary`: the selected stage completed normally
  - `fallback`: the selected stage completed through its documented fallback path
- `output`
  - `stage`
  - `access_path` or `source_path`
  - `matches`
  - install result or generation guidance when applicable
  - one next step when follow-up is required

## Guards and Stop Conditions

- Do not run install actions without explicit user approval.
- Do not invent docset identifiers or catalog matches.
- Stop with `blocked` when agent-side Dash MCP usage, HTTP, and URL or Service paths are all unusable for `search`.
- Stop with `blocked` when `install` or `generate` lacks a concrete docset request.
- Keep `search`, `install`, and `generate` in forward stage order; do not blend them into competing primary workflows.

## Fallbacks and Handoffs

- `search` falls back in this order: agent-side Dash MCP usage, local HTTP API, then URL or Service guidance.
- `install` hands off to `generate` when no installable catalog match exists.
- `generate` falls back from stable automation to deterministic manual guidance.
- Use `references/stage-handoff-contract.md` when `search` transitions to `install` or `install` transitions to `generate`.
- Recommend `apple-xcode-workflow` directly when the user’s task shifts from docs management to Apple or Swift execution work.
- Recommend `apple-swift-package-bootstrap` directly when the user needs new Swift package scaffolding.
- `scripts/run_workflow.py` is the only local runtime entrypoint for stage behavior; helper scripts remain implementation details behind it.

## Customization

- Use `references/customization-flow.md`.
- `scripts/customization_config.py` stores and reports customization state.
- `scripts/run_workflow.py` loads and enforces the runtime-safe knobs documented in `references/customization-flow.md`.

## References

### Workflow References

- `references/dash_mcp_tools.md`
- `references/dash_http_api.md`
- `references/dash_url_and_service.md`

### Contract References

- `references/stage-handoff-contract.md`
- `references/automation-prompts.md`
- `references/customization-flow.md`

### Support References

- Recommend `references/snippets/apple-swift-core.md` when the user needs a reusable Apple and Swift baseline snippet in their own repo alongside Dash-based docs workflows.
- `references/catalog_built_in_docsets.json`
- `references/catalog_user_contrib_docsets.json`
- `references/catalog_cheatsheets.json`
- `references/snippets/apple-swift-core.md`

### Script Inventory

- `scripts/run_workflow.py`
- `scripts/dash_api_probe.py`
- `scripts/dash_catalog_match.py`
- `scripts/dash_catalog_refresh.py`
- `scripts/dash_url_search.py`
- `scripts/dash_url_install.py`
