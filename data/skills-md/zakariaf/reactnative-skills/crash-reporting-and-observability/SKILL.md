---
name: crash-reporting-and-observability
description: "Wires Sentry crash reporting behind a port: start on consent, PII scrubbing, releases, source maps per build and update. Use when adding Sentry or a DSN, or stacks are minified. Not for analytics (analytics-and-consent)."
---

# Crash reporting and observability

Makes an Expo app report its crashes to Sentry through one port and one adapter, plugged into the
canonical root skeleton as a root kit (one registry entry, no root file edited): nothing leaves the
device before the person's choice, nothing personal leaves at all, every error reaches exactly one
issue, and every store build and OTA update can be read in TypeScript source. One zero-dependency
checker proves it on the real code and configs.

## Rules that must hold

1. **`@sentry/react-native` is imported only by `src/services/crash-reporter/sentry-crash-reporter-adapter.ts`
   (never the root entry file, where Sentry's manual setup puts `Sentry.init`); the app reports through `CrashReporterPort`** (`setConsent`, `captureException`, `addBreadcrumb`,
   `flush`, `status`), created once by the root-kit registry (`src/services/create-root-kits.ts`, part of
   the composition root), tests through `createFakeCrashReporter()`, and Jest gets the root mock.
   `sentry-expo` is never installed. *Why:* one file decides what leaves the device, and the real
   SDK in Jest leaks a timer that keeps workers alive.
2. **Nothing is sent before the person's choice, and never from development or tests.** The adapter
   does no I/O when created (no `Sentry.init` in the factory body); `Sentry.init` runs inside `setConsent(true)` only, which
   `useCrashReportingConsent` calls from the crash reporting kit's effects, mounted beside the root
   Stack after the splash release (never the registry, the composition root or the root layout); the
   choice comes from a consent source over the settings field (or `fixedCrashConsent(false)` until the
   app has the row); earlier reports wait in a bounded queue and a refusal drops them; the
   development variant and an empty DSN never start the SDK. The settings default follows the
   contract's `consentModel` (`opt-in` by default). *Why:* crash data is personal data under most
   privacy laws, and startup must open no connection before the first frame.
3. **The options are the privacy-first set.** `sendDefaultPii: false` written; no screenshots, view
   hierarchy, Session Replay, feedback widget, logs or failed-request capture. *Why:* each of those
   sends what the person typed, saw or requested; Sentry's own Expo snippet turns several on.
4. **Every event and breadcrumb passes the scrubber, and no report names a person.** `beforeSend`,
   `beforeSendTransaction` and `beforeBreadcrumb` call `crash-scrubber.ts`; there is no `setUser`
   (only `setUser(null)`), and the port has no member for it; the developer turns on Sentry's
   server-side scrubbing. *Why:* `beforeSend` never sees native crashes, but the JavaScript scope is
   synced into them, so identity set anywhere ends up in reports the scrubber cannot touch.
5. **Each error reaches Sentry exactly once.** The error net keeps Hermes' rejection tracker
   (`reactNativeErrorHandlersIntegration({ onunhandledrejection: false })`), Sentry keeps the global
   handler (it flushes fatal errors, and both native SDKs drop React Native's fatal-JS crash expecting
   it), and the root skeleton's error sink records everything locally and hands each report to the
   kit's `forward: createCrashForwarder(crashReporter)`, which sends exactly `render` and
   `unhandled-rejection` (the reports of the first moments included: the sink replays them). *Why:*
   Hermes keeps one tracker (last caller wins), and a forwarded `global-handler` report would
   duplicate every uncaught exception.
6. **Breadcrumbs carry route patterns and fixed event names, never content.** Route crumbs come from
   `useSegments()` (`tasks/[id]`), never `usePathname()` or search params; console, touch and UI crumbs
   are dropped; no `Sentry.wrap` or `TouchEventBoundary`. *Why:* paths, console lines and pressed
   labels hold ids, search text and titles.
7. **Release and dist come from the native build; environment is the variant.** No `release` or
   `dist` in the options (`<id>@<version>+<build>` and `<build>` come from native);
   `environment: config.environment`. *Why:* a JavaScript release splits one build into two releases
   and no longer matches the uploaded symbols; without `environment` every preview crash is filed under
   production.
8. **Every bundle reports its debug ID and every reporting build uploads its maps and symbols.** Metro
   uses `getSentryExpoConfig`, as the crash reporting Metro kit in `scripts/metro/metro-kits.ts` (the
   canonical `metro.config.js` composes it; never edited); `app.config.ts` lists `@sentry/react-native/expo` with `organization`
   and `project`; profiles in the contract's `uploadProfiles` never set `SENTRY_DISABLE_AUTO_UPLOAD`,
   `SENTRY_ALLOW_FAILURE` or a debug-upload switch; installs keep optional dependencies (the
   `sentry-cli` binary). *Why:* Expo's default config writes a debug ID into the map only, and a
   build without uploads ships crashes nobody can read.
