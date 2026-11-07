---
name: xray-testing
description: Use when the user says 'pull test PROJ-T42', 'create Xray test from this AFS', 'upload JUnit to test plan', or performs any Xray CRUD. CRUD plus results import on Xray entities (Test, Precondition, Test Set/Plan/Execution/Run) across Cloud (GraphQL) and Server/DC (REST).
license: Apache-2.0
metadata:
  authors:
    - Alexander Bychinskiy <alexander_bychinskiy@epam.com>
    - Artem Rozumenko <artem_rozumenko@epam.com>
  version: "0.1.0"
---

# Xray — the TMS that lives inside Jira

Xray stores test cases and execution records as Jira issues of
specific issue types (`Test`, `Precondition`, `Test Set`,
`Test Plan`, `Test Execution`). That design is why this skill is
separate from `atlassian-content`: the **Jira issue layer** (ADF,
comments, mentions) is covered there; **everything Xray-specific**
(test steps, preconditions, test run statuses, results import,
coverage links) lives here and talks to Xray's own API.

This skill is **transport-agnostic** (GraphQL / REST / MCP /
connector) and **deployment-agnostic** (Cloud or Server / DC).

## When to load this skill

Load when the task involves reading, authoring, linking, or
recording results against Xray entities:

- Fetching a Test's steps (structured, not the Jira description)
- Creating a Test / Precondition / Test Set / Test Plan
- Adding or editing steps on a Test
- Adding Tests to a Test Set / Test Plan
- Creating a Test Execution and reporting Test Run results
- Importing results from JUnit / Cucumber / NUnit / TestNG /
  generic Xray JSON
- Linking a Test to a story / requirement / bug for coverage
- Querying coverage ("which tests cover PROJ-42?" /
  "which requirements have no tests?")

Do NOT load for: pure Jira field reads / comment authoring on
Xray issue keys — those don't need Xray-specific endpoints.
Use `atlassian-content` for that.

## Transport priority — check in this order on every call

**MCP is first. The CLI is a fallback. Raw REST / GraphQL is a
last resort.** Never default to `scripts/xray.py` when an MCP
tool already covers the operation — secrets stay out of agent
context when you go through MCP, and an MCP-wired project has
already invested in permissions / audit / reliability the CLI
can't match.

1. **MCP tools** — `mcp__<server>__<toolset>_*`
   (e.g. `mcp__Elitea_Dev__JiraIntegration_get_issue_details`,
   `mcp__dmtools-cli__xray_get_test`, `mcp__mcp-xray__*`). Discover
   with the host's MCP-listing command (`copilot --list-mcp`,
   `claude mcp list`, Cursor / Windsurf settings panel) and match
   the tool to the operation. Use the MCP if a matching tool
   exists, even if the skill's examples show CLI commands.
2. **Bundled CLI** — `scripts/xray.py` (stdlib Python, zero deps).
   Only when no MCP tool covers the operation, or when the MCP
   server is offline. The CLI auto-detects Cloud vs Server,
   caches JWTs, and bakes in the re-fetch + validate discipline
   (exit 3 on mismatch). See `scripts/README.md` for the surface.
3. **Raw REST / GraphQL** — assemble your own HTTP call. Reserve
   for debugging or when both MCP and the CLI are unavailable.

If you start an operation on MCP and hit a gap (missing tool,
auth error, stale cache), log the gap clearly in your reply,
drop down to the CLI, and surface the gap in your summary so the
operator can fix the MCP config.

Agents are allowed (and encouraged) to fix / extend `scripts/xray.py`
when they hit a bug or missing capability. Rules of the road —
preserve exit codes and env-var names, stdlib-only, re-fetch-and-verify
on every new write, syntax-check before commit — live in
[`scripts/README.md` § Extending this script](scripts/README.md).

## Absolute boundaries

- **Don't fake a Test by POSTing a plain Jira issue with
  `issuetype=Test`.** Xray requires its own REST / GraphQL calls
  to populate `Test Type`, step list, preconditions, and scenario
  body. Creating the Jira issue alone leaves an empty Xray Test.
