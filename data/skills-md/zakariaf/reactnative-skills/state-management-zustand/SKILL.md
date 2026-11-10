---
name: state-management-zustand
description: Builds Zustand 5 stores - pure reducers. Use when adding a store, action or selector, deciding where state lives, leaving Redux or persist+AsyncStorage, or on Maximum update depth. Not for server data (networking-and-server-state).
---

# State management with Zustand

Client state lives in thin Zustand 5 stores, one per domain, created once per app start over the
data layer's ports; every change is reduced by a pure reducer, written to disk, and only then shown;
server data stays in TanStack Query. Two zero-dependency scripts prove it on the app's own code.

## Rules that must hold

1. **One store per domain, made by a factory and created once per app start.** `create<Domain>Store(deps)`
   builds a vanilla store (`createStore` from `zustand/vanilla`) over the ports it receives;
   `createStores(deps)` calls each factory once (the root layout's `useState` initializer, and
   `test/test-app.tsx` over fakes), `StoresProvider` hands the set down, components read
   `use<Domain>Store(selector)`. No `create` from `zustand`, no store at module level, no factory call in
   feature or UI code; the one module-level store is an OS mirror listed in `contracts/stores.json`
   (accessibility-as-code owns it). A store another skill ships with its own provider (the settings
   store) is created once by its own opener and follows the same rules. Why: tests need fresh stores,
   and Fast Refresh re-runs an edited module while components keep their state, so a module-level
   store is made a second time; a `useState` initializer makes it once per React tree.
2. **Persist before publish.** A change asks the reducer first (a refused or no-op change returns the
   same object: no write, no render), writes through the port the factory received (a repository, the
   document service, a preferences port: synchronous, committed when it returns ok), checks the result,
   and only then calls `set`. A failed write publishes nothing but the failure (a returned `Result`, or a
   `…Failure` field). When persistence assigns the id, persist first and publish the saved row through
   the reducer. State a service produces (a Premium entitlement from the purchase flow) still enters
   through a store method that writes it (`grantPremium(entitlement)`), never a publish-only `dispatch`.
   A store meant to forget at restart says `// memory-only: <why>`, never a store whose state is saved. Why: the screen never
   shows a value that is not on disk, and iOS and Android both end background apps without warning.
3. **All logic sits in pure reducers with imperative kebab-case actions, pinned by a cases table.**
   `<domain>Reducer(state, action)` imports no runtime code, never mutates, never reads the clock or
   randomness (time and ids arrive in the action) and returns the same object when nothing changes; every
   `set` publishes a reducer result; `<name>-reducer-cases.ts` beside it holds the rules as plain data (at
   least one `same: true` case), run by its test and by `check-reducers`. Why: pure reducers replay the
   same in Jest, Node and on both platforms, and a rule nobody pins drifts.
4. **Selectors return a primitive or a reference already in the state; a built value goes through
   `useShallow`; no store hook without a selector, no equality argument.** Named selectors live in
   `<domain>-selectors.ts`; a builder (`.filter`, `.map`, `{ … }`) is read as
   `use<Domain>Store(useShallow(selectX))`. Why: in Zustand 5 a selector returning a new reference each
   call makes React throw "Maximum update depth exceeded" (verified, RNTL 14 on React 19.2), and the v4
   equality argument is gone.
5. **A write that spans stores is one transaction, then every store re-reads.**
   `updateAndPublish(stores, () => tasks.removeList(id))`, with each such write named in
   `contracts/stores.json` `crossStoreWrites`. Never several store calls, never the bare write. Why: a kill
   between two writes leaves half a change, and a bare write leaves other stores showing deleted rows.
6. **Server state and navigation state never enter a store.** Network data lives in the TanStack Query
   cache (networking-and-server-state): no `fetch`, API client or React Query in a store, no effect that
   copies `query.data` into one; route params belong to Expo Router. Stores hold client state: local
   rows, UI choices, preferences, sessions. Why: two copies of server data drift on every refetch, and a
   copied route goes stale on back (Android predictive back, the iOS swipe).
