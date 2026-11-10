---
name: async-safety
description: "Prevents silent async bugs: effect races, stale results, lost promises, leaked listeners and timers, AbortSignal gaps. Use when writing useEffect, setTimeout, listeners or cancellation. Not for query caching (networking-and-server-state)."
---

# Async safety

No async failure in an Expo app is silent and no async result lands where it no longer belongs: every
promise has an owner that sees its rejection, every effect cancels the work it started, overlapping
calls resolve latest-wins, cancellation is read from the signal (with only the abort APIs a phone
really has), every subscription and timer is released by whoever created it, and every wait has a
deadline. A zero-dependency checker proves the parts ESLint and `tsc` cannot see, on iOS and Android
code alike; race tests prove the rest.

## Rules that must hold

The inline handler forms (no floating promise, no `async` handler, block-bodied handlers) are
typescript-and-lint-rules rule 10 and its ESLint config; these rules close everything after them.
Server data is read with `useQuery` (networking-and-server-state): no effect, no
`createLatestRequest`, because query keys already give latest-wins and TanStack passes the signal.
Rules 3 and 4 are for async work that is not server state: SQLite repositories, native SDKs, OS
reads, device APIs.

1. **No promise goes into a slot that ignores it.** A promise-returning function (an `async` function,
   one typed `Promise<...>`, an `*Async` call, `Linking.openURL`) never goes by reference into an `on*`
   prop, an `on*` model field or a listener: wrap it, `onPress={() => { retry().catch(reportError); }}`.
   Why: React Native's Strict API types `Pressable` `onPress`, `TextInput` `onSubmitEditing` and
   `Keyboard` listeners as returning `unknown`, and `RefreshControl` `onRefresh` accepts a Promise it
   never awaits, so no linter sees `onPress={retry}` (verified) and the rejection vanishes in
   release. (`async-by-reference`)
2. **Callback types return `void`.** Every `on*` prop, `on*` model field and `handle*` member is typed
   `(...) => void`, never `Promise<...>` or `unknown`; the model owns the promise and exposes a void
   intent plus its state (`isSaving`). Why: with `void`, `no-misused-promises` reports every async
   function passed in, so the type does the review at each call site. (`void-callback-type`)
3. **An effect owns the async work it starts.** One `AbortController` per run (or an `isActive` flag
   for work that takes no signal), aborted by the cleanup; every write after an await checks
   `signal.aborted` first; a subscription that arrives asynchronously (`watchPositionAsync`) is removed
   on arrival when the cleanup already ran; state remembers which request it answers. Why: answers
   arrive out of order, and a response for the previous id or a left screen otherwise overwrites,
   navigates or leaks. (`effect-stale-result`)
4. **Overlapping calls of one read resolve latest-wins; writes never run twice.** Search, filters
   and refresh over local or SDK data, and the first read of an OS value, use one
   `createLatestRequest()` per action, so a newer call (or a change event) aborts the older one; a
   write is never aborted for a newer one and is disabled while in flight. Why: the last answer to arrive is not the last one asked for, and an
   aborted write may still have landed. (race tests, `templates/src/core/async/latest-request.ts`)
5. **Cancellation is read from the signal and is never a failure.** After a rejection ask
   `signal.aborted`, never `error.name === 'AbortError'` or `instanceof DOMException`; a cancelled call
   shows nothing and records nothing; use only `abort()`, `aborted` and hand-removed listeners. Why:
   on a device expo/fetch rejects most aborted requests with a `FetchError`, and React Native's
   AbortSignal polyfill has no `throwIfAborted()` or `AbortSignal.abort()`, drops the reason passed to
   `abort(reason)` and ignores `{ signal }` listener options, while Jest on Node has them all.
   (`abort-signal`)
6. **Every subscription handle is kept and released by its creator.** The value of `addEventListener`,
   `addListener`, `add*Listener`, `subscribe` and `watch*()` is stored and removed in the matching
   cleanup, a `useSyncExternalStore` subscribe's return or a `stop()`; never `removeAllListeners` on a
   shared emitter; only a composition-root listener that lives as long as the app may say
   `// app-lifetime: <why>` instead. Why: a leaked listener fires after unmount, Fast Refresh stacks
   copies, and a leaked Android back handler swallows every later back press. (`subscription-released`)
7. **Every timer id is kept and cleared; pauses are abortable.** `setTimeout`, `setInterval`,
   `requestAnimationFrame` and `requestIdleCallback` ids go to their clear function in the cleanup,
   `finally` or `stop()`; a pause is `await delayOrAbort(ms, signal)`, never
   `new Promise((resolve) => setTimeout(resolve, ms))`. Why: a timer outlives its owner and acts on
   state nobody shows; an uncancellable sleep keeps a retry loop alive after its screen is gone.
   (`timer-cleared`)
