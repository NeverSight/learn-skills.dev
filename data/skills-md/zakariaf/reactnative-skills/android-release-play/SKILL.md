---
name: android-release-play
description: "Ships Android App Bundles to Google Play: upload key, Play App Signing, AAB gate, versionCode, tracks, rollout. Use when releasing or signing for Play, or an upload, rollout or version code fails. Not for eas.json (eas-build-and-submit)."
---

# Android release to Google Play

Takes one green commit to a signed Android App Bundle on a Google Play testing track, then to users by
staged rollout, on the EAS lane (EAS Build + EAS Submit, the default) or the local lane (Gradle + the
Play Developer API). Before anything reaches Google, the store-AAB gate reads the exact bundle and
proves what users would get: the registered upload key, a fresh versionCode, the production package,
target SDK 36, 16 KB pages, every permission accounted for, no test code and no template value.
Everything that needs a person is asked for, never worked around. Verified on 2026-10-14 with Expo
SDK 57 (React Native 0.86.3, targetSdk 36, AGP 8.12), eas-cli 24.10.0, aapt2 36.0.0, NDK r28.2 and
JDK 17; the iOS twin is `ios-release-testflight`.

## Rules that must hold

1. **Nothing reaches Google Play without the developer's word in this session, and uploads go only to
   the contract's testing track.** `contracts/android-release.json` `uploadTrack` is `internal`, `alpha`
   or `beta`, and `eas.json`'s Android submit track equals it. Why: an upload, a track change or a tag
   push cannot be undone, and a production upload reaches users before anyone installed it.
   (`contract`, `lane`)
2. **The gate passes on the exact bytes that are uploaded.** `check-store-aab.mjs --stamp` writes the
   bundle's sha256 only after a PASS; the local `upload` refuses any other bytes, and the EAS lane
   submits that file with `eas submit --path` after eas-build-and-submit's record check (never
   `--latest`, never `--auto-submit`, for Android not even from the store profile). Why: a
   bundle rebuilt or picked after the gate is an unchecked bundle. (`gated-upload`, `lane`: `eas.json`
   pins the contract `applicationId`)
3. **A store bundle is signed by the registered upload key, never the debug key.** Play App Signing
   holds the app-signing key; the contract registers the upload certificate's SHA-256 and the gate
   compares it. Why: Play refuses debug-signed bundles and bundles from any other key, and React
   Native's template signs release builds with the debug keystore. (`signing`)
4. **Keys and passwords never enter the repo, a log or the chat, and are never opened.** The EAS lane
   keeps the keystore and the service-account key on EAS; the local lane keeps them in
   `~/.android-keys/` (mode 600), passwords in `~/.gradle/gradle.properties`, read only by Gradle and
   `play-credentials.ts`, never a repo `gradle.properties`, `keystore.properties` or `.env*`; git
   ignores and agents are denied `*.jks`, `*.keystore`, service-account JSON. Why: whoever holds the upload key and the service account releases as the app.
   (`secrets-outside`, `secrets-ignored`, `credentials-read`, `inline-secrets`)
5. **versionCode only goes up, is never reused, and Android counts its own.** EAS counts remotely
   (`appVersionSource: remote`, `autoIncrement`); the local lane keeps one literal
   `const ANDROID_VERSION_CODE = <n>;` feeding only `android.versionCode` (the iOS twin keeps its own
   `IOS_BUILD_NUMBER`), bumped and committed by the build; uploads are tagged `vX.Y.Z+android.<n>` on
   both lanes, and every bundle is above every Android upload tag. Why: Play refuses a versionCode it
   has seen, forever, and one scheme per app keeps the tag order meaningful. (`version-code`,
   `version-name`, `version-source`)
6. **A store bundle is the production variant: the contract's package, a matching embedded config, no
   test-only code, not debuggable, no cleartext traffic.** Why: a lost `APP_VARIANT` ships the debug
   menu or another app id, and these are invisible in the source. (`package`, `constants-variant`,
   `test-code`, `debuggable`, `cleartext`)
7. **targetSdkVersion is 36 or higher, in the bundle and in the config.** Why: from 2026-08-31 Play
   refuses new apps and updates below API 36; Expo SDK 57 targets 36, so only an override lowers it.
   (`target-sdk`, `target-sdk-config`)
