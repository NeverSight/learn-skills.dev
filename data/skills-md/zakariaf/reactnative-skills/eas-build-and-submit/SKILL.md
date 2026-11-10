---
name: eas-build-and-submit
description: "Configures EAS Build and Submit: eas.json profiles, remote build numbers, fingerprints, gated store submits. Use when editing eas.json, running eas build/submit, or a build fails. Not for local builds (ios-release-testflight) or OTA (ota-updates)."
---

# EAS Build and Submit

An Expo app builds every variant on EAS from one checked `eas.json`, and a store build reaches
TestFlight and Google Play internal testing only after the gates passed, from the reviewed commit, with
a build number no store has seen and a fingerprint that matches the reviewed native inputs. Credentials
stay with EAS and the developer; the agent builds, proves and submits with the developer's word.

## Rules that must hold

1. **Nothing leaves the machine without the developer's word in this session.** A store `eas build`,
   every `eas submit`, `eas build:version:set` and any `eas credentials` change ask first. *Why:* each
   uploads, spends a build number or changes shared signing state, and none can be undone.
2. **eas.json is valid for the CLI it names.** `cli.version` is a floor `>= 24.10.0` (or newer), every key
   and value passes EAS CLI's own schema (`image` only inside `ios`/`android`, `node` a full version),
   and `extends` chains resolve. *Why:* EAS CLI refuses an invalid file only after a login, often in CI;
   the checker and `eas config --eas-json-only` catch it offline in seconds.
3. **Build numbers are remote and only go up.** `cli.appVersionSource` is `remote`, every store profile
   has `autoIncrement: true`, and the app config holds a literal `version: 'x.y.z'` (raised per store
   release) and no `ios.buildNumber` or `android.versionCode`. *Why:* EAS keeps one counter per app id,
   so two machines can never upload the same number (ITMS-90189, a used `versionCode`), and a number in
   the file would only mislead.
4. **A build is exactly a commit.** `cli.requireCommit` is `true`, and store builds start from a clean
   tree on the release branch. *Why:* without it EAS CLI copies uncommitted and untracked files into the
   build, so its `gitCommitHash` lies and the review covered other code.
5. **A profile per variant (and per simulator build), and only `production` is a store build.** `development`,
   `development-simulator`, `preview`, `preview-simulator` and `production` (templates/eas.json);
   the store profile builds an Android app bundle, signs, and never sets `developmentClient`,
   `withoutCredentials` or `ios.simulator`; internal profiles never build an AAB. *Why:* EAS defaults a
   profile without `distribution` to `store`, Play takes only app bundles, and testers cannot install an
   AAB from a link.
6. **Every build profile pins the project's Node.** `"node": "26.4.0"`, equal to `.nvmrc` (or an
   `eas-build-pre-install` script that upgrades npm). *Why:* the SDK 57 images ship npm 10.9.8, which the <!-- stack-pin-ignore -->
   `engines` field and the install policy refuse (`EBADENGINE`), and which ignores `min-release-age`.
7. **`submit.production` pins the production ids and reaches testers only.** `ios.ascAppId` (digits) and
   `ios.bundleIdentifier`, `android.applicationId`, never a `.dev`/`.preview` id; Android `track` is
   `internal` (or `alpha`/`beta`) with `releaseStatus` `completed` or `draft`. *Why:* a standalone
   `eas submit` evaluates the app config without the profile's env and would look up the development
   id; promotion and rollouts are store-console decisions (android-release-play).
8. **Credentials stay with EAS and the developer.** Managed credentials (`credentialsSource: remote`),
   `--freeze-credentials` on every `eas build` (EAS Workflows build jobs have no such flag), no `appleId` login and no literal key path in `eas.json`
   (EAS-stored keys or `$VARIABLES` from CI secrets); the agent never opens a `.p8`, `.p12`, keystore or
   service-account file. *Why:* a leaked key publishes apps in the developer's name, and a build that
   regenerates a certificate breaks every app that shares it.
