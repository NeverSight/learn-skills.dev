---
name: performance-budgets
description: Measures cold start, hitches, draw calls, storage writes, bundle and memory against budgets on iOS and Android. Use when adding animation, Skia, lists, packages, startup work, or the app lags. Not for re-renders (react-components-and-hooks).
---

# Performance budgets

Keeps an Expo app inside budgets that live in one checked-in file: cold start measured from process
start, hitch rate and p95 frame time, draw calls per frame, canvases per screen, the per-change storage
write, bundle size per platform and memory. The numbers come from Release builds on real iPhones and
Android phones, from simulators and emulators (regressions only) and from Jest (fast guards); four
zero-dependency checkers judge the code, the budgets, the device reports and the bundles.

## Rules that must hold

1. **Every budget lives in `quality-gates.json` `"perf"`, and tests and checkers read it from there.**
   The ten keys start at the values in `assets/perf-budgets.json` (cold start < 1,000 ms, hitch rate
   ≤ 10 ms/s, p95 frame ≤ 17 ms, storage write p95 < 5 ms, ≤ 1,000 draw calls, ≤ 8 canvases per screen,
   ≤ 6,000,000 bytes of JS per platform and ≤ ×1.1 growth, ≤ 150 MB). Tighten them after the first
   device report; loosening needs that report, the reviewer's approval and the `Gate-Change:` trailer,
   plus `check-budgets --allow <key>` above the starting value (the checker knows only the starting
   values; loosening an already-tightened value is caught by the trailer and the review). Why: one
   reviewed source, and a budget raised to pass a check is no budget (`budget-missing`,
   `budget-looser`, `budget-unknown`).
2. **Before a release, only Release builds of an internal variant on real target devices are the
   truth, on both platforms; a simulator or emulator only compares with its own committed baseline.
   After a release, the field metrics (Xcode Organizer, Play Console Android vitals) are the truth at
   scale and feed the next tightening.** Why: dev mode slows JS on purpose, the iOS simulator runs on
   the Mac's CPU and caps at 60 fps, an emulator's timing follows the host, and a few test phones are
   not the users' phones (`cold-start`, `frame-data` vs `--sim-baseline`).
3. **Cold start is process start to the first screen drawn with data, read natively, and only for a
   process the launch created.** The local Expo module `modules/process-start` (iOS `sysctl`, Android
   the process start elapsed time) gives the start; `markJsEntry()` runs once inside the startup
   function (never at module scope); `useColdStartMark({ perf, perfLog, label, isReady })` marks the
   first screen one frame after `isReady` turns true (real data, not a spinner). A prewarmed (iOS) or
   background-started (Android push, broadcast, job) process, or one started over 10 s before the JS
   entry, is flagged `prewarmed` and left out. Why: React Native's own marks start at bundle load and
   missed about 90 % of a launch (iOS simulator, 66 launches: 539 ms median, 484 ms before JS), and a
   stale process start adds hours (`perf-layer`, `cold-start-runs`).
4. **Frame times come from a recorder that never owns a frame callback.** The frame callback that
   already runs (a canvas surface's `onFrameTime`, a loop's runner) calls `sampleFrame`; the report
   picks 120, 90 or 60 Hz from the shortest interval. Why: an extra display link keeps an idle screen
   rendering and changes what it measures; a 90 Hz phone judged as 120 Hz shows a false hitch on every
   frame (`recorder-callback`, `hitch-rate`, `frame-p95`).
5. **No per-frame data in React state.** Shared values and Skia pictures carry it; a React setter
   never runs inside `useFrameCallback`. Why: a render per frame cannot fit an 8.3 ms frame at 120 Hz.
   `scheduleOnRN` per frame is motion-and-animation's `no-js-per-frame` (`react-state-per-frame`).
