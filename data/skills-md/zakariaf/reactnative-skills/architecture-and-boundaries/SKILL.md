---
name: architecture-and-boundaries
description: "Places app code in the src/ layout and checks import boundaries: one-way zones, pure core, ports with fakes, one composition root. Use when adding a file, folder, port or adapter, or on an import error. Not for names (naming-conventions)."
---

# Architecture and boundaries

Keeps an Expo app in a provable shape: every file has one home in the `src/` layout, dependencies point
one way along declared zones, `src/core` is pure, every side effect sits behind a port with an adapter
and an in-memory fake, one composition root creates the adapters, and nothing runs at import time. Two
zero-dependency checkers prove it on every change, on resolved imports, for iOS and Android alike.

## Rules that must hold

1. **Every file has one home.** `src/app` (routes only), `src/features/<feature>/` (screen, model hook,
   components, pure logic, tests beside them), `src/ui`, `src/theme`, `src/core`, `src/services/<concern>/`,
   `src/stores`, `src/data`, `src/api`, `src/i18n`, `src/config`, `src/hooks` (shared cross-feature hooks),
   `src/canvas` (the canvas kit), and `src/games/<game>/` for the games plugin; a `src/**/test-only.ts` gate beside its entry; a web stylesheet in `src/theme/`;
   `assets/<kind>/` at the root for images, fonts and sounds; local Expo modules in `modules/<name>/`;
   `test/`, `__mocks__/`, `scripts/<area>/`, `plugins/`, `contracts/`. Why: an agent finds code by path, and
   a `utils/` or `helpers/` folder becomes the place everything goes. (`folders`, `placement`)
2. **Routes are thin leaves.** Every file in `src/app` default-exports a route (`export default`, or
   `export { SettingsScreen as default } from ...`) that renders a screen from `src/features/` (or only
   redirects); hooks and helpers live elsewhere, and tests in the feature (a route test is
   `src/features/<feature>/<feature>-navigation.test.tsx`); a route other than a `_layout` never imports a
   store, `src/data`, `src/api` or a service and calls no hook but router hooks (`expo-router`) and the ones
   it imports from `src/features/` (no `useState`, `useEffect`, `useQuery`, `useMemo`, shared or local
   hooks); nothing but a test imports a route. Why: Expo Router bundles every file in that folder (verified:
   a test file there shipped in the production bundle), and logic in a route can be neither reused nor
   tested alone. (`route-file`, `route-thin`, `route-leaf`)
3. **Dependencies point one way.** routes → features → shared layers (`ui`, `theme`, `services`,
   `stores`, `data`, `api`, `i18n`, `config`) → `core`. A shared layer never imports a feature, features
   never import each other, and `src/ui` is presentational (no stores, data, api, or services other than
   port types). A game never imports another game and faces only `src/core`, `src/ui`, `src/theme`,
   `src/i18n`, `src/canvas`, port types, its own folder and the seam recorded in `gameFacing`. A deliberate exception is an
   `allowedImports` entry with its reason. Why: a feature or a game can change or disappear without breaking
   another, and UI stays reusable with props. (`layer-direction`, `feature-to-feature`, `ui-presentational`,
   `game-to-game`, `game-facing`)
4. **`src/core` is pure.** No React, React Native, Expo, Skia, Zustand, navigation or i18n library, no Node
   built-in, nothing outside `src/core` (game rules and levels: `src/core` plus their own rules and levels).
   Time and randomness arrive as values. Why: pure code runs the same in Jest, Node tooling and on every
   device, and is the cheapest code to test. (`core-pure`)
