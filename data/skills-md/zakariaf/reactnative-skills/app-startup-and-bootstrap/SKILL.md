---
name: app-startup-and-bootstrap
description: Orders an Expo app's cold start - polyfills, error net, splash hold, storage open, providers, splash release, background flush. Use when editing the root _layout.tsx or the app root, or the splash hangs or flashes. Not for routes (navigation-and-routing).
---

# App startup and bootstrap

The app starts in one fixed order: the entry loads the polyfills and then the router; the root layout
installs the error net, holds the native splash and decides the direction before anything opens; the
app root opens storage once, connects the error log and hydrates the stores synchronously, mounts the
providers in dependency order and releases the splash once the first screen is real. Buffered writes
flush from one root hook when the app leaves the foreground. Optional kits (crash reporting,
analytics, notifications, ...) plug into typed slots from one registry, so the root files stay
canonical when a kit is added. One zero-dependency checker proves it.

## Rules that must hold

1. **The entry imports the polyfills first and `expo-router/entry` last.** Nothing follows the router
   import. Why: ES imports evaluate in order; a module after the router entry loads after the root
   component was registered. (`entry-router-last`)
2. **The root layout's first imports are side effects: the error net installer, then the splash
   hold.** Every import with bindings comes after them. Why: a module that throws while loading must
   find the net, and the hold must run before any other app module. (`root-import-order`)
3. **The native splash is held once, at module scope, in `hold-splash.ts`.** Why: Expo Router hides
   an unheld splash at "navigation ready", over a direction restart's empty screen or a blocking wait;
   called in a component or effect, the hold comes after native content appeared, when iOS and Android
   may already have hidden it. (`splash-hold`)
4. **The splash is released once, in an effect, below the direction gate, when the startup gate is
   ready** (`useStartupReady(gate, hideSplash)` in the app root). A startup component renders `null`
   only while the splash is held. Why: a hold with no release keeps a release build on the splash
   forever; a release in render or above the gate uncovers a frame that is not the first screen.
   (`splash-release`, `blank-frame`)
5. **The root layout's first render creates adapters, reads config and resolves the language, and
   opens nothing; `DirectionGate` is its outermost element (directly inside web-support's
   `WebStorageGate` when the app ships the web); everything with effects lives in its child
   `AppRoot`.** Why: a direction restart re-runs every module and initializer, so work done
   before the decision happens twice (rtl-and-direction's `direction-before-render` enforces the gate).
6. **The data layer opens once, synchronously, in the app root's startup initializer, then the error
   net's sink connects, then the query client, settings and stores hydrate, then the optional kits are
   created, in that order** (`startApp`, run as `useState(() => startApp(services, language))`). Why: the first frame has the real rows
   with no loading state, the buffered errors of the first moments reach the log before any provider
   renders, and a second open runs migrations again. (`storage-open-once`, `sink-before-providers`)
7. **The startup path awaits nothing.** The root layout and the app root contain no `await`,
   `.then`, `.catch` or `.finally`; async work the first screen truly needs is a non-interactive
   blocking task of `createStartupGate` with a literal `deadlineMs` at or under 3000. A session
   restore follows auth-and-secure-storage: its read is async and non-interactive, so it is a blocking
   task under the deadline, and a miss starts the session as unknown or unavailable; a biometric
   unlock is never a gate task but a lock screen after the splash. Why: a promise that never settles
   keeps a held splash up forever, and a prompt that waits for the person outlasts any deadline; the
   gate always opens by its deadline and reports what it missed. (`startup-await`, `startup-deadline`)
8. **Fonts are embedded with the expo-font config plugin, never loaded at runtime.** Why: `useFonts`
   either holds the first frame or swaps the font after it. (`runtime-font-load`)
9. **Providers nest in one dependency order and each is mounted once on the root path:** services (or
   `AppProviders`), data, query, settings store, stores, preferences (i18n, theme, text locale), root
   stack (gesture root, keyboard, `RootMotion` (the one MotionConfig), navigation theme, session,
   feedback, ads, games, then `AppStack`, whose `RootKits` slot wraps the `Stack` in the kits'
   providers). Why: each provider reads only those
   outside it, a misplaced one throws only when its path renders on a device, and a second copy
   silently overrides the first. (`provider-order`, `provider-once`)
10. **Deferred work starts after the splash release, in the component or service that owns it; never
    through `InteractionManager`.** Why: consent, entitlements, OTA checks and prefetches must not delay
    the first frame, and `InteractionManager` is a deprecated stub in React Native 0.86 that runs on the
    next tick. (`interaction-manager`)
11. **Buffered writes flush from one root hook when the app leaves the foreground:**
    `useFlushOnBackground(flushers, errorLog)` once, in the app root, before
    `useCheckpointOnBackground`; features hand it a `Flusher` and never write from their own `AppState`
    listener. Why: an iOS swipe-kill from the app switcher sends `inactive` and no `background`, and
    listeners run in subscription order, so the drafts must land before the WAL is folded.
    (`flush-root`, `lifecycle-write`)
12. **Optional kits join through the slots, never through the root files.** A kit returns a `RootKit`
    (`forward`, `blocking`, `flushers`, `motion`, `opensDebugRoutes`, `provide`, `effects`; every part
    optional) from the app's one registry, `src/services/create-root-kits.ts`; `startApp` first calls
    the registry's `prepareRootKits` (the ports every reader uses: a test build's simulated clock and
    network), then `createRootKits` once, after the stores, attaches the kits to the error sink
    (which replays the reports it kept) and hands their tasks to the gate and their flushers to the
    flush; `RootMotion` renders the first kit's motion slot in `MotionConfig`'s place; `AppStack`
    opens its `(debug)` group only while a kit says so and renders `<RootKits kits>` around the
    `Stack`; a kit that needs Metro lists a `MetroKit` in `scripts/metro/metro-kits.ts`, which the
    canonical `metro.config.js` composes. A slot no kit fills does nothing, and a test build's kits
    are reached only through the test-only gate. Why: the root skeleton stays the canonical file
    every skill cites, a kit is added or removed in one line, and every kit's work still runs at its
    place in the startup order (E1, E2, E6, E7, F5, F6, I1). (`root-kits`)
