---
name: error-handling-typed-results
description: Builds a typed Result spine - failures converted at boundaries, exhaustive handling. Use when writing try/catch, .catch or a Result, or fixing swallowed errors or unhandled rejections. Not for error UI (ui-states-and-feedback).
---

# Error handling with typed results

Expected failures travel as typed values (`Result<T, F>` with a `kind` union) that every caller must
handle; only bugs throw, and those land in one global error net and a recording error boundary. No error
path ever destroys the user's data. Two zero-dependency checkers prove what ESLint and `tsc` cannot see.

## Rules that must hold

1. **Expected failures are values; only bugs throw.** Anything that can happen in a correct program (not
   found, offline, storage full, invalid input, cancelled, a corrupt row) returns `Result<T, F>`; a broken
   invariant throws `new Error(message, { cause })`. Why: the type system then forces every caller to handle
   every expected case, and a thrown expected failure crashes a handler or is swallowed by a caller.
2. **One Result type, from `src/core/result.ts`.** `{ ok: true, value } | { ok: false, error }` with `ok`,
   `err`, `attempt`, `attemptAsync`; no second Result/Either and no result library. Why: one vocabulary
   from core to screen; two shapes need adapter code everywhere they meet.
3. **A failure is a kebab-case `kind` with typed params, never text or an Error.** `err({ kind:
   'task-title-taken', title })`; never `err('...')`, `err(new Error())`, `Result<T, string | Error |
   unknown>`, nor a `message` in a failure. Why: a string cannot be switched on exhaustively or translated,
   and baked-in English breaks an Arabic UI.
4. **Convert at the boundary, once.** Adapters, repositories, the ApiClient and parsers catch the vendor's
   error and return the boundary's failure family; no `await` in an adapter escapes outside try/catch or
   `attemptAsync`. Why: above the boundary nobody knows SQLite or StoreKit error shapes, and an escaped
   rejection is dropped silently in release builds.
5. **Every catch maps, records with a fallback, or rethrows with `{ cause }`.** Console-only, comment-only
   and `.catch(() => undefined)` handlers fail; a cosmetic effect may ignore its failure only inside its
   adapter with a `// best-effort: <reason>` comment. Why: nobody reads the console on a user's phone, so
   a swallowed error leaves no trace, and a rethrow without `cause` loses the original stack.
6. **Record the unexpected, with the original error, before returning the failure.** The error log gets
   the raw error; expected failures (user input, offline) are not recorded. Why: after the conversion only
   `{ kind, params }` exists, and a log full of expected failures hides real defects.
7. **Handle every failure exhaustively and never drop a Result.** Branch on `error.kind` with a `switch`
   or a `Record<F['kind'], ...>` table, never an `if/else` whose `else` absorbs future kinds; a call that
   returns a Result is never a bare statement (`if (x) save(t);` included), a `forEach` callback's body or
   an `on*` arrow body. Why: a new kind becomes a compile error everywhere it must be handled, and
   `no-floating-promises` cannot see a dropped `Result`.
8. **The UI shows a message chosen by kind, never `error.message`.** One table per failure family maps
   each kind to a catalog key (params become ICU values) and every key exists in every locale. Why:
   `error.message` is English, technical and can hold user data; a missing key renders a raw id.
9. **One global error net, installed by the root layout's first app import and connected by the
   composition root.** It forwards to the handler it replaced, enables Hermes rejection tracking in every
   build (nothing in the net tests `__DEV__`), buffers until the composition root connects the error log
   (before any provider renders), and calls its sink inside try/catch. Why: React Native 0.86 tracks
   unhandled rejections only in `__DEV__`,
   a module that throws while loading runs before any install call in a module body, and a net nobody
   connects keeps every report in memory until the process ends.
10. **The root route exports an `ErrorBoundary` that records the error and offers one way out.** It never
    retries or navigates away from an effect or a timer, and its fallback stays trivial and reads no
    context that lacks a default. Why: render errors never reach the net (React Native reports them
    straight to its ExceptionsManager) and Expo Router's boundary records nothing, so its `record` is the
    only record; an automatic retry of a repeating render error is a crash loop; and the fallback renders
    outside every provider, where an error it throws is a fatal crash nobody records.
11. **No error path destroys data.** No delete, drop, clear, truncate or reset inside a catch, a `.catch`
    handler or a failure branch; a bad record is quarantined and the rest loads; data newer than the app
    is left untouched. Why: "reset on error" turns a recoverable failure into permanent loss.
