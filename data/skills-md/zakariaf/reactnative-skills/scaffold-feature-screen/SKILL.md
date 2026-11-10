---
name: scaffold-feature-screen
description: Scaffolds one Expo Router feature - thin route, pure view, model hook, tests, message keys, typed params - and proves it. Use when adding a screen, page or feature folder, or checking one is done. Not for screen contents (screen-contracts).
---

# Scaffold a feature screen

Every screen of an Expo Router app starts the same way: a script writes one feature folder
(`src/features/<feature>/`) with a pure view, its model hook, a test for each, a thin route file and
its route test, the message keys in every catalog, and, for a dynamic route, a valibot params parser
with an invalid-link state; it registers the route and the screen in the app's contracts. A second
script proves the feature is complete, on iOS and Android alike, before anything grows on it.

## Rules that must hold

1. **Generate the feature with `scaffold-feature.mjs`; never copy a neighbour.** The script fills
   every placeholder in paths and contents, writes all files of the unit together, and never
   overwrites a file that differs (`conflict`). Why: a copied feature keeps the old testIDs, keys,
   titles and wiring in corners no test reads, and a hand-copied template leaves `__FEATURE__`
   behind. (`placeholder-left`)
2. **One feature is one kebab-case folder, and that name is everything's name.** `note-detail` is
   the folder, the testID scope (`note-detail.screen`), the message-key prefix (`note-detail.title`),
   the screen-contract id and the file prefix; the types are `NoteDetail…`. Why: one grep finds the
   whole feature, and E2E flows, translators and reviewers see the same word. (`feature-names`)
3. **Four files exist from the first commit, named after the folder:** `<f>-screen.tsx` exporting
   `<F>Screen`, `use-<f>-model.ts` exporting `use<F>Model` and `type <F>Model`, and
   `<f>-screen.test.tsx` and `use-<f>-model.test.tsx` beside them. Why: the view is tested with plain
   values and the hook with providers and fakes; a screen without both tests is the one that ships
   broken. (`feature-files`, `feature-names`)