7. **Stores are synchronous and persist only through the data layer's ports.** No `async`, `await` or
   `.then` in a store; no zustand `persist` middleware anywhere, and no AsyncStorage, MMKV, SQLite, driver,
   slot store or adapter import in a store (which engines the rest of the app may use is
   persistence-and-migrations' one-engine rule); only a store's own methods change
   it, never `setState` from outside. Why: an async action races itself and can publish a stale answer
   last, and a second persistence path has no version, no migration and no backup.
8. **An undoable session lives in a per-session store over a pure session reducer.** `past` stays in
   memory for instant undo; the written form keeps `start`, the command log and the snapshot; restore
   replays the log to rebuild undo, keeps the snapshot when the replay disagrees, and comes back paused;
   persist before publish. Why: a kill mid-animation loses nothing, and a relaunch never moves on unseen.
9. **Every reducer has a test beside it that runs its cases, and every persisting store a thin store
   test** (a subscriber already sees the value on disk; a failed write publishes nothing; a no-op writes
   nothing). Why: the order inside a store is invisible in review, and one moved line breaks it.

## Workflow

1. Read [references/store-pattern.md](references/store-pattern.md): the store shape, both persist orders,
   composition, reducers and cases tables, selectors, cross-store writes, tests, every checker rule and
   the contract. Read [references/state-homes.md](references/state-homes.md) when deciding where a piece
   of state lives or when moving off Redux, Context, MobX or a `persist` + AsyncStorage store, and
   [references/undoable-session.md](references/undoable-session.md) before building undo.
2. Check the prerequisites: `src/core/result.ts` (error-handling-typed-results), the data layer
   (persistence-and-migrations: repositories on `AppData`, or the document service) and the composition
   root (architecture-and-boundaries). Install the pinned version from the repo root:
   `npm install -E zustand@5.0.15` (stack table, verified 2026-10-03; re-verify with
   `npm view zustand version`). When multi-package: run it in the app workspace (`-w apps/<app>`).
3. First stores: copy `templates/src/stores/` (leave out `session/` until step 7), `templates/contracts/`,
   and replace the Tasks lists and tasks with the app's domains, keeping each file's shape (reducer +
   cases + test, selectors + test, store + test). Wire `createStores` in AppRoot's `startApp` after the data layer and the error sink, as in
   [examples/app-root.tsx](examples/app-root.tsx) with [examples/app-providers.tsx](examples/app-providers.tsx), add the stores to `test/test-app.tsx`, and fill
   `contracts/stores.json`.
4. New action: add the failing case to `<name>-reducer-cases.ts` first (its test runs it), then the
   union member and the reducer case, then the store method in the order of rule 2.
5. New read: add or reuse a selector; read built values through `useShallow`, as
   [examples/use-tasks-model.ts](examples/use-tasks-model.ts) does, and change state only in handlers.
6. A write that spans stores: name it in `crossStoreWrites`, call it through `updateAndPublish`, and give
   every new store holding rows a `reload` and a line in `updateAndPublish`.
7. Undo: copy `templates/src/stores/session/` and `templates/test/stores/`; the feature creates one
   session store per session in a `useState` initializer, with a `persist` callback that writes
   `toSavedSession(...)` through a repository; restore with `restoreSession` (it comes back paused).
8. Run `npx jest src/stores --ci --maxWorkers=2` and `npm run typecheck`.
9. After changing a persisting store's write order, kill and relaunch a Release build on a named device
   (iOS: `xcrun simctl terminate <udid> <bundle-id>`, then `xcrun simctl launch <udid> <bundle-id>`;
   Android: `adb -s <serial> shell am force-stop <package>`, then
   `adb -s <serial> shell monkey -p <package> -c android.intent.category.LAUNCHER 1`): what the screen
   showed must still be there. persistence-and-migrations' kill test automates the data side.
10. Run the checks from the repo root and fix every `FAIL` line (each names file, rule and fix) until
    both print `RESULT: PASS`.

## Definition of done

- [ ] Every domain store comes from `create<Domain>Store(deps)`, is created once (createStores in the root layout and the test app; a store another skill ships with its own provider, such as the settings store, once by its own opener) and is read through `use<Domain>Store(selector)`; no `create` from zustand, no module-level store outside `osMirrorStores`.
- [ ] Every store method reduces (same object: no write), persists through its port, checks the result, then publishes; failures are returned or recorded; service-fed state (an entitlement) enters through a writing store method; a memory-only store says so.
- [ ] Every reducer is pure with imperative kebab-case actions, has a cases table with a `same: true` case, and a test that runs it.
- [ ] Every selector call returns a primitive or a state reference, or goes through `useShallow`; no selectorless hook, no equality argument.
- [ ] Every write that spans stores is in `contracts/stores.json` and goes through `updateAndPublish`.
- [ ] No `fetch`, React Query or API client in a store, no effect copying query data into one, no `async` in a store, no persist middleware anywhere, no AsyncStorage or MMKV in a store.
- [ ] `npx jest src/stores --ci --maxWorkers=2` passes and `npm run typecheck` is clean.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-reducers.mjs .` prints `RESULT: PASS` (the one expected SKIP: `SKIP src/stores/settings/settings-reducer-cases.ts [reducer-cases-missing] not yet created (settings-and-preferences creates it)`, only in an app that has not yet added that cases file).
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-stores.mjs .` prints `RESULT: PASS`

## Anti-patterns

- **`export const useTasksStore = create(...)`.** A hook-store singleton shares state across tests and is
  created again when Fast Refresh re-runs its module; write a factory and add it to `createStores`.
- **`set(next)` and then the write, or a `setTimeout` "debounced save".** The screen shows unsaved data
  and a kill loses it; persist first, synchronously, then publish.
- **Ignoring the write's result** (`tasks.setDone(id, true); set(next);`). A full disk still shows the
  change; keep the `Result` and return it when it failed.
- **`useListsStore((state) => ({ count: …, failure: … }))`.** A new object every render loops forever in
  Zustand 5; wrap it in `useShallow` or select two primitives.
- **`useTasksStore()` or `useTasksStore((s) => s)` to "get everything".** Both re-render on every
  change; select what is shown.
- **Removing a list with `tasks.removeList(id)` and reloading only the lists store.** The tasks store
  keeps the deleted tasks; use `updateAndPublish`.
- **`useEffect(() => { setTasks(query.data) }, [query.data])`.** Two copies of server data drift; read
  `useQuery` where it is shown and keep only client choices in a store.
- **An `async` store action that fetches and then calls `set`.** Two calls race and the slower one
  wins; fetch with TanStack Query, write locally through a synchronous port.
- **`Date.now()`, `Math.random()` or `randomUUID()` in a reducer.** Pass the time in the action and let
  the repository assign ids; reducers must replay identically.
- **Event-style action names (`task-added`, `onToggle`).** Name the command: `add-task`, `set-done`.
- **Pushing into `state.tasks` or `session.past`.** Spread into new arrays; `check-reducers` deep-freezes
  the input to catch it.
- **A publish-only Premium store (`dispatch: (action) => set(premiumReducer(get(), action))`) fed by a
  purchase service that writes first.** Two writers own one fact and the store cannot report a failed
  write; give the store `grantPremium(entitlement)`, which writes and then publishes.
- **Keeping undo history on disk.** Save the start, the command log and the snapshot; replay on restore.
- **A floating install (`npm install zustand`, `@latest`, a caret range).** It drifts from the verified
  pin and can be younger than the release-age policy; install `zustand@5.0.15` exactly.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/store-pattern.md](references/store-pattern.md) | Store shape, persist orders, entitlements and other service-fed state, composition, actions, reducers and cases tables, selectors and useShallow, cross-store writes, document mode, tests, platform notes, multi-package, checker rules, contract, limits | Workflow step 1, and on any store change |
