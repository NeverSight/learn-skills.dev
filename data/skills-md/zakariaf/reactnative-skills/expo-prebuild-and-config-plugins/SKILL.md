---
name: expo-prebuild-and-config-plugins
description: Keeps ios/ and android/ generated from app.config.ts and tested config plugins. Use when adding a plugin, an Info.plist or AndroidManifest entry, or a prebuild step. Not for native code (native-modules-and-new-architecture).
---

# Expo prebuild and config plugins

Continuous Native Generation: `ios/` and `android/` are build output of `app.config.ts`, its config
plugins and the installed native packages. Every native change is a config key or one line in the
plugin list; local plugins are typed, idempotent and tested; the generated folders stay out of git
and out of every script's reach; a committed snapshot of the introspected native config makes each
native change visible in review. Two checkers prove it. Leaving this model is a recorded decision.

## Rules that must hold

1. **`app.config.ts` is the one config, and a pure function.** No `app.json`, `app.config.json` or
   second `app.config.*`; it returns the object synchronously, the same environment gives the same
   JSON, it holds no `null`, and it applies no plugin in code. Why: Expo reads `.ts` first and ignores
   the rest; a Promise is refused; the fingerprint hashes the config; `null` reaches the app as `{}`
   (all verified on SDK 57). (`single-config`, `config-evaluates`, `config-deterministic`,
   `config-null`, `config-mods`)
2. **`ios/` and `android/` are generated output.** `.gitignore` (and `.easignore`, which replaces it
   for EAS) ignores `/ios` and `/android`, anchored; git tracks nothing there; no npm script, `scripts/`
   file or CI step writes into them. Why: SDK 57's prebuild deletes them by default, EAS prebuilds
   only when they are absent, and an unanchored `ios/` also hides a local module's Swift code.
   (`native-ignored`, `native-tracked`, `native-ignore-scope`, `easignore-native`, `native-edit`)
3. **A config key before a plugin.** `ios.infoPlist`, `ios.entitlements`, `locales`,
   `android.permissions`/`blockedPermissions`, `ios.deploymentTarget` and expo-build-properties
   (SDK versions, `manifestQueries`, cleartext, frameworks) cover most needs; a plugin only for what
   none covers. Why: keys are validated, introspectable and maintained by Expo across upgrades.
   (`builtin-first`)
4. **Nothing reaches the native projects implicitly.** Every installed package whose plugin prebuild
   applies on its own (`assets/auto-plugins.json`) is listed, with the options the app means, in every
   variant; no plugin is listed twice; a permission a plugin adds whatever its options (expo-file-system's
   storage pair, which every app gets through `expo`) is removed only by `android.blockedPermissions`
   (exact case, `WRITE_EXTERNAL_STORAGE`): block it unless the app needs it (shared-storage access).
   Why: the defaults add push and Sign in with Apple entitlements, permissions and English purpose
   strings (seen in the reference app), and a run-once plugin silently drops a second entry's options
   (verified). (`auto-plugin-listed`, `plugin-duplicate`)
5. **Local plugins live in `plugins/with-<capability>.ts`, listed by path.** Default export (a typed
   `ConfigPlugin<Options | undefined>`, tagged `@public`), Expo's helpers from `'expo/config-plugins.js'`
   on SDK 57 (bare from SDK 58), never `@expo/config-plugins`. Why: `npx expo config` then shows the
   file; the bare specifier fails with `ERR_MODULE_NOT_FOUND` once Node imports the file as an ES
   module (verified). (`plugin-entry`, `plugin-import`)
6. **Typed mods first; text mods merge; dangerous mods are justified.** A text mod edits through
   `CodeGenerator.mergeContents` or behind an `includes` check (inline or in a `plugins/lib/` helper);
   `withDangerousMod` carries `// dangerous-mod: <reason>`, writes files only inside it (or helpers
   it calls), and writes them whole or guards an append. Why: only typed mods are
   introspected; dangerous mods run first and break silently when the SDK template changes.
   (`dangerous-mod`, `text-mod-idempotent`)
7. **Every plugin is idempotent and validates its options.** Applying it twice equals once; a bare
   entry or a bad option throws a message showing the right entry. Why: `prebuild --no-clean` and
   `expo run:*` rerun mods onto existing files (verified: an appending plugin left 1, 2, 3 copies).
