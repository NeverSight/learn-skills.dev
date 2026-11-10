---
name: troubleshooting-playbook
description: Diagnoses React Native/Expo errors, red boxes, crashes, hangs and failed builds from known failures. Use when something errors, crashes, hangs or renders wrong, or a log needs explaining. Not for gate setup (quality-gates).
---

# Troubleshooting playbook

Turns an error into a proven fix fast, on iOS and Android: look the failure up in a catalogue of about 460 known React Native 0.86 / Expo SDK 57 / Xcode / Gradle / Jest / Metro / EAS / Maestro failures, red boxes and run-time faults (each with symptom, cause, fix, status, platform and the skill that owns the procedure), apply the fix at its cause, prove it with the command that failed, scan the repo for failures that are visible in files before they happen, and record anything new so the next session finds it in seconds.

## Rules that must hold

1. **Look it up before you diagnose.** Run `find-fix.mjs` with the exact first error line before touching code. Many fixes here are counter-intuitive (a Metro cache that ignores the variant, a frame clock that resets, a polyfill that lacks `throwIfAborted`) and were expensive to find; guessing repeats that cost.
2. **Fix the cause, never the check.** No widened tolerance, skipped or deleted test, `eslint-disable`, raised limit, regenerated golden or loosened version to make a failure go away. A green gate over a real bug ships the bug.
3. **Rows that need a human are stops.** Keychain, agreements, licences, 401/403, a missing store record, signing keys, `sudo`, consoles and product decisions: send one message (the step, the exact error line, the one action needed) and wait. Retrying can lock an account or burn build numbers, and the decisions are not the agent's.
4. **When an entry names a skill, load that skill for the fix.** The catalogue gives the diagnosis; the owning skill has the procedure, templates and checks that prove the fix.
5. **A fix is proven only by rerunning the command that failed, then the area's gate.** "The error went away once" is not evidence; the same command passing, and then `npm run -s check:fast`, `npm run verify`, the simulator or emulator build, or the release gate, is.
6. **Treat `open` entries as the current fallback, not as settled facts.** Apply their fix, say in the report that the behaviour is unverified, and never present it as proven.
7. **Record every newly solved failure in `assets/known-failures/<area>.json` and its first error line in `assets/known-queries.tsv`, never in the rendered references.** Then run `check-catalogue.mjs --write`. When the cause is visible in repo files, add a rule to `scripts/lib/pitfalls.mjs` with a planted-bug case, so the scanner catches it before it happens.
8. **Change one thing at a time; after three failed hypotheses, stop and report** what was tried and what the evidence shows. A pile of simultaneous changes hides the cause, and a stuck report beats a clever workaround.
9. **Never destroy evidence or other sessions' state to "start clean".** No `xcrun simctl erase|shutdown|delete all` or `booted`, no `xcode-select -s` (select Xcode per process with `DEVELOPER_DIR`), no `adb` without `-s <serial>`, no `adb kill-server` or `./gradlew --stop`, no wiping caches or `node_modules` before the cause is known; clean only your own build folder and the simulators and emulators you created (`<project>-<purpose>`).
10. **Versions decide facts.** Read the installed source in `node_modules/` before trusting memory or docs; a version-bound entry carries `appliesTo`, and `find-fix.mjs .` ranks entries for other versions lower and says so. Training data uses APIs this stack deprecates or replaces (`runOnJS` -> `scheduleOnRN`, `.value` -> `.get()`/`.set()`, `Skia.Path.Make()` -> `Skia.PathBuilder`) and versions it cannot take yet (Jest 30, ESLint 10).

## Workflow

