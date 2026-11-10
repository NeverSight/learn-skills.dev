---
name: tdd-workflow
description: Drives changes test-first (TDD, red-green-refactor) - one behaviour per commit, test names, layer order, no test edited to pass. Use when writing or changing product code or deciding what to test. Not for Jest setup (unit-and-component-tests).
---

# Test-driven workflow

Every behaviour of an Expo app (iOS and Android) is built red-green-refactor: a failing test that
quotes the requirement, the least code that turns it green, a refactor, the fast gate, and one commit
holding test and code together. When an agent writes most of the code, the reviewer reads the report
first, so the tests are both the specification and the evidence; two scripts prove the tree and the
git history follow the rules.

## Rules that must hold

1. **No product code without a red test seen failing for the right reason.** Run it and read the
   failure: an assertion diff (`Expected ... Received ...`), never `Cannot find module`, a type or a
   syntax error. Why: a test that was never red proves nothing, and one written after the code asserts
   what the code does.
2. **Red and green in the same commit, one behaviour per commit.** Never commit a failing test. Why:
   the pre-commit hook reruns related tests, and only a history where test and code arrive together
   shows each behaviour was test-first (`code-without-test`).
3. **Never edit an existing assertion to make it pass.** Fix the code. Only a changed requirement may
   change an expectation, and that commit carries `Spec-Change: <requirement ID or issue> <what
   changed>` (git-commits-and-reporting owns the trailer format); a trailer that names no requirement
   reference (`TASKS-12`, `#41`, `issue 41`) does not count. "The test was wrong", "fix test" or
   "update snapshot" is never a Spec-Change. A rename refactor in its own `refactor` commit (the same
   literals and matchers, one consistent rename) is not an edit. Why: it is the likeliest way an
   unsupervised agent turns red into green (`assertion-changed`, `test-deleted`, `spec-change-reason`).
4. **Never skip, focus, retry or weaken:** no `.skip`, `.only`, `.failing`, `.todo`, `xit`, `fit`,
   `jest.retryTimes`, component snapshots, lowered thresholds, `eslint-disable` or `--no-verify`. If a
   gate looks wrong, stop and ask the developer. Why: a parked test rots, a retry hides a real bug, and
   nothing else would notice (`disabled-test`, `disabled-test-added`, `test-retry`).
5. **Quote the requirement in the first test** (title or comment above it:
   `it('returns today for a task due today (TASKS-12)')`), printed from the spec or the issue, never
   from memory; with no written requirement, write the one sentence in the plan and have the developer
   confirm it. Why: the quote ties the test to what was asked, and with `requirementIdPattern` in
   `contracts/tdd.json` check-test-edits fails a new feat/fix test that quotes none
   (`requirement-not-quoted`).
6. **Build in layer order:** pure logic -> persistence and migrations -> services behind ports with
   fakes -> stores and the model hook -> components and screens -> the route and its route test ->
   end-to-end flows -> screenshot matrix. Each layer is tested before anything depends on it. Why: a
   screen test that fails because a rule is wrong wastes the slice; a rule proven by properties never
   needs debugging through the UI.
7. **Pure logic gets examples, fast-check properties and at least one pinned exact value** in the same
   file, every limit at exactly its value and one past it. Why: on a seeded random-number generator,
   properties alone left 3 of 8 mutants alive; the pinned value killed them.
8. **Tests are deterministic:** no `Math.random`, `Date.now`, `new Date()`, `performance.now()`, real
   timers, network, locale or time zone; inject the fake clock and the seeded random-number generator.
   The one exception is a perf budget test (`test/**/<name>.perf.test.ts`) timing real work with
   `performance` from `node:perf_hooks`. Why: jest-expo mocks the global `performance.now`, and a test
   that reads the real world passes today and fails tomorrow (`test-nondeterminism`).
9. **Tests live where they run, named so they read as the requirement:** `<unit>.test.ts(x)` next to the
   unit under `src/`, `<unit>.android.test.ts(x)` for Android-only behaviour, `*.golden.test.ts` for
   goldens, Node-API tests under `test/`, never a test in the routes folder `src/app/`, never
   `__tests__/` or `.spec.ts`; `describe('<exported name>')`, `it('<third-person verb> ...')`, never
   `test(`. Why: the Jest projects select by suffix, so a stray name never runs; Expo Router bundles
   every file in `src/app/` as a route; the app program has no Node types (`test-file-name`,
   `test-in-routes`, `node-api-in-app-test`, `use-it`, `test-title-verb`, `describe-generic`).
10. **Every logic module ships with its test**, fakes included; only a thin native wrapper Jest cannot
    load starts with `// device-only: covered by <the e2e flow or device check>` in its first 6 lines.
    Why: an untested module is code no test can defend, and the same marker drives the coverage
    exclusion of unit-and-component-tests (`untested-module`, `device-only-reason`,
    `test-without-assertion`).
