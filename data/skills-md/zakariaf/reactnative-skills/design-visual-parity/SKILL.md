---
name: design-visual-parity
description: Proves built screens match approved design references (iOS, Android, light/dark, RTL) per element. Use when a screen is built or changed, or for visual parity, design match, screenshot compare. Not for building screens (screen-contracts).
---

# Design visual parity

Makes one rule true: every built screen is compared with its approved design reference on every
device, theme and language of the app, and fixed until it matches. Machines check geometry, text,
colour, borders, type and shape per element; the agent checks the rest by looking at side-by-side
sheets; `check-signoff.mjs` proves both happened for the current build and writes the summary a report's
"Design match" line names.

## Rules that must hold

1. **No screen is done until every run of the done set passes**: each design frame on every device of
   the contract (an iOS simulator and an Android emulator by default), in light and dark, in every
   language the app ships (its RTL one included), at every scroll offset `run-parity.mjs` plans for a
   tall frame, against the reference the app's facts pick. Narrowing is for iteration: a narrowed check
   prints `narrowed: not a sign-off` and fails. Why: dark mode and right to left are where screens
   break; one passing variant proves little. (`narrowed`, `not-captured`, `coverage`)
2. **The committed references are the authority.** They change only after the reviewer approved a
   design change, logged first in the manifest's `referenceChanges`, rendered with
   `shoot-design.mjs --update-reference --change <id>`; never to make a screen pass, and a change is
   never a waiver. Why: a reference edited to match the app turns the check into a mirror.
   (`reference-change-unlogged`, `reference-drift`, `stale-reference`)
3. **The app's facts pick the reference; nobody guesses.** A frame that depends on what the app has
   gets design-derived variants (contract `facts`, `variants`), composed when several match; a fact left
   out stops every script; a variant is derived from the rendered mockup, never drawn by hand. Why: a
   missing element that only another fact has is a wrong reference, not a waiver.
   (`reference-variant`, `variant-derive`, `contract-invalid`)
4. **Never widen a tolerance, add a mask or skip a gate to get a pass.** Every number is a measured
   noise floor; type-role floors need their probe evidence and stay at or under 3 pt. What the platform
   truly cannot draw gets a waiver: one element, one rule, its class (`platform`,
   `platform-text-shaping` naming the glyphs, `design-artefact` quoting the mockup CSS), the reason,
   the date the reviewer was told. Why: a widened number hides every future defect of that size.
   (`waiver-invalid`)
5. **Capture the real app with `capture-app.mjs` on this session's own named device**: a Release build
   of a development or preview variant, launched straight into the frame (iOS: the `-parity` launch
   argument, never `simctl openurl`; Android: the parity link sent to the named package). Every call
   names its device (a UDID, `adb -s <serial>`, Maestro `--device` and this run's own driver port
   before the command, on both platforms), and every launch carries a nonce the hierarchy dump must contain. Why: a dump
   once came from another session's simulator; a Debug build, a deep link alert or a hand-made
   screenshot compares nothing. (`system-alert`, `unstable`, `changed-during-capture`, `not-a-capture`)
6. **Machine gates first, then the look.** `check-parity.mjs` must pass, then every sheet image is read
   and the seven eye checks and every difference go into the ledger for exactly that sheet. Why: the
   gates have tolerances; icons, pictures, shadow feel, wrapping and mirroring need eyes.
   (`not-looked`, `eye-check-open`, `difference-open`, `looked-at-old-sheet`, `stale-sheet`)
7. **Fix the app one gate at a time, in the printed order** (reached, scroll, missing, bounds, text,
   fill, border, text-ink, structure); read the element's crop before changing code; stop and report
   after three failed fixes of the same failure. Why: a wrong padding moves everything below it.
8. **testIDs exactly as the screen contract says, on the accessible element; bounds only for what
   Maestro can list.** Parts inside an accessible element (`parent`) and decoration hidden from screen
   readers (`a11yHidden`) are crop-only, judged in their `coveredBy` ancestor's aligned crop, never
   `missing`; never un-hide decoration to measure it. Why: Maestro reads the accessibility tree.
   (`element-reach`, `element-cover`, `missing`)
9. **The harness is the shipped templates, test-only.** One strict launch parser (an error screen on
   bad input, never a silent fallback), the consent moment held (in an app with ads only an
   `ADS_MODE=off` build launches), every test-build switch set on every launch, the design's
   fixture written unchanged through the app's repositories, each frame state opened by its owning
   model's `useFrameStateOpener` through the handler a press uses, motion held still through the one
   reduce-motion path, reached only through the test-only gate, the launch marker in every modal root
   as the first child of its `accessibilityViewIsModal` view (the shared Scrim and ConfirmDialog
   included), no capture-only branch (`harness-capture-branch`).
   Why: a hand-written harness kept stale state across frames and drew things the screen never would.
   (`harness-*`, check-harness.mjs)
