---
name: privacy-and-store-declarations
description: Proves an app's privacy - network via the API port or offline-only, SDK inventory, privacy manifest, App Privacy and Data safety answers. Use when an SDK lands, a release nears or an audit fails. Not for installs (dependency-management).
---

# Privacy and store declarations

Makes the app's privacy story true and provable: its own code reaches the network only through the
declared seam (or not at all), every SDK that goes online is declared with what it collects, the iOS
privacy manifest covers every pod, the App Privacy and Data safety answers come from one checked
contract, the release binaries match it, and no key or keystore sits in the repo. Four zero-dependency
audits prove it on the source, the shipped JavaScript, the prebuilt pods and the built app.

## Rules that must hold

1. **First-party network code lives only in the declared seam.** Profile `api-port` (default):
   `fetch`, `XMLHttpRequest`, `WebSocket`, `EventSource`, `sendBeacon`, expo-file-system transfers
   and request-client imports (`expo/fetch`, axios, …) only in `src/api/**` and the `networkModules`
   of `contracts/privacy.json`; remote URL literals only in `src/config` and `linkFiles` (never
   `src/api`: endpoints are paths on the configured base URL). Profile `offline-only`: no
   first-party request at all, URLs only in `linkFiles`. Aliased and bracket forms count. *Why:* one
   seam owns deadlines, validation and the privacy inventory, and remote images and fonts request
   without `fetch`. (`network-call`, `network-global`, `remote-url`; in the bundle
   `first-party-network`)
2. **Every network-capable SDK is declared.** Each installed SDK that goes online by itself (ads,
   purchases, crash reporting, analytics, attribution, push, OTA, web views, sign-in, NetInfo, HTTP
   clients) has an entry in `contracts/privacy.json` `sdks` with why, its trunk pods, its Gradle
   groups, whether it tracks and what it collects; no entry outlives its package. *Why:* the store
   answers cover SDK collection too, and an undeclared SDK is an undeclared data flow.
   (`network-sdk`, `sdk-inventory`, `contract`)
3. **Native SDKs are only the declared ones.** Every CocoaPods trunk pod belongs to a declared SDK;
   no pod comes from `:git`, `:http` or outside the repo; tracking, analytics or crash Gradle groups in
   the release classpath belong to a declared SDK. *Why:* binaries bypass every source layer.
   (`vendor-pod`, `banned-pod`, `pod-source`, `vendor-maven`)
4. **Every shipped third-party network capability is declared or reasoned.** A package the app uses
   to go online is a declared SDK (rule 2), which covers its findings; any other capability has a
   baseline entry saying why the app cannot reach it. First-party code is never baselined. The
   baseline and the contract are gated paths in `quality-gates.json`, so a change carries a
   `Gate-Change:` trailer and the reviewer's approval; STALE entries are notes. *Why:* Metro does not
   tree-shake, so unused SDK clients ship. (`baseline-new`, `baseline-reason`, `baseline`,
   `gated-paths`)
5. **The iOS privacy manifest declares every reason any pod declares, and no tracking.**
   `src/config/privacy-manifest.ts` is wired through `ios.privacyManifests`, keeps
   `NSPrivacyTracking: false` and no `NSPrivacyTrackingDomains`; only pods of SDKs declared
   `"tracking": true` may declare tracking; the prebuilt and shipped manifests are current. *Why:*
   Apple does not reliably read static pods' manifests (ITMS-91053), and listed domains are blocked for
   everyone who declines ATT. (`privacy-manifest`, `required-reason`, `missing-reason`, `app-tracking`,
   `tracking-outside-declared`, `prebuilt-stale`, `unreadable-manifest`, `built-manifest`,
   `privacy-manifest-file`)
6. **The store answers come from the contract and match the SDKs.** Every data type a pod's manifest
   collects is in its SDK's `collects` with the same linked and tracking answers and every purpose
   the pod names; the app's own code never tracks; offline-only apps collect nothing themselves; a
   purchase server adds purchase history; push adds the push token (device-id); an app with accounts
   (or a sign-in SDK or account data in the contract) declares its account data and both deletion
   paths. *Why:* both forms are legal declarations, and Apple compares them with the SDKs'
   manifests. (`undeclared-collection`, `store-answer`)
7. **Every permission has a store answer.** Each kind in `contracts/permissions.json` and each purpose
   string or runtime permission in the built binaries (library-merged ones included) is answered in
   `permissionAnswers`, or removed with `android.blockedPermissions`; a merged `AD_ID` needs a
   tracking SDK or a device-id row for advertising or analytics, and Play Console's Advertising ID
   answer. *Why:* libraries and the prebuild template merge permissions nobody asked for.
   (`permission-answer`, `android-ad-id`)
