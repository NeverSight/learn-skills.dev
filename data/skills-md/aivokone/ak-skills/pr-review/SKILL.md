---
name: pr-review
description: Use FIRST for any PR/code review work — checking feedback, reading CR comments, responding to reviewers, addressing review bot or human comments, or preparing commits on a PR. Collects feedback from ALL sources (conversation, inline, reviews) to prevent the common failure of missing inline feedback. Start with get-context.sh for state detection, then follow the Decision Tree. All operations through provided scripts — never raw git/gh commands.
---

# PR Review Workflow

Systematic workflow for checking, responding to, and reporting on PR feedback from any source — human reviewers, review bots (CodeRabbit, Gemini, Codex, Snyk, etc.), or AI agents.

**Requirements:** GitHub repository with [GitHub CLI (`gh`)](https://cli.github.com/) installed and authenticated.

**Key insight:** PR feedback arrives through three different channels (conversation comments, inline threads, review submissions). Missing any channel means missing feedback. This skill ensures all channels are checked systematically.

## Self-Contained Constraint

**ALL operations MUST go through the provided scripts.** Never run raw `git`, `gh`, `date`, or bash heredocs (`cat > file << 'EOF'`) when a script or agent tool covers the same operation.

| Instead of (prohibited) | Use |
|---|---|
| `git status`, `git branch`, `gh pr view`, `gh repo view` | `get-context.sh` |
| `git add`, `git commit`, `git push` | `commit-and-push.sh` |
| `git checkout -b`, `git switch -c` | `open-branch.sh` |
| `gh pr create` | `create-pr.sh` |
| `gh api repos/.../comments`, `gh pr view --json` | `check-pr-feedback.sh` |
| `gh api ... -f body=` (posting comments) | `post-fix-report.sh` or `reply-to-inline.sh` |
| `date -u +%Y-%m-%dT%H:%M:%SZ` | `get-context.sh` (outputs `timestamp:` field) |
| `cat > file.md << 'EOF'` (bash heredoc) | Agent's native Write tool to `.agents/scratch/`, then pass file path to script |

**Entry point:** Always start with `get-context.sh` to detect current state. Use its output to decide next steps via the Decision Tree below.

**File creation:** When a script accepts a file path (e.g., `create-pr.sh --body`, `post-fix-report.sh`), write the file to `.agents/scratch/` using the agent's native Write tool, then pass the path to the script. Never use bash heredocs to create temp files.

- **Directory:** `.agents/scratch/` — inside the repo, avoids out-of-tree write permission prompts
- **Setup:** Run `mkdir -p .agents/scratch` before the first write if it doesn't exist
- **Gitignore:** Ensure `.agents/` is in the project's `.gitignore`
- **Cleanup:** Scripts auto-delete scratch files after reading them, so the file won't exist on subsequent runs (no overwrite prompts)

**Acceptable raw commands:** Project-specific test/build commands (`npm test`, `pytest`, `make build`, etc.) are fine — these are not PR workflow operations.

## Entry Point Decision Tree

Run `get-context.sh` first. Based on its output, follow the matching path:

| `on_default` | `has_changes` | `pr_number` | Action sequence |
|---|---|---|---|
| `true` | `true` | empty | `open-branch.sh` → `commit-and-push.sh` → `create-pr.sh --invoke --title "..."` |
| `true` | `false` | empty | Ask user what to do (no changes to work with) |
| `false` | any | has number | `check-pr-feedback.sh` (existing PR — review cycle) |
| `false` | `true` | empty | `commit-and-push.sh` → `create-pr.sh --invoke --title "..."` |
| `false` | `false` | empty | `create-pr.sh --invoke --title "..."` (branch exists, already pushed) |

For loop mode, see the Loop Mode section — the decision tree gets you started, then the loop takes over.

## Quick Commands

**Script path resolution:** Before running any script, determine the correct base path. Check in this order:
1. `~/.claude/skills/pr-review/scripts/` — global install for Claude Code
2. Other global paths by preference of the agent

Use whichever path exists. Script paths below use the global form; substitute accordingly for your agent or install method.

### Get Context (Entry Point)

```bash
~/.claude/skills/pr-review/scripts/get-context.sh
```

Outputs key-value pairs: `branch`, `on_default`, `has_changes`, `change_summary`, `pr_number`, `pr_url`, `pr_state`, `timestamp`, `repo`. Use `timestamp` for `wait-for-reviews.sh --since`. Gracefully handles missing `gh` (empty PR/repo fields). Exits 1 only on detached HEAD or not in a git repo.

### Open Branch (Idempotent)

```bash
~/.claude/skills/pr-review/scripts/open-branch.sh [BRANCH_NAME]
```

If already on a non-main/master branch, prints branch name and exits. If on main/master, creates branch, switches, and pushes with `-u`. Default name: `review-loop-YYYYMMDD-HHMMSS`.

### Check All Feedback (CRITICAL - Use First)

```bash
~/.claude/skills/pr-review/scripts/check-pr-feedback.sh [PR_NUMBER]
```

Checks all three channels: conversation comments, inline comments, reviews.

If no PR number provided, detects current PR from branch.

### Reply to Inline Comment

```bash
~/.claude/skills/pr-review/scripts/reply-to-inline.sh <COMMENT_ID> "Your message"
~/.claude/skills/pr-review/scripts/reply-to-inline.sh <COMMENT_ID> .agents/scratch/reply.md
```

Replies in-thread to inline comments. Accepts message as inline text or a file path (auto-detects). Use file path when message contains `${...}` or other shell-sensitive syntax to avoid permission prompts. Uses `-F` flag (not `--raw-field`) which properly handles numeric ID conversion in `gh` CLI.

**Must be run from repository root** with an active PR branch.

**Important:** Always sign inline replies with your agent identity (e.g., `—Claude Sonnet 4.5`, `—GPT-4`, `—Custom Agent`) to distinguish agent responses from human responses in the GitHub UI.

### Invoke Review Agents

```bash
~/.claude/skills/pr-review/scripts/invoke-review-agents.sh [--agents SLUG,...] [--format-only] [PR_NUMBER]
```

Posts trigger comments to start agent reviews. Without `--agents`, invokes all known agents (Codex, Gemini, CodeRabbit). Use `--list` to see available agents. Use `--format-only` to print trigger text to stdout without posting (for embedding in PR body).

### Post Fix Report

```bash
~/.claude/skills/pr-review/scripts/post-fix-report.sh [PR_NUMBER] .agents/scratch/fix-report.md
```

Or via stdin:

```bash
echo "$body" | ~/.claude/skills/pr-review/scripts/post-fix-report.sh [PR_NUMBER]
```

### Create PR (Idempotent)

```bash
~/.claude/skills/pr-review/scripts/create-pr.sh --title "PR title" --body .agents/scratch/pr-body.md [--invoke]
```

Or body as text string or via stdin:

```bash
~/.claude/skills/pr-review/scripts/create-pr.sh --title "PR title" --body "Short description"
echo "Description" | ~/.claude/skills/pr-review/scripts/create-pr.sh --title "PR title"
```

`--body` auto-detects: if the value is a readable file, reads from it; otherwise treats as text. Idempotent: if a PR already exists, outputs its info. Refuses to run on `main`/`master`. Pushes branch if not yet pushed.

`--invoke` appends review agent trigger text to the PR body (via `invoke-review-agents.sh --format-only`), avoiding a separate trigger comment that causes double-invocations when auto-review is enabled.

Output prefixes (machine-parseable):
- `EXISTS: <url>` — PR already existed for this branch
- `CREATED: <url>` — new PR was created

### Commit and Push

```bash
~/.claude/skills/pr-review/scripts/commit-and-push.sh -m "fix: address review feedback"
```

Or message via stdin:

```bash
echo "fix: address review feedback" | ~/.claude/skills/pr-review/scripts/commit-and-push.sh
```

Stages all changes, commits, and pushes. Refuses to run on `main`/`master`. Never force-pushes. Outputs commit hash and branch.

### Wait for Reviews

```bash
~/.claude/skills/pr-review/scripts/wait-for-reviews.sh [PR_NUMBER] --since TIMESTAMP [--timeout 600] [--interval 30]
```

Polls all three feedback channels for new comments posted after `TIMESTAMP` by non-self users. Exits 0 when new feedback detected, exits 1 on timeout. Default: 10 min timeout, 30s interval.

### Check New Feedback (Differential)

```bash
~/.claude/skills/pr-review/scripts/check-new-feedback.sh [PR_NUMBER] --since TIMESTAMP
```

Like `check-pr-feedback.sh` but only shows feedback created after `TIMESTAMP`, excluding self-posted comments. Use in loop mode to distinguish new from already-addressed feedback. Ends with a summary line: `Summary: N conversation, M inline, K reviews`.

## Commit Workflows

Always use `commit-and-push.sh` for committing. It stages all changes, commits, pushes, and enforces branch safety (refuses `main`/`master`, never force-pushes).

```bash
~/.claude/skills/pr-review/scripts/commit-and-push.sh -m "<type>: <outcome>"
```

### Commit Type Conventions

Types: `feat`, `fix`, `refactor`, `docs`, `chore`, `test`

### Self-Check Before Commit

Before committing, verify:

1. **Test changes** — Run project-specific tests (`npm test`, `pytest`, etc.) if modifying working code
2. **Check latest feedback** — Run `check-pr-feedback.sh` to catch any new comments
3. **User confirmation** — If user is active in session, ask before committing
4. **Verify claims** — If Fix Report says "verified:", actually verify

## PR Creation

### Set Up Template (Once)

Create `.github/pull_request_template.md`:

```markdown
## Summary
-

## How to test
-

## Notes
- Review feedback may arrive in conversation comments, inline threads, or review submissions. Check all channels.
```

Or copy from `assets/pr_template.md`.

### Create PR

Fill Summary, How to test, and Notes sections.

## Code Review Coordination

### Feedback Channels

| Channel | Reviewer Type | Format |
|---------|---------------|--------|
| Conversation | AI agents, humans | Top-level comments |
| Inline | Review bots (CodeRabbit, Gemini, Codex, Snyk, etc.), humans | File/line threads |
| Reviews | Humans, some bots | Approve/Request Changes + optional body |

### Critical Rule: Check ALL Three Channels

```bash
~/.claude/skills/pr-review/scripts/check-pr-feedback.sh
```

**Why:** Different reviewers post in different channels. Missing any channel = missing feedback.

Three channels:

1. **Conversation comments** — general discussion, agent reviews
2. **Inline comments** — file/line-specific feedback from any reviewer
3. **Reviews** — approval state + optional body

### Critical Evaluation of Feedback

**Never trust review feedback at face value.** Before acting on any comment — whether from a human reviewer, review bot, or AI agent — critically evaluate it:

1. **Verify the claim** — Read the actual code being referenced. Does the reviewer's description match reality? Reviewers (especially bots) may misread context, reference wrong lines, or describe code that doesn't exist.
2. **Check for hallucinations** — Review bots may fabricate issues: non-existent variables, imagined type mismatches, phantom security vulnerabilities. Always confirm the issue exists before fixing it.
3. **Assess correctness** — Even if the issue is real, the suggested fix may be wrong. Evaluate whether the suggestion would break existing behavior, introduce regressions, or conflict with project conventions.
4. **Test before committing** — If a suggestion modifies working code, run tests before and after to confirm the change is actually an improvement.

If a review comment is incorrect, respond with a clear explanation of why rather than applying a bad fix. Use WONTFIX status with reasoning in the Fix Report.

### Responding to Inline Comments

1. **Critically evaluate the feedback** (see above), then address it in code if valid
2. **Reply inline** to each comment (sign with agent identity):

```bash
# Short messages — inline text:
~/.claude/skills/pr-review/scripts/reply-to-inline.sh <COMMENT_ID> "Fixed @ abc123. [details] —[Your Agent Name]"
# Messages with ${...} or shell-sensitive syntax — write to file first, pass path:
~/.claude/skills/pr-review/scripts/reply-to-inline.sh <COMMENT_ID> .agents/scratch/reply.md
```

3. **Include in Fix Report** (conversation comment) — the Fix Report summarizes all changes, but inline replies ensure each comment gets a direct acknowledgment

## Invoking Review Agents

Run `invoke-review-agents.sh` when `check-pr-feedback.sh` returns empty output from **all three channels** — no feedback means no agents have reviewed yet.

```bash
# No feedback on the PR? Invoke all agents:
~/.claude/skills/pr-review/scripts/invoke-review-agents.sh

# User mentioned specific agents (e.g., "ask Gemini and Codex to review"):
~/.claude/skills/pr-review/scripts/invoke-review-agents.sh --agents gemini,codex
```

**Agent selection from prompt:** If the user's prompt names specific agents (e.g., "have Codex review this"), use `--agents` with the matching slug(s). Otherwise invoke all.

**Embedding in PR body:** When creating a new PR with `create-pr.sh --invoke`, trigger text is appended to the PR body automatically (via `--format-only`). This avoids a separate trigger comment that would cause double-invocations when auto-review is enabled. Only use `invoke-review-agents.sh` directly when the PR already exists.

**After invoking:** Inform the user that trigger comments were posted and suggest running `check-pr-feedback.sh` again once agents have had time to respond (typically a few minutes).

**See `references/review-agents.md` for the full agent registry and instructions for adding new agents.**

## Fix Reporting

After addressing feedback, **always** post ONE conversation comment (Fix Report). This is separate from requesting re-review — the Fix Report documents what was done, even if no re-review is needed.

Write the report with the agent's Write tool (e.g., to `.agents/scratch/fix-report.md`), then post it:

```bash
~/.claude/skills/pr-review/scripts/post-fix-report.sh .agents/scratch/fix-report.md
```

Fix Report format:

```markdown
### Fix Report

- [file.ext:L10 Symbol]: FIXED @ abc123 — verified: `npm test` passes
- [file.ext:L42 fn]: WONTFIX — reason: intentional per AGENTS.md
- [file.ext:L100 class]: DEFERRED — tracking: #123
- [file.ext:L200 method]: QUESTION — Should this handle X?
```

Optionally, if re-review is needed, add `@reviewer-username please re-review.` at the end of the body.

### Fix Statuses

| Status | Required Info |
|--------|---------------|
| FIXED | Commit hash + verification command/result |
| WONTFIX | Reason (cite docs if applicable) |
| DEFERRED | Issue/ticket link |
| QUESTION | Specific question to unblock |

**See `references/fix-report-examples.md` for real-world examples.**

Use `assets/fix-report-template.md` as starting point.

## Review Format (For Agent-Reviewers)

Agent-reviewers MUST post ONE top-level conversation comment:

```markdown
### Review - Actionable Findings

**Blocking**
- path/file.ext:L10-L15 (Symbol): Issue → Fix → Verify: `command`

**Optional**
- path/file.ext:L100 (class): Improvement → Fix
```

Rules:

- Blocking MUST include verification (runnable command or objective check)
- Use `file:line` + symbol anchor
- Actionable, not prose
- Group by severity

**Do NOT:**

- Create inline file/line comments
- Submit GitHub review submissions
- Post multiple separate comments

**Why:** Inline comments harder to retrieve. Conversation comments deterministic.

## Re-Review Loop

After Fix Report:

1. **Request re-review**: `@reviewer please re-review. See Fix Report.`
2. **Tag ALL reviewers** who provided feedback
3. **If QUESTION items**: Wait for clarification
4. **If blocking feedback was only provided inline**: Mention it was addressed, optionally ask to mirror to conversation for future determinism

## Loop Mode

Activate when the user's prompt requests a review loop, review cycle, or similar — in any words — meaning: run the full review-fix-review cycle autonomously until no new feedback remains.

**Default max rounds: 5.** Override with user instruction if needed.

**Loop workflow:**

0. **Branch** — `open-branch.sh` (idempotent — creates branch if on main/master)
1. **PR** — `create-pr.sh --invoke --title "..." --body <path>` — write body with agent Write tool, pass path. Capture output prefix (`CREATED:` / `EXISTS:`)
2. **Invoke** — Round 1: if step 1 output `CREATED:`, skip (triggers in PR body). If `EXISTS:`, run `invoke-review-agents.sh`. Rounds 2+: agents triggered by @-mentions in previous Fix Report footer (no separate invoke step)
3. **Wait** — `wait-for-reviews.sh --since <timestamp>` — use `timestamp` from `get-context.sh` (run after last commit, or after step 1 for round 1). Polls until new feedback or timeout
4. **Check** — `check-pr-feedback.sh` (ALL feedback, all channels)
5. **Process** — compare all feedback against previous Fix Reports. Address only: (a) items not covered in any Fix Report, (b) items with new follow-up comments after the last Fix Report. Critically evaluate each item before fixing
6. **Fix code, commit** — `commit-and-push.sh -m "fix: address review feedback round N"`
7. **Get timestamp** — `get-context.sh` (capture `timestamp` for next wait step)
8. **Reply inline** — `reply-to-inline.sh` for each addressed inline comment; sign with agent identity; tag the reviewer's `@github-user`
9. **Fix Report** — write report with agent Write tool, then `post-fix-report.sh <PR> <path>`
   - Before max: footer has @-mentions + `@coderabbitai review` on its own line
   - At max: footer has max-reached message (see below)
10. **Loop** — if `ROUND < MAX_ROUNDS`, go to step 3

**Why full check instead of differential:** Using `check-new-feedback.sh --since` in the check step risks missing feedback that arrives during the fix phase (e.g., Gemini posts while agent is fixing Codex's comments). The full check + Fix Report comparison approach is gap-free.

**Termination conditions** (any):
- Step 5 finds nothing new to process (all feedback already addressed in Fix Reports)
- `wait-for-reviews.sh` times out (no new feedback after invocation)
- A reviewer posts an Approve review
- User explicitly stops the loop
- Max rounds reached

**Final round Fix Report footer:**

```markdown
Max review rounds (N) reached. Remaining items addressed above. Manual re-review recommended.
```

**Inline reply tagging:** When replying to a bot/agent inline comment, include the reviewer's GitHub username in the reply (e.g., `—Claude Sonnet 4.6 | addressed @gemini-code-assist feedback`).

**See `references/fix-report-examples.md` Examples 7–8 for loop-mode Fix Reports.**

## Multi-Reviewer Patterns

### Duplicate Feedback

If multiple reviewers flag the same issue:

```markdown
- [file.php:L42 (ALL flagged)]: FIXED @ abc123 — verified: `npm test` passes
  - Gemini: "use const"
  - Codex: "prefer immutable"
  - Claude: "const prevents reassignment"
```

### Conflicting Suggestions

```markdown
- [file.php:L100]: QUESTION — Gemini suggests pattern A, Codex suggests pattern B. Which aligns with project conventions? See AGENTS.md.
```

### Finding Comments by Reviewer

Use `check-pr-feedback.sh` — its output already includes `[user.login]` for every comment across all three channels. Filter the output for the reviewer you need:

```bash
~/.claude/skills/pr-review/scripts/check-pr-feedback.sh | grep "coderabbitai"
```

## Troubleshooting

**"Can't find review comments"**
→ Check all three channels. Use `~/.claude/skills/pr-review/scripts/check-pr-feedback.sh`, not just `gh pr view`.

**"Reviewer posted inline, should I reply inline?"**
→ Yes, always. Reply inline with a brief ack so the comment can be resolved in GitHub UI. Also include in Fix Report.

**"Multiple reviewers flagged same issue"**
→ Fix once, report once (note all sources), tag all reviewers.

**"Conflicting suggestions"**
→ Mark QUESTION, check project docs, cite specific suggestions.

**"Script can't detect PR"**
→ Run from repository root. Must be on branch with open PR.

**"Reply script fails with HTTP 422"**
→ Use `-F in_reply_to=ID` not `--raw-field`. The `-F` flag works correctly with `gh` CLI for numeric IDs.

**"Review suggestion broke working code"**
→ Never trust suggestions blindly. Verify the issue exists, evaluate the fix, and test before committing. Review bots frequently hallucinate problems or suggest incorrect fixes.

**"No feedback on PR — all three channels empty"**
→ Agents haven't reviewed yet. Run `~/.claude/skills/pr-review/scripts/invoke-review-agents.sh` to trigger them, then wait and re-check.

**"Committed before checking latest feedback"**
→ Run feedback check script immediately before declaring PR "ready" or "complete."

## Summary

**Key principles:**

1. Always check all three channels (conversation + inline + reviews)
2. **Critically evaluate every comment** — reviewers can be wrong, misread context, or hallucinate issues
3. Any reviewer (human, bot, agent) can post in any channel
4. One Fix Report per round
5. Tag all reviewers explicitly
6. If no feedback exists, invoke agents first — never declare a PR complete without at least one review round

**Most common mistakes:**
❌ Only checking conversation or `gh pr view`
✅ Always run `~/.claude/skills/pr-review/scripts/check-pr-feedback.sh`

❌ Blindly applying review suggestions without verifying the issue exists
✅ Read the actual code, confirm the problem, test the fix
