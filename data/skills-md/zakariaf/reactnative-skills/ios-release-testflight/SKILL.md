---
name: ios-release-testflight
description: "Ships iOS builds to TestFlight: API-key signing, archive, export, store gate on the .ipa, upload, VALID wait, build numbers. Use when releasing, signing or uploading an iOS build, or an upload fails. Not for eas.json (eas-build-and-submit)."
---

# iOS release to TestFlight

Takes one commit of an Expo app to a processed TestFlight build and proves, on the exported `.ipa` itself, that testers and users get exactly what was meant: the right identity, version and build number, no test-only code, no StoreKit test files, no debug entitlement, no placeholder value, every usage string in every language. Two lanes share one gate: **EAS Build + EAS Submit** (the default; `eas-build-and-submit` owns `eas.json` and credentials) and the **local lane**, `npm run release:ios -- --variant preview|production`, which needs no Expo account and signs with the team's App Store Connect API key through Apple's own command-line tools. Everything that needs a person is asked for, never worked around. Verified on 2026-10-14 with Expo SDK 57, Xcode 26.6 (altool 26.40) and the App Store Connect API v1; the Android twin is `android-release-play`.

## Rules that must hold

1. **Nothing leaves the machine without the developer's word in this session.** Uploading (`release:ios`, `eas submit`), pushing tags and submitting for review are outward-facing and cannot be undone: ask first. "Ship" creates the release tag; only "submit" submits. Why: a wrong build in front of testers or reviewers cannot be taken back.
2. **Never open, print, copy, move, commit or log the `.p8` key, a JWT or an `Authorization` header.** Tools receive only `ASC_KEY_ID`, `ASC_ISSUER_ID` and `APPLE_TEAM_ID`; only `scripts/asc/asc-credentials.ts` reads the key, into memory; xcodebuild gets its path and altool finds it itself. On EAS the credentials live in EAS (`eas credentials`) and the agent never handles key files. Why: a leaked team key can publish apps in the team's name.
3. **Sign only with the team API key:** automatic signing, `-allowProvisioningUpdates` plus the three `-authenticationKey*` flags on archive and export, cloud-managed distribution certificates. No `.p12`, no hand-made profiles, no switching signing method to get past an error. Why: one signing method that needs no Keychain exports is the only one an agent can run safely.
4. **One counter holds the build number, and it never goes back.** Local lane: the single line `const IOS_BUILD_NUMBER = <n>;` in `app.config.ts`, bumped and committed (`chore(release): build <n>`) before the archive; EAS: remote versioning (`appVersionSource: "remote"`), never both. A failed upload still spends its number; the version must rise above the last approved one. Why: App Store Connect refuses a reused build number (ITMS-90189) and a lower version (ITMS-90062).
5. **Build only through the release command, from a clean tree on the release branch, after the full verify gate**, from a clean prebuild (for production builds also green E2E flows and reviewed screenshots of the same commit when the repo has them). Why: an upload must be one known commit whose gates were green; a stale `ios/` builds another identity.
6. **Preview builds are internal-only; production builds use the store export.** `export-options-preview.plist` sets `testFlightInternalTestingOnly: true`, and a preview build carries `<appId>.preview`, so it needs its own app record. Why: an internal build can never reach external testers or the App Store by mistake.
7. **The store-artifact gate passes on the exported `.ipa` before `--validate-app` or `eas submit`, on every lane.** `check-store-artifact.mjs` (and `store-gate.ts` inside `release:ios`) read the signed export. Why: it is the only proof that the debug menu, the StoreKit harness, test ads and dev-client keys are absent from what users receive.
8. **An upload is done only when processing reaches `VALID`.** `altool --upload-package --wait` (and `eas submit`) return while Apple is still `PROCESSING`; the local lane polls the REST API every 60 s for up to an hour. Why: an `INVALID` build never reaches TestFlight, and announcing it early sends testers looking for nothing.
9. **Stop and ask, never retry,** on `errSecInternalComponent`, the Xcode licence, any agreement error, a missing app record, HTTP 401/403, `INVALID`/`FAILED` processing, or a `[ship-placeholder]` line. Send one message: the step, the exact error line, the one action. Why: each needs a person or a credential, and retries can lock the account or burn build numbers.
10. **Tag every processed upload, annotated: `v<version>+ios.<n>`; tag `v<version>` on the developer's "ship".** When multi-package, prefix the app folder (`mobile/v1.4.0+ios.14`). Push tags only with the developer's word. Why: each TestFlight build traces back to its commit, and the tag check (`git-commits-and-reporting`) can order builds by tag date.
11. **Select the pinned Xcode through `DEVELOPER_DIR`, never `xcode-select` or `sudo`;** the gate checks `DTXcode`. Why: a Mac often holds several Xcodes, and a global switch needs a password and changes every build on the machine.
12. **Nothing unfinished ships, in any variant:** the contract's `unfinishedMarkers` files stop the preflight and both checkers, its `forbiddenBundleStrings` stop the gate, and the test-only sentinels are absent from production bundles (present in preview ones); a test-only gate without a known sentinel stops `release:ios` before the bump. Why: testers and users would open a stand-in screen or a debug menu.
13. **No placeholder value ships.** The bundle id comes from `contracts/ios-release.json` (`appId`; `com.example.*` always fails); a production build carries no `example.com` link and, with live ads, no sample or template AdMob id; no build carries a template AdMob app id or an unfilled `__TOKEN__`; each fails the gate (as a `[ship-placeholder]` stop, or `ad-app-id` for a testing build's app id), and no option turns it into a pass. Why: a placeholder is often format-valid, so only a value check stops it, and the real values come from the developer.
14. **Every build carries every usage description, in Info.plist and in every language the app is localized into** (the contract's `usageStrings`, the tracking text whenever the app can ask for tracking, and every `NS*UsageDescription` it carries). Why: without the Info.plist key iOS terminates an app that requests the protected resource and App Store Connect rejects the upload (ITMS-90683); without a language's text, users of that language see the prompt in the development language.
15. **Human judgement steps never block the pipeline.** A translation review, a play-test or a look at a new screen go into the report under "Human steps (not blocking)"; only "ship", "submit" and missing real values gate what happens next. Why: the release stays a machine-checkable process, and the person still sees everything they should judge.
16. **A keyless rehearsal is never release evidence.** `check-store-artifact.mjs --rehearsal` exists only for an archive built with `CODE_SIGNING_ALLOWED=NO`: it prints `REHEARSAL: not a release gate`, reports only the signing rule as `SKIP` and keeps every other rule strict; `release:ios` never passes it. Why: a rehearsal proves the build, never what users receive.

## Workflow

1. **Before the first release in a repo:** read [references/signing-and-keys.md](references/signing-and-keys.md) and [references/human-steps.md](references/human-steps.md). Ask the developer for every missing once-only step (developer program and agreements, the team API key with the Admin role, the Xcode licence) and the per-app steps (the app record for each uploaded variant with its internal tester group) in one message.
2. **Pick the lane.** EAS (default): read [references/eas-lane-and-android.md](references/eas-lane-and-android.md); `eas-build-and-submit` sets up profiles and credentials, and this skill adds the contract and the gate. Local lane: install the templates (line 1 of each names its repo path; fill `__APP_ID__`):

   | Template | Goes to |
   |---|---|
   | `templates/scripts/release/*` (CLI, steps, pure modules with tests, both export options files) | `scripts/release/` |
   | `templates/scripts/asc/*` (JWT, credentials, REST client, app lookup, What to Test, with tests) | `scripts/asc/` |
   | `templates/contracts/ios-release.json` + `.schema.json` | `contracts/` (both lanes) |
   | `templates/scripts/ios/toolchain.ts`, `templates/scripts/clock/system-clock.ts`, `templates/src/config/app-variant.ts` (+ tests, canonical) | their paths, when missing |

   Add the build-number lines to `app.config.ts` ([examples/app-config-version.ts](examples/app-config-version.ts)) and `"release:ios": "node scripts/release/release-ios.ts"` to `package.json`, then run `npm run typecheck`, `npx eslint scripts --max-warnings 0` and `npx jest scripts --ci --maxWorkers=2`.
3. **Check the setup:** `node ${CLAUDE_SKILL_DIR}/scripts/check-release-setup.mjs .`. Fix every `FAIL` and rerun until `RESULT: PASS`; [references/contract-and-checks.md](references/contract-and-checks.md) explains every rule and contract key. An EAS-only repo prints `NOT APPLICABLE` (no local lane).
4. **Prepare the commit:** `npm run verify` green, the version raised above the last release tag for a production build, E2E and screenshots of this commit when the repo has them. Without the team key yet, rehearse instead ([references/release-pipeline.md](references/release-pipeline.md), "Rehearsal without the key"): an unsigned archive and the gate with `--rehearsal`; it uploads nothing.
5. **Release, with the developer's go-ahead.** Local: `npm run release:ios -- --variant production` (or `preview`; add `--notes "..."` for what testers should check, `--known-issue "..."`). EAS, in the order `eas-build-and-submit`'s release preflight prints: `eas build --profile production --platform ios`, `check-eas-build` on its record, download the `.ipa` to `build/ios-release/export/app.ipa`, run this gate on it, then `eas submit --profile production --platform ios --path build/ios-release/export/app.ipa --non-interactive --what-to-test '<text>'`. The pipeline reference says what each of the 12 steps does and how to run one by hand.
6. **Prove the build:** `node ${CLAUDE_SKILL_DIR}/scripts/check-store-artifact.mjs . --ipa <ipa> --variant <v> --version <x.y.z> --build <n>` must print `RESULT: PASS` without `--rehearsal`, and the run must have printed `processed (VALID)` (EAS: the build shows in the TestFlight tab).
7. **On any failure**, read the message the run printed (it already matched [references/failure-playbook.md](references/failure-playbook.md)). A stop goes to the developer as printed, without the `(log: ...)` and `Resume:` lines, which are for you. Then rerun as the `Resume:` line says: the same command, `--resume build` (same number, nothing uploaded) or `--resume processing` (the upload is done). REST errors: [references/app-store-connect-api.md](references/app-store-connect-api.md).
8. **Report and wait:** one message shaped like [examples/release-messages.md](examples/release-messages.md): app, version, build, variant, gate result, What to Test, the one question ("ship" or "don't ship") and "Human steps (not blocking)". On "ship": `git tag -a v<version> -m "..."`; submission only on "submit". Then `git-commits-and-reporting` checks the tags and the report.

## Definition of done

- [ ] The developer agreed to this upload in this session; nothing was pushed or submitted without their word.
- [ ] The release finished: build number bumped and committed (local) or counted remotely (EAS), gate passed, validated, uploaded, processing `VALID`, What to Test set, annotated upload tag created.
- [ ] No key material, token or signing file appears in the repo, logs or report; the key was never opened.
- [ ] The developer has one report with the build, the evidence, the one question and the human steps that do not block.
- [ ] No `REHEARSAL` result is cited as release evidence; a hand-over before the real values exist is a slice report with the rehearsal under "Not tested or not verified".
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-store-artifact.mjs . --ipa <ipa> --variant <v> --version <x.y.z> --build <n>` prints `RESULT: PASS` (a ship gate: no SKIP line; the only SKIP, `[get-task-allow] REHEARSAL: ...`, belongs to a `--rehearsal` run).
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-release-setup.mjs .` prints `RESULT: PASS` (or `NOT APPLICABLE` on an EAS-only repo)

## Anti-patterns

- **Retrying after `errSecInternalComponent`, a 401 or an agreement error.** Send the stop message and wait.
- **`cat ~/.appstoreconnect/private_keys/AuthKey_*.p8` "to check the key".** Check path and mode with `stat`; the file is never opened.
- **Switching to manual signing or importing a `.p12` when automatic signing fails.** Follow the playbook row (missing flags, `appleTeamId` before prebuild, key role) or stop.
- **Reusing build 14 after a failed upload, or lowering `IOS_BUILD_NUMBER`.** A number is spent once an upload was attempted; rerun without `--resume` so it bumps again.
- **A plain rerun after the upload "because processing timed out".** That uploads a second build; use `--resume processing`.
- **Announcing "uploaded" after altool or `eas submit` returns.** Wait for `VALID`; `INVALID` needs Apple's email and a new build.
- **Skipping the gate "because the simulator production build was clean", or because EAS built it.** The gate checks the signed export users receive.
- **Uploading a preview build with the production export options**, or giving preview and production one bundle id. Preview builds are internal-only by construction.
- **Local lane next to EAS remote versioning.** Two counters collide; pick one (`check-release-setup` rule `version-source`).
- **Submitting for review because the developer said "ship".** "Ship" tags the release; "submit" submits.
- **Typing a real-looking value over a placeholder to pass the gate.** The bundle id, ad ids and links come from the developer: ask, and report it as a human step.
- **Citing a `--rehearsal` run as the store gate, or passing `--rehearsal` in the pipeline.** A rehearsal proves the build, never what users receive.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/signing-and-keys.md](references/signing-and-keys.md) | What signs what, the team key and its role, the three variables, key and token rules, keychain, entitlements, leak response, verified vs not | Workflow step 1, and on any signing error |
| [references/release-pipeline.md](references/release-pipeline.md) | Steps 0-12 with every command, ExportOptions keys, the gate by hand, processing wait, What to Test, resuming, the keyless rehearsal, versions and tags, after "ship" | Workflow steps 4-5, and to run a step by hand |
| [references/eas-lane-and-android.md](references/eas-lane-and-android.md) | The EAS lane to TestFlight (profiles, local EAS builds, getting the `.ipa`, submit, remote versions, tags) and the Android counterpart of every step | Workflow steps 2 and 5 |
| [references/contract-and-checks.md](references/contract-and-checks.md) | Every contract key, the `rn-skills.config.json` keys, every checker rule with its reason, when multi-package | Workflow step 3, and when a check fails |
| [references/app-store-connect-api.md](references/app-store-connect-api.md) | REST endpoints and when to use them, token rules, the `scripts/asc/` modules, error codes | When a REST call fails or a new one is needed |
| [references/human-steps.md](references/human-steps.md) | Human steps once, per app and per release, how to ask, the release checklist | Workflow steps 1 and 4 |
| [references/failure-playbook.md](references/failure-playbook.md) | Symptom, cause and action for every known release failure; stops; open questions | Workflow step 7 |
| [examples/release-messages.md](examples/release-messages.md) | A finished-release report, a stop message, an app record request, and bad versions | Workflow step 8 |
| [examples/app-config-version.ts](examples/app-config-version.ts) | The version, build number and team id lines of `app.config.ts` (shape, merge into the app's own) | Workflow step 2 |
| `templates/scripts/release/` | `release-ios.ts` (CLI, `--resume build\|processing`), `release-preflight.ts`, `release-build.ts`, `release-upload.ts`, `release-steps.ts`, `artifact-facts.ts`, and the tested pure modules `release-options.ts`, `release-config.ts`, `release-failures.ts`, `build-number.ts`, `what-to-test.ts`, `processing.ts`, `processing-wait.ts`, `store-gate.ts`, `test-only-sentinels.ts`; `bump-build-number.ts`; `export-options-{preview,production}.plist` | Workflow step 2 (local lane) |
| `templates/scripts/asc/` | `asc-jwt.ts` (+ `asc-jwt.test.ts`), `asc-credentials.ts`, `asc-client.ts` (canonical, synced from the library and owned by this skill; do not edit here; in-app-purchases uses the same three), `find-app.ts`, `print-app-record.ts`, `beta-notes.ts`, with tests | Workflow step 2 (local lane) |
| `templates/contracts/ios-release.json` | The release contract (appId, branch, scripts, usage strings, encryption answer, forbidden strings, unfinished markers, production ads mode, What to Test lines) | Workflow step 2 (both lanes) |
| `templates/contracts/ios-release.schema.json` | Its schema, with what each key does and its default | When editing the contract |
| `templates/scripts/ios/toolchain.ts` | The Xcode pin and `selectXcode()` (synced from the library; do not edit here) | Workflow step 2, when missing |
| `templates/scripts/ios/toolchain.test.ts` | Its tests (synced; do not edit here) | With the toolchain |
| `templates/scripts/clock/system-clock.ts` | `nowEpochSeconds()`, the only wall-clock reader (synced; do not edit here) | Workflow step 2, when missing |
| `templates/scripts/clock/system-clock.test.ts` | Its tests (synced; do not edit here) | With the clock |
| `templates/src/config/app-variant.ts` | The variant resolver, `variantEnv`, `variantIdentity` (synced; do not edit here) | Workflow step 2, when missing |
| `templates/src/config/app-variant.test.ts` | Its tests (synced; do not edit here) | With the resolver |
| `scripts/check-release-setup.mjs` | Checks the local lane's setup: files, ExportOptions, contract, build number, team id, placeholders, scripts, signing, key and token hygiene, `.gitignore`, deny rules, Xcode switch, unfinished markers | Workflow step 3 and the definition of done |
| `scripts/check-store-artifact.mjs` | The store-artifact gate on an `.ipa` or `Payload/<App>.app` from either lane; `--rehearsal` for the keyless dry run only | Workflow step 6 and the definition of done |
| `scripts/lib/release-contract.mjs` | Reads the contract, the Xcode pin, dependencies and test-only sentinels for both checkers | Never by hand |
| `scripts/lib/artifact-rules.mjs` | The rules of `check-store-artifact` | Never by hand |
| `scripts/lib/plist.mjs` | XML and binary plist reader (synced from the library; do not edit here) | Never by hand |
| `scripts/lib/usage-strings.mjs` | Usage descriptions per language (synced; do not edit here) | Never by hand |
| `scripts/lib/ship-placeholders.mjs` | The placeholder values a ship gate refuses (synced; do not edit here) | Never by hand |
| `scripts/check-lib.mjs` | Shared checker library (synced; do not edit here) | Never by hand |
| `scripts/selftest.mjs` | Proves both checkers pass their good fixtures and catch every planted bug (key files and `.ipa` files are made at run time) | After changing a checker or a template |
| `assets/shared.json` | The shared files this skill syncs in | When adding a shared file |
| `assets/template-placeholders.json` | Values for the template placeholders in template checks | When a template gains a placeholder |
| `tests/bases/` | The app repo and the unpacked `.app` the fixtures assemble from | When adding a fixture |
| `tests/fixtures/` | Overlay cases per checker: good, one bad case per rule, pass and error cases | When adding a rule |

## Related skills

- `eas-build-and-submit` - `eas.json` profiles, EAS credentials and cloud builds (the default lane).
- `android-release-play` - the same release on Google Play.
- `ios-simulator-build` - Release simulator builds, the Xcode pin and the variant proof before a release.
- `app-variants-and-environment` - the variant resolver, bundle ids per variant and the Metro cache key.
- `git-commits-and-reporting` - release commits, tags, the report and stop messages.
- `privacy-and-store-declarations` - the privacy manifest, the audits after prebuild and the App Privacy answers.
- `quality-gates` - the verify gate the preflight runs.
- `e2e-maestro` - flows and screenshots of the release commit.
- `debug-menu-and-test-hooks` - the test-only gate and the sentinel the gate looks for.
- `admob-ads-and-consent` - real ad ids per variant, SKAdNetwork, `app-ads.txt`.
- `in-app-purchases` - products, the StoreKit test harness the gate refuses in production.
- `troubleshooting-playbook` - failures outside the release pipeline.
