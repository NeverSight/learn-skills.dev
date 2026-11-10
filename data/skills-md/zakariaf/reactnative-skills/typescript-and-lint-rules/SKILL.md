---
name: typescript-and-lint-rules
description: Enforces strict tsconfig, ESLint flat config, size limits, forbidden patterns, TSDoc. Use when writing or splitting .ts/.tsx or fixing tsc, ESLint or Prettier errors. Not for import zones (architecture-and-boundaries).
---

# TypeScript and lint rules

Every `.ts`/`.tsx` file of the app compiles under one strict tsconfig set and passes one ESLint config
with no warnings, no inline disables and hard size limits; Prettier formats and knip finds dead code.
Style is enforced by machines or it does not exist. This skill holds those configs, the limits table,
the forbidden patterns, the TSDoc contract, and two checkers that prove the repo still follows them.

## Rules that must hold

1. **Never silence a gate.** No `eslint-disable`, `@ts-ignore` or `@ts-nocheck`; `@ts-expect-error`
   only where a third-party type is wrong, with a reason of 10+ characters. Why: silencing a check is
   the likeliest failure of an unsupervised agent, and inline config is switched off anyway.
2. **One strict `tsconfig.base.json`.** It extends `expo/tsconfig.base` and holds every compiler
   option and no other (no member of `strict` set to `false`); each program tsconfig sets only
   `types`, `paths`, `tsBuildInfoFile`, `include` and `exclude`, never `lib` (the Expo base gives DOM +
   ESNext). Why: one set of guarantees for all code; no program quietly drops `strict`.
3. **Two programs, two worlds.** `src/tsconfig.json` is the app (types `jest`, no Node); the root
   `tsconfig.json` checks the whole repo with Node types. App code never imports a Node-world file
   (`app.config.ts`, `plugins/`, `scripts/`, `node:*`), not even with `import type`; `expo-env.d.ts`
   never enters a program; `src/app-env.d.ts` stays out of the root program; the app program excludes
   nothing; both programs resolve `@/*` and `@test/*` to the same folders. Why: a type-only import
   still pulls the file into the app program and Node code into the bundle.
4. **One ESLint config, errors only, all app code in scope.** `eslint.config.mjs` at the root is the
   only config; every rule is an error, lint runs as `eslint . --max-warnings 0` and only through the
   npm scripts. No ignore list (`PRE_EXISTING`, `.prettierignore`, the root `exclude`) reaches app
   code. The canonical blocks, file groups and shared lists stay as the template ships them; an
   exception is a new block that names exact files and rebuilds the rule from the shared lists, with a
   reason comment and a `Gate-Change:` trailer. Why: a later flat-config block replaces a rule's
   options, it does not merge, so a fresh short list, a widened group or a folder-wide block silently
   drops every other ban, however it is spelled.
5. **Stay inside the limits.** 250 code lines per file (400 in tests), 40 per `.ts` function, 80 per
   `.tsx` component, cyclomatic complexity 10 (`modified`), cognitive 15, nesting 3, 3 parameters
   (function types too), 3 nested callbacks (4 in tests), JSX depth 5, one component and one class per
   file, a string literal at most twice (the third use gets a name). Why: a small unit is read whole
   and fails in one place.
6. **When a limit trips, split by responsibility.** Extract named pure functions, a lookup table, an
   options object or a sub-component with its own test. Never join lines, never `part-2.ts`, never
   move logic into JSON; large static data does go in `.json`. Why: the limit detects a symptom;
   gaming it keeps the problem.
7. **Erasable TypeScript only.** No `enum` (an `as const` array and a union), no `namespace`, no
   constructor parameter properties, `type` instead of `interface` (merging in `*.d.ts` aside), no
   `any`, no non-null `!` outside tests. Why: `erasableSyntaxOnly` keeps every file runnable by Node
   type stripping and single-file transforms, and unions work with exhaustive switches.
8. **Named exports, one alias, no parent imports.** `export default` only where a tool reads it:
   Expo Router route files in `src/app/`, `app.config.ts`, config plugins, `__mocks__`, `jest.setup.ts`. Import a
   sibling as `./x` and any other folder as `@/…`; Node-run files (`app.config.ts`, `plugins/`,
   `scripts/`) write the extension (`./x.ts`) and may use `../`. When multi-package, every import
   writes its extension. Why: greppable names and paths that survive moves; Node type stripping
   resolves no extensionless import.
