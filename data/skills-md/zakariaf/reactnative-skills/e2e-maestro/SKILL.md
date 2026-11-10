---
name: e2e-maestro
description: Writes and runs Maestro E2E flows on iOS simulators and Android emulators - testID steps, debug-link setup, screenshot baselines. Use when adding a flow or an e2e or screenshots run fails. Not for Jest (unit-and-component-tests).
---

# End-to-end flows with Maestro

The app's wiring is proven on real Release builds: Maestro flows drive the journeys on a simulator
and an emulator the repo owns, a socket sampler proves the app's network policy while they run, the
accessibility flows pass at the largest text size, and every screen is captured per platform, locale
and theme against reviewed baselines. This skill sets up that tooling, writes the flows, runs them,
and its scripts prove the setup, every flow (statically) and each run's reports. Verified on
2026-10-14 with Maestro 2.10.0, Expo SDK 57 (expo 57.0.26), React Native 0.86.3 and Xcode 26.6 with
the iOS 26.5 runtime; the Maestro facts were read in the 2.10.0 jar (re-verify:
references/maestro-setup.md, "Changing the pin"). The templates pass tsc, ESLint and Jest in the
reference app, and on 2026-10-14 the runner, the capture and the report checker ran end to end on a
Release preview build of the reference app: an iOS 26.5 simulator and an Android API 35 emulator,
phone and tablet each. The Android facts were observed on API 35; the default API 36 image is not yet
run end to end. The sampler liveness proof, the per-platform capture folders and the two-link matrix
setup came after that run and are proven by the self-test and Jest only.

## Rules that must hold

1. **Maestro comes only from the pinned installer and runs quietly.** `scripts/e2e/install-maestro.sh`
   downloads 2.10.0, checks its SHA-256, and unzips into the git-ignored `tools/maestro/`; Maestro runs
   with Java 17 and `MAESTRO_CLI_NO_ANALYTICS`, `MAESTRO_CLI_ANALYSIS_NOTIFICATION_DISABLED` and
   `MAESTRO_DISABLE_UPDATE_CHECK` set to `true`. Why: Homebrew and `curl | bash` are unpinned and
   unverified, and by default Maestro sends analytics and checks for updates.
   (`maestro-pin`, `maestro-install-source`, `maestro-env`)
2. **Every Maestro run names its device and a driver port of its own, before the command.**
   `maestro --device <udid or serial> --driver-host-port <free port> test ...`, built by
   `maestroGlobalArgs`; never the per-command `--udid` alone, never port 7001. `simctl` names a UDID,
   `adb` gets `-s <serial>`, and the devices are the repo's own `<prefix>-<purpose>`. Why: on a shared
   machine the default driver port answered from another session's simulator.
   (`maestro-device`, `shared-device`, `run-command-device`)
