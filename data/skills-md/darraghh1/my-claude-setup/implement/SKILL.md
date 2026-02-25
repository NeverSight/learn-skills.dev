---
name: implement
description: "Execute phases from a plan using group-based processing. Builds phases in parallel within groups, audits each group after completion, and auto-fixes Medium/Low issues while escalating High/Critical to the user."
argument-hint: "[plan-folder]"
disable-model-invocation: true
metadata:
  version: 4.0.0
---

# Implement Plan

Implement phases from: **$ARGUMENTS/plan.md**

## Architecture

This skill is a **thin dispatcher**. It does NOT read references, extract patterns, or implement code. Builders handle implementation, validators handle review, and auditors handle cross-phase analysis.

| Role | Responsibility |
|------|---------------|
| **Orchestrator (you)** | Parse groups, gate checks, spawn/shutdown agents, route verdicts, triage auditor findings, track cross-group state |
| **Builder** | Phase implementation: read phase, find references, invoke skills, code, test, typecheck. Does NOT review its own code. |
| **Validator** | Independent review: runs `/code-review` (reference-grounded, with auto-fix), then typecheck + tests. Reports PASS/FAIL. |
| **Auditor** | Group-level audit: cross-phase regressions, deferred items, plan drift, system integrity. Read-only — reports findings with severity ratings. |

**All agents are ephemeral.** Each gets a fresh 200K context and is shut down after its cycle. This prevents context contamination, ensures skill instructions are never compacted, and eliminates bottlenecks.

### Processing Model

```
for each group (sequential):
  1. Gate check all phases in group
  2. Build phases (parallel where deps allow)
  3. Validate each phase (PASS/FAIL routing)
  4. When all group phases PASS → spawn auditor
  5. Orchestrator reads auditor report and triages:
     - Clean/Low → log deviations, continue to next group
     - Medium → auto-spawn builder + validator to fix
     - High/Critical → checkpoint with user, then fix
  6. Track deviation summary for next group's auditor
```

---

## Step 1: Read and Review the Plan

1. Read the plan file at `$ARGUMENTS/plan.md`
2. Check if `$ARGUMENTS/reviews/planning/plan.md` exists
3. If no review exists, run `/review-plan $ARGUMENTS` first
4. **Read the review file** at `$ARGUMENTS/reviews/planning/plan.md`
5. **Check the Verdict section:**
   - If `Yes` → proceed to Step 2
   - If `No` → **STOP** and report the Critical Issues to the user

## Step 2: Check Flow Audit

**1. Count phases** in the Phase Table.

**2. Skip for small plans:** If 1-2 phases, skip to Step 3.

**3. Check if audit exists:** Look for `$ARGUMENTS/reviews/planning/flow-audit.md`.

**4. If missing:** STOP and tell the user to run `/audit-plan $ARGUMENTS` first.

**5. Gate logic:**

| Overall Assessment | Behaviour |
|--------------------|----------|
| **"Major Restructuring Needed"** | **HARD BLOCK:** STOP. Report issues to user. |
| **"Significant Issues"** | **SOFT BLOCK:** WARN user. Ask whether to proceed or fix. |
| **"Minor Issues"** or **"Coherent"** | **PROCEED.** |

## Step 3: Parse Groups and Build Execution Plan

**3a: Check for existing tasks (compact recovery):**

Run `TaskList` first. If tasks already exist from a previous session or context compact:
1. Read existing tasks with `TaskGet` for each task ID
2. If any task is `in_progress` — resume from that point
3. Do NOT recreate the task list

**3b: Parse the Phase Table and Group Summary:**

Read plan.md's Phase Table. For each phase, extract: number, title, group, focus, status, dependencies.

Read the Group Summary table to get group ordering and descriptions.

Build a group execution plan:

```
groups = [
  { name: "auth-system", phases: [P01, P02, P03], description: "..." },
  { name: "dashboard-ui", phases: [P04, P05, P06, P07], description: "..." },
  ...
]
```

Groups are processed sequentially in the order listed in the Group Summary. Phases within a group are processed in parallel where dependencies allow.

If all phases are done:
1. Remove the plan's sidecar: `rm -f ~/.cache/claude-statusline/plans/PLAN_NAME.json`
2. Report completion to the user
3. Skip to Step 10 (cleanup)

