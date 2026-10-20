---
name: build-design-system
description: Use when someone wants a design system built from the UI an app already ships, or one phase of it, such as "extract tokens from the app", "add states to our Button", "replace the hardcoded colors with tokens" or "start a design system". Moving screens onto an existing system's components is migrate-design-system. A vague whole-app ask goes to design-system-boss.
---

# Build a design system

Vocabulary is in `references/glossary.md`, defaults for bans and widths in `references/taste.md`. The app's own look is the source. Invent no colour, font, shadow, gradient or motion value it does not already have, unless the person chose a design source and confirmed a sample.

Scripts are in this skill's `scripts/`. Run them from the repo root with node, and read `--help` first. `scripts/capture.mjs` takes the screenshots behind `scripts/capture-guard.mjs`, which blocks every write, and `scripts/pixdiff.mjs` compares them. Capture and pixdiff need Playwright and a Chromium, which `scripts/find-chromium.mjs` finds or explains how to install.

## Steps

1. **Frame.** Read AGENTS.md or CLAUDE.md, the manifest and the route tree. Write the complaint in the person's words, the first visible change that answers it, and the pilot flow (the one the complaint names, else the flow with the most component families and a form with an error state). Add `.design-system/` to `.git/info/exclude` so no note, capture or scratch file is ever committed. Use the branch the person named as the run branch, or cut one and write the branch you started on to `.design-system/start-branch`, which `land.mjs` refuses. Offer `references/taste.md` once with its bans unselected and save the accepted copy to `.design-system/taste.md`. Ask nothing else. Take the default, record it as `default (unanswered)` and go on.
   Done when the complaint, pilot, branch and accepted taste file are written down.

2. **Inventory and baselines.** List every surface, its states and whether it writes data. Count raw values in occurrences (`#fff`, `text-gray-500`, `p-[13px]`) with `scripts/check-system.mjs --no-allowlist --no-self-test --json`, and group components into families. Capture every surface in every state at the narrowest and widest supported width (390 and 1280 by default), one fresh navigation per width, before any edit. With the app running (port 3000 here), list each surface as a `surface<TAB>route<TAB>states` row in `.design-system/surfaces.tsv` and every write the app sends as `METHOD URL` in `.design-system/writes.txt`, copied from its network log, then run `node <this skill>/scripts/capture.mjs --base http://localhost:3000 --kind before --out .design-system/captures --surfaces .design-system/surfaces.tsv --writes .design-system/writes.txt`. It refuses to start without `--writes` (or `--no-backend` for an app that sends no writes), proves each write blocked before the browser opens, saves each capture's accessibility tree and exits 1 on any capture it missed. Delete what nothing uses, in its own commit.
   Done when each surface has a baseline or a stated `not captured` reason.

3. **Tokens.** Cluster raw values by role, name them by purpose and pair each surface with its foreground (`references/tokens.md`). Run `token-mapping` until every raw value maps to a role, a merge or a listed exception. Merges inside tolerance are decisions. Past tolerance, open one gate per cluster whose default is the merge. Make every identical-value swap on every route.
   Done when `token-mapping` reports zero gaps outside the exception list and `pixdiff.mjs` at tolerance 0 reports 0% for every surface a swap touched.

4. **Components.** Build the most-used family end to end first (`references/components.md`). The text primitive and the small-text primitive ship in wave 1 beside Button. Document each with `component-docs`. Show the family to the person before fan-out, because a core bug found after screens consume the system costs a sweep (a disabled field still drawn red, a Combobox 2 px taller than Input, panel actions that do not wrap, a file drop that fails in silence).
   Done when every canonical component has a registry row and a doc, and its disabled, required, error and long-text states are captured in the showcase and shown to the person.

