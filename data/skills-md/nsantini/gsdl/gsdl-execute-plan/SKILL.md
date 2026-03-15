---
name: gsdl-execute-plan
description: Execute an implementation plan step-by-step with completion tracking. Use when the user wants to work through a plan, implement tasks sequentially, track progress on a task list, or asks to "execute the plan" or "start implementing".
disable-model-invocation: true
---

# Manage Task List

Guides implementation of task lists with structured completion tracking. This skill enforces a disciplined, step-by-step approach to working through tasks generated from PRDs.

## Project Context

Task lists are located at `.planning/[project-name]/tasks/tasks-[prd-name].md`. Implementation code lives at the workspace root (not inside `.planning/`).

## Operating Modes

### Standard Mode (default)

Work on **ONE sub-task at a time**. Do **NOT** start the next sub-task until the user explicitly approves. Stop after each sub-task and wait for "yes", "go", "next", etc.

### Batch Mode (GSD orchestrator only)

If your instructions say **"BATCH MODE"**, complete **all sub-tasks under your assigned parent task** without pausing for approval between sub-tasks. Apply the full completion protocol (mark `[x]`, update task file) after each sub-task, then immediately continue to the next. When the entire parent task is `[x]`, follow the **Parent Task Completion** protocol (including the git commit), then **stop and return a summary** — do not start any other parent task.

## Completion Protocol

Follow this protocol strictly when completing tasks:

### When You Finish a Sub-Task

1. **Mark the sub-task as completed**: Change `[ ]` to `[x]` immediately
2. **Update the task list file**: Save the changes to the task list
3. **Check parent task**: If ALL subtasks under a parent are now `[x]`, mark the parent as `[x]` too, then follow the **Parent Task Completion** protocol below
4. **Pause** *(Standard Mode only)*: Stop and wait for user approval before starting the next sub-task. In Batch Mode, skip this step and continue immediately.

### When You Complete a Parent Task

Once all sub-tasks under a parent are `[x]` and the parent itself is marked `[x]`:

1. **Stage all changes**: `git add -A`
2. **Commit with a descriptive message**:

```bash
git commit -m "$(cat <<'EOF'
[N.0] [Parent Task Title]

[2–4 bullet points summarising what was implemented, one per sub-task or logical group]
EOF
)"
```

Example:
```bash
git commit -m "$(cat <<'EOF'
1.0 Set up authentication module

- Created auth directory structure and base config
- Installed and configured JWT dependencies
- Added environment variable definitions for secrets
EOF
)"
```

3. **Then** pause for user approval (Standard Mode) or continue to the next parent task (Batch Mode).

### Example Workflow

```markdown
Before:
- [ ] 1.0 Parent Task
  - [x] 1.1 First sub-task (completed earlier)
  - [ ] 1.2 Second sub-task (just finished)
  - [ ] 1.3 Third sub-task (not started)

After (when 1.2 is complete):
- [ ] 1.0 Parent Task
  - [x] 1.1 First sub-task
  - [x] 1.2 Second sub-task
  - [ ] 1.3 Third sub-task (next up)

After (when 1.3 is complete and parent is done):
- [x] 1.0 Parent Task
  - [x] 1.1 First sub-task
  - [x] 1.2 Second sub-task
  - [x] 1.3 Third sub-task
```

## Task List Maintenance

### Update as You Work

1. **Mark completed items**: Update `[x]` for each finished task/sub-task
2. **Add new tasks**: If you discover additional work needed, add new tasks to the list
3. **Keep files current**: Maintain the "Relevant Files" section with accurate descriptions

### Relevant Files Section

The "Relevant Files" section should be kept up to date:

- List every file created or modified (implementation files at workspace root, planning files under `.planning/`)
- Use full paths relative to workspace root (e.g., `src/file.ts` for code, `.planning/[project-name]/tasks/tasks-prd-name.md` for planning)
- Provide a one-line description of each file's purpose
- Add new files as they are created during implementation

## Implementation Process

### Before Starting Work

1. **Read the task list from disk**: Read the task file directly from its path on disk — do **not** rely on any in-context version. The user may have edited the file (added tasks, reworded sub-tasks, reordered items) since the plan was generated. Always use the on-disk state as the source of truth.
2. **Identify the next sub-task**: Find the first unchecked `[ ]` sub-task
3. **Check for dependencies**: Ensure previous tasks are completed
4. **Understand the goal**: Make sure you understand what the sub-task requires

### During Implementation

1. **Focus on current sub-task**: Work only on the current sub-task
2. **Implement thoroughly**: Write code, tests, and documentation as needed
3. **Test your work**: Verify the implementation works correctly

### After Completing a Sub-Task

1. **Update task list**: Mark the sub-task as `[x]`
2. **Check parent task**: If all sub-tasks done, mark parent as `[x]`, then follow the **Parent Task Completion** protocol (commit before proceeding)
3. **Update Relevant Files**: Add any new files created
4. **Save the task list file**: Persist the changes
5. **Report to user**: Briefly describe what was completed
6. **Request permission**: Ask "Ready to move to the next sub-task?" or similar
7. **Wait**: Do not proceed until the user confirms

## AI Instructions

When working with task lists, you must:

1. **Regularly update the task list file** after finishing any significant work
2. **Follow the completion protocol**:
   - Mark each finished sub-task `[x]`
   - Mark parent task `[x]` once all its subtasks are `[x]`
3. **Add newly discovered tasks** if additional work is identified
4. **Keep "Relevant Files" accurate and up to date**
5. **Check which sub-task is next** before starting work
6. **Pause after each sub-task** and wait for user approval

## User Permission Phrases

Accept these as permission to continue to the next sub-task:
- "yes"
- "y"
- "go"
- "continue"
- "next"
- "proceed"
- "keep going"

Do NOT continue if the user:
- Asks questions
- Requests changes
- Wants to review something
- Says "wait", "hold on", "stop", etc.

## Handling Changes and Additions

### Discovered Issues

If you discover issues while implementing:
1. Add a new task or sub-task to the list
2. Inform the user about the addition
3. Ask if they want to address it now or later

### Task Modifications

If the user requests changes to the task list:
1. Update the task list as requested
2. Confirm the changes with the user
3. Resume from the current position

### Skipping Tasks

If the user wants to skip a task:
1. Mark it with a note (e.g., `- [ ] 2.3 [SKIPPED] Original description`)
2. Continue to the next task
3. Update the parent task status appropriately

## Quality Focus

This one-task-at-a-time approach ensures:
- **Thoroughness**: Each task gets full attention
- **Quality**: Work is reviewed before moving on
- **Alignment**: User can course-correct at each step
- **Documentation**: Progress is clearly tracked
- **Learning**: Junior developers see proper implementation pace

## Example Interaction

```
AI: "I've completed sub-task 1.2: Create login endpoint. The endpoint is now functional with proper error handling. I've marked it as complete in the task list. Ready to move to sub-task 1.3: Implement credential validation?"

User: "yes"

AI: [Proceeds to work on sub-task 1.3]
```

## File Location

Task lists follow this structure:
- **Path**: `.planning/[project-name]/tasks/tasks-[prd-name].md`
- **Example**: `.planning/my-auth-project/tasks/tasks-prd-user-authentication.md`

Always work within the project's directory structure.
