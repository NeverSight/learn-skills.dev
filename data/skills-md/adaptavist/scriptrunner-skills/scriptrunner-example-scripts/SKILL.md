---
name: scriptrunner-example-scripts
description: Working ScriptRunner example scripts grouped by feature, including listeners, scheduled jobs, behaviours, workflow functions and scripted fields. Use as a starting point instead of writing a script from scratch.
metadata:
    author: sms-core
    version: '1.0'
    generated-script-count: '365'
    generated-cloud-script-count: '134'
    generated-data-center-script-count: '231'
---

# ScriptRunner Example Scripts Skill

Use this skill for bundled local example scripts. Prefer it over remote example lookup tools.

## Activation signals

- User asks for a starter script or working example.
- User wants feature-specific ScriptRunner code patterns.
- User needs a concrete snippet to adapt for Cloud or Data Center.

## Workflow

1. Confirm the target platform.
2. Open the relevant platform index:
    - `references/INDEX-CLOUD.md`
    - `references/INDEX-DATA-CENTER.md`
3. Use `references/FEATURE-INDEX.md` to narrow by feature.
4. Use focused local reads against 1-3 matching files in `references/scripts/...`.
5. Use a subagent only for bounded discovery across a large search space. Ask it for concise findings, local file paths, original source URLs, feature labels, and line ranges, not full script contents.
6. Return adapted code and cite both the local file path and original source URL.

## Resource map

- `references/INDEX-CLOUD.md` - Cloud script inventory.
- `references/INDEX-DATA-CENTER.md` - Data Center script inventory.
- `references/FEATURE-INDEX.md` - cross-platform feature map.
- `references/scripts/...` - script pages grouped by platform and feature.
- `assets/scripts.json` - machine-readable manifest.

## Notes

- Prefer feature-first lookup to minimize context load.
- Do not ask subagents to return full scripts or large excerpts; the parent agent should perform any final focused reads directly.
- Preserve the platform and API style shown by the chosen example.
- Explain any placeholders or assumptions you change while adapting a script.
