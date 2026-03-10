---
name: git-workflow
description: "LOAD THIS SKILL when: creating PRs, pushing changes, creating branches, fixing PR review comments, syncing branches, user mentions 'pr', 'push', 'branch', 'pr-fix-comments', 'sync-branches'. Covers git workflow automation with CI monitoring, PR lifecycle, and branch management."
---

# Git Workflow

Git workflow automation covering PR lifecycle, branch management, CI monitoring, and review comment handling.

## PR Workflow

Create branch (if needed), commit, push, and create/update PR in one command.

### Instructions

Run everything as ONE chained command so user approves only once:

```bash
git checkout -b <branch> && git add -A && git commit -m "<msg>" && git push -u origin HEAD && bun run gh-tool pr create --base <base> --title "<title>" --body "<body>"
```

- If already on a feature branch, skip `git checkout -b`
- Check if PR exists: `bun run gh-tool pr view --json number -q .number 2>/dev/null`
- If PR exists, use `bun run gh-tool pr edit <pr_number> --title "<title>" --body "<body>"` instead of `bun run gh-tool pr create`
- Base branch: argument provided by user (default: `test`)
- Branch naming: `feat/`, `fix/`, `chore/` based on changes

### Monitor Checks and Iterate

After pushing, **automatically enter the monitoring loop**.

Inform the user: "PR created. Monitoring CI checks... (say 'stop' to exit the loop)"

#### Wait for CI checks to complete

Poll check status every 30 seconds:

```bash
bun run gh-tool pr checks --pr <pr_number> --watch
```

Or manually poll:

```bash
bun run gh-tool pr checks --pr <pr_number>
```

States: `PENDING`, `QUEUED` → still running. `COMPLETED` → check conclusion.

#### Handle check results

**If any check fails:**

1. Get the failed check details:

   ```bash
   bun run gh-tool pr checks-failed --pr <pr_number>
   ```

2. For build/lint/test failures, fetch logs if available or analyze the error
3. Fix the issues locally
4. Run validation command (e.g., `bun run check`)
5. Commit and push the fix
6. **Go back to monitoring** to check again

**If all checks pass:**

- Inform user: "All checks passed. PR is ready for review! 🎉"
- Exit the loop

#### Loop exit conditions

Exit the monitoring loop when:

- All checks pass
- User says "stop" or requests to exit
- Maximum 5 iterations reached (then ask user to continue)

### PR Body Format

```
## Summary
<1-2 sentences>

## Changes
- <bullet list>
```

---

## Push Workflow

Commit all changes and push to current branch in one command.

### Instructions

Run everything as ONE chained command so user approves only once:

```bash
git add -A && git commit -m "<msg>" && git push origin HEAD
```

- Commit message: conventional commits (`feat:`, `fix:`, `chore:`, etc.)
- If no changes, skip

---

## Branch Workflow

Create a new feature branch from base, preserving current changes.

- Base branch: argument provided by user, or `test` if not provided
- Branch naming: `feat/`, `fix/`, `chore/` based on changes
- Infer branch name from changes or ask user

### Instructions

**If there are uncommitted changes:**

```bash
but oplog snapshot -m "before branch switch" && git checkout <base> && git pull origin <base> && git checkout -b <branch-name> && but oplog restore
```

Note: `but oplog snapshot/restore` is the GitButler-safe alternative to `git stash` (which is banned in GitButler workspaces).

**If working tree is clean:**

```bash
git checkout <base> && git pull origin <base> && git checkout -b <branch-name>
```

---

## PR Fix Comments Workflow

Fetch PR review comments from AI code review assistants, analyze them, apply valid fixes, respond to comments explaining how they were addressed, then commit and push.

### Step 1: Get PR

If a PR number is provided as an argument, use that PR number. Otherwise, use the current branch's PR.

If no PR found, inform the user and exit.

### Step 2: Fetch Review Comments

There are two sources of review feedback:

1. **Inline review threads** — code-specific comments attached to file lines
2. **AI reviewer issue comments** — general PR comments from bots like `claude` or `sentry-io[bot]` (posted as `issuecomment-*`, not as inline threads)

#### 2.1 Check inline review threads