8. **Every local plugin has a sibling test that imports it and that Jest runs, through Expo's own mod chain.** `runMod`
   (`test/config-plugins/run-mod.ts`), a fresh config per test, a second run, bad options, the other
   platform untouched; the Jest config's test roots include `plugins/`. Why: Expo ships no plugin
   test harness, the `with*` helpers mutate the config they get, and an unreached test passes silently.
   (`plugin-test`)
9. **One owner per native key, and a deliberate order.** Mods run newest first: the plugin listed
   first in `plugins` writes last and wins a shared key (verified). Two plugins on one file are tested
   together. Why: otherwise a reorder silently changes the app.
10. **Native changes are proven by introspection and reviewed as a snapshot.** `contracts/native-config.json`
    is regenerated with `--write` only after a deliberate change and committed with it. Why: the
    generated folders never appear in a pull request; the snapshot shows a new permission or entitlement
    from any plugin or package. (`native-snapshot`, `native-drift`)
11. **Prebuild is clean in scripts and CI, and before every local build.** Never `--no-clean` in a
    script; `npx expo prebuild --clean` before `expo run:*` or a local release build after any config,
    plugin, package or variant change. Why: `expo run:*` builds an existing folder as it is (verified);
    a layered prebuild depends on earlier runs. (`prebuild-clean`)
12. **Leaving CNG is a recorded decision.** `contracts/native-generation.json` `"mode": "committed"`
    with a `reason` and `decidedOn`, both folders committed, no prebuild in any script; native keys
    then change by hand. Why: committed folders and prebuild-only keys drift apart (expo-doctor reports
    it). (`native-mode`)

## Workflow

