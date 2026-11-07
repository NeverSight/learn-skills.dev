---
name: archlang-brief-to-plan
description: Use when the user gives a written brief for a new floor plan (rooms, areas, how rooms connect, a plot size) and wants the drawing, e.g. "design a two-bedroom flat of about 75 m²" or "lay out a small office with four rooms". Writes an ArchLang .arch file from the brief, checks it against the brief with the archlang CLI, and finishes it as a sheet. Not for changing an existing plan (archlang-edit-plan) or for exporting one (archlang-export).
license: MIT
compatibility: Needs a shell with Node 18+ and the archlang CLI (npx -y @chanmeng666/archlang, or npm i -g @chanmeng666/archlang for a global archlang).
---

# Brief to plan

Turn a written brief into a checked `.arch` floor plan. Every step is a CLI call; never judge the
plan from the SVG markup.
If `archlang` is not on the path, write `npx -y @chanmeng666/archlang` in its place.
Never run a bare `arch`: on Linux, macOS and Git Bash that name is the coreutils command.

This skill is a workflow, not a language reference. The language is whatever `archlang spec` prints.

## Scope

- Run the `archlang` CLI commands below and no other program.
- Write one new plan file, `plan.arch` here or the name the user gives, in the user's working
  directory, plus the drawings the CLI renders beside it. If a file of that name already exists,
  ask the user before replacing it.
- The user's explicit instructions take priority over these steps.

## Steps

1. **Read the language.** Run `archlang spec` and read all of it before writing a line. For one
   command's flags and examples run `archlang <cmd> --help`, for example `archlang finish --help`.
2. **List what the brief asks for.** Write down each room, each stated area, each stated
   connection ("opens off the hall"), each stated window, and any outer size. Keep numbers exactly
   as the brief states them. If two requirements cannot both hold, stop and tell the user which
   ones; do not quietly change a number.
3. **Write `plan.arch`.** Give every room an `id`, a `label` and a `uses`. Attach doors and windows
   to walls and place furniture by anchor, as `archlang spec` shows, instead of computing coordinates.
   Give every room a door or an opening.
4. **Compile.** `archlang compile plan.arch -o plan.svg --json`. If `ok` is false, read each
   `diagnostics[].fix`. Preview the mechanical fixes with `archlang fix plan.arch --dry-run --json`,
   then apply them with `archlang fix plan.arch`. Fix the rest by hand and compile again.
5. **Check the plan against your list.** `archlang describe plan.arch --select rooms,doors,windows,totals --json`.
   Compare room count, labels, each area, what each door connects and which rooms have windows
   with the list from step 2. Edit and repeat from step 4 until they match. `area_m2` is measured on
   wall centrelines; `net_area_m2` is the floor no wall stands on.
6. **Check soundness.** `archlang lint plan.arch --json`. Fix each warning, or keep it on purpose and
   say why. If a room cannot be reached or a bedroom has no window, `archlang suggest plan.arch --json`
   returns door and window statements you can paste.
7. **Finish the drawing.** `archlang finish plan.arch --dry-run --json` shows the furniture and sheet
   statements it would add; `archlang finish plan.arch` applies them. Read `unresolved`: it names each
   room left empty and each statement left out, with the reason.
8. **Gate and show.** `archlang validate plan.arch --strict --json` must exit `0`, or you must be able
   to name each remaining warning as deliberate. Then `archlang preview plan.arch -o plan.png` to show
   the user.

## Report to the user

- The file you wrote and the drawing you rendered.
- Every requirement of the brief the plan does not meet, or "none".
- Which area you quote: `net_area_m2` is the floor no wall stands on, `area_m2` the larger
  centreline figure. If a room has no `net_area_m2`, say its net area could not be computed.
- Every lint warning still present, with the reason it stays.

## When something goes wrong

- Exit code `2` is a fault in the source. Read the diagnostic and fix it; do not run the same
  command again unchanged. `3` is a wrong flag: run `archlang <cmd> --help`.
- For an unfamiliar code, run `archlang explain <CODE> --json`.
- To gate on the brief as data instead of by eye, write it as an intent file and run
  `archlang validate plan.arch --intent intent.json --feedback --json`. The archlang-review-plan
  skill covers this.
