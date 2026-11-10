---
name: navigation-and-routing
description: "Builds and checks Expo Router routes and layouts against a contract: typed hrefs, params, protected flows, modals, back guards. Use when adding a route, link or guard, or Back acts up. Not for deep links (deep-links-and-universal-links)."
---

# Navigation and routing

An Expo app has one navigation tree, built by Expo Router from the files in `src/app/`, whose routes
equal a repo-owned route contract (`contracts/navigation.json`): flows switch by guards, hrefs and
params are checked, screens with unsaved work cannot be lost by a stray Back, and every URL lands
somewhere. React Navigation 7's static API is the fenced alternative. A script proves it.

## Rules that must hold

1. **One router, one tree: Expo Router's.** The root `src/app/_layout.tsx` default-exports a layout
   that renders the root navigator, directly or through the components it renders (app-startup-and-bootstrap's
   root skeleton: `AppRoot` > `RootStack` > `AppStack`). No `NavigationContainer`,
   `createStaticNavigation` or `@react-navigation/*` import beside it: expo-router 57 carries its own
   React Navigation, and a second copy has its own contexts and its own back stack. (`root-layout`,
   `one-navigator`)
2. **The contract is the route table.** Every route file (route id = its path under `src/app` without
   the extension) is in `contracts/navigation.json` `routes`, and every contract route has a file;
   `home` names the first screen. A route change starts in the contract, so a stray file (Expo Router
   bundles everything in `src/app`) or a forgotten screen is caught. (`contract`, `route-table`,
   `home-route`)
3. **Flows switch by guards, never by navigating.** Signed out / signed in, onboarding / main and
   test-build-only screens are `Stack.Protected` groups whose `guard` reads a store selector, each in
   the contract (`protected`). No `<Redirect>` in a layout and no `router.*` call from a layout's
   effect: they render the wrong screen first and leave it in the history, while a guard turning false
   removes its screens from the history. Guards hide screens; the server still checks data.
   (`protected-guard`, `flow-by-guard`)
4. **Hrefs are typed.** `experiments.typedRoutes` is on (CI generates the types with
   `npx expo customize tsconfig.json` before `tsc`), and app code never writes `as Href`: a renamed
   route then fails `tsc` wherever it is linked. (`typed-routes`, `href-cast`)
5. **Params are parsed at the edge.** Any URL can open a dynamic route with any text, and
   `useLocalSearchParams<T>()` is a cast. Each dynamic route has a valibot parser returning a `Result`
   (`paramParsers`), the model shows the screen's not-found state on failure, and params stay ids and
   short plain values. (`params-parsed`)
6. **A screen with unsaved work blocks its removal.** Its model hook calls `usePreventRemove` (the
   template's `useDiscardGuard`), which sees the header back button, the iOS swipe, a sheet's swipe
   down, Android's back button and predictive back gesture, and `router.back()`; Back asks before
   discarding. The contract lists it in `guarded`. Turn the iOS swipe off (`gestureEnabled` and
   `fullScreenGestureEnabled` false, `"gesture": "off"`) only where starting it already harms. The
   guard cannot see a kill: save drafts as they change. (`guarded-prevent-remove`,
   `guarded-gesture-off`)
7. **Going back never stacks a second home.** `router.navigate` and `push` (and `<Link>`) push, so the
   home route is reached with `router.dismissTo(home)` or `router.back()` (`<Link dismissTo>`).
   (`go-back`)
8. **A destination is a route; a layer over a live screen is not.** Modal destinations are routes with
   a modal `presentation`, exactly the contract's `modals` (on Android `modal` opens like a push,
   `formSheet` is a bottom sheet). Confirmations, the discard dialog and a pause layer render inside
   the screen or the dialog host, because a route change would cover or unmount what they sit on.
   (`modal-presentation`)
9. **Every URL lands somewhere.** `src/app/+not-found.tsx` renders for an unknown URL (without it the
   router shows its development page); its one action is `dismissTo('/')`, so Back cannot return to
   the dead link, and it never prints the URL. (`not-found`)