8. **The release binaries carry no surprise.** No `NSAllowsArbitraryLoads` or cleartext exception, no
   dev launcher local-network keys in production, the tracking text in every language exactly when
   tracking is declared, no placeholder values in production. *Why:* the binary is what users get.
   (`ats`, `android-cleartext`, `local-network`, `att-string`, `ship-placeholder`)
9. **The offline-only profile is enforced at install and config time too.** The dependency policy
   lists `offline-only`, `updates.enabled` is false, no OTA plugin, no ATS or cleartext switch.
   *Why:* a banned package is easier to stop than to find. (`profile-policy`, `config-updates`,
   `config-ats`)
10. **Test builds prove it at runtime.** `contracts/e2e.json` `network.mode` is the profile's policy
    (`offline-only` for offline-only; `allowlist` with the API host, or `offline-only`, for api-port),
    so e2e-maestro's socket sampler on each named simulator and emulator fails any other peer; the JS
    network guard (test-only code, never imported elsewhere) blocks and counts every request outside
    the same hosts. *Why:* the runtime layer catches what static layers miss.
    (`runtime-proof`, `network-guard-import`)
11. **No key, keystore or credential anywhere in the repo.** `.gitignore` covers them, no such file
    sits in the tree (installed skills included), no PEM armour in any file, agent deny rules cover
    them. Never open, print, copy or log a key or a token made from it. *Why:* a leaked key publishes
    apps. (`gitignore-secrets`, `secret-file`, `private-key`, `deny-rules`)
12. **Fix findings, never the audit.** Never loosen a baseline, the contract, a lint rule or a checker
    to get green; stop and ask the reviewer for any baseline or profile change, and the developer
    before entering store answers.

## Workflow

1. Read [references/network-layers.md](references/network-layers.md) for the profiles and what each
   layer catches. Decide the profile with the developer (it is a product decision).
2. Copy the templates (each names its repo path on line 1, JSON files sit at their path): `contracts/`
   (`privacy.json`, `privacy.schema.json`, `network-baseline.json`), `src/config/privacy-manifest.ts`
   (+ test), `src/services/test-hooks/network-guard.ts` (+ test) and `scripts/audit/*.ts` (+ tests).
   Set `ios: { privacyManifests: PRIVACY_MANIFESTS }` in `app.config.ts` and add
   `"audit:network": "node scripts/audit/audit-network.ts"` and
   `"audit:privacy": "node scripts/audit/audit-privacy.ts"` to `package.json`. Run their Jest tests.
   Add `contracts/network-baseline.json` and `contracts/privacy.json` to `quality-gates.json`
   `gatedPaths` (quality-gates owns the file), so the commit-msg gate asks for the trailer.
3. Fill `contracts/privacy.json`: the profile, every SDK
   ([references/sdk-inventory.md](references/sdk-inventory.md)), the app's own collection, the
   permission answers and account deletion
   ([references/store-declarations.md](references/store-declarations.md); shape:
   `examples/contracts/privacy.json`). Offline-only: also add `offline-only` to
   `contracts/dependency-policy.json` `profiles` (dependency-management).
4. Run `node ${CLAUDE_SKILL_DIR}/scripts/audit-repo.mjs .` before every push and after any dependency,
   config or native change; fix each `FAIL` (file, rule, fix) and rerun until `RESULT: PASS`. With an
   Android build at hand add `--gradle-deps <report>`.
5. After a native install or an SDK upgrade: `npx expo prebuild --platform ios --clean`, then
   `node ${CLAUDE_SKILL_DIR}/scripts/audit-privacy-manifest.mjs .`; add missing reasons to
   `privacy-manifest.ts` and collected data to the contract, prebuild again
   ([references/privacy-manifest.md](references/privacy-manifest.md)).
6. `npm run export:audit`, then `node ${CLAUDE_SKILL_DIR}/scripts/audit-bundle.mjs .` (or
   `npm run audit:network` for every layer). A `NEW` finding: a package the app uses to go online
   is an SDK to declare (that covers it); an unreachable capability gets a baseline entry with a
   reason, a `Gate-Change:` trailer and the reviewer's approval.
