---
name: quality-gates
description: Installs and repairs quality gates (check:fast, verify, lefthook, Claude Code hooks, the guardrail) without weakening them. Use when a gate, hook or verify fails or a gate file changes. Not for a lint error (typescript-and-lint-rules).
---

# Quality gates

When an agent writes most of the code, the gates are the reviewer: a hook after every edit,
`check:fast` before the agent stops, lefthook on every commit and push, and `npm run verify`, whose
guardrail compares every resolved tool config with `quality-gates.json`. This skill installs those
gates from tested templates, fixes failures the right way, and proves with two checkers that no gate
is missing, weakened or bypassed.

## Rules that must hold

1. **When a gate fails, fix the code, never the gate.** No lowered threshold, raised limit, wider
   exemption glob (a `!` entry in `collectCoverageFrom`, an ignored test path), `eslint-disable`, `@ts-ignore`, `.skip`, `jest.retryTimes`, istanbul or Stryker
   ignore comment. *Why:* quietly relaxing a check to get green is the likeliest failure of an
   unsupervised agent, and nothing else would notice.
2. **Never bypass a hook:** no `--no-verify`, `git commit -n`, `LEFTHOOK=0`, `LEFTHOOK_EXCLUDE`,
   `lefthook uninstall`, `core.hooksPath`, no `skip:`, `only:` or `exclude_tags:` in `lefthook.yml` or
   in a local `lefthook-local.yml` (usually git-ignored), no `disableAllHooks`, no `|| true` on a hook. *Why:* the hooks are the reviewer; a
   local override is invisible to everyone else, which is why the guardrail reads the merged config.
3. **A gate changes only with the developer's agreement,** in one commit that changes the gate and
   `quality-gates.json` together, with a `Gate-Change: <reason>` trailer (git-commits-and-reporting
   owns the trailer format). If a gate looks wrong, stop and send the note in
   `assets/gate-question.md`; never edit `quality-gates.json` to match a weakened config. *Why:* the
   guardrail and `git log --grep Gate-Change` only mean something if every change goes through them.