- **Don't put test steps into the issue description.** Xray's
  steps live in a separate structured store. The Jira
  `description` field is a free-text sibling, not the spec.
- **Don't invent a test `Status` value.** Xray statuses are
  project-configurable (defaults: `PASSED`, `FAILED`,
  `EXECUTING`, `TODO`, `ABORTED`, `BLOCKED`). If you don't know
  which statuses this project uses, query them first; do not
  guess.
- **Don't upload result files you haven't verified.** JUnit and
  Cucumber XML/JSON shapes vary between runners — a mis-shaped
  report uploads silently as zero results. Always confirm the
  created Test Execution has the expected Test Run count after
  import.
- **Don't rewrite step IDs.** Steps have opaque IDs. When
  updating, fetch, modify in place, and submit — don't
  regenerate the step list from scratch (you'll orphan execution
  history).
- **Don't leave a new Test orphaned from its story.** When you
  create a Test that covers a user story / requirement / bug,
  you MUST link it via Xray's **coverage link** —
  `addTestsToRequirement` (Cloud GraphQL) /
  `POST /api/test/<key>/requirement` (Server REST) — or
  `xray test link-requirement <TEST> <STORY>` from the CLI. The
  plain Jira `issuelinks` field (`Tests` / `Is tested by`) does
  NOT register coverage in Xray's reports on modern Cloud
  installs. If you skip this step, coverage rollups show the
  story as "uncovered" even though the Test exists — a silent
  bug in triage. See § "Link Tests to stories" below for the
  full rule.

## Deployment — Cloud vs Server / DC

| Trait | **Xray Cloud** | **Xray Server / DC** |
|---|---|---|
| Primary API | GraphQL (`/api/v2/graphql`) | REST (`<jira>/rest/raven/2.0`, `/1.0`) |
| Auth | JWT from `/api/v2/authenticate` (client_id + client_secret) | Basic auth or PAT against Jira |
| Typical base URL | `https://xray.cloud.getxray.app/api/v2` | `https://<your-jira>/rest/raven/2.0` |
| Entity keys | Jira keys (`PROJ-T42`) | Jira keys (`PROJ-T42`) |
| Project scope | Xray app per Atlassian tenant | Xray app per Jira instance |

The **entity model is identical** across both. Only the transport
differs. Detect which one you're on from the project's
`.agents/profile.md` § Project systems and the adapter declared
in `.agents/test-automation.yaml`:

```yaml
# .agents/test-automation.yaml
tms:
  adapter: xray
  deployment: cloud        # or: server
  base_url: https://xray.cloud.getxray.app/api/v2
  auth_env: XRAY_CLIENT_ID, XRAY_CLIENT_SECRET   # cloud
  # auth_env: JIRA_TOKEN                         # server
  jira_base_url: https://your-site.atlassian.net
```

If `.agents/test-automation.yaml` doesn't exist yet (project not
seeded, or the test-automation pipeline skill isn't installed),
the bundled CLI falls back to reading env vars directly —
`XRAY_DEPLOYMENT`, `XRAY_CLIENT_ID`/`XRAY_CLIENT_SECRET` +
`JIRA_BASE_URL` for Cloud, or `JIRA_TOKEN` + `JIRA_BASE_URL` for
Server. Ask the operator for those values before running against
an unseeded repo; see `scripts/README.md` § Configure via
environment.

If MCP is wired in (`Elitea_Dev`, `dmtools-cli`, `mcp-xray`, …),
prefer the MCP tool — it usually normalizes Cloud vs Server
under one interface.

If no MCP is available, use the bundled CLI at
[`scripts/xray.py`](scripts/xray.py) (stdlib-only Python,
`scripts/README.md` for the full surface). The CLI auto-detects
Cloud vs Server from env, caches JWTs, and bakes in the
post-write re-fetch discipline (exit 3 on mismatch). Common ops:

```bash
xray auth-verify                          # reachability + status set check
xray test get PROJ-T42                    # summary + step list (Cloud: needs Jira creds)
xray test get --issue-id 10042            # bypass Jira: use a known issueId directly
xray test create --project PROJ --summary "..." --type Manual --steps steps.txt
xray exec create --project PROJ --summary "Smoke 04-22" \
  --tests PROJ-T42,PROJ-T43 --plan PROJ-P7
xray import junit target/junit.xml --project PROJ --plan PROJ-P7
```

