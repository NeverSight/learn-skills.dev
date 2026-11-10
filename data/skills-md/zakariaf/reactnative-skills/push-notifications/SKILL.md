---
name: push-notifications
description: "Builds remote push on expo-notifications: in-context permission, token sync, server contract, channels, tap routing. Use when adding push, push tokens, FCM/APNs setup or notification taps. Not for local reminders (local-notifications)."
---

# Push notifications

Makes remote push correct on iOS and Android: the permission is asked only when the person sees why,
the server always holds this device's current token (and drops it at sign-out), Android channels and
data kinds match a written contract with the server, a tap opens exactly the screen it is about and
nothing a payload names, and one foreground policy decides what shows while the app is open. A
zero-dependency checker proves the structure; Jest tests over a fake port prove the behaviour.

## Rules that must hold

1. **Ask in context, never at launch; channels first.** The prompt comes from a person's action
   that the notification extends (`optInToPush` from an `onPress`, after the explanation), never from
   the root layout, the composition root or an effect. Android channels exist before the prompt;
   `blocked` offers the system settings. Why: iOS shows its prompt once in an install's life, Android
   issues no token before a channel exists (and an app targeting 12L or lower gets its prompt only
   after the first channel), and a launch prompt is refused more often than any other.
   (`permission-in-context`, `channel-setup`)
2. **One adapter owns expo-notifications' push APIs.** Token, permission, handler and response calls
   live only in `expo-notifications-push-adapter.ts` behind `PushPort`; everything else, tests
   included, uses the port or `createFakePush()`. Why: the SDK's quirks (deprecated `*Async`, the iOS
   `body` key, provisional status, error codes) stay in one tested file, and no test loads native code.
   (`push-adapter-only`)
3. **The token carries an explicit EAS project id and follows every change.** `getExpoPushTokenAsync`
   gets `{ projectId }` from `readEasProjectId()` and the app config sets `extra.eas.projectId`;
   `addPushTokenListener` re-registers each rotation with the token it replaces. Why: without the id a
   non-EAS build gets no token, and a rotated token the server never learned is a silent dead end.
   (`expo-project-id`, `token-rotation`)
4. **One registration, serialized, idempotent, triggered, remembered.** `createPushRegistration`
   syncs at launch, on every return to the foreground (after the channel sync), on rotation and on
   account change, one sync at a time, through a `PushRegistrar` over the signed-in ApiClient, never
   the plain `services.api` while registrations need an account (`PUT /push/registrations/{token}`;
   the server takes the account from the credentials only). The last
   accepted registration is saved (`PushRecordPort`, kv-store), so the first sync after notifications
   were switched off in Settings unregisters it, in the same process or a new one; a failure waits for
   the next trigger (no retry timer); the server drops what is never seen again (`not-seen-270-days`).
   Why: two concurrent registrations arrive in any order; an unsigned call is answered 401 and the
   device never registers; Android ends the process when the permission is revoked; and iOS silently
   drops pushes to a device that turned them off while the server counts them as sent.
   (`push-wiring`, registration tests)
5. **`contracts/push.json` is the agreement with the server.** It names the provider, whether
   registrations need an account, every data kind and every channel; `PUSH_KINDS` and `PUSH_CHANNELS`
   equal it. Why: the server and the app ship separately; a kind or channel only one side knows is a
   notification that never shows or never opens. (`push-contract`, `push-token`, `kinds-contract`,
   `channel-contract`)
6. **The payload is untrusted input.** `parsePushData` (valibot) reads `{ kind, <id> }` with opaque
   ids; every value a string, the whole message at most 4096 bytes, no secret or personal content.
   Why: anyone holding a token can send any JSON, a direct FCM message turns values into strings, and
   the text passes through Apple, Google and Expo onto a locked screen. (`payload-parse`, `kinds-contract`)
7. **A tap opens a destination from the table, never a route or URL from the payload.**
   `destinationFor` maps a parsed kind to a `PushDestination`; the app maps it to a typed href. Why: a
   forged or stale push could otherwise open debug routes, guarded screens or any website.
   (`payload-navigation`)
