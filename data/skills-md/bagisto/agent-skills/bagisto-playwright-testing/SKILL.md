---
name: bagisto-playwright-testing
description: Use when writing, changing or debugging a Bagisto end-to-end test — deciding what to cover, Playwright specs, page objects, locators, assertions, ACL role coverage, fixtures, test data, admin-versus-storefront coverage, a regression test, or a failing E2E run. Trigger phrases include "playwright", "e2e", "end to end", "spec.ts", "page object", "browser test", "add tests for", "flaky test", "regression test", "shard".
---

# Playwright Testing

## Do not write the spec first

"Add Playwright tests for X" is not an instruction to start typing a spec. It is
an instruction to find out what X actually does, what already covers it, and
which of its behaviours a browser can prove that a Pest test cannot.

A test written before that investigation is usually a duplicate, a test of the
wrong layer, or a test that passes whether or not the feature works. All three
cost more than they return: someone maintains them, and nobody can trust them.

Work the pipeline in order — understand the feature and its rules, map what
already covers it, decide the scenarios and which belong in Pest, design the data
and locators, implement, then classify every failure before changing anything:

| Phase | Read | Produces |
|---|---|---|
| Investigate | [investigation.md](investigation.md) | The feature, its rules, its impact surface, and what already covers it |
| Structure | [architecture.md](architecture.md) | Where a helper, page object or shared utility belongs |
| Design | [test-design.md](test-design.md), [admin-and-shop.md](admin-and-shop.md) | State transitions, a coverage matrix, an E2E-vs-Pest call per scenario |
| Implement | [authoring.md](authoring.md), [test-data.md](test-data.md), [locators.md](locators.md), [assertions.md](assertions.md) | A spec and its page object |
| Time-dependent work | [time-and-timezone.md](time-and-timezone.md) | Booking, rental, slot, availability and "today" coverage that holds in CI |
| Clicking a storefront product card | [lost-clicks.md](lost-clicks.md) | A click that an image finishing its load cannot swallow |
| Prove | [troubleshooting.md](troubleshooting.md) | A run that passes for the right reason, twice |
| Gate | [quality-gate.md](quality-gate.md) | A completed checklist |

**Scale the process to the change.** A one-line locator fix needs the
investigation step (why did the locator break?) and the proof step (does it still
fail when the feature does?), not a coverage matrix. A new feature area needs all
of it. What never gets skipped: reading the application code, and proving the
test can fail.

## How to think about this work

- **Maximise meaningful behavioural coverage, not test count.** Ten tests that
  differ only in input value are one test with a data table.
- **A passing test is not evidence of a good test.** Ask separately whether it
  *could* have failed — if the feature were deleted, would this go red?
- **Do not copy an existing test without deciding what it proves.** These suites
  contain tests that assert only that a toast appeared.
- **A business prerequisite is not an execution dependency.** Establish the state
  you need; never rely on another spec having run.
- **Do not add a wait without naming the thing you are waiting for.**
- **Classify a failure before changing anything.** If the application is wrong,
  the red test is doing its job — never edit an assertion to get green.
- **Choose a locator because it is stable and uniquely identifies the intended
  element**, never because it is short or made strict mode quiet.
- **Search before you build.** A new fixture, helper or page object is the last
  resort, after reuse, extension and refactoring.
- **A regression test is not finished until it has failed against the bug.**
- **Prefer the strongest behavioural verification with the least machinery**, and
  stop when the risks are covered — [test-design.md](test-design.md) says when.

## Architecture

Three independent Playwright projects — `packages/Webkul/{Admin,Shop,Installer}/tests/e2e-pw/`,
each with its own `playwright.config.ts`, `setup.ts`, `pages/`, `tests/`, `utils/`
and `data/` — plus a root-level `tests/e2e-pw/helpers/` layer of
**dependency-free** helpers all three import through `@shared/*`.

Two rules follow, and both are load-bearing:

- **The shared layer takes no dependencies.** CI installs `node_modules` per
  package only, so nothing under `helpers/` may import `@playwright/test`,
  `dotenv` or any third-party package. A helper that needs one belongs in that
  package's `utils/`.
- **The suites share no page objects, fixtures or specs.** Each carries page
  objects for whatever screens it drives, including the other side's. Never
  import across package boundaries.

Timeouts differ per suite and per release line, so read the checkout's
`playwright.config.ts`. Raise a single flow with `test.setTimeout(...)`, never
the config.

Full layout, the where-does-code-go table, the wrapper pattern and the timeout
values: [architecture.md](architecture.md).

## Running

Run from the package directory, never the repo root — that is where
`node_modules` lives. All three packages expose the same scripts:

```bash
cd packages/Webkul/Admin          # or Shop, or Installer
npm install && npm run install:browsers
npm run test:e2e
npm run test:e2e -- tests/catalog/categories.spec.ts -g "create a category"
npm run typecheck                 # tsc --noEmit over the suite
```

`test:e2e:headed`, `:ui`, `:debug` and `:report` mirror the Playwright flags.
Admin and Shop need a running, installed, seeded app; Installer needs an
*uninstalled* one. [troubleshooting.md](troubleshooting.md) has the environment
contract.

## Non-negotiables

- **The suite shares one database and does not roll back.** An E2E run leaves
  every record it creates. Assertions must survive that: scope to the row you
  created, never to a global count or a list position.
- **A test owns its state.** It creates what it needs, restores any global
  setting it changed, and deletes only what it made. Never operate on "the first
  row" or an arbitrary existing record because it was convenient —
  [test-data.md](test-data.md).
- **Tests are independently runnable, across suites too.** `workers: 1` and file
  order are not permission to depend on another test having run, and a Shop spec
  never assumes an Admin spec configured anything —
  [admin-and-shop.md](admin-and-shop.md).
- **Admin auth is cached** to `.state/admin-auth.json` by the `adminPage` fixture.
  Do not log in by hand in a spec; the Shop promotion specs that call
  `loginAsAdmin(page)` are legacy — see [authoring.md](authoring.md).
- **Rebuild assets before running** after any frontend change, or the browser
  loads the previous bundle and the failure will look like a test bug.
- **Never run Pest and Playwright against the same database at once.** An E2E
  run reprices products and changes settings while the feature suites read
  them, and the Pest failures it causes look like broken code —
  [troubleshooting.md](troubleshooting.md).
- **No comments anywhere under `tests/e2e-pw/`** — no `//`, no `/* */`, no
  docblock. This is a Bagisto convention, held without exception across all three
  suites today, and it diverges from generic Playwright advice deliberately. Put
  the reason in a method name instead; [authoring.md](authoring.md) shows how.
- **Generate test data inside `beforeEach`, never at module scope.** One
  module-scope `uniqueStamp()` gives every test in the file the same SKU, and the
  file only passes while cleanup never misses.
- **A test that depends on the clock is a timezone question first.** The app runs
  on `APP_TIMEZONE` (`Asia/Kolkata` here) and the configs pin Node and the browser
  to the same zone. Anything involving today, tomorrow, slots, availability or
  expiry is investigated with [time-and-timezone.md](time-and-timezone.md) before
  anything else.
- **"Flaky" is a conclusion, not a starting hypothesis.** One shard failing, one
  database driver failing, or a local pass are not evidence of flakiness. Get the
  trace, the timestamps and the server log first —
  [troubleshooting.md](troubleshooting.md).
- **Filenames are lower-kebab** and **a file that declares a class is named
  exactly for it** — `CatalogAclPage.ts`, not `catalog.ts`. Describe and test
  titles are lower case with single spaces. No numeric ordering prefixes.

The spec names the intent and composes the workflow; the page object owns every
locator and asserts through named `expect…` methods. A spec that contains a CSS
selector belongs in a page object instead — [authoring.md](authoring.md).

**REQUIRED SUB-SKILL:** Use bagisto-change-verification before calling any change done.