**Jira creds are command-scoped.** Cloud's Xray-only commands (`config`,
`auth-verify`, `statuses`, `run *`, `import *`) work with **only** `XRAY_*`
set. Anything that translates a Jira key → numeric `issueId` (`test *`,
`testset *`, `testplan *`, `exec create`, `coverage`) needs `JIRA_BASE_URL`
+ `JIRA_USER` + `JIRA_TOKEN`. If you already have the `issueId` from
elsewhere — Atlassian MCP, prior CLI call, JQL search — pass `--issue-id`
where supported and skip the Jira-REST hop entirely.

## Entity model + coverage linking

### The six entities Xray tracks

| Entity | Jira issue type | Purpose |
|---|---|---|
| **Test** | `Test` | Single test case. Test Type: Manual / Cucumber / Generic. |
| **Precondition** | `Precondition` | Shared setup steps referenced by multiple Tests. |
| **Test Set** | `Test Set` | Named grouping — "smoke", "regression-P1". No execution semantics. |
| **Test Plan** | `Test Plan` | Planning container — "Release 2.7 QA sign-off". Aggregates latest Test Run status. |
| **Test Execution** | `Test Execution` | Single run event. Contains one **Test Run** per Test executed. |
| **Test Run** | (inside a Test Execution) | Status + evidence + comments for one Test in one Execution. Run ID, not Jira key. |

```
Requirement (Story / Bug) ──covered by── Test
                                          ├── Precondition(s)
                                          ├── in Test Set(s)
                                          └── in Test Plan(s)
                                                           │
                                                           └─ executed via
                                                              Test Execution → Test Run
```

A Test Run is never standalone — it only exists as a row inside a
Test Execution. "Reporting a result" means posting to the Test Run
that belongs to (Test Execution × Test).

Full field list per entity + Test Type specifics:
[`references/entities.md`](references/entities.md).

### Coverage linking — the non-negotiable rule

Creating a Test for a story and stopping there is half-finished.
The story will show "no tests" in Xray's coverage reports until
you link them — and the link is **not** a standard Jira
`issuelinks` entry.

> **Rule:** every Test created to validate a story / requirement /
> bug MUST be linked via Xray's coverage link, *in the same unit
> of work* as the Test creation. If the Test covers nothing (pure
> infra / CI-smoke), document that explicitly in the Test
> description.

| Deployment | Call |
|---|---|
| Cloud (GraphQL) | `addTestsToRequirement(issueId: <STORY>, testIssueIds: [<TEST>])` |
| Server / DC (REST) | `POST /rest/raven/2.0/api/test/<TEST>/requirement` body `{ "add": ["<STORY>"] }` |
| CLI (either) | `xray test link-requirement <TEST-KEY> <STORY-KEY>` |
| MCP (if available) | typically `*.add_tests_to_requirement` — prefer MCP when present |

The plain Jira "Tests" / "Is tested by" `issuelinks` does **not**
register coverage in modern Xray Cloud reports — it's free-text
traceability, not a coverage edge. Use the native call above.

**Verify after linking** (cloud GraphQL):
`getCoverableIssue(issueId: <STORY>) { tests { results { jira(fields:["key"]) } } }`
— expect the new Test key. CLI equivalent:
`xray coverage <STORY>`. If the list is empty, inspect
`addedTests` / `warning` in the link response and re-link.

Skip coverage only when the Test genuinely covers nothing (infra /
CI-smoke) — and document that in the Test body.

## The CRUD loop (every call, every time)

Mirrors the discipline of `atlassian-content`:

