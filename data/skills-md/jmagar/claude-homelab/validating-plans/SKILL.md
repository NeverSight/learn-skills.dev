---
name: validating-plans
description: Use when validating an implementation plan created by writing-plans - coordinates parallel checks for hallucinations, TDD violations, missing references, and architectural issues before execution.
---

# Validating Plans

## Version History

- **v1.0.0** (2025-12-08): Initial release with agent-based validation
  - Three specialized validators: static-analyzer, environment-verifier, architecture-reviewer
  - Parallel execution for efficiency
  - TodoWrite integration for plan fixes
  - GitHub issue creation post-validation

## Overview

Systematically audit implementation plans before execution. Catch hallucinations, TDD violations, missing pieces, and logical gaps that derail implementations. Trust nothing - verify everything that can be verified.

**Announce at start:** "I'm using the validating-plans skill to audit this implementation plan."

**REQUIRED SUB-SKILL:** Use superpowers:writing-plans
**REQUIRED SUB-SKILL:** Use superpowers:executing-plans

**Input:** A plan document (from writing-plans skill)
**Output:** Validation report with issues categorized by severity

**Workflow Position:** Runs between `writing-plans` and `executing-plans`:
1. Brainstorm → 2. Write-plan → **3. Validate-plan** → 4. Execute-plan → 5. Finish-branch

---

## When to Use This Skill

Use this skill when:
- A plan document has been created by the writing-plans skill
- User explicitly requests validation with `/validate-plan`
- About to execute a plan and want to verify assumptions first
- Returning to an older plan that may need re-verification

**Do NOT use this skill for:**
- Validating code (use code-review skills instead)
- Planning implementation (use writing-plans instead)
- Executing plans (use executing-plans instead)

---

## Validation Process

### Step 1: Locate and Load Plan

Accept plan file path as argument:

```bash
PLAN_FILE="$1"

# Validate plan file exists
if [[ -z "$PLAN_FILE" ]]; then
    echo "🔴 ERROR: Plan file path required"
    echo "Usage: /validate-plan <path-to-plan-file>"
    exit 1
fi

if [[ ! -f "$PLAN_FILE" ]]; then
    echo "🔴 ERROR: Plan file not found: $PLAN_FILE"
    exit 1
fi

echo "📋 Validating: $PLAN_FILE"
```

### Step 2: Add Organization Note to Plan

**CRITICAL: Before running validation agents, add organization note to the plan file.**

Add this note to the top of the plan file (after the title/header):

```markdown
> **📁 Organization Note:** When this plan is fully implemented and verified, move this file to `docs/plans/complete/` to keep the plans folder organized.
```

**This is the ONLY edit made to the plan during validation phase.**

### Step 3: Launch Parallel Validation Agents

Spawn **3 parallel validation agents** using the Task tool in a **SINGLE message with 3 Task tool calls**:

**Agent 1: static-analyzer**
- Reference: `references/agent-guide.md`
- Validates: Plan structure, TDD compliance, coding principles (DRY/YAGNI/KISS)
- Returns: Structure and TDD compliance report

**Agent 2: environment-verifier**
- Reference: `references/agent-guide.md`
- Validates: Files exist, packages real, APIs valid, security vulnerabilities
- Returns: Environment verification report

**Agent 3: architecture-reviewer**
- Reference: `references/agent-guide.md`
- Validates: SOLID principles, design patterns, separation of concerns, scalability
- Returns: Architecture review report

**Launch Pattern:**

```
Task 1: Static Analysis
- subagent_type: "static-analyzer"
- description: "Analyze plan structure"
- prompt: "Validate the structure, TDD compliance, and internal consistency of: $PLAN_FILE"

Task 2: Environment Verification
- subagent_type: "environment-verifier"
- description: "Verify environment assumptions"
- prompt: "Verify all files, packages, and environment assumptions in: $PLAN_FILE"

Task 3: Architecture Review
- subagent_type: "architecture-reviewer"
- description: "Review architecture"
- prompt: "Review the architectural soundness and design quality of: $PLAN_FILE"
```

**CRITICAL: All 3 agents MUST be launched in ONE message with 3 tool calls.**

### Step 4: Aggregate Results

After all 3 agents complete, aggregate their findings into a unified validation report.

#### Severity Levels

```
🔴 BLOCKER   - Execution will fail. Plan references non-existent things. Must fix.
🟠 CRITICAL  - High risk of rework. TDD violation, stale line numbers. Should fix.
🟡 WARNING   - Suboptimal. Missing edge cases, vague steps. Consider fixing.
🔵 NIT       - Style/preference. Fix if time permits.
```

#### Validation Report Template

```markdown
# Plan Validation Report: [Feature Name]

**Plan:** `<plan-file-path>`
**Validated:** [timestamp]
**Verdict:** ✅ PASS | ⚠️ PASS WITH NOTES | 🔴 NEEDS REVISION

---

## Verification Summary

| Check | Status | Notes |
|-------|--------|-------|
| TDD Compliance | ✅/🔴 | [from static-analyzer] |
| File Targets | ✅/🔴 | [from environment-verifier] |
| Packages/Deps | ✅/🔴 | [from environment-verifier] |
| API Signatures | ✅/🔴 | [from environment-verifier] |
| Architecture | ✅/🟠/🔴 | [from architecture-reviewer] |

---

## Issues Found

### 🔴 BLOCKERS (N)
[Aggregated from all agents]

### 🟠 CRITICAL (N)
[Aggregated from all agents]

### 🟡 WARNINGS (N)
[Aggregated from all agents]

---

## Architecture Analysis
[From architecture-reviewer]

**Architectural Alignment:** ✅ ALIGNED | 🟠 CONCERNS | 🔴 VIOLATIONS

---

## Sign-off Checklist

- [ ] All blockers resolved
- [ ] Critical issues addressed or explicitly risk-accepted
- [ ] TDD order verified for all tasks
- [ ] All external references verified to exist
- [ ] Architecture alignment verified

**Validated by:** Claude Code
**Ready for execution:** YES / NO
```