10. **The mockup is static, offline and marked.** One `data-frame` per design frame, one `data-testid`
    per element of the frame and no unknown ones, fonts from the exact files the app bundles. Why: both
    sides must rasterise the same outlines, and a mockup that disagrees with the contract renders
    references nobody can match. (`mockup-*`, `fonts`, `design-text`)
11. **Pixel identity is never promised.** Anti-aliasing, 1/3 pt rounding and each type role's measured
    glyph offset always differ; the whole-screen difference is printed for information and never
    decides. Why: correct builds scored 0.13-0.51 %, overlapping real defects.
12. **The waivers, references (with the manifest), fixture, mockup and device profiles are gated
    paths, the sign-off ledger is not; the summary backs the report.** A commit that changes a gated
    one carries a `Gate-Change:` trailer; a report's Design match line names
    `reports/parity/summary.json`. Why: what the gate accepts changes only on purpose and in sight.
    (`gated-paths`)

## Workflow

1. **Look first.** From the app root run `node ${CLAUDE_SKILL_DIR}/scripts/check-mockup.mjs .` and
   `node ${CLAUDE_SKILL_DIR}/scripts/check-harness.mjs .`. NOT APPLICABLE means the app keeps no parity
   contract yet: step 2. Read [references/contract-format.md](references/contract-format.md) once.
2. **The contract and the mockup, once per app.** Copy `templates/contracts/visual-parity.json` (+
   schema) to `contracts/`, `templates/design/parity/` to `design/parity/` (device profiles, empty
   waivers and ledger, the fixture, the demo mockup), and give each design frame's screen-contract state
   its `"reference": "<frame>.png"` (screen-contracts; [examples/screens.json](examples/screens.json)
   shows the shape; step 3 writes the image it names). Draw or port the approved design into the mockup
   following [references/mockup-and-references.md](references/mockup-and-references.md); run
   `check-mockup.mjs .` until `RESULT: PASS`.
3. **The references, once per approved design.** Install the pinned Playwright once (`npm ci --prefix
   ${CLAUDE_SKILL_DIR}/scripts`, or into `.skill-tooling/design-visual-parity` with `--tooling` when the
   skill folder is read-only or shared). The first render of an approved design: `node
   ${CLAUDE_SKILL_DIR}/scripts/shoot-design.mjs . --update-reference` (it also writes the screen
   contract's `<frame>.png`); later ones only after logging the change (`--change <id>`); prove them
   with `shoot-design.mjs . --check`. The reviewer looks at the
   renders and approves them.
4. **The harness, once per app.** Read [references/parity-harness.md](references/parity-harness.md).
   Copy `templates/src/features/parity/` (the parity kit `parity-root-kit.tsx` included),
   `templates/src/hooks/use-frame-request.tsx`, `use-frame-state-opener.ts` and
   `use-frame-scroll-target.ts`, and `templates/src/ui/parity-launch-marker.tsx` (each with its
   test); export `createParityKit` and the app's launch screen from the test-only entry
   ([examples/test-only-entry-additions.ts](examples/test-only-entry-additions.ts)), register the kit
   in the app's root-kit registry among the test build's kits
   ([examples/create-root-kits-parity.ts](examples/create-root-kits-parity.ts): the root skeleton stays
   unchanged) and add the launch route ([examples/parity-route.tsx](examples/parity-route.tsx)); build
   the appliers, `consent` included; open each planned frame state in its model; add the marker to the
   shared modal roots; register the launch route in `contracts/navigation.json` (`routes`,
   `debugRoutes`) and `contracts/screens.json` (`ignoredRoutes`); keep `.parity/` git-ignored and the
   parity paths gated (both in the canonical `.gitignore` and `quality-gates.json`; rule 12: listed one
   by one, never `design/parity/**`, plus `design/parity/<device>/**` for a device beyond the two
   defaults). Run the harness tests (`npx jest src/features/parity src/hooks/use-frame
   src/ui/parity-launch-marker.test.tsx --ci --maxWorkers=2`), then `check-harness.mjs .` until it
   passes. Before the first approved design, `contracts/visual-parity.json` may plan no frame
   (`"frames": {}` and no screen state with a `reference`): check-harness still proves the wiring and
   the frame scripts print NOT APPLICABLE.
5. **Before building or changing a screen,** open its references (light and dark RTL first), the
   frame's elements (screen-contracts' `list-screen.mjs`) and the frame kind and masks in the contract.