1. **Capture** the first error line (not the last), the command that produced it, and the platform. The logs on both platforms are listed in [references/diagnosing-new-failures.md](references/diagnosing-new-failures.md) ("Where the evidence is").
2. **Look it up:** `node ${CLAUDE_SKILL_DIR}/scripts/find-fix.mjs . --text "<first error line>"` from the repo root. Also try two or three plain words for what you see ("banner never appears"), `--log <file>` for a whole log (error patterns only), `--id <id>` for an id another checker printed, `--platform ios|android` to drop the other platform's entries. Every `MATCH` and `MATCH?` prints the cause, the fix, the status, the platform and the owning skill.
3. **Act on the match.** Only a `MATCH` line (an error pattern matched) is a diagnosis. A `MATCH?` line matched words only: confirm its symptom against what you see before acting on it, and treat it as no match when it does not fit. Marked `stop and ask a human` (only ever on a `MATCH`): send the stop message and end the step. Names a skill: load it and apply the fix with its procedure. Otherwise apply the fix directly. The full table of each area is its reference (below); read it when the match is close but not exact.
4. **No match, or the fix did not work:** follow the loop in [references/diagnosing-new-failures.md](references/diagnosing-new-failures.md): reproduce cleanly, change one thing at a time, suspect the newest change first, make a minimal repro in a scratch copy for library bugs.
5. **Scan for known pitfalls** before a first device build, a release, a dependency or SDK bump, and whenever failures repeat: `node ${CLAUDE_SKILL_DIR}/scripts/check-known-pitfalls.mjs .` from the repo root. Each `FAIL` line names the file, the catalogue id, the fix and the cause; fix and rerun until `RESULT: PASS`. It reads paths through the repo layout (`src/`, `scripts/`, `.maestro/`, `contracts/`; `rn-skills.config.json` keys `srcDir`, `scriptsDir`, `e2eDir`, `configDir`, `servicesDir`, `contractsDir`, and `package.json` workspaces when multi-package), and two repo facts owned by other skills: `contracts/ads.json` `audience` (admob-ads-and-consent; a child-directed app needs no tracking plugin) and `contracts/rtl.json` `directionSource` (rtl-and-direction; the `device` profile tolerates `supportsRTL`).
6. **Verify:** rerun the failing command, then the area's gate.
7. **Record:** add or correct the entry (field rules in the diagnosing reference), add `<id><TAB><first error line>` to `assets/known-queries.tsv`, run `node ${CLAUDE_SKILL_DIR}/scripts/check-catalogue.mjs --write`, then `check-catalogue.mjs` without flags. If you added a pitfall rule, add its `bad-<id>` case to `tests/fixtures/check-known-pitfalls/CASES.json` (its ops and its `"expect"` lines: the rule id and the planted file:line). Then run `node ${CLAUDE_SKILL_DIR}/scripts/selftest.mjs`.
8. **Report** in plain words (git-commits-and-reporting owns the format): what failed, the cause, the fix, the evidence (the passing command and its `RESULT` lines), the catalogue id, and any human step still needed.

The catalogue by area (each reference is a generated table: ID, symptom, cause, fix, status, platform, skill):

| Area | Reference | Covers |
|---|---|---|
| build | [references/build-and-expo-config.md](references/build-and-expo-config.md) | app.config.ts, variants, config plugins, prebuild, Metro, native modules |
| ios | [references/ios-xcode-and-simulator.md](references/ios-xcode-and-simulator.md) | Xcode selection, pods, xcodebuild, the simulator |
| android | [references/android-gradle-and-emulator.md](references/android-gradle-and-emulator.md) | JDK and SDK, Gradle, the emulator, adb installs, signing, Android 16 |
| release | [references/release-and-signing.md](references/release-and-signing.md) | signing, export, store gate, App Store and Google Play uploads, processing, testers, EAS submit |
| deps | [references/dependencies-and-supply-chain.md](references/dependencies-and-supply-chain.md) | pins, release age, held-back majors, install scripts, knip |
| lint | [references/typescript-and-lint.md](references/typescript-and-lint.md) | TS error codes, ESLint config bugs, naming |
| testing | [references/testing-jest-and-goldens.md](references/testing-jest-and-goldens.md) | Jest setup, mocks, RNTL, goldens, coverage, Stryker |
| e2e | [references/e2e-maestro.md](references/e2e-maestro.md) | Maestro flows, named devices, driver ports |
| animation | [references/animation-skia-and-gestures.md](references/animation-skia-and-gestures.md) | frame callbacks, worklets, springs, Skia, frame rate, gestures |
| i18n | [references/i18n-and-rtl.md](references/i18n-and-rtl.md) | Hermes Intl, catalogs, RTL and direction switches, fonts |
| services | [references/ads-purchases-audio-privacy.md](references/ads-purchases-audio-privacy.md) | AdMob, UMP and ATT consent, purchases, audio, haptics, privacy |
| state | [references/state-persistence-navigation.md](references/state-persistence-navigation.md) | stores, SQLite, navigation, cancellation, day maths |
| gates | [references/quality-gates-and-git.md](references/quality-gates-and-git.md) | commit rules, hooks, guardrail, Claude Code hooks and settings |
| perf | [references/performance-and-accessibility.md](references/performance-and-accessibility.md) | cold start, budgets, VoiceOver, TalkBack, text scaling |
| parity | [references/visual-parity-and-screenshots.md](references/visual-parity-and-screenshots.md) | screenshot capture and design comparison (design-visual-parity owns the full failure-message table) |
| skills | [references/agent-skills.md](references/agent-skills.md) | skills that do not load, trigger or run (skill-maintenance owns the procedure) |
| games | [references/games-optional.md](references/games-optional.md) | the optional games plugin: determinism, real-time loops, balance |
| runtime | [references/runtime-and-dev-server.md](references/runtime-and-dev-server.md) | Metro and the dev server, React red boxes, Expo Router navigation, network requests, TanStack Query, updates, crash reports, secure storage, deep links |

