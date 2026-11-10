---
name: react-components-and-hooks
description: Writes React components and hooks - model hooks, effects, React Compiler, lists, safe areas, error boundaries. Use when writing a component, hook, effect or list. Not for shared UI (ui-component-library).
---

# React components and hooks

Every component and hook in the app follows one set of React rules: function components with
read-only props, a thin route over a pure view and one model hook, effects only for systems outside
React, React Compiler instead of hand-written memoization, pressables only in the UI layer, virtualized
lists with stable keys, layouts that survive any window and both platforms' system bars, and error
boundaries with one way out. A zero-dependency checker proves the rules lint cannot see, on iOS and
Android code alike.

## Rules that must hold

1. **Function components, one per file, with read-only props.** A named export, `type XProps =
   { readonly … }` with `readonly T[]` for arrays, callbacks `onX`, local handlers `handleX`. The only
   class is an error boundary. Why: React Compiler optimizes functions only, and lint does not see
   `props.items.push()`; a read-only type turns it into a `tsc` error. (`class-component`,
   `props-readonly`)
2. **A screen is a thin route, a pure view and one model hook.** The route file renders
   `const model = useTasksModel(); return <TasksScreen model={model} />`; the view renders its props;
   `use-<feature>-model.ts` is the only code that reads stores, services, server state, the clock and
   navigation; rules and derived values are pure functions beside it. Why: each piece is tested alone,
   and architecture-and-boundaries checks the route (`route-thin`).
3. **Effects only synchronise with a system outside React, and clean up.** Four kinds: subscribe to an
   OS or native event (return the unsubscribe), push React state into a native API, run work while a
   screen is focused, measure. Everything else is computed during render or done in the handler that
   caused it; no state setter runs synchronously in an effect body; a callback the effect must not
   re-subscribe for goes through `useEffectEvent`; an OS value the UI reads comes from
   `useSyncExternalStore` (with a server snapshot, or static web rendering throws) or an OS-mirror
   store, never `useState` plus an effect. Why: a leaked listener keeps firing after unmount and after
   Fast Refresh, and copying state in effects renders twice and drifts. (`effect-cleanup`)
4. **React Compiler memoizes: no `useMemo`, `useCallback` or `memo`.** A measured exception carries
   `// memo-exemption: <measurement>` and a reviewed lint exemption; `'use no memo'` appears only with
   `// use-no-memo-test: <title>` naming the failing test that shows the compiler bug; Reanimated shared
   values use `.get()` and `.set()`, never `.value`. The rules apply while the app config sets
   `experiments.reactCompiler: true` (the Expo template default). Why: the compiler silently skips any
   function that breaks a Rule of React, and a stray memo hides that the compiler is doing the work.
   (`no-memo-apis`, `use-no-memo`, `shared-value-get-set`)
5. **Render is pure.** No `Date.now()`, `new Date()`, `Math.random()` or `performance.now()` in a
   component, no ref read, no component declared inside another, no state set during render. Time and
   randomness come from ports in the model hook. Why: the compiler caches renders on the assumption that
   the same inputs give the same output. (`render-impure`)
6. **Every store read passes a selector; a built value goes through `useShallow`.** The rule is
   state-management-zustand's, and its checks enforce it (`check-stores` [selector-missing],
   [selector-new-object]; lint `storeWithoutSelector`); components and model hooks follow it. Why: a
   bare `useTasksStore()` re-renders on every change, and in Zustand 5 a fresh array or object per call
   loops forever ("Maximum update depth exceeded").
7. **A hook lives in its own hook file.** `use-<name>.ts` exports `useName` (a store file exports its
   `useXStore`, a context file its `useX`), takes at most three parameters, returns one value or an
   object with named fields, and never JSX. Why: the hooks and compiler lint find hooks by the `use`
   prefix, and readers find them by file name. (`hook-file`)
8. **Pressables live in `src/ui` and take a required `testID`.** Screens compose the shared buttons
   and rows, which own the role, translated label, state and 44 pt box (accessibility-as-code); a
   reusable component derives its part ids from its one testID (`${testID}.label`); pressed feedback is
   `style={(state) => [styles.base, state.pressed && styles.pressed]}`. Why: accessibility and touch
   size are solved once, and E2E flows select by testID on both platforms. (`banned-import`,
   `testid-required`, `pressed-destructure`)
