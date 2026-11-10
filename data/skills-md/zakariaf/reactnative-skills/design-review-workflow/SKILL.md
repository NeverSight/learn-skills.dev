---
name: design-review-workflow
description: "Runs the end-of-build design review: every screen x theme x direction x text size x device, graded findings, a fix round, a sign-off. Use when a release nears or needs a QA sweep or sign-off. Not for parity (design-visual-parity)."
---

# Design review workflow

Once per release, at the end, on a green release build: a capture sweep of every screen and state in
both themes, both text directions, the default and the largest text size, on the smallest phone and a
large screen of each platform, every motion moment on video, and an on-device pass on real cheap
phones. Findings are graded, fixed in exactly one round and verified on new shots, and a dated
sign-off in a committed record gates the release. Four zero-dependency scripts prove the plan covers
the app, the record is complete and honest, and nothing people see changed after the sign-off.

## Rules that must hold

1. **Review once per release, at the end, on a build whose gates are green; never per task.** The
   record names the swept commit and `"verify": "pass"` (`review-record`). Why: blocking build tasks on
   a visual critique slows every task, and a review of a red build re-tests what CI proves instead of
   judging what only eyes, ears and hands catch.
2. **The plan sweeps the whole app, decided by the app's own facts.** Every screen and state of the
   screen contract (embedded parts and reasoned exclusions aside), every theme `userInterfaceStyle`
   shows, one ltr and one rtl locale, `default` on every device and `largest` (iOS
   `accessibility-extra-extra-extra-large`, Android `font_scale` 2) on every smallest phone, a smallest
   phone and a large screen per platform, the large screens in landscape (Android's always, the
   iPad's unless `requireFullScreen`), because a portrait lock binds phones only (`plan-screens`,
   `plan-themes`, `plan-locales`, `plan-text-sizes`, `plan-devices`). Why: nobody looks at every
   screen otherwise, and the worst cell (dark, rtl, largest text, smallest phone) is where most bugs are.
3. **Every state opens by a recorded link.** `screens.open` maps each `<screen>.<state>` to a
   debug-link query (parameters from `contracts/debug-links.json`, never `lang`, `theme` or `motion`)
   or an app path (`plan-open`). Why: a cell anyone can re-shoot the same way is evidence; a state
   reached by tapping through a flow drifts between runs.
4. **Sweep the preview build on simulators and emulators you created and named.** `preview` only
   (Release JavaScript that keeps the debug link every combination sets language, theme and
   `motion=still` through, and the videos `motion=system`, so the contract must declare those values), each device
   `<project>-<purpose>`, the status bar pinned to 9:41, stills captured upright by the runner, never
   by the flow (`plan-build`, `plan-open`, `plan-devices`). Why: the development client, a shared or
   "booted" device and a moving clock make captures that differ where the app does not; production
   strips the link, and the on-device pass judges the store build.
5. **Every cell is a real capture in one folder, and an axis that changed nothing is a failure.** One
   PNG per cell named `<screen>.<state>--<theme>--<locale>--<text>--<device>.png`, its hash in the
   record, not blank (at least three colours), the device's size and orientation; two captures that
   differ only in theme, locale or text size and are identical fail unless the plan declares the
   screen invariant there (`review-cells`, `review-capture`, `review-axis`). Why: a missing appearance or language switch
   produces a sweep that looks complete and checks nothing.
6. **Motion is judged on video, at full and reduced motion, per platform.** Every moment of the motion
   catalog is recorded or listed with why; each recorded moment has both videos (`plan-motion`,
   `review-videos`). Why: a still cannot show a skip, a blocked tap or a reduced alternative.
7. **Grade every finding BLOCKER, FIX or NOTE; every accessibility-floor finding is a BLOCKER.**
   Contrast, touch target, text scale, colour alone, direction, reduce motion, screen reader and
   assistive access, and a failed floor or data step of the device pass, are BLOCKERs however good the
   screen looks; a BLOCKER or FIX is never deferred (`review-findings`, `review-floor`). Why: the floor
   is what keeps the app usable, and aesthetics never buy it back.
