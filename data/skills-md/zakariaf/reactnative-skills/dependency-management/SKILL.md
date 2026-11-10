---
name: dependency-management
description: Adds, upgrades and removes npm packages in Expo apps under a written policy - expo install, exact pins, 7-day release age, script review, licences. Use when adding or bumping a package or on ETARGET. Not for SDK majors (expo-sdk-upgrade).
---

# Dependency management

Keeps every package of an Expo app on a written, verified set: the right version and specifier, in
the right place, old enough, not deprecated, reviewed, allowed to ship, and installed once. The facts
live in the app's `contracts/dependency-policy.json`; this skill seeds it, plans every change, and
proves the repo against it.

## Rules that must hold

1. **One written policy.** `contracts/dependency-policy.json` holds the versions table (version,
   specifier, place, why), held-back majors, do-not-add, bans and the licence policy, seeded from
   `templates/contracts/dependency-policy.json` (the canonical stack verified 2026-10-03, Expo SDK
   57). A row changes in the same commit as `package.json` and `package-lock.json`. *Why:* npm
   `latest` is the wrong major for several packages today (React Native 0.87, TypeScript 7, ESLint 10,
   Jest 30); one written truth stops upgrades from memory.
2. **Install Expo-managed packages only with `npx expo install <pkg>@<row spec>`, and keep the
   specifier it writes.** *Why:* Expo tests one native set per SDK and `expo install --check` verifies
   it; without the spec, `npx expo install` writes whatever Expo's online list names today, which can
   be a patch published that morning. A same-day Expo patch is a `WARN` with its due date, never an
   install.
3. **Pin every other package exactly, in its place** (`save-exact=true`): runtime code in
   `dependencies`, tools in `devDependencies`. *Why:* a patch of a native wrapper changes binaries;
   Expo's checks only test that the installed version is inside its range, so the exact pin is what
   makes each change a reviewed lockfile commit.
4. **One copy of everything.** Companions a row lets float are installed in the same command or
   pinned in the root `overrides` (all ten `@typescript-eslint/*` at the `typescript-eslint` pin);
   one `react`, one `react-native`; `npm ls <pkg>` shows one version. *Why:* two `@typescript-eslint`
   plugins crash ESLint, and a native module can be compiled into a build only once.
5. **Commit `package-lock.json`, install clean trees with `npm ci` (EAS Build does too), and never
   delete the lockfile, set `package-lock=false`, use `--force` / `--legacy-peer-deps` (on the
   command line, in `.npmrc` or in an `NPM_CONFIG_*` variable), or set `EAS_NO_FROZEN_LOCKFILE`.**
   *Why:* the lockfile is what makes every machine and CI build the same app: EAS Build runs
   `npm ci` and fails on a lockfile out of sync, while `npm install` (what developers run, and EAS
   Build under `EAS_NO_FROZEN_LOCKFILE`) ignores it under `package-lock=false`; `ETARGET` means too
   young, `ERESOLVE` means off the SDK set, and `legacy-peer-deps=true` silences that for every
   later install.
6. **`.npmrc` holds `min-release-age=7` (or a stricter number of days), `engine-strict=true`,
   `save-exact=true` and `strict-allow-scripts=true`; the root `package.json` holds `engines`
   `npm >=11.17.0` and `node >=22.18`; nothing weakens them: no later line, no `before=`, no
   `NPM_CONFIG_*` variable in `eas.json` or CI, no `~/.npmrc` line the project file leaves open.** A
   younger release enters only through a dated `# exclude-block expires=YYYY-MM-DD reason=…` block
   the developer agreed to, naming exact packages, expiring on the publish date + the release age,
   deleted (never extended) on that date. *Why:* a 7-day wait lets most malicious or broken releases
   be pulled first; npm keeps the last value of a key and reads command line, then environment, then
   project `.npmrc`, then `~/.npmrc`; `engine-strict` guards nothing without `engines`, and the npm
   of the default EAS images ignores the release age and `allowScripts`.
