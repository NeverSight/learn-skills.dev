---
name: testomatio-mcp
description: Configures and leverages the Testomat.io MCP server for test management analytics, run analysis, failure investigation, and defect triage. Use when the user needs to connect to Testomat.io via MCP, analyze test runs, cluster failures, investigate root causes.
license: MIT
metadata:
  author: Testomat.io
  version: 1.0.0
---

# Testomatio MCP

Set up access to Testomat.io via MCP and run QA analysis workflows: run analysis, failure clustering, root-cause investigation, plan analysis, defect triage.

## When to Use

- Detect or set up the Testomat.io MCP server for an AI agent (Claude, Cursor, OpenCode, etc.).
- Analyze test runs: recent results, success rates, failure trends.
- Investigate failures: group similar failures, find patterns.
- Find the root cause when many tests fail with the same issue.
- Create defects from failed tests in the user's issue tracker (e.g. Jira).

## MCP Tools

- Test: `tests_list`, `tests_get`, `tests_search`
- Test Plan: `plans_list`, `plans_get`, `plans_search`
- Run: `runs_list`, `runs_get`, `runs_search`
- Testrun (results within a run): `testruns_list`, `testruns_get`
- Suite: `suites_list`, `suites_get`, `suites_search`
- Label: `labels_list`, `labels_get`, `labels_create`, `labels_update`, `labels_delete`. Labels may be scoped (`key:value`). Attach or swap them on entities via the `link` parameter — [MCP Setup Reference](./references/MCP_SETUP.md).
- Tag: `tags_list`, `tags_get`, `tags_search`

**CRUD tools (create, update, delete) exist for all entities. Use them only when explicitly needed for targeted updates.**

## Rules

- **Prefer local tests over MCP.** If the repo contains markdown test cases (`*.test.md`) or automated test files, read them from the filesystem (or load them via the `sync-test-cases-with-tms` skill) instead of using MCP for full test discovery and analysis.
- Use MCP for:
  - reading and analyzing run reports
  - analytics and reporting
  - test plan management
  - tests that live exclusively in Testomat.io (no local copies), or quick test case searches (`tests_list`, `tests_search`)
  - targeted searches and point updates to remote test cases
- Filter `runs_list`, `plans_list`, `testruns_list` with TQL (Testomat.io Query Language). Operators and examples: [MCP Setup Reference](./references/MCP_SETUP.md).

## Setup

### Step 1: Detect Existing Configuration

Check the user's AI agent config files for a `testomatio` or `mcp.testomatio` entry:
- `opencode.json`
- `.cursor/mcp.json`
- `claude_desktop_config.json`
- other, based on the user's local agent

Validate:
- the server is enabled (when the client supports enable/disable flags)
- `TESTOMATIO_PROJECT_TOKEN` and `TESTOMATIO_PROJECT_ID` are present

Configured and enabled → go to Workflows. Missing, incomplete, or disabled → Step 2.

### Step 2: Configure MCP

Before configuring:
- Prefer confirming the project contains no more than 1000 tests.
- If project size cannot be determined, warn the user about MCP performance limits on large projects.
- **Use only targeted or filtered operations when explicitly requested.**

Credential priority for `TESTOMATIO_PROJECT_TOKEN` and `TESTOMATIO_PROJECT_ID`:
1. Existing environment variables.
2. Existing MCP configuration.
3. User-provided values.

Per-agent config formats (OpenCode, Cursor, Claude Desktop) and where to obtain credentials: [MCP Setup Reference](./references/MCP_SETUP.md).

**Rules:**
- **Do not overwrite unrelated MCP server configurations.** Merge changes carefully with existing config content.
- **Do not expose project tokens, secrets, or credentials in chat responses.**

After successful configuration, confirm with a summary:

```text
Testomat.io MCP configuration completed successfully.

AI Agent: Cursor
Config Updated: `.cursor/mcp.json`
MCP Server: Enabled
Authentication: Verified

Available workflows:
- Test run analysis
- Failure clustering
- Root-cause investigation
- Plan analysis & defect triage
```

## Workflows

Common patterns, not a complete list — adapt and extend to the user's needs. All assume the MCP server is enabled.

### Workflow 1: Analyze Test Runs

Goal: understand the health of recent test execution.

