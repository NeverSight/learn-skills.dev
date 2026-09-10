---
name: sb-explore
description: "Iterate on a new or redesigned component in a sandboxed Explore story outside src/components/ (+ Figma), checked against a graduation gate. Use for 'prototype this', 'try a v2', 'explore from Figma', or net-new UI not ready to ship."
compatibility: "Requires bash; a running Storybook (Node.js) to view the sandboxed Explore story."
allowed-tools: Bash Read Glob Grep Write Edit
license: MIT
metadata:
  author: strongeron
  version: '2.3.0'
  bundle: storybook-workbench
  vendor:
    scripts: []
    wrappers: false
    references: [labs-workflow.md, figma-to-storybook.md]
---

# sb-explore — sandboxed iteration (Build mode: Explore)

The component is new or being redesigned. It lives **outside `src/components/`** so production
code can't depend on it. **Load `references/labs-workflow.md` before scaffolding.**
If the user pasted a Figma URL, ALSO load `references/figma-to-storybook.md`. Do NOT
load `composition-patterns.md` (that's Compare → `sb-wrappers`).

> **Naming:** **`Explore`** is the canonical term used throughout this skill (titles, disk paths, tags).
> `references/labs-workflow.md` predates the rename and says **`Labs`** / `src/stories/labs/` — read it as
> the same track (Explore = Labs). Author with `Explore`; treat `Labs` only as a legacy alias you may meet
> in an existing repo.

## Before scaffolding (ask yourself)

- **Iterating on a shipping component, or net-new?** Determines Path A vs Path B at Ship time.
- **Figma URL pasted?** If yes — set `parameters.design = { type: 'figma', url }` immediately and
  iterate against the frame (see figma-to-storybook.md).
- **API stable enough to graduate?** See the 4 criteria in labs-workflow.md. If not — stay in Explore.

## Scaffold

- **Disk path** — honor the recorded `storiesLocation` (`.storybook/audit/status.md`): when stories are
  **isolated** (the audit/client default), scaffold the experiment under `.storybook/explore/<topic>/` —
  don't scatter into a `src/` you don't own. Only use `src/explore/<topic>/` when the user opted into
  **co-located** for a project they own. Vite excludes either from the production bundle.
- **Title** — `Explore/<topic>/<name>` — last in `storySort.order`, bottom of sidebar.
- **Tags** — `['explore', '!autodocs', '!test']`. Optional: `'motion'`, `'figma-sync'`, `'v2-preview'`.

## Graduation gate (Explore → Component)

Four criteria in labs-workflow.md: stable API · ≥3 callsites planned · designer-reviewed ·
tokens not magic numbers. When all met → trigger **`sb-ship`** (it preserves the experiment,
never `git mv`). Until then, keep iterating here.

## Next

Iterate; when the gate is met, hand off to `sb-ship`. Append progress to `.storybook/audit/status.md`
so an interrupted session resumes cleanly (CONTEXT.md resume protocol).