3. **Flows run only through the runner, on a Release build of a test variant with ads off.**
   `npm run e2e:ios` and `npm run e2e:android` refuse a Debug build (no embedded bundle: Metro's
   WebSocket hides the app's traffic), the production variant (no debug link) and a build whose
   `expo.extra` misses `contracts/e2e.json` `buildExtra` (`adsMode: off` for an app with ads: an
   ads-on build shows the consent form over every cleared launch and its ad SDK opens sockets).
   Evidence is the full run: no tag filter, the large-text step included. (`runner-build-guard`,
   `e2e-ads-off`, `runner-steps`, `run-record`, `run-filtered`)
4. **Select elements by `id:` only, with ids from the contracts.** `contracts/screens.json`
   (screen-contracts) plus `contracts/e2e.json` `extraTestIDs`; text only for OS-owned UI under a
   `# system-ui: <why>` comment; never a crop-only part (inside an accessible element, or hidden from
   screen readers). Why: the flow then runs in every locale on both platforms, and an unknown id fails
   in a second instead of after a 15 s timeout. (`text-selector`, `testid-format`, `unknown-testid`,
   `unreachable-testid`, `no-testid-step`)
5. **State comes from a cleared launch and one debug link per setup.** Each flow starts with
   `launchApp: { clearState: true }`; state is set only through `subflows/debug-setup.yaml`
   (debug-menu-and-test-hooks' `<scheme>://debug/setup?...`), whose query ends on the screen it opens
   (`open=`) and waits for that screen's testID. A language that can flip the layout direction goes
   alone, first, through `subflows/set-language.yaml` (the launch link; it waits out the restart). No
   `openLink` in flows, no tapping through menus; the one tap is the control under test. Why: setting
   up through the UI is slow and flaky, waiting for the start screen passes with a lost link, and a
   direction restart drops the rest of a link. (`first-step-launch`, `raw-open-link`, `debug-query`,
   `debug-open`, `debug-lang-alone`)
6. **iOS's "Open in …?" alert is accepted by its title, and tools never use `simctl openurl`.** Guard
   on `'Open in .*\?'` and tap `Open` below it with `optional: true`. Why: Maestro's text match ignores
   case, so a bare `'Open'` also matches any in-app OPEN button, and `openurl` leaves the alert up so
   the app never gets the link. Android-only steps (`back`, `pressKey: back`, airplane mode) run
   under `runFlow: { when: { platform: Android } }`: iOS skips them silently. (`open-alert-guard`,
   `openurl-prompt`, `platform-guard`)
7. **A flow never sets `APP_ID`, `APP_SCHEME`, `LANG` or `THEME` in `env:`.** Why: in Maestro 2.10
   a flow's `env:` beats `-e`, so every run would silently use the flow's value. (`env-shadows-cli`)
8. **Flows live in `.maestro/flows/<area>/<nn>-<name>.yaml`.** Shared steps in `subflows/`, the matrix
   in `screenshots/`, hand-run flows in declared manual folders. Why: Maestro runs only the top level
   of the folder it is given, so a nested flow never runs and a sub-flow under `flows/` runs alone and
   fails. (`flow-location`, `flow-name`, `subflow-in-flows`, `runflow-missing`, `flow-header`,
   `flow-tags`, `flow-parse`)
9. **No AI commands and nothing that uploads.** `assertWithAI`, `assertNoDefectsWithAI`,
   `extractTextWithAI`, `maestro cloud`, `maestro login`, `test --analyze`, `record` without
   `--local`. Why: they send screenshots or the app to a third party. (`ai-command`, `maestro-upload`)
10. **A flaky flow is a bug.** Wait on ids (`extendedWaitUntil`), never sleep, no `retry:` around app
    steps; a non-smoke flow may be quarantined for 7 days with `# quarantine YYYY-MM-DD: <reason>`, a
    smoke flow never. Why: retries and sleeps hide the races users hit. (`retry-app-assertion`,
    `quarantine-note`, `smoke-quarantine`)
11. **The run proves the network policy at runtime, on its own devices, with live samplers.** One
    sampler per device of the run lists the app's sockets (`lsof` on iOS, `/proc/net` by uid on
    Android); every socket `contracts/e2e.json` `network` does not allow (`offline-only`: any other
    host; `allowlist`: hosts outside `allowHosts`) fails the run, and so does a sampler that did not
    sample until the end or never found the app (`network-samplers.json`). Why: iOS simulators have no
    airplane mode, a JS-only check misses native SDKs, and a dead sampler leaves the same empty report
    as a quiet app. (`e2e-contract`, `runner-network`, `sampler-own-devices`, `sampler-liveness`,
    `network-sampler`, `network-sockets`)
12. **The accessibility flows pass at the largest text size.** `flows/a11y/` runs on the phone and
    the tablet in every `largeText.locales` entry (a left-to-right and, when the app has one, a
    right-to-left locale). Why: clipping and overlap at the largest system size (iOS AX5, about 3.6x in
    React Native; Android font scale 2.0) only show on a device, and each a11y flow sets the locale it
    is given through `set-language.yaml`. (`runner-steps`, `large-text-lang`, `large-text-missing`,
    `large-text-failed`)
13. **Screenshots come only from a still, deterministic screen, with a fixed tolerance.** Status bar
    9:41, animations held (`motion=still`), a fixed day, one device model per baseline set, baselines
    per platform; 0.2 % of pixels at a 0.1 colour distance, never raised. Each capture empties
    `reports/screenshots/<platform>/` first and records a combination that failed instead of stopping.
    Why: an animating screen differed by about 1 % between two captures a second apart, and a shared or
    stale summary passed for another platform or an earlier run. (`deterministic-capture`,
    `screenshot-tolerance`, `capture-evidence`, `matrix-incomplete`, `screenshot-capture-failed`,
    `screenshot-platform`)
14. **Baselines change only on purpose.** `--update` narrowed to the sets a change touched, every new
    or changed PNG and its diff opened, one commit with a `Gate-Change:` trailer. Why: an unread
    baseline freezes a bug for every later run. (`baseline-matrix`, `screenshot-changed`)
15. **Hand-run flows live in declared manual folders the runner never lists.** Flows that need
    production SDK behaviour or a real system prompt sit in `contracts/e2e.json` `manualFolders`; when
    `launchApp` would pre-grant the permission under test they start outside Maestro and never call it.
    Why: `launchApp` grants every permission by default, so the prompt would never show.
    (`manual-folder`, `runner-steps`)

## Workflow

1. **Prerequisites.** Screen testIDs in `contracts/screens.json` (screen-contracts), the debug link and
   `contracts/debug-links.json` (debug-menu-and-test-hooks), Release builds of the preview variant
   (ios-simulator-build, android-emulator-build, or eas-build-and-submit with `--local`), and Java 17.
   If neither `/usr/libexec/java_home -v 17` nor Android Studio's JDK exists, stop and ask the developer.
2. **Install the templates** (line 1 names each repo path): `templates/scripts/e2e/` (with every test),
   `templates/.maestro/` and `templates/contracts/e2e.json` with its schema; fill `productionAppIds`,
   `network`, `largeText` and `screenshots`, and the flows' testIDs (`assets/template-placeholders.json`
   lists what each placeholder stands for). Add the four npm scripts and `/tools/maestro/` to
   `.gitignore`; declare `screenshots` and each manual folder in `contracts/naming.json`
   `extraE2eFolders`. Read [references/maestro-setup.md](references/maestro-setup.md) and
   [references/runner-and-devices.md](references/runner-and-devices.md) the first time. Run
   `npx jest scripts/e2e --ci --maxWorkers=2`, `npm run typecheck` and `npx eslint scripts/e2e --max-warnings 0`.