6. **The device, once per session.** `node ${CLAUDE_SKILL_DIR}/scripts/setup-parity-device.mjs .
   --device iphone-16-pro --appearance light --name <project>-parity-<key>` (and the same for
   `android-parity`); it prints the UDID or serial. Build and install the Release build of the preview
   variant on it (ios-simulator-build, android-emulator-build). Read
   [references/devices-and-capture.md](references/devices-and-capture.md) when anything fails.
7. **Run the machine side:** `node ${CLAUDE_SKILL_DIR}/scripts/run-parity.mjs . --screen <id> --device
   iphone-16-pro --name <project>-parity-<key>`: capture, check and sheets for every frame of the screen
   in every theme and language (tall frames at every planned offset). A run takes 10 to 20 s, so run a
   whole screen in the background or narrow with `--frame`, `--themes`, `--langs` while fixing, never
   for the sign-off. Repeat per device. After a hand-run `check-parity.mjs`, `node
   ${CLAUDE_SKILL_DIR}/scripts/make-sheet.mjs . --run <run-dir>` redraws that run's sheets.
8. **On FAIL**, read [references/failure-messages.md](references/failure-messages.md) for the rule, open
   `crops/<testID>.png`, the reference `.layout.json` and, for a gap inside an element, the mockup's
   CSS; fix the first failing rule of each run in the app code, rebuild (or swap the bundle on iOS), run
   step 7 again. [references/what-exact-means.md](references/what-exact-means.md) explains every gate.
9. **On PASS, look.** Follow [references/signoff-and-waivers.md](references/signoff-and-waivers.md):
   read `sheet.png`, every `zoom-*.png` and every `eye-*.png` of every run, answer the seven eye checks,
   fix every visible difference. A difference the app cannot fix becomes a waiver (its class and why),
   reported to the reviewer.
10. **Record and prove.** For each run, `node ${CLAUDE_SKILL_DIR}/scripts/check-signoff.mjs . --draft
    <run-dir>` prints the ledger entry dated today (after a rebuild add `--from-ledger`); complete it in
    `design/parity/signoff.json`. Then run `check-signoff.mjs . --screen <id>` until `RESULT: PASS`.
    [examples/worked-loop.md](examples/worked-loop.md) shows the whole loop.
11. **Report** per frame: the reference used, the runs that pass, what was checked by eye, every waiver
    with its class and reason, every intended reference change, open questions, and the dark RTL
    `sheet.png`; the Design match line names `reports/parity/summary.json`.
12. **Clean up:** shut down this session's own devices by UDID or serial, never another one.

## Definition of done