10. **The native stack.** `Stack` from `expo-router` (react-native-screens): the platform draws the
    transitions, swipe and header. The JavaScript stack only with `"jsStack": true` and a reason.
    Every `<Stack>` takes its animation from motion-and-animation's `useScreenAnimation()`.
    (`native-stack`)
11. **Navigation lives in screens' model hooks.** `src/ui`, `src/stores`, `src/services`, `src/data`,
    `src/api` and `src/core` never import a router: components take `onPress`, stores change state.
    The one exception is a root kit (`src/services/<concern>/<concern>-root-kit.tsx`, registered in
    app-startup-and-bootstrap's `createRootKits`), whose effects route notification taps beside the
    root Stack. Navigation state is never persisted; an open editor is reopened from its saved draft.
    (`nav-in-screens`)
12. **Debug routes are gated and guarded.** A test-build screen renders only through `TEST_ONLY`
    (debug-menu-and-test-hooks' gate, so production bundles drop it) and sits in a protected group,
    so a production deep link cannot open it. (`debug-gated`)
13. **Placeholders are listed and never ship.** While screens are built one by one, an unbuilt route
    renders the placeholder screen, so the route table, its typed hrefs and every model hook's
    navigation exist from day one (no no-op handlers); the contract lists them and `--release` fails
    while any is left. (`placeholder-route`, `placeholder-release`)
14. **With React Navigation 7 instead (appendix):** one static config whose groups (`if` hooks) equal
    the contract's `groups`, one `createStaticNavigation` container (never `<NavigationContainer>`),
    `RootParamList` from `StaticParamList`, plain-data params, `popTo` to go back, no `reset()` to
    switch flows, and the stack wrapped with `.with()` so pushes cross-fade under reduce motion.
    (`group-if`, `static-container`, `typed-routes`, `params-serialisable`, `flow-by-guard`,
    `motion-transition`)

## Workflow

1. **Read what the task needs** in [references/expo-router-in-practice.md](references/expo-router-in-practice.md):

   | Task | Section |
   |---|---|
   | first setup, the root layout, reopening work after a kill | "The root layout and the startup order" |
   | a new screen, a tab, a header | "File routes", "Layouts: one navigator tree" |
   | a link or a param | "Typed routes and hrefs", "Params: parse them at the edge" |
   | sign-in, onboarding, test-only screens | "Flows: Stack.Protected, never a redirect", "Debug routes and placeholders" |
   | a modal, a sheet, a dialog | "Modals and what is not a route" |
   | Back, the swipe, Android back, unsaved changes | "Back handling (iOS and Android)", "Going back to a screen already in the stack" |
   | a route test | "Testing navigation" |

   With React Navigation instead of Expo Router, read [references/react-navigation-static.md](references/react-navigation-static.md)
   and imitate `examples/react-navigation/`.
2. **Set up once.** Copy `templates/contracts/navigation.json` (and its schema) and list the app's
   routes; copy `templates/src/app/+not-found.tsx` with `templates/src/features/not-found/` and add the
   `not-found.*` keys of `templates/src/i18n/catalogs/` to every catalog (i18n-strings-and-catalogs).
   Turn on `experiments.typedRoutes` in `app.config.ts`. The root layout and `AppStack` come from
   app-startup-and-bootstrap's root skeleton; add the root `Stack.Protected` groups inside `AppStack`.
3. **Add a route:** add its id to the contract, create the thin route file rendering the feature's
   screen (architecture-and-boundaries), add its `Stack.Screen` in the layout only for options (a
   title, `presentation`), and put its navigation calls in the feature's model hook.
4. **A dynamic route:** write `src/features/<feature>/<feature>-params.ts` after
   `templates/src/features/task-detail/task-detail-params.ts` (with its test), map it in
   `paramParsers`, and render the not-found state on a parse failure.
5. **A flow:** wrap its screens in `<Stack.Protected guard={...}>` fed by a store selector, add the
   group to `protected`, and test it the way `templates/src/features/root-navigator/protected-routes.test.tsx`
   does (copy that test when the app adds its first flow; it also pins the router facts).
6. **A screen with unsaved work:** copy `templates/src/features/task-editor/use-discard-guard.ts` with
   both tests, call it from the model hook with the "unsaved" boolean, render the dialog while
   `isPromptOpen`, leave after a save through `leave()`, and list the route in `guarded`.
7. **Run the tests**, paths first (`--selectProjects` takes every following word as a project):
   `npx jest src/features/not-found src/features/root-navigator src/features/task-editor src/features/task-detail --selectProjects unit android`,
   then `npm run typecheck` and lint as quality-gates requires.
8. **Run the checker:** `node ${CLAUDE_SKILL_DIR}/scripts/check-navigation.mjs .`; fix every `FAIL`
   line (file, rule, fix) and rerun until `RESULT: PASS`. Rules and contract keys:
   [references/contract-and-checker.md](references/contract-and-checker.md). Before a release, run it
   with `--release`.

## Definition of done

- [ ] `contracts/navigation.json` lists exactly the app's routes, `home`, every protected group, every
      guarded route with its hook, every modal, a parser for every dynamic route, the debug routes,
      and the placeholders (none before a release).
- [ ] The root layout renders the one Expo Router tree in the canonical startup order; no hand-built
      container and no `@react-navigation/*` import.
- [ ] Flows are `Stack.Protected` groups fed by stores; no layout redirects or navigates from an effect.
- [ ] Typed routes are on and generated in CI; no `as Href`; dynamic routes parse their params with
      valibot.
- [ ] Every guarded screen asks before discarding on iOS (button, swipe, sheet) and Android (back
      button, gesture); its tests pass (`use-discard-guard.test.tsx`, `use-discard-guard.android.test.tsx`).
- [ ] The not-found route and its test pass (`not-found-navigation.test.tsx`).
- [ ] Before a release: `node ${CLAUDE_SKILL_DIR}/scripts/check-navigation.mjs . --release` prints
      `RESULT: PASS`.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-navigation.mjs .` prints `RESULT: PASS` (no SKIP lines:
      every target is this skill's own).

## Anti-patterns

- **Deciding the first screen in the root layout** with `router.replace` in an effect, or a
  `<Redirect>` in a layout. Use `Stack.Protected`; the guard decides before anything renders.
- **`router.navigate('/')` or `<Link href="/">` to go home.** It stacks a second home; use
  `dismissTo`.
- **Trusting `useLocalSearchParams<{ id: string }>()`.** Repeated keys arrive as arrays and links carry
  anything; parse with valibot.
- **Passing a whole object through params** (`params: { task: JSON.stringify(task) }`). Pass the id;
  the screen reads the task from its store or query.
- **A `BackHandler` listener as the unsaved-changes guard.** It misses the iOS swipe, the header button
  and code; use `usePreventRemove`.
- **Turning off the swipe on every screen "to be safe".** People rely on it; guard the screens with
  work instead, and turn it off only where starting it harms.
- **A modal route for a confirmation or a pause layer.** It covers or unmounts the screen beneath;
  render it in the screen or the dialog host.
- **Importing `@react-navigation/native` in an Expo Router app** for `useIsFocused` or a theme. Import
  them from `expo-router`.
- **A debug route that re-exports the debug screen.** It ships in production; render
  `TEST_ONLY?.DebugScreen` behind a guard.
- **No-op handlers for screens not built yet.** Route them to the placeholder and list them.
- **`useNavigation` or `router` in a `src/ui` component.** Pass `onPress` from the screen.
- **Persisting navigation state** to reopen where the person was. Reopen from saved data instead;
  a stale state breaks after any route change.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/expo-router-in-practice.md](references/expo-router-in-practice.md) | Routes, the root tree (owned by app-startup-and-bootstrap), reopening work, layouts, typed hrefs, params, flows, modals, back on iOS and Android, not-found, debug routes, placeholders, testing, verified facts, pitfalls | Workflow step 1 |
| [references/contract-and-checker.md](references/contract-and-checker.md) | Every contract key, every checker rule with its fix, configuration, multi-package | Workflow steps 2 and 8 |
| [references/react-navigation-static.md](references/react-navigation-static.md) | Appendix: React Navigation 7 static API, the mapping from Expo Router, tests, versions | Only for a React Navigation app |
| `templates/contracts/navigation.json` | The route contract, filled for the starting app | Workflow step 2 |
| `templates/contracts/navigation.schema.json` | Its JSON schema | Workflow step 2 |
| `templates/src/app/+not-found.tsx` | The not-found route (thin) | Workflow step 2 |
| `templates/src/features/not-found/` | Its pure view and model hook (`dismissTo('/')`), each with its test, and the route test, which also pins `dismissTo` vs `navigate` | Workflow step 2 |
| `templates/src/i18n/catalogs/` | The `not-found.*` keys in `en` and `ar`, merged into the app's catalogs | Workflow step 2 |
| `templates/src/features/task-detail/` | A route params parser (valibot, `Result`) and its test | Workflow step 4 |
| `templates/src/features/root-navigator/protected-routes.test.tsx` | Flow tests with `Stack.Protected`; pins the guard facts | Workflow step 5 |
| `templates/src/features/task-editor/` | `useDiscardGuard` (usePreventRemove) and its iOS and Android tests | Workflow step 6 |
| `examples/placeholder-screen.tsx` | The placeholder screen shape for routes not built yet | When building screen by screen |
| `examples/react-navigation/` | The static API shapes: stack, guards, container, types, params, debug route, guarded model, contract | Only for a React Navigation app |
| `scripts/check-navigation.mjs` | Checker for every rule above, both routers | Workflow step 8, and before a release with `--release` |
| `scripts/selftest.mjs` | Proves the checker passes both good apps and catches each planted bug | After changing the checker |
| `scripts/check-lib.mjs` | Shared script library (synced; do not edit here) | Never by hand |
| `scripts/lib/source-scan.mjs` | Shared lexer, JSX and import-resolution helpers (synced) | Never by hand |
| `scripts/lib/object-literal.mjs` | Shared reader for the static config object (synced) | Never by hand |
| `assets/shared.json` | Declares the synced helpers | When adding a shared file |
| `tests/bases/` | The two fixture apps: Expo Router (`app/`) and React Navigation (`react-navigation/`) | When adding a rule |
| `tests/fixtures/` | The self-test cases per router: good, planted bugs, NOT APPLICABLE, bad input | When adding a rule |

## Related skills

- `architecture-and-boundaries` - thin routes, where route tests live, the test-only gate's imports.
- `react-components-and-hooks` - the model hook that holds navigation; `ScreenFrame` edges.
- `motion-and-animation` - `useScreenAnimation()` for every `<Stack>`.
- `rtl-and-direction` - the navigator's layout direction and the restart.
- `design-system-structure` - the navigation theme.
- `app-startup-and-bootstrap` - the root skeleton (`_layout.tsx`, `AppRoot`, `RootStack`, `AppStack`), the startup order, the splash and the draft flush that "Continue editing" reads.
- `auth-and-secure-storage` - the session store a sign-in guard reads.
- `deep-links-and-universal-links` - schemes, universal and app links, `+native-intent`.
- `ui-states-and-feedback` - the dialog host and not-found states inside screens.
- `screen-contracts` - what each screen shows.
- `debug-menu-and-test-hooks` - the `TEST_ONLY` gate and debug deep links.
- `unit-and-component-tests` - `renderRouterWithProviders` and the Jest projects.
- `e2e-maestro` - the real swipe and back gesture on named devices.
- `canvas-gestures-and-hit-testing` - turning the back swipe off over a canvas.
- `expo-router` (Expo's official skill) - the Expo Router API reference.