5. **Checks.** Copy `scripts/check-system.mjs` and `scripts/oklch.mjs` into the repo's `scripts/`, run `--init`, then `--init-allowlist` once. A rule counts only once it is seen failing: plant one violation in a scanned folder, run `--files <plant> --no-allowlist`, see exit 1 naming the rule, then delete the plant. The allowlist and ratchet only shrink. A ban ships with its check rule in the same change. Copy rules ship with their exemptions, element-scoped, for text that must stay verbatim (quotes, terms, version strings) and for payload strings that a machine or person pastes elsewhere (a prompt, an API example, a clipboard value), because rewriting them changes what someone else receives.
   Done when the check exits 0 on a clean clone, `--self-test` ends "all as expected", and every rule the run added was seen failing on its plant this session.

6. **Pilot.** Move the pilot flow with a codemod you read hunk by hunk. Capture after with the baseline's command, widths, themes and data, changing only `--kind after`, then `pixdiff.mjs` the two folders. An unexplained difference is a defect. Walk the flow by keyboard, force its error and loading states, then run `ui-review` on the after captures.
   Done when every difference in the captures traces to a decision or gate. A rendered change with no capture is reported `checks-only`.

7. **Readiness.** Before a migration fans out, the five audits below hold or carry a recorded exemption.

8. **Handoff.** Rerun the counts. Report what the system covers in numbers, unanswered defaults first, then what was found and not fixed, ranked. Offer the migration with its size. Do not start it.
   Done when every number in the report names the command that produced it.

## Readiness audits

A gap found after screens consume the system costs a sweep. A gap found before costs a row. Run these at the end of step 5 and again before the first wave. Write each result to `.design-system/readiness.md` with a verdict word.

1. **Slot and prop parity.** Every prop of each legacy primitive that has call sites has a matching prop on the new primitive or a gap row.
2. **Behaviour contracts.** A "what fires when" table per interactive primitive, each row a test (`references/components.md`).
3. **Tone parity.** Every pressable and row primitive crossed with every status tone plus muted. Each empty cell is a gap row or stated unsupported.
4. **Pinned strings.** Every legacy test query by role name or text has a default name on the new primitive and a label override.
5. **Hardest screens.** One hardest call site per family renders in the showcase, with a screenshot.

A family that is not ready is not migrated. Its screens stay on legacy.

## Never

- Push, publish or deploy, unless the person asks for it in this session.
- Commit on the branch the run started on. Cut the run branch first.
- Stash, or switch branches in a dirty checkout. A dirty checkout gets the run branch in its own worktree (`git worktree add`).
- Delete anything another package or a public API exports. Stop, and list it as a gate with its importers.
- Skip a step in silence. If the app will not build or run, the report says `code-complete, not runtime-verified` and names what was not exercised.
- Call your own work `verified`. On a host that cannot start other agents, run the steps in order, check each from a fresh read of the diff and the captures, and mark those verdicts `self-verified`.

## Rules

- Raw value smells are `#fff`, `rgb(`, `text-gray-500`, `p-[13px]` and `style={{ padding: 12 }}`. Each maps to a semantic token or a listed exception.
- A missing primitive is a gap row, never a workaround inside a surface.
- Colour merges inside delta E OK 2 and spacing merges inside 2 px are decisions. Border width, weight and easing have no tolerance.
- A change that only adds semantics (a name, a role, `aria-current`) is a decision. One that removes or restructures semantics is a gate.
- Wrong: `{saving ? "Saving..." : "Save"}`. Right: the idle label stays, a spinner sits inside the same box, `aria-busy` is set.
- A fix that recurs twice becomes a check rule or a script, not another sentence.
- A baseline is never edited to make a diff pass. A check that flags correct code is fixed in the check, with a planted case that proves the fix, never by bending the code.
- A count no script produced, or a check never seen failing, is not reported.

## Done

The check exits 0 on a clean clone with every rule seen failing, every route answers 200 on the production build (`capture.mjs --status`), the pilot matches its baseline except for the listed intended changes, and every handoff count comes from a script.

`references/traps.md` lists behaviour traps by ID. `references/tokens.md` holds layers, names, tolerances and motion presets.
