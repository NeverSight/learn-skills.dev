---
name: ios-simulator-build
description: Builds Release iOS simulator apps (clean prebuild, pinned Xcode, UDID-named simulator) and proves the .app. Use when smoke-testing on the iOS simulator, or xcodebuild, simctl or CocoaPods fails. Not for TestFlight (ios-release-testflight).
---

# iOS simulator build

Turns the Expo app into a Release simulator app with one command, `npm run build:ios:sim -- --variant preview`, and proves what was built: the pinned Xcode made it, the variant is the one asked for (test-only code present in development and preview, absent in production), and the app starts and draws on a simulator this repo owns. No Xcode GUI, no Metro, no signing. Verified on 2026-10-04 with Expo SDK 57 (expo 57.0.26), React Native 0.86.3, Xcode 26.6 and the iOS 26.5 simulator runtime; the Android twin is `android-emulator-build`.

## Rules that must hold

1. **Every simulator build runs through one script and starts from a clean prebuild.** `scripts/build/build-ios-sim.ts` preflights every npm script it will run (exit 2, nothing built), then `npx expo prebuild --platform ios --clean`, the contract's post-prebuild scripts, xcodebuild, install, launch and screenshot. Why: `ios/` is generated (Continuous Native Generation, owned by `expo-prebuild-and-config-plugins`) and a stale `ios/` from another variant builds the wrong identity; a missing audit script must stop the run before the slow, destructive prebuild.
2. **Xcode is selected by version through `DEVELOPER_DIR`, per process; never `xcode-select` or `sudo`.** `scripts/ios/toolchain.ts` pins `XCODE_VERSION` and `IOS_RUNTIME`; `selectXcode()` picks the matching `/Applications/Xcode*.app` and asserts `xcodebuild -version`. Why: a Mac often holds several Xcodes (the newest is the one named `Xcode.app`), and one global switch needs a password and changes every build on the machine.
3. **The variant is exported once, for the whole run.** `variantEnv(variant)` from `src/config/app-variant.ts` sets `APP_VARIANT` = `EXPO_PUBLIC_APP_VARIANT` on the one environment every step gets. Why: the variant enters the binary three times, each in its own process: prebuild (Info.plist), the Constants build phase (`EXConstants.bundle/app.config`) and Metro (the JS bundle); a lost variable silently mixes variants.
4. **Metro's cache is keyed on the public values before any Release build.** `metro.config.js` sets `cacheVersion` from the `EXPO_PUBLIC_*` values (the key and its proof belong to `app-variants-and-environment`). Why: this build runs with `CI=1`, and `@expo/cli` then skips `--reset-cache` in the Release bundling phase, so without the key a production build made after a preview build can ship the preview bundle.
5. **The simulator build is Release, for the simulator SDK, on one UDID, unsigned.** `-configuration Release -sdk iphonesimulator -destination id=<udid> ONLY_ACTIVE_ARCH=YES ARCHS=arm64 CODE_SIGNING_ALLOWED=NO`, DerivedData in `build/ios-sim/dd`. Why: Release embeds the Hermes bundle users run; `expo start`, `expo run:ios` and Debug builds load JS from Metro with a dev menu, and no signing material is ever touched.
6. **Simulators are named `<prefix>-<purpose>`, created once on the pinned runtime and targeted only by UDID.** Only prefixed simulators are shut down, erased or deleted, one at a time, never `all` or `booted`; Maestro runs pass `--device <udid>` and their own driver port; Android tooling passes `adb -s <serial>` and starts emulators with `-avd <name>`. Why: several sessions, agents and CI jobs share a Mac, and an implicit device reaches someone else's.
7. **Every tooling process runs with `EXPO_NO_TELEMETRY=1` and `CI=1`.** Why: no telemetry, and no interactive prompt that would hang an unattended run.
8. **Wait on a signal, never a fixed sleep; then check the screenshot and look at it.** The ready signal is the contract's `readyMarker` file in the app's data container, else two identical screenshots after at least 3 s. Why: a build that "succeeded" can still launch to a black, white or empty screen; only the picture shows it.
9. **The built `.app` proves its variant.** `check-sim-app` reads the artifact: the pinned Xcode (`DTXcode`), the simulator platform, the test-only sentinel (present in development and preview, absent in production), Info.plist and `EXConstants` agreeing on the variant's bundle id, usage strings in every language, the privacy manifest, no ATS exception, and for production no placeholder, no test artefact and the encryption flag. Why: `** BUILD SUCCEEDED **` says nothing about what shipped inside.
10. **A change to variants, Metro, test-only code or the build tooling is proven by a preview build and a production build made back to back, without clearing any cache.** Why: only that order shows a missing cache key or a broken gate.
11. **Human steps are asked for, never worked around.** Installing Xcode, accepting its licence and its first-launch setup need `sudo` and an admin password; the agent stops and asks. Why: a workaround (another Xcode, `xcode-select`) builds with the wrong SDK and hides the problem.
12. **Generated and output folders stay out of git:** `ios/`, `android/`, `build/` and `reports/`. Why: prebuild regenerates the native folders, `build/` holds DerivedData and logs, `reports/` the screenshots.