11. **Each kind of change carries its evidence** (`references/definition-of-done.md`): UI changes add
    component tests plus screenshots of each changed screen on the iOS simulator and the Android
    emulator, light and dark, LTR and RTL when the app ships an RTL locale, compared with the approved
    design baseline. Why: Jest has no layout engine, and a platform nobody looked at ships broken.

## Workflow

0. **Start from green** (once per session, from the repo root): `git status` and
   `git log --oneline -10` (never discard work you did not make; ask about it), note
   `git rev-parse --short HEAD` as the session's `<base>`, then `npm run -s check:fast`. If it is red,
   getting back to green is the first slice, and the report says what was broken.
1. **Find the requirement** the task serves (spec-traceability prints a spec entry exactly; otherwise
   the issue or acceptance criterion) and fill [assets/slice-plan.md](assets/slice-plan.md): behaviour
   in one sentence, first test title, files, evidence.
2. **Place the slice in the layer order** ([references/build-order.md](references/build-order.md)). If
   a lower layer it needs is untested, build that slice first.
3. **Write one failing test.** Copy [templates/logic.test.ts](templates/logic.test.ts) (pure logic) or
   [templates/component.test.tsx](templates/component.test.tsx) (a component, through
   unit-and-component-tests' `renderWithProviders`) next to the unit and replace every
   `__PLACEHOLDER__`, then run `npx prettier --write <test-file>` (filled placeholders make long lines,
   and `check:fast` starts with `prettier --check`). Names and places follow
   [references/test-conventions.md](references/test-conventions.md).
4. **Run it and read the failure:** `npx jest --ci <test-file>` (`--selectProjects android` after the
   path for an `.android.test.tsx`). If it fails on an import or a type, add a typed stub that returns
   a wrong value and rerun until the failure is an assertion diff
   ([references/tdd-loop.md](references/tdd-loop.md), "Red for the right reason"). Keep the red lines
   for the report.
5. **Write the minimum code** to turn that test green, rerun. Add the next example, see it red, make it
   green. For pure logic add the properties and the pinned value; turn any fast-check counterexample
   into an example test first.
6. **Refactor by responsibility** (split a module, extract a pure function with its own test); tests
   stay green.
7. **Run the fast gate and the tree check** from the repo root: `npm run -s check:fast`, then
   `node ${CLAUDE_SKILL_DIR}/scripts/check-tests.mjs .`. Fix every `FAIL` line and rerun until both
   pass. Where the app keeps logic outside the default folders, or has requirement IDs, copy
   [templates/contracts/tdd.json](templates/contracts/tdd.json) to `contracts/tdd.json` and edit it.
8. **Commit the slice** (test and code together, the requirement in the body; git-commits-and-reporting
   has the message format). Before committing,
   `node ${CLAUDE_SKILL_DIR}/scripts/check-test-edits.mjs . --staged --message <file>` checks the staged
   slice; after, `node ${CLAUDE_SKILL_DIR}/scripts/check-test-edits.mjs . --range <base>..HEAD` checks
   the history (`<base>` from step 0).
9. **Collect the evidence** the change kind needs from
   [references/definition-of-done.md](references/definition-of-done.md) and report it. Read
   [examples/slice-walkthrough.md](examples/slice-walkthrough.md) once to see a complete slice.

## Definition of done

- [ ] Every new behaviour has a test that was seen failing on an assertion before its code existed; the
      red lines are in the report.
- [ ] Each commit holds one behaviour with its tests and code together; no existing assertion changed
      without a valid `Spec-Change:` trailer naming the requirement.
- [ ] Pure logic has examples, properties and a pinned exact value; UI has component tests plus
      screenshots on both platforms (light/dark, LTR/RTL when shipped) compared with the approved
      baseline.
- [ ] `npm run -s check:fast` is green (and `npm run verify` before any push).
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-test-edits.mjs . --range <base>..HEAD` prints
      `RESULT: PASS`
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-tests.mjs .` prints `RESULT: PASS` (neither checker
      prints a SKIP line; both exit 2 when there is nothing to check)

## Anti-patterns

- **Writing the code, then a test that passes first time.** It asserts what the code does, not what
  the requirement says. Delete the code, watch the test fail, rewrite.
- **"Red" from a missing file.** `Cannot find module` is not a failing behaviour; stub the export with a
  wrong value and get an assertion diff.
- **Changing `toBe('today')` to `toBe('soon')` (or a row of an `it.each` table) because the code
  returns `'soon'`.** That is editing the test to pass; `check-test-edits.mjs` reports it as
  `assertion-changed`, and a `Spec-Change: the test was wrong` trailer adds `spec-change-reason`.
- **Parking a test with `.skip` "for later".** Finish the behaviour in the slice or delete the test.
- **A 40-line object literal in every test.** Use a `make<Thing>(overrides)` builder.
- **Snapshotting a component tree.** Assert roles, accessible names and visible text; snapshots belong
  only in `*.golden.test.ts`.
- **A test next to the route file in `src/app/`.** Expo Router bundles it as a route and `expo export`
  breaks; the route test lives in `src/features/<feature>/<feature>-navigation.test.tsx`.
- **`Platform.OS = 'android'` inside an iOS test.** It leaks into later tests; write
  `<unit>.android.test.tsx`.
- **Testing through the UI what a property already proves.** One level per behaviour; the flow proves
  the wiring, not the rule.
- **Several behaviours in one commit** ("add reminders, snooze and repeat"). The history can no longer
  show that each was test-first.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/tdd-loop.md](references/tdd-loop.md) | The loop, where the requirement comes from, red for the right reason, commands, discipline rules, examples + properties + pinned value, determinism, Android-only tests, counterexamples | Before the first slice of a session, and whenever a red run looks wrong |
