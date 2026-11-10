---
name: naming-conventions
description: Names files, routes, exports, hooks, booleans, kinds, testIDs, message keys, app ids and env vars. Use when adding or renaming anything or on a naming lint error. Not for placement (architecture-and-boundaries).
---

# Naming conventions

One naming scheme for an Expo app, so every name is predictable from the thing it names and every
thing is findable from its name: agents and reviewers find code by `grep` and by path, and names are
the search index. This skill holds the rules, a repo-owned contract for the app's own naming facts,
and two zero-dependency checkers that prove the repo follows them.

## Rules that must hold

1. **Files and folders are kebab-case; route files follow the Expo Router grammar.** `task-row.tsx`,
   `use-tasks-model.ts`, `task-details/`; middle extensions (`.test`, `.golden.test`, `.sim.test`,
   `.perf.test`, `.d`, `.config`) and platform extensions (`.ios`, `.android`, `.web`) are fine. In
   `src/app/`: kebab URL segments, `(group)` folders, `[camelCaseParam]`, `[...rest]`, `_layout`,
   `index`, `+not-found`. Why: macOS (also EAS's iOS builders) ignores case, but Linux CI and EAS's
   Android (Linux) workers do not, and a param name becomes the key of `useLocalSearchParams()`.
2. **The main export is named after its file.** `task-row.tsx` → `TaskRow`, `use-tasks-model.ts` →
   `useTasksModel`, `tasks-screen.tsx` → `TasksScreen`, `system-clock-adapter.ts` →
   `createSystemClockAdapter`, `fake-clock.ts` → `createFakeClock`, `clock-port.ts` → `ClockPort`,
   `src/stores/tasks-store.ts` → `useTasksStore`, `tasks-reducer.ts` → `tasksReducer`,
   `plugins/with-x.ts` → `withX`. A route file default-exports `<Name>Route` (`<Name>Layout` in
   `_layout.tsx`), never anonymous and never `<Name>Screen`. Why: the file name alone tells what to
   import, and the screen name stays unique.
3. **No grab-bag files or folders, no barrels.** No `utils.ts`, `helpers.ts`, `common.ts`, `shared.ts`,
   `misc.ts`, `stuff.ts`, no `src/utils/`; the only `index` files are route files and files a tool
   requires (declared in `contracts/naming.json`). Why: grab-bags grow without limit and barrels
   create import cycles.
4. **Line 1 of every `.ts`/`.tsx`/`.js`/`.mjs`/`.cjs` file names its path.** `// src/ui/app-text.tsx`
   (a note may follow after `: ` or a space; after a `#!` line, line 2; a directive comes after it).
   Why: snippets, diffs and tool output always show where code lives. This skill owns the rule; other
   skills cite it. On by default; `"pathHeader": false` in the contract turns it off.
5. **Case by kind.** Values and functions camelCase; components and types PascalCase; module-level
   fixed data (a literal, a regex, an `as const` table) UPPER_CASE; objects built by a call stay
   camelCase (`styles`, `queryClient`). Acronyms are words (`SqlDriver`, `isRtl`, `ApiClient`); no
   leading or trailing underscores except unused parameters. Why: word boundaries and mutability stay
   visible.
6. **Booleans read as questions.** Every boolean variable and parameter starts with `is`, `has`, `can`,
   `should`, `did`, `will` or `was`; destructured booleans are renamed (`{ disabled: isDisabled }`).
   Why: `if (isDone)` reads as a question at the call site.
7. **Types are `type`, never `interface` (outside `*.d.ts` merging), never `I`-prefixed, never
   `enum`.** A closed set is an `as const` array plus a derived union. Suffixes say whose:
   `<Component>Props`, `<Domain>State`, `<Domain>Action`, `<Operation>Error`, `<Function>Options`,
   `<Concern>Port`; type parameters `T` or `TName`. Why: erasable syntax, exhaustive switches, and
   names that say what they belong to.
8. **React names the React way.** Handlers inside a component are `handleX`, callback props `onX`,
   hooks `useX` in `use-x.ts` (one per file; a second hook exported there is only a building block
   `useX` calls, like `useFontScale` beside `useTextStyle`; a context's own hook stays beside its
   private context in `<x>-context.tsx`, which exports `XProvider`), screens `<Name>Screen` in
   `<name>-screen.tsx`, a feature's model hook `use-<feature>-model.ts`. Why: the React Compiler and
   `react-hooks` rules rely on `use`; readers rely on the rest.
9. **`kind` and `type` values are kebab-case with a grammar.** Commands imperative
   (`'complete-task'`), events past tense (`'task-completed'`), errors a noun phrase
   (`'stale-revision'`), reducer actions imperative (`'set-filter'`). A stored value is a data format:
   renaming it needs a migration. A value a format or library owns is not a kind: MIME types,
   react-hook-form's `setError` types, an adapter's SDK options. Why: one grep finds every producer
   and consumer.
10. **testIDs are `<screen>.<element>[.<key>]` and flows select only by id.** `tasks.add-button`,
    `tasks.task-row.<task id>`; repeated items append a stable data key as its own segment, never a
    list index; interactive elements end in their role (`-button`, `-row`, `-switch`, `-input`). OS-owned UI
    without a testID is tapped only under a `# system-ui: <why>` comment. Why: Maestro's `id:` matches
    `testID` on iOS and Android, so one flow runs in every locale on both platforms.
11. **Message keys are semantic literals with typed placeholders.** 2-5 dot-separated kebab segments
    (`tasks.add-button.label`), the first a feature folder or a declared area (`common`, `errors`, ...),
    written as a literal or picked from a typed table, never built; placeholders camelCase and typed
    (`{count, number}`, `{taskCount, plural, ...}`, free text `{listName}`). Why: a wording change never
    renames a key, and tools can check what they can see.
12. **Tests and flows are named after what they cover.** `<unit>.test.ts(x)` next to the unit
    (`.golden.test.ts`, `.sim.test.ts`, `.android.test.tsx`, Node-API tests in root `test/`); `describe('<export>')` →
    `describe('when ...')` → `it('<third-person verb> ...')`, `it` never `test`; flows
    `.maestro/flows/<area>/<nn>-<name>.yaml`, sub-flows `.maestro/subflows/<name>.yaml`; a folder of
    flows CI deliberately skips is declared in `contracts/naming.json` `extraE2eFolders`. Why: Jest
    projects select by suffix and Maestro runs only the top level of the folder it is given.
13. **Ids outside the code have one shape.** The iOS bundle id and Android package are one lowercase
    reverse-DNS id with no Java keyword segment (`com.acme.tasks`); product ids are
    `<app id>.<product>` (`<last app-id segment>.<product>` only when that passes the limit), valid
    on both stores, at most 40 characters; the slug is kebab-case; an id already live on a store or
    EAS keeps its shape and is recorded in `contracts/naming.json` `published*`. Env vars are
    UPPER_SNAKE_CASE; app code reads only `EXPO_PUBLIC_*` and Expo's own `EXPO_OS`, `EXPO_SERVER`,
    `EXPO_BASE_URL`, `NODE_ENV`, by name with dot access (never destructured, copied, spread or
    bracketed), while server code (`+api.ts`, `+middleware.ts`, `src/server/`) reads secrets under
    plain names, never under an `EXPO_PUBLIC_` name; npm scripts `<verb>` or `<area>:<verb>`; one
    package scope when multi-package. Why: both stores, both native projects and Expo's inlining
    accept exactly these shapes (anything else read in app code is `undefined` in a release build),
    and changing a live id ships a new app.
14. **Canonical names are declared and never renamed silently.** Port types, npm scripts and env vars
    that other code, CI or docs depend on are listed in `contracts/naming.json` `canonical`; renaming
    one is a stop-and-ask decision. Why: lint exemptions, fakes, CI jobs and EAS config match them by
    name.

## Workflow

1. Name what you are about to create before writing it. Find the kind of name in the table below and
   read that reference section; for anything new, start with
   [references/naming-rules.md](references/naming-rules.md) (every rule with a good/bad table).
2. First time in a repo: copy [templates/contracts/naming.json](templates/contracts/naming.json) to
   `contracts/naming.json` and fill the app's `locales`, `keyAreas` (drop template areas no key
   uses), `canonical` names and `storeProductIds`. Product ids are permanent on both stores: stop and
   ask the developer before writing a new one. In an app that is already published, ask which bundle
   id, package, slug and products are live and record them in `publishedAppIds`, `publishedSlugs`,
   `publishedProductIds` (each with its `why`) instead of "fixing" them.