9. **Errors are values or loud.** An expected failure returns a `Result` with a `kind` union (the type
   is `src/core/result.ts`, owned by error-handling-typed-results); throw only `Error` objects with
   `{ cause }`, for programmer errors; every `catch` maps, records through the error-reporting port
   with a fallback, or rethrows. Why: callers must handle every case, and nothing fails silently.
10. **No floating promises; handlers stay synchronous and return nothing.** Await, return, or end
    with `.catch(reportError)`; `void promise` does not count. A `handleX` function or inline `on*`
    handler is never `async` and has a block body that returns nothing, and `handleSubmit(onValid)` is
    never passed straight to an `on*` prop. Why: React Native's Strict TypeScript API types `onPress`
    as returning `unknown`, so `no-misused-promises` misses an async or promise-returning handler
    (`onPress={() => Linking.openURL(url)}`) and its rejection vanishes; in a block body
    `no-floating-promises` sees the promise. A promise-returning function passed by reference
    (`onPress={retry}`) passes every lint rule; async-safety's checker (rule `async-by-reference`)
    catches it.
11. **Immutable data, injected time and randomness.** `readonly` types and `as const` tables, new
    objects instead of mutation; `Date.now`, `new Date()`, `performance.now` and `Math.random` only
    behind the clock and random ports; deterministic code (`src/core/rng`, `src/core/dates`,
    `*-generator.ts` modules, game rules) uses integer-safe math and never reads the device locale
    (`localeCompare`, `Intl`, `toLocale*`). Why: wall-clock code cannot be tested, and seeded output
    must match on every device (Hermes uses the platform libm and ICU data, V8 in Jest its own).
12. **Prettier formats, knip prunes, pins hold.** Prettier is the only formatter
    (`eslint-config-prettier` last, never `eslint-plugin-prettier`); every knip rule is `error`;
    TypeScript, ESLint and its plugins, Prettier and knip stay on the verified exact pins. A limit, pin
    or baseline change is a stop-and-ask decision. Why: one formatter, no dead code, reproducible lint.
13. **Comments say why; contracts get TSDoc.** Every exported function or class in `src/core/` and
    every exported `*Port` type has a one-sentence `/** … */` stating its contract; no
    `TODO`/`FIXME`/`HACK`, no commented-out code. Why: summaries are read before bodies, and nothing
    comes back to a TODO.

## Workflow

1. Pick the task: set up or change configs (step 2), write code (step 3), fix a `tsc` or lint error
   (step 4), or add an exception (step 5). Always finish with step 6.
