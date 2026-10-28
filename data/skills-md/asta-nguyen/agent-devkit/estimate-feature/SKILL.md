---
name: estimate-feature
description: Use when a user, BA, PM, or delivery team asks for an effort estimate of a written feature plan or tasks.md.
---

# Estimate Feature

Estimate active engineering hours for a developer using an AI coding agent.
Never run this optional skill unless the user requests an estimate.

## Process

1. Require a written plan under `docs/agent-devkit/plans/`, or a change's
   `tasks.md` under `docs/agent-devkit/changes/<folder>/`. If neither exists
   and the user also requested a plan with a written `design.md`, call
   `plan-feature` as a route handoff: it writes the plan, calls this skill
   before its approval gate, and presents both together. Otherwise stop and
   request a plan. Use a repair handoff to `plan-feature` only to fix missing
   detail in an existing plan. Never estimate directly from a feature request.
2. Read `AGENTS.md`, the plan or `tasks.md`, the linked design, `delta.md`
   (when present), relevant wiki, source, and tests.
   Call the available Skill entry whose local name is `read-codebase-context`
   when source exists. If the plan has an `## Impact map`, follow
   `read-codebase-context`'s `## Refresh an impact map`; if its baseline is
   missing, unavailable, or no longer an ancestor, trace existing source from
   scratch. Do not try to trace planned
   entry points, callers, or tests that do not exist yet; use planned files,
   interfaces, behavior, and verification only from the written design and
   plan. Pending approval does not block estimation: label planned assumptions
   `pending approval` and report the gate's current status. It does not
   authorize implementation. Mark unspecified behavior as unknown and block
   an estimate when it prevents a defensible range. Re-trace planned paths
   only after source exists.
   Read current source for every existing file the plan says implementation
   will edit. For a planned file that does not exist yet, use the written
   design and plan; do not treat that file as traced source. If
   tasks omit files, behavior, or verification, call `plan-feature` as a repair
   handoff (see `using-devkit`) to fix the plan, then resume this estimate;
   `plan-feature` must not start implementation from this call.
3. State the AI support profile. Assume the coding agent can inspect and edit
   source, write and run tests, and update documentation, while a developer
   reviews output and resolves product decisions. Include context gathering,
   prompting, coding, tests, expected debugging, review, and planned docs.
   Exclude waiting, stakeholder response, deployment, and manual QA unless
   planned.
4. Estimate every plan task with a defensible hours range, confidence, and
   evidence-based rationale. Consider local patterns, novelty, touched files,
   migrations, integrations, test cost, and unresolved dependencies. Never
   apply a generic "AI is N% faster" discount. When an unknown prevents a
   defensible range, mark the task `Blocked: spike required` and keep it in the
   task table with `Blocked` in Hours, `N/A` confidence, and the unknown in its
   rationale. Exclude blocked tasks from the total and report their count. While
   any task is blocked, total confidence cannot be `High`. If every task is
   blocked, report the total as `Not estimable — spike required` and total
   confidence as `N/A`.
5. For a change, save `estimate.md` beside its `tasks.md` and link to that file
   relatively. For a legacy plan, save a new estimate at
   `docs/agent-devkit/estimates/YYYY-MM-DD-<slug>-estimate.md` and link to the
   exact plan filename. Follow the shared artifact naming rule in `using-devkit`
   (read it if it is not loaded). Create `docs/agent-devkit/estimates/` only now
   if it does not exist. Use:

   ```md
   # Feature Estimate

   ## Plan
   - <link to the exact plan file>

   ## AI support profile
   <included effort and exclusions>

   ## Task estimates
   | Plan task | Hours | Confidence | Basis and risks |
   |---|---:|---|---|
   | Task 1: <name> | 2-4h | Medium | <repo evidence and uncertainty> |
   | Task N: <name> | Blocked | N/A | Blocked: spike required — <unknown> |

   ## Total
   - Active engineering effort: <sum of estimable ranges, or `Not estimable — spike required` if all tasks are blocked>
   - Blocked tasks: <N excluded from the effort total; `0 (all tasks estimable)` when none>
   - Confidence: <High/Medium/Low; not High if any task is blocked; `N/A` if all are blocked>

   ## Open unknowns
   - <unresolved information behind a blocked estimate, or "None">
   ```

6. For a legacy plan, add `## Estimate` with a link to the estimate in the plan,
   and add the estimate to `docs/agent-devkit/INDEX.md` under `## Estimates`.
   For a change, link `estimate.md` from `tasks.md`; no separate index entry is
   needed; the change folder's own entry covers it (`using-devkit`'s
   `## Change lifecycle`).
7. Treat the estimate as stale when the linked plan's tasks, files, behavior,
   verification, or assumptions change. On refresh, compare the whole current
   plan with the estimate, then update the same estimate file and totals.
8. Verify every plan task appears exactly once as a row in `Task estimates`,
   blocked rows follow step 4, the blocked-task count in the total matches the
   table, and range totals include only estimable tasks. If all tasks are
   blocked, verify the total and confidence follow step 4. Verify all links
   resolve and `git diff --check` passes. Do not repeat task rows in `Open
   unknowns`; list only the unresolved information there. Do not edit
   application code or start implementation (no commits: `using-devkit`).
9. When `plan-feature` called this skill, return the estimate to it so it
   presents the estimate with the plan and approval gate. When the user called
   this skill directly, present the estimate yourself with the plan's current
   approval-gate status and end with the `Next:` block from `using-devkit`; do
   not call `plan-feature` again. The estimate does not approve the plan or
   authorize implementation.
