---
name: archlang-review-plan
description: Use when the user wants an existing ArchLang .arch floor plan checked rather than changed, e.g. "review this plan", "does this layout meet the brief?", "is every room reachable?", "check it for accessibility", "why does lint complain?". Reads the plan's facts, runs the lint profiles and the intent gate through the archlang CLI, and reports findings with suggested fixes. It edits nothing unless asked.
license: MIT
compatibility: Needs a shell with Node 18+ and the archlang CLI (npx -y @chanmeng666/archlang, or npm i -g @chanmeng666/archlang for a global archlang).
---

# Review a plan

Report what is true of a `.arch` plan and what is wrong with it, from the compiler's own facts.
If `archlang` is not on the path, write `npx -y @chanmeng666/archlang` in its place.
Never run a bare `arch`: on Linux, macOS and Git Bash that name is the coreutils command.

This skill is a workflow, not a language reference. Run `archlang spec` for the language,
`archlang context --section errors` for the diagnostic catalog, and `archlang <cmd> --help` for flags.

The checks are drafting heuristics. They do not establish that a plan meets a building code, and
your report must not say that it does.

## Steps

1. **Does it compile?** `archlang validate plan.arch --json`. Errors come first in the report; a plan
   with errors has no facts to review until they are fixed.
2. **Read the facts.** `archlang describe plan.arch --json` gives rooms with areas and uses, what each
   door and window connects, the access graph and the totals. On a large plan narrow it:
   `archlang describe plan.arch --select rooms,access,totals --json`. `area_m2` is measured on wall
   centrelines, so it counts the wall bands that stand on the room; `net_area_m2` subtracts them.
   Say which one you quote.
3. **Run the default lint.** `archlang lint plan.arch --json`. Each warning has a code, a place in the
   source and a `fix` in prose. `archlang explain <CODE> --json` explains a code you do not know.
4. **Run the accessibility profile when the user asks about access,** or when the brief mentions
   a wheelchair, step-free access or ageing in place:
   `archlang lint plan.arch --profile accessibility-advisory --json`.
5. **Check against the brief, if there is one.** Write the brief's checkable requirements as an
   intent file: room count only if the brief lists the rooms, an area band only where the brief
   gives a number. The format is the JSON Schema at <https://archlang.uk/intent.schema.json>,
   explained at <https://archlang.uk/intent>; a malformed file is refused with exit `3` and the
   path of the bad field. Then run
   `archlang validate plan.arch --intent intent.json --feedback --json`. A failed gating assertion
   exits `2` and comes with a correction prompt for each violation.
   `archlang score plan.arch --brief intent.json --json` gives the same comparison as a number that
   never fails.
6. **Ask for candidate fixes.** For an unreachable room, a building with no entrance, a bathroom
   reached only through a bedroom, or a bedroom with no window, `archlang suggest plan.arch --json`
   returns door and window statements with a reason for each. Put them in the report as options.
   Do not apply them.
7. **Look at it, if that helps.** `archlang preview plan.arch --ascii` prints a text plan;
   `archlang preview plan.arch -o plan.png` renders an image. `archlang compile plan.arch --overlay circulation -o walk.svg`
   draws the walking routes and their narrow points.

## Report to the user

Order the findings so the user can act on them:

1. Errors: the plan does not compile, with each diagnostic.
2. Brief: each requirement the plan misses, with the measured value beside the asked value.
3. Soundness: each lint warning, grouped by room, with the fix the diagnostic proposes.
4. What you did not check, for example "no brief was given, so nothing was compared to one".

State which lint profile produced each warning. Do not call a warning-free plan compliant, safe
or approved: say that the checks you ran raised nothing.

## When something goes wrong

- `--code` and `--severity` on `archlang lint` and `archlang validate` only filter what is shown. `ok` and
  the exit code still count every diagnostic, so a filtered result is not a clean one.
- Exit code `3` is a wrong flag: run `archlang <cmd> --help`.
