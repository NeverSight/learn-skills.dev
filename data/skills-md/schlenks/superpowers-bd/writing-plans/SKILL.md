---
name: writing-plans
description: Use when you have a spec or requirements for a multi-step task, before touching code
---

# Writing Plans

Write comprehensive implementation plans assuming zero codebase context. Document: which files to touch, code, testing, docs, how to test. Bite-sized tasks. DRY. YAGNI. TDD. Frequent commits. Assume skilled developer, minimal domain knowledge, weak test design.

**Announce at start:** "I'm using the writing-plans skill to create the implementation plan."
**Context:** Run in a dedicated worktree (created by brainstorming skill).
**Save plans to:** `docs/plans/YYYY-MM-DD-<feature-name>.md`
**REQUIRED:** Before ExitPlanMode, run Plan Verification Checklist, then rule-of-five-plans. Verify *what* before polishing *how* -- scope errors caught early save wasted polish on deleted tasks.

## Mandatory Tasks (Enforcement)

Create these 7 native tasks at plan start (each blocked by previous via addBlockedBy). Cannot call ExitPlanMode with pending tasks:

1. **Write draft plan** -- Initial structure with all tasks, dependencies, file lists
   - After saving the plan to disk, show a copy-pasteable `/compact` command with the **actual plan file path** substituted (not a placeholder). Format: `Plan written to {actual path}. Run this to free context for verification:` followed by the command on its own line: `/compact Verification phase. Plan saved to {actual path} — re-read it from disk for each verification pass. Next: task 2 (Plan Verification Checklist), then tasks 3-7 (rule-of-five-plans: Draft, Feasibility, Completeness, Risk, Optimality). Drop all research findings, approach comparisons, and decision rationale. The plan speaks for itself.`
   - Also tell the user: **"After compaction finishes, type `continue` to resume verification."** (`/compact` doesn't give the model a turn — a follow-up message is required to restart.)
   - Wait for the user's follow-up message, then proceed to task 2
2. **Plan Verification Checklist** -- Complete/Accurate/Commands valid/YAGNI/Minimal/Not over-engineered
3. **Rule-of-five-plans: Draft pass** -- Shape and structure
4. **Rule-of-five-plans: Feasibility pass** -- Can every step be executed? Deps available? Paths valid?
5. **Rule-of-five-plans: Completeness pass** -- Every requirement traced to a task?
6. **Rule-of-five-plans: Risk pass** -- What could go wrong? Migration, breaking changes?
7. **Rule-of-five-plans: Optimality pass** -- Simplest approach? YAGNI?

**Tasks 2-7: Sub-Agent Dispatch.** After user types "continue", dispatch each pass sequentially as a **sonnet** sub-agent using the template in `references/verification-dispatch.md`. Mark each native task in_progress before dispatch, completed after collecting verdict. If any verdict is BLOCKED/FAIL, stop and report to user. After all 6 verdicts collected, assemble Verification Record (see `references/verification-footer.md`) and append to plan file.

See `references/task-enforcement-examples.md` for full TaskCreate blocks and dispatch loop.

## Bite-Sized Task Granularity

Each step is one action (2-5 min): write failing test, run it to verify failure, implement minimal code, run test to verify pass, commit.

## Plan Document Header

Every plan MUST start with:

```markdown
# [Feature Name] Implementation Plan

> **For Claude:** After human approval, use plan2beads to convert this plan to a beads epic, then use `superpowers-bd:subagent-driven-development` for parallel execution.

**Goal:** [One sentence]
**Architecture:** [2-3 sentences]
**Tech Stack:** [Key technologies]
**Key Decisions:**
- **[Area]:** [Choice] -- [Why over alternatives]
---
```

Key Decisions: 3-5 decisions implementers might question. WHAT was decided AND WHY. Focus where alternatives existed.

## File Structure

Before defining tasks, map out which files will be created or modified and what each one is responsible for. This is where decomposition decisions get locked in.

```markdown
| File | Responsibility | Action |
|------|---------------|--------|
| `exact/path/to/file.py` | One clear responsibility | Create |
| `exact/path/to/existing.py` | One clear responsibility | Modify |
| `tests/exact/path/to/test.py` | Tests for file.py | Create |
```

- Design units with clear boundaries and well-defined interfaces. Each file should have one clear responsibility.
- Prefer smaller, focused files. Files that can be held in context at once produce more reliable edits.
- Files that change together should live together. Split by responsibility, not by technical layer.
- In existing codebases, follow established patterns. If a file has grown unwieldy, including a split in the plan is reasonable.

This structure informs task decomposition. Each task's `Files:` section must reference entries from this table — no task should introduce files not listed here.

## Task Structure

**CRITICAL: Every task MUST include `Depends on:`, `Complexity:`, and `Files:` sections.** These enable safe parallel execution, model selection, and file conflict detection. See `references/dependency-analysis.md` and `references/file-lists.md`.

Recommended context: `Purpose:` (why), `Not In Scope:` (prevents overbuilding), `Gotchas:` (quirks).

```markdown
### Task N: [Component Name]
**Depends on:** Task M, Task P | None
**Complexity:** simple | standard | complex
**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Purpose:** [One sentence]

**Step 1: Write the failing test**
[code block]
**Step 2: Run test to verify it fails**
Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL
**Step 3: Write minimal implementation**
[code block]
**Step 4: Run test to verify it passes**
Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS
**Step 5: Commit**
`git add ...` then `git commit -m "feat: add specific feature"`
```

## Plan Verification Checklist

Before rule-of-five-plans, verify scope and accuracy:

- **Complete** -- All requirements from brainstorming addressed?
- **Accurate** -- File paths verified? (existing files exist, new files in correct locations)
- **Commands valid** -- Test/build commands correct and runnable?
- **YAGNI** -- Every task directly serves a stated requirement?
- **Minimal** -- Could any task be removed/combined without losing functionality?
- **Not over-engineered** -- Simplest approach that works?
- **Key Decisions documented** -- 3-5 decisions with rationale?
- **Context sections present** -- Purpose for non-obvious tasks? Not In Scope for boundary tasks?
- **File Structure complete** -- Every file in task `Files:` sections appears in File Structure table? No undeclared files?

## Remember

- Exact file paths always
- Complete code in plan (not "add validation")
- Exact commands with expected output
- Reference relevant skills by name
- **Every task needs `Depends on:`, `Complexity:`, and `Files:`**
- **Include `Purpose:`, `Not In Scope:`, `Gotchas:` where needed**
- **File Structure table before tasks — tasks reference it, never introduce undeclared files**
- **Run Plan Verification Checklist before rule-of-five-plans**
- **Announce each verification phase** (see `references/announcements-protocol.md`)
- **Plan MUST end with Verification Record** (see `references/verification-footer.md`)
- **After approval, follow execution handoff** (see `references/execution-handoff.md`)

## Reference Files

- `references/task-enforcement-examples.md`: Full TaskCreate blocks with blocked-by relationships
- `references/dependency-analysis.md`: Identifying and expressing task dependencies
- `references/file-lists.md`: File list format, parallel execution rules, and complexity estimation
- `references/announcements-protocol.md`: Required announcement templates for verification phases
- `references/verification-dispatch.md`: Sub-agent prompt templates and dispatch flow for verification passes
- `references/verification-footer.md`: Plan Document Footer template (Verification Record)
- `references/execution-handoff.md`: Post-plan workflow: plan2beads -> subagent-driven-development

<!-- compressed: 2026-02-11, original: 915 words, compressed: 599 words -->
