---
name: test-audit
description: Prunes low-value tests to a measured target while holding coverage, and gates new tests before they land. Use when asked to "remove useless tests", "prune the test suite", "we have too many tests", "agents keep writing pointless tests", "cut 20% of tests without losing coverage", "audit these tests", or "should this test exist". For a slow pipeline use ci-speedup; for reviewing a diff use tidy.
compatibility: Needs the repository's test runner and a coverage tool it already supports (Vitest, Jest, c8, pytest-cov, go test -cover, or equivalent).
---

# Test Audit

Tests earn their place by catching a credible regression that nothing else catches. Agents write a test for every small change, and most of those re-assert the source, replay a stronger test through a mock, or pin a private call shape. Coverage barely moves when they go; maintenance cost and suite time do.

- **IS:** gating a new or changed test before it lands, sweeping a directory for low-value tests, and campaign-pruning a whole subsystem to a measured target with coverage held, plus deleting the test-only production seams those tests kept alive.
- **IS NOT:** making CI faster by splitting or sharding (`ci-speedup`), reviewing a feature diff (`tidy`), or writing tests for untested code (though any test that work adds should pass the gate).

## Pick a mode

| Mode | When | Done means |
|------|------|------------|
| **Gate** | About to add or change a test, or asked "should this test exist" | Each test passes the four questions and no junk pattern, or is rewritten at the owning boundary, or is not added |
| **Audit** | A focused sweep of named files or a directory | A handful of high-confidence candidates with full evidence, deleted in one coherent batch with validation green |
| **Campaign** | A subsystem's whole test surface, or any request with a target ("remove 20%") | The target is met or the ledger shows why it cannot be, coverage held within tolerance, and the preservation review passed. Read `references/campaign.md` first |

## Set a target before starting

An open-ended "clean up the tests" stops after a few obvious deletions, because every remaining candidate looks defensible in isolation. Audit and Campaign need a number to work against. When the user gave one, use it. When they did not, propose one and proceed on it rather than waiting:

> Remove the least useful 20% of test declarations in `<scope>`, keeping line and branch coverage within 2 percentage points of the baseline and every retained test green.

Measure the baseline first (`references/coverage.md`), then keep deleting in order of lowest value until the target is met or the coverage budget is spent. Stopping short is a valid result only with a ledger showing that the remaining candidates each guard a named contract. The target is a floor on effort, not permission to cut uncertain tests: the retention bar below still wins over the number.

## The gate

Before adding any test, answer four questions. A missing answer means do not add it yet.

1. What observable behavior, invariant, or independent contract does it protect?
2. What credible regression makes it fail?
3. Why does existing coverage not already catch that failure? Each contract has one primary test at the strongest boundary; another layer needs its own distinct risk, such as a transport or lifecycle failure the owner cannot reach. Extend a table-driven case or shared fixture before writing a near-duplicate.
4. Does it need a production seam (export, flag, wrapper, injection hook) that no production caller needs? If yes, test at the real boundary instead.

Then check it against the junk patterns. A test that would break under a behavior-preserving refactor asserts implementation, not behavior; rewrite it at the owning boundary.

A bug regression test must fail on the pre-fix code for the intended reason, and pass after the fix. One that never demonstrably failed proves the mock, not the fix. One regression at the owner boundary covers the bug; do not replay it at every layer it crosses.

## Junk patterns

What the gate rejects and what audits hunt:

- assertion-free coverage probes, and tests whose only assertion is "does not throw" on a path that cannot throw
- self-comparisons, identity copies, and expected values produced by the helper or renderer under test
- copied fixtures, inventories, manifests, export lists, or snapshots of data the test also defines
- exact source, import, or string greps that fail on a rename and survive a real behavior change
- private predicate or call-shape tests (`toHaveBeenCalledWith` on an internal) duplicated at a real boundary
- duplicate invocations of one contract, and per-provider replays of a shared helper
- tests whose only purpose is keeping a test-only export, global, or wrapper alive, and production code whose only callers are tests
- mocks that implement the asserted behavior, or one mock standing in for several different APIs
- fixtures that supply the ordering, receipt, or callback the code under test should produce, or persistence asserted against a store the path never writes
- capability tests that restate declared flags instead of exercising what the flag promises
- negative controls that pass for an unrelated reason, such as a rejection from a different guard
- names that promise more than the assertions check: judge the test by its assertions, not its title

