---
name: fix-github-pr
description: Use when asked to fix, resolve, or address a GitHub PR — including review comments, Copilot suggestions, and CI test failures. Triggers on phrases like "fix PR", "fix PR comments", "resolve review", "address Copilot feedback", "fix review comments", "fix CI", "fix failing tests on PR", or when given a PR number to fix.
---

# Fix GitHub PR

## Overview

Systematically read, evaluate, implement, and resolve all review comments AND CI test failures on a GitHub PR — one issue at a time, with tests and commits after each fix.

**Core principle:** Never mark a comment as resolved without verified implementation and passing specs. Never claim CI is fixed without confirmed green status.

## The Process

### Phase 1: Setup

1. **Identify the PR**

   If a PR number was provided, use it directly. Otherwise, detect the PR from the current branch:

   ```bash
   # Auto-detect PR from current branch (when no PR number is given)
   gh pr view --json number,title,headRefName,baseRefName,statusCheckRollup
   ```

   If no PR is found for the current branch, list recent open PRs and ask the user to confirm:

   ```bash
   gh pr list --limit 10 --json number,title,headRefName
   ```

   Once identified, set `$PR_NUMBER` for all subsequent steps.

2. **Get full PR details**
   ```bash
   gh pr view $PR_NUMBER --json number,title,headRefName,baseRefName,statusCheckRollup
   ```

3. **Determine where to work**

   Check if the current working directory is already on the PR branch:

   ```bash
   git branch --show-current
   ```

   - **Already on the PR branch** → work here directly, no worktree needed
   - **On a different branch** → check if a worktree exists for the PR branch:
     ```bash
     git worktree list
     ```
     - Worktree exists → navigate to it
     - Worktree does not exist → create it:
       ```bash
       git worktree add ../worktrees/<branch-name> <branch-name>
       ```
     Then navigate to the worktree and work exclusively there

### Phase 2: Load All Issues to Fix

Collect ALL issues in parallel before starting to fix:

#### 2a. Review Comments

```bash
# Get review threads with their node IDs (needed to resolve them later)
gh api graphql -f query='
  query {
    repository(owner: ":owner", name: ":repo") {
      pullRequest(number: '$PR_NUMBER') {
        reviewThreads(first: 100) {
          nodes {
            id
            isResolved
            comments(first: 10) {
              nodes {
                id
                databaseId
                path
                line
                body
                author { login }
              }
            }
          }
        }
      }
    }
  }
'
```

Filter for **unresolved** threads only (`isResolved: false`). Save each thread's `id` (node ID) — it will be used to resolve the conversation after implementing the fix.

#### 2b. CI Test Failures

```bash
# Get check runs status
gh pr checks $PR_NUMBER

# Get detailed failure logs from the failed check
gh run list --branch <branch-name> --limit 5
gh run view <run-id> --log-failed
```

Parse the output to extract:
- Which spec files failed
- Exact error messages and line numbers
- Whether failures are related to review comment fixes or pre-existing

### Phase 3: Process Each Review Comment (Loop)

For **each unresolved comment**, in order:

#### 3a. Evaluate

- Read the comment carefully
- Understand what change is requested
- Check the file and line referenced
- Decide: implement, partially implement, or reply with justification

#### 3b. Implement

- Make the minimal change requested
- Stay focused on the scope of the comment — no "while I'm here" changes
- If comment is unclear or wrong, reply explaining why it won't be implemented

#### 3c. Update/Create Specs

```bash
bundle exec rspec spec/path/to/changed_file_spec.rb
```

- Create specs if the change introduces new behavior
- Ensure all related specs pass before committing

#### 3d. Commit

```bash
git add <changed files>
git commit -m "fix: address PR review comment in <file>

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

#### 3e. Resolve the Conversation

After committing the fix, resolve the review thread on GitHub:

```bash
# Reply to the comment confirming the fix
gh api repos/:owner/:repo/pulls/$PR_NUMBER/comments/$COMMENT_ID/replies \
  --method POST \
  --field body="✅ Corrigido no commit $(git rev-parse --short HEAD)"

