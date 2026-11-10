---
name: skia-canvas-rendering
description: Builds hand-drawn Skia canvases - pure worklet draw() in one Picture, scene clock, timelines, canvas text, goldens. Use when drawing a chart, grid or board, or canvas animation freezes. Not for touch (canvas-gestures-and-hit-testing).
---

# Skia canvas rendering

Every hand-drawn surface of the app (a progress grid, a chart, an editor, a game board) is one Skia
`<Canvas>` whose single `<Picture>` is recorded on the UI thread from the surface's pure `draw()`,
animated by a timeline that a self-stopping scene clock plays, and proven by unit tests, a draw-call
budget and pixel goldens. This skill ships the canvas kit (`src/canvas/`), a template surface and two
checkers that prove the result.

## Rules that must hold

1. **One `<Canvas>` per surface with one `<Picture>` recorded in `useDerivedValue` from the surface's
   `draw()`, and every computed picture lives in the kit or a surface folder.** Why: dynamic pictures
   are Skia's immediate-mode case; one picture per frame keeps cost predictable; a computed canvas
   elsewhere (a Picture sparkline in `components/`, animated Skia nodes in a child component) escapes
   every rule below. Retained nodes only for static art: a declarative gradient, blur or fixed shape
   may live anywhere (sizing it through `onSize` is layout, not motion), and art recorded once
   (`createPicture`) is listed in the contract's `staticCanvases`. An atlas only for hundreds of sprites.
2. **`draw(canvas, frame)` is a pure worklet in a `'worklet'` file:** it reads only `frame` (`view`,
   `fx`, `highlight`, `colors`, `layout`, `kit`), imports Skia types only, allocates no Skia objects,
   reads no clock or random source, and imports values only from other `'worklet'` modules. Why: the
   same function then renders on device, in Jest goldens and in Node with identical pixels, and a plain
   function called on the UI thread crashes at runtime only.
3. **An opaque canvas paints every pixel first.** `SurfaceCanvas` is opaque by default, so `draw()`
   starts with `canvas.drawColor(colors.color.background)`; a canvas that must show what lies behind it
   is declared `"opaque": false` in the contract and every `SurfaceHost`/`SurfaceCanvas` rendering it
   passes a literal `isOpaque={false}`. Why: on Android an opaque canvas is a SurfaceView, neither
   clipped by a rounded parent nor blended with what lies behind it, so unpainted pixels show black on
   device while iOS and the goldens look right; the declaration alone changes nothing on screen.
4. **Push one `scene` shared value per committed change** (`makeScene(seq, view, tracks)`, `startAt:
   NOT_STARTED`); the frame runner stamps `startAt = info.timestamp` on its first frame. Never use
   `timeSinceFirstFrame`. Why: Reanimated resets it to 0 on every re-activation, which froze every
   animation after the first (verified on Reanimated 4.5.1).
5. **The frame callback runs only while something moves** and its body is one call into
   `runSceneFrame`, which holds the `try/catch`; never Skia's `useClock()` or `withRepeat(…, -1)`. Why:
   an idle surface must cost nothing (both of those run every frame forever), an uncaught UI-thread
   error kills the app, and React Compiler bails out of hooks with value blocks inside `try/catch`.
6. **Persist before animating; a new change fast-forwards; only changes committed while the surface is mounted animate.** The store applies and saves, then
   `presentChange` cancels old cues, pushes the final view and schedules new cues; the change present
   at mount is shown without animation. Why: killing the app mid-animation must lose nothing, the view
   is always the final state, and a screen opened again must not replay its last celebration.
7. **`buildTimeline(events, motion)` is pure and honours `'reduced'`:** half durations, no particles or
   shake, no overshoot. Why: reduce motion is an accessibility requirement, and as data it is testable.