7. **Review an install script before it runs, one package at a time.** With
   `strict-allow-scripts=true` npm stops an install whose tree holds an unreviewed script before
   anything runs (`ESTRICTALLOWSCRIPTS`); without it npm 11.17 runs the script and only prints a
   notice afterwards. Read the script the plan prints, write its pinned key
   (`"<pkg>@<x.y.z>": true`) into the root `allowScripts`, then install; a bump needs a new review.
   Never a name-only approval (`"<pkg>": true`, `"<pkg>@*": true`): npm runs every future version's
   script under it; a name-only `false` (deny every version, what `npm deny-scripts` writes) is
   fine. npx and `npm exec` inside the repo follow `.npmrc` but never the root `allowScripts`: a
   tool the repo runs is a devDependency (npx then runs the reviewed local copy), EAS CLI (expo-doctor
   refuses it as a dependency) a global install with the policy flags, and `allow-scripts` stays out
   of every `.npmrc` and variable. *Why:* an install script runs arbitrary code on every machine and
   CI runner that installs.
8. **Never add a banned package:** the supply-chain floor (compromised or deprecated packages), plus
   the app's own bans and opt-in profiles (`offline-only`, `no-telemetry`), all listed in the
   policy's `banned`. *Why:* the app's own gate reads only the policy, so the list is complete there.
9. **No deprecated direct dependency without a written reason in its row.** *Why:* deprecated code
   gets no fixes; a deliberate hold (ESLint 9, held back) stays visible instead of silent.
10. **Ship only allowed licences** (by default MIT, ISC, Apache-2.0, BSD-2/3-Clause, 0BSD, OFL-1.1,
    CC0-1.0) or an approved exception with its exact licence and reason; audit the release bundle,
    not the lockfile, and read the native SDKs a native module brings by hand. *Why:* only shipped
    code carries obligations into the app, and the bundle audit sees JavaScript only: the CocoaPods
    and Gradle SDKs under a native module (an ads or crash SDK) ship too.
11. **`npx expo install --check` and `npx expo-doctor` pass.** *Why:* they see SDK drift and
    duplicate native modules that `tsc` and Jest cannot.
12. **Respect held-back majors until their written triggers; move Expo SDK majors only with the
    expo-sdk-upgrade skill.** *Why:* each held-back major breaks a verified part of the stack.
13. **Install a package in the same change as the code that uses it.** *Why:* an unused package ages
    unreviewed, and knip cannot see an unused native module once a shared package peers it.
14. **Stop and ask the developer before a package not in the policy, a dated exception, a licence
    exception or a deprecation hold,** bringing the facts `plan-dependency.mjs --online` prints.
15. **Read a library's versioned docs before coding against it, never memory,** and re-verify a row
    before trusting it when the policy's `verified` date is more than a few weeks old.

When multi-package (npm workspaces), rules 3 and 4 also mean: a native module is never in a shared
package's `dependencies` or at the root (Expo's checks verify only an app's direct dependencies, and
only one copy of a native module can be compiled); a shared package lists the native modules its code
imports as `"*"` peers; every app that depends on it installs them with one specifier; the root
`overrides` pin each peer at the apps' version, plus `react` and `react-native`. A JavaScript library
the apps and a shared package both import is one row whose `where` lists both places.

## Workflow

1. Name the task: add, upgrade, remove, the monthly pass, a dated exception, or a failing dependency
   gate. A failing gate: go straight to "When a gate in this area fails" in
   [references/supply-chain.md](references/supply-chain.md).
2. No `contracts/dependency-policy.json` yet: copy `templates/contracts/dependency-policy.json`,
   delete the rows the app will never use, and read
   [references/policy-contract.md](references/policy-contract.md). No `.npmrc`: copy
   `templates/dot-npmrc` to `.npmrc`.
3. Read the package's row (and [references/versions.md](references/versions.md) for why the seed
   says what it says), then the matching section of
   [references/procedures.md](references/procedures.md).
