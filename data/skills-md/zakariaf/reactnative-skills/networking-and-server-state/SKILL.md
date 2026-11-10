---
name: networking-and-server-state
description: Builds TanStack Query server state over an ApiClient - validated responses, keys, retries, optimistic writes, offline. Use when calling an API, adding a query or mutation, or data is stale. Not for local data (persistence-and-migrations).
---

# Networking and server state

The app talks to its server through one typed `ApiClient` port whose only transport calls `fetch` with
a deadline, checks every response against a valibot schema and never rejects; server data lives in
TanStack Query's cache, defined once per resource in `src/api/`, read in model hooks, retried only when
a retry can help, kept fresh by React Native focus and connectivity, and honest about offline. A
zero-dependency checker proves it.

## Rules that must hold

1. **One network seam.** `fetch`, `XMLHttpRequest`, `WebSocket`, `EventSource` and `sendBeacon` appear
   only in `src/api/`, and `fetch` in exactly one file, `src/api/fetch-api-client.ts`; no HTTP client
   package (axios, ky, `expo/fetch` imports). `src/api/api-client.ts` exports `ApiClient`,
   `src/api/api-failure.ts` exports `ApiFailure`. Why: one place owns deadlines, validation, auth
   headers and the privacy inventory, and lint can ban the rest.
2. **The ApiClient never rejects.** `request()` returns `Result<T, ApiFailure>`: offline, timeouts,
   cancellation, HTTP errors and invalid bodies are typed values; every awaited `fetch` and body read
   sits inside one `try/catch`; a failure is classified by who aborted (the caller's signal, the
   client's own deadline) and by status, never by error text. Why: expo/fetch, React Native's fetch and
   Node's fetch word every error differently, and a rejection that escapes crashes a release handler.
3. **Every attempt has a deadline and honours the caller's signal.** The transport aborts each attempt
   after `timeoutMs` (default 15 s, body included), links TanStack's `signal`, and every `queryFn` passes
   `signal` to the request. Why: Android's OkHttp client has no timeouts, so a stalled request never
   ends; TanStack cancels an abandoned fetch only when the `queryFn` read the signal.
4. **Every response passes its schema, tolerantly.** Each request names a valibot `schema`; the
   transport `safeParse`s every 2xx body and records an invalid one once (method, path, issue paths,
   never the body); no `.json() as T`, no `.json()` or `JSON.parse` outside the transport; response
   schemas use `v.object` (never `v.strictObject`) and wrap closed sets in `v.fallback`. Why: a cast
   checks nothing, and a server that adds a field or an enum value must not break installed apps.
5. **The base URL comes from config, over HTTPS.** `EXPO_PUBLIC_API_URL` per EAS environment, read by
   the app's `src/config` reader and checked by `parseApiBaseUrl` (https outside development); no URL
   literal in `src/api/`, no `baseUrl: '<literal>'`, no `NSAllowsArbitraryLoads` or
   `usesCleartextTraffic` switch. Why: each variant talks to its own server, and release builds block
   cleartext on iOS (ATS) and Android 9+, so a global switch ships to the store.
6. **Queries and mutations are defined once, next to their keys.** Each resource has
   `src/api/<resource>/<resource>-keys.ts` (hierarchical, `all` root, `as const`),
   `-schemas.ts`, `-queries.ts` (`queryOptions`/`infiniteQueryOptions`) and `-mutations.ts`
   (`mutationOptions`); no inline key arrays, no `queryFn`/`mutationFn` or `.request({ method, path })`
   elsewhere. Why: one typo in an inline key misses an invalidation, and `queryOptions` ties the key to
   the data type for `getQueryData`/`setQueryData` without casts.
7. **Server state is read in the feature's model hook.** TanStack hooks appear only in
   `src/features/**/use-*.ts(x)`, `src/hooks/` and `src/api/`; views get plain props; query data is
   never copied into a store, `useState` or an effect (the house ESLint config catches the effect copy,
   not this checker). Why: two copies drift on every refetch, and the view stays testable without a
   client.
8. **One QueryClient per app run, with a failure-aware retry policy.** `createQueryClient` in
   `src/api/` is the only `new QueryClient` in app code, called once from AppRoot's `startApp` (a
   `useState` initializer, after the data layer and the error sink; never at module level or in a render body); queries retry only retryable failures
   (no connection, deadline, 408, 429 after `Retry-After`, 5xx), at most 3 times; mutations retry only
   with an `idempotencyKey`; never `retry: true`/`Infinity`/more than 3. Why: TanStack's default spins
   about seven seconds on a 404, and a retried POST without a key can create two tasks.
