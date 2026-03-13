---
name: planner-workflow
description: "Phase-level planning workflow for planner agents. Handles reading templates, exploring codebase references, creating plan.md and phase files, self-validation, and checkpoint reporting to the orchestrator. Invoke this skill as your first action — not user-invocable."
user-invocable: false
metadata:
  version: 1.0.0
---

# Planner Phase Workflow

You have been assigned a **planning task** to create a full plan with phases for a feature. Your spawn prompt contains the feature description, requirements, and plan folder path. This skill teaches you how to handle the entire planning process end-to-end.

## Why This Workflow Exists

The user experienced planners that guessed at patterns, skipped template sections, and produced phases with generic code blocks. Each step below prevents a specific failure:

| Step | Prevents |
|------|----------|
| Read templates completely | Missing required sections, rework during review |
| Create task list | Lost progress after context compact, skipped phases |
| Read codebase references | Code blocks that don't match real project patterns |
| Checkpoint 1 (plan summary) | Building 20 phases on wrong assumptions — hours wasted |
| Self-validate each phase | Placeholder content and missing TDD discovered late in review |

## Step 1: Read Templates

The user created these templates specifically so phases don't miss required sections. Skipping template reading causes incomplete phases that require rework during implementation.

Read both templates completely:
- `$CLAUDE_PROJECT_DIR/.claude/skills/create-plan/references/PLAN-TEMPLATE.md`
- `$CLAUDE_PROJECT_DIR/.claude/skills/create-plan/references/PHASE-TEMPLATE.md`

Every section in these templates is required. Extract the section lists — you'll use them as checklists when writing plan.md and phase files.

## Step 2: Create Folder Structure

**Folder naming pattern:** `plans/{YYMMDD}-{feature-name}/`

Examples:
- `plans/260220-voice-assistant/`
- `plans/260220-notification-system/`

**Create these items:**
1. Main folder: `plans/{YYMMDD}-{feature-name}/`
2. Planning reviews folder: `plans/{YYMMDD}-{feature-name}/reviews/planning/`
3. Code reviews folder: `plans/{YYMMDD}-{feature-name}/reviews/code/`

## Step 3: Create Task List

Tasks survive context compacts — skipping this check causes duplicate tasks and lost progress.

Before creating tasks, run `TaskList` to check if tasks already exist from a previous session or before a compact. If tasks exist:
1. Read existing tasks with `TaskGet` for each task ID
2. Find the first task with status `pending` or `in_progress`
3. Resume from that task — do NOT recreate the task list

If no tasks exist, create them now. **Prefix all task subjects with `[Plan]`** to distinguish from the orchestrator's tasks in the shared team task list. Always set `owner` to your agent name and include structured `metadata`:

```
TaskCreate({
  subject: "[Plan] Create plan.md scaffold",
  description: "Write plan.md with all sections from template except Phase Table rows. Include: frontmatter, executive summary, phasing strategy, architectural north star, security requirements, implementation standards, success metrics, decision log, resources.",
  activeForm: "Creating plan.md scaffold",
  metadata: {
    created_by: "{your-agent-name}",
    agent_type: "planner",
    role: "plan",
    attempt: 1,
    parent_task_id: "{orchestrator-task-id-from-spawn-prompt}"
  }
})
// Then: TaskUpdate({ taskId: "{id}", owner: "{your-agent-name}" })
```

**Standard planner tasks:**

```
[Plan] Create plan.md scaffold (all sections except Phase Table content)
[Plan] Read codebase references
[Plan] Checkpoint 1 — report plan summary to orchestrator
[Plan] Create Phase 01 - [Title]
[Plan] Create Phase 02 - [Title]
[...continue for all phases...]
[Plan] Checkpoint 2 — report completion to orchestrator
```

Mark each task `in_progress` before starting and `completed` when done via `TaskUpdate`.

## Step 4: Read Codebase References

Code blocks written from memory often don't match the real codebase — this is the #1 source of phase quality issues. Reading actual files before writing phases ensures patterns are accurate.

Identify which file types the feature will need and read one reference for each:

