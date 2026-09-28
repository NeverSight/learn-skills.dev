---
name: writing-plan
description: Use when you have a spec or requirements for a multi-step task, before touching code. Supports either Markdown plans or review-oriented HTML plan artifacts.
---

## Overview

Write an execution-ready handoff for a skilled engineer unfamiliar with the repository. Ground tasks in repository evidence, dependencies, verification, and observable acceptance criteria. Preserve user requirements, overrides, and approved decisions; leave routine implementation choices to the implementer.

## Output Mode

Honor an explicitly requested format or filename. Otherwise, default to Markdown. Produce both formats only when explicitly requested.

- For Markdown, write `plan-${implementation-task}.md` using a kebab-case task slug.
- For HTML, write `plan-${implementation-task}.html` using the same slug. Before writing, read [HTML Plan Artifact Guidance](./html-plan-artifact-guidance.md), [Plan Artifact Skeleton](./example/plan-artifact-skeleton.html), and [Plan Artifact Panel Reference](./example/plan-artifact-panel-reference.html), then use their contract and scaffold.

## Required Plan Contract

Expose these sections in order:

1. Feature name
2. Goal
3. Architecture
4. Tech stack
5. File structure
6. Dependency-aware tasks
7. Verification
8. Progress tracking
9. Out of scope

Preserve the same implementation detail in Markdown and HTML.

Markdown plans must start with:

```markdown
# [Feature Name] Implementation Plan

**Goal:** [One sentence describing what this builds]

**Architecture:** [Two or three sentences describing the approach]

**Tech Stack:** [Key technologies and libraries]

---
```

## Scope And File Structure

Choose plan boundaries based on the requested handoff scope, shared acceptance criteria, and integration dependencies. Independently deliverable and testable subsystems may warrant separate plans; otherwise, keep them in one dependency-aware plan.

List known affected files and their responsibilities, verifying existing paths against the repository and labeling proposed new files. Follow the repository's existing organization, introducing a split only when the planned change requires a distinct boundary. Use this inventory to define task ownership and dependencies.

Distinguish confirmed constraints, proposed choices, and unresolved decisions. Record a decision as locked only when supported by an explicit requirement, established constraint, or approved decision. When file boundaries depend on pending design work, identify the affected boundary and prerequisite instead of presenting speculative paths as final.

## Task Structure

Each task must produce one reviewable outcome with affected files or boundaries, dependencies, verification, and acceptance criteria. Use exact paths where established. Identify parallel tasks only when their dependencies and file ownership permit concurrent work; keep work sharing the same boundary in one coherent slice.

Require `@program-design` for a task that introduces or substantially reshapes modules, interfaces, types, file layout, dependencies, or control flow. Omit it for small fixes, local implementation changes, and mechanical edits.

A plan is ready when a skilled implementer can proceed without inventing material requirements or making unapproved architectural decisions. An investigation or design step is actionable when its question, expected evidence or approved output, and dependent work are clear. Resolve choices that determine scope, dependencies, or acceptance before declaring the affected implementation ready; assigning an unresolved choice to implementation does not settle it.

Assess every task for a Human Review Focus. Add one only when correctness depends materially on product, domain, architectural, security, privacy, or UX judgment that automated checks and agent reviews cannot establish. The category alone is insufficient: routine UI styling and other mechanical changes do not qualify by default.

A Human Review Focus is advisory. It never becomes a dependency, acceptance criterion, verification result, task state, review gate, or completion gate. Name the narrowest stable file, symbol, screen, workflow, policy, or boundary; state the judgment the human should apply; and explain why agent or automated validation is insufficient. Reject broad directions such as "review the business logic" or "review the UI." Use at most three focus items in one task; split an overloaded task or prioritize its highest-risk areas instead of adding more.

A focus identifies where human inspection is valuable. Record unresolved material decisions as prerequisites and explicitly required human checks in verification; neither can be replaced by an advisory focus.

Plan the smallest meaningful verification for each outcome, preserving mandatory repository checks. Ground commands in repository tooling and specify expected results or manual steps where appropriate. Distinguish task checks from final integration checks. Require new tests or repeated broad checks only when the change, failures, or unresolved concerns justify them.

Use this Markdown task contract:

````markdown
#### Task `task-id`

**Title**: [Action-oriented task title].

**Description**: [One short sentence explaining what this task accomplishes and why it exists.]

- Create or modify `exact/path/to/file.ts` for [specific responsibility].
- Reuse `exact/path/to/reference.ts` for [existing pattern, type, or behavior].
- Preserve [named constraint, public API, or runtime behavior].
- Run `exact verification command`; expect [observable result].

**Required skills**: `@skill-name` when the task depends on one; otherwise omit this field.

**Depends on**: `upstream-task-id` or Nothing.

> **Human Review Focus**
>
> - Review [narrow implementation surface]; confirm [judgment that requires a human] because [limit of agent or automated validation].

**Produces**: `exact/path/to/file.ts`; updated `exact/path/to/other-file.ts`.

**Acceptance**: [Observable outcome that proves the task is done.]
````

Adapt the instruction bullets and `Produces` to the task: investigation or design work should name its evidence or design artifact and affected boundary rather than invent final implementation paths. Omit the Human Review Focus blockquote when no focus applies.

For HTML plans, render the same task fields visibly inside task cards, tables, or sections. When a task has a Human Review Focus, add a `Human Review Focus` pill after its dependency pill and a matching content box beside `Produces` and `Acceptance`. Omit both when no focus applies.

## Progress Tracking

Place `Progress Tracking` between `Verification` and `Out of Scope`, in the plan file:

```markdown
## Progress Tracking

- **Current status:** Not started
- **Started on:** Not started
- **Completed on:** Not completed
- **Last executed tasks:** None
- **Current blocker or next focus:** [First runnable task ID or Waiting to start]
```

Use `Not started`, `In progress`, `Blocked`, or `Completed` for `Current status`. Record executed task IDs newest first. Add `Unplanned necessary work` only when execution requires work outside the original task list.

## Plan Review Loop

After writing the plan, dispatch one reviewer using [Plan Document Reviewer Prompt](./plan-document-reviewer-prompt.md). Supply the plan path, repository location, requirements or spec paths, user overrides, and approved decisions, including relevant context established in conversation. A separate spec file is not required when the requirements are supplied directly. Resolve substantiated issues, then review the complete plan again. Reviewer approval completes the plan handoff; required design approvals and unresolved prerequisites still govern when affected implementation may begin.

After three unsuccessful review cycles, present each unresolved objection with its disposition or rebuttal and ask the user to decide.
