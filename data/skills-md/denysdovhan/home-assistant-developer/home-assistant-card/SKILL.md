---
name: home-assistant-card
description: Use when creating, reviewing, debugging, or maintaining Home Assistant custom Lovelace cards or card editors, including custom elements, Web Components, hass data, setConfig, getCardSize/getGridOptions, getConfigElement/getConfigForm, window.customCards, resource registration, HACS card packages, entity display, service calls, translations, or frontend build validation.
---

# Home Assistant Card Skill

Use this skill for Home Assistant custom card development. Custom cards are Web Components; any framework that defines custom elements can work. Lit and helper libraries are optional unless the repo already uses them.

This is separate from Python integrations, automations, scripts, helpers, and ordinary dashboard YAML. Use those skills unless the work changes a custom card package, registration, editor, or card usage contract.

## Start With Current Docs

Fetch current Markdown from Home Assistant Contributors before changing card APIs. All upstream doc paths in this skill and its references are relative to this base URL:

```text
https://contributors.home-assistant.io/
```

Each page has a Markdown version at `<page URL>index.md`. Use `frontend/llms.txt` to find current frontend pages and `marketplace/llms.txt` for packaging and distribution. Start at `llms.txt` for other areas. Fetch only relevant pages; do not load `llms-full.txt` by default or copy Home Assistant docs into generated skill or repo files. For human-readable links, omit `index.md`.

Use `references/frontend-docs.md` as the docs routing index. Start with `frontend/custom-ui/card/index.md` for card APIs and `frontend/custom-ui/card-editor/index.md` for editors and picker registration.

## Local Workflow

1. Inspect local instructions first: `AGENTS.md`, package scripts, README, HACS metadata, build config, source entrypoints, card/editor files, translations, and release notes.
2. Preserve the existing architecture and framework. Do not convert frameworks, add helper libraries, or add build tooling unless required.
3. Read the relevant reference: `references/card-workflow.md` for repo structure and validation, `references/card-patterns.md` for card API patterns, `references/card-examples.md` for card/editor examples, and `references/frontend-docs.md` for current docs.
4. Keep diffs surgical. Work with dirty worktrees; never revert unrelated edits.
5. Prefer explicit config validation/defaulting in `setConfig` or a local helper. A `buildConfig` helper is a useful pattern, not a requirement.
6. Use Home Assistant frontend data and APIs deliberately: `hass.states`, `hass.localize`, `hass.callService`, custom events, card sizing, editor APIs, and resource registration.
7. Handle unavailable or missing entities without crashing the whole dashboard.
8. For card editors, dispatch `config-changed` with the full updated config and preserve existing editor UX.
9. Run repo-local validation, usually `npm test`, `npm run lint`, `npm run build`, or equivalent scripts. For dependency changes in public repos, keep lockfiles and package-manager config free of private or machine-local registry URLs.

## Scaffolding Guidance

When scaffolding a new card, copy the repo's preferred structure if one exists. Minimum shape is a JavaScript module that defines a custom element and is registered as a dashboard resource with type `module`. Add TypeScript, bundling, visual editors, translations, HACS metadata, screenshots, or release automation only when requested or already expected.

## Review Checklist

Before finishing:

1. Re-fetch the relevant current docs.
2. Confirm the custom element name, dashboard `custom:` type, and resource URL still match.
3. Check `setConfig`, defaults, missing-entity handling, unavailable state, card sizing, editor updates, and card picker metadata.
4. Verify service calls use the intended domain, service, data, and target shape.
5. Check translations, HACS metadata, generated bundle expectations, and public-registry hygiene if dependencies changed.
6. Run local validation scripts and report any commands that could not be run.