1. **Place the change.** Read [references/app-config.md](references/app-config.md) ("Built-in keys
   before plugins", "Auto-applied plugins"). A key covers it: edit `app.config.ts` and go to step 6.
   A new native package: dependency-management installs it, then list its plugin here (rule 4).
2. **First time in a repo:** read [references/cng-and-native-folders.md](references/cng-and-native-folders.md);
   copy `templates/contracts/native-generation.json` to `contracts/`; anchor `/ios` and `/android` in
   `.gitignore`; make sure the Jest config's test roots include `'<rootDir>/plugins/**/'`
   (unit-and-component-tests owns `jest.config.js`); copy `templates/test/config-plugins/run-mod.ts`
   and its test. Then `node ${CLAUDE_SKILL_DIR}/scripts/check-native-snapshot.mjs . --write` and read
   every key of `contracts/native-config.json`: it is the audit of what prebuild writes today.
3. **Write the plugin** when no key covers the need: read
   [references/config-plugins.md](references/config-plugins.md); copy
   `templates/plugins/with-android-optional-features.ts` and its test as the shape (or keep them when
   the app needs optional hardware); [examples/with-gradle-jvm-args.ts](examples/with-gradle-jvm-args.ts)
   shows a gradle.properties mod. Pure transform, option validation, one typed mod per file.
4. **Test it** per [references/testing-and-proof.md](references/testing-and-proof.md) (levels 1 and 2):
   `npx jest --ci --selectProjects unit --runTestsByPath plugins/<file>.test.ts`, and
   `npx jest --listTests | grep plugins/` lists it.
5. **List it** in `app.config.ts` by path, with its options and a comment naming the owning skill, the
   way [examples/app-config-plugin-list.ts](examples/app-config-plugin-list.ts) does. Variant-dependent
   options are computed in the config (app-variants-and-environment owns the variants).
6. **Prove it:** `APP_VARIANT=<v> EXPO_PUBLIC_APP_VARIANT=<v> npx expo config --type introspect --json`
   for each variant; `node ${CLAUDE_SKILL_DIR}/scripts/check-native-snapshot.mjs .` and read every
   `native-drift` line; when each one is intended, rerun with `--write`. Text or dangerous mods also
   get `npx expo prebuild --clean --no-install --platform <p>`, then the same with `--no-clean`, and a
   look at the generated file (the change appears once).
7. **Run the app's gates:** `npm run typecheck`, `npx eslint . --max-warnings 0`, `npx jest --ci`.
8. **Check:** `node ${CLAUDE_SKILL_DIR}/scripts/check-native-generation.mjs .` and the snapshot check.
   Each `FAIL` names the file, the rule and the fix; [references/pitfalls-and-rules.md](references/pitfalls-and-rules.md)
   explains every rule and error text. Fix and rerun until both print `RESULT: PASS`.
9. **Leaving or returning to CNG:** stop and ask the developer first; it changes how every later
   native change is made. Then follow "When to leave CNG" or "Coming back to CNG" in
   [references/cng-and-native-folders.md](references/cng-and-native-folders.md).
10. **Report** like [examples/native-change-report.md](examples/native-change-report.md): what changed,
    the snapshot diff, the proof commands and every `RESULT` line, and what a build still has to show.

## Definition of done

- [ ] `app.config.ts` is the only app config; it evaluates for every variant, twice the same, without `null`.
- [ ] Every native change is a config key or one entry in `plugins`; every installed auto-applied package is listed; no entry twice.
- [ ] Local plugins sit in `plugins/`, listed by path, default-export a typed plugin, import `expo/config-plugins.js` (SDK 57), use typed mods, guard text mods, justify dangerous ones.
- [ ] Each plugin's sibling test passes, applies the plugin twice, covers bad options, and `npx jest --listTests` lists it.
- [ ] Introspection reviewed for each variant; `contracts/native-config.json` regenerated on purpose and committed with the change.
- [ ] Text or dangerous mods: a clean and then a `--no-clean` prebuild show the change once.
- [ ] `.gitignore` ignores `/ios` and `/android` (anchored); git tracks nothing there; no script writes there or runs `--no-clean`; or the committed mode is recorded with its reason.
- [ ] Expected SKIP line only while the app has no Jest config: `SKIP jest.config.js [plugin-test] not yet created (unit-and-component-tests creates it)`. `note:` lines are information, not failures.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-native-snapshot.mjs .` prints `RESULT: PASS`
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-native-generation.mjs .` prints `RESULT: PASS`

## Anti-patterns

- **Opening `ios/` in Xcode to fix a setting, or `sed -i` on `AndroidManifest.xml` in a script.** The
  next prebuild erases it and the build differs by machine. Put it in a key or a plugin.
- **A plugin for something a key does.** `LSApplicationQueriesSchemes` belongs in `ios.infoPlist`,
  Android `<queries>` in expo-build-properties' `manifestQueries`, permissions in `android.permissions`.
- **Leaving an installed package off the plugin list "because it works".** Prebuild applies its plugin
  with defaults: an `aps-environment` entitlement the signing profile lacks, `RECORD_AUDIO` for an app
  that never records, generic English purpose strings App Review may find too vague.
- **`import withX from './plugins/with-x.ts'` and `withX(config)` in `app.config.ts`.** It works and it
  hides the plugin from `npx expo config`; list `'./plugins/with-x.ts'` instead.
- **`'expo/config-plugins'` on SDK 57** (or `'expo/config-plugins.js'` on SDK 58), or
  `'@expo/config-plugins'` at any time.
- **Appending to the manifest, a Gradle file or the Podfile without checking.** Every `--no-clean`
  run adds another copy; replace by identity or use `CodeGenerator.mergeContents`.
- **A shared `const BASE: ExpoConfig` in plugin tests.** The helpers write `config.mods` onto it and
  later tests run earlier tests' mods.
- **`npx expo run:ios` after changing the config, without a clean prebuild.** It builds the old project.
- **`npx expo prebuild --no-clean` in CI or a build script.** The output then depends on the runner's history.
- **`ios/` in `.gitignore` instead of `/ios`.** A local Expo module's native folder is never committed.
- **An `.easignore` that forgets `/ios` and `/android`.** EAS uploads the stale folders and skips prebuild.
- **`--write` on the native snapshot to make the check pass.** Read each drift line first; an unexpected
  permission is the finding.
- **Committing the native folders "for now".** Record the decision with its reason, or keep them generated.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/cng-and-native-folders.md](references/cng-and-native-folders.md) | Why generated folders; what SDK 57's prebuild does (clean default, package.json edits); `.gitignore`/`.easignore`; EAS and `expo run`; local modules; leaving and returning to CNG; timings | Workflow steps 2 and 9 |
| [references/app-config.md](references/app-config.md) | How Expo finds, loads and serializes the config; context; determinism; what ships; `expo config` types; built-in keys before plugins; auto-applied plugins; variants | Workflow step 1 |
| [references/config-plugins.md](references/config-plugins.md) | Resolution and errors, local plugin form, imports per SDK, typed/text/dangerous mods, mod order, idempotence, options, run-once, lifecycle code in modules | Workflow step 3 |
| [references/testing-and-proof.md](references/testing-and-proof.md) | The four proof levels, `runMod` recipes, Jest reach, introspection and the snapshot, prebuild checks, blind spots, CI | Workflow steps 4 and 6 |
| [references/pitfalls-and-rules.md](references/pitfalls-and-rules.md) | Symptoms with causes and fixes, every rule of both checkers, options, config keys, expected lines | Workflow step 8, whenever something fails |
| `templates/plugins/with-android-optional-features.ts` | A complete local plugin: optional Android hardware features (`<uses-feature required="false">`) | Workflow step 3 |
| `templates/plugins/with-android-optional-features.test.ts` | Its tests: through `runMod`, iOS untouched, replace and keep, idempotent, bad options | With the plugin |
| `templates/test/config-plugins/run-mod.ts` | Runs the mods queued for one native file the way prebuild does, on test contents | Workflow step 2 |
| `templates/test/config-plugins/run-mod.test.ts` | Its tests, including mod order and the mutation of the config | With `run-mod.ts` |
| `templates/contracts/native-generation.json` | The native-folder model: `generated` (default) or `committed` with reason and date | Workflow step 2; leaving CNG |
| [examples/app-config-plugin-list.ts](examples/app-config-plugin-list.ts) | The shape of a Tasks app's plugin list, one owner comment per line | Workflow step 5 |
| [examples/with-gradle-jvm-args.ts](examples/with-gradle-jvm-args.ts) | A gradle.properties plugin shape (replace by key) | Workflow step 3 |
| [examples/native-change-report.md](examples/native-change-report.md) | A report with real snapshot drift and proof output | Workflow step 10 |
| `scripts/check-native-generation.mjs` | The CNG checker: config, plugin list, local plugin sources and tests, native folders, scripts, contract | Workflow step 8 |
| `scripts/check-native-snapshot.mjs` | Introspects the native config, compares it with `contracts/native-config.json`; `--write` regenerates it | Workflow steps 2 and 6 |
| `scripts/lib/cng-scan.mjs` | Helpers: ignore-file matcher, config evaluation, plugin entries, Jest reach | Only when changing a checker |
| `scripts/lib/source-scan.mjs` | Dependency-free source lexer (synced from the library; do not edit here) | Only when changing a checker |
| `scripts/check-lib.mjs` | Shared checker library (synced from the library; do not edit here) | Never by hand |
| `scripts/selftest.mjs` | Runs both checkers against the fixtures | After changing a checker, a template or the data |
| `tests/bases/` | The fixture base apps: a Tasks app (with planted decoys added by the suite) and a saved introspection with its snapshot | When adding a fixture |
| `tests/fixtures/` | Overlay cases per checker: good, one bad case per rule, pass and error cases | When adding a rule |
| `assets/auto-plugins.json` | The packages SDK 57's prebuild applies on its own, the exempt ones, observed defaults, and the permissions only `blockedPermissions` removes | When the SDK moves |
| `assets/shared.json` | The shared files this skill syncs in | When adding a shared file |

