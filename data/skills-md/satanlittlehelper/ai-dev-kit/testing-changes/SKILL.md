---
name: testing-changes
description: Use when the user asks to test the current changes by hand — "протестируй изменения", "проведи тестирование", "проверь изменения руками", "test my changes", "manual QA" — or before declaring a branch done. Requires project infrastructure (DB, Redis, proxy) to be up already.
---

# Testing Changes

## Overview

Manual end-to-end test run of the current branch: analyze the changes, write a test plan, start every app, run the tests, show a report, stop what this run started once the report is approved, delete the test plan and the report. **The test plan is written and saved before anything starts, but it is not sent for approval; nothing this run started outlives the run.**

## Phases

| # | Phase | Read |
|---|---|---|
| 0 | Preconditions: infrastructure is up, no stale run | `references/environment.md` § Preconditions |
| 1-2 | Analyze changes and task documents, write and save the test plan | `references/test-plan.md` |
| 3 | Check Playwright MCP and Max login, start all apps, write the state file | `references/environment.md` |
| 4 | Run the tests, record actual vs expected | `references/execution.md` |
| 5 | Write the report, show it through Plannotator; the apps keep running while the user reviews | `references/report.md` |
| 6 | Stop every app this run started, once the report is approved (or the review is dismissed, or the run is aborted). On approval also delete the test plan and the report | `references/environment.md` § Teardown, § Cleanup of documents |

Read each reference when you reach its phase, not upfront.

## Hard rules

- The test plan and the report are written in Russian (code, commands, identifiers stay as-is).
- The test plan is not sent for approval: no Plan Mode, no waiting. Write it, save it, run it.
- Never start infrastructure. If it is down, stop and say what is down.
- API → `curl`. Frontend → Playwright (the backend is covered through the page's own requests). Max bot or Max mini app → the web version of Max only. Existing e2e specs that cover a changed behavior join the plan.
- Start the whole monorepo: every app, including those the tests do not touch, without asking which. Use only the project's own commands (`testing.apps[].start` or `start:*` scripts). Never override env vars or add `NODE_TLS_REJECT_UNAUTHORIZED=0`.
- Record every app in `tmp/test-run-state.json` the moment it starts. Stop every `owned: true` entry in Phase 6. An app that already answers before you start it is not yours: do not start or stop it.
- On report approval only: delete the test plan file and the run's temp files (app logs), and the report with its evidence in `tmp/reports/<run>/`, without asking. Dismissed review or abort: delete nothing.
- Never fix code, commit, or push during a test run. Report failures; fix only on request.
- Playwright runs headless; open a visible window only for the Max login (`references/environment.md`). Logging in is the user's job: never type a phone number or a code.
- Bash: no `cd`, no `sleep` chains (use Monitor), one check per call.

## Project config

Project values live in `.claude/dev-conventions.json` under `testing` (schema in `references/environment.md`). No such block: discover `start:*` scripts in `package.json`, show them in the plan, offer to save them to the config.

## Common mistakes

| Mistake | Fix |
|---|---|
| Starting apps before the plan is written and saved | Phase 3 begins only after the plan file is saved |
| Killing only the parent `npm`/`nx` process | Kill the process group (`kill -- -<pgid>`) and verify the ports are free |
| Reporting "passed" without actual results | Every test gets expected vs actual |