9. **Lists that grow are a `FlatList` with stable keys.** `keyExtractor` returns the item's id;
   FlashList only when profiling shows the need; a `ScrollView` that maps data only for a short list that
   can never grow, with `// bounded-list: <bound>` above it; never key by the array index, except a
   positional series built with `Array.from({ length })`. Why: an index key remounts the wrong rows when
   the list is filtered, and an unbounded ScrollView mounts every row at once. (`list-key-index`,
   `scrollview-list`)
10. **Layout survives any window and both platforms' system bars.** Never `Dimensions`: size from
    `useWindowDimensions()`, `useWindowClass()` or `onLayout`, with layout maths in pure functions tested at the window table's
    sizes and at `fontScale` 2. Every screen sits in `ScreenFrame` (react-native-safe-area-context,
    physical edges) and names what sits around it through the required `edges`: `ALL_EDGES`,
    `BELOW_HEADER_EDGES` (a header above), `ABOVE_TAB_BAR_EDGES` (a tab bar below),
    `BETWEEN_HEADER_AND_TAB_BAR_EDGES` or `BELOW_HEADER_SCROLLING_EDGES` (a header above, content
    padding the bottom inset as it scrolls under the home indicator). One exception: a list-detail
    screen renders adaptive-layout's `ListDetailLayout` in react-native-safe-area-context's
    `SafeAreaView` with one of these edge sets, because ScreenFrame's column is narrower than two
    panes. Insets never become start/end keys; style keys are logical;
    direction is never read from `isRTL` outside the direction module. Why: iPads, foldables and
    Android multi-window resize the app, Android draws edge to edge, a navigator header and the tab bar
    pad their own inset (an edge the screen shares with one is added twice), and the notch does not
    mirror in RTL. (`banned-import`, `inset-direction`, `no-isrtl`)
11. **Text goes through the app's text primitive.** `Text` from react-native is imported only by
    `AppText` (design-system-structure owns it). Why: direction, font, the 200 % cap and the header
    role live in one place. (`banned-import`)
12. **A failing part fails alone and offers one way out.** A route fails into Expo Router's
    `ErrorBoundary` export (error-handling-typed-results); a part of a screen that can fail on its own
    (a canvas, a chart, a WebView) sits in `SubtreeErrorBoundary`; a fallback never retries by itself;
    errors no boundary sees (handlers, promises, worklets) are caught where they happen, and an async
    handler starts `task().catch(reportError)`. Why: an automatic retry of a render error that repeats
    is a crash loop.

## Workflow

1. Read [references/rules-explained.md](references/rules-explained.md) once per session before
   writing React code: every rule with its reason and what enforces it (lint, this checker, a test, or
   another skill's checker).
2. **First time in an app.** Copy `templates/src/hooks/` to `src/hooks/` and `templates/src/ui/` to
   `src/ui/`, each file with its test. `screen-frame.tsx` imports design-system-structure's
   `src/theme/` (`makeStyles`, tokens); the tests use
   unit-and-component-tests' `@test/render-with-providers`. Every template's first line names its repo
   path; files in `examples/` are shapes, never copied.
3. **A screen.** Follow "A screen and its model hook" in
   [references/patterns-and-recipes.md](references/patterns-and-recipes.md): the route file, the pure
   view in `src/features/<feature>/<feature>-screen.tsx`, the model hook with its `renderHook` test, pure
   logic beside it. Put the view in `ScreenFrame` with the edges the "Safe areas" table gives for what
   sits above it (a header?) and below it (a tab bar?).
   Split a model hook that passes 40 lines into `use-<feature>-actions.ts` and a pure
   `<feature>-model-of.ts`.
4. **A component.** Imitate [examples/labelled-value.tsx](examples/labelled-value.tsx) for a
   presentational `src/ui/` component and [examples/hide-for-premium.tsx](examples/hide-for-premium.tsx)
   for one that reads one store value; check the Pressable table in the patterns reference.
5. **A hook or an effect.** Imitate [examples/use-step-pager.ts](examples/use-step-pager.ts) (state and
   derived values, no effect), `templates/src/hooks/use-is-app-active.ts` (an OS value through
   `useSyncExternalStore`) or ui-component-library's `useHoldToConfirm` (a Reanimated timer, described
   under "Hooks without effects"). Before
   writing `useEffect`, find the effect's kind in the four-kinds table; if it has none, compute in render
   or move the work into the handler.
6. **A list.** Read "Lists" in the patterns reference: a `FlatList` with `keyExtractor`, FlashList only
   after a measurement, a `ScrollView` only for a bounded list with its comment.
