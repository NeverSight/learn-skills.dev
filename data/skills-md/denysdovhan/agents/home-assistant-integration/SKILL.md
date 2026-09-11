---
name: home-assistant-integration
description: Use this skill when creating, scaffolding, reviewing, or maintaining Python Home Assistant custom integrations, including work on custom_components, manifests, config flows, options flows, config entries, platforms/entities, DataUpdateCoordinator, integration automation triggers, diagnostics, repairs, discovery/networking, authentication, HACS-ready repositories, or Home Assistant integration quality scale compliance.
---

# Home Assistant Integration Skill

Use this skill for Home Assistant custom integration development. This is separate from Home Assistant automation, helper, script, and Lovelace work.

## Start With Current Docs

Fetch the latest markdown from the Home Assistant developers docs repository before coding. All doc paths in this skill and its references are relative to this base URL — prepend it when fetching:

```text
https://raw.githubusercontent.com/home-assistant/developers.home-assistant/master/docs/
```

Use rendered pages on `developers.home-assistant.io` only as secondary reading. Do not copy Home Assistant docs into generated skill or repo files. Fetch only the files relevant to the task.

The reference files in this skill are the routing indexes to the doc paths; do not rely on remembered Home Assistant APIs. Always consult the relevant reference, then fetch the current markdown files it points to, before editing matching files:

| Reference | Use when |
|---|---|
| [`references/architecture.md`](references/architecture.md) | Editing generic integration architecture, lifecycle, setup, manifest, config entries, data fetching, events, diagnostics, auth, networking, docs, tests, or translations |
| [`references/core-integration-files.md`](references/core-integration-files.md) | Editing core integration files such as `__init__.py`, `manifest.json`, `config_flow.py`, `coordinator.py`, `diagnostics.py`, `repairs.py`, services, translations, tests, or docs |
| [`references/entities-and-domains.md`](references/entities-and-domains.md) | Editing platform/entity files such as `sensor.py`, `binary_sensor.py`, `calendar.py`, `weather.py`, or deciding which platform domain fits a feature |
| [`references/automation-triggers.md`](references/automation-triggers.md) | Adding or maintaining new integration-provided automation triggers in `trigger.py` and `triggers.yaml` |
| [`references/quality-rules.md`](references/quality-rules.md) | Checking Bronze/Silver/Gold/Platinum quality scale rules or reviewing an integration against Home Assistant quality requirements |

## Local Workflow

1. Inspect local instructions first: `AGENTS.md`, scripts, `pyproject.toml`, workflows, README files, and existing `custom_components/<domain>` files.
2. Preserve repo conventions. Prefer existing user Home Assistant repo patterns: `uv` tooling, `scripts/lint`, `scripts/test`, typed runtime data, `DataUpdateCoordinator`, config flows, diagnostics, translations, and minimal diffs.
3. Keep API/client code Home Assistant agnostic where the repo already separates it from integration code.
4. Use config entries and UI setup by default for real integrations. Use YAML only when the user explicitly asks or the existing repo still requires it.
5. Keep entities cheap: no I/O in entity properties; update cached values through setup, coordinator refreshes, or event callbacks.
6. Use `ConfigEntry.runtime_data` for runtime objects when adding or reshaping integration state.
7. Handle setup failures with the Home Assistant exceptions that match the failure: retryable setup failures, auth failures, and permanent invalid configuration should not be conflated.
8. Add tests for changed behavior. Run the repo scripts requested by local instructions, usually `scripts/lint` after Python changes and `scripts/test` before finishing.
9. When behavior is unclear, add narrow debug logging or ask for logs instead of guessing.

## Scaffolding Guidance

When scaffolding a new integration from an existing user repo, copy structure and tooling style, then remove business logic that does not belong to the new integration. Keep only the integration basics needed for setup, manifest validity, importability, testability, and future feature work.

Minimum shape for a custom integration is usually:

```text
custom_components/<domain>/
  __init__.py
  manifest.json
```

Add files such as `config_flow.py`, platform modules, `coordinator.py`, `entity.py`, `diagnostics.py`, `repairs.py`, translations, tests, and brand assets only when required by the requested scope or the selected quality target. Use `references/core-integration-files.md` before adding or editing these files.

## Quality Scale

Default to Bronze. Higher levels are cumulative and should only be added when the user asks or explicitly accepts the extra scope. Bronze means all Bronze rules apply; Silver includes Bronze; Gold includes Silver and Bronze; Platinum includes all lower levels.

Before finishing ordinary integration work, read `references/quality-rules.md`, confirm the current rule list from `core/integration-quality-scale/_includes/tiers.json`, fetch the latest markdown for each relevant rule, and verify every Bronze rule against the current code. If the user asks for Silver, Gold, or Platinum, make the additional rule set part of the implementation scope before coding.

## Review Checklist

Before finishing:

1. Re-fetch relevant docs and quality rule files.
2. Verify the requested quality level, defaulting to Bronze.
3. Run component and platform review checklists relevant to changed files.
4. Confirm config entry setup, unload, runtime data, entity IDs, translations, diagnostics, and tests match the selected scope.
5. Run local validation scripts from the repo instructions.
