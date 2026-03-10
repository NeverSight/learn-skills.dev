---
name: auditor-workflow
description: "Group-level implementation audit workflow for auditor agents. Handles loading project rules, reading connected phases, reviewing code reviews, checking deferred items, cross-phase impact analysis, verification, and structured reporting to the orchestrator. Invoke this skill as your first action — not user-invocable."
user-invocable: false
metadata:
  version: 1.0.0
---

# Auditor Group Workflow

You have been assigned a **group of connected phases** to audit. Your spawn prompt contains: the plan folder path, the group name, the list of phase files in this group, and a summary of previous groups' deviations (if any).

You are **read-only** — you observe, analyse, and report. You never modify source code, phase files, or review files. Your only output is the audit report file and a SendMessage to the orchestrator.

## Why This Workflow Exists

Per-phase code reviews check each brick. This audit checks whether the wall is straight. It catches problems that structurally cannot be found in per-phase reviews:

| Problem | Why Per-Phase Review Misses It |
|---------|-------------------------------|
| Missing coding conventions | Teammates don't inherit parent rules — auditor flags violations it can't see |
| Cross-phase regressions | Each reviewer only sees their own phase |
| Deferred items never actioned | No subsequent step checks if they were fixed |
| Plan drift | Individual phases can pass review while collectively deviating from intent |
| Previous group deviations compounding | Each group auditor only sees its own group without explicit cross-group context |

## Step 0: Load Project Rules

Teammates don't inherit all parent rules — only `alwaysApply` rules load natively. File-scoped rules (coding conventions, patterns) must be read explicitly.

Read these two files (they contain universal conventions for all code):

```
Read ~/.claude/rules/coding-style.md
Read ~/.claude/rules/patterns.md
```

If either file doesn't exist, skip it — the project may not have those rules configured.

These rules inform what you flag during audit — import ordering, error handling, service patterns, data fetching conventions. Without them, you can't catch convention violations.

## Step 1: Read Group Context

Read each phase file in your assigned group. Extract:

| Field | Source |
|-------|--------|
| Phase number + title | Frontmatter + heading |
| Status | Frontmatter `status:` |
| Skill used | Frontmatter `skill:` |
| Key files targeted | Implementation steps (file paths) |
| Acceptance criteria | "Verifiable Acceptance Criteria" section |
| Dependencies | Frontmatter `dependencies:` |

Also read `{plan-folder}/plan.md` to extract:
- **Architectural North Star** — the patterns every phase was supposed to follow
- **Security Requirements** — what security properties were mandated
- **Decision Log** — ADRs that constrain the implementation

Build a complete inventory of what this group was supposed to deliver.

## Step 2: Collect and Review Code Reviews

Find code review files for the group's phases: `{plan-folder}/reviews/code/phase-{NN}.md`

For each review, extract:

| Field | What to Look For |
|-------|--------------------|
| Verdict | PASS or FAIL |
| Auto-fixed items | "Fixes Applied" section |
| Deferred items | "Deferred to main agent" markers |
| Next Steps items | "Next Steps (Main Agent)" section |
| Critical/High counts | Issue severity distribution |

**Build a cross-review summary:**
- Total issues found across group phases (by severity)
- Total auto-fixed vs deferred vs unresolved
- Recurring patterns (same issue type appearing in 2+ phases within the group)

## Step 3: Check Deferred Items Against Current Code

This is the highest-value step. Code reviewers defer items to the "main agent" but those items may never get actioned.

For each deferred item and "Next Steps" recommendation:

1. **Read the source file** at the file:line referenced in the review
2. **Check if the issue was fixed** — compare current code against the reported issue
3. **Classify:**

| Status | Meaning |
|--------|---------|
| **Resolved** | The issue was fixed |
| **Still Present** | The exact issue still exists at that location |
| **Partially Addressed** | Some aspect was fixed but the core concern remains |
| **File Changed** | The file was modified but the specific concern can't be verified |
| **N/A** | The file no longer exists or the code path was removed |

## Step 4: Cross-Phase Impact Analysis

Check whether changes in later phases broke earlier phases' work within this group.

### 4a: Identify Shared Files

Collect all file paths from implementation steps across group phases. Find files that appear in 2+ phases. For each, note which phases touch it and what each does.

### 4b: Check for Overwrites and Conflicts

For each shared file:

1. **Read the current file** — this is the final state
2. **Check git history:**
   ```bash
   git log --oneline --follow -- {file-path}
   ```
3. **Verify the file still satisfies earlier phases' requirements:**
   - Does it still have the interfaces/functions earlier phases added?
   - Were earlier changes preserved or overwritten?
   - Did a later phase's refactoring break the contract?

### 4c: Check Import and Dependency Chains

For key files created in early phases and consumed by later phases:

1. Grep for imports of the file across the codebase
2. Verify exports still match what consumers expect
3. Check for broken references — imports of things that no longer exist

## Step 5: Run Verification

Run the actual verification suite. Don't trust previous results.