8. **Taps are handled at cold start and while running, once each, below the navigator.** The launch
   tap is read once and cleared, the listener handles the rest, each notification id once; only
   taps whose data parses as a push message are handled or cleared (a reminder's launch tap stays for
   local-notifications); `usePushTaps` runs in the push root kit's effects, beside the root Stack. Why: at a cold start the same tap arrives twice,
   and Expo Router refuses to navigate before the root layout mounts. (`tap-handling`, `push-wiring`)
9. **Exactly one foreground handler decides for remote and local notifications.** The adapter installs
   it from `foregroundPresentation`, answering at once with `shouldShowBanner`/`shouldShowList` (never
   the deprecated `shouldShowAlert`). Why: with no handler (or one slower than 3 s) a foreground
   notification is not shown, and a second `setNotificationHandler` silently replaces the first.
   (`foreground-handler`, `deprecated-api`)
10. **Android channels are stable, translated and contracted.** Each id means one behaviour forever
    (importance is fixed once created), names come from the catalogs, the plugin's `defaultChannel`
    equals the contract's. Why: a push naming a channel the device lacks is dropped, and a reused id
    keeps its old importance on every installed phone. (`channel-contract`, `plugin-config`)
11. **Native config per variant; credentials by a person, never in the repo.** The plugin sets `mode`
    (the APNs environment each variant states: `development` for the dev client, `production` for
    builds that ship), `icon` and `defaultChannel`; `android.googleServicesFile` lists every variant's
    package; the APNs key and the FCM V1 service account key go to EAS through `eas credentials`.
    Why: distribution export signs with the profile's production entitlement (Expo's docs), so a
    store build gets pushes only when its bundle id has the Push capability and an APNs key in EAS;
    Android issues no token without FCM; a committed key lets anyone push as the app.
    (`plugin-config`, `fcm-config`, `push-credentials`)
12. **Sign-out removes the registration while the session is still valid.** `pushRegistrationStep`
    is a server sign-out step named `push-registration` in `contracts/auth.json`; its `DELETE` carries
    the step's own access token and removes the saved token first (the one the server holds), then a
    newer one; the server also drops registrations of revoked or expired sessions and on
    `DeviceNotRegistered`, and deletes only the caller's own registrations. Why: otherwise the next
    person on the phone receives this person's notifications. (`sign-out-unregister`)
13. **The app never sends pushes.** No Expo, FCM or APNs send endpoint, no `expo-server-sdk`, no push
    access token in `EXPO_PUBLIC_*`. Why: sending needs a credential, and anything in the app is
    public. (`client-send`, `push-credentials`)

## Workflow

1. Read `references/architecture-and-contract.md` (the pieces, the registration, the contract, the
   payload, taps, the foreground policy). Stop and ask the developer: the provider (`expo` unless the
   server already talks to APNs and FCM), whether registrations need an account, the data kinds and
   what each opens, and the channels a person may want to mute separately.
2. Install and configure (`references/setup-and-credentials.md` sections 1-3):
   `npx expo install expo-notifications expo-constants`, then the plugin, `googleServicesFile` and
   `extra.eas.projectId` in `app.config.ts` (`examples/app.config.ts`). The credential steps
   (section 4) create keys in outside accounts: hand them to the developer; never create, read or
   commit a key.
