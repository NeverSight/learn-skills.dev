---
name: plan-fast
description: '[Planning] ⚡⚡ No research. Only analyze and create an implementation plan'
argument-hint: [task]
---

Think.
Activate `plan` skill.

> **CRITICAL:** Do NOT use `EnterPlanMode` tool — it blocks Write/Edit/Task tools needed for plan creation. Follow the workflow below.
> **Planning is collaborative:** Validate plan, ask user to confirm, surface decision questions with recommendations.

## Your mission

<task>
$ARGUMENTS
</task>

## Pre-Creation Check (Active vs Suggested Plan)

Check the `## Plan Context` section in the injected context:

- If "Plan:" shows a path → Active plan exists. Ask user: "Continue with this? [Y/n]"
- If "Suggested:" shows a path → Branch-matched hint only. Ask if they want to activate or create new.
- If "Plan: none" → Create new plan using naming from `## Naming` section.

## Workflow

Use `planner` subagent to:

1. If creating new: Create directory using `Plan dir:` from `## Naming` section, then run `node .claude/scripts/set-active-plan.cjs {plan-dir}`
   If reusing: Use the active plan path from Plan Context.
   Make sure you pass the directory path to every subagent during the process.
2. Follow strictly to the "Plan Creation & Organization" rules of `plan` skill.
3. Analyze the codebase by reading `codebase-summary.md`, `code-standards.md`, `system-architecture.md` and `project-overview-pdr.md` file.
4. Gathers all information and create an implementation plan of this task.
5. Ask user to review the plan.

## Output Requirements

**Plan Directory Structure** (use `Plan dir:` from `## Naming` section)

```
{plan-dir}/
├── reports/
│   ├── XX-report.md
│   └── ...
├── plan.md
├── phase-XX-phase-name-here.md
└── ...
```

**Plan File Specification**

- Every `plan.md` MUST start with YAML frontmatter:

    ```yaml
    ---
    title: '{Brief title}'
    description: '{One sentence for card preview}'
    status: pending
    priority: P2
    effort: { sum of phases, e.g., 4h }
    branch: { current git branch }
    tags: [relevant, tags]
    created: { YYYY-MM-DD }
    ---
    ```

- Save the overview access point at `{plan-dir}/plan.md`. Keep it generic, under 80 lines, and list each implementation phase with status and progress plus links to phase files.
- For each phase, create `{plan-dir}/phase-XX-phase-name-here.md` containing the following sections in order: Context links (reference parent plan, dependencies, docs), Overview (date, description, priority, implementation status, review status), Key Insights, Requirements, Architecture, **Trade-offs & Alternatives** (Alternatives considered: [list]. Failure modes: [list]), Related code files, Implementation Steps, Todo list, Success Criteria, Risk Assessment, Security Considerations, Next steps.

## MANDATORY: Plan Collaboration Protocol (READ THIS)

- **Do NOT use `EnterPlanMode` tool** — it blocks Write/Edit/Task tools needed to create plan files and launch subagents
- **Do NOT start implementing** — plan only, wait for user approval
- **ALWAYS validate:** After plan creation, execute `/plan-review` to validate the plan
- **ALWAYS confirm:** Ask user to review and approve the plan using `AskUserQuestion` with a recommendation
- **ALWAYS surface decisions:** Use `AskUserQuestion` with recommended options for key architectural/design decisions
- **Planning = Collaboration:** The plan is shaped by user input — never treat it as a unilateral output
- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end
- Sacrifice grammar for concision. List unresolved questions at the end
