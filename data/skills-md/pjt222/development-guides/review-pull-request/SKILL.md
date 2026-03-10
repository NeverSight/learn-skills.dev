---
name: review-pull-request
description: >
  Review a pull request end-to-end using GitHub CLI. Covers diff analysis,
  commit history review, CI/CD check verification, severity-leveled feedback
  (blocking/suggestion/nit/praise), and gh pr review submission. Use when a
  pull request is assigned for review, performing a self-review before
  requesting others' input, conducting a second review after feedback is
  addressed, or auditing a merged PR for post-merge quality assessment.
license: MIT
allowed-tools: Read Grep Glob Bash WebFetch
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: review
  complexity: intermediate
  language: multi
  tags: review, pull-request, github, code-review, gh-cli, feedback, pr
---

# Review Pull Request

Review a GitHub pull request end-to-end — from understanding the change through submitting structured feedback. Uses `gh` CLI for all GitHub interactions and produces severity-leveled review comments.

## When to Use

- A pull request is ready for review and assigned to you
- Performing a second review after the author addresses feedback
- Reviewing your own PR before requesting others' review (self-review)
- Auditing a merged PR for post-merge quality assessment
- When you want a structured review process rather than ad-hoc scanning

## Inputs

- **Required**: PR identifier (number, URL, or `owner/repo#number`)
- **Optional**: Review focus (security, performance, correctness, style)
- **Optional**: Codebase familiarity level (familiar, somewhat, unfamiliar)
- **Optional**: Time budget for the review (quick scan, standard, thorough)

## Procedure

### Step 1: Understand the Context

Read the PR description and understand what the change is trying to accomplish.

1. Fetch PR metadata:
   ```bash
   gh pr view <number> --json title,body,author,baseRefName,headRefName,labels,additions,deletions,changedFiles,reviewDecision
   ```
2. Read the PR title and description:
   - What problem does this PR solve?
   - What approach did the author take?
   - Are there any specific areas the author wants reviewed?
3. Check the PR size and assess time required:

```
PR Size Guide:
+--------+-----------+---------+-------------------------------------+
| Size   | Files     | Lines   | Review Approach                     |
+--------+-----------+---------+-------------------------------------+
| Small  | 1-5       | <100    | Read every line, quick review       |
| Medium | 5-15      | 100-500 | Focus on logic changes, skim config |
| Large  | 15-30     | 500-    | Review by commit, focus on critical  |
|        |           | 1000    | files, flag if should be split       |
| XL     | 30+       | 1000+   | Flag for splitting. Review only the  |
|        |           |         | most critical files.                 |
+--------+-----------+---------+-------------------------------------+
```

4. Review the commit history:
   ```bash
   gh pr view <number> --json commits --jq '.commits[].messageHeadline'
   ```
   - Are commits logical and well-structured?
   - Does the history tell a story (each commit a coherent step)?
5. Check CI/CD status:
   ```bash
   gh pr checks <number>
   ```
   - Are all checks passing?
   - If checks are failing, note which ones — this affects the review

**Expected:** A clear understanding of what the PR does, why it exists, how big it is, and whether CI is green. This context shapes the review approach.

**On failure:** If the PR description is empty or unclear, note this as the first piece of feedback. A PR without context is a review antipattern. If `gh` commands fail, verify you're authenticated (`gh auth status`) and have access to the repository.

### Step 2: Analyze the Diff

Read the actual code changes systematically.

1. Fetch the full diff:
   ```bash
   gh pr diff <number>
   ```
2. For **small/medium PRs**, read the entire diff sequentially
3. For **large PRs**, review by commit:
   ```bash
   gh pr diff <number> --patch  # full patch format
   ```
4. For each changed file, evaluate:
   - **Correctness**: Does the code do what the PR says it does?
   - **Edge cases**: Are boundary conditions handled?
   - **Error handling**: Are errors caught and handled appropriately?
   - **Security**: Any injection, auth, or data exposure risks?
   - **Performance**: Any obvious O(n^2) loops, missing indexes, or memory issues?
   - **Naming**: Are new variables/functions/classes named clearly?
   - **Tests**: Are new behaviors covered by tests?
5. Take notes as you read, classifying each observation by severity

**Expected:** A set of observations covering correctness, security, performance, and quality for every meaningful change in the diff. Each observation has a severity level.

**On failure:** If the diff is too large to review effectively, flag it: "This PR changes {N} files and {M} lines. I recommend splitting it into smaller PRs for more effective review." Still review the highest-risk files.

### Step 3: Classify Feedback

Organize observations into severity levels.

1. Classify each observation:

```
Feedback Severity Levels:
+-----------+------+----------------------------------------------------+
| Level     | Icon | Description                                        |
+-----------+------+----------------------------------------------------+
| Blocking  | [B]  | Must fix before merge. Bugs, security issues,      |
|           |      | data loss risks, broken functionality.             |
| Suggest   | [S]  | Should fix, but won't block merge. Better           |
|           |      | approaches, missing edge cases, style issues that   |
|           |      | affect maintainability.                            |
| Nit       | [N]  | Optional improvement. Style preferences, minor      |
|           |      | naming suggestions, formatting.                    |
| Praise    | [P]  | Good work worth calling out. Clever solutions,      |
|           |      | thorough testing, clean abstractions.              |
+-----------+------+----------------------------------------------------+
```

