---
name: motion-and-animation
description: Catalogs each animation as a Reanimated 4 moment. Use when animating a transition, sheet, loop, drag, spring or celebration, or one ignores Reduce Motion or blocks taps. Not for canvases (skia-canvas-rendering).
---

# Motion and animation

Makes every moving thing in an Expo app a declared moment: named once in a catalog with what starts
it, the motion tokens it spends and what it shows when motion is reduced; built with Reanimated 4 on
the UI thread from wherever it is now; never in the way of the next touch; looping only while someone
can see it; celebrating within a budget, once. One checker proves the code and the catalog agree.

## Rules that must hold

1. **Declare every moment once, in the moment catalog** (`src/ui/motion/motion-moments.ts`): its
   kind, a trigger a reviewer can find in the app, its timing as token names (`{ duration, easing,
   delay?, stagger? }`, `{ spring }` or `{ navigator: 'stack' }`) and its reduced alternative; plain
   data with type-only imports. Why: a moment nobody declared is a library default chosen by nobody,
   and it never meets the reduce-motion review (`moment-catalog`, `moment-tokens`).
2. **Every file that animates names its moment.** It takes timing through `timingOf` / `springOf` /
   `delayOf` / `staggerOf(MOTION_MOMENTS.<id>)` (`moment-config.ts`), or, when it cannot import the
   catalog (the shared press surface, a file rendering a native `<Stack>`), the moment lists it in
   `files` and the file spends the token the moment names; nothing declared goes unused. Why: the
   catalog stays a true list only if code cannot move without it (`moment-declared`,
   `moment-files`, `moment-unused`).
3. **Every moment declares what reduced motion shows, as its kind allows:** feedback `instant`,
   `fade` or `none`; state `instant` or `fade`; transition `fade`, `instant` or `none`; attention
   `static` or `none`; celebration `static`, `fade` or `none` (`none` when drawn with
   `<CelebrationBurst>`); functional `unchanged` only; a `fade` uses `REDUCED_FADE` or
   `reducedEntering()` in code. Why: the end state must be identical with motion off (WCAG 2.3.3),
   and "it is small" is not an alternative (`moment-reduced`).
4. **Reduce motion reaches every animation from one root.** The root layout, or a file it renders,
   mounts accessibility-as-code's `<MotionConfig preference>` and starts `watchSystemA11y()`;
   anything that reads `useReduceMotion()` or `useScreenAnimation()` renders below `<MotionConfig>`,
   never in the component that mounts it; only a functional moment's file (and the reduced fade in
   `moment-config.ts`) passes `ReduceMotion.Never`. Why: without the config no `withTiming`,
   `withSpring` or layout animation sees the in-app setting or a live switch; context flows down
   only, so the mounting component reads the default `'system'`; without the watcher
   `useReduceMotion()` stays false (`reduce-motion-root`, `reduce-motion-opt-out`).
5. **What the root cannot reach reads the answer itself.** Reanimated CSS animations and
   transitions carry the condition on the key (`transitionProperty: isReducedMotion ? 'none' : ...`;
   a bare `transitionDuration` transitions `'all'`);
   every native `<Stack>` takes `animation: useScreenAnimation()`; React Native's `LayoutAnimation`
   is not used. Why: Reanimated 4.5.1 applies no reduce-motion setting to CSS, and
   react-native-screens 4.26.2 reads none (both verified in source) (`css-motion-reduced`,
   `screen-transition-reduced`, `reanimated-only`).
6. **Loop only through `useMotionLoop(moment, { isFocused })`.** It runs while the screen is
   focused, the app is active and motion is not reduced, and cancels a running loop when that
   changes. Why: Reanimated decides reduce motion once, when an animation starts, so a running loop
   ignores the switch; a pushed screen keeps the one below mounted, loop and battery drain included
   (`loop-through-hook`).
7. **Motion decorates state; it never is the state.** Commit in the handler first, then animate; no
   completion callback hands work back to JS outside a functional moment; nothing switches input off
   while something moves. Why: an interrupted animation calls back with `finished: false`, so the
   commit never happens, and a locked control reads as a frozen app (`commit-before-motion`,
   `no-input-lock`).