# Resolve the review thread using the thread node ID from Phase 2a
gh api graphql -f query='
  mutation {
    resolveReviewThread(input: {threadId: "'$THREAD_NODE_ID'"}) {
      thread { isResolved }
    }
  }
'
```

**IMPORTANT:** Only resolve threads where the code was actually implemented and committed. If the comment was replied to with a justification (not implemented), do NOT resolve the thread — let the reviewer decide.

### Phase 4: Fix CI Test Failures (Loop)

For **each failing spec** from Phase 2b, in order:

#### 4a. Reproduce Locally

```bash
bundle exec rspec spec/path/to/failing_spec.rb
```

If it passes locally but failed in CI → use `superpowers:systematic-debugging` to investigate.

#### 4b. Diagnose Root Cause

- Read the full error message
- Check if failure is caused by a review comment fix from Phase 3
- Check if it's a pre-existing or environment-related failure

#### 4c. Fix and Verify

- Implement the minimal fix
- Run the spec again to confirm it passes:
  ```bash
  bundle exec rspec spec/path/to/failing_spec.rb
  ```

#### 4d. Commit

```bash
git add <changed files>
git commit -m "fix: corrigir spec falhando no CI em <file>

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

### Phase 5: Final Verification and Push

1. **Run all specs for all modified files** (not the full suite):
   ```bash
   # Find all changed files and their specs
   git diff main...HEAD --name-only | grep -v _spec | while read f; do
     spec="spec/${f#app/}"
     spec="${spec%.rb}_spec.rb"
     [ -f "$spec" ] && echo "$spec"
   done

   bundle exec rspec <list of spec files>
   ```

2. **Push the branch**
   ```bash
   git push origin <branch-name>
   ```

3. **Monitor CI** (optional, if time allows)
   ```bash
   gh pr checks $PR_NUMBER --watch
   ```

4. **Add a summary comment on the PR**
   ```bash
   gh pr comment $PR_NUMBER --body "## Revisão Concluída

   **Comentários de revisão endereçados:**
   - <list each resolved comment>

   **Falhas de CI corrigidas:**
   - <list each fixed spec>

   Specs dos arquivos modificados estão passando localmente."
   ```

## Quick Reference

| Phase | Action | Success Criteria |
|-------|--------|-----------------|
| 1. Setup | Get PR info + worktree | Correct worktree active |
| 2. Load issues | Comments + CI failures | Full list collected |
| 3. Review comments | Evaluate → implement → spec → commit → resolve | Comment marked resolved |
| 4. CI failures | Reproduce → diagnose → fix → spec → commit | Spec passes locally |
| 5. Final | Run all related specs + push + summary | PR updated, no red specs |

## Red Flags — STOP and Reassess

- Marking a conversation resolved WITHOUT a commit
- Resolving a thread where the fix was NOT implemented (only replied with justification)
- Running the full test suite (only run related specs)
- Making changes outside the scope of the comment
- Skipping spec creation for new behavior
- Claiming CI is fixed without running the spec locally
- Pushing without verifying specs pass

**STOP. Follow the process.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Comment is trivial, no test needed" | Every behavior change needs a test. |
| "I'll run all specs at the end" | Run per-file specs after EACH change. |
| "I'll resolve comments in batch" | Resolve after EACH commit, not after all. |
| "This change is obvious, skip the worktree" | Use a worktree only when NOT already on the PR branch. Never switch local branches. |
| "The comment is wrong, I'll ignore it" | Reply explaining why — never silently skip. |
| "CI failure is flaky, I'll ignore it" | Reproduce locally first, then decide. |
| "Spec passes locally, CI must be wrong" | Investigate environment differences — don't assume. |

## Notes for Kobana Project

- **Never push to main** — always use the worktree branch
- **Brazilian Portuguese** for commit summaries and PR comments
- **Only run specs for modified files** — not the entire suite
- Worktrees live in `../worktrees/<branch-name>` relative to the main repo
- Use `gh` CLI for all GitHub operations
- For flaky CI failures, use `superpowers:systematic-debugging`
