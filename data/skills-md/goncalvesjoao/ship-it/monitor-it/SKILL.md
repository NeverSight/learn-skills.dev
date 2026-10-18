---
name: monitor-it
description: "Monitor an open GitHub PR every two minutes, optionally use Copilot review, resolve feedback, and request human review only when ready for merge or blocked."
---

# Monitor it

## Repository identity

Before GitHub access, Git writes/network operations, delegation, or scheduling, read and follow [the shared identity instructions](references/github-identity.md). Apply them to invoked upstream skills and every worker.

## User questions

Before asking or relaying any user question, read and follow [the user question rules](references/user-questions.md).

Requires authenticated GitHub CLI (`gh`). Monitoring also requires access to the PR's head repository and monitoring-worker and nested implementer subagent support. Accept a spec issue number or an explicit PR URL. Invocation authorizes the scheduled checks, scoped fixes, normal pushes to the PR's head branch, review requests and replies, labels, and assignment described here and in the monitoring workflow. Creating or editing this skill does not authorize execution. Merging is not authorized.

## Dispatch one cycle

Read repository instructions and resolve the target repository. Treat numeric input such as `#<id>` as a spec issue number and fetch its authoritative URL, verifying it is an issue. Load `docs/implementations/<id>.md` when present, verifying its spec URL and repository; recover it from existing worktrees or branch contents when needed. Retain its integration branch, decisions, approved deviations, limitations, validation, and evidence. Resolve the PR through GitHub using the recorded integration head branch or verified links to the spec or its tickets, including closing references. Include open, closed, and merged PRs in lookup. Paginate candidate results and verify repository, issue association, and actual head branch before selecting a unique match. An absent report permits issue-link lookup; an unreadable or conflicting report, incomplete lookup, no match, or multiple matches requires a reported blocker or clarification before mutations. Explicit PR URLs and already verified PR identities from callers or scheduled ticks bypass issue lookup. For explicit PR URLs or verified caller/tick identities, retain the supplied identity without fetching live PR state in this coordinator; the worker verifies identity, head, and current state before acting. Issue lookup fetches only the identity and association needed to select the target. Stored PR entries in implementation reports are unnecessary and are not used for resolution. Attach the PR to this chat when supported. Resolve the absolute paths of [references/monitoring-cycle.md](references/monitoring-cycle.md) and [address-it](../address-it/SKILL.md). The worker loads both; this chat loads only this coordinator skill.

When implementation context is supplied, persist the retained report or durable report pointer, evidence pointers, approved deviations, limitations, and user decisions/constraints in the PR ledger before dispatch. Recover its verified path or initialize `<git-common-dir>/address-it/<owner>/<repo>/<PR-number>.json` from the supplied checkout, recording PR identity. Use the ownership and atomic-write rules below. Verify the saved context and preserve later recorded human decisions. If persistence fails, leave affected work paused and report the failure. Require every worker to recover this context from the supplied ledger and pass relevant decisions and evidence to the resolver.

Dispatch one fresh monitoring subagent without inherited conversation history, using `fork_turns="none"` when available. Pass both instruction paths, absolute project/checkout and ledger paths when known, PR identity and supplied expected base/head repository, branch, and SHA, authoritative spec/ticket pointers, explicit user constraints/review preference, authorization above, and start/resume or scheduled-tick intent. For scheduled ticks, supply the verified automation ID. Supply a cancellation condition revoking PR-write authorization when monitoring is stopped or superseded. Confirm nested implementer support before dispatch.

Wait for its compact result and use its verified state without duplicating its GitHub fetches in this coordinator. Leave PR fetching, feedback resolution, review requests, wait/retry decisions, readiness verification, and PR mutations to the worker. Preserve one active monitoring cycle and implementer per PR; skip overlapping ticks. An interrupted/missing/unverifiable result is incomplete work; recover through a fresh worker after reconciling inactive ownership, without claiming completion.

Before dispatching or resuming work affected by a consequential human answer, persist the actual answer, its scope, source message reference when available, and superseded decision in the ledger under the ownership and atomic-write rules below. Preserve unrelated ledger fields and verify the saved answer. If a cycle is active, interrupt affected work and reconcile ownership before recording the answer. If persistence fails, leave affected work paused and report the failure. Pass the answer explicitly to the next worker; every later worker must recover current decisions from the ledger. An answer changes only its stated scope and does not itself resume stopped monitoring.

## Schedule and lifecycle

A scheduled tick first verifies its automation is active and matches the ledger ID. Paused, deleted, superseded, or unverifiable ticks return without PR writes or schedule changes. Only an explicit start/resume may activate or replace a schedule.

On start/resume, inspect matching schedules and the ledger ID, reconcile pending schedule writes, then dispatch one cycle. Match by chat, repository, and PR. If schedule state cannot be inspected, report the limitation instead of risking duplicates.

If the worker returns active with useful work or a bounded wait, reuse a matching active schedule. Only an explicit start/resume may reactivate a matching paused schedule or create a replacement when none exists. Reconcile duplicates and record the verified ID/status. Persist schedule intents before writing, inspect the result afterward, and reconcile uncertainty before retrying. Use temporary-file atomic ledger replacement under `<ledger-path>.lock`, preserving worker-owned fields and releasing only your own lock; acquire it by atomic directory creation and verify owner inactivity before stale-lock takeover.

Each heartbeat returns here every **120 seconds** and dispatches one fresh worker. Its saved prompt invokes this coordinator by absolute path and includes the absolute monitoring reference, resolver, project and ledger paths, PR identity, spec pointers, authorization, constraints/review preference, scheduled-tick intent, notification rules, and stop conditions. Require the prompt to load implementation context and current human decisions from the ledger; saved constraints are a snapshot and cannot override later recorded answers. Local scheduling requires the machine and desktop app to remain running.

Skipped ownership conflicts leave scheduling unchanged for the next tick. Honor returned retry-after times without resetting deadlines. If scheduling is unavailable and monitoring is still needed, dispatch a worker with that limitation to finish independent work and record the blocked handoff. Relay required human questions once through the User questions procedure; review-mode decisions leave scheduling inactive until explicitly answered/resumed.

## Stop and report

On ready for merge, blocked, closed/merged, needs review-mode decision, or user stop, disable every matching monitor and verify inactivity. On user stop, interrupt the active worker and its implementer before shutdown, preserving ledger, branch, and unpublished work. Report shutdown failures; unverifiable terminal writes or shutdown prevent claiming completed handoff/readiness. Resume only through Schedule and lifecycle.

Report the compact verified outcome, PR URL/head SHA, meaningful changes, and required action. Active monitoring is incomplete delivery. Stay quiet while state is unchanged/non-actionable; notify on verified pushes, readiness/handoff, closure/merge, new failures, or required decisions. Report unchanged blockers once. Keep detailed evidence in the ledger rather than rereading it into this chat.

When changing behavior, evaluate [the shared offline behavior checks](../address-it/references/behavior-checks.md) offline, without GitHub or schedule writes.
