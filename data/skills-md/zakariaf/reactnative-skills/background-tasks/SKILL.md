---
name: background-tasks
description: "Builds expo-background-task jobs: idempotent, budgeted runs. Use when adding periodic sync, TaskManager.defineTask, leaving expo-background-fetch, or a background task never runs. Not for reminders (local-notifications)."
---

# Background tasks

Work outside the foreground is a short, idempotent job that the system may run, cut short, repeat or
never run at all, on iOS (BGTaskScheduler) and Android (WorkManager) alike. Every task is defined
where a headless launch can find it, goes through one runner that applies a budget and never throws,
is scheduled through a port with one explicit interval, also runs on a foreground path, and leaves a
durable run record. A zero-dependency checker proves the parts tsc, ESLint and Jest cannot see.

## Rules that must hold

Verified on 2026-10-14 against `expo-background-task` and `expo-task-manager` 57.0.21 (source,
introspection and the Expo SDK 57 pages; device behaviour is from the platform docs, see
references/platform-behaviour.md).

1. **Use expo-background-task, and list its config plugin.** No `expo-background-fetch` (deprecated,
   no patches); `'expo-background-task'` is in the app config plugins and the native snapshot shows
   `UIBackgroundModes` `processing` and the identifier `com.expo.modules.backgroundtask.processing`.
   Why: prebuild does not apply this plugin on its own in SDK 57 (introspected), and without
   `processing` every registration rejects on an iOS device. (`no-background-fetch`,
   `background-plugin`, `background-plist`)
2. **Define every task at module scope, in a file the app entry imports.** `TaskManager.defineTask`
   lives only in `define-background-tasks.ts`, at top level, and `index.ts` (`package.json` `main`)
   imports it after the Intl polyfills and before `'expo-router/entry'`. Why: an Android run in a
   stopped process evaluates the bundle with the headless loader and renders no route, and a task that
   fires undefined is unregistered for good. (`define-task-top-level`, `define-task-entry`)
3. **A job's name is one literal, declared once.** `defineBackgroundJob({ name: '<area>.<job>' })`,
   kebab-case, unique; every other call uses `job.name`. Why: a literal at a call site drifts from the
   definition, and two definitions of one name overwrite each other. (`job-name`, `task-name-literal`)
4. **Every executor is `toTaskExecutor(job, createBackgroundEnvironment)`**, for notification and
   location tasks too (their `data` and `error` reach the job as `input` and `error`). Why: the task
   manager only `console.error`s a rejected executor; the runner turns a throw into a recorded
   `crashed` run with its cause in the durable background error log (kv-store, read later by the
   debug screen), records it as a `background` run, disposes the environment, maps the end to
   `BackgroundTaskResult` and never rejects. (`executor-through-runner`)
5. **Every job has a literal budget of at most 25 s and asks `shouldStop()` before each step.** Why:
   the system may end a run at any moment (iOS expiry, Android stopping the worker) and 25 s is this
   library's design default, and only the job can stop cleanly between steps; the runner aborts the signal at the budget and records `timed-out`.
   (`job-budget`, runner tests)
6. **Jobs are idempotent and resumable, and their test proves both.** Idempotency keys on every
   external effect, state transitions instead of increments, one commit per step, progress in storage;
   the sibling test calls `runJobTwice` and `runJobUntilAborted`. Why: runs repeat (expiry after the
   server applied a change) and die between any two instructions. (`job-tested`)
7. **Jobs run without React.** A job imports no React, React Native, router, store, feature, ui or
   context module; it receives ports and repositories in `BackgroundDeps`, created per run by
   `createBackgroundEnvironment()`. Why: a headless run has no providers, and on iOS the root layout
   may not have created its services when the task fires. (`job-no-react`)
8. **A background run never migrates, and gets the database from the data layer.** The data layer's
   background open path opens its own connection only when the version equals the latest and returns
   repositories (never the driver); otherwise the job returns `deferred` (`schema-behind`). Why: a
   migration there can be cut mid-step, races the foreground start, and fails where nobody sees it;
   a shared connection closed in `dispose` would close the app's. (`job-no-migrate`)
9. **Only the adapter and the registry import the SDKs.** App code schedules through
   `BackgroundTasksPort`; tests read the SDK with `jest.requireMock`/`requireActual`. Why: one file
   per vendor surface, and Jest never touches native code. (`vendor-import-confined`)
