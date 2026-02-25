---
name: coderabbit-resolver
description: Automates the full CodeRabbit PR review cycle — extracts review comments, fixes code, commits, pushes, monitors CI, resolves threads, and repeats until all checks pass and threads are resolved, then merges and cleans up branches. Supports --bulk to process all open PRs sequentially. Use when asked to fix CodeRabbit reviews, resolve PR comments, or handle the complete review-fix-merge workflow.
argument-hint: [pr-number|--bulk]
---

<essential_principles>
## How This Skill Works

Automates the iterative CodeRabbit review loop on a GitHub PR until all review comments are resolved and CI is green, then merges and cleans up.

### Principle 1: GraphQL-Only Thread Resolution

GitHub has NO REST API for resolving review threads. You MUST use the GraphQL `resolveReviewThread` mutation with `PRRT_`-prefixed thread IDs. The mutation is idempotent — safe to call on already-resolved threads.

### Principle 2: Iterative Loop Until Clean

The workflow runs in a loop:
1. Extract unresolved CodeRabbit review comments
2. Fix code issues OR resolve already-fixed threads
3. Commit → Push → Wait for CI + CodeRabbit re-review
4. Repeat until: zero unresolved threads AND all CI checks pass

### Principle 3: Validation Before Every Push

Run `pnpm validate` (or project-specific validation) before every commit. Never push broken code.

### Principle 4: Safe Merge and Cleanup

Only merge when ALL conditions are met: CI green, no unresolved threads, CodeRabbit check complete. After merge, delete remote branch and prune local.

### Principle 5: Rate Limit Handling

CodeRabbit may hit API rate limits and post a comment instead of reviewing. When detected, the workflow automatically waits for the rate limit to expire (+ 30s buffer), then posts `@coderabbitai full review` to trigger a complete re-review. Max 3 rate limit retries per PR to prevent infinite loops.
</essential_principles>

<intake>
This skill accepts a PR number or `--bulk` flag as argument. Usage:

```
/coderabbit-resolver <PR_NUMBER>       # Process single PR
/coderabbit-resolver 17                # Process PR #17
/coderabbit-resolver --bulk            # Process ALL open PRs (oldest first)
```

If no PR number provided (and no `--bulk`), detect from current branch:
```bash
gh pr view --json number -q .number
```

**After obtaining the PR number, read and follow `workflows/review-loop.md`.**
**If `--bulk` is specified, read and follow `workflows/bulk-loop.md`.**
</intake>

<routing>
| Input | Action |
|-------|--------|
| PR number provided | Read `workflows/review-loop.md` and execute with that PR |
| No PR number | Auto-detect from current branch, then read `workflows/review-loop.md` |
| `--bulk` flag | Read `workflows/bulk-loop.md` and process all open PRs |

**After reading the workflow, follow it exactly.**
</routing>

<reference_index>
## References

All in `references/`:

| File | Content |
|------|---------|
| github-graphql-api.md | GraphQL queries/mutations for thread resolution, CI status checks |
| coderabbit-commands.md | CodeRabbit bot commands and behavior reference |
</reference_index>

<workflows_index>
## Workflows

All in `workflows/`:

| Workflow | Purpose |
|----------|---------|
| review-loop.md | The main iterative review-fix-resolve-merge loop (single PR) |
| bulk-loop.md | Process all open PRs sequentially (oldest first), merging each |
</workflows_index>

<scripts_index>
## Scripts

| Script | Purpose |
|--------|---------|
| resolve-threads.sh | Resolve all unresolved CodeRabbit threads on a PR |
| check-ci-status.sh | Check CI and CodeRabbit review status for a PR |
| wait-for-ratelimit.sh | Detect CodeRabbit rate limit, wait for expiry, trigger full review |
</scripts_index>

<success_criteria>
A successful coderabbit-resolver invocation (single PR):
- [ ] All CodeRabbit review threads resolved (zero unresolved)
- [ ] All CI checks passing (green), including fixes for unrelated CI failures
- [ ] CodeRabbit review status is complete
- [ ] PR merged successfully
- [ ] Remote branch deleted
- [ ] Local branch cleaned up (switched to main, pruned)

A successful `--bulk` invocation:
- [ ] All open PRs processed (oldest first)
- [ ] Each PR either MERGED or SKIPPED (with reason)
- [ ] Summary report generated with results table
</success_criteria>