4. **The route is two lines of work.** `src/app/<route id>.tsx` default-exports `<F>Route`, calls
   `use<F>Model()` once, hands the translated title to the header with `<Stack.Screen options>` and
   renders `<F>Screen model={model}`; nothing else. Why: Expo Router bundles every file in `src/app`,
   and logic there can be neither reused nor tested alone (architecture-and-boundaries' `route-thin`).
   (`route-wiring`)
5. **Every route has its route test in the feature.** `<f>-navigation.test.tsx` imports the route's
   default export from `@/app/<route id>` and opens it at its URL with `renderRouterWithProviders`;
   only a route an E2E flow covers may carry `// device-only:` instead. Why: tests cannot live in
   `src/app`, and only this test proves URL → route → model → view runs once as on a device.
   (`route-test`)
6. **The view is pure and the model hook is the only reader.** The screen and every `components/`
   file import no router, store, service, `src/data`, `src/api` or `t()`, and call none of their
   hooks; the model hook reads them and hands texts translated and handlers ready. The view's root is
   react-components-and-hooks' `<ScreenFrame edges={BELOW_HEADER_EDGES}>` when the app has
   `src/ui/screen-frame.tsx` (the generator writes it), a plain `View` until then. Why: the view then
   renders every state from plain values, the reads live in one tested place, and the Android 15+
   edge-to-edge and iPhone insets are handled once. (`view-pure`)
7. **Components live in `components/`, a dialog with its own model in its own subfolder.** The feature
   root holds the screen, the model hook (and its split parts), pure logic and the tests. Why: the
   reviewer finds the screen at a glance, and a component that a second feature needs moves to
   `src/ui` without untangling. (`component-placement`)
8. **A dynamic route parses its params at the edge, in the model hook.** `<f>-params.ts` is a valibot
   schema whose keys equal the route's `[param]` names, returns a `Result`, and has its test; the
   model hook calls `parse<F>Params(useLocalSearchParams())`; the route and the view never read
   params. A failed parse is the invalid-link state, whose one way out is `router.dismissTo('/')`.
   Why: any link opens the route with any text, repeated keys arrive as arrays, and the type argument
   of `useLocalSearchParams<T>()` is a cast. (`params-parser`, `params-in-model`)
9. **Every text is a key under `<f>.` in every catalog, in the same change.** `--title` and `--body`
   are source-language text (the app's `SOURCE_LANGUAGE`): the source catalog gets them, every other
   catalog gets them as drafts. The fixed texts come from the skill's translation for a language, else
   English as a draft. The generator lists the drafts per language; each drafted language belongs in
   `contracts/i18n.json` `reviewLanguages`, the translation queue. Why: a missing key fails a person on
   a phone in another language, not a test, and a draft nobody queues ships as English.
   (`message-key-missing`; after a rename, `--orphans`: `message-key-orphan`)
10. **The feature is registered where the app keeps its contracts.** Its route id is in
    `contracts/navigation.json` `routes` (a dynamic route also in `paramParsers`), and
    `contracts/screens.json` has its entry (route, model, view, states, elements). Why: a route change
    starts in the contract, and the screen's ids and keys are agreed there before code grows.
    (`nav-contract`, `screen-contract`)
11. **The scaffold is a skeleton; everything after it is test-first.** Reading data, a handler or a
    state starts as a failing test in the matching test file; a model past about 40 lines splits into
    `use-<f>-actions.ts` and a pure `<f>-model-of.ts`. Why: the scaffold proves the wiring once; only
    tests keep it true while the screen grows.
12. **Prove the feature complete before handing it over.** `check-feature.mjs` passes for it, and so
    do the neighbours that own the deeper rules (navigation, screen contract, catalogs). Why: a feature
    "done" by eye is the one missing its route test or its Arabic keys.

## Workflow

1. **Name it.** Pick the feature name, route id and title in the source language
   ([references/feature-anatomy.md](references/feature-anatomy.md) "Naming the feature",
   [references/routes-and-params.md](references/routes-and-params.md) "Route ids and hrefs"). A list
   and its detail are two features (`notes`, `note-detail`). Confirm the prerequisites listed in
   feature-anatomy "What the scaffold needs" exist; each names the skill that creates it.
   - **An app fresh from expo-project-bootstrap** still has its starter screen (`src/app/index.tsx`
     rendering `src/features/home/`, whose header says this skill replaces it). It holds no work:
     delete both, and generate the first feature at its route (`--route index`, or `"(app)/index"`
     in an app with an `(app)` group). The generator names the starter instead of overwriting it
     (`starter`), and `check-feature.mjs` reports it as one `starter-screen` line until it is gone.
2. **Plan.** From the repo root run
   `node ${CLAUDE_SKILL_DIR}/scripts/scaffold-feature.mjs . --feature <name> --route "<route id>" --title "<Title>"`.
   Read the plan: `new`, `same`, `edit` lines, the `drafts <lang>:` lines and the `note` lines (the
   view's frame, a drafted language missing from `reviewLanguages`, a Tabs parent, a `home` other
   than `/`); a `conflict` means the name, the route or its URL is taken (another route file already
   serves it, perhaps in another group: pick another, or finish the existing feature by hand), or a
   contract holds `//` comments the edit would drop. Compare with [examples/scaffold-plan.txt](examples/scaffold-plan.txt).
3. **Write.** Rerun with `--write`. It formats the written files with the app's Prettier when
   installed. The generator and its options: [references/generator-and-checker.md](references/generator-and-checker.md).
4. **Run the feature's tests and gates:** `npx jest src/features/<name> --ci --maxWorkers=2`, then
   `npm run typecheck` and `npx eslint src/features/<name> src/app --max-warnings 0`.
5. **Check it:** `node ${CLAUDE_SKILL_DIR}/scripts/check-feature.mjs . --feature <name>`. Fix every
   `FAIL` line (file, rule, fix; each rule is explained in generator-and-checker "check-feature
   rules") and rerun until `RESULT: PASS`.
6. **Finish what a person decides:** translate the draft keys the plan listed (add each drafted
   language to `contracts/i18n.json` `reviewLanguages` when the plan says it is missing; then
   i18n-strings-and-catalogs' review queue carries them), adjust the screen entry's states and elements as the design says (screen-contracts), and
   pick the header and presentation (navigation-and-routing).
7. **Grow it test-first** with [references/test-recipes.md](references/test-recipes.md): a failing
   test, then the code, for each behaviour (data through a repository or query, handlers, the states
   the screen contract lists). Imitate [examples/list-detail/](examples/list-detail/) for a detail
   screen that reads data by a numeric id.
8. **Run the neighbours' checkers:** navigation-and-routing's `check-navigation.mjs`, screen-contracts'
   `check-screens.mjs . --screen <name>`, i18n-strings-and-catalogs' `check-catalogs.mjs`.
9. **Rerun `check-feature.mjs`** (add `--orphans` after renaming or deleting part of a feature) until
   `RESULT: PASS`, and report: the route, the keys still to translate, the states still to build.

## Definition of done

- [ ] The feature was written by `scaffold-feature.mjs` (no copied folder), and its folder name is its
      testID scope, key prefix and screen id.
- [ ] `<f>-screen.tsx`, `use-<f>-model.ts`, both tests and `<f>-navigation.test.tsx` exist; the route
      calls the model hook once and renders the view.
- [ ] A dynamic route has `<f>-params.ts` with its test, read only by the model hook, and an
      invalid-link state with one way out.
- [ ] The view and `components/` read nothing; every text arrives translated from the model.
- [ ] The view's root is `<ScreenFrame testID edges={BELOW_HEADER_EDGES}>` when the app has
      `src/ui/screen-frame.tsx` (a plain `View` only while it does not).
- [ ] No starter screen of expo-project-bootstrap is left (`src/app/index.tsx` + `src/features/home/`).
- [ ] Every key is in every catalog; every language the plan listed drafts for is in
      `contracts/i18n.json` `reviewLanguages` (or, before that contract exists, the drafts are in the
      report).
- [ ] The route is in `contracts/navigation.json` (and `paramParsers`), the screen in
      `contracts/screens.json`.
- [ ] `npx jest src/features/<f>`, `npm run typecheck` and ESLint pass.
- [ ] The only SKIP lines allowed are, while the app has none: `SKIP contracts/navigation.json
      [nav-contract] not yet created (navigation-and-routing creates it)`, `SKIP contracts/screens.json
      [screen-contract] not yet created (screen-contracts creates it)`, `SKIP src/i18n/catalogs
      [message-key-missing] not yet created (i18n-strings-and-catalogs creates it)`, or for an empty
      catalogs folder `SKIP src/i18n/catalogs [message-key-missing] holds no catalog
      (i18n-strings-and-catalogs creates them)`.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-feature.mjs . --feature <f>` prints `RESULT: PASS`

## Anti-patterns

- **`cp -R src/features/tasks src/features/notes` and search-and-replace.** Old ids, keys and titles
  survive; run the generator.
- **Copying the templates by hand.** `__FEATURE__` ends up in a path or a key; the generator fills
  them and `placeholder-left` catches what is left.
- **Logic in the route file** (`useState`, a query, `useLocalSearchParams`). Move it to the model hook.
- **Calling `useT()` or `useRouter()` in the view "just for one label".** Translate and build the
  handler in the model; the view stays a function of its props.
- **A route test under `src/app/`.** Expo Router bundles it as a route; it lives in the feature.
- **Trusting `useLocalSearchParams<{ noteId: string }>()`.** A cast; parse with the feature's parser.
- **A parser key that differs from the bracket** (`[noteId].tsx`, schema `id`). Every link then opens
  the invalid-link state; `params-parser` names it.
- **Going home with `router.navigate('/')` from the invalid-link state.** It stacks a second home;
  `dismissTo('/')`.
- **Adding keys to `en.json` only.** The other languages fail on the phone; every catalog gets them.
- **Overwriting the bootstrap starter by hand-editing `home-screen.tsx` into a feature.** It has no
  model, tests or contract entry; delete it and generate the first feature at `--route index`.
- **One feature folder for a list and its detail.** Two screens, two features, two models.
- **Writing the data reads into the scaffold before a test asks for them.** Grow it test-first.
- **Calling the scaffold done because the generator passed.** The feature is done at
  `check-feature.mjs` and the neighbours' checks.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/feature-anatomy.md](references/feature-anatomy.md) | The unit: naming, each file's job and imports, the model's shape and splits, components and dialogs, iOS and Android behaviour, prerequisites, pitfalls | Workflow steps 1 and 7 |
| [references/routes-and-params.md](references/routes-and-params.md) | Route ids, hrefs, the header title, dynamic params and their parser, the invalid-link state, contracts, verified router facts | Workflow steps 1 and 7 |
| [references/generator-and-checker.md](references/generator-and-checker.md) | `scaffold-feature.mjs` options and plan lines; every `check-feature.mjs` rule with its fix; config keys; multi-package | Workflow steps 2, 3, 5 and 9 |
| [references/test-recipes.md](references/test-recipes.md) | The view, model, route and params tests, growing test-first, Jest commands | Workflow steps 4 and 7 |
| `templates/src/app/__ROUTE_ID__.tsx` | The thin route of a static screen | The generator writes it |
| `templates/src/app/__DETAIL_ROUTE_ID__.tsx` | The thin route of a dynamic screen | The generator writes it |
| `templates/src/features/__FEATURE__/` | Static screen: view, model hook, view test, model test, route test | The generator writes it |
| `templates/src/features/__DETAIL__/` | Dynamic screen: the same plus the params parser and its test and the invalid-link component | The generator writes it |
| `templates/src/i18n/catalogs/` | The scaffold's keys in `en` and `ar`, merged into every catalog | The generator merges them |
| [examples/scaffold-plan.txt](examples/scaffold-plan.txt) | A dry run and a write for a dynamic route in the reference app | Workflow step 2 |
| [examples/list-detail/](examples/list-detail/) | A grown detail feature: numeric id parser, pure state chooser, model reading a repository | Workflow step 7 |
| `scripts/scaffold-feature.mjs` | Generator: plan (default) or `--write`; never overwrites | Workflow steps 2 and 3 |
| `scripts/check-feature.mjs` | Checker: every rule above, one feature or all | Workflow steps 5 and 9 |
| `scripts/lib/json-format.mjs` | Prints JSON in Prettier's layout for the catalog and contract edits | When changing the generator |
| `scripts/lib/feature-app.mjs` | App facts both scripts read: the bootstrap starter screen and the source language | When changing either script |
| `scripts/selftest.mjs` | Proves both scripts: planted bugs, plans, conflicts, and the generator's output passing the checker | After changing a script, template or fixture |
| `scripts/check-lib.mjs` | Shared script library (synced; do not edit here) | Never by hand |
| `scripts/lib/source-scan.mjs` | Shared import-resolution helpers (synced; do not edit here) | Never by hand |
| `assets/shared.json` | Declares the synced files | When adding a shared file |
| `assets/template-placeholders.json` | The placeholder values that prove the templates in the reference app | When adding a placeholder |
| `tests/bases/` | Fixture apps: `app/` (contracts, planted skill decoys), `empty-app/` (for the generator) | When adding a case |
| `tests/fixtures/` | The self-test cases per script | When adding a rule |

## Related skills

- `screen-contracts` - what the screen shows: states, testIDs, copy keys, the view test per state.
- `navigation-and-routing` - the route contract, layouts, guards, modals and the not-found route.
- `architecture-and-boundaries` - where files live and the thin-route rule.
- `react-components-and-hooks` - the model hook, effects, `ScreenFrame` edges, components.
- `i18n-strings-and-catalogs` - catalogs, key names, translating the drafts.
- `naming-conventions` - file, export, testID and key shapes.
- `expo-project-bootstrap` - the new app whose starter screen the first feature replaces.
- `unit-and-component-tests` - the render helpers and Jest projects.
- `ui-states-and-feedback` - loading, empty, error and offline states as the screen grows.
- `forms-and-input` - a screen that edits data.
- `state-management-zustand` and `networking-and-server-state` - what the model hook reads.
- `deep-links-and-universal-links` - links from outside the app into the new route.
- `e2e-maestro` - the device flow for the new screen.
