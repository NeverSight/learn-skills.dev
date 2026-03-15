---
name: ah-create-tasks
description: Use this skill to create tasks from a PRD and ADR using the "ah" prefix. Use when asked to "ah create tasks". This skill runs the full Spec Kit pipeline -- specify, clarify, plan, research, complexity check, checklist, and task generation -- with consistency analysis passes, committing after each major step.
argument-hint: "path to prd.md file and adr.md file"
---

# Create Tasks from PRD and ADR

Orchestrate the full Spec Kit pipeline to transform a `prd.md` and `adr.md` file into a well-structured `tasks.md` file. The workflow generates intermediate design artifacts (spec.md, plan.md, research.md, checklists), performs consistency checks, and commits after each major step.

## Input

- **prd.md path** (required): Path to the PRD file that describes the feature. If not provided by the user, ask before proceeding.
- **adr.md path** (required): Path to the ADR (Architectural Decision Records) file that describes architectural decisions, constraints, and rationale. If not provided by the user, ask before proceeding.
- **issue number** (required): The GitHub issue number this feature relates to (e.g., `42`). If not provided by the user, ask before proceeding.

## Configuration

- **Subagent model defaults**: Opus for all subagents except `committer`, which uses Sonnet
- **Thinking mode**: ultrathink effort for all subagents

## Procedure

### 0. Initialize

```bash
BASE_BRANCH=$(git branch --show-current)
REPO_NAME=$(basename -s .git "$(git remote get-url origin)")
PROGRESS_TEMPLATE="progress-tasks.md"
```

If the user did not provide **prd.md path**, **adr.md path**, or **issue number**, ask them for all missing values now (before any other work begins). Store these values as `PRD_PATH`, `ADR_PATH`, and `ISSUE_NUMBER`.

Verify that `prd.md` exists at `PRD_PATH` and `adr.md` exists at `ADR_PATH`. If either file does not exist, ask the user for the correct path.

### 1. Specify

Read `prd.md` and distill it into a prompt for the `/speckit.specify` command. The prompt should focus on **what** and **why** -- strip out tech stack details, implementation specifics, and architecture choices. Keep only the user-facing requirements, goals, and motivation.

Spawn subagent **specifier** (Opus, ultrathink):

- Run `/speckit.specify` with the distilled prompt
- After `/speckit.specify` completes, it will have created a new branch. Capture it:
  ```bash
  NEW_BRANCH_NAME=$(git branch --show-current)
  SPEC_DIR="specs/${NEW_BRANCH_NAME}"
  SAFE_BRANCH_NAME=$(echo "${NEW_BRANCH_NAME}" | tr '/' '-')
  PROGRESS_FILE="~/.agents/arinhub/progresses/progress-tasks-${REPO_NAME}-${SAFE_BRANCH_NAME}.md"
  ```
- Initialize `${PROGRESS_FILE}` using the template `references/${PROGRESS_TEMPLATE}`. Replace all `<PLACEHOLDER>` values with actual values (branch name, base branch, PRD path, ADR path, issue number, timestamp). Every subagent updates its own section in this file after completing its work.
- After the file is generated, prepend the following metadata block at the very top of `spec.md` (before any existing content):
  ```
  **Base Branch**: <BASE_BRANCH>
  **Issue Number**: <ISSUE_NUMBER>
  **Input**: <the distilled prompt>
  ```
- Update `${PROGRESS_FILE}` Specifier section (status: completed, findings)

### 2. Commit

Spawn subagent **committer** (Sonnet):

- Run `/commit`

### 3. Verify Spec

Spawn subagent **spec-verifier** (Opus, ultrathink):

- Prompt: `Act as a Senior Code Reviewer. Analyze spec.md in ${SPEC_DIR} and identify errors, logical gaps, or inconsistencies. If the spec.md references refactoring or existing codebases, perform a comparative analysis to ensure functional parity and identify any missing requirements. Fix all issues you find.`
- Update `${PROGRESS_FILE}` Spec Verifier section

### 4. Commit

Spawn subagent **committer** (Sonnet):

- Run `/commit`

### 5. Clarify

Run `/speckit.clarify` yourself (not as a subagent -- this command may require user interaction).

If the clarification process asks questions that need user input, **wait for the user to respond** before proceeding. Do not skip or auto-answer clarification questions.

Update `${PROGRESS_FILE}` Clarifier section.

### 6. Commit

Spawn subagent **committer** (Sonnet):

- Run `/commit`

### 7. Plan

Read `adr.md` at `ADR_PATH` and create a concise prompt for the `/speckit.plan` command. The ADR contains architectural decisions, constraints, and rationale -- use these to inform the prompt with tech stack choices, architecture patterns, and design trade-offs. Keep it short -- just the key technology decisions, architectural patterns, and relevant ADR decisions.

Also read AGENTS.md in the repo root to gather active technologies and recent changes. After generating the plan, update AGENTS.md with any new active technologies or recent changes discovered during planning.

Spawn subagent **planner** (Opus, ultrathink):

- Run `/speckit.plan` with the concise tech/architecture prompt
- Update `${PROGRESS_FILE}` Planner section

### 8. Commit

Spawn subagent **committer** (Sonnet):

