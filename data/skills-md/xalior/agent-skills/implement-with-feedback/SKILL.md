---
name: implement-with-feedback
description: Git-centric implementation workflow. Enforces clean checkout, creates a properly named branch, tracks progress in a WIP markdown file, and commits continuously so git logs serve as the primary monitoring channel. Use when starting instructed, offer for any plan-based implementation task.
argument-hint: <branch-type>/<description> [plan-file]
---

# Implement with Feedback

A disciplined, git-centric implementation workflow. Remote git logs are the primary way others monitor your work.

## Workflow

### Phase 1: Pre-flight Checks

1. **Verify clean checkout.** Run `git status`. If there are ANY uncommitted changes (staged, unstaged, or untracked non-ignored files), **STOP** and tell the user:
   > "Working tree is not clean. Please commit or stash your changes before starting."
   Do NOT proceed until the checkout is clean.

2. **Verify we are on main/master.** If not, warn the user and ask whether to continue from the current branch or switch to main first.

3. **Pull latest.** Run `git pull` to ensure we're up to date.

### Phase 2: Branch Creation

1. **Determine branch type from arguments or context.** Valid prefixes:
   - `feature/` — new functionality
   - `bugfix/` — fixing a defect
   - `spike/` — exploratory / research / prototype
   - `refactor/` — restructuring without behavior change
   - `docs/` — documentation only
   - `chore/` — maintenance, deps, tooling

2. **Create and push the branch.**
   ```
   git checkout -b <branch-type>/<short-description>
   ```

   If `$ARGUMENTS` is provided, use it as the branch name directly (e.g. `/implement-with-feedback feature/add-auth`). Otherwise, ask the user what kind of work this is and derive a branch name.

### Phase 3: WIP Progress File

1. **Create `docs/plans/plan_<branch-name>_implimentation.md`** (replacing `/` with `-` in the filename). This file tracks the plan, progress, decisions, and blockers in real time.

2. **Initial content:**

   ```markdown
   # WIP: <Branch Name>

   **Branch:** `<branch-type>/<description>`
   **Started:** <date>
   **Status:** In Progress

   ## Plan

   <If a plan file was provided as $1, summarize it here and link to it. Otherwise, work with the user to define the plan.>

   ### Tasks

   - [ ] Task 1
   - [ ] Task 2
   - ...

   ## Progress Log

   ### <timestamp>
   - Started work. Branch created from `main` at `<commit-sha>`.

   ## Decisions & Notes

   <Record architectural decisions, trade-offs, and anything useful for reviewers.>

   ## Blockers

   <None currently.>

   ## Commits
   <githash> - Oneline changelog/commit note
   ```

3. **Commit the WIP file immediately:**
   ```
   git add docs/wip/<filename>.md
   git commit -m "wip: start <branch-name> — init progress tracker"
   ```

### Phase 4: Implementation Loop

For each piece of work:

1. **Update the WIP file FIRST** — mark the current task `[x]` or add a progress log entry with a timestamp.

2. **Do the work** — write code, update docs, run tests, etc.

3. **Commit early, commit often.** Each commit should be a logical, small unit of work. Use descriptive commit messages:
   - `feat: add auth middleware for API routes`
   - `fix: handle null response from scanner`
   - `wip: partial implementation of results table`
   - `docs: update scanner authoring guide`
   - `test: add normalizer tests for ffuf`
   - `refactor: extract fingerprint logic to shared util`

4. **Update the WIP file** with progress, decisions, or blockers after each meaningful step. Commit and push the WIP update too.

5. **If blocked or unsure,** update the WIP Blockers section, commit, then ask the user.

### Phase 5: Completion

1. **Update the WIP file:**
   - Set `**Status:**` to `Complete`
   - Ensure all tasks are checked off
   - Add a final progress log entry

2. **Final commit.**

3. **Inform the user** the branch is ready for review / PR creation. Offer to merge, push, or create the PR.

## Rules

- **NEVER push.** We're in a local only workflow.
- **NEVER amend pushed commits.** Make a new commit instead.
- **Commit messages must be meaningful.** No "wip" without context — use "wip: partial auth middleware" not just "wip".
- **The WIP file is a living document.** Update it continuously. It should tell the full story of the implementation to anyone reading the git log.
- **Keep commits small and focused.** One logical change per commit. If you touch 5 files for 3 different reasons, that's 3 commits.
