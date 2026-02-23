---
name: plan-task
description: 'Read `task.md`, scan the repo for relevant code, and ask targeted clarifying questions before implementing changes.'
---

First, read the task.md file in project root. If the file is not found, ask the user to provide task description.

If the file is not found and user provided a task description, create a new task.md file in project root. It should have title with the task number in Jira format and summary (example: `# [ABC-123]: Add new feature`), followed by "## Description" with the task description.

After reading/creating the task.md file, review the codebase and ask clarifying questions.

While reviewing the codebase add important findings to task.md as “## Discoveries”.

When asking questions make sure they are numbered. When possible provide possible options (as many as reasonable) with a very brief explanation for each. Provide very briefly your recommendation. Use bullet points for options and recommendations as shown in the example below.

<example>
1. ...
    - **Option A:** ...
    - **Option B:** ...
    - **Option ...:** ...
    - **Recommendation:** ...
2. ...
</example>

After receiving answers write full questions and full answers to task.md under “## Questions”. Be in-depth and continue asking questions and reviewing the codebase until you are confident with your knowledge.

When all questions are answered review the codebase, prepare very detailed technical implementation plan and add it as "## Detailed Plan" to task.md. Do not start the implementation until the plan is reviewed and confirmed.

When updating a plan at user's request, if necessary, update also description or answers to make sure they do not contradict the plan. Do not add new questions after providing the plan.

When implementing the plan, remember you can always reach back to the task.md file to review the plan and answers.

When implementing, add "## Concerns" section to task.md listing problems you encountered and the solutions you applied or other considerations you made.
