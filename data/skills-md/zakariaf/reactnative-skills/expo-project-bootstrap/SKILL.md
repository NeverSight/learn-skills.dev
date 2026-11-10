---
name: expo-project-bootstrap
description: Creates a new Expo app from empty - SDK 57 stack, Expo Router, root configs, gates, variants, icons - proven by a checker. Use when bootstrapping, setting up or scaffolding an app or repo. Not for adding packages (dependency-management).
---

# Expo project bootstrap

Turns an empty (or docs-only) folder into an Expo app with the canonical stack: one app at the repo
root with Expo Router in `src/app/`, every root config, the gate scripts, the dependency policy,
`app.config.ts` with three variants for iOS and Android, a starter route and screen, and placeholder
art. Everything comes from templates that were installed and run end to end; every gate is green on
day one, and a checker proves the skeleton stays that way. The multi-package form is fenced under
"When multi-package" in `references/project-layout.md`.

## Rules that must hold

1. **Generate the skeleton with `scaffold-app.mjs`; never type a config by hand.** Each template was
   installed and run (tsc, ESLint, Prettier, Jest, knip, `expo config`); a hand-typed config drifts
   from the gates on the first character, and the guardrail then fails for a reason nobody sees.
2. **Bootstrap at the repo root, inside a git repository, and leave pre-existing folders where they
   are.** `npm install` installs the git hooks only in a repository, and agents load settings from
   the root. Folders that predate the app (docs, design exports) go into `.prettierignore`, ESLint's
   `PRE_EXISTING` and the root tsconfig `exclude`, never moved or reformatted. (`format-ignore`,
   `lint-ignore`, `tsconfig-program`)
3. **Never overwrite a file that differs from its template without reading both.** The generator
   reports a conflict instead of writing; `.gitignore` gains missing lines, `.claude/settings.json`
   keeps the developer's keys and allow rules, `CLAUDE.md` gains the `@AGENTS.md` import. Extra deny
   or ask rules or hooks are a question for the developer, because the guardrail compares them exactly.
4. **Start from this skeleton, not from `create-expo-app`'s demo.** `app.json`, the demo tabs and
   components, `scripts/reset-project.js`, a second routes folder and a second tool config
   (`eslint.config.js` from `npx expo lint`, `prettier.config.*`) are leftovers: they ship literal
   strings, or a config that Expo merges or that its tool loads before the canonical one. Move what
   is needed, delete the rest; never ignore them. (`template-leftover`)
5. **One identity, three variants, both platforms.** The production id is the reverse-DNS id the
   developer registers in App Store Connect and Google Play, valid as an iOS bundle id and an Android
   package (lower case, dot-separated, each part starting with a letter, no Kotlin or Java keyword);
   `development` and `preview` append `.dev` and `.preview`, so all three install side by side.
   `app.config.ts` sets `ios.bundleIdentifier`, `android.package` and the adaptive icon from it, and
   every icon it names exists. A `com.example` id is allowed only until the first store build. (`app-id`, `platforms`,
   `app-files`)
6. **Install exactly the policy's versions, with a committed lockfile.** Specifiers come from
   `contracts/dependency-policy.json`: Expo SDK modules keep the `~` that `npx expo install` writes,
   everything else is exact at the policy's version, React and React Native included. `overrides` pins all ten
   `@typescript-eslint/*` packages at the `typescript-eslint` pin: a second copy crashes every ESLint
   run with `Cannot redefine plugin "@typescript-eslint"`. (`pin-exact`, `root-overrides`,
   `one-react`, `lockfile`)
