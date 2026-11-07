---
name: design-system
description: "Builds a design system for a codebase and keeps it enforced, by running five phases in order: measure the spacing, type and color values in use, settle the design decisions with the user, write them as tokens, update the code to use the tokens, and install a linter. Use when the user wants a design system, says their UI is inconsistent, or asks to standardize spacing, type or color."
---

# Design System

Runs the five Motif phases in order. Each phase reads the file the previous phase wrote, so none of them can run without the one before it.

| Phase | Skill | What it does | Writes |
|---|---|---|---|
| 1 | `design-extract` | Measures the values the code uses today | `.design/drift.json` |
| 2 | `design-grill` | Asks the user to settle each design decision | `.design/decisions.json` |
| 3 | `design-ratify` | Turns the decisions into tokens and docs | tokens, `DESIGN.md`, `.design/records/` |
| 4 | `design-apply` | Updates the code to use the tokens | one commit per batch |
| 5 | `design-enforce` | Installs a linter so the code stays consistent | `scripts/design-lint.mjs` |

## Steps

Check for progress from an earlier run:

```bash
ls .design/ 2>/dev/null && cat .design/state.json 2>/dev/null
```

Start at the first phase whose output file is missing, and tell the user which phase that is. This lets an interrupted run pick up where it stopped.

Call the Skill tool for each phase in order. Do not skip a phase.

## Never make up a value

Phases 1 to 3 decide what the system is. Phases 4 and 5 change the code to match it.

During phases 4 and 5, if the code needs a value that no token covers, stop and note it. Do not pick a substitute. At the end of the phase, show the user every value you noted, as questions. Each one is either a gap in the system or a value that shouldn't exist, and the user decides which.

## Passes to run afterwards

These four skills use the finished system. Each needs `DESIGN.md` and will not run without it.

| Skill | What it does |
|---|---|
| `beautify` | Fixes spacing, font sizes, line length, alignment and overflow without redesigning anything |
| `apply-transitions` | Adds transitions to things that currently appear or change instantly |
| `choose-icons` | Picks one icon library that covers what the product needs, and uses it everywhere |
| `empty-states` | Adds a proper empty state to anything that shows nothing when it has no data |