9. **Focus and online come from React Native, through one port.** `connectQueryManagers` feeds
   `focusManager` from AppState (`active` only) and `onlineManager` from the `ConnectivityPort`, whose
   one expo-network adapter (the only importer of expo-network or NetInfo) is created by the
   composition root; `QueryProvider` mounts the client and the wiring in the root providers. Online
   means `isConnected` alone; Android's `isInternetReachable` is only the `reachability()` hint for
   banners, ads and purchases. Why: React Native has no window events, so without it nothing pauses
   offline, resumes on reconnect or refetches on return; and Android marks some working networks
   unvalidated for good, where pausing on reachability would keep every request waiting forever.
10. **Every write says what it does to the cache; optimistic writes can roll back.** A mutation
    invalidates or sets the keys it changed in `onSuccess`/`onSettled`, or carries
    `// no-cache-effect: <why>`; an `onMutate` that writes the cache cancels in-flight queries first,
    snapshots, restores the snapshot in `onError` and invalidates in `onSettled`. Why: otherwise lists
    show old data, or a refused write stays on screen as if it happened.
11. **Offline pauses, it does not fail.** Keep `networkMode: 'online'` (a local-only query says
    `// network-mode-always: <why>`); show cached data with an offline notice, never an error in its
    place; a persisted cache sets `buster` and `maxAge`; writes that must survive a kill go to the
    outbox (persistence-and-migrations) and sync with their id as `idempotencyKey`. Why: paused work
    resumes by itself, and a restored cache in an old shape would skip every schema.
12. **Tests use the seams, never the network.** The transport gets a fake `FetchLike`; everything above
    it gets `createFakeApiClient()` from `test/api/`, which checks canned bodies through the request's
    schema and rejects unscripted requests; no test replaces the global `fetch` or mocks `expo/fetch`.
    Why: a replaced global leaks across tests and proves a seam the app never uses.
13. **The UI shows failures by kind.** Model hooks read `apiFailureOf(error)` and map each `kind`
    through one `Record<ApiFailureKind, MessageKey | null>` table; never `error.message`; `cancelled` is
    never shown and expected failures are never recorded. Why: a new kind is then a compile error until
    it has a message in every locale.

## Workflow

1. Decide whether the app has a server. An app with no network at all follows the `offline-only`
   profile of privacy-and-store-declarations instead (the checker prints NOT APPLICABLE there). Read
   [references/api-client-and-transport.md](references/api-client-and-transport.md).
2. Install (stack table, verified 2026-10-03): `npx expo install expo-network` and
   `npm install -E @tanstack/react-query@5.104.0 valibot@1.5.0`.
3. Copy `templates/src/api/` (with `tasks/`), `templates/src/config/api-base-url.ts` and its test,
   `templates/src/services/connectivity/`, and `templates/test/api/`. The synced files
   (`src/core/result.ts`, `src/config/app-variant.ts`, `src/services/error-log/*`,
   `test/flush-microtasks.ts`) come from their owner skills: copy them only if the app lacks them.
4. Environment: declare `EXPO_PUBLIC_API_URL` in `src/env.d.ts` and read it in the app's
   `src/config/environment.ts` as `examples/environment.ts` shows. Setting the value in each EAS
   environment (`eas env:set --name EXPO_PUBLIC_API_URL --value <https-url> --environment <env>
   --visibility plaintext`) is the developer's step: stop and ask before running it.
