---
name: task
description: Manage tasks using the fine CLI. Use this skill whenever the user asks to create, view, update, or work with tasks, project requirements, feature specs, or work tracking through markdown files. Also use it when the user mentions "fine" in the context of project management, or asks about task status, step progress, or wants to break work into tracked steps.
---

# Task Management with Fine

Fine is an agent-first project management CLI. Tasks are markdown files in a
`tasks/` directory, managed via CLI commands and direct file editing.

## Key principle: tasks are self-contained

Each task must have a **well-defined deliverable** — something concrete that can
be verified when the task is done. Executors can read other tasks, but they have
**no context from previous task executions** (no memory of decisions made,
approaches taken, or intermediate findings from other sessions). This means:

- **Every step must be achievable from the repository and the task description
  alone.** Don't write steps that depend on runtime state, environment-specific
  setup, or decisions made during a previous task's execution.
- **Tasks need well-defined deliverables, not open-ended research.** "Identify
  all broken links" is not a good task — it produces no deliverable. "Fix all
  broken links in the docs" is good — the deliverable is updated files. If
  research is needed, fold it into a task that acts on the findings.
- **Verification steps are fine if they have clear pass/fail criteria.** For
  example, "Verify all links return 200" is a good step. If you can't define
  concrete verification criteria for a step, leave it out — but note the
  omission in your summary so the user can adjust.
- **Include context the executor will need.** The executor can see other task
  files, but doesn't know what happened during their execution. If a task
  depends on choices made in another task, reference the expected output (e.g.,
  "the auth module added in task 003") rather than assuming the executor knows
  the approach that was taken.

## Task file format

Each task is a markdown file named `NNN-slug.md` (e.g.,
`001-user-authentication.md`). The ID and slug come from the filename, not the
content.

```markdown
# Title

Description paragraph(s).

## Steps

- [ ] Incomplete step
- [x] Completed step
```

- **Title**: The first H1. Required.
- **Description**: Everything between the title and `## Steps`. Can be multiple
  paragraphs.
- **Steps**: Checklist items under `## Steps`. Omit the section entirely if
  there are no steps.

## CLI commands

Run commands with `npx @jagersoftware/fine <command>`.

### Create a task

```sh
npx @jagersoftware/fine create --title "Feature Name" --description "What this feature does and why"
```

This auto-assigns the next available ID and generates the slug from the title.
Use descriptive titles that read well as filenames — "User Authentication"
becomes `001-user-authentication.md`.

### List all tasks

```sh
npx @jagersoftware/fine list
```

Shows each task with its ID, title, and step progress (completed/total). This is
the default command — running `fine` with no arguments does the same thing.

### Show a task

```sh
npx @jagersoftware/fine show <id>
```

Accepts padded or unpadded IDs — both `1` and `001` work. Displays the full task
content including description and all steps with their completion status.

### Add a step

```sh
npx @jagersoftware/fine add-step <id> --step "Step description"
```

Appends a new incomplete step to the task. Steps are always added as unchecked
(`- [ ]`).

## Direct markdown editing

Some operations don't have CLI commands yet. Handle these by editing the task
file directly.

### Complete a step

Open the file in `tasks/` and change `[ ]` to `[x]`:

```
Before: - [ ] Implement login endpoint
After:  - [x] Implement login endpoint
```

### Remove a step

Delete the entire line (`- [ ]` or `- [x]`) from the Steps section. If no steps
remain, remove the `## Steps` heading and the blank line above it too, so the
file stays clean.

### Edit the description

Modify the text between the `# Title` line and `## Steps`. Keep at least one
blank line after the title and before the steps heading.

### Reorder steps

Move the `- [ ]` / `- [x]` lines into the desired order. Each step is one line,
so reordering is straightforward.

## Workflow

When asked to work with tasks, follow this approach:

1. **Check what exists first.** Run `list` to see current tasks before creating
   new ones — avoid duplicates.
2. **Create tasks for distinct features**, not for individual steps. A task
   represents a self-contained body of work with a well-defined deliverable;
   steps go inside it. The executor can read other tasks but has no context from
   their execution.
3. **Break work into concrete steps using TDD.** Each step should be a single
   action with a clear deliverable, not a vague goal. "Add login endpoint with
   JWT validation" is better than "Handle authentication." Follow a test-driven
   approach: for each piece of functionality, add a step to write a failing test
   _before_ the step that implements the feature. The test step should produce a
   test that runs and fails (red), and the implementation step should make it
   pass (green). For example, instead of just "Add login endpoint," use two
   steps: "Write failing test for login endpoint" followed by "Implement login
   endpoint to pass test." Not every step needs a test (e.g., config changes,
   refactors with existing coverage), but any step that adds or changes behavior
   should be preceded by a test step.
4. **Ask when unclear.** Use AskUserQuestion to clarify ambiguities before
   creating or modifying tasks — e.g., unclear scope, missing acceptance
   criteria, or uncertain deliverables. It's better to ask than to guess wrong.
5. **Do NOT perform the work.** This skill is for task management only —
   creating, viewing, updating, and organizing tasks. After creating or updating
   a task, summarize what was created/changed and stop. Do not start
   implementing the steps.
6. **Summarize when done.** After creating a task or making changes, give a
   brief summary of the task (title, description, steps) so the user can confirm
   it looks right.

## Typical agent session

Here's the natural flow for using fine as an agent. Note: always stop after the
task management action and summarize — never start implementing the work.

```
User: "Create a task for adding dark mode support"

1. npx @jagersoftware/fine create --title "Dark Mode Support" --description "Add a dark/light theme toggle..."
2. npx @jagersoftware/fine add-step 1 --step "Define color tokens for both themes"
3. npx @jagersoftware/fine add-step 1 --step "Write failing test for ThemeProvider context"
4. npx @jagersoftware/fine add-step 1 --step "Implement ThemeProvider context to pass test"
5. npx @jagersoftware/fine add-step 1 --step "Write failing test for toggle component"
6. npx @jagersoftware/fine add-step 1 --step "Add toggle component to header to pass test"
7. npx @jagersoftware/fine add-step 1 --step "Write failing test for persisting theme preference"
8. npx @jagersoftware/fine add-step 1 --step "Persist preference to localStorage to pass test"
9. Summarize: "Created task 001 — Dark Mode Support with 7 steps (TDD: red/green pairs for each behavior): ..."
   STOP here. Do not begin implementing the steps.
```

```
User: "What's the status of our tasks?"

1. npx @jagersoftware/fine list
   → Shows all tasks with progress
2. npx @jagersoftware/fine show 1
   → Shows detail for any task that needs attention
3. Summarize the current status for the user. Do not start working on incomplete steps.
```

```
User: "Mark the color tokens step as done"

1. Edit tasks/001-dark-mode-support.md
   Change: - [ ] Define color tokens for both themes
   To:     - [x] Define color tokens for both themes
2. Summarize: "Marked 'Define color tokens for both themes' as complete."
   STOP here.
```
