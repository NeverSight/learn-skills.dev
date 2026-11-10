---
name: debug-menu-and-test-hooks
description: "Gates test-only code behind one literal TEST_ONLY switch: debug menu, debug link, simulated clock and offline. Use when adding a debug screen, a test hook, a debug link or a fake date for E2E or QA. Not for E2E flows (e2e-maestro)."
---

# Debug menu and test hooks

Development and preview builds carry a debug menu, one strict debug deep link and a simulated clock
and network that reach every reader, all through one literal gate; production builds contain none of
it, and a checker proves the gate, the entry, the wiring, the registry and the simulations on the
app's own code. Verified on 2026-10-10 with Expo SDK 57 (expo 57.0.26), React Native 0.86.3,
expo-router 57.0.24 and knip 6.38.0, in Jest and with back-to-back `expo export` bundles (iOS);
re-verified on 2026-10-17 wired through the root slots in the library's reference app, with
development and production exports for iOS and Android passing `check-variant-bundle`; not yet
driven on a simulator or an emulator.

## Rules that must hold

1. **One gate, one literal expression.** `src/test-only.ts` is the only way into test-only code:
   `export const TEST_ONLY: TestOnlyApi | null = process.env.EXPO_PUBLIC_APP_VARIANT === 'production'
   ? null : (require('./test-only-entry') as TestOnlyApi);` and nothing else runs there. Why: Metro
   folds only that literal comparison before it collects `require()` calls; an imported constant, a
   helper, `__DEV__` or `NODE_ENV` ships the code to the store or strips it from preview builds
   (app-variants-and-environment owns that rule). (`gate-file`, `gate-form`)
2. **`TestOnlyApi` is `typeof` the entry, never hand-written.** `import type * as TestOnlyEntry from
   './test-only-entry'`. Why: the gate casts the `require()`, so a hand-written type is never compared
   with the exports (`TEST_ONLY.x is not a function` in a preview build), and knip reported every
   entry export as unused with one (measured). (`api-derived`)
3. **The entry is a manifest with one unique sentinel.** Only `export { ... } from` lines and
   `TEST_BUILD_SENTINEL = '<APP>_TEST_BUILD_ONLY'`, a string no other app file contains. Why: the
   bundle and build checks prove the strip by that string, and a copy in shipped code fails every
   production proof. (`entry-manifest`, `sentinel`)
4. **Every export is read through `TEST_ONLY`, from declared test-only folders.** Each member is used
   as `TEST_ONLY?.member` by the startup, the root stack or a debug route, and each folder the entry
   re-exports from is in `contracts/architecture.json` `testOnlyFolders`. Why: an unread export is
   forgotten wiring, and an undeclared folder lets a static import ship it unnoticed.
   (`entry-reachable`, `test-only-folders`)
5. **The startup wraps the real ports once and hands only the wrapped services on.**
   `TEST_ONLY?.createTestHooks({ services: device, ... })` in the app registry's `prepareRootKits`
   (`src/services/create-root-kits.ts`), which AppRoot's `startApp` calls first, before the data layer
   opens, swaps `clock` and, when the services hold it, `connectivity` inside the services; every
   reader gets `testHooks?.services ?? device`. Why: one wrapper reaches every reader (due dates,
   repositories, TanStack Query through `services.connectivity`, banners, ads); a simulated port
   handed out beside the services leaves those readers on the real one. (`hooks-wired`, and the
   createTestHooks test)
6. **The simulated clock changes `today()` only.** It reads the simulated day on every call; `nowMs()`
   and `msUntilNextLocalDay()` call the real clock every time. Why: timers, timestamps and the
   next-day countdown must never jump, and `useToday()` still turns at the real midnight.
   (`simulated-clock`)
7. **Simulated offline is a full `ConnectivityPort` on the reachability hub.** `none` while
   simulating, the real reachability otherwise, `isOnline` derived from it, unchanged reports dropped,
   `stop()` releases the real adapter. Why: every consumer then follows the switch exactly as it
   follows a real outage. (`simulated-connectivity`)
8. **One debug deep link: an Expo Router route, one registry, one contract.**
   `<scheme>://debug/setup?...` is the route `src/app/(debug)/debug/setup.tsx`, which renders
   `TEST_ONLY?.DebugSetupRoot` with `useLocalSearchParams()` and redirects home in production (the
   canonical AppStack keeps the `(debug)` group behind `Stack.Protected` until the debug kit opens it);
   `DEBUG_LINK_PARAMS` and `contracts/debug-links.json` list the same parameters and values. Why:
   Expo Router delivers cold-start and running links once the navigator is ready, and flows read the
   contract, not the TypeScript. (`debug-registry`, `link-route`)