8. **An effect layer that is not a tween of something visible (flash, glow, burst, shake) draws only
   while its track plays (`isPlaying`: `ageMs > 0 && progress < 1`).** Why: a sample holds a track's
   `from` before it starts, so an unguarded effect shows at full strength at moment 0.
9. **Selection and hints are UI state the screen passes as `highlight` (`CanvasHighlight`,
   `EMPTY_HIGHLIGHT`), and a drag preview sits exactly on the hovered cell.** The gesture layer applies
   the surface's `dragLiftPt` once; draw adds no offset. Why: stores, undo and persistence never see a
   selection, and the previewed cell must be the cell that receives the drop.
10. **The layout is a pure worklet of the actual canvas size, shared by draw and hit-testing.** Why:
   tablets, landscape, foldables and resizable windows need no special case, and draw and touch cannot
   drift.
11. **Never pixel-flip.** A surface that opts in (`isMirroredInRtl`) mirrors positions in the layout.
    Why: `scaleX(-1)` mirrors letters and digits.
12. **Digits are localised in `toView()` and drawn with `drawText` (`drawFittedText` in a small
    shape); words and complex scripts use a cached Skia `Paragraph`; widths come from glyph widths;
    fonts come from the bundled TTF through one `useFonts` provider on both platforms.** Why:
    `drawText` does no shaping, `measureText` is unimplemented in CanvasKit (Jest, Node), and Skia's
    Android font manager cannot see fonts embedded with the `expo-font` plugin.
13. **Paths are built once with `Skia.PathBuilder` at unit size** and placed with
    `canvas.translate/scale`. Why: the mutable `SkPath` API is deprecated in Skia 2.6 and allocates.
14. **Palettes are semantic tokens in sets with identical keys (`light`, `dark`, plus the opt-in sets
    `contracts/canvas-surfaces.json` lists), beside a `canvas-contrast.json` saying which colour sits on
    which; every declared pair meets WCAG 2.2 AA in every set (text 4.5:1, graphics and shapes 3:1,
    `distinct` kinds apart under colour-blind simulation); meaning is never carried by colour alone.**
    Why: a missing token is a crash on one theme only, and contrast is provable only when the pairs are
    declared and measured; `accessibility-as-code`'s contrast check measures the same file, so its format
    is stable and the pairs are never declared a second time in `contracts/contrast.json`.
15. **Stop everything when the surface may not run, and switch the clock only through
    `scene-clock-state`.** `useCanvasLifecycle` (app active, screen focused and not covered) stops
    the clock, cancels cues and suspends audio; a scene pushed while the surface may not run is held
    until it may; every resume records at least one frame; a done message names its run, and JS never
    reads the scene shared value back. Why: an overlay or an unfocused screen that stays mounted must
    not keep a display link running, no cue or sound may fire once the app leaves the foreground, and a
    stale done read through `scene.get()` froze the picture after an interruption (the case study in
    `timeline-and-clock.md`).
16. **iOS: keep `CADisableMinimumFrameDurationOnPhone` true.** Expo's prebuild template sets it, so a
    Continuous Native Generation app needs no key; never override it with `false` in the config or a
    plugin, and committed native folders keep it in `ios/<App>/Info.plist`. Why: without it iOS caps
    the app at 60 fps on ProMotion iPhones. Android needs no key.
17. **Every canvas is one accessible image:** `accessible`, `accessibilityRole="image"` (or `role="img"`)
    and `accessibilityLabel` (or `aria-label`) = `t()` of `surface.describe(view)`; a purely decorative
    canvas opts out explicitly (`accessible={false}`). Why: Skia content is invisible to VoiceOver and
    TalkBack, labels must be translated, and React Native 0.86 defaults `accessible` to false: iOS
    ignores the label and role of a view that is not accessible.
18. **Every surface is proven three ways:** pure unit tests (timeline, clock, layout), a draw-call
    budget test that also asserts every localised label, and pixel goldens at 3 sizes × moments 0,
    0.5, 1 with 0.1 % tolerance, accepted only after opening every PNG. Why: a two-digit label is
    below the golden tolerance, so pixels alone miss it; goldens catch what assertions forget.
