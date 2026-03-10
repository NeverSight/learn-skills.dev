---
name: deep-work
description: >
  Structured development workflow that separates research, planning, and implementation
  into distinct phases with persistent markdown artifacts. Use when starting any non-trivial
  feature, refactor, bug investigation, or codebase change. Trigger on: "deep work",
  "research and plan", "plan before coding", "write a plan", "research this codebase",
  "don't code yet", "understand then implement", or when the user wants a disciplined
  approach to a complex task. Also use when the user says "research", "plan", "annotate",
  "implement the plan", or references research.md/plan.md artifacts.
---

# Deep Work

Structured workflow that separates thinking from typing. Never write code until a written plan has been reviewed and approved.

## Workflow Overview

```
Research → Plan → Annotate (repeat 1-6x) → Todo List → Implement → Feedback
```

All artifacts persist as markdown files in `.claude/` (not the project root).

## Phase 1: Research

Deeply read the relevant codebase before doing anything else. Write findings to `.claude/research.md`.

**How to research:**
1. Read every file in the target area — not just signatures, but implementations, edge cases, error handling
2. Trace data flows end-to-end
3. Identify existing patterns, conventions, utilities, and caching layers
4. Note integration points with other parts of the system
5. Write a detailed report to `.claude/research.md`

**Research depth signals:** Read deeply. Understand intricacies. Go through everything. Surface-level reading is not acceptable. Continue until you have a thorough understanding.

**Template:** See [references/research-template.md](references/research-template.md) for the research document structure.

**Critical rule:** Stop after writing research.md. Do not proceed to planning until the user has reviewed the research and confirmed it's accurate.

## Phase 2: Plan

Write a detailed implementation plan to `.claude/plan.md`. Base the plan on the actual codebase — read source files before suggesting changes.

**Plan contents:**
- Explanation of the approach and rationale
- Code snippets showing actual changes (not pseudocode)
- File paths that will be modified or created
- Considerations and trade-offs
- Things explicitly not being changed and why

**Template:** See [references/plan-template.md](references/plan-template.md) for the plan document structure.

**Reference implementations:** If the user provides reference code from other projects, study it and adapt the approach to fit the current codebase's patterns.

**Critical rule:** End the plan with "Ready for your review. Add inline notes directly to `.claude/plan.md` and tell me when to address them." Do not implement.

## Phase 3: Annotation Cycle

The user adds inline notes directly into plan.md. When they say "address my notes" or similar:

1. Read `.claude/plan.md` thoroughly, finding all user annotations
2. User annotations are any text that wasn't in your original plan — look for corrections, questions, overrides, and constraints
3. Address every single annotation: update sections, remove rejected approaches, incorporate domain knowledge
4. Remove the annotation text itself after addressing it (keep the plan clean)
5. End with: "All notes addressed. Review again or say 'add the todo list' when satisfied."

**Critical rule:** Do not implement. The phrase "don't implement yet" is a hard constraint. Repeat the annotation cycle until the user explicitly approves.

## Phase 4: Todo List

When the user approves the plan, add a granular task checklist to `.claude/plan.md`:

```markdown
## Tasks

### Phase 1: [Phase Name]
- [ ] Task 1 — specific, actionable description
- [ ] Task 2 — specific, actionable description

### Phase 2: [Phase Name]
- [ ] Task 3 — specific, actionable description
- [ ] Task 4 — specific, actionable description
```

Each task should be small enough to complete in one focused step. Include all phases needed to fully implement the plan.

**Critical rule:** Do not implement yet. Wait for user confirmation to begin.

## Phase 5: Implementation

When the user says "implement" or "go":

1. Execute every task in the plan sequentially
2. After completing each task, update `.claude/plan.md` — change `- [ ]` to `- [x]`
3. Do not stop until all tasks are completed
4. Run the project's type checker / linter after each phase to catch issues early
5. Do not add unnecessary comments, docstrings, or type workarounds (`any`, `unknown`)

**Code quality rules during implementation:**
- No unnecessary comments or jsdocs
- No `any` or `unknown` types (TypeScript projects)
- Run typecheck/lint continuously
- Follow existing codebase patterns exactly

## Phase 6: Feedback

During implementation, the user may provide terse corrections. These are sufficient because full context exists in the plan and session:

- "You missed the dedup function" → implement what was missed
- "Move this to the admin app" → relocate as directed
- "Wider" / "2px gap" / "still cropped" → adjust and re-check
- "Make it look like the users table" → read that reference, match it exactly

**On reverts:** If the user says "I reverted everything" — re-read the current file state, narrow scope to exactly what they specify, and re-implement cleanly.

## Prompt Reference

See [references/prompts.md](references/prompts.md) for ready-to-use prompts for each phase that the user can copy and adapt.
