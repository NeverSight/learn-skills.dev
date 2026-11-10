---
name: analytics-and-consent
description: "Gates analytics on opt-in consent: no SDK before a yes, typed events without personal data, ATT. Use when adding analytics, events, screen views or a usage-data toggle. Not for crashes (crash-reporting-and-observability)."
---

# Analytics and consent

Makes product analytics in an Expo app something a reviewer can trust: nothing leaves the device
until the user said yes, the vendor SDK exists only after that yes, every event comes from a typed
catalog that cannot carry personal data, analytics never tracks unless the app deliberately opts into
Apple's ATT, and the App Store and Google Play answers are generated from the same contract the code
is checked against. Two zero-dependency checkers prove it on the real code.

## Rules that must hold

1. **Opt-in before any analytics SDK exists.** The consent state starts `'unknown'`; `createAnalytics`
   drops every event until `setConsent('granted')` answers the current question, and calls `createSdk`
   (the vendor adapter) only then, in a build whose mode is not `off`. *Why:* Apple 5.1.1(ii) requires
   consent for usage data even when anonymous, ePrivacy requires it for an install id, and some SDKs
   contact their servers when constructed, opted out or not (PostHog 4.79.1 loads remote config).
2. **Withdrawing is as easy as giving, and stops and forgets.** A settings row calls `setConsent` at any
   time; a no runs `reset()` (anonymous and device ids and the unsent queue dropped) then `optOut()`, in
   that order, or `clearSdkStorage` when no SDK runs in the session, and `forget()` also clears the
   saved answer (account deletion). *Why:* 5.1.1(ii) and the
   GDPR require an easy withdrawal; PostHog's `reset()` clears a saved opt-out (the reverse order opts
   the user back in) and by default keeps the device id and the queue, which a flush still sends; an
   earlier session's ids stay on the device until something deletes them.
3. **A changed question asks again.** Raise `ANALYTICS_CONSENT_VERSION` whenever `collects`, `sdk` or
   `endpoints` in `contracts/analytics.json` change; an older answer reads as `'unknown'`. The contract's
   `consent: { version, covers }` records the fingerprint of what that version covers (`consent-covers`).
   *Why:* consent covers the purposes the user was shown, not the ones added later.
4. **Ads consent is not analytics consent, and analytics does not track by default.** Never derive the
   analytics answer from UMP's `canRequestAds`; the default contract says `tracking: false`, the adapter
   reads no advertising id, and `createAnalytics` gets no `tracking` option. The tracking profile passes
   the canonical `createExpoTrackingConsentAdapter` (never a second ATT import) and the adapter learns
   `isTrackingAllowed` only from an `'authorized'` answer. *Why:* UMP asks for Google's ad vendors, not
   the app's analytics vendor; tracking without ATT breaks 5.1.2(i).
5. **One vendor, one importer, created lazily in the root-kit registry.** `contracts/analytics.json`
   `sdk` is the only analytics package installed; only `src/services/analytics/<vendor>-analytics-adapter.ts`
   imports it; the adapter is created only inside `createAnalytics({ createSdk })` in
   `src/services/create-root-kits.ts` (app-startup-and-bootstrap's registry, part of the composition
   root), which registers `createAnalyticsKit`: features reach the port through `useAnalytics()`, never
   through an edited root file; the client is constructed inside the adapter's factory,
   never at module level; tests use the fakes. Auto-start SDKs (expo-insights; expo-observe unless the
   app writes `dispatchingEnabled: false`) and session replay are not allowed. *Why:* one seam to audit and upgrade, and a structural guarantee
   that nothing runs before consent.