**3c: Create orchestrator tasks (first run only):**

If no tasks exist yet, create tasks with **rich, self-contained descriptions**:

```
TaskCreate({
  subject: "Group: {group-name} — Phase {NN}: {title}",
  description: `Phase file: $ARGUMENTS/phase-{NN}-{slug}.md
Group: {group-name} ({N} phases in group: P{NN}, P{MM}, ...)
Skill: {skill-from-frontmatter}
Dependencies: {list or "none"}

Key deliverables from acceptance criteria:
- {criterion 1}
- {criterion 2}
- {criterion 3}

Gate check → build → validate → mark done.
After all phases in group "{group-name}" complete, spawn auditor for group review.`,
  activeForm: "Implementing Phase {NN} ({group-name})"
})
```

Then set up dependencies with `TaskUpdate` using `addBlockedBy` to mirror each phase's `dependencies` frontmatter.

Also create one task per group for the audit step:

```
TaskCreate({
  subject: "Audit group: {group-name}",
  description: `Spawn auditor after all phases in group complete.
Group: {group-name}
Phases: P{NN}, P{MM}, ...
Plan folder: $ARGUMENTS

Auditor reviews: cross-phase regressions, deferred items, plan drift, acceptance criteria.
Triage: Clean/Low → continue. Medium → auto-fix. High/Critical → ask user.`,
  activeForm: "Auditing group {group-name}"
})
```

Set audit tasks to be blocked by all phase tasks in their group.

**3d: Determine current group and unblocked phases:**

Find the first group with pending phases. Within that group, identify unblocked phases (all dependencies satisfied).

**Update the statusline sidecar:**

```bash
mkdir -p ~/.cache/claude-statusline/plans && echo '{"plan":"PLAN_NAME","phase":PHASE_NUM,"group":"GROUP_NAME","updated":'$(date +%s)'}' > ~/.cache/claude-statusline/plans/PLAN_NAME.json
```

## Step 4: Gate Check Phases

Before spawning builders, gate-check each unblocked phase. Mark each phase task as `in_progress`:

```
TaskUpdate({ taskId: "{phase-task-id}", status: "in_progress" })
```

**4a: Check for skeleton/placeholder content:**

```bash
echo '{"cwd":"."}' | uv run $CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_no_placeholders.py \
  --directory $ARGUMENTS --extension .md
```

If non-zero exit, the phase contains placeholder content. **STOP** — do not spawn a builder for a skeleton phase.

**4b: Verify the phase review:**

1. Check if `$ARGUMENTS/reviews/planning/phase-{NN}.md` exists
2. If no review exists, run `/review-plan $ARGUMENTS phase {NN}`
3. **Read the review Verdict:**
   - **Ready: Yes** → proceed to Step 5
   - **Ready: No** → **FIX the phase first**, re-run review, then proceed

## Step 5: Create Team (First Run Only)

Create the team on the first run. Reuse it across all groups.

```
TeamCreate({
  team_name: "{plan-name}-impl",
  description: "Implementation team for {plan title}"
})
```

## Concurrency Limits

**Hard cap: 4 total active agents (builders + validators + auditor combined).** The auditor runs alone — no builders or validators during audit.

| Constraint | Limit | Why |
|-----------|-------|-----|
| Builders per batch | Max 2 | Context pressure from parallel completions |
| Validators per batch | Max 2 (one per active builder) | Each builder gets one validator |
| **Total active agents** | **Max 4** | Orchestrator context budget |
| Auditor | **Runs alone** | Needs undivided orchestrator attention for triage |
| Batch overlap | **None** | Wait for current batch to fully complete before next |

## Step 6: Spawn Builders

Spawn a fresh builder for each unblocked phase that passed gate-checking. **Max 2 builders per batch.**

**Before spawning, extract the `skill:` field from each phase's YAML frontmatter.**

```
Task({
  description: "Implement phase {NN}",
  subagent_type: "builder",
  model: "opus",
  team_name: "{plan-name}-impl",
  name: "builder-1",
  mode: "bypassPermissions",
  prompt: `Implement the phase at: $ARGUMENTS/phase-{NN}-{slug}.md
Plan folder: $ARGUMENTS
Skill: {skill-from-frontmatter}