8. **Run the on-device pass on real, cheap phones in real state, every step answered, destructive
   steps last.** One phone per shipped platform with model, OS and day; every core step `pass`, `fail`
   with its finding, or `n/a` with why, in plan order (`plan-device-pass`, `review-device-pass`). Why:
   screenshots prove layout, never audio, haptics, fonts, memory or upgrades; and upgrade, restore,
   crash and reinstall destroy the state the other steps need.
9. **Exactly one fix round, every fix verified on its new shot, and verification opens only NOTEs.**
   The round's commit and green gates are recorded, each fixed finding's cells and videos differ from
   the captures it was seen on, and a finding opened while verifying is a NOTE (`review-fix-round`). Why: a second round
   never ends, and a fix nobody looked at again is a guess.
10. **The dated sign-off agrees with the record.** Date (local, not future, after the fix round),
    reviewer, the commit that was looked at, and `SIGNED OFF` only with every BLOCKER and FIX fixed,
    every NOTE in the backlog, every cell and video captured and no failed step; otherwise
    `NOT SIGNED OFF` with the escalation (`review-signoff`). Why: a verdict that contradicts the
    findings is a rubber stamp.
11. **The sign-off gates the release.** The newest review of the version is SIGNED OFF, the plan and
    screen contract are unchanged since, and no user-facing file changed after the signed commit
    (`signoff-missing`, `signoff-stale`, `signoff-ui-changed`): app code, assets, the entry, the app
    config and the files it imports, the lockfiles, the build transforms, `eas.json`, plugins, patches
    and env files, plus the plan's `signoff.watch`; a release lane's build-number bump alone does not
    count. Why: the build people looked at must be the build that ships.
12. **Never narrow the sweep or soften the record to get a pass.** The text sizes are fixed values, a
    sign-off refuses uncaptured cells, and a ship gate never skips. Why: a narrowed or clamped sweep
    hides exactly the clipping and mirroring the review exists to catch.

## Workflow

1. **Trigger.** Every build task of the release is done and `npm run verify` is green on the commit.
   Read [references/record-and-signoff.md](references/record-and-signoff.md) ("When a review runs").
2. **Plan, once per app.** Copy `templates/contracts/design-review.json` and its schema to
   `contracts/`; fill the devices, the open link of every state and the hardware from
   [references/sweep-matrix.md](references/sweep-matrix.md). Run
   `node ${CLAUDE_SKILL_DIR}/scripts/check-review-plan.mjs .` until `RESULT: PASS`; `--list` prints
   every cell. Commit the plan on its own.
3. **Start the record.** `node ${CLAUDE_SKILL_DIR}/scripts/new-review.mjs .` writes
   `design-review/<review-id>/review.json` and the capture folders; fill `build.commit` and
   `"verify": "pass"`.
