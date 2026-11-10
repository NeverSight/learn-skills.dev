---
name: expo-sdk-upgrade
description: Moves an Expo app to the next SDK and Xcode/Android toolchain in one proven commit - expo install --fix, overrides, breaking changes. Use when an SDK, Xcode or targetSdk upgrade is due. Not for one package (dependency-management).
---

# Expo SDK upgrade

Moves the app (every app and shared package, when multi-package) to the next Expo SDK, or the build
toolchain to another Xcode or Android level, in one proven step: only when the new SDK is stable and
old enough or a store deadline forces it, with every package, tool, override, code migration and
toolchain change in one commit, and two checkers that prove when a move is due and that the repo sits
on one SDK line.

## Rules that must hold

1. **Move only when the trigger holds:** npm `latest` (or the target's `sdk-<n>` tag) is the new SDK
   and at least the repo's release age old (`.npmrc` `min-release-age`, 7 days at least, measured to
   the minute as npm measures it), and so is every package the repo takes from its module map plus
   the `@react-native/*` tools at the new React Native version (`check-sdk-trigger.mjs` reports
   `upgrade-due`), and on a branch the whole repo passes the gate, iOS and Android release builds,
   E2E and the visual baselines. `RESULT: PASS` from the trigger means no move is due (stay). Never a
   preview, beta, release candidate or `next` release, never a release-age exclude for an SDK. *Why:*
   previews break things, and the first patch releases fix what `.0` broke; an SDK is never urgent
   enough for an exception.
2. **One SDK at a time, unless Expo's notes say to skip one; never an expo release the SDK's advisory
   rules out.** Apps on SDK 55 go straight to SDK 57 and no app installs expo 57.0.8 or older (a
   Hermes V1 memory regression with Worklets and Reanimated, in SDK 56 too); the SDK lines hold this <!-- stack-pin-ignore -->
   as `skipFrom` and `minExpo`, the trigger picks the target from them and `expo-min` fails a release
   below the floor. *Why:* skipping changes nothing else in the move, and the regression ships to
   every user.
3. **Move the whole repo in one commit, on a branch.** *Why:* Expo supports one React Native version
   per repo, and a half-moved tree can be neither tested nor rolled back cleanly.
4. **Expo-managed packages move only with `npx expo install expo@~<version>` then
   `npx expo install --fix`** (in every app when multi-package). Never hand-edit an Expo-managed
   specifier or install `react-native`, React, Reanimated, Worklets, Skia or Gesture Handler by hand.
   *Why:* Expo tests one coherent native set per SDK, and `--fix` writes exactly that set.