9. **Every OTA update uploads its source maps.** Each script or workflow that runs `eas update` also
   runs `npx sentry-expo-upload-sourcemaps dist`; each EAS Workflows `type: update` job sets
   `upload_sentry_sourcemaps: true` (or uploads in its `after_update` hook); ota-updates' restart
   path awaits `crashReporter.flush()` before reloading (that skill owns the step). *Why:* an update's bundle was never built natively, so nothing else uploads it.
10. **The upload token is a build secret.** `SENTRY_AUTH_TOKEN` lives in EAS (secret visibility) or CI
    secrets; never in the plugin options, the app config, a committed `.sentryclirc` or
    `sentry.properties`; `.env.sentry-build-plugin` is git-ignored. *Why:* the plugin writes an
    `authToken` option into the native projects, and the token grants write access to the org.
11. **Tracing is off by default, capped and declared.** `TRACES_SAMPLE_RATE` and
    `PROFILES_SAMPLE_RATE` are literals in `src/config/crash-reporting-config.ts`, at most the
    contract's `maxTracesSampleRate`, no `tracesSampler`; a rate above 0 declares `performance-data`.
    *Why:* tracing multiplies volume and is a separate data type in both stores' declarations.
12. **`contracts/crash-reporting.json` states the facts and the store declarations match them**:
    provider, consent model, tracing cap, upload profiles, and `collects` (`crash-data`,
    `other-diagnostic-data`, `performance-data`), never linked to the user or used for tracking; the
    `@sentry/react-native` rows of `contracts/privacy.json` copy them (`privacy-sync`). *Why:*
    privacy-and-store-declarations turns these facts into App Privacy, Data safety and privacy-manifest answers.
13. **The developer owns the Sentry account; prove it on a release build.** Ask for the org, project
    and DSN (never invent them), hand over the `eas env:set` commands and server-side settings, and
    stop and ask before anything that sends data to their project or changes their account. *Why:*
    those are outward-facing actions on someone else's service.

## Workflow

1. **Decide with the developer.** Read [references/privacy-consent-and-scrubbing.md](references/privacy-consent-and-scrubbing.md)
   (sections 6 to 9) and agree the consent model, whether tracing is on, the upload profiles and the
   org/project slugs. Copy `templates/contracts/crash-reporting.json` (+ schema) and fill the facts.
2. **Install:** `npx expo install @sentry/react-native` (never `@latest`); keep optional dependencies;
   rebuild the development client. Details: [references/setup-and-wiring.md](references/setup-and-wiring.md).
