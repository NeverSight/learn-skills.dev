---
name: react-native-conventions-index
description: Routes any React Native or Expo task to its skills - house rules, a task table, build orders for an app, a feature, a release. Use when starting or planning a task, or unsure which skill applies. Not for editing skills (skill-maintenance).
---

# React Native conventions index

The front door of the library. Every task starts here: find its rows in the task table, load every skill they name, build in the documented order, prove the work with each loaded skill's own checks, and report with that evidence. The tables are generated from the library catalogue and every skill's description, and a script proves the index lists exactly the skills that exist.

## Rules that must hold

1. **Load every skill of every matching row before writing code, the lead first.** A skill's rules and checks protect only work done with it loaded; loading just the most obvious skill is the most common way a task goes wrong (a hard-coded string, a screen never compared with its design, a write that bypasses the repository).
2. **Skills the developer names are binding.** A task that says "Skills: forms-and-input tdd-workflow" (or `/react-native:forms-and-input`) loads those first and holds their definitions of done; the row's other skills are added, never swapped for them.
3. **Code is test-first and every task ends in a report.** `tdd-workflow` joins every task that changes product code and `git-commits-and-reporting` every task that commits or reports (row rule `test-first`). Nobody may read the diff, so the tests and the report are the review.
4. **Every UI change carries its verification skills** (row rule `ui-verification`): a screen, component, state or form task also loads `i18n-strings-and-catalogs`, `rtl-and-direction`, `accessibility-as-code` and `design-visual-parity`, whether a UI skill leads the row or a screen skill joins it (a setting, a paywall, a game screen), so the change is checked in light and dark, LTR and RTL, at the largest text size, on iOS and Android, against its approved design.
5. **Build in the documented order** ([references/build-orders.md](references/build-orders.md)): a layer starts only when the layer under it passes its checks. Each step lists what it copies (tests included), merges, installs and generates: do exactly that, so tsc, lint and coverage stay green after every step. A file fetched by following a tsc error means the manifest is wrong, so report it.
6. **Done means every loaded skill's checks print `RESULT: PASS`,** plus `npm run -s check:fast` (and `npm run verify` before a push or pull request). `SKIP <file> [<rule>] not yet created (<skill> creates it)` lines and `NOT APPLICABLE: <fact>` count as a pass; exit 2 (nothing to check, bad input) never does. A verify gate the build order lists as red until a later step (`i18n:verify` before the catalogs) is not a failure of the current step: run the other gates one by one and name the pending one. A check that could not run is named in the report with the reason.
7. **When no row fits, never guess.** Read the intent map and load every skill whose "Use when" matches; a requirement ID in the task goes to `spec-traceability`, an error or a log to `troubleshooting-playbook`. Never infer a skill's content from its name.
8. **House defaults are stated once, in their owner skills**, and every task keeps them: one Expo app with a `src/` layout and the `@/` alias, ports with fakes and one composition root (`architecture-and-boundaries`); Expo Router (`navigation-and-routing`); typed results at boundaries (`error-handling-typed-results`); no secrets in the repo or the bundle (`app-variants-and-environment`, `privacy-and-store-declarations`); iOS and Android both, web opt-in (`web-support`); gates never weakened (`quality-gates`); versions from the verified stack (`dependency-management`); devices always named (`e2e-maestro`); stop and ask before anything outward-facing (`git-commits-and-reporting`).
9. **The index is generated and exact.** Never edit a generated part. After a skill is added, removed, renamed or re-described, or the catalogue changes, run `build-index.mjs --write`, then `check-index.mjs`; a stale index routes tasks to skills that are gone.

## The task table

The most common tasks. Several rows can apply: load the union. Every row, with its note, is in [references/task-matrix.md](references/task-matrix.md); the lead skill for any intent is in [references/intent-map.md](references/intent-map.md).

