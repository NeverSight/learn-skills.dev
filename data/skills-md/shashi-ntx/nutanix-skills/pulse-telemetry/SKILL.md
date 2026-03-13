---
name: pulse-telemetry
description: >-
  Implement UI telemetry tracking using @nutanix-ui/pulse-telemetry. Use when
  asked to: add telemetry/analytics/tracking to a web app, implement telemetry
  requirements from a CSV/list, instrument clicks/hovers/page visits, set up
  TelemetryProvider or TelemetryManager, create telemetry config files, or
  verify telemetry payloads. Covers React and non-React codebases.
---

# Pulse Telemetry Implementation

Implement telemetry tracking for web apps using `@nutanix-ui/pulse-telemetry`. This skill uses a gated workflow: scaffold the foundation, verify one event works end-to-end in the browser, then ask the user before implementing the remaining requirements.

## Workflow

```
1. Detect  →  2. Scaffold  →  3. Smoke Test  →  3c. Handoff Doc  →  4. CHECKPOINT ✋  →  5. Implement All  →  6. Verify  →  7. Report
```

### 1. Detect Project State

**First, check for an existing handoff doc** (`TELEMETRY_STATUS.md` in the telemetry utils directory). If one exists, read it — it contains the full context from a prior session: file map, established patterns, and a requirements tracker. Resume from the first row with status `Pending`. Skip steps 2–4 and go to step 5, but continue using this skill's reference files (templates, requirement-type-map, codebase-adapters) whenever you encounter a requirement type or pattern not covered in the handoff doc.

If no handoff doc exists, search the codebase for existing telemetry setup:

```
Look for:
├── TELEMETRY_STATUS.md in utils/telemetry/ or shared/telemetry/
├── TelemetryProvider or TelemetryManager imports
├── utils/telemetry/ or shared/telemetry/ directory
├── constants.ts with FEAT_NAME / PAGE_SECTION / SUB_PAGE_SECTION
├── data/ directory with TelemetryConfigObj aggregation
├── data-telemetry attributes in JSX/HTML
└── @nutanix-ui/pulse-telemetry in package.json
```

**If handoff doc exists:** read it and resume from its first `Pending` requirement (skip to step 5). Still consult skill reference files for unfamiliar requirement types.
**If telemetry exists but no handoff doc:** extend the current setup — add new constants, config files, and provider wiring as needed.
**If telemetry is missing:** scaffold the full foundation (step 2).

See [references/setup-detection.md](references/setup-detection.md) for detection commands, scaffold rules, and handoff doc resume logic.

### 2. Scaffold Missing Foundation

Only create files that don't already exist. Required foundation:

| File                                | Purpose                                                                                |
| ----------------------------------- | -------------------------------------------------------------------------------------- |
| `utils/telemetry/constants.ts`      | `FEAT_NAME`, `PAGE_SECTION`, `SUB_PAGE_SECTION` as const objects                       |
| `utils/telemetry/data/index.ts`     | Aggregates all feature configs into one `TelemetryConfigObj`                           |
| `utils/telemetry/data/<feature>.ts` | Per-feature `TelemetryConfigData` with defaults + eventMap                             |
| `utils/telemetry/index.ts`          | Exports config args; creates `TelemetryManager` if non-React code needs access         |
| Provider wiring                     | `TelemetryProvider` at app/page root, or `TelemetryManager.initialize()` for non-React |

See [references/templates.md](references/templates.md) for copy-paste file templates.

**Adapt, don't copy-paste.** Templates show the full pattern — only use the parts you actually need. Don't add wrapper components, extra files, or abstractions unless the specific case requires them. Match the style and complexity of the existing codebase. See the General Principles section in [references/templates.md](references/templates.md) for details.

**Important:** At this stage, only populate `constants.ts` with values needed for the smoke-test event (step 3). Do NOT add all constants from the full requirement list yet — those will be added in step 5 after the user approves.

### 3. Smoke Test — One Event End-to-End