4. **Capture.** Copy `templates/scripts/design-review/review-cells.ts` and `device-settings.ts` (with
   their tests) into the app; build a runner shaped like
   [examples/capture-sweep.ts](examples/capture-sweep.ts) and
   [examples/open-cell.yaml](examples/open-cell.yaml) (e2e-maestro owns the Maestro runner). Follow
   [references/capture-recipes.md](references/capture-recipes.md): your own named devices, Release
   build, clean status bar, the planned orientation, then every combination, then `motion=system`
   (`VIDEO_QUERY`: the stills' `motion=still` is saved) and every motion video. Then
   `node ${CLAUDE_SKILL_DIR}/scripts/new-review.mjs . --refresh` and
   `node ${CLAUDE_SKILL_DIR}/scripts/check-review.mjs . --in-progress` until only findings, the device
   pass and the sign-off remain.
5. **Look and grade.** Read every cell and watch every video, following
   [references/grading-rubric.md](references/grading-rubric.md); write each finding with its exact
   cell names, lens and grade. Consolidate one finding per cause.
6. **Device pass (human step).** Ask a person for it on the store-channel builds, following
   [references/device-pass.md](references/device-pass.md); record every answer as reported, never
   from memory.
7. **Fix round.** `new-review.mjs . --refresh` (stores each finding's `seen` hashes); fix every BLOCKER
   and FIX with a failing test first where a machine can catch it; run the gates; re-shoot only the
   named cells and videos and re-run failed steps; `--refresh`; look at each new capture; record the
   fix round.
8. **Sign off.** Write the sign-off (or `NOT SIGNED OFF` with the escalation), then
   `node ${CLAUDE_SKILL_DIR}/scripts/check-review.mjs .` until `RESULT: PASS`. Any FAIL line:
   [references/failure-messages.md](references/failure-messages.md). [examples/tasks-review.json](examples/tasks-review.json) is a
   finished record.
9. **Gate the release.** `node ${CLAUDE_SKILL_DIR}/scripts/check-signoff.mjs .` (in CI with full
   history, or `--changed-from <file>` holding `git diff -U0 <signed>..<release>`). Put the Design review line in the release report
   (git-commits-and-reporting), deferred NOTEs under "Not tested or not verified", and archive the
   capture folder with the release.

## Definition of done

- [ ] The review ran once, at the end, on a Release build of a commit whose gates were green.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-review-plan.mjs .` prints `RESULT: PASS`. Allowed SKIP
      lines, only while their owners have not created the file (a review itself needs the screen
      contract): `SKIP contracts/debug-links.json [plan-open] not yet created (debug-menu-and-test-hooks creates it)`,
      `SKIP src/ui/motion/motion-moments.ts [plan-motion] not yet created (motion-and-animation creates it)`,
      `SKIP contracts/screens.json [plan-screens] not yet created (screen-contracts creates it)`,
      `SKIP src/i18n/languages.ts [plan-locales] not yet created (i18n-strings-and-catalogs creates it)`.
- [ ] Every cell and motion video is captured, every cell and video was looked at, every finding is
      graded with the floor as BLOCKER, the on-device pass is answered on real phones, and the one fix
      round is verified on new shots.
- [ ] The record is committed with a dated sign-off; the capture folder is archived with the release.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-review.mjs .` prints `RESULT: PASS` on the machine that holds the captures.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-signoff.mjs .` prints `RESULT: PASS`

## Anti-patterns

- **Per-task design review.** Critiquing pixels while building blocks every task; note it and keep
  going, the review looks at everything once.
- **Reviewing a debug build, the development client, or a shared "booted" simulator.** Wrong bundle,
  overlays, someone else's device; sweep the preview Release build on devices you created.
- **A sample instead of the matrix.** "I checked the main screens in light mode" finds nothing that
  breaks; every cell, then the worst cell of each screen.
- **Clamping text or picking a "largest" the layout survives.** That hides the bug the cell exists to
  find; the cap is accessibility-as-code's 200 %, never lower.
- **Skipping right to left because the device locale has none.** The in-app language (the debug link's
  `lang`) is the path people use and the hardest case.
- **Grading a floor miss as FIX because the screen is beautiful.** Floor misses are BLOCKERs.
- **A second fix round, or quiet iteration on a surviving BLOCKER.** One round; then sign-off or
  escalation and a new review.
- **Marking a finding fixed without re-shooting its cells or recording its videos again.**
  `review-fix-round` refuses it; look at the new capture.
- **Re-testing what CI proves.** Lint, types, catalog parity and goldens are the precondition, not the
  review.
- **A device farm or a flagship instead of a cheap phone in real state.** Both hide what the median
  person hits.
- **Shipping after a change to `src/`, a lockfile or the build config with the old sign-off.** The
  gate fails it; re-shoot and sign again, or revert.
- **A loose note as the sign-off.** It is a committed record the release gate reads.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/sweep-matrix.md](references/sweep-matrix.md) | The axes and why, cell names and cost, every plan key, devices and models, text sizes, motion, hardware | Workflow step 2; any `plan-*` failure |
| [references/capture-recipes.md](references/capture-recipes.md) | Named devices, the capture order, iOS and Android commands, motion videos, pitfalls, what was verified | Workflow step 4 |
| [references/grading-rubric.md](references/grading-rubric.md) | How to look, the five lenses, the accessibility floor, grades, the finding format, examples | Workflow step 5 |
| [references/device-pass.md](references/device-pass.md) | The hardware, the eleven core steps, recording results, asking a person | Workflow step 6 |
| [references/record-and-signoff.md](references/record-and-signoff.md) | When a review runs, the record's life and format, hashes, the fix round, the sign-off, the release gate, CI, the report line | Workflow steps 1, 3, 7 to 9 |
| [references/failure-messages.md](references/failure-messages.md) | Every rule id with cause and fix, the ERROR and SKIP lines, the limits of the picture heuristics | Any FAIL, ERROR or SKIP line |
| `templates/contracts/design-review.json` | The plan for the reference Tasks app (2 screens, 4 devices, 48 cells, 8 videos) | Workflow step 2 (copy, then fill) |
| `templates/contracts/design-review.schema.json` | Its JSON schema | Workflow step 2 (copy with it) |
| `templates/scripts/design-review/review-cells.ts` | Cells, capture combinations, open links, files and videos for the app's runner | Workflow step 4 (copy with its test) |
| `templates/scripts/design-review/review-cells.test.ts` | Its test | Workflow step 4 (copy) |
| `templates/scripts/design-review/device-settings.ts` | Appearance, text size, orientation, status bar, upright screenshot, video and animation-scale commands, always on a named device | Workflow step 4 (copy with its test) |
| `templates/scripts/design-review/device-settings.test.ts` | Its test | Workflow step 4 (copy) |
| [examples/capture-sweep.ts](examples/capture-sweep.ts) | The shape of a sweep runner built on the two templates: devices in parallel, one capture path | Workflow step 4 |
| [examples/open-cell.yaml](examples/open-cell.yaml) | The shape of a Maestro flow that turns the simulator, opens a link and waits for the cell | Workflow step 4 |
| [examples/tasks-review.json](examples/tasks-review.json) | A finished, signed-off record: one FIX fixed and re-shot, one NOTE in the backlog | Workflow steps 5 to 8 |
| `scripts/check-review-plan.mjs` | Proves the plan covers the app; `--list` prints every cell and video | Workflow step 2 and before every review |
| `scripts/new-review.mjs` | Writes the record from the plan; `--refresh` follows the plan, stores `seen` hashes, hashes captures | Workflow steps 3, 4 and 7 |
| `scripts/check-review.mjs` | Proves one review: captures, axes, videos, findings, device pass, fix round, sign-off; `--in-progress` | Workflow steps 4 and 8 |
| `scripts/check-signoff.mjs` | The release gate: signed off, not stale, nothing user-facing changed since; `--changed-from` for CI | Workflow step 9; before every release upload |
| `scripts/selftest.mjs` | Proves every script on a reviewed Tasks app and planted bugs; compares the template's cell grammar | After changing a script |
| `scripts/lib/review-plan.mjs` | The plan, the app facts, the cell grammar (this skill's own) | Never directly |
| `scripts/lib/review-record.mjs` | The record, the shared review rules, the Prettier-shaped JSON writer (this skill's own) | Never directly |
| `scripts/lib/ts-literal.mjs` | Reads TypeScript literal data (synced, do not edit) | Never directly |
| `scripts/check-lib.mjs` | Shared script library (synced, do not edit) | Never directly |
| `tests/bases/app/` | The small Tasks app the fixtures start from | When changing a script |
| `tests/fixtures/` | Overlay cases per script: good, pass-*, bad-* (one planted bug per rule), error-* | When changing a script |
| `assets/shared.json` | The shared files this skill syncs | When adding a shared file |

## Related skills

- `design-visual-parity` - per-screen match with the approved design baselines while building.
- `accessibility-as-code` - the floor's numbers and the screen-reader checklist the device pass runs.
- `screen-contracts` - the screens and states the sweep covers.
- `debug-menu-and-test-hooks` - the debug link that opens every state and holds motion still.
- `e2e-maestro` - the Maestro flows and runner that capture the cells.
- `ios-simulator-build` / `android-emulator-build` - the Release builds on named devices.
- `motion-and-animation` - the moment catalog recorded on video.
- `rtl-and-direction`, `i18n-strings-and-catalogs`, `adaptive-layout` - what the rtl, locale and tablet cells judge.
- `ui-states-and-feedback` - the empty, error and offline states swept as their own cells.
- `tdd-workflow` - a failing test first for every fix a machine can catch.
- `git-commits-and-reporting` - the release report line and the stop-and-ask for the device pass.
- `ci-pipeline-and-gates`, `ios-release-testflight`, `android-release-play`, `eas-build-and-submit` - where the release gate runs.
- `run-migration`, `data-export-and-restore` - the upgrade and restore steps of the device pass.
