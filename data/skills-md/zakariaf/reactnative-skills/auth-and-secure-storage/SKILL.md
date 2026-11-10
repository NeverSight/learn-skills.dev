---
name: auth-and-secure-storage
description: Builds sign-in - tokens in expo-secure-store, shared refresh, protected routes, OAuth PKCE, Apple sign-in. Use when adding login, tokens, 401 retries, logout or account deletion. Not for API calls (networking-and-server-state).
---

# Auth and secure storage

Makes sign-in safe and complete on iOS and Android: tokens live only in the Keychain or Keystore behind
one port, one session manager restores, refreshes and ends the session without races, route groups open
and close with it, OAuth runs the code flow with PKCE, Sign in with Apple uses a nonce, and sign-out
leaves nothing of the last person behind. A zero-dependency checker proves the structure; Jest tests
prove the behaviour.

## Rules that must hold

1. **Tokens live only in expo-secure-store, behind `SecureStoragePort`.** One adapter imports the SDK
   and passes one frozen options object (`keychainAccessible: AFTER_FIRST_UNLOCK_THIS_DEVICE_ONLY`) to
   every async call; never `getItem`/`setItem`, never `ALWAYS`, no `requireAuthentication` on session
   tokens. Why: a read with other options finds nothing; `WHEN_UNLOCKED` breaks background refresh;
   biometrics prompt on every Android read and a new fingerprint signs people out.
   (`vendor-import`, `secure-store-call`)
2. **A credential appears nowhere else.** Not in SQLite, kv-store, AsyncStorage, MMKV or files, not in a
   Zustand store (not even a bare `token` field), not in a log, crash report or analytics event, not in
   a TanStack mutation (its cache keeps variables and data), not in a URL, never in `EXPO_PUBLIC_*`.
   Why: none of those is encrypted with a hardware key, and logs, backups and URLs travel.
   (`token-storage`, `token-in-state`, `token-in-log`, `token-in-url`; these four run in every app)
3. **Every secret key is declared once in `SECURE_KEYS`; wipes loop over `ALL_SECURE_KEYS`.** Why: a
   key typed by hand somewhere survives sign-out and the fresh-install wipe. (`secure-keys`)
4. **A fresh install wipes what the Keychain kept.** An install marker in the app sandbox
   (kv-store) is checked at restore: missing means wipe every key, then mark; unreadable means never
   wipe. Why: the iOS Keychain outlives an uninstall, so a reinstall would sign the previous person
   back in. (`fresh-install-wipe`)
5. **Restore never guesses, and never waits forever.** A read that fails in the background publishes
   `unavailable` and is retried in the foreground; one that fails in the foreground (read twice) signs
   out with reason `storage-unavailable` and keeps the values; an unreadable session signs out but is
   kept. The restore is app-startup-and-bootstrap's blocking startup-gate task `restoreSessionTask`
   under its `deadlineMs` (that skill owns the one splash hold and release; auth calls no
   `SplashScreen` function); a miss opens only a "checking your session" route, never a `null` frame.
   Why: a locked phone or a parser bug must not destroy a valid session, and a broken Keystore must not
   keep the app checking so long that the person can never reach sign-in. (session-manager,
   session-context and session-guards tests)
6. **Persist, then publish; a sign-out always wins.** Sign-in writes the refresh token first, then the
   rest, and only then publishes `signed-in`; every write and wipe runs through one queue, and a
   generation number drops work started before a sign-out. Why: the reverse order shows the app and
   loses the session at the next launch; a late refresh would sign a signed-out person back in.
   (session-manager tests)
7. **One token issuer, one refresh at a time, owned by the session manager.** Every sign-in method
   ends in tokens from the issuer whose `TokenRefresher` the session holds: with an app server (Apple
   needs one) each method is exchanged there and the refresher is `createServerTokenRefresher`; the
   OAuth refresher only when OAuth is the sole method and there is no server. Callers share the
   in-flight refresh; only the session manager calls the refresher. Why: a refresh token sent to the
   wrong issuer answers `invalid_grant` one token lifetime later, and two refreshes with a rotating
   refresh token look like a replay that revokes every session. (`single-flight-refresh`, tests)
8. **Only the server ends a session.** `invalid_grant` or another OAuth error ends it; no connection,
   a timeout or 5xx keep it, and an unexpired token still goes out offline; a 401 renews once
   (`sendWithSession`), a second 401 signs out. Why: a train tunnel must never sign anyone out.
   (token-set and send-with-session tests)
