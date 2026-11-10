---
name: native-modules-and-new-architecture
description: Writes New Architecture native code in typed local Expo modules. Use when adding Swift or Kotlin, a local or Turbo module, codegen, or checking a library for New Architecture. Not for config plugins (expo-prebuild-and-config-plugins).
---

# Native modules and the New Architecture

Makes the app's own native code safe to own on iOS and Android: native code only where no package
fits, written with the Expo Modules API in a local module under `modules/<name>/`, reached through one
typed, lazy, optional binding in its adapter behind a port, with the binding type and the Swift and
Kotlin definitions proven equal; Turbo Modules only where shared C++ or publishing needs them; and
every third-party native library either native on the New Architecture or a recorded decision. Two
zero-dependency checkers prove it.

## Rules that must hold

1. **Native code comes last, and lives in a local Expo module.** First an Expo SDK package, then a
   library that is native on the New Architecture, then a config plugin; only then a local module made
   by `npx create-expo-module@latest --local`, in Swift and Kotlin with the Expo Modules API. No native
   source outside `modules/<name>/` (no inline modules, no edits to generated `ios/`/`android/`) and no
   legacy bridge code (`RCT_EXPORT_MODULE`, `ReactContextBaseJavaModule`, `@ReactMethod`). Why: SDK 55 <!-- stack-pin-ignore: the release that changed it -->
   and later run only on the New Architecture, legacy modules run only through interop layers React
   Native will remove, and native code outside the module is never built or reviewed.
   (`native-placement`, `legacy-native-api`)
2. **The module folder is complete.** `expo-module.config.json` declares each platform and lists every
   `Module` class (Swift class names, Kotlin full names); every listed class exists, extends `Module`
   and is `public` in Swift; `ios/*.podspec` depends on `ExpoModulesCore`; `android/build.gradle`
   applies `expo-module-gradle-plugin`. Why: autolinking registers only listed classes, and a missing
   piece fails one platform's build or leaves the module unreachable.
   (`module-config`, `module-class`, `module-build-files`)
3. **One JavaScript name per module.** `Name("TimeChange")` is written explicitly, is identical in
   Swift and Kotlin, and is unique in the app. Why: the name is the lookup key; inferred or differing
   names find the module on one platform only. (`module-name`)
4. **One binding per module, in its adapter, behind a port.** `requireOptionalNativeModule` and
   `requireNativeView` appear only in the module's adapter, `src/services/<concern>/native-<concern>-adapter.ts`
   (the checker accepts any `<library>-<concern>-adapter.ts(x)` in `src/services`, following
   architecture-and-boundaries), with a literal name a local module or spec defines; every module is
   bound, by exactly one adapter (platform variants `-adapter.ios.ts`/`.android.ts` count as one);
   `TurboModuleRegistry.get` appears only in a codegen spec (`Native<Name>.ts`); no
   `NativeModules`, `requireNativeComponent`, `NativeEventEmitter` or `UIManager`. The port, fake and
   composition root follow architecture-and-boundaries. Why: one line reaches native code, so one
   place guards it and everything above it runs in Jest on the fake; a second binding is a second,
   unguarded copy of the contract. (`binding-place`, `binding-unique`, `binding-name`, `codegen-spec`,
   `legacy-js-api`)
5. **The binding is lazy and optional.** The lookup runs in the factory's default parameter, never at
   module scope, and uses `requireOptionalNativeModule` for both kinds of module (for a Turbo Module it
   falls back to `TurboModuleRegistry.get`): a missing module becomes a typed `unavailable` failure.
   Why: the module is missing in Jest, on web, in a dev client or store build older than the module,
   and when an update reaches an older binary; the throwing forms crash at import there.
   (`binding-lazy`, `binding-optional`)
6. **The binding type is the cross-language contract.** `requireOptionalNativeModule<TimeChangeBinding>`
   names a type declared in the adapter that lists every native function, property and event by its
   native name, and nothing else; Swift, Kotlin and the type change in one commit. Why: the Expo Modules
   API has no cross-platform codegen (`expo-type-information` drafts a type from Swift only), so a
   renamed member compiles everywhere and fails at runtime. For a Turbo Module the codegen spec is the
   contract: bind `requireOptionalNativeModule<Spec>(...)` with `import type { Spec }` from its
   `Native<Name>.ts`; a hand-written type is compared with the spec. (`binding-type`, `contract-drift`)
