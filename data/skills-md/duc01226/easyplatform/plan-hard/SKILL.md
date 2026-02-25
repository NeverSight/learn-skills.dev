---
name: plan-hard
description: '[Planning] ⚡⚡⚡ Research, analyze, and create an implementation plan. Use --parallel for parallel-executable phases'
argument-hint: [task]
---

Think harder.
Activate `plan` skill.

## Summary

**Goal:** Research, analyze codebase, and create a detailed phased implementation plan with parallel researcher subagents.

| Step | Action            | Key Notes                                                                |
| ---- | ----------------- | ------------------------------------------------------------------------ |
| 1    | Check active plan | Reuse existing or create new using naming convention                     |
| 2    | Research          | Max 2 parallel researcher agents, 5 tool calls each, reports <=150 lines |
| 3    | Analyze codebase  | Read codebase-summary.md, code-standards.md, system-architecture.md      |
| 4    | Create plan       | Planner subagent generates plan.md + phase-XX files                      |
| 5    | User review       | Ask user to approve; offer optional validation interview                 |

**Key Principles:**

- Do NOT use `EnterPlanMode` tool -- it blocks Write/Edit/Task tools
- Do NOT start implementing -- plan only, wait for user approval
- Use `--parallel` flag for phases with no file overlap that can run concurrently

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

1. If creating new: Create directory using `Plan dir:` from `## Naming` section, then run `node .claude/scripts/set-active-plan.cjs {plan-dir}`
   If reusing: Use the active plan path from Plan Context.
   Make sure you pass the directory path to every subagent during the process.
2. Follow strictly to the "Plan Creation & Organization" rules of `plan` skill.
3. Use multiple `researcher` agents (max 2 agents) in parallel to research for this task:
   Each agent research for a different aspect of the task and are allowed to perform max 5 tool calls.
4. Analyze the codebase by reading `codebase-summary.md`, `code-standards.md`, `system-architecture.md` and `project-overview-pdr.md` file.
   **ONLY PERFORM THIS FOLLOWING STEP IF `codebase-summary.md` is not available or older than 3 days**: Use `/scout <instructions>` slash command to search the codebase for files needed to complete the task.
5. Main agent gathers all research and scout report filepaths, and pass them to `planner` subagent with the prompt to create an implementation plan of this task.
6. Main agent receives the implementation plan from `planner` subagent, and ask user to review the plan

## Post-Plan Validation (Optional)

After plan creation, offer validation interview to confirm decisions before implementation.

**Check `## Plan Context` → `Validation: mode=X, questions=MIN-MAX`:**

| Mode     | Behavior                                                                        |
| -------- | ------------------------------------------------------------------------------- |
| `prompt` | Ask user: "Validate this plan with a brief interview?" → Yes (Recommended) / No |
| `auto`   | Automatically execute `/plan-validate {plan-path}`                              |
| `off`    | Skip validation step entirely                                                   |

**If mode is `prompt`:** Use `AskUserQuestion` tool with options above.
**If user chooses validation or mode is `auto`:** Execute `/plan-validate {plan-path}` SlashCommand.

## Output Requirements

**Plan Directory Structure** (use `Plan dir:` from `## Naming` section)

```
{plan-dir}/
├── research/
│   ├── researcher-XX-report.md
│   └── ...
├── reports/
│   ├── XX-report.md
│   └── ...
├── scout/
│   ├── scout-XX-report.md
│   └── ...
├── plan.md
├── phase-XX-phase-name-here.md
└── ...
```

**Research Output Requirements**

- Ensure every research markdown report remains concise (≤150 lines) while covering all requested topics and citations.

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
- For each phase, create `{plan-dir}/phase-XX-phase-name-here.md` containing the following sections in order: Context links (reference parent plan, dependencies, docs), Overview (date, description, priority, implementation status, review status), Key Insights, Requirements, Architecture, **Trade-offs & Alternatives** (What alternative approaches were considered? What are the failure modes? Under what changed requirements would you choose differently?), Related code files, Implementation Steps, Todo list, Success Criteria, Risk Assessment, Security Considerations, Next steps.

## Parallel Mode (--parallel flag)

When `$ARGUMENTS` contains `--parallel`, apply these additional requirements:

**CRITICAL:** The planner subagent must create phases that:

1. **Can be executed independently** - Each phase self-contained with no runtime dependencies
2. **Have clear boundaries** - No file overlap between phases (each file modified in ONE phase only)
3. **Separate concerns logically** - Group by architectural layer, feature domain, or technology stack
4. **Include dependency matrix** - Document which phases run sequentially vs in parallel

**Parallelization Strategy:**

- Group frontend/backend/database into separate phases
- Separate infrastructure setup from application logic
- Isolate different feature domains
- Create independent test phases per module

**Additional plan.md requirements when --parallel:**

- Dependency graph showing which phases can run in parallel
- Execution strategy (e.g., "Phases 1-3 parallel, then Phase 4")
- File ownership matrix (which phase owns which files)

**Additional phase file requirements when --parallel:**

- Parallelization Info section (which phases can run concurrently)
- File Ownership section (explicit list of files this phase owns/modifies)
- Conflict Prevention section (how this phase avoids conflicts with parallel phases)

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