6. **No Skia object is created per frame.** Worklet functions outside the canvas folders allocate
   nothing; static layers are cached; 100 or more identical sprites use an atlas; pre-rendered
   textures (`w × h × 4` bytes) are disposed on a theme change. Why: each `Skia.Paint()` per frame is
   a native allocation. Frame-hook callbacks and the canvas folders are skia-canvas-rendering's
   `frame-alloc` and `draw-pure` (`skia-alloc-per-frame`).
7. **Every frame callback can stop:** it starts inactive (`useFrameCallback(cb, false)`) and
   `setActive(false)` runs when the animation ends, on background, on blur and under a full-screen
   interruption (modal, ad, video). Why: an idle screen must render no frames (`frame-callback-stop`
   sees the autostart argument and a stop call in the file, not every path; the rules reference says
   what to review by hand).
8. **Every custom drawing's draw-call budget stays at or under the app's ceiling**
   (`perf.drawCallsPerFrameMax`). Why: counting canvas calls on the busiest frame is the headless
   stand-in for GPU cost; skia-canvas-rendering's `draw-budget` requires the test itself
   (`draw-call-budget`).
9. **At most `perf.skiaCanvasesPerScreenMax` canvases per screen file, never a canvas per list item**
   (`.map(...)`, `renderItem`). Lists: `FlatList` by default, FlashList only after a measurement, a
   `ScrollView` only for a short bounded list. Why: each canvas cost about 0.18 MB and 2.8 ms to mount
   (iOS); one per tile made a 90-tile grid ten times slower (`canvases-per-screen`, `canvas-per-item`;
   react-components-and-hooks owns `scrollview-list`).
10. **Check the bundle delta before adding a runtime dependency, per platform, against a committed
    baseline; import locale data only in the polyfill module.** Why: bundle weight is start-up work,
    and Hermes maps bytecode but still runs every module's initialisation (`bundle-cap`,
    `bundle-growth`, `intl-locale-data`).
11. **Keep Hermes V1 and generate no code at runtime.** Why: release builds ship precompiled bytecode;
    `eval`, `new Function` and string timers defeat it (`hermes-engine`, `runtime-codegen`).
12. **The per-change storage write stays under its p95 budget, proven twice:** a Jest guard writes the
    app's largest realistic data through the real write path on `node:sqlite`, timed with
    `node:perf_hooks`; a test build's benchmark writes it 300 times into a scratch database. Why: the
    React Native Jest preset mocks `performance.now` at 1 ms, and only the device measures real I/O
    (`perf-clock-in-tests`, `storage-write-p95`, `storage-write-runs`).
13. **Start-up stays cheap:** nothing runs at import time, and ads, consent, purchases, analytics and
    prefetches start after the first screen. Why: the cold-start budget (app-startup-and-bootstrap
    owns the order; this skill measures it).