4. Plan: `node ${CLAUDE_SKILL_DIR}/scripts/plan-dependency.mjs <pkg>[@<version>] . --online` (add
   `--remove` to remove; when multi-package, `--peer-of <workspace>` when a shared package imports it;
   offline, save `npm view <pkg>@<v> version time license scripts deprecated --json` to a file and
   pass `--npm-view <file>`). A `FAIL` line (`banned`, `do-not-add`, `held-back`, `not-in-table`,
   `version-differs`, `too-young`, `deprecated`, `licence`) means stop: fix the request, follow the
   upgrade procedure, or ask the developer.
5. Too young but needed: read [references/release-age-policy.md](references/release-age-policy.md),
   get the developer's agreement, fill `assets/npmrc-exclude-block.txt` (expiry = the publish date +
   the `.npmrc` min-release-age; the plan's `too-young` fix line prints it) and append it to `.npmrc`
   after one blank line.
6. Review before installing: when the plan prints a `review first` step, read that script and write
   its pinned key into the root `allowScripts` ([references/supply-chain.md](references/supply-chain.md),
   "Install scripts"). An install that stops with `ESTRICTALLOWSCRIPTS` ran nothing: review each
   package it names the same way, then run the install again. A tool run through npx (EAS CLI, a
   scaffolder) follows "npx and one-off tools inside the repo" in the same reference instead.
7. Run the printed install steps exactly, in order (companions in the same command; when
   multi-package, the peer and its root override first, then every app in the same change). Then
   `npm approve-scripts --allow-scripts-pending` must print `No packages with unreviewed install
   scripts.`
8. A config plugin: one entry in the `plugins` list of `app.config.ts`, with a comment naming the
   owning skill; never a second list, never an edit in the generated `ios/` or `android/`. A package
   whose plugin prebuild applies on its own (`expo-notifications`, `expo-image-picker`, ...) is
   listed even when its defaults are wanted (expo-prebuild-and-config-plugins, `auto-plugin-listed`).
9. Write the code that uses the package in the same change; a vendor SDK is imported only by its
   adapter in `src/services/<concern>/`.
10. `npx expo install --check` and `npx expo-doctor` (inside each Expo app when multi-package, plus
    `npx expo-modules-autolinking verify` for duplicate native modules).
11. Run `node ${CLAUDE_SKILL_DIR}/scripts/check-deps-policy.mjs .`; fix every `FAIL` line (each names
    the file, the rule and the fix) and rerun until `RESULT: PASS`. Then `npm run -s check:fast` and
    `npm run -s check:unused`.
12. A native or pre-1.0 package: `npx expo prebuild --clean`, a development build on a named iOS
    simulator and a named Android emulator (or `eas build --profile development` with a simulator
    profile: `ios.simulator: true`, an APK for Android; eas-build-and-submit owns the profiles);
    read what the config plugin changed (`npx expo config --type introspect`: iOS usage strings,
    plugin-written manifest entries), the Android permissions in the merged manifest or the built
    APK (library manifests and Play services add them at build time; the procedures reference says
    where), the new vendor SDKs in `ios/Podfile.lock` and `./gradlew :app:dependencies`, and any
    binary the build downloads (podspec `prepare_command`, Gradle download tasks), for the
    privacy-and-store-declarations skill. Before the next release, also launch a preview or release
    build on both (R8, Hermes bytecode and release-only plugin branches never run in development).