9. **Gates first, then one named command.** An outward `eas build` runs after `npm run verify` or
   `scripts/eas/release-preflight.ts`, and an `eas submit` after `check-eas-build` on its record, in the
   same script or job, as a command, never only in a comment (an EAS Workflows `type: build` job
   `needs:` the job that ran verify, a `type: submit` job the job that ran the record check); every
   `eas build`/`eas submit` names `--profile` (a job: `params.profile`); EAS CLI is the global `eas`,
   never `npx eas-cli`; no `eas submit --latest`; `--auto-submit` (`-s`) only from the store profile and
   only for iOS; CI commands pass `--platform`, and `eas submit` `--non-interactive`. *Why:* `eas build`
   defaults to `production`, `--latest` submits whatever finished last, verify proves the code but not
   what EAS built, an auto-submitted Android bundle reaches Play before its gate read it, and
   `eas submit` stays interactive even in CI.
10. **Only a build whose record proves it is submitted, and only the file its gate read.**
    `check-eas-build` on `eas build:view <id> --json`: finished, store distribution, the production
    profile, the reviewed commit, the production id, the app config's version, a build number above
    every upload tag, and the fingerprint the preflight wrote. Then the record's artifact is downloaded
    to `build/ios-release/export/app.ipa` / `build/release-android/app-release.aab`, the stores' own
    gates read it (ios-release-testflight, android-release-play), and `eas submit --path <that file>`
    uploads exactly those bytes. *Why:* the record is the only evidence of what EAS built, the artifact
    gate the only evidence of what is inside it; a wrong variant or commit looks like success until
    testers open it.
11. **The fingerprint decides between a build and an update, and nothing hides native inputs from it.**
    Compare fingerprints of the same variant and platform (`eas fingerprint:compare --build-id <id>`);
    `.fingerprintignore` never hides `package.json`, the lockfile, the app config, `plugins/`, `patches/`
    or `node_modules/`, and `sourceSkips` never `ExpoConfigAll`. *Why:* a hidden native change ships as
    an update to binaries that lack the code, and the build-record check loses its proof.
12. **Stops are never retried.** Credentials errors, agreements, HTTP 401/403, missing app records, a
    used build number, a draft Play app, an `INVALID` processing state: one message with the step, the
    exact error and the one action. *Why:* retries lock accounts, burn numbers and hide the real cause.
13. **Every submitted build is tagged from its record.** `git tag -a v1.4.0+ios.14 -m "App Store build 14"`
    (and `+android.<n>`, "Play build N"), with the record's `appBuildVersion`, pushed only with the
    developer's word. *Why:* each TestFlight and Play build traces back to its commit, and the next
    record check compares against these numbers (git-commits-and-reporting owns the scheme).

## Workflow

1. **Choose the lane and list the human steps.** EAS is the default; a team that cannot use EAS takes the
   local lane (ios-release-testflight, android-release-play) and this skill's checker prints NOT
   APPLICABLE. Read [references/credentials-and-signing.md](references/credentials-and-signing.md) and
   ask the developer, one step per message, for what is missing: accounts, `eas init` (writes
   `extra.eas.projectId`), app records, signing and submit keys, `EXPO_TOKEN` for CI.
2. **Install EAS CLI** globally with the policy flags:
   `npm install -g --min-release-age=7 --ignore-scripts eas-cli@24.10.0`, never `npx eas-cli` in the app
   ([references/build-and-submit-runbook.md](references/build-and-submit-runbook.md), "Install the CLI").
