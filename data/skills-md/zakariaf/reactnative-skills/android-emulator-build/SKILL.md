---
name: android-emulator-build
description: Assembles Release APKs with Gradle on an AVD started by name (pinned JDK and SDK) and inspects them. Use when trying the app on the Android emulator, or Gradle, adb, an AVD or the SDK fails. Not for Play uploads (android-release-play).
---

# Android emulator build

Turns the Expo app into a Release APK with one command, `npm run build:android:emu -- --variant preview`, and proves what was built: JDK 17 and the pinned Android SDK made it, the APK is the variant asked for (test-only code present in development and preview, absent in production; the variant's package; only the permissions the app declared), and the app starts and draws on an emulator this repo owns. No Android Studio, no Metro, no upload key. Verified on 2026-10-14 with Expo SDK 57 (expo 57.0.26), React Native 0.86.3 (compileSdk and targetSdk 36, build tools 36.0.0, Gradle 9.3.1 from the prebuild template), JDK 17.0.11 and Android emulator 35.1.20 on Apple silicon, booting the API 35 16 KB Play Store image (`system-images;android-35;google_apis_playstore_ps16k;arm64-v8a`) through the contract's `systemImage`; the pinned default image (`system-images;android-36;google_apis;<abi>`) has not had a real boot yet. The iOS twin is `ios-simulator-build`.

## Rules that must hold

1. **Every emulator build runs through one script and starts from a clean prebuild.** `scripts/build/build-android-emu.ts` preflights every npm script it will run (exit 2, nothing built), then `npx expo prebuild --platform android --clean`, the contract's post-prebuild scripts, Gradle, install, launch and screenshot. Why: `android/` is generated (Continuous Native Generation, owned by `expo-prebuild-and-config-plugins`), and a stale `android/` from another variant builds the wrong package.
2. **JDK 17 and the Android SDK are selected per process, and the pins match React Native.** `scripts/android/toolchain.ts` pins `JDK_MAJOR`, `ANDROID_API` and `BUILD_TOOLS_VERSION` as literals equal to the installed React Native's version catalog; `selectToolchain()` finds JDK 17 by its `release` file, checks the SDK packages and sets `JAVA_HOME` and `ANDROID_HOME` on the child environment. Never `jenv global`, `sdk default java`, `update-alternatives` or `sudo`. Why: a machine often holds several JDKs (Android Studio's bundled one changes with Studio updates), and a global switch changes every build on it.
3. **The variant is exported once, for the whole run.** `variantEnv(variant)` from `src/config/app-variant.ts` sets `APP_VARIANT` = `EXPO_PUBLIC_APP_VARIANT` on the one environment every step gets. Why: the variant enters the APK three times, each in its own process: the prebuild (package, manifest), expo-constants' `createExpoConfig` Gradle task (`assets/app.config`) and Metro (`export:embed`, the JS bundle).
4. **Metro's cache is keyed on the public values before any Release build.** `metro.config.js` sets `cacheVersion` from the `EXPO_PUBLIC_*` values (the key and its proof belong to `app-variants-and-environment`). Why: the build runs with `CI=1`, so the bundling task keeps Metro's cache, and a production APK built after a preview APK can ship the preview bundle.
5. **The build is `:app:assembleRelease` for one ABI, with no daemon and no upload key.** `./gradlew --no-daemon :app:assembleRelease -PreactNativeArchitectures=<abi>` (`gradleReleaseArgs`), the ABI of the emulator (`hostAbi()`: arm64-v8a on Apple silicon, x86_64 elsewhere). Why: Release embeds the Hermes bundle users run (Debug loads JS from Metro); one ABI builds about four times faster than the template's four; a daemon would keep another run's environment and 2 GB of memory on a shared machine; the prebuild template signs Release with the public debug keystore, so no secret is touched (upload signing is `android-release-play`).
6. **Emulators are AVDs named `<prefix>-<purpose>`, started on a console port this run picked and addressed only by serial.** `emulator -avd <prefix>-<purpose> -port <even port>`, then `adb -s emulator-<port> ...` after `adb -s emulator-<port> emu avd name` confirmed the AVD behind it; only prefixed AVDs are created, stopped (`adb -s <serial> emu kill`) or deleted. Never `adb -e`/`-d`, `adb kill-server`, `gradlew --stop`, a Gradle `install*` task, `pkill` of emulators or `eas build:run -p android`. Why: several sessions share one machine and one adb server; each of those reaches, restarts or installs on someone else's device.
7. **Every tooling process runs with `EXPO_NO_TELEMETRY=1` and `CI=1`.** Why: no telemetry, and no interactive prompt that would hang an unattended run.
8. **A fresh install and a cold start, then wait on a signal, never a fixed sleep; then check the screenshot and look at it.** The previous copy is uninstalled, `am start -S -W` starts the launcher activity, and the run polls: the process alive (`pidof`), its activity resumed, the crash buffer empty, and the contract's `readyLog` line or two identical screenshots after at least 3 s. Why: a build that installed can still crash at launch, sit behind a system dialog, or draw a blank screen; only the picture shows the last one.
9. **The built APK proves its variant.** `check-apk` reads the APK: an embedded Hermes bundle, the test-only sentinel (present in development and preview, absent in production), not debuggable, the variant's own package in the manifest and in expo-constants' `assets/app.config`, targetSdk 36 and minSdk 24 or higher, native libraries for the emulator ABI with 16 KB aligned segments, a signing block, and for production no placeholder and no cleartext traffic. Why: `BUILD SUCCESSFUL` says nothing about what shipped inside.
10. **The merged manifest is the permission evidence.** The contract's `permissions` lists every permission the app may carry (seeded with the five the prebuild template always adds; one named after the app is written `${applicationId}.NAME`, and the APK's own signature permission from androidx.core needs no entry); `check-apk` fails on any other in the APK. Why: libraries add permissions at Gradle merge time (an image picker's CAMERA, a template's SYSTEM_ALERT_WINDOW), and neither `app.config.ts` nor the prebuild output shows them.
11. **A change to variants, Metro, test-only code or the build tooling is proven by a preview build and a production build made back to back, without clearing any cache.** Why: only that order shows a missing cache key or a broken gate.
12. **Human steps are asked for, never worked around.** Installing a JDK, the SDK packages and a system image, and accepting the SDK licences, are the developer's steps (a licence is a legal agreement); the agent stops and asks. Why: a workaround (another JDK, an auto-accepted licence, a different image) builds with the wrong toolchain and hides the problem.
13. **Generated and output folders stay out of git:** `android/`, `build/` and `reports/`. Why: the prebuild regenerates `android/`, `build/` holds the kept APKs and logs, `reports/` the screenshots.