| [references/test-conventions.md](references/test-conventions.md) | File names and places, titles, builders, banned test code, what not to test, snapshots, flaky-test policy, when multi-package | Workflow step 3, and when `check-tests.mjs` fails |
| [references/build-order.md](references/build-order.md) | The layer order, a feature slice by slice, first tests per layer, appendices for React Navigation 7 and the games plugin | Workflow step 2 |
| [references/definition-of-done.md](references/definition-of-done.md) | Always-true items, evidence by kind of change (both platforms), the test pyramid, coverage and mutation gates, where evidence files are | Workflow step 9, before calling work done |
| [templates/logic.test.ts](templates/logic.test.ts) | Test file for a pure unit: pinned example, rule table, determinism and invariant properties | Workflow step 3 for logic |
| [templates/component.test.tsx](templates/component.test.tsx) | Component test through `renderWithProviders`, by role and name, awaited presses, the accessibility audit line | Workflow step 3 for a component |
| [templates/contracts/tdd.json](templates/contracts/tdd.json) | The optional contract: logic globs, source globs, ignores, the requirement-ID pattern (filled with the defaults) | Workflow step 7, when the app's facts differ from the defaults |
| [templates/contracts/tdd.schema.json](templates/contracts/tdd.schema.json) | JSON Schema of the contract | With the contract |
| [assets/slice-plan.md](assets/slice-plan.md) | The plan for one slice (requirement, first test, files, layer, evidence, red run) | Workflow step 1 |
| `assets/template-placeholders.json` | The values the template check fills in (the Tasks app's digest planner and task row) | When changing a template |
| [examples/slice-walkthrough.md](examples/slice-walkthrough.md) | One complete slice (TASKS-12, task urgency) with the real red and green runs, the commit and both checkers | Once, to see the whole loop |
| `scripts/check-tests.mjs` | Checks the tree: disabled or retried tests, titles, snapshots, clock and randomness in tests, Node APIs in app tests, file names, tests in the routes folder, assertion-free files, untested logic modules, device-only reasons | Workflow step 7 and the definition of done |
| `scripts/check-test-edits.mjs` | Checks commits (`--range`, `--log`) or the staged slice (`--staged`): changed assertions or deleted tests without a valid Spec-Change, feat/fix code without a test (device-only, generated and types-only files exempt), newly disabled tests, Spec-Change reasons, unquoted requirements | Workflow step 8 and the definition of done |
| `scripts/lib/tdd-contract.mjs` | Shared by both checkers: the contract, its layout-derived defaults (single app or workspaces), test-file and source patterns | When changing a checker |
| `scripts/lib/git-fixture.mjs` | Builds throwaway git repositories with fixed dates for the self-test's `--range` and `--staged` cases | When changing the git suite |
| `scripts/lib/source-scan.mjs` | Shared import resolver (tsconfig aliases, workspace packages, platform files), synced from the library (do not edit here) | Never by hand |
| `scripts/selftest.mjs` | Proves both checkers pass good fixtures and catch each planted bug | After changing a checker |
| `scripts/check-lib.mjs` | Shared script helper, synced from the library (do not edit here) | Never by hand |
| `assets/requirement-ref.json` | The default requirement-reference pattern (`TASKS-12`, `#41`, `issue 41`, `spec 4.2`), synced from git-commits-and-reporting's `scripts/git/requirement-ref.json` so a Spec-Change its hook accepts passes here | Never by hand (synced) |
| `assets/shared.json` | Declares the shared files this skill copies in | When adding a shared file |
| `tests/fixtures/` | Good, pass, bad and error cases: the tree checker's overlay suite, history logs captured from real git, and the git-backed suite | When adding a rule to a checker |

## Related skills

- `unit-and-component-tests` - Jest projects, `renderWithProviders`, mocks, fakes, fast-check, coverage and Stryker set-up.
- `spec-traceability` - the requirement IDs each first test quotes.
- `golden-and-snapshot-tests` - data and pixel goldens and when `jest -u` is allowed.
- `e2e-maestro` - end-to-end flows on the simulator and the emulator.
- `design-visual-parity` - matching each changed screen to its approved baseline.
- `quality-gates` - what `check:fast` and `verify` run and how to fix a failing gate.
- `git-commits-and-reporting` - the commit message, the Spec-Change trailer and the evidence report.
- `react-native-conventions-index` - the order in which a whole app is built.
- `architecture-and-boundaries` - where a unit, a port and its fake live.
