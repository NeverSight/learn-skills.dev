---
name: deep-links-and-universal-links
description: "Gates every incoming link: custom schemes, universal links (AASA), App Links (assetlinks), a route allow-list. Use when adding a deep link, scheme, associated domain or share link. Not for routes (navigation-and-routing)."
---

# Deep links and universal links

Every link that opens the app (a custom scheme, an iOS universal link, an Android App Link; cold start
or warm) passes one synchronous gate that opens only allow-listed routes with checked values. Verified
hosts flow from one contract into the app config of every variant and into the hosted
apple-app-site-association and assetlinks.json files. A checker replays hostile URLs through the app's
own gate. Verified on 2026-10-14 with Expo SDK 57 (expo 57.0.26), expo-router 57.0.24 and expo-linking
57.0.11 in Jest inside the real router and with `npx expo config`; not yet driven on a device.

## Rules that must hold

1. **One gate for every incoming link: `src/app/+native-intent.tsx`.** It exports `redirectSystemPath`,
   which hands every URL, cold (`initial: true`) and warm (`initial: false`), to `routeIncomingLink` and
   returns only its answer. No other code subscribes to links: no `'url'` listener, `getInitialURL`,
   `getLinkingURL`, `useLinkingURL`, `useURL` or `legacy_subscribe`. Why: Expo Router turns every file into
   a URL and routes whatever arrives; a second handler navigates twice or opens what the gate refused.
   (`intent-gate`, `one-listener`)
2. **The gate is synchronous and total.** The decision runs inside `attempt(...)`; a crash is reported to
   the error net and treated as a refusal; no `async`, `await`, `then` or `fetch` in it. Why: a throw there
   crashes the launch, a promise holds the first screen, and a rejection loses the link. Short links and
   referral codes resolve in a landing route that replaces itself. (`intent-total`, `gate-behaviour`)
3. **An allow-list decides what a link may open.** `LINK_ROUTES` names each linkable route by URL path
   (groups dropped, no catch-alls), and every entry is a real route file. Anything else opens the first
   screen. Why: without it any web page, QR code or app can open account deletion, checkout or a debug
   screen with any params. (`link-routes`, `link-route-exists`)
4. **Values are checked by kind, query keys are listed, the href is re-encoded.** Each dynamic segment has
   a kind (`slug`, `uuid`, `int`); unknown query keys (`utm_source`, `fbclid`) are dropped; a repeated kept
   key, a control character or a value over 256 characters is refused; no query key shadows a segment
   name; the gate returns an encoded path.
   The screen still parses its params with its valibot parser. Why: Expo Router decodes query values and
   joins them again unencoded (`a%26b` becomes two keys), and in-app navigation never passes the gate.
   (`link-routes`, `gate-behaviour`)
5. **A refused cold link lands on the first screen; a refused warm link changes nothing.** Cold returns
   `/`, warm returns `null`, and the refused URL is shown nowhere. Why: the router must render something at
   launch, but navigating home from a running app throws away unsaved work for a link that opens nothing.
6. **A link into a guarded group waits, then opens once.** Its entry names the `gate` and builds a typed
   href in `open()`; the guard's owner calls `useLinkGate(gate, isOpen)`; the first screen behind the guard
   calls `useOpenPendingLink(gate)`. Why: on SDK 57 a link into a closed `Stack.Protected` group lands on the
   first reachable screen and is lost after sign-in; `+native-intent` cannot read React state.
   (`pending-link`)
7. **Custom schemes reach anyone; secrets ride only verified links.** A route whose query or params carry a
   token, password, OTP, magic or reset code is `verifiedOnly` (http(s) of a verified host: Android verifies
   both schemes, iOS delivers only https). The secret is single-use, short-lived and confirmed on screen.
   Why: any app can register the app's scheme and receive the link; any app can still send a verified one.
   (`link-secret`)
8. **Links open screens; they never act, and never forward.** No route opened by a link mutates, buys,
   deletes, signs in or changes settings on arrival; the person taps. No link's params reach
   `Linking.openURL` or the browser, and none becomes an href (`router.replace(params.next)`): a
   return after sign-in goes through the pending-link inbox. Why: links are sent by strangers, prefetched by mail scanners and
   re-delivered after a reload; a forwarded URL is an open redirect with the app's trust. (`open-redirect`)