14. **The test-build perf log never uploads; it leaves only through the share sheet.** The perf log
    (its own kv-store database, apart from the user's data and preferences) and the debug menu's
    Performance actions exist in test builds only. Why: the evidence is the developer's, and nothing
    of it ships in a store build (`debug-perf-wired`). Production performance monitoring (Sentry
    tracing, MetricKit) is a separate, consent-gated concern of crash-reporting-and-observability.
15. **Memory after the smoke flow stays under `perf.memoryFootprintMbMax`:** iOS `phys_footprint`,
    Android `TOTAL PSS`. Why: the OS kills a backgrounded app that holds too much first.

## Workflow

1. **Budgets.** Merge `assets/perf-budgets.json` into `quality-gates.json` `"perf"` (quality-gates
   owns the file; its `Gate-Change:` trailer applies) and run `check-budgets.mjs`. Read
   [references/budgets-and-gates.md](references/budgets-and-gates.md) before changing a value; stop
   and ask the reviewer before loosening one.
2. **The measurement layer** (once per app). Copy every template to the path its first line names
   (`src/core/perf/`, `src/services/perf/`, `src/services/perf-log/`, `src/hooks/use-cold-start-mark.ts`,
   `test/perf/storage-write.perf.test.ts`, `modules/process-start/`, `contracts/perf.json`), then wire
   it as [examples/wiring-the-measurement-layer.md](examples/wiring-the-measurement-layer.md) shows:
   `perf: createExpoPerfAdapter()` in the composition root (architecture-and-boundaries), the JS entry
   mark in the root layout's startup decision (app-startup-and-bootstrap), `useColdStartMark` in the
   first screen's model hook, and the perf log plus `createPerfDebugActions` in the test-only entry
   (debug-menu-and-test-hooks). Pass `isReady` from the screen's data (`query.isSuccess`). The adapter
   needs `npx expo install expo-application` (the native build number). Fill `contracts/perf.json`
   with those files. The native module needs a native rebuild (EAS or `npx expo prebuild --clean`).
   Replace the seed and write in `src/data/perf/tasks-benchmark.ts` (shared by the storage guard and
   the device benchmark) with the app's heaviest per-change write.
3. **Any change with animation, Skia, frame callbacks, lists or start-up work.** Read
   [references/performance-rules.md](references/performance-rules.md), then run `check-perf-code.mjs`.
   Feed a new frame runner to the recorder (`sampleFrame`) and stop it with its lifecycle.
4. **Adding a runtime dependency.** Export both platforms before and after
   (`npx expo export --platform ios --no-bytecode`, then `--platform android`) and run
   `check-bundle-size.mjs` for each (it reads `perf-baselines/bundle-<platform>.json` under the repo
   root; the first run adds `--write-baseline`); explain any growth to the reviewer.
5. **Simulator and emulator regression run** (Release, internal variant, named devices): 6 cold
   launches each, the perf log read back, `check-perf-report.mjs <log.json> . --sim-baseline-file
   perf-baselines/cold-start-sim-ios.json --memory <reading>` (the first accepted run adds
   `--write-sim-baseline`), after e2e-maestro's smoke flows (its runner hosts no perf step). [references/measuring.md](references/measuring.md) has every command
   for iOS (`simctl`, `footprint`) and Android (`adb -s`, `dumpsys meminfo`, `am start -W`).
6. **Before a release (a human step).** Ask the developer for a device report from each platform (the
   steps are in the measuring reference: frames, one storage benchmark, five relaunches), save them
   under `reports/perf/`, run `check-perf-report.mjs <report.json> .` on each and report the numbers as
   [examples/reading-a-perf-report.md](examples/reading-a-perf-report.md) does.
   After the release, read the field metrics (measuring reference, "Field metrics") and tighten from
   them as [references/budgets-and-gates.md](references/budgets-and-gates.md) describes.
7. **Run the checks** from the repo root and fix every `FAIL` line until each prints `RESULT: PASS`.

## Definition of done

- [ ] `quality-gates.json` holds all ten `perf` budgets, none looser than its starting value without
      an approved `--allow`.
- [ ] No React setter, Skia allocation or unstoppable frame callback runs per frame; the recorder
      only samples existing frame callbacks.
- [ ] Draw-call budgets sit at or under the ceiling; screens keep their canvas budget and no list item
      mounts a canvas.
- [ ] The measurement layer is declared in `contracts/perf.json` and wired: native module rebuilt, JS
      entry mark, first-screen mark, perf log and Performance actions in the test-only entry.
- [ ] The layer's tests and the storage guard pass (`npx jest src/core/perf src/services/perf
      src/services/perf-log src/hooks test/perf test/sqlite/tasks-benchmark.test.ts --ci`).
- [ ] A new runtime dependency passed `check-bundle-size.mjs` on both platforms against the committed
      `perf-baselines/bundle-<platform>.json`.
- [ ] After the smoke flows on the named simulator and emulator: six cold launches pass
      `check-perf-report.mjs <log> . --sim-baseline-file perf-baselines/cold-start-sim-ios.json` (and
      `cold-start-emu-android.json`; the first accepted run adds `--write-sim-baseline`), and the
      memory reading passes `--memory <footprint.json | meminfo.txt>` (`memory-footprint`).
- [ ] Before a release: an iOS and an Android device report of the release build, each with 5 counted
      cold starts, a frame recording and a storage benchmark stamped with that build, pass
      `check-perf-report.mjs`, and the numbers are in the report to the reviewer.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-budgets.mjs .` prints `RESULT: PASS`.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-perf-code.mjs .` prints `RESULT: PASS`. Expected
      non-problem lines: `SKIP src/test-only-entry.ts [debug-perf-wired] not yet created
      (debug-menu-and-test-hooks creates it)` until that entry exists, and the `perf-layer: ...` note
      while `contracts/perf.json` declares no layer (an app that measures nothing on devices yet).

## Anti-patterns

- **`setProgress(x)` inside `useFrameCallback`.** A React render per frame; keep it in a shared value
  and cross to JS once, when the animation ends.
- **`Skia.Paint()` inside a worklet.** Build paints and paths once and pass them in.
- **A `<Canvas>` per row or per icon.** Use the Icon primitive, or draw the group on one canvas.
- **A frame recorder with its own `useFrameCallback`.** It keeps idle screens rendering; sample from
  the runner that already exists.
- **Judging a 90 Hz Android phone against 120 Hz frames.** Every frame looks late; the report picks
  the rate from the shortest interval.
- **Measuring a dev build, a simulator or an emulator and calling it the budget.** Only Release
  builds on devices are the truth.
- **Marking the first screen while it shows a spinner.** `totalMs` then stops before the work the
  budget is about; pass `isReady` from the data (`query.isSuccess`).
- **Counting a prewarmed or push-started launch.** Its process start is hours old; the report flags it
  and the checker leaves it out, so relaunch until five counted launches remain.
- **`performance.now()` in a Jest perf test.** It is a 1 ms mock there; import it from
  `node:perf_hooks`.
- **Raising a budget to make a check pass.** Fix the work; loosening needs a device report and the
  reviewer.
- **Starting ads, consent or purchases before the first screen "to be ready".** They belong after it.
- **Adding a library or locale data "just in case".** Measure the bundle delta first.
- **Keeping the perf log in the user's database, or sending it anywhere.** Test builds keep it apart;
  only the share sheet takes it off the phone.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/budgets-and-gates.md](references/budgets-and-gates.md) | The ten budgets, where each is measured, `quality-gates.json`, how a budget changes, the measured reference points | Workflow step 1, and whenever a budget is in question |
| [references/measuring.md](references/measuring.md) | Recorder, perf log, cold start, prewarmed and background starts, storage benchmark, draw calls, bundle, memory, list measurement, simulator/emulator and device steps, field metrics (Organizer, MetricKit, Play vitals) | Workflow steps 2, 5 and 6 |
| [references/performance-rules.md](references/performance-rules.md) | Per-frame work, Skia cost, frame callbacks and textures, lists, bundle, Hermes and start-up, who owns which rule | Workflow step 3 |
| [examples/reading-a-perf-report.md](examples/reading-a-perf-report.md) | A device report, the checker's output and how to read and report it | Workflow step 6 |
| [examples/wiring-the-measurement-layer.md](examples/wiring-the-measurement-layer.md) | The composition-root member, the JS entry mark, the first-screen mark and the test-only entry, as shapes | Workflow step 2 |
| `templates/src/core/perf/` | Frame histogram and report (120/90/60 Hz), perf entries and the ring buffer, write-time summary and benchmark, cold-start report, with tests | Workflow step 2 |
| `templates/src/services/perf/` | `PerfPort`, the Expo adapter (clocks, process start, build header, share sheet), fake, cold-start marks, frame recorder, the debug menu's Performance actions, with tests | Workflow step 2 |
| `templates/src/services/perf-log/` | `PerfLogPort`, the expo-sqlite/kv-store adapter (its own `perf-log.db`), fake (+ test) | Workflow step 2 |
| `templates/src/hooks/` | `use-cold-start-mark.ts` (+ test): the first-screen mark, waiting for `isReady` | Workflow step 2 |
| `templates/src/data/perf/` | `tasks-benchmark.ts`: the storage benchmark's opener and seed (largest realistic data, the per-change write, scratch file deleted on close), shared by the device benchmark and the Jest guard | Workflow step 2 |
| `templates/test/perf/` | `storage-write.perf.test.ts`: the Jest guard, per-change write p95 under the budget on `node:sqlite` | Workflow step 2 |
| `templates/test/sqlite/` | `tasks-benchmark.test.ts`: the opener on real SQLite (seed, write, delete on close) | Workflow step 2 |
| `templates/modules/process-start/` | Local Expo module: `expo-module.config.json`; iOS `ProcessStartInfo.swift` (start, prewarm, model) + module + podspec; Android `ProcessStartInfo.kt` (start, background start, model) + module + Gradle + manifest | Workflow step 2 |
| `templates/contracts/` | `perf.json` and `perf.schema.json`: the app's performance contract (layer files, canvas exemptions) | Workflow step 2 |
| `assets/perf-budgets.json` | The `perf` block with its starting values | Workflow step 1 |
| `assets/shared.json` | The shared files this skill copies in | When adding a shared file |
| `scripts/check-perf-code.mjs` | Code rules: Skia and React state per frame, stoppable callbacks, the recorder, draw-call ceiling, canvases, codegen, Hermes, locale data, Jest clocks, the declared layer and its debug wiring | Workflow steps 3 and 7 |
| `scripts/check-budgets.mjs` | `quality-gates.json` `perf`: present, positive, known, not looser | Workflow steps 1 and 7 |
| `scripts/check-perf-report.mjs` | Judges a device report (this build's entries only), or a simulator/emulator log against `--sim-baseline-file`, plus `--memory` | Workflow steps 5 and 6 |
| `scripts/check-bundle-size.mjs` | Checks one platform's export against the cap and its baseline (`--platform`, `--write-baseline`) | Workflow step 4 |
| `scripts/lib/budgets.mjs` | The budget table, its starting values and the loader | When changing a budget rule |
| `scripts/lib/source-scan.mjs` | Shared source scanner (synced, do not edit) | When changing a checker |
| `scripts/check-lib.mjs` | Shared checker library (synced, do not edit) | Never by hand |
| `scripts/selftest.mjs` | Proves every checker against its fixtures | After changing a script or fixture |
| `tests/bases/app/` | A small Tasks app the code checker's fixtures start from | When adding a rule |
| `tests/fixtures/` | Good, pass, bad and error cases per checker (overlay format) | When adding a rule |

## Related skills

- `skia-canvas-rendering` - canvas surfaces, `onFrameTime`, per-frame allocation in canvas code, draw tests.
- `motion-and-animation` - per-frame JS crossings, loops that stop.
- `react-components-and-hooks` - re-render boundaries, list choice and keys.
- `app-startup-and-bootstrap` - the startup order this skill measures.
- `architecture-and-boundaries` - the composition root that creates the perf adapter.
- `debug-menu-and-test-hooks` - the test-only entry and the debug menu.
- `app-variants-and-environment` - proving test-only code leaves store bundles.
- `dependency-management` - adding packages (with the bundle delta from here).
- `i18n-strings-and-catalogs` - the polyfill module and its locale list.
- `quality-gates` - `quality-gates.json` and the `Gate-Change:` trailer.
- `crash-reporting-and-observability` - production performance monitoring (consent-gated tracing).
- `ios-simulator-build`, `android-emulator-build` - Release builds on named devices.
- `e2e-maestro` - the smoke flows that run before the cold-start and memory runs.