2. For each Blocking item, explain:
   - What's wrong (the specific issue)
   - Why it matters (the impact)
   - How to fix it (a concrete suggestion)
3. For each Suggest item, explain the alternative and why it's better
4. Keep Nits brief — one sentence is enough
5. Include at least one Praise if anything positive stands out

**Expected:** A sorted list of feedback items with clear severity levels. Blocking items have fix suggestions. The ratio should generally be: few Blocking, some Suggest, minimal Nit, at least one Praise.

**On failure:** If everything seems blocking, the PR may need to be reworked rather than patched. Consider requesting changes at the PR level rather than line-by-line comments. If nothing seems wrong, say so — "LGTM" is valid feedback when the code is good.

### Step 4: Write Review Comments

Compose the review with structured, actionable feedback.

1. Write the **review summary** (top-level comment):
   - One sentence: what the PR does (confirm understanding)
   - Overall assessment: approve, request changes, or comment
   - Key items: list Blocking issues (if any) and top Suggest items
   - Praise: call out good work
2. Write **inline comments** for specific code locations:
   ```bash
   # Post inline comments via gh API
   gh api repos/{owner}/{repo}/pulls/{number}/comments \
     -f body="[B] This SQL query is vulnerable to injection. Use parameterized queries instead.\n\n\`\`\`suggestion\ndb.query('SELECT * FROM users WHERE id = $1', [userId])\n\`\`\`" \
     -f commit_id="<sha>" \
     -f path="src/users.js" \
     -F line=42 \
     -f side="RIGHT"
   ```
3. Format feedback consistently:
   - Start each comment with the severity tag: `[B]`, `[S]`, `[N]`, or `[P]`
   - Use GitHub suggestion blocks for concrete fixes
   - Link to documentation for style/pattern suggestions
4. Submit the review:
   ```bash
   # Approve
   gh pr review <number> --approve --body "Review summary here"

   # Request changes (when blocking issues exist)
   gh pr review <number> --request-changes --body "Review summary here"

   # Comment only (when unsure or providing FYI feedback)
   gh pr review <number> --comment --body "Review summary here"
   ```

**Expected:** A submitted review with clear, actionable feedback. The author knows exactly what to fix (Blocking), what to consider (Suggest), and what went well (Praise).

**On failure:** If `gh pr review` fails, check permissions. You need write access to the repo or to be a requested reviewer. If inline comments fail, fall back to putting all feedback in the review body with file:line references.

### Step 5: Follow Up

Track the review resolution.

1. After the author responds or pushes updates:
   ```bash
   gh pr view <number> --json reviewDecision,reviews
   ```
2. Re-review only the changes that address your feedback:
   ```bash
   gh pr diff <number>  # check new commits
   ```
3. Verify Blocking items are resolved before approving
4. Resolve comment threads as issues are addressed
5. Approve when all Blocking items are fixed:
   ```bash
   gh pr review <number> --approve --body "All blocking issues resolved. LGTM."
   ```

**Expected:** Blocking issues verified as fixed. Review conversation resolved. PR approved or further changes requested with specific remaining items.

**On failure:** If the author disagrees with feedback, discuss in the PR thread. Focus on impact (why it matters) rather than authority. If disagreement persists on non-blocking items, yield gracefully — the author owns the code.

## Validation Checklist

- [ ] PR context understood (purpose, size, CI status)
- [ ] All changed files reviewed (or highest-risk files for XL PRs)
- [ ] Feedback classified by severity (Blocking/Suggest/Nit/Praise)
- [ ] Blocking items have specific fix suggestions
- [ ] At least one Praise included for positive aspects
- [ ] Review decision matches feedback (approve only if no Blocking items)
- [ ] Inline comments reference specific lines with severity tags
- [ ] CI/CD checks verified (green before approval)
- [ ] Follow-up completed after author's revisions

## Common Pitfalls

- **Rubber-stamping**: Approving without actually reading the diff. Every approval is an assertion of quality
- **Nit avalanche**: Drowning the author in style preferences. Save nits for mentoring situations; skip them in time-sensitive reviews
- **Missing the forest**: Reviewing line-by-line without understanding the overall design. Read the PR description and commit history first
- **Blocking on style**: Formatting and naming are almost never blocking. Reserve Blocking for bugs, security, and data integrity
- **No praise**: Only pointing out problems is demoralizing. Good code deserves recognition
- **Review scope creep**: Commenting on code that wasn't changed in the PR. If pre-existing issues bother you, file a separate issue

## Related Skills

- `review-software-architecture` — System-level architecture review (complementary to PR-level review)
- `security-audit-codebase` — Deep security analysis for PRs with security-sensitive changes
- `create-pull-request` — The other side of the process: creating PRs that are easy to review
- `commit-changes` — Clean commit history makes PR review significantly easier
