---
name: canvas-gestures-and-hit-testing
description: "Turns canvas taps, swipes, drags and aim into typed intents: one gesture module, hit-testing on the drawn layout. Use when a Skia canvas takes touch or a tap hits the wrong cell. Not for drawing (skia-canvas-rendering)."
---

# Canvas gestures and hit-testing

Every touch on a hand-drawn canvas (a progress grid, a planner, a chart, a game board) goes through one
gesture module, `useCanvasGestures`, which hit-tests against the same `CanvasLayout` the renderer draws
with and emits at most one typed `CanvasIntent` per gesture; the surface's pure `intentToAction(state,
intent)` alone decides whether it becomes a domain action. This skill ships that input kit
(`src/canvas/gestures/`), the shape of each surface's intent function and hit-targets test, and a
checker that proves both.

## Rules that must hold

1. **One gesture module builds every canvas gesture:** `src/canvas/gestures/use-canvas-gestures.ts`
   (`Gesture.*` builders on Gesture Handler 2.x, hooks on 3.x). No builder or gesture hook in the canvas
   kit, a surface folder, a file that renders a canvas or feeds one (a hook named in a canvas
   `GestureDetector` or `SurfaceCanvas input`), or the feature folder of a canvas that takes touch. A
   self-contained control there (a sheet's own `GestureDetector`) is ordinary UI; a gesture hook that is
   ordinary UI is listed in `contracts/canvas-input.json` `gestureExempt`. Why: a Gesture Handler major then rewrites one file, and no second gesture can
   double-fire on a canvas.
2. **One gesture yields at most one intent,** emitted in `onEnd` (`onStart` for long press), never in
   `onUpdate`/`onChange`; every pan has an `onFinalize` that resets the pointer (or the stick command).
   Why: a drag that emitted per update would apply many actions, and a cancelled drag (a call, the
   system back gesture) must not leave its preview behind.
3. **Hit-testing uses the surface's shared layout with slop:** `hitTest(layout.get(), point,
   HIT_SLOP)` on the derived layout the picture draws with (`useSurfacePlayer().layout`). Why: draw and
   touch cannot drift at any canvas size, and taps on the outer edge still land.
4. **Meaning and legality live only in the surface's pure intent function:** `intentToAction(state,
   intent)` in the surface folder beside `to-view.ts` (a game surface: `intent-to-move.ts`,
   `intentToMove`). It builds a candidate and returns it only when the domain's one source of truth
   accepts it (`listActions(state)` lists it, or `validate(state, action)` passes), and imports no
   React, React Native, Expo, Skia, store, service, API or UI value. Why: tests, undo, hints, bots and
   replays share one definition of allowed, and a finished or locked state gives `null`.
5. **The intent function handles every intent kind explicitly** (`tap`, `long-press`, `swipe`,
   `drag-end`, `aim`), returning `null` for the kinds the surface ignores. Why: an exhaustive switch
   turns a new kind into a compile error instead of a silent no-op.
6. **A tap-then-tap selection is screen UI state, never domain state or an action.** The model hook
   keeps it and passes it as `highlight.selected`; the gesture layer always sends `selected: null` and
   the model hook fills it in; a tap inside a select region only selects; a miss or an applied action
   clears it. Why: the store, undo, persistence, analytics and automated players never see a selection.
7. **The drag lift is applied once, in the gesture layer** (`surface.dragLiftPt`, default 0), to the
   hover, the drawn preview and the drop target; the intent function and `draw()` add none, and a
   surface with a lift keeps that much canvas below its last row (`unreachableByDrag` proves it). Why:
   the preview cell is then always the drop cell, and no edge row becomes unreachable.
8. **Touches are physical.** Gesture code never reads the writing direction; a surface that mirrors in
   right-to-left locales does it in its layout (regions mirrored as rectangles, never the touch point),
   and swipe directions stay physical. Why: `event.x/y` do not mirror under RTL (verified on iOS), so
   flipping again sends touches to the wrong cell.
9. **Per-frame finger state stays on the UI thread:** the `pointer` shared value feeds the picture
   (`frame.fx.pointer`); only hover changes cross to JS, behind `isSameTarget`. Why: a React render
   per finger move cannot fit a 120 Hz frame (8.3 ms).
10. **Every tappable region is at least `MIN_TOUCH_PT` on the smallest supported canvas,** proven by
    a hit-targets test with `smallestTargetPt`; `MIN_TOUCH_PT` follows `quality-gates.json`
    `a11y.minTouchPt` (44 pt; 48 for Material-sized Android designs). Fix the layout, never the test,
    never `hitSlop`. Why: accessibility-as-code's target minimum applies to canvas cells too.
11. **No React Native touch on a canvas, and the app's outermost view is `GestureHandlerRootView`.** No
    Pressable, Touchable or button inside a canvas `GestureDetector` or around a `<Canvas>`/`<SurfaceCanvas>`,
    and no `onPress*`/`onLongPress`/`onTouch*`/`onResponder*` on the canvas or on the element that directly
    wraps it; a whole-card press around a display-only canvas is an ordinary control, listed in
    `gestureExempt`. Why: React Native's touch system hit-tests on its own (no shared layout, no slop, no
    single intent) and competes with Gesture Handler; without the root view no gesture fires on a device.
12. **Everything a gesture callback calls is a `'worklet'` module** (`classify-swipe.ts`,
    `stick-command.ts`, `pan-intent.ts`, the kit's `canvas-layout.ts`) importing values only from other
    `'worklet'` modules; JS is reached with `scheduleOnRN` (never `runOnJS`), shared values with
    `.get()`/`.set()` (never `.value`). Why: a plain function throws on the UI thread on a device while
    every Jest test passes, and React Compiler needs the accessors.
13. **Gesture Handler follows the Expo SDK's pin** (`npx expo install`; ~2.32.0 on SDK 57): the builder
    API on 2.x, the hook API on 3.x, never mixed, the gesture module migrated whole. Why: the 3.x
    composition hooks accept only 3.x gestures.
14. **Continuous values are quantised before they enter state:** an aim vector becomes integers
    (thousandths of a unit vector, `Math.sqrt` only) inside the intent function. Why: saves stay
    compact and replays exact on every device.
15. **Continuous input for a simulation is an integer stick command** (games): 0 idle, 1 to 16 by the
    largest dot product with a committed table, a 12 pt dead zone, written only on change, 0 on lift.
    Why: a fixed-step simulation replays bit-exactly only from integer `(tick, command)` logs.
16. **Pans stay clear of the system back gestures:** the stack screen of a canvas that reads
    horizontal swipes or drags sets `fullScreenGestureEnabled: false` (iOS 26 turns full-screen back on
    by default) and the canvas keeps off the side edges (iOS edge swipe, Android gesture navigation).
    Why: the system claims those swipes first, so the move goes back instead.
17. **A hold-only action has a non-hold alternative** (a mode toggle on the screen, or an
    accessibility action on the canvas). Why: VoiceOver and TalkBack users cannot aim a hold at a cell.

## Workflow

1. **Read [references/input-pipeline.md](references/input-pipeline.md)** and pick the surface's pan
   mode (`none`, `swipe`, `drag`, `aim`; a simulation uses the stick,
   [references/stick-input.md](references/stick-input.md)). Input needs the canvas kit's
   `src/canvas/canvas-layout.ts` and `canvas-types.ts`: when they are missing, set the kit up with
   `skia-canvas-rendering` first (this skill's `templates/src/canvas/` holds identical synced copies).
2. **Copy the input kit.** Copy `templates/src/canvas/gestures/` to `src/canvas/gestures/` verbatim,
   and `templates/contracts/canvas-input.json` with its schema to `contracts/` (replace `__FEATURE__`
   and `__SURFACE__`, list `buttonComponents`). Make `GestureHandlerRootView` the app's outermost view
   (input-pipeline.md, "The root view"). Run `node ${CLAUDE_SKILL_DIR}/scripts/check-canvas-input.mjs .`:
   it names every missing piece.
3. **Write the intent function test-first.** Read
   [references/intent-to-action.md](references/intent-to-action.md) and shape it like
   [examples/progress-grid/](examples/progress-grid/) (tap to act),
   [examples/inbox-planner/](examples/inbox-planner/) (drag with a lift, tap-then-tap),
   [examples/sliding-puzzle/](examples/sliding-puzzle/) (swipe) or
   [examples/arena-aim/](examples/arena-aim/) (aim). Keep the finished-state, ignored-kind and
   legality-property tests. A game surface keeps `intent-to-move.ts` in its canvas folder (game rules
   cannot import the canvas kit); games may import `src/canvas/**` by default
   (architecture-and-boundaries' `gameFacing` defaults), so no contract entry is needed.
4. **Prove touch targets.** Write the surface's `hit-targets.test.ts` like the examples: the largest
   view laid out on the smallest supported canvas, `smallestTargetPt(layout) >= MIN_TOUCH_PT`, and with
   a lift `unreachableByDrag(layout, edgeRowTargets(...), DRAG_LIFT_PT)` empty on portrait and wide
   canvases. A region below the minimum changes the layout, not the test.
5. **Wire the screen.** The feature's model hook calls `useCanvasGestures(player.layout, { panMode,
   dragLiftPt: surface.dragLiftPt ?? 0, onIntent, onHover, onMiss })`, keeps the selection, dispatches
   non-null actions and hands `input` and `highlight` to `<SurfaceCanvas>`
   ([examples/progress-grid/use-progress-grid-input.ts](examples/progress-grid/use-progress-grid-input.ts)).
   Set the stack screen's gesture options (rule 16) in the route's layout.
6. **Run the tests:** `npx jest src/canvas/gestures src/features/<feature> --ci --selectProjects unit`
   (paths first: `--selectProjects` takes several values and would swallow them). Gesture tests follow
   [references/testing-gestures.md](references/testing-gestures.md).
7. **Lint, format and type-check:** `npx eslint --fix` and `npx prettier --write` on the new files, then
   `npm run typecheck`.
8. **Run the check** `node ${CLAUDE_SKILL_DIR}/scripts/check-canvas-input.mjs .` (or `--surface <id>`
   to limit the surface side), fix every `FAIL` line (each names the file, the rule and the fix) and
   rerun until it prints `RESULT: PASS`.
9. **Touch it for real** on a named iOS simulator and a named Android emulator (testing-gestures.md,
   "On devices"): tap the outer cells, drag to the edge rows, cancel a drag mid-way, try tap-then-tap,
   switch to an RTL locale, swipe near the screen edges, and use the non-hold alternative with
   VoiceOver and TalkBack. When the Expo SDK moves Gesture Handler, follow
   [references/gesture-handler-versions.md](references/gesture-handler-versions.md).

## Definition of done

- [ ] `src/canvas/gestures/` holds the kit and `npx jest src/canvas/gestures --ci --selectProjects unit`
      passes: tap → cell with `selected: null`, a miss → `onMiss`, drag → one `drag-end`, a cancelled
      drag → nothing, swipe → one direction, hover on change only, a lifted drag's hover and drop on
      one cell, long press → cell, stick → integer commands, touch-target helpers.
- [ ] Each surface that takes touch has its pure intent function in the surface folder, listing every
      intent kind and returning only actions the domain accepts; its test covers each used kind,
      illegal targets, ignored kinds, a finished or locked state and a legality property (plus
      select-region taps and drag ≡ tap-then-tap for a selecting surface).
- [ ] Each tappable surface's `hit-targets.test.ts` proves `MIN_TOUCH_PT` on the smallest supported
      canvas, and a surface with a drag lift proves every edge row reachable on portrait and wide canvases.
- [ ] No gesture outside the gesture module in the canvas scope, no button inside a canvas
      `GestureDetector`, no React Native touch on a canvas, `GestureHandlerRootView` outermost, and the canvas screen's stack options keep
      the system back gestures off horizontal pans (checked on both platforms).
- [ ] `npm run typecheck`, `npx eslint --max-warnings 0` and `npx prettier --check` pass; no
      `__PLACEHOLDER__` is left.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-canvas-input.mjs .` prints `RESULT: PASS`

The checker prints one SKIP only while the root layout does not exist yet
(`SKIP src/app/_layout.tsx [gesture-root] not yet created (app-startup-and-bootstrap creates it)`),
and `NOT APPLICABLE` when no canvas takes touch (no input kit, no contract surface, no surface with an
intent file or a `useCanvasGestures` caller, no `SurfaceCanvas` input, no gesture and no React Native
touch in the canvas scope); a contract holding only `gestureExempt` or `buttonComponents` asks for nothing.

## Anti-patterns

- **A `Gesture.Tap()` in a feature component or screen around the canvas.** It skips hit-testing and the
  one-intent rule; add a mode to `use-canvas-gestures.ts` and consume its intents.
- **A `select-*` action or a `selected` field in the store for tap-then-tap.** Undo, persistence and bots
  see it; keep it in the model hook, list the region in `SELECT_REGIONS`, read `intent.selected`.
- **Adding a lift in the intent function or in `draw()` (`row - 1`).** The preview and the drop drift
  apart and an edge row becomes unreachable; set `dragLiftPt` on the surface.
- **Checking legality in a gesture worklet.** The domain cannot run there safely and bots would
  disagree with fingers; return the intent and let the intent function decide.
- **Emitting intents from `onUpdate` "for responsiveness".** One drag becomes many actions; show
  responsiveness through the pointer preview and emit on release.
- **Mirroring `event.x` for right-to-left.** The layout already mirrors surfaces that opt in.
- **Storing a raw gesture float (an angle, a velocity) in state.** Quantise it to integers first.
- **Growing hit areas with `hitSlop` or shrinking the test's grid to reach 44 pt.** Fix the layout; the
  slop is the fixed 8 pt `HIT_SLOP` of hit-testing, not a substitute for size.
- **Spying on a mocked shared value** (`jest.spyOn(sv, 'set')`): the mock's members are read-only;
  pass a recording stand-in.
- **A new helper for a gesture callback in a plain module.** Every Jest test passes and the first touch
  on a device throws; put it in a `'worklet'` module.
- **Mixing 3.x hooks with 2.x builders during an upgrade.** They cannot compose; migrate the module whole.
- **A `Pressable` around the canvas, or `onTouchStart` on it, "just for one tap".** It hit-tests beside
  the layout and double-fires with the gesture module; add the mode to `use-canvas-gestures.ts`.
- **An inline `style={{ flex: 1 }}` on `GestureHandlerRootView`.** The canonical lint bans inline
  styles; use a `StyleSheet` style.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/input-pipeline.md](references/input-pipeline.md) | The pipeline, `CanvasIntent`, hit-testing, composition and thresholds, pan modes, pointer and drag lift, RTL, touch targets, the root view, the detector and React Native touch on a canvas, system back gestures on iOS and Android, accessibility and E2E taps, the contract and config keys, When multi-package | Workflow step 1, before any input work |
| [references/intent-to-action.md](references/intent-to-action.md) | Rules for the intent function, the two legality forms, patterns (tap, drag with a lift, tap-then-tap, swipe, aim, long press), wiring the screen, games, tests | Steps 3 and 5 |
| [references/testing-gestures.md](references/testing-gestures.md) | Jest set-up, what each test proves, driving gestures, mock traps, checks on named iOS simulators and Android emulators | Step 6, step 9, and when a gesture test misbehaves |
| [references/stick-input.md](references/stick-input.md) | Integer stick commands for simulations and their tests | Step 1 for real-time games |
| [references/gesture-handler-versions.md](references/gesture-handler-versions.md) | Gesture Handler 2.32 today, the 3.x hook mapping (verified on 3.2.1) and the one-file migration | When the Expo SDK moves Gesture Handler, or when reading 3.x examples |
| `templates/src/canvas/gestures/` | The input kit: `canvas-intent.ts`, `classify-swipe.ts`, `pan-intent.ts`, `stick-command.ts`, `touch-targets.ts`, `use-canvas-gestures.ts`, the two test probes, and a test for each module | Step 2 (copy verbatim) |
| `templates/src/canvas/` (other files) | `canvas-layout.ts` (+ test), `canvas-types.ts`, `timeline/` (+ test): synced canonical copies of the canvas kit's contract files (skia-canvas-rendering owns them) | Step 1, only when the app has no canvas kit yet |
| `templates/contracts/` | `canvas-input.json` (the surfaces that take touch, button components, exemptions) and its JSON schema | Step 2 |
| [examples/progress-grid/](examples/progress-grid/) | Tasks progress grid: tap to toggle a day; `intent-to-action.ts` (+ test), `progress-grid-rules.ts` (the legality list), `hit-targets.test.ts`, `use-progress-grid-input.ts` (the screen wiring) | Steps 3 to 5 |
| [examples/inbox-planner/](examples/inbox-planner/) | Drag an inbox task onto a day, or tap-then-tap; a drag lift with edge-row proofs on portrait and wide canvases | Steps 3 and 4, for drag and selection |
| [examples/sliding-puzzle/](examples/sliding-puzzle/) | Games: swipe to slide (the 15-puzzle), rules in `rules/`, `intentToMove` in the surface folder | Step 3, for swipe surfaces |
| [examples/arena-aim/](examples/arena-aim/) | Games: pull back and release, aim quantised to integers, with a property test | Step 3, for aim surfaces |
| `scripts/check-canvas-input.mjs` | Checks the kit, its worklets, the one gesture module, test ids, single intents, hover on change, pan finalize, slop, physical coordinates, detector children, React Native touch on a canvas (`canvas-rn-touch`), the root view, the intent function (present, tested, pure, exhaustive), touch-target tests and gate, the API version and the Worklets API | Steps 2 and 8, and at the end |
| `scripts/lib/input-scope.mjs` | Where the checker looks: layout, config keys, the contract, surfaces and which take touch | When changing the checker |
| `scripts/lib/source-scan.mjs` | Synced source helpers (masking, JSX tags, imports, worklet directive) | When changing the checker |
| `scripts/check-lib.mjs` | The shared script library (synced; never edit here) | Never by hand |
| `scripts/selftest.mjs` | Proves the checker passes the templates and examples and catches each planted bug | After changing the checker, a template or an example |
| `tests/bases/app/` | Fixture base: stand-ins for files other skills own (the root layout, `SurfaceCanvas`, the progress-grid model, view, layout and surface, the screen and model hook), `package.json`, `quality-gates.json` | When changing a fixture |
| `tests/fixtures/` | One overlay suite: `good/` plus one planted bug per case (`mutation.json` or `DELETE.txt`, `EXPECT.txt`) | When adding a rule to the checker |
| `assets/shared.json` | The shared files this skill copies in | When adding a shared file |
| `assets/template-placeholders.json` | The placeholder values the template checks fill in (`tasks`, `progress-grid`) | When renaming the template surface |

## Related skills

- `skia-canvas-rendering` - the picture, `CanvasLayout`, `PointerSample`, `SurfaceCanvas` and the drag preview this skill feeds (load both for an interactive canvas).
- `accessibility-as-code` - the touch-target minimum, hold alternatives and the canvas's spoken summary.
- `unit-and-component-tests` - the Jest projects, `jest.setup.ts` and test forms the gesture tests follow.
- `naming-conventions` - testID grammar and kebab-case kinds.
- `state-management-zustand` - the store whose dispatch receives the actions.
- `react-components-and-hooks` - model hooks and React Compiler rules for the wiring.
- `app-startup-and-bootstrap` - the root layout that holds `GestureHandlerRootView`.
- `navigation-and-routing` - stack screen options for back gestures.
- `rtl-and-direction` - which surfaces mirror and how direction switches.
- `e2e-maestro` - tapping canvas cells from the published layout on both platforms.
- `realtime-game-loop` - the fixed-step loop that consumes stick commands.
- `game-rules-engine` and `game-session-host` - `listMoves`, hints and the game screen.
- `expo-sdk-upgrade` - the SDK move that brings Gesture Handler 3.