8. **Native libraries support 16 KB pages and ship 64-bit.** Every arm64-v8a/x86_64 `.so` has 16 KB
   LOAD alignment, uncompressed libraries are 16 KB zip-aligned, every 32-bit library has its 64-bit
   twin. Why: a 4 KB library crashes at start on 16 KB devices, and Play refuses such updates from
   2027-02-01 and 32-bit-only code already. (`page-alignment`, `abi-64bit`)
9. **Every permission in the bundle is in the contract with its reason, and Play-declared ones name
   their declaration.** Development-only permissions (`SYSTEM_ALERT_WINDOW`) are blocked for release.
   Why: libraries add permissions silently, each changes the Data safety answers, and an undeclared
   sensitive permission gets the release rejected. (`permissions`, `permission-declaration`)
10. **No template value ships.** No `com.example.*`, Google sample or all-zero AdMob id, `example.com`
    link or `__NAME__` token in the package, the manifest or the embedded config; the AdMob app id is
    present and the app's own. Why: they are format-valid and pass every other check. (`ship-placeholder`,
    `ad-app-id`, `upload-cert` with `--release`)
11. **Production is reached only by staged rollout of an uploaded versionCode, at the contract's
    steps; a bad release is halted, never rebuilt.** Why: a fraction limits the harm of a regression,
    and a halted versionCode is spent. (`rollout`, `halt`, contract `rollout`)
12. **Stop and ask, never retry, on 401/403, an app not found, the API not enabled, a draft app, a used
    version code or missing declarations; a `--rehearsal` is never release evidence.** Why: each
    needs a person or a new number; retries lock accounts and burn numbers.

## Workflow

1. **Before the first release:** read [references/human-steps.md](references/human-steps.md) and
   [references/signing-and-keys.md](references/signing-and-keys.md); ask the developer for every
   missing human step in one message, each with its default.
2. **Install the templates** (each to the path its first line names; tests first, see them fail on an
   assertion, then the module: `tdd-workflow`):
   - both lanes: `templates/contracts/android-release.json` + schema; fill `applicationId`,
     `permissions` (from the merged manifest), `lane`;
   - local lane: `templates/scripts/release-android/` (CLI and seven tested modules),
     `templates/scripts/clock/system-clock.ts` + test (the CLI's clock; synced, skip when present),
     `templates/plugins/with-upload-signing.ts` + test, and the three app edits in
     [examples/app-config-local-lane.md](examples/app-config-local-lane.md) (`ANDROID_VERSION_CODE`,
     the plugin line, `"release:android": "node scripts/release-android/release-android.ts"`);
   - EAS lane: `eas.json` comes from `eas-build-and-submit`; make its Android submit track equal
     `uploadTrack`, and keep `--auto-submit` off Android.
   Then `npm run -s check:fast`.
3. **Check the setup:** `node ${CLAUDE_SKILL_DIR}/scripts/check-play-release-setup.mjs .` until
   `RESULT: PASS`; before a store build add `--release`.
4. **Build** with the developer's go: EAS (`eas build --platform android --profile production --non-interactive --freeze-credentials --json`,
   eas-build-and-submit's `check-eas-build` on the record, then download its
   `artifacts.applicationArchiveUrl` to `build/release-android/app-release.aab`) or local
   (`npm run release:android -- build`). Steps and by-hand
   commands: [references/release-pipeline.md](references/release-pipeline.md). Without a key yet,
   rehearse (same reference, "Rehearsal without a key").
5. **Gate:** `node ${CLAUDE_SKILL_DIR}/scripts/check-store-aab.mjs . --aab <bundle> --version-code <n> --stamp build/release-android/aab-gate.json`
   until `RESULT: PASS`. Each rule and its source: [references/play-policy-and-artifact.md](references/play-policy-and-artifact.md).
   First release: register the printed fingerprint after confirming it.
6. **Upload** with the developer's word (name a pending schema version in the ask: run-migration
   records it with `record-shipped` after the upload; design-review-workflow's `check-signoff.mjs` passes
   first when the app uses it): `eas submit --platform android --profile production --path build/release-android/app-release.aab --non-interactive`
   or `npm run release:android -- upload`; then the annotated tag
   `vX.Y.Z+android.<n>`. Calls and stops:
   [references/play-api.md](references/play-api.md).