```
0. If updating: raw-fetch the current entity (Cloud GraphQL
   returns structured fields; Server REST returns JSON). Merge
   your change; don't regenerate.
1. Detect deployment   → Cloud (GraphQL) or Server (REST)?
2. Detect entity       → Test, Precondition, Set, Plan, Execution, Run?
3. Resolve identities  → Jira keys, accountIds (for assignee/executedBy),
                         test run IDs (inside an Execution)
4. Assemble body       → GraphQL variables or REST JSON per
                         references/cloud-graphql.md / server-rest.md
5. Submit              → MCP tool or HTTP call
6. Re-fetch            → GET the updated entity back
7. Validate            → counts match (steps, tests in set, runs in
                         execution); statuses are permitted values;
                         no orphaned links
8. Repair              → fix in place; don't leave a half-written
                         execution
```

### 0. Raw-fetch first (for any update)

Same rule as atlassian-content: fetch the current entity body in
its **structured form** before editing. For Xray this is:

- Cloud GraphQL: query the fields you're about to modify
  (`steps { id action data result }`, `preconditions { issueId }`,
  `tests { issueId }`, …).
- Server REST: `GET /rest/raven/2.0/api/test/<key>` etc.

**Applies regardless of transport** — raw GraphQL / REST, MCP
server (`Elitea_Dev`, `dmtools-cli`, `mcp-xray`), or any
Atlassian-connected integration. Choose the variant that returns
structured fields, not a human-readable summary.

Reason: step IDs, run IDs, and evidence attachments are opaque
values — regenerating them from scratch loses history and breaks
references from Test Plans / Test Executions that already
reference them.

### 1–2. Detect deployment + entity

Branch once here. Every subsequent call uses one family of
endpoints for the rest of the loop.

### 3. Resolve identities

- **Jira keys** — you usually already have these
  (`PROJ-T42` / `PROJ-123`).
- **accountId** (Cloud) — for `assignee`, `executedBy`, comment
  authorship. Use the lookup in `atlassian-content/mentions.md`.
- **issueId** — Xray's GraphQL often expects internal Jira
  `issueId` (numeric) rather than the `issueKey`. Resolve with
  `GET /rest/api/3/issue/<key>?fields=summary` — the `id` field
  in the response is the numeric id.
- **testRunId** — obtain from the Test Execution:
  `getTestExecution(issueId: ...) { testRuns { results { id test { jira { key } } } } }`
  (Cloud) or `GET /rest/raven/2.0/api/testexec/<key>/test` (Server).

### 4. Assemble body

- Cloud → GraphQL — see `references/cloud-graphql.md` for
  queries, mutations, and authentication flow.
- Server → REST — see `references/server-rest.md` for endpoints
  and JSON shapes.
- Results import → see `references/results-import.md` for
  JUnit / Cucumber / Xray JSON formats.

### 5–8. Submit, re-fetch, validate, repair

The re-fetch step proves what you intended actually landed:

- **Test creation** → re-fetch the Test; confirm `testType`,
  step count, any precondition links.
- **Results import** → re-fetch the Test Execution; confirm the
  Test Run count matches the number of cases in the report, and
  statuses are the expected values.
- **Linking** → re-fetch the Test (or the requirement); confirm
  the link appears on both sides.

If counts don't match or statuses are wrong, the report shape
was off — fix the report and re-import.

## Common task shapes

The CRUD loop above applies to every task. Three common flows, as
checklists:

**Create Manual Test from AFS covering PROJ-123** — detect deployment
→ resolve project key + assignee accountId + preconditions + story
key → POST new Test (GraphQL `createTest` or REST
`POST /api/test`) → link coverage
(`addTestsToRequirement(PROJ-123, [<new>])`) → re-fetch Test for step
count AND re-fetch PROJ-123 coverage for the new Test key.

**Import JUnit results against Test Plan PROJ-P7** — build
Xray-recognized JUnit XML (classname / name mapped to Jira keys per
the adapter config) → `POST /import/execution/junit?testPlanKey=PROJ-P7`
→ re-fetch the returned Test Execution → run count must equal
`<testcase>` count. Zero = broken mapping (silent-fail signature).

**Add Test PROJ-T42 to Test Set PROJ-TS10** — raw-fetch PROJ-TS10 →
skip if already present → `addTestsToTestSet` (Cloud) or
`POST /api/testset/<TS10>/test` (Server) → re-fetch to confirm.