7. **Tests first.** RNTL 14 through `renderWithProviders` / `renderHookWithProviders` (await them), or
   `// no-providers: <why>` for a unit that reads no context; query by role and name; give a hot
   store-reading component a `<Profiler>` re-render test like
   [examples/hide-for-premium.test.tsx](examples/hide-for-premium.test.tsx). Recipes are in the patterns
   reference.
8. **Check.** Run `npm run typecheck`, `npx eslint <changed paths> --max-warnings 0` and the Jest tests,
   then from the repo root `node ${CLAUDE_SKILL_DIR}/scripts/check-react-rules.mjs .`. Fix every `FAIL`
   line (file:line, rule, fix) and rerun until it prints `RESULT: PASS`. For a monorepo, a moved source
   folder or a renamed text primitive, read "Checker configuration" in the patterns reference.

## Definition of done

- [ ] Every new component is a function with a named export, read-only props (`readonly T[]` arrays),
      translated strings only, a required `testID` when it is an interactive `src/ui/` component, and a
      test that queries it by role and name.
- [ ] Every screen is a thin route, a pure view in `ScreenFrame` whose `edges` match its header and
      tab bar (the "Safe areas" table in the patterns reference), and one model hook that alone reads
      stores, services and navigation, with a `renderHook` test.
- [ ] Every new hook sits in its `use-<name>.ts` with a test; every effect is one of the four kinds and
      returns its cleanup when it subscribes or starts a timer.
- [ ] No `useMemo`, `useCallback`, `memo`, `.value`, `Dimensions`, index key or raw pressable outside
      `src/ui` was added; any `'use no memo'` names its failing test.