| Feature Needs | Reference to Read |
|---------------|-------------------|
| Server actions | Glob `app/home/[account]/**/*server-actions*.ts` → read one |
| Service layer | Glob `app/home/[account]/**/*service*.ts` → read one |
| Zod schemas | Glob `app/home/[account]/**/*.schema.ts` → read one |
| SQL migrations / RLS | Glob `supabase/migrations/*.sql` → read a recent one |
| React components | Glob `app/home/[account]/**/_components/*.tsx` → read one |
| Page files | Glob `app/home/[account]/**/page.tsx` → read one |
| Tests | Glob `__tests__/**/*.test.ts` → read one |

**Key patterns to extract and use in phase code blocks:**
- Server action pattern: `'use server'` + Zod parse + `getSession()` auth check
- Account resolution: slug → ID via `client.from('accounts').select('id').eq('slug', data.accountSlug).single()`
- Permission check: your RLS helper function (e.g., `client.rpc('check_account_access', { ... })`)
- Supabase client: `createClient()` from `@/lib/supabase/server`
- Service factory: `createXxxService(client: SupabaseClient<Database>)` wrapping a private class
- Import paths: `import 'server-only'`, `@/` path alias for project root
- File naming: `_lib/schema/` (singular), `server-actions.ts`, exports ending in `Action`
- TypeScript: consider enums or union types for constants, `interface` preferred for objects
- After mutations: `revalidatePath('/home/[account]/...')`

### Pre-Implementation Analysis

Before scoping phases, run through the checklist in `.claude/rules/pre-implementation-analysis.md`. Its 7 dimensions — existing patterns, blast radius, security surface, performance, maintainability, multi-tenant safety, and upstream compatibility — directly inform phase boundaries and what each phase's `Prerequisites & Clarifications` section should cover. Findings from this analysis (e.g. "touches auth flow", "new table needs RLS") should surface in the relevant phase files, not be left implicit.

### Frontend Guidelines (If Applicable)

If the feature involves React components, Next.js pages, or UI work, invoke this skill BEFORE designing phases:

```
/vercel-react-best-practices
```

This loads 57 performance rules across 8 categories. Reference these when designing data fetching patterns, component architecture, and bundle optimisation requirements.

Keep these patterns in mind for every code block you write in phase files. The review step will flag any code blocks that deviate from these codebase patterns.

## Step 5: Create plan.md

Write `plans/{folder}/plan.md` with ALL sections from the template:

1. YAML Frontmatter (title, status, priority, tags, dates)
2. Executive Summary (Mission, Big Shift, Deliverables)
3. Phasing Strategy (Phase Constraints, Phase File Naming)
4. **Phase Table** — Header row only, no content rows yet
5. Architectural North Star (patterns with Core Principle + Enforcement)
6. Component Library Priority (check your UI library before building custom)
7. Security Requirements (RLS, Input Validation, Authorization, Error Handling)
8. Implementation Standards (Test Strategy, Documentation Standard)
9. Success Metrics & Quality Gates
10. Global Decision Log (ADRs)
11. Resources & References

Complete ALL sections except Phase Table rows. Missing sections are caught during review but cost extra review cycles to fix.

### Phase Constraints

Phases that exceed one context window cause Claude to lose earlier context mid-implementation, producing incomplete or inconsistent code. Each phase should be atomic enough for implementation in **1 context window** (~15KB document, ~2-3 hour focused session).

**30 small phases > 5 large phases**

| Wrong Approach | Right Approach |
|----------------|----------------|
| "Phase 01: Database + API + UI" | Split into 3 phases |
| "Phase 02: Full Feature Implementation" | Break into atomic steps |
| "Phase 03: Testing and Polish" | TDD is Step 0 in EACH phase |

**TDD Note:** Both backend and frontend code require full unit tests:
- **Backend** (services, schemas, APIs): Unit tests in `__tests__/{feature}/`
- **Frontend** (React/TSX): Component tests using happy-dom (default) and @testing-library/react
- The default happy-dom environment works for component tests. Only add `// @vitest-environment happy-dom` if explicitly overriding another environment.
- Use `it.todo('description')` for TDD stubs
- Use `vi.hoisted()` for mock variables needed before module evaluation
- For Supabase client mocks, add `.then()` method for thenable/awaitable pattern
- Path aliases in tests: use your project's configured path alias (e.g., `@/` or `~/`)

