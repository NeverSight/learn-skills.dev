---
name: add-task
description: Create a new task file following the taskmd specification. Use when the user wants to add a new task to the project.
allowed-tools: Read, Edit, Bash
---

# Add Task

Create a new task file using the `taskmd add` CLI command.

## Instructions

The user's task description is in `$ARGUMENTS`.

1. **Parse the user's input** from `$ARGUMENTS` to extract:
   - The task **title** (required)
   - An optional **template** name (e.g. "bug", "feature", "chore", or a custom template)
   - Any optional flags: `--priority`, `--effort`, `--tags`, `--group`, `--depends-on`, `--parent`, `--owner`

2. **Choose the group** based on the task's domain (pass with `--group`):
   - `cli` — CLI commands, Go backend, terminal features
   - `web` — Web frontend, UI, React components
   - Omit `--group` for cross-cutting, infrastructure, documentation, or unclear domain

3. **Run `taskmd add`** with the appropriate flags:

   ```bash
   # Basic task
   taskmd add "Fix the login bug" --group cli

   # With a template
   taskmd add "Login fails on Safari" --template bug --group cli

   # With extra flags
   taskmd add "Dark mode support" --template feature --priority high --tags ui,frontend --group web
   ```

   Available templates can be listed with `taskmd templates list`. Built-in templates include `bug`, `feature`, and `chore`. Projects may define custom templates in `.taskmd/templates/`.

4. **Fill in the task content**: Read the created file and replace placeholder content (HTML comments like `<!-- ... -->`, `TODO`, `1. ...`) with real content derived from the user's description in `$ARGUMENTS`. Fill in:
   - The **Objective** section with a clear description of the goal
   - The **Tasks** section with specific, actionable subtasks
   - The **Acceptance Criteria** with concrete, verifiable criteria
   - Any template-specific sections (e.g. "Steps to Reproduce", "Expected Behavior" for bug templates)

   Use your understanding of the user's request to write meaningful content — don't leave placeholders.

5. **Validate** by running `taskmd validate` to ensure the task file is valid. If validation fails, fix the issues.

6. **Confirm** the created file path and ID to the user.