- [ ] Every store read passes a selector and wraps a built value in `useShallow`
      (state-management-zustand's `check-stores` and lint `storeWithoutSelector` prove it).
- [ ] Lists that grow are `FlatList`s keyed by id; each remaining mapped `ScrollView` states its bound.
- [ ] Layout functions are tested at the window table's sizes and at `fontScale` 2.
- [ ] Hot store-reading components have a `<Profiler>` re-render test.
- [ ] `npm run typecheck`, ESLint `--max-warnings 0` and Jest pass.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-react-rules.mjs .` prints `RESULT: PASS` (it prints no SKIP
      lines; in an app whose config leaves React Compiler off it prints one `note:` line and does not
      apply the two memo rules).

## Anti-patterns

- **Copying a prop into state with an effect.** Compute it during render; `react-hooks/set-state-in-effect`
  is right. Reset state on an identity change with a `key` on the component instead.
- **`useCallback` "to be safe".** The compiler already memoizes, and the checker fails the import.
- **`useTasksStore((state) => state.tasks.filter(isOpen))`.** A fresh array each call loops in
  Zustand 5: wrap it in `useShallow` (state-management-zustand) or select primitives.
- **A `Pressable` or `TouchableOpacity` in a screen, or `onPress` on a `View`.** Compose the
  `src/ui` primitives so role, label, state and size are right once.
- **`items.map((item, index) => <Row key={index} />)` or `keyExtractor={(_, i) => String(i)}`.** Key by
  the item's id; the index moves when the list is filtered or sorted.
- **A `ScrollView` over the user's tasks.** It mounts every row; use a `FlatList`, and FlashList when a
  profile shows the FlatList is the bottleneck.
- **`Dimensions.get('window')` at module level or in a render.** Windows resize; use
  `useWindowClass()`.
- **`paddingStart: insets.left`.** The camera cutout stays on the physical left in RTL; take both
  sides with `paddingInline: Math.max(gutter, insets.left, insets.right)`, or use `SafeAreaView` edges
  (`paddingLeft` is swapped to the start side in RTL too).
- **`ScreenFrame` with every edge under a header.** The provider's top inset is added under the header
  again; pass `BELOW_HEADER_EDGES`.
- **`ScreenFrame` with the bottom edge on a tab screen.** The tab bar already pads the home indicator
  or the Android navigation bar, so an empty band (34 pt on a home-indicator iPhone) sits above it;
  pass `ABOVE_TAB_BAR_EDGES`, or `BETWEEN_HEADER_AND_TAB_BAR_EDGES` when the tab shows a header.
- **An effect that adds a `BackHandler`, `AppState` or `Keyboard` listener and returns nothing.** Return
  `subscription.remove()`; on Android a leaked back handler swallows every later back press.
- **An error fallback that retries in an effect.** It becomes a crash loop; offer one button.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/rules-explained.md](references/rules-explained.md) | The full rule catalogue (components, hooks and effects, React Compiler, stores, styles, text, RTL, pressables, lists, layout, motion, errors), each with its reason and enforcer, and the rules owned by other skills | Workflow step 1 |
| [references/patterns-and-recipes.md](references/patterns-and-recipes.md) | Where files go, a screen and its model hook, hooks without effects, the four effect kinds, store reads, styles, the Pressable table, lists and the measurement method, the window table, safe areas on iOS and Android, error boundaries, testing recipes, the React Navigation appendix, When multi-package, checker configuration, verified facts | Workflow steps 3-8 |
| [examples/labelled-value.tsx](examples/labelled-value.tsx) | Example (shape only): a presentational `src/ui/` component with derived part testIDs and a slot | Workflow step 4 |
| [examples/labelled-value.test.tsx](examples/labelled-value.test.tsx) | Example: its test | Workflow step 4 |
| [examples/hide-for-premium.tsx](examples/hide-for-premium.tsx) | Example (shape only): a component that reads one store value with a primitive selector | Workflow step 4 |
| [examples/hide-for-premium.test.tsx](examples/hide-for-premium.test.tsx) | Example: the `<Profiler>` re-render guard and store-driven tests | Workflow steps 4 and 7 |
| [examples/use-step-pager.ts](examples/use-step-pager.ts) | Example (shape only): a hook with state and derived values, no effect | Workflow step 5 |
| [examples/use-step-pager.test.ts](examples/use-step-pager.test.ts) | Example: its `renderHook` tests | Workflow step 5 |
| `templates/src/hooks/` | Canonical shared hooks, owned here and synced from the library (edit the canonical copy, never this one): `use-is-app-active.ts` (foreground or not through `useSyncExternalStore`, with a server snapshot for static web rendering; iOS `inactive`, Android `background`) and `use-window-class.ts` (`classifyWindow()`, `useWindowClass()`: compact or regular at 600, landscape, large text at `fontScale` 1.25), each with its test | Workflow steps 2, 3 and 5; copy to `src/hooks/` |
| `templates/src/ui/` | `screen-frame.tsx` (`ScreenFrame` with a required `edges`, and the four edge sets for a header above and a tab bar below), `subtree-error-boundary.tsx` (the one class, for a part of a screen that fails alone), each with its test (the press-and-hold hook `use-hold-to-confirm.ts` is ui-component-library's) | Workflow steps 2, 3 and 5; copy to `src/ui/` |
| `scripts/check-react-rules.mjs` | The checker for the rules lint does not fully cover (store reads are state-management-zustand's) | Workflow step 8, and at the end |
| `scripts/selftest.mjs` | Proves the checker passes the good fixture and catches each planted bug | After changing the checker |
| `scripts/check-lib.mjs` | Shared script helper (CLI, reporting, repo walk, layout, self-test), synced from the library (do not edit here) | Never by hand |
| `scripts/lib/object-literal.mjs` | Bracket-matching helper the checker uses, synced from the library (do not edit here) | Never by hand |
| `scripts/lib/source-scan.mjs` | Source lexer helpers (`maskCode` blanks comments and string contents), synced from the library (do not edit here) | Never by hand |
| `assets/shared.json` | Declares the shared files this skill copies in | When adding a shared file |
| `tests/bases/app/` | The small Tasks app the fixtures start from (the templates are laid over it) | When adding a rule to the checker |
| `tests/fixtures/` | The overlay cases: good, planted bugs, passing variants (compiler off, conditional subscriptions, bounded scroll lists, whole-repo scan, monorepo) and bad input | When adding a rule to the checker |

## Related skills

- `architecture-and-boundaries` - where files go, thin routes, `src/ui` stays presentational.
- `naming-conventions` - file, export, hook, handler and testID names.
- `typescript-and-lint-rules` - the ESLint config (react-hooks rules), size and complexity limits.
- `design-system-structure` - theme, `makeStyles`, `AppText`, `PressableSurface`, motion tokens.
- `ui-component-library` - the shared buttons, rows and dialogs built on these rules, and the
  press-and-hold hook `useHoldToConfirm`.
- `accessibility-as-code` - roles, names, 44 pt targets, `hitSlop`, reduce motion, text scaling.
- `state-management-zustand` - stores, reducers, selectors and `useShallow`; owns and checks the store-read rule.
- `error-handling-typed-results` - the route `ErrorBoundary`, the error net, `Result`.
- `async-safety` - async work in effects: abort per run, latest wins, handles released.
- `unit-and-component-tests` - `renderWithProviders`, Jest projects, RNTL conventions.
- `navigation-and-routing` - Expo Router layouts, tabs, params, back handling and predictive back.
- `adaptive-layout` and `performance-budgets` - two-pane layouts, list and re-render budgets.