7. **Same surface on iOS and Android, or a declared difference.** A member one platform lacks is
   optional in the binding type (`isAutomaticTimeEnabledAsync?()`) and the adapter maps its absence to
   `unsupported`; a one-platform module says so in `platforms`. Why: an undeclared gap is "is not a
   function" on one platform only, found by users. (`platform-parity`)
8. **Definitions stay thin, respect threads and release what they observe.** Each closure calls a plain
   helper that imports no Expo type; `Function`/`Property`/`Constant` only do cheap reads; UI work runs
   in `AsyncFunction(...).runOnQueue(.main)` (`Queues.MAIN`); OS observation starts in
   `OnStartObserving`, stops in `OnStopObserving` (same event, or the unnamed form) and `OnDestroy` in
   the Module itself, and every observer or receiver added is removed in the same file. Why: sync
   functions block the JavaScript thread, async ones default to a background queue, and a leaked
   observer keeps firing and keeps the module alive; a helper with a correct `stop()` still leaks when
   the Module never calls it. (`main-thread`, `observer-release`, `observer-stop`)
9. **Turbo Modules only for shared C++ or publishing, built as a local package.** `modules/<name>/` with
   `package.json` `codegenConfig` (`name`, `type`, a `jsSrcsDir` holding specs,
   `android.javaPackageName`), its podspec at the package root, specs named `Native<Name>.ts` declaring
   `export interface Spec extends TurboModule`; never `codegenConfig` in the app's `package.json`. Why:
   codegen reads only those files, autolinking looks for a React Native module's podspec only at its
   root, and CNG deletes app-level native code. (`codegen-config`, `codegen-spec`)
10. **Every native dependency runs on the New Architecture natively, or is a recorded decision.** A
    dependency without `expo-module.config.json`, `codegenConfig` or a Nitro marker has an entry in
    `contracts/native-libraries.json` (architecture, keep or replace, reason, evidence, `recheckBy`);
    entries stay true and are rechecked by their date. Why: such a library runs through the interop
    layer, whose limits and removal the app must plan for, not discover.
    (`library-legacy`, `library-entry`, `library-stale`, `library-recheck`)
11. **expo-doctor's React Native Directory check stays on.** No `enabled: false`; every exact-name
    `exclude` has a decision entry; no regex exclusions. Why: the directory check is the only automatic
    warning for unmaintained or New-Architecture-incompatible packages. (`doctor-check`)
12. **Proven on both platforms before done; a native change is a new binary.** Jest covers the fake and
    the adapter's mapping; `npx expo-modules-autolinking resolve` lists the module for apple and
    android; the Swift type-checks and the Kotlin helpers compile (testing-and-proof.md); a dev client
    on a named simulator and emulator exercises every member. Why: Fast Refresh and over-the-air
    updates never carry native code, and each layer catches what the others cannot.
13. **Stop and ask before** a new native module, a Turbo Module instead of an Expo module, keeping an
    interop library, an expo-doctor exclusion, or a `nativeSourceDirs` entry. Why: each binds the app
    for every later SDK and OS move.

## Workflow

1. **Decide whether native code is needed.** Read [references/decisions.md](references/decisions.md)
   sections 1 to 4; walk the order of reach. A native package: go to step 7. Ask the developer before
   writing a module (rule 13).
2. **Create the module.** From the app root:
   `EXPO_NONINTERACTIVE=1 npx create-expo-module@latest --local <name> --name <Pascal> --platform apple android --features Function AsyncFunction Event`.
   Delete its `src/` folder (the binding lives in the adapter). Shape it like
   `templates/modules/time-change/` (config, podspec, Gradle file, a thin `<Pascal>Module` per platform
   over a plain `<Pascal>System` helper). API details: [references/expo-modules-api.md](references/expo-modules-api.md).
3. **Write the port, fake and adapter.** Copy `templates/src/services/time-change/` as the pattern:
   `<concern>-port.ts` (Result failures, unsubscribe), `fake-<concern>.ts` + test first, then
   `native-<concern>-adapter.ts` with the binding type, the lazy optional binding and the error mapping,
   and its test against a stand-in native object. Wire it as
   [examples/wiring-the-port.md](examples/wiring-the-port.md) shows (architecture-and-boundaries owns the
   composition root).
4. **Need shared C++ or a module for non-Expo apps?** Read
   [references/turbo-modules-and-codegen.md](references/turbo-modules-and-codegen.md) and follow
   [examples/turbo-module/](examples/turbo-module/) instead of steps 2 and 3's module half.