8. **Screen work runs only while the screen is focused and the app is active.** Polling, countdowns,
   sensors and location in a screen run in `useFocusEffect` and pause while `useIsAppActive()` is
   false. Server polling is `useQuery({ refetchInterval, subscribed: useIsFocused() })`, never a
   hand-rolled interval. Why: covered stack screens and inactive tabs stay mounted with their effects
   (and query observers) running, and Android keeps JS running in the background where iOS suspends
   it. (`focus-scoped-work`)
9. **Every wait that can hang has a deadline that cancels what it abandons.** `withTimeout(task,
   afterMs, signal)` returns `timed-out` or `cancelled` as Result failures and aborts the task's
   signal; retries are bounded, back off through `delayOrAbort` and retry only retryable kinds;
   server-state retries stay with TanStack Query. Why: a hung request keeps the spinner forever, and a
   timed-out request left running writes later. (race tests, `templates/src/services/async/with-timeout.ts`)
10. **Every async unit has a race test.** Answers settled out of order, unmount in the middle, a
    cancelled call that records nothing, and nothing left behind (`jest.getTimerCount()` 0, a fake's
    listener count back to 0). Why: every test that resolves promises in start order passes the race
    bugs this skill exists for.

## Workflow

1. **Classify the change**: a handler or callback type (rules 1-2), an effect (3), overlapping calls
   or an OS mirror (4), cancellation (5), a listener or timer (6-7), screen-scoped work (8), a wait or
   retry (9). Read [references/silent-failure-catalogue.md](references/silent-failure-catalogue.md)
   once to see the whole list.
2. **Add the async toolkit when first needed**, each with its test, at the path its first line names:
   `templates/src/core/async/latest-request.ts`, `templates/src/services/async/delay-or-abort.ts`,
   `templates/src/services/async/with-timeout.ts` (it imports `src/core/result.ts`, which
   error-handling-typed-results creates). Copy them as they are; they pass tsc, ESLint and Jest in the
   reference app. An existing `with-timeout.ts` that takes a promise (`withTimeout(sdk.fetch(), 8000)`)
   is replaced: rewrite its call sites to the task form first
   ([references/cancellation-and-deadlines.md](references/cancellation-and-deadlines.md), section 6).
3. **Handlers and callback types**: read
   [references/promises-and-handlers.md](references/promises-and-handlers.md). Type every `on*` member
   `=> void`; let the model own the promise and expose a void intent; wrap any promise-returning
   reference.
4. **Effects** (only for work that is not server state; a server read is a `useQuery`, handed to
   networking-and-server-state): read [references/effects-and-races.md](references/effects-and-races.md)
   sections 1-6 and imitate [examples/use-task-details-model.ts](examples/use-task-details-model.ts)
   (a SQLite read: one controller per run, a request key beside the answer, cancellation not recorded).
5. **Overlapping calls and OS mirrors** over local, SDK or OS sources (server search and filters are
   query keys): sections 7-11 of the same reference; imitate
   [examples/use-task-search-model.ts](examples/use-task-search-model.ts) (latest-wins, debounce,
   deadline) and [examples/watch-sync-status.ts](examples/watch-sync-status.ts) (subscribe first, an
   event cancels the first read).
6. **Cancellation, deadlines, retries, ports**: read
   [references/cancellation-and-deadlines.md](references/cancellation-and-deadlines.md). Give every
   abandonable port member a `signal` parameter
   ([examples/task-details-port.ts](examples/task-details-port.ts)) and decide cancellation by
   `signal.aborted` in the adapter.
7. **Listeners and timers**: read [references/listeners-and-timers.md](references/listeners-and-timers.md)
   for the release call of each API, the New Architecture timer facts and the background behaviour of
   iOS and Android. Use `useFocusEffect` for screen work; mark a composition-root listener that lives
   as long as the app with `// app-lifetime: <why>`.
8. **Tests**: write the race tests first, from
   [references/test-recipes.md](references/test-recipes.md) (controlled promises, out-of-order,
   unmount, fake timers, nothing left behind); see each fail by deleting the guard it protects.
9. **Run the checks** from the repo root: `npm run typecheck`, `npm run lint` (the lint rules of
   typescript-and-lint-rules carry rule 10 there), `npx jest <changed tests> --ci`, then
   `node ${CLAUDE_SKILL_DIR}/scripts/check-async-safety.mjs .`. Fix every `FAIL` line (it names the
   file, the rule and the fix; [references/checker-rules.md](references/checker-rules.md) explains each
   rule and its limits) and rerun until `RESULT: PASS`.
10. **On a device**, for a change in rows marked D of the catalogue (abort code, backgrounding,
    covered screens): run the flow on an iOS simulator and an Android emulator (e2e-maestro) before
    calling it done.