5. Composition root: add `api` and `connectivity` to `Services`, `createDeviceServices` and
   `createTestServices` as in `examples/composition-root/`.
6. Startup: read the checked environment in the root layout's `decideStartup`
   (`examples/root-layout.tsx`), create the client in AppRoot's `startApp` right after the error sink,
   and render `QueryProvider` right after `AppDataProvider` inside `AppProviders`
   (`examples/app-root.tsx`, `examples/app-providers.tsx`; app-startup-and-bootstrap owns the order).
7. Each resource: replace the Tasks keys, schemas, queries and mutations with the app's own, reading
   [references/schemas-and-failures.md](references/schemas-and-failures.md),
   [references/queries-and-cache.md](references/queries-and-cache.md) and
   [references/mutations-and-optimistic-updates.md](references/mutations-and-optimistic-updates.md).
   Paged lists: `examples/task-pages.ts`.
8. Model hooks: read server state as `examples/use-tasks-model.ts` does, turn query state into a view
   state (`examples/task-list-state.ts`) and failures into message keys
   (`examples/api-failure-message.ts`; add the keys to every catalog with i18n-strings-and-catalogs).
9. Offline needs (a persisted cache, an outbox, sign-out clearing): read
   [references/online-focus-and-offline.md](references/online-focus-and-offline.md).
10. Tests: follow [references/testing-server-state.md](references/testing-server-state.md); run
    `npx jest src/api src/config src/services/connectivity test/api --ci` and `npm run typecheck`.
11. Run `node ${CLAUDE_SKILL_DIR}/scripts/check-server-state.mjs .` from the repo root; fix each `FAIL`
    line (rule ids in [references/checker-rules.md](references/checker-rules.md)) and rerun until
    `RESULT: PASS`.

## Definition of done

- [ ] `fetch` appears only in `src/api/fetch-api-client.ts`; no other network API outside `src/api/`; no HTTP client package.
- [ ] `request()` never rejects: fetch and the body read sit in one `try/catch`; each attempt has a deadline linked to the caller's signal; every `queryFn` passes `signal`.
- [ ] Every request names a schema; invalid bodies are recorded once without the data; response schemas are tolerant (`v.object`, `v.fallback` around closed sets).
- [ ] The base URL comes from `parseApiBaseUrl(process.env.EXPO_PUBLIC_API_URL, variant)` in `src/config`; each EAS environment has its HTTPS value (or the report says the developer still has to set it); no cleartext switch.
- [ ] Each resource has keys, schemas, `queryOptions` and `mutationOptions` factories in `src/api/<resource>/`, each with its test against the fake ApiClient.
- [ ] TanStack hooks only in model hooks; one client from `createQueryClient` in AppRoot's `startApp` (a `useState` initializer); `QueryProvider` mounted right after `AppDataProvider`.
- [ ] Every mutation has a cache effect (or a reasoned `no-cache-effect` marker); optimistic ones cancel, snapshot, roll back and invalidate; retrying writes send an idempotency key.
- [ ] `npx jest src/api src/config src/services/connectivity test/api --ci` passes and `npm run typecheck` is clean; the device checks of testing-server-state.md section 9 ran, or the report says they are owed.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-server-state.mjs .` prints `RESULT: PASS`. Expected only before the root layout exists: `SKIP src/app/_layout.tsx [managers-wired] not yet created (navigation-and-routing creates it)`. An app without a server prints `NOT APPLICABLE: no app code imports @tanstack/react-query or calls the network, and there is no src/api/`.

## Anti-patterns

- **`fetch` in a hook or a screen "just for this one call".** No deadline, no schema, no auth header,
  no fake in tests; add a query factory in `src/api/<resource>/`.
- **`await response.json() as Task[]`.** Nothing is checked; the first server change crashes a screen
  far from the cause. Pass a schema.
- **Deciding offline from `error.message === 'Network request failed'`.** That text exists only in
  React Native's fetch; expo/fetch says `fetch failed: ...`. Ask the signal, the deadline flag and the
  ConnectivityPort.
- **`new QueryClient()` at module level or in the layout body.** It outlives logout and is shared by
  every test, or it is a new empty cache on every render. Create it in a `useState` initializer.
- **`retry: 3` on a mutation, or keeping TanStack's default retry for queries.** Duplicate writes;
  seven seconds of spinner before a 404 shows.
- **`queryKey: ['task', id]` typed inline.** One letter off from `['tasks']`, and the invalidation
  misses it. Use the key factory.
- **Copying `query.data` into a Zustand store or `useState` "to edit it".** Two copies drift; edit a
  draft keyed by id, and write through a mutation.
- **NetInfo or `expo-network` subscribed in a screen or in the onlineManager wiring.** A second native
  subscription, and on iOS the module's single monitor can be cancelled for good. Read the
  ConnectivityPort.
- **Feeding onlineManager from `isInternetReachable`.** On an Android network that never validates
  (a firewall blocking the probe, "use this network anyway") every query stays paused forever while
  requests would succeed. Feed it `isOnline()`; show `reachability()` in a banner.
- **An optimistic update without `cancelQueries` or a rollback.** The value flickers back, or a refused
  write stays on screen.
- **`usesCleartextTraffic: true` to make a preview build reach `http://10.0.2.2`.** It ships to the
  store; give the API an HTTPS endpoint per environment.
