---
name: ota-updates
description: Ships EAS Update over-the-air updates - fingerprint runtimes, a channel per variant, rollout, rollback. Use when running eas update, setting runtimeVersion or channels, or an update never arrives. Not for store builds (eas-build-and-submit).
---

# OTA updates

An update reaches only the binaries whose native layer it was made for: the runtime version is the
fingerprint of the native inputs, each shipping variant bakes its own channel into its binaries, every
publish names that channel and its environment, passes the gates and a preflight that proves the
runtime is live, and reaches a store channel in stages. Launch never waits for the network, the
anti-brick recovery stays on, the app checks again when it returns to the foreground and restarts
only on the person's tap. One zero-dependency checker proves the repo side.

## Rules that must hold

1. **The runtime version is the fingerprint, one policy for the app.** `runtimeVersion:
   { policy: 'fingerprint' }` at the top level (from `updatesConfig()`), no string, no
   `appVersion`/`nativeVersion`, no `ios`/`android` override. Why: an update reaches a binary only
   when the runtime versions match; a hand-kept number lets JS reach a binary that lacks its native
   code, while a wrong fingerprint only reaches nobody, which the preflight catches.
   (`runtime-policy`)
2. **The fingerprint hashes native inputs and nothing else.** Ship `fingerprint.config.js`: lifecycle
   scripts (`pre`/`post` `install` and `prepare`, `eas-build-*`) stay in the hash, other
   npm scripts and the app version fields leave it; never skip every script. Why: measured on SDK 57,
   editing the `lint` script or bumping only `version` gave every binary a new runtime and stranded
   the next update; a `postinstall` that patches native code must still count. (`fingerprint-scripts`)
3. **`updates.url` is the project's EAS Update URL.** `https://u.expo.dev/<id>` with the same id as
   `extra.eas.projectId`, built by `easUpdateUrl()`. Why: a wrong id makes binaries ask another
   project, or none, and `Updates.isEnabled` is false without a URL. (`updates-url`, `updates-config`)
4. **Updates are on with a URL, or off explicitly.** With expo-updates installed, every shipping
   variant either has `updates.url` or says `updates: { enabled: false }`; expo-updates is a
   dependency, never a devDependency. Why: installed but unconfigured is silently disabled, and EAS
   Build ignores channels when the package is a devDependency. (`updates-config`, `updates-off-publish`)
5. **Launch never waits and recovery stays on.** `fallbackToCacheTimeout: 0`, `checkAutomatically:
   'ON_LOAD'`, no `useEmbeddedUpdate: false`, no `disableAntiBrickingMeasures` or `useNativeDebug`
   committed. Why: a launch that waits on the network leaves people on the splash; `NEVER` turns off
   error recovery's fix check (a broken update stays until a reinstall), `ON_ERROR_RECOVERY` asks only
   after a crash at launch, `WIFI_ONLY` delays every fix on cellular.
   (`launch-nonblocking`, `error-recovery`)
6. **One channel per shipping variant, baked into its builds.** Each eas.json build profile of a
   shipping variant sets `channel` = its variant = `environment` (the variant is `env.APP_VARIANT`,
   else the EAS environment's; with no `environment`, EAS Build picks production for store distribution,
   development for a development client, preview otherwise); every shipping variant has such a profile; the dev client has none; no channel
   serves two variants. Why: the channel is fixed in the binary at build time, a binary built without
   one never receives an update, and an update embeds one variant's config and runtime.
   (`build-channel`)
7. **Every publish names its channel, its environment and a message.** `eas update --channel <v>
   --environment <v> --message "<fix>"`; never `--auto`; EAS Workflows update jobs set `environment`.
   Why: `eas update` evaluates the config with the EAS environment's variables, so another environment
   means another runtime version and another embedded config; in CI (`CI` set) the CLI neither asks
   for nor requires `--environment` and silently loads none; EAS Workflows defaults to production.
   (`update-target`, `update-environment`)
8. **Nothing native ships over the air.** An update goes out only after `npm run verify` and
   `scripts/ota/update-preflight.ts`, which resolves each platform's runtime with the channel's
   environment and refuses one that no finished build on that channel has. A new SDK, native package,
   plugin or config change means a store build first. Why: EAS CLI does not check it, and JS for native
   code a phone lacks crashes it at launch. (`gates-first`, `update-preflight`)