### Step 5: Create TodoWrite Tasks for Plan Fixes

**CRITICAL: TodoWrite creates todos to FIX THE PLAN, not to fix the problems the plan would create.**

**IF validation finds blockers or critical issues:**

Create one todo PER blocker/critical issue:

```json
{
  "content": "Fix plan blocker: [specific issue in plan]",
  "activeForm": "Fixing plan blocker: [specific issue]",
  "status": "pending"
}
```

**Examples of CORRECT todos:**

✅ "Fix plan blocker: Update Task 3 to import from starlette.responses instead of hallucinated fastapi_utils"
✅ "Fix plan critical: Reorder Task 2 steps to test-first (TDD violation)"
✅ "Fix plan blocker: Change Task 5 target from non-existent src/services/legacy_auth.py to correct path"

**Examples of WRONG todos (these fix CODE, not PLAN):**

❌ "Fix: Install fastapi_utils package" (no, fix the plan to not use it)
❌ "Fix: Create missing src/services/legacy_auth.py file" (no, fix the plan path)
❌ "Add error handling to Task 3" (this changes implementation, not plan)

### Step 6: Provide Handoff Message

**If ✅ PASS (no issues):**

> "Plan validated - all references verified, TDD compliance confirmed. No plan fixes needed.
>
> Ready to proceed with GitHub issue creation or direct execution."

**If 🔴 NEEDS REVISION (blockers/criticals found):**

> "Found N blockers and M critical issues in the plan.
>
> Created N+M TodoWrite tasks to fix the PLAN document:
> 1. Fix plan blocker: [summary]
> 2. Fix plan critical: [summary]
>
> Complete these todos to update the plan file, then re-run /validate-plan to verify fixes."

**If ⚠️ PASS WITH NOTES (warnings only):**

> "Plan validation passed with N warnings (non-blocking).
>
> Warnings noted but no todos created (not critical for execution).
>
> Ready to proceed with GitHub issue creation or direct execution."

---

## GitHub Issue Creation (Post-Validation)

After successful validation (✅ PASS or ⚠️ PASS WITH NOTES), offer to create a GitHub issue.

Full workflow, prerequisites, prompts, and scripts live in:
`references/github-issue-workflow.md`

---

## Validation Checks Summary

### Phase 1: Static Analysis (static-analyzer)
- Plan structure validation
- Red-green-refactor cycle order
- DRY, YAGNI, KISS compliance
- Task granularity (2-5 minute steps)
- Test quality and naming

### Phase 2: Environment Verification (environment-verifier)
- File existence and line numbers
- Package existence in registries
- API signatures and exports
- Security vulnerability checks
- Command availability

### Phase 3: Architecture Review (architecture-reviewer)
- SOLID principles compliance
- Design pattern appropriateness
- Separation of concerns
- Technology stack alignment
- Scalability considerations

---

## Integration with Superpowers Workflow

**Plan Header Verification:**

Verify the plan contains the required header from writing-plans:

```markdown
> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.
```

**Plan Location Standard:**

Validate plan is in correct location: `docs/plans/YYYY-MM-DD-<feature-name>.md`

**Batch Execution Compatibility:**

- Verify tasks can be batched independently (default 3 tasks)
- Flag tasks with hidden dependencies
- Warn if batch size would be problematic

**TDD 5-Step Pattern:**

Validate each task follows this exact sequence:
1. Write failing test
2. Run to verify fail
3. Write minimal code
4. Run to verify pass
5. Commit

---

## Common Validation Scenarios

### Scenario 1: Plan Validates Clean

```
$ /validate-plan docs/plans/feature.md
📋 Validating: docs/plans/feature.md
✅ All checks passed
✅ Architecture aligned

Create GitHub issue? (y/n): y
✅ Issue created: #123

Ready for execution via /superpowers:executing-plans
```

### Scenario 2: Plan Has Blockers

```
$ /validate-plan docs/plans/feature.md
🔴 2 blockers found
🟠 1 critical issue found

Created 3 TodoWrite tasks to fix plan:
1. Fix plan blocker: Hallucinated package
2. Fix plan blocker: File not found
3. Fix plan critical: TDD violation

Complete todos → re-run /validate-plan
```

### Scenario 3: Architecture Concerns

```
$ /validate-plan docs/plans/feature.md
⚠️ PASS WITH NOTES

🟠 Architecture concerns:
  - Plan places business logic in controller layer
  - Recommendation: Extract to service layer per existing patterns

Create GitHub issue? (y/n): y
✅ Issue created with architecture notes: #124
```

---

## Remember

- Launch all 3 validation agents in parallel (single message, 3 tool calls)
- Only add organization note to plan (no other edits during validation)
- TodoWrite tasks fix THE PLAN, not the code
- Distinguish validation verdicts: ✅ PASS, ⚠️ PASS WITH NOTES, 🔴 NEEDS REVISION
- Offer GitHub issue creation only after successful validation
- Validation sits between writing-plans and executing-plans in workflow
