---
name: tasks
description: "Whenever the user says something like: 'Begin task: <task name>' - always read this skill to understand how to proceed."
---

# Tasks

Tasks are stored in the project root under a folder: `.agents/tasks/<task name>/`

If this folder doesn't exist, create it.

`<task name>` refers to a task name specified by the user. For example, if the user says, `Begin task: update-pull-request-workflow`, `<task name>` would be `update-pull-request-workflow`.

Inside of this `<task name>` folder are the following possible files:

- `CURRENT_DESIGN.md` - detailed description of all relevant parts of the codebase for the task we're working on. It contains all files and important functions and/or selectors for the task description given to us. If this file doesn't exist, then your first task is to create it. If this file already does exist, you do not need to read it unless it is relevant to the current TODO that you're working on.
- `PLAN.md` - detailed plan of the changes to be made. This file contains a detailed high-level plan of the changes that need to be made to the codebase in order to accomplish the task. It is based on the understanding of the codebase as established by the project `AGENTS.md` file (if it exists) and the `CURRENT_DESIGN.md` file. If this file doesn't exist, you are to create it based on the task description that the user gave you, and then afterward create `TODOs.md` based on this plan (see next bullet point). You do not need to read this file if it already exists, but you can if you find it helpful to accomplishing your current TODO from `TODOs.md`.
- `TODOs.md` - a non heirarchical numbered outline of sequential steps to be taken. Each of the todos in this file correspond to a `STEP-<N>.md` file, and those files are where any sub-steps go. Always read this file before starting any task so that you know what specific step to work on next. Example:

    ```md
    1. [x] Analyze all existing code related to creating users
    2. [ ] Refactor the codebase so that all users join the `#general` channel when they're created
    ```

- `STEP-<N>.md` - these file correspond to the numbered step from `TODOs.md`. They contain the current step status, a series of numbered sub-steps, and a final section of notes related to where we are in completing this step. You can use this file as a memory bank for important information for picking up where you left off in case the session ends, the context clears, and you need to pick up from where you left off in a new context. Here's an example of what this file could look like:

    ```md .agents/tasks/update-pull-request-workflow/STEP-1.md
    # Analyze all existing code related to creating users
    
    Status: COMPLETED
    
    ## Sub tasks
    
    1. [x] review all user-creation code in `backend/`
    2. [x] review all user-creation code in `frontend/`
    
    ## NOTES
    
    I've completed my investigation and found the following functions as relevant for creating users, starting with the backend:
    
    ### Backend user creation code
    
    - `createUser()` - `backend/userManagement.ts:78-190`
    - ...
    ```

- `KNOWLEDGE.md` - if this file exists, always read it before beginning on any TODOs. It contains project gotchas and dos & donts. Create/update this file as necessary with any useful feedback the user provides, and any discoveries you've made about the codebase as you're working (this is to save you from having to perform the same troubleshooting steps next time). Keep it concise and not too long.


## NOTES

Work in segments of one TODO at a time unless instructed otherwise. When you've completed a TODO, give the user a very brief report on what you've done. Leave any further details in the `NOTES` section of the corresponding `STEP-<N>.md` file.

To avoid using up unnecessary context, do not read previous step files (unless you need to in order to complete the current step you're working on).

Your progress should be tracked in the particular `STEP-<N>.md` file you're working on. However, if it's pertinent to completing the current step you're working on, you may update any of the other files in the tasks folder.

If as you're working on a subtask you discover that it makes sense to adjust and update the `PLAN.md` or `TODOs.md` files, then please do so immediately before proceeding on modifying any source.

- Important: never mark a TODO in TODOs.md as completed unless you've first created a corresponding `STEP-<N>.md` file for it, done the step, updated its notes section, and marked its status as `COMPLETED`.
- Important: as you are working, always update the current `STEP-<N>.md` file to mark subtasks as completed immediately after you complete them. No exceptions! Do not start the next substask until you've done this! This is to ensure interrupted sessions can smoothly pick up from where you left off. You must do this in addition to any 'todos' type tools that you are using to keep track of progress.
- Important: if your agent environment has a `todos` tool (a UI checklist), it must mirror the one-step-at-a-time discipline — **only** populate it with the current step's sub-tasks (from the current `STEP-<N>.md`). Do NOT pre-populate it with all remaining top-level TODOs from `TODOs.md`. The `todos` tool tracks *sub-tasks within the current step*, not the overall plan. Update it as you complete each sub-task, and clear/reset it when you move to the next step.

After you've completed a step and marked its TODO in the `TODOs.md` as done, stop and let the user review your changes (unless otherwise instructed to continue without stopping).

## Review Only Instruction

If the user tells you either "review only", "verify only" or "verify plan" for the task (or something to that effect), this indicates that they don't want you to actually complete any TODOs. Instead, for this session just review the existing CURRENT_DESIGN.md, PLAN.md, TODOs.md (and any relevant STEP file), compare it to the codebase, and verify whether the current plan is sound or if any adjustments should be made. If adjustments should be made, update the documents accordingly and then stop after giving the user a brief summary of the changes.

## Managing limited context

There are two useful tools an agent environment might have:

- (A) The ability to know how much context is remaining
- (B) A tool that lets you start a fresh session context and continue where you left off by passing in context to the new session tool

If the agent software has (A) but not (B), then come to a stop when you have little context remaining and give a brief report to the user.

If the agent software has both (A) and (B) and it's time to start a fresh session because of limited remaining context, use (B) to start a fresh session in a way that let's you pick up from where you left off. Make sure to **always** tell yourself to load the 'tasks' skill in the new session context, and then per the instructions here, provide it the user-given `<task name>` you've been working on.

If it has neither (A) nor (B), don't worry about it, hopefully it will auto-compact properly.