## Definition of done

- [ ] `npm run lint` passes: no floating promise, no `async` or expression-bodied handler (typescript-and-lint-rules).
- [ ] No promise-returning function is passed by reference to an `on*` prop, model field or listener; every `on*`/`handle*` type returns `void`.
- [ ] Every effect that writes, dispatches or navigates after async work aborts (or flags) it in its cleanup and checks the signal before each write; async-acquired subscriptions are guarded.
- [ ] Overlapping reads use `createLatestRequest`; writes are never aborted and are disabled while in flight.
- [ ] Cancellation is decided by `signal.aborted`, never shown or recorded; no `throwIfAborted`, `signal.reason`, `AbortSignal.abort()` or `{ signal }` listener in app code.
- [ ] Every subscription and timer is released where its work ends; only composition-root listeners carry `// app-lifetime: <why>`.
- [ ] Screen polling, sensors and location run in `useFocusEffect` and pause in the background.
- [ ] Every wait that can hang goes through `withTimeout`; retries are bounded and abortable.
- [ ] Race tests cover out-of-order answers, unmount mid-flight, unrecorded cancellation and nothing left behind, and each fails when its guard is removed.
- [ ] Copied templates pass `npm run typecheck`, `npm run lint` and their Jest tests.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-async-safety.mjs .` prints `RESULT: PASS` (no SKIP lines; the note `focus-scoped-work not applied` appears only without expo-router or React Navigation, `NOT APPLICABLE` only without react-native)

## Anti-patterns

- **`onPress={retry}` because it type-checks.** React Native's prop returns `unknown`; the rejection is
  lost. `onPress={() => { retry().catch(reportError); }}`, or a void intent from the model.
- **`onSave: () => Promise<void>` in props "so the button can show busy".** The button gets `isBusy`
  from the model; the type returns `void`.
- **`useEffect(() => { load().then(setTasks); }, [id])`.** The previous id's answer can land last.
  One `AbortController` per run, `if (signal.aborted) return;` before the write.
- **`useEffect` + `useState` around an `ApiClient` or `queryClient` call.** It re-implements caching,
  latest-wins and retries badly. `useQuery` with the inputs in the key (networking-and-server-state).
- **`let isMounted = true` checked once at the top.** The hazard is after each await; check before
  every write, and prefer the signal, which also stops the work.
- **`if (error.name === 'AbortError')`.** expo/fetch on a device rejects most aborts with a `FetchError`. Ask
  `signal.aborted`.
- **`signal.throwIfAborted()`, `signal.reason`, `addEventListener(type, fn, { signal })`.** All pass in
  Jest and fail on the phone. `if (signal.aborted) return;` and `removeEventListener` by hand.
- **`AppState.addEventListener('change', onChange);` with no variable.** Nothing can remove it. Keep
  the subscription and `remove()` it in the cleanup.
- **`Keyboard.removeAllListeners('keyboardDidShow')`.** It also removes the listeners other libraries
  added. Remove your own subscription.
- **`await new Promise((resolve) => setTimeout(resolve, 1000))` in a retry loop.** It cannot stop when
  the screen leaves. `await delayOrAbort(1000, signal)`.
- **A polling `setInterval` in a screen's `useEffect`.** The screen stays mounted when covered.
  `useFocusEffect` plus `useIsAppActive()`.
- **`Promise.race([request, timeout])` without clearing the timer or aborting the loser.** Both keep
  running. `withTimeout`.
- **Aborting a save because the user typed again.** The save may already have landed. Queue or
  coalesce writes; disable the action while one is in flight.
- **`await save(); router.back();`** It pops whatever is on top by then. Navigate first, or only while
  the screen is still focused.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/promises-and-handlers.md](references/promises-and-handlers.md) | Promise ownership, the verified lint gap per prop and listener, by-reference fixes, void callback types, model intents, combinators, unhandled rejections | Workflow step 3 |
| [references/effects-and-races.md](references/effects-and-races.md) | Effect cancellation shapes, request keys, async acquisition, focus effects, latest-wins, first read vs event, writes, navigation after await, stores | Workflow steps 4-5 |
| [references/cancellation-and-deadlines.md](references/cancellation-and-deadlines.md) | The device's AbortController vs Jest (verified), expo/fetch abort errors, signal-first cancellation, ports, withTimeout, delayOrAbort, bounded retries, TanStack signals | Workflow step 6 |
| [references/listeners-and-timers.md](references/listeners-and-timers.md) | Subscription APIs and their release (verified), traps, New Architecture timers, iOS and Android background behaviour, covered screens, app-lifetime listeners | Workflow step 7 |
| [references/test-recipes.md](references/test-recipes.md) | Controlled promises, out-of-order, unmount, fake timers, nothing-left-behind assertions, what only a device proves | Workflow step 8 |
| [references/checker-rules.md](references/checker-rules.md) | Every checker rule, configuration, notes and errors, limits, overlaps with other skills, verification record | Workflow step 9; a finding you disagree with |
| [references/silent-failure-catalogue.md](references/silent-failure-catalogue.md) | The closed list of silent async failures with guard and proof (checker, lint, Jest, device, net) | Workflow step 1 |
| `templates/src/core/async/latest-request.ts` | `createLatestRequest()`: one current request per action, starting a new one aborts the previous (canonical, owned by this skill; synced from the library, do not edit here) | Workflow steps 2 and 5 |
| `templates/src/core/async/latest-request.test.ts` | Its tests, including an out-of-order answer | Workflow step 2 |
| `templates/src/services/async/delay-or-abort.ts` | `delayOrAbort(ms, signal)`: a pause that stops on abort and leaves no timer or listener (canonical, synced; do not edit here) | Workflow steps 2, 5 and 6 |
| `templates/src/services/async/delay-or-abort.test.ts` | Its fake-timer tests (`allow-fake-timers` marker) | Workflow step 2 |
| `templates/src/services/async/with-timeout.ts` | `withTimeout((signal) => Promise<Result>, afterMs, signal?)`: a deadline that aborts the abandoned task; `TimedOut` and `Cancelled` failures (canonical, synced; do not edit here) | Workflow steps 2 and 6 |
| `templates/src/services/async/with-timeout.test.ts` | Its fake-timer tests: value, failure, timeout, caller abort, already aborted | Workflow step 2 |
| [examples/task-details-port.ts](examples/task-details-port.ts) | A port over on-device data (SQLite) whose async members take the caller's signal and return Results | Workflow step 6 |
| [examples/use-task-details-model.ts](examples/use-task-details-model.ts) | An effect with one AbortController per run, a request key, unrecorded cancellation | Workflow step 4 |
| [examples/use-task-details-model.test.ts](examples/use-task-details-model.test.ts) | Its race tests: out of order, unmount, retry, unexpected rejection | Workflow steps 4 and 8 |
| [examples/use-task-search-model.ts](examples/use-task-search-model.ts) | Latest-wins search with debounce (`delayOrAbort`) and a deadline (`withTimeout`) | Workflow step 5 |
| [examples/use-task-search-model.test.ts](examples/use-task-search-model.test.ts) | Its fake-timer race tests | Workflow steps 5 and 8 |
| [examples/watch-sync-status.ts](examples/watch-sync-status.ts) | Subscribe first, then read; a change event cancels the first read | Workflow step 5 |
| [examples/watch-sync-status.test.ts](examples/watch-sync-status.test.ts) | Its tests: event beats read, stop removes the listener | Workflow steps 5 and 8 |
| `scripts/check-async-safety.mjs` | The checker: `async-by-reference`, `void-callback-type`, `effect-stale-result`, `abort-signal`, `subscription-released`, `timer-cleared`, `focus-scoped-work` | Workflow step 9; definition of done |
| `scripts/lib/async-scan.mjs` | This skill's scanning helpers: sources, effect blocks and cleanups, promise functions, what happens to a returned handle | Only when changing the checker |
| `scripts/selftest.mjs` | Proves the checker passes the templates and examples and fails every planted bug | After changing the checker, a template or an example |
| `scripts/check-lib.mjs` | Shared script helper (synced; never edit here) | Never by hand |
| `scripts/lib/source-scan.mjs` | Shared lexer and scanner (synced; never edit here) | Never by hand |
| `assets/shared.json` | The shared files this skill copies in: the script helpers and its own three canonical async modules with their tests | When adding a shared file |
| `tests/` | The fixture base app (`tests/bases/app`) and the overlay cases of the self-test (`tests/fixtures/check-async-safety`) | When adding a rule to the checker |

## Related skills

- `typescript-and-lint-rules` - owns no-floating-promises, the synchronous-handler selectors and the timer-delay rule this skill builds on.
- `error-handling-typed-results` - the Result type, what a catch may do, attemptAsync, and the global error net for rejections nothing caught.
- `react-components-and-hooks` - which effects are allowed at all, effect cleanup presence, `useIsAppActive`, `useSyncExternalStore`.
- `networking-and-server-state` - the ApiClient, TanStack Query cancellation and retries, the connectivity port.
- `state-management-zustand` - stores whose async actions use the same latest-wins and dispose rules.
- `unit-and-component-tests` - render helpers, fakes, fake-timer and sleep rules for the race tests.
- `motion-and-animation` - UI-thread timing, worklets and `scheduleOnRN` instead of JS timers.
- `background-tasks` - work that must run while the app is not in the foreground.
- `e2e-maestro` - device runs for the failures Jest cannot see.
