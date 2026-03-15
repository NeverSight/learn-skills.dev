---
name: rule-of-five-plans
description: Use when writing 50+ lines of plans, design docs, skill documents, or process documentation - apply 5 focused passes (Draft, Feasibility, Completeness, Risk, Optimality) to catch issues single-shot generation misses
---

# Rule of Five — Plans

Each pass has ONE job. Re-read the entire artifact through that lens. See `references/pass-order-rationale.md` for order rationale.

## Quick Start

**Create native tasks for 5 passes with sequential dependencies:**

```
TaskCreate: "Pass 1: Draft"
  description: "Shape and structure. All sections sketched. Task list complete. Breadth over depth."
  activeForm: "Drafting"

TaskCreate: "Pass 2: Feasibility"
  description: "Can every step be executed? Dependencies available? Paths valid? Estimates realistic?"
  activeForm: "Checking feasibility"
  addBlockedBy: [draft-task-id]

TaskCreate: "Pass 3: Completeness"
  description: "Every requirement traced to a task? Gaps? Missing rollback? Missing error handling?"
  activeForm: "Checking completeness"
  addBlockedBy: [feasibility-task-id]

TaskCreate: "Pass 4: Risk"
  description: "What could go wrong? Migration risks? Data loss? Breaking changes? Parallel conflicts?"
  activeForm: "Assessing risk"
  addBlockedBy: [completeness-task-id]

TaskCreate: "Pass 5: Optimality"
  description: "Simplest approach? YAGNI? Could tasks be combined? Would you defend every task to a senior colleague?"
  activeForm: "Optimizing"
  addBlockedBy: [risk-task-id]
```

**ENFORCEMENT:**
- Each pass is blocked until the previous completes
- Cannot commit until all 5 tasks show `status: completed`
- TaskList shows your progress through the passes
- Skipping passes is visible - blocked tasks can't be marked in_progress

For each pass: re-read the full artifact, evaluate through that lens only, make changes, then mark task complete.

## Detection Triggers

Invoke when: >50 lines of plan/design doc/skill document written, implementation plans, architecture decisions, process documentation, or skill SKILL.md files.

For code, use `rule-of-five-code`. For tests, use `rule-of-five-tests`.

Skip for: Minor doc edits, trivial changes under 20 lines, README updates.

Announce: "Applying rule-of-five-plans to [artifact]. Starting 5-pass review."

## The 5 Passes

| Pass | Focus | Exit when... |
|------|-------|--------------|
| **Draft** | Shape and structure. All sections sketched, task list complete. | All major sections exist; task list complete |
| **Feasibility** | Can every step be executed? Deps available? Paths valid? Estimates realistic? | No infeasible steps; all references verified |
| **Completeness** | Every requirement traced to a task? Gaps? Missing rollback? | Every requirement maps to task(s) |
| **Risk** | What could go wrong? Migration, data loss, breaking changes, parallel conflicts? | Risks identified and mitigated |
| **Optimality** | Simplest approach? YAGNI? Could tasks be combined? | You'd defend every task to a senior colleague |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Multiple lenses in one pass | ONE lens per pass. Feasibility pass ignores optimality. |
| Checking for code bugs in plans | Plans don't have bugs — check feasibility and completeness instead. |
| Skipping Risk pass on "simple" plans | All 5 or none. Simple plans still have risks (wrong assumptions, missing deps). |
| Rushing through passes | Each pass: genuinely re-read the full artifact |
| Optimizing before checking completeness | Completeness before Optimality — don't simplify away requirements. |
| Not verifying file paths and commands | Feasibility pass: Glob for paths, verify commands exist. |

## Reference Files

- `references/pass-definitions.md`: Detailed pass definitions with checklists
- `references/pass-order-rationale.md`: Why this order for plans

<!-- compressed: 2026-02-11, original: 520 words, compressed: 520 words -->
