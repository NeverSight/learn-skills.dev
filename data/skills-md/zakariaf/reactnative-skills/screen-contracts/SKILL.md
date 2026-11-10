---
name: screen-contracts
description: Builds screens, dialogs and overlays to a contract (testIDs, copy keys, states in contracts/screens.json) and proves it. Use when building or changing a screen, dialog, testID or state. Not for shared components (ui-component-library).
---

# Screen contracts

Every screen of an Expo app, every dialog and every overlay is built from one repo-owned contract,
`contracts/screens.json`: where its route, model hook, view and test live, every state (the ones the
design does not draw too), and every element with its testID, role, component and copy keys. The code,
the view tests, the E2E flows and the screenshot checks all use exactly those ids, on iOS and Android.
Two zero-dependency scripts print a screen's contract and prove the built screens match it.

## Rules that must hold

1. **The contract comes first: every screen, dialog and overlay has an entry, and every route file
   belongs to one** (`screen-unlisted`, `contract-invalid`). A new screen, state or testID is a
   contract change in its own reviewed change, then code. Why: ids, keys and states agreed in one
   place are what E2E flows, screenshots and translators rely on; a route without an entry ships
   unchecked.
2. **Use exactly the contract's testIDs: none missing, none invented, none from another screen**
   (`missing-testid`, `unknown-testid`, `testid-wrong-screen`). Repeated items take a data key
   (`lists.list-row.${list.id}`), never an index; parts extend their parent's id; a library component
   derives its parts from the base id the screen passes. Why: flows and screenshot checks find
   elements only by these ids, and an index id points at another item after a sort.
3. **Every text comes from `t()` with the contract's copy key**, the key exists in the source catalog,
   and a retired key is gone (`missing-copy-key`, `unknown-copy-key`, `retired-copy-key`). The model
   hook translates; a view built to a screen contract never calls `t()` and never renders `<T>` (that
   component is for text outside the screen pattern). Why: a wrong key shows the wrong words in every
   language, and a literal is one language for everyone.
4. **Build every state the contract lists, including the ones the design does not draw** (`drawn:
   false` with its `why`: empty, error, offline, a paying user), and decide which state shows in a pure,
   tested function. Why: a state without a layout is a blank screen in front of a person.
5. **A screen is a thin route, a pure view and one model hook with its test** (`route-model-hook`,
   `model-hook-missing`, `model-hook-test`). The route calls `use<Feature>Model()` and renders the
   view; the hook alone reads stores, repositories, services and navigation. Why: the view is tested
   with plain data, the hook with fakes, and the layout lives in one place.
6. **Every screen has a view test that names its testIDs, tests each state in a block named for it,
   and ends every block that renders with the pressable audit** (`screen-test-missing`,
   `testid-untested`, `state-untested`, `state-test-audit`):
   `expect(findInaccessiblePressables(screen.container)).toStrictEqual([])`. Why: each state is its own
   screen for VoiceOver and TalkBack, and an untested state is the one that ships broken.
7. **Dialogs, overlays and sheets keep VoiceOver and TalkBack inside, and Android back closes them**
   (`overlay-not-modal`, `overlay-no-back`): React Native's `Modal` (or the library `Scrim`) with a
   real `onRequestClose`, or an Expo Router modal route. `accessibilityViewIsModal` alone is iOS only
   (accessibility-as-code owns the Android hide). Why: otherwise a screen
   reader wanders onto the screen behind, and a dialog that ignores back traps Android users.
8. **One primary action per screen; ad slots only on the screens the policy allows, never for paying
   users** (`one-primary-action`, `ad-slot-not-allowed`, from `policies` in the contract). Why: one
   obvious "go", and ads never interrupt a task, a dialog or a purchase.
9. **testIDs sit on the accessible element, and a card is never a pressable panel with a nested
   button.** Draw the pressable surface and the button as siblings; decorative parts stay hidden from
   screen readers. Why: on iOS an accessible container hides its children from VoiceOver and from the
   tree E2E tools read, so the nested button can be neither found nor pressed.
   (accessibility-as-code checks it: `nested-pressable`)
10. **Hide what a state hides; never grey it out.** A feature the person cannot use here is left out,
    not shown disabled. Why: a dead control with no way forward reads as a bug.
11. **A design frame that shows a state is opened by the model that owns it, through the handler a
    person's press uses; motion holds still through the reduce-motion hook.** No capture-only branch in
    a view or a model. Why: the screenshot then shows the real code path, and a frame never settles
    while a loop ignores reduce motion.
12. **A screen that is not built is not routed, and nothing stands in for it.** `--all` fails
    `screen-not-built` until every contract screen exists; never a no-op handler or a provider only an
    unbuilt screen needs. Why: both pass every test and fail on a device.