2. **Configs.** Read [references/tsconfig-set.md](references/tsconfig-set.md) and
   [references/eslint-config-guide.md](references/eslint-config-guide.md). Copy each template to its
   destination (table below), list each pre-existing top-level folder in three places
   (`PRE_EXISTING`, `.prettierignore` and the root `tsconfig.json` `exclude`), install the pinned
   versions and the `overrides` block with the guide's commands, then run
   `node ${CLAUDE_SKILL_DIR}/scripts/check-configs.mjs .`. A folder holding code the app imports (an
   older template's `components/` or `hooks/`) is not pre-existing: move it under `src/` or declare it
   in `rn-skills.config.json` `"layoutEntries"`.
3. **Code.** Before error handling, async code, a service or a new module, read the matching section
   of [references/code-policies.md](references/code-policies.md). Imitate
   [examples/parse-task-id-param.ts](examples/parse-task-id-param.ts) (a Result),
   [examples/with-timeout.ts](examples/with-timeout.ts) (a timeout as a value; a synced copy of
   async-safety's template) and
   [examples/use-task-editor-model.ts](examples/use-task-editor-model.ts) (a synchronous handler).
   Keep every unit inside the limits from the start.
4. **Errors.** Find the rule in [references/forbidden-patterns.md](references/forbidden-patterns.md)
   and write the replacement it names. For a limit, read
   [references/limits-and-splitting.md](references/limits-and-splitting.md) and follow
   [examples/splitting-a-long-function.md](examples/splitting-a-long-function.md). Never edit the
   config to make an error go away.
5. **Exception.** Only for a tool or library contract. Follow "Adding an exception, step by step" in
   [references/eslint-config-guide.md](references/eslint-config-guide.md): a file-exact block rebuilt
   from the shared lists, a reason comment, `--print-config` proof, the quality-gates guardrail still
   green, a `Gate-Change:` trailer. A limit or baseline change: stop and ask the developer.
6. **Check.** From the repo root, once `node_modules` exist: `npm run typecheck`, `npm run lint`,
   `npm run format:check`, `npm run check:unused` (before quality-gates adds the scripts:
   `npx tsc --noEmit -p tsconfig.json && npx tsc --noEmit -p src/tsconfig.json`,
   `npx eslint . --max-warnings 0`, `npx prettier --check .`, `npx knip`). Always:
   `node ${CLAUDE_SKILL_DIR}/scripts/check-source.mjs .` and
   `node ${CLAUDE_SKILL_DIR}/scripts/check-configs.mjs .`. Fix every `FAIL` line (each names the file,
   the rule and the fix) and rerun until all print `RESULT: PASS`.

The templates are the verified canonical files; expo-project-bootstrap writes the same bytes when it
creates an app. Fill one thing when the repo has top-level folders or files that predate the app
(`handbook/`): add one line each at the end of `.prettierignore` (`handbook/`), the same entries to
`PRE_EXISTING` in `eslint.config.mjs` (`'handbook/**'`) and to the root `tsconfig.json` `exclude`
(`"handbook"`: its `**/*.ts` include would otherwise type-check them). With none, the files stay as
shipped. A tool config the app uses (`tailwind.config.js`) is app code, not pre-existing: declare it
in `rn-skills.config.json` `"layoutEntries"` when `check-configs` asks. `design/` (the design tokens)
is app layout; pre-existing exports inside it get their own `.prettierignore` line (`design/exports/`).

| Template | Destination in the app repo |
|---|---|
| `templates/tsconfig.base.json` | `tsconfig.base.json` |
| `templates/tsconfig.json` | `tsconfig.json` (root program: Node and tests) |
| `templates/src/tsconfig.json` | `src/tsconfig.json` (app program) |
| `templates/src/app-env.d.ts` | `src/app-env.d.ts` |
| `templates/eslint.config.mjs` | `eslint.config.mjs` |
| `templates/dot-prettierrc.json`, `templates/dot-prettierignore` | `.prettierrc.json`, `.prettierignore` |
| `templates/knip.json` | `knip.json`, with quality-gates' `templates/contracts/knip-ignores.json` at `contracts/knip-ignores.json` (the reasons for its ten `ignore` entries; its `knip-ignores` rule fails without them) |

When multi-package, read the "When multi-package" sections of both config references first; one
`.prettierignore` line per generated native folder (`apps/*/ios/`, `apps/*/android/`) is required.

## Definition of done

- [ ] `npm run typecheck` passes for both programs (`tsc --noEmit -p tsconfig.json` and `-p src/tsconfig.json`).
- [ ] `npm run lint` passes with `--max-warnings 0`; `npm run format:check` and `npm run check:unused` pass.
- [ ] No new `eslint-disable`, `@ts-ignore` or `@ts-nocheck`; any `@ts-expect-error` names its third-party cause.
- [ ] No file over 250 code lines (400 for tests), no function over 40 (80 for a component); every split followed a responsibility.
- [ ] Every new exported function in `src/core/` and every port type has a one-sentence TSDoc summary; no TODOs, no commented-out code.
- [ ] Every expected failure is a `Result` with a `kind` union; every `catch` maps, records or rethrows with `cause`; no floating promise; every handler is synchronous with a block body.
- [ ] Any config exception is a named, commented, file-exact block, committed with a `Gate-Change:` trailer.
- [ ] Every pre-existing top-level folder is in `PRE_EXISTING`, `.prettierignore` and the root `tsconfig.json` `exclude`, and no entry of those lists reaches app code; `package.json` pins the tools exactly and its `overrides` hold the ten `@typescript-eslint/*` packages.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-configs.mjs .` prints `RESULT: PASS` (neither checker prints SKIP lines: every file they read is this skill's own)
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-source.mjs .` prints `RESULT: PASS`

## Anti-patterns

- **`eslint-disable` or `@ts-ignore` "just this once".** Inline config is inert and reported; the
  error is still there. Fix the code, or add a file-exact exception block for a real tool contract.
- **Raising a limit or turning a rule off in a later block.** `check-configs` reports
  `eslint-limit-changed` in every shape ESLint accepts (`['error', 6]`, `['error', { max: 6 }]`, a bare
  `'error'` that falls back to ESLint's default), any extra declaration of a limit rule, and
  `eslint-rule-off`. Split the code; a limit change is the developer's call.
- **Ignoring app code to get to green.** `PRE_EXISTING: ['src/features/**']`, a `.prettierignore` line,
  an `exclude` entry, `eslint src` or `--ignore-pattern` take app code out of the gates while every
  tool stays quiet; `check-configs` reports `ignore-app-code` and `lint-script`, and `check-source`
  checks those files anyway. Fix the code.
- **A fresh short list, a widened group or a new folder-wide block.** `'no-restricted-imports':
  ['error', { paths: [x] }]`, `RESTRICTED_PROPERTIES.filter(...)` or `'src/**/*-screen.tsx'` added to
  `TESTS` drops bans for whole folders while ESLint stays green. `check-configs` compares the config
  with the template: a changed canonical block (`[canonical-block]`), a block beyond them that reaches
  more than named files (`[exemption-scope]`), a file group that loses a glob or gains a folder
  (`[file-group]`), an edited shared list (`[canonical-const]`), plus `[fresh-list]` and
  `[option-redeclared]`. Name the one file and rebuild from `RUNTIME_PATHS` with `without(...)`.
- **Compressing code to get under a limit.** Joined lines and nested ternaries read worse and trip
  `no-nested-ternary`. Extract named functions or a lookup table.
- **`import type` from `app.config.ts` or `scripts/` into `src/`.** It drags the Node world into the
  app program. Put the shared type in a neutral file under `src/` and import it from both sides.
- **`onPress={async () => ...}`, `onPress={() => Linking.openURL(url)}` or
  `onPress={handleSubmit(onValid)}` because it type-checks.** The Strict API hides the rejection (and
  `openURL` rejects when no app handles the URL), and react-hook-form rethrows what `onValid` throws.
  Keep the handler synchronous with a block body:
  `onPress={() => { handleSubmit(onValid)().catch(reportError); }}`.
- **Throwing for bad outside input.** Callers forget to catch. Return a `Result` with a `kind` union.
- **Rewording a `RESTRICTED_PROPERTIES` message or reformatting an option list.** The quality-gates
  guardrail compares resolved values verbatim, and `check-configs` pins the canonical messages.
- **`noUnusedLocals` in tsconfig.** Two reporters disagree about `_`-prefixed parameters; ESLint's
  `no-unused-vars` is the one reporter.
- **Declaring "the checkers pass" without ESLint and tsc.** The scripts mirror the rules most often
  broken and run before `node_modules` exist; `npm run lint` and `npm run typecheck` are the full gate.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/tsconfig-set.md](references/tsconfig-set.md) | The two programs, every compiler option, `app-env.d.ts`, typed routes, `expo-env.d.ts`, Node-run code, when multi-package | Workflow step 2; a missing global or a file in the wrong program |
| [references/eslint-config-guide.md](references/eslint-config-guide.md) | Versions and install, the blocks, file groups, shared lists, exemptions, adding an exception, Prettier, knip, troubleshooting, when multi-package | Workflow steps 2 and 5; an unclear lint message |
| [references/limits-and-splitting.md](references/limits-and-splitting.md) | The limits table with rationale, how lines are counted, the move for each tripped limit | Workflow step 4 for a limit; before a large module |
| [references/forbidden-patterns.md](references/forbidden-patterns.md) | Every rejected pattern, why, which rule, and what to write instead | Workflow step 4 |
| [references/code-policies.md](references/code-policies.md) | Comments and TSDoc, errors, async, immutability, dependency injection, imports | Workflow step 3 |
| `templates/tsconfig.base.json` | The strict compiler options every program extends | Workflow step 2 |
| `templates/tsconfig.json` | Root program: the whole repo with `jest` and `node` types, the aliases | Workflow step 2 |
| `templates/src/tsconfig.json` | App program: `jest` types only, typed routes, the same aliases | Workflow step 2 |
| `templates/src/app-env.d.ts` | `process` for `EXPO_PUBLIC_*` dot access in the app program | Workflow step 2 |
| `templates/eslint.config.mjs` | The complete, verified ESLint 9 flat config | Workflow steps 2 and 5 |
| `templates/dot-prettierrc.json` | Prettier options (copy to `.prettierrc.json`) | Workflow step 2 |
| `templates/dot-prettierignore` | Prettier ignore list; pre-existing top-level entries go at its end (copy to `.prettierignore`) | Workflow step 2 |
| `templates/knip.json` | knip entry points, the agent-folder `ignore` list and every rule at `error` | Workflow step 2 |
| [examples/parse-task-id-param.ts](examples/parse-task-id-param.ts) | A route parameter parsed into a `Result` instead of a throw | Workflow step 3 |
| [examples/parse-task-id-param.test.ts](examples/parse-task-id-param.test.ts) | Its test: success and each expected failure | Workflow step 3 |
| [examples/with-timeout.ts](examples/with-timeout.ts) | A timeout and a cancel as expected failures, with the abandoned task aborted (synced from async-safety, which owns `src/services/async/with-timeout.ts`) | Workflow step 3 (async adapters) |
| [examples/with-timeout.test.ts](examples/with-timeout.test.ts) | Fake-timer tests for it (synced from async-safety) | Workflow step 3 |
| [examples/use-report-error.ts](examples/use-report-error.ts) | The rejection handler for fire-and-forget work | Workflow step 3 (handlers) |
| [examples/use-task-editor-model.ts](examples/use-task-editor-model.ts) | A model hook whose synchronous handler starts async work | Workflow step 3 (handlers) |
| [examples/splitting-a-long-function.md](examples/splitting-a-long-function.md) | A 44-line, complexity-12 function, its four lint errors, and the split | Workflow step 4 for a limit |
| [examples/score-day.ts](examples/score-day.ts) | The split result: options object, lookup tables, named steps | Workflow step 4 |
| [examples/score-day.test.ts](examples/score-day.test.ts) | Tests for each extracted piece | Workflow step 4 |
| [examples/rn-skills.config.example.json](examples/rn-skills.config.example.json) | The optional repo keys both checkers read | When the app's layout differs from the default |
| `scripts/check-configs.mjs` | Checks the tsconfig set, the ESLint config against `templates/eslint.config.mjs` (canonical blocks, file groups, shared lists, extra blocks name exact files, limits in any shape, fresh lists, re-declared options), Prettier and its ignore list, pre-existing folders in all three lists, ignore lists that reach app code, knip, pins, `overrides`, lint scripts and stray configs against the baseline | Workflow steps 2, 5 and 6 |
| `scripts/check-source.mjs` | Checks every `.ts`/`.tsx` for silenced gates, limits, non-erasable syntax, exports, imports, the two worlds, handlers, errors and TSDoc | Workflow step 6 |
| `scripts/selftest.mjs` | Proves both checkers pass the good fixtures and catch every planted bug | After changing a checker, the baseline or a template |
| `scripts/check-lib.mjs` | Shared script helper (synced; never edit here) | Never by hand |
| `scripts/lib/source-scan.mjs` | Dependency-free lexer and import resolver (synced) | Only when changing a checker |
| `scripts/lib/workspaces.mjs` | Workspace and Expo-app detection for the multi-package checks (synced) | Only when changing a checker |
| `scripts/lib/app-scope.mjs` | Which repo paths are app code and whether an ignore entry reaches them (this skill's own helper, used by both checkers) | Only when changing a checker |
| `scripts/lib/eslint-structure.mjs` | Reads an `eslint.config.mjs` without running it: consts, blocks, the files each block reaches (this skill's own helper) | Only when changing check-configs |
| `assets/ts-lint-baseline.json` | The canonical compiler options, programs, required ESLint settings, limits, pins, knip rules | When a verified setting changes (stop and ask) |
| `assets/shared.json` | The shared files this skill copies in | When adding a shared file |
| `tests/` | Overlay fixtures: `tests/bases/configs-app` plus the templates for check-configs, `good/` for check-source | When adding a rule to a checker |

## Related skills

- `naming-conventions` - file, identifier, route, testID and key names (the naming rules inside this config), and the path header (line 1 names the repo path).
- `architecture-and-boundaries` - where code goes, the import zones, ports and the composition root.
- `error-handling-typed-results` - the `Result` type and failure design that rule 9 relies on.
- `quality-gates` - the npm scripts, `lefthook.yml` hooks and the config guardrail that run these checks.
- `react-components-and-hooks` - the UI lint rules (primitives, memo, selectors) in depth.
- `unit-and-component-tests` - the Jest and Testing Library rules and the tests that go with a split.
- `i18n-strings-and-catalogs` and `rtl-and-direction` - the literal-string and logical-style rules.
- `seeded-determinism-and-golden-vectors` - the deterministic folders and their integer-safe math.
- `dependency-management` - installing, pinning and the release-age policy for these tools.
- `expo-project-bootstrap` - creates a new app with these files already in place.
