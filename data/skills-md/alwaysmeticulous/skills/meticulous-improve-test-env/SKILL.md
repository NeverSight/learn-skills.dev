---
name: meticulous-improve-test-env
description: Work out what to change in a project's test environment so Agent swarm stops getting blocked when it tests against a live backend — seed better test data, widen the test user's permissions, enable feature flags, fix test login, and so on. Reads the setup blockers Agent swarm has recorded, inspects the codebase and test-environment configuration, and proposes concrete fixes. Use when Agent swarm cases are blocked by the environment rather than by the app, or when asked to "improve the test environment", "fix Agent swarm setup blockers" or "why is Agent swarm blocked".
user-invocable: true
---

When Agent swarm tests a pull request against a live backend (rather than with mocked network responses), it can only verify what the test environment lets it reach. A case it couldn't verify because of the environment — no records to act on, a test user without the right role, a feature flag that's off, a login that fails, a backend that errors — is reported as **blocked**, and Meticulous records it as a **setup blocker** with a category, the evidence the agent saw and a suggested fix. This skill turns those records into concrete changes to the project's test environment.

> Before starting, run the `meticulous-cli-update` skill to ensure the Meticulous CLI and skills are up to date — unless it has already run earlier in this conversation, in which case skip it.

Setup blockers are only recorded for Agent swarm runs against a live backend. If the project's Agent swarm runs use mocked network responses, there will be none: tell the user, and stop.

## Step 1 -- Read the recorded setup blockers

```bash
# CLI (default: the last 30 days, newest first, 100 per page)
meticulous agent agent-swarm-setup-blockers [--since=<date>] [--category=<category>] [--runId=<swarmRunId>] [--limit=<n>] [--offset=<n>] [--project=<project>]

# MCP
get_agent_swarm_setup_blockers(since="<date>", category="<category>", runId="<swarmRunId>", limit=<n>, offset=<n>)
```

The CLI prints each category's count across all matching blockers on stderr, then a TSV table with `createdAt`, `swarmRunId`, `caseIndex`, `caseId`, `commitSha`, `category`, `blockedBy`, `caseTitle`, `summary`, `evidence` and `suggestedFix`. `--json` and MCP return the same data as `{ since, counts, setupBlockers }`. If the response says there are more results, page through them with `--offset` before drawing conclusions, or narrow with `--category`.

Start from the `counts`: the categories with the most blockers are where a fix unblocks the most cases. Then group the rows within each category by root cause — the same missing record type, the same missing role, the same flag — since many blockers usually share a handful of causes. For any blocker whose `evidence` is too thin to act on, read the full case, including the steps the agent took:

```bash
meticulous agent agent-swarm-run-case --swarmRunId=<swarmRunId> --caseIndex=<caseIndex>
# MCP: get_agent_swarm_run_case(swarmRunId="<swarmRunId>", caseIndex=<caseIndex>)
```

**If there are no setup blockers** but the user still reports Agent swarm getting blocked, list recent runs with `meticulous agent agent-swarm-runs --includeCounts` (MCP: `get_agent_swarm_runs`), open a run with many blocked cases with `meticulous agent agent-swarm-run --swarmRunId=<id> --status=blocked`, and read those cases. Cases blocked by `application` are the app's own behaviour, not the environment; treat only `environment` ones as candidates here, and fall back to the static review in Step 2 to find likely gaps.

## Step 2 -- Inventory how the test environment is set up

Before proposing anything, find out where each part of the test environment is defined. Search the codebase for:

- **Seed data and fixtures**: seed scripts, database migrations that insert data, factories, fixture files, and the commands or CI steps that run them when the environment is created or reset.
- **Test users**: how the account Agent swarm signs in with is created, which roles, permissions, organisation or plan it gets, and any allow-lists it has to be on.
- **Feature flags**: how flags are evaluated in the test environment (a flag service, environment variables, a config file) and their defaults there.
- **Authentication**: how the test login works — credentials, SSO or MFA bypasses, session lifetimes, and the environment variables or secrets it reads.
- **Backend configuration**: the environment variables, deploy manifests (for example Docker Compose, Helm charts, Terraform or a platform config file) and service URLs the test deployment uses, including which third-party services are real, sandboxed or stubbed.