**The test:** Can Claude implement this phase without running out of context? If unsure, split it.

## Step 6: Checkpoint 1 — Report Plan Summary

After creating plan.md, report to the orchestrator for user review. This is the key benefit of the team pattern — the user can course-correct before you spend time writing 15 phase files.

```
SendMessage({
  type: "message",
  recipient: "team-lead",
  content: `## Plan Summary — Ready for Review

**Feature**: {feature name}
**Plan folder**: plans/{YYMMDD}-{feature-name}/

### Executive Summary
{1-2 sentence mission}

### Proposed Phase Breakdown
| # | Title | Group | Skill | Dependencies |
|---|-------|-------|-------|-------------|
| 01 | {title} | {group} | {skill} | None |
| 02 | {title} | {group} | {skill} | Phase 01 |
...

### Group Summary
| Group | Phases | Description |
|-------|--------|-------------|
| {name} | P01-P03 | {what this group delivers} |

### Architecture Decisions
- {key decision 1}
- {key decision 2}

### Security Requirements
- {key requirement}

Awaiting approval or feedback before creating phase files.`,
  summary: "Plan summary ready for review"
})
```

**Then WAIT.** Do not proceed to Step 7 until the orchestrator responds with approval or feedback.

- **If approved:** Continue to Step 7.
- **If changes requested:** Revise plan.md and the phase breakdown, then re-send the summary. Repeat until approved.

## Step 7: Create Phases (Iterative)

For EACH phase, in order:

### 7a: Add Row to Phase Table

Edit `plan.md` to add the phase row:

```markdown
| **01** | [Title](./phase-01-slug.md) | [group-name] | [Focus] | Pending |
```

### 7b: Create Phase File

Write the complete phase file following PHASE-TEMPLATE.md exactly.

**File:** `plans/{folder}/phase-{NN}-{slug}.md`

**Include `skill` in Frontmatter** — without it, the implementer won't know which skill to invoke and will use generic patterns instead of project-specific ones.

| Phase Type | Skill Value |
|------------|-------------|
| Database schema, migrations, RLS | `postgres-expert` |
| Server actions, services, API | `server-action-builder` |
| React forms with validation | `react-form-builder` |
| E2E tests | `playwright-e2e` |
| React components/pages | `vercel-react-best-practices` |
| UI/UX focused work | `web-design-guidelines` |

**Example frontmatter:**
```yaml
---
title: "Phase 01 - Database Schema"
skill: postgres-expert
status: pending
group: "auth-system"
dependencies: []
---
```

**Group assignment rules:**
- Connected phases building the same feature/component MUST share a `group:` name
- Group names should be descriptive: `auth-system`, `dashboard-ui`, `data-pipeline`
- Single-phase groups are valid for standalone work
- Groups define audit boundaries — after all phases in a group complete during implementation, an auditor reviews them together
- Order groups so dependencies flow top-to-bottom (group A before group B if B depends on A)

For phases spanning multiple concerns, list the primary skill or use comma-separated values:
```yaml
skill: react-form-builder, vercel-react-best-practices
```

**Required sections** (from template):
1. YAML Frontmatter (title, description, status, dependencies, tags, dates, **skill**)
2. Overview (brief description, single-sentence Goal)
3. Context & Workflow (How the Project Uses This, User Workflow, Problem Being Solved)
4. Prerequisites & Clarifications (Questions for User with Context/Assumptions/Impact)
5. Requirements (Functional + Technical)
6. Decision Log (phase-specific ADRs)
7. Implementation Steps — **Step 0: TDD is first**
8. Verifiable Acceptance Criteria (Critical Path, Quality Gates, Integration)
9. Quality Assurance (Manual Testing, Automated Testing, Performance Testing, Review Checklist)
10. Dependencies (Upstream, Downstream, External)
11. Completion Gate (Sign-off checklist)