7. **Install only what the skeleton uses.** knip fails on an unused dependency, and a package
   installed early ages without review; every later package arrives with the skill that first imports
   it, through dependency-management. (`banned` keeps the policy's banned and doNotAdd lists out.)
8. **Keep the `.npmrc` policy whole; a dated exclude lives only until its `expires=` date.** npm keeps
   the last value of a key, so a later `min-release-age=0` silently switches the policy off; an
   exclude outside a dated block, or past its date, is a problem. (`npmrc-policy`, `npmrc-exclude`)
9. **Approve install scripts one package at a time, after reading them.** `strict-allow-scripts` stops
   an install on an unreviewed script; an approval is pinned to the reviewed version. Never
   `--dangerously-allow-all-scripts`. (`install-scripts`)
10. **Never stub a missing gate script to make `npm run verify` pass.** `i18n:verify` waits for
    i18n-strings-and-catalogs; report it as pending. A gate that passes without checking hides every
    later failure. (`tooling-files` for the scripts the skeleton does own)
11. **Agents get one contract.** `AGENTS.md` (start green with `npm run -s check:fast`, stop and ask,
    never bypass a hook, devices always named) and `CLAUDE.md` = `@AGENTS.md`. An app nested in a
    larger repository may take them from there (`"agentInstructions": "parent-repo"`; only up to that
    repository's top level counts). (`agents`)
12. **Stop and ask for human steps.** Xcode and its licence, Android SDK licences, `sudo`, store
    accounts, signing credentials and trusting the folder in the agent are the developer's; ask once,
    name the step and the default that applies meanwhile. Never read or create a signing key.
13. **The first commit stages exactly the generated files, with a `Gate-Change:` trailer, through the
    hooks; nothing is pushed unless the developer asks.** Never `git add -A`: the folder may hold the
    developer's own uncommitted work.

The checker also guards what the other skills own inside the skeleton, so a bootstrap cannot drift
from them: the canonical scripts (`root-scripts`), Prettier and TypeScript options (`prettier-config`,
`tsconfig-base`), the gate wiring (`knip-config`, `lefthook`, `quality-gates`, `gate-scope`,
`stryker-config`, `claude-settings`), the app config (`app-config`, `metro-cache`, `app-env`) and
unfilled template tokens (`placeholder`). Each rule's reason is in `references/root-files.md`.

## Workflow

1. **Toolchain.** Read [references/toolchain-setup.md](references/toolchain-setup.md) and run its
   "Checks before installing" (Node 26.4.0, npm 11.17.0, git; Xcode and the Android SDK only from the
   first native build). Ask the developer for any human step that is missing.
2. **Identity.** Ask the developer for the display name and the store id (`com.<org>.<app>`); the slug
   and scheme default from the name. Read [references/project-layout.md](references/project-layout.md)
   so the tree, the left-out parts and the pre-existing entries are clear. Run `git status`; `git init`
   only if the folder is not a repository yet; never discard work you did not make.
3. **Plan without writing:** `node ${CLAUDE_SKILL_DIR}/scripts/scaffold-app.mjs . --app-id com.acme.tasks --name "Tasks"`.
   Read the plan: the pre-existing entries it will ignore, the merges, every `conflict` and `leftover`.
4. **Resolve** each conflict with [references/root-files.md](references/root-files.md) ("Merging an
   existing repo"): edit the file to the template content, or rerun with `--replace <file>` when it is
   only an old draft; ask the developer when a settings rule would be dropped. Delete each leftover
   after moving what the app still needs (an `app.json` value goes into `app.config.ts`).
5. **Write:** the same command with `--write`. Rerun the dry run: it must print `0 new, 0 merged` and
   `RESULT: PASS`.
6. **Install** exactly as [references/first-install-and-verify.md](references/first-install-and-verify.md)
   says ("Install and approve install scripts"): `npm install`, read each pending script, approve one
   package at a time until `npm approve-scripts --allow-scripts-pending` lists none; `npm ls react
   react-native @typescript-eslint/eslint-plugin` shows one version each.
7. **Gates:** every gate one by one, with no format step first ("The gate runs":
   `export:audit` is the only one that bundles through Metro, then `audit:licenses` reads its source
   maps) and the Expo config for the three variants on both platforms ("The Expo config for every
   variant"). Fix the cause of a failure in the files; a gate is never loosened.
8. **Check:** `node ${CLAUDE_SKILL_DIR}/scripts/check-skeleton.mjs .`; fix every `FAIL` line (each
   names the file, the rule and the fix) and rerun until `RESULT: PASS`.
9. **Commit** as "The first commit" says (exact paths, `Gate-Change: initial quality gates`, hooks run).
10. **Report** in the shape of [examples/bootstrap-report.md](examples/bootstrap-report.md): outcome,
    at most one request, what to look at, the pending gate in plain words, then the numbers. Hand off
    in the order of "What the bootstrap leaves out" (project-layout.md).

## Definition of done

- [ ] `scaffold-app.mjs . --app-id <id> --name <name>` prints `0 new, 0 merged` and `RESULT: PASS`
      (no conflict, no leftover); pre-existing folders are untouched and ignored by Prettier, ESLint
      and the root tsconfig.
- [ ] `package-lock.json` is committed; `npm approve-scripts --allow-scripts-pending` lists no
      package; `npm ls react react-native @typescript-eslint/eslint-plugin` shows one version each.
- [ ] `npm run -s check:fast`, `npm run -s lint`, `npm run -s typecheck`, `npm run -s test:coverage`
      (thresholds met), `npm run -s check:unused`, `npm run -s export:audit` (iOS and Android
      bundles), `npm run -s audit:licenses`, `node scripts/quality/check-quality-gates.ts` and
      `npm run -s check:deps` pass; `npx lefthook validate` prints `All good`.
- [ ] `npx expo config --type public` resolves for `development`, `preview` and `production` (each
      with the same `APP_VARIANT` and `EXPO_PUBLIC_APP_VARIANT`), with three ids, names, schemes and
      icons on iOS and Android; `APP_VARIANT=production` alone fails.
- [ ] The first commit went through the hooks with a `Gate-Change:` trailer; nothing was pushed
      without the developer.
- [ ] The report names the pending gate (`i18n:verify`, i18n-strings-and-catalogs) and the next
      skills in order.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-skeleton.mjs .` prints `RESULT: PASS` (a `com.example`
      id adds one `NOTE ... [app-id]` line; there are no SKIP lines).

## Anti-patterns

- **Running `create-expo-app` and trimming the demo by hand.** Leftovers survive (`app.json`, the
  tabs, `src/components/`), and the configs miss the gates. Generate from this skill; on top of an
  existing template app, the plan lists every leftover.
- **Installing the whole stack on day one.** knip fails on a dozen unused dependencies; each package
  arrives with its first user, at the policy's version.
- **Dropping an `overrides` row, or excluding `typescript-eslint` from the release age.** A fresh
  install then takes whatever npm published that morning; on 2026-09-29 that was a one-day-old
  `@typescript-eslint` 8.71.0 next to 8.70.1, and ESLint crashed on every run.
- **Deleting `package-lock.json` or loosening `.npmrc` when an install fails with `ETARGET`.** The
  version is younger than the release age; use dependency-management's dated-exception procedure.
- **Approving install scripts with `--dangerously-allow-all-scripts`, or `npm audit fix --force`.**
  Read each script; `npm audit` is information (the force fix moves `expo` off the SDK).
- **Adding a stub `verify-catalogs.ts` so `npm run verify` goes green.** Report the pending gate.
- **Editing `quality-gates.json` to match a changed config.** The guardrail exists to catch exactly
  that; restore the config, or change both with the developer and a `Gate-Change:` trailer.
- **Reformatting or linting the developer's pre-existing folders**, or ignoring app code to silence a
  gate: only folders that are not app code go in the ignore lists.
- **Committing `ios/` or `android/`.** They are generated by `npx expo prebuild` (Continuous Native
  Generation); native changes go through `app.config.ts` and config plugins.
- **Selecting Xcode with `sudo xcode-select`, or building on "the booted simulator".** Use
  `DEVELOPER_DIR`, and name every simulator, emulator and device.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/toolchain-setup.md](references/toolchain-setup.md) | Node, npm, git, Xcode by `DEVELOPER_DIR`, CocoaPods, JDK 17 and Android SDK 36, human steps, checks, prebuild facts for both platforms | Workflow step 1 |
| [references/project-layout.md](references/project-layout.md) | The tree, what is left out and which skill adds it, who maintains each file, pre-existing entries, leftovers, When multi-package | Workflow step 2, and when a skill asks where a file goes |
| [references/root-files.md](references/root-files.md) | Every root file and the reasons behind it; merging an existing repo | Workflow step 4, and when a check names a config |
| [references/first-install-and-verify.md](references/first-install-and-verify.md) | Install and approvals, the gate runs, the variant configs, other skills' checkers on a fresh skeleton, the first commit, pending gates, traps, the verified run | Workflow steps 6 to 9 |
| [examples/bootstrap-report.md](examples/bootstrap-report.md) | A complete report after a bootstrap | Workflow step 10 |
| `scripts/scaffold-app.mjs` | Generator: dry-run plan, `--write`, `--replace <file>`, `--compare`; rules `conflict`, `leftover`, `differs` | Workflow steps 3 to 5 |
| `scripts/check-skeleton.mjs` | Checker for the whole skeleton (the rule ids above; when multi-package also `workspace-layout`, `package-manifest`, `app-lockstep`, `root-runtime`) | Workflow step 8, and after any change to a root config |
| `scripts/lib/bootstrap-plan.mjs` | Template mapping, rendering, merges, pre-existing entries, leftovers, placeholder art | Read only to change the generator |
| `scripts/lib/repo-read.mjs` | JSONC, `.npmrc` policy and dated-exclude readers | Read only to change the checker |
| `scripts/lib/ship-placeholders.mjs` | The placeholder values the ship gates refuse (synced; do not edit here) | Read to see why `com.example` is only a NOTE here |
| `scripts/check-lib.mjs` | Shared script helper (synced; do not edit here) | Never by hand |
| `scripts/selftest.mjs` | Proves both scripts: generator cases, and the checker on a skeleton generated at test time (single app, multi-package, nested) with a planted bug per rule | After changing a script or a template |
| `templates/` | Every file of the skeleton: the canonical root configs, `contracts/`, `scripts/` (gates, hooks, git, deps, audit, clock, metro), `src/` (env types, app-variant, starter layout, route and screen), `app.config.ts`, `metro.config.js`, `AGENTS.md`, `CLAUDE.md`, `dot-nvmrc` (a `dot-` file name becomes `.`; synced copies are listed in `assets/shared.json`) | The generator writes them; read one when resolving a conflict |
| `assets/skeleton-package.json` | The canonical skeleton manifest (scripts, dev tools, overrides, approvals; synced) | The generator renders `package.json` from it |
| `assets/claude-settings.json` | The canonical `.claude/settings.json` (synced) | The generator writes or merges it |
| `assets/app-dependencies.json` | The skeleton's runtime packages and the dev tools it leaves out until first use | When the skeleton's dependency set changes |
| `assets/template-placeholders.json` | Placeholder values for the template harness | Maintainers only |
| `assets/shared.json` | The shared files copied into this skill | When adding a shared file |
| `tests/fixtures/` | Generator cases and the planted bugs for the checker (`mutation.json` on the generated skeleton) | When adding a rule |

## Related skills

- `react-native-conventions-index` - the build order after the bootstrap.
- `dependency-management` - every package after the bootstrap, the policy file, dated exceptions.
- `quality-gates` - what each gate checks and how to fix a failing one.
- `typescript-and-lint-rules` - the tsconfig set, the ESLint config, Prettier, pre-existing entries.
- `architecture-and-boundaries` - where files go; the composition root.
- `app-startup-and-bootstrap` - replaces the starter `_layout.tsx` with the root skeleton.
- `navigation-and-routing` - the route contract and the not-found route.
- `scaffold-feature-screen` - every screen after the starter, the first one in its place.
- `app-variants-and-environment` - variants, `EXPO_PUBLIC_*`, the Metro cache key.
- `unit-and-component-tests` - Jest projects, render helpers, coverage, Stryker.
- `git-commits-and-reporting` - the commit format, the `Gate-Change:` trailer, the report.
- `icons-app-icon-and-splash` - real art in place of the placeholder icons.
- `eas-build-and-submit` - `eas.json` and the first build; `ios-simulator-build`, `android-emulator-build` for local builds.
- `expo-sdk-upgrade` - moving the whole app to the next Expo SDK.