- **`jest.spyOn(globalThis, 'fetch')`.** Leaks into other tests; pass a fake `FetchLike` or the fake
  ApiClient.
- **Persisting the query cache without `buster` and `maxAge`.** Restored data in an old shape skips
  every schema, and data of any age reappears.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/api-client-and-transport.md](references/api-client-and-transport.md) | The port, what `fetch` is on iOS and Android in SDK 57, deadlines, cancellation, failure classification, URLs and headers, idempotency, base URL and cleartext per platform, HTTP cache and cookies, verified facts | Workflow steps 1-4 |
| [references/schemas-and-failures.md](references/schemas-and-failures.md) | One schema per response, tolerant reading, transforms, recording invalid responses, the failure family and who handles each kind, `unwrap`/`apiFailureOf` | Workflow steps 7-8 |
| [references/queries-and-cache.md](references/queries-and-cache.md) | TanStack defaults, `queryOptions`, key factories, the retry policy, freshness, stacked screens and `subscribed`, status vs fetchStatus, dependent, paged and prefetched queries | Workflow steps 7-8 |
| [references/mutations-and-optimistic-updates.md](references/mutations-and-optimistic-updates.md) | `mutationOptions`, choosing a cache effect, the four optimistic steps, UI-only optimism, concurrent writes, idempotency, conflicts, calling mutations, 5.104 callback signatures | Workflow step 7 |
| [references/online-focus-and-offline.md](references/online-focus-and-offline.md) | Why React Native needs manager wiring, the ConnectivityPort on iOS and Android, AppState focus, paused queries and mutations, offline UI, the persisted cache, the outbox split, sign-out | Workflow steps 6 and 9 |
| [references/testing-server-state.md](references/testing-server-state.md) | The seam per layer, transport, factory, hook, manager and optimistic tests, timing without fake timers, device checks | Workflow step 10 |
| [references/checker-rules.md](references/checker-rules.md) | Every rule id, its scope, the two markers, layout keys, monorepo use, known limits | Workflow step 11, on a FAIL |
| `templates/src/api/` | `api-client.ts`, `api-failure.ts`, `api-error.ts`, `build-url.ts`, `to-api-failure.ts`, `fetch-api-client.ts`, `api-query-options.ts`, `create-query-client.ts`, `query-managers.ts`, `query-provider.tsx`, and their tests; `tasks/` holds the Tasks resource (keys, schemas, queries, mutations with an optimistic toggle and an idempotent create, with tests) | Workflow steps 3 and 7 |
| `templates/src/config/` | `api-base-url.ts` (`parseApiBaseUrl`, the checked base URL per variant) and its test; `app-variant.ts` and its test are synced from app-variants-and-environment (do not edit here) | Workflow steps 3-4 |
| `templates/src/services/connectivity/` | The `ConnectivityPort` (`isOnline` plus the `reachability` hint), its expo-network adapter, the shared `reachability-hub.ts` fan-out and the fake, with tests (this skill owns them; synced from the library, do not edit here) | Workflow step 3 |
| `templates/src/services/error-log/` | The error log port and fake with its test, synced from architecture-and-boundaries (do not edit here) | Workflow step 3, only if the app lacks them |
| `templates/src/core/` | `result.ts` and its test, synced from error-handling-typed-results (do not edit here) | Workflow step 3, only if the app lacks them |
| `templates/test/` | `api/fake-api-client.ts`, the scripted ApiClient for tests, and its test; `flush-microtasks.ts`, synced from unit-and-component-tests (do not edit here) | Workflow steps 3 and 10 |
| `examples/environment.ts` | The app's public-environment reader with the API base URL | Workflow step 4 |
| `examples/composition-root/` | `Services`, `createDeviceServices`, `createTestServices` with the `api` and `connectivity` ports, and a test | Workflow step 5 |
| `examples/root-layout.tsx` | The canonical root layout reading the checked environment in `decideStartup` | Workflow step 6 |
| `examples/app-root.tsx` | The canonical AppRoot creating the QueryClient once in `startApp` | Workflow step 6 |
| `examples/app-providers.tsx` | AppRoot's outer providers with `QueryProvider` right after `AppDataProvider` | Workflow step 6 |
| `examples/task-pages.ts` | A paged list with `infiniteQueryOptions` and a cursor | Workflow step 7 |
| `examples/use-tasks-model.ts` | A model hook over server state (`subscribed: isFocused`, an optimistic toggle) | Workflow step 8 |
| `examples/use-tasks-model.test.tsx` | Testing that hook in a route with the fake ApiClient, offline included | Workflow steps 8 and 10 |
| `examples/task-list-state.ts` | TanStack's status and fetchStatus turned into one view state | Workflow step 8 |
| `examples/api-failure-message.ts` | The message table of the ApiFailure family, with the catalog strings | Workflow step 8 |
| `scripts/check-server-state.mjs` | The checker (21 rules; options `--src-dir`, `--api-dir`, `--json`) | Workflow step 11, and at the end |
| `scripts/lib/` | The checker's rule sets and source model, and the synced `source-scan.mjs` (do not edit that one here) | Never by hand |
| `scripts/check-lib.mjs` | Shared script helper, synced from the library (do not edit here) | Never by hand |
| `scripts/selftest.mjs` | Proves the checker passes the templates and examples and catches every planted bug | After changing the checker, a template or an example |
| `assets/shared.json` | Declares the shared files this skill copies in | When adding a shared file |
| `tests/` | The overlay base app (with planted findings in installed-skill folders that must stay silent) and one fixture per rule, plus pass and error cases | When adding a checker rule |

## Related skills

- `error-handling-typed-results` - the Result type, failure families, the error net; the ApiClient is one of its boundaries.
- `architecture-and-boundaries` - ports, adapters and the composition root the ApiClient and ConnectivityPort join.
- `app-variants-and-environment` - `EXPO_PUBLIC_*` readers and EAS environments.
- `state-management-zustand` - client state; no server data in stores (its `server-state-in-store` check).
- `persistence-and-migrations` - local tables, the outbox and the kv-store adapter under a persisted cache.
- `auth-and-secure-storage` - tokens, the `headers()` hook and sign-out.
- `async-safety` - effects, listeners and cancellation outside TanStack Query.
- `ui-states-and-feedback` - loading, offline and error states on screen.
- `forms-and-input` - server validation codes mapped to fields.
- `unit-and-component-tests` - the test app, render helpers and test forms.
- `privacy-and-store-declarations` - the network inventory and the `offline-only` profile.
- `admob-ads-and-consent`, `in-app-purchases` - other consumers of the ConnectivityPort.
- `background-tasks` - syncing the outbox while the app is closed.
- Expo's official `expo-data-fetching` skill - the Expo fetch API reference.
