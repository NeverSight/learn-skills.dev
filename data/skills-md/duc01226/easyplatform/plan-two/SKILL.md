---
name: plan-two
description: '[Planning] ⚡⚡⚡⚡ Research & create an implementation plan with 2 approaches'
argument-hint: [task]
---

Think harder.
Activate `plan` skill.

> **CRITICAL:** Do NOT use `EnterPlanMode` tool — it blocks Write/Edit/Task tools needed for plan creation. Follow the workflow below.
> **Planning is collaborative:** Validate plan, ask user to confirm, surface decision questions with recommendations.

## Your mission

Use the `planner` subagent to create 2 detailed implementation plans for this following task:
<task>
$ARGUMENTS
</task>

## Workflow

1. First: Create a directory using naming pattern from `## Naming` section in injected context.
   Make sure you pass the directory path to every subagent during the process.
2. Follow strictly to the "Plan Creation & Organization" rules of `plan` skill.
3. Use multiple `researcher` agents in parallel to research for this task, each agent research for a different aspect of the task and perform max 5 researches (max 5 tool calls).
4. Use `scout` agent to search the codebase for files needed to complete the task.
5. Main agent gathers all research and scout report filepaths, and pass them to `planner` subagent with the detailed instructions prompt to create an implementation plan of this task.
   **Output:** Provide at least 2 implementation approaches with clear trade-offs, and explain the pros and cons of each approach, and provide a recommended approach.
6. Main agent receives the implementation plan from `planner` subagent, and ask user to review the plan

## Plan File Specification

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