1. Call `runs_list` with `tql` filters (e.g. `finished`, `failed`, `with_defect`); narrow scope by status, environment, or plan.
2. Select a run of interest and call `runs_get` for detailed metadata.
3. Call `testruns_list` with `run_id` and `filter_status: failed` to extract failed results.
4. Summarize: total tests, passed, failed, skipped, environments involved.
   - Compare success/failure ratios across runs to spot regressions.

### Workflow 2: Failure Investigation & Error Clustering

Goal: determine what went wrong and which areas are affected.

1. Call `testruns_list` (`filter_status: failed`, `run_id`) to get failed results.
2. For each failed testrun, call `tests_get` to map it to its suite, priority, tags, and linked issues.
3. Cluster failures:
   - by `suite_id` → identify the suite with the highest failure count
   - by `message` substring → find tests failing with the same exception or assertion
4. Present clusters ranked by count, with suite and message breakdowns and affected test titles.

### Workflow 3: Plan Analysis & Root-Cause Detection

Goal: when many tests fail with the same issue, explain the root cause.

1. Call `plans_get` (if a plan is linked to the run) to understand the intended scope; check whether failures correlate with specific plan sections.
2. Call `runs_list` with `tql` targeting the same plan or environment to get historical runs.
3. Compare failures across runs:
   - increasing failure count → new regression
   - same failures across multiple runs → stable bug or flaky infrastructure
   - spike in a single suite or tag → localized code change, feature regression
   - scattered across unrelated suites → systemic issue (infrastructure, config, dependency)
4. Call `tests_get` on affected tests to check `code`, `state`, and linked issues.
5. Report a root-cause hypothesis.

Example — user asks: "Check why 20 tests failed in the last run — one suite or a systemic issue?"

```text
1. Detecting existing Testomat.io MCP configuration:
   - Found `.cursor/mcp.json`
   - Found `testomatio` MCP server entry
   - MCP server status: enabled

2. Verifying MCP availability...
   - Authentication successful
   - Testomat.io tools available

3. Analyzing latest test run...
   - Retrieved last completed run
   - Total failed tests: 20

4. Failure clustering summary:
   - 16/20 failures belong to suite: "Checkout / Payments"
   - 14 failures share the same error: "Timeout waiting for payment confirmation"
   - First failure timestamp indicates failures started simultaneously

5. Probable root cause:
   - The failures appear systemic rather than test-specific.
   - Most failures point to instability or outage in the payment gateway service used during checkout flows.
```

### Workflow 4: Defect Creation from Failed Tests

Goal: turn recurring failures into trackable defects.

1. Run Workflow 2 to cluster failures by message.
2. If a cluster contains 5+ tests with the same failure:
   - propose creating a defect (e.g. Jira issue) to the user
   - draft the defect summary: title, description, affected test titles, failure messages, run link, environment
   - if a Jira MCP is available, offer to create the ticket via the Jira skill
3. After defect creation, call `tests_issues_link` for each affected test to link it to the defect.

### Workflow 5: Update Labels & Tags on Tests

Goal: set, change, or remove labels and tags on tests — for example, update a status label that drives a dashboard chart.

1. Call `labels_list` (or `project_info`) to read the exact label values that exist in the project, including the full `key:value` form of scoped labels. Do not guess label strings.
2. Optionally find the tests to update with `tests_list` + TQL: `label == 'regression:yes'`.
3. Update with `tests_update` (or `tests_create`) using the `link` array — one `{ action, type, value }` entry per change. To change a value (e.g. `regression:no` → `regression:yes`), send a `remove` and an `add` in the same call. The same shape works for `tag`, `custom_field`, `milestone`, `issue`, and `jira`.

Link format and a full swap example: [MCP Setup Reference](./references/MCP_SETUP.md).

## Quick Commands

| Action              | MCP Tool        | Key Parameters |
|---------------------|-----------------|----------------|
| List failed results | `testruns_list` | `run_id`, `filter_status: failed` |
| List runs           | `runs_list`     | `tql`, `page`, `per_page` |
| Get run details     | `runs_get`      | `run_id` |
| Get test details    | `tests_get`     | `test_id` |
| Get plan details    | `plans_get`     | `plan_id` |
| Link issue to test  | `tests_issues_link` | `test_id`, `url` or `jira_id` |
| List labels         | `labels_list`   | `page`, `per_page` |
| Set / swap label on test | `tests_update` | `test_id`, `link` |
| Find tests by label | `tests_list`    | `tql: label == '...'` |
| Check server status | `system_ping`   | none |
