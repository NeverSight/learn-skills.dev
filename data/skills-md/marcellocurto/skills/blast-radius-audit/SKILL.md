---
name: blast-radius-audit
description: Find downstream breakage a code change could cause beyond the files it directly touches.
---

# Blast Radius Audit

Find how a change could break behavior outside the edited files, and check the facts its safety depends on.

This is an audit. Do not edit repository files, add permanent tests, apply fixes, commit, or touch production or external systems unless the user separately asks. Read-only inspection and reversible local commands are fine. Put temporary probes outside the working tree and delete them when done.

## 1. List the changed contracts

Audit the pull request, branch, commit, or working changes the user names. If none is named, audit the current branch against the default branch plus uncommitted changes. Record the exact commits.

Read the full diff, the commit messages, the related tests, and the repository instructions. Then list every contract the change alters, including ones not obvious from the edited lines:

- function and type signatures, return shapes, thrown errors, and error messages that callers match on
- stored data: database columns, serialized formats, cache keys, events, files, and exports
- external interfaces: HTTP or RPC responses, CLI output and flags, and public package exports
- configuration keys, environment variables, feature flags, and defaults
- timing: order of operations, retries, transactions, startup and shutdown, and work that runs later or more than once
- permission checks, validation, and other checks that were moved, loosened, or removed
- cost on hot paths: query counts, payload sizes, and loops over large collections

## 2. Find the consumers

For each changed contract, find what depends on it. Search by symbol name and by literal value, such as a column name, event name, config key, or route path, because many consumers reference a contract by string. Look beyond direct callers: generated code, dependency injection, plugins, reflection, migrations, fixtures, scripts, documentation, other services and repositories, and older versions still running during a rollout.

A search with no results does not prove a contract is unused. Say where you looked.

When a conclusion depends on how a library or runtime behaves, check the installed version and its code or documentation.

## 3. Check each risk

A risk needs a plausible path from the change to a consumer. Do not list concerns without one.

For each risk, state what must be true for the change to be safe, and check it the cheapest reliable way: read the code or documented contract, trace the path, run an existing test, or run a temporary probe. A probe must use the real code and dependency version and fail clearly if the assumption is false. A probe against a mock proves nothing about the shipped path. Do not rerun checks to repeat proof you already have.

Give each risk one status:

- **Confirmed:** the failure can happen. State the conditions, and whether you reproduced it or established it by reading.
- **Unresolved:** a specific missing fact prevents confirming or ruling it out. Name the fact and the check that would settle it.
- **Ruled out:** evidence shows it cannot happen in the audited scenario.

## 4. Report

Choose the verdict:

- **Material risk** if any confirmed risk affects correctness, data, compatibility, or operation.
- **Unverified** if nothing is confirmed but an unresolved risk could change the verdict.
- **Contained** if every risk is ruled out. This covers only what you inspected.

Use this format and omit sections with nothing to report:

```markdown
**Verdict:** Material risk | Unverified | Contained, with one sentence on why.

**Changed contracts:** the contracts from step 1 that have consumers outside the diff.

**Risks**, confirmed and unresolved, most severe first:

- **Status: what breaks.** The conditions, who is affected, and the evidence. The next check or fix direction, plus detection and rollback when they matter.

**Ruled out:** only concerns a reviewer would likely raise, each with its evidence in one line.

**Before merge:** checks or decisions still needed.
```
