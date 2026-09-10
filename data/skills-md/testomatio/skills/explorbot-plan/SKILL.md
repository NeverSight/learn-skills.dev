---
name: explorbot-plan
description: Use when the user wants to write an Explorbot test plan by hand — from a feature description, requirements, ticket, or docs, without exploring a live page — so `explorbot test` can run it.
license: MIT
metadata:
  author: Testomat.io
  version: 0.1.0
---

# Writing Explorbot Test Plans

Write an Explorbot **test plan** by hand in Explorbot's exact markdown format, from a feature
description / requirements / docs and a starting URL. No browser or live exploration needed.

**Explorbot does not need to be installed to author a plan** — it is just a markdown file.
Installation is only required later to *run* the plan (see Output).

## Inputs to gather

- The feature / requirements / user story (ask for docs or a description).
- A suite title (the feature under test).
- The **start URL**: a path relative to the app host (e.g. `/login`), or a full absolute URL.
  This is mandatory. Relative paths resolve against `web.url` in a project config, or against
  the site the command names (`EXPLORBOT_URL` / a registered host) in global mode.
- Optional per-test start URLs when a scenario begins on a different page.
- Priority for each scenario: `critical`, `important`, `high`, `normal`, `low`.

## Format

```markdown
<!-- suite -->
# User Authentication

### Prerequisite

* URL: /login

<!-- test
priority: critical
-->
# User signs in with valid credentials

## Requirements
/login

## Steps
* Enter a registered email in the email field
* Enter the matching password
* Submit the sign-in form

## Expected
* The user lands on the authenticated dashboard
* The signed-in account is shown in the header

<!-- test
priority: high
-->
# Sign-in is rejected for an unknown account

## Requirements
/login

## Steps
* Enter an unregistered email and any password
* Submit the sign-in form

## Expected
* An invalid-credentials error is shown
* The user stays on the sign-in page
```

## Rules

- `<!-- suite -->` then the **next line** is `# Suite Title`. One suite per file is normal;
  add more by repeating `<!-- suite -->`.
- `### Prerequisite` — its **first list item** must be `* URL: <path>`. This documents the
  suite-wide start page for readers and the TUI. A relative path resolves against `web.url` /
  `playwright.url`; absolute URLs work too.
- Each test: a `<!-- test` … `priority: <level>` … `-->` block, then `# Scenario` (h1).
  Missing priority defaults to `normal`.
- **Give every test its own `## Requirements` line with the start URL** (same value as the
  Prerequisite, unless the scenario starts elsewhere). Execution reads the per-test
  `## Requirements` URL; a test with no `## Requirements` may have no start URL and fail to
  run. The canonical generated plans repeat the URL in every test for this reason.
- `## Steps` and `## Expected` use `* ` bullets; wrap a long bullet by indenting continuation
  lines two spaces.
- Steps are **guidance** — the Tester adapts them; keep each step atomic and free of brittle
  selectors. Every `## Expected` bullet must be **independently verifiable** (a data change,
  state change, or UI change with a real side effect), not a restated step.
- Scenario titles describe a **business outcome**, not a click path.

## Output

A hand-written plan is input only — Explorbot never rewrites it, so keep it in the repo next to
the code it covers (`tests/plans/<feature>.md` or similar) and pass its path to `explorbot test`.
Save it under the run's `output/plans/` only when the user wants it alongside generated plans:
`output/plans/` in a project setup, `~/.explorbot/sites/<host>/output/plans/` in global mode.

Run it (index: `1`, `1,3`, `1-5`, or `*` for all):

```bash
npx explorbot test checkout-plan.md '*'
EXPLORBOT_URL=https://app.example.com npx explorbot test checkout-plan.md '*'
```

`test` takes no URL argument: it uses `web.url` from a project config, and needs `EXPLORBOT_URL`
in global mode. It exits `0` whenever the session completes — read the report in
`output/reports/`, not the exit code. See [[explorbot-fundamentals]].