Code blocks in phases should match codebase patterns from Step 4 — not memory, not generic examples. Generic code blocks cause the implementer to write code that doesn't follow project conventions, creating rework. If you don't remember the exact pattern, re-read the reference file from Step 4 before writing the code block.

### 7c: Validate Phase Quality

After creating each phase file, run these validators to catch issues immediately (before review agents get involved):

```bash
# Check for skeleton/placeholder content
echo '{"cwd":"."}' | uv run $CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_no_placeholders.py \
  --directory plans/{folder} --extension .md

# Check TDD tasks appear before implementation tasks
echo '{"cwd":"."}' | uv run $CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_tdd_tasks.py \
  --directory plans/{folder} --extension .md

# Confirm the phase file was actually created
echo '{"cwd":"."}' | uv run $CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_new_file.py \
  --directory plans/{folder} --extension .md
```

If any validator exits non-zero, fix the issue before moving to the next phase. Placeholder content and missing TDD steps are the two most common causes of rework during implementation.

### 7d: Update Task Status

Mark the phase task as completed, move to next phase.

### 7e: Repeat

Continue until all phases are created.

## Step 8: Checkpoint 2 — Report Completion

After all phases are created and validated, send a full summary to the orchestrator:

```
SendMessage({
  type: "message",
  recipient: "team-lead",
  content: `## Plan Complete — All Phases Created

**Plan folder**: plans/{YYMMDD}-{feature-name}/
**Phases**: {count} phases created

### Phase Breakdown
| # | Title | Group | Skill | Dependencies | Self-Validation |
|---|-------|-------|-------|-------------|-----------------|
| 01 | {title} | {group} | {skill} | None | Passed |
| 02 | {title} | {group} | {skill} | Phase 01 | Passed |
...

### Dependency Graph
{describe the dependency flow — which phases unlock which}

### Self-Validation Results
- Placeholder check: {pass/fail count}
- TDD ordering: {pass/fail count}
- File creation: {pass/fail count}

Ready for review via /review-plan.`,
  summary: "All phases created — ready for review"
})
```

Then go idle. The orchestrator will handle spawning review validators and routing feedback.

---

## Resuming After Context Compact

If your context was compacted mid-planning:

1. `TaskList` → scan for tasks where you are the `owner` (your agent name)
2. Find your `in_progress` task, or if none, your first `pending` task
3. `TaskGet` on that task → read the description AND `metadata`
4. Metadata tells you: which orchestrator task you report to (`parent_task_id`)
5. Continue from that task — don't restart the planning process
6. The task list and metadata are your source of truth, not your memory

**Pattern for every work cycle:**
```
TaskList → filter by owner → find in_progress or first pending → TaskGet → continue work → TaskUpdate (completed) → next task
```

Tasks are the planner's source of truth for progress — not memory, not plan.md alone.

## Troubleshooting

### Context Window Overflow

**Symptom:** Planner loses track of phases mid-creation, produces incomplete or inconsistent output.

**Cause:** Too many phases being created without task tracking, or codebase references consuming too much context.

**Fix:** Follow Task List pattern in Step 3 — mark tasks complete as you go. For codebase references, read only what you need (one file per type).

### Missing Template Sections

**Symptom:** Review agents flag missing sections in plan.md or phase files.

**Cause:** Template not read before writing, or sections skipped during creation.

**Fix:** Re-read the template (`$CLAUDE_PROJECT_DIR/.claude/skills/create-plan/references/PLAN-TEMPLATE.md` or `PHASE-TEMPLATE.md`) and add the missing sections. Each section exists because omitting it caused implementation problems.

### Code Blocks Don't Match Codebase

**Symptom:** Review agents flag code blocks as not matching project patterns.

**Cause:** Code blocks written from memory instead of from codebase references.

**Fix:** Re-read the reference file from Step 4 for the relevant file type. Copy the actual pattern — function signatures, imports, naming conventions — into the code block.

### Orchestrator Not Responding After Checkpoint

**Symptom:** Sent checkpoint message but no response.

**Cause:** The orchestrator relays your checkpoint to the user, who may need time to review. This is expected.

**Fix:** Wait. Do not proceed past a checkpoint without orchestrator approval. The whole point of checkpoints is user course-correction.