3. For a closed set of values (filters, priorities, variants), copy
   [templates/string-union.ts](templates/string-union.ts) and its test
   [templates/string-union.test.ts](templates/string-union.test.ts) to
   `src/features/<feature>/<name>.ts` and fill every `__PLACEHOLDER__`.
4. Imitate the examples: [examples/task-row.tsx](examples/task-row.tsx) (component, props, boolean
   prop, handler, testID), [examples/task-details-route.tsx](examples/task-details-route.tsx) (route
   file), [examples/tasks-reducer.ts](examples/tasks-reducer.ts) and its test (state, actions, test
   titles), [examples/task-sync-types.ts](examples/task-sync-types.ts) (the kind grammar),
   [examples/01-add-task.yaml](examples/01-add-task.yaml) (flow selectors), and for the games plugin
   [examples/lights-out-types.ts](examples/lights-out-types.ts).
5. Renaming: change the file, its path header, its main export and every import in one commit. A
   stored name (a `kind` value, an analytics event, a catalog key) also needs a migration or a catalog
   update, and a `Gate-Change:` trailer when a golden or frozen fixture changes (git-commits-and-reporting
   owns the trailer). A route file rename changes a URL: keep a redirect for deep links and app links.
   A canonical name (rule 14): stop and ask the reviewer, then update the contract in the same commit.
   Never rename a bundle id, package, slug or product id that is live: that ships a new app and breaks
   updates, purchases and links; stop, ask the developer, and record it as published.