3. **Write eas.json** from `templates/eas.json`: fill `__ASC_APP_ID__` (the Apple ID number of the app
   record) and `__APP_ID__` (the production id); keep an existing file's extra profiles and merge the
   variant wiring app-variants-and-environment owns. Read [references/eas-json.md](references/eas-json.md)
   for every key and the ownership table; leave `image` out (expo-sdk-upgrade's `auto` default).
   Validate offline: `eas config --eas-json-only --profile production --platform ios --json --non-interactive`.
4. **Fix the version fields** in `app.config.ts`: a literal `version`, no `ios.buildNumber` or
   `android.versionCode`. For an app with store history, ask the developer to run
   `eas build:version:set` per platform with the last store numbers
   ([references/versions-and-fingerprints.md](references/versions-and-fingerprints.md)).
5. **Copy the release templates**: `templates/scripts/eas/` (`eas-profile.ts`, `eas-commands.ts`,
   `release-plan.ts`, `release-preflight.ts` and the three tests) and, when missing,
   `templates/src/config/app-variant.ts` with its test (the canonical resolver). Run
   `npx jest scripts/eas --ci --maxWorkers=2`, `npm run typecheck` and `npx eslint scripts/eas --max-warnings 0`.
6. **Check the setup:** `node ${CLAUDE_SKILL_DIR}/scripts/check-eas-config.mjs .`; fix every `FAIL`
   line and rerun until `RESULT: PASS`. Then app-variants-and-environment's `check-variants` and
   expo-sdk-upgrade's `check-sdk-alignment` for the parts they own.
7. **Internal builds** (dev client, preview, simulator builds for E2E) need no preflight: the runbook's
   table has each command.
8. **A store release**, step by step from the runbook: `check-eas-config.mjs . --release`; then
   `node scripts/eas/release-preflight.ts --profile production --platform all --what-to-test "<text>"`,
   which prints the sequence; then ask (rule 1, shape in [examples/release-report.md](examples/release-report.md));
   then its build line, `eas build ... --json > dist/eas/builds.json` (no `--auto-submit`); then
   `node ${CLAUDE_SKILL_DIR}/scripts/check-eas-build.mjs . --build dist/eas/builds.json --platform ios`
   (and android); then its download and store-artifact gate lines (ios-release-testflight's
   `check-store-artifact`, android-release-play's `check-store-aab`); then its submit lines,
   `eas submit --profile production --platform <p> --path <gated file> --non-interactive` (What to Test
   on iOS); then tag and report. The preflight's `--auto-submit` (iOS only: the build submits itself,
   record checked afterwards) only when the developer explicitly agreed to skip the record check.
9. **Before an update instead of a build**, compare fingerprints
   ([references/versions-and-fingerprints.md](references/versions-and-fingerprints.md), "New build or
   update?") and hand the update to ota-updates.
10. **On any failure** find the row in [references/failure-playbook.md](references/failure-playbook.md):
    fix and rerun, or send the stop message and wait.

## Definition of done

- [ ] `eas.json` has the five profiles, remote versions, `requireCommit`, the CLI floor, `node` in every
      profile and `submit.production` with the production ids; `eas config --eas-json-only` accepts it.
- [ ] `app.config.ts` has a literal `version` and no build numbers; remote counters are initialised
      for an app with store history (or it is a new app).
- [ ] `scripts/eas/` is in place and its tests pass with the app's typecheck and lint.
- [ ] For a store release: the developer agreed in this session; the preflight passed; each submitted
      build's `check-eas-build` printed `RESULT: PASS`; each build is tagged; the report holds every
      RESULT line and nothing was retried after a stop.
- [ ] No key file was opened, copied or uploaded by the agent; `eas.json` holds no secret or key path.
- [ ] An app on the local lane prints `NOT APPLICABLE: no eas.json and nothing uses EAS ...`; an app
      whose EAS profiles are all internal while `release:ios`/`release:android` ships the store builds
      prints the `internal-only EAS: ...` note; there are no SKIP lines (both checkers are strict; a
      shared `base` profile others extend is judged through the profiles built from it).
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-eas-config.mjs .` prints `RESULT: PASS` (with `--release`
      before a store build)

## Anti-patterns

- **`eas build` with no `--profile`.** It silently builds `production`, spends a store number and, with
  `--auto-submit`, uploads. Name the profile every time.
- **`eas submit --latest`.** It takes whatever build finished last: a preview build, another branch.
  Submit the gated file with `--path` after `check-eas-build` and the store-artifact gate.
- **`eas build --platform all --auto-submit`.** The Android bundle reaches Play before any gate read
  it; build, check, gate, then `eas submit --path`.
- **`"appVersionSource": "local"` plus a script that bumps `buildNumber` and commits.** Two machines or a
  retried CI job upload the same number. Use remote versions.
- **`"image": "latest"`** (what `eas init`'s template writes). A new Xcode reaches the build without a
  commit; leave `image` out.
- **No `node` in the profiles "because it worked locally".** The worker's npm 10 refuses `engines` or, <!-- stack-pin-ignore -->
  worse, ignores the release-age policy.
- **Fixing a credentials error by switching to `credentialsSource: "local"` or an Apple ID login.** A
  stop was worked around and a key file was handled; send the stop message.
- **Reading the `.p8` or the keystore "to check it is there".** Ask the developer or read
  `eas credentials` output; never open the file.
- **`eas build:version:set` to a lower number to "reuse" a failed build's number.** The store refuses it;
  spent numbers stay spent.
- **Announcing "on TestFlight" when `eas build` returns.** Check the record, submit, then wait for
  Apple's processing.
- **`.fingerprintignore` with `package.json` or `**/node_modules/**` to make builds "reusable".** Native
  changes stop changing the fingerprint and updates reach binaries without the code.
- **`--auto-submit` from `preview` to put testers on TestFlight.** Preview is an internal build with the
  preview id; TestFlight takes store builds of the production id.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/eas-json.md](references/eas-json.md) | Every profile and key with its reason, the extends merge, Node on EAS, images, the submit profile, the full schema table, offline validation, ownership | Workflow step 3; an `eas-schema`, `cli-version`, `store-profile`, `internal-profile`, `build-node` or `submit-profile` failure |
| [references/credentials-and-signing.md](references/credentials-and-signing.md) | What signs what, the human setup steps, frozen credentials, submit keys, local credentials, CI, never-list, leak response | Workflow step 1; a `submit-credentials` failure; any credentials error |
| [references/versions-and-fingerprints.md](references/versions-and-fingerprints.md) | Version policy, remote counters per app id, initialising them, tags, what the fingerprint hashes (measured), how EAS records it, build or update, test recipes | Workflow steps 4 and 9; a `version-source`, `config-versions` or `fingerprint-config` failure |
| [references/build-and-submit-runbook.md](references/build-and-submit-runbook.md) | Installing the CLI, internal builds, the store release step by step, What to Test, groups and tracks, after submission, `--local`, workflows, what needs the developer | Workflow steps 2, 7 and 8 |
| [references/failure-playbook.md](references/failure-playbook.md) | Symptom, cause, fix or stop for every known local, worker, version, submission and processing failure | Workflow step 10 |
| [examples/release-report.md](examples/release-report.md) | The ask, the evidence message and a stop message for a Tasks release, and bad versions | Workflow step 8 |
| `templates/eas.json` | The five build profiles and `submit.production` (`__ASC_APP_ID__`, `__APP_ID__`) | Workflow step 3 |
| `templates/scripts/eas/eas-profile.ts` | Resolves a build profile like EAS CLI; store-profile problems; pinned submit ids | Workflow step 5 |
| `templates/scripts/eas/eas-commands.ts` | `eas build` / `eas submit --path` argument lists, the gated artifact paths, the release sequence, the What to Test limit, upload tags, a shell-safe line | Workflow step 5 |
| `templates/scripts/eas/release-plan.ts` | The preflight's pure decisions: tree, branch, profile, version above the last release, ids | Workflow step 5 |
| `templates/scripts/eas/release-preflight.ts` | The gates-first CLI: tree and profile, `npm run verify`, the app config, fingerprints to `dist/eas/`, the printed release sequence (build, record checks, download and store-artifact gates, `--path` submits; iOS `--auto-submit` only on request); unattended under `CI=true`, non-zero on any failed gate | Workflow steps 5 and 8 |
| `templates/scripts/eas/eas-profile.test.ts` | Tests of the profile resolution and the store-profile rules | With the module |
| `templates/scripts/eas/eas-commands.test.ts` | Tests of the command lines, the release sequence (no `--auto-submit` by default, never for Android), the What to Test limit and upload tags | With the module |
| `templates/scripts/eas/release-plan.test.ts` | Tests of the preflight's decisions | With the module |
| `templates/src/config/app-variant.ts` | The canonical variant resolver the profile module reads (synced from the library; do not edit here) | Workflow step 5, when missing |
| `templates/src/config/app-variant.test.ts` | Its tests (synced; do not edit here) | With the resolver |
| `scripts/check-eas-config.mjs` | Checks eas.json, the app config's version fields, commands and their gates, the preflight and the fingerprint inputs (`--release`: ship mode) | Workflow steps 6 and 8 |
| `scripts/check-eas-build.mjs` | The ship gate on a build record before submission | Workflow step 8 |
| `scripts/lib/eas-json.mjs` | eas.json reader, EAS's schema and extends resolution, offline | Only when changing a checker |
| `scripts/lib/repo-facts.mjs` | App config facts, Node pins, eas commands in scripts and workflows | Only when changing a checker |
| `scripts/lib/ship-placeholders.mjs` | The placeholder values a ship gate refuses (synced from the library; do not edit here) | Only when changing a checker |
| `scripts/check-lib.mjs` | Shared checker library (synced from the library; do not edit here) | Never by hand |
| `scripts/selftest.mjs` | Runs both checkers against the fixtures (the tags suite builds a throwaway git repo per case from its `TAGS.txt`) | After changing a checker or a template |
| `tests/bases/` | The Tasks base app, build records and fingerprints, and decoys under `.agents/skills/`, `skills/` and a vendored SKILL.md folder | When adding a fixture |
| `tests/fixtures/` | Overlay cases per checker: good, one bad case per rule, pass and error cases; `eas-build-tags/` reads upload tags of an app at `apps/mobile` | When adding a rule |
| `assets/eas-facts.json` | The verified CLI floor, image Node and npm, the project Node, the What to Test limit | When re-verifying for a new CLI or SDK |
| `assets/shared.json` | The shared files this skill syncs in | When adding a shared file |
| `assets/template-placeholders.json` | Values for the template placeholders in template checks | When a template gains a placeholder |

## Related skills

- `app-variants-and-environment` - the variant env and `environment` of each profile, secrets in EAS environments.
- `expo-sdk-upgrade` - EAS images (`auto` by default, never `latest`) and the SDK move.
- `dependency-management` - the install on EAS (`npm ci`, the lockfile, `NPM_CONFIG_*`), the global EAS CLI install.
- `ota-updates` - channels per profile, runtime versions from fingerprints, `eas update`.
- `ios-release-testflight` - signing details, the store-artifact gate on the `.ipa`, and the local lane.
- `android-release-play` - Play App Signing, the AAB gate, tracks beyond internal, staged rollout.
- `ci-pipeline-and-gates` - the CI jobs that run these commands with `EXPO_TOKEN`.
- `git-commits-and-reporting` - upload and release tags, the evidence message, the stop list.
- `privacy-and-store-declarations` - privacy manifest and store answers before a submission.
- `ios-simulator-build`, `android-emulator-build`, `e2e-maestro` - local builds and E2E on named devices.
- Expo's official `eas-app-stores` and `eas-workflows` skills - API references for EAS Submit and EAS Workflows.
