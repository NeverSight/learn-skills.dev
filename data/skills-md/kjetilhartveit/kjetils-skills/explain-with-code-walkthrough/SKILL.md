---
name: explain-with-code-walkthrough
description: Use when asked to explain visually with a code walkthrough.
---

# Explain with Code Walkthrough

Short steps on the left scroll past a sticky code panel on the right, held in the vertical centre of the viewport.
For each step the panel shows the right file and highlights the lines that step is about. The reader watches
today's code become the proposed code.

## Use this skill when

- The user asks for a visual explanation of changes with a code walkthrough.
- Used by an orchestrator to explain changes visually with a code walkthrough.

## Steps

- 4–8 steps, in the order a reader should understand them (usually: today's code → where the change goes → the
  new code → who uses it).
- Each step: **one bold sentence** saying what this step shows, then at most 1–2 short lines.
- The current step gets a mild marker (the kit's `ev-step.is-active`: accent edge and a faint tint). Never dim
  the other steps.
- Deeper explanation, tables and traces go in one `ev-more` toggle per step whose summary **names what's inside**
  (e.g. "Why 5 rows are enough · Tick trace"). The reader should know what they'd get without clicking.
- Make toggle content visual: highlighted code, groups, status chips, compact tables. No walls of text.

## The code panel

- Show real code from the codebase (or the proposed code), with the file path in the panel header. 3–4 snippets
  of ≤ 15 lines each are plenty.
- Animate with **highlights, not content shifts**: dim unfocused lines, glide a focus band to the new range,
  cross-fade when the file changes. Don't grow or collapse lines while the reader is looking.
- The panel's first state (file and highlighted lines) belongs to step 1 and must not change while step 1 is
  current. The first change happens when step 2 becomes current.
- Scrolling back up restores the earlier step's file and highlight exactly: set the panel from the step number
  alone, never from the previous state.
- Mark new lines with a green `+` gutter and removed lines with `−`.
- Select lines by stable ids (tag lines in the code data), not by hand-counted line numbers, which drift.
- Keep snippets to the relevant lines plus a little context; mark skipped parts ("⋯ 12 lines hidden") instead of
  showing whole files. Avoid lines that need sideways scrolling where possible.

## Phones

- Add `ev-side--pin` to pin the code panel above the steps on phones; keep lines short (≤ 70 characters) so
  nothing scrolls sideways.

## Building it

- Build it as a fragment with the `explainer-kit` skill (its `SCRIPTS-AND-TABS.md` covers `EV.steps`). Use the kit's code block (`ev-code` with `data-add`,
  `data-hl`, `data-groups`, `data-marks`) for inline and toggle code.
- Lay it out with the kit's `ev-side` (steps left) + `ev-stick` (code panel right, sticky and vertically centred
  below the top bar). The first step starts at the top of its column, level with the code panel (no top padding or
  spacer); add bottom padding so the last step can reach the middle. Make steps `ev-step` boxes and drive the
  panel with `EV.steps(steps, function (i) { … })` (not an `IntersectionObserver`, which gets the reverse scroll
  wrong). Initialise in `EV.onShow` and re-measure the focus band on resize.
- Give each step `id` + `data-toc` so it appears in the chapter list.