## Workflow

1. **First time in a repo, or after a setup check fails:** read [references/toolchain-and-sdk.md](references/toolchain-and-sdk.md) (versions, JDK selection, SDK packages, human steps, the SDK 58 move) and [references/build-variants.md](references/build-variants.md) (the three moments, the Metro trap, signing, what proves a variant).
2. **Install the templates that are missing** (line 1 of each names its repo path; fill `__AVD_PREFIX__` and `__APP_ID__` in the contract):

   | Template | Goes to |
   |---|---|
   | `templates/scripts/android/toolchain.ts`, `adb-args.ts`, `emulators.ts` (+ tests) | `scripts/android/` |
   | `templates/scripts/build/build-android-emu.ts` and `emu-build-*.ts`, `emu-ready-signal.ts` (+ tests) | `scripts/build/` |
   | `templates/contracts/android-emu-build.json` + `.schema.json` | `contracts/` |
   | `templates/src/config/app-variant.ts` + test (canonical) | `src/config/` (skip when present) |

   Add `"build:android:emu": "node scripts/build/build-android-emu.ts"` to `package.json`, check the `.gitignore` lines (rule 13), and run `npm run typecheck`, `npx eslint scripts --max-warnings 0` and `npx jest scripts --ci --maxWorkers=2`. Metro's cache key comes from `app-variants-and-environment`; post-prebuild scripts go into the contract's `postPrebuild`; list the app's permissions in the contract's `permissions`.
