---
name: ah-finalize-code
description: Use this skill to finalize code changes before creating a PR when using the "ah" prefix. Use when asked to "ah finalize code", or "ah finalize changes". Runs a multi-step workflow that simplifies code, creates a retrospective, adds tests, updates JSDoc references, updates documentation, optimizes specs, performs a code review, and creates a pull request -- committing after each step.
argument-hint: "no arguments needed, works on the current branch"
---

# Finalize Code

Orchestrate the full pre-PR finalization workflow for the current branch. This involves running a sequence of specialized subagents -- each handling a different aspect of the finalization (simplification, testing, documentation, specs, code review) -- with a commit after every step. The workflow ends by creating a pull request.

## Configuration

- **Subagent model defaults**: Opus for all subagents except `committer`, which uses Sonnet
- **Thinking mode**: ultrathink effort for all subagents

## Procedure

### 0. Initialize

```bash
BRANCH_NAME=$(git branch --show-current)
REPO_NAME=$(basename -s .git "$(git remote get-url origin)")
SAFE_BRANCH_NAME=$(echo "${BRANCH_NAME}" | tr '/' '-')
SPEC_DIR="specs/${BRANCH_NAME}"
PROGRESS_FILE="~/.agents/arinhub/progresses/progress-pr-${REPO_NAME}-${SAFE_BRANCH_NAME}.md"
```

Read `${SPEC_DIR}/spec.md` and extract:

- `BASE_BRANCH` from the **Base Branch** metadata field
- `ISSUE_NUMBER` from the **Issue Number** metadata field

If either value is missing from spec.md, ask the user before proceeding.

Compute the merge base for the current branch:

```bash
MERGE_BASE=$(git merge-base "${BASE_BRANCH}" HEAD)
```

Each subagent that analyzes code changes must compute its own fresh diff before starting its work:

```bash
DIFF=$(git diff "${MERGE_BASE}")
```

This ensures every subagent sees the latest state of changes, including modifications committed by previous steps.

If the repository is a monorepo, identify the correct application from the changed files in the diff and run all commands in the context of that application.

Read the template from `references/progress-pr.md`, replace all `<BRANCH_NAME>`, `<BASE_BRANCH>`, `<ISSUE_NUMBER>`, and `<TIMESTAMP>` placeholders with actual values, and write the result to `${PROGRESS_FILE}`. Every subagent updates its own section after completing its work.

### 1. Simplify

Spawn subagent **simplifier** (Opus, ultrathink):

- Get fresh diff: `git diff "${MERGE_BASE}"`
- Run `/simplify` with prompt: `Simplify changes in current diff only, then check "pnpm preflight"`
- Update `${PROGRESS_FILE}` Simplifier section (status: completed, findings)

Then spawn subagent **committer** (Sonnet) -- run `/commit`.

### 2. Retrospective

Spawn subagent **retrospective** (Opus, ultrathink):

- Run `/speckit.retrospective.analyze` with prompt: `On the end fix follow-up actions in retrospective file and update retrospective file`
- Update `${PROGRESS_FILE}` Retrospective section

Then spawn subagent **committer** (Sonnet) -- run `/commit`.

### 3. Test Creator

Spawn subagent **test-creator** (Opus, ultrathink):

- Get fresh diff: `git diff "${MERGE_BASE}"`
- Prompt: `Run command "npm run test:coverage", find the coverage file location from the npm script test:coverage configuration, read coverage file, add important tests for changes in current diff only, optimize count of tests to avoid redundancy, verify coverage improvements, then run "npm run preflight"`
- Update `${PROGRESS_FILE}` Test Creator section

Then spawn subagent **committer** (Sonnet) -- run `/commit`.

### 4. JSDoc Updater

Spawn subagent **jsdoc-updater** (Opus, ultrathink):

- Get fresh diff: `git diff "${MERGE_BASE}"`
- Prompt: `In JSDoc comments on the current diff, add/update spec references using shorthand "SXXX:FR-YYY" or "SXXX:SC-YYY" format (S001=001-minute-qset-react) with short descriptions, remove outdated refs and task numbers (e.g. T012), ensure standard JSDoc format, add missing shorthand to spec.md if needed, and run formatter + linter on modified files.`
- Update `${PROGRESS_FILE}` JSDoc Updater section

Then spawn subagent **committer** (Sonnet) -- run `/commit`.

### 5. Tests Docs Updater