## Workflow

1. **Look first.** From the repo root run
   `node ${CLAUDE_SKILL_DIR}/scripts/check-screens.mjs .`. NOT APPLICABLE means the app keeps no
   screen contract yet; otherwise every FAIL line is work. Read
   [references/contract-format.md](references/contract-format.md) once per session.
2. **Contract first.** No contract yet: copy `templates/contracts/screens.json` and
   `screens.schema.json` to `contracts/`, keep the policies the app wants (`adSlot` only with ads), and
   describe each existing screen. For the screen at hand add or change its entry: route, model, view,
   every state (Chosen ones with `why`), every element with testID, role, component and keys. Write
   its spec beside the design, shaped like [examples/lists-screen-spec.md](examples/lists-screen-spec.md)
   (a detail screen built from library components: [examples/task-detail-entry.json](examples/task-detail-entry.json)).
   A key the catalog lacks goes into the source catalog first, then every language
   (i18n-strings-and-catalogs). Then print the contract you build to:
   `node ${CLAUDE_SKILL_DIR}/scripts/list-screen.mjs . --screen <id>`.
3. **Prerequisites.** The theme, `AppText` and `PressableSurface` (design-system-structure), the render
   helpers (unit-and-component-tests), `test/a11y/find-inaccessible-pressables.ts`
   (accessibility-as-code), the catalogs and `t()` (i18n-strings-and-catalogs), the data layer the
   model reads (persistence-and-migrations). Library components and their part lists come from
   ui-component-library, `ScreenFrame` from react-components-and-hooks.
4. **Tests first.** Copy and adapt the template tests: the view test (one block per state, ids,
   handlers, audit), the model-hook test (`renderHook`, fakes, the app's `I18nProvider`), the state
   function's test. Watch them fail.
5. **Build.** Read [references/screen-building.md](references/screen-building.md) (the three files, the
   common frame on iOS and Android, rules, states, RTL, dark, large text, screenshots) and, for a
   dialog, overlay or sheet, [references/overlays-and-dialogs.md](references/overlays-and-dialogs.md).
   Copy from `templates/` to the same paths what the screen needs: the Lists feature is the model to
   follow (`src/app/(app)/lists.tsx`, `src/features/lists/`), `src/ui/screen-body.tsx`,
   `use-page-bottom-padding.ts` and `use-pair-layout.ts` for bounded pages and side-by-side pairs, the
   catalogs' keys. Rename `lists` to the feature and keep the structure.
6. **Gates.** `npm run typecheck`, `npx eslint . --max-warnings 0`, and the screen's tests
   (`npx jest src/features/<feature> --ci --maxWorkers=2`, paths before any `--selectProjects`).
7. **Check the screen.** `node ${CLAUDE_SKILL_DIR}/scripts/check-screens.mjs . --screen <id>`; fix
   every FAIL line (each names the file, the rule and the fix;
   [references/checks.md](references/checks.md) explains each rule) and rerun until `RESULT: PASS`. At
   the end of screen work run it with `--all`.
8. **Compare and report.** Open the state's reference image and the running screen in light, dark and
   the app's RTL locale on an iOS simulator and an Android emulator, then hand the screen to
   design-visual-parity for the measured comparison. Report which screens pass, the Chosen states you
   added and why, and open questions (a missing key, an id the design needs but the contract lacks):
   the reviewer decides those; never invent.

## Definition of done

- [ ] The screen, each of its dialogs and overlays, and every route file have contract entries; the
      contract validates against its schema.
- [ ] Every contract state has a layout and a view-test block named for it; the state is chosen by a
      pure, tested function.
- [ ] The view sets exactly the contract's testIDs on accessible elements, shows only translated text
      from the model, and reads no store, service or navigation.
- [ ] The view sits in `ScreenFrame` with the edges for what sits around it (`BELOW_HEADER_EDGES` under
      a Stack header; right and left only when the body scrolls on under the home indicator).
- [ ] The route calls the model hook; the hook has its test (each state, each handler, failures).
- [ ] Every block that renders the screen ends with the `findInaccessiblePressables` audit.
- [ ] Overlays render in `Modal` (or a modal root) and close on Android back.
- [ ] `npm run typecheck`, `npx eslint . --max-warnings 0` and the screen's Jest tests pass.
- [ ] The screen was compared with its reference in light, dark and RTL on iOS and Android, and handed
      to design-visual-parity.
- [ ] The only SKIP line allowed is `SKIP src/i18n/catalogs/en.json [unknown-copy-key] not yet created
      (i18n-strings-and-catalogs creates it)`, and only before the app has catalogs.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/list-screen.mjs . --all` prints `RESULT: PASS`
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-screens.mjs . --all` prints `RESULT: PASS`

## Anti-patterns

- **Inventing or renaming a testID to make a test pass.** Change the code to the contract; propose a
  contract change when the design truly needs a new id.
- **An index key** (`lists.list-row.0`, `${testID}.${index}`). Use the item's id or key.
- **A testID on a child of an accessible element, or `accessible` on a row that holds a button.**
  Maestro and VoiceOver never see inside it; keep the row plain and the controls siblings.
- **Un-hiding a decorative part to measure it.** Query it in tests with `includeHiddenElements`; the
  contract marks it crop-only (`a11yHidden`, `coveredBy`).
- **Re-drawing a library component in a screen folder** (a local button, row or dialog card). Use the
  one in `src/ui`; its look and derived ids live there once. The templates draw the dialog card and
  buttons locally only because they must compile without the library; an app with it composes
  `Scrim`, `DialogCard` and `Button`, so `policies.primaryAction` matches its real primary.
- **A store read, `router.push` or `t()` inside a view.** They belong in the model hook.
- **A state the design forgot, left blank** (no empty or error layout). Add it as a Chosen state with
  its why, build it, test it.
- **Greying out a feature the state hides** (Premium content for a free user, the ad slot for a paying
  one). Leave it out.
- **A dialog drawn as a plain View over the screen, or `accessibilityViewIsModal` alone.** TalkBack
  reaches the list behind it; use `Modal` with `onRequestClose`.
- **`onRequestClose={() => {}}`, or no `onRequestClose`.** Android's back does nothing and the person
  is trapped; point it at the cancel handler and test it through the Modal's `requestClose` event.
- **Two primary buttons on one screen** or a destructive action styled as primary.
- **A no-op handler or a placeholder provider for a screen that is not built yet.** Leave it out of
  navigation until it is built.
- **A capture-only branch** (`if (isScreenshotRun)`) in a view or a model. Open the state through the
  owner's handler and freeze motion through `useReduceMotion()`.
- **Declaring a screen done from Jest alone.** Open the reference and the running app on both
  platforms; edge to edge, the home indicator and 200 % text only show there.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/contract-format.md](references/contract-format.md) | The contract file: screens, presentations, code ownership, states, elements and testIDs, derived parts, screenshot reach, policies, ignored routes, changing it, multi-package | Workflow steps 1-2 |