3. **Check the setup:** `node ${CLAUDE_SKILL_DIR}/scripts/check-emu-setup.mjs .`. Fix every `FAIL` (each names the file, the rule and the fix) and rerun until `RESULT: PASS`. [references/contract-and-checks.md](references/contract-and-checks.md) explains every rule and contract key.
4. **Build and run:** `npm run build:android:emu -- --variant preview` (`--help` prints the options; `--emu <purpose>` picks another AVD, `--link <path>` also screenshots a deep-linked screen, `--keep-emulator` leaves the emulator this run started running). Read [references/emulator-commands.md](references/emulator-commands.md) when a step fails, when you run a step by hand, or before changing the script. The run prints the APK path and the screenshot path.
5. **Prove the build:** `node ${CLAUDE_SKILL_DIR}/scripts/check-apk.mjs . --apk build/android-emu/app-preview.apk --variant preview`, then `node ${CLAUDE_SKILL_DIR}/scripts/check-emu-screenshot.mjs reports/android-emu/`, then open the PNG and look at it (the intended screen, text drawn, no system dialog, no blank area). [references/apk-anatomy.md](references/apk-anatomy.md) says what each part of the APK proves.
6. **When the change touches variants, `metro.config.js`, test-only code or the build tooling:** run `--variant production` right after the preview build without clearing any cache, and `check-apk.mjs` on both. [examples/variant-proof.md](examples/variant-proof.md) shows the commands and the output.
7. **EAS or iOS:** an EAS APK (`android.buildType: "apk"`, built with `--local`) is checked the same way and installed with `adb -s <serial> install`; the iOS simulator build is `ios-simulator-build`. Both are in [references/eas-and-ios.md](references/eas-and-ios.md).
8. **On any failure**, match the text in [references/failures.md](references/failures.md), fix the cause (never the check), rerun the failing step, then the checks. Stop and ask the developer for anything that needs an install, a licence or a password.
9. **Report** in plain words: variant, AVD name, profile and image, the APK and screenshot paths, what the screenshot shows, every SKIP line, and the three `RESULT` lines. Stop this session's emulators by serial at the end (`adb -s <serial> emu kill`).

## Definition of done

- [ ] `npm run build:android:emu -- --variant <v>` ran from a clean prebuild and printed `ready (...)` with a screenshot path.
- [ ] The screenshot was opened and looked at, and shows the intended screen (not black, white, empty or covered by a system dialog).
- [ ] For variant, Metro, test-only or tooling changes: a preview and a production APK built back to back both pass `check-apk.mjs`.
- [ ] Only `<prefix>-<purpose>` AVDs were created or touched, each by its serial; no `sudo`, global JDK switch, `adb -e`/`-d`, `adb kill-server` or `gradlew --stop` anywhere; this session's emulators are stopped.
- [ ] Expected SKIP line only: `SKIP src/test-only.ts [test-code] not yet created (debug-menu-and-test-hooks creates it)` while the app has no test-only gate.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-apk.mjs . --apk build/android-emu/app-<v>.apk --variant <v>` and `node ${CLAUDE_SKILL_DIR}/scripts/check-emu-screenshot.mjs reports/android-emu/` print `RESULT: PASS`.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-emu-setup.mjs .` prints `RESULT: PASS`

## Anti-patterns

