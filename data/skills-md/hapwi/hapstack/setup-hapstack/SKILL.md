---
name: setup-hapstack
description: Configure Hapstack model roles, reasoning budget, delegation, tooling,
  and shipping preferences for the current operator. Use for setup-hapstack or changing
  Hapstack settings.
license: MIT
---

# Setup Hapstack

Configure the package for the operator's actual host and preferences. Setup is not a React audit, shipment, tooling migration, scheduler activation, or permission to change other projects.

1. Read [the runtime contract](../hap-mode/references/runtime.md) and [configuration](references/configuration.md). Detect the host, model discovery, delegation, browser, PR watch, scheduler, shell/Git, and secret capabilities. Report prerequisites relevant to selected workflows; do not require Bun, GitHub, Cursor, or a paid model for every task.
2. Load existing project/global settings without printing secrets. Ask which scope to configure, preserving a prior choice. Global suits personal defaults across projects; project suits shared or project-specific preferences. Report the resolved destination. Never write into the plugin cache or unrelated application configuration.
3. Discover available models. On T3 use `orchestrator_capabilities`, including custom models and provider constraints. Elsewhere use documented discovery. If unavailable, offer current-model operation rather than guess IDs or request credentials in chat.
4. Ask for a reasoning budget: small (medium effort), medium (high), large (xhigh), or unlimited (highest supported). Show exact supported options and any limitation. Preserve selected model roles on reruns. Explain that the host/composer owns the current chat's model and effort.
5. Show every role from the configuration reference, including panel seats. Start unconfigured roles with `inherit-parent`. Offer supported choices and different model families where available. Ask only for unresolved choices; a request for default setup permits the documented defaults. Never describe same-model seats as model diversity.
6. Select delegation (on-request or workflow), tooling (preserve or optional Vite+/Bun preference), versioning (project, bump-on-ship, release-only), and optional changelog-policy offers. Defaults preserve project conventions. These settings do not install tooling, edit repository instructions, authorize messages, or bypass gates.
7. Validate schema, preference values, nonempty panels, and explicit provider/model/options against live availability. Reject malformed settings. Preserve unrelated user content and unknown settings; report deprecated roles instead of silently deleting them. Write the selected Markdown/YAML file at the chosen destination.
8. Read it back and verify the resolved configuration matches the choices. Report location, budget, role choices, relevant gaps, and settings used on the next invocation. Do not spawn agents, run diagnostics, create automations, ship, or make billable requests solely to check setup.
9. If the user wants a missing project verification harness, route to `create-verification-skill`. Otherwise finish. Setup does not require a new harness.

On Codex invoke `$hapstack:setup-hapstack` for the native plugin or `$setup-hapstack` for linked standalone skills. On slash-based hosts use their supported command form, such as `/hapstack:setup-hapstack` for a native Claude plugin. If discovery is unavailable, direct the agent to this file and report that discovery has not been verified. Installation is documented in the package README.
