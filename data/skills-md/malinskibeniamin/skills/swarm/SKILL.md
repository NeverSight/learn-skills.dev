---
name: swarm
description: Parallel executor for independent bulk work across worktree lanes.
disable-model-invocation: true
---

# Swarm

Shard independent bulk work across lanes, verify each, then integrate. Swarm executes an
existing goal; it does not replace planning or own delivery. Parallelism requires explicit opt-in
through `/swarm` or a direct user request; no other skill grants consent.

`/work` owns lifecycle, `/grilling` resolves choices, and `/go` ships.

## Launch

1. Inspect repository rules, state, branch/PR, relevant docs, and the active goal.
2. For long or costly waves, use `/efficient-frontier` before launch and between waves.
   Default to at most three parallel agents unless the user says otherwise.
3. Keep orchestration, critical-path work, integration, and judgment with the coordinator.
   Delegate only bounded search, implementation, test, or evidence-reduction work.
4. Choose workspace policy:
   - Default: same branch/worktree/PR.
   - Requested isolation: one descriptive worktree and branch per lane.
   - High conflict risk: separate scopes or serialize writes.
5. Show a compact swarm manifest, then launch:

   ```text
   Swarm manifest
   Policy: shared | worktrees | hybrid
   - swarm-<lane>: <mission> | scope: <paths> | skills: </skill...>
   ```

6. Spawn only distinct lanes. The coordinator integrates results, resolves conflicting
   findings, runs final verification, and closes agents.

## Task packet

Every lane receives:

```yaml
agent_name: swarm-<area>-<mission>
role: explorer | worker | reviewer | teacher
mission: one concrete outcome
skills: [only relevant skills]
context: rules, decisions, branch or PR, paths
workspace_policy: shared | worktree | hybrid
write_scope: exact paths or report-only
forbidden: duplicate work, unrelated files, commits or pushes unless requested
termination: deliverable and stop condition
model_policy: inherit unless evidence or the user requires an override
output schema: status, summary, changed_files, tests_run, findings, blockers, next_action
```

Workers may write only within their scope. Shared lanes need distinct ownership; worktree
lanes use descriptive branches; descendants require separate authorization.

## Lane rules

- Use `config/model-routing.json`; do not duplicate one implementation across model pairs.
- Assign one implementation owner per write scope and matching evals or eval ownership for
  each changed skill or hook.
- TDD lanes return RED -> GREEN or failing-test evidence before implementation evidence.
- Split architecture by module or seam; tests by independent public behavior.
- Split `/visual-review` and `/ux-copy` only when scopes do not overlap.
- Review lanes may separate spec, standards, resilience, security, performance, tests, and UX.
- Diagnosis lanes may separate reproduction, hypotheses, instrumentation, and regression proof.
- Keep synthesis and user-reserved decisions with the coordinator.

## Merge protocol

Read artifacts and changed files, not summaries alone. Reject or reconcile overlaps
intentionally. For conflicting recommendations, show evidence, options, and the coordinator's
choice. Run targeted checks after integration; TDD work needs RED evidence before GREEN.
Report the manifest, landed and rejected work, tests, blockers, and next action.

## Compatibility

Codex and Claude Code must operate from explicit prompts and artifacts. Without native
subagents, emit Task packets for manual launch.