12. **A failed user write keeps the input and says so.** The model clears a form only after `ok`; a
    failure becomes a message with a retry; user writes are never fire-and-forget. Why: a silent failed
    save is data loss the user discovers days later.

## Workflow

1. **Choose the mechanism** for each failure with the table in
   [references/result-and-failures.md](references/result-and-failures.md) (section 1): Result, `T | null`,
   throw, boundary or net.
2. **Add the Result module** when `src/core/result.ts` is missing: copy `templates/src/core/result.ts`
   and its test (line 1 names the path). Other skills cite this file; extend it in place (a helper earns
   its place at three call sites, with a test), never with a second Result module.
3. **Design one failure family per boundary**, imitating
   [examples/tasks/task-failure.ts](examples/tasks/task-failure.ts) (sections 4 and 5 of the result
   reference: kinds, params, layering).
4. **Convert at the boundary**: read [references/boundaries-and-catches.md](references/boundaries-and-catches.md),
   imitate [examples/tasks/to-storage-failure.ts](examples/tasks/to-storage-failure.ts) (and its test on
   real `node:sqlite` errors) and [examples/tasks/task-repository.ts](examples/tasks/task-repository.ts) (and its test);
   wrap adapter calls with `attemptAsync`, and a call that can hang with async-safety's
   `withTimeout((signal) => Promise<Result>, afterMs, signal?)` (section 7); a cosmetic adapter follows
   [examples/haptics-adapter.ts](examples/haptics-adapter.ts).
5. **Handle and present**: switch or table on `kind`; add a message table like
   [examples/tasks/task-failure-message.ts](examples/tasks/task-failure-message.ts), put its keys in every
   catalog, and add the per-locale test from [references/test-recipes.md](references/test-recipes.md)
   (section 2). Screens call a void intent of the model hook, never a Result function.
6. **Protect the user's data**: follow [references/never-lose-data.md](references/never-lose-data.md);
   the model keeps input until `ok`, as [examples/tasks/use-add-task-model.ts](examples/tasks/use-add-task-model.ts)
   and its test show.
7. **Install the global net** (once per app): copy `templates/src/services/error-net/` (`error-net.ts`,
   `app-error-net.ts`, `install-error-net.ts`, each with its test); make
   `import '@/services/error-net/install-error-net';` the first app import of `src/app/_layout.tsx`
   (or the line after the Intl polyfills in `index.ts`); connect the error log right after the composition
   root creates the services, in the root layout's `useState` initializer, before any provider renders
   ([examples/root-layout.tsx](examples/root-layout.tsx), [examples/connect-error-log.ts](examples/connect-error-log.ts)).
   Read [references/global-error-net.md](references/global-error-net.md) (section 5 for connecting and
   durability) before changing the net, and section 8 there when the app ships a crash reporter.