9. **A bad link refuses everything and says so.** An unknown, repeated or bad parameter returns a
   typed `debug-link-*` failure, applies nothing, is logged and shown as `debug.setup-error`. Why: a
   typo that is ignored makes a flow test the wrong state and pass. (`registry-strict`)
10. **Parse, plan, apply, replace.** The switches first, then saved settings (through the app's
    `DebugSettingsTarget`; refused when there is none), then `router.replace` to the screen; a
    direction restart ends the run. Every step sets a value, so a link applied twice changes nothing
    more. Why: reloads re-deliver the launch link and React's development effects run twice.
11. **The switches are one store, persisted apart from the app's data.** `src/stores/debug-overrides/`
    (reducer, cases, persist before publish) in `expo-sqlite/kv-store` under `debug.overrides`; the
    link and the menu write it through the same actions. Why: a reload or a kill keeps them, Maestro's
    `clearState` wipes them, and the menu always shows what a link set.
12. **Motion and probes follow the same switches, through the app's own seams.** The debug kit
    (`TEST_ONLY?.createDebugKit`, registered in the app's root-kit registry) fills the root's motion
    slot: `TestHooksRoot` takes `MotionConfig`'s place and passes `preference="on"` while
    `motion=still`; canvas probes
    render only while `probe=1`. Why: screenshots and E2E rest on the one reduce-motion path, never a
    second switch, and screenshots never show a probe.
13. **The strip is proven on the artifact.** After any change to the gate, the entry or variants,
    export development and production back to back without `--clear` and run
    app-variants-and-environment's `check-variant-bundle` on both. Why: only the bundle shows that the
    gate, the cache key and the variables worked together.

## Workflow

1. **Read** [references/gate-and-entry.md](references/gate-and-entry.md) (always), then for the task:
   the link [references/debug-deep-link.md](references/debug-deep-link.md); the clock, the network or
   the switches [references/simulated-clock-and-connectivity.md](references/simulated-clock-and-connectivity.md);
   wiring, the menu or another skill's hook [references/wiring-and-menu.md](references/wiring-and-menu.md);
   a checker line [references/checker.md](references/checker.md).
2. **Check the prerequisites**: the composition root and clock (architecture-and-boundaries), the
   `ConnectivityPort` and its hub (networking-and-server-state), `src/core/result.ts`, `date-key.ts`,
   `languages.ts`, the settings store if links change settings, and app-variants-and-environment's
   variants and Metro cache key.
3. **Copy the templates** to the paths their first lines name: `templates/src/test-only.ts` and
   `test-only-entry.ts` (rename `TASKS` in the sentinel), `templates/src/services/test-hooks/`,
   `templates/src/services/debug-storage/`, `templates/src/stores/debug-overrides/`,
   `templates/src/features/debug/` (the debug kit `debug-root-kit.tsx` included),
   `templates/src/app/(debug)/`, the `debug.*` keys of `templates/src/i18n/catalogs/`, and
   `templates/contracts/debug-links.json` with its schema. The test-hook kit (the gate, the hooks,
   the switches store, the storage, `TestHooksRoot` and the debug kit) is canonical in the library
   (its shared templates): the copies here are synced, never edited here.
4. **Declare the folders**: add `src/features/debug/`, `src/services/test-hooks/`,
   `src/services/debug-storage/` and `src/stores/debug-overrides/` to `contracts/architecture.json`
   `testOnlyFolders`; with a second persisting store, add state-management-zustand's
   `contracts/stores.json`.
5. **Wire it through the root slots** ([references/wiring-and-menu.md](references/wiring-and-menu.md)):
   two edits to the app's root-kit registry, never to the canonical root files
   ([examples/create-root-kits.ts](examples/create-root-kits.ts)): `prepareRootKits` makes the hooks
   and returns their services, and `createRootKits` registers `TEST_ONLY?.createDebugKit(hooks)` (the
   motion slot and the `(debug)` group); a settings target
   ([examples/settings-target.ts](examples/settings-target.ts)) once the app saves language and theme.
6. **Change a parameter or a switch test-first**: the registry test, the plan test, the reducer cases,
   then the code, then `contracts/debug-links.json`.
7. **Run the tests**: `npx jest src/features/debug src/services/test-hooks src/services/debug-storage src/stores/debug-overrides --ci --maxWorkers=2`
   and `npm run typecheck`, `npx eslint . --max-warnings 0`, `npx knip`.
8. **Prove the strip** (rule 13): the two exports, then app-variants-and-environment's
   `check-variant-bundle` on each; `rm -rf dist/variant-proof` after.
9. **Run the checker**: `node ${CLAUDE_SKILL_DIR}/scripts/check-test-hooks.mjs .`; fix each `FAIL`
   line (file, rule, fix) and rerun until `RESULT: PASS`.

## Definition of done

- [ ] `src/test-only.ts` is the template's expression with the derived `TestOnlyApi`; nothing else
      `require()`s code.
- [ ] `src/test-only-entry.ts` holds re-exports and one unique `<APP>_TEST_BUILD_ONLY` sentinel; every
      export is read through `TEST_ONLY?.` outside the test-only folders.
- [ ] The registry's `prepareRootKits` returns `testHooks?.services ?? device` and `createRootKits`
      registers `TEST_ONLY?.createDebugKit` (TestHooksRoot in the motion slot, the `(debug)` group
      opened); the root files are the canonical ones, unedited; the group layout is a plain `Slot`
      and both leaf routes redirect in production.
- [ ] `contracts/debug-links.json` equals the registry; a bad link shows `debug.setup-error`.
- [ ] The test-only folders are in `testOnlyFolders`; tests, typecheck, ESLint and knip pass.
- [ ] A development and a production export made back to back pass app-variants-and-environment's
      `check-variant-bundle` (the sentinel in development, absent in production).
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-test-hooks.mjs .` prints `RESULT: PASS`. Allowed:
      `SKIP contracts/architecture.json [test-only-folders] not yet created (architecture-and-boundaries creates it)`,
      `NOT APPLICABLE: the app has no test-only code: ...` before this skill is adopted, and the
      `note: link-route` line on React Navigation.

## Anti-patterns

- **`const IS_TEST_BUILD = ...` in a config file, then `IS_TEST_BUILD ? require(...) : null`.**
  Metro keeps the module in production. The literal comparison, in the gate.
- **`if (__DEV__) showDebugMenu()`.** Strips the menu from the preview builds testers use, and keeps
  nothing out of the bundle. Read `TEST_ONLY?.DebugMenuRoot`.
- **A debug route that imports the debug screen.** Expo Router bundles every route, so the screen and
  its fakes ship. Render it through `TEST_ONLY` and redirect when it is undefined.
- **A hand-written `TestOnlyApi` with `@public` tags or knip ignores to quiet it.** Derive the type.
- **A `Linking.addEventListener('url')` handler for debug links.** It misses the launch link and
  duplicates the router; let Expo Router open the route.
- **A parser that skips unknown parameters, or `offline=true`.** Refuse the link; booleans are `0`/`1`.
- **`setDate()` that replaces `nowMs()`**, or a "simulate offline" that patches one screen. Wrap the
  port once, in the startup.
- **Debug switches in React state or in the app's preferences.** They vanish on the direction reload
  or leak into user data. The test-only kv store, through the switches store.
- **A second gate for another skill's hooks.** Re-export them from the one entry.
- **A simulated connectivity port handed out next to the services.** `services.connectivity` stays
  the device adapter and TanStack Query never hears the switch; let `createTestHooks` swap it inside.
- **`xcrun simctl openurl` for a debug link, or `adb -s <serial> shell am start -d` with the URL
  quoted once.** iOS waits on an "Open in …?" alert nobody accepts; the device shell cuts the URL at
  `&`. Use the Maestro subflow with the guarded accept step (references/debug-deep-link.md).
- **A `<Redirect>` in the `(debug)` group layout.** navigation-and-routing's `flow-by-guard` fails it,
  and `Stack.Protected` plus the leaf routes' redirects already keep production out.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| `references/gate-and-entry.md` | Owners, the gate, the derived type (knip measurement), the manifest, the sentinel, test-only folders, the measured strip proof, pitfalls | Workflow step 1, always |
| `references/debug-deep-link.md` | The URL, Expo Router delivery on iOS and Android, the link screen's order, strict parsing, idempotence, tool commands, adding a parameter | Workflow steps 1 and 6 |
| `references/simulated-clock-and-connectivity.md` | `createTestHooks`, the clock and network wrappers, the switches store, the kv persistence, tests, pitfalls | Workflow steps 1 and 6 |
| `references/wiring-and-menu.md` | The startup order, the four edits, the debug routes, the menu, other skills' hooks, what is left out | Workflow steps 4 and 5 |
| `references/checker.md` | Every rule, the SKIP, NOT APPLICABLE and note lines, configuration keys, multi-package, the self-test | Workflow step 9, a FAIL line |
| `templates/src/test-only.ts` | The gate | Workflow step 3 |
| `templates/src/test-only-entry.ts` | The entry: re-exports and the sentinel | Workflow step 3 |
| `templates/src/services/test-hooks/` | `createTestHooks`, the simulated clock and connectivity, `DebugSettingsTarget` (+ tests) | Workflow step 3 |
| `templates/src/services/debug-storage/` | The storage port, the kv-store adapter and the fake (+ tests) | Workflow step 3 |
| `templates/src/stores/debug-overrides/` | The switches: codec, reducer, cases, store, selectors (+ tests) | Workflow steps 3 and 6 |
| `templates/src/features/debug/` | The registry and plan, the link screen and the menu (model, view, root), `TestHooksRoot` and the debug kit `debug-root-kit.tsx` (canonical, synced), the model, gate and route tests | Workflow steps 3 and 6 |
| `templates/src/app/(debug)/` | The group layout, `/debug` and `/debug/setup` routes | Workflow step 3 |
| `templates/src/i18n/catalogs/en.json` | The `debug.*` keys in the source language (merged into the app's catalog) | Workflow step 3 |
| `templates/src/i18n/catalogs/ar.json` | The same keys in the RTL example locale | Workflow step 3 |
| `templates/contracts/debug-links.json` | The link contract (mirrors the registry; a synced copy of the canonical file other skills' checkers read, edited only at its canonical home) | Workflow steps 3 and 6 |
| `templates/contracts/debug-links.schema.json` | Its JSON schema (synced copy) | Workflow step 3 |
| `examples/create-root-kits.ts` | The app's root-kit registry with the test build's lines: `prepareRootKits` (the hooks, their services) and the debug kit (also the self-test's base) | Workflow step 5 |
| `examples/settings-target.ts` | A `DebugSettingsTarget` over the settings store and the direction restart | Workflow step 5 |
| `examples/debug-setup-flow.yaml` | A Maestro subflow that opens the link, accepts iOS's "Open in …?" alert (guarded) and proves the state | Writing flows (hand to e2e-maestro) |
| `scripts/check-test-hooks.mjs` | The checker (13 rules) | Workflow step 9 |
| `scripts/lib/hook-probes.mjs` | Its behaviour probes (registry, clock, connectivity) | Never by hand |
| `scripts/selftest.mjs` | Proves the checker against `tests/fixtures/` | After changing the checker |
| `scripts/check-lib.mjs` | Synced checker library (do not edit here) | Never by hand |
| `scripts/lib/app-modules.mjs` | Synced: loads the app's pure TypeScript for the probes | Never by hand |
| `scripts/lib/source-scan.mjs` | Synced: import resolution and test-file detection | Never by hand |
| `tests/fixtures/` | Overlay cases: good, one bad per rule, pass and error cases | After changing the checker |
| `tests/bases/` | The minimal app the cases start from (with synced canonical files) | After changing the checker |
| `assets/shared.json` | The synced-file manifest | When a shared file is added |

## Related skills

- `app-startup-and-bootstrap` - the root slots the debug kit fills (`prepareRootKits`, `motion`, `opensDebugRoutes`).
- `app-variants-and-environment` - the literal-comparison rule, the Metro cache key and the bundle proof.
- `architecture-and-boundaries` - the import side of the gate, `testOnlyFolders`, the composition root.
- `navigation-and-routing` - `Stack.Protected` for the debug group and the startup skeleton.
- `e2e-maestro` - flows that open the debug link and wait on testIDs.
- `ios-simulator-build` - the sentinel in a built `.app` and the ready marker.
- `dates-streaks-and-statistics` - `useToday()` and what a simulated day must keep real.
- `networking-and-server-state` - the `ConnectivityPort` and its hub.
- `state-management-zustand` - the store rules the switches follow.
- `motion-and-animation`, `skia-canvas-rendering`, `audio-and-haptics-feedback` - motion held still, canvas probes, recorded feedback.