5. **Everything that follows the SDK moves in the same commit:** the root tools in one
   `npm install -D` (`jest-expo`, `eslint-config-expo`, `@react-native/jest-preset`,
   `@react-native/eslint-plugin`, `@types/react`, `test-renderer`, and `jest`, `babel-jest`,
   `@types/jest` when the SDK's jest-expo peers on a new Jest line), every root `overrides` key at the
   version the app installs, `allowScripts`, the code migrations, eas.json images that name an SDK,
   Android SDK pins that fell behind, and the app's `contracts/dependency-policy.json` rows. *Why:*
   each one alone breaks the install (`ERESOLVE`), the tree (duplicate native modules) or a gate.
6. **Tools the SDK does not move stay:** TypeScript (6.0 on SDKs 56 to 58), ESLint, Prettier and
   everything outside Expo's map keep their own held-back triggers (dependency-management). A tool
   ahead of the SDK's line fails `held-back`; one behind a line the SDK needs fails `sdk-tooling`.
   *Why:* two moves in one commit cannot be debugged.
7. **Readiness first:** run `check-sdk-alignment.mjs --target-sdk <next>` before the branch and fix
   every `FAIL` (React Native or Jest APIs the next SDK removes, app config keys its schema dropped,
   an Xcode too old) on the current SDK in its own commit; the `todo` lines (config plugin imports,
   Jest config, builder gestures, image aliases, pins) change only in the move commit. *Why:* the
   replacements already work on the old SDK, so the move commit stays about the move.
8. **When the SDK moves a library to a new API generation, migrate every user of it as a whole** in
   the move commit (Gesture Handler 2 builder to 3 hooks: every component that builds gestures).
   *Why:* hook and builder gestures cannot be related to each other, so a component that mixes them
   loses the exclusive or simultaneous relations it depends on.
9. **The toolchain follows the SDK and is chosen by version.** Xcode through `DEVELOPER_DIR` on a Mac
   (never `sudo xcode-select`) or an EAS image (`auto`, `sdk-<n>` or an exact name, never `latest`),
   recorded in one place the checkers read; an Xcode major newer than the SDK supports gets that SDK's
   extra step first (SDK 57 with Xcode 27 needs `ios.enableSceneSupport`, removed again on SDK 58;
   SDKs 55 and 56 have no such option and stay on Xcode 26); Android compileSdk, targetSdk and minSdk
   and the iOS deployment target follow the SDK, and an `expo-build-properties` pin never stays behind
   them. *Why:* a floating image or a stale pin changes the binary without a commit, a deployment
   target below the SDK's pods fails `pod install`, and an iOS 27 SDK build on the application life
   cycle does not launch correctly on iOS 27.
10. **Store deadlines are triggers too:** an App Store minimum Xcode or a Google Play minimum
    targetSdk in effect that the app does not meet fails `store-deadline` and is fixed by a toolchain
    or SDK move. *Why:* the store rejects the next upload regardless of how stable the app is.
11. **Never loosen a gate or re-accept a golden or screenshot to get green.** Every diff is explained
    by the change list and committed with a `Gate-Change:` trailer. *Why:* a silent visual or
    behavioural regression ships to every user at once.
12. **Read the new versions' release notes, versioned docs and published packages, never memory.**
    Put every new finding in the move report; when this skill's entry for the new SDK is missing or
    pre-release, write the app's own `contracts/expo-sdk-lines.json` entry from the stable release.
    *Why:* SDK facts change between previews (SDK 58's jest-expo switched to Jest 30 while SDK 58 was
    still a pre-release).
13. **Stop and ask before the branch (one message with a default: start on the branch) and wait for
    an explicit go before merging, pushing, EAS builds or uploads** (silence is never a go: the
    branch waits unmerged). Installing Xcode, licences, simulator runtimes, JDKs and `sudo` are human
    steps.

## Workflow

1. Read [references/upgrade-policy.md](references/upgrade-policy.md): the current and next line,
   the trigger, store deadlines, what moves together, what never does.
2. Check the trigger: `node ${CLAUDE_SKILL_DIR}/scripts/check-sdk-trigger.mjs . --online
   --save-facts reports/sdk-trigger.json` (offline: `--facts <saved file>`; with neither it exits 2).
   Its `sdk` line names the target (the next SDK, or the one Expo says to move to: a `note` line
   says so). `RESULT: PASS` means no move is due: its `wait` lines (`target-stable`, `target-age`,
   `package-age`, `package-missing`) say why and from which moment it can change; stop and, if asked,
   report "not yet" with that moment (message 1 of [examples/sdk-move-report.md](examples/sdk-move-report.md)).
   `FAIL [upgrade-due]`: the move is due; keep its `plan` lines and continue. `FAIL [store-deadline]`:
   a toolchain move is due; go to step 6.
3. Start green (the project gate, clean `git status`, and the plain
   `node ${CLAUDE_SKILL_DIR}/scripts/check-sdk-alignment.mjs .` passing: the readiness scan checks
   imports only against the target SDK's line), then scan readiness:
   `node ${CLAUDE_SKILL_DIR}/scripts/check-sdk-alignment.mjs . --target-sdk <target>` (58 from SDK
   57). Fix every `FAIL` on the current SDK in its own commit; the `todo` lines are the move commit's
   work list.
4. Tell the developer (message 2 of the example) and continue unless told to wait.
5. Read [references/sdk-58-changes.md](references/sdk-58-changes.md) in full (or the release notes
   of the target SDK, for 57 and later ones), then follow [references/runbook.md](references/runbook.md) steps 5 to 18: branch,
   `npx expo install`, root tools in one command, overrides, approvals, code migrations (config plugin
   imports, Jest resolver and Jest 30, Gesture Handler 3, scene-support removal), EAS images, Android
   and iOS pins, the dependency policy rows and, when needed, the app's SDK line entry
   ([references/sdk-lines.md](references/sdk-lines.md)).
6. For a toolchain-only change (a new Xcode, an EAS image, an Android target, a store deadline) read
   [references/toolchain.md](references/toolchain.md). SDK 57 with Xcode 27: copy
   `templates/scripts/config/scene-support.ts` and its test to `scripts/config/`, import it in
   `app.config.ts` with the extension, `import { addSceneSupport } from './scripts/config/scene-support.ts';`
   (Expo loads `app.config.ts` through Node, which needs the `.ts`; without it `npx expo config`
   fails with "Cannot find module"), wrap the plugin list with `addSceneSupport([...])`, then record
   the new Xcode.
7. Verification loop (runbook "Verification loop"): `node ${CLAUDE_SKILL_DIR}/scripts/check-sdk-alignment.mjs .`
   until `RESULT: PASS` (each `FAIL` names the file, the rule and the fix), `npx expo install --check`,
   `npx expo-doctor` (an `install.exclude` entry only for a stale Expo suggestion, with its reason:
   runbook failure table), `npm ls react react-native react-native-reanimated react-native-worklets`, the
   gate, then a clean prebuild with Release builds on a named iOS simulator and a named Android
   emulator (or EAS preview builds), E2E and the visual baselines (hand-offs below); open every diff.
8. Commit the move as one commit with its `Gate-Change:` trailer (runbook "Commit, report, merge"),
   report with message 3 of the example, and merge or push only on the developer's go.

## Definition of done

- [ ] Before the branch, `check-sdk-trigger.mjs` reported `upgrade-due` (or `store-deadline` for a
      toolchain move) and its facts are saved in `reports/`; after the move
      `node ${CLAUDE_SKILL_DIR}/scripts/check-sdk-trigger.mjs . --online` prints `RESULT: PASS` again.
- [ ] Every app declares the new `expo` and exactly the new module map's specifiers;
      `npx expo install --check` and `npx expo-doctor` pass (in every app when multi-package);
      `npm ls` shows one version of `react`, `react-native`, `react-native-reanimated` and
      `react-native-worklets`.
- [ ] Root tools, overrides, `allowScripts`, eas.json images, Android and iOS pins and the dependency
      policy rows moved in the same commit; TypeScript, ESLint and the other held-back tools did not.
- [ ] Config plugin imports, the Jest config, gestures and scene support match the new SDK; the gate
      is green.
- [ ] Release builds launched on a named iOS simulator and a named Android emulator (or EAS preview
      builds), E2E passed, and every golden or screenshot diff was looked at and explained.
- [ ] The developer got the report; nothing was merged, pushed, built on EAS or uploaded without an
      explicit go (silence is not one: the branch waits unmerged).
- [ ] Expected SKIP lines only: `SKIP eas.json [xcode] not yet created (eas-build-and-submit creates
      it)` while the app has neither eas.json nor an Xcode pin, and `SKIP jest.config.js [jest-config]
      not yet created (unit-and-component-tests creates it)` while it has neither a `jest.config.*` file
      nor a package.json `"jest"` key (on an SDK with Jest config lines). `note` lines are information.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-sdk-alignment.mjs .` prints `RESULT: PASS`

## Anti-patterns

- **Adopting a preview, beta, release candidate or `next` release,** or adding a
  `min-release-age-exclude` to get an SDK early: wait for the trigger.
- **Moving one part first "to try it"** (one app, one package, the tools before the SDK), or merging a
  half-moved repo: the whole move lives on one branch until it is green.
- **Installing `jest-expo` alone**, then `--legacy-peer-deps` to silence `ERESOLVE`: install the root
  tools in one command, Jest included when the SDK's jest-expo peers on a new line.
- **`npm dedupe` or deleting `node_modules` against duplicate native modules:** set the overrides and
  `npm install`; expo-doctor must show no duplicates.
- **Switching config plugins to `expo/config-plugins` before the move:** on SDK 57 and older, Node
  ESM (a plugin module referenced as `./plugins/x.ts`, scripts under `"type": "module"`) cannot
  resolve the bare specifier; `app.config.ts` itself, which Expo loads as CommonJS, accepts both, but
  keeps the house `.js` form (a `note` line). Keeping `expo/config-plugins.js` after the move breaks
  too, in every file that imports it, tests and test helpers included: SDK 58 resolves it to
  `config-plugins.js.js` (Node, Jest) and tsc fails with TS2307.
- **Mocking Reanimated to quiet Jest:** the mock loads the native initializers too; use the Reanimated
  resolver plus the asset-registry mapping.
- **Mixing builder and hook gestures** during the move: migrate each component completely.
- **`jest -u` over every golden, or a new screenshot baseline without looking:** open each diff;
  accept only what the change list explains.
- **`"image": "latest"` in eas.json, or an `sdk-<n>` alias left from the old SDK:** use `auto`,
  `sdk-<n>` of the current SDK or an exact image.
- **Selecting Xcode 27 on SDK 57 without scene support, or with `sudo xcode-select`.**
- **Leaving an `expo-build-properties` `compileSdkVersion`/`targetSdkVersion` or `ios.deploymentTarget`
  pin from an older SDK**, or keeping `newArchEnabled` and `android.edgeToEdgeEnabled` in the app config.
- **Moving an SDK 55 app to 56, or installing expo 57.0.8 or older:** go to the newest SDK 57 release.
- **Taking TypeScript 7, ESLint 10, a Node or npm move, or any held-back major along with the SDK.**

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/upgrade-policy.md](references/upgrade-policy.md) | Current and next SDK line, the three-part trigger, store deadlines, what moves together and what never does, toolchain policy in short, human steps, fact-check commands | Workflow step 1, and at session starts in an SDK window |
| [references/runbook.md](references/runbook.md) | The ordered steps with commands and expected output, the iOS and Android verification loop, commit, failure table, rollback, when multi-package, other package managers (Yarn, pnpm, Bun) | Workflow steps 5, 7 and 8, and when the repo has no package-lock.json |
| [references/sdk-58-changes.md](references/sdk-58-changes.md) | Every 57 to 58 change with its error text and fix: packages, root tools, overrides, config plugins, Jest resolver, Jest 30, Gesture Handler 3, Reanimated, Skia, React 19.3, React Native 0.88, Android AGP 9, iOS | Workflow step 5, and for each failing gate during the move |
| [references/toolchain.md](references/toolchain.md) | Where the Xcode version is recorded, Xcode selection, EAS images, scene support for SDK 57 with Xcode 27, Android SDK levels, AGP and JDK, store deadlines | Workflow step 6, and on a `scene-support`, `xcode`, `eas-image`, `android-sdk` or `store-deadline` failure |
| [references/sdk-lines.md](references/sdk-lines.md) | Every key of an SDK entry and the rule that reads it, the app's `contracts/expo-sdk-lines.json`, `rn-skills.config.json` keys, refreshing the data at each SDK release | Before writing an SDK entry; on `sdk-unknown` or `sdk-lines-contract` |
| [examples/sdk-move-report.md](examples/sdk-move-report.md) | The three developer messages (not yet, ready, done), the evidence list and the move commit, for a Tasks app | Workflow steps 2, 4 and 8 |
| `examples/expo-sdk-lines.json` | A complete repo-owned SDK entry (the SDK 58 snapshot) to start `contracts/expo-sdk-lines.json` from | When this skill lacks the app's new SDK |
| `templates/scripts/config/scene-support.ts` | `addSceneSupport(plugins)`: merges `ios.enableSceneSupport` into the `expo-build-properties` entry (tested) | Workflow step 6 (SDK 57 with Xcode 27) |
| `templates/scripts/config/scene-support.test.ts` | Its Jest tests (4 cases) | Copied with the template |
| `assets/sdk-lines.json` | Per-SDK expectations: React, test-renderer, @types/react, TypeScript and Jest lines, Gesture Handler major, config-plugin import, Jest config lines, Xcode and scene support, Android levels, EAS images, removed APIs and config keys | Read by the scripts |
| `assets/sdk-lines.schema.json` | The shape of an SDK entry (the skill's table and the app's contract) | When writing an entry |
| `assets/store-requirements.json` | App Store minimum Xcode and Google Play minimum targetSdk, with dates and sources | Read by `check-sdk-trigger.mjs`; add new store rules |
| `assets/expo-sdk-57-module-map.json` | Expo 57.0.27's `bundledNativeModules.json` (synced from the library, shared with dependency-management; do not edit here) | Read by the scripts when `node_modules` is absent |
| `assets/expo-sdk-58-next-module-map.json` | Expo 58.0.3's map (npm `next`, 2026-10-04); replaced by the stable map at the move | Read by the scripts when `node_modules` is absent |
| `assets/shared.json` | Declares the shared files copied into this skill | When adding a shared file |
| `scripts/check-sdk-trigger.mjs` | Is an SDK or toolchain move due? From npm facts (`--online` or `--facts`): `RESULT: PASS` = no move due, with `wait` reasons and dates; `FAIL [upgrade-due]` with this repo's plan; `FAIL [store-deadline]`; exit 2 without facts | Workflow step 2, at session starts in an SDK window, and after the move |
| `scripts/check-sdk-alignment.mjs` | Proves the repo sits on one SDK line (`--help` lists every rule); `--target-sdk` adds the readiness scan | Workflow steps 3 and 7, and after any SDK or toolchain change |
| `scripts/lib/sdk.mjs` | Helpers: the repo (single app or workspaces), SDK lines and the app's contract, module maps, code files, eas.json, Xcode sources, Android pins, versions and dates | Read only to change a script |
| `scripts/selftest.mjs` | Proves both scripts on five overlay suites: SDK 57, readiness for 58, SDK 58, multi-package, and the trigger on saved facts (one planted bug per `tests/fixtures/*/bad-*` case; pass cases pin SKIP, NOT APPLICABLE, notice and wait lines) | After changing a script, an asset, a template or a fixture |
| `scripts/check-lib.mjs` | Shared script helper, synced from the library (do not edit here) | Never by hand |
| `tests/bases/` | Base trees: a single app on SDK 57, the SDK 58 overlay, two apps and a shared package, saved trigger facts | When adding a case |
| `tests/fixtures/` | One folder per suite (`SUITE.json`) and per case (`EXPECT.txt`, `mutation.json`, `ARGS.txt`) | When adding a rule |

## Related skills

- `dependency-management` - single-package changes, the policy rows the move updates, held-back majors, the Node move.
- `unit-and-component-tests` - the Jest config, setup file and mocks the move touches (Jest 30).
- `golden-and-snapshot-tests` - reviewing and re-accepting goldens after a Skia or React Native change.
- `run-goldens-rebaseline` - the guarded re-accept of every golden when Jest 30 rewrites the snapshot headers.
- `native-modules-and-new-architecture` - rechecking `contracts/native-libraries.json` after the move.
- `ios-simulator-build`, `android-emulator-build` - clean prebuild, Release builds on named devices, Xcode selection.
- `eas-build-and-submit` - eas.json profiles and images, EAS builds.
- `e2e-maestro` - E2E flows and the screenshot matrix on the branch.
- `expo-prebuild-and-config-plugins` - local config plugins, `expo-build-properties`, AGP-sensitive plugins.
- `canvas-gestures-and-hit-testing`, `motion-and-animation`, `skia-canvas-rendering` - gesture, Reanimated and Skia code the change list touches.
- `ota-updates` - runtime versions across an SDK move.
- `quality-gates`, `git-commits-and-reporting` - the gate, the `Gate-Change:` trailer, the move commit and report.
- Expo's `expo-upgrade` skill - Expo's per-SDK migration guides (React 19, expo-av, React Navigation imports).
