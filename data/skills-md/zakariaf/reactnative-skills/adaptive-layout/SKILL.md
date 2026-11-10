---
name: adaptive-layout
description: "Lays screens out by window, not device: breakpoints, master-detail panes, readable widths, grids. Use when making screens responsive or for tablets, iPad, foldables, rotation, split screen, orientation lock. Not for tab bars (navigation-and-routing)."
---

# Adaptive layout

Every screen lays out for the window the app has now, on iOS and Android: one window classifier,
breakpoints in one module, a readable column on wide windows, a list beside its detail when both
fit in the box the panes get, grids sized from their own box, no orientation lock or resizing
opt-out the platforms ignore anyway, and a selection that lives in the route so rotation, resizing
and links keep it. A zero-dependency checker proves what a reviewer would otherwise check by eye.

## Rules that must hold

1. **Layout decides by the window, never the device.** No `Platform.isPad`, `interfaceIdiom`,
   expo-device `DeviceType`, `isTablet()` or `isPhone` helper picks a layout, and no
   `getOrientationAsync` or orientation listener shapes one: read `useWindowClass()` (and its
   `isLandscape`, the window's shape). Why: iPad Split View, Slide Over and Stage Manager, Android
   multi-window and freeform windows, and a foldable opening all resize the app while it runs; an
   iPad in a third of the screen is a compact, portrait-shaped window. A hardware capability in
   `src/services/` (no haptic engine on iPad) is not a layout decision; the rule reads UI code only.
   (`device-branch`, `device-orientation`)
2. **One window classifier, never forked.** `src/hooks/use-window-class.ts` (react-components-and-hooks
   owns it) gives `{ width: 'compact' | 'regular' (600), isLandscape, isLargeText (1.25) }`; no second
   `useBreakpoint`, `useIsTablet` or `REGULAR_WIDTH_MIN` elsewhere. Why: two classifiers disagree at the
   boundary and screens stop agreeing on what "regular" means. (`window-class-fork`)
3. **Breakpoints beyond the class live in `src/ui/adaptive/pane-layout.ts`, as content rules.** A
   width or height compared with a number of 300 or more anywhere else fails; a new rule is a pure
   function ("two panes when the list at 320 and the detail at 400 fit") tested at the window table.
   Why: a number in a screen drifts from every other screen's, and a content rule explains itself.
   (`raw-breakpoint`)
4. **Every screen caps its reading width at `CONTENT_MAX_WIDTH`.** Through `ScreenFrame`,
   `ListDetailLayout`, or a list's `contentContainerStyle` (`width: '100%', maxWidth:
   CONTENT_MAX_WIDTH, alignSelf: 'center'`); a canvas, map, camera or video screen is listed in
   `contracts/adaptive-layout.json` `fullBleedScreens` with its reason; no hand-picked `maxWidth: 720`.
   A screen in a `contracts/architecture.json` `testOnlyFolders` folder (a capture harness, a test
   build's screen) is not judged: it never ships in a store build.
   Why: on a 13-inch iPad in landscape an uncapped line runs 1,300 pt wide. (`readable-width`,
   `readable-width-token`)
5. **No fixed width wider than the narrowest window allows (288).** Regions size by `flex`,
   percentages, the pane layout's `listWidth` or a measured container. Why: a 320 pt Split View pane
   or small phone minus two 16 pt gutters leaves 288; anything wider scrolls sideways or clips.
   (`fixed-width`)
6. **A list and its detail share one screen through `ListDetailLayout`, sized by its own box.** The
   pane count comes from `useListDetailLayout()`: one pane on a compact window; on a regular one, two
   panes only when the list, a hairline and the detail minimum fit in the width `ListDetailLayout`
   measures inside the screen's `SafeAreaView` (721 pt, 801 pt with large text; before the first
   layout, the window minus the side insets). Each screen in `listDetailScreens` renders it with
   `panes={model.panes}`. Why: a regular window is not always wide enough (a half-width iPad Split
   View is 678 pt; an iPad mini beside an 80 pt side rail leaves 664 pt; a form sheet is narrower
   still), and the notch side is not usable space. (`list-detail-screens`)
7. **The selection is the route's, and each route owns its param.** The list route carries
   `?selected=<id>`, the detail route is `[id]`, both render the same screen and each reads only its
   own param; selecting calls `router.push` on one pane, and on two panes `router.setParams` with the
   param the current route owns (`{ selected }` on the list route, `{ id }` on the detail route);
   nothing navigates when the window changes; no `useState` selection. Why: a rotation, a resize, a
   restored route and a link all land on the same item, back never walks through every tapped row,
   and `/tasks/t2?selected=t3` would leave the detail pane on `t2`. (`list-detail-selection`)
8. **Grid columns come from the grid's own box, and a new count remounts the list.**
   `useMeasuredWidth()` + `gridColumnsOf({ width, minCellWidth, gap, maxColumns })`, and
   ``key={`grid-${columns}`}`` on the `FlatList`. Why: inside a pane the window is far wider than the
   grid, and React Native throws "Changing numColumns on the fly is not supported" on the first
   rotation. (`grid-columns-source`, `grid-columns-key`)
9. **Orientation is not locked, except where the contract says why.** The app config sets
   `orientation: 'portrait'` (a phone-only lock in practice) or `'default'`; `'landscape'` needs
   `appOrientation: 'landscape'` in the contract. A per-screen lock (`lockAsync`, a Stack screen's
   `orientation` option) sits only in an `orientationLocks` file with its reason, and every
   `lockAsync` has its `unlockAsync`; expo-screen-orientation's `initialOrientation` lock needs the
   matching `appOrientation`. Why: iPads with multitasking and Android displays 600 dp and wider (apps
   targeting API 36) ignore locks, so the layout must handle both shapes anyway.
   (`orientation-lock`, `orientation-unlock`, `config-orientation`)
10. **The app never opts out of resizing, and supports tablets.** No `requireFullScreen: true` or
    `UIRequiresFullScreen` (unless `UIRequiresFullScreenIgnoredStartingWithVersion` of 27 or lower,
    usually `'26'`, limits it to older iOS), no `resizeableActivity`, aspect-ratio limits or
    `PROPERTY_COMPAT_ALLOW_RESTRICTED_RESIZABILITY` in the config or a plugin, not even set to the
    default (TN3192 asks apps to drop the key; the checker calls that redundant); `ios.supportsTablet:
    true` unless the contract says `tablets: false` with a reason. Why: Apple deprecated full screen in
    iPadOS 26 and ignores it for apps built with the iOS 27 SDK; Android 16 ignores the opt-outs on
    large displays and the last one stops working at API 37; a phone-only app runs in a scaled frame
    on iPad. (`full-screen-opt-out`, `tablet-support`)
11. **Insets are physical and change with the window.** Rotation moves the notch or cutout to a side;
    take both sides (or `SafeAreaView` edges), never `paddingStart: insets.left`, and never count the
    notch side as pane width (measure inside the edges; subtract the side insets from a window).
    Why: the cutout does not mirror in RTL, and a detail pane under the notch is unusable.
    (react-components-and-hooks' `inset-direction`; the pane tests here)
12. **Every layout decision is a pure function tested at the window table, at `fontScale` 1 and 2.**
    320 × 568, 360 × 800, 402 × 874, 874 × 402 (62 pt side insets), 678 × 1032, 744 × 1133,
    800 × 1280, 1376 × 1032; screenshots on named devices at the same sizes. Why: Jest lays nothing
    out, and adaptive bugs live at the size nobody opened.

## Workflow

1. Read [references/window-classes-and-panes.md](references/window-classes-and-panes.md): window
   versus device, the classifier, the window table, the pane rule, readable widths, grids, fixed
   widths, large text, and the decisions with their reasons.
2. **First time in an app.** Make sure `src/hooks/use-window-class.ts` exists (react-components-and-hooks
   ships it; this skill's synced copy is the same file). Copy `templates/src/ui/adaptive/` to
   `src/ui/adaptive/` with every test, and `templates/contracts/adaptive-layout.json` plus its schema
   to `contracts/`. The kit imports design-system-structure's `@/theme/*`; the tests use
   unit-and-component-tests' `@test/render-with-providers`.
3. **The app config.** Read [references/platforms-orientation-and-resizing.md](references/platforms-orientation-and-resizing.md)
   sections 1-3: keep `orientation: 'portrait'` or `'default'`, set `ios.supportsTablet: true`, remove
   every resizing opt-out, and record a deliberate profile (landscape app, no iPad layout yet) in the
   contract (section 8).
4. **A screen.** Put it in `ScreenFrame` (or cap its list's `contentContainerStyle`); a full-bleed
   screen goes into `fullBleedScreens` with its reason. Decide variations from `useWindowClass()`;
   if a decision needs a width, add a pure function to `pane-layout.ts` with window-table tests.
5. **A list and its detail.** Read [references/list-detail-and-navigation.md](references/list-detail-and-navigation.md)
   and imitate [examples/tasks-list-detail.md](examples/tasks-list-detail.md): two thin routes over one
   screen, the model hook reads the route's own param from `useLocalSearchParams()` and the panes from
   `useListDetailLayout()`, `onSelect` sets the current route's param on two panes, the screen renders
   `<ListDetailLayout panes={model.panes}>` in a `SafeAreaView` with the named edges. Add the screen
   to `listDetailScreens`, and the example's route tests (both routes, a measured box).
6. **A grid.** Imitate [examples/task-board.tsx](examples/task-board.tsx): measure the container,
   `gridColumnsOf` and `gridCellWidthOf`, render nothing until the first layout, key the list by the
   column count.
7. **An orientation lock** (camera, full-screen video): platforms reference section 5. Lock in an
   effect whose cleanup unlocks, list the file in `orientationLocks` with its reason, and still lay the
   screen out for both shapes.
8. **Tests first.** Follow [references/testing-and-checker.md](references/testing-and-checker.md)
   sections 1-2: window-table tables at `fontScale` 1 and 2, the `useWindowDimensions` mock (Jest's
   default `fontScale` is 2), `SafeAreaProvider` with `initialMetrics`, a fired layout event, the
   crossing test. Route tests use the router helper as in the example.
9. **Check.** Run `npm run typecheck`, `npx eslint <changed paths> --max-warnings 0` and the Jest tests,
   then `node ${CLAUDE_SKILL_DIR}/scripts/check-adaptive-layout.mjs .`. Fix every `FAIL` line
   (file:line, rule, fix) and rerun until it prints `RESULT: PASS`. For a monorepo pass
   `--app-dir apps/mobile`; for a moved source folder or other globs read testing reference section 5.
10. **On devices** (by hand, before a release): screenshots at the window table on named simulators
    and emulators (`<project>-tablet`, a foldable profile), including a half-width iPad Split View,
    `fontScale` 2 and an RTL locale; fold and unfold with a task selected. ios-simulator-build,
    android-emulator-build and e2e-maestro own the commands.

## Definition of done

- [ ] No layout decision reads the device kind or the device orientation; every one comes from
      `useWindowClass()`, `useListDetailLayout()` or a measured container.
- [ ] No width breakpoint outside `src/hooks/use-window-class.ts` and `src/ui/adaptive/`; each new
      layout function has a window-table test at `fontScale` 1 and 2.
- [ ] Every screen caps its reading width, or is listed in `fullBleedScreens` with a reason; no fixed
      width above 288.
- [ ] Every list-detail screen renders `ListDetailLayout`, is in `listDetailScreens`, and reads its
      selection from the route; route tests prove push on a phone window, `setParams` of the current
      route's own param on a wide one (from the list and from the detail route), and one pane in a box
      narrower than two panes.
- [ ] Every computed `numColumns` comes from `gridColumnsOf` on a measured width and keys the list;
      cells take `gridCellWidthOf`, so a short last row keeps the cell size.
- [ ] The app config keeps `portrait` or `default` (or the contract's `appOrientation`), supports
      tablets (or the contract says why not), and opts out of no resizing; each orientation lock is in
      the contract with its reason and unlocks.
- [ ] `npm run typecheck`, ESLint `--max-warnings 0` and Jest pass.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-adaptive-layout.mjs .` prints `RESULT: PASS`. A passing run
      may print only these SKIP lines while the app is being set up:
      `SKIP src/hooks/use-window-class.ts [window-class-fork] not yet created (react-components-and-hooks creates it)`
      and `SKIP app.config.ts [config-orientation] not yet created (expo-project-bootstrap creates it)`;
      it prints `NOT APPLICABLE: react-native is not in package.json` outside a React Native app.

## Anti-patterns

- **`Platform.isPad ? 2 : 1` columns.** An iPad in Split View gets two cramped columns and a phone in
  landscape gets one; use `gridColumnsOf` on the measured width.
- **`width >= 768` in a screen.** A third breakpoint nobody else shares; use the window class or add a
  content rule to `pane-layout.ts`.
- **"Regular means two panes."** A 678 pt Split View pane is regular and too narrow; let
  `listDetailLayoutOf` decide from what fits.
- **Deciding panes from the window beside a side bar or in a sheet.** The window is wider than the
  panes there; pass the panes' own measured box (`ListDetailLayout` does it through `panes`).
- **`router.setParams({ selected })` from the detail route.** It gives `/tasks/t2?selected=t3` and
  the detail stays on `t2`; set `{ id }` there.
- **`useEffect(() => { if (isTwoPane) router.replace(...) }, [isTwoPane])`.** It fights the back stack
  on every rotation; both routes already render both ways.
- **`const [selectedId, setSelectedId] = useState()` for the detail pane.** A resize remounts it and a
  link cannot set it; use the route param.
- **A list-detail screen inside `ScreenFrame`.** Its 640 pt column is narrower than two panes, so the
  screen never splits; render `ListDetailLayout` in a `SafeAreaView` with the named edges.
- **`numColumns={columns}` without a key.** React Native throws the first time the count changes.
- **`orientation: 'landscape'` "because it looks better", or `lockAsync` without `unlockAsync`.**
  Tablets rotate anyway, and every later screen stays locked.
- **`requireFullScreen: true` to avoid iPad work.** Deprecated and ignored from the iOS 27 SDK; the
  app gets resized with a layout that never planned for it.
- **`Dimensions.get('window')` at module level.** It never updates (react-components-and-hooks bans
  it); read `useWindowDimensions()` through the hooks.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/window-classes-and-panes.md](references/window-classes-and-panes.md) | Window versus device, the classifier, the window table, the pane rule, readable widths, grids, fixed widths, large text, wide-window navigation facts, decisions and re-verify commands | Workflow steps 1 and 4 |
| [references/list-detail-and-navigation.md](references/list-detail-and-navigation.md) | The route-owned selection with Expo Router: files, selecting, crossing the two-pane width, back and links, what not to do, tests | Workflow step 5 |
| [references/platforms-orientation-and-resizing.md](references/platforms-orientation-and-resizing.md) | App config keys, iPadOS multitasking and TN3192, Android 16 large screens, foldables, per-screen locks, device orientation versus window shape, insets, profiles | Workflow steps 3 and 7 |
| [references/testing-and-checker.md](references/testing-and-checker.md) | Jest recipes, device runs at the window table, the checker's rules and scope (layout rules read UI code only), the contract keys, multi-package use, limits to review by hand | Workflow steps 8 and 9 |
| [examples/tasks-list-detail.md](examples/tasks-list-detail.md) | Example (shape only): routes, model hook, screen, a supporting pane, five route tests and the contract entry | Workflow step 5 |
| [examples/task-board.tsx](examples/task-board.tsx) | Example (shape only): a grid whose columns and cell width follow its measured container | Workflow step 6 |
| `templates/src/ui/adaptive/` | The pane kit, each file with its test: `pane-layout.ts` (`listDetailLayoutOf`, `gridColumnsOf`, `gridCellWidthOf`, the pane constants: the only home of extra breakpoints, tested at the window table), `use-list-detail-layout.ts` (`{ layout, onLayout }`: the pane count for the panes' measured box, the window minus the side insets until the first layout), `list-detail-layout.tsx` (`ListDetailLayout`: one pane per route or two side by side, measures its own box, a readable detail column, panes kept across a crossing), `use-measured-width.ts` (a container's whole-point width from `onLayout`) | Workflow steps 2, 4, 5 and 6; copy to `src/ui/adaptive/` |
| `templates/src/hooks/` | `use-window-class.ts` and its test: the canonical window classifier, synced from react-components-and-hooks (never edit this copy) | Workflow step 2 |
| `templates/contracts/` | `adaptive-layout.json` (the app's adaptive facts: orientation, tablets, list-detail and full-bleed screens, locks) and `adaptive-layout.schema.json` | Workflow steps 2, 3, 5 and 7; copy to `contracts/` |
| `scripts/check-adaptive-layout.mjs` | The checker for every rule above (`--help` lists them) | Workflow step 9, and at the end |
| `scripts/selftest.mjs` | Proves the checker passes the templates over a small Tasks app and catches each planted bug | After changing the checker |
| `scripts/check-lib.mjs` | Shared script helper (CLI, reporting, repo walk, layout, self-test), synced (do not edit here) | Never by hand |
| `scripts/lib/source-scan.mjs` | Source lexer and JSX helpers, synced (do not edit here) | Never by hand |
| `assets/shared.json` | Declares the shared files this skill copies in | When adding a shared file |
| `tests/bases/app/` | The small Tasks app the fixtures start from (the templates are laid over it) | When adding a rule |
| `tests/fixtures/` | Overlay cases: good, one planted bug per rule, passing profiles (landscape app, no tablets, older-iOS full screen, monorepo, small values) and bad input | When adding a rule |

## Related skills

- `react-components-and-hooks` - owns `useWindowClass`, `ScreenFrame`, safe-area edges and `Dimensions`.
- `design-system-structure` - owns `CONTENT_MAX_WIDTH`, spacing and the theme the kit styles with.
- `navigation-and-routing` - tab bars and side bars on wide windows, route params, predictive back.
- `accessibility-as-code` - the large-text threshold, 200 % text and touch targets.
- `rtl-and-direction` - mirrored panes and physical insets in right-to-left layouts.
- `forms-and-input` - keyboard avoidance (not a layout class).
- `skia-canvas-rendering` - canvases size from their own box, never the window.
- `unit-and-component-tests` - render helpers, the router helper, Jest conventions.
- `ios-simulator-build`, `android-emulator-build`, `e2e-maestro` - named devices and screenshots at the window table.
- `expo-prebuild-and-config-plugins` - config plugins that touch the manifest or Info.plist.
