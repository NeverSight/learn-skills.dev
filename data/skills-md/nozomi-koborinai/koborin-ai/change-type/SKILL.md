---
name: change-type
description: Classify a change set as behavior vs structure, then recommend the correct PR label (change:behavior or change:structure) and the appropriate local/CI checks. Use when the user asks whether a change is a behavior change or a structure change, what label to apply, or how CI/testing should differ based on change type.
---

# change-type

Classify the current work as either a **Behavior Change** or a **Structure Change**, then recommend:

- PR label (`change:behavior` or `change:structure`)
- local verification commands
- what CI is expected to run

## Trigger Examples

- "Is this a Behavior Change or a Structure Change?"
- "Which label should I apply: change:behavior or change:structure?"
- "Can we skip build/audit for this refactor?"
- "How should CI differ for behavior vs structure changes?"

## Execution Flow

### 1. Inspect the change set

- Identify changed files/paths
- Identify intent (behavior vs refactor)
- If any uncertainty remains, default to **Behavior Change**

### 2. Classify

**Behavior Change** if the change is externally observable (site output, infra behavior, CI behavior).

**Structure Change** if the change is intended to preserve external behavior while improving maintainability.

### 3. Apply repo-specific heuristics

Treat as **Behavior Change** if the diff touches any of:

- `app/src/content/docs/**` (published content)
- `app/src/**` (components/layouts/pages)
- `app/public/**` or `app/src/assets/**` (published assets)
- `app/astro.config.mjs`, `app/nginx/**`, `app/Dockerfile`
- `infra/src/**` (Pulumi stacks)
- `.github/workflows/**` (CI behavior)

Treat as **Structure Change** candidates if the diff touches only:

- `README.md`, `AGENTS.md`, `CLAUDE.md`
- `.github/release.yml`
- other non-deployed repository documentation files

### 4. Recommend label + checks

Return:

1. **Change type**: `behavior` or `structure`
2. **PR label**: `change:behavior` or `change:structure`
3. **Local checks**
4. **CI expectations**

## Recommended checks

### App

- Behavior:
  - `cd app && npm run lint && npm run build`
- Structure:
  - `cd app && npm run lint`

### Infra

- Always (local static checks):
  - `cd infra && npm run build && npm run lint && npm run typecheck`
- Never run `pulumi preview`/`pulumi up` locally (CI only).