## Workflow

1. **First time in a repo, or after a setup check fails:** read [references/environment-and-xcode.md](references/environment-and-xcode.md) (toolchain, human steps, Xcode selection, the Xcode 27 move) and [references/build-variants.md](references/build-variants.md) (the three moments, the Metro trap, what proves a variant).
2. **Install the templates that are missing** (line 1 of each names its repo path; fill `__SIMULATOR_PREFIX__` and `__APP_ID__` in the contract):

   | Template | Goes to |
   |---|---|
   | `templates/scripts/ios/toolchain.ts` + test (canonical) | `scripts/ios/` |
   | `templates/scripts/ios/simulators.ts` + test | `scripts/ios/` |
   | `templates/scripts/build/*.ts` (+ tests) | `scripts/build/` |
   | `templates/scripts/e2e/maestro-args.ts` + test | `scripts/e2e/` (e2e-maestro owns it; skip when present) |
   | `templates/contracts/ios-sim-build.json` + `.schema.json` | `contracts/` |
   | `templates/src/config/app-variant.ts` + test (canonical) | `src/config/` (skip when present) |

   Add `"build:ios:sim": "node scripts/build/build-ios-sim.ts"` to `package.json`, check the `.gitignore` lines (rule 12), and run `npm run typecheck`, `npx eslint scripts --max-warnings 0` and `npx jest scripts --ci --maxWorkers=2`. Metro's cache key comes from `app-variants-and-environment`; post-prebuild scripts (a privacy-manifest audit) go into the contract's `postPrebuild`.