## Definition of done

- [ ] The command that failed now passes, and the gate of its area passes.
- [ ] The fix is at the cause: no check, limit, tolerance, golden or test was weakened, and no human stop was worked around.
- [ ] Human steps, if any, were sent as one message and are named in the report.
- [ ] A failure that was not in the catalogue is now an entry (or the wrong entry was corrected), with its first error line in `assets/known-queries.tsv`, and `node ${CLAUDE_SKILL_DIR}/scripts/check-catalogue.mjs` prints `RESULT: PASS`.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-known-pitfalls.mjs .` prints `RESULT: PASS` (it has no SKIP lines).

## Anti-patterns

- **Fixing from memory.** Look up first, then read the installed source; the stack is newer than most docs.
- **Retrying `errSecInternalComponent`, a 401/403, an agreement or a keystore password error.** These are stops; send the message.
- **Raising `max-params`, a coverage threshold or a pixel tolerance because a check fails.** That hides the defect and needs a `Gate-Change:` trailer and the reviewer anyway.
- **`xcrun simctl erase all`, `adb kill-server` or deleting `~/Library/Developer` "to start fresh".** Other sessions' devices and all evidence are gone; clean only what you created.
- **Deleting the Metro cache to fix a stale variant.** It hides the missing cache key until the next build.
- **Editing a rendered reference to add a row.** The next `--write` erases it; edit the area JSON.
- **An entry like "build failed, rebuild".** Symptoms quote the error text, causes say why, fixes say what to change, and match patterns are specific (`entry-match-broad` fails a pattern that matches anything).
- **Declaring victory after one green run of a flaky test.** Find why it flaked (time, randomness, order, a real race); `jest.retryTimes` is banned.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/diagnosing-new-failures.md](references/diagnosing-new-failures.md) | The loop for unknown failures, where every log is on iOS and Android, isolation, stop rules, the entry fields, adding a pitfall rule, a worked example | Workflow steps 1, 4 and 7 |
| [references/build-and-expo-config.md](references/build-and-expo-config.md) | Generated table: build area | Workflow step 3, config, prebuild and Metro failures |
| [references/ios-xcode-and-simulator.md](references/ios-xcode-and-simulator.md) | Generated table: ios area | Workflow step 3, Xcode and simulator failures |
| [references/android-gradle-and-emulator.md](references/android-gradle-and-emulator.md) | Generated table: android area | Workflow step 3, Gradle, emulator and adb failures |
| [references/release-and-signing.md](references/release-and-signing.md) | Generated table: release area | Workflow step 3, signing and upload failures |
| [references/dependencies-and-supply-chain.md](references/dependencies-and-supply-chain.md) | Generated table: deps area | Workflow step 3, install, upgrade and knip failures |
| [references/typescript-and-lint.md](references/typescript-and-lint.md) | Generated table: lint area | Workflow step 3, tsc and ESLint errors |
| [references/testing-jest-and-goldens.md](references/testing-jest-and-goldens.md) | Generated table: testing area | Workflow step 3, Jest failures |
| [references/e2e-maestro.md](references/e2e-maestro.md) | Generated table: e2e area | Workflow step 3, Maestro failures |
| [references/animation-skia-and-gestures.md](references/animation-skia-and-gestures.md) | Generated table: animation area | Workflow step 3, animation, canvas and gesture bugs |
| [references/i18n-and-rtl.md](references/i18n-and-rtl.md) | Generated table: i18n area | Workflow step 3, language and RTL bugs |
| [references/ads-purchases-audio-privacy.md](references/ads-purchases-audio-privacy.md) | Generated table: services area | Workflow step 3, ads, consent, purchases, audio and privacy |
| [references/state-persistence-navigation.md](references/state-persistence-navigation.md) | Generated table: state area | Workflow step 3, data, navigation and async bugs |
| [references/quality-gates-and-git.md](references/quality-gates-and-git.md) | Generated table: gates area | Workflow step 3, hook and commit failures |
| [references/performance-and-accessibility.md](references/performance-and-accessibility.md) | Generated table: perf area | Workflow step 3, perf and a11y findings |
| [references/visual-parity-and-screenshots.md](references/visual-parity-and-screenshots.md) | Generated table: parity area | Workflow step 3, capture and design-comparison failures |
| [references/agent-skills.md](references/agent-skills.md) | Generated table: skills area | Workflow step 3, a skill misbehaves |
| [references/games-optional.md](references/games-optional.md) | Generated table: games area (optional plugin) | Workflow step 3, game rules, loops and balance |
| [references/runtime-and-dev-server.md](references/runtime-and-dev-server.md) | Generated table: runtime area | Workflow step 3, red boxes, dev-server, navigation, network and run-time faults |
| `assets/known-failures/` | The catalogue: `index.json` (version, reviewed date, stack, areas, skill names, banned terms) and one `<area>.json` per area (the one place entries are written) | Workflow step 7 |
| `assets/known-queries.tsv` | Recorded first error lines, one `<id><TAB><text>` per line; check-catalogue proves each ranks its entry first | Workflow step 7 |
| `scripts/find-fix.mjs` | Looks up error text, a log or an id; exit 1 when nothing is known | Workflow step 2 |
| `scripts/check-known-pitfalls.mjs` | Scans the app repo for the known failures visible in files (variants, Metro, devices, versions, configs, flows, export options) | Workflow step 5 and the definition of done |
| `scripts/check-catalogue.mjs` | Validates the catalogue, runs the recorded queries, renders (`--write`) and checks the references, checks pitfall ids | Workflow step 7; repo CI |
| `scripts/lib/catalogue.mjs` | Catalogue loader, validator, version ranges, search ranking and renderer | When changing the entry format |
| `scripts/lib/pitfalls.mjs` | The pitfall rules, one per catalogue id, with layout-derived globs | Workflow step 7, to add a rule |
| `scripts/selftest.mjs` | Proves all three scripts against the fixtures (one planted bug per rule) and this skill's own catalogue | After changing a script, a rule, an entry or a query |
| `scripts/check-lib.mjs` | Shared script helper, synced from the library (do not edit here) | Never by hand |
| `assets/shared.json` | Declares the shared files this skill copies in | When adding a shared file |
| `tests/fixtures/` | Overlay suites: a single-app tree with planted pitfalls (and silent installed-skill traps), a two-area catalogue, find-fix queries | When adding a rule or a lookup case |

## Related skills

- `react-native-conventions-index` - which skill owns a task; start there when unsure.
- `quality-gates` - what each gate checks and the Gate-Change rule.
- `ios-simulator-build` / `android-emulator-build` - running and proving a device build.
- `ios-release-testflight` / `android-release-play` / `eas-build-and-submit` - the release pipelines and their stop tables.
- `dependency-management` / `expo-sdk-upgrade` - installing, pinning and upgrading, where many held-back entries end.
- `skill-maintenance` - a skill that does not load, trigger or pass the validator.
- `git-commits-and-reporting` - the report and the stop message.
- Expo's official `expo-dev-client`, `eas-app-stores` and `expo-upgrade` skills - Expo's own API reference for dev builds, store submission and SDK upgrades.
