---
name: infrahub-planning-upgrades
description: >-
  Plans a version-by-version Infrahub upgrade path and scores each release's breaking
  changes against the user's repository and instance, producing UPGRADE_PLAN.md.
  TRIGGER when: planning an Infrahub upgrade, asking what breaks between two versions,
  checking upgrade impact before a maintenance window, asked to "just run the upgrade",
  updating or extending an existing UPGRADE_PLAN.md after the target release or the
  repository moved, debugging a plan that missed a breaking change.
  DO NOT TRIGGER when: auditing a repo against best practices, querying live data,
  designing schemas, collecting diagnostics after a failed upgrade, switching between
  the Community and Enterprise editions.
  ALWAYS pass the user's request verbatim as args, versions, pasted schema, deployment,
  and edition included: this skill runs in a forked context and cannot see the parent
  conversation.
context: fork
argument-hint: "[the user's upgrade request, verbatim]"
metadata:
  version: 1.3.0
  author: OpsMill
---

# Infrahub Upgrade Path Planner

## Overview

Produces `UPGRADE_PLAN.md`: the route from the running
Infrahub version to the target, one hop per minor
version, with every breaking change in that range
checked against this repository and, when reachable,
this instance.

**The plan describes how to upgrade; it does not
upgrade.** It never runs the upgrade, a schema load, or
a branch write, and it never hands the user the upgrade
command. It may run and show read-only probes.
The user's deployment method (Docker Compose, Helm,
Enterprise, Community) decides the exact commands, and
the upgrade guide for that deployment owns them.

**Versions, not editions.** The plan covers a move to a
later version within one edition. Switching between
Community and Enterprise, in either direction, is not a
version upgrade and the release notes do not cover it.
Say so and point at
<https://docs.infrahub.app/overview/community-vs-enterprise#migration-path>
instead of planning it. A request that does both plans
the version upgrade only and names the edition change
as out of scope.

`Write` is granted for `UPGRADE_PLAN.md` only. `Bash` is
granted for reading release notes with `gh` and for the
read-only probes.

## Project Context

This skill runs in a forked context and has no view of
the parent conversation, so the user's request arrives
verbatim as the arguments: the versions, and everything
else the plan depends on, such as a pasted schema, the
deployment method (step 6 picks the upgrade guide from
it), the edition, and any pressure to "just run it".
For example:
`/infrahub:planning-upgrades We run 1.9.2 on Docker Compose, Community, and want 1.10.0. Here is our schema: ...`

With no target, ask for one. With no current version,
read it from `infrahubctl info` (`Infrahub Version:`),
and ask if the server is unreachable.

## Workflow

1. **Fix the endpoints and the hops.** Infrahub
   supports upgrades only from the previous minor
   version (N-1), so 1.6.3 to 1.9.0 is three hops:
   1.6 to 1.7, 1.7 to 1.8, 1.8 to 1.9. Never plan a
   jump across minors, even when the user asks for
   "one go". Patches are different: one upgrade
   applies every pending migration in order, so
   1.9.1 to 1.9.6 is a single hop, and a minor hop can
   start from any patch of the previous minor (1.9.1
   to 1.10.0). Rolling up patches within the current
   minor first (1.10.8 to 1.10.10) is fine as its own
   section, not a requirement.
2. **Enumerate every release in the range, patches
   included, and read each one's notes.** Read
   [rules/sources-enumerate-every-hop.md](./rules/sources-enumerate-every-hop.md)
   before fetching anything: breaking changes ship in
   patch releases, and no machine-readable flag marks
   them.
3. **Inventory the repository.** Schema YAML,
   `.infrahub.yml`, GraphQL queries, and the Python
   checks, generators, and transforms. If an instance
   is reachable, confirm it with `infrahubctl info`
   ([connectivity-server-check](../infrahub-common/rules/connectivity-server-check.md))
   and read live data through the MCP read tools
   ([mcp-tools](../infrahub-analyzing-data/rules/mcp-tools.md)).
   The instance is optional; the repository is not.
4. **Give every finding a verdict and back it.** Read
   [rules/impact-verdict-needs-evidence.md](./rules/impact-verdict-needs-evidence.md)
   before filling the `Affected` and `Evidence`
   columns.
5. **Probe, read-only.** Read
   [rules/safety-read-only-probes.md](./rules/safety-read-only-probes.md)
   before running or showing any command, and again
   if the user asks you to run the upgrade.
6. **Write `UPGRADE_PLAN.md`** in the shape below.
   Each hop's steps are prose: take a backup, clear
   the `before` findings, upgrade to the hop's target
   following the upgrade guide, clear the `during` and
   `after` findings. Link the guide rather than
   transcribing it, picking the edition page when you
   know the edition:
   - overview: <https://docs.infrahub.app/deploy-manage/maintain-upgrade/upgrade/overview>
   - Community: <https://docs.infrahub.app/deploy-manage/maintain-upgrade/upgrade/community>
   - Enterprise: <https://docs.infrahub.app/deploy-manage/maintain-upgrade/upgrade/enterprise>

## Plan Format

One `##` section per hop, in ascending order, with the
hop's two versions in the heading (`## 1.9 -> 1.10`).
Each hop carries one findings table with these nine
columns, in this order:

| Change | Release | Kind | Severity | When | Affected | Evidence | Action | Source |
| ------ | ------- | ---- | -------- | ---- | -------- | -------- | ------ | ------ |

| Column | Values |
| ------ | ------ |
| `Release` | one version, `X.Y.Z`, never a range |
| `Kind` | `breaking` or `preparation` |
| `Severity` | `critical`, `warning`, or `info` |
| `When` | `before`, `during`, or `after` the hop |
| `Affected` | `yes`, `no`, or `unknown` |

What each value means, and a worked example, are in
[reference.md](./reference.md). Read it before writing
the first row.

## Rule Categories

| Category | Prefix | Rules |
| -------- | ------ | ----- |
| Sources | `sources-` | [sources-enumerate-every-hop](./rules/sources-enumerate-every-hop.md) |
| Impact | `impact-` | [impact-verdict-needs-evidence](./rules/impact-verdict-needs-evidence.md) |
| Safety | `safety-` | [safety-read-only-probes](./rules/safety-read-only-probes.md) |

## Supporting References

- [reference.md](./reference.md): column semantics and
  an example plan. Read at step 6.
- [rules/_sections.md](./rules/_sections.md): the rule
  index.
