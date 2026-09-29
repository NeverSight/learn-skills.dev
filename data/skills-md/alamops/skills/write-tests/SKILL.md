---
name: write-tests
description: (alamops) Writes the tests a change needs — unit, integration, and e2e whenever it has a user-visible flow or crosses a process boundary. Use it whenever the user asks for tests to be written, added or backfilled — for the changes on their branch vs main, a new endpoint, an under-tested module, or an e2e flow — in any framework (jest, vitest, pytest, Playwright, Cypress…). Works from a plan's test breakdown, a branch diff, or a named module or flow; fans out agents partitioned by module under test; extends the existing harness and fixtures; covers acceptance criteria plus negative paths and failure states; keeps e2e deterministic; records 'e2e not applicable' as an explicit decision; and proves each new test runs and can fail, reporting real product defects instead of bending tests to pass. Phase 6 of `implement`, runnable alone; accepts `--no-e2e`. Not for running or fixing a failing suite (test-loop), bug hunting on a running app (break-fix), or building the feature (implement).
---

# Write tests — the coverage the change actually needs

Your job is to add tests that would catch this change breaking: its acceptance criteria, the negative paths, and — when the change spans layers — the assembled flow end to end. You coordinate; agents write the test files in parallel, partitioned so they never edit the same file.

## Where this sits

This is Phase 6 of the `implement` delivery loop, packaged to run on its own. It usually follows `execute-plan` (or any finished change) and is followed by `test-loop`, which runs the full suite and drives it to green. This skill runs only the tests it writes — once, to prove they execute.

## 1. Work out what needs covering

Find the target, in order of preference:

1. **A plan's test breakdown** — `docs/plans/<slug>.md` §5 lists test tasks, their layer, which implementation task each covers, and the e2e run recipe. Use it as the partition.
2. **A branch diff** — `git diff <base>...HEAD` plus uncommitted changes. Default `<base>` to the plan's `Base SHA` if there is one, else the merge-base with `origin/main` (or `main`/`master`).
3. **A named module or flow** — "backfill tests for `billing/proration.ts`", "add e2e for checkout".

Then gather **what the change is supposed to do** — the plan's objective and acceptance criteria, a grill record, the PR description, the ticket. Tests encode intent; tests written only from the diff encode whatever the code happens to do, bugs included.

Finally, **map the existing test setup** before writing anything: the test runner and command per layer, where test files live and how they're named, fixtures, factories, and helpers, how state is reset between tests, and how the app is started for integration/e2e (an `investigate` brief's *Runnability* section has this if one exists). New tests should look like the tests already there; a second, parallel harness is a maintenance cost nobody asked for.

## 2. Decide whether e2e applies — explicitly

Unit and integration tests validate pieces in isolation. A class of bugs only shows up in the assembled system — broken wiring between layers, auth and session behavior, a migration meeting real data, a UI flow that dies on its second step — and for those an e2e test is often the only automated way to catch it before a user does.

- **E2e applies** when the change has a user-visible flow or crosses a process boundary (UI → API → DB, service → service, CLI → filesystem) and the app can run locally.
- **It doesn't** for a pure library or helper change fully exercised by unit tests. Say so in your report: "not applicable" is a recorded decision, never a silent omission.
- **No e2e harness in the repo?** Don't stand up heavyweight infrastructure on your own initiative. Propose the minimal ecosystem-standard harness scoped to this change's flows and let the user decide; if they asked for e2e coverage outright, build that minimal harness and nothing more.
- **Under `--no-e2e`** (or "skip e2e"), write no e2e tests and set up no harness — unit and integration coverage is unchanged.

## 3. Partition and fan out

Partition test tasks **by the module or file under test**, so each agent owns its own test files. Shared test infrastructure — a fixtures module, a factory file, a global setup, snapshot directories — is the hot spot: give each shared file to exactly one task, or sequence the tasks that need it.

Keep the fleet proportionate: a small change is one agent or none (write the tests yourself); a feature spanning several modules might be 2–4. Spawn a wave's agents **in a single message** so they run concurrently. On Claude Code, use `general-purpose` agents and leave the model unset so they inherit the session's model, unless the user asked for another. If your harness has no sub-agent tool, write the tasks yourself one at a time.

Each brief carries:

- **Objective** — what behavior this agent's tests pin down.
- **Owned files** — the test files it creates or edits, and "touch nothing else"; in particular, **don't modify product code** — if it looks wrong, that's a finding to report, not something to fix here.
- **Intent** — the acceptance criteria and business rules to encode, with sources.
- **Conventions** — the existing tests to mirror (`file:line`), the fixtures and helpers to reuse, the command to run just these tests.
- **Output** — files added, what each test covers, the result of running them once, and any test that fails because the product is wrong.

## 4. What good tests look like here

- **Acceptance plus the unhappy paths.** The happy path is the one already exercised by hand a hundred times. Add the negative paths, the boundaries (0, 1, max, max+1, empty, whitespace-only), the error and permission-denied states, and the states the change newly makes reachable.
- **Assert behavior, not implementation.** Test through the public surface. A test that breaks when the code is refactored without changing behavior is a tax, not a guard.
- **Don't mock the thing under test.** Mock at the boundaries you don't own (third-party APIs, the clock, randomness), not the logic you're verifying.
- **Deterministic and isolated.** Seeded data, reset state between tests, fixed clocks. Never `sleep` to wait for something — wait for the condition (a readiness endpoint, an element, a response). A flaky test gets skipped within a month, and a skipped test guards nothing.
- **E2e: critical paths only.** The feature's happy path plus at least one failure state a real user could plausibly hit, over the real stack — an e2e suite that only walks the happy path misses exactly the wiring bugs it exists for. E2e is the slowest, flakiest layer, so it covers what only it can catch rather than duplicating unit tests.

## 5. Run what you wrote — once

Every new test gets run at least once before you report, with the narrowest command that runs it. A test file nobody has executed might not even load.

- **It passes** → prove it can fail. For each behavior the change is about, break it on purpose in a scratch copy (flip the condition, drop the guard, return early, delete the route) and confirm the test covering it goes red. A test that stays green against broken code guards nothing, and this is the cheapest way to find out — it takes seconds per mutation and routinely catches assertions that only look like they check something.
- **It fails because the test is wrong** (bad fixture, wrong selector, wrong assumption about setup) → fix the test.
- **It fails because the product is wrong** → that's the test doing its job. Don't loosen the assertion, skip it, or delete it to get green, and don't fix product code here. Keep the failing test, and report the defect with the evidence (expected vs actual, the test that shows it). Driving it to green is `test-loop`'s job — or the user's call.

A full-suite run is out of scope here; if the new tests needed app startup, tear down whatever you started.

## 6. Report

- **Tests added**, per layer and file, and what each one covers.
- **E2e decision** — applies to which flows, not applicable and why, or skipped by flag.
- **Run results** — the command(s) used and pass/fail for the new tests.
- **Product defects found** — anything a new test exposed, with evidence.
- **Next step** — `test-loop` to run the whole suite and drive it to green.
