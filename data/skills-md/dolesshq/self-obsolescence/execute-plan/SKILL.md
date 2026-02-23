---
name: execute-plan
description: Execute an existing plan file. Use when a user asks to carry out a .plan.md task list.
metadata:
  short-description: Execute a plan
---

# Execute Plan

## Goal

Execute a plan stored in `.cursor/plans/*.plan.md`, updating todo statuses as work progresses.

## Minimal workflow

1. **Load the plan file**
   - Read the provided `.plan.md` path.
   - Confirm the plan uses the expected YAML frontmatter with `todos`.
   - If the path or format is missing, ask the user for clarification.

2. **Execute tasks with status transitions**
   - When starting a task, set its `status` to `in_progress`.
   - Keep at most one `in_progress` task at a time.
   - When a task is finished, set its `status` to `completed`.
   - Update the plan file after each status change.

3. **Handle scope changes**
   - If the user adds or changes requirements, update the plan file to reflect the new or adjusted todos.

4. **Output formatting**
   - In responses, reference the plan file path and describe what was completed or is in progress.

5. **Completion requirements**
   - When all todos are completed, output a Markdown block that begins with:
     - `I just implemented <plan filepath>. Review the plan, review all code changes, and determine if the changes align with the plan. Then have a UI testing subagent manually verify any and all front-end changes.`
   - Below that opening line, include:
     - A concise summary of all changes made while executing the plan.
     - A file-level change log describing what changed in each file and why.
     - Clear, actionable instructions for a UI tester to manually validate the changes, using a generic tester alias (for example, `ui-ux-tester`).
       - Assume the tester has zero knowledge of the codebase.
       - For every manual check, specify where to go in product terms (route/page URL and the relevant section, panel, or table).
       - Avoid component-only references (for example, "DatePicker", "TableRow", "Modal X") unless paired with exact on-page location and user-visible labels.
       - Prefer task language the tester can execute directly: "Open `<route>`, click `<button label>`, verify `<expected result>`."
   - Write the same completion Markdown (opening line + summary + file-level change log + UI tester instructions) back into the `.plan.md` file under a new section named `## Reviewer Handoff`.
     - This section is for reviewers to reference later.
     - Do **not** include the request for approval to archive the plan in this `.plan.md` section.
   - The summary must include the plan name and its filepath.
   - After the summary, ask the user for approval to archive the plan.
   - If the user approves, move the plan file from `.cursor/plans/` to `.cursor/plans/archive/` and confirm the new location.

## Reviewer Handoff Template

Use this exact structure in the final user response and mirror it in the plan file under `## Reviewer Handoff` (excluding the archive-approval ask in the plan file):

```markdown
I just implemented <plan filepath>. Review the plan, review all code changes, and determine if the changes align with the plan. Then have a UI testing subagent manually verify any and all front-end changes.

Implemented plan: **<plan name>** at `<plan filepath>`.

Change summary:
- <high-level outcome 1>
- <high-level outcome 2>

File-level changelog:
- `<absolute-or-workspace-relative-path>`: <what changed and why>
- `<absolute-or-workspace-relative-path>`: <what changed and why>

UI manual verification checklist:
1. `<ui tester alias>`: Open `<route>`. In `<section/panel/table>`, click `<control label>`, then verify `<expected result>`.
1. `<ui tester alias>`: Open `<route>`. In `<section/panel/table>`, perform `<user action>`, then verify `<expected result>`.
1. `<ui tester alias>`: Open `<route>`. In `<section/panel/table>`, verify `<visual/behavioral expectation>`.
```