<!-- generated:task-table:start (build-index.mjs; edit assets/index.json instead) -->
| Task | Load these skills (the first one leads) |
|---|---|
| Bootstrap a new Expo app from an empty or docs-only repo | `expo-project-bootstrap` `dependency-management` `typescript-and-lint-rules` `quality-gates` `architecture-and-boundaries` `unit-and-component-tests` `git-commits-and-reporting` |
| Add a feature: a screen with its logic, data and route | `scaffold-feature-screen` `tdd-workflow` `screen-contracts` `react-components-and-hooks` `navigation-and-routing` `state-management-zustand` `i18n-strings-and-catalogs` `rtl-and-direction` `accessibility-as-code` `design-visual-parity` `unit-and-component-tests` |
| Build or change a screen, dialog or overlay | `screen-contracts` `ui-component-library` `ui-states-and-feedback` `design-system-structure` `react-components-and-hooks` `i18n-strings-and-catalogs` `rtl-and-direction` `accessibility-as-code` `design-visual-parity` `tdd-workflow` |
| Add or restyle a shared component | `ui-component-library` `design-system-structure` `accessibility-as-code` `react-components-and-hooks` `unit-and-component-tests` `i18n-strings-and-catalogs` `rtl-and-direction` `design-visual-parity` `tdd-workflow` |
| Change colours, fonts, dark mode or the theme | `design-system-structure` `accessibility-as-code` `design-visual-parity` `ui-component-library` `tdd-workflow` |
| Show loading, empty, failed or offline states, a toast, a confirm or Undo | `ui-states-and-feedback` `error-handling-typed-results` `motion-and-animation` `i18n-strings-and-catalogs` `rtl-and-direction` `accessibility-as-code` `design-visual-parity` `tdd-workflow` |
| Add a form, a text field or validation | `forms-and-input` `i18n-strings-and-catalogs` `rtl-and-direction` `accessibility-as-code` `design-visual-parity` `unit-and-component-tests` `tdd-workflow` |
| Animate a transition, sheet, loop, drag or celebration | `motion-and-animation` `accessibility-as-code` `performance-budgets` `react-components-and-hooks` `tdd-workflow` |
| Add or change visible text, a message key, a plural or a translation | `i18n-strings-and-catalogs` `rtl-and-direction` `naming-conventions` `accessibility-as-code` |
| Add a route, a link or a guard, or fix Back | `navigation-and-routing` `scaffold-feature-screen` `react-components-and-hooks` `deep-links-and-universal-links` `tdd-workflow` `i18n-strings-and-catalogs` `rtl-and-direction` `accessibility-as-code` `design-visual-parity` |
| Edit the root layout or the cold start, or fix a splash that hangs or flashes | `app-startup-and-bootstrap` `error-handling-typed-results` `persistence-and-migrations` `performance-budgets` `icons-app-icon-and-splash` `tdd-workflow` |
| Add a setting or a toggle, or fix one that is ignored or lost | `settings-and-preferences` `state-management-zustand` `persistence-and-migrations` `screen-contracts` `i18n-strings-and-catalogs` `design-visual-parity` `tdd-workflow` `rtl-and-direction` `accessibility-as-code` |
| Add a store, an action or a selector, or decide where state lives | `state-management-zustand` `react-components-and-hooks` `persistence-and-migrations` `unit-and-component-tests` `tdd-workflow` |
| Call an API, add a query or a mutation, or fix stale data | `networking-and-server-state` `error-handling-typed-results` `async-safety` `ui-states-and-feedback` `privacy-and-store-declarations` `tdd-workflow` |
| Add a table, a column or saved data, or leave AsyncStorage | `persistence-and-migrations` `state-management-zustand` `error-handling-typed-results` `golden-and-snapshot-tests` `tdd-workflow` |
| Write try/catch, .catch or a Result, or fix swallowed errors | `error-handling-typed-results` `async-safety` `crash-reporting-and-observability` `ui-states-and-feedback` `tdd-workflow` |
| Answer App Privacy or Data safety, or prove what the app sends | `privacy-and-store-declarations` `dependency-management` `admob-ads-and-consent` `analytics-and-consent` `crash-reporting-and-observability` `e2e-maestro` |
| Add, upgrade or remove an npm package | `dependency-management` `privacy-and-store-declarations` `performance-budgets` `quality-gates` `native-modules-and-new-architecture` |
| A quality gate, hook or verify run fails | `quality-gates` `troubleshooting-playbook` `typescript-and-lint-rules` `unit-and-component-tests` |
| Fix a TypeScript, ESLint or Prettier error, or split a file that is too long | `typescript-and-lint-rules` `naming-conventions` `architecture-and-boundaries` `quality-gates` |
| Place a new file, folder, port or adapter, or fix an import error | `architecture-and-boundaries` `naming-conventions` `typescript-and-lint-rules` `unit-and-component-tests` |
| Something errors, crashes, hangs or renders wrong | `troubleshooting-playbook` `quality-gates` `ios-simulator-build` `android-emulator-build` |
| Write a test or a mock, or Jest fails or flakes | `unit-and-component-tests` `tdd-workflow` `async-safety` `troubleshooting-playbook` |
| Prove a screen matches its approved design | `design-visual-parity` `ios-simulator-build` `android-emulator-build` `screen-contracts` `design-system-structure` `i18n-strings-and-catalogs` `rtl-and-direction` `accessibility-as-code` |
| Release to TestFlight | `ios-release-testflight` `eas-build-and-submit` `privacy-and-store-declarations` `e2e-maestro` `design-review-workflow` `git-commits-and-reporting` |
| Release to Google Play | `android-release-play` `eas-build-and-submit` `privacy-and-store-declarations` `e2e-maestro` `design-review-workflow` `git-commits-and-reporting` |
| Commit, tag, report, or ask the developer a question | `git-commits-and-reporting` `quality-gates` `spec-traceability` |
| Find out what the spec requires, or the task cites a requirement ID | `spec-traceability` `react-native-conventions-index` |
<!-- generated:task-table:end -->