3. **Check the setup:** `node ${CLAUDE_SKILL_DIR}/scripts/check-e2e-setup.mjs .`; fix every `FAIL`
   (file, rule, fix) and rerun.
4. **Write or change a flow:** read [references/flows.md](references/flows.md); one link per setup,
   ids from the contracts (screen-contracts' `list-screen.mjs` prints a screen's ids), the one tap the
   control under test; a canvas tap follows [examples/canvas-tap-flow.yaml](examples/canvas-tap-flow.yaml).
   Then `node ${CLAUDE_SKILL_DIR}/scripts/check-flows.mjs .`, and once Maestro is
   installed add `--syntax` (Maestro's own `check-syntax`, about 3 s per file).
5. **Run them:** `npm run e2e:ios` and `npm run e2e:android` (`-- --sim <purpose>` for this session's
   own devices, `-- --help` for every option). While iterating, `-- --include-tags smoke
   --skip-large-text` is fine; it is never evidence. Then
   `node ${CLAUDE_SKILL_DIR}/scripts/check-e2e-report.mjs . --platform ios` (and `android`). For a
   failure open `reports/e2e/<platform>/` and rerun that flow alone; a line in `network.txt` is a real
   finding: find the code that opened it ([references/network-proof.md](references/network-proof.md)).
   Open every screenshot under `reports/e2e/<platform>/large-text/`.
6. **Screenshot matrix** (after UI changes, before a release): read
   [references/screenshot-matrix.md](references/screenshot-matrix.md), run `npm run screenshots:ios`
   and `npm run screenshots:android` (each writes `reports/screenshots/<platform>/`), open every changed
   PNG and its diff, then `node ${CLAUDE_SKILL_DIR}/scripts/check-e2e-report.mjs . --platform ios --screenshots`
   (and `android`). Commit new
   baselines with `Gate-Change: <which screens and why>`; before a release add
   `check-e2e-setup.mjs . --baselines`.
7. **Report and clean up:** paste the `evidence:` lines the report checker prints
   ([examples/evidence-report.md](examples/evidence-report.md) shows them), name any
   quarantined flow, and shut down the devices the run started (by UDID or serial, your own only).
   [references/checks.md](references/checks.md) explains every rule and contract key.

## Definition of done

- [ ] Every new flow is in `.maestro/flows/<area>/<nn>-<name>.yaml`, selects by id, sets state through
      `debug-setup.yaml`, and was seen passing on an iOS simulator and an Android emulator.
- [ ] `npx jest scripts/e2e --ci --maxWorkers=2`, `npm run typecheck` and ESLint pass on the tooling.
- [ ] `npm run e2e:ios` and `npm run e2e:android` passed without a tag filter and with the large-text
      step; no smoke flow is quarantined; the large-text screenshots were opened.
- [ ] Every Maestro line of the run log names this session's device and a driver port of its own.
- [ ] After UI changes the matrix ran on both platforms, every changed PNG and diff was opened, and
      every baseline change has a `Gate-Change:` trailer; the tolerance is unchanged.
- [ ] Only `<prefix>-<purpose>` devices were started, each targeted by UDID or serial, and shut down.
- [ ] Allowed SKIP lines: `SKIP contracts/screens.json [unknown-testid] not yet created (screen-contracts creates it)`
      (and `[unreachable-testid]`), `SKIP contracts/debug-links.json [debug-query] not yet created (debug-menu-and-test-hooks creates it)`,
      `SKIP scripts/ios/simulators.ts [runner-file-missing] not yet created (ios-simulator-build creates it)`
      (and `toolchain.ts`), `SKIP scripts/android/adb-args.ts [runner-file-missing] not yet created (android-emulator-build creates it)`;
      `NOT APPLICABLE: the app has no Maestro E2E yet ...` before step 2.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-e2e-report.mjs . --platform ios` and `--platform android` print `RESULT: PASS`.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-e2e-setup.mjs .` prints `RESULT: PASS` (with `--baselines` before a release).
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-flows.mjs . --syntax` prints `RESULT: PASS`

## Anti-patterns

- **`tapOn: 'Add task'` or `assertVisible: 'Tasks'`.** Breaks in every other locale and whenever the
  copy changes. Use `id: 'tasks.add-button'`.
- **Tapping Settings → Language → … to reach a state.** Slow, flaky, and every screen change breaks
  unrelated flows. One debug link that ends on the screen under test.
- **`xcrun simctl openurl` (or `adb -s <serial> shell am start -d` with the URL quoted once) from a
  script.** iOS waits on an alert nobody accepts; the device shell cuts the URL at `&`. Run the
  open-link or debug-setup sub-flow through `runMaestro`.
- **`brew install maestro` or the `curl | bash` installer.** Unknown version, no checksum, analytics
  on. Run `scripts/e2e/install-maestro.sh` (the runner calls it anyway).
- **Running on the booted simulator, on "the only emulator", or on a Debug build.** Another session's
  device breaks, and Metro's socket makes the network proof meaningless.
- **An `env:` block with `APP_ID` "so the flow runs on its own".** It overrides `-e`; pass
  `-e APP_ID=... -e APP_SCHEME=...` when running one flow by hand.
- **`retry:` or a longer timeout to make a red flow green.** Hides the race users hit. Wait on the id
  that proves the state, or fix the app.
- **`--update` for every set, or a bigger `MAX_DIFF_RATIO`, to clear a diff.** Accepts regressions
  nobody looked at. Open the diff, fix the screen, update only what you meant to change.
- **`assertNoDefectsWithAI` for "visual QA".** It uploads screenshots. Open the PNGs.
- **Adding a host to `allowHosts` to silence `network.txt`.** Find who opened the socket first; a new
  host is a privacy declaration change (privacy-and-store-declarations), agreed with the reviewer. An
  ad network's host never goes there: the E2E build has ads off (`buildExtra`).
- **Trusting an empty `network.txt` on its own.** A sampler that crashed or never matched the app
  leaves it empty too; the evidence is `network-samplers.json` with every device alive to the end.
- **`lang=${LANG}&theme=...&open=...` in one link.** In the right-to-left locale the app restarts and
  the rest is lost; run `set-language.yaml` first.
- **A shared sub-flow under `flows/`, or a flow two folders deep.** One runs alone and fails, the
  other never runs.
- **Tapping a row right after `scrollUntilVisible`.** A tap while the list still glides only stops it;
  `waitForAnimationToEnd` first.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/maestro-setup.md](references/maestro-setup.md) | The pin, the installer, the quiet environment, device and driver port on both platforms, verified and banned commands, `check-syntax`, changing the pin | Workflow step 2, an install or command failure |
| [references/runner-and-devices.md](references/runner-and-devices.md) | What a run needs, the runner's steps, the build guard, iOS simulators and Android emulators, large text, reports, failures | Workflow steps 2 and 5 |
| [references/flows.md](references/flows.md) | Folders, names, headers and tags, id selectors, the debug-link setup, sub-flows, waits, canvas taps, manual folders, quarantine, what a flow should not prove | Workflow step 4 |
| [references/network-proof.md](references/network-proof.md) | The three network modes, how each platform's sampler works, reading `network.txt` | Workflow step 5, a network finding |
| [references/screenshot-matrix.md](references/screenshot-matrix.md) | Still screens, running the matrix, baselines per platform, review, the gallery, the large-text pass | Workflow step 6 |
| [references/checks.md](references/checks.md) | `contracts/e2e.json` keys, every checker rule with its reason, SKIP and NOT APPLICABLE lines, when multi-package | A `FAIL` line, editing the contract |
| [examples/canvas-tap-flow.yaml](examples/canvas-tap-flow.yaml) | A flow that taps a Skia canvas cell from the canvas layout probe | Writing a canvas flow |
| [examples/evidence-report.md](examples/evidence-report.md) | The evidence lines of a passing run, as a report shows them | Workflow step 7 |
| `templates/scripts/e2e/install-maestro.sh` | Pinned, checksum-verified, idempotent installer | Workflow step 2 |
| `templates/scripts/e2e/run-e2e.ts` | `npm run e2e:<platform>`: build guard, flows, large text, samplers, `run.json` | Workflow step 2 |
| `templates/scripts/e2e/e2e-cli.ts` | The runner's command line, pure (+ test) | Workflow step 2 |
| `templates/scripts/e2e/e2e-config.ts` | Reads `contracts/e2e.json` with valibot, defaults filled (+ test) | Workflow step 2 |
| `templates/scripts/e2e/e2e-device.ts` | The device interface both platforms implement | Workflow step 2 |
| `templates/scripts/e2e/build-guard.ts` | Release, test-variant and `buildExtra` (ads off) check from the build's embedded config (+ test) | Workflow step 2 |
| `templates/scripts/e2e/ios-device.ts` | An iOS simulator by UDID: boot, install, status bar, text size, appearance (+ test) | Workflow step 2 |
| `templates/scripts/e2e/android-device.ts` | An Android emulator by serial: AVD, boot, demo mode, font scale, night mode (+ test) | Workflow step 2 |
| `templates/scripts/e2e/open-device.ts` | Opens the build and the device of one platform | Workflow step 2 |
| `templates/scripts/e2e/maestro-run.ts` | `runMaestro`, the quiet environment, `appEnv`, `debugSetupArgs` (+ test) | Workflow step 2 |
| `templates/scripts/e2e/maestro-args.ts` | `maestroGlobalArgs`, `freeDriverPort`, `driverPortFor`, `maestroRunLine` (synced; do not edit here) | Workflow step 2 |
| `templates/scripts/e2e/maestro-args.test.ts` | Its test (synced; do not edit here) | With maestro-args |
| `templates/scripts/e2e/network-sampler.ts` | Pure socket parsing for both platforms and the policy judge (+ test) | Workflow step 2 |
| `templates/scripts/e2e/sample-sockets.ts` | The sampler process, one per device of a run; rewrites its status after every sample | Workflow step 2 |
| `templates/scripts/e2e/sampler-evidence.ts` | The liveness proof: `trackSampler`, `proveSamplersAlive`, `network-samplers.json` (+ test) | Workflow step 2 |
| `templates/scripts/e2e/capture-screenshots.ts` | `npm run screenshots:<platform>`: capture, compare, `capture-failed` rows, `reports/screenshots/<platform>/` summary and gallery | Workflow step 2 |
| `templates/scripts/e2e/screenshots-cli.ts` | Its command line, pure (+ test) | Workflow step 2 |
| `templates/scripts/e2e/screenshot-compare.ts` | One screenshot against its baseline, the gated tolerances | Workflow step 2 |
| `templates/scripts/e2e/png-diff.ts` | Zero-dependency PNG decode, colour distance and diff image (+ test) | Workflow step 2 |
| `templates/scripts/e2e/write-gallery.ts` | The baseline / run / diff gallery (+ test) | Workflow step 2 |
| `templates/scripts/e2e/` | The modules above with their `*.test.ts` files | Workflow step 2 |
| `templates/.maestro/subflows/` | `open-link.yaml`, `debug-setup.yaml`, `shoot-screen.yaml`, `set-language.yaml` (a language alone, as the launch link), `airplane-mode.yaml` (optional: real airplane mode on Android) | Workflow step 2 |
| `templates/.maestro/screenshots/matrix.yaml` | The capture flow: the language alone, then the rest, then one `runFlow` per screen | Workflow steps 2 and 6 |
| `templates/.maestro/flows/` | A smoke flow and an offline journey that survives a kill | Workflow steps 2 and 4 |
| `templates/contracts/e2e.json` | The app's E2E facts | Workflow step 2 |
| `templates/contracts/e2e.schema.json` | Its schema: every key, its meaning and default | Editing the contract |
| `assets/template-placeholders.json` | What each template placeholder stands for (the reference Tasks app's values) | Workflow step 2 |
| `assets/shared.json` | The synced-file manifest | When a shared file is added |
| `scripts/check-flows.mjs` | Checks every flow statically (30 rules) | Workflow step 4, definition of done |
| `scripts/check-e2e-setup.mjs` | Checks the tooling, contract, scripts and baselines (22 rules) | Workflow step 3, definition of done |
| `scripts/check-e2e-report.mjs` | Checks one run's reports, the samplers' liveness and one platform's capture, and prints the evidence lines (13 rules) | Workflow steps 5-6, definition of done |
| `scripts/lib/e2e-repo.mjs` | Layout, adoption, the contracts and the known testIDs | Never by hand |
| `scripts/lib/flow-rules.mjs` | The per-file flow rules | Never by hand |
| `scripts/lib/maestro-yaml.mjs` | Zero-dependency Maestro YAML reader with line numbers | Never by hand |
| `scripts/lib/maestro-spawns.mjs` | The `maestro-device` spawn rule (synced; do not edit here) | Never by hand |
| `scripts/check-lib.mjs` | Shared checker library (synced; do not edit here) | Never by hand |
| `scripts/selftest.mjs` | Proves the three checkers against `tests/fixtures/` | After changing a checker or a template |
| `tests/bases/` | The small app and report trees the cases start from | When adding a fixture |
| `tests/fixtures/` | Overlay cases: good (the templates), a bad case per rule, pass and error cases | When adding a rule |

## Related skills

- `screen-contracts` - the testIDs flows select by (`contracts/screens.json`).
- `debug-menu-and-test-hooks` - the debug link, its contract and the simulated clock and network.
- `ios-simulator-build` and `android-emulator-build` - the Release builds the runner tests, and the device kits it imports (`scripts/ios/`, and `adbArgs` from `scripts/android/adb-args.ts`).
- `eas-build-and-submit` - local EAS builds of the preview profile.
- `naming-conventions` - testID and flow-file names, `extraE2eFolders`.
- `golden-and-snapshot-tests` - the baseline policy screenshots share with pixel goldens.
- `run-goldens-rebaseline` - regenerating every baseline after a runtime, Xcode or design-wide change.
- `privacy-and-store-declarations` - what the network policy declares to the stores.
- `accessibility-as-code` and `rtl-and-direction` - the large-text and language-switch flows.
- `performance-budgets` - simulator and emulator cold-start and memory runs.
- `unit-and-component-tests` - everything a flow should not have to prove.
- `git-commits-and-reporting` - the Gate-Change trailer and the evidence report.