Before implementing the full requirement list, verify that the base telemetry setup is working correctly by testing one event end-to-end.

#### 3a. Pick One Simple Requirement

Choose the simplest config-driven click event from the requirement list (e.g., a button click with a static `data-test` attribute). Implement only this single event:

1. Add the minimal constants needed for this one event to `constants.ts`
2. Create the config file with just this one `eventMap` entry
3. Wire the aggregation and provider
4. Ensure `data-telemetry` and `data-test` attributes exist on the relevant elements

#### 3b. Verify in the Browser

This step is mandatory. Use the browser automation tool (or ask the user to assist) to confirm the event fires correctly:

1. Enable `debugLog: true` and `verboseClicks: true` in the provider/config options
2. Start the dev server (or confirm it is already running)
3. Navigate to the page containing the tracked element
4. Click the element and check the browser console for the telemetry log output
5. Confirm the logged payload has the correct `featName`, `actionName`, `pageSection`, `subPageSection`, and `actionType`

See [references/payload-verification.md](references/payload-verification.md) for what the console output looks like and common issues.

**If the event fires correctly:** proceed to step 3c (handoff doc).
**If it does not fire:** debug and fix the setup before proceeding. Common issues include missing `data-telemetry` on a parent container, mismatched `data-test` / `eventMap` keys, or the provider not wrapping the component tree.

#### 3c. Create the Handoff Doc

After smoke test passes, create `TELEMETRY_STATUS.md` in the telemetry utils directory (e.g., `utils/telemetry/TELEMETRY_STATUS.md`). This file is a concise context snapshot that lets a fresh agent thread resume implementation without re-discovering the codebase.

The handoff doc must contain:

1. **Quick Start** — dev server URL, next pending requirement, known quirks (e.g., dismiss a modal before testing), active `data-telemetry` container keys
2. **Telemetry File Map** — paths of all created/modified telemetry files and key non-telemetry wiring files (e.g., the component where `TelemetryProvider` was added)
3. **Established Patterns** — project-specific rules discovered during detection (e.g., EBR uses `telemetryName`, codebase adapter type, import alias conventions)
4. **Requirements Tracker** — table with columns: `#`, `Requirement`, `Status`, `Type`, `Files`, `Verified Payload`. Mark the smoke-test row as `Done` with its verified payload. All remaining rows start as `Pending`.
5. **Code Snippet** — one concrete example showing the pattern used for the smoke-test event (config entry + wiring). Keep it short — just enough for a new agent to replicate the pattern without re-reading templates.

See [references/templates.md](references/templates.md) for the `TELEMETRY_STATUS.md` template.

**Rules:**

- Keep the doc under 200 lines. Use tables over prose, snippets over full files.
- Never include sensitive data or user-entered content in payload examples.
- The doc is a working aid, not a deliverable — do not commit it. Add it to `.gitignore` if not already ignored.

### 4. CHECKPOINT — Ask the User Before Continuing ✋

**STOP HERE.** Do not proceed to implement the remaining requirements automatically.

Present the user with:

1. **What was set up** — list the scaffolded files and the provider wiring
2. **The smoke test result** — show the verified payload from step 3b
3. **The handoff doc** — mention the path to `TELEMETRY_STATUS.md` and that it can be used to resume in a new thread
4. **The remaining work** — summarize how many requirements are left and what types they are (config-driven clicks, hover tracking, debounced inputs, etc.)

Then ask the user:

"The base telemetry setup is working — [describe the verified event]. I've created a handoff doc at `[path to TELEMETRY_STATUS.md]` so work can be continued in a new thread if needed. There are [N] remaining requirements to implement. Would you like me to continue implementing all of them, or would you prefer to review the setup first?"

**Wait for the user's response.** Only proceed to step 5 if the user confirms.

### 5. Implement Remaining Requirements

Process each remaining requirement row in order. For each:

