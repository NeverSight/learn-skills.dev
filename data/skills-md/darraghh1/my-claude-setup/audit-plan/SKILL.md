---
name: audit-plan
description: "Audit implementation plans for phase-to-phase dependencies, data flow consistency, ordering logic, and stale artifacts. Produces a risk-assessed flow audit report."
argument-hint: "[plan-folder]"
context: fork
agent: general-purpose
model: sonnet
allowed-tools: "Read Grep Glob Write Edit Bash(uv run*) TaskCreate TaskUpdate TaskList TaskGet"
metadata:
  version: 1.2.0
---

<!-- ultrathink: Enable extended thinking for holistic flow analysis -->

# Plan Flow Audit

**YOUR ARGUMENTS: `$ARGUMENTS`**

Arguments are provided above via `$ARGUMENTS`. Parse them to determine the plan folder path (e.g., `plans/detector-refactor`). Do NOT ask the user to re-provide the path.

This skill performs a **holistic flow audit** of a multi-phase implementation plan. It assesses whether phases connect coherently as a pipeline — NOT whether individual phases comply with templates (that's `/review-plan`'s job).

## Critical

- Do NOT modify plan files, phase files, or codebase files — this skill only writes the audit report
- Read ALL phase files, not just a sample — the value of this audit is completeness
- Ground findings in actual codebase files, not just plan documents
- When you claim a phase targets a file that doesn't exist, verify with Glob first
- Distinguish between intentional design choices and actual discrepancies

## Task Tracking

Tasks survive context compacts — skipping this check causes lost progress and repeated work.

Before starting work, run `TaskList` to check if tasks already exist from a previous session or before a compact. If tasks exist:
1. Read existing tasks with `TaskGet` for each task ID
2. Find the first task with status `pending` or `in_progress`
3. Resume from that task — do NOT recreate the task list

If no tasks exist, create them after reading the master plan (Step 1):

**Example task list:**
```
Task 1: Read the master plan
Task 2: Read all phase files and extract metadata
Task 3: Build dependency graph
Task 4: Assess data flow consistency
Task 5: Evaluate phase ordering
Task 6: Identify stale artifacts
Task 7: Cross-check "Done" phases against codebase
Task 8: Assess risk for pending phases
Task 9: Write audit report
Task 10: Return summary
```

Mark each task `in_progress` when starting and `completed` when done.

## Why This Audit Exists

`/review-plan` checks individual files. This audit checks the **connections between them**. Problems that only appear at the whole-plan level:

| Problem | How It Manifests | Cost If Missed |
|---------|-----------------|----------------|
| Circular dependencies | Phase A waits for B, B waits for A — deadlock | Implementation stalls, requires plan restructuring |
| Missing dependencies | Phase 5 uses a table from Phase 3 but doesn't declare it | Phase 5 fails at runtime, debugging time wasted |
| Wrong ordering | Consumer phase runs before its data producer | Code compiles but crashes, phase must be re-sequenced |
| Stale artifacts | plan.md says "Done" but phase file says "Pending" | `/implement` picks the wrong next phase |
| "Done" phase not actually done | Phase marked complete but deliverables missing from codebase | Downstream phases build on a false foundation |

The audit report feeds into `/implement` — it checks the plan review verdict before building. A flow audit catches structural problems that per-phase reviews cannot see.

## Output Location

The flow audit report goes in the `reviews/planning/` subfolder alongside per-phase reviews:

**Write to:** `{plan-folder}/reviews/planning/flow-audit.md`

Examples:
- `plans/250202-voice-assistant/reviews/planning/flow-audit.md`
- `plans/250202-api-refactor/reviews/planning/flow-audit.md`

Create the `reviews/planning/` directory if it doesn't exist.

> **Note:** Per-phase template/codebase reviews go in the same folder — see `/review-plan`. Code/implementation reviews go in `reviews/code/` — see `/code-review`.

---

## Step 1: Read the Master Plan

Read `{plan-folder}/plan.md` completely. Extract:

1. **Phase table** — all phases with titles, status, and any noted issues
2. **ADRs / Decision Log** — decisions that constrain phase design
3. **Critical Issues section** — known problems already documented
4. **Architectural North Star** — patterns all phases must follow

Note any phases marked as deprecated, renumbered, or amended.

## Step 2: Read All Phase Files

Use Glob to find all phase files: `{plan-folder}/phase-*.md`

For EACH phase file, extract from the frontmatter and overview:

| Field | Where to Find |
|-------|---------------|
| Phase number | Filename `phase-NN-*` |
| Title | Frontmatter `title:` |
| Status | Frontmatter `status:` |
| Dependencies | Frontmatter `dependencies:` |
| What it produces | Overview section |
| What it consumes | "How This Phase Fits" or "Prerequisites" sections |
| Key files it targets | Implementation steps (file paths mentioned) |

Build a mental model of the full dependency graph as you read.

