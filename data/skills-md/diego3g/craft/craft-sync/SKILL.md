---
name: craft-sync
description: Use when a design task is about to start in a project whose design system already lives in code (a UI package, design tokens, a component library) but isn't in the design tool, when asked to import or bring the design system, tokens or components into the design tool, or to apply, push or sync changes from the design tool's guide back to the code.
---

# Design system sync

## Overview

When a design system already lives in code, the design tool should **mirror it, not reinvent it**.
- **Import** brings the code's tokens and the components the person picks into the tool, under the same names.
- **Export** takes changes made in the tool's guide back to the code as a reviewed diff.

A small file at the project root, **`design-sync.json`**, remembers what was last synced. Code stays the source of truth until the person says otherwise: changes are *drawn* first in the tool and *land* in code through an approved export.

## When to use

- A design task is about to start in a project with a design system in code and no guide in the tool. `craft-setup` and `craft` hand off to this.
- "Import / bring our design system (tokens, components) into Paper / Figma / the design tool."
- "Apply / push / sync the guide's changes to the code."

## When NOT to use

- No design system in code: `craft-system` (create mode).
- A review, options or a small edit in such a project: those skills work from the code as it is.
- A single token value the person dictated ("make the accent #3d7f69 in code"): edit it directly, update `design-sync.json` for that name, say what it affects.

## Before you start

0. Read `DESIGN.md` (Brand says where the system lives) and `design-sync.json` if they exist.
1. Pick your tool's adapter in `references/adapters/` (`paper.md`, `figma.md`, `html.md`). If no adapter matches your tool, do the same verbs in your tool and say which you mapped by hand. With no design tool at all, build in HTML (`html.md`). If an image is all you have, say that values read from it are estimates.

## `design-sync.json`

```json
{
  "source": "packages/ui/tokens.css",
  "tool": "paper: file 'Fieldnote', page 'Guide'",
  "naming": "CSS custom property names as written in the source",
  "synced": "2026-11-15",
  "tokens": { "--color-accent": "#2e6b57", "--radius-md": "10px" },
  "components": { "Button": "drawn", "Badge": "drawn", "Input": "in code only" }
}
```

- `tokens` holds the values **both sides agreed on** at the last sync, and only those.
- A component import changes only its own `components` entry.

## Import (code → design tool)

1. **Detect** with [the signals](references/detect.md). Find the **source of truth for values** (the token source, not a generated output) and the **naming rule** the tool will use. **Two UI packages** → list both and ask which is the source.
2. **Inventory, then stop.** Use [the inventory format](references/inventory.md):
   - tokens by role, with counts and paths;
   - components (grouped with counts when there are more than about 15);
   - guideline docs;
   - gaps;
   - **conflicts**: any name that already exists in the tool with a different value, and any token type the tool can't hold.

   **Ask which components to draw now**, suggesting 3–6 for the next screens, and how to settle each conflict. Never draw everything by default.
3. **Build in the tool** after the answers:
   - register the tokens under the naming rule; never overwrite a tool value the person didn't settle;
   - make a foundations guide page, with guideline docs as the legend;
   - make a **component index**: name, code path, status (`drawn` / `in code only`), with variants filled in once drawn;
   - draw the picked components with their states matrix, using values from code. A state the code doesn't define is drawn and labelled **"proposed"**.
4. **Self-check.** Render the guide. If the code can render the component (Storybook, a demo page), compare at the same size. Otherwise say the values were read from code, unrendered.
5. **Record:**
   - write `design-sync.json` (all token values now equal on both sides, plus component statuses);
   - in `DESIGN.md`, Brand gets "Design system source: `<path>`; the <tool> guide mirrors it", and the Decisions log gets a dated import line;
   - if there's no `DESIGN.md`, create one whose first line is `<!-- sync record only: run craft-setup for the brief -->` with just Brand and the Decisions log. `craft` treats a `DESIGN.md` without a Product section as missing.

### Import of one component (from `craft`)

The person already agreed to mirror the system, so there's no inventory stop:
- draw that component;
- set its `components` entry to `drawn`;
- leave `tokens` alone.

If the tool has no guide yet, or the person never agreed to an import (or declined it), ask once: "Input exists only in code. Import it into the guide first?"

## Export (design tool → code)

1. **Read** the guide's values (adapter) and the code's values, by name.
2. **Classify every name** with `design-sync.json` and [the diff format](references/export-diff.md):
   - **equal now** → in sync;
   - **guide changed** → propose;
   - **code changed** → offer to refresh the guide;
   - **both changed** → show the three values and **ask which wins**.

   With no `design-sync.json`, list every difference and ask the direction for each.
3. **Propose the edits** to the **source** files (never a generated output): file and line, what each affects, and the contrast for colours. "Proposed" states and substituted fonts aren't changes to export. **Stop.**
4. **Apply** only what was approved, update the guide for anything decided in the code's favour, and **run the project's checks** (lint, typecheck, tests, visual tests), or say there are none.
5. **Record:**
   - update `design-sync.json` with the values now equal on both sides;
   - add a dated line to `DESIGN.md` › Decisions log;
   - add open conflicts to Open questions.

## Rules

| Rule | Why |
|---|---|
| Same names in code and tool, by one written naming rule | One name per decision; no mapping to drift |
| `design-sync.json` records only agreed values | Without the last agreed value, "who changed it?" is a guess |
| Inventory and pick before drawing; conflicts listed there | Big packages and existing tool tokens need the person's say |
| Values from code, never from screenshots | Screenshots round colours and sizes |
| Missing states drawn as "proposed" | The guide must not claim the code does what it doesn't |
| Export proposes, then stops; edits the source, not generated output | Code ships to users; a generated file is overwritten by the next build |
| Both changed → ask | Overwriting either side loses someone's decision |
| Code is the source of truth until the person says otherwise | Matches "code beats a stale brief" |

## Done when

- **Import:** inventory and conflicts settled; picked components drawn; guide rendered (or "unrendered" stated); `design-sync.json` and `DESIGN.md` written.
- **One component:** drawn, with its status updated.
- **Export:** approved edits applied, the checks run (or "none" stated), `design-sync.json` updated, conflicts decided or open.

## Common mistakes

| Thought | Reality |
|---|---|
| "The code has the system, so setup only needs the brief" | Offer the import, or the tool never gets a guide and screens drift from the code. |
| "I'll build foundations and an index, components later" | Show the inventory and ask which components to draw now. |
| "I'll rename `--sand-200` to a role name while importing" | Keep the code's name; propose a role as an open question. |
| "The tool already has `--color-accent`, I'll update it" | That's a conflict for the inventory stop, not a silent overwrite. |
| "Guide and code differ, so the guide is out of date" | Check `design-sync.json`: it may be the person's unexported change. |
| "The diff is tiny, I'll just apply it" | Propose, stop, then apply and run the project's checks. |