8. **Add the root error boundary**: copy `templates/src/features/crash-recovery/`
   (`create-route-error-boundary.tsx`, `crash-screen.tsx`, `crash-fallback.tsx`, their tests). The
   fallback reads no provider: the background from `useTheme()` (its context defaults to the light
   theme) and copy from `createTranslateNow(onError)` in `src/i18n/translate-now.ts`
   (i18n-strings-and-catalogs owns it; it keeps the language the app showed last), wrapped in
   `TextLocaleProvider` with that same `languageNow()` language and `directionOf(language)`, so an RTL
   crash text is laid out right to left (rtl-and-direction's `root-direction-provider`). Put `crash.title`,
   `crash.body` and `crash.restart` in every catalog (`tsc` fails on a missing source key). Export
   `ErrorBoundary` from the root layout with `record` reaching `appErrorNet.report` and
   `restart: () => reloadAppAsync(...)`. The tests import unit-and-component-tests' router helper
   (`test/render-router-with-providers.tsx`) and accessibility-as-code's audit
   (`test/a11y/find-inaccessible-pressables.ts`); when either is missing, set it up with that skill
   first. They render the boundary and the fallback with no provider on purpose, under the documented
   `// no-providers: <why>` marker (section 5 of the test recipes).
9. **Test**: the recipes in [references/test-recipes.md](references/test-recipes.md); then `npm run
   typecheck`, `npx eslint . --max-warnings 0` and `npx jest --ci`.
10. **Run the checkers** from the repo root; look up any rule in
    [references/checker-rules.md](references/checker-rules.md); fix and rerun until both print
    `RESULT: PASS`.
11. **On a device** (once per release candidate, by hand): prove a rejection, a render error and a
    handler error each reach the error log in a release build on a named simulator or emulator (recipe in
    section 10 of the net reference).

## Definition of done

- [ ] `src/core/result.ts` comes from the template (any helper added there, with a test); no other Result/Either type and no result library.
- [ ] Every expected failure is a `kind` union with typed params; no `err('...')`, `err(new Error())`, `Result<T, string | Error | unknown>` or `message` field.
- [ ] Each boundary converts once, records unexpected failures with the original error, and no adapter `await` escapes.
- [ ] Every catch maps, records with a fallback, or rethrows with `{ cause }`; `// best-effort:` appears only in adapters.
- [ ] Failures are handled with a `switch` or a `Record<F['kind'], ...>`; no Result is dropped; handlers call void intents.
- [ ] Every failure family a screen shows has a message table; its keys exist in every locale (per-locale test); no `error.message` in UI.
- [ ] No destructive call on an error path; input survives a failed write (test); quarantine and newer-version outcomes are typed.
- [ ] The net is the root layout's first app import; the composition root connects the error log before any provider renders; the root `ErrorBoundary` records and offers one way out.
- [ ] `npm run typecheck`, `npx eslint . --max-warnings 0` and `npx jest --ci` pass.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-error-net.mjs .` prints `RESULT: PASS`. Allowed only while the root layout is not yet created:
  - `SKIP src/app/_layout.tsx [net-installed] not yet created (app-startup-and-bootstrap creates it)`
  - `SKIP src/app/_layout.tsx [root-boundary] not yet created (app-startup-and-bootstrap creates it)`
  - `SKIP src/app/_layout.tsx [net-connected] not yet created (app-startup-and-bootstrap creates it)`
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-error-spine.mjs .` prints `RESULT: PASS` (allowed: `SKIP src/i18n/catalogs/en.json [failure-message-key] not yet created (i18n-strings-and-catalogs creates it)`).

## Anti-patterns

- **`catch (error) { console.warn(error); return []; }`** - nobody reads the console on a user's phone.
  Map it, record it with a fallback, or rethrow with `{ cause }`.
- **`catch { return null; }`** - a failure turns into "not found" and the error is gone. Return
  `err({ kind })`, or bind the error and record it before the fallback.
- **`err('Could not save')` or `{ kind, message }`** - untranslatable and impossible to switch on.
  Carry the kind and params; the screen picks the message key.
- **`<AppText>{error.message}</AppText>`** - shows English internals (and sometimes user data). Show the
  failure's message key; send the error to the log.
- **Wrapping a whole function in try/catch** - turns typos into "storage unavailable". Wrap the vendor
  call only, with `attempt`/`attemptAsync`.
- **`onPress={() => repository.add(draft)}`** - the Result vanishes into a void handler. Call
  `model.add()`, which handles it.
- **`titles.forEach((title) => repository.add({ id: title, title }))`** - every failed write vanishes.
  Loop with `for...of` and branch on each Result.
- **`if (failure.kind === 'a') ... else ...`** - a kind added later silently lands in the `else`. Use a
  `switch` (lint demands every case) or a `Record<F['kind'], ...>` table.
- **`catch { deleteDatabaseSync(name); }` "to start fresh"** - permanent loss. Keep the file, show the
  failure, open read-only.
- **Resetting the form on submit** - a failed save erases the input. Clear after `ok`.
- **`appErrorNet.install()` in the layout's body** - every import already ran. Use the side-effect
  import first.
- **`if (__DEV__)` anywhere in the net** (around the tracker, the install call or `previous(error,
  isFatal)`) - release builds, the only ones nobody watches, lose rejections or stop crashing on fatal
  errors. The net is the same in every build.
- **`catch { return false; }` around `new URL(raw)` or a feature probe** - looks like a swallowed defect.
  The throw is the answer: `attempt(() => new URL(raw), () => ({ kind: 'invalid-url' }) as const).ok`.
- **A fallback that calls `retry()` in an effect, `setTimeout(onRestart, 3000)` or
  `router.replace('/')` after a delay** - a crash loop when the error repeats. One button, the user decides.
- **A net nobody connects** - every report waits in its buffer until the process ends. Connect the error
  log right after the composition root creates the services.
- **A fallback that calls `useT()` or a store hook** - the providers sit inside the crashed layout, so
  the fallback itself throws, and that crash is never recorded. Read no context that lacks a default
  (`useTheme()` has one); take copy from `createTranslateNow` (`src/i18n/translate-now.ts`).
- **`APP_THEMES` imported for a "static" crash background** - design-system-structure forbids palette
  imports, and the theme context's default already is the light theme. Use `useTheme()`.
- **`record: (error) => { console.warn(error); }`** - the boundary's `record` is the only record of a
  render error; send it to `appErrorNet.report`.
- **A second `ErrorUtils.setGlobalHandler`** - it replaces the net. Report through `appErrorNet`.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/result-and-failures.md](references/result-and-failures.md) | Mechanism table, the Result type and why, attempt/attemptAsync, failure design and layering, exhaustive handling, dropped Results, messages, pitfalls | Workflow steps 1-3 and 5 |
| [references/boundaries-and-catches.md](references/boundaries-and-catches.md) | Where boundaries are, the conversion pattern, verified vendor error shapes (expo-sqlite per platform, node:sqlite, CodedError, fetch), recording, the three catch outcomes, best-effort, timeouts, adapters | Workflow step 4 |
| [references/global-error-net.md](references/global-error-net.md) | What reaches the net (render errors do not), React Native 0.86 dev/release behaviour on iOS and Android, the template net, install order, connecting the log, Expo Router's ErrorBoundary, crash loops, Sentry, web, device proof | Workflow steps 7, 8 and 11 |
| [references/never-lose-data.md](references/never-lose-data.md) | The four data-loss paths, no destructive recovery, keeping input, quarantine, read-only newer data, visible failures, tests | Workflow step 6 |
| [references/test-recipes.md](references/test-recipes.md) | Asserting Results, per-locale message test, mappers on real errors, net and boundary tests, input survival, test-first order | Workflow steps 5 and 9 |
| [references/checker-rules.md](references/checker-rules.md) | Every rule of both checkers, limits, configuration keys (`sourceCatalog`, `resultModule`), multi-package runs, SKIP and NOT APPLICABLE lines | Workflow step 10, on any FAIL line |
| `templates/src/core/result.ts` | The canonical Result module (synced from the library; do not edit here) | Workflow step 2 |
| `templates/src/core/result.test.ts` | Its tests (synced from the library) | Workflow step 2 |
| `templates/src/services/error-net/error-net.ts` | `createErrorNet` and `readGlobalErrorHooks`: chain, rejection tracking, buffer, guarded sink | Workflow step 7 |
| `templates/src/services/error-net/error-net.test.ts` | Its tests with fake hooks | Workflow step 7 |
| `templates/src/services/error-net/app-error-net.ts` | The app's one net instance | Workflow step 7 |
| `templates/src/services/error-net/app-error-net.test.ts` | Its test against jest-expo's real ErrorUtils | Workflow step 7 |
| `templates/src/services/error-net/install-error-net.ts` | The side-effect installer the root layout imports first | Workflow step 7 |
| `templates/src/services/error-net/install-error-net.test.ts` | Its test: installs once, restores | Workflow step 7 |
| `templates/src/features/crash-recovery/create-route-error-boundary.tsx` | Factory for a route's `ErrorBoundary`: records once, one way out | Workflow step 8 |
| `templates/src/features/crash-recovery/create-route-error-boundary.test.tsx` | Unit tests without providers and `renderRouterWithProviders` tests through Expo Router (a throwing route, a throwing root layout) | Workflow step 8 |
| `templates/src/features/crash-recovery/crash-screen.tsx` | The crash fallback view (translated strings and the theme background as props; React Native's `Button`, marked `// press-outside-host:` for ui-component-library) | Workflow step 8 |
| `templates/src/features/crash-recovery/crash-screen.test.tsx` | Its tests: copy, one way out by role and name, no press no call, the accessibility audit | Workflow step 8 |
| `templates/src/features/crash-recovery/crash-fallback.tsx` | The app's root fallback: crash screen with `createTranslateNow` copy, its own `TextLocaleProvider` (language and direction from `languageNow()`) and the `useTheme()` background, no app provider needed | Workflow step 8 |
| `templates/src/features/crash-recovery/crash-fallback.test.tsx` | Its test, rendered with no provider at all (the only proof it survives outside the layout), plus the writing direction per language | Workflow step 8 |
| [examples/tasks/task-failure.ts](examples/tasks/task-failure.ts) | Shape: a failure family and its kinds as data | Workflow step 3 |
| [examples/tasks/to-storage-failure.ts](examples/tasks/to-storage-failure.ts) | Shape: a total mapper from SQLite errors (both expo-sqlite device forms) | Workflow step 4 |
| [examples/tasks/to-storage-failure.test.ts](examples/tasks/to-storage-failure.test.ts) | Shape: the mapper tested on real node:sqlite errors and the iOS and Android message forms | Workflow step 4 |
| [examples/tasks/task-repository.ts](examples/tasks/task-repository.ts) | Shape: a boundary converting once and recording the unexpected (only `tasks.title` is the user's duplicate; a reused id is a recorded defect) | Workflow step 4 |
| [examples/tasks/task-repository.test.ts](examples/tasks/task-repository.test.ts) | Shape: the repository on real SQL: a duplicate title is expected and unrecorded, an id clash is recorded | Workflow step 4 |
| [examples/haptics-adapter.ts](examples/haptics-adapter.ts) | Shape: the one licensed best-effort swallow | Workflow step 4 |
| [examples/tasks/task-failure-message.ts](examples/tasks/task-failure-message.ts) | Shape: kind to message key table with ICU values | Workflow step 5 |
| [examples/tasks/use-add-task-model.ts](examples/tasks/use-add-task-model.ts) | Shape: a model hook that keeps input until `ok` | Workflow step 6 |
| [examples/tasks/use-add-task-model.test.ts](examples/tasks/use-add-task-model.test.ts) | Shape: the input-survives test | Workflow step 6 |
| [examples/root-layout.tsx](examples/root-layout.tsx) | Shape: the root layout's net import, the composition root connecting the log, the `ErrorBoundary` export | Workflow steps 7-8 |
| [examples/connect-error-log.ts](examples/connect-error-log.ts) | Shape: connecting the error log to the net | Workflow step 7 |
| `scripts/check-error-spine.mjs` | Checker: Result module, failure shape and text, catches, causes, adapters, dropped Results, UI messages, catalog keys, destructive recovery | Workflow step 10, definition of done |
| `scripts/check-error-net.mjs` | Checker: one net that forwards, tracks rejections, guards its sink, is installed first and connected; a recording root boundary without auto-retry | Workflow step 10, definition of done |
| `scripts/lib/error-scan.mjs` | Shared scans of both checkers (catch blocks, handlers, failure branches) | Never by hand |
| `scripts/lib/source-scan.mjs` | Lexer and import resolution (synced from the library; do not edit here) | Never by hand |
| `scripts/check-lib.mjs` | Shared checker library (synced from the library; do not edit here) | Never by hand |
| `scripts/selftest.mjs` | Proves both checkers against the fixtures (`node scripts/selftest.mjs`) | After changing a checker |
| `assets/shared.json` | The shared files this skill copies in | When adding a shared file |
| `tests/bases/` | The base app the fixtures assemble with the templates and examples; the canonical error-log port, memory adapter and `src/i18n/translate-now.ts` are synced in (do not edit those copies) | When a fixture needs a new base file |
| `tests/fixtures/` | Overlay cases: good, pass-*, one bad-* per rule, error-* | When adding a rule |

## Related skills

- `typescript-and-lint-rules` - the lint rules this builds on (`switch-exhaustiveness-check`, `only-throw-error`, `no-empty`, `kindValue`); it cites `src/core/result.ts`.
- `architecture-and-boundaries` - ports and adapters, the composition root, the `ErrorLogPort` the net's sink writes to.
- `async-safety` - floating promises, synchronous handlers, `.catch(reportError)`, cancellation.
- `persistence-and-migrations` - the `SqlDriver`, transactions, quarantine in the save-document appendix, and newer-file handling (never touch a file the build cannot use); `run-migration` to ship a schema step.
- `networking-and-server-state` - the ApiClient's HTTP failure family and retries.
- `ui-states-and-feedback` - how a failure message is shown: inline, banner, dialog, retry, Undo.
- `i18n-strings-and-catalogs` - the catalogs the failure-message keys live in, and `src/i18n/translate-now.ts` (`createTranslateNow`), the fallback's t() without a provider.
- `design-system-structure` - `AppText`, `useTheme()` and the theme context's light default the crash screen's background comes from.
- `app-startup-and-bootstrap` - the full startup order around the net import.
- `crash-reporting-and-observability` - Sentry behind `CrashReporterPort`, fed from the net's sink.
- `react-components-and-hooks` - component rules for the fallback and model hooks.
- `forms-and-input` - drafts and field errors that keep input.
- `debug-menu-and-test-hooks` - the test-only triggers for the device proof.
- `unit-and-component-tests` - Jest projects, the render helpers (`renderRouterWithProviders`) and the `no-providers` marker the recipes use.
- `accessibility-as-code` - `findInaccessiblePressables`, the audit the crash screen's test ends with.
- `rtl-and-direction` - the crash fallback's own `TextLocaleProvider` (`languageNow()`, `directionOf`) and its `root-direction-provider` rule.
- `ui-component-library` - why the crash screen's core `Button` carries the `press-outside-host` marker.
- `data-export-and-restore` - backups and all-or-nothing restore.