| [references/state-homes.md](references/state-homes.md) | Where each kind of state lives (server, navigation, forms, UI, preferences, secrets, OS state, sessions) and moving off Redux, Context, MobX or persist + AsyncStorage | Workflow step 1, when choosing a home for state |
| [references/undoable-session.md](references/undoable-session.md) | The undoable session: types, actions, design choices, per-session store, when it is written, save and restore, property tests, the games hand-off | Workflow steps 1 and 7 |
| `templates/src/stores/` | `lists-*` and `tasks-*` reducers, cases tables, selectors and stores with tests; `reducer-cases.ts`; `stores-context.tsx`; `create-stores.ts`; `update-and-publish.ts`; all tests | Workflow steps 3 to 6 |
| `templates/src/stores/session/` | Undoable session types, reducer, per-session store, saved session (save and restore), with tests | Workflow step 7 |
| `templates/test/stores/counter-session-rules.ts` | Tiny session rules and codec the session tests use | Workflow step 7 |
| `templates/contracts/` | `stores.json` (cross-store writes, OS mirror stores) and its JSON schema | Workflow step 3 |
| [examples/use-tasks-model.ts](examples/use-tasks-model.ts) | A model hook reading two stores (primitive, reference and useShallow selectors) and changing state only in handlers | Workflow step 5 |
| [examples/app-root.tsx](examples/app-root.tsx) | Where `createStores` joins the canonical AppRoot's `startApp` | Workflow step 3 |
| [examples/app-providers.tsx](examples/app-providers.tsx) | AppRoot's outer providers with `StoresProvider` after the data layer | Workflow step 3 |
| `scripts/check-stores.mjs` | Static checker of the store rules over `src/`; options `--src-dir`, `--stores-dir`, `--contract` | Workflow step 10, and at the end |
| `scripts/check-reducers.mjs` | Runs every reducer's cases table and the generic invariants, and the session reducer's rules, in Node | Workflow step 10, and at the end |
| `scripts/lib/store-rules.mjs` | check-stores' rules, one function per concern | Never by hand |
| `scripts/lib/store-scan.mjs` | check-stores' text helpers (calls, store initializers, builder selectors) | Never by hand |
| `scripts/lib/reducer-cases.mjs` | check-reducers' case-table runner and generic reducer invariants | Never by hand |
| `scripts/lib/session-checks.mjs` | check-reducers' undoable-session rules with the built-in counter | Never by hand |
| `scripts/lib/source-scan.mjs` | Shared import resolution and code masking, synced from the library (do not edit here) | Never by hand |
| `scripts/lib/app-modules.mjs` | Shared loader of the app's TypeScript in Node, synced from the library (do not edit here) | Never by hand |
| `scripts/check-lib.mjs` | Shared script helper, synced from the library (do not edit here) | Never by hand |
| `scripts/selftest.mjs` | Proves both checkers pass the templates and examples and catch every planted bug | After changing a checker or a template |
| `assets/shared.json` | Declares the synced files above | When adding a shared file |
| `tests/` | `bases/app` (the fixture app) and overlay fixtures (`bad-*`, `pass-*`, `error-*`) for both checkers | When adding a checker rule |

## Related skills

- `persistence-and-migrations` - the repositories, document service and SQLite the stores write through.
- `networking-and-server-state` - server state in TanStack Query over the ApiClient port.
- `settings-and-preferences` - the settings store, its storage port and its provider.
- `react-components-and-hooks` - components and model hooks that read stores.
- `architecture-and-boundaries` - the composition root, ports and where stores sit in the layers.
- `unit-and-component-tests` - render helpers, `test/test-app.tsx` and the store test forms.
- `error-handling-typed-results` - the `Result` every store method returns.
- `accessibility-as-code` - the OS-mirror store for the accessibility switches.
- `game-session-host` - continues, hints and outcomes on top of the undoable session (games).
- `forms-and-input` - form drafts in react-hook-form, not in a store.
- `tdd-workflow` - the test-first loop for every reducer change.