Follow your preloaded builder-workflow skill. It teaches you how to:
1. Read the phase and extract requirements
2. Invoke the Skill above (if not "none") and find reference files
3. Create internal tasks (TaskCreate) for each step — prefix with [Step]. This is REQUIRED for context compact recovery
4. Implement with TDD (Step 0 first), marking tasks in_progress/completed as you go
5. Run tests and typecheck
6. Report completion to team-lead (do NOT run /code-review — the validator handles that independently)

IMPORTANT: Before using the Write tool on any existing file, you MUST Read it first or the write will silently fail.`
})
```

## Step 7: Wait and Route Builder/Validator Cycle

Wait for builder completion messages. When a builder reports done:

1. **Spawn a fresh validator for this phase:**

```
Task({
  description: "Validate phase {NN}",
  subagent_type: "validator",
  team_name: "{plan-name}-impl",
  name: "validator-{N}",
  mode: "bypassPermissions",
  prompt: `Validate phase {NN} on the {plan-name}-impl team. Follow the workflow defined in your agent instructions.

Phase file: $ARGUMENTS/phase-{NN}-{slug}.md
Plan folder: $ARGUMENTS

Run /code-review against the phase file, then verify with typecheck + tests. Report PASS/FAIL to team-lead via SendMessage.`
})
```

2. **Wait for ALL validator verdicts in this batch before proceeding.**

### Handle Verdict

**PASS:**
1. Update phase YAML frontmatter: `status: done`
2. Update Phase Table in plan.md: status → "Done"
3. Mark the phase task as completed
4. Shutdown the builder and validator for this phase
5. When the entire batch is complete, check: are ALL phases in the current group done?
   - **Yes** → proceed to Step 8 (Group Audit)
   - **No** → loop back to find next unblocked phases in this group, spawn next batch

**FAIL:**
1. Shutdown current builder AND validator (both contexts may be stale)
2. Spawn a **fresh builder** with the validator's fix instructions
3. Wait for fix builder → spawn fresh validator → re-validate → repeat until PASS

## Step 8: Group Audit

When all phases in a group have passed validation, spawn an auditor for the group.

**Mark the group audit task as `in_progress`:**

```
TaskUpdate({ taskId: "{audit-task-id}", status: "in_progress" })
```

**Shutdown all builders and validators from this group first** — the auditor runs alone.

**Spawn the auditor:**

```
Task({
  description: "Audit group {group-name}",
  subagent_type: "auditor",
  model: "opus",
  team_name: "{plan-name}-impl",
  name: "auditor-{group-name}",
  mode: "bypassPermissions",
  prompt: `Audit the "{group-name}" phase group.

Plan folder: $ARGUMENTS
Group: {group-name}
Phases in this group:
- Phase {NN}: {title} — $ARGUMENTS/phase-{NN}-{slug}.md
- Phase {MM}: {title} — $ARGUMENTS/phase-{MM}-{slug}.md
[...list all phases in group...]

Previous group deviations:
{deviation-summary-from-previous-groups OR "None — this is the first group."}

Follow your preloaded auditor-workflow skill. It teaches you how to:
1. Read all group phases and build inventory
2. Collect and review code reviews for group phases
3. Check deferred items against current code
4. Cross-phase impact analysis (shared files, imports, overwrites)
5. Run verification (tests + typecheck)
6. Plan vs implementation comparison (acceptance criteria, ADRs)
7. Consider previous groups' deviations
8. Write audit report to $ARGUMENTS/reviews/implementation/group-{group-name}-audit.md
9. Report findings to team-lead with severity ratings

IMPORTANT: You are READ-ONLY. Do not modify source code. Write only the audit report file.`
})
```

## Step 9: Triage Auditor Findings

When the auditor reports back, **read the full audit report** at `$ARGUMENTS/reviews/implementation/group-{group-name}-audit.md`.

**9a: Create tasks from findings FIRST (compact safety):**

Before spawning any fix builders, create tasks for each finding that needs action. This ensures findings survive context compaction:

```
TaskCreate({
  subject: "Fix: {finding summary} (group {group-name})",
  description: `From auditor report: $ARGUMENTS/reviews/implementation/group-{group-name}-audit.md