19. **Draw-call budget per surface on the busiest frame, never above 1,000.** Why: counting canvas
    calls is the headless stand-in for GPU cost; a higher number needs an on-device frame report.
20. **Server data becomes changes through `useCommittedChange(data, diffEvents)`** with a pure, tested
    `diffEvents(previous, next)` in the surface folder: the first data and identical refetches animate
    nothing; an optimistic update and its rollback are two changes. Why: a query has no reducer to
    return events, and a chart that replays on every refetch is noise.

## Workflow

1. **Decide and classify.** Read [references/architecture.md](references/architecture.md): draw with
   Skia only when the picture is computed; pick the kind (timeline: this skill end to end;
   simulate-then-replay or live: the loop comes from `realtime-game-loop`, palettes and drawing rules
   from here). A surface that takes touch also needs `canvas-gestures-and-hit-testing` in the same
   session. A game board: also read [references/game-boards.md](references/game-boards.md).
2. **Copy the kit.** Copy `templates/contracts/canvas-surfaces.json` to `contracts/` and fill in the
   first surface, then from the repo root run `node ${CLAUDE_SKILL_DIR}/scripts/check-canvas-files.mjs .`:
   it lists every file to copy. Copy each `kit-file-missing`
   file verbatim from `templates/` to the path its first line names (`templates/src/canvas/**` →
   `src/canvas/`, `templates/scripts/quality/**`, `templates/test/goldens/skia-golden.ts`), and
   `templates/src/hooks/use-is-app-active.ts` (+ test) → `src/hooks/` when the app does not have it
   yet. A `kit-import-unresolved` line names the prerequisite and the skill that creates it (the
   table in architecture.md). The iOS 120 Hz key comes from Expo's template (`plist-120hz` fails only an
   override or a committed `Info.plist` without it); the canonical `jest.config.js` has the golden
   project (`jest-golden-project`).
3. **Read before writing the surface:** [references/timeline-and-clock.md](references/timeline-and-clock.md)
   for `buildTimeline`, the clock and the lifecycle, [references/drawing.md](references/drawing.md) for
   `draw()`, the kit, palettes, layout and text, [references/api-traps.md](references/api-traps.md) for
   the worklet rules and API traps. Imitate the template surface and
   [examples/weekly-chart/](examples/weekly-chart/).
4. **Copy the surface templates** from `templates/src/features/__FEATURE__/canvas/` to
   `src/features/<feature>/canvas/`, the golden test and its nine baselines from `templates/test/goldens/canvas/`,
   and the contract's schema (`templates/contracts/canvas-surfaces.schema.json`). Replace `__FEATURE__`
   (`tasks`), `__SURFACE__` (kebab, `progress-grid`), `__SURFACE_PASCAL__` and `__SURFACE_CAMEL__` in
   file names and contents. The copy compiles and passes as is; then adapt the model, the view, the
   events, the layers, the palettes and the contrast pairs.
5. **Build test-first, in this order:** palettes and `canvas-contrast.json` → `canvas-model.ts` →
   `to-view.ts` → `build-timeline.ts` with its test (budget, reduced motion, cues) → `layout-<id>.ts`
   with its any-size test → `draw-<id>.ts` with the budget, moment-0, highlight and label tests →
   `<id>-surface.ts` (`isMirroredInRtl`, the `describe` key in every locale catalog, `dragLiftPt` and
   `targetsOf` when the surface drags or suggests). Run `npx jest src/features/<feature>/canvas --ci
   --selectProjects unit` after each step (paths first: `--selectProjects` would swallow them).
