---
name: pr-comments
description: Triages and resolves PR review comments from humans and bots. Fetches unresolved threads, deduplicates bot findings, classifies by severity, writes a fix plan for approval, then fixes real issues and resolves noise. Use when asked to fix PR comments, resolve review feedback, triage review threads, handle bot comments, or address PR review findings.
---

# PR Comment Triage

Triage and resolve PR review comments from humans and bots in a structured four-phase workflow.

## Scope

- Use for: unresolved review threads on open PRs, both human and bot comments
- Skip: closed PRs, PRs with no unresolved threads, draft PRs unless explicitly requested

## Reference Files

| File | Read When |
|------|-----------|
| `references/github-api.md` | Default: GraphQL queries for fetching, replying, and resolving threads |
| `references/bot-patterns.md` | Phase 2: bot detection, severity parsing, deduplication, false positive rules |
| `references/fix-plan-template.md` | Phase 3: generating the fix plan document |

## Workflow

Copy this checklist to track progress:

```
PR comment triage progress:
- [ ] Phase 1: Fetch unresolved review threads, reviews, and comments
- [ ] Phase 2: Triage and classify all items
- [ ] Phase 3: Write fix plan and get approval
- [ ] Phase 4: Execute fixes and resolve threads
```

### Phase 1: Fetch

Load `references/github-api.md` for query templates.

1. **Identify the PR** — auto-detect from current branch (`gh pr view --json number`) or accept an explicit PR number argument
2. **Extract owner/repo** — `gh repo view --json owner,name`
3. **Fetch all review threads** — use the GraphQL `reviewThreads` query with pagination. Collect every thread, then filter to `isResolved == false`
4. **Fetch PR reviews** — use the REST reviews endpoint. Collect all reviews with their state, body, and author. Pay attention to `CHANGES_REQUESTED` reviews with body text — these contain the reviewer's summary of what needs to change
5. **Fetch issue-level comments** — use the REST endpoint for all PR conversation comments. Do not filter by author — bot comments from `github-actions[bot]` may contain actionable findings (DangerJS warnings, schema compatibility checks)
6. **Early exit** — if zero unresolved threads, zero actionable reviews, and zero actionable issue comments, report "No unresolved review items found" and stop

Output: three lists — unresolved threads, reviews with content, and issue-level comments.

### Phase 2: Triage

Load `references/bot-patterns.md` for detection and parsing rules.

For each item across all three sources:

1. **Identify author type** — human or bot. For bots, classify by **content first, then username**:
   - `github-actions[bot]` is a shared identity — match on DangerJS markers, schema compatibility tables, or other patterns to determine if actionable
   - `devin-ai-integration[bot]` is an active reviewer — but "No Issues Found" reviews are noise
   - `linear[bot]` is always noise (project linkback)
2. **Skip noise** — auto-classify noise items (linear linkbacks, vercel deployments, Devin "no issues" reviews, changeset releases, event-lib triggers)
3. **Parse severity** — extract from bot-specific format (emoji, SVG, HTML tables). Human comments: default to Major for `CHANGES_REQUESTED`, Minor for `APPROVED` + question
4. **Deduplicate** — group inline comments on the same file within a 3-line range. Keep the highest-severity, most-actionable comment. Mark others as `ignore-duplicate`
5. **Classify** each remaining item:
   - **Category:** bug, security, performance, style, correctness, docs, test-coverage
   - **Severity:** critical, major, minor, nitpick
   - **Confidence:** high (human or multi-bot), medium (single bot, clear issue), low (single bot, likely false positive)
   - **Disposition:** fix or ignore (with reason)
   - **Source type:** thread (resolvable), conversation (reply-only)
6. **Flag ignore candidates** with specific reasoning:
   - Pre-existing code not changed in this PR
   - Bot flagged .md, config, lock, or migration files (no security implications)
   - Contradicts project CLAUDE.md/AGENTS.md conventions
   - Outdated thread where code has changed substantially
   - Noise bot boilerplate or badge injection

**Human comments are never auto-ignored.** Always classify as fix unless clearly already resolved or the reviewer explicitly marked it as optional ("up to you", "but not blocking").

### Phase 3: Plan

Load `references/fix-plan-template.md` for the output template.

1. **Create plan file** — write to `.claude/scratchpad/pr-{N}-review-plan.md` (create directory if needed)
2. **Issues to Fix** — ordered by severity (critical first), each with thread ID, file:line, author, category, finding, fix approach, and commit group label
3. **Conversation Items** — issue-level comments and review bodies that need fixes but have no thread ID. These get a reply but no resolve mutation
4. **Ignored** — each with thread ID or comment ID, author, reason, and the brief reply to post when resolving
5. **Summary table** — disposition-by-severity matrix for quick scanning
6. **Present to user** — print a summary showing counts (N to fix, K conversation items, M to ignore) and ask for approval

**Stop here. Do not proceed to Phase 4 until the user reviews and approves the plan.**

The user may edit the plan — move items between fix/conversation/ignore, change priorities, add notes. Re-read the plan file before executing.

### Phase 4: Execute

After user approval, re-read `.claude/scratchpad/pr-{N}-review-plan.md` in case it was edited.

**4a. Resolve ignored threads:**

For each ignored item that has a thread ID:
1. Post a brief reply explaining the decision
2. Resolve the thread via GraphQL mutation

Use concise, specific reasons:
- "Duplicate of thread addressing the same finding — resolving."
- "Contradicts project convention (see CLAUDE.md) — resolving."
- "Outdated thread — code has been refactored. Resolving."
- "CI notification — not actionable. Resolving."

For ignored noise without a thread ID (issue-level bot comments), do nothing — no reply needed.

**4b. Fix real issues:**

Group fixes by commit group label from the plan. For each group:
- If fixes touch independent files, launch parallel subagents (one per file group)
- If fixes touch the same file or overlapping lines, execute sequentially
- Each subagent reads the file, applies the fix, and verifies correctness

Subagent prompt template:
```
Fix the following PR review issue(s) on branch {BRANCH}:

Issue: {finding}
File: {path}:{line}
Fix approach: {fix_approach}

Read the file, understand the surrounding context, and make the fix.
After fixing, verify the change is correct.
Do NOT touch unrelated code.
```

**4c. Commit and push:**

- Run project lint/test commands if available
- One commit per logical fix group, message format: `fix({scope}): {description}`
- Push the branch

**4d. Resolve and reply:**

- Resolved threads: post reply ("Fixed in latest push.") then resolve via GraphQL
- Conversation items: post reply acknowledging the fix
- Issue-level comments have no resolve mechanism — the reply is the acknowledgment

**4e. Verify:**

- Re-fetch threads from GitHub (fresh API call) to confirm zero unresolved remain
- Check CI status with `gh pr checks`
- Report results to the user

## Anti-patterns

- Resolving threads without posting a reply — reviewers need to see the reasoning
- Auto-ignoring human comments — always classify for user review
- Fixing items the plan marked as ignore without approval
- One commit per individual comment — group related fixes by commit group label
- Pushing before verifying lint/test pass locally
- Skipping Phase 3 approval — the fix plan is the quality gate
- Classifying `github-actions[bot]` as always noise — it is a shared identity used by DangerJS, schema checkers, and other active tools. Classify by content.
- Filtering issue-level comments to humans only — bot comments from DangerJS and schema checkers are actionable

## Related skills

- `review-pr` for reviewing PRs and posting comments (outbound — complementary to this skill)
- `plan-feature` for complex feature planning when a PR comment requires significant rework