## Workflow

1. **Match the task.** Find its rows here or in [references/task-matrix.md](references/task-matrix.md). A requirement ID (REQ-4, SCR-2) adds `spec-traceability` to quote it exactly; an error message adds `troubleshooting-playbook`, whose entry names the skill that prevents it. No row fits: read [references/intent-map.md](references/intent-map.md) and load every skill whose "Use when" matches part of the task; [references/skill-table.md](references/skill-table.md) has each skill's full description when two look alike.
2. **Load the skills,** the lead first, and read each one's Rules and Definition of done before starting. [references/loading-and-reporting.md](references/loading-and-reporting.md) says how: the Claude Code plugins (`react-native:<skill>`, `react-native-games:<skill>`), a standalone install, other agents through AGENTS.md, the developer's "Skills:" line, and what to do when a skill will not load.
3. **Place the work.** For a new app, a new feature, a release, an existing app or a new game, find the current step in [references/build-orders.md](references/build-orders.md); never start a step before its predecessor passes. Copy, merge and install what the step's manifest lists; the "When `npm run verify` is green" table says which verify gate may still be red. Run each step's "done when" commands as written: `node <skill folder>/scripts/<script>.mjs . <options>`, the repo root first, never `--root`. A `SKIP ... not yet created (<skill> creates it)` line is expected only until the step that creates the file.
4. **Do the work** as the lead skill's workflow says, test-first, with the other loaded skills' rules applied to the parts they own.
5. **Prove it.** Run every loaded skill's definition-of-done checks and `npm run -s check:fast`; fix every `FAIL` line and rerun until each prints `RESULT: PASS`.
6. **Report** as [references/loading-and-reporting.md](references/loading-and-reporting.md) ("Reporting") says: outcome first, the skills used, their `RESULT` lines copied, what was not verified, the human checks that do not block, at most one question with its default. `git-commits-and-reporting` owns the format and its checker.
7. **Keep the index exact** (only when skills or the catalogue changed). In the library repo, where `<catalogue>` is the library's catalogue file (the JSON its catalogue build reads): `node ${CLAUDE_SKILL_DIR}/scripts/build-index.mjs . --catalog <catalogue> --write`, then `node ${CLAUDE_SKILL_DIR}/scripts/check-index.mjs . --library --catalog <catalogue> --agents AGENTS.md --readme README.md`. In an app with installed skills: `node ${CLAUDE_SKILL_DIR}/scripts/check-index.mjs .` proves the installed skills and the index come from the same release. A build step that lists `installs` is checked against the companions in the dependency policy `contracts/dependency-policy.json` (dependency-management owns it; `--policy <file>` points elsewhere).

## Definition of done