3. Copy every file under `templates/` to the path its first line names (JSON files land at their path
   under `templates/`), tests included; the catalog keys merge into the app's catalogs, keys kept
   in sorted order (i18n-strings-and-catalogs' linter fails on unsorted keys).
4. Make the templates the app's: kinds in `push-message.ts`, destinations in `push-destination.ts`,
   the policy in `foreground-presentation.ts`, channels in `push-channels.ts` plus their catalog keys
   in every language, and the same facts in `contracts/push.json`; update each test with them.
5. Wire it as a root kit (`references/architecture-and-contract.md` section 10): the adapter, the
   saved-record adapter and the registration (`examples/create-app-push.ts`; with accounts they exist
   before the session, which takes `pushRegistrationStep` and attaches itself to the signed-in client,
   `"push-registration"` in `contracts/auth.json`, `examples/create-app-session.ts`), the registrar over
   the signed-in client, never the plain `services.api` (`examples/push-registrar.ts`,
   `examples/session-api-client.ts`), and `createPushKit({ push, registration, errorLog, account,
   openSettings, hrefForDestination })` registered in app-startup-and-bootstrap's
   `src/services/create-root-kits.ts` (`examples/create-root-kits.ts`, with the route table
   `examples/push-destination-href.ts`). The kit provides the in-context ask's dependencies
   (`usePushServices()`) and mounts `usePushSync`, the rotation watch (`registration.start()`) and
   `usePushTaps` beside the root Stack; the root files stay unchanged. Add `expo-notifications` to the architecture contract's
   `vendorSdks` (`"LocalNotificationsPort/PushPort"` when local-notifications is adopted too). With
   local-notifications adopted, create its adapter with `installForegroundHandler: false` (this
   adapter's handler decides for both; never edit the copied local adapter).
6. Build the in-context ask where the value is visible (`examples/use-share-list-model.ts`). The
   notification permission is the `notifications` kind of permissions-and-system-prompts'
   `PermissionsPort`: bind `access.notifications` to this port's `permission`/`requestPermission`
   (architecture-and-contract.md section 2), ask through its `usePermissionGate` from the press, and
   call `optInToPush` from `onAllowed` (it then only syncs channels and registers). Add a
   `notifications` entry to `contracts/permissions.json` (no `purposeKey`; explain and settings copy
   keys in every catalog; `askedFrom` = that model, with a sibling test naming blocked and declined),
   or check-permissions fails. Without that skill, `optInToPush` asks itself and `blocked` offers
   `Linking.openSettings()`.
7. Hand the store facts to privacy-and-store-declarations (`references/setup-and-credentials.md`
   section 6) and the server facts (`contracts/push.json`, `examples/server/send-task-assigned.ts`) to
   the backend developer.
8. Test the copied registrar and session client too (testing-push.md section 1, "The registrar":
   401 → rejected, 404 on DELETE → done, retryable → unavailable, the sign-out DELETE's bearer, the
   unattached client → unauthorized). Run `npx jest --ci src/core/push src/services/push src/hooks`, then
   `node ${CLAUDE_SKILL_DIR}/scripts/check-push.mjs .`; fix and rerun until `RESULT: PASS`. Look up a
   rule in `references/checker-rules.md`, a symptom in `references/platform-behaviour.md` section 8.
9. Prove the native path on a named simulator (`xcrun simctl push <udid> ...` with
   `examples/task-assigned.apns`) and an emulator, then hand the device checklist
   (`references/testing-push.md` section 5) to a person for one iPhone and one Android phone.

## Definition of done

- [ ] No prompt at launch; the ask comes from an action, channels first, `blocked` offers Settings.
- [ ] Only the push adapter calls expo-notifications' push APIs; tests use `createFakePush()`.
- [ ] Explicit `projectId`; `extra.eas.projectId` set; rotations re-register with `previousToken`.
- [ ] One registration service, synced at launch, foreground, rotation and account change; its record saved.
- [ ] `contracts/push.json` filled in and handed to the server; kinds and channels equal the code.
- [ ] Payloads parsed with valibot; taps open only `destinationFor` destinations via typed hrefs.
- [ ] Launch tap read once and cleared (push taps only); listener deduped; `usePushTaps` below the navigator.
- [ ] One `setNotificationHandler`, from `foregroundPresentation`; no deprecated API.
- [ ] Plugin with `mode` per variant, `icon`, `defaultChannel`; `googleServicesFile` with every variant.
- [ ] Credentials uploaded to EAS by a person; no key or access token anywhere in the repo.
- [ ] `push-registration` in `serverSignOutSteps` when registrations need an account.
- [ ] The push root kit is registered in `src/services/create-root-kits.ts`; no root file imports push code.
- [ ] The registrar signs every call: `signedInApi` (attached by the session), never `services.api`
  when registrations need an account; the sign-out `DELETE` carries the step's access token.
- [ ] `npx jest --ci` passes, including every template test.
- [ ] Device checklist done on one iPhone and one Android phone before release.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-push.mjs .` prints `RESULT: PASS` (the only allowed
  SKIP is `SKIP contracts/auth.json [sign-out-unregister] not yet created (auth-and-secure-storage
  creates it)`; `NOT APPLICABLE` only while expo-notifications is absent or nothing requests a token).

## Anti-patterns

- **`requestPermissionsAsync()` in the root layout "so it is done".** Asked before any value is
  shown, refused, and on iOS never asked again. Ask from the action the notification extends.
- **`router.push(response.notification.request.content.data.url)`** (Expo's own sample shape). Any
  sender can open any route or site. Parse, map to a destination, map that to a typed href.
- **Registering only after the prompt.** Tokens rotate and people flip Settings; sync on launch,
  foreground, rotation and account change.
- **A `setNotificationHandler` per feature.** The last one wins for every notification; one policy.
- **`useLastNotificationResponse()` in a screen.** It is `undefined`, then `null`, then the response:
  late, twice, and only on that screen. One router hook below the navigator.
- **Custom keys at the top of a hand-made APNs payload.** iOS hands `content.data` from `"body"`
  only; the tap finds no data.
- **Reusing a channel id with new importance.** Installed phones keep the old one; new id instead.
- **Unregistering after the token wipe at sign-out.** It goes out unauthenticated and fails
  silently; make it a server sign-out step.
- **Data-only pushes as a sync mechanism.** iOS throttles and drops them; refresh on foreground.
- **Sending a push from the app or putting the Expo access token in `EXPO_PUBLIC_*`.** Public the
  moment the app ships.
- **Testing push in Expo Go on Android.** Removed in SDK 53; use a development build.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| `references/architecture-and-contract.md` | The pieces, port, provider choice, registration, contract keys and server duties, payload layout per platform, taps, foreground policy, sign-out, tests, multi-package | Steps 1, 4, 5 |
| `references/platform-behaviour.md` | Permission, tokens, channels, delivery by app state, taps, badges and icons, Expo Go and simulators; pitfalls with fixes | Building; a push misbehaves |
| `references/setup-and-credentials.md` | Packages, plugin options, variants, credential steps a person does, contracts, store facts | Steps 2, 7 |
| `references/testing-push.md` | Jest recipes, simulator and emulator pushes, a real push in development, the device checklist, Maestro | Steps 8, 9 |
| `references/checker-rules.md` | Each check-push rule, when it applies, contract and config keys | Reading a check-push result |
| `templates/src/core/push/` | `push-message.ts` (kinds, schema, `parsePushData`), `push-destination.ts`, `foreground-presentation.ts`, `registration-plan.ts`, `push-registration.ts` (registration and registrar types), tests | Steps 3, 4 |
| `templates/src/services/push/` | `PushPort`, the expo-notifications adapter (+ iOS and Android tests), the fake, channels, registration service and sign-out step, the saved record (`PushRecordPort`, kv-store adapter, fake), opt-in, tap router, project id reader, the root kit `push-root-kit.tsx` and `push-context.tsx` (`usePushServices`), tests | Steps 3-5 |
| `templates/src/hooks/` | `use-push-sync.ts`, `use-push-taps.ts` (+ tests); `use-is-app-active.ts` (+ test, synced, react-components-and-hooks owns it) | Steps 3, 5 |
| `templates/src/i18n/catalogs/` | Channel names and descriptions in `en` and `ar` (merged into the app's catalogs) | Step 4 |
| `templates/contracts/` | `push.json` (the app's push facts, shared with the server) and its schema | Steps 3, 4 |
| `templates/src/core/result.ts` | Canonical Result type the templates import (synced; never edit here) | Only if the app lacks it |
| `templates/src/core/result.test.ts` | Its test (synced) | Only if the app lacks it |
| `templates/src/services/clock/clock-port.ts` | Canonical clock port (synced) | Only if the app lacks it |
| `templates/src/services/error-log/error-log-port.ts` | Canonical error log port (synced) | Only if the app lacks it |
| `templates/src/services/error-log/fake-error-log.ts` | Canonical fake error log (synced) | Only if the app lacks it |
| `templates/src/services/error-log/fake-error-log.test.ts` | Its test (synced) | Only if the app lacks it |
| `templates/test/flush-microtasks.ts` | Canonical test helper (synced) | Only if the app lacks it |
| `examples/create-app-push.ts` | The push parts of an app with accounts: the signed-in client, the adapter, the saved record and the registration, created before the session | Step 5 |
| `examples/create-root-kits.ts` | The root-kit registry with the push kit: the session as the account source, `openSettings`, the route table | Step 5 |
| `examples/push-registrar.ts` | The registrar over the signed-in ApiClient; the sign-out DELETE carries the step's access token (404 as done) | Step 5 |
| `examples/session-api-client.ts` | The signed-in client created before the session and attached by it (breaks the session/registration cycle) | Step 5 |
| `examples/push-destination-href.ts` | Destinations to typed routes | Step 5 |
| `examples/create-app-session.ts` | `pushRegistrationStep` in `serverSignOutSteps`; the session attached to the push parts' `signedInApi` | Step 5 |
| `examples/use-share-list-model.ts` | The in-context ask from a feature model through permissions-and-system-prompts' gate, then `optInToPush` | Step 6 |
| `examples/app.config.ts` | Plugin options, `googleServicesFile`, `extra.eas.projectId` | Step 2 |
| `examples/server/send-task-assigned.ts` | The server half: language, string data, channel, tickets and receipts | Step 7 |
| `examples/task-assigned.apns` | A simulator payload (`xcrun simctl push`), data under `body` | Step 9 |
| `scripts/check-push.mjs` | The checker (20 rules) | Step 8 and the definition of done |
| `scripts/lib/push-rules.mjs` | The checker's rules | Changing the checker |
| `scripts/lib/push-source.mjs` | Source loading, import and call helpers for the rules | Changing the checker |
| `scripts/check-lib.mjs` | Shared checker library (synced; never edit here) | Never by hand |
| `scripts/lib/source-scan.mjs` | Shared source scanner (synced; never edit here) | Never by hand |
| `scripts/selftest.mjs` | Proves the checker on planted bugs | After changing the checker |
| `tests/bases/app/` | The fixture base app, with planted findings in installed skills that must stay silent | The self-test reads it |
| `tests/fixtures/check-push/` | One overlay case per rule (good, bad-*, pass-*, error-*) on the base, templates and examples | The self-test reads them |
| `assets/shared.json` | Which shared files are synced into this skill | Maintenance |

## Related skills

- `local-notifications` - reminders scheduled on the device; they share the one foreground handler.
- `permissions-and-system-prompts` - the explanation before the prompt, denied versus blocked.
- `deep-links-and-universal-links` - links from outside; push taps reuse destinations, not URLs.
- `auth-and-secure-storage` - the server sign-out step that removes the registration.
- `networking-and-server-state` - the ApiClient the registrar uses.
- `architecture-and-boundaries` - ports, adapters, the composition root, `vendorSdks`.
- `app-variants-and-environment` - per-variant ids, `mode` and Firebase apps.
- `expo-prebuild-and-config-plugins` - the plugin and the native snapshot.
- `privacy-and-store-declarations` - the push token in App Privacy and Data safety.
- `i18n-strings-and-catalogs` - channel names in every language.
- `background-tasks` - data-only pushes and headless tasks.
- `unit-and-component-tests` - fakes, render helpers and mocks.
- `e2e-maestro` - flows for the opt-in and the screens a tap opens.
- `eas-build-and-submit` - the builds and credentials push needs.