Fetch unresolved inline review threads:

```bash
bun run gh-tool pr threads --pr <pr_number> --unresolved-only
```

Each thread includes `threadId`, `commentId`, `path`, `line`, and `body`.

If unresolved comments exist, proceed directly to Step 3.

If the result is empty but you need to verify, re-run the command above to confirm.

#### 2.2 Check AI reviewer issue comments

**Even if inline threads are empty**, check for AI reviewer comments that contain actionable findings:

```bash
bun run gh-tool pr discussion-summary --pr <pr_number>
bun run gh-tool pr issue-comments-latest --pr <pr_number> --author claude --body-contains "Claude Code Review"
bun run gh-tool pr issue-comments-latest --pr <pr_number> --author sentry-io --body-contains "Sentry"
```

AI reviewers (Claude bot, Sentry Seer) post code review findings as general PR comments, not inline threads. These comments typically contain:

- Severity-tagged findings (Critical, Major, Minor)
- Specific file paths and line numbers
- Code suggestions and explanations

Parse the comment body to extract actionable items with file paths and line numbers.

#### 2.3 Determine if there is work to do

If **both** inline threads AND AI reviewer comments are empty or have no actionable findings, inform the user and exit.

If either source has actionable items, proceed to Step 3 with the combined list.

### Step 3: Analyze Each Comment

For each comment:

1. **Read the file** mentioned in the comment at the specific line
2. **Understand the suggestion** — what change is being requested?
3. **Evaluate validity**:
   - **Apply automatically**: Clear improvements (typos, style, obvious bugs, performance)
   - **Apply with judgment**: Suggestions that align with CLAUDE.md conventions
   - **Ask user**: Major architectural changes, unclear suggestions, or potentially breaking changes

### Step 4: Apply Fixes

For each valid suggestion:

1. Make the code change
2. Track what was changed and why

### Step 5: Respond to Comments and Resolve

**CRITICAL: Every thread MUST have a reply before being resolved.** This includes:

- Threads you're about to resolve
- Threads that are already resolved but missing replies
- Positive feedback comments (reply with acknowledgment like "Thanks for the feedback!")

#### 5.1 Get thread IDs and check for missing replies

First, fetch review threads to get thread IDs and resolution status:

```bash
bun run gh-tool pr threads --pr <pr_number>
```

Then check which threads have replies:

```bash
bun run gh-tool pr comments --pr <pr_number>
```

**Identify threads missing replies** — threads with only 1 comment (the original) need a reply added.

#### 5.2 Reply to EVERY thread (including already resolved ones)

For inline review comment replies:

```bash
bun run gh-tool pr reply --pr <pr_number> --comment-id <comment_id> --body "<response>"
```

For general PR comments:

```bash
bun run gh-tool pr comment --pr <pr_number> --body "<response>"
```

Response format:

- **If fixed**: "Addressed - [brief description of what was changed]"
- **If not applicable**: "Not applicable - [brief explanation why]"
- **If positive feedback**: "Thanks for the feedback!" or similar acknowledgment
- **If needs discussion**: "Question: [ask for clarification]"

#### 5.3 Resolve the thread

**Only after replying**, resolve the thread:

```bash
bun run gh-tool pr resolve --thread-id <thread_id>
```

**Do NOT resolve** threads where you asked a question or need discussion.

### Step 6: Run Validation

```bash
bun run check
```

Fix any new issues introduced by the changes.

### Step 7: Commit and Push

```bash
git add -A && git commit -m "fix(<scope>): <description of changes>" && git push origin HEAD
```

Generate a descriptive commit message based on what was actually changed (e.g., "fix(auth): correct token validation" or "fix(ui): improve error message display").

### Step 8: Monitor Checks and Iterate

After pushing, **automatically enter the monitoring loop**.

Inform the user: "Fixes pushed. Monitoring CI checks... (say 'stop' to exit the loop)"

#### 8.1 Wait for CI checks to complete

Use the built-in `--watch` flag to wait for checks (suppress verbose output):

```bash
bun run gh-tool pr checks --pr <pr_number> --watch --fail-fast > /dev/null 2>&1; echo $?
```

**Exit codes:**

- `0` — All checks passed
- `1` — One or more checks failed