Severity: {Critical/High/Medium/Low}
Phase: P{NN}
File: {file:line from auditor report}
Issue: {description from auditor report}
Suggested fix: {fix from auditor report}`,
  activeForm: "Fixing {finding summary}"
})
```

**9b: Triage by severity:**

| Finding Severity | Action |
|-----------------|--------|
| **No issues / Low only** | Log deviation summary, mark audit task complete, continue to next group |
| **Medium** | Auto-spawn builder to fix + validator to verify. No user input needed. |
| **High / Critical** | **Checkpoint with user.** Present the findings and ask for direction before proceeding. |

**9c: For Medium findings — auto-fix cycle:**

1. Spawn a builder with the specific fix instructions from the auditor report
2. Wait for builder completion
3. Spawn validator to verify the fix
4. If PASS → mark fix task complete
5. If FAIL → retry (max 3 attempts per finding, then escalate to user)

**9d: For High/Critical findings — user checkpoint:**

Present the auditor's findings to the user:

```
## Group "{group-name}" Audit — Needs Your Input

**Assessment:** {from audit report}

### Critical/High Findings:
1. {finding 1 — severity, phase, file:line, issue}
2. {finding 2}
...

### Auditor's Recommendation:
{from audit report}

**Options:**
1. Fix all — I'll spawn builders for each finding
2. Fix specific items — tell me which ones
3. Skip and continue — accept the findings as-is
4. Stop implementation — address these manually
```

Use `AskUserQuestion` to get the user's choice, then act accordingly.

**9e: Track deviation summary:**

After all findings are resolved (or accepted), build a deviation summary for the next group's auditor:

```
deviation_summaries[group_name] = {
  assessment: "{from audit report}",
  key_deviations: ["{finding 1}", "{finding 2}"],
  unresolved: ["{any findings user chose to skip}"]
}
```

Pass this to the next auditor in its spawn prompt (see Step 8, "Previous group deviations").

**9f: Mark audit task complete and continue:**

```
TaskUpdate({ taskId: "{audit-task-id}", status: "completed" })
```

Shutdown the auditor:

```
SendMessage({ type: "shutdown_request", recipient: "auditor-{group-name}" })
```

Loop back to Step 3 to start the next group.

## Step 10: Cleanup

When all groups are done OR an error breakout condition is met:

1. **Shutdown all active teammates:**

```
// For each active agent:
SendMessage({ type: "shutdown_request", recipient: "{agent-name}" })
```

2. **Delete team:** `TeamDelete()`

3. **Remove this plan's statusline sidecar:**

```bash
rm -f ~/.cache/claude-statusline/plans/PLAN_NAME.json
```

4. **Report final summary to user:**

```
## Implementation Complete

**Plan:** $ARGUMENTS
**Groups:** {count} completed
**Phases:** {count} Done

### Group Audit Results:
| Group | Assessment | Critical | High | Medium | Low |
|-------|-----------|----------|------|--------|-----|
| {name} | {verdict} | {N} | {N} | {N} | {N} |

### Unresolved Items:
{any findings the user chose to skip}

### Verification:
- Tests: {pass/fail}
- Typecheck: {pass/fail}
```

**Error breakout conditions** — STOP and shut down if:
- Validator FAIL repeats 3+ times on the same phase
- Auditor finding fix fails 3+ times
- Phase has Critical blocking issues from plan review
- User requests cancellation

---

## Resuming After Context Compact

If you notice context was compacted:

1. Run `TaskList` to see all tasks and their status
2. Find the `in_progress` task — that's where you were
3. Run `TaskGet {id}` on that task for full details
4. Read plan.md to get the Phase Table and Group Summary
5. Check existing audit reports in `$ARGUMENTS/reviews/implementation/` to rebuild deviation summaries
6. Check if team exists: read `~/.claude/teams/{plan-name}-impl/config.json`
   - If team exists, teammates may still be active — coordinate via messages
   - If no team, re-create it
7. Continue from the in_progress task

**Pattern for every work cycle:**
```
TaskList → find in_progress or first pending → TaskGet → continue work → TaskUpdate (completed) → next task
```

Tasks are the orchestrator's source of truth for progress — not memory, not plan.md alone.

---

## Reference Material

For anti-pattern prevention, context compact recovery, and troubleshooting, see [references/team-operations.md](references/team-operations.md).