7. Runtime ([references/network-layers.md](references/network-layers.md), layer F): set
   `contracts/e2e.json` `network` from the profile (e2e-maestro runs the sampler on named devices
   with it). Wire the guard by hand (debug-menu-and-test-hooks' entry does not carry it): add
   `export { installNetworkGuard } from '@/services/test-hooks/network-guard';` to
   `src/test-only-entry.ts`, and call
   `TEST_ONLY?.installNetworkGuard(globalThis, { onAttempt, allowedHosts })` in
   `src/services/test-hooks/install-network-guard.ts`, imported by `src/app/_layout.tsx` right after
   the error net (the module and its hosts: layer F in the reference). Expect zero blocked attempts
   and an empty sampler report on both platforms.
8. Release: run `audit-app-bundle.mjs` on the built `.app` and the merged Android manifest
   ([references/release-audit.md](references/release-audit.md)).
9. Secrets: follow [references/secrets.md](references/secrets.md); on any leak, stop and walk the
   developer through the leak response.
10. Print the answers with `audit-repo.mjs . --answers` and report in plain words
    (`examples/audit-run.md`): what passed, any baseline waiting for approval, and the App Privacy and
    Data safety answers the developer enters by hand.

## Definition of done

- [ ] `contracts/privacy.json` names the profile, every network-capable SDK with its pods, Gradle groups,
      tracking and collected data, the app's own collection, every permission answer and account deletion.
- [ ] The templates are in place, wired (`ios.privacyManifests`, `audit:network`, `audit:privacy`), and
      their Jest tests pass.
- [ ] After the latest prebuild `audit-privacy-manifest.mjs` passes; after the latest export
      `audit-bundle.mjs` passes for iOS and Android; `npm run audit:network` passes.
- [ ] E2E shows zero blocked attempts and an empty socket report from live samplers on both platforms.
- [ ] Release: `audit-app-bundle.mjs --app … --android-manifest …` passes on the production build.
- [ ] The developer has the printed App Privacy and Data safety answers; every baseline or profile change
      has a `Gate-Change:` trailer and the reviewer's approval.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/audit-repo.mjs .` prints `RESULT: PASS` (expected SKIP lines:
      `ios/Podfile.lock [vendor-pod]` before a prebuild; `contracts/dependency-policy.json [profile-policy]`
      for an offline-only app before dependency-management creates the policy; `quality-gates.json
      [gated-paths]` before quality-gates; `contracts/e2e.json [runtime-proof]` before e2e-maestro)

## Anti-patterns

- **Baselining first-party code or adding a pod "to unblock the release".** Remove the code or the SDK;
  allow-list changes are the reviewer's call.
- **Grepping the raw bundle for an ad ID or a URL.** SDKs ship their test IDs and docs links in every
  bundle; attribute by module through the source maps (`audit-bundle.mjs`).
- **Answering "Data Not Collected" because the app's own code collects nothing.** The SDKs' collection
  is the app's collection in both stores; print the answers from the contract.
- **Listing an ads SDK's domains in `NSPrivacyTrackingDomains` "to be safe".** iOS then blocks them for
  everyone who declines ATT, and their ads stop.
- **Editing `ios/` (PrivacyInfo, Info.plist) or `android/` by hand.** Prebuild rewrites them; change
  `privacy-manifest.ts`, `app.config.ts` or a config plugin.
- **Trusting `expo config --type introspect` for ATS.** Without `ios/` it shows a placeholder
  Info.plist with `NSAllowsArbitraryLoads: true` that prebuild never writes; check the built app.
- **Installing NetInfo for online detection.** Its default reachability check requests a Google URL;
  use `expo-network` behind the `ConnectivityPort` (networking-and-server-state).
- **Running the runtime layer on a development build or with ads on.** Metro and ads open sockets
  legitimately; use a release build of a testing variant with ads off, on named devices.