10. **One explicit interval of at least 15 minutes, registered by `reconcileBackgroundTasks` after
    startup.** The reconcile honours `availability` and the user's setting, removes names the build no
    longer defines and re-registers a changed interval. Why: all jobs share one system worker (the last
    registration sets the interval), the defaults differ (12 h iOS, 24 h Android), and
    `registerTaskAsync` keeps an existing registration. (`minimum-interval`, reconcile tests)
11. **Every job also runs on a foreground path, through the same runner, as a `foreground` run.** App
    active, after a write, pull to refresh: `runBackgroundJob(job, environment, { trigger:
    'foreground' })`. Why: the system may never grant a background run (restricted device, Low Power
    Mode, an iOS force-quit), the runner's single flight stops the two from overlapping, and the run
    log keeps the two triggers apart. (`job-foreground-path`)
12. **The test trigger is debug-only, and the device proof is done.** `triggerTaskWorkerForTestingAsync`
    only through `triggerBackgroundRunForTesting()` (returns false unless `__DEV__`); every new job is
    forced once on a named Android emulator (`adb -s`) and on an iOS device, and
    `lastRun(name, 'background')` shows a run newer than the trigger (a `foreground` record never
    counts). Why: in a release build the trigger does nothing (the SDK resolves false outside
    `__DEV__`), so a debug control left in silently does nothing; the iOS simulator has no background
    tasks, and only a device proves the headless path and the configuration. (`trigger-dev-only`, references/testing-and-device-proof.md)

## Workflow

1. **Decide whether it is background work at all**: read
   [references/api-and-config.md](references/api-and-config.md) section 1. A reminder at a time is a
   local notification, a server event is a push, freshness on open is the foreground path.
2. **Learn the platform limits** before designing: [references/platform-behaviour.md](references/platform-behaviour.md)
   (one worker, network required, budgets, headless runs, force-quit, intervals, simulator).
3. **Install and configure**: `npx expo install expo-background-task expo-task-manager`; add
   `'expo-background-task'` to the app config plugins; regenerate the native snapshot
   (expo-prebuild-and-config-plugins); add the contract entries and ESLint vendor lines of
   api-and-config.md section 6. Remove `expo-background-fetch` if present (section 8).
4. **Copy the templates** at the paths their first lines name: `templates/src/services/background-tasks/`,
   `templates/src/services/background-run-log/`, `templates/test/background/`. They pass tsc, ESLint
   and Jest in the reference app.
5. **Wire the entry**: add `import '@/services/background-tasks/define-background-tasks';` to
   `index.ts` after the Intl polyfills, before `'expo-router/entry'` (`examples/index.ts`). An app
   whose `main` is `expo-router/entry` gets an `index.ts` first.
6. **Write the job** from [references/job-design.md](references/job-design.md), imitating
   `examples/sync-outbox-job.ts`: `defineBackgroundJob`, a literal name and budget, a bounded batch,
   `shouldStop()` before each step, outcomes with kebab-case reasons.
