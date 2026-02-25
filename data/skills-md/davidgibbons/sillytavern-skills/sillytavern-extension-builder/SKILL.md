---
name: sillytavern-extension-builder
description: Build, scaffold, and ship SillyTavern third-party extensions. Use when creating a new extension, adding extension settings/UI hooks, wiring events or slash commands, integrating modules, or packaging a release from a template.
---

# SillyTavern Extension Builder

## Overview

Create production-ready SillyTavern third-party extensions with the documented extension APIs and packaging rules.

## Workflow

1. Define the extension contract.
- Confirm extension slug, display name, minimum supported SillyTavern version, required modules, and whether the feature is UI-only, slash-command-only, or background worker based.
- If the user does not provide a slug, generate a lowercase kebab-case slug.

2. Scaffold baseline files.
- Prefer `scripts/scaffold_extension.sh` to generate `manifest.json`, `index.js`, `style.css`, and `settings.html`.
- Choose template mode:
  - `default` for UI/event-focused extensions.
  - `slash` for slash-command-first extensions.
- If the user already has files, perform minimal edits instead of full rewrites.

3. Wire extension lifecycle and settings.
- Keep extension settings under `extension_settings[EXTENSION_NAME]`.
- Call `loadExtensionSettings(EXTENSION_NAME)` before reading setting values.
- Use `saveSettingsDebounced()` after setting changes.
- Register startup/event handlers inside `jQuery(async () => { ... })`.

4. Implement user-facing behavior.
- For DOM/UI integration, use documented APIs (context helpers, templates, settings rendering).
- For command behavior, add slash commands and argument parsing with the slash-command APIs when needed.
- For background logic, use a module worker class and gate execution by current chat context.

5. Validate compatibility and packaging.
- Ensure manifest keys are correct and file names match actual files.
- Ensure import paths are valid from the extension directory.
- Keep third-party dependency usage explicit and minimal.
- Package as a repo or zip with only required runtime files.

6. Return deliverables.
- Provide final file set and a concise integration note.
- Include install path expectations and any required module prerequisites.

## Output Rules

- Prefer minimal-diff changes when editing an existing extension.
- Keep settings schema stable; migrate old keys instead of silently breaking them.
- Use deterministic IDs/command names (derive from extension slug).
- If introducing a slash command, include help text and argument validation.
- If introducing a module worker, include clear stop conditions for idle/no-chat states.

## Resources

- `references/writing-extensions-reference.md`
  - Condensed upstream authoring guidance, required file anatomy, APIs, and release rules.
- `references/st-extension-example-walkthrough.md`
  - Practical breakdown of the `city-unit/st-extension-example` template and reuse patterns.
- `references/extension-quality-guidelines.md`
  - Research-backed recommendations for quality, maintainability, security, and release readiness.
- `references/template-selection-guide.md`
  - Decision guide for choosing `default` vs `slash` scaffold mode and migrating between them.
- `assets/templates/extension/manifest.json`
  - Starter manifest with placeholders.
- `assets/templates/extension/index.js`
  - Starter extension entrypoint with settings and event wiring.
- `assets/templates/extension/style.css`
  - Starter CSS file referenced by manifest.
- `assets/templates/extension/settings.html`
  - Starter settings template for `renderExtensionTemplateAsync`.
- `assets/templates/extension-slash/manifest.json`
  - Slash-command-first starter manifest.
- `assets/templates/extension-slash/index.js`
  - Slash-command-first starter entrypoint with parser registration and validation.
- `assets/templates/extension-slash/style.css`
  - Minimal stylesheet for command help/settings rows.
- `assets/templates/extension-slash/settings.html`
  - Starter settings block for enabling/disabling command behavior.
- `scripts/scaffold_extension.sh`
  - Generator script for new extension skeletons.

## Notes

- The docs and extension APIs evolve. If behavior is uncertain, prefer upstream docs over assumptions and keep code conservative.
- Keep code style aligned with existing SillyTavern extension conventions (imports, settings handling, and event registration).
