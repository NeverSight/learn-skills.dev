---
name: test-suite-doctor
description: Audit and shrink bloated JavaScript/TypeScript test suites (Vitest or Jest) without losing real quality. Use when the user wants to reduce or minimize a test suite, clean up AI-slop or duplicate tests, audit test quality, prune redundant tests, or verify a reduced suite against coverage and mutation-score baselines. Metrics-driven — the bundled CLI measures per-test coverage and runtime and computes the keep/drop plan; never prune tests by gut feeling.
---

# test-suite-doctor

Shrink an oversized test suite (e.g. 2,000+ tests, much of it AI-generated slop)
to a small, high-quality suite while retaining a configurable share of real
coverage — measured, not guessed.

## Hard rules

1. **Metrics before opinions.** Never propose deleting a test before
   `collect` and `minimize` have produced a plan. Reading test
   code and judging it "useless" is not evidence — a trivial-looking test can be
   the only cover for a branch.
2. **The plan is a proposal, not a verdict.** Coverage cannot see API
   contracts, documented regression cases, or property invariants. Every drop
   candidate gets reviewed (step 3) before deletion.
3. **Work on a branch.** Before deleting anything, verify the working tree is
   clean and create a branch (e.g. `test-doctor/minimize`). Never delete tests
   on a dirty tree or the default branch.
4. **Verify or revert.** The job is not done until `verify` exits 0. If it
   fails, regenerate tests for the reported gaps and re-verify — or restore the
   deleted tests.

## Requirements check (do this first)

- Node.js ≥ 22 and a package.json using a locally installed Vitest or Jest
  (`node <skill-root>/dist/cli.mjs collect --help`).
- A coverage provider must be installed (Vitest: `@vitest/coverage-v8`;
  Jest has one built in). If missing, offer to install it as a dev dependency.
- Mutation verification additionally needs `@stryker-mutator/core` configured
  in the target repo — it is opt-in, do not install it unprompted.
- The suite should be green before starting. If the baseline run reports
  failures, tell the user and get agreement on how to handle them before
  minimizing (failing tests contribute unreliable coverage).

All commands below run from the target repo root; `$SKILL` is this skill's
directory. Artifacts land in `.test-doctor/` (suggest gitignoring it).

## Workflow

### 1. MEASURE (script — always first)

```bash
node "$SKILL/dist/cli.mjs" collect --cwd .
```

Detects the runner, runs the full suite once as the coverage baseline, then
re-runs each test file in isolation recording covered lines/branches and
runtime. Writes `.test-doctor/report.json`.

- Default granularity is per test **file** (per-test isolation is exact but
  runs every test separately — offer `--granularity test` only for small or
  already-reduced suites, or scoped with `--filter`).
- On a 2,000-test suite this takes a while; run it in the background and
  report progress. Take `collectionErrors` in the report seriously — those
  units block minimization by default. If the user explicitly chooses
  `--keep-unmeasured`, every affected unit is a mandatory keep and the plan is
  marked untrusted.
- `--filter` creates a deliberately scoped baseline: collection, minimization,
  and verification cover only matching test files. State that scope in every
  recommendation; it is not a whole-repository guarantee.

### 2. MINIMIZE (script)

```bash
node "$SKILL/dist/cli.mjs" minimize --coverage-floor 0.97 --target-count 200
```

Greedy weighted-sum selection: repeatedly keeps the unit with the most newly
covered lines/branches per millisecond of runtime until the coverage floor is
met. Writes `.test-doctor/plan.json` and a human-readable `.test-doctor/plan.md`
with a justification per kept and dropped unit.

- Ask the user for their thresholds if not stated; defaults are a 0.97 line
  floor, no branch floor, no target count. `--help` lists all knobs.
- Force-keep known contract/regression tests up front:
  `--keep 'contract' --keep 'regression'` (regex on unit id).
- Heed the plan's `warnings` array — e.g. the floor being unreachable, or
  requiring more units than the target count. Relay them to the user verbatim.

### 3. REVIEW (judgment — yours)

Read `references/slop-patterns.md`, then review the **drop list** in
`plan.md`:

- Rescue any test that verifies behavior invisible to coverage: public API
  contracts, regressions referencing an issue/bug ID, error-message wording
  relied on by consumers, property/invariant checks. Re-run minimize with
  additional `--keep` patterns rather than editing the plan by hand.
- Confirm the rest are safe deletions; classify them by slop pattern so the
  user sees *why* each dies (the patterns file has the catalog).

Then review the **keep list** against `references/quality-rules.md`: kept
tests that smell (mock-the-mock, tautologies, hollow snapshots) get rewritten
in place — they earn their coverage, but they should earn it cleanly.

Only after this review, delete the dropped test files/cases on the branch.
Delete whole files when all their units are dropped; edit files when only some
tests within them die (test granularity).

### 4. REGENERATE (judgment — yours)

Run verify once (expect it may fail) to get the coverage-gap report, then write
new tests for the worst-hit source files listed by `verify`, following
`references/quality-rules.md`: AAA structure, behavior-driven names, one
behavior per test, mocks only at external boundaries. Prefer one strong test
covering a real user-visible behavior over three shallow ones.

### 5. VERIFY (script — gates completion)

```bash
node "$SKILL/dist/cli.mjs" verify --coverage-floor 0.97
# optionally, for critical modules only (slow):
node "$SKILL/dist/cli.mjs" verify --mutation --mutate "src/billing/**/*.ts" --mutation-floor 80
```

Re-runs the suite, requires it green, and requires line retention vs the
baseline to meet the floor. Exit 0 = done; exit 1 = fix and re-run (regenerate
more tests, or restore deletions); exit 2 = environment problem, stop and
report. Mutation testing is opt-in per module because it is slow — offer it for
the modules the user calls critical.

Version 2 baselines fingerprint covered source, runner configuration, lockfile,
runner, and coverage provider. If verify reports provenance drift, collect a
new baseline. Use `--allow-provenance-drift` only with explicit user agreement
and report the resulting verdict as untrusted. Legacy v1 baselines similarly
require the explicit `--allow-legacy-baseline` escape hatch.

## Reporting back

Summarize for the user: units before → after, line/branch retention, runtime
before → after, slop patterns found (with counts), tests rescued from the drop
list and why, tests regenerated, and the final verify verdict. Include the path
to `plan.md` for the full audit trail.

## Failure modes

- **Runner not detected / ambiguous** → the CLI exits 2 with guidance; pass
  `--runner` or `--cwd` (monorepos: run per package).
- **Incomplete collection** → fix the isolated failures. Do not filter them
  away merely to make a plan pass; a filter changes the declared baseline
  scope. `--keep-unmeasured` is the conservative escape hatch.
- **Verify keeps failing after regeneration** → stop looping after ~3
  attempts; present the residual gap file-by-file and let the user decide
  between lowering the floor and keeping more tests.
- **Suite was red before starting** → do not "fix" unrelated failures
  silently; report them and agree on scope first.