- Run `/commit`

### 9. Research

Spawn subagent **researcher** (Opus, ultrathink):

- Prompt: `I want you to go through the implementation plan and implementation details in ${SPEC_DIR}, looking for areas that could benefit from additional research. For those areas that you identify that require further research, update the research document with additional details about the specific versions that we are going to be using in this application and spawn parallel research tasks to clarify any details using research from the web or context7 tool.`
- Update `${PROGRESS_FILE}` Researcher section

### 10. Commit

Spawn subagent **committer** (Sonnet):

- Run `/commit`

### 11. Complexity Check

Spawn subagent **complexity-checker** (Opus, ultrathink):

- Prompt: `Cross-check the details to see if there are any over-engineered pieces in folder ${SPEC_DIR}. Return a numbered list of all issues found with severity and recommended fix for each.`

After the subagent returns, present its findings to the user yourself (not in a subagent) and **ask which issues to fix**. Wait for the user to respond before continuing.

Once the user responds, spawn subagent **complexity-fixer** (Opus, ultrathink):

- Prompt: `Fix the following issues in ${SPEC_DIR}: <list of user-selected issues from complexity-checker findings>`
- Update `${PROGRESS_FILE}` Complexity Checker section

### 12. Commit

Spawn subagent **committer** (Sonnet):

- Run `/commit`

### 13. Generate Checklist

Spawn subagent **checklist-generator** (Opus, ultrathink):

- Run `/speckit.checklist` with prompt: `full breadth pre-implementation checklist, exclude the general spec-quality items already covered in requirements.md and focus only on domain-specific requirement gaps`
- Update `${PROGRESS_FILE}` Checklist Generator section

### 14. Check Checklist

Spawn subagent **checklist-checker** (Opus, ultrathink):

- Prompt: `Read the checklist in ${SPEC_DIR}, and check off each item in the checklist if the feature spec meets the criteria. Leave it empty if it does not. Fix all gaps.`
- Update `${PROGRESS_FILE}` Checklist Checker section

### 15. Commit

Spawn subagent **committer** (Sonnet):

- Run `/commit`

### 16. Generate Tasks

Spawn subagent **tasks-generator** (Opus, ultrathink):

- Run `/speckit.tasks`
- Update `${PROGRESS_FILE}` Tasks Generator section

### 17. Commit

Spawn subagent **committer** (Sonnet):

- Run `/commit`

### 18. Analyze Tasks (Pass 1)

Spawn subagent **tasks-analyzer** (Opus, ultrathink):

- Run `/speckit.analyze` with prompt: `if there are any issues fix all`
- Update `${PROGRESS_FILE}` Tasks Analyzer (pass 1) section

### 19. Commit

Spawn subagent **committer** (Sonnet):

- Run `/commit`

### 20. Analyze Tasks (Pass 2)

Spawn subagent **tasks-analyzer-2** (Opus, ultrathink):

- Run `/speckit.analyze` with prompt: `if there are any issues fix all`
- Update `${PROGRESS_FILE}` Tasks Analyzer (pass 2) section

### 21. Commit (Final)

Spawn subagent **committer** (Sonnet):

- Run `/commit`

### 22. Report to User

Present a summary:

- Path to the generated `tasks.md`
- Path to `${PROGRESS_FILE}` with the full audit trail
- List of all generated artifacts in `${SPEC_DIR}/`
- Any unresolved issues or warnings from the analysis passes
- Next steps: the user can now run `/speckit.implement` to begin implementation

## Workflow Diagram

```
prd.md + adr.md
  |        |
  v        |
[1] /speckit.specify --> spec.md (uses prd.md)
  |        |
  v        |
[3] spec-verifier --> fixes spec.md
  |        |
  v        |
[5] /speckit.clarify --> user Q&A --> updates spec.md
  |        |
  v        v
[7] /speckit.plan --> plan.md, research.md, data-model.md (uses adr.md)
  |
  v
[9] researcher --> updates research.md
  |
  v
[11] complexity-checker --> user picks fixes
  |
  v
[13-14] /speckit.checklist --> checklist-checker --> fixes gaps
  |
  v
[16] /speckit.tasks --> tasks.md
  |
  v
[18] /speckit.analyze (pass 1) --> fixes
  |
  v
[20] /speckit.analyze (pass 2) --> fixes
  |
  v
tasks.md (final)
```

Each arrow includes a `/commit` step (not shown for brevity).

## Important Notes

- Every subagent except `committer` runs on Opus with ultrathink effort mode. The `committer` subagent runs on Sonnet.
- Steps 5 (clarify) and 11 (complexity check) require user interaction -- the workflow pauses and waits for user input before continuing.
- The `${PROGRESS_FILE}` file serves as a running audit trail. Each subagent updates its section immediately after finishing, so you can always see what has been done and what remains.
- All Spec Kit output files are saved to `specs/<NEW_BRANCH_NAME>/`.
- If any subagent fails, note the failure in `${PROGRESS_FILE}` and report to the user before continuing. Do not silently skip steps.
- The `/commit` command creates a conventional commit with a descriptive message based on the staged changes. The committer subagent should not do anything else beyond creating the commit.