- [ ] `contracts/visual-parity.json` lists the app's themes, languages and devices, and every design
      frame is a screen-contract state with a reference.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-mockup.mjs .` prints `RESULT: PASS`, and
      `shoot-design.mjs . --check` passes (it needs Playwright and Google Chrome).
- [ ] `run-parity.mjs` passed every frame of the screen on every device, theme and language (never a
      narrowed set), at every planned scroll offset, against the reference the facts select, with no
      tolerance, mask or reference changed.
- [ ] Every sheet image of every run was read; the ledger has an entry for each run's current sheet
      with all seven eye checks answered and no open difference.
- [ ] Every waiver names one element, one rule and its class, gives the reason and the reviewer-report
      date, and is in the report.
- [ ] Allowed SKIP lines of check-harness.mjs, only before the owning skill adopted its file:
      `SKIP src/test-only-entry.ts [harness-not-exported] not yet created (debug-menu-and-test-hooks creates it)`
      (and `[harness-not-wired]`), `SKIP contracts/architecture.json [harness-test-only-folder] not yet created (architecture-and-boundaries creates it)`,
      `SKIP quality-gates.json [gated-paths] not yet created (quality-gates creates it)`.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-harness.mjs .` prints `RESULT: PASS`.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-signoff.mjs . --screen <id>` prints `RESULT: PASS`

## Anti-patterns

- **Judging a screen by one whole-screen percentage or SSIM.** Correct builds and real defects score
  the same; only the per-element gates and the look decide.
- **Re-rendering the references, adding a mask or loosening a number after a failure.** Fix the app;
  ask the reviewer when the design itself seems wrong.
- **A screenshot from the everyday simulator, a Debug build, `simctl openurl` or manual navigation.**
  Wrong geometry, dev overlays, an "Open in ...?" alert, a state that is almost right.
- **The testID on the inner Text of a button.** Maestro lists only the Pressable: `missing`.
- **Un-hiding a decorative icon so Maestro lists it.** Screen readers would read decoration; the
  contract already judges hidden parts by their cover's crop.
- **Signing off after reading only `sheet.png`.** Icons, radii and shadows show in the zoom bands and
  eye pages; the ledger demands every image.
- **A waiver for "close enough".** A waiver is for what the platform cannot draw; anything else is a fix.
- **A capture-only branch** (`if (isParityRun)`) in a view or a model, or a parity-only layout. Open the
  state through `useFrameStateOpener` and the real handler; hold motion through `useReduceMotion()`.
- **Fixing several rules at once.** A wrong padding moves everything below it; fix the first failing
  element from the top, then run again.
- **Hand-writing the harness or editing the fixture.** Copy the templates; the fixture is the design's.
- **Nudging glyphs to pass `text-ink`.** A translate or padding breaks the boxes that match; rule out a
  type-role mismatch first, and measure the role when its floor is unknown.
- **Copying the reference in as `app.png`.** `not-a-capture`, and it proves nothing.
- **Signing off a narrowed set,** or one device only. The done set is every device, theme and language.
- **Sharing a device or a driver port with another session, or `simctl ... booted`.** Name your own
  device, let the scripts pick a free port, trust the nonce check.
- **Hand-drawing a reference variant.** Variants are derived from the rendered mockup by the contract's
  `derive`.
- **A mockup loading fonts from the web, or `system-ui` for an app that bundles its own font.** The
  outlines differ and every text run fails.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/contract-format.md](references/contract-format.md) | The parity contract, device profiles, the fixture, rn-skills.config keys | Workflow steps 1-2 |
| [references/mockup-and-references.md](references/mockup-and-references.md) | Mockup conventions, rendering, frame kinds, variants, masks, when references change, the change log | Workflow steps 2-3 and 5 |
| [references/parity-harness.md](references/parity-harness.md) | The app side: the launch contract, templates, appliers, openers, markers, wiring, testIDs, React Navigation appendix | Workflow step 4; a frame not reached |
| [references/devices-and-capture.md](references/devices-and-capture.md) | iOS simulator and Android emulator setup, launching into a frame, probes, screenshots, Maestro bounds, the nonce, bundle swap | Workflow steps 6-7; capture problems |
| [references/what-exact-means.md](references/what-exact-means.md) | The gates, their measured tolerances, text ink, measuring type-role floors, what only a look proves | Workflow step 8; when a tolerance seems wrong |
| [references/signoff-and-waivers.md](references/signoff-and-waivers.md) | Reading the sheets, the done set, the ledger, waivers, known platform causes, the summary and the report | Workflow steps 9-11 |
| [references/failure-messages.md](references/failure-messages.md) | Every rule id of every script: meaning, real cause, fix | Any FAIL line |
| `templates/contracts/visual-parity.json` | The contract, filled for the demo Tasks app | Workflow step 2 (copy) |
| `templates/contracts/visual-parity.schema.json` | Its JSON Schema | Workflow step 2 (copy beside it) |
| `templates/design/parity/devices/` | Device profiles: `iphone-16-pro.json`, `android-parity.json` | Workflow step 2 (copy) |
| `templates/design/parity/mockup/index.html` | The demo mockup (3 frames, light/dark, en/ar) showing the conventions | Workflow step 2 |
| `templates/design/parity/fixture.json` | The design's data in every language | Workflow step 2 (copy) |
| `templates/design/parity/waivers.json` | An empty waiver file | Workflow step 2 (copy) |
| `templates/design/parity/signoff.json` | An empty sign-off ledger | Workflow step 2 (copy) |
| `templates/src/features/parity/` | The test-only harness: plans, parser, fixture, session, launch, launch root, frame root, error screen, launch reader and bridge, each with its test | Workflow step 4 (copy) |
| `templates/src/hooks/use-frame-request.tsx` | Production: the frame request (`FrameRequestProvider`, `useFrameRequest`) | Workflow step 4 (copy) |
| `templates/src/hooks/use-frame-request.test.tsx` | Its test | Workflow step 4 (copy) |
| `templates/src/hooks/use-frame-state-opener.ts` | Production: the model's frame-state opener (one hook per file) | Workflow step 4 (copy) |
| `templates/src/hooks/use-frame-state-opener.test.tsx` | Its test | Workflow step 4 (copy) |
| `templates/src/hooks/use-frame-scroll-target.ts` | Production: a tall frame's scroll offset | Workflow step 4 (copy) |
| `templates/src/hooks/use-frame-scroll-target.test.tsx` | Its test | Workflow step 4 (copy) |
| `templates/src/ui/parity-launch-marker.tsx` | Production: the launch marker for the parity root and every modal root | Workflow step 4 (copy) |
| `templates/src/ui/parity-launch-marker.test.tsx` | Its test | Workflow step 4 (copy) |
| [examples/screens.json](examples/screens.json) | Shape: screen-contracts' `contracts/screens.json` with a `reference` on each design-frame state and `checks` on compared elements | Workflow step 2 |
| [examples/parity-route.tsx](examples/parity-route.tsx) | Shape: the launch route `src/app/(debug)/debug/parity.tsx` | Workflow step 4 |
| [examples/create-root-kits-parity.ts](examples/create-root-kits-parity.ts) | Shape: the parity kit registered among the test build's kits in the app's root-kit registry | Workflow step 4 |
| [examples/test-only-entry-additions.ts](examples/test-only-entry-additions.ts) | Shape: the entry's harness exports | Workflow step 4 |
| [examples/parity-launch-screen.tsx](examples/parity-launch-screen.tsx) | Shape: the app's test-only screen that builds the appliers (consent hold, switches, repositories, settings target) and renders the launch | Workflow step 4 |
| [examples/model-opener.ts](examples/model-opener.ts) | Shape: a model that opens its frame state and passes the scroll target | Workflow step 4 |
| [examples/worked-loop.md](examples/worked-loop.md) | The whole loop for one screen, with outputs | First time through the loop |
| `scripts/check-mockup.mjs` | Contracts and mockup agree, statically | Workflow steps 1-2 |
| `scripts/shoot-design.mjs` | Renders references (`--update-reference`), proves them (`--check`), renders for a look (`--out`) | Workflow step 3 |
| `scripts/check-harness.mjs` | The app side of parity | Workflow steps 1 and 4 |
| `scripts/setup-parity-device.mjs` | Creates, boots and pins this session's simulator or emulator; `--check` | Workflow step 6 |
| `scripts/capture-app.mjs` | One capture: launch into the frame, still screenshot, Maestro bounds, run.json | Called by run-parity; alone for one run |
| `scripts/check-parity.mjs` | The per-element gates; writes report.json | Called by run-parity; alone to check again |
| `scripts/make-sheet.mjs` | sheet.png, zoom bands, failing-element crops, eye pages | Called by run-parity; alone after a check |
| `scripts/run-parity.mjs` | Capture, check and sheets for every frame x theme x language on one device | Workflow step 7 |
| `scripts/check-signoff.mjs` | Definition of done per screen; `--draft` prints a ledger entry; writes the summary | Workflow step 10 |
| `scripts/selftest.mjs` | Proves every script on good and planted-defect fixtures | After changing a script |
| `scripts/lib/` | Contract, gates, pixel difference, images, hierarchy, runs and waivers, reference changes, device tools, rendering, mockup reader, self-test scenes; synced helpers (do not edit those) | Never directly |
| `scripts/check-lib.mjs` | Shared script library, synced (do not edit here) | Never by hand |
| `scripts/package.json` | The one pin: playwright 1.63.0 (only shoot-design.mjs uses it) | Workflow step 3 (`npm ci --prefix`) |
| `scripts/package-lock.json` | Its lockfile | Never by hand |
| `assets/shared.json` | Declares the shared files this skill copies in | When adding a shared file |
| `tests/bases/` | The self-test apps: the demo contracts, scene-drawn frames, a wired harness | When the self-test base changes |
| `tests/fakes/` | Fake xcrun, adb, emulator tools, maestro and clock for the self-test | When a device script changes |
| `tests/fixtures/` | Good, pass, planted-bad and error cases for every script (overlay format) | When adding a rule |

## Related skills

- `screen-contracts` - the screens, states, testIDs and screenshot reach this skill checks.
- `ui-component-library` - the components whose parts the gates measure; as-rendered border widths.
- `design-system-structure` - tokens and fonts; a `fill` or `text-ink` failure usually points there.
- `icons-app-icon-and-splash` - icons and pictures the eye checks look at.
- `rtl-and-direction` - the mirroring rules behind the `direction` eye check.
- `debug-menu-and-test-hooks` - the test-only gate, the switches and the settings target the launch uses.
- `ios-simulator-build`, `android-emulator-build` - the builds that are captured.
- `e2e-maestro` - installing Maestro and Java 17; the device-binding helper.
- `git-commits-and-reporting` - the Gate-Change trailer and the Design match line.
- `golden-and-snapshot-tests` - pixel goldens of what the app itself renders (canvas, pictures).