9. **Protected groups are guards, not navigation.** Each signed-in group has its own `_layout` and
   sits inside `<Stack.Protected guard={isSignedIn}>`; signed-out routes sit inside
   `guard={isSignedOut}`; flows switch by changing the session, never with `router.replace`; no
   `redirectTo` before SDK 58. Why: without the group layout the guard protects none of its screens
   (verified), and a deep link opens them signed out. (`protected-groups`, session-guards test)
10. **Sign-out clears everything, in two phases.** First, on `signOut('user')`, the
    `serverSignOutSteps` (push unregistration, server logout) run with the still-valid token under one
    5 s deadline; then wipe every key, publish `signed-out` (protected screens leave), run every
    `signOutSteps` entry (query cache, account stores, rows, reminders) even when one fails, and revoke
    the refresh token best effort. Both lists are named in `contracts/auth.json`. Why: a cache nobody
    cleared shows the next person this person's data, and a push registration nobody removed sends
    them this person's notifications; after the wipe no server call can be authorized. (`sign-out-steps`)
11. **OAuth is the authorization code flow with PKCE (S256) in an ephemeral system browser.** No
    implicit flow, no WebView, no client secret, the `code_verifier` passed to `exchangeCodeAsync`
    (expo-auth-session does not add it). Why: anything else leaks tokens or codes, and a shared browser
    cookie signs the last person straight back in. (`oauth-pkce`, `oauth-ephemeral`)
12. **Sign in with Apple is iOS-only, configured, and nonced.** `usesAppleSignIn` (or the plugin), a
    fresh nonce hashed with SHA-256, `ERR_REQUEST_CANCELED` silent, the credential verified by the
    app's server, the name and email saved on the first sign-in, a revoked credential signing out,
    Apple's own button. Offer it (or an equal private login) whenever a third-party login sets up the
    account (App Store guideline 4.8). (`apple-sign-in`)
13. **Android backups leave the secure store out.** `['expo-secure-store', { faceIDPermission: false }]`
    in `app.config.ts`, or the app's own rules named in the contract. Why: prebuild does not apply this
    plugin by itself, and a restored copy cannot be decrypted on the new phone. (`secure-store-plugin`)
14. **An app that creates accounts deletes them inside the app.** A route in the signed-in group, the
    server deletes (and revokes Apple tokens), then `signOut('account-deleted')`. Why: App Store
    guideline 5.1.1(v) and Google Play (which also wants a web link) require it. (`account-deletion`)

## Workflow

1. Read `references/session-lifecycle.md` (the states, races and sign-out order) and
   `references/secure-storage.md` (platform behaviour). For the provider read
   `references/oauth-and-apple.md`; for routes `references/protected-routes.md`.
2. Install the packages and edit `app.config.ts` (`references/adopting-in-an-app.md` sections 1-2):
   the expo-secure-store plugin with `faceIDPermission: false`, Apple's plugin, a scheme per variant.
3. Copy every file under `templates/` to the path its first line names, tests included; the contract
   and schema land in `contracts/`.
4. Add the four ports to the composition root and its test, and record the SDKs in
   `contracts/architecture.json` (`examples/create-device-services.ts`, `examples/services-context.tsx`,
   adopting-in-an-app.md sections 4-5).
5. Read the provider settings in `src/config/oauth-config.ts` (`examples/oauth-config.ts`); register
   `<scheme>://oauth-redirect` for each variant with the provider (Google refuses custom schemes on
   Android: `references/oauth-and-apple.md` section 3). Stop and ask the developer for the
   issuer, client id and Apple team setup: they are outward-facing accounts.
6. Pick the one token issuer (rule 7): with a server, every method exchanges there and the session gets
   `examples/server-refresher.ts`. Create the session once (`examples/create-app-session.ts`) in
   `AppRoot`, render `SessionProvider` in
   `RootStack` (`examples/root-stack.tsx`), and guard the Stack (`examples/app-stack.tsx`); give each
   protected group its own `_layout.tsx`.
7. Build sign-in as a feature: `examples/use-sign-in-model.ts`, `examples/sign-in-screen.tsx`,
   `examples/sign-in-route.tsx`, the Android redirect route (`examples/oauth-redirect-route.tsx`,
   `examples/use-oauth-redirect.ts`), and on iOS `examples/use-apple-sign-in.ts` over
   `examples/auth-mutations.ts`.
8. Send requests to the app's server through `examples/authorized-api-client.ts` (`sessionHeaders` and
   `sendWithSession`), pass every per-account cache as a sign-out step and every server call that needs
   the session (push unregistration) as a server sign-out step; list both in `contracts/auth.json`.