| [references/screen-building.md](references/screen-building.md) | The three files of a screen, the common frame on iOS and Android, screen rules, testIDs and copy in code, states, view and model-hook tests, RTL, dark, large text, screenshots, unbuilt screens, React Navigation appendix | Workflow step 5 |
| [references/overlays-and-dialogs.md](references/overlays-and-dialogs.md) | Choosing a presentation, keeping VoiceOver and TalkBack inside, Android back and predictive back, who opens a dialog, the template dialog, tests | Building a dialog, overlay or sheet |
| [references/checks.md](references/checks.md) | Every rule of both scripts with its reason and fix, what counts as a testID, the allowed SKIP and NOT APPLICABLE lines, the heuristics' known limits | When a FAIL line needs explaining |
| [examples/lists-screen-spec.md](examples/lists-screen-spec.md) | The written spec of one screen: requirements, blocks in order, states, model data, pitfalls | Workflow step 2, writing a spec |
| [examples/task-detail-entry.json](examples/task-detail-entry.json) | A contract entry for a detail screen built from library components (derived parts, a paid-only element, Chosen states) | Workflow step 2 |
| [examples/dialog-host.tsx](examples/dialog-host.tsx) | Shape: one dialog host above the navigator (a request union, `useOpenDialog()`, action-then-close) for apps with dialogs on several screens | When a second screen needs a dialog |
| `templates/contracts/screens.json` | The contract template, filled for the demo app (Tasks, Lists, the delete-list dialog) | Workflow step 2; copy to `contracts/` |
| `templates/contracts/screens.schema.json` | Its JSON Schema | Workflow step 2; copy beside it |
| `templates/src/app/(app)/lists.tsx` | A thin Expo Router route: model hook, header title, view | Workflow step 5 |
| `templates/src/features/lists/lists-screen.tsx` | The pure view, one layout per state, renders the dialog while a delete is pending; its plain `View` root stands in for `ScreenFrame` only so it compiles without it (the header comment gives the frame and edges) | Workflow step 5 |
| `templates/src/features/lists/lists-screen.test.tsx` | Its view test: a block per state, ids, handlers, audits | Workflow step 4 |
| `templates/src/features/lists/use-lists-model.ts` | The model hook: data layer, copy, reduce motion, the delete dialog's state | Workflow step 5 |
| `templates/src/features/lists/use-lists-model.test.tsx` | Its test: each state, retry, ask, confirm, cancel, a failed delete | Workflow step 4 |
| `templates/src/features/lists/lists-state.ts` | Which state shows, a pure function of the repository's answer | Workflow step 5 |
| `templates/src/features/lists/lists-state.test.ts` | Its test | Workflow step 4 |
| `templates/src/features/lists/components/list-summary-row.tsx` | A row: the name and its delete button as siblings, data-keyed ids | Workflow step 5 |
| `templates/src/features/lists/components/lists-empty-body.tsx` | The empty state (Chosen) in `ScreenBody` | Workflow step 5 |
| `templates/src/features/lists/components/lists-error-body.tsx` | The error state (Chosen): message, spacer, one action at the bottom | Workflow step 5 |
| `templates/src/features/lists/delete-list-dialog/delete-list-dialog.tsx` | A dialog in React Native's `Modal`: modal root, Android back, edge to edge; card and buttons drawn locally only so it compiles without ui-component-library (an app composes `Scrim`, `DialogCard`, `Button`) | Building a dialog |
| `templates/src/features/lists/delete-list-dialog/delete-list-dialog.test.tsx` | Its view test, Android back through the Modal's `requestClose` included | Building a dialog |
| `templates/src/ui/screen-body.tsx` | The bounded page body: one gap, under the home indicator, opening at an offset, top overhang. ui-component-library treats it as owned elsewhere by default | Workflow step 5 |
| `templates/src/ui/screen-body.test.tsx` | Its test | With screen-body.tsx |
| `templates/src/ui/use-page-bottom-padding.ts` | The bottom padding of a page that scrolls under the system bar | With screen-body.tsx |
| `templates/src/ui/use-page-bottom-padding.test.tsx` | Its test | With the hook |
| `templates/src/ui/use-pair-layout.ts` | Two blocks side by side that stack at large text | A screen with side-by-side pairs |
| `templates/src/ui/use-pair-layout.test.tsx` | Its test | With the hook |
| `templates/src/i18n/catalogs/en.json` | The Lists and dialog keys in the source language (merge into the app's catalog) | Workflow step 2 |
| `templates/src/i18n/catalogs/ar.json` | The same keys in Arabic, the demo's RTL locale | Workflow step 2 |
| `scripts/check-screens.mjs` | Checker: contract format, route coverage, exact testIDs (derived parts counted), copy keys, policies, view tests per state with audits, modal overlays that close on Android back, route to model hook wiring | Workflow steps 1 and 7 |
| `scripts/list-screen.mjs` | Prints one screen's contract (ids, roles, components, keys with text, states, who sets each id, screenshot reach); `--all` validates the contract (exit 2 without one) | Workflow step 2 |
| `scripts/lib/screen-contract.mjs` | Helper: loads and validates the contract, file ownership, derived parts, route files | Never by hand |
| `scripts/lib/screen-source.mjs` | Helper: strings, patterns, `t()` keys, JSX uses and test blocks in TypeScript sources | Never by hand |
| `scripts/selftest.mjs` | Proves both scripts pass the templates and fail every planted bug | After changing a script or template |
| `scripts/check-lib.mjs` | Shared script library, synced (do not edit here) | Never by hand |
| `assets/shared.json` | Declares the shared files this skill copies in | When adding a shared file |
| `tests/bases/app/` | The small Tasks app the templates are laid over in the self-test | When the self-test base changes |
| `tests/fixtures/` | Good, pass, planted-bad and error cases for both scripts (overlay format) | When adding a rule |

## Related skills

- `ui-component-library` - the components screens are made of and the parts they derive.
- `design-system-structure` - tokens, `AppText`, `PressableSurface`, colours and dark mode.
- `design-visual-parity` - the measured screenshot comparison each finished screen goes through.
- `navigation-and-routing` - routes, groups, Back, deep links and placeholder routes.
- `react-components-and-hooks` - model hooks, effects, `ScreenFrame` and the window class.
- `ui-states-and-feedback` - the shared loading, empty, error and offline patterns.
- `i18n-strings-and-catalogs`, `rtl-and-direction`, `accessibility-as-code` - texts, mirroring, screen readers.
- `unit-and-component-tests` - the render helpers and test conventions; `e2e-maestro` - flows on the same ids.
- `admob-ads-and-consent`, `in-app-purchases` - the ad slots and paid states behind the policies.
- `debug-menu-and-test-hooks` - how a test build asks for a frame state.