13. **Prove the launch on a release build, on both platforms.** Expo Go shows the app icon instead of
    the splash, and a development build does not apply every splash config property (Expo's SDK 57
    splash-screen docs); only a release build shows the hold, the release and a direction restart as
    people see them.

## Workflow

1. **Read the order**: [references/startup-order.md](references/startup-order.md) (section 1 is the
   table of every step, its file and its owner skill). Find where the change belongs before writing it.
2. **New app or no root yet**: copy the templates (line 1 names each repo path):
   `templates/src/app/_layout.tsx`, `templates/src/features/root-navigator/` (`app-root.tsx`,
   `root-stack.tsx`, `app-stack.tsx`, `hold-splash.ts`, `startup-gate.ts`, `use-startup-ready.ts`,
   `background-flush.ts`, `use-flush-on-background.ts`, `root-kits.tsx`, the helpers each with its
   test), `templates/src/services/root-kits/root-kit.ts` (+ test, the slot types and helpers),
   `templates/src/services/create-root-kits.ts` (the app's registry, empty) and
   `templates/contracts/startup.json`. These files are the canonical root skeleton that other skills
   cite; each of them owns one piece inside it. They expect the composition root
   (architecture-and-boundaries), the error net (error-handling-typed-results), `DirectionGate`
   (rtl-and-direction), the data layer (persistence-and-migrations), `watchSystemA11y` and
   `MotionConfig` (accessibility-as-code), `useScreenAnimation` (motion-and-animation) and the
   navigation theme (design-system-structure); set up a missing one with its skill first. Route groups
   and `Stack.Protected` inside `AppStack` are navigation-and-routing's.
3. **Adding a piece of startup.** An optional kit from another skill (crash reporting, analytics,
   push or local notifications): one entry in `src/services/create-root-kits.ts`, as that skill's
   example shows; the root files stay unchanged (read [references/startup-order.md](references/startup-order.md)
   section 15, the slot contract). An app piece (a store, a client, the session): its creation in
   `startApp` at its row of the order table, its provider at its place in the tree, and its name in
   `appRootOrder` in `contracts/startup.json` if it is new; pass what a kit reads (the settings, the
   session) on to `createRootKits`. Imitate [examples/app-root-with-session.tsx](examples/app-root-with-session.tsx).
4. **Work that is async**: decide with [references/startup-gate-and-deferred-work.md](references/startup-gate-and-deferred-work.md)
   (section 1) whether it blocks the first screen. Deferred is the default; a blocking task returns a
   Result, goes into `createStartupGate({ blocking })` and gets a test that drives it resolving, failing
   and hanging.
5. **Splash problems** (hangs, flashes, empty frame): [references/splash-screen.md](references/splash-screen.md)
   (sections 3-4 and the pitfalls table). The splash art itself is icons-app-icon-and-splash's.
6. **A buffered writer** (debounced draft, batch queue): read [references/lifecycle-flush.md](references/lifecycle-flush.md),
   imitate [examples/task-draft-buffer.ts](examples/task-draft-buffer.ts), return its flusher from
   `startApp`.
7. **Test**: `npx jest src/features/root-navigator --ci --maxWorkers=2`, then `npm run typecheck` and
   `npx eslint . --max-warnings 0`.
8. **Run the checker** from the repo root: `node ${CLAUDE_SKILL_DIR}/scripts/check-startup.mjs .`;
   look up a FAIL line's rule in [references/checker-rules.md](references/checker-rules.md); fix and
   rerun until `RESULT: PASS`.
9. **On devices** (by hand, once per release candidate, a step for the developer): cold start a release
   build on a named simulator and a named emulator, once per layout direction of the app's languages:
   the frame after the splash is the first screen; type a draft, swipe the app away, relaunch: the draft
   is there.

## Definition of done

- [ ] `index.ts` imports the polyfills first and `expo-router/entry` last (or `main` is `expo-router/entry`).
- [ ] `src/app/_layout.tsx` imports the error net installer, then `hold-splash`; renders `DirectionGate` outermost (inside `WebStorageGate` when the app ships the web) and `AppRoot` inside it; opens nothing.
- [ ] `AppRoot` runs `startApp` once in a `useState` initializer: the registry's prepared ports, open, sink, client, settings, stores, kits, gate; no `await` or promise chain; `ServicesProvider` gets the prepared services.
- [ ] The splash is held once at module scope and released once through `useStartupReady`; every blocking task returns a Result and the gate's deadline is at most 3000 ms.
- [ ] Providers follow `appRootOrder` / `rootStackOrder`, each mounted once; fonts are embedded; no `InteractionManager`.
- [ ] Buffered writers hand a `Flusher` to the one `useFlushOnBackground`, called before `useCheckpointOnBackground`.
- [ ] Optional kits are entries of `createRootKits`, created once in `startApp` after the stores and handed to every slot (`errors.attach`, `kitBlocking`, `kitFlushers`, `RootMotion`, `AppStack`'s `(debug)` guard, `<RootKits kits>`); `prepareRootKits` runs before the data layer opens; no root file imports a kit; Metro kits live in `scripts/metro/metro-kits.ts`.
- [ ] `npx jest src/features/root-navigator --ci --maxWorkers=2`, `npm run typecheck` and `npx eslint . --max-warnings 0` pass.
- [ ] The release-build launch of step 9 was done on iOS and Android, or listed for the developer.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-startup.mjs .` prints `RESULT: PASS` (no SKIP lines are expected: every file it reads is this skill's).

## Anti-patterns

- **`await openDatabaseAsync()` in the root layout behind a loading spinner** - a second startup path
  with nothing on screen. Open synchronously in `startApp`.
- **`SplashScreen.preventAutoHideAsync()` inside `useEffect`** - by then the splash may be gone. Hold
  it at module scope in `hold-splash.ts`.
- **`hide()` in the root layout's effect** - it also runs in the JS run that is about to restart for
  the direction. Release in the app root.
- **A hold and no release "because Expo Router hides it"** - the router leaves a held splash alone.
- **`useFonts` in the root layout with `if (!loaded) return null`** - an empty frame or a font swap.
  Embed the fonts.
- **`InteractionManager.runAfterInteractions(prefetch)`** - runs on the next tick, mid-startup. Start
  it from the owner after the release.
- **`appErrorNet.connect` in `useEffect`** - errors of the first render wait or are lost. Connect in
  `startApp`.
- **A screen's own `AppState` listener that saves its draft** - gone when the screen unmounts, and
  unordered against the checkpoint. Hand a `Flusher` to the root.
- **Flushing only on `background`** - an iOS swipe-kill from the switcher never sends it.
- **A `MotionConfig` in `PreferencesRoot` beside the root stack's `RootMotion`, or a second
  `I18nProvider`** - the inner one overrides the person's setting (and two MotionConfigs fight over
  Reanimated's global mode). `PreferencesRoot` provides `ReduceMotionPreferenceContext` instead.
- **`<StrictMode>` around `AppRoot`** - React runs the initializer twice in development: two database
  opens. Put it around `RootStack` if wanted.
- **A blocking task without a deadline, or a deadline from a variable** - a splash that can wait
  forever. A literal or module constant up to 3000 ms.
- **A biometric read (`requireAuthentication`) as a startup-gate task** - the deadline expires under
  the Face ID or BiometricPrompt sheet and the answer arrives after the app opened. Show a lock
  screen after the splash release.
- **`reloadAppAsync` in a module body** - crashed a Release build while the bundle was still
  evaluating. Restart from a mounted component's effect.
- **A kit wired into `app-root.tsx`, `app-stack.tsx` or `metro.config.js`** (a Sentry sink in
  `startApp`, a tap hook in `AppStack`, `getSentryExpoConfig` in Metro) - forks the canonical skeleton
  every skill cites. Register the kit in `createRootKits`; list a Metro kit in `metro-kits.ts`.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/startup-order.md](references/startup-order.md) | The canonical order step by step (entry, imports, first render, gate, startApp, hooks, providers, splash, deferred, flush), owners, reloads, Strict Mode, React Navigation and multi-package notes | Workflow steps 1-3 |
| [references/splash-screen.md](references/splash-screen.md) | Verified splash behaviour of expo-splash-screen and Expo Router on iOS and Android, hold and release, crashes, Expo Go, pitfalls, tests | Workflow step 5 |
| [references/startup-gate-and-deferred-work.md](references/startup-gate-and-deferred-work.md) | Synchronous vs blocking vs deferred work, the gate, the deadline, where deferred work starts, fonts, InteractionManager, cold start hand-off | Workflow step 4 |
| [references/lifecycle-flush.md](references/lifecycle-flush.md) | AppState sequences per platform, what must flush, one root hook, flush before checkpoint, synchronous flushers, tests | Workflow step 6 |
| [references/checker-rules.md](references/checker-rules.md) | Every check-startup rule, the contract keys, SKIP and NOT APPLICABLE, limits | Workflow step 8, on any FAIL line |
| `templates/src/app/_layout.tsx` | The root layout: net, hold, `ErrorBoundary`, adapters and language, `DirectionGate` around `AppRoot` | Workflow step 2 |
| `templates/src/features/root-navigator/app-root.tsx` | The app root: `startApp`, lifecycle hooks, splash release, providers | Workflow steps 2-3 |
| `templates/src/features/root-navigator/root-stack.tsx` | The root stack: gesture root, `KeyboardProvider`, `RootMotion`, navigation theme around `AppStack` | Workflow steps 2-3 |
| `templates/src/features/root-navigator/root-motion.tsx` | `RootMotion`: the one `MotionConfig` with the preference above it, or the first kit's motion slot | Workflow steps 2-3 |
| `templates/src/features/root-navigator/root-motion.test.tsx` | Its tests: "system" by default, the provided preference, the first kit's motion slot | Workflow step 2 |
| `templates/src/features/root-navigator/app-stack.tsx` | The root `Stack` with `useScreenAnimation()`, the test-build `(debug)` group behind `Stack.Protected` (`opensDebugRoutes`), inside the `RootKits` slot; route groups go inside it | Workflow step 2 |
| `templates/src/features/root-navigator/root-kits.tsx` | `RootKits`: every kit's provider around the Stack and its effects beside it | Workflow steps 2-3 |
| `templates/src/features/root-navigator/root-kits.test.tsx` | Its tests: no kits, provider nesting in registry order, effects mounted once | Workflow step 2 |
| `templates/src/services/root-kits/root-kit.ts` | The slot contract: `RootKit`, `createKitErrorSink` (records, then forwards; replays the first moments), `kitBlocking`, `kitFlushers`, `kitMotion`, `kitsOpenDebugRoutes` | Workflow steps 2-3 |
| `templates/src/services/root-kits/root-kit.test.ts` | Its tests: records always, replay, limit, attach once, a throwing kit, shared names | Workflow step 2 |
| `templates/src/services/create-root-kits.ts` | The app's one kit registry: `prepareRootKits` (returns the services unchanged) and `createRootKits` (empty); part of the composition root | Workflow steps 2-3 |
| `templates/src/features/root-navigator/hold-splash.ts` | The module-scope splash hold | Workflow step 2 |
| `templates/src/features/root-navigator/hold-splash.test.ts` | Its test: once per registry, rejection to the net | Workflow step 2 |
| `templates/src/features/root-navigator/startup-gate.ts` | `createStartupGate`: blocking tasks under one deadline, never rejects | Workflow steps 2 and 4 |
| `templates/src/features/root-navigator/startup-gate.test.ts` | Its tests: no task, all tasks, failure, hang, throw, start twice, unsubscribe, a throwing listener | Workflow step 4 |
| `templates/src/features/root-navigator/use-startup-ready.ts` | Reads the gate and releases the splash after the commit | Workflow step 2 |
| `templates/src/features/root-navigator/use-startup-ready.test.ts` | Its tests with a real gate | Workflow step 2 |
| `templates/src/features/root-navigator/background-flush.ts` | `Flusher`, `isLeavingForeground`, `runFlushers` | Workflow step 6 |
| `templates/src/features/root-navigator/background-flush.test.ts` | The transition table and the throwing flusher | Workflow step 6 |
| `templates/src/features/root-navigator/use-flush-on-background.ts` | The one root flush hook | Workflow step 6 |
| `templates/src/features/root-navigator/use-flush-on-background.test.ts` | iOS and Android sequences, unmount | Workflow step 6 |
| `templates/contracts/startup.json` | The app's startup facts for the checker (defaults filled in) | Workflow steps 2-3 |
| `templates/contracts/startup.schema.json` | Its JSON schema | When editing the contract |
| [examples/app-root-with-session.tsx](examples/app-root-with-session.tsx) | Shape: the app root with the session restore (auth-and-secure-storage) as its one blocking task, settings, stores, query and a draft buffer | Workflow step 3 |
| [examples/task-draft-buffer.ts](examples/task-draft-buffer.ts) | Shape: a debounced writer that hands a `Flusher` to the root | Workflow step 6 |
| `scripts/check-startup.mjs` | The checker (16 rules) | Workflow step 8, definition of done |
| `scripts/selftest.mjs` | Proves the checker on the fixtures | After changing the checker |
| `scripts/check-lib.mjs` | Shared checker library (synced; do not edit here) | Never by hand |
| `scripts/lib/source-scan.mjs` | Shared source lexer and import resolver (synced; do not edit here) | Never by hand |
| `scripts/lib/startup-scan.mjs` | Scope, function and JSX-span analysis for the checker | When changing the checker |
| `assets/shared.json` | Which shared files this skill syncs | Maintainers |
| `tests/` | `bases/app/` (stand-ins for the error net and the entry) and `fixtures/check-startup/` (good, bad-*, pass-*, error-* cases on the templates) | After changing the checker or a template |

## Related skills

- `navigation-and-routing` - the routes, route groups, guards and `Stack` options inside `AppStack`.
- `rtl-and-direction` - `DirectionGate` and the direction restart this order is built around.
- `error-handling-typed-results` - the error net and the root `ErrorBoundary`.
- `persistence-and-migrations` - what `openDeviceData` opens, migrations and the WAL checkpoint.
- `architecture-and-boundaries` - the composition root and "nothing at import time".
- `settings-and-preferences`, `state-management-zustand`, `networking-and-server-state` - the stores, `PreferencesRoot` and `QueryProvider` that join `startApp`.
- `i18n-strings-and-catalogs` - the Intl polyfills and language resolution.
- `icons-app-icon-and-splash` - the splash image and colours.
- `performance-budgets` - measuring cold start.
- `ota-updates`, `admob-ads-and-consent`, `in-app-purchases` - deferred startup work.
- `deep-links-and-universal-links`, `push-notifications`, `local-notifications` - the incoming-link gate and the tap hooks that run below the navigator (startup-order step F6; the notification kits plug into the slots).
- `crash-reporting-and-observability`, `analytics-and-consent` - root kits: error forwarding, consent after the splash, screen views, the Metro kit.
- `app-variants-and-environment` - the canonical `metro.config.js` that composes the Metro slot.
