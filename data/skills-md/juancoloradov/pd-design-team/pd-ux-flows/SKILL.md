---
name: pd-ux-flows
description: >-
  Use when an experience spans multiple steps or screens and needs structure: mapping user flows, task
  flows, journey maps, and state and decision logic. Sits between research (or pd-ux-architecture) and
  screen design. For content structure, taxonomy, sitemaps, or navigation models, use pd-ux-architecture
  instead. Part of the pd-* design team.
metadata:
  team: product-design
  role: ux-flows
  version: "2.0.0"
---

# pd-ux-flows — paths before screens

## Overview

Define the paths of an experience before any screen is designed: which steps a user takes, in what order,
with which decisions, and in which states. A flow earns its keep by exposing dead ends, redundant steps,
and missing states while they are still cheap to fix.

## Before you start

1. Load `pd-foundations`: `principles.md`, `accessibility.md`, `handoff-protocol.md`.
2. Read `docs/design/PROJECT.md`. If it is missing, proceed with defaults and record them as assumptions,
   or ask `pd-design-lead` to set it up.
3. Read the upstream research artifact (`*-research-*.md`), which the user may waive in favor of stated
   assumptions, and the architecture artifact (optional) if content or navigation structure has been
   defined. Pull the requirement from the tracker named in `PROJECT.md` (see `integrations.md`).

## When to use

- The experience has multiple steps, branches, or screens.
- Every path, decision, and state should be visible before pixels are designed.

**Not for:** a single isolated screen, component, or copy change; defining content structure, taxonomy,
sitemaps, or navigation (`pd-ux-architecture`; this skill traces paths through that structure).

## Artifacts

| Artifact | What it answers |
|---|---|
| **User flow** | Steps and decisions to complete a task, including error and alternate paths |
| **Task flow** | One linear path for one specific task |
| **Journey map** | The end-to-end experience by phase: actions, touchpoints (channel/system per action), thoughts, emotions (as a curve), pain points, and opportunities (the response to each pain point) |

## Process

1. **Pull the goals** from research: the jobs and tasks users need to complete, and their context.
2. **List entry points and triggers**: how users arrive.
3. **Map the happy path**, step by step, one decision per branch.
4. **Add the unhappy paths**: errors, empty states, edge cases, interruptions, back/cancel, permissions.
   A flow without its error and alternate paths is incomplete.
5. **Name states per step** (loading, success, error, empty, partial) as decision outcomes. The visual and
   behavioral spec of each state belongs to `pd-ux-design`.
6. **Model permission and role gates as their own decision type.** In any product with roles or plan
   tiers, each task needs explicit branches for what this role or state can see or do; a failed permission
   check is not a user error.
7. **Include system-triggered interruptions**: session expiry, connection loss, a role change mid-task.
8. **Check**: no dead ends, no orphan screens, every decision has all its branches, a keyboard path exists.

## Notation

Write flows as text or a diagram in whatever the project uses (a diagramming tool, Mermaid, plain text).
Use one consistent vocabulary:

- **Step** (screen or action), **Decision** (every outcome drawn), **State**, **Entry/Exit**,
  **System action** (vs. user action), **Loop/Retry** (an explicit back-edge), **Parallel** (two branches
  active at once, such as a background sync while the user edits; show how they rejoin or flag the
  conflict as an open risk).

```
[Entry: email invite] → (Open app) → <Signed in?>
   ├─ no  → [Sign in] → <Valid?> ─ no → [Error: re-enter] ↺
   │                              └ yes ↓
   └─ yes ───────────────────────────→ [Onboarding step 1] → … → [Done]
```

## Output

`<artifacts_dir>/<date>-flows-<topic>.md` with the artifact header from `handoff-protocol.md`
(`discipline: flows`), then: entry points, the flows with all branches and states, open questions and
risks. `upstream:` the artifacts actually consumed — research and architecture, if they
existed and were used (list none when research was replaced by stated assumptions). `downstream:` `design`, `content`,
`responsive`, `prototype`.

## Domain packs

If `PROJECT.md` lists domain packs, read each pack's section for flows and apply it on top of this skill.

## Common mistakes

- Mapping only the happy path.
- Leaving out loading, empty, and error states, which then get "designed later", meaning never.
- Dead ends, orphan screens, and no way back.
- A Decision node with one documented outcome; the else branch is assumed instead of drawn.
- Modeling only user-triggered errors and no system-triggered interruptions.
- Treating a permission denial as a generic error branch.
- In incomplete-data situations (missing prerequisite records, partial saves), assuming the data is
  present instead of drawing the path where it is not.