5. **Check the contract:** `node ${CLAUDE_SKILL_DIR}/scripts/check-native-modules.mjs .`; fix every
   `FAIL` line and rerun.
6. **Prove it builds and links** ([references/testing-and-proof.md](references/testing-and-proof.md)):
   `npm test`, `npx expo-modules-autolinking resolve --platform apple --json` and `--platform android`,
   the Swift type-check, the Kotlin helper compile; then a dev client on a named iOS simulator and
   Android emulator (ios-simulator-build, android-emulator-build), every member on both, and the manual
   check for OS events.
7. **Check native libraries.** After `npm ci`:
   `node ${CLAUDE_SKILL_DIR}/scripts/check-native-libraries.mjs .` and `npx expo-doctor`. An `interop`
   library: replace it, wrap what you need in a module, or (after asking) record it in
   `contracts/native-libraries.json` from `templates/contracts/` ([examples/native-libraries.json](examples/native-libraries.json);
   [references/library-compatibility.md](references/library-compatibility.md)).
8. **Run both checks** until each prints `RESULT: PASS`.

## Definition of done

- [ ] No package covered the need, and the developer agreed to native code; the module is in
      `modules/<name>/`, written with the Expo Modules API (or a Turbo Module package for shared C++ or
      publishing), with no native source elsewhere.
- [ ] `expo-module.config.json`, podspec and Gradle file complete; one explicit `Name()` on both platforms.
- [ ] One typed, lazy, optional binding in `native-<concern>-adapter.ts`; the binding type lists exactly
      the native members and events; platform gaps optional and mapped to `unsupported`.
- [ ] Port, fake (+ test) and adapter test in Jest; `npm test` passes.
- [ ] `npx expo-modules-autolinking resolve` lists the module for apple and android; the Swift
      type-checks; a dev client ran every member on a named simulator and emulator.