- **Opening `android/` in Android Studio to fix a Gradle setting.** The next prebuild erases it; put the setting in `app.config.ts`, `expo-build-properties` or a config plugin.
- **`export JAVA_HOME=...` in a shell profile, `jenv global 17` or `sudo update-alternatives` because "Gradle picked the wrong Java".** Select JDK 17 per process with `selectToolchain()`; installing a JDK is the developer's step.
- **`npx expo run:android`, `./gradlew installDebug` or `installRelease` to "check quickly".** Debug loads JS from Metro with a dev menu, and the install tasks install on every connected device, another session's emulator included.
- **`adb install app.apk` or `adb -e shell ...`.** It fails with two devices attached, or reaches the device another session started; write `adb -s <serial>`.
- **`adb kill-server` to "fix" an offline device, or `./gradlew --stop` after a build.** Both hit every session on the machine; reconnect your own device, and build with `--no-daemon`.
- **`sleep 30 && adb -s <serial> exec-out screencap -p > shot.png`.** Too short on a cold emulator, wasted time on a warm one; poll the ready signal.
- **`eas build:run -p android --latest`.** It installs on the first running emulator; extract the APK and install it by serial.
- **Disabling animations (`settings put global window_animation_scale`, `transition_animation_scale` or `animator_duration_scale 0`) for stable screenshots.** React Native's AccessibilityInfo and Reanimated read `transition_animation_scale` 0 as Reduce Motion, so the screenshot shows the reduced-motion app (and `animator_duration_scale` 0 makes Android's own animators instant); the ready signal waits for a still screen instead.
- **`yes | sdkmanager --licenses` in a setup script.** Accepting a licence is the developer's decision, made once in their own terminal.
- **Declaring success from `BUILD SUCCESSFUL`.** Install, launch, screenshot, check and look.
- **Deleting `$TMPDIR/metro-cache` to fix a stale variant.** It hides the missing cache key until the next build; key `cacheVersion` on the public values.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/toolchain-and-sdk.md](references/toolchain-and-sdk.md) | Versions with re-verify commands, JDK selection, ANDROID_HOME, the SDK packages and the NDK, human steps, Gradle and memory on a shared machine, the SDK 58 move | Workflow step 1, and when the JDK, the SDK or the machine changes |
| [references/build-variants.md](references/build-variants.md) | The three variants on an emulator, the three moments, the Metro cache trap, the Gradle daemon and the environment, signing, the evidence `check-apk` reads, the back-to-back proof | Workflow steps 1 and 6 |
| [references/emulator-commands.md](references/emulator-commands.md) | Every command of the run with its flags, profiles and sizes, ports and serials, boot, demo mode, install, launch, the ready signal, crash evidence, deep links, cleanup, timings | Workflow step 4, and when running a step by hand |
| [references/apk-anatomy.md](references/apk-anatomy.md) | What a Release APK holds and what each part proves: the binary manifest, the merged manifest, the Hermes bundle, app.config, native libraries and 16 KB pages, the signing block, and the SDK tools that show them | Workflow step 5, and when check-apk fails |
| [references/contract-and-checks.md](references/contract-and-checks.md) | The contract keys, the `rn-skills.config.json` keys, every checker rule with its reason, the limits of the text rules, when multi-package | Workflow step 3, and when a check fails |
| [references/eas-and-ios.md](references/eas-and-ios.md) | The EAS APK lane (profile, `--local`, why not `build:run`) and the iOS counterpart of every step | Workflow step 7 |
| [references/failures.md](references/failures.md) | Symptom, cause and fix for toolchain, prebuild, Gradle, emulator, install, launch and screenshot failures | Workflow step 8, whenever something fails |
| [examples/variant-proof.md](examples/variant-proof.md) | A real preview and production build of the reference Tasks app: timings, the checker output, real findings, the report | Workflow steps 5 and 6 |
| `templates/scripts/android/toolchain.ts` | The JDK and SDK pins, `selectToolchain()`, `toolEnv()`, `hostAbi()`, `systemImageFor()`, `sdkTool()` | Workflow step 2 |
| `templates/scripts/android/adb-args.ts` | `adbArgs(serial, ...)`: the only way the repo builds adb arguments | Workflow step 2 |
| `templates/scripts/android/emulators.ts` | AVD names, console ports, the identity check, boot, demo mode, fresh install, cold start, own-only stop | Workflow step 2 |
| `templates/scripts/android/` | The three modules above and their tests (`*.test.ts` beside each) | Workflow step 2 |
| `templates/scripts/build/build-android-emu.ts` | The CLI behind `npm run build:android:emu` | Workflow step 2 |
| `templates/scripts/build/emu-build-steps.ts` | Its side effects: logged steps, package.json kept clean, the AVD and emulator, boot wait, screencap, the ready poll | Workflow step 2 |
| `templates/scripts/build/emu-build-args.ts` | The command line, parsed with the app's variant resolver | Workflow step 2 |
| `templates/scripts/build/emu-build-config.ts` | The contract reader (valibot), defaults filled | Workflow step 2 |
| `templates/scripts/build/emu-build-plan.ts` | Prebuild and Gradle arguments, APK, merged manifest and screenshot paths, the preflight, the deep-link intent | Workflow step 2 |
| `templates/scripts/build/emu-ready-signal.ts` | When the launched app counts as ready, and when it has failed | Workflow step 2 |
| `templates/scripts/build/` | The build modules above and the tests of the pure ones | Workflow step 2 |
| `templates/contracts/android-emu-build.json` | The contract: AVD prefix, profile, image, app id, post-prebuild scripts, SDK levels, permissions, application keys, ready log | Workflow step 2 |
| `templates/contracts/android-emu-build.schema.json` | Its schema, with what each key does and its default | When editing the contract |
| `templates/src/config/app-variant.ts` | The canonical variant resolver (`variantEnv`, `parseAppVariant`; synced from the library; do not edit here) | Workflow step 2, when the repo has none |
| `templates/src/config/app-variant.test.ts` | Its tests (synced; do not edit here) | With the resolver |
| `scripts/check-emu-setup.mjs` | Checks the repo setup: contract, pins, build plan, signing, variant environment, Metro key, npm scripts, device and shared-machine safety, `.gitignore` | Workflow step 3 and the definition of done |
| `scripts/check-apk.mjs` | Checks a built APK (or an unzipped / decoded one) against its variant | Workflow steps 5-7 and the definition of done |
| `scripts/check-emu-screenshot.mjs` | Checks screenshots for the AVD profile's size and a blank screen | Workflow step 5 |
| `scripts/lib/emu-contract.mjs` | Reads the contract, the toolchain pins, React Native's version catalog and package.json | Never by hand |
| `scripts/lib/android-device-safety.mjs` | The `adb-device`, `emulator-avd`, `shared-machine` and `no-global-switch` rules | Never by hand |
| `scripts/lib/apk-reader.mjs` | ZIP, binary XML and text manifest reader, ELF segment alignment | Never by hand |
| `scripts/lib/apk-rules.mjs` | The rules of `check-apk` | Never by hand |
| `scripts/lib/apk-fixture.mjs` | Writes APK-shaped fixtures (ZIP, binary XML, ELF headers) for the self-test only | Never by hand |
| `scripts/lib/ship-placeholders.mjs` | The placeholder values a ship gate refuses (synced from the library; do not edit here) | Never by hand |
| `scripts/check-lib.mjs` | Shared checker library (synced from the library; do not edit here) | Never by hand |
| `scripts/selftest.mjs` | Proves all three checkers pass their good fixtures and catch every planted bug | After changing a checker or a template |
| `assets/shared.json` | The shared files this skill syncs in | When adding a shared file |
| `assets/template-placeholders.json` | Values for the template placeholders in template checks | When a template gains a placeholder |
| `tests/bases/` | The repo, decoded APK and screenshot bases the fixtures assemble from | When adding a fixture |
| `tests/fixtures/` | Overlay cases per checker: good, a bad case per rule, pass and error cases | When adding a rule |

## Related skills

- `app-variants-and-environment` - the variant resolver, the Metro cache key and the exported-bundle proof.
- `expo-prebuild-and-config-plugins` - `app.config.ts` as the single source and never editing `android/`.
- `debug-menu-and-test-hooks` - the test-only gate, its entry and the sentinel this build looks for.
- `android-release-play` - the signed App Bundle, the upload key and Google Play.
- `eas-build-and-submit` - EAS profiles, credentials and cloud builds.
- `ios-simulator-build` - the same proof on an iOS simulator.
- `e2e-maestro` - flows and screenshots on a preview APK with `--device <serial>`.
- `privacy-and-store-declarations` - the permissions and data the store forms must declare.
- `permissions-and-system-prompts` - asking for the permissions the contract lists.
- `expo-sdk-upgrade` - moving the Expo SDK, the JDK and the Android pins.
- `troubleshooting-playbook` - failures outside the emulator build.
