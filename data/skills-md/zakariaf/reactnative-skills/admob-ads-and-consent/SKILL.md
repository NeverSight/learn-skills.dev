---
name: admob-ads-and-consent
description: Builds AdMob ads behind a port - banners, interstitials, rewarded, UMP consent then ATT, pacing, ADS_MODE test IDs. Use when touching ads, consent, ATT, ad IDs or rewarded perks. Not for purchases (in-app-purchases).
---

# AdMob ads and consent

Makes an Expo app show Google AdMob ads that never interrupt a focused task: Google's consent and
Apple's tracking prompt come first, every "may an ad appear now?" answer comes from pure, tested
functions, testing builds only ever see Google's test ads, iOS and Android each get their own IDs, and
two zero-dependency checkers prove it on the real code.

## Rules that must hold

1. **Ads never interrupt a focused task.** Banners only on the screens contracts/ads.json `bannerSlots`
   declares (browsing screens, never a form, editor, dialog, paywall or onboarding), and only while that
   screen is focused (`useBannerSlot(screen, facts, useIsFocused())`: stacks and tabs keep it mounted
   under pushed screens); interstitials only from the press handler that leaves a natural break the user
   just finished, never on mount, app start or during onboarding; rewarded ads only on the user's tap
   behind a clear "Watch an ad to ..." label; the AdsPort's show, initialize and preload calls only in
   `ad-moments.ts` and `ad-gate.ts`. *Why:* an interruption costs the user's trust, and Google's policies
   punish ads that surprise or invite accidental taps.
2. **Every ad decision comes from `ad-policy.ts` / `rewarded-offer.ts`** (pure; numbers from
   `src/config/ad-pacing.ts`, at or above contracts/ads.json `pacingFloors`, default 3 breaks before the
   first interstitial, then 3 minutes and 2 breaks between two), and every finished natural break is
   saved with `recordBreak` where it finishes. *Why:* only pure rules can be tested one by one, the
   numbers are configuration, and a history that never counts a break allows exactly one interstitial.
3. **Consent, then Apple's prompt, before any ad request, through the consent moment, and none at all
   when ads are off.** UMP refreshes at every launch; where Google's form is required, the app's optional
   primer and then the form; once `canRequestAds`, ATT through `ConsentPort.requestTracking()` (iOS only,
   while not-determined, the app active); then `setRequestConfiguration` + `initialize` + preload. Only
   after onboarding, online, not Premium, over a focused ad screen. `AdsProvider` (through
   `consent-moment-flow.ts`) is the only runner of `prepareAds`; banners are allowed only after the ATT
   answer and a successful `initialize`, and the adapter mounts its native banner only after it. The
   ConsentPort comes from `createConsentPort(adsMode, () => createAdmobConsentAdapter(...))`, so an
   `ADS_MODE=off` build never calls UMP or ATT. *Why:* Google requires consent (EEA, UK, Switzerland, US
   states), Apple's guideline 5.1.2(i) requires the ATT answer before IDFA use, the SDK may preload at
   initialisation, and a UMP update is a network request that would fail the network audit of off builds.
4. **Testing builds never see real ads; real IDs reach the runtime only in production + live builds.**
   `resolveAdsMode` decides: development and preview -> `test` (or `off`), production -> `live` (or
   `off`); the other pairs throw. IDs live only in `src/config/admob-ids.ts`, read only by
   `app.config.ts`; `admobPluginOptions` always gives both platforms an app ID (Google's sample unless
   live); `adsExtra` writes units only in live builds; the template's placeholder IDs are noted and
   never reach a store build. `expo.extra` is embedded at build time, or replaced by the running EAS
   Update's manifest, so `eas update` runs with the channel's environment and the app reads it through
   `readAdsExtraForBinary(Application.applicationId)`, which turns ads off for a manifest made for
   another variant's app id. *Why:* real ads in a testing build risk the AdMob account; a missing app ID
   stops the app at launch.
5. **`react-native-google-mobile-ads` is exactly 17.2.0 and is imported only by `admob-ads-adapter.ts`,
   `admob-consent-adapter.ts` and the test-only `admob-consent-debug-adapter.ts`**, with the classic
   create/load/show API (no v17 hooks or pools), and the adapters are created only inside
   `createAdsPort` / `createConsentPort` in the composition root. *Why:* an upgrade touches three files,
   pacing stays in pure code, and pools preload (on Android initialise) before consent.