13. Commit as in [references/procedures.md](references/procedures.md) ("What to record in the
    commit"), following [examples/add-expo-haptics.md](examples/add-expo-haptics.md).
14. A gate file under `scripts/deps/`, `scripts/audit/` or `scripts/clock/` missing or damaged:
    restore it from `templates/scripts/` (the path its first line names) and rerun its Jest tests.
    The root `package.json` runs them through `"check:deps": "node scripts/deps/check-deps.ts"`
    (quality-gates calls it in `npm run verify`), `"check:npm-config": "node
    scripts/deps/check-npm-config.ts"` and `"audit:licenses": "node scripts/audit/audit-licenses.ts"`
    (after `npm run export:audit`, the production release export with source maps).

## Definition of done

- [ ] Every changed package is at its row's version and specifier, in its row's place, with its
      companions installed in the same command or pinned in the root `overrides`.
- [ ] `npm ls <pkg>` shows one version for every package the change touched, and for `react`,
      `react-native` and `@typescript-eslint/eslint-plugin`.
- [ ] The policy rows changed in the same commit as `package.json` and `package-lock.json`.
- [ ] Every new install script was read before it ran (the plan's `review first` step or an
      `ESTRICTALLOWSCRIPTS` stop) and is approved by its pinned key (no name-only `true`);
      `npm approve-scripts --allow-scripts-pending` prints `No packages with unreviewed install
      scripts.`
- [ ] `node scripts/deps/check-npm-config.ts` passes on the machine and in CI: the config npm runs
      with (`npm config get min-release-age strict-allow-scripts legacy-peer-deps package-lock
      before allow-scripts`) is the policy, not an `NPM_CONFIG_*` variable or `~/.npmrc` line.
- [ ] No committed npx call (package.json scripts, workflows, `lefthook.yml`) installs a package the
      policy keeps out; EAS CLI runs from a pinned global install with the policy flags.
- [ ] `npx expo install --check` and `npx expo-doctor` pass (an Expo patch younger than 7 days is a
      `WARN` line with its due date from `scripts/deps/check-deps.ts`, reported, not installed);
      `npm run -s check:unused` and `npm run -s check:fast` are green.
- [ ] No banned package, no undated, expired, catch-all or extended exclude, no unaccepted
      deprecation, no licence outside the policy without an approved exception (`npm run
      export:audit && npm run audit:licenses` checks more than 0 packages and finds every one).
- [ ] A native change: development builds launched on a named iOS simulator and Android emulator,
      and a preview or release build on both before the next release.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-deps-policy.mjs .` prints `RESULT: PASS` (the only
      expected SKIP, while the app has no source folder yet:
      `SKIP src [unused-dependency] not yet created (expo-project-bootstrap creates it)`)

## Anti-patterns

- **Installing from memory or from npm `latest`** (`npm install react-native`): the newest release
  is the wrong major. Take the policy row.
- **A bare `npx expo install <pkg>` for an Expo-managed package**: it writes what Expo's online list
  names today, possibly a patch published that morning. Pass the spec:
  `npx expo install expo-constants@~57.0.21`.
- **`npx expo install <pkg>` for a package outside Expo's map**: it runs `npm install --save <pkg>`,
  which takes npm `latest` (the newest release at least 7 days old, possibly the wrong major), not
  the policy row. Use `npm install <pkg>@<exact>`.
- **`npx expo install X -- --save-dev`** (it lands in `dependencies`) or `npx expo install X --dev`
  for a dev tool (Expo writes its `~` range into `devDependencies`, which fails `pin-exact`): use
  `npm install -D <pkg>@<row version>`; Expo-map dev tools are pinned exactly inside Expo's range.
- **Installing a package before the code that uses it**: knip or `unused-dependency` fails, and the
  package ages unreviewed.
- **Deleting `package-lock.json`, `--force` or `--legacy-peer-deps` when an install fails, or writing
  `legacy-peer-deps=true` into `.npmrc` to get past `ERESOLVE`**: go back to the row instead.
- **Extending an expired exclude block, a glob exclude where an exact name would do, a catch-all
  (`*`, `@*/*`), or an exclude outside a dated block in any spelling**: npm reads
  `min-release-age-exclude = x` like `[]=x`, and splits `a,b` into two patterns.
- **`before=<date>` in `.npmrc`**: npm then drops `min-release-age` altogether.
- **`"env": { "NPM_CONFIG_LEGACY_PEER_DEPS": "true" }` in `eas.json`** (the usual ERESOLVE workaround
  on EAS) or any `NPM_CONFIG_*` policy key in CI: a variable beats every line of `.npmrc`.
- **`"EAS_NO_FROZEN_LOCKFILE": "1"` when an EAS build fails with `EUSAGE`** (`npm ci` found
  `package.json` and `package-lock.json` out of sync): EAS then runs `npm install` and resolves the
  drift on the worker, outside the reviewed lockfile. Run `npm install` locally and commit both.
- **Installing first and approving after**, `npm approve-scripts --all`, `dangerously-allow-all-scripts`,
  `npm approve-scripts --no-allow-scripts-pin` (it writes a name-only key), or approving without
  reading the script: without `strict-allow-scripts=true` the script has already run by the time the
  notice appears.
- **`npx eas-cli …` inside the repo, or `eas-cli` in `devDependencies`**: npx installs it under the
  project's `strict-allow-scripts` without the root `allowScripts`, so it stops with
  `ESTRICTALLOWSCRIPTS` on a fresh runner (a warm npx cache hides that), and expo-doctor fails the
  dependency. Install it globally: `npm install -g --min-release-age=7 --ignore-scripts
  eas-cli@<x.y.z>` after reading its scripts, then call `eas` (`npx eas` is an unrelated package).
- **Getting an npx tool past `ESTRICTALLOWSCRIPTS` the wrong way**: running it from outside the repo
  (no release age, every script runs unreviewed), `--dangerously-allow-all-scripts`, `allow-scripts`
  in `.npmrc` or `~/.npmrc`, or `NPM_CONFIG_ALLOW_SCRIPTS` (npm then refuses `npm ci` with
  `EALLOWSCRIPTS`). Read the listed scripts and pass `--ignore-scripts` or pinned `--allow-scripts`
  keys on that one call, or make the tool a devDependency.
- **`npm audit fix` (or `--force`)**: it rewrites pins outside the policy and can move `expo` to
  another SDK; `npm explain <pkg>` shows whether an advisory ships at all.
- **Installing RNTL without `test-renderer`, `jest-image-snapshot` without its types, or
  `expo-router` without its peers**: npm fills the gap with its newest release (`test-renderer`
  1.3.0, the SDK 58 line). Take the plan's companions.
- **Bumping `react`, `react-native`, Reanimated, Skia or Gesture Handler by hand**: they move only with
  an Expo SDK (expo-sdk-upgrade).
- **Installing an Expo patch the day `expo install --check` asks for it**: it is younger than 7 days;
  it moves on its due date.
- **Hiding a banned or deprecated package behind an `overrides` entry**: remove the parent instead
  (`npm explain <pkg>`).
- **When multi-package: installing a native module in one app "to try it first", at the root, or in a
  shared package's `dependencies`**: autolinking finds it (since SDK 54 it resolves recursively), but
  `npx expo install --check` and `expo-doctor` verify only an app's direct dependencies, so that copy
  escapes the SDK set, and only one copy of a native module can be compiled. Install it in every app.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/policy-contract.md](references/policy-contract.md) | Every key of `contracts/dependency-policy.json`, the ban floor and profiles, licences, what reads which key, editing rules | Workflow step 2, and before editing the policy |
| [references/versions.md](references/versions.md) | The canonical-stack rows the policy is seeded with, companions and overrides, held-back majors, do-not-add, toolchain (EAS Node and npm), the React Navigation appendix, re-verify commands | Workflow step 3, before any install or review |
| [references/procedures.md](references/procedures.md) | Add, add outside the policy, upgrade, remove, the monthly pass, after a native change (iOS and Android), command traps, the same-day Expo patch, EAS installs (`npm ci`, `EAS_NO_FROZEN_LOCKFILE`), the commit record, when multi-package | Workflow steps 3 and 13 |
| [references/release-age-policy.md](references/release-age-policy.md) | The `.npmrc` and `engines`, keys that must never be in `.npmrc`, verified npm 11.17 behaviour (npx and global installs included), how the plan measures age (`--now`, `--today`), the bootstrap block, dated exceptions, expiry, pnpm/Yarn/Bun notes | On `ETARGET`, before an exception, on an expiry date |
| [references/supply-chain.md](references/supply-chain.md) | Bans, deprecation, install scripts (review before they run, `strict-allow-scripts`, the key each decision writes), npx and one-off tools inside the repo (EAS CLI, EAS workers), licences, Expo alignment, the gate files, fixes for failing gates | Before adding a package or running a tool through npx; when a dependency gate fails |
| [examples/add-expo-haptics.md](examples/add-expo-haptics.md) | A complete add in a Tasks app: real plan output, install, approvals, checks, commit, report line | Workflow step 13, as the model |
| `templates/contracts/dependency-policy.json` | The seed policy: 90 canonical-stack rows, held-back majors, do-not-add, the supply-chain bans, the licence allowlist | Workflow step 2 (copy to `contracts/`) |
| `templates/dot-npmrc` | The `.npmrc` policy (copy to `.npmrc`) | Workflow step 2 |
| `templates/scripts/` | The app's gates: `deps/check-deps.ts` (+ `dependency-policy`, which finds the policy like the checkers do, `release-age-excludes` (the `.npmrc` policy), `effective-npm-config` (the config npm runs with), `unpinned-approvals`, `engines-floor`, `banned-packages`, `workspace-lockstep`, `expo-patch-age`, all with tests), `deps/check-npm-config.ts` (before an install: CI, EAS), `audit/audit-licenses.ts` (+ `license-policy` with test), `clock/system-clock.ts` (+ test) | Workflow step 14; when setting up `npm run verify` |
| `assets/npmrc-exclude-block.txt` | The dated exclude block (`__EXPIRES__`, `__REASON__`, `__PACKAGE__`) | Workflow step 5 |
| `assets/banned-packages.json` | The supply-chain floor and the `offline-only` and `no-telemetry` profiles (`offline-only` bans everything `no-telemetry` bans) | Read by the scripts; copy entries into the policy |
| `assets/expo-sdk-57-module-map.json` | `bundledNativeModules.json` of `expo` 57.0.27 (what `npx expo install` writes), used when `node_modules` is absent | Read by the scripts |
| `assets/shared.json` | Declares the files the library keeps in sync with other skills: the module map, every file under `templates/`, `scripts/check-lib.mjs` (edit the library's canonical copy, never these) | When adding a shared file |
| `scripts/plan-dependency.mjs` | Prints the policy plan for one package (the script review before the install, companions, peers and overrides, `npx expo install <pkg>@<spec>`) and fails a forbidden request; `--online` adds age (measured like npm, from `--now`), deprecation, licence, scripts | Workflow step 4 |
| `scripts/check-deps-policy.mjs` | Checks the manifests, lockfile, `.npmrc`, `engines`, `NPM_CONFIG_*` variables in `eas.json` and GitHub workflows, `EAS_NO_FROZEN_LOCKFILE` in `eas.json`, committed npx calls (scripts, workflows, `lefthook.yml`), and the policy against the rules (29 rules, 4 more when multi-package) | Workflow step 11, and after any dependency change |
| `scripts/lib/policy.mjs` | Loads the policy, the ban lists and the module map; reads the repo (single app or workspaces) | Read only to change a script |
| `scripts/selftest.mjs` | Proves both scripts: 4 overlay suites (single app and workspaces), 98 planted bugs, passing plans and SKIP lines pinned | After changing a script, an asset, a template or a fixture |
| `scripts/check-lib.mjs` | Shared script helper, synced from the library (do not edit here) | Never by hand |
| `tests/bases/` | The single-app and npm-workspaces base trees the suites start from | When adding a case |
| `tests/fixtures/` | One folder per case (`EXPECT.txt` plus `mutation.json`, `DELETE.txt`, `ARGS.txt` or overlay files) in four suites | When adding a rule |

## Related skills

- `expo-sdk-upgrade` - moving the app to a new Expo SDK (the policy rows move in that commit).
- `expo-project-bootstrap` - the first install, `.npmrc` and policy of a new app.
- `quality-gates` - `npm run verify` and the gated paths; wire `scripts/deps/check-deps.ts` into it.
- `privacy-and-store-declarations` - the `offline-only` profile, permissions and privacy manifests after a native install.
- `expo-prebuild-and-config-plugins` - config plugins a new package brings.
- `ios-simulator-build`, `android-emulator-build`, `eas-build-and-submit` - the rebuild after a native change.
- `architecture-and-boundaries` - where a new adapter goes and which files may import a vendor SDK.
- `git-commits-and-reporting` - commit format, the `Gate-Change:` trailer and the report.