6. Check (validation loop): when `node_modules` exist, `npx eslint . --max-warnings 0` (the
   naming-convention, check-file, testID and kind rules). Always:
   `node ${CLAUDE_SKILL_DIR}/scripts/check-file-names.mjs .` and
   `node ${CLAUDE_SKILL_DIR}/scripts/check-code-names.mjs .`. Fix every `FAIL` line (file, rule, fix)
   and rerun until both print `RESULT: PASS`. A finding that looks wrong:
   [references/contract-and-checkers.md](references/contract-and-checkers.md), "Fixing a finding".

| Naming... | Read |
|---|---|
| a file, folder, route file, test file, fake, flow, catalog, fixture or plugin | [references/files-and-folders.md](references/files-and-folders.md) |
| a variable, constant, type, component, hook, handler, prop, route component, store, reducer or action | [references/code-identifiers.md](references/code-identifiers.md) |
| a command, event, error or action value, a testID, a Maestro selector, a message key or placeholder | [references/kinds-testids-and-keys.md](references/kinds-testids-and-keys.md) |
| an app id, product id, slug, variant, npm script, env variable, package, commit or tag | [references/packages-scripts-env-and-tags.md](references/packages-scripts-env-and-tags.md) |
| the contract, a checker rule, a SKIP line or a false positive | [references/contract-and-checkers.md](references/contract-and-checkers.md) |

## Definition of done

- [ ] `npx eslint . --max-warnings 0` passes (naming-convention, check-file, testID and kind rules).
- [ ] `contracts/naming.json` exists (from the template) with the app's locales, key areas, canonical
      names and product ids.
- [ ] Every new file is kebab-case (route files: the router grammar), its main export is named after
      it, route files default-export `<Name>Route`/`<Name>Layout`, and line 1 is its path.
- [ ] No new `utils`/`helpers`/`common` files or folders and no barrel `index` files.
- [ ] New commands are imperative, events past tense, all `kind`/`type` values kebab-case; renamed
      stored names have a migration.
- [ ] Every tappable or asserted element has a `<screen>.<element>` testID ending in its role, and
      flows select by `id:` only.
- [ ] New message keys start with a feature or declared area, are literals, and their placeholders
      are typed; after a catalog change the i18n-strings-and-catalogs catalog verifier passes and
      every new key exists in every locale catalog.
- [ ] New ports, adapters and fakes follow `<concern>-port.ts`, `<library>-<concern>-adapter.ts` and
      `fake-<concern>.ts`, and live ids stay as recorded in `published*`.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-code-names.mjs .` prints `RESULT: PASS`. Expected SKIP
      lines while an Expo app has not created those folders yet: `SKIP src/i18n/catalogs [i18n-key] not
      yet created (i18n-strings-and-catalogs creates it)` and `SKIP .maestro [maestro-selector] not yet
      created (e2e-maestro creates it)`; when multi-package, one pair per Expo app workspace, prefixed
      with its folder (`SKIP apps/mobile/.maestro ...`).
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-file-names.mjs .` prints `RESULT: PASS`