9. **Store channels roll out in stages.** The first publish to a store channel uses
   `--rollout-percentage` 1-25, raised with `eas update:edit` after `eas update:insights` shows a crash
   rate no worse than the control's; preview needs no rollout; a CI job names its channel literally,
   and `--branch production` counts as the production channel (they are linked by name).
   Why: an update reaches every phone of the channel at its next launch; a rollout bounds the damage
   of a bad one, and one job with `--channel ${{ inputs.channel }}` either throttles preview or sends
   production to everyone. (`staged-rollout`)
10. **An update is published per channel, never promoted across channels.** The same commit is
    published to preview, tested, then published to production with production's environment; no
    `eas update:republish --destination-channel`. Why: the republished bundle carries the source
    variant's config and runtime. (`cross-channel-republish`)
11. **Rolling back is a person's decision, and never past a data migration.** Pause the channel
    first (`eas channel:pause`); revert a rollout (`update:revert-update-rollout`, `channel:rollout`
    End > Revert) or roll back (`eas update:rollback`) only when no update since the target carried a
    schema step, else fix forward; none of these run in CI. Why: older code against newer data opens
    nothing the user saved (run-migration). (`rollback-manual`)
12. **The app reaches expo-updates only through the UpdatesPort.** One adapter imports expo-updates,
    reads `Updates.isEnabled` before every call, maps a rejection coded `ERR_NOT_AVAILABLE_IN_DEV_CLIENT`
    or `ERR_UPDATES_DISABLED` to `disabled`, never rejects, and exposes `isEmergencyLaunch`; the update
    checker reports an emergency launch once, checks at mount and on return to the foreground at most
    hourly, and applies a downloaded update only on the person's tap. Why: with `isEnabled` false
    (Expo Go, no URL) every method rejects; a development build reports `isEnabled` true and rejects
    checks and fetches with the dev-client code, which would otherwise log a failure at every
    foreground; a broken update must be heard about; a reload drops unsaved input.
    (`updates-adapter`, `adapter-enabled-guard`, `emergency-launch`)
13. **Prove the update path on a release build of each platform.** A preview build on a named iOS
    simulator and Android emulator downloads a preview update at one cold start and runs it at the
    next. Why: debug builds load JS from the dev server, so only a release build runs the updater.

## Workflow

1. Read [references/runtime-versions-and-fingerprints.md](references/runtime-versions-and-fingerprints.md)
   (the policy, what is hashed, the two traps) before touching `runtimeVersion` or native inputs.
2. Install (stack table, verified 2026-10-14): `npx expo install expo-updates` (~57.0.24); it brings the
   CocoaPods pod ReachabilitySwift, which privacy-and-store-declarations' contract lists under
   `sdks['expo-updates'].pods`. The EAS
   project and `eas init` are eas-build-and-submit's; copy `extra.eas.projectId` into one
   `EAS_PROJECT_ID` constant.
3. Copy `templates/src/config/updates-config.ts` (and its test) and spread `updatesConfig(EAS_PROJECT_ID)`
   into `app.config.ts` in place of `updates: { enabled: false }` (`examples/app.config.ts`). Copy
   `templates/fingerprint.config.js` with `templates/scripts/ota/fingerprint-config.test.ts`.
4. Channels: add `"channel": "<variant>"` to each shipping build profile, with `environment` equal;
   the development client gets none: it opens any compatible update from its Extensions tab
   (`examples/eas.json` is eas-build-and-submit's template plus `channel` on each shipping profile;
   its `environment` already equals the variant; eas.json takes no comment key). Ask the developer to create `APP_VARIANT` and `EXPO_PUBLIC_APP_VARIANT` as
   plain-text variables in each EAS environment, plus every variable the config reads; stop and ask
   before running `eas env:create`. Read
   [references/channels-branches-and-publishing.md](references/channels-branches-and-publishing.md).
5. App code: copy `templates/src/services/updates/` and `templates/src/hooks/use-update-checks.ts` (each
   with its test); the synced files come from their owner skills, copy them only if missing:
   `src/core/result.ts` (error-handling-typed-results), `src/config/app-variant.ts`
   (app-variants-and-environment), `src/services/error-log/*` and `src/services/clock/clock-port.ts`
   (architecture-and-boundaries), `src/core/dates/date-key.ts` (seeded-determinism-and-golden-vectors),
   `src/hooks/use-is-app-active.ts` (react-components-and-hooks), `src/services/async/with-timeout.ts`
   (async-safety) and `test/flush-microtasks.ts`. With crash reporting wired, pass
   `beforeApply: () => crashReporter.flush()` to the checker. Wire the composition root and the app root as `examples/composition-root.ts` and
   `examples/app-root-wiring.tsx` show; a "Restart to update" row follows
   `examples/restart-to-update-row.tsx`. Details: [references/app-integration.md](references/app-integration.md).