Also read the project's Agent swarm instructions in `.meticulous/agent-swarm-instructions.md`, if it exists: it may already describe the test accounts or the data to expect, and can be out of date.

Record, for each blocker group from Step 1, the file or system that controls it. If a blocker's cause lives outside the codebase — a flag dashboard, an identity provider, a secrets manager, a hosted database — note that the change has to be made there.

## Step 3 -- Work out the fix for each group

Use the category to decide where to look, and the blocker's `suggestedFix` as a starting point, not a final answer — check it against what you found in Step 2.

| Category              | What it usually means                                                    | Typical fix                                                                                                                                                                                               |
| --------------------- | ------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `missingTestData`     | The flow needs records that don't exist for the test user                | Extend the seed data or fixtures so the test user has representative records in each state the flows need (e.g. an empty list _and_ a populated one, a draft _and_ a published item), and reseed on reset |
| `testUserPermissions` | The test user can't see or do what the flow needs                        | Give the test user the role or permissions the flows need, or add a test user per role and describe each in the Agent swarm instructions                                                                  |
| `featureFlag`         | The flow is behind a flag that is off in the test environment            | Enable the flag for the test environment or the test user; for flags under development, default them on in test environments                                                                              |
| `authentication`      | The agent couldn't sign in, or its session expired or was rejected       | Fix the test credentials or secret, disable MFA/CAPTCHA for the test user, or lengthen the test session; make sure the login works without human interaction                                              |
| `backendError`        | The backend errored, timed out or was unhealthy                          | Check the test backend's logs around `createdAt`, then fix the failing service, its configuration or its resource limits; distinguish a broken environment from a real bug the pull request introduced    |
| `externalDependency`  | A third-party service (payments, email, maps, …) was unreachable or real | Point the test environment at the provider's sandbox, or stub that service in the test environment                                                                                                        |
| `other`               | A setup problem that doesn't fit the categories above                    | Read the `summary` and `evidence`, then decide case by case                                                                                                                                               |

Prefer fixes that make the environment reliably reproducible — seed scripts that run on every reset, flag defaults in config — over one-off manual changes that drift. Don't weaken production security to unblock testing: keep any relaxed login, permissions or flags scoped to the test environment and its test users.

If a `backendError` or other blocker looks like it was caused by the pull request itself rather than the environment, say so instead of proposing an environment change — it's a bug to fix in the change.

## Step 4 -- Propose the changes

Present a short plan to the user, ordered by how many blocked cases each fix should unblock:

1. For each fix, the blocker category, the number of blockers it addresses (with one or two example case titles), the root cause and the change.
2. **Codebase changes** (seed data, fixtures, test-user setup, flag defaults, environment configuration): implement them if the user agrees, and open a pull request that explains which Agent swarm setup blockers they address.
3. **Changes outside the codebase** (a flag dashboard, an identity provider, secrets, a hosted test database): list the exact steps for the user, since you can't make them from the codebase.
4. **Agent swarm instructions**: if the agent was missing knowledge it couldn't discover — which test account to use for which role, where seeded data lives, which flows are intentionally unavailable — add it to `.meticulous/agent-swarm-instructions.md` in the same pull request. Keep secrets out of that file.

Don't change anything that affects a shared or production environment without the user's explicit go-ahead.

## Step 5 -- Verify

Once the changes are deployed to the test environment, the next Agent swarm runs should record fewer setup blockers. After at least one new run has finished, compare:

```bash
# Blockers recorded since the fix was deployed
meticulous agent agent-swarm-setup-blockers --since=<deploy time>

# Or a specific new run
meticulous agent agent-swarm-setup-blockers --runId=<swarmRunId>
```

Check that the categories you fixed have dropped, and read any blockers that remain in them: a fix that only partly worked, or a new blocker it uncovered, will show up here. Report back to the user with the before and after counts.