6. **The SDK's privacy options are written out.** PostHog: `defaultOptIn: false`, `personProfiles:
   'never'` (anonymous), `disableGeoip: true` or a declared coarse location, no lifecycle events, no
   autocapture, no session replay, no `PostHogProvider`, error autocapture off, an explicit `host`,
   `disableRemoteFeatureFlags: true`, and a reset that is `reset([])` plus clearing the queue.
   *Why:* every default above either collects more than the catalog or survives a withdrawal.
7. **Every event is in the typed catalog, with a purpose, sent by a literal name.** `ANALYTICS_EVENTS`
   is plain data; names are snake_case, at most 40 characters, never vendor-reserved; `track()` is called
   from a model hook's handler as `track({ name: '<event>', props })`. *Why:* tsc and a text search then
   show every event and where it is sent; an event without a decision behind it is collection without a
   purpose.
8. **Events carry no personal data.** Properties are `enum`, `boolean`, bucketed `count` or `route`,
   never free text; names that mean ids, text, contact or location fail; `sanitizeEvent` drops anything
   that does not match at run time. *Why:* free strings are where titles, search terms and emails leak,
   usually by accident.
9. **Screens are route patterns.** `useScreenViews` sends `screenNameFromSegments(useSegments())`
   (`tasks/[id]`); nothing sends `usePathname()`, search params or URLs. *Why:* a concrete path holds
   record ids and whatever a deep link carried.
10. **Anonymous by default.** No identify, alias or person properties unless the contract says
    `identifies: true`, and then a linked `user-id` is declared. *Why:* the declarations and the consent
    text must match what is sent.
11. **Builds decide the project.** Development and preview are `off` (or `test`), production is `live`
    (or `off`); key and host come from the build's environment through `analyticsExtra()` into
    `expo.extra`, read back with `readAnalyticsExtra(extra, applicationId)`; never a key in code, never
    `EXPO_PUBLIC_ANALYTICS_*`. *Why:* testing builds must not pollute production data, E2E and audit
    builds must send nothing, and an EAS Update made for another variant must not redirect events.
12. **Store declarations come from the contract.** `collects` covers what the catalog, the SDK and the
    identity setting imply; `app.config.ts` writes `privacyManifests: { ...PRIVACY_MANIFESTS,
    NSPrivacyCollectedDataTypes: [...analyticsCollectedDataTypes(projectRoot)] }`; `contracts/privacy.json`
    `sdks["<sdk>"].collects` holds the same rows; the developer enters them in App Store Connect and
    Play's Data safety form. *Why:* a JavaScript SDK ships no privacy manifest, replacing the manifest
    drops its required-reason APIs (ITMS-91053), and answers that differ from the code get apps rejected.
13. **Apps for children ship no third-party analytics.** `audience: 'child-directed'` means `sdk:
    'none'`, no tracking, no identify; stop and ask before any analytics there. *Why:* App Review 1.3
    and 5.1.4 and Play Families forbid device information to third parties.
14. **Analytics is silent and never breaks a feature.** No port method throws or rejects; failures go
    to the error log; at most 100 events wait while the SDK starts. *Why:* analytics is never what the
    user came for, and an escaped rejection is lost in release builds.

## Workflow

1. **Decide with the developer** (stop and ask; never invent): the vendor (default PostHog), the region
   (`endpoints`), the audience, whether the app identifies users, and whether any SDK tracks. Read
   [references/vendors-and-sdk-facts.md](references/vendors-and-sdk-facts.md) and
   [references/att-and-tracking.md](references/att-and-tracking.md). The vendor project, its data
   retention and its data processing agreement are the developer's to set up.
2. **Install**: `npm install -E posthog-react-native@4.79.1` (outside the Expo map, pinned exactly) and
   `npx expo install expo-application` (`readAnalyticsExtra` compares the binary's application id);
   classify it in `contracts/architecture.json` (`"vendorSdks": { "posthog-react-native": "AnalyticsPort" }`,
   plus `vendor('posthog-react-native', 'AnalyticsPort')` in the ESLint config) and in the dependency policy.
3. **Copy the templates** at the paths their first lines name: `templates/src/services/analytics/`,
   `templates/src/config/analytics-config.ts` (+ test), `templates/src/hooks/use-screen-views.ts` (+ test),
   `templates/scripts/analytics/` (+ test), `templates/contracts/analytics.json` (+ schema; fill it). The
   synced canonical files (`src/services/consent/*`, `src/config/app-variant.ts`, `src/core/result.ts`, the
   tracking mock) are copied only when the app lacks them.
4. **Write the catalog** from the app's real questions: read
   [references/event-catalog.md](references/event-catalog.md); one event per decision, closed property kinds.
5. **Write the vendor adapter** after [examples/posthog-analytics-adapter.ts](examples/posthog-analytics-adapter.ts)
   and its test (mock the package; the only test that imports it).
6. **Register the kit** in app-startup-and-bootstrap's registry `src/services/create-root-kits.ts`
   ([examples/create-root-kits.ts](examples/create-root-kits.ts)): `createAnalytics` with the adapter call
   inside `createSdk`, then `createAnalyticsKit({ analytics, errorLog: data.errorLog })` in the list. The
   kit provides the port (`useAnalytics()`), sends screen views beside the root Stack and flushes on the
   way to the background; the root files stay unchanged. Wire `app.config.ts` ([examples/app-config-analytics.ts](examples/app-config-analytics.ts))
   and the EAS environments ([references/modes-keys-and-testing.md](references/modes-keys-and-testing.md)).
7. **Ask and let the user change the answer**: read [references/consent-gate.md](references/consent-gate.md);
   the prompt after onboarding and the settings row ([examples/use-usage-data-model.ts](examples/use-usage-data-model.ts),
   [examples/usage-data-prompt.tsx](examples/usage-data-prompt.tsx)), its keys merged into every catalog
   (`templates/src/i18n/catalogs/`); `forget()` from account deletion.
8. **Send events** from model handlers through `useAnalytics()` ([examples/use-tasks-model.ts](examples/use-tasks-model.ts));
   screen views and the background flush come with the kit (`analytics-root-kit.tsx`).
9. **Declare**: read [references/store-declarations.md](references/store-declarations.md); fill `collects`
   (the one source), copy it into `contracts/privacy.json` `sdks["<sdk>"].collects` when that contract
   exists, give the developer the App Privacy and Data safety rows; hand the manifest and network audit
   to privacy-and-store-declarations.
10. **Run the tests**: `npx jest src/services/analytics src/config/analytics-config.test.ts src/hooks/use-screen-views.test.tsx scripts/analytics --ci --maxWorkers=2`.
    An app with the port and catalog but no vendor yet sets `sdk: "none"` (every build off, nothing
    collected): check-analytics then notes that `manifest-wiring` and `consent-ui` wait for the vendor.
11. **Run the checkers**: `node ${CLAUDE_SKILL_DIR}/scripts/check-analytics.mjs .` and
    `node ${CLAUDE_SKILL_DIR}/scripts/check-analytics-behaviour.mjs .`; fix every `FAIL` line and rerun until
    both print `RESULT: PASS`.
12. **Tell the developer** what is theirs (vendor-console and store steps the agent cannot do): the
    vendor project and region, its "Discard client IP data" setting turned on (`disableGeoip` does not
    stop the server storing the IP; otherwise declare and justify keeping it), retention, the agreement,
    the store forms, the privacy policy text, and the device walkthrough (references/modes-keys-and-testing.md).

## Definition of done

- [ ] One analytics SDK, declared in `contracts/analytics.json`, pinned, imported only by its adapter,
      created only inside `createSdk` in the root-kit registry, which registers `createAnalyticsKit`;
      no auto-start or replay SDK; tests use the fakes.
- [ ] Nothing is sent and no SDK exists before a yes; a no resets then opts out (or `clearSdkStorage`
      deletes the stored SDK state when no SDK runs); `forget()` is wired to
      account deletion; the settings row changes the answer; `ANALYTICS_CONSENT_VERSION` equals
      `consent.version` and `consent.covers` is the fingerprint of the current `sdk`, `endpoints` and
      `collects` (check-analytics `consent-covers`).
- [ ] Every event is in `ANALYTICS_EVENTS` with a purpose and closed property kinds; screen views are
      route patterns; no identify unless declared.
- [ ] Default profile: no ATT from analytics, no advertising id, nothing declared as tracking (or the
      tracking profile done as references/att-and-tracking.md says); child-directed apps have no vendor.
- [ ] `ANALYTICS_MODE` per variant set in the EAS environments; no key in code; off builds for E2E,
      screenshots and the network audit.
- [ ] `collects` drives the privacy manifest; the developer has the App Privacy and Data safety rows; the
      device walkthrough is done or reported as owed.
- [ ] The Jest suites of step 10 pass.
- [ ] Expected only: `SKIP app.config.ts [manifest-wiring] not yet created (expo-project-bootstrap creates it)`
      before the app has a config, `SKIP contracts/privacy.json [privacy-sync] not yet created
      (privacy-and-store-declarations creates it)` before the privacy contract exists, and
      `NOT APPLICABLE` in an app with no analytics folder, contract or SDK.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-analytics.mjs .` prints `RESULT: PASS`
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-analytics-behaviour.mjs .` prints `RESULT: PASS`

## Anti-patterns

- **Constructing the SDK at startup "opted out until consent".** Some SDKs still call home on
  construction; create it inside `createSdk` (check-analytics `sdk-lazy`).
- **`optOut()` then `reset()`.** PostHog's reset clears the saved opt-out; reset first, then opt out.
- **Treating UMP's `canRequestAds` as analytics consent**, or putting analytics in Google's form
  (check-analytics `consent-source`).
- **`setConsent('granted')` in an effect, a render, a service or at startup.** Only the user's tap
  answers (`consent-source`).
- **Constructing the SDK only to reset it after a no.** Pass `clearSdkStorage` (`sdk-clear`).
- **`const client = new PostHog(...)` at the top of the adapter**, as vendor guides show: importing
  the module builds the client at launch (check-analytics `sdk-lazy`).
- **`privacyManifests: { NSPrivacyCollectedDataTypes: [...] }` without `...PRIVACY_MANIFESTS`.** It
  drops the required-reason APIs and the upload is rejected (`manifest-wiring`).
- **A pre-checked box, a bigger "Share" button, or a feature unlocked by sharing.** Two equal choices;
  nothing depends on the answer (5.1.1(ii)).
- **`track({ name, props: { title: task.title } })` or any free-text property.** Use enums, booleans and
  bucketed counts (`event-pii`, `event-props`).
- **Screen tracking with `usePathname()` and params**, as generic guides show. Send route patterns.
- **`identify(user.email)`.** Anonymous by default; an account id only with `identifies: true` and a
  linked `user-id` declaration.
- **`PostHogProvider` with autocapture, session replay, or the SDK's automatic screen capture.** They
  collect what the catalog does not allow.
- **Listing the analytics host in `NSPrivacyTrackingDomains`.** iOS then blocks it for everyone who
  declined ATT; that list is for tracking hosts only.
- **`EXPO_PUBLIC_ANALYTICS_KEY` or a key typed in `src/`.** Use the build environment and `expo.extra`.
- **A second `expo-tracking-transparency` import for analytics.** Use the canonical tracking adapter.
- **Asking for consent at first launch, over a task, or more than once per question version.**
- **Fixing a failing checker by loosening the catalog or the fixture.** Fix the event or the module.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/consent-gate.md](references/consent-gate.md) | Opt-in default and its sources, ads vs analytics consent, the record and version, the gate's life cycle, lazy creation, withdrawal order, forget, when to ask, modes, failures, tests | Workflow step 7; before changing the gate |
| [references/event-catalog.md](references/event-catalog.md) | Catalog shape, property kinds, names and limits, personal data, screen views with Expo Router, where to track, changing events, tests | Workflow steps 4 and 8 |
| [references/att-and-tracking.md](references/att-and-tracking.md) | Apple's tracking definition, the default and tracking profiles, the canonical ATT adapter, Android's advertising ID, manifest tracking keys, apps for children | Workflow step 1; before any attribution SDK |
| [references/store-declarations.md](references/store-declarations.md) | App Privacy answers, the manifest of a JavaScript SDK, Data safety, the mapping table, what the checker requires, when answers change, the privacy policy | Workflow step 9 |
| [references/vendors-and-sdk-facts.md](references/vendors-and-sdk-facts.md) | Why PostHog, install, every option with its default, source-verified pitfalls, repo wiring, other vendors, re-verify commands | Workflow steps 1, 2 and 5; on an SDK upgrade |
| [references/modes-keys-and-testing.md](references/modes-keys-and-testing.md) | Keys and hosts, modes per variant and EAS environments, the binary guard, off builds, the device walkthrough, test recipes, troubleshooting | Workflow steps 6 and 12; when events do not arrive |
| `templates/src/services/analytics/` | Port and SDK seam, consent-store port, event catalog, sanitizer, consent record, the gate (`createAnalytics`), kv-store consent adapter, fakes, screen names, the root kit (`analytics-root-kit.tsx`: provider, screen views, flusher) and `analytics-context.tsx` (`useAnalytics`), each with its test | Workflow steps 3 and 6 |
| `templates/src/config/` | `analytics-config.ts` (+ test): modes per variant, `analyticsExtra`, `readAnalyticsExtra`; `app-variant.ts` (+ test), synced (app-variants-and-environment owns it) | Workflow steps 3 and 6 |
| `templates/src/hooks/` | `use-screen-views.ts` (+ test): screen views by route pattern | Workflow step 8 |
| `templates/scripts/analytics/` | `analytics-manifest.ts` (+ test): `collects` to privacy-manifest entries and Data safety rows | Workflow steps 6 and 9 |
| `templates/src/i18n/catalogs/` | `en.json`, `ar.json`: the prompt's and the settings row's keys (merge into every catalog of the app) | Workflow step 7 |
| `templates/contracts/` | `analytics.json` (the app's analytics contract) and `analytics.schema.json` (every key documented) | Workflow step 3 |
| `templates/src/services/consent/` | The canonical ConsentPort, tracking adapter (+ iOS and Android tests) and fake (+ test), synced; admob-ads-and-consent owns them | Workflow step 3 (tracking profile) |
| `templates/src/core/` | `result.ts` (+ test), synced (error-handling-typed-results owns it) | Workflow step 3, only when missing |
| `templates/__mocks__/` | The `expo-tracking-transparency` root mock, synced (do not edit here) | Workflow step 3, tracking profile |
| [examples/posthog-analytics-adapter.ts](examples/posthog-analytics-adapter.ts) | The PostHog vendor adapter with every privacy option | Workflow step 5 |
| [examples/create-root-kits.ts](examples/create-root-kits.ts) | The analytics lines of the root-kit registry: the gate with the vendor inside `createSdk`, and the kit | Workflow step 6 |
| [examples/app-config-analytics.ts](examples/app-config-analytics.ts) | The analytics lines of `app.config.ts` | Workflow step 6 |
| [examples/use-usage-data-model.ts](examples/use-usage-data-model.ts) | The prompt and settings-row model | Workflow step 7 |
| [examples/usage-data-prompt.tsx](examples/usage-data-prompt.tsx) | The opt-in prompt, a pure view | Workflow step 7 |
| [examples/use-tasks-model.ts](examples/use-tasks-model.ts) | Tracking from a model handler | Workflow step 8 |
| `scripts/check-analytics.mjs` | Static checks: contract, files, inventory, imports, lazy creation, the root kit, stored-state clear, options, catalog, track calls, screens, identity, tracking, audience, declarations, wiring, privacy-contract sync, keys, test isolation, consent UI and its source | Workflow step 11 |
| `scripts/check-analytics-behaviour.mjs` | Runs the app's gate, consent codec, sanitizer, screen names, config and declaration mapping against stand-ins | Workflow step 11 |
| `scripts/lib/` | `analytics-repo.mjs` (facts, layout, contract, sources), `analytics-rules.mjs` (check-analytics' rules), `analytics-scenarios.mjs` (the behaviour scenarios); `app-modules.mjs`, `source-scan.mjs`, `ts-literal.mjs` synced (do not edit here) | Only to change a checker |
| `scripts/check-lib.mjs` | Shared script helper (synced; do not edit here) | Never by hand |
| `scripts/selftest.mjs` | Proves both checkers: templates and examples pass, every planted bug fails for its rule | After changing a checker, template or fixture |
| `assets/analytics-facts.json` | SDK facts (options, auto-start, kinds), advertising-id names, key patterns, catalog limits and personal-data words, Apple identifiers | Read by the checkers; update on an SDK upgrade |
| `assets/shared.json` | The shared files copied into this skill | When adding a shared file |
| `tests/` | The base app (a trimmed privacy contract and privacy-manifest module, silent planted findings under `.agents/skills/`, `skills/` and a vendored folder) and the overlay cases per checker | When adding a rule |

## Related skills

- `admob-ads-and-consent` - Google's consent form and the ATT prompt for ads; owns the ConsentPort.
- `privacy-and-store-declarations` - the whole privacy manifest, SDK inventory, network audit and release audit.
- `crash-reporting-and-observability` - crash and performance data, its own port and consent decision.
- `architecture-and-boundaries` - ports, adapters, the composition root, SDK classification.
- `app-variants-and-environment` - variants and environment variables the modes build on.
- `settings-and-preferences` - the look of the usage-data row.
- `auth-and-secure-storage` - account deletion, which calls `forget()`.
- `app-startup-and-bootstrap` - the root-kit registry and slots the kit plugs into (provider, effects, flushers).
- `dependency-management` - pinning the vendor SDK.
- `ota-updates` - publishing updates with the channel's environment.
- `e2e-maestro` - flows on `ANALYTICS_MODE=off` builds.
- `i18n-strings-and-catalogs` - the prompt's text in every language.