- [ ] Every interop library has a current decision entry; expo-doctor's directory check is on.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-native-libraries.mjs .` prints `RESULT: PASS` (after
      `npm ci`; `note:` lines name transitive interop packages with their parent, and native devDependencies).
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-native-modules.mjs .` prints `RESULT: PASS`

Neither checker prints SKIP lines. Each prints `NOT APPLICABLE` when `expo` (modules) or `react-native`
(libraries) is not a dependency. `check-native-libraries` exits 2 without `node_modules`.

## Anti-patterns

- **`export default requireNativeModule<...>('X')` as `create-expo-module` writes it.** It runs at
  import and throws in Jest, on web and in older binaries; bind in the adapter factory with
  `requireOptionalNativeModule`.
- **`import { NativeModules } from 'react-native'`, or `requireOptionalNativeModule` in a screen or
  hook.** Native code then reaches untested layers; take the port from `useServices()`.
- **An untyped binding, or a type that "roughly" matches.** Nothing catches `getTimeZone` versus
  `getTimeZoneId` until a user calls it; list the native members exactly.
- **A function added to Kotlin only.** It works on Android and is "not a function" on iOS; implement it
  on both, or make it optional in the binding and map the gap.
- **Business logic inside `definition()` closures.** It cannot be compiled, read or tested alone; call a
  plain helper.
- **`addObserver` in `OnStartObserving` with no `removeObserver`, or a helper's `stop()` the Module
  never calls.** Events keep arriving after the screen closed; stop in `OnStopObserving` and `OnDestroy`.
- **A second adapter that binds a module already bound.** Two copies of the contract drift apart;
  take the first adapter's port instead.
- **UIKit in a `Function`, or in an `AsyncFunction` without `.runOnQueue(.main)`.** Main Thread Checker
  warnings in debug, corrupted UI in release.
- **Swift or Kotlin beside screens through `experiments.inlineModules`.** Experimental, outside every
  rule and review; use `modules/<name>/`.
- **A Turbo Module "for performance" with no C++ to share.** The Expo Modules API is JSI-based too, with
  far less code; codegen earns its cost only for shared C++ or publishing.
- **`codegenConfig` in the app's package.json.** Its native half would live in generated folders that
  a clean prebuild deletes.
- **Silencing expo-doctor with `enabled: false` or `"/react-native-.*/"`.** It hides every future
  warning; exclude exact names with a recorded decision.
- **Testing native behaviour only in Jest.** Jest proves the mapping; only a dev build proves the OS
  sends what the module claims.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/decisions.md](references/decisions.md) | The order of reach, Expo module vs Turbo Module vs legacy vs inline, file layout, the binding design, platform gaps, views, native changes and updates | Workflow step 1; any design question |
| [references/expo-modules-api.md](references/expo-modules-api.md) | create-expo-module output, the config, definition components, types, threads, events, errors, lifecycle, views, the JavaScript side, iOS vs Android | Workflow step 2 |
| [references/turbo-modules-and-codegen.md](references/turbo-modules-and-codegen.md) | Turbo Modules as local packages, specs, codegenConfig, native halves, linking proof, Fabric components | Workflow step 4 |
| [references/library-compatibility.md](references/library-compatibility.md) | Interop facts for React Native 0.86, classifying packages, expo-doctor's directory check, the decisions file, transitive packages | Workflow step 7 |
| [references/testing-and-proof.md](references/testing-and-proof.md) | Jest layers, the contract check, autolinking proof, Swift type-check and Kotlin compile recipes, device checks, problems and fixes | Workflow steps 3, 5 and 6 |
| `templates/modules/time-change/` | A complete local Expo module: config, podspec, Gradle file, manifest; Swift and Kotlin definitions over plain helpers (time zone, clock and day changes) | Workflow step 2 (copy the shape, or adopt it) |
| `templates/src/services/time-change/time-change-port.ts` | The port: Result failures, an unsubscribe for events | Workflow step 3 |
| `templates/src/services/time-change/native-time-change-adapter.ts` | The one binding: binding type, lazy optional lookup, error and event mapping | Workflow step 3 |
| `templates/src/services/time-change/native-time-change-adapter.test.ts` | The adapter against a stand-in native object, and the null lookup under Jest | Workflow step 3 |
| `templates/src/services/time-change/fake-time-change.ts` | The port's fake with emit, listener count and a call log | Workflow step 3 |
| `templates/src/services/time-change/fake-time-change.test.ts` | Its test | Workflow step 3 |
| `templates/contracts/native-libraries.json` | The empty decisions file | Workflow step 7 |
| `templates/contracts/native-libraries.schema.json` | Its JSON schema | Workflow step 7 |
| [examples/wiring-the-port.md](examples/wiring-the-port.md) | Services, composition root, test services, a model hook that subscribes | Workflow step 3 |
| [examples/turbo-module/](examples/turbo-module/) | A local Turbo Module package: spec, codegenConfig, root podspec, Objective-C++, Kotlin, package, shared C++ reached through JNI and CMake on Android | Workflow step 4 |
| [examples/native-libraries.json](examples/native-libraries.json) | A filled decisions file (keep and replace) | Workflow step 7 |
| `scripts/check-native-modules.mjs` | Checks modules (config, classes, build files, names, parity, threads, observers, legacy code), bindings and the contract, codegen, placement | Workflow step 5; definition of done |
| `scripts/check-native-libraries.mjs` | Classifies installed native dependencies; checks the decisions file and expo-doctor's directory check | Workflow step 7; definition of done |
| `scripts/lib/native-scan.mjs` | Swift/Kotlin class and definition reader, binding and binding-type parser, package classifier | Only when changing a checker |
| `scripts/lib/source-scan.mjs` | Dependency-free lexer (synced from the library; do not edit here) | Only when changing a checker |
| `scripts/check-lib.mjs` | Shared script helper (synced from the library; do not edit here) | Never by hand |
| `scripts/selftest.mjs` | Proves both checkers pass the templates and example and catch every planted bug | After changing a checker |
| `assets/shared.json` | Declares the synced files | When adding a shared file |
| `tests/` | The base apps and the overlay cases (one planted bug per rule) | When adding a rule |

## Related skills

- `architecture-and-boundaries` - ports, adapters, fakes, the composition root; `modules/<name>/` as an SDK only its adapter reaches.
- `expo-prebuild-and-config-plugins` - Info.plist, manifest and entitlement changes a module needs; generated folders.
- `dependency-management` - installing and pinning a native library before this skill's compatibility check.
- `expo-sdk-upgrade` - SDK moves, removed `newArchEnabled`, rechecking interop decisions.
- `unit-and-component-tests` - render helpers and test services for code above the adapter.
- `error-handling-typed-results` - the Result and failure kinds the port returns.
- `async-safety` - effect cleanup for subscriptions to module events.
- `ios-simulator-build`, `android-emulator-build` - dev builds on named devices.
- `e2e-maestro` - flows that exercise native features on both platforms.
- `ota-updates` - runtime versions: why native changes need a new binary.
- `permissions-and-system-prompts` - a module that needs a runtime permission asks through that port.
- `troubleshooting-playbook` - the wider error catalog.