7. **Roll out** later, each step with its own word:
   [references/tracks-and-rollout.md](references/tracks-and-rollout.md).
8. **On any failure** match [references/failure-playbook.md](references/failure-playbook.md); a stop
   goes to the developer as one message and is never retried.
9. **Report** (git-commits-and-reporting): version, versionCode, the gate's RESULT line, the track,
   the tag, the human checks; model: [examples/release-run.md](examples/release-run.md).

## Definition of done

- [ ] The developer agreed to the upload in this session; nothing was pushed, promoted or submitted
      without their word; production changed only by a contract rollout step.
- [ ] The bundle came from a clean, verified commit; the gate passed on those exact bytes with a stamp,
      and the uploaded file's sha256 equals the stamp's.
- [ ] No key, password, service-account JSON or token appears in the repo, a log or the report, and
      none was opened.
- [ ] The upload tag is annotated and local (pushed only with the developer's word).
- [ ] Before the first key exists: the rehearsal printed `REHEARSAL: not a release gate` and the
      report lists it under "Not tested or not verified".
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-play-release-setup.mjs . --release` prints
      `RESULT: PASS` (without `--release`, `NOT APPLICABLE: nothing in the repo ships to Google Play yet`
      is expected until the contract exists).
- [ ] The gate run below used no `--rehearsal`; it never skips (a ship gate: no SKIP, no NOT APPLICABLE).
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-store-aab.mjs . --aab <bundle> --version-code <n> --stamp build/release-android/aab-gate.json` prints `RESULT: PASS`

## Anti-patterns

- **`eas build --auto-submit` or `eas submit --latest`.** The gate never saw those bytes; download
  the artifact, gate it, submit it with `--path`.
- **`eas build` without `--freeze-credentials`.** A non-interactive build may then update
  credentials, and a second keystore for the same application id is refused by Play for good.
- **Two passwords for the upload keystore.** PKCS12 keeps one; keytool ignores the second and
  Gradle fails to sign. Generate one and write it under both property names.
- **One `BUILD_NUMBER` for both stores with `+<n>` tags while iOS tags `+ios.<n>`.** Mixed schemes
  break the tag order; Android counts in `ANDROID_VERSION_CODE` and tags `+android.<n>`.
- **`keytool -list -keystore ...` "to check the key".** That opens it; `stat` the file, and read a
  bundle's signer with `keytool -printcert -jarfile <aab>`.
- **`-Pandroid.injected.signing.store.password=...` or a password in `build.gradle`.** It lands in the
  process list and logs; Gradle reads `~/.gradle/gradle.properties` by itself.
- **Retrying after a 403 or lowering the build number after "version code already used".** The first
  needs a person, the second a new number.
- **Uploading straight to production, or promoting to 100 % at once.** Upload to the testing track;
  promote in the contract's steps after a person checked the crash-free rate.
- **Adding a permission to the contract to make the gate pass.** Find who adds it; block it unless the
  app uses it, and then review Data safety.
- **Ignoring a `page-alignment` FAIL because the app "works on my phone".** 4 KB phones load it; 16 KB
  devices crash. Update the library.
- **Citing a `--rehearsal` run as the store gate**, or typing stand-in ids to get past
  `ship-placeholder`.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/signing-and-keys.md](references/signing-and-keys.md) | Play App Signing, the upload key on each lane, the plugin, the registered fingerprint, the service account, may/may-not, leak response | Workflow step 1, any signing error |