5. **Every side effect sits behind a port, and every SDK is classified.** A vendor-neutral type in
   `src/services/<concern>/<concern>-port.ts` (expected failures are `Result` values, never rejections);
   the only importer of the SDK is `<library>-<concern>-adapter.ts` (platform files `*-adapter.ios.ts` and
   `*-adapter.android.ts` count, and so do `*-adapter.ts` files in `src/data/`; subpaths such as
   `expo-sqlite/kv-store` are the SDK); an in-memory `fake-<concern>.ts` with its own test. Every SDK the
   app's runtime code imports is either in `vendorSdks` (behind a port) or in `portlessSdks` (UI building
   blocks and read-only facts, with the reason): every `expo-*`, `react-native-*`, `*-react-native(-*)`,
   `@react-native-*/*` and `@scope/react-native*` or `@scope/*-react-native*` package, any name in the
   contract's `sdkPackagePatterns`, and (when `node_modules` exists) any package that ships native code. A
   local Expo module (`modules/<name>/`) is an SDK too: only its adapter imports it. Pure logic gets no port.
   Why: Jest never touches native code, a vendor swap touches one file, and a new SDK forces a decision
   instead of slipping into a screen. (`vendor-sdk`, `unclassified-sdk`, `port-triple`, `banned-package`)