9. When the app creates accounts, build deletion (`examples/use-delete-account-model.ts`) and name the
   route in the contract. Test it against a staging server only, never production.
10. Write a test for every example you adopted (`createSessionTestKit` keeps them short), and a router
    test for the app's own AppStack (from `session-guards.test.tsx`: a signed-out deep link lands on
    sign-in; the checker cannot see a guard bound to the wrong boolean), run
    `npx jest --ci` (the templates' tests cover rules 5-8, 10 and 9's behaviour), then the checker:
    `node ${CLAUDE_SKILL_DIR}/scripts/check-auth.mjs .`; fix and rerun until `RESULT: PASS`. Look up a
    rule in `references/checker-rules.md`.
11. Hand the device checklist (`references/oauth-and-apple.md` section 9) to a human for one named iOS
    device and one named Android device before release.

## Definition of done

- [ ] Tokens only behind `SecureStoragePort`; one adapter, one frozen options object.
- [ ] No credential in plain storage, stores, logs, URLs or `EXPO_PUBLIC_*`.
- [ ] Fresh-install wipe; `unavailable` in the background, `storage-unavailable` after two failed
  foreground reads (values kept); the restore is the startup gate's blocking task, and a miss shows the
  checking-session route (no `SplashScreen` call in auth code, no `null` frame).