- [ ] Every skill of the matching rows, and every skill the developer named, was loaded before the work started.
- [ ] Each loaded skill's definition-of-done checks print `RESULT: PASS` (SKIP lines and NOT APPLICABLE included; exit 2 is not a pass, and the report names any check that could not run and why), and `npm run -s check:fast` is green.
- [ ] Build work followed the build order; no step started before its predecessor passed.
- [ ] The report names the skills used, their `RESULT` lines and what was not verified.
- [ ] After any change to the skill set, a description or the catalogue, `build-index.mjs --write` ran (library) and nothing generated was edited by hand.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-index.mjs .` prints `RESULT: PASS`: in the library with `--library --catalog <catalogue> --agents AGENTS.md --readme README.md`, where it prints the notes `library mode: ...` and `step-import-closure: <n> copied files followed through 3 orders` and no SKIP line; in an app it prints `installed mode: ...`, or `NOT APPLICABLE: no skills folder ...` when no skill is installed (`build-index.mjs` in an app prints `NOT APPLICABLE: ... holds installed skills ...` and writes nothing).

## Anti-patterns

- **Loading one skill because its name matches.** "Build the task list screen" with only `screen-contracts` misses the texts, the mirroring, the screen reader names and the design comparison; load the whole row.
- **Starting a layer before the one under it is proven.** A screen built on an untested rule fails in the wrong place; the build order exists because a layer debugged through the layer above it costs many times more.
- **Declaring done from `check:fast` alone.** Each loaded skill has its own check for what lint and Jest cannot see (testIDs, copy keys, write order, design parity).
- **Reading exit 2 as "not applicable".** Exit 2 means the check found nothing to check or got bad input (often a guessed `--root`); rerun it with the command from the build order. Only `SKIP` lines and `NOT APPLICABLE` before `RESULT: PASS` mean a rule did not apply.
- **Editing a generated table by hand.** The next generation overwrites it and `check-index.mjs` reports it; change `assets/index.json`, the skill's description or the library catalogue, then regenerate.
- **Inventing a skill name** ("the audio skill", "/ads"). Use the exact names from the catalogue; a wrong name loads nothing.
- **Testing on one platform and calling it done.** A behaviour that differs on Android (back, permissions, channels, edge-to-edge) is proven there too, or the report lists it as not verified.
- **A report that lists work instead of outcome.** The reader may read only the first lines: what now works for the user, then the evidence.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/skill-table.md](references/skill-table.md) | Every skill with its description, by catalogue group (generated) | To see what a skill covers |
| [references/intent-map.md](references/intent-map.md) | One row per skill: its "Use when" and "Not for" clauses, the same map as the library's AGENTS.md (generated) | Workflow step 1 when no row fits |
| [references/task-matrix.md](references/task-matrix.md) | Every task row with its note, and the row rules (generated) | Workflow step 1 |
| [references/build-orders.md](references/build-orders.md) | Build orders: a new app, a new feature, a release, adopting the skills in an existing app, a new game; each step's skills and exact "done when" commands (generated) | Workflow step 3 |
| [references/loading-and-reporting.md](references/loading-and-reporting.md) | Loading skills in Claude Code and other agents, the "Skills:" line, compaction, reading check results, reporting, when to stop and ask | Workflow steps 2 and 6 |
| `assets/index.json` | The curated data: the catalogue snapshot (written from the library catalogue), category notes, task rows, row rules (`when` the lead, `whenAny` anywhere in the row), build orders with their manifests (`copies`, `installs`, `generates`, `noManifest`), `requireManifests` (the orders whose every step must keep one), the `verifyGreen` table and the closure settings | When a task pattern, a row rule or a build step changes |
| `scripts/build-index.mjs` | Renders every generated part from the data and each skill's frontmatter; `--catalog` syncs the catalogue snapshot; without `--write` it only reports | Workflow step 7 |
| `scripts/check-index.mjs` | Proves the index exact: library mode (coverage, row rules, generated parts, real scripts and flags, required and import-closed manifests, agreement with the catalogue, AGENTS.md and README.md) or installed mode (installed skills match the index's descriptions) | Workflow step 7 and the definition of done |
| `scripts/lib/index-model.mjs` | Frontmatter reader, skills-folder finder, data validation and the renderers | Never by hand |
| `scripts/lib/catalog-sync.mjs` | Reads the library catalogue and lists its differences from the snapshot | Never by hand |
| `scripts/lib/step-closure.mjs` | The build-order contract: finds each copied template by its line-1 repo path (a glob never takes an example) and plays an order step by step (imports, installs, catalog merges, tests, coverage) | Read it when a `step-import-closure` line is unclear |
| `scripts/selftest.mjs` | Proves both scripts pass a good mini library and catch each planted bug | After changing a script |
| `scripts/check-lib.mjs` | Shared script helper, synced from the library (do not edit here) | Never by hand |
| `assets/shared.json` | Declares the shared files this skill copies in | When adding a shared file |
| `tests/bases/` | The mini library every case starts from: an index skill, two skills with templates, a catalogue file, AGENTS.md and README.md | When a fixture needs a new base file |
| `tests/fixtures/` | Overlay cases (`mutation.json`, `EXPECT.txt`, `ARGS.txt`) over that library, for both scripts | When adding a rule |

## Related skills

- `skill-maintenance` - adding or changing a skill (then regenerate this index).
- `tdd-workflow` - the test-first loop every code task follows; owns the layer order inside a feature.
- `git-commits-and-reporting` - commit messages, the report format and stop-and-ask messages.
- `spec-traceability` - what the app must do: requirement IDs quoted exactly.
- `troubleshooting-playbook` - a failure or an error message: its entry names the owning skill.
- `quality-gates` - `check:fast`, `verify` and the hooks every task ends with.
- `expo-project-bootstrap` - the first step of a new app.