The `--fail-fast` flag exits immediately when any check fails, allowing faster iteration.

#### 8.2 Handle check results

**If exit code is 1 (checks failed):**

1. Get failed check details:

   ```bash
   bun run gh-tool pr checks-failed --pr <pr_number>
   ```

2. For build/lint/test failures, fetch logs if available or analyze the error from the link
3. Fix the issues locally
4. Run `bun run check` to validate
5. Commit and push the fix:
   ```bash
   git add -A && git commit -m "fix: resolve CI check failures" && git push origin HEAD
   ```
6. **Go back to Step 8.1** to monitor again

**If exit code is 0 (all checks passed):**

1. Check for new review comments since last check:

   ```bash
   bun run gh-tool pr comments --pr <pr_number> --since "<last_check_timestamp>"
   bun run gh-tool pr issue-comments --pr <pr_number> --since "<last_check_timestamp>"
   ```

2. **If new comments exist:**
   - Inform user: "CI passed but X new review comments found. Processing..."
   - **Go back to Step 2** to process new comments

3. **If no new comments:**
   - Inform user: "All checks passed and no new comments. PR is ready for review! 🎉"
   - Exit the loop

#### 8.3 Loop exit conditions

Exit the monitoring loop when:

- All checks pass AND no new comments
- User says "stop" or requests to exit
- Maximum 5 iterations reached (then ask user to continue)

### Decision Guidelines

**Auto-apply (no user confirmation needed):**

- Typo fixes in comments or strings
- Import organization/cleanup
- Adding missing types
- Style fixes matching CLAUDE.md (kebab-case files, absolute imports, etc.)
- Performance improvements (Promise.all, prefetch patterns)
- Security fixes (removing hardcoded values, adding validation)

**Apply with judgment:**

- Refactoring suggestions that improve code clarity
- Adding error handling
- Improving variable/function names

**Ask user first:**

- Removing functionality
- Changing public API signatures
- Suggestions that contradict existing patterns
- Comments you don't understand or disagree with

---

## Sync Branches Workflow

Merge all environment branches so test, prod, and main point to the same commit.

### Step 1: Safety snapshot and teardown

```bash
but oplog snapshot -m "pre-sync safety"
but teardown
```

If teardown fails with "No active branches found", manually checkout test:

```bash
git checkout test
```

### Step 2: Checkout test and pull

```bash
git checkout test
git pull origin test
```

### Step 3: Merge prod and main into test

```bash
git fetch origin prod main
git merge origin/prod --no-edit
git merge origin/main --no-edit
```

If conflicts occur, resolve using `--theirs` (prefer incoming) and ask the user only if the conflict is ambiguous:

```bash
git checkout --theirs <conflicted-files>
git add <conflicted-files>
git commit --no-edit
```

### Step 4: Push test

```bash
git push origin test
```

### Step 5: Fast-forward prod from test

```bash
git fetch origin test prod main
git checkout prod
git pull origin prod
git merge origin/test --no-edit
git push origin prod
```

### Step 6: Fast-forward main from prod

```bash
git fetch origin test prod main
git checkout main
git pull origin main
git merge origin/prod --no-edit
git push origin main
```

### Step 7: Verify sync

```bash
git fetch origin test prod main
echo "test:  $(git rev-parse origin/test)"
echo "prod:  $(git rev-parse origin/prod)"
echo "main:  $(git rev-parse origin/main)"
```

All three must show the same SHA. If not, investigate and fix.

### Step 8: Return to GitButler workspace

```bash
git checkout test
but setup
```

### Constraints

- **ALWAYS snapshot before teardown** — protects uncommitted workspace files
- **ALWAYS use `--no-edit`** for merge commits — no interactive editors
- **ALWAYS set non-interactive env vars** before git commands (`GIT_MERGE_AUTOEDIT=no`, `GIT_PAGER=cat`, etc.)
- **NEVER force push** — all merges should be fast-forward or regular merge
- **NEVER skip verification** (Step 7) — confirm all SHAs match before returning to workspace

### Output

Report final state:

```
Branches synced to <SHA>
test:  <SHA>
prod:  <SHA>
main:  <SHA>
```
