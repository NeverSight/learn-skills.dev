---
name: done
description: Wrap up the current session — commits, pushes, creates PR, updates Linear. Detects worktree vs main branch context automatically.
user-invocable: true
allowed-tools: Bash(git:*) Bash(gh:*) Bash(entire:*) Bash(cat:*) Bash(python3:*) mcp__linear-server__create_comment mcp__linear-server__update_issue mcp__linear-server__create_issue mcp__claude_ai_Linear__create_comment mcp__claude_ai_Linear__update_issue mcp__claude_ai_Linear__create_issue mcp__claude_ai_Supabase__merge_branch mcp__claude_ai_Supabase__delete_branch
---

# Session Wrap-up

## Step 1: Detect Context

Run ALL of these commands:

```bash
echo "=== CONTEXT ==="
echo "Branch: $(git branch --show-current)"
echo "Is worktree: $([ -f .git ] && echo YES || echo NO)"
echo "Has session-state: $([ -f .claude/session-state.json ] && echo YES || echo NO)"
[ -f .claude/session-state.json ] && cat .claude/session-state.json
echo "=== END CONTEXT ==="
```

Read `.claude/session-config.json` if it exists, otherwise use these defaults:
- linear.team: "Engineering"
- linear.labels: ["claude-session"]
- linear.doneState: "done"
- github.baseBranch: "main"
- supabase.branchingEnabled: false
- entire.enabled: false

**Now decide:**

- If "Is worktree: YES" AND session-state.json contains `linearIssueId` → go to **WORKTREE FLOW** below
- Otherwise → go to **MAIN FLOW** below

---

## WORKTREE FLOW

You MUST complete ALL 9 steps below. Do NOT stop early. Do NOT skip any step.

### W1: Gather Changes

```bash
git diff main --stat
git log main..HEAD --oneline
```

If entire is enabled in config:
```bash
entire explain --short 2>&1 || true
```

Write a concise summary of what changed.

### W2: Note Supabase Branch

Read `supabaseBranchId` and `supabaseBranchProjectRef` from `.claude/session-state.json`.

If a Supabase branch exists, set `hasSupabaseBranch = true`.

### W3: Commit Uncommitted Work

```bash
git status --porcelain
```

If there are uncommitted changes, ask the user whether to commit. If yes, stage all and commit with a descriptive message.

### W4: Push Branch

```bash
git push -u origin $(git branch --show-current)
```

### W5: Create Pull Request

THIS STEP IS MANDATORY. You MUST create a PR.

Build the PR body with your summary.

If `hasSupabaseBranch`:
Add to the PR body:

```
## Supabase Branch

This PR has an associated Supabase preview branch.
- Branch ID: `<supabaseBranchId>`
- Project Ref: `<supabaseBranchProjectRef>`

**After merging this PR**, merge the Supabase branch:
Use `mcp__claude_ai_Supabase__merge_branch` with branch_id: `<supabaseBranchId>`
```

Now create the PR:

```bash
gh pr create --title "<linearIssueIdentifier>: <short-title>" --body "<body>" --base main
```

Save the PR URL from the output.

### W6: Merge PR and Supabase Branch

THIS STEP IS MANDATORY. You MUST merge the PR.

Merge the PR:
```bash
gh pr merge <pr-number> --merge
```

If `hasSupabaseBranch` (from W2), merge the Supabase branch to production:

Use `mcp__claude_ai_Supabase__merge_branch` with:
- branch_id: the `supabaseBranchId` from session-state

If merge fails (e.g., migrations failed status), delete the branch instead:
Use `mcp__claude_ai_Supabase__delete_branch` with:
- branch_id: the `supabaseBranchId`

Note: The GitHub integration will apply migration files from main automatically.

### W7: Update Linear

Extract `linearIssueId` from `.claude/session-state.json`.

First, add a comment with the PR URL and summary:

Use `mcp__linear-server__create_comment` (or `mcp__claude_ai_Linear__create_comment`):
- issueId: the linearIssueId
- body: include PR URL and summary

Then, update the issue state to done:

Use `mcp__linear-server__update_issue` (or `mcp__claude_ai_Linear__update_issue`):
- id: the linearIssueId
- state: config.linear.doneState (default: "done")

### W8: Mark for Cleanup and Confirm

Update the main repo's worktree session file. The `mainRepoPath` and `linearBranchName` are in session-state.json. The file is at:
`<mainRepoPath>/.claude/worktree-sessions/<linearBranchName with / replaced by ->.json`

```bash
python3 -c "
import json
path = '<mainRepoPath>/.claude/worktree-sessions/<sanitized-branch>.json'
d = json.load(open(path))
d['status'] = 'done'
json.dump(d, open(path, 'w'), indent=2)
"
```

Also update local `.claude/session-state.json` status to "done".

### W9: Confirm

Print:
- PR merged: <PR URL>
- Linear issue: <identifier> → Done
- If `hasSupabaseBranch`: "Supabase branch merged to production"
- "Close this terminal tab."

---

## MAIN FLOW

For sessions on the main branch without a worktree.

### M1: Gather Context

```bash
git branch --show-current
```

If entire is enabled:
```bash
entire status 2>&1
```

Extract session ID from output, then:
```bash
entire explain --session <session_id> --short 2>&1
```

Check `.claude/session-state.json` for a linked Linear issue.

### M2: Build Summary

Based on conversation history, write a concise summary:
- **Summary** — what was accomplished
- **Files Changed** — only if files were changed
- **Follow-ups** — only if there are open items

### M3: Push to Linear

If session-state has `linearIssueId`:
- Add a comment to the existing issue

If no linked issue:
- Create a new issue with team from config, labels from config, and the summary as description

### M4: Save State and Confirm

Write `.claude/session-state.json` with the issue details and current timestamp.

Print the Linear issue identifier and a one-line summary.