| [references/release-pipeline.md](references/release-pipeline.md) | EAS lane, local lane, gate and stamp, rehearsal, version codes and tags, resuming, multi-package | Workflow steps 4-6 |
| [references/play-policy-and-artifact.md](references/play-policy-and-artifact.md) | What the gate reads, each rule with its Play source, target SDK, 16 KB, permissions, App content, contract fields | Workflow step 5, any gate FAIL |
| [references/tracks-and-rollout.md](references/tracks-and-rollout.md) | Tracks, staged rollout, halt, draft apps, new accounts' closed test | Workflow step 7 |
| [references/play-api.md](references/play-api.md) | JWT and token, upload and track calls, stops | Workflow step 6, an upload stop |
| [references/human-steps.md](references/human-steps.md) | Account, app, service account, App content, testers, first upload, human checks | Workflow step 1, before asking |
| [references/failure-playbook.md](references/failure-playbook.md) | Symptom, cause, action for setup, build, gate, upload, after | Workflow step 8 |
| [examples/app-config-local-lane.md](examples/app-config-local-lane.md) | The app config, script and contract of a local-lane app | Workflow step 2 |
| [examples/release-run.md](examples/release-run.md) | An EAS-lane release from gate failure to rollout and report | Workflow step 9 |
| `templates/contracts/` | The release contract `android-release.json` and its schema | Workflow step 2 |
| `templates/plugins/` | `with-upload-signing.ts` (release builds signed by the upload key when its properties exist) and its test | Workflow step 2 (local lane) |
| `templates/scripts/release-android/` | The local-lane CLI `release-android.ts` (build, upload, rollout, halt) and its tested modules: `release-args`, `release-plan` (preflight, stamp, toolchain), `version-code`, `upload-key`, `play-credentials`, `play-client`, `rollout` | Workflow steps 2, 4, 6, 7 (local lane) |
| `templates/scripts/clock/` | The canonical `system-clock.ts` (dependency-management's) and its test, which the CLI imports for the token's time (synced; do not edit) | Workflow step 2, when missing |
| `templates/src/config/` | The canonical `app-variant.ts` and its test, which the CLI imports (synced; do not edit) | Workflow step 2, when missing |
| `scripts/check-play-release-setup.mjs` | Repo setup: contract, lane, plugin, version code, target SDK, secrets, credentials, inline passwords (code, `*.properties`, `.env*`), no Android `--auto-submit`/`--latest`; `--release`; `--app-dir` when multi-package | Workflow step 3, definition of done |
| `scripts/check-store-aab.mjs` | The store-AAB gate (ship gate; `--rehearsal`, `--stamp`) | Workflow step 5, definition of done |
| `scripts/lib/aab.mjs` | ZIP, protobuf manifest, ELF, BundleConfig and PKCS#7 reader | Never by hand |
| `scripts/lib/release-facts.mjs` | Contract, app config, tags and sentinel helpers of both checkers | Never by hand |
| `scripts/lib/aab-fixture.mjs` | Writes self-test bundles from a JSON spec | When adding a gate case |
| `scripts/lib/ship-placeholders.mjs` | The template values every ship gate refuses (synced; do not edit) | Never by hand |
| `scripts/check-lib.mjs` | Shared script helper (synced; do not edit) | Never by hand |
| `scripts/selftest.mjs` | Proves the stamp and both checkers on good fixtures and every planted bug | After changing a checker, a fact or a template |
| `assets/play-facts.json` | Play's numbers and lists with sources (target SDK, versionCode max, 16 KB, declarations) | When a Play requirement changes |
| `assets/template-placeholders.json` | Placeholder values for template verification | Never by hand |
| `assets/shared.json` | The shared files this skill syncs | When adding a shared file |
| `tests/bases/app/` | The local-lane Tasks app every case starts from (with the templates) | When adding a rule |
| `tests/fixtures/` | One suite per checker: `SUITE.json`, good, one bad-* per rule, pass-* and error-* cases | When adding a rule |
| `tests/real-tools.json` | Real aapt2 manifest, NDK libraries and jarsigner blocks (public test certificates) | When the reader changes |

## Related skills

- `eas-build-and-submit` - owns `eas.json` and the EAS commands this lane runs.
- `android-emulator-build` - the toolchain and the Release emulator build proven before a release.
- `ios-release-testflight` - the iOS twin; its own `IOS_BUILD_NUMBER` and `+ios.<n>` tags.
- `privacy-and-store-declarations` - the Data safety answers and the network audit.
- `admob-ads-and-consent` - the production AdMob app id; `in-app-purchases` - Play products.
- `git-commits-and-reporting` - release commits, tags, stop messages and the report.
- `ota-updates` - JavaScript fixes without a store release.