3. **Check the setup:** `node ${CLAUDE_SKILL_DIR}/scripts/check-sim-setup.mjs .`. Fix every `FAIL` (each names the file, the rule and the fix) and rerun until `RESULT: PASS`. [references/contract-and-checks.md](references/contract-and-checks.md) explains every rule and contract key.
4. **Build and run:** `npm run build:ios:sim -- --variant preview` (`--help` prints the options; `--sim <purpose>` picks another simulator; `--link <path> --wait-for <testID>` also screenshots a deep-linked screen through a Maestro sub-flow, because `simctl openurl` leaves iOS's "Open in ...?" prompt up). Read [references/simulator-commands.md](references/simulator-commands.md) when a step fails, when you run a step by hand, or before changing the script. The run prints the `.app` path and the screenshot path.
5. **Prove the build:** `node ${CLAUDE_SKILL_DIR}/scripts/check-sim-app.mjs . --app <printed .app path> --variant preview`, then `node ${CLAUDE_SKILL_DIR}/scripts/check-screenshot.mjs reports/ios-sim/`, then open the PNG and look at it (the intended screen, text drawn, no alert, no notification banner, no blank area).
6. **When the change touches variants, `metro.config.js`, test-only code or the build tooling:** run `--variant production` right after the preview build without clearing any cache, and `check-sim-app.mjs` on both. [examples/variant-proof.md](examples/variant-proof.md) shows the commands and the output.
7. **EAS or Android:** an EAS simulator build (`ios.simulator: true`) is checked the same way after extracting its `.app`; the Android emulator build is `android-emulator-build`. Both lanes are in [references/eas-and-android.md](references/eas-and-android.md).
8. **On any failure**, match the text in [references/failures.md](references/failures.md), fix the cause (never the check), rerun the failing step, then the checks. Stop and ask the developer for anything that needs a password.
9. **Report** in plain words: variant, simulator name and model, the `.app` and screenshot paths, what the screenshot shows, every SKIP line, and the three `RESULT` lines. Shut down this session's simulators by UDID at the end.

## Definition of done

- [ ] `npm run build:ios:sim -- --variant <v>` ran from a clean prebuild and printed `ready (...)` with a screenshot path.
- [ ] The screenshot was opened and looked at, and shows the intended screen (not black, white, empty or covered by an alert).
- [ ] For variant, Metro, test-only or tooling changes: a preview and a production build made back to back both pass `check-sim-app.mjs`.
- [ ] Only `<prefix>-<purpose>` simulators were created or touched, each by its UDID; no `xcode-select`, `sudo`, `booted` or `all` anywhere; this session's simulators are shut down.
- [ ] Expected SKIP line only: `SKIP src/test-only.ts [test-code] not yet created (debug-menu-and-test-hooks creates it)` while the app has no test-only gate.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-sim-app.mjs . --app <app> --variant <v>` and `node ${CLAUDE_SKILL_DIR}/scripts/check-screenshot.mjs reports/ios-sim/` print `RESULT: PASS`.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-sim-setup.mjs .` prints `RESULT: PASS`

## Anti-patterns

- **Opening `ios/` in Xcode to fix a build setting.** The next prebuild erases it; put the setting in `app.config.ts` or a config plugin.
- **`sudo xcode-select -s /Applications/Xcode.app` because "xcodebuild picked the wrong one".** Pass `DEVELOPER_DIR` from `selectXcode()`; installing and licensing Xcode is the developer's step.
- **`APP_VARIANT=production npx expo prebuild`, then `xcodebuild` in a fresh shell.** The Constants phase and Metro see no variant; export once and keep one environment.
- **`npx expo start`, `npx expo run:ios` or a Debug build to "check quickly".** Metro, the dev menu and LogBox are not what users run, and `run:ios` builds on whatever Xcode `xcode-select` points at.
- **`sleep 10 && xcrun simctl io <udid> screenshot ...`.** Too short on a cold Mac, wasted time on a warm one; poll the ready signal.
- **`xcrun simctl shutdown all`, `erase all` or any command with `booted`.** Shut down or delete only your own `<prefix>-<purpose>` simulator, by UDID.
- **`eas build:run -p ios --latest` without `--simulator <udid>`.** It installs on the first booted simulator, which may be another session's.
- **Declaring success from `** BUILD SUCCEEDED **`.** Launch, screenshot, check and look.
- **Deleting a post-prebuild script because the preflight stopped the first build.** Install the tooling it runs; the audit is what keeps an undeclared required-reason API out of the build.
- **`npx expo export --clear` or deleting `$TMPDIR/metro-cache` to fix a stale variant.** It hides the missing cache key until the next build; key `cacheVersion` on the public values.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/environment-and-xcode.md](references/environment-and-xcode.md) | Toolchain versions, human steps, Xcode selection, tool environment, the Xcode 27 move with scene support, `.gitignore`, disk space | Workflow step 1, and when Xcode or the Mac changes |
| [references/build-variants.md](references/build-variants.md) | The three variants on a simulator, the three moments, the Metro cache trap under `CI=1`, the test-only sentinel, the evidence `check-sim-app` reads, the back-to-back proof | Workflow steps 1 and 6 |
| [references/simulator-commands.md](references/simulator-commands.md) | Every command of the run with its flags, simulator models and sizes, the ready signal, verified pitfalls, other simctl commands, timings | Workflow step 4, and when running a step by hand |
| [references/contract-and-checks.md](references/contract-and-checks.md) | The contract keys, the `rn-skills.config.json` keys, every checker rule with its reason, when multi-package | Workflow step 3, and when a check fails |
| [references/eas-and-android.md](references/eas-and-android.md) | The EAS simulator lane (profiles, `--local`, `build:run --simulator`) and the Android counterpart of every step | Workflow step 7 |
| [references/failures.md](references/failures.md) | Symptom, cause and fix for environment, prebuild, xcodebuild, variant, simulator and screenshot failures | Workflow step 8, whenever something fails |
| [examples/variant-proof.md](examples/variant-proof.md) | A real preview build of the reference Tasks app: timings, the checker output, a real finding, the production step and the report | Workflow steps 5 and 6 |
| `templates/scripts/ios/toolchain.ts` | The Xcode pin, `selectXcode()`, `toolEnv()`, `xcodeBuildNumber()` (synced from the library; do not edit here) | Workflow step 2 |
| `templates/scripts/ios/toolchain.test.ts` | Its tests (synced; do not edit here) | With the toolchain |
| `templates/scripts/ios/simulators.ts` | `<prefix>-<purpose>` simulators: create, warm up, boot, status bar, install, launch, own-only shutdown and delete | Workflow step 2 |
| `templates/scripts/ios/simulators.test.ts` | Its tests | With the simulators module |
| `templates/scripts/build/build-ios-sim.ts` | The CLI behind `npm run build:ios:sim` | Workflow step 2 |
| `templates/scripts/build/build-steps.ts` | Its side effects: logged steps, workspace, plist values, stale DerivedData, package.json kept clean, the ready poll | Workflow step 2 |
| `templates/scripts/build/sim-build-args.ts` | The command line, parsed with the app's variant resolver | Workflow step 2 |
| `templates/scripts/build/sim-build-config.ts` | The contract reader (valibot), defaults filled | Workflow step 2 |
| `templates/scripts/build/sim-build-plan.ts` | Prebuild and xcodebuild arguments, paths, the preflight, the `--link` Maestro line | Workflow step 2 |
| `templates/scripts/build/derived-data.ts` | Stale DerivedData detection (a copied or moved repo) | Workflow step 2 |
| `templates/scripts/build/ready-signal.ts` | When the launched app counts as ready | Workflow step 2 |
| `templates/scripts/build/` | The build modules above and the tests of the pure ones (`*.test.ts` beside each) | Workflow step 2 |
| `templates/scripts/e2e/maestro-args.ts` | `maestroGlobalArgs`, `freeDriverPort`, `driverPortFor`, `maestroRunLine` (synced from the library; do not edit here) | Workflow step 2, when the repo has none |
| `templates/scripts/e2e/maestro-args.test.ts` | Its tests (synced from the library; do not edit here) | With maestro-args |
| `templates/contracts/ios-sim-build.json` | The contract: simulator prefix, device type, app id, post-prebuild scripts, usage strings, Info.plist keys, ready marker | Workflow step 2 |
| `templates/contracts/ios-sim-build.schema.json` | Its schema, with what each key does and its default | When editing the contract |
| `templates/src/config/app-variant.ts` | The canonical variant resolver (`variantEnv`, `parseAppVariant`; synced from the library; do not edit here) | Workflow step 2, when the repo has none |
| `templates/src/config/app-variant.test.ts` | Its tests (synced; do not edit here) | With the resolver |
| `scripts/check-sim-setup.mjs` | Checks the repo setup: contract, Xcode pin, scene support, build arguments, variant environment, Metro key, npm scripts, device safety, `.gitignore` | Workflow step 3 and the definition of done |
| `scripts/check-sim-app.mjs` | Checks a built `.app` against its variant | Workflow steps 5-7 and the definition of done |
| `scripts/check-screenshot.mjs` | Checks screenshots for the device size, a blank screen and a light system banner | Workflow step 5 |
| `scripts/lib/sim-contract.mjs` | Reads the contract, the Xcode pin and package.json for both repo checkers | Never by hand |
| `scripts/lib/device-safety.mjs` | The `no-xcode-select`, `sim-safety` and `adb-device` rules | Never by hand |
| `scripts/lib/sim-app-sentinels.mjs` | The `test-code` rule: sentinels and the test-only gate | Never by hand |
| `scripts/lib/sim-app-rules.mjs` | Identity, placeholder, ads, usage-string, Info.plist and store rules of `check-sim-app` | Never by hand |
| `scripts/lib/screen-measure.mjs` | Dominant colour and light-banner rows of a decoded screenshot | Never by hand |
| `scripts/lib/plist.mjs` | XML and binary plist reader (synced from the library; do not edit here) | Never by hand |
| `scripts/lib/usage-strings.mjs` | Usage descriptions per language (synced from the library; do not edit here) | Never by hand |
| `scripts/lib/ship-placeholders.mjs` | The placeholder values a ship gate refuses (synced from the library; do not edit here) | Never by hand |
| `scripts/lib/maestro-spawns.mjs` | The `maestro-device` rule (synced from the library; do not edit here) | Never by hand |
| `scripts/check-lib.mjs` | Shared checker library (synced from the library; do not edit here) | Never by hand |
| `scripts/selftest.mjs` | Proves all three checkers pass their good fixtures and catch every planted bug | After changing a checker or a template |
| `assets/shared.json` | The shared files this skill syncs in | When adding a shared file |
| `assets/template-placeholders.json` | Values for the template placeholders in template checks | When a template gains a placeholder |
| `tests/bases/` | The repo, built `.app` and screenshot bases the fixtures assemble from | When adding a fixture |
| `tests/fixtures/` | Overlay cases per checker: good, a bad case per rule, pass and error cases | When adding a rule |

## Related skills

- `app-variants-and-environment` - the variant resolver, the Metro cache key and the exported-bundle proof.
- `expo-prebuild-and-config-plugins` - `app.config.ts` as the single source and never editing `ios/`.
- `debug-menu-and-test-hooks` - the test-only gate, its entry and the sentinel this build looks for.
- `ios-release-testflight` - signed archive, export, validation and upload.
- `eas-build-and-submit` - EAS profiles, credentials and cloud builds.
- `android-emulator-build` - the same proof on an Android emulator.
- `e2e-maestro` - flows, the open-link sub-flow and the screenshot matrix on a preview build.
- `privacy-and-store-declarations` - the privacy-manifest audit a post-prebuild script runs.
- `expo-sdk-upgrade` - moving the Expo SDK or Xcode.
- `troubleshooting-playbook` - failures outside the simulator build.
