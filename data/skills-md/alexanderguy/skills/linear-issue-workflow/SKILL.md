---
name: linear-issue-workflow
description: Implement a feature or fix based on a Linear issue
argument-hint: "<issue-id> [--reviewer <reviewer>]"
disable-model-invocation: true
---

# Linear Issue Workflow

Use this skill when implementing features or fixes tracked in Linear.

## Phase 1: Understand the Issue

Fetch the Linear issue using the `linear` subagent:

```
Task(subagent_type="linear", prompt="Fetch issue <ISSUE-ID> including title, description, status, and acceptance criteria")
```

Ask the user clarifying questions if the scope is unclear before proceeding.

## Phase 2: Explore and Plan

1. Use the `explore` subagent to understand the codebase:
   - Where changes need to be made
   - Existing patterns to follow
   - Related code that might be affected

2. Create an implementation plan covering:
   - Files to modify
   - New functions/types to add
   - Tests to write

3. Present the plan to the user and ask if they would like any changes before proceeding. Do not start implementation until the user approves the plan.

4. Optionally attach the plan to the Linear issue:

   ```
   Task(subagent_type="linear", prompt="Attach this implementation plan as a document to <ISSUE-ID>: <plan>")
   ```

5. Mark the issue as "In Progress":
   ```
   Task(subagent_type="linear", prompt="Update issue <ISSUE-ID> status to In Progress")
   ```

## Phase 3: Set Up Worktree

Get the branch name from Linear:

```
Task(subagent_type="linear", prompt="Get the git branch name for issue <ISSUE-ID>")
```

Determine the repository's default branch:

```bash
git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@'
```

Fetch the latest changes and create a worktree based on the remote default branch:

```bash
git fetch origin
git worktree add ../worktree/<branch-name> -b <branch-name> origin/<default-branch>
```

**Important**: Always base new branches on `origin/<default-branch>` (where `<default-branch>` is `main`, `master`, or whatever the repository uses). This ensures your branch starts from the latest remote state, even if your local default branch is out of date.

After creating the worktree:

```bash
cd ../worktree/<branch-name>
```

Then install local dependencies (look at developer documentation for how to do this).

Worktrees share the `.git` directory but have their own working directory. The `node_modules` directory is NOT shared, so each worktree needs its own dependency installation.

All subsequent work happens in the worktree directory.

## Phase 4: Implement

1. Use `TodoWrite` to track implementation tasks
2. Implement changes, marking todos as complete as you go
3. Write tests for new functionality
4. Run the project's build/verification command

## Phase 5: Verify

If the changes affect critical paths or integration points, run the project's test suite or integration tests as appropriate for the changes made.

## Phase 6: Commit and PR

### Squash commits if needed

If you made multiple commits that should be one:

```bash
git reset --soft HEAD~<n> && git commit -m "<message>"
```

### Self-review

Before pushing, load the `code-review` skill and perform a self-review of your changes. If serious issues are found that would prohibit merging, fix them before proceeding. Do not push until the review passes.

After the review passes, ask the user for confirmation before pushing and creating the PR.

### Post review to PR

After creating the PR, post a summary of the code review as a comment:

```bash
gh pr comment <PR-NUMBER> --body "$(cat <<'EOF'
## Self-Review Summary

<summary of what was reviewed and any issues found/fixed>

### Files Reviewed

- `path/to/file.ts`: <brief assessment>

### Issues Found and Resolved

<list any issues found during self-review and how they were fixed, or "None">
EOF
)"
```

### Push and create PR

Fetch the latest changes and rebase before pushing:

```bash
git fetch origin
git rebase origin/<default-branch>
```

Verify the build still passes after rebasing, then push:

```bash
git push -u origin <branch-name>
```

Create the PR:

```bash
gh pr create \
  --title "<title>" \
  --reviewer <REVIEWER> \
  --body "$(cat <<'EOF'
## Summary

<1-3 bullet points>

## Changes

- `path/to/file.ts`: <what changed>

## Testing

<how it was tested>

Closes <ISSUE-ID>
EOF
)"
```

## Phase 7: Cleanup After Merge

After the PR has been merged, clean up the worktree and local branch:

```bash
# From the main repository directory (not the worktree)
git fetch origin
git worktree remove ../worktree/<branch-name>
git branch -d <branch-name>
```

If the worktree directory was already manually deleted, prune stale worktree references:

```bash
git worktree prune
```

## Linear Subagent Patterns

Common operations:

| Action          | Prompt                                                          |
| --------------- | --------------------------------------------------------------- |
| Fetch issue     | `Fetch issue <ISSUE-ID> with full details`                      |
| Get branch name | `Get the git branch name for issue <ISSUE-ID>`                  |
| Update status   | `Update issue <ISSUE-ID> status to In Progress`                 |
| Attach document | `Attach this as a document titled "X" to <ISSUE-ID>: <content>` |
| Add comment     | `Add a comment to <ISSUE-ID>: <comment>`                        |

Always use `subagent_type="linear"` when calling the Task tool for Linear operations.