8. **Every animation is interruptible.** Retarget from the current value (never snap to the start
   first), let the finger catch the motion, and give a spring started when a drag, pinch or rotation
   ends the gesture's velocity (tap, long-press and fling events carry none). Why: Reanimated starts a new animation where the old one is and a spring keeps its
   momentum; a reset snaps, and a flick without velocity feels dead (`no-reset-before-animate`,
   `gesture-velocity`).
9. **Sequence on the UI thread.** `withDelay` and `withSequence`, never `setTimeout`, `setInterval`
   or `requestAnimationFrame` to start or stop an animation. Why: `withDelay` skips its delay under
   reduced motion, while a JS timer waits it out, drifts from the frames and fires after unmount
   (`no-timer-sequencing`).
10. **Frames stay on the UI thread.** No `scheduleOnRN` or React setter inside `useAnimatedStyle`,
    `useDerivedValue`, `useAnimatedProps`, `useFrameCallback`, a scroll handler or a gesture's
    `onUpdate` / `onChange`; cross once in `onEnd` or a `useAnimatedReaction`; `scheduleOnRN`, never
    the deprecated `runOnJS` / `runOnUI`. Why: one React render per frame is the jank Reanimated
    exists to remove (`no-js-per-frame`, `worklets-api`).
11. **Animate transform and opacity.** A layout key in `useAnimatedStyle` (`width`, `top`,
    `margin`...) needs `// motion-layout: <reason>` on the line above (an absolutely positioned,
    childless fill); laid-out size changes use layout animations. Why: a layout key re-runs Yoga for
    the node and its siblings on every frame (`compositor-props`).
12. **Celebrations are bounded, played once and skippable.** A celebration counts its `pieces` and
    ends within `CELEBRATION_LIMITS` (library ceilings 2000 ms and 40 pieces, computed from the
    tokens), plays through `useCelebration` from the handler that committed the result (never a
    `useEffect` or focus effect), starts at the point of action and takes no touch. Why: an unbounded flourish is a
    loading screen nobody asked for, and a mount-effect trigger replays it on every remount
    (`celebration-budget`, `celebration-through-hook`).

Owned elsewhere and only cited here: motion token values, complete springs and `no-raw-duration`
(design-system-structure); `useReduceMotion`, `MotionConfig` and the ban on Reanimated's
`useReducedMotion` (accessibility-as-code); `.get()` / `.set()` (react-components-and-hooks); when
sounds and haptics play (audio-and-haptics-feedback); canvas timelines (skia-canvas-rendering).

## Workflow

1. **Detect.** `package.json` must depend on `react-native-reanimated` (`npx expo install
   react-native-reanimated react-native-worklets`; `babel-preset-expo` adds the Worklets plugin);
   without it check-motion prints NOT APPLICABLE. The catalog reads design-system-structure's
   `src/theme/motion.ts`, and the root wiring uses accessibility-as-code's `src/ui/a11y/`.
2. **Set up once.** Copy `templates/src/ui/motion/` to `src/ui/motion/`; copy
   `templates/src/ui/a11y/` and `templates/src/hooks/` only where the app lacks them (synced,
   identical canonical copies). Replace `__ROOT_STACK_FILE__` in the catalog with the file that
   renders the root `<Stack>` and list every other `<Stack>` file there. Start `watchSystemA11y` in
   the root layout and mount `<MotionConfig>` around the navigator, every `<Stack>` taking
   `useScreenAnimation()` in a component rendered below `<MotionConfig>`, as
   [examples/root-layout.tsx](examples/root-layout.tsx),
   [examples/root-stack.tsx](examples/root-stack.tsx) and
   [examples/app-stack.tsx](examples/app-stack.tsx) show. Read
   [references/reduce-motion-and-interruption.md](references/reduce-motion-and-interruption.md).
3. **Decide whether it should move.** Read [references/moment-catalog.md](references/moment-catalog.md)
   ("Should it move at all", kinds, tokens, choreography). If the answer is no, there is no moment.
4. **Declare the moment.** Add the entry: kind, trigger, token names (a missing token goes into the
   token file first, design-system-structure), the reduced alternative its kind allows, `pieces` for
   a celebration, `cue` when the commit plays a sound or haptic. Imitate
   [examples/tasks-motion-moments.ts](examples/tasks-motion-moments.ts). Review with
   `node ${CLAUDE_SKILL_DIR}/scripts/check-motion.mjs . --table`.
