---
name: harness
description: >-
  Create or simplify a compact repository harness for coding agents. Use when a
  repository needs concise AGENTS.md instructions, task-local scope and handoff,
  routes to canonical specifications and decisions, and a minimal read-only
  Bash init.sh verification entrypoint.
---

# Harness v2

Create the smallest harness that lets an agent find truth, stay scoped, verify,
and resume. Reuse repository-native documents and trackers before creating any.
Use `harness-task` when installed to size work; it is intake policy, not orchestration.

## Artifacts

| File | Owns |
|---|---|
| `AGENTS.md` | Short router, repository invariants, verification commands |
| `tasks/index.md` | Roadmap and links to tasks or tracker; no mirrored execution state |
| `tasks/task-<slug>.md` | One task's scope, acceptance, dependencies, status, evidence, handoff |
| `docs/plans/task-<slug>.md` | Separate execution plan only when sequencing or recovery requires it |
| `init.sh` | Minimal read-only repository verification entrypoint |

These are conventions, not a required tree. Keep a requested roadmap/index,
but change it only when tasks or roadmap scope change, not on every status
update. Dependencies live in tasks or the tracker; the index links to them.
No root progress log. No empty directories, generated helpers, mandatory global
active task, or duplicated external tracker. Do not reference `.agents/README.md`
from `AGENTS.md`. Keep durable behavior and decisions in their canonical specs,
design documents, decision records, or architecture map, not task history.

## Inspect before writing

1. Read git status, applicable instructions, README, and existing canonical docs.
2. Inspect manifests, lockfiles, declared workspaces, CI, and relevant tests.
3. Find the repository's existing verification entrypoint and inspect its safety.
4. Identify existing task ownership and trackers only for in-scope tracked work.
5. Label conflicting evidence `Observed`, `Intended`, `Proposed`, or `Uncertain`.
6. Ask when requirements, overwrite permission, ownership, or check coverage are unclear.

## Create or update

Use `templates/` as starting points, not files to copy wholesale. Replace
placeholders with evidence. Preserve unrelated work and repository-native paths.
Create a task only when scope, risk, or cross-session handoff needs persistence.
Bounded tracked work keeps its plan inline. A separate plan needs a concrete
sequencing, coordination, recovery, or high-impact control requirement; file
count and diff size are not decision rules.

For a local task:

- Reuse the tracker ID or a descriptive `task-<slug>`; do not allocate global counters.
- Check the tracker and known concurrent work for a conflicting ID or scope.
- Keep `todo`, `active`, `blocked`, or `done` in the task, not a second index.
- Name its owner. Several independent tasks can be active at once.
- Start only user-approved work. Distinguish dependencies required to start
  from those required to integrate/release; do not serialize independent implementation.
- For parallel edits, agree file ownership or integration order; a task file is not a lock.
- To inspect start readiness across local tasks when choosing next work, run `node <path-to-skill>/scripts/task-ready.mjs [tasks-dir]`. Do not run for assigned tasks; readiness does not grant approval to start backlog work.
- Update only this task's evidence and handoff when state materially changes.
- Mark done only when acceptance passes and relevant verification evidence is recorded.

Copy `templates/task-template.md` only when a record is needed. Do not create a
repository copy of the template unless maintainers need it. Link a separate plan
from the task without copying its execution details. Use an adequate external
tracker instead of creating local state. Use `templates/task-index.md` only
when a local roadmap is needed; avoid duplicating the external tracker.

After completion, move durable behavior, rationale, and constraints into their
canonical docs/tests. Retain or selectively archive useful execution evidence.
Remove a disposable task only after checking incoming links, dependencies,
consumers, and repository retention policy; never archive everything by default.

## Minimal init.sh

Keep Bash and `set -euo pipefail`. Resolve the script's directory before checks.
Use `run_check` for explicit commands: print RUN/PASS/FAIL and preserve nonzero
exit status. Run sequentially and stop at the first failure.

- Prefer the observed root check command when it owns coverage and concurrency.
- Otherwise list only existing read-only commands needed for coverage.
- Use check-only formatter and linter modes. Never fix source or install dependencies.
- Do not invent scripts, infer commands at runtime, generate child scripts, or build a Bash job scheduler.
- Do not hide failures with `|| true` or finish with success after a failed check.
- Syntax and git whitespace checks alone do not verify application behavior.
- If no project check exists, print the gap and report only configured checks passed.
- Preserve target-repository rules. Non-mutating source checks can still write build/test outputs; inspect side effects first.

The distributed template provides only syntax and git whitespace checks. Before
claiming full repository verification, replace its explicit project-check gap
with evidence-backed commands. An intentionally docs-only repository can keep
the gap with a documented coverage boundary. Set the generated script executable.
Run it after meaningful changes, not at every startup merely to read docs.

## Existing harness and migration

Read the `AGENTS.md` provenance footer, legacy `_harness.version` if present,
and `metadata.json`. When versions differ, read the applicable `CHANGELOG.md`
entries. Propose the smallest diff, preserve custom rules and commands, and
obtain approval before changing managed target-repository files.

For v1 state, follow [v2 migration](references/migration-v2.md). Do not delete
feature or progress history or silently change its owner. Update the provenance
marker only after the approved migration is verified. Unknown versions require
inspection, not wholesale regeneration. Harness maintenance needs no task log
unless its risk or handoff independently requires one.

## Finish

1. Verify affected paths and the generated Bash script using observed commands.
2. Record task evidence when tracked; distinguish existing failures and uncovered checks.
3. State omissions and unresolved decisions without calling an unchecked result done.
4. Route known docs repairs to `agent-docs-writer`, unclear ownership to
   `agent-docs-architect`, and read-only docs assessment to `agent-docs-checker`.

## References

Read only for the current need:

- [Migration](references/migration-v2.md): existing v1 harnesses
- [Memory](references/memory-persistence-pattern.md): cross-session restart
- [Context](references/context-engineering-pattern.md): context pressure
- [Coordination](references/multi-agent-pattern.md): concurrent work
- [Gotchas](references/gotchas.md): core failure modes
- [Runtime archive](references/gotchas-full.md): engine-specific issues only