## Anti-patterns

- **Naming after the implementation instead of the job.** `sqlite-helpers.ts`, `utils.ts`: name the
  file after what it does (`read-task.ts`), one job per file.
- **A second name for a canonical thing.** `ClockService`, `IClock`, `DbDriver` next to `SqlDriver`:
  every fake, lint exemption and test expects the declared name.
- **A route component called `TasksScreen`.** The route is `TasksRoute`; `TasksScreen` is the view in
  `src/features/tasks/`. Two symbols with one name make every grep ambiguous.
- **English text in keys.** `tasks.add-a-new-task` breaks when the wording changes; name the meaning
  (`tasks.add-button.label`).
- **Building keys or testIDs from strings.** `` t(`tasks.priority.${priority}`) `` and
  `` testID={`row-${index}`} `` hide names from the tools; use a typed table of literal keys and a
  stable data key.
- **Imperative events or past-tense commands.** `{ kind: 'complete-task' }` as an event reads as a
  request; events say what happened (`'task-completed'`).
- **Renaming a stored `kind` "for consistency".** The outbox, backups and analytics still hold the old
  value; migrate them or keep the name.
- **Selecting by text in a flow.** `tapOn: 'Add task'` fails in Arabic; select by id. Only OS-owned UI
  without a testID (the iOS link alert, Android's permission dialog) may use text, under a
  `# system-ui: <why>` comment.
- **Two catalogs or files that differ only by case.** `pt-BR.json` next to `pt-br.json`, `TaskRow.tsx`
  next to `task-row.tsx`: on a case-insensitive Mac they are one file; in CI they are two.
- **Silencing the rule instead of renaming.** Inline disables are switched off and the checkers have no
  ignore comment; the rename (or a reviewed contract entry) is always the fix.
- **Renaming a secret to `EXPO_PUBLIC_` to quiet `env-var`.** Every `EXPO_PUBLIC_` value ships inside
  the app; server-only code moves to an `+api.ts` route or `src/server/`, Node-only code goes in
  `nodeCode`.
- **"Fixing" a live bundle id or slug.** `com.Acme.Tasks` on the App Store stays `com.Acme.Tasks`;
  record it in `publishedAppIds` instead.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/naming-rules.md](references/naming-rules.md) | Every rule with its reason and enforcement, and a good/bad table for every kind of name | Workflow step 1 |