5. **Build it with the right tool** ([references/reanimated-4-in-practice.md](references/reanimated-4-in-practice.md),
   "Choosing the tool"): a state change follows its value
   ([examples/task-check.tsx](examples/task-check.tsx)); enter and exit are layout animations with
   `reducedEntering()` ([examples/task-list-row.tsx](examples/task-list-row.tsx)); a drag springs
   with the finger's velocity ([examples/task-sheet.tsx](examples/task-sheet.tsx)); a loop uses
   `useMotionLoop` ([examples/sync-badge.tsx](examples/sync-badge.tsx)); a celebration uses
   `useCelebration` and `<CelebrationBurst>` from the committing handler
   ([examples/task-check-cell.tsx](examples/task-check-cell.tsx)); a CSS transition carries the
   condition on its key ([examples/due-chip.tsx](examples/due-chip.tsx)); a fill that must animate
   its width carries the marker ([examples/progress-bar.tsx](examples/progress-bar.tsx)); a safety
   timer is a functional moment ([examples/hold-to-delete.tsx](examples/hold-to-delete.tsx)).
6. **Test it.** Read [references/testing-motion.md](references/testing-motion.md): fake timers,
   the `<MotionConfig preference>` wrapper, the end state with motion reduced, an interruption, a
   loop's stop conditions, a celebration's once-per-event rule.
7. **Run the checks** from the repo root and loop until each passes: `npm run typecheck`,
   `npx eslint . --max-warnings 0`, `npx jest --ci`, then
   `node ${CLAUDE_SKILL_DIR}/scripts/check-motion.mjs .`. Each `FAIL` line names the file, the rule
   and the fix: fix the code or the catalog, never widen `CELEBRATION_LIMITS` past its ceilings or
   mark a moment functional to escape a rule. When installed, also run design-system-structure's
   `check-raw-values` and accessibility-as-code's `check-a11y-code` (they own the token and hook rules).
