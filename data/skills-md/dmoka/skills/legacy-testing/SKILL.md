---
name: legacy-testing
description: "Test legacy code: assess first, then propose a plan. Use when a codebase or module has few or no tests and you need to change it safely: adding tests to untested code, getting a safety net before a refactor, taking over code you did not write. Looks at the stack, the dependencies and the code no test touches, proposes which steps this repo needs (make it testable, characterize, approve, property tests that hunt for crashes at every entry point, measure, refactor last), waits for approval once, then runs every approved step without stopping."
---

# Legacy testing

Legacy code is code without tests. The job is a **net** under the behaviour that carries the business, built before anyone refactors. Assess first, propose, wait for approval, then execute.

## Steps

1. **Assess.** Run `scripts/assess.sh [path]` from the repo root; the path is a file or a folder. It lists the tests anywhere in the repo that import the target, and the files no test imports. Read those tests and the three biggest untested areas, and name, for each, the **load-bearing** behaviour (money, permissions, data that must not be lost). Then list the target's **entry points**: every place outside input reaches it (an HTTP route, a CLI command, a message handler, a parser, an exported function called with user data); grep for the target's imports outside the tests and follow them to the edge. Done when you can state, per area: what it does, what it depends on, which tests already touch it, its entry points, and how a mistake there would hurt.
2. **Propose.** Write the plan with the template below: which steps this repo needs, in which order, and why each one. Choose from the menu; skip what the assessment says is not needed. The refactor is the plan's last step by default, with its target and why; leave it out only when the user said so. Done when every chosen step names its target (files or functions) and its why.
3. **Stop for approval, once.** Show the plan and wait. The user judges two things: is it aimed at the load-bearing behaviour, and do the tests check behaviour rather than today's implementation? Approving the plan approves its refactor step too. Done when the user approves or edits the plan.
4. **Execute the approved plan without stopping.** Do the steps in order: open the step's playbook, do it, run the suite, start the next step. Do not ask "shall I go ahead?" between steps; approving the plan approved every step in it. Stop and ask only to: mark a mutant equivalent, change CI or config the plan did not list, or fix a suspected bug instead of pinning it. Start the refactor only after the measure step meets the target, and commit it separately from the tests, in commits that change no behaviour. Done when every step's own completion check passes and the suite is green.
5. **Report once, at the end:** the score before and after, the tests added, the suspected bugs (the crashes the crash-hunt properties found included), what the refactor changed, the open decisions. Delete every TEMPORARY file first.

## The menu

| Step | Use it when | Playbook |
|---|---|---|
| Make it testable | the code reaches a database, an API, a queue, the clock or the filesystem directly | `references/make-it-testable.md` |
| Characterize | nobody can say what the code does today | `references/characterize.md` |
| Approval tests | the output is big: JSON, HTML, reports | `references/approval-tests.md` |
| Property tests: crash hunt | every target outside input can reach (an endpoint, a CLI command, a handler, a parser): generated input, valid and broken, must never crash an entry point | `references/property-testing.md` |
| Property tests: invariants | rules with edge cases: money, dates, limits, round trips | `references/property-testing.md` |
| Measure | before calling the net done: coverage shows what never ran, mutation shows what was never checked | `references/measure.md` |
| Refactor | every plan, as the last step, after measure meets the target; leave it out only when the user says so | `references/refactor.md` |

## Plan template

```
Area: <files> — load-bearing: <behaviour>
Entry points: <route / command / handler / exported function> → <target>
1. <step> on <target> — why: <reason from the assessment>
2. ...
n. Crash-hunt property on <each entry point> — why: outside input reaches it; no input may crash it
n+1. Invariant properties on <rules> — why: <the rules with edge cases>
last. Refactor <target>: <the structure change> — why: <what the assessment found hard to read or change>
Skipped: <step> — why not needed here
Target: mutation score on <area> ≥ <n>% (coverage is a hint, not the goal)
```

## Gotchas

- Characterization tests **pin** today's behaviour, bugs included. When a pinned result looks wrong, pin it anyway, name the test `pins current behaviour — suspected bug: <what is wrong>`, and list it in the final report; fixing it is a separate, later change.
- A dependency that is fast, or that carries the business logic, stays real in the test (an in-memory or containerised database, the real rules engine). Use a test double only for slow or unreliable edges.
- Approval tests are scaffolding. Mark them as temporary in their file name or a comment, so they get deleted once functional tests cover the behaviour.
- A crash the crash-hunt property finds is a suspected bug, even when no user has hit it: pin the shrunk input, list it, and keep the property hunting. A crash spotted while reading the code does not replace the property: pin the spotted crash, and add the property for that entry point anyway.
- A flaky test is not a net. When a test passes and fails without a change, quarantine it and report it before building on it.
- Long suites: run the narrowest command that covers the area while working (one file, one folder), and the full suite at the end of each step.
- Aim the mutation score at the load-bearing area, not the whole repo; a repo-wide number hides the money code in the average.
- Scope every mutation run twice: mutate only the target file (Stryker: `--mutate <file>`), and run only the tests that import it (`assess.sh <file>` lists them). Use a project script if one exists; otherwise see "Scoped runs" in `references/measure.md`. The repo's own config can run its whole suite as the dry run.

Last verified: 2026-10-04 with Claude Code 2.1.289, plan only (no execution run), on TicketBay branch `legacy/reporting`: for `src/finance/payouts.ts` 2 of 2 plans listed a crash-hunt property on `GET /api/v1/organizer/payouts` and the refactor as the last step, unasked (the previous version: 0 of 2, "Skipped: Refactor" in both); 1 of 1 plan on `src/finance/invoices.ts` did the same. Before that, 2026-10-04 on TicketBay `src/db/admin-queries.ts`: mutation score 62.7% → 98.5%, four suspected bugs pinned. That trial drove this version: assess.sh took no file path and missed tests outside the target folder; the agent paused after every step; the unscoped dry run passed 10 minutes and never finished, the scoped one took 1.5 minutes. Earlier: 2026-09-29 with 2.1.284 (TicketBay with deleted tests, and a real untested MERN app).