1. **Classify** the requirement type (static click, dynamic click, hover, debounced input, tutorial step, non-React event)
2. **Choose approach** — config-driven first; programmatic only when required
3. **Implement** using the matching pattern
4. **Update the handoff doc** — set the row's status to `Done`, fill in files touched and verified payload. This keeps `TELEMETRY_STATUS.md` current so that if the session is interrupted, a new thread can resume from the exact point of interruption.
5. **Record** files touched and expected payload

See [references/requirement-type-map.md](references/requirement-type-map.md) for the classification table and implementation patterns.
See [references/codebase-adapters.md](references/codebase-adapters.md) for adapting patterns to different codebase structures.

#### Decision: Config-Driven vs. Programmatic

| Use config-driven                  | Use programmatic                              |
| ---------------------------------- | --------------------------------------------- |
| Simple clicks on static elements   | Hover / tooltip tracking                      |
| Elements with existing `data-test` | Debounced search/input                        |
| Buttons, links, tabs, checkboxes   | Multi-step tutorials/wizards                  |
|                                    | Events needing dynamic payload data           |
|                                    | Non-React code (render functions, middleware) |

### 6. Verify Payloads

For each implemented requirement, verify the emitted payload matches the expected telemetry data.

**Automated (preferred):** enable `debugLog: true` and `verboseClicks: true`, trigger the interaction, confirm logged payload fields.

**Manual fallback:** structured checklist when runtime is unavailable.

See [references/payload-verification.md](references/payload-verification.md) for the full verification playbook.

### 7. Return Completion Report

After all requirements are implemented:

1. Ensure every row in `TELEMETRY_STATUS.md` is marked `Done` (or `Not feasible` with a reason). The handoff doc's requirements tracker should be fully up to date.
2. Produce a summary table for the user:

```
| # | Requirement | Status | Type | Files | Payload |
|---|-------------|--------|------|-------|---------|
| 1 | ... | Done | config-driven | ... | { ... } |
```

See [references/templates.md](references/templates.md) for the report template.

## Guardrails

These rules are non-negotiable:

1. **Config-driven first** — use `data-telemetry` + `data-test` + `eventMap` for static clicks. Only use programmatic tracking when config-driven cannot handle the interaction type.
2. **Typed constants** — all `featName`, `pageSection`, `subPageSection` values must come from typed `as const` objects in `constants.ts`. Never use raw strings in config or event calls.
3. **`ACTION_TYPE` enum** — always use `ACTION_TYPE.CLICK`, `ACTION_TYPE.HOVER`, `ACTION_TYPE.CHANGE`. Never use raw string `'click'`.
4. **`data-test` / `data-telemetry` consistency** — every `eventMap` key must match an actual `data-test` attribute in the DOM. Every `data-telemetry` value must match a key in the aggregated `TelemetryConfigObj`.
5. **Regex for dynamic IDs** — when `data-test` contains dynamic segments (entity IDs, row indices), add a regex to `defaults.regexList` and use the static prefix as the `eventMap` key.
6. **`getInstanceSafe()` in non-React code** — always use `telemetryManager.getInstanceSafe()` (with optional chaining) outside React components. Never use `getInstance()` which throws if uninitialized.
7. **No sensitive data** — track that an action happened, not user-entered content. `actionName: 'Search'`, not `actionName: searchQuery`.
8. **`mapDataToEventMap` for repetitive actions** — when 3+ buttons share the same `subPageSection`, use the helper to reduce boilerplate.
9. **Shared events for similar features** — export common event maps and spread them into feature-specific configs instead of duplicating.
10. **snake_case naming** — `featName`, `pageSection`, `subPageSection` use `snake_case`. `actionName` is human-readable and descriptive.
11. **Never batch-implement without checkpoint** — always complete steps 1–4 (detect, scaffold, smoke test, checkpoint) before implementing the full requirement list. Do not skip the user confirmation step.
12. **Always create and maintain the handoff doc** — create `TELEMETRY_STATUS.md` after the smoke test (step 3c) and update it after each requirement is implemented (step 5). If resuming from an existing handoff doc, re-validate that referenced files still exist before implementing.
