---
name: kata-linear
description: "Linear ticket lifecycle for any project. Use when starting work on a Linear issue, ending work on an issue, or asking what to work on next. Triggers: start KAT-N, pick up, implement, finish, complete, done with, close, what's next, next ticket, next issue. Handles blocker validation, status transitions, context loading, branch creation, evidence gating, and chain promotion."
---

# Linear Ticket Lifecycle

This skill wraps the general `/linear` skill with structured start/next/end workflows.
Always invoke `/linear` for the actual MCP calls.

## Determining the Mode

Parse the user's request to determine which workflow to run:

| User says                                                           | Mode      |
| ------------------------------------------------------------------- | --------- |
| "start KAT-N", "pick up KAT-N", "implement KAT-N", "work on KAT-N"  | **Start** |
| "finish KAT-N", "complete KAT-N", "done with KAT-N", "close KAT-N"  | **End**   |
| "what's next", "what should I work on", "next ticket", "next issue" | **Next**  |

If ambiguous, ask.

## Identifying the Project

1. Check the current working directory's CLAUDE.md for a Linear project reference.
2. If not found, call `list_projects` and ask the user which project to use.
3. Cache the project name for the remainder of the session.

---

## Mode: Next

Find the next actionable issue.

1. Query `list_issues` for the project with state `Todo`.
2. If results exist, present them. The first `Todo` issue is the recommended next pick.
3. If no `Todo` issues, resolve from blocking relations:
   a. Query `list_issues` for the project with state `Backlog`.
   b. For each Backlog issue, call `get_issue` with `includeRelations: true`.
   c. Find issues whose `blockedBy` entries are all `Done` (or have no blockers).
   d. Present unblocked issues as candidates.
4. If the project has Linear documents (execution model, workflow contract), fetch them
   with `list_documents` and `get_document` to understand pillar/phase ordering.

---

## Mode: Start

### Step 1 — Validate the issue

1. Call `get_issue` for the requested issue with `includeRelations: true`.
2. Check every entry in `blockedBy`. For each blocker, confirm its status is `Done`.
3. If any blocker is not `Done`, stop and report which blockers remain open.

### Step 2 — Move to In Progress

1. Call `update_issue` to set state to `In Progress`.

### Step 3 — Load context

1. Read the issue description for references to specs, mocks, docs, or design files.
2. Read Linear documents (execution model, workflow contract) for project-specific guidance.
3. Read relevant spec files, mock images, or design references found in steps 1 and 2.
4. Check existing source code in the areas the issue will touch.

### Step 4 — Create feature branch

1. Use the `gitBranchName` field from the issue response as the branch name.
2. Create the branch from the main branch.

### Step 5 — Summarize

Present to the user:

- Issue title and acceptance criteria
- Blocker status (all clear)
- Context loaded (specs, mocks, relevant code)
- Branch name created
- Any project-specific workflow reminders from CLAUDE.md (e.g., TDD mandate)

---

## Mode: End

### Step 1 — Gather evidence

Ask the user to confirm or provide:

- PR link or branch with changes
- Test results (unit and/or E2E)
- Screenshots or spec-state references demonstrating acceptance criteria

If a PR already exists on the current branch, detect it with `gh pr view`.

### Step 2 — Validate completion gate

Check if the project's CLAUDE.md or Linear workflow contract defines a hard gate.
Common gates:

- Referenced spec states/interactions are verified
- Evidence links are attached (tests, screenshots, or traceable PR notes)
- Gap analysis items are either closed or split into follow-up issues

If evidence is insufficient, list what's missing and stop.

### Step 3 — Attach evidence to the issue

1. Call `create_comment` on the issue with a structured evidence summary:
   ```
   ## Completion Evidence
   - PR: [link]
   - Tests: [pass/fail summary]
   - Acceptance coverage: [which criteria verified]
   - Screenshots: [if applicable]
   ```

### Step 4 — Move to Done

1. Call `update_issue` to set state to `Done`.

### Step 5 — Promote next in chain

1. Call `get_issue` with `includeRelations: true` on the completed issue.
2. For each issue in the `blocks` list:
   a. Call `get_issue` with `includeRelations: true` on that downstream issue.
   b. Check if ALL of its `blockedBy` entries are now `Done`.
   c. If yes, call `update_issue` to move it to `Todo`.
   d. Report which issue was promoted.

### Step 6 — Summarize

Present:

- Issue marked Done with evidence link
- Which downstream issue(s) were promoted to Todo
- Suggested next action

## Important Reminders

- Always pass `includeRelations: true` when calling `get_issue` to see blocking dependencies.
- Always reference the attached media as the source of truth for design specs and mocks.