4. **Use the canonical npm scripts byte for byte** (`templates/package-scripts.json`; `start`,
   `android`, `ios` and `web` stay the app's own). *Why:* the guardrail compares the gate scripts
   exactly, and a weaker copy in a hook or CI would bypass it.
5. **Run `npm run -s check:fast` before saying a change is done, and `npm run verify` before every
   push** (the pre-push hook runs it). *Why:* `check:fast` closes the inner loop in seconds; `verify`
   is the only run that holds every gate.
6. **`verify` is one strict pipeline, cheapest first, stopping at the first failure.** Every step
   runs strict; a skill that adds a gate appends its npm script to `verifyExtraSteps` in
   `quality-gates.json`, and `test:sim` joins once a simulation exists. Never stub a target, add
   `--passWithNoTests` or drop a step to get green. *Why:* a step that can skip quietly is a gate
   that is already gone.
7. **Hooks that must reach the agent exit 2 and write to stderr.** *Why:* any other exit is a
   non-blocking error: the agent never sees it, and the user sees only a one-line notice.
8. **Start the agent at the repository root, and merge `.claude/settings.json`, never replace it.**
   *Why:* hooks and permissions load only from the folder the session starts in, and the file holds
   keys the gates do not own (plugins, skill permissions).
9. **Pin every dependency exactly, keep the 7-day release age, review install scripts before they
   run, ship only allowed licences;** each exception is a dated, agreed entry (dependency-management
   owns the procedure, `verify` enforces it). *Why:* the supply chain is code the reviewer never
   reads.
10. **When a size or complexity limit trips, split by responsibility,** never by line count, never
    by compressing code or moving logic into JSON (the limits table is typescript-and-lint-rules').
    *Why:* the limit detects a symptom; gaming it keeps the problem.
11. **Every ignore entry in `knip.json` has a written reason in `contracts/knip-ignores.json`.**
    *Why:* knip takes no comments, and an ignore entry silences it for good.
12. **No gate reaches into installed agent skills through a wildcard:** `gated-paths.ts` keeps
    `**/` patterns out of `skills/`, `.agents/`, `.claude/` and the other agent folders, the `ask`
    rules are anchored at the repo root, and `knip.json` `ignore`s the ten agent folders. *Why:*
    installed skills hold tsconfigs, snapshots, vectors and imports of uninstalled packages on
    purpose; they must not demand a trailer or a prompt, or fail `check:unused`.
13. **`SKIP` lines and `NOT APPLICABLE` count as a pass; exit 2 never does.** A checker prints
    `SKIP <file> [<rule>] not yet created (<skill> creates it)` for a gate file another skill has not
    created yet. *Why:* exit 2 means a bad command or nothing to check: fix the command, never read
    it as not applicable.

## Workflow

1. **Know the gates.** Read [references/gates-overview.md](references/gates-overview.md): what runs
   when, every canonical script and its owner, and the order and cost of `verify`.
2. **Install or repair them** (a new app, or `check-gate-wiring.mjs` reports a missing or changed
   file). In an existing app adopt the owners first ("Adopting into an existing app" in the
   overview), then copy from this skill and read
   [references/hooks-and-settings.md](references/hooks-and-settings.md):

   | From this skill | Goes to |
   |---|---|
   | `templates/package-scripts.json` | the `scripts` of the root `package.json` (merge; keep `start`, `android`, `ios`, `web`) |
   | `templates/lefthook.yml`, `templates/quality-gates.json` | the repo root |
   | `assets/claude-settings.json` | `.claude/settings.json` (merge: keep existing keys, add every deny and ask rule and both hooks) |
   | `templates/scripts/quality/`, `templates/scripts/hooks/` | the same paths (guardrail, verify plan and runner, gated paths, edit hook, tests) |
   | `templates/contracts/knip-ignores.json` (+ schema) | `contracts/` |
   | `templates/knip.json`, `templates/dot-gitignore`, `templates/dot-npmrc`, `templates/scripts/quality/device-only.ts` | only when their owner skill has not written them (synced copies of typescript-and-lint-rules', dependency-management's and unit-and-component-tests' files) |

   If an existing app's `knip.json` lacks the `"ignore"` list for the ten agent folders (the canonical
   copy in `templates/knip.json` has it), add it in the same change, each entry with its reason from
   `templates/contracts/knip-ignores.json` (rule 12).
   Then `npm run prepare` (runs `lefthook install` when the app folder is the git top level, else
   prints why it skipped) and `npx lefthook validate` (prints `All good`). The commit-msg job
   runs git-commits-and-reporting's `scripts/git/check-commit-message.ts`: install that skill's check
   in the same change, or every commit fails with `Cannot find module` (loud, and correct).
3. **Prove the wiring.** `node scripts/quality/check-quality-gates.ts` prints
   `quality-gates: all resolved configs match quality-gates.json`; then
   `node ${CLAUDE_SKILL_DIR}/scripts/check-gate-wiring.mjs .` (the repo root is the positional
   argument, never `--root`) and `npm run -s check:fast`.
4. **When a gate fails,** read [references/fixing-failures.md](references/fixing-failures.md): the
   fix for each failure and the never list. Fix, rerun the step, rerun `npm run -s check:fast`.
5. **When a gate itself looks wrong,** follow "Changing a gate" in
   [references/guardrail.md](references/guardrail.md): stop, send `assets/gate-question.md` to the
   developer, change nothing until they agree.
6. **When a skill adds a gate** (a verify step, a gated path, a knip ignore, a budget), read
   [references/root-files.md](references/root-files.md): `verifyExtraSteps`, `gatedPaths`, the knip
   reasons contract, and what `check-gate-wiring.mjs` compares.
7. **For a dependency, install-script, licence, knip or CI question,** read
   [references/supply-chain.md](references/supply-chain.md).
8. **Before calling the work done,** run `npm run -s check:fast`, then both checkers from the repo
   root. Fix every `FAIL` line (each names the file, the rule and the fix) and rerun until both print
   `RESULT: PASS`. Before a push, `npm run verify` must be green.

**When multi-package** (npm workspaces): `typecheck` takes the workspace form in
`assets/package-scripts.multi-package.json` (each workspace keeps its own `typecheck` script),
`quality-gates.json` lists each program under `typescript.projects` (a glob such as
`apps/*/tsconfig.json` covers new ones), knip gets one `workspaces` entry per package, and the one
root `jest.config.js` writes its test roots, coverage glob and logic keys in workspace form
(`<rootDir>/apps/*/src/**/`, `./packages/core/src/`), restated in `quality-gates.json` `jest` in the
same gate change. The gate files stay at the repo root; `check-gate-wiring.mjs` reads the workspaces
from `package.json` and compares the Jest scope with the canonical one, workspace prefixes stripped.

## Definition of done

- [ ] `npm run -s check:fast` is green; before any push `npm run verify` ends with
      `verify: <n> steps passed (...)`.
- [ ] The guardrail prints `quality-gates: all resolved configs match quality-gates.json`, and
      `npx lefthook validate` prints `All good`.
- [ ] No gate changed without the developer's agreement and a `Gate-Change:` trailer; no hook was
      bypassed, and no `lefthook-local.yml` or `.claude/settings.local.json` switches one off.
- [ ] `.claude/settings.json` still holds its other keys plus every deny and ask rule and both hooks.
- [ ] Every `knip.json` ignore entry has its reason in `contracts/knip-ignores.json`, and `knip.json`
      ignores every agent folder that holds code (`.claude/skills/`, `.agents/skills/`, ...).
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-bypasses.mjs .` prints `RESULT: PASS`.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-gate-wiring.mjs .` prints `RESULT: PASS` with no SKIP
      line once every owner has run (the reference app does). Only in an app adopted step by step,
      each until its owner runs: `SKIP scripts/git/check-commit-message.ts [script-target] not yet
      created (git-commits-and-reporting creates it)`, the same for `scripts/deps/check-deps.ts`, `scripts/deps/check-npm-config.ts`, `scripts/audit/audit-licenses.ts`
      (dependency-management) and `scripts/i18n/verify-catalogs.ts` (i18n-strings-and-catalogs), and
      `[gate-file-missing]` SKIPs for `eslint.config.mjs`, `knip.json`, `.prettierrc.json`,
      `tsconfig.base.json` (typescript-and-lint-rules), `jest.config.js`,
      `scripts/quality/device-only.ts` (unit-and-component-tests) and `.npmrc` (dependency-management).

## Anti-patterns

- **Editing `quality-gates.json` to match a weakened config.** The guardrail then passes and the
  gate is gone. Restore the config; `check-gate-wiring.mjs` still fails the weaker value.
- **`// eslint-disable-next-line` "just this once".** It is inert (`noInlineConfig`) and reported;
  fix the code, or ask for a file-exact exception block (typescript-and-lint-rules).
- **Retrying a failing commit with `--no-verify`.** Denied by the permissions and found by
  `check-bypasses.mjs`; read the hook's output instead.
- **A `lefthook-local.yml` with `skip: true` "while I fix this".** It is usually git-ignored, so
  nobody sees it, and the guardrail fails it through `lefthook dump`.
- **Adding a test's path to `testPathIgnorePatterns` or a folder to `collectCoverageFrom` as `!...`.**
  It hides the failure, not fixes it; `jest-scope` and the guardrail's Jest scope both fail it.
- **Replacing `.claude/settings.json` with the asset.** That drops the plugin entry and the skill
  permissions; merge instead.
- **Splitting a 300-line file into `part-1.ts` and `part-2.ts`.** Split by responsibility, each part
  with its own test.
- **Adding `--passWithNoTests` or `-u` to a script, or a stub file behind a script, to get green.** A
  test command that finds no tests must fail; goldens change only by hand with a trailer.
- **Editing `verify-plan.ts` to add a step.** Append the script to `verifyExtraSteps` instead; the
  plan file is canonical.
- **A knip ignore entry "to silence a false positive".** Find why knip cannot see the use; an entry
  needs a tool contract, a reason in `contracts/knip-ignores.json` and the developer's agreement.
- **Guessing `--root .` for a checker.** The repo root is the first positional argument; the exit 2
  it prints is not a result.
- **Extending an expired release-age block.** Delete it; the lockfile keeps the installed versions.
- **Deleting the agent-folder `ignore` entries of `knip.json` because knip hints "Remove from
  ignore".** The hint appears while a folder does not exist; the first installed skill then fails
  `check:unused`. Keep the ten entries and their reasons.
- **Looping on the Stop hook.** When the turn ends with the gate still red, report the failing gate
  to the developer instead of working around it.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/gates-overview.md](references/gates-overview.md) | The gate stack, every canonical script and its owner, the verify pipeline with measured timings, check:fast, what runs outside verify, adopting into an existing app, when multi-package | Workflow step 1 |
| [references/hooks-and-settings.md](references/hooks-and-settings.md) | lefthook jobs and secret globs, the commit-msg hand-off, the Claude Code hooks, permissions, merging settings, local overrides, other agents, what was verified | Workflow step 2, and when a hook misbehaves |
| [references/guardrail.md](references/guardrail.md) | What the guardrail compares, what `quality-gates.json` holds, the gated paths, how a gate may change | Workflow step 5, and before touching a gate file |
| [references/fixing-failures.md](references/fixing-failures.md) | Fix by failure, flaky tests, limits, the never list, the gate-looks-wrong note | Workflow step 4, whenever a gate fails |
| [references/root-files.md](references/root-files.md) | `verifyExtraSteps`, adding a gate from another skill, the knip reasons contract, the coverage policy, the gated-paths module, what `check-gate-wiring.mjs` compares | Workflow step 6 |
| [references/supply-chain.md](references/supply-chain.md) | The dependency steps of verify, dated release-age blocks, install scripts, licences, knip settings, CI, other package managers | Workflow step 7 |
| `templates/package-scripts.json` | The canonical root npm scripts (canonical file, owned here) | Workflow step 2 |
| `templates/lefthook.yml` | pre-commit, commit-msg and pre-push hooks (canonical, owned here) | Workflow step 2 |
| `templates/quality-gates.json` | The guardrail's expectations, budgets, verify extra steps and gated paths; the baseline `check-gate-wiring.mjs` compares with (canonical, owned here) | Workflow step 2 |
| `templates/scripts/` | The gate scripts with their tests (canonical, owned here, synced): `quality/check-quality-gates.ts` + `gate-diff.ts` (the guardrail), `quality/verify-plan.ts` + `run-verify.ts` (the verify steps and runner), `quality/gated-paths.ts` (which changed files are gates), `hooks/after-edit.ts` (the PostToolUse hook), `hooks/install-git-hooks.ts` + `hook-install-plan.ts` (`prepare`: lefthook install at the git top level only), and `quality/device-only.ts` (unit-and-component-tests' coverage helper, synced: the baseline for `gate-script-changed`) | Workflow step 2 |
| `templates/contracts/` | `knip-ignores.json` (the reason for every knip ignore entry, the ten agent folders included) and its schema | Workflow step 2, and when an ignore entry is added |
| `templates/knip.json` | typescript-and-lint-rules' knip config (synced) | Only when its owner has not written it |
| `templates/dot-gitignore` | typescript-and-lint-rules' `.gitignore` (synced; copy as `.gitignore`) | Only when its owner has not written it |
| `templates/dot-npmrc` | dependency-management's `.npmrc` policy (synced; copy as `.npmrc`) | Only when its owner has not written it |
| `assets/claude-settings.json` | The deny rules (iOS and Android keys, hook bypasses), the ask rules (gate files), the PostToolUse and Stop hooks (canonical, owned here, synced; merge into `.claude/settings.json`) | Workflow step 2 |
| `assets/jest-config-baseline.js` | unit-and-component-tests' canonical `jest.config.js` (synced, never copied into the app): the scope values `jest-scope` compares with | Read only to see the canonical scope |
| `assets/package-scripts.multi-package.json` | The scripts that change when multi-package | When package.json has workspaces |
| `assets/gate-question.md` | The one-message note to the developer when a gate looks wrong | Workflow step 5 |
| `assets/shared.json` | Declares the files synced from the library (edit the canonical copies, never these) | When adding a shared file |
| `scripts/check-gate-wiring.mjs` | Checks gate files, scripts and their targets, hooks (commands byte for byte), settings and the local overrides, `.npmrc`, linter options, thresholds and logic folder keys, the Jest coverage and test scope, verify extra steps, knip reasons, that `quality-gates.json` is no weaker than the baseline, and that no gate reaches into agent folders while knip ignores them (14 rules) | Workflow steps 3 and 8 |
| `scripts/check-bypasses.mjs` | Finds suppressions, ignore comments, hook bypasses, auto-updated snapshots, relaxed ESLint flags and stale release-age exceptions anywhere in the repo (11 rules) | Workflow step 8 and the definition of done |
| `scripts/lib/not-weaker.mjs` | The direction-aware comparison the wiring check uses | Read only to change a rule |
| `scripts/lib/workspace-scope.mjs` | The workspace form of the Jest scope (prefixes from `package.json` `workspaces`, the single-app form, logic-key counterparts, reach probes) | Read only to change the multi-package rules |
| `scripts/selftest.mjs` | Proves both checkers on good fixtures and every planted bug | After changing a checker, a template or a fixture |
| `scripts/check-lib.mjs` | Shared script helper, synced from the library (do not edit here) | Never by hand |
| `tests/bases/` | The canonical root configs (synced) and stub targets the wiring suite starts from | When adding a case |
| `tests/fixtures/` | Overlay cases for both checkers (`EXPECT.txt` plus `mutation.json`, `DELETE.txt`, `ARGS.txt` or overlay files) | When adding a rule |

## Related skills

- `typescript-and-lint-rules` - `eslint.config.mjs`, the tsconfig set, knip, Prettier and the limits table.
- `unit-and-component-tests` - the Jest configs, coverage thresholds, the device-only marker, Stryker.
- `dependency-management` - installs, `.npmrc`, `check:deps`, `audit:licenses`, release-age exceptions.
- `git-commits-and-reporting` - the commit-message check, the `Gate-Change:` trailer, the report.
- `tdd-workflow` - the test-first loop that `check:fast` closes.
- `expo-project-bootstrap` - writes these gate files into a new app.
- `ci-pipeline-and-gates` - running `npm run verify` in CI.
- `golden-and-snapshot-tests`, `seeded-determinism-and-golden-vectors` - the goldens and vectors behind gated paths.
- `accessibility-as-code`, `performance-budgets` - the `a11y` and `perf` blocks of `quality-gates.json`.
- `troubleshooting-playbook` - known tool failures behind a red gate.
