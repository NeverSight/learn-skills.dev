---
name: qa-test-code-coverage
description: Map test cases — manual (markdown) and automated e2e (Playwright, Cypress, WebdriverIO, CodeceptJS, Puppeteer, Appium) — to source code files and produce a `coverage.tests.yml` mapping consumed by `@testomatio/reporter --filter "coverage:..."`. Use this skill when the user wants to run only the tests affected by a code change, generate a coverage file (manual, e2e, or both), build a traceability matrix between tests and source code, or set up change-aware regression.
license: MIT
metadata:
  author: Testomat.io
  version: 1.0.0
---

# Tests to Code Coverage

Analyze the project's tests — manual markdown cases and automated e2e tests — and its source code. Produce `coverage.tests.yml` — a map from source files (or globs) to test identifiers: suite IDs, test IDs, tags. Testomat.io keeps manual and automated tests in one project, so one coverage file serves both. `@testomatio/reporter` consumes it to run only the tests affected by a diff (Step 6).

## Critical Constraints

- **Map the tests that exist — manual markdown cases, automated e2e tests, or both.** No unit tests. Do not suggest creating new tests.
- You may write to exactly three places, nothing else:
  - the coverage file — default `coverage.tests.yml`, or the path the user gave;
  - the `.testeiya/` cache dir — clone automated test repos, pull manual cases from Testomat.io (Step 1);
  - `.gitignore` — add a `.testeiya/` line if it is missing.
- **Never modify a source or test file.**
- Never pull or clone tests into a tracked folder — only into the gitignored `.testeiya/`.
- **Everything in the coverage file must come from this project:** file keys from its source tree, identifiers from the Step 2 inventory. Never copy a path or ID from this skill's docs — they are placeholders.
- **No ad-hoc scripts, no parsers, never Python.** File reads and `grep` only; the single exception is the bundled checker (Step 5); beyond that a one-line `node -e '…'` is the limit.
- **Be proactive — never stop at a representative sample.** A few entries per domain is a failed run. Keep mapping without asking permission to continue until the completion criterion in Step 4 is met.
- Stop if you cannot write the output file, or no tests are found and the user declines every option in Step 1.

## Workflow

### Step 1: Discover the project

- Run the `scan-automation-project` skill to inventory the project. Use its output as the source of truth — do not duplicate the scan.
- Capture from its result:
  - Manual Tests — the `.test.md` files and their suite/test titles.
  - Automated Tests — the e2e test files and framework(s). See [E2E Frameworks](./references/E2E_FRAMEWORKS.md) if the scan is ambiguous.
  - Project Overview — languages, frameworks, complexity (drives the subagent split in Step 4).
- Map whatever exists: both kinds go into one coverage file; a single kind is fine too.
- ❓ If the scan finds no tests at all (it checks the `.testeiya/` cache too), ask the user:
  1. Pull manual cases from Testomat.io — have `sync-test-cases-with-tms` pull into the cache: `npx check-tests pull -d .testeiya/manual-tests`, add `.testeiya/` to `.gitignore` if missing, re-run the scan.
  2. Clone the automated tests repo: `git clone <url> .testeiya/e2e-tests`, add `.testeiya/` to `.gitignore` if missing, re-run the scan.
  3. Point to a directory the scan missed, then re-run the scan there.
  4. Stop.
- ❓ If two automated frameworks are detected (say Jest and Playwright), ask which one is the e2e framework — coverage filtering runs per runner.

### Step 2: Extract test information

Build one inventory of identifiers across both kinds:

- Suite IDs — `@S` + 8 chars.
- Test IDs — `@T` + 8 chars.
- Tags — other `@word` markers.
- Context — titles, steps, page objects, routes hit. This drives the mapping in Step 4.

Where IDs live:

- Manual cases follow the [Classical Tests Markdown Format](../qa-write-test-cases/references/test-case-format.md) — IDs in `<!-- suite ... id: @S... -->` / `<!-- test ... id: @T... -->` blocks, tags in titles and `tags:` lines.
- Automated tests carry IDs in `describe` / `it` / `test` / `Feature` / `Scenario` titles — see [E2E Frameworks](./references/E2E_FRAMEWORKS.md).

Read the files, or `grep` the directories that hold the tests:

```bash
grep -rnE 'id:[[:space:]]*@[ST]' <dir>          # manual suite/test IDs
grep -rnoE '@[ST][0-9a-f]{8}' <dir>             # IDs in automated test titles
grep -rhoE '@[A-Za-z0-9_-]+' <dir> | sort -u    # every @token, tags included
```

Missing IDs mean the tests were never synced with Testomat.io — the reporter cannot select them:

- ❓ Manual files without IDs: ask whether to push them first via `sync-test-cases-with-tms`, or skip those files.
- Automated tests without IDs in most files: stop and instruct the user to run `npx check-tests@latest <Framework> "<glob>" --update-ids` first (per-framework commands: [E2E Frameworks](./references/E2E_FRAMEWORKS.md)).

### Step 3: Plan the coverage map by domain

**Do not crawl the codebase file by file.** Identify the application's domain areas first; Step 4 then maps area by area.

- Derive the areas from both sides:
  - the suite tree from Step 2 — the suite hierarchy is the QA team's own map of the product;
  - the source structure — modules, routes, services, entry points.