9. **Debug and test-build routes are refused in production.** The debug link entry is
   `{ path: '/debug/setup', query: 'any', testBuildOnly: true }`. Why: a production link must not reach a
   screen the production bundle does not contain. (`link-test-only`)
10. **One contract for verified hosts, applied to every variant.** `contracts/deep-links.json` lists hosts
    per variant; `linkNativeConfig()` turns them into `applinks:<host>` entries and one App Links filter
    (`autoVerify`, `VIEW`, `BROWSABLE`, `DEFAULT`, http and https, a `pathPattern` per web path); the gate
    accepts exactly the hosts of the running config (publish each update with the build's `APP_VARIANT`). Why: when the entitlement, the filter and the gate
    disagree, links silently open the browser or a page the app refuses. (`link-contract`, `native-links`)
11. **The web paths and the hosted files match the app.** Every `webPaths` entry opens a listed route; each
    host's AASA and assetlinks.json are generated by `write-well-known.mjs` and deployed by a person to
    `https://<host>/.well-known/` over HTTPS with no redirect. Why: iOS fetches the AASA through Apple's CDN
    at install and about weekly after, and Android verifies at install; a wrong file fails silently.
    (`web-paths`, `well-known`)
12. **Real ids and fingerprints before a release.** The assetlinks fingerprint is the key that signs what
    people install (Play App Signing's, not the upload key's); `--release` fails on `example.com` hosts,
    `com.example.*` ids and unfilled tokens. (`ship-placeholder`)
13. **Every linked route is tested cold and warm.** Jest through the real router with a `+native-intent`
    entry (cold via `initialUrl`, warm via the router's `url` listener), then named devices or Maestro
    `openLink`. Why: Jest cannot prove the OS hands the link to the app.

## Workflow

1. **Read what the task needs:**

   | Task | Read |
   |---|---|
   | first setup, a new linked screen, params, gates, cold vs warm, notification or OAuth links | [references/link-routing.md](references/link-routing.md) |
   | universal links, App Links, AASA, assetlinks.json, fingerprints, hosting | [references/universal-and-app-links.md](references/universal-and-app-links.md) |
   | trying links on a simulator, an emulator or in Maestro | [references/device-testing.md](references/device-testing.md) |
   | a FAIL line, the replay, configuration | [references/checker.md](references/checker.md) |
   | a React Navigation app | [references/react-navigation-linking.md](references/react-navigation-linking.md) |

2. **Set up the gate once.** Copy `templates/src/app/+native-intent.tsx`, `templates/src/core/links/`,
   `templates/src/features/deep-links/`, `templates/src/services/deep-links/`, the two hooks in
   `templates/src/hooks/` and `templates/contracts/` (every test with its file). The scheme per variant
   comes from app-variants-and-environment. With the debug menu (debug-menu-and-test-hooks), add its
   test-build entry to `LINK_ROUTES`. Run
   `npx jest src/core/links src/features/deep-links src/services/deep-links src/hooks --selectProjects unit`.
3. **Link a screen.** Add its entry to `LINK_ROUTES` after `examples/link-routes-tasks.ts`: the URL path,
   a kind per segment, the query keys the screen reads, `verifiedOnly` for secrets. The screen parses its
   params (navigation-and-routing's params parser). Behind a guard: add `gate` and `open`, call
   `useLinkGate` where the guard is decided and `useOpenPendingLink` in the first screen's model. Add a
   case to `deep-links-navigation.test.tsx` for the new route, cold and warm.
4. **Add verified links** (when the app has a domain): fill `contracts/deep-links.json` (hosts per variant,
   `webPaths`, `appleTeamId`, `androidCertFingerprints`), wire `templates/scripts/deep-links/link-native-config.ts`
   into app.config.ts as `examples/app-config-deep-links.ts` shows (a variant without hosts gets no
   `associatedDomains` key: an empty array still writes the entitlement), make a new native build, and hand
   off to expo-prebuild-and-config-plugins: refresh its native snapshot with its `--write` option after
   reading the drift (the new entitlement and MainActivity filter) and commit it with the change. Then run
   `node ${CLAUDE_SKILL_DIR}/scripts/write-well-known.mjs .`. **Stop and ask the developer** to deploy each
   `<wellKnownDir>/<host>/` folder to `https://<host>/.well-known/` and to confirm the fingerprints from
   Play Console or `eas credentials`; uploading to a website is outward-facing.
5. **Try it on devices** (references/device-testing.md): cold and warm on a named simulator and emulator,
   `pm get-app-links` for Android verification; hand the flows to e2e-maestro (`examples/maestro-deep-links.yaml`).
6. **Run the checks:** `node ${CLAUDE_SKILL_DIR}/scripts/check-deep-links.mjs .`; fix every `FAIL` line
   (file, rule, fix) and rerun until `RESULT: PASS`. In CI, also
   `node ${CLAUDE_SKILL_DIR}/scripts/write-well-known.mjs . --check`. Before a release, run the checker with
   `--release`.

## Definition of done

- [ ] `src/app/+native-intent.tsx` re-exports `redirectSystemPath`; no other code listens to links.
- [ ] `LINK_ROUTES` lists every linkable route with kinds and query keys; secrets are `verifiedOnly`, debug
      routes `testBuildOnly`, gated routes have `open()`, `useLinkGate` and `useOpenPendingLink`.
- [ ] No linked screen acts on arrival; no link's params reach `openURL` or the browser.
- [ ] The template tests and a cold and warm case per linked route pass in Jest; `redirect-system-path.test.ts`
      is what proves rule 5 (refused cold `/`, refused warm `null`), which the checker cannot replay.
- [ ] With a domain: the contract, the app config of every variant and the well-known files agree
      (`write-well-known.mjs . --check` prints `RESULT: PASS`); the developer deployed the files and saw
      `verified` in `pm get-app-links` and the app open from a link in Notes.
- [ ] Before a release: `node ${CLAUDE_SKILL_DIR}/scripts/check-deep-links.mjs . --release` prints
      `RESULT: PASS`.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-deep-links.mjs .` prints `RESULT: PASS` (no SKIP lines:
      every target is this skill's own; an app that takes no input from links prints NOT APPLICABLE).

## Anti-patterns

- **A `+native-intent` that returns `path` "for now".** Every link then opens whatever it names. Return
  only what `routeIncomingLink` decided.
- **`Linking.addEventListener('url')` or `useLinkingURL()` in a screen.** It double-handles links and skips
  the gate. List the route; read params in the screen model.
- **Resolving a short link inside `redirectSystemPath` with `await fetch`.** The launch waits on the
  network. Open a landing route that resolves and replaces itself.
- **`router.navigate('/')` for a link that opens nothing while the app runs.** It discards work; return
  `null`.
- **A password-reset or magic-link token on the custom scheme.** Another app can receive it. Verified
  https links only, single-use, confirmed on screen.
- **A link that completes, joins, pays or deletes on arrival.** Show the screen; the person taps.
- **`Linking.openURL(params.url)`.** An open redirect; links carry ids, the app builds URLs in `src/config`.
- **Refusing links with unknown query keys.** Shared links gain `utm_*` and `fbclid`; drop them instead.
- **`applinks:https://example.com` or an https filter without `autoVerify`.** Universal links never work;
  Android 12+ opens the browser.
- **The upload key's fingerprint with Play App Signing.** Installs from Play fail verification; use the
  app signing key's.
- **Editing the hosted AASA by hand.** It drifts from the app; change the contract and regenerate.
- **Sharing `tasks://...` links.** They open nothing without the app; share the https link.
- **`npx uri-scheme open` or `simctl openurl booted` with several simulators running.** Name the device.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/link-routing.md](references/link-routing.md) | How links reach the router (read in source), the gate's decisions, the allow-list, origins, cold/warm/gated, links never act, OAuth, notifications, the debug link, share links, test recipes, pitfalls | Workflow steps 1-3 |
| [references/universal-and-app-links.md](references/universal-and-app-links.md) | Scheme vs verified links, the contract pipeline, iOS entitlement and AASA, Android filter and assetlinks.json, fingerprints, hosting, variants, debugging verification | Workflow step 4 |
| [references/device-testing.md](references/device-testing.md) | Cold and warm on named simulators and emulators, verified links on devices, Maestro `openLink`, Expo Go | Workflow step 5 |
| [references/checker.md](references/checker.md) | Every rule with its fix, the gate-behaviour replay, configuration, write-well-known, the self-test | Workflow step 6, on a FAIL |
| [references/react-navigation-linking.md](references/react-navigation-linking.md) | Appendix: the same gate in a React Navigation 7 app | Only for a React Navigation app |
| `templates/src/app/+native-intent.tsx` | The gate's entry for Expo Router (re-exports `redirectSystemPath`) | Workflow step 2 |
| `templates/src/core/links/` | `link-route.ts` (kinds, the entry type, table checks), `incoming-link.ts` (URL parsing), `route-incoming-link.ts` (the decision), each with its test | Workflow step 2 |
| `templates/src/features/deep-links/` | `link-routes.ts` (the allow-list), `link-origins.ts`, `app-link-policy.ts`, `redirect-system-path.ts`, their tests and the router test `deep-links-navigation.test.tsx` | Workflow steps 2-3 |
| `templates/src/services/deep-links/` | `pending-link-inbox.ts` and `link-gates.ts` with tests | Workflow steps 2-3 |
| `templates/src/hooks/` | `use-link-gate.ts` and `use-open-pending-link.ts` with tests | Workflow step 3 |
| `templates/scripts/deep-links/` | `link-native-config.ts` (contract to associatedDomains and intentFilters, for app.config.ts) with its test | Workflow step 4 |
| `templates/contracts/` | `deep-links.json` (empty hosts) and its JSON schema | Workflow steps 2 and 4 |
| `examples/link-routes-tasks.ts` | A full Tasks allow-list: shared, static, gated, invitation, verified-only, OAuth, paywall, debug | Workflow step 3 |
| `examples/app-config-deep-links.ts` | The app.config.ts lines that wire verified links per variant | Workflow step 4 |
| `examples/share-task-link.ts` | Building share links on the verified host in `src/config` | When the app shares links |
| `examples/maestro-deep-links.yaml` | Cold, warm and Android verified links in a Maestro flow | Workflow step 5 |
| `scripts/check-deep-links.mjs` | Checker for every rule above, with the gate replay | Workflow step 6, before a release with `--release` |
| `scripts/write-well-known.mjs` | Writes or (`--check`) verifies each host's AASA and assetlinks.json | Workflow step 4, in CI |
| `scripts/selftest.mjs` | Proves both scripts against the fixtures | After changing a script |
| `scripts/lib/link-facts.mjs` | This skill's shared facts: paths, config evaluation, origins, expected files | Never by hand unless changing the scripts |
| `scripts/check-lib.mjs` | Shared script library (synced; do not edit here) | Never by hand |
| `scripts/lib/source-scan.mjs` | Shared import resolution and test-file detection (synced) | Never by hand |
| `scripts/lib/app-modules.mjs` | Shared loader for the app's pure TypeScript (synced) | Never by hand |
| `scripts/lib/ship-placeholders.mjs` | Shared placeholder list for `--release` (synced) | Never by hand |
| `assets/shared.json` | Declares the synced files | When adding a shared file |
| `tests/bases/` | The fixture apps: `app/` (six link routes, two verified hosts, development without hosts, planted installed skills) and `plain/` (no link input) | When adding a rule |
| `tests/fixtures/` | The self-test cases per script: good, one planted bug per rule, NOT APPLICABLE, bad input | When adding a rule |

## Related skills

- `navigation-and-routing` - routes, guards (`Stack.Protected`), params parsers, the not-found route.
- `app-variants-and-environment` - one scheme, id and name per variant.
- `auth-and-secure-storage` - the session guard, the OAuth redirect route and PKCE.
- `push-notifications`, `local-notifications` - notification taps mapped to typed hrefs.
- `debug-menu-and-test-hooks` - the debug link and the `TEST_ONLY` gate.
- `error-handling-typed-results` - `attempt` and the error net the gate reports to.
- `expo-prebuild-and-config-plugins` - native config from app.config.ts; a rebuild after link changes.
- `eas-build-and-submit`, `ios-release-testflight`, `android-release-play` - the Associated Domains capability and signing keys.
- `e2e-maestro` - link flows on named devices; `ios-simulator-build`, `android-emulator-build` - the devices.
- `web-support` - serving the website and the well-known files with Expo Router web.
- `expo-router` (Expo's official skill) - the Expo Router API reference.