8. **Ask for the device pass (human step).** A release build on a named iOS simulator and a named
   Android emulator, each changed moment recorded with motion on and reduced, interrupted on
   purpose, haptics felt on a real phone (reduce-motion-and-interruption.md, "Trying it on
   devices"). Report the `--table` output, the checks that passed and any SKIP line.

## Definition of done

- [ ] Every moment the change touches is in the catalog with a kind, a trigger, token timing and a
      reduced alternative its kind allows; the `--table` output is in the report.
- [ ] Animating code takes its timing through `moment-config.ts`; shared primitives and `<Stack>`
      files are listed in their moment's `files`; no placeholder is left.
- [ ] The root starts `watchSystemA11y` and mounts `<MotionConfig>`; every `<Stack>` uses
      `useScreenAnimation()`; CSS animations carry the reduce-motion condition on their key.
- [ ] Loops run through `useMotionLoop`, celebrations through `useCelebration` from the committing
      handler; nothing locks input; no completion callback commits outside a functional moment.
- [ ] Tests prove the end state with motion reduced and an interruption; `npm run typecheck`,
      `npx eslint . --max-warnings 0` and `npx jest --ci` pass.
- [ ] The developer has been asked for the device pass (release build, both platforms, motion on
      and reduced).
- [ ] Expected SKIP lines only while their target is not created yet:
      `SKIP src/ui/a11y/motion-config.tsx [reduce-motion-root] not yet created (accessibility-as-code creates it)`,
      `SKIP src/app/_layout.tsx [reduce-motion-root] not yet created (expo-project-bootstrap creates it)`,
      `SKIP src/theme/motion.ts [moment-tokens] not yet created (design-system-structure creates it)`.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-motion.mjs .` prints `RESULT: PASS`

## Anti-patterns

- **A duration or a spring chosen in the component.** It escapes the catalog and the reduce-motion
  review; declare the moment and take `timingOf(MOTION_MOMENTS.<id>)`.
- **A moment whose reduced alternative is "it is short anyway".** Pick from the kind's list; the
  end state must be reachable with motion off.
- **Reanimated's `useReducedMotion()`, or a second "animations off" switch for screenshots.** Read
  `useReduceMotion()`; screenshot runs pass `preference="on"` to `<MotionConfig>`.
- **A `withRepeat(..., -1)` in a component.** It keeps running off screen, in the background and
  after Reduce Motion turns on; use `useMotionLoop`.
- **A Reanimated CSS animation or a native stack slide with no reduce-motion condition.** Neither
  follows the root config; put the condition on the key, use `useScreenAnimation()`.
- **`setTimeout(() => sv.set(withSpring(1)), 700)`.** Use `withDelay(delayOf(m), ...)`; the timer
  waits under reduced motion and fires after unmount.
- **Removing a row in `withTiming(0, cfg, () => scheduleOnRN(remove))`.** An interrupted fade never
  removes it; remove it in the handler and give the row `exiting`.
- **`disabled={isAnimating}` or `pointerEvents: isCelebrating ? 'none' : 'auto'`.** Let the next
  touch interrupt or `skip()`; decorative layers take no touch at all.
- **`x.set(0); x.set(withTiming(1))` on every press.** An interrupted animation snaps back; animate
  from where it is.
- **A release spring without the gesture's velocity, or `scheduleOnRN` in `onUpdate`.** The flick
  dies, or React renders every frame; pass `velocity`, commit in `onEnd`.
- **Animating `height` or `top` because it was easier.** Animate a transform, use a layout
  animation, or mark the one childless fill that must keep `width`.
- **Celebrating from a mount effect, or with an endless confetti loop.** It replays on every
  remount and never ends; `useCelebration().play(eventKey)` from the handler, within the budget.
- **Marking a moment `functional` to use `ReduceMotion.Never`, or raising `CELEBRATION_LIMITS`.**
  Both silence the rule the person relies on; stop and ask the developer if a rule looks wrong.
- **Judging feel in Expo Go, a development build or the simulator alone.** Feel is checked on a
  release build, on both platforms, with motion on and reduced.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/moment-catalog.md](references/moment-catalog.md) | Why one catalog, every field, kinds and their reduced alternatives, timing shapes, the should-it-move gate, token roles, choreography and direction, cues, `files`, the celebration budget, `--table`, config keys, multi-package | Workflow steps 3 and 4 |
| [references/reanimated-4-in-practice.md](references/reanimated-4-in-practice.md) | Verified APIs (4.5.1, Worklets 0.10.1, Gesture Handler 2.32, screens 4.26.2): setup, runtimes, choosing the tool, retargeting, callbacks, delay/sequence/repeat under reduced motion, layout and CSS animations, gestures, property costs, native stack, iOS and Android notes, troubleshooting | Workflow step 5, any Reanimated question |
| [references/reduce-motion-and-interruption.md](references/reduce-motion-and-interruption.md) | The one answer, root wiring, what the root reaches and what it does not, each kind in code, the reduced fade, loop stop conditions, interruption, commit first, device toggles on named devices, screenshots held still | Workflow steps 2 and 8 |
| [references/testing-motion.md](references/testing-motion.md) | Jest setup, fake timers, the MotionConfig wrapper, what to assert, recipes (end state, interruption, loop, celebration, functional timer), what Jest cannot prove | Workflow step 6 |
| `templates/src/ui/motion/` | The catalog template (`motion-moments.ts`: kinds, reduced alternatives, token types, `CELEBRATION_LIMITS`, press, release, screen push) and its Jest twin; `moment-config.ts` (timing, spring, delay, stagger, celebration plan, the reduced fade); `use-motion-loop.ts`; `use-celebration.ts`; `use-screen-animation.ts`; `celebration-burst.tsx` and `burst-piece.tsx`; each with its test | Workflow step 2 (copy to `src/ui/motion/`) |
| `templates/src/ui/a11y/` | accessibility-as-code's system store, `useReduceMotion` and `MotionConfig` with their tests (synced; never edit here) | Workflow step 2, only when the app has none |
| `templates/src/hooks/` | react-components-and-hooks' `use-is-app-active.ts` with its test (synced; never edit here) | Workflow step 2, only when the app has none |
| [examples/tasks-motion-moments.ts](examples/tasks-motion-moments.ts) | A Tasks catalog using every kind of moment | Workflow step 4 |
| [examples/root-layout.tsx](examples/root-layout.tsx) | The root layout starting the system accessibility store, with the gesture root | Workflow step 2 |
| [examples/root-stack.tsx](examples/root-stack.tsx) | The providers above the root Stack: MotionConfig with the saved preference, reading nothing itself | Workflow step 2 |
| [examples/app-stack.tsx](examples/app-stack.tsx) | The root Stack rendered below MotionConfig, animations from `useScreenAnimation()`; listed in `screenPush.files` | Workflow step 2 |
| [examples/task-check.tsx](examples/task-check.tsx) | A state moment that retargets from where it is | Workflow step 5 |
| [examples/task-check-cell.tsx](examples/task-check-cell.tsx) | A celebration played from the committing handler, drawn at the point of action | Workflow step 5 |
| [examples/task-list-row.tsx](examples/task-list-row.tsx) | Enter and exit as layout animations, reduced fade | Workflow step 5 |
| [examples/task-sheet.tsx](examples/task-sheet.tsx) | A drag caught mid-flight, released with the finger's velocity | Workflow step 5 |
| [examples/sync-badge.tsx](examples/sync-badge.tsx) | An attention loop through `useMotionLoop` | Workflow step 5 |
| [examples/due-chip.tsx](examples/due-chip.tsx) | A Reanimated CSS transition gated on reduce motion | Workflow step 5 |
| [examples/progress-bar.tsx](examples/progress-bar.tsx) | The one sanctioned layout key, with its marker | Workflow step 5 |
| [examples/hold-to-delete.tsx](examples/hold-to-delete.tsx) | A functional timer that never shortens and commits on completion | Workflow step 5 |
| `scripts/check-motion.mjs` | Checker: the catalog, code tied to it, the reduce-motion root and what it cannot reach, loops, celebrations, interruption, UI-thread frames, compositor properties (22 rules; `--table`, `--catalog`, `--root-layout`, `--exclude`; `--help` lists them) | Workflow steps 4 and 7 |
| `scripts/selftest.mjs` | Proves the checker on a full Tasks app built on the templates and on a fresh adoption, and every planted bug | After changing the checker, a template or a fixture |
| `scripts/lib/` | `motion-catalog.mjs` (loads and judges the catalog), `motion-code.mjs` (per-file rules); synced `source-scan.mjs` and `app-modules.mjs` (never edit here) | When changing a rule |
| `scripts/check-lib.mjs` | Shared script helper (synced; never edit here) | Never by hand |
| `assets/shared.json` | Declares the synced files (check-lib, scan and module helpers, the a11y and app-active templates, the token file of the test base) | When adding a shared file |
| `assets/template-placeholders.json` | The placeholder value the reference app fills in (`__ROOT_STACK_FILE__`) | When adding a placeholder |
| `tests/` | `bases/app/` (a neutral Tasks app with every kind of moment and silent planted findings under `.agents/skills/`, `skills/`, `src/canvas/` and a vendored skill folder) and `fixtures/` (overlay suites `check-motion` and `check-motion-adopt`) | When adding a rule |

## Related skills

- `design-system-structure` - the motion tokens, complete springs and the raw-duration ban this skill spends.
- `accessibility-as-code` - `useReduceMotion`, `MotionConfig` and the system store; screen-reader alternatives for holds and gestures.
- `react-components-and-hooks` - `.get()` / `.set()`, effects, and the shared `useIsAppActive` hook.
- `audio-and-haptics-feedback` - the cue table a moment's `cue` names, played at the commit.
- `settings-and-preferences` - the saved "Reduce motion" preference passed to `MotionConfig`.
- `skia-canvas-rendering` - canvas timelines and their reduced timelines.
- `canvas-gestures-and-hit-testing` - gestures on a canvas turned into commands.
- `navigation-and-routing` - the Stack layouts whose animation comes from `useScreenAnimation()`.
- `rtl-and-direction` - which way a horizontal moment moves in right-to-left languages.
- `ui-component-library` - the press surface's users and the hold button built on a functional moment.
- `performance-budgets` - frame-time budgets measured on devices.
- `debug-menu-and-test-hooks` - launching test builds with motion held still.
- `unit-and-component-tests` - the Jest set-up and render helpers the motion tests use.
- Expo's `expo-animation` skill - a broader Reanimated and gesture API reference.