Spawn subagent **tests-docs-updater** (Opus, ultrathink):

- Get fresh diff: `git diff "${MERGE_BASE}"`
- Prompt: `Update docs/tests/tests-*.md files to reflect changes in current diff only, ensure that each test file follows the established format and includes all necessary details. If no code changes are detected, do not make changes. Check if there are any redundant or unnecessary tests in changes in current diff -- if so, remove redundant tests.`
- Update `${PROGRESS_FILE}` Tests Docs Updater section

Then spawn subagent **committer** (Sonnet) -- run `/commit`.

### 6. API Docs Updater

Spawn subagent **api-docs-updater** (Opus, ultrathink):

- Prompt: `Run "pnpm docs:generate", then extract type definitions, interfaces, and function signatures from "docs/typedoc" output to create/update "docs/api/index.md" (overview + TOC) and topic files ("docs/api/api-components.md", "api-hooks.md", etc.) with one file per logical section, validate all index links resolve to existing files, and report progress -- do not generate code examples, tutorials, or document private APIs.`
- Update `${PROGRESS_FILE}` API Docs Updater section

Then spawn subagent **committer** (Sonnet) -- run `/commit`.

### 7. Spec Optimizer

Spawn subagent **spec-optimizer** (Opus, ultrathink):

- Get fresh diff: `git diff "${MERGE_BASE}"`
- Prompt: `Optimize the "${SPEC_DIR}/" folder by reading all files, removing redundant ones (completed research, moved quickstart guides, done checklists/task lists), consolidating key info into the essential files (spec.md, plan.md, data-model.md, retrospective.md, contracts/), removing obsolete contracts and outdated "Next Steps" sections, and verifying no critical context, valid links, or needed information is lost.`
- Update `${PROGRESS_FILE}` Spec Optimizer section

Then spawn subagent **committer** (Sonnet) -- run `/commit`.

### 8. Spec Updater

Spawn subagent **spec-updater** (Opus, ultrathink):

- Get fresh diff: `git diff "${MERGE_BASE}"`
- Prompt: `Update files in the "${SPEC_DIR}/" folder to reflect the code changes in current diff only. Ensure that each spec file follows the established format and includes all necessary details. If no code changes are detected, do not make changes.`
- Update `${PROGRESS_FILE}` Spec Updater section

Then spawn subagent **committer** (Sonnet) -- run `/commit`.

### 9. Code Review

Spawn subagent **code-reviewer** (Opus, ultrathink):

- Run `/ah-review-code` with prompt: `base branch is ${BASE_BRANCH}, after code review read the code review file and fix all issues you find, then check "pnpm preflight"`
- Update `${PROGRESS_FILE}` Code Reviewer section

Then spawn subagent **committer** (Sonnet) -- run `/commit`.

### 10. Create PR

Spawn subagent **pr-creator** (Opus, ultrathink):

- Run `/ah-create-pr` with prompt: `base branch: ${BASE_BRANCH}, issue number: ${ISSUE_NUMBER}`
- Update `${PROGRESS_FILE}` PR Creator section (status: completed, PR URL).

### 11. Report to User

Present a summary:

- Path to `${PROGRESS_FILE}` with the full audit trail
- PR URL
- List of steps completed and any issues encountered
- Any unresolved findings from the code review

## Important Notes

- Every subagent except `committer` runs on Opus with ultrathink effort mode. The `committer` subagent runs on Sonnet.
- The `${PROGRESS_FILE}` serves as a running audit trail. Each subagent (except `committer`) updates its section immediately after finishing, so progress is always visible. The `committer` subagent only creates a commit and does not update the progress file.
- All Spec Kit output files live in `specs/<branch-name>/`.
- The workflow is strictly sequential -- each step must complete before the next begins, because later steps depend on commits from earlier steps.
- If any subagent fails, note the failure in `${PROGRESS_FILE}` and report to the user before continuing. Do not silently skip steps.
- The `/commit` command creates a conventional commit with a descriptive message based on the staged changes. The committer subagent should not do anything else beyond creating the commit.
- Base branch and issue number come from `spec.md` metadata -- if they are missing, ask the user before starting.
- Each subagent computes a fresh diff (`git diff "${MERGE_BASE}"`) before starting its work, so it always sees the latest state including commits from previous steps.
- In a monorepo, identify the correct application from the changed file paths and scope all commands (preflight, test, lint, etc.) to that application.