3. **Copy the templates** at the paths their first lines name: `templates/src/services/crash-reporter/`
   (port, adapter, scrubber, forwarder, fake and the root kit), `templates/src/config/` (the config,
   its reader and the DSN's type in `crash-reporting-env.d.ts`), `templates/src/hooks/use-crash-reporting-consent.ts`,
   `templates/src/hooks/use-route-breadcrumbs.ts` (each with its test), `templates/scripts/metro/metro-kits.ts`
   and `templates/__mocks__/@sentry/react-native.ts`. The root skeleton's slots come from
   app-startup-and-bootstrap; set them up with it first.
4. **Register the kit** in app-startup-and-bootstrap's registry `src/services/create-root-kits.ts`
   ([examples/create-root-kits.ts](examples/create-root-kits.ts)): create the adapter from
   `readCrashReportingConfig()` and add `createCrashReportingKit({ crashReporter, consent })` to the
   list. The root files stay unchanged: the kit's `forward` reaches the error sink and its effects
   (the choice applied after the splash, route breadcrumbs) mount beside the root Stack.
5. **Give the person the choice** ([examples/settings-schema.ts](examples/settings-schema.ts)): add
   `crashReportsEnabled` the settings-and-preferences way (default from the consent model) with its
   settings row, whose hint says that turning it back on after turning it off applies at the next
   launch, and pass the kit a consent source over that field (the example's `settingsCrashConsent`).
   Until the row exists, pass `fixedCrashConsent(false)`. Read
   [references/error-flow-breadcrumbs-and-tracing.md](references/error-flow-breadcrumbs-and-tracing.md).
6. **Build config** (`templates/scripts/metro/metro-kits.ts`, [examples/app.config.ts](examples/app.config.ts)):
   the Metro kit builds the base config with `getSentryExpoConfig` (the canonical `metro.config.js`
   composes it and keeps `cacheVersion`); the plugin entry with `organization` and `project`;
   `SENTRY_DISABLE_AUTO_UPLOAD=true` only in non-reporting eas.json profiles; append
   `&& npx sentry-expo-upload-sourcemaps dist` to every `eas update` script. Read
   [references/releases-symbols-and-sourcemaps.md](references/releases-symbols-and-sourcemaps.md).
7. **Hand over the human steps** and stop until the developer confirms: the `eas env:set` commands
   (DSN plain text per reporting environment, `SENTRY_AUTH_TOKEN` secret), Sentry's server-side
   scrubbing settings, and the declarations for privacy-and-store-declarations (App Privacy, Data
   safety, `ios.privacyManifests` entries).
8. **Run the tests:** `npx jest src/services/crash-reporter src/hooks src/config scripts/metro --ci --maxWorkers=2`,
   then the app's typecheck and lint.
9. **Run the checker:** `node ${CLAUDE_SKILL_DIR}/scripts/check-crash-reporting.mjs .` (multi-package:
   `--app-dir apps/<app>`). Fix every `FAIL` line ([references/testing-and-checker-rules.md](references/testing-and-checker-rules.md)
   explains each rule) and rerun until `RESULT: PASS`.
10. **Before the first store release:** the device proof on a preview build and a named simulator and
    emulator (testing reference, section 5), with the developer's go-ahead.
11. **Report** the consent model, the files changed, the SKIP lines, the open human steps, and every
    `RESULT` line.

## Definition of done

- [ ] Only the adapter imports `@sentry/react-native`; the registry creates it and registers `createCrashReportingKit`; tests use the fake; the root mock is in `__mocks__/@sentry/`.
- [ ] The SDK starts only from `setConsent(true)`, applied by the kit's effects after the splash; the settings default matches `consentModel`; the development variant never reports.
- [ ] The options are the privacy-first set with the scrubber hooks, `environment`, the rejection-tracker integration, and no `release`, `dist`, `setUser` or `Sentry.wrap`.
- [ ] The kit forwards through `createCrashForwarder`: exactly `render` and `unhandled-rejection`.
- [ ] The Metro kit uses `getSentryExpoConfig`; the plugin entry has `organization` and `project` and no token; upload profiles keep uploads on; every `eas update` uploads its maps.
- [ ] `contracts/crash-reporting.json` is filled; tracing is 0 or within the cap and declared.
- [ ] The developer confirmed the EAS variables, the server-side scrubbing settings and the store declarations, or the report lists them as open.
- [ ] The tests in workflow step 8 pass, with the app's typecheck and lint.
- [ ] Expected SKIP only: `SKIP eas.json [upload-not-disabled] not yet created (eas-build-and-submit creates it)` before eas.json exists.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-crash-reporting.mjs .` prints `RESULT: PASS`

## Anti-patterns

- **Pasting Sentry's setup snippet.** It sets `sendDefaultPii: true`, replay sample rates and
  `Sentry.wrap(RootLayout)`, and calls `Sentry.init` at module scope: data leaves before any choice.
  Copy the adapter template.
- **`Sentry.init` in `index.ts`, `App.tsx`, `_layout.tsx` or the composition root.** It starts the SDK and its connection
  during startup and before consent; the kit's effects apply the choice after the splash.
- **Wiring crash reporting into `app-root.tsx`, `app-stack.tsx` or `metro.config.js`.** The root
  skeleton stays canonical: register the kit in `src/services/create-root-kits.ts` and list the Metro
  kit in `scripts/metro/metro-kits.ts` (check-startup's `root-kits` fails a kit imported by a root file).
- **Turning off Sentry's global handler "to avoid duplicates".** Native SDKs drop React Native's
  fatal-JS crash expecting the JavaScript handler, so fatal errors vanish; turn off only the rejection
  tracker and forward rejections from the sink.
- **Forwarding every net source to `captureException`.** Uncaught exceptions arrive twice.
- **`setUser({ id: account.id })` "for support".** It is synced into native crash reports and changes
  the store declarations; give support the event id instead.
- **Breadcrumbs from `usePathname()`, console logs or `Sentry.wrap` touch tracking.** Ids, search text
  and titles leave the device.
- **Setting `release` to `version` or a git SHA in JavaScript.** Native events and uploads use the
  native name; the JavaScript one splits the build.
- **`SENTRY_DISABLE_AUTO_UPLOAD=true` in a shared base profile** to make development builds pass: the
  production profile inherits it. Put it in the development profile only.
- **`authToken: process.env.SENTRY_AUTH_TOKEN` in the plugin entry.** Prebuild writes the token into
  the native projects; sentry-cli reads the environment by itself.
- **Reporting expected failures** (offline, validation, a handled 404): they bury real crashes and
  spend the quota; they are `Result` values.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/setup-and-wiring.md](references/setup-and-wiring.md) | Install, the files, DSN and variant, composition root, root mock, config plugin, Metro, EAS variables, Expo Go, multi-package | Workflow steps 2 to 4 and 6 |
| [references/privacy-consent-and-scrubbing.md](references/privacy-consent-and-scrubbing.md) | What a report holds, the option set, the scrubber and its limits, no identity, server-side scrubbing, consent models and timing, store declarations, privacy manifest, children's apps | Workflow steps 1, 5 and 7 |
| [references/error-flow-breadcrumbs-and-tracing.md](references/error-flow-breadcrumbs-and-tracing.md) | Who catches what, the rejection tracker and global handler, the sink, defects vs expected failures, breadcrumb rules, tracing, flush before OTA reload | Workflow step 5 |
| [references/releases-symbols-and-sourcemaps.md](references/releases-symbols-and-sourcemaps.md) | Release, dist, environment; debug IDs; EAS and local uploads; OTA uploads; Hermes; proving symbolication; failure modes | Workflow step 6, minified stacks |
| [references/testing-and-checker-rules.md](references/testing-and-checker-rules.md) | What the tests prove, testing reporting code, every checker rule with its fix, SKIP and NOT APPLICABLE, the device proof, pitfalls | Workflow steps 8 to 10 |
| `templates/src/services/crash-reporter/` | Port, Sentry adapter, scrubber, forwarder, fake, and the root kit `crash-reporting-root-kit.tsx` (+ tests) | Workflow steps 3-4 |
| `templates/src/config/` | `crash-reporting-config.ts`: the DSN and variant parser, `readCrashReportingConfig()` and the sample-rate constants (+ test); `crash-reporting-env.d.ts`: the DSN variable's type | Workflow step 3 |
| `templates/scripts/metro/metro-kits.ts` | The Metro kit list with Sentry's `getSentryExpoConfig` (the canonical `metro.config.js` composes it) | Workflow step 6 |
| `templates/src/hooks/` | `use-crash-reporting-consent.ts` (applies the saved choice after the splash) and `use-route-breadcrumbs.ts` (route-pattern breadcrumbs), each with its test | Workflow step 3 |
| `templates/__mocks__/@sentry/react-native.ts` | Root Jest mock of the SDK | Workflow step 3 |
| `templates/contracts/` | `crash-reporting.json` and its schema | Workflow step 1 |
| [examples/create-root-kits.ts](examples/create-root-kits.ts) | The root-kit registry with the crash reporting kit and a consent source over the settings store | Workflow steps 4-5 |
| [examples/settings-schema.ts](examples/settings-schema.ts) | The `crashReportsEnabled` settings field | Workflow step 5 |
| [examples/app.config.ts](examples/app.config.ts) | The config plugin entry | Workflow step 6 |
| `scripts/check-crash-reporting.mjs` | The checker (29 rules; `--help` lists them) | Workflow step 9, definition of done |
| `scripts/lib/` | `crash-scan.mjs` (the checker's source helpers); `source-scan.mjs`, `object-literal.mjs` (shared, synced; do not edit) | With the checker |
| `scripts/check-lib.mjs` | Shared checker library (synced; do not edit) | With the checker |
| `scripts/selftest.mjs` | Proves the checker against the fixtures | After changing the checker |
| `tests/bases/app/` | The fixture base app (package.json, eas.json, .npmrc, .gitignore) | With the self-test |
| `tests/fixtures/` | One good case, a bad case per rule, pass and error cases | With the self-test |
| `assets/shared.json` | Which shared files this skill syncs | When syncing |

## Related skills

- `error-handling-typed-results` - the error net, the crash fallback and `Result` values.
- `architecture-and-boundaries` - ports, adapters, the composition root, the error log.
- `app-startup-and-bootstrap` - the root skeleton's slots and registry the kit plugs into, and the startup order.
- `settings-and-preferences` - adding the `crashReportsEnabled` field and its row.
- `analytics-and-consent` - product analytics and its own consent.
- `privacy-and-store-declarations` - App Privacy, Data safety, the privacy manifest, the network inventory.
- `app-variants-and-environment` - `EXPO_PUBLIC_*` readers and EAS secrets.
- `eas-build-and-submit` - profiles, remote versions and the build environment.
- `ota-updates` - publishing updates and the flush before reload.
- `performance-budgets` - startup and frame budgets measured in test builds.
- `debug-menu-and-test-hooks` - test-only crash triggers for the device proof.
- `unit-and-component-tests` - root mocks and the fake-based test style.