## Related skills

- `app-variants-and-environment` - `app.config.ts` identities per variant and the `APP_VARIANT` resolver this config calls.
- `dependency-management` - installing the native package before its plugin is listed.
- `native-modules-and-new-architecture` - native code in a local Expo module (Expo's official `expo-module` skill is the API reference).
- `unit-and-component-tests` - the Jest config whose test roots must include `plugins/`.
- `typescript-and-lint-rules` - the Node-code lint block and `.gitignore` for `app.config.ts` and `plugins/`.
- `naming-conventions` - `plugins/with-<capability>.ts` and the `with<Capability>` export.
- `architecture-and-boundaries` - app code never imports `app.config.ts` or `plugins/`.
- `expo-sdk-upgrade` - the SDK move (the import spelling flip, template changes plugins must survive).
- `ios-simulator-build`, `android-emulator-build` - clean prebuild and builds on named devices.
- `eas-build-and-submit` - EAS profiles; EAS runs prebuild when the folders are absent.
- `ota-updates` - runtime versions from the fingerprint, which hashes this config and its plugins.
- `permissions-and-system-prompts`, `privacy-and-store-declarations` - purpose-string wording and the store declarations the native snapshot feeds.
- `expo-project-bootstrap` - a new app's first config and `.gitignore`.