6. **Wire the screen.** The feature's model hook passes the store's `CommittedChange` (server data:
   `useCommittedChange(data, diffEvents)`, the timeline reference's server section), the `ViewFormat`,
   the live `motion`, `useIsFocused()`, `isInterrupted`, the colours, the kit (built once the
   `useFonts` provider exists, drawing.md) and the highlight to `SurfaceHost` (display-only), or calls
   `useSurfacePlayer` and renders `SurfaceCanvas` with the gesture layer's `input` (interactive). The
   label is `t(surface.describe(view))`. A canvas that shows what lies behind it passes
   `isOpaque={false}` (written out on the element, not through a spread) and declares
   `"opaque": false` in the contract.
7. **Lint, format and type-check:** `npx eslint --fix src/canvas src/features/<feature>/canvas test/goldens scripts/quality`,
   `npx prettier --write` on them (import order and wrapping depend on the names you chose), then
   `npm run typecheck`.
8. **Create the pixel goldens deliberately** ([references/testing-and-goldens.md](references/testing-and-goldens.md)):
   `npx jest test/goldens/canvas/<id>.golden.test.ts --selectProjects golden -u`, open all nine PNGs
   and compare them with the intended look (moment 0: old geometry, no effect that starts later,
   labels from the view already final; 0.5 mid-flight; 1 the final view), then
   `CI=1 npx jest --ci --selectProjects golden`.
9. **Run the checks:** `node ${CLAUDE_SKILL_DIR}/scripts/check-canvas-code.mjs .` and
   `node ${CLAUDE_SKILL_DIR}/scripts/check-canvas-files.mjs .`. Fix every `FAIL` line (each names the
   file, the rule and the fix) and rerun until both print `RESULT: PASS`.
10. **Look at it for real.** A Release build on a named iOS simulator and a named Android emulator,
    screenshots in every locale (one RTL locale at least), then the developer confirms 120 Hz and the
    hitch rate on real phones with a frame-time recorder (simulators are not devices).

## Definition of done

- [ ] The kit is in `src/canvas/` with its tests, plus `test/goldens/skia-golden.ts` and the worklet
      boundary gate in `scripts/quality/`; `npx jest src/canvas scripts/quality --ci --selectProjects unit` passes.
- [ ] Each surface folder has palettes (identical tokens in every set) with `canvas-contrast.json`,
      `to-view.ts`, `build-timeline.ts`, `layout-<id>.ts`, `draw-<id>.ts`, `<id>-surface.ts`, and their
      tests pass; every pair in `canvas-contrast.json` meets its ratio in every palette set (the
      contrast rules of `check-canvas-files.mjs`), and no `contracts/contrast.json` entry names the
      surface's palettes (`contrast-declared-once`).
- [ ] Moment 0 draws no effect that starts later (a draw test and the moment-0 goldens), the
      highlight is drawn, and a surface with a drag lift draws its preview on the dropped cell.
- [ ] The draw test asserts that the first call is `drawColor` (or the surface is declared
      `"opaque": false` and every element rendering it passes `isOpaque={false}`); every computed
      canvas lives in the kit or a surface folder, and no surface file sits outside one.
- [ ] A server-data surface has `diff-events.ts` with its test and feeds `useCommittedChange`;
      reopening the screen replays nothing (`use-surface-player.test.ts` passes).
- [ ] The busiest frame stays within the surface's draw-call budget (≤ 1,000) and every localised
      label is asserted through the recording canvas.
- [ ] Nine golden PNGs (3 sizes × 0, 0.5, 1) exist, were opened and looked at, and
      `CI=1 npx jest --ci --selectProjects golden` passes.
- [ ] `npm run typecheck` and `npx eslint --max-warnings 0` pass; no `__PLACEHOLDER__` is left.
- [ ] Reduced motion removes particles, shake and overshoot; every canvas is `accessible` with an
      image role and a translated `accessibilityLabel` (or opts out as decorative); the surface runs
      only while the app is active, the screen focused and nothing covers it (no `useClock`, no
      endless repeat); nothing turns the iOS 120 Hz key off.
- [ ] `npx jest src/canvas/scene-clock --ci --selectProjects unit` passes (push while paused, resume
      after done, stale done, and both recorded traces).
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-canvas-code.mjs .` prints `RESULT: PASS`.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-canvas-files.mjs .` prints `RESULT: PASS`.

Neither checker prints SKIP lines. Both print `NOT APPLICABLE` only when no `package.json` declares
`@shopify/react-native-skia`, and both stop with exit 2 when a configured `canvasSurfaceDirs` glob
matches no surface folder or `contracts/canvas-surfaces.json` is malformed.

## Anti-patterns

- **Animating with `timeSinceFirstFrame` or a `t0` stored on JS.** The second change freezes. Stamp
  `startAt` from `info.timestamp` in the frame runner.
- **Creating `Skia.Paint()`, `Skia.Color()` or paths inside `draw()` or at module import.** Native
  allocations every frame, and module scope breaks tests. Build once in the kit (`makeDrawKit`,
  `buildPaths`); one recorder per canvas via `useState`.
- **Putting per-frame data in React state or re-rendering a label per frame.** A 120 Hz frame is
  8.3 ms. Positions live in shared values and the picture; React renders on committed changes.
- **Storing only "the change" in the view and reading old state in `draw()`.** The view is the final
  state; anything that vanishes carries its own position in a track.
- **A frame callback that keeps running on an idle surface, on an unfocused screen or under an
  overlay.** Stop on `onDone(run, seq)` through `finishRun` and through `useCanvasLifecycle`.
- **Guarding `onDone` with `scene.get().seq` on the JS thread.** Until the UI applies a push, the JS
  read returns the old scene, so the done of the scene before an interruption stops the next scene on
  its first frame. Compare runs in `scene-clock-state`.
- **Starting the clock for a scene pushed while the surface is covered or unfocused.** Its animation
  plays where nobody sees it; `pushScene` holds it until the surface may run.
- **Reading Reanimated's `useReducedMotion()` in canvas code.** It reads the setting once at app
  start, so a later change is missed; pass the live setting as `motion`.
- **Flipping the canvas with `scaleX: -1` for RTL.** Mirror positions in the layout instead.
- **Leaving the background unpainted on the default opaque canvas.** iOS and the goldens look fine;
  Android shows black corners. Start draw with `drawColor`, or pass `isOpaque={false}` and declare it.
- **Embedding fonts with the `expo-font` plugin and resolving them with `matchFont` or
  `Skia.FontMgr.System()` for the canvas.** Works on iOS only; Android falls back to a system font.
  Load the TTF with `useFonts` and pass the provider everywhere.
- **Presenting the change a screen mounts with, or clearing store events to avoid it.** The player
  shows the mounted change's final view and animates only later `seq`s.
- **Setting `structuralSharing: false`, or putting `Date`, `Map`, `Set` or class instances into the
  query data or `select` result a surface reads.** Only plain JSON keeps its identity across
  refetches, so each refetch becomes a change and the chart replays.
- **A computed `<Canvas>` (a `<Picture>`, shared values, draw calls) in `src/ui/` or `components/`,
  or a surface's files in a folder no surface glob matches.** Make it a surface folder and render it
  with `SurfaceHost`; a static declarative canvas is fine anywhere.
- **Animating a canvas with Skia's `useClock()` or `withRepeat(…, -1)`.** The frame loop runs for as
  long as the canvas is mounted (idle, unfocused, covered); play a timeline through the scene clock.
- **A canvas with an image role and a label but no `accessible`.** TalkBack may read it, VoiceOver never
  focuses it; write all three (`SurfaceCanvas` does).
- **Declaring a surface's colour pairs again in `contracts/contrast.json`.** Two tables drift. The pairs
  live once, in the surface's `canvas-contrast.json`, which this skill and `accessibility-as-code` both
  measure. If that skill reports `canvas-palettes.json` as an undeclared colour table, update it (drawing.md).
- **`isRtl && TextDirection.RTL`.** RTL is 0; choose explicitly.
- **Raising the golden tolerance or re-running `-u` without opening the PNGs.** Fix the code, or
  accept a deliberate change and say why.
- **Calling a plain JS helper from `draw()` or `layout()`.** It throws on the UI thread at runtime
  only; move the helper into a `'worklet'` module (the template's `canvas-ids.ts`).
- **Asserting small text through pixels.** Use the recording canvas; 0.1 % tolerance cannot see a
  missing number.
- **Drawing a flash or glow whenever its entry exists.** It shows at full strength at moment 0; guard
  it with `isPlaying`.
- **Offsetting a drag preview in `draw()` (`row - 1`).** The item lands elsewhere and an edge row
  becomes unreachable; set `dragLiftPt` on the surface and let the gesture layer lift the pointer.
- **Keeping a selection or hint in the store.** Undo and persistence would see it; the screen passes it
  as `highlight`.
- **Measuring text with `measureText`, or drawing golden text without a loaded typeface.** CanvasKit
  returns `undefined` for the first and draws nothing for the second.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/architecture.md](references/architecture.md) | When to use Skia, data flow, file map, the kit's public API, the `CanvasSurface` contract, surface kinds, prerequisites and owners, the contract file and config keys, When multi-package | Workflow step 1, before any canvas work |
| [references/timeline-and-clock.md](references/timeline-and-clock.md) | Tracks, sampling, `buildTimeline`, the startAt fix, `scene-clock-state`, the frozen-surface case study with its traces, presenter, cues, lifecycle on iOS and Android, the clock trace and canvas-frame probe, 120 Hz | Step 3, before writing a timeline or touching the clock |
| [references/drawing.md](references/drawing.md) | `draw()` rules, highlights and effects, kit and palettes, contrast pairs and the colour-blind profile, paths, layout, RTL, text and fonts, particles, atlas, performance, accessibility, the template and the example | Step 3, before writing draw, layout, view or palettes |
| [references/testing-and-goldens.md](references/testing-and-goldens.md) | Test levels, the draw-call budget, golden set-up and acceptance, failures, the device-only marker, headless previews, simulators, emulators and the E2E probe | Step 8, and whenever a golden fails |
| [references/api-traps.md](references/api-traps.md) | Worklet rules, the SDK 57 API churn table, the re-verify list | Step 3, and when something works in Jest but not on a device |
| [references/game-boards.md](references/game-boards.md) | Games appendix: board folders, kinds, Lights Out from the template, selection, hints and drag, recurring needs | Step 1, when the surface is a game board |
| `templates/src/canvas/` | The kit: layout, types, timeline, draw kit, scene, clock decisions (+ the recorded-trace test), frame runner, clock hook, recorder, text, canvas (`isOpaque`), presenter, cues, lifecycle, player, host, server-data change hook, E2E probe, PNG painter, with tests (layout, types, track and sample are canonical synced copies, identical in every skill that carries them) | Step 2 (copy verbatim) |
| `templates/src/hooks/` | `use-is-app-active.ts` (+ test): the shared foreground hook the lifecycle reads, a synced copy of the canonical file `react-components-and-hooks` owns; keep the app's copy if it already has one | Step 2 (copy verbatim, unless the app has it) |
| `templates/src/features/__FEATURE__/canvas/` | The template surface (the Tasks progress grid): palettes, contrast pairs (`canvas-contrast.json`, format 1 in drawing.md), model, ids, view, timeline, layout, draw, surface object, tests | Step 4 |
| `templates/test/goldens/` | `skia-golden.ts` (synced canonical matcher), the `__SURFACE__.golden.test.ts` golden and its nine reviewed baselines | Steps 2, 4 and 8 |
| `templates/scripts/quality/` | `check-worklet-boundary.ts` (+ test) and `worklet-transform.test.ts`: the `npm test` gate for `'worklet'` modules | Step 2 (copy verbatim) |
| `templates/contracts/` | `canvas-surfaces.json` (the app's surfaces, kinds, opacity, palette sets, `staticCanvases`) and its JSON schema | Steps 2 and 4 |
| [examples/weekly-chart/](examples/weekly-chart/) | A second, complete surface folder to imitate: a server-fed bar chart with `diff-events.ts`, tweens, a guarded flash, RTL mirroring, two regions, fitted digits, its tests and a golden test that loads the bundled TTF (no baselines: you accept them in step 8) | Steps 3 and 6 |
| `scripts/check-canvas-code.mjs` | Checks worklets, the frame clock and idle clocks, the worklets API, pure and opaque draw, the opacity contract, per-frame allocation, the Skia API, where computed canvases and surface files live, accessibility, lifecycle, the clock decisions and the reduce-motion source | Step 9 and at the end |
| `scripts/check-canvas-files.mjs` | Checks kit files and their imports, the layout probe's containment, surface files, palettes, the contrast pairs (measured in every set, never declared again in `contracts/contrast.json`), timeline and draw tests, goldens and baselines, the iOS 120 Hz key (no override, committed `Info.plist`), the Jest golden project | Steps 2 and 9 and at the end |
| `scripts/selftest.mjs` | Proves both checkers pass the templates and catch each planted bug | After changing a checker or a template |
| `scripts/lib/` | `canvas-scope.mjs` (kit and surface folders, the contract, declared packages), `canvas-contrast.mjs` (the contrast file's keys, WCAG and colour-blind maths), `source-scan.mjs` (synced: worklet, JSX and import helpers) and `plist.mjs` (synced: reads `Info.plist`) | When changing a checker |
| `scripts/check-lib.mjs` | The shared script library (synced; never edit here) | Never by hand |
| `assets/shared.json` | The shared files this skill copies in | When adding a shared file |
| `assets/template-placeholders.json` | The placeholder values the template checks fill in (`tasks`, `progress-grid`) | When renaming the template surface |
| `tests/bases/app/` | Fixture base beside the templates: stand-ins for files other skills own (`AppText`, `renderWithProviders`, `app.config.ts`, `jest.config.js`), `package.json`, a live surface and the contract | When changing a fixture |
| `tests/fixtures/` | One overlay suite per checker: `good/` plus one planted bug per case (`mutation.json` + `EXPECT.txt`) | When adding a rule to a checker |

## Related skills

- `canvas-gestures-and-hit-testing` - touch on the canvas: gestures, hit-testing, drag, the pointer sample (load with this skill for any interactive surface).
- `networking-and-server-state` - the queries, keys and optimistic updates a server-fed surface reads.
- `realtime-game-loop` - fixed-step loops, simulate-then-replay and live surfaces.
- `game-rules-engine` - rules, events and seeded randomness for game boards.
- `audio-and-haptics-feedback` - the audio and haptics ports the cue scheduler calls.
- `accessibility-as-code` - contrast and colour-blind checks of the palettes, the live reduce-motion value, per-cell actions.
- `golden-and-snapshot-tests` - the golden policy and accepting baselines.
- `performance-budgets` - frame-time recording and on-device budgets.
- `i18n-strings-and-catalogs` and `rtl-and-direction` - the describe keys, digits and direction.
- `unit-and-component-tests` - the Jest projects, the Skia unit mock and the device-only marker.
- `design-system-structure` - the tokens the palettes take their values from, and `AppText`.
- `e2e-maestro` and `debug-menu-and-test-hooks` - flows that read the canvas probe, and the switch that shows it.
- `motion-and-animation` - Reanimated animations of ordinary views.
- `icons-app-icon-and-splash` - code-drawn icons and store art from the same Skia code.
- `expo-sdk-upgrade` - moving Skia, Reanimated and Worklets to the next SDK.