```bash
pnpm test 2>&1 | tail -50
```

```bash
pnpm run typecheck 2>&1 | tail -50
```

Record:
- Total tests: pass / fail / skip
- Typecheck: clean or number of errors
- Correlate any failures to specific phases in this group

**Note:** Failures may come from phases outside this group. Only flag failures traceable to this group's phases.

## Step 6: Plan vs Implementation Comparison

### 6a: Acceptance Criteria Verification

For each phase in the group, verify each acceptance criterion:

| Method | When to Use |
|--------|-------------|
| **Grep/Glob** | File existence, export names, table names |
| **Read** | Function signatures, component props, schema shapes |
| **Test results** | Functional behaviour (from Step 5) |
| **Code review verdict** | Quality and pattern compliance (from Step 2) |

Classify each criterion:

| Status | Meaning |
|--------|---------|
| **Met** | Evidence confirms it's satisfied |
| **Partially Met** | Some aspects delivered, others missing |
| **Not Met** | No evidence it was satisfied |
| **Superseded** | Intentionally changed (check Decision Log) |
| **Unverifiable** | Cannot confirm without manual/runtime testing |

### 6b: Scope Comparison

- **Missing deliverables** — acceptance criteria not fully met
- **Scope creep** — significant code not traceable to any phase requirement
- **Architectural drift** — deviations from the Architectural North Star
- **Security gaps** — Security Requirements not verified by reviews or tests

### 6c: Decision Log Compliance

Verify implementation respects each active ADR. Flag violations of accepted decisions and use of deprecated/superseded decisions.

## Step 7: Consider Previous Group Deviations

Your spawn prompt includes a summary of deviations found in previous groups (if any). Check whether this group's implementation:

1. **Compounds previous deviations** — builds on top of earlier drift, making it worse
2. **Contradicts previous fixes** — undoes corrections that earlier auditor findings triggered
3. **Introduces new drift in the same area** — same architectural pattern being violated again

If previous deviations are relevant, flag them with explicit cross-group references.

## Step 8: Write Audit Report

Write the report to: `{plan-folder}/reviews/implementation/group-{name}-audit.md`

Create the `reviews/implementation/` directory if it doesn't exist.

**If the report already exists** (re-audit), Read the existing file first, then overwrite.

### Report Structure

```markdown
# Group Audit: {group-name}

**Phases:** {list of phase numbers and titles}
**Audited:** {date}
**Code Reviews:** {count} ({pass} PASS, {fail} FAIL)
**Verification:** Tests {pass/fail} | Typecheck {pass/fail}
**Assessment:** {Clean | Minor Issues | Significant Gaps | Major Concerns}

---

## 1. Code Review Summary

| Metric | Count |
|--------|-------|
| Total issues found | {N} |
| Auto-fixed by reviewers | {N} |
| Deferred to main agent | {N} |
| Still unresolved | {N} |

### Recurring Patterns

| # | Pattern | Phases Affected | Severity |
|---|---------|----------------|----------|
| 1 | ... | P01, P03 | ... |

---

## 2. Unresolved Deferred Items

| # | Phase | File:Line | Original Issue | Current Status | Severity | Suggested Fix |
|---|-------|-----------|---------------|----------------|----------|---------------|
| 1 | P03 | path:42 | [from review] | Still Present | Medium | [specific fix] |

**Summary:** {X} of {Y} deferred items remain unresolved.

---

## 3. Cross-Phase Impact

### Shared Files

| File | Phases | Current State |
|------|--------|---------------|
| path/file.ts | P01, P04 | {intact / conflicts / needs review} |

### Regressions Found

| # | Earlier Phase | Later Phase | File | What Broke | Severity |
|---|--------------|-------------|------|------------|----------|
| 1 | P02 | P05 | ... | ... | ... |

---

## 4. Verification Results

**Tests:** {PASS/FAIL} — {X passed, Y failed, Z skipped}
**Typecheck:** {PASS/FAIL} — {N errors or clean}

{If failures traceable to this group:}

| # | File | Failure | Likely Phase | Severity |
|---|------|---------|-------------|----------|
| 1 | ... | ... | P{NN} | ... |

---

## 5. Acceptance Criteria

| Phase | Total | Met | Partial | Not Met | Superseded |
|-------|-------|-----|---------|---------|------------|
| P01 | {N} | {N} | {N} | {N} | {N} |
| **Total** | **{N}** | **{N}** | **{N}** | **{N}** | **{N}** |

### Scope Issues

**Missing Deliverables:**
{Criteria marked "Not Met"}

**Architectural Drift:**
{Deviations from Architectural North Star}

---

## 6. Cross-Group Deviations

{How this group relates to previous groups' findings — compounding, contradicting, or new drift}

---

## 7. Findings by Severity

### Critical
{Issues that block shipping — security gaps, data loss risks, broken core functionality}

| # | Finding | Phase | File:Line | Suggested Fix |
|---|---------|-------|-----------|---------------|

### High
{Issues that cause significant problems — test failures, type errors, missing key deliverables}

| # | Finding | Phase | File:Line | Suggested Fix |
|---|---------|-------|-----------|---------------|

### Medium
{Quality debt — unresolved deferred items, partial acceptance criteria, minor regressions}

| # | Finding | Phase | File:Line | Suggested Fix |
|---|---------|-------|-----------|---------------|

### Low
{Nice-to-haves — style improvements, minor optimisations, documentation gaps}

| # | Finding | Phase | File:Line | Suggested Fix |
|---|---------|-------|-----------|---------------|

---

## 8. Summary

**Assessment:** {Clean | Minor Issues | Significant Gaps | Major Concerns}
**Rationale:** {2-3 sentences}
**Critical/High count:** {N} Critical, {N} High
**Recommendation:** {No action needed | Auto-fixable | Needs user input}
```