6. **The reward is granted only on `EARNED_REWARD`, and the AdsPort reports a `RewardedStatus`
   (`'loading' | 'ready' | 'unavailable'`), never a loaded flag.** `rewardedOffer` gives a perk the user
   waits on `'loading'` and `'hidden'` only when no ad can come, so a flow waiting on it moves on. *Why:*
   with a flag, "not loaded" means both "still loading" and "cannot come", and a waiting user is stranded.
7. **Pause media around every fullscreen ad (`runFullscreenAd` with the one `MediaLifecycle`), resume in
   `finally`, and make every show settle** on `CLOSED`, on `ERROR` (phase `show`) and on a rejected
   `show()`. *Why:* iOS does not background the app for these ads, so nothing else pauses audio or
   timers, and a show that never settles leaves media suspended and the handler stuck.
8. **Ads are silent and their failures are values.** Never an error, spinner or "please connect" for
   ads; failures go to the error log; branch on `error.phase` then `error.reason`, never `error.code`;
   `initialize()` returns a Result; the banner slot has zero height until an ad has loaded. *Why:* an ad
   is never what the user came for, and an escaped rejection is dropped silently in release builds.
9. **The audience is declared and enforced, and tracking follows Apple's rules.** contracts/ads.json
   `audience`: `general` -> the declared `maxAdContentRating` (default PG), no child tags;
   `child-directed` -> G, both child tags, Android's `AD_ID` permission blocked, and no ATT at all (no
   tracking package, plugin, purpose text or adapter; `tracking: null`). General audience:
   `expo-tracking-transparency` is imported only by `expo-tracking-consent-adapter.ts`, handed to the
   consent adapter as `tracking`; its plugin entry gets the source text and every language's catalog has
   it; the AdMob plugin gets no `userTrackingUsageDescription`; the console publishes no IDFA explainer.
   Declined, restricted or unavailable tracking still serves ads, and nothing is gated on the answer.
   *Why:* the rating must match the console, apps for children may not send device data to third
   parties (App Review 1.3, Play Families), a missing purpose text crashes, and 5.1.2(i) forbids gating
   on ATT.
10. **The SKAdNetwork list is Google's full list of `xxxxxxxxxx.skadnetwork` identifiers, generated and
    checked (`--check`) before every release.** *Why:* the plugin copies only what it gets, and Google
    changes the list.
11. **Consent reset, the debug geography and the Ad Inspector exist only in test-only code** (the
    debug adapter and debug options reached through the test-only entry). *Why:* they change consent
    behaviour for real users.
12. **The developer does the AdMob console steps; ask and wait, never invent IDs or publish anything.**
    *Why:* the console is the developer's account, and an invented ID or a published setting reaches real
    users.

## Workflow

1. **Install.** Read [references/setup-ids-and-modes.md](references/setup-ids-and-modes.md):
   `npm install -E react-native-google-mobile-ads@17.2.0` and
   `npx expo install expo-tracking-transparency expo-network expo-constants expo-application` (a
   child-directed app leaves out `expo-tracking-transparency`).
2. **Copy the templates** at the paths their first lines name (never rewrite them from memory):
   `templates/src/services/ads/`, `templates/src/services/consent/admob-consent-debug-adapter.ts` (+ test),
   `templates/src/config/{ads-config,admob-ids,ad-pacing,skadnetwork-ids}.ts` (+ tests),
   `templates/src/hooks/`, `templates/src/ui/ad-banner-slot.tsx` (+ test), `templates/scripts/ads/`,
   `templates/contracts/ads.json` (+ schema; fill the banner screens, audience and floors). The synced
   canonical files (`src/services/consent/*`, `src/services/connectivity/*`, `src/config/app-variant.ts`,
   `src/core/result.ts`, the two root mocks) are copied only when the app lacks them; a child-directed
   app deletes `expo-tracking-consent-adapter.ts` (+ tests) and the tracking mock.
3. **Wire `app.config.ts`** as [examples/app-config-ads.ts](examples/app-config-ads.ts) shows:
   `resolveAdsMode`, the two plugin entries, `extra: { ...adsExtra(adsMode, ADMOB_IDS) }`, the tracking
   text in every language's `locales` (none of the tracking lines for a child-directed app). With EAS the
   next build applies it; locally rerun `npx expo prebuild --clean`. Refresh the native config snapshot
   (expo-prebuild-and-config-plugins' checker with `--write`: `APPLICATION_ID` and
   `DELAY_APP_MEASUREMENT_INIT` change) and commit it with the plugin change. Publish every later
   `eas update` with the channel's environment (`--environment <env>`, `ADS_MODE` unset).