### Placeholder Check

Run the placeholder validator across all phase files to catch skeleton content early:

```bash
echo '{"cwd":"."}' | uv run $CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_no_placeholders.py \
  --directory {plan-folder} --extension .md
```

If the validator exits non-zero, flag any placeholder-containing phases as stale artifacts in the report (Step 6). Phases with `[To be detailed]`, `TBD`, or other skeleton markers cannot be meaningfully audited for flow.

## Step 3: Build Dependency Graph

From the data collected in Step 2, construct the full dependency graph.

**For each phase, document:**
- Declared dependencies (from frontmatter `dependencies:` field)
- Implicit dependencies (phase references data/files/services created by another phase but doesn't declare it)
- What downstream phases depend on it

**Check for:**

| Issue Type | How to Detect |
|------------|---------------|
| Circular dependencies | Phase A depends on B, B depends on A (directly or transitively) |
| Missing dependencies | Phase X uses output from Phase Y but doesn't list Y in dependencies |
| Unnecessary dependencies | Phase X lists Phase Y but doesn't actually use any of Y's output |
| Orphaned phases | Phase exists but no other phase depends on it AND it doesn't depend on anything |
| Dependency on deprecated phase | A phase depends on a phase marked `status: deprecated` |

## Step 4: Assess Data Flow Consistency

Trace how data flows through the plan pipeline. For plans involving data transformations (API -> storage -> consumption), check:

1. **Source consistency** — Do all phases agree on where data comes from?
2. **Schema consistency** — Do phases that share data structures use the same types/interfaces?
3. **Pattern consistency** — Is there one architectural pattern or do different phases use contradictory approaches?
   - Example: Some phases have components query the database directly while others expect data passed via context/props
4. **Table/entity naming** — Do all phases reference the same table names consistently?
5. **File path consistency** — Do phases reference files that actually exist at those paths?

**Verify against codebase:** For key files referenced by "Done" phases, use Glob to check they exist. For critical claims (e.g., "Phase 11 updated the orchestrator to load summary data"), read the actual file to confirm.

## Step 5: Evaluate Phase Ordering

Assess whether the current phase sequence makes logical sense:

1. **Infrastructure before consumers** — Are foundational phases (schemas, services, APIs) ordered before phases that use them?
2. **Producers before consumers** — Does the phase that creates data run before phases that read it?
3. **Refactoring order** — For refactoring plans, is the new system built before the old system is deprecated/removed?
4. **Test timing** — Are testing phases positioned to test code that already exists?
5. **Cleanup last** — Are deprecation, migration, and drop phases at the end?

**Flag ordering issues like:**
- A consumer phase runs before its data producer
- A centralized service is created AFTER the things that should use it
- Tests are written before the code they test exists
- Cleanup runs before all references are migrated

## Step 6: Identify Stale Artifacts

Check for:

| Artifact | How to Find |
|----------|-------------|
| Deprecated phase files | `status: deprecated` in frontmatter but file still exists |
| Duplicate phase numbers | Multiple files with same `phase-NN-` prefix |
| Broken inter-phase links | `[[phase-XX]]` or `[Phase XX](./phase-XX-*)` links that point to non-existent files |
| Renumbered but not updated | Phase file title says "Phase 17" but filename says `phase-18-*` |
| Phase table mismatches | plan.md phase table lists a phase title/file that doesn't match the actual file |
| Stale status | plan.md says "Done" but phase file says "Pending" (or vice versa) |

## Step 7: Cross-Check "Done" Phases Against Codebase

For phases marked as "Done", spot-check 2-3 key claims against the actual codebase:

1. Pick 2-3 "Done" phases that make testable claims (e.g., "created table X", "updated file Y", "added field Z to interface")
2. Use Glob/Grep to verify the claim holds in the codebase
3. Check if `{plan-folder}/reviews/code/phase-{NN}.md` exists for each "Done" phase — a passing code review verdict is stronger evidence than file existence alone
4. Flag any "Done" phases whose deliverables can't be found

This prevents the plan from proceeding on a false foundation.

## Step 8: Assess Risk for Pending Phases

For each pending phase, evaluate risk based on:

| Risk Factor | High Risk | Low Risk |
|-------------|-----------|----------|
| Dependencies | Depends on phases with known issues | Dependencies are clean and verified |
| File targets | References files that don't exist or are uncertain | Targets well-known, stable files |
| Scope | Touches many files across many directories | Focused on 1-2 files |
| Pattern clarity | Introduces new patterns not seen in codebase | Follows established patterns from "Done" phases |
| Blocking | Many downstream phases depend on it | Few or no downstream dependencies |

## Step 9: Write Audit Report

Write the report to: `{plan-folder}/reviews/planning/flow-audit.md`

Create the `reviews/planning/` directory if it doesn't exist.

**If the report already exists** (re-auditing after fixes), Read the existing file first — the Write tool silently fails on existing files without a prior Read. A re-audit should fully overwrite the previous report since the value is a fresh holistic view, not incremental updates.

### Report Structure

```markdown
# Flow Audit: {Plan Title}

**Audited:** {date}
**Phases reviewed:** {count} ({done count} Done, {pending count} Pending, {deprecated count} Deprecated)
**Overall Assessment:** {Coherent | Minor Issues | Significant Issues | Major Restructuring Needed}

---

## 1. Dependency Graph

{Visual or textual representation. Use indentation to show dependency chains.}

### Dependency Issues

| # | Issue | Phases Affected | Severity | Suggested Fix |
|---|-------|----------------|----------|---------------|
| 1 | ... | P05, P12 | High | ... |

---

## 2. Data Flow Analysis

### Architecture Pattern(s)

{Describe the data flow pattern(s) used across the plan}

### Inconsistencies

| # | Issue | Phases Affected | Details |
|---|-------|----------------|---------|
| 1 | ... | ... | ... |

---

## 3. Phase Ordering Assessment

### Current Order
{List phases in order with one-line description}

### Ordering Issues

| # | Issue | Current Order | Suggested Order | Rationale |
|---|-------|--------------|-----------------|-----------|
| 1 | ... | P12 after P11 | P12 before P11 | Loader should exist before orchestrator uses it |

---

## 4. Stale Artifacts

| # | Artifact | Type | Location | Action Needed |
|---|----------|------|----------|---------------|
| 1 | ... | Deprecated file | phase-17-unit-tests-update.md | Delete or archive |

---

## 5. "Done" Phase Verification

| Phase | Claim Checked | Verified? | Notes |
|-------|--------------|-----------|-------|
| P01 | Summary table created | Yes/No | ... |
| P11 | Orchestrator loads summaries | Yes/No | ... |

---

## 6. Risk Assessment (Pending Phases)

| Phase | Risk | Key Risk Factors | Recommendation |
|-------|------|-----------------|----------------|
| P12 | High | Depends on P11 which may have ordering issues | Review dependency direction |
| P14 | Medium | Modifies Edge Function with complex existing logic | Read function before implementing |

---

## 7. Recommendations (Priority Order)

1. **[Critical]** {Description} — Fix before continuing implementation
2. **[High]** {Description} — Fix before implementing affected phases
3. **[Medium]** {Description} — Fix for plan hygiene
4. **[Low]** {Description} — Nice to have
```

## Step 10: Return Summary

After writing the report, return to the main agent:

1. **Report location** — file path
2. **Overall assessment** — one-line verdict
3. **Critical/High issues count** — how many need attention before implementation continues
4. **Top 3 findings** — the most impactful discoveries
5. **Recommendation** — whether to proceed, fix first, or restructure

---

## Resuming After Context Compact

If you notice context was compacted or you're unsure of current progress:

1. Run `TaskList` to see all tasks and their status
2. Find the `in_progress` task — that's where you were
3. Run `TaskGet {id}` on that task to read full details
4. Continue from that task — don't restart from the beginning

Tasks persist across compacts. The task list is your source of truth for progress, not your memory.

**Pattern for every work session:**
```
TaskList → find in_progress or first pending → TaskGet → continue work → TaskUpdate (completed) → next task
```

## Constraints

- **Source files are read-only** — do NOT modify plan files, phase files, or codebase files. The only file you write is the audit report at `{plan-folder}/reviews/planning/flow-audit.md`
- **All phases** — read every phase file, not just a sample
- **Codebase grounding** — verify at least 2-3 "Done" phase claims against actual code. Use file paths from the phases themselves (implementation steps list target files)
- **No template checking** — that's `/review-plan`'s job. Focus on flow, not format
- **Severity calibration** — only mark issues as Critical if they would cause implementation failure. Use High for likely problems, Medium for hygiene issues, Low for suggestions
- **Pipeline awareness** — `/implement` checks the plan review verdict before building. Your audit report influences whether implementation proceeds or blocks

## Troubleshooting

### Too Many Phase Files

**Symptom:** Plan has 30+ phases and reading all of them is slow.

**Fix:** Read frontmatter + overview section only (first 60 lines) for initial pass. Deep-read only phases flagged as problematic during the dependency/flow analysis.

### Plan Has No Dependency Metadata

**Symptom:** Phase files don't have `dependencies:` in frontmatter.

**Fix:** Infer dependencies from content — look for "requires Phase X", "uses table from Phase Y", "after Phase Z is complete" in the overview and prerequisites sections. Flag the missing metadata as a stale artifact.

### "Done" Phase Can't Be Verified

**Symptom:** Phase claims to have modified a file but Glob/Grep can't confirm.

**Fix:** Don't assume the phase wasn't implemented — the file might have been refactored or renamed since. Check git history if available, or note as "Unverifiable" rather than "Not Done."