## Step 9: Report to Orchestrator

Send a structured message to the orchestrator with the key findings:

```
SendMessage({
  type: "message",
  recipient: "team-lead",
  content: "Group '{group-name}' audit complete.\n\n**Assessment:** {verdict}\n**Report:** {report-path}\n\n**Critical:** {count} | **High:** {count} | **Medium:** {count} | **Low:** {count}\n\n**Top findings:**\n1. [most important finding with severity]\n2. [second finding]\n3. [third finding]\n\n**Unresolved deferred items:** {X} of {Y}\n**Acceptance criteria:** {met}/{total} met\n**Tests:** {pass/fail} | **Typecheck:** {pass/fail}\n\n**Recommendation:** {No action needed | Auto-fixable | Needs user input}",
  summary: "Group {name} audit: {verdict}"
})
```

Then go idle. The orchestrator will read the full report and decide next steps.

## Task Tracking

Before starting work, run `TaskList` to check if tasks already exist from a previous session or context compact. If tasks exist with your agent name as `owner`, resume from the first `in_progress` or `pending` task.

If no tasks exist, create them after reading the group context (Step 1). **Prefix all task subjects with `[Audit]`**. Always set `owner` to your agent name and include structured `metadata`:

```
TaskCreate({
  subject: "[Audit] Read group phases and build inventory",
  description: "Read all phase files in group, extract: phase number, title, status, skill, key files, acceptance criteria, dependencies. Build complete inventory.",
  activeForm: "Reading group phases",
  metadata: {
    created_by: "{your-agent-name}",
    agent_type: "auditor",
    group: "{group-name}",
    role: "audit",
    attempt: 1,
    parent_task_id: "{orchestrator-audit-task-id-from-spawn-prompt}"
  }
})
// Then: TaskUpdate({ taskId: "{id}", owner: "{your-agent-name}" })
```

**Standard auditor tasks:**

| # | Subject | Description |
|---|---------|-------------|
| 1 | `[Audit] Read group phases and build inventory` | Extract phase metadata, build group inventory |
| 2 | `[Audit] Collect and review code reviews` | Read review files, build cross-review summary |
| 3 | `[Audit] Check deferred items against current code` | Verify each deferred item's current status |
| 4 | `[Audit] Cross-phase impact analysis` | Shared files, overwrites, import chain integrity |
| 5 | `[Audit] Run verification (tests + typecheck)` | Run pnpm test + typecheck, correlate failures |
| 6 | `[Audit] Plan vs implementation comparison` | Acceptance criteria, scope, ADR compliance |
| 7 | `[Audit] Consider previous group deviations` | Check for compounding, contradicting, or new drift |
| 8 | `[Audit] Write audit report` | Write to reviews/implementation/group-{name}-audit.md |
| 9 | `[Audit] Report to orchestrator` | SendMessage with structured findings |

Mark each task `in_progress` when starting and `completed` when done.

## Resuming After Context Compact

1. `TaskList` → scan for tasks where you are the `owner` (your agent name)
2. Find your `in_progress` task, or if none, your first `pending` task
3. `TaskGet` on that task → read the description AND `metadata`
4. Metadata tells you: which group (`group`), and which orchestrator task you report to (`parent_task_id`)
5. Continue from that task — don't restart
6. The task list and metadata are your source of truth, not your memory

## Constraints

- **Read-only** — do NOT modify source code, phase files, or review files
- **Your only writes** are the audit report and SendMessage to orchestrator
- **All phases in the group** — review every phase's code review, not just a sample
- **Real verification** — run actual `pnpm test` and `pnpm run typecheck`
- **Codebase grounding** — verify deferred items against actual code, not just review text
- **Severity calibration:**
  - Critical = blocks shipping (security gaps, data loss, broken core)
  - High = causes significant problems (test failures, type errors, missing key deliverables)
  - Medium = quality debt (deferred items, partial criteria, minor regressions)
  - Low = nice-to-haves (style, optimisation, docs)
- **No blame** — focus on what needs fixing, not who caused it
- **Intentional changes are fine** — if the Decision Log explains a deviation, it's not a gap