- Pair each area with the suites that test it and the source folders that implement it.
- Order the areas by criticality, most critical first: payments/billing, auth and access control, data integrity, core business flows — then supporting features, then peripheral UI. Suite size is a signal: what QA tests heavily, they consider critical.
- Show the ordered plan to the user before mapping.
- Business code only: skip test code, manual test directories, dependency/build/vendor folders, framework configs, lock files.
- **Templates and views are mappable source** (`.vue`, `.erb`, `.blade.php`, …) — tests check the rendered UI, so map them like code.
- ❓ If areas or their priority are unclear, ask the user.

### Step 4: Map source files to tests

**The Step 2 inventory is the work list. The map is complete only when every suite in it is either present in the coverage file or recorded as unmapped with a reason.** Work through the areas in Step 3's order — most critical first, so even an interrupted run covers what matters most. Run two passes — always both:

- Code → tests: for each area, map its source files and subtrees to the identifiers of the tests that check them.
- Tests → code: walk the inventory; for every suite still absent from the map, find the source it exercises and add it — or record why it cannot be mapped (feature has no code here, external system, needs user input).

Scale the passes to the project — codebase size and suite count from Step 1:

- Small codebase and few suites — run both passes in this session.
- Large codebase or dozens of suites — spawn subagents in parallel: one per domain area for the code→tests pass, then one per batch of still-unmapped suites for the tests→code pass. Give each subagent:
  - its slice — one area (its suites and source folders), or a batch of suites;
  - the full test inventory from Step 2 — subagents must not re-extract it;
  - the mapping rules below and the [Coverage File Format](./references/COVERAGE_FILE_FORMAT.md);
  - the instruction to return a YAML fragment for its slice only.
- Merge the fragments into one map, drop duplicate keys and empty entries. Only the main session writes the file (Step 5).

For each candidate source file, pick the identifier that keeps selecting the right tests as the test suite grows:

- Suite (`@S`) — the default. Most tests in the suite relate to the file.
- Tag (`@word`) — the relevant tests live across several suites.
- Test (`@T`) — the exception. Use only when just one or two tests in a suite match the file.

Rules:

- **More than a few test IDs from one suite or category → replace them with the suite or tag.** Tests added there later are picked up automatically; a list of test IDs goes stale.
- Never list a test ID whose suite is already in the same entry.
- Keys are source file paths or globs, relative to the repo root; use a glob when a whole subtree maps to the same identifiers.
- Manual and automated identifiers mix freely in one entry.
- No empty entries.
- Annotate each identifier with a `#` comment naming its suite/test/tag title.

YAML grammar: [Coverage File Format](./references/COVERAGE_FILE_FORMAT.md).

### Step 5: Save and validate the coverage file

- Write the YAML to the output path, keeping the `#` comments.
- Keys are paths to source files in this repo — never `.testeiya/...` paths.
- Check it with the bundled checker. It ships in this skill's `scripts/` directory (next to this SKILL.md), not in the project — resolve its path from the skill location:

```bash
npx js-yaml coverage.tests.yml | node <path-to-this-skill>/scripts/check-coverage.mjs
```

- The checker flags keys missing on disk and empty entries, and prints every identifier referenced — cross-check them against the Step 2 inventory; only you know which are real.
- Reconcile the other direction too: every suite in the inventory must appear in the file or in the unmapped list. Anything missing from both means the tests→code pass is not finished — go back to Step 4.

### Step 6: Report coverage completeness

Show the user:

- Suites mapped vs. total suites in the inventory; same for tests and tags where meaningful.
- Every unmapped suite with its reason.
- The produced YAML (or its path and entry count when large).

### Step 7: Show next steps

Tell the user how to use the file with `@testomatio/reporter`:

```bash
# Automated tests — the project's runner command must be passed in
npx @testomatio/reporter run "npx playwright test" \
  --filter "coverage:file=coverage.tests.yml,diff=main"

# Manual tests — creates a pending run with only the affected cases
npx @testomatio/reporter run --kind manual \
  --filter "coverage:file=coverage.tests.yml,diff=main"
```

- Per-framework runner commands and a GitHub Actions example: [Coverage File Format](./references/COVERAGE_FILE_FORMAT.md).
- To group manual and automated runs of one regression cycle, set the same `TESTOMATIO_RUNGROUP` env var on both commands.
- Recommend committing the coverage file so CI and teammates use the same mapping.
- In CI, diff against the base branch — `diff=origin/main` — and checkout with `fetch-depth: 0`.
- Pulled or cloned tests stay in the gitignored `.testeiya/` cache for re-runs — don't delete it or move it into a tracked folder.

### Step 8: Suggest follow-ups

- Wire the map into CI — runs created per PR and launched on preview/merge: delegate to `setup-change-aware-pr-testing`.
- Run the affected tests right now from the terminal: delegate to `run-tests-with-testomatio-reporter`.
- Coverage gaps — source features no test maps to. On approval, propose new cases (delegate to `qa-write-test-cases`).
- Dead tests — tests whose features no longer exist in source.
- Answer questions like "do we have tests for X?" from the inventory.
- Editing pulled manual cases: edit them in `.testeiya/manual-tests/` and push back with `sync-test-cases-with-tms`.

## References

- [Coverage File Format](./references/COVERAGE_FILE_FORMAT.md) — coverage YAML grammar, reporter contract, GitHub Actions example.
- [E2E Frameworks](./references/E2E_FRAMEWORKS.md) — framework detection signals, where IDs live, per-framework `check-tests` commands.
- [Manual test markdown format](../qa-write-test-cases/references/test-case-format.md) — canonical, owned by `qa-write-test-cases`.