7. **Test the job first** with `test/background/job-test-kit.ts` (`runJobTwice`, `runJobUntilAborted`,
   the job's own failure modes), imitating `examples/sync-outbox-job.test.ts` and
   [references/testing-and-device-proof.md](references/testing-and-device-proof.md) section 2.
8. **Register it**: add it to `BACKGROUND_JOBS` and its dependencies to `BackgroundDeps` and
   `createBackgroundEnvironment()` (`examples/background-jobs.ts`, `examples/background-environment.ts`).
   A job that needs the app database gets repositories from the data layer's background open path
   (`examples/open-background-data.ts` at `src/data/open-background-data.ts`: own connection, current
   schema only, closed in `dispose`), listed in `contracts/persistence.json` `sqlAllowed`
   (api-and-config.md section 6).
9. **Schedule after startup**: call `reconcileBackgroundTasks` from a hook the root runs once startup
   is ready and when the setting changes (`examples/use-background-registration.ts`, with its test);
   show `restricted` as unavailable in the setting row.
10. **Add the foreground path**: run the same job through `runBackgroundJob(job, environment,
    { trigger: 'foreground' })` on app active or after a write, importing the job or the job list
    (`examples/use-sync-outbox-on-foreground.ts`, with its test).
11. **Run the checks**: `npm run typecheck`, `npm run lint`, `npx jest <changed tests> --ci`, then
    `node ${CLAUDE_SKILL_DIR}/scripts/check-background-tasks.mjs .`. Fix each `FAIL` line
    ([references/checker-rules.md](references/checker-rules.md) explains every rule) and rerun until
    `RESULT: PASS`.
12. **Prove it on devices**: force a run on a named Android emulator with `adb -s <serial>` (also with
    the process killed) and on an iOS device from the debug menu or LLDB; read the newest
    `background` record of each job (testing-and-device-proof.md sections 3 to 5). The developer signs
    and installs the iOS build.

## Definition of done

- [ ] `expo-background-task` and `expo-task-manager` installed with `npx expo install`; no `expo-background-fetch`.
- [ ] `'expo-background-task'` listed in the app config; the native snapshot shows `processing` and the identifier.
- [ ] `define-background-tasks.ts` defines every job at module scope; `index.ts` imports it before `'expo-router/entry'`.
- [ ] Every job: `defineBackgroundJob` with a literal `<area>.<job>` name and a budget of at most 25 s, `shouldStop()` before each step, idempotency keys, one commit per step.
- [ ] Every job's sibling test calls `runJobTwice` and `runJobUntilAborted`, plus its own failure modes.
- [ ] Jobs import no React, router, store, feature, ui or context module and never migrate.
- [ ] Scheduling goes through `reconcileBackgroundTasks` after startup, with one interval of at least 15 minutes and the user's setting.
- [ ] Every job also runs on a foreground path through `runBackgroundJob` with `{ trigger: 'foreground' }`.
- [ ] The registration hook and the foreground hook each have a test (setting off unregisters, restricted and failed reach the row, no foreground run while inactive, `overlapping` during a background run).
- [ ] The background environment records into the durable background error log; a job that needs the database gets repositories from `src/data/open-background-data.ts` (listed in `sqlAllowed`), never the driver.
- [ ] The contract entries (architecture-and-boundaries) and ESLint vendor lines are in place.
- [ ] Copied templates pass `npm run typecheck`, `npm run lint` and their Jest tests.
- [ ] A forced run on a named Android emulator and on an iOS device leaves, for each job, a `lastRun(name, 'background')` record newer than the trigger with `done`, `partial` or `deferred`.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-background-tasks.mjs .` prints `RESULT: PASS` (allowed: the note `background-plist not applied` before the native snapshot exists; the SKIP `app.config.ts [background-plugin] not yet created (expo-project-bootstrap creates it)` only before an app config exists; `NOT APPLICABLE` only without the three packages).

## Anti-patterns

- **`TaskManager.defineTask` inside a component, a hook or `useEffect`.** It is never defined in a
  headless run, and the task manager unregisters the task the first time it fires. Module scope of the
  registry, imported by the entry.
- **Expecting "every 15 minutes".** Intervals are minimums; iOS runs in windows, often overnight.
  Copy says "when your phone allows it"; time-critical work is a notification or a push.
- **A job that loops until nothing is left.** It outruns the window and is killed mid-write. A bounded
  batch, `partial`, and the next run.
- **"Send all, then mark all as synced".** A cut run resends everything without idempotency keys, or
  loses track with them. One commit per step.
- **Reading a Zustand store or `useServices()` from a job.** Undefined in a headless run, stale on iOS.
  `BackgroundDeps` from the background environment.
- **Running migrations because the job needs the new table.** Defer with `schema-behind`; the
  foreground start migrates.
- **Registering at import time, or on every render.** A native call before the first frame, repeated.
  `reconcileBackgroundTasks` once after startup and when the setting changes.
- **Changing `minimumInterval` and expecting it to apply.** `registerTaskAsync` keeps the old
  registration; the reconcile unregisters and registers.
- **`unregisterAllTasksAsync()` on sign-out.** It also removes location and notification tasks.
  Reconcile with `isEnabled: false`.
- **Testing on the iOS simulator and concluding "it never runs".** The simulator has no
  BGTaskScheduler (`Restricted`). A device, or the Android emulator.
- **Taking any fresh run log entry as the device proof.** Opening the app to read it runs the
  foreground path, which records a run too. Read `lastRun(name, 'background')` only.
- **Opening a database connection per run and leaving it open.** A warm process piles them up.
  Close it in the environment's `dispose`.
- **Opening the background connection without `useNewConnection`, or in the environment.** It may be
  the app's own connection, and `dispose` closes it under the UI; and SQL outside `src/data/` fails
  persistence-and-migrations. The data layer's background open path, with its own connection.
- **An in-memory error log in the background environment.** The run's process dies with the cause of
  a crash in it. The kv-store background error log the template wires.
- **`triggerTaskWorkerForTestingAsync()` behind a button in every build.** Debug builds only, through
  `triggerBackgroundRunForTesting()`, from the debug menu; on Android use `adb`.
- **Trusting `addExpirationListener` to save state.** In 57.0.21 it may never fire; commit per step.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/platform-behaviour.md](references/platform-behaviour.md) | iOS and Android behaviour with sources: one worker, run conditions, budgets, headless runs, force-quit, intervals, simulator and Expo Go | Workflow step 2; a run that never happens |
| [references/api-and-config.md](references/api-and-config.md) | Choosing the mechanism, install, the config plugin (not auto-applied), the SDK 57 API, contract and ESLint entries, privacy, moving off expo-background-fetch, multi-package | Workflow steps 1 and 3 |
| [references/job-design.md](references/job-design.md) | The job contract: idempotent, resumable, bounded, outcomes, single flight, the environment, the database, reconcile and settings, the run log, battery | Workflow steps 6 to 10 |
| [references/testing-and-device-proof.md](references/testing-and-device-proof.md) | Jest recipes, the Android emulator proof with `adb -s`, the iOS device proof, reading the run log, limits of automation | Workflow steps 7 and 12 |
| [references/checker-rules.md](references/checker-rules.md) | Every checker rule, scope, configuration, limits and the verification record | Workflow step 11; a finding you disagree with |
| `templates/src/services/background-tasks/background-job.ts` | `defineBackgroundJob`, `runBackgroundJob` (trigger, budget, single flight, crash recording, run log), `stopRunningJobs`, `isSuccessfulEnd` | Workflow step 4 |
| `templates/src/services/background-tasks/background-job.test.ts` | Runner tests: outcomes, crash, overlap, budget with fake timers, stop | Workflow step 4 |
| `templates/src/services/background-tasks/task-executor.ts` | `toTaskExecutor`: the only executor shape (background trigger, task data and error, dispose), `TASK_RESULT` | Workflow step 4 |
| `templates/src/services/background-tasks/task-executor.test.ts` | Pins `TASK_RESULT` to the SDK enum; never rejects; disposes after a crash and a timeout | Workflow step 4 |
| `templates/src/services/background-tasks/background-tasks-port.ts` | `BackgroundTasksPort`: availability, scheduled, register, unregister | Workflow step 4 |
| `templates/src/services/background-tasks/expo-background-tasks-adapter.ts` | The adapter on expo-background-task and expo-task-manager; `watchBackgroundExpiry`, `triggerBackgroundRunForTesting` | Workflow step 4 |
| `templates/src/services/background-tasks/expo-background-tasks-adapter.test.ts` | Adapter tests on mocked SDKs (iOS project) | Workflow step 4 |
| `templates/src/services/background-tasks/expo-background-tasks-adapter.android.test.ts` | The expiry subscription is iOS-only (Android project) | Workflow step 4 |
| `templates/src/services/background-tasks/fake-background-tasks.ts` | In-memory port for tests: schedule, call log, availability, failures | Workflow steps 7 and 9 |
| `templates/src/services/background-tasks/fake-background-tasks.test.ts` | Its tests | Workflow step 4 |
| `templates/src/services/background-tasks/reconcile-background-tasks.ts` | `reconcileBackgroundTasks`, `MIN_INTERVAL_MINUTES` | Workflow step 9 |
| `templates/src/services/background-tasks/reconcile-background-tasks.test.ts` | Orphans, changed interval, disabled, restricted, failure, bad interval | Workflow step 9 |
| `templates/src/services/background-tasks/background-jobs.ts` | The app's job list, `BackgroundDeps`, `BACKGROUND_INTERVAL_MINUTES` (the app fills it) | Workflow step 8 |
| `templates/src/services/background-tasks/background-jobs.test.ts` | Unique names, budgets within the cap, interval at the floor or above | Workflow step 8 |
| `templates/src/services/background-tasks/background-environment.ts` | The composition root of a background run (device-only) | Workflow step 8 |
| `templates/src/services/background-tasks/define-background-tasks.ts` | The task registry the entry imports | Workflow steps 4 and 5 |
| `templates/src/services/background-tasks/define-background-tasks.test.ts` | Every job defined at import; one expiry subscription | Workflow step 4 |
| `templates/src/services/background-run-log/background-run-log-port.ts` | `BackgroundRunLogPort` (`lastRun(name, trigger)`), `BackgroundRunRecord`, `RunEnd`, `RunTrigger` | Workflow step 4 |
| `templates/src/services/background-run-log/kv-background-run-log-adapter.ts` | The run log on `expo-sqlite/kv-store` | Workflow step 4 |
| `templates/src/services/background-run-log/kv-background-run-log-adapter.test.ts` | Its tests (newest per job and trigger, foreground never overwrites background, unreadable, failing storage) | Workflow step 4 |
| `templates/src/services/background-run-log/kv-background-error-log-adapter.ts` | The durable error log of background runs on `expo-sqlite/kv-store` (newest 50, memory fallback) | Workflow step 4; reading why a run crashed |
| `templates/src/services/background-run-log/kv-background-error-log-adapter.test.ts` | Its tests, including a crashed run read back by another adapter instance | Workflow step 4 |
| `templates/src/services/background-run-log/fake-background-run-log.ts` | In-memory run log for tests | Workflow step 7 |
| `templates/src/services/background-run-log/fake-background-run-log.test.ts` | Its test | Workflow step 4 |
| `templates/test/background/job-test-kit.ts` | `runJobOnce`, `runJobTwice`, `runJobUntilAborted` (each takes the task body's input and error) | Workflow step 7 |
| `templates/test/background/job-test-kit.test.ts` | The kit on a counter job | Workflow step 4 |
| `examples/sync-outbox-job.ts` | A Tasks outbox sync job: idempotency keys, one commit per step, outcomes, permanent rejections set aside | Workflow step 6 |
| `examples/sync-outbox-job.test.ts` | Its tests: twice, cut mid-run, cut between send and commit, poison change, retryable rejection, schema behind | Workflow step 7 |
| `examples/background-jobs.ts` | The job list with the outbox job | Workflow step 8 |
| `examples/background-environment.ts` | The environment with the database from the data layer (closed in `dispose`) and a durable error log either way | Workflow step 8 |
| `examples/open-background-data.ts` | The data layer's background open path: own connection, current schema only, pragmas, repositories and the SQLite error log, never the driver | Workflow step 8 |
| `examples/use-background-registration.ts` | The startup and setting hook around `reconcileBackgroundTasks` | Workflow step 9 |
| `examples/use-background-registration.test.ts` | Its test: registers, setting off unregisters, orphan removed, restricted, failed | Workflow step 9 |
| `examples/use-sync-outbox-on-foreground.ts` | The foreground path through the same runner (`foreground` trigger) | Workflow step 10 |
| `examples/use-sync-outbox-on-foreground.test.ts` | Its test: runs on active, not while inactive, `overlapping` during a background run | Workflow step 10 |
| `examples/index.ts` | The entry importing the registry | Workflow step 5 |
| `scripts/check-background-tasks.mjs` | The checker (16 rules) | Workflow step 11; definition of done |
| `scripts/lib/background-scan.mjs` | This skill's scanning helpers: calls, arguments, object entries, function ranges, numbers | Only when changing the checker |
| `scripts/selftest.mjs` | Proves the checker passes the templates and examples and fails every planted bug | After changing the checker, a template or an example |
| `scripts/check-lib.mjs` | Shared script helper (synced; never edit here) | Never by hand |
| `scripts/lib/source-scan.mjs` | Shared lexer and import resolver (synced; never edit here) | Never by hand |
| `assets/shared.json` | The shared files this skill copies in | When adding a shared file |
| `tests/` | The fixture base app (`tests/bases/app`) and the overlay cases (`tests/fixtures/check-background-tasks`) | When adding a rule to the checker |

## Related skills

- `networking-and-server-state` - the ApiClient, idempotency keys and the outbox sync the job calls.
- `persistence-and-migrations` - the database, migrations (foreground only) and connection pragmas.
- `async-safety` - `withTimeout`, abort signals and app-lifetime listeners the runner builds on.
- `error-handling-typed-results` - Result values, the error log and what a catch may do.
- `architecture-and-boundaries` - ports, adapters, the composition root and the SDK classification.
- `expo-prebuild-and-config-plugins` - the plugin list and the native snapshot.
- `settings-and-preferences` - the "sync in the background" setting that feeds the reconcile.
- `app-startup-and-bootstrap` - where the reconcile hook runs after the startup gate.
- `local-notifications` - reminders at a time (not background tasks).
- `push-notifications` - server events and notification tasks (their executor goes through `toTaskExecutor`).
- `debug-menu-and-test-hooks` - the debug action that triggers a run and shows the run log.
- `android-emulator-build` - the named emulator for the Android device proof.
- `unit-and-component-tests` - fakes, render helpers and fake-timer rules for the tests.