- **Printing a JWT or a request with its headers while debugging an upload.** Log the error body only.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/network-layers.md](references/network-layers.md) | The profiles; layers A to F, what each catches and misses (and the limits of the source patterns); the runner; the runtime policy, the guard and what the samplers measure (iOS and Android); baselines and gated paths | Workflow steps 1 and 7; on any NEW or STALE finding |
| [references/sdk-inventory.md](references/sdk-inventory.md) | What counts as a network SDK, declaring one, facts for common SDKs, before adding a package, multi-package | Workflow step 3; before installing any SDK |
| [references/store-declarations.md](references/store-declarations.md) | The contract key by key, collected/linked/tracking/shared, App Privacy and Data safety mapping, facts other skills hand over, permissions, deletion, the human step, a worked answer set | Workflow steps 3 and 10 |
| [references/privacy-manifest.md](references/privacy-manifest.md) | Why the manifest is aggregated, the wiring, the verified SDK 57 reasons, the after-prebuild audit, tracking, collected data | Workflow step 5 |
| [references/release-audit.md](references/release-audit.md) | The binary audit for iOS and Android, rule by rule, commands in order, checklist | Workflow step 8 |
| [references/secrets.md](references/secrets.md) | What counts as a secret, where secrets live, the checks, agent rules, leak response | Workflow step 9 |
| `examples/contracts/privacy.json` | A filled contract for a Tasks app with accounts, ads, Premium, crash reporting and pushes; its SDK rows pass `audit-privacy-manifest.mjs` on a real SDK 57 prebuild | Workflow step 3, as the shape |
| [examples/audit-run.md](examples/audit-run.md) | A complete audit run with findings handled and the report | Workflow step 10, as the model |
| `templates/contracts/privacy.json` | The empty contract (api-port, nothing declared) | Workflow step 2 |
| `templates/contracts/privacy.schema.json` | Its JSON schema (editors validate the contract with it) | Workflow step 2 |
| `templates/contracts/network-baseline.json` | The starting js and native baseline of a `create-expo-app` SDK 57 app and the canonical stack, with reasons | Workflow step 2 |
| `templates/src/config/privacy-manifest.ts` | `PRIVACY_MANIFESTS`: the seven reasons every Expo SDK 57 app ships, no tracking | Workflow steps 2 and 5 |
| `templates/src/config/privacy-manifest.test.ts` | Pins the reasons and the absence of tracking (add a reason here first) | Workflow step 5 |
| `templates/src/services/test-hooks/network-guard.ts` | The test-only JS network guard with allowed hosts and the dev loopback exception; keeps WebSocket's constants and prototype and reads a Request's url (installed from the test-only entry) | Workflow steps 2 and 7 |
| `templates/src/services/test-hooks/network-guard.test.ts` | Its test on a fake global scope | Workflow step 2 |
| `templates/scripts/audit/` | `audit-network.ts` and its layers (contract, bundle modules, JS, native, pods, config, baseline, `sdk-packages.ts`: the packages a declared SDK installs), `audit-privacy.ts` + `privacy-manifest.ts`, with tests | Workflow steps 2 and 6 |
| `assets/privacy-facts.json` | Network SDK families, pod and Gradle families, verified required reasons per package, permission kinds, secret patterns, JS patterns | Read by the scripts; change with the reviewer |
| `assets/data-types.json` | Data types and purposes mapped to App Privacy, the manifest constants and Data safety | Read by the scripts and references |
| `scripts/audit-repo.mjs` | Static audit: network seams, SDK inventory (workspaces included), store answers, permissions, offline profile, pods, Gradle, manifest, tooling, gated paths, runtime policy, secrets; `--answers` prints both forms and the Data safety security practices | Workflow steps 4 and 10 |
| `scripts/audit-bundle.mjs` | The release export's JavaScript, iOS and Android, attributed per module | Workflow step 6 |
| `scripts/audit-privacy-manifest.mjs` | Pod manifests (trunk and development) against the declared manifest and the contract | Workflow step 5 |
| `scripts/audit-app-bundle.mjs` | The built `.app` and the merged Android manifest against the contract | Workflow step 8 |
| `scripts/lib/privacy-scan.mjs` | Shared helpers: facts, the contract reader, installed packages, source files, seams | Read only to change a script |
| `scripts/lib/plist.mjs` | Shared plist parser, XML and binary (synced; never edit here) | Read only to change a script |
| `scripts/lib/usage-strings.mjs` | Shared purpose-string reader for Info.plist and `.lproj` files (synced; never edit here) | Read only to change a script |
| `scripts/lib/ship-placeholders.mjs` | Shared list of placeholder values a release refuses (synced; never edit here) | Read only to change a script |
| `scripts/check-lib.mjs` | Shared script helper (synced; never edit here) | Never by hand |
| `scripts/selftest.mjs` | Proves the four audits on assembled fixtures | After changing a script, template or fixture |
| `assets/shared.json` | Declares the synced files | When adding a shared file |
| `tests/` | Bases (`repo`, `bundle`, `pods`, `app`) and one overlay case per planted bug | When adding a rule |

## Related skills

- `networking-and-server-state` - the ApiClient port, cleartext and base URLs under api-port.
- `dependency-management` - installs, pins and the offline-only ban list in the dependency policy.
- `architecture-and-boundaries` - SDKs only in their adapters.
- `admob-ads-and-consent` - the ads SDK, consent and the ATT flow and text.
- `in-app-purchases` - expo-iap, its server opt-ins and StoreKit artefacts.
- `push-notifications`, `crash-reporting-and-observability`, `analytics-and-consent` - SDK facts to declare.
- `permissions-and-system-prompts` - the permissions contract this skill answers.
- `e2e-maestro` - the runner and socket sampler that run layer F with `contracts/e2e.json` `network`.
- `debug-menu-and-test-hooks` - the test-only entry the guard is installed from.
- `quality-gates` - `gatedPaths`, which makes the baseline and the contract need a `Gate-Change:` trailer.
- `ios-release-testflight`, `android-release-play`, `eas-build-and-submit` - the release gates and consoles.
- `git-commits-and-reporting` - the `Gate-Change:` trailer and the report.