## Retention bar

Keep a test when it independently enforces a public API, protocol, config, migration, storage, security, platform, default value, generated cross-language, package, release, or architecture contract. Also keep:

- call ordering when the order is observable behavior
- a regression with a credible failure mode
- a source inspection when it is the cheapest independent guard: it fails when the user-facing key, byte, or path changes and survives an identifier-only rename
- a retained test that fails on the baseline: treat it as a possible product bug, reproduce it, and fix the owner rather than deleting it

Static or slow is not a reason to delete. A test that resembles implementation may still be the only proof of a contract; show otherwise before removing it.

## Evidence per candidate

Before judging, read the complete test, the production owner, its callers and callees, sibling implementations, overlapping tests, and the history that explains why the test exists. Record for each deletion:

- test name and location, and what failure it can actually detect
- non-test callers of the seam it covers
- the stronger proof that remains (name the keeper test), or why no contract exists
- the production or test-support code the deletion unlocks
- coverage delta from removing it, when measured

A missing field means the candidate is not ready. Prefer a few high-confidence deletions over a long speculative list; do not convert uncertain candidates into deletions to reach the number.

## Edit shape

Delete in coherent owner-boundary batches. With each batch, delete the test-only exports, globals, wrappers, reset hooks, and dead production paths it unlocks instead of keeping aliases. Move retained regressions to their canonical owner and fold duplicated setup into shared fixtures. Aim for net-negative production lines as well as test lines. Do not add replacement tests that restate the same implementation.

## Validation

1. Run the owner and sibling tests for each batch.
2. Where a deleted test grepped source or asserted a plan, run the script or dry-run that owns the real contract.
3. Re-measure coverage with the same command as the baseline and compare against the budget, per file.
4. Report `git diff --numstat` with production and tooling lines separate from test lines.

## Permissions

Running tests and coverage locally, and deleting tests and test-only seams in the working tree, are the task: do them without asking. Commit, push, or open a PR only when asked. A test that meets the retention bar stays; deleting one anyway is the user's call, as is changing coverage thresholds or CI gates.

## Handoff

- target, baseline, and final numbers: declarations or lines, and line and branch coverage
- removed categories and the root cause behind them (what kept producing these tests)
- production simplifications, counted separately from test lines
- retained false positives and why each stays
- validation actually run, with results
- a proposed gate for the repo's `AGENTS.md`, drawn from the patterns this audit actually found, so agents stop writing them

## Gotchas

- Line coverage survives deletions that remove the only assertion on a path, because another test still executes the lines without checking them. Where a deletion looks free on coverage, confirm a keeper asserts the behavior, or run a mutation against the owner (`references/coverage.md`).
- Aggregate coverage hides a subsystem that lost its only proof while an unrelated area gained. Compare per file for every production file the deleted tests touched.
- Ranking candidates by unique line coverage alone deletes the wrong tests: a test with zero unique lines can still hold the only assertion on them. Unique coverage makes a test a candidate; a named keeper makes it a deletion.
- Editing tests while Vitest or Jest runs in watch mode on the same checkout re-runs half-edited files, and the failures read as regressions from the deletion. Stop the watcher before a batch.

## Reference files

| File | Read when |
|------|-----------|
| `references/campaign.md` | Campaign mode, or any target-driven prune larger than one directory |
| `references/coverage.md` | Measuring the baseline, per-file and per-test coverage, the budget check, and mutation spot checks |

Maintenance only: `evals/evals.json` holds scenarios and routing prompts for changing this skill; it never loads during a task.

## Sources

Adapted from OpenClaw's `test-audit` skill and its campaign guide ([openclaw/openclaw](https://github.com/openclaw/openclaw/tree/main/.agents/skills/test-audit), MIT), which removed about 400k lines of tests with little change in coverage. Took the gate, junk patterns, retention bar, evidence fields, and campaign order. Left the OpenClaw-specific runners, CI routing, and PR tooling. Authored the target-and-budget framing (an agent told only to "clean up" stops early), the coverage measurement reference, and the AGENTS.md gate handoff.