Full request/response shapes: `references/cloud-graphql.md` (Cloud),
`references/server-rest.md` (Server), `references/results-import.md`
(imports).

## Anti-patterns

- **"I created the Test issue in Jira, why is Xray empty?"** —
  Xray tracks Test Type, steps, scenarios in its own store.
  Creating the Jira issue alone leaves an empty Test. Use the
  Xray mutation / REST.
- **"I imported the JUnit report and the response was 200, but
  the Test Execution is empty."** — 200 often means "accepted
  the upload". Zero runs = bad mapping between your
  `classname`/`name` and Jira Test keys. See the import
  reference.
- **"I updated the step list but the execution history
  disappeared."** — You regenerated step IDs. Never reassign
  step IDs; fetch, edit in place, submit.
- **"I assigned a Test Run status that Xray rejected."** —
  Statuses are project-configurable. Query allowed values
  (`getStatuses` GraphQL query) first.
- **"I link the Test to the story via Jira's `links` field."**
  — That works for free-text traceability but doesn't register
  coverage in Xray's reports on modern Cloud installs. Use
  Xray's `addTestsToRequirement` (Cloud GraphQL) or
  `/api/test/<key>/requirement` (Server) so coverage rolls up.
  See § "Link Tests to stories" above.
- **"I created a Test for the story and moved on without
  linking it."** — Coverage reports will show the story as
  uncovered even though the Test exists. Linking is part of
  "creating a Test for X", not a follow-up task.
- **"I POSTed a JSON body with `markdown` formatting."** — Xray
  fields that accept rich text follow the same rule as
  `atlassian-content`: Cloud uses ADF, Server uses wiki markup.
  Test step text is typically plain text; check the field docs.

## Escalation

Ask the operator when:

- The project uses a non-default set of Test Run statuses and
  none are declared in `.agents/profile.md`.
- A Test requires custom fields (defined per-project) that
  aren't documented.
- The results-file format doesn't match any supported importer
  (e.g. Robot Framework when no Xray Robot plugin is installed).
- Coverage links are expected to a custom issue type (some teams
  cover Epics, others cover Stories only — ask which).

## References

- `references/cloud-graphql.md` — Xray Cloud API v2: auth flow,
  core queries (`getTests`, `getTestExecution`, `getStatuses`,
  `getCoverableIssue`), core mutations (`createTest`,
  `updateTestSteps`, `addTestsToTestSet`, `addTestRuns`),
  fragments, pagination.
- `references/server-rest.md` — Xray Server / DC REST endpoints
  for Test / Precondition / Test Set / Test Plan / Test Execution
  / Test Run, including JSON examples and the `import/execution/*`
  endpoints.
- `references/entities.md` — Test Types (Manual / Cucumber /
  Generic), field-by-field reference per entity, coverage model.
- `references/results-import.md` — JUnit, Cucumber JSON, TestNG,
  NUnit, and generic Xray JSON result formats; classname/name
  mapping; validation after import.
- `scripts/xray.py` + `scripts/README.md` — stdlib-only Python
  CLI covering every operation above; the HTTP fallback to use
  when an MCP tool isn't wired. Agents are explicitly allowed to
  fix / extend the script when they hit bugs or missing
  capabilities — see § Evolving the CLI above.
- `references/jira-rest-fallback.md` — what's still reachable
  when the Xray API itself is unreachable (credentials rejected,
  regional mismatch, outage). Jira REST alone lets you list /
  filter Tests by type, read issue shells, and file defects; it
  does NOT expose structured Test bodies or Test Runs.

External — primary sources:

- Xray Cloud GraphQL: https://xray.cloud.getxray.app/doc/graphql/
- Xray Cloud REST (v2): https://docs.getxray.app/display/XRAYCLOUD/REST+API
- Xray Server / DC REST: https://docs.getxray.app/display/XRAY/REST+API
- dmtools-cli Xray module (for patterns / examples):
  https://github.com/IstiN/dmtools-cli/tree/main/dmtools-core/src
- Elitea SDK Xray tools:
  https://github.com/EliteaAI/elitea-sdk/tree/main/elitea_sdk/tools/xray
