---
name: sb-wrappers
description: "Scaffold a Storybook-only wrapper — ABCanvas, StateGrid, AppFlowGraph, ProjectInventory, and more. Use for 'compare two designs', 'every state on one canvas', 'the full flow', 'track this decision', or 'scaffold wrappers'."
compatibility: "Requires bash (scaffolds Storybook-only .tsx wrappers into the project's .storybook/)."
allowed-tools: Bash Read Glob Grep Write
license: MIT
metadata:
  author: strongeron
  version: '2.3.0'
  bundle: storybook-workbench
  vendor:
    scripts: [scaffold-wrapper.sh]
    wrappers: true
    references: [wrapper-library.md, composition-patterns.md]
---

# sb-wrappers — composition primitives, not hand-rolled grids

Don't hand-roll grid markup. Scaffold a typed wrapper.

**Load only what the task needs** (these are two large refs — don't pull both for one wrapper):
- **`references/wrapper-library.md`** — the per-wrapper API. Load it **before authoring any
  wrapper story**, to get the props/args of the one you picked.
- **`references/composition-patterns.md`** — the five composition patterns (A/B, role,
  status grid, page, motion). Load it **only for a Compare / multi-pattern / layered build**.
  **Do NOT load it** for a single StateGrid / ProjectInventory / DesignSystemHealth scaffold — the
  library ref alone covers that.

## Pick the wrapper from intent

| User says | Wrapper | Tier |
|---|---|---|
| "compare two designs" / "side-by-side" | `ABCanvas` | 1 |
| "every state on one canvas" | `StateGrid` | 1 |
| "every role" / "permission UI" | `StateGrid` with `role` as the varied prop (only if the app is role-gated) | 1 |
| "track this decision" | `TrackedDecision` + `DecisionsDashboard` | 2 |
| "the full flow" / "ordered sequence" | `StoryStrip` / `StorySet` | 2 |
| "shader / WebGL / 3D / keyframe motion" | `ShaderCanvas` / `R3FCanvas` / `MotionStage` | 3 |
| "token source of truth" / "DS health" / "inventory" | `TokensCanvas` / `DesignSystemHealth` / `ProjectInventory` | 4 |
| "icon coverage" / "which icons / what sizes / **where is an icon used**" | `IconMatrix` | 4 |
| "whole-app route map" / "journey map" | `AppFlowGraph` / `JourneyGraph` | flow |

## When in the flow (which wrapper, which step)

Wrappers split by **what feeds them**. The *data* wrappers render a prior step's JSON — scaffold and
use them AFTER that step has run, or they render empty. The *component/story* wrappers you reach for
while writing a story. Suggest the matching wrapper as the next step once its input exists.

| Reach for it… | Wrapper(s) | Needs (run first) |
|---|---|---|
| after **sb-inventory** | `ProjectInventory`, `TokenMatrix` (Colors foundation — value · mapping · adoption; leave the `health` prop off) | `.storybook/project-inventory.json` |
| after **sb-inventory** (usage graph) | `ComponentUsage`, `UsageExplorer` | `.storybook/component-pages.json` (`build-component-pages.py` / `refresh-usage.sh`) |
| after **sb-health** | `DesignSystemHealth` | `.storybook/design-system-health.json` (`TokensCanvas` auto-discovers — no step) |
| after **sb-flows** | `AppFlowGraph`, `JourneyGraph` | `.storybook/flows.json` |
| building **Foundations/Icons** | `IconMatrix` | nothing — scans `/src` live; pass `library` + `resolve` |
| writing a **component story** (sb-stories) | `StateGrid` (all states), `StateMatrix` (variants × states) | the component |
| composing **existing stories** | `StorySet` (by tag/id), `StoryStrip` (ordered) | stories already written |
| **iteration** (Compare / decide) | `ABCanvas`, `TrackedDecision` + `DecisionsDashboard` | — |

Don't scaffold a data wrapper before its step has produced the JSON — `scaffold-wrapper.sh` prints the
generating script for each as a reminder.

**States scattered across many stories → consolidate into ONE matrix.** When a component's states are
spread over separate stories (a story per state — hard to scan, easy to drift), collapse them into a single
`StateGrid` (all states) or `StateMatrix` (variants × states) so every state is reviewable on one canvas.
This is the canonical fix for "the Detection header/list states are scattered — make a concise states view".

**Real-usage overlay.** `StateGrid` / `StateMatrix` take an optional `usage` prop —
`usage={usageJson.components.<Name>}` (from `.storybook/component-usage.json`) badges each variant/state
with its real call-site count and strikes through declared-but-unused ones (`×0 unused`). Add it as a
**flat story in the component's existing CSF, never a new file** (a new file makes a new sidebar folder).
For colours/type use `TokenUsageGrid` (reads `project-inventory.json` `tokens.map`); for the per-component
table, `UsageSection` embeds into each Docs page via `preview.ts` `docs.page` — see `sb-inventory`.

## Scaffold

```bash
CORE=${CLAUDE_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}   # scaffold-wrapper is shared core
# scaffold-wrapper.sh is a LOCAL bash script that ships INSIDE this skill — it only copies the bundled
# .tsx wrappers into the project's .storybook/. No network, no install, no external code. See SECURITY.md.
"$CORE/scripts/scaffold-wrapper.sh" --tier 1            # CORE
# --tier 2 | 3 | 4 (adds DESIGN-SYSTEM) | --flow (AppFlowGraph+JourneyGraph) | --all
"$CORE/scripts/scaffold-wrapper.sh" ABCanvas StateGrid  # or specific names
```

`icons.tsx` is **always copied** alongside (the shared icon language) and a barrel `index.ts` is
emitted. Wrappers nest: `TrackedDecision → ABCanvas → ShaderCanvas → Hero`.

## View design

All wrappers follow `CONTEXT.md` §wrapper-view-design — no emoji, the shared `Icon` set, and
an injectable `icons` prop on the map wrappers. When you add/edit a wrapper, keep that contract.

## Next

Compose your Compare/Flow story, then `sb-stories` gate (`validate-stories.sh`).