4. **Compose the ports** in the composition root ([examples/create-device-services.ts](examples/create-device-services.ts)):
   add `ads`, `consent`, `connectivity`, `fullscreenAd` to `Services`, `createDeviceServices` and
   `createTestServices` (architecture-and-boundaries' port recipe), with
   `readAdsExtraForBinary(Application.applicationId)` and the consent adapter's `tracking`.
5. **Mount the consent moment.** Read [references/consent-flow.md](references/consent-flow.md); render
   `AdsRoot` ([examples/ads-root.tsx](examples/ads-root.tsx)) inside `RootStack` around `AppStack`, with
   the app's Premium, onboarding and saved consent facts and, optionally, a primer
   ([examples/consent-primer.tsx](examples/consent-primer.tsx)). Show the "Ad privacy choices" entry only
   while required: the settings model returns `adPrivacy`
   ([examples/use-settings-model.ts](examples/use-settings-model.ts)), the row is a pure view
   ([examples/ad-privacy-row.tsx](examples/ad-privacy-row.tsx)).
6. **Place the ads.** Read [references/ad-policy.md](references/ad-policy.md) and
   [references/placements-and-lifecycle.md](references/placements-and-lifecycle.md); follow
   [examples/use-tasks-model.ts](examples/use-tasks-model.ts) and [examples/tasks-screen.tsx](examples/tasks-screen.tsx):
   `useBannerSlot('<screen>', facts, useIsFocused())` in the model hook and `AdBannerSlot` in the view;
   `recordBreak` where a break finishes; `showInterstitialIfDue` in the press handler that leaves it;
   `useRewardedOffer` and `earnRewardedPerk` for rewards; the `fullscreenAd` gate for every fullscreen ad.
7. **Run the tests**: `npx jest src/services/ads src/services/consent src/config src/hooks src/ui scripts/ads --ci --maxWorkers=2`.
8. **Run the checkers**: `node ${CLAUDE_SKILL_DIR}/scripts/check-ads.mjs .` and
   `node ${CLAUDE_SKILL_DIR}/scripts/check-ad-behaviour.mjs .` (multi-package: add `--app apps/<app>`).
   Fix every `FAIL` line (file, rule, fix) and rerun until both print `RESULT: PASS`.
9. **Before a release**: `node scripts/ads/refresh-skadnetwork.ts --check`; the ads smoke test by hand on
   an `ADS_MODE=test` build, on a named iOS simulator and a named Android emulator
   ([references/console-privacy-troubleshooting.md](references/console-privacy-troubleshooting.md),
   `templates/maestro/ads-smoke/`; declare the folder in `contracts/naming.json` `extraE2eFolders` as
   `{ "folder": "ads-smoke", "why": "by-hand ads smoke on ADS_MODE=test builds; CI never runs it" }`,
   so naming-conventions' checkers pass); then hand off the App Privacy and Data safety answers
   (privacy-and-store-declarations).
10. **Tell the developer**, in plain words, which console steps are still open (account, apps and units,
    the GDPR message, blocking controls before the first store build; store links and `app-ads.txt`
    after the first release) and what each needs from them.

## Definition of done

- [ ] The SDK is exactly 17.2.0 and imported only by the three adapter files; `expo-tracking-transparency`
      is installed and imported only by `expo-tracking-consent-adapter.ts` (general audience) or absent
      with `tracking: null` (child-directed); the root mocks exist.
- [ ] Every template is in place and its Jest suite passes; the consent folder equals the canonical copy.
- [ ] The AdMob plugin gets `admobPluginOptions(...)`; `expo.extra` comes from `adsExtra(...)`; no AdMob
      ID is typed in app code and no app code imports `admob-ids.ts`; the app reads it through
      `readAdsExtraForBinary(Application.applicationId)`; the native config snapshot is refreshed.
- [ ] Consent: launch refresh, the primer (if any) then Google's form, then Apple's prompt while
      not-determined (general audience), after onboarding, over a focused ad screen, before the first
      ad; nothing initialised or loaded without `canRequestAds`; banners only after the ATT answer and
      a successful `initialize`; declined, restricted or unavailable tracking still initializes;
      `ADS_MODE=off` never calls UMP or ATT; the privacy entry shows only when required.
- [ ] The purpose text: the plugin entry, every language's catalog, the localised writer; no IDFA
      explainer in the console; the audience profile matches the adapter and the console rating.
- [ ] Every finished break is recorded once; banners only on the declared slots with their testIDs and
      a policy-computed `isAllowed`, only while focused; interstitials only from press handlers through
      `showInterstitialIfDue`; rewards only on `EARNED_REWARD`; media is suspended during fullscreen ads.
- [ ] Offline, Premium, no consent and `ADS_MODE=off` each show no ad and no message.
- [ ] `refresh-skadnetwork.ts --check` passes before a release; the ads smoke flows passed on iOS and
      Android (or the report says they are owed); `contracts/naming.json` declares `ads-smoke`; the
      developer has done the console steps.
- [ ] Expected only: `SKIP src/i18n/catalogs [att-plugin] not yet created (i18n-strings-and-catalogs creates it)`
      before the app has catalogs; the placeholder-IDs line (informational, not a problem) until the
      developer gives the real IDs (never in a release report); a consent-only app's note that the ads
      rules do not apply yet; and `NOT APPLICABLE` in an app without the SDK. A multi-package repo runs
      each app with `--app <dir>`.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-ads.mjs .` prints `RESULT: PASS`
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-ad-behaviour.mjs .` prints `RESULT: PASS`

## Anti-patterns

- **Calling `showInterstitialIfDue` from an effect of the next screen or on app resume** (an
  `AppState` listener), directly or through a helper. The ad covers what the user just opened. Only the
  press handler that leaves the break calls it (check-ads `ad-in-effect`).
- **"Upgrading" the child tags to `ageRestrictedTreatment`.** In react-native-google-mobile-ads 17.2.0 Android drops it silently;
  keep the deprecated tags (references/consent-flow.md, Audience; check-ads `content-rating`).
- **"Upgrading" the adapter to `useInterstitialAd`, `useRewardedAd` or ad pools.** Hooks tie ads to a
  component; pools preload (and on Android initialise the SDK) before consent. Keep the classic API.
- **Initialising the SDK at app start "to be ready"** (`createAdsPort(...).initialize()`). It may preload
  ads before consent; `prepareAds` is the only caller of `initialize` (check-ads `port-calls`).
- **`deps.ads.showInterstitial()` straight from a press handler.** It skips the pacing policy, the media
  pause and the history; call `showInterstitialIfDue` (check-ads `port-calls`).
- **Holding the ad moment while the banner screen is merely mounted.** A pushed editor gets the primer,
  the form and ATT; pass `useIsFocused()` to `useBannerSlot`.
- **`readAdsExtra()` in the composition root, or `eas update` with whatever environment the shell has.**
  An update made for another variant changes the ads of installed builds; use `readAdsExtraForBinary`
  and `--environment`.
- **ATT in a child-directed app.** Kids Category apps do not implement it; no package, no purpose text,
  `tracking: null`.
- **`createAdmobConsentAdapter(...)` or `createAdmobAdsAdapter(...)` outside the factories.** An
  `ADS_MODE=off` build then asks Google UMP at launch and the network audit fails.
- **Typing test unit IDs or the sample publisher ID in code.** Use `units: 'test'` (the adapter maps
  `TestIds.*`) and `GOOGLE_SAMPLE_APP_IDS` in `ads-config.ts`.
- **`npx expo install react-native-google-mobile-ads`.** It writes a caret; use `npm install -E`.
- **One AdMob app for both platforms, or iOS units on Android.** They are separate AdMob apps; the
  factory picks this platform's units.
- **Hiding an ad failure behind a message, a retry button or a spinner.** Ads are silent; log and move on.
- **Granting a reward on `CLOSED`, or a pressable "Watch an ad" with nothing loaded.** Use
  `rewardedOffer`: `'loading'` busy, `'hidden'` gone.
- **Wrapping `AdBannerSlot` in a frame that renders nothing until an ad has loaded.** The native banner
  must be mounted to load; pass the frame as `loadedStyle`.
- **Asking ATT at launch, before Google's form, or from a screen.** Apple's prompt comes through
  `ConsentPort.requestTracking()` inside `prepareAds`, over a focused ad screen only.
- **Hiding a feature, a reward or Premium behind "Allow".** 5.1.2(i) forbids gating on the ATT answer.
- **Publishing an IDFA explainer in the AdMob console or setting the AdMob plugin's
  `userTrackingUsageDescription`.** UMP runs a second ATT flow, and the text gets two writers.
- **Proving ATT with a flow that starts with `launchApp`.** Maestro grants every permission; launch with
  `xcrun simctl launch <udid> <bundle id>`.
- **Changing pacing by editing `ad-policy.ts`, or lowering a number below its floor "for testing".**
  Change `src/config/ad-pacing.ts`; a testing build already serves test ads.
- **Putting `AdsConsent.reset()` or the Ad Inspector in the consent adapter.** They belong to the
  test-only debug adapter.
- **Fixing a failing checker by weakening a Jest test or the fixture.** The behaviour check runs the real
  modules; fix the module.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/setup-ids-and-modes.md](references/setup-ids-and-modes.md) | Versions, install, the variant x ads-mode matrix, IDs, plugin options, test IDs, the ports per mode, SKAdNetwork, multi-package, re-verify | Workflow steps 1-4 |
| [references/consent-flow.md](references/consent-flow.md) | UMP and ATT rules with sources, Android, the audience profiles, the canonical consent folder, the sequence, the consent moment, the privacy entry, test-only tools | Workflow step 5 |
| [references/ad-policy.md](references/ad-policy.md) | The default pacing, the pure policy, floors, the history, rewarded offers, interpretations, tests | Workflow step 6; before changing any ad rule |
| [references/placements-and-lifecycle.md](references/placements-and-lifecycle.md) | AdsPort and adapter facts, the banner slot, natural breaks, rewards, pausing media on iOS and Android, offline, React Navigation | Workflow step 6 |
| [references/console-privacy-troubleshooting.md](references/console-privacy-troubleshooting.md) | The developer's console steps, App Privacy and Data safety facts, the smoke test, root mocks, error and symptom tables | Workflow steps 9-10; when an ad misbehaves |
| [examples/app-config-ads.ts](examples/app-config-ads.ts) | The ads lines of `app.config.ts` | Workflow step 3 |
| [examples/create-device-services.ts](examples/create-device-services.ts) | The composition root with the ads, consent, connectivity and media gate ports | Workflow step 4 |
| [examples/ads-root.tsx](examples/ads-root.tsx) | Mounting `AdsProvider` with the app's facts | Workflow step 5 |
| [examples/consent-primer.tsx](examples/consent-primer.tsx) | An optional consent primer before Google's form | Workflow step 5 |
| [examples/use-tasks-model.ts](examples/use-tasks-model.ts) | A model hook with the banner, a natural break, an interstitial and a rewarded offer | Workflow step 6 |
| [examples/tasks-screen.tsx](examples/tasks-screen.tsx) | The banner slot at the bottom of a pure view | Workflow step 6 |
| [examples/use-settings-model.ts](examples/use-settings-model.ts) | The settings model's `adPrivacy` (reads the consent answer and the port) | Workflow step 5 |
| [examples/ad-privacy-row.tsx](examples/ad-privacy-row.tsx) | The "Ad privacy choices" entry, a pure view | Workflow step 5 |
| `templates/src/services/ads/` | Port, AdMob adapter, fake, factory, read-ads-extra, policy, history, rewarded offer, gate, consent moment flow, moments, fullscreen gate, AdsProvider, its context and hook, with tests | Workflow step 2 |
| `templates/src/services/consent/` | ConsentPort, the AdMob consent adapter (+ iOS and Android tests), the expo-tracking-transparency ATT adapter (+ iOS and Android tests; general audience only), the factory, the fake (+ tests): synced canonical files this skill owns; the test-only debug adapter (+ test) | Workflow step 2 |
| `templates/src/services/connectivity/` | The ConnectivityPort, expo-network adapter, reachability hub, fake (synced; networking-and-server-state owns them) | Workflow step 2 |
| `templates/src/config/` | `ads-config.ts`, `admob-ids.ts`, `ad-pacing.ts` (+ tests), `skadnetwork-ids.ts` (Google's 50 IDs, 2026-10-10); `app-variant.ts` (+ test, synced) | Workflow steps 2-3 |
| `templates/src/hooks/` | `useAdContext`, `useBannerSlot`, `useRewardedOffer` (+ tests) | Workflow step 6 |
| `templates/src/ui/` | `ad-banner-slot.tsx` (collapsed until loaded) and its test | Workflow step 6 |
| `templates/src/core/` | `result.ts` (`Result`, `ok`, `err`, `attemptAsync`) and its test (synced; error-handling-typed-results owns them) | Workflow step 2 |
| `templates/scripts/ads/` | `refresh-skadnetwork.ts` and the tested `skadnetwork-list.ts` | Workflow step 9 |
| `templates/contracts/` | `ads.json` (the app's ads contract) and `ads.schema.json` (every key documented) | Workflow step 2 |
| `templates/maestro/ads-smoke/` | Six Maestro flows of the by-hand smoke test (they land in `.maestro/ads-smoke/`) | Workflow step 9 |
| `templates/__mocks__/` | The SDK and tracking root mocks (synced; do not edit here) | Workflow step 2 |
| `assets/admob-facts.json` | Version, adapter allowlists, banned names, ID formats, SKAdNetwork facts, default floors, required files | Read by the checkers; update on an SDK upgrade |
| `scripts/check-ads.mjs` | Static checks: files, pin, imports, SDK API, factories, test-only tools, IDs, ATT order/plugin/text/wiring per audience, plugin and extra wiring, the binary guard, SKAdNetwork, audience, pacing, placements, effects, port calls, breaks, the consent moment and focus, the smoke folder, free allowances | Workflow step 8 |
| `scripts/check-ad-behaviour.mjs` | Runs the app's modules against the decision tables and the adapters and factories against scripted stand-ins | Workflow step 8 |
| `scripts/lib/ads-facts.mjs` | The facts, the layout paths, the contract reader and the scanned sources | Only to change a checker |
| `scripts/lib/consent-rules.mjs` | check-ads' consent, ATT and SDK-boundary rules | Only to change a checker |
| `scripts/lib/ads-rules.mjs` | check-ads' ads-module, wiring and placement rules | Only to change a checker |
| `scripts/lib/consent-scenarios.mjs` | check-ad-behaviour's consent adapter, tracking and factory scenarios | Only to change a checker |
| `scripts/lib/ads-scenarios.mjs` | check-ad-behaviour's policy, offer, gate, flow, moments, config, adapter, factory and extra scenarios | Only to change a checker |
| `scripts/lib/load-ts.mjs` | Loads the app's TypeScript (type stripping, tsconfig aliases) with the stand-ins | Only to change a checker |
| `scripts/lib/repo-scan.mjs` | File lists (check-lib's repo walk) and import and call helpers | Only to change a checker |
| `scripts/lib/stubs/` | Scripted stand-ins of `react-native-google-mobile-ads` 17.2.0, `expo-tracking-transparency`, `react-native`, `react` and `expo-constants` (update on an SDK upgrade) | Only to change a checker |
| `scripts/lib/app-modules.mjs` | Imports the app's pure TypeScript (synced; do not edit here) | Never by hand |
| `scripts/check-lib.mjs` | Shared script helper (synced; do not edit here) | Never by hand |
| `scripts/selftest.mjs` | Proves both checkers: the shipped templates and examples pass, every planted bug fails for its rule | After changing a checker, a template or a fixture |
| `assets/shared.json` | The shared files copied into this skill | When adding a shared file |
| `tests/` | The base app (with silent planted findings under `.agents/skills/`, `skills/` and a vendored folder) and the overlay cases per checker | When adding a rule |

## Related skills

- `in-app-purchases` - the Premium entitlement that removes every ad.
- `privacy-and-store-declarations` - privacy manifests, App Privacy and Data safety answers, the network audit.
- `architecture-and-boundaries` - ports, adapters, the composition root and SDK classification.
- `networking-and-server-state` - the ConnectivityPort the ads read.
- `debug-menu-and-test-hooks` - the test-only gate, the debug link and simulated offline.
- `settings-and-preferences` - the look of the "Ad privacy choices" row.
- `i18n-strings-and-catalogs` - the tracking purpose text in every language.
- `persistence-and-migrations` - where the ad history and the consent answer are saved.
- `app-variants-and-environment` - the variants `resolveAdsMode` builds on.
- `audio-and-haptics-feedback` - audio that follows the fullscreen gate.
- `navigation-and-routing`, `app-startup-and-bootstrap` - where `AdsProvider` sits in the root tree.
- `e2e-maestro`, `ios-simulator-build` - running the smoke flows on named devices.
- `ios-release-testflight`, `android-release-play` - the release gates that refuse the placeholder or
  sample AdMob app ID in a store build.
- `expo-prebuild-and-config-plugins` - the native config snapshot the plugin change refreshes.
- `ota-updates` - publishing EAS Updates with the channel's environment.
- `naming-conventions` - the `extraE2eFolders` entry of the smoke flows.
- `dependency-management` - pinning and upgrading the SDK.
- `analytics-and-consent` - analytics has its own consent; it shares only the ATT half (`TrackingConsent`).