| [references/files-and-folders.md](references/files-and-folders.md) | File patterns by kind, route files, ports/adapters/fakes, tests, catalogs, flows, plugins, tool-owned names, the path header, multi-package | Naming a file, folder or route |
| [references/code-identifiers.md](references/code-identifiers.md) | Identifiers, types, React parts, route components, stores and actions, the enforcing ESLint config, React Navigation appendix | Naming inside a file; a naming-convention error |
| [references/kinds-testids-and-keys.md](references/kinds-testids-and-keys.md) | The kind grammar, testIDs on iOS and Android, Maestro selectors, message keys and placeholders | Adding a command, event, action, testID or key |
| [references/packages-scripts-env-and-tags.md](references/packages-scripts-env-and-tags.md) | App ids, product ids, slug and scheme, variants, npm scripts, env variables, packages, commit and tag names | Adding an app id, product, script, variable, workspace or release |
| [references/contract-and-checkers.md](references/contract-and-checkers.md) | contracts/naming.json keys, layout keys, every checker rule, SKIP lines, fixing a finding | Adopting the skill; an unexpected checker result |
| [templates/contracts/naming.json](templates/contracts/naming.json) | The repo-owned naming contract (copied to `contracts/naming.json`) | Workflow step 2 |
| [templates/string-union.ts](templates/string-union.ts) | `as const` values + derived union + type guard (the enum replacement) | Workflow step 3 |
| [templates/string-union.test.ts](templates/string-union.test.ts) | The guard's test, copied next to it | Workflow step 3 |
| [examples/task-row.tsx](examples/task-row.tsx) | Component, props, boolean prop, handler, callback prop, testID with a data key and role | Workflow step 4 |
| [examples/task-details-route.tsx](examples/task-details-route.tsx) | An Expo Router route file: camelCase param, `<Name>Route` default export | Workflow step 4 |
| [examples/tasks-reducer.ts](examples/tasks-reducer.ts) | State, action union, default, reducer and an `as const` table | Workflow step 4 |
| [examples/tasks-reducer.test.ts](examples/tasks-reducer.test.ts) | describe/when/it titles with third-person verbs | Workflow step 4 |
| [examples/task-sync-types.ts](examples/task-sync-types.ts) | Commands, events, errors and a result union on a sync log | Workflow step 4 |
| [examples/lights-out-types.ts](examples/lights-out-types.ts) | The kind grammar on a public-domain puzzle (games plugin) | Workflow step 4, games |
| [examples/01-add-task.yaml](examples/01-add-task.yaml) | A Maestro flow that selects only by id | Workflow step 4 (E2E) |
| `scripts/check-file-names.mjs` | Checks file, folder and route names, path headers, export and route component names, one hook per `use-*.ts`, file patterns, package names, app and product ids, script names, canonical names | Workflow step 6 |
| `scripts/check-code-names.mjs` | Checks testIDs, kind values, message keys and placeholders, env vars, test titles, type/boolean/handler/constant/acronym names, flow selectors | Workflow step 6 |
| `scripts/lib/names.mjs` | Case helpers, the route grammar and the grammar loader | Only when changing a checker |
| `scripts/lib/naming-scope.mjs` | The scan scope (layout, workspaces, server and Node code) and the contract reader (published ids and extra e2e folders included) | Only when changing a checker |
| `scripts/lib/app-config-ids.mjs` | Reads the slug, bundle id, package and id candidates from `app.config.*` and `app.json`, including Expo's variant shapes (ternary, `??`, template start, `getUniqueIdentifier()`) | Only when changing a checker |
| `scripts/lib/source-scan.mjs` | Dependency-free lexer for comments, strings, JSX tags and imports (synced; do not edit here) | Only when changing a checker |
| `scripts/lib/workspaces.mjs` | Reads package.json workspaces (synced; do not edit here) | Only when changing a checker |
| `scripts/check-lib.mjs` | Shared script helper: arguments, reporting, layout, repo walk, self-test assembly (synced; do not edit here) | Never by hand |
| `scripts/selftest.mjs` | Proves both checkers pass the assembled good app and catch every planted bug | After changing a checker or the grammar data |
| `assets/naming-rules.json` | The library's name grammars (testID, key, app id, product id, locale tag, script, env, MIME type), prefixes, role words, secret env words | When a grammar changes |
| `assets/naming-contract.schema.json` | JSON Schema of `contracts/naming.json` | Editing the contract |
| `assets/template-placeholders.json` | Placeholder values used when the templates are verified in the reference app | When adding a template placeholder |
| `assets/shared.json` | Declares the shared files this skill copies in | When adding a shared file |
| `tests/bases/app/` | The neutral Tasks app the self-test cases start from (with planted decoys in installed-skill folders) | When adding a self-test case |
| `tests/fixtures/` | One overlay case per rule (`mutation.json`/`DELETE.txt` + `EXPECT.txt`) for each checker | When adding a rule to a checker |

## Related skills

- `typescript-and-lint-rules` - the full ESLint and tsconfig set, size limits and forbidden patterns.
- `architecture-and-boundaries` - which folder and layer a file belongs in.
- `navigation-and-routing` - Expo Router layouts, typed routes, params and redirects.
- `i18n-strings-and-catalogs` - catalog format, ICU messages, polyfills and translations.
- `e2e-maestro` - writing the flows that use these testIDs.
- `app-variants-and-environment` - variants, ids per variant and `EXPO_PUBLIC_*` values.
- `in-app-purchases` - creating the store products behind the product ids.
- `git-commits-and-reporting` - commit bodies, trailers, tags and reports.
- `game-rules-engine` - (games plugin) the moves and events a game defines.
- `expo-project-structure` - (Expo's official skill) Expo's own folder conventions; where it differs
  on names (an `index.tsx` component root, `HomeScreen` route exports, `utils/`), this skill wins.