6. **One composition root creates the adapters; fakes stay in tests.** `createDeviceServices()` builds each
   adapter once; only the root layout imports it, calls it in a `useState` initializer and renders
   `ServicesProvider`; code reads the ports with `useServices()` or receives them as factory arguments; only
   the composition root imports an adapter (the data layer's device opener `src/data/open-device-*.ts` and
   app-startup-and-bootstrap's root-kit registry `src/services/create-root-kits.ts` are part of it). Tests pass fakes through `createTestServices()`, never `jest.mock()` of the app's own
   modules; runtime code never imports a fake or `createTestServices` (the test-only entry may). Context
   carries dependencies, never state that changes. Why: one file lists every outside dependency, a render
   never rebuilds the device, and a test controls exactly the ports it touches. (`adapter-import`,
   `composition-root`, `fake-import`)
7. **Nothing runs at import time.** No module-level database open, adapter or services creation, store
   (a zustand `create`, a vanilla `createStore`, a project factory such as `createTasksStore()`),
   `AudioContext`, direction switch or reload. The only module-level store is an OS mirror: a vanilla store
   with a plain initial state, fed by a platform listener. Why: a reload, a direction change and Fast Refresh re-run
   modules on iOS and Android, so module-level work runs twice and tests share state. (`import-time-work`)
8. **App code never imports Node-world code; Node code loads only neutral files.** `app.config.ts`,
   `plugins/` and `scripts/` run in Node: app code never imports them (not even `import type`) or a Node
   built-in (an npm polyfill the app declares, such as `buffer`, is a package). A `src/` file that Node code
   imports stays neutral: no JSX, no React Native or Expo import, relative imports with the extension.
   Expo Router server code (every `+api` file under `src/app`, the root `+middleware.ts`, contract
   `serverFiles` such as `src/server/**`) runs on the server, never in the native bundle: it may use Node
   built-ins, imports only `src/core`, `src/api`, `src/config`, `src/data`, port types, `expo-server` and
   `expo-router/server`, and app code never imports it. Why: a type-only import drags `process` and
   `node:fs` into the app program, Node ignores tsconfig paths and cannot load Expo modules (verified:
   `expo config` fails), and server code runs where React Native and the device do not exist (the native
   bundle leaves `+api` and `+middleware` out, verified in expo-router 57.0.24).
   (`node-world-import`, `node-builtin`, `node-import`, `no-tooling-import`, `server-boundary`)
9. **Imports resolve and never loop.** No `../` outside Node code (use `./sibling`, `@/` or `@/assets/`), no
   import that resolves to nothing, no cycle among value imports (type-only imports are erased and do not
   count). Why: parent paths hide which zone a file reaches, and a cycle makes a value `undefined` depending
   on which file loads first. (`parent-import`, `unresolved-import`, `import-cycle`)
10. **`require()` is for assets and the test-only gate.** An asset is required by its file
    (`require('@/assets/images/empty-list.png')`, through the alias of rule 11; an extension the app adds
    to Metro's `resolver.assetExts` goes into the contract's `assetExtensions`). Test-only code has one way
    in: a `src/**/test-only.ts` gate beside its entry,
    `process.env.EXPO_PUBLIC_APP_VARIANT === 'production' ? null : require('./test-only-entry')`; nothing
    else imports the entry, code the entry reaches never imports the gate, and other bundled code reaches a
    `testOnlyFolders` folder only through `TEST_ONLY` (a debug route renders `TEST_ONLY?.DebugScreen`;
    `import type` is fine). The forms app-variants-and-environment sanctions pass too: debug tooling behind
    `__DEV__` (Reactotron, `devOnlyRequires`, anywhere in an `if (__DEV__)` block) and another
    `EXPO_PUBLIC_*` inclusion flag at its `require()`. That skill owns the comparison's literal and polarity. Why: one gate is one place to prove the strip, and a module reached
    any other way ships in production (verified on iOS and Android exports). (`test-only-gate`,
    `import-cycle`)
11. **The entry is thin and the aliases exist.** `package.json` `main` is `expo-router/entry` (or an
    `index.ts` that only imports, ending in `expo-router/entry`); `tsconfig.json` maps `@/*` to `src/*`;
    `src/app/_layout.tsx` exists. A folder alias beside `@/*` lives in three places: the root
    `tsconfig.json` (`"@/assets/*": ["./assets/*"]`, the Expo template default; `"@/modules/*":
    ["./modules/*"]`), `jest.config.js` `moduleNameMapper` (`'^@/assets/(.*)$': '<rootDir>/assets/$1'`
    **before** `'^@/(.*)$'`; with no `@/` mapper of its own, jest-expo maps `tsconfig.json` `paths` in their
    order, so list `"@/assets/*"` before `"@/*"` there), and for imports `src/tsconfig.json`. Why:
    startup work belongs in the root layout and the composition root, where it is ordered and testable;
    every rule above assumes the alias; and Jest takes the first mapper that matches, so without the order
    `npm test` fails ("Could not locate module @/assets/... mapped as <rootDir>/src/$1") while tsc, Metro and both
    checkers pass. (`app-entry`, `app-files`)
12. **When multi-package, apps never import each other and packages never import an app.** Workspaces
    `apps/*` + `packages/*`, each package recorded in the contract (`pure`, `world`), packages consumed as
    TypeScript source, one React, every native module in every app at one version. Why: one change in a
    package reaches every app, and autolinking (iOS and Android) sees only an app's own dependencies.
    (`workspaces`, `manifest`, `one-react`, `native-deps`, `app-to-app`, `package-direction`)
13. **Stop and ask before changing the architecture.** A new top-level folder, package, SDK classification,
    ban, game-facing seam or exception is a decision for the developer: it changes
    `contracts/architecture.json` and the same list in `eslint.config.mjs` (a `Gate-Change:` trailer). Why:
    these choices bind every later change.

## Workflow

1. Name the task and read its reference before writing code:

   | Task | Read |
   |---|---|
   | where a file goes; a new folder, screen, feature, API route, local Expo module or kind of file | [references/src-layout-and-placement.md](references/src-layout-and-placement.md) |
   | an import across folders, a boundary lint error, a new SDK, a game's imports, Node code that imports app code, server code, an asset alias, the test-only gate | [references/dependency-zones.md](references/dependency-zones.md) |
   | a new or changed service, adapter, fake, the composition root, testing with fakes | [references/ports-and-adapters.md](references/ports-and-adapters.md) |
   | `contracts/architecture.json`, `rn-skills.config.json`, an exception, a moved folder | [references/contract-and-config.md](references/contract-and-config.md) |
   | a monorepo (apps and packages) | [references/multi-package.md](references/multi-package.md) |

2. **New app or first port.** Copy `templates/src/services/` (the composition root; the clock, error-log
   and direction-guard ports) to `src/services/`, and `templates/contracts/` to `contracts/`. The ports
   import `src/core/result.ts`, `src/core/dates/date-key.ts` and `src/i18n/languages.ts`: copy them from
   `templates/src/` only when the app does not have them yet (their owners are error-handling-typed-results,
   seeded-determinism-and-golden-vectors and i18n-strings-and-catalogs). Mount the root as
   [examples/root-layout.tsx](examples/root-layout.tsx) shows.
3. **New port.** Follow the add-a-port recipe in ports-and-adapters.md: copy the four files of
   `templates/port/` to `src/services/<concern>/` (fill every `__PLACEHOLDER__`; the clock folder is the
   finished example), write the fake and its test first, then the adapter; add the port to `Services`,
   `createDeviceServices` and `createTestServices`; add the SDK to `vendorSdks` in
   `contracts/architecture.json` and to `VENDOR_SDK_PATHS` in `eslint.config.mjs`. A model hook then reads
   it as [examples/use-tasks-model.ts](examples/use-tasks-model.ts) does.
4. **New SDK or file.** Classify every new SDK (`expo-*`, `react-native-*`, `*-react-native`, a package
   with native code) before the first import: a side effect goes to `vendorSdks` (step 3), a UI building
   block or a read-only fact to `portlessSdks` with its reason. Place every file by the placement table
   (images, fonts and sounds in `assets/<kind>/`, API routes as `src/app/**/<name>+api.ts`, a local Expo
   module in `modules/<name>/` behind an adapter); a new kind of file gets a row. The first `@/assets/` (or
   `@/modules/`) import adds the alias in all three places of rule 11 (the SDK 57 template lists `"@/*"`
   first in `tsconfig.json`; move `"@/assets/*"` above it). Let Prettier format filled templates.
5. **Stop and ask** the developer before a new top-level folder, workspace package, SDK classification,
   ban, `gameFacing` seam or `allowedImports` exception (rule 13), then record the decision in
   `contracts/architecture.json`.
6. **Check (validation loop).** When `node_modules` exist: `npm run lint`, `npm run typecheck` and
   `npm test`; after adding an SDK also `npx expo install --check`, `npx expo-doctor` and
   `npm ls react react-native` (one version of each), which catch SDK version drift. Always, from the repo
   root: `node ${CLAUDE_SKILL_DIR}/scripts/check-layout.mjs .` and
   `node ${CLAUDE_SKILL_DIR}/scripts/check-boundaries.mjs .`. Fix every `FAIL` line (file, rule, fix) and
   rerun until both print `RESULT: PASS`.

| Template | Destination in the app repo |
|---|---|
| `templates/src/services/services-context.tsx`, `create-device-services.ts`, `create-test-services.ts` (+ tests) | `src/services/` (the composition root) |
| `templates/src/services/clock/`, `error-log/`, `direction-guard/` | `src/services/clock/`, `error-log/`, `direction-guard/` as they are |
| `templates/port/port.ts`, `vendor-port-adapter.ts`, `fake-port.ts`, `fake-port.test.ts` | `src/services/<concern>/<concern>-port.ts`, `<library>-<concern>-adapter.ts`, `fake-<concern>.ts`, `fake-<concern>.test.ts` |
| `templates/contracts/architecture.json`, `architecture.schema.json` | `contracts/` |
| `templates/src/core/result.ts`, `templates/src/core/dates/date-key.ts`, `templates/src/i18n/languages.ts` | the same paths, only when missing |

## Definition of done

- [ ] Every new file sits where the placement table says; a new kind of file got a row, and a new
      top-level folder, package, SDK classification, ban, seam or exception was approved and recorded in
      the contract.
- [ ] Route files only render a feature screen (or redirect), calling only router hooks and the feature's; a feature's model
      hook is the code that reads stores and services; `src/ui` receives data through props; `src/core` imports only `src/core`; a game imports
      no other game and only what it faces.
- [ ] Every new outside service has its port, adapter, fake and fake test, is a member of `Services`, is
      created once in `createDeviceServices()` (called by the root layout's `useState` initializer) and stands
      in through `createTestServices()` in tests; every SDK the app imports is in `vendorSdks` or
      `portlessSdks`; no runtime file imports a fake or `createTestServices`.
- [ ] Assets are required from `assets/<kind>/` through `@/assets/`, mapped in `tsconfig.json` and ahead of
      `@/` for Jest; test-only code is required only by a `src/**/test-only.ts` gate (debug tooling behind
      `__DEV__` and other inclusion flags as app-variants-and-environment allows), and a `testOnlyFolders`
      folder is reached only through `TEST_ONLY`.
- [ ] API routes and middleware import no app runtime module or UI; nothing bundled imports them.
- [ ] No module-level side effect; no Node-world import in app code; files Node code imports are neutral.
- [ ] `npm run lint`, `npm run typecheck` and `npm test` pass; after a new SDK, `npx expo install --check`
      and `npx expo-doctor` pass and `npm ls react react-native` shows one version of each.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-layout.mjs .` prints `RESULT: PASS`.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-boundaries.mjs .` prints `RESULT: PASS`

Neither checker prints SKIP lines. Without `contracts/architecture.json` each prints one `note:` line and
applies the defaults; a multi-package repo needs the contract. In a repo where no app depends on `expo`,
check-layout prints `NOT APPLICABLE: expo is not a dependency in package.json` (a pass).

## Anti-patterns

- **A `utils/`, `helpers/` or `components/` folder under `src/`.** Pure logic goes to `src/core` or its
  feature, shared UI to `src/ui`, a hook beside the feature that uses it (`src/hooks/` only once two
  features share it).
- **A route that holds its screen** (`useState`, `useEffect`, a `FlatList` and a `fetch` in
  `src/app/explore.tsx`, as the SDK 57 template ships it). Move it to `src/features/<feature>/` with its
  model hook; the route renders it.
- **`const services = createDeviceServices()` in a component or hook.** Each render builds a new device;
  the root layout's `useState(createDeviceServices)` builds it once.
- **A helper, hook or test next to the routes.** Expo Router makes it a route and bundles it; keep
  `src/app` to route files, and test screens and routes in `src/features/` (`<feature>-navigation.test.tsx`).
- **A screen that imports `expo-iap` (or `expo-sqlite/kv-store`, which ESLint's bare-name ban misses).**
  Take the port from `useServices()`; only the adapter imports the SDK.
- **Importing an adapter "just this once" from a store or a model hook.** It hard-wires the device into
  the code and the test; ask for the port and let the composition root decide.
- **`jest.mock('@/services/...')` for the app's own modules.** Pass a fake through `createTestServices()`;
  root `__mocks__/` exist only for vendor SDKs that crash on import.
- **`import type` from `app.config.ts`, `plugins/` or `scripts/` "because it is only a type".** It still
  pulls Node into the app program; move the type to a neutral file in `src/config/`.
- **A debug route that re-exports the debug screen** (`export { DebugScreen as default } from ...`). Expo
  Router bundles it, so the debug folder ships; import `TEST_ONLY` and render `TEST_ONLY?.DebugScreen`.
- **A `require()` of test-only code outside `src/**/test-only.ts`, behind an imported `IS_TEST_BUILD`.**
  Metro keeps the module in production bundles; reach it through the gate's `TEST_ONLY`, whose literal
  comparison app-variants-and-environment checks.
- **`import logo from './logo.png'` or an image under `src/`.** There is no module to import; keep it in
  `assets/images/` and write `require('@/assets/images/logo.png')`.
- **An `expo-*` import with no decision behind it.** Classify it first (`vendorSdks` with a port, or
  `portlessSdks` with the reason); "it is only one call" is how SDKs end up in screens.
- **An API route that imports a store, a screen helper or `react-native`.** It runs on the server; share
  schemas through `src/api/` and logic through `src/core/`, and let the app call the route over HTTP.
- **`import { start } from '@/modules/live-activity'` in a model hook.** A local Expo module is native
  code: put it behind a port and import it only from the adapter.
- **`export const useTasksStore = create(...)`, `export const listsStore = createTasksStore()` or
  `const db = openDatabaseSync(...)` at module level.** Create stores and adapters in factories the root
  layout calls once.
- **A game importing a store, `useServices()` or another game.** The host hands values in through the
  seam; shared pieces move to `src/core` or `src/ui`.
- **Feature A reaching into feature B's files to save a copy.** Move the shared piece down
  (`src/ui`, `src/core`, `src/stores`) or navigate to B's route.
- **A port for pure code.** Ports wrap what cannot run in Jest (SDKs, device APIs, time); a pure function
  stays a function in `src/core`.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/src-layout-and-placement.md](references/src-layout-and-placement.md) | The tree, what each folder holds and imports, the placement table (assets, the test-only gate), route files, the add-a-feature and add-a-folder recipes | Workflow step 1 (placement) |
| [references/dependency-zones.md](references/dependency-zones.md) | The zone graph, what each zone may import, games, what enforces each edge (ESLint and checker), classifying SDKs, Node world and neutral files, assets and `require()`, the test-only gate (verified forms), cycles | Workflow step 1 (imports) |
| [references/ports-and-adapters.md](references/ports-and-adapters.md) | Why ports and when not, the port/adapter/fake anatomy, `Result`, the composition root, injection and testing rules, platform differences, the add-a-port recipe | Workflow steps 1 to 3 |
| [references/contract-and-config.md](references/contract-and-config.md) | Every key of `contracts/architecture.json` and `rn-skills.config.json`, the defaults, exceptions with reasons | Workflow steps 1 and 5 |
| [references/multi-package.md](references/multi-package.md) | When multi-package: workspaces, manifests, TypeScript-source packages, one React, native modules, zones across workspaces | Workflow step 1 (monorepo) |
| `templates/src/services/services-context.tsx` | `Services`, `ServicesProvider`, `useServices()` (the composition-root files and their tests are synced from the library; this skill owns them) | New app; a new port |
| `templates/src/services/services-context.test.tsx` | Its tests (provider, missing provider) | With the context |
| `templates/src/services/create-device-services.ts` | The composition root: every device adapter, once | New app; a new port |
| `templates/src/services/create-device-services.test.ts` | Its tests | With the composition root |
| `templates/src/services/create-test-services.ts` | Test services: the given fakes, and stand-ins that throw on first use | New app; a new port |
| `templates/src/services/create-test-services.test.ts` | Its tests | With it |
| `templates/src/services/clock/` | `ClockPort`, the system adapter, the fake and their tests (synced from the library; do not edit here) | New app; the finished example of a port |
| `templates/src/services/error-log/` | `ErrorLogPort`, the in-memory adapter, the fake and their tests (synced from the library; do not edit here) | New app |
| `templates/src/services/direction-guard/` | `DirectionGuardPort`, its `expo-sqlite/kv-store` adapter, the fake and its test (synced from the library; rtl-and-direction owns it; do not edit here) | New app |
| `templates/port/` | `port.ts` (a vendor-neutral port type, placeholders), `vendor-port-adapter.ts` (the only SDK importer, errors mapped to values), `fake-port.ts` (the in-memory fake with a call counter) and `fake-port.test.ts` | A new port |
| `templates/contracts/architecture.json` | The app's starting architecture contract | New app; an architecture decision |
| `templates/contracts/architecture.schema.json` | Its JSON schema (editor help and the key reference) | With the contract |
| `templates/src/core/result.ts` | `Result`, `ok`, `err`, `attemptAsync` the port templates use (synced from the library; error-handling-typed-results owns it) | Only when the app has none |
| `templates/src/core/dates/date-key.ts` | Calendar-day keys the clock uses (synced from the library; seeded-determinism-and-golden-vectors owns it) | Only when the app has none |
| `templates/src/i18n/languages.ts` | The app's languages and the `Direction` type the guard uses (synced from the library; i18n-strings-and-catalogs owns it) | Only when the app has none |
| [examples/root-layout.tsx](examples/root-layout.tsx) | The root layout mounting the composition root | Workflow step 2 |
| [examples/use-tasks-model.ts](examples/use-tasks-model.ts) | A feature model hook reading ports and a store | Workflow step 3 |
| [examples/architecture-multi-package.json](examples/architecture-multi-package.json) | A contract for a repo with apps and packages | Multi-package repos |
| `scripts/check-boundaries.mjs` | Resolves every import (TypeScript and JavaScript) and checks zones, thin routes (imports and hooks), games, purity, vendor and unclassified SDKs, bans (with the install policy's `doNotAdd`), local Expo modules, adapters and the services factories, fakes, Node world, server code, `require()` and the test-only gate (its entry and `testOnlyFolders`), `../`, unresolved imports and cycles | Workflow step 6 |
| `scripts/check-layout.mjs` | Checks folders, route files, port triples, the composition root and how the root layout mounts it (directly or through an imported startup helper), placement, import-time work (OS mirrors allowed; with or without semicolons), the entry, the aliases (tsconfig and Jest order, explicit or derived by jest-expo), and the multi-package manifests | Workflow step 6 |
| `scripts/lib/architecture.mjs` | Defaults + contract + layout, and the zone of every file | Only when changing a checker |
| `scripts/lib/import-graph.mjs` | Builds and resolves the import graph, Node-world reach, cycles | Only when changing a checker |
| `scripts/lib/source-scan.mjs` | Dependency-free lexer and import resolver (synced from the library; do not edit here) | Only when changing a checker |
| `scripts/check-lib.mjs` | Shared script helper (synced from the library; do not edit here) | Never by hand |
| `scripts/selftest.mjs` | Proves both checkers pass the good fixtures and catch every planted bug | After changing a checker or the defaults |
| `assets/architecture-defaults.json` | The default folders, SDK name patterns, vendor and portless SDKs, bans, adapter, composition-root, game-facing, Node-world and server globs, the server packages, the local-modules folder, the gate's variant, the asset extensions | When a default changes (with eslint.config.mjs) |
| `assets/template-placeholders.json` | Values that fill the port templates in the template harness | When the port templates change |
| `assets/shared.json` | Declares the shared files this skill copies in | When adding a shared file |
| `tests/` | The Tasks-app and multi-package bases and the planted-bug cases (overlay format) | When adding a rule to a checker |

## Related skills

- `typescript-and-lint-rules` - the ESLint zones, vendor and ban lists, and the two TypeScript programs.
- `naming-conventions` - names of the files, ports, adapters and fakes placed here.
- `expo-project-bootstrap` - creating the app with this layout from empty.
- `error-handling-typed-results` - the `Result` type and failure kinds ports return.
- `persistence-and-migrations` - the `SqlDriver` port, repositories and a persistent error-log adapter.
- `state-management-zustand` - stores made by factories and created once.
- `app-startup-and-bootstrap` - the order of work in the root layout around the composition root.
- `unit-and-component-tests` - `renderWithProviders` over `createTestServices()`; route tests with `renderRouterWithProviders`.
- `app-variants-and-environment` - the gate's literal comparison, inclusion flags, `devOnlyRequires`, the bundle proof.
- `dependency-management` - `contracts/dependency-policy.json`, whose `doNotAdd` this skill also bans.
- `debug-menu-and-test-hooks` - what the test-only entry exports.
- `expo-prebuild-and-config-plugins` - `app.config.ts` and local config plugins in `plugins/`.
- `navigation-and-routing` - route files, layouts and typed routes.
- `game-session-host` - the games plugin's seam between a game module and the app; it records the seam's
  files in `gameFacing`.
- `accessibility-as-code` - the OS mirror store (`src/ui/a11y/system-a11y-store.ts`) rule 7 allows.
- `react-components-and-hooks` - the shared cross-feature hooks in `src/hooks/`.
- `skia-canvas-rendering` - the canvas kit in `src/canvas/`.
- `native-modules-and-new-architecture` - writing the local Expo module that `modules/<name>/` holds.
- `web-support` - API routes, EAS Hosting and the web stylesheet.
- `ota-updates` - the `UpdatesPort` over `expo-updates`.