- [ ] Sign-in persists before it publishes; a sign-out during sign-in or refresh wins (tests pass).
- [ ] One token issuer per session (every sign-in method ends at the refresher's issuer); one shared
  refresh in the session manager; a 401 renews once, then signs out.
- [ ] Every protected group has its own `_layout` and a guard; no `router.replace` after sign-in/out.
- [ ] Every per-account cache is a sign-out step, every server call that needs the session a server
  sign-out step, both listed in `contracts/auth.json`.
- [ ] OAuth: code + PKCE S256, ephemeral, verifier on exchange, no client secret; redirect per variant.
- [ ] Sign in with Apple configured with a nonce and a silent cancel (when offered).
- [ ] expo-secure-store plugin listed; account deletion route when accounts are created.
- [ ] `npx jest --ci` passes, including `session-guards.test.tsx` and a test per adopted example.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-auth.mjs .` prints `RESULT: PASS` (no SKIP lines exist;
  `NOT APPLICABLE` only while no app file imports an auth package, no contract exists and no
  credential leaks; an app with secrets but no sign-in writes `{ "signIn": false }` and passes the
  storage rules, `references/secure-storage.md` section 7).

## Anti-patterns

- **Publishing the session before the write** (Expo's sample `useStorageState` sets state, then writes
  without awaiting). The UI shows the app; a failed write signs the person out next launch.
- **`router.replace('/')` after `signIn()`.** The guard already navigates; a second navigation races it.
- **A guard around a group without its own `_layout`.** It protects nothing and Expo Router says
  nothing.
- **Refreshing in an Axios-style interceptor per request.** Ten 401s, ten refreshes, a revoked token
  family. Share one refresh in the session manager; a server refresh endpoint is a `TokenRefresher`.
- **Wiping, then calling the server at sign-out.** The push unregister goes out signed out and fails
  silently; make it a server sign-out step.
- **Waiting for a Keystore that stays broken.** `unavailable` forever is a checking screen forever.
- **Hiding the splash from `AppStack` when `isRestoring` ends, or returning `null` while restoring.**
  The hold and release are app-startup-and-bootstrap's; once its gate opened, `null` is a blank frame.
  Make the restore a gate task and render the guarded checking-session route.
- **Signing out on any refresh error.** Offline is not expired; only `invalid_grant` ends a session.
- **Wiping the session on a read error.** A locked keychain is not an empty one.
- **Clearing only the tokens at sign-out.** The query cache and account stores still show the last
  person's data; make each one a step.
- **Tokens in a Zustand `persist` store or kv-store "for speed".** Plain files, in backups.
- **Sign-in exchanges through `useMutation`.** The MutationCache keeps the credential and the tokens.
- **A client secret in `app.config.ts` or `EXPO_PUBLIC_*`.** Public the moment the app ships.
- **Trusting the id token on the device.** Read its claims for display; the server verifies.
- **Calling Apple's `signOutAsync` to sign out.** It shows Apple's sheet; clear the app's session.
- **A hand-drawn Apple button.** It must follow Apple's branding rules; use Apple's own through the port.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| `references/session-lifecycle.md` | States, restore, persist-then-publish, single-flight refresh, 401s, sign-out order, races, startup order, test recipes | Before building or changing the session |
| `references/secure-storage.md` | Keychain and Keystore behaviour, options, keys, uninstall, backups, biometrics, verified facts | Storing any secret; a secret is lost or survives |
| `references/oauth-and-apple.md` | Code + PKCE with expo-auth-session 57, redirects, errors, id tokens, Sign in with Apple, guidelines 4.8 and 5.1.1(v), Google Play deletion, device checklist | Adding a provider or Apple; before release |
| `references/protected-routes.md` | Stack.Protected behaviour (verified), the group-layout pitfall, the checking-session route while restoring, SDK 57 limits | Guarding routes |
| `references/adopting-in-an-app.md` | Every edit to adopt the templates, as verified on the reference app | Workflow steps 2-9 |
| `references/checker-rules.md` | Each check-auth rule, the contract keys, config keys | Reading a check-auth result |
| `templates/src/core/session/` | `token-set.ts` (tokens, expiry, which failures end a session, meta schema), `id-token-claims.ts` (unverified display claims), tests | Step 3 |
| `templates/src/services/secure-storage/` | `SecureStoragePort`, the expo-secure-store adapter, `SECURE_KEYS`, the fake, tests | Step 3 |
| `templates/src/services/install-marker/` | `InstallMarkerPort`, the kv-store adapter, the fake, tests | Step 3 |
| `templates/src/services/oauth/` | `OauthPort` and `OauthConfig`, the expo-auth-session adapter (PKCE, ephemeral, timeouts), the fake, tests | Step 3 |
| `templates/src/services/apple-sign-in/` | `AppleSignInPort` (with Apple's button), the expo-apple-authentication adapter (nonce), the fake, tests | Step 3 |
| `templates/src/services/session/` | The session manager and its machine (state, queue, generation), types, vault, single-flight, the server `TokenRefresher` (`createServerTokenRefresher`), server and local sign-out steps and factories, `sendWithSession`/`sessionHeaders`, `SessionProvider` and hooks, guards with the router test | Step 3 |
| `templates/test/session/` | `createSessionTestKit`: a real session over fakes, for screen and route tests | Testing code that uses a session |
| `templates/contracts/` | `auth.json` (the app's sign-in facts) and its schema | Step 3, then fill in |
| `examples/` | Verified adoption shapes: composition root, `Services`, config, session creation with the server refresher (`server-refresher.ts`), root stack, guarded Stack, sign-in feature (id token exchanged at the server), redirect route, Apple flow, auth exchanges, authorized ApiClient, account deletion | Steps 4-9 |
| `scripts/check-auth.mjs` | The checker (17 rules; storage rules only with `"signIn": false`) | Step 10 and the definition of done |
| `scripts/lib/auth-rules.mjs` | The checker's rules | Changing the checker |
| `scripts/lib/auth-source.mjs` | Source loading and text helpers for the rules | Changing the checker |
| `scripts/check-lib.mjs` | Shared checker library (synced; never edit here) | Never by hand |
| `scripts/lib/source-scan.mjs` | Shared source scanner (synced; never edit here) | Never by hand |
| `scripts/selftest.mjs` | Proves the checker on planted bugs | After changing the checker |
| `tests/bases/app/` | The fixture base app, with planted installed-skill findings that must stay silent | The self-test reads it |
| `tests/fixtures/check-auth/` | One overlay case per rule (good, bad-*, pass-*, error-*) on the base, templates and examples | The self-test reads them |
| `assets/shared.json` | Which shared libraries are synced into this skill | Maintenance |

## Related skills

- `networking-and-server-state` - the ApiClient, mutations and the query cache sign-out clears.
- `state-management-zustand` - an account store holding only non-secret facts.
- `architecture-and-boundaries` - the composition root and the SDK lists.
- `navigation-and-routing` - the navigator tree the guards sit in.
- `app-startup-and-bootstrap` - the startup order and the splash screen.
- `app-variants-and-environment` - schemes and `EXPO_PUBLIC_*` per variant.
- `expo-prebuild-and-config-plugins` - the native snapshot after adding the plugins.
- `push-notifications` - the push registration a server sign-out step removes.
- `error-handling-typed-results` - Result failures and recording.
- `async-safety` - deadlines and effects that own their work.
- `privacy-and-store-declarations` - data-safety answers and export compliance.
- `unit-and-component-tests` - the router test helper and test conventions.