6. Copy `templates/scripts/ota/update-plan.ts`, `update-preflight.ts` and `update-plan.test.ts`. A CI
   publish follows `examples/ota-update-workflow.yml`: one job per channel with literal channels, the
   message passed through `env:`, each job in the protected GitHub environment named like its channel
   (the shape of ci-pipeline-and-gates' `release.yml`: SHA pins, no cache next to a secret). An EAS
   Workflows update job `needs:` its gate (references/channels-branches-and-publishing.md section 9).
7. Store builds first: build and release each variant with its channel (eas-build-and-submit,
   ios-release-testflight, android-release-play) before the first update.
8. Prove it on release builds of both platforms (rule 13, app-integration section 9).
9. Publishing (each time): `node scripts/ota/update-preflight.ts --channel preview --message "<fix>"`,
   then the printed command after the developer's yes; test on a preview phone; then the same for
   `--channel production --rollout 10`. Watch and raise per
   [references/rollouts-rollbacks-and-incidents.md](references/rollouts-rollbacks-and-incidents.md),
   which also holds the incident runbook. Never publish, raise, roll back or pause without the
   developer's explicit go-ahead.
10. Run `node ${CLAUDE_SKILL_DIR}/scripts/check-ota.mjs .` from the repo root; fix each `FAIL` line
    (rule ids in [references/checker-rules.md](references/checker-rules.md)) and rerun until
    `RESULT: PASS`.

## Definition of done

- [ ] `runtimeVersion` is `{ policy: 'fingerprint' }` and `updates` come from `updatesConfig()` with one
      `EAS_PROJECT_ID`; or `updates: { enabled: false }` while the app ships no OTA.
- [ ] `fingerprint.config.js` and its test are in place; `npx expo-updates runtimeversion:resolve
      --platform ios` (and android) gives the same value twice on a clean checkout.
- [ ] Every shipping build profile has `channel` = `APP_VARIANT` = `environment`; each EAS environment
      holds both variant variables (the developer confirmed).
- [ ] The UpdatesPort adapter, fake, checker and hooks with their tests pass `npm run verify`; the
      composition root and the app root are wired.
- [ ] `scripts/ota/update-preflight.ts` exists and every scripted `eas update` runs after the gates.
- [ ] A preview update was seen running on a release build of iOS and of Android.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-ota.mjs .` prints `RESULT: PASS` (an app without eas.json
      yet may print `SKIP eas.json [build-channel] not yet created (eas-build-and-submit creates it)`).

## Anti-patterns

- **`runtimeVersion: '1.0.0'` or `{ policy: 'appVersion' }` "to keep it simple".** One forgotten bump
  after a native package and updates crash old binaries. Use the fingerprint.
- **Publishing right after adding a native package or moving the SDK.** The update targets a runtime
  no phone has; ship store builds first, then update.
- **`eas update --auto` or `eas update --channel production` with no `--environment`.** The config is
  evaluated with the wrong variables: another runtime, another app id in `extra`.
- **Promoting a preview update to production with `update:republish --destination-channel`.** Publish
  the commit again with production's environment.
- **`fallbackToCacheTimeout: 30000` to "make sure people get the fix".** Every launch on a slow network
  waits; use foreground checks and a restart prompt instead.
- **`checkAutomatically: 'NEVER'` with checks only in JS.** Error recovery stops fetching a fix.
- **Calling `Updates.reloadAsync()` as soon as a download finishes, or for a language switch.** The
  person loses their input; restarts for direction use `reloadAppAsync` from expo.
- **`eas update:rollback` in a CI step, or past an update that migrated data.** Pause, decide, fix
  forward.
- **Editing npm scripts freely without `fingerprint.config.js`.** Each edit strands the next update.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/runtime-versions-and-fingerprints.md](references/runtime-versions-and-fingerprints.md) | Policy decision, what the fingerprint hashes, per-variant runtimes, the two measured traps, determinism, SDK moves, bare projects | Workflow 1; any change to native inputs |
| [references/channels-branches-and-publishing.md](references/channels-branches-and-publishing.md) | Channels baked in builds, one per variant, branches, the EAS environment, the command and flags, the preflight, no promotion, previews, CI, local lane | Workflow 4, 6, 9 |
| [references/rollouts-rollbacks-and-incidents.md](references/rollouts-rollbacks-and-incidents.md) | Per-update rollouts, insights, error recovery, rollback kinds, pausing, migrations, the incident runbook, code signing | Before raising, rolling back or pausing |
| [references/app-integration.md](references/app-integration.md) | Every updates key and default, launch behaviour, the port, adapter and checker, wiring, testing on both platforms, debugging | Workflow 5, 8 |
| [references/checker-rules.md](references/checker-rules.md) | Every check-ota rule, NOT APPLICABLE and SKIP conditions, options | When check-ota prints FAIL |
| `templates/src/config/` | `updates-config.ts` (`updatesConfig()`, `easUpdateUrl()`) and its test; the synced `app-variant.ts` and its test | Workflow 3 |
| `templates/fingerprint.config.js` | Lifecycle-scripts-only hash and version skips for the fingerprint | Workflow 3 |
| `templates/scripts/ota/` | `fingerprint-config.test.ts` (loads the root config), `update-plan.ts` and its test, `update-preflight.ts` (the CLI) | Workflow 3, 6, 9 |
| `templates/src/services/updates/` | `updates-port.ts`, `expo-updates-adapter.ts`, `fake-updates.ts`, `update-checker.ts`, each with a test | Workflow 5 |
| `templates/src/hooks/` | `use-update-checks.ts` (`useUpdateChecks`, `useUpdateStatus`) and its test; the synced `use-is-app-active.ts` and its test | Workflow 5 |
| `templates/src/core/` | Synced `result.ts` and its test, synced `dates/date-key.ts` (the clock port's type) | Only if the app lacks them |
| `templates/src/services/error-log/` | Synced error-log port and fake with its test | Only if the app lacks them |
| `templates/src/services/clock/` | Synced `clock-port.ts` (the update checker's clock) | Only if the app lacks it |
| `templates/src/services/async/` | Synced `with-timeout.ts` (bounds the checker's `beforeApply`) | Only if the app lacks it |
| `templates/test/` | Synced `flush-microtasks.ts` | Only if the app lacks it |
| `examples/app.config.ts` | The OTA lines of the app config | Workflow 3 |
| `examples/eas.json` | The channel of each build profile | Workflow 4 |
| `examples/composition-root.ts` | Creating the adapter and the checker | Workflow 5 |
| `examples/app-root-wiring.tsx` | Where the foreground checks start | Workflow 5 |
| `examples/restart-to-update-row.tsx` | The "Restart to update" settings row | Workflow 5 |
| `examples/ota-update-workflow.yml` | A manual GitHub Actions publish: a preview job and a staged production job | Workflow 6 |
| `scripts/check-ota.mjs` | The checker (Node, zero dependencies) | Workflow 10 |
| `scripts/lib/app-config.mjs` | Evaluates the app config once per variant | When changing the checker |
| `scripts/lib/evaluate-app-config.mjs` | The child process that evaluates one variant's config | When changing the checker |
| `scripts/lib/eas-profiles.mjs` | Resolves eas.json build profiles and their channels | When changing the checker |
| `scripts/lib/update-commands.mjs` | Finds every eas update / update:* / channel:* command | When changing the checker |
| `scripts/lib/ota-code-rules.mjs` | The fingerprint-config and adapter rules | When changing the checker |
| `scripts/check-lib.mjs` | Shared checker library (synced) | Never edit |
| `scripts/selftest.mjs` | Proves the checker against `tests/fixtures/` | After changing the checker |
| `tests/` | The fixture base app and one case per rule (`tests/bases/`, `tests/fixtures/`) | With the self-test |
| `assets/ota-facts.json` | Verified versions, the update host, the first-rollout ceiling | When re-verifying |
| `assets/shared.json` | Which canonical files are synced in | When syncing |

## Related skills

- Expo's official `eas-update` skill - the API reference for EAS Update; this skill enforces the
  rules around it.
- `eas-build-and-submit` - eas.json profiles, the EAS project, store builds, fingerprint ignore rules.
- `app-variants-and-environment` - APP_VARIANT, EAS environments and their variables.
- `expo-prebuild-and-config-plugins` - native inputs and a deterministic app config.
- `expo-sdk-upgrade` - an SDK move changes the runtime: store builds before updates.
- `app-startup-and-bootstrap` - OTA checks are deferred work after the splash.
- `architecture-and-boundaries` - the composition root, the clock port and the UpdatesPort's place.
- `react-components-and-hooks` - `useIsAppActive`, which the foreground checks read.
- `run-migration` - why a rollback never goes past a shipped schema step.
- `crash-reporting-and-observability` - the flush before the reload (`beforeApply`) and each update's source maps.
- `ci-pipeline-and-gates` - the CI job that publishes.
- `ios-release-testflight`, `android-release-play` - the store builds an update depends on.
