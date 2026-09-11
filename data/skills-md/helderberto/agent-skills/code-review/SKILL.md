---
name: code-review
effort: high
description: Review a GitHub Pull Request for bugs, security, performance, and code quality. Use when user asks to review a PR or wants pull request feedback. Don't use for reviewing local uncommitted changes, creating new PRs, or merging branches.
---

# Review Pull Request

Mode: $ARGUMENTS

If mode is one of the following, adjust the review:

- BUGS: Focus only on logical or other bugs
- SECURITY: Focus only on security issues
- PERFORMANCE: Focus only on performance issues

## Approval standard

Approve when the change definitely improves overall code health, even if it isn't perfect. Perfect code doesn't exist — don't block a change because it isn't how you would have written it. If it improves the codebase and follows its conventions, approve.

If the change is too large to review well (~1000+ lines), asking the author to split it is a valid review outcome. Suggest a strategy: stack (small change, next one based on it), by file group, horizontal (shared code first, then consumers), or vertical (one end-to-end slice per PR).

## Workflow

1. Analyze the diff and pre-loaded PR context
2. Read changed files to understand full context
3. Review based on mode (or all categories if no mode set)
4. Provide structured feedback

## Review criteria

Apply all axes (or narrow to the mode above):

- **Correctness**: Logic bugs, off-by-ones, race conditions, unhandled states, missing error paths
- **Readability**: Functions <50 lines, nesting <3 levels, no dead code/unused imports
- **Security**: No exposed secrets, no `any`, no unvalidated external data
- **Immutability**: No push/pop/splice/direct mutation
- **Patterns**: Consistent with codebase conventions, no reinvented wheels
- **Performance**: Unnecessary re-renders, O(n²) where O(n) works, missing memoization
- **Code smells**: match the diff against the baseline in [smells.md](references/smells.md) — always judgement calls, and the repo's documented style overrides the baseline

## Output format

Group by severity:

- **Critical** - must fix before merge (bugs, security vulnerabilities)
- **Suggestions** - improvements worth considering
- **Nit** - minor and optional; the author may ignore (formatting, naming taste)
- **FYI** - informational only, no action needed
- **Positives** - good patterns to call out

If you have one structural problem and ten nits, the structural problem _is_ the review — lead with it.

Use `file:line` references for all findings. Include suggested fix for each critical issue.

## Rules

- Review ALL changed files, not just the latest commit
- Be specific — label true nitpicks as **Nit** rather than dropping or inflating them
- **Dependency upgrades** (when `package.json`/lockfile is in the diff): one dependency per change — a bulk bump that breaks hides which package did it; verify against the changelog, not the version number; review the lockfile diff (one direct bump pulls dozens of transitive changes); flag hand-edited lockfiles

## Common Rationalizations

| Excuse                    | Rebuttal                                                       |
| ------------------------- | -------------------------------------------------------------- |
| "Too small to review"     | Small changes cause big bugs — review everything               |
| "It's just a refactor"    | Refactors break behavior silently — verify contracts preserved |
| "Tests pass so it's fine" | Tests don't catch readability, security, or design issues      |
| "I'll clean it up later"  | Later never comes — fix now or it ships as-is                  |

## Verification

- [ ] Every changed file reviewed (not just the diff summary)
- [ ] No critical issue left without a suggested fix
- [ ] Security concerns flagged with specific fix
- [ ] Feedback grouped by severity, not file order
- [ ] Verdict stated against the approval standard — improves code health, or blocked with a reason

## Error Handling

- If `gh pr view` fails → run `gh auth status` to verify authentication; ask user for PR number if not on a PR branch
- If a changed file is deleted in the PR → skip reading it; note it was removed
- If diff is too large → prioritize changed files with highest risk (auth, payments, data mutation)
