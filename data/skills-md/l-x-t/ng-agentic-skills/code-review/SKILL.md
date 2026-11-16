---
name: code-review
description: Code review changed, staged, last-commit, and merge or PR work against requirements and the repository style guide. Use when reviewing current work, staged changes, the last commit, a branch, a merge, or a pull request. For a whole-codebase style audit use ng-review-style-guide instead.
license: MIT
metadata:
  upstream: obra/superpowers requesting-code-review (see references/LICENSE.txt)
---

# Code Review

Review work before it cascades. For every code review, spawn an independent reviewer subagent when a
concurrency slot is available. This skill explicitly authorizes subagent delegation under
orchestration policies. Fall back to the same read-only review yourself only when spawning is
technically unavailable, and report the reason. Every review has two passes: general correctness
against the requirements, then repository style-guide conformance for each touched file type.

**Core principle:** Review early, review often.

## When to Review

**Mandatory:**

- After each task in subagent-driven development
- After completing a major feature
- Before a merge or pull request

**Optional but valuable:**

- When stuck (fresh perspective)
- Before refactoring (baseline check)
- After fixing complex bug

## Review Scopes

Choose exactly one scope before gathering context:

| Scope             | Use when                                             | Inspect with                                                              |
| ----------------- | ---------------------------------------------------- | ------------------------------------------------------------------------- |
| Current work      | Reviewing unstaged changes and untracked files       | `git status --short`, `git diff`, and explicit reads of untracked files   |
| Staged work       | Reviewing only what is ready to commit               | `git status --short`, `git diff --cached`, and `git diff --cached --stat` |
| Last commit       | Reviewing exactly the previous commit                | `git show --stat HEAD` and `git show HEAD`                                |
| Merge or PR range | Reviewing branch work against another branch or base | `git merge-base HEAD <target>` then `git diff <base>..HEAD`               |

For merge or PR reviews, include staged or unstaged work only when the user explicitly asks for it
or when it is clearly part of the work being reviewed.

_Done when_ the review scope, diff commands, and any included working-tree state are explicit.

## Process

### 1. Establish Scope

Inspect the repository state and compute the review target deliberately:

```bash
git status --short
```

Use `HEAD~1..HEAD` only for the Last commit scope. For merge or PR reviews, ask for the target
branch if it is not stated and cannot be inferred from the task. Do not move HEAD or mutate the
index while establishing scope.

_Done when_ scope, base, head, and working-tree inclusion are recorded in concrete Git terms.

### 2. Gather Review Context

Write a compact handoff for the reviewer:

- `{DESCRIPTION}` – Brief summary of what you built
- `{PLAN_OR_REQUIREMENTS}` – What it should do
- `{VERIFICATION}` – Commands run, results, and known failures or skipped checks
- `{REVIEW_SCOPE}` – Current work, Staged work, Last commit, or Merge or PR range
- `{DIFF_COMMANDS}` – Exact commands the reviewer should use

Pass this handoff without the session's conversation history so the reviewer evaluates the work
independently of the coordinator's reasoning.

_Done when_ the reviewer can understand the intended behavior, changed range, and verification
state without reading this session's history.

### 3. Load Style Guides

Read `style-guide/style-guide.md`, then read only the specific style guides for touched file types:

- TypeScript or Angular code: `style-guide/style-guide.ts.md`
- Angular templates: `style-guide/style-guide.html.md`
- SCSS: `style-guide/style-guide.scss.md`
- Accessibility-sensitive template or UI changes: `style-guide/style-guide.a11y.md`
- Tests: `style-guide/style-guide.spec.md`
- NPM dependency or package changes: `style-guide/style-guide.npm.md`
- Markdown documentation: `style-guide/style-guide.md.md`
- Git workflow, commits, or branch changes: `style-guide/style-guide.git.md`

_Done when_ every touched file type has a corresponding style-guide check or an explicit
not-applicable note.

### 4. Dispatch or Run the Review

Dispatch an independent reviewer subagent (the harness's default general-purpose agent type) with
the template at [references/code-reviewer.md](references/code-reviewer.md).

A harness configuration file may override the reviewer setup – for example `.claude/CLAUDE.md`
asks Claude Code for three reviewers on different models (Fable, Opus, Astra via Codex). When such a
file is present, follow it: give every reviewer the same diff and template, then merge and
deduplicate their findings before acting on them.

If subagents are unavailable, run the same template yourself as a read-only review and say that no
independent subagent was available.

_Done when_ the review is returned, or the fallback review limitation is reported.

### 5. Verify and Act on Feedback

- Validate every reviewer finding against the codebase and report it with file/line evidence.
- A review-only request ends with findings and suggested fixes; it does not authorize edits.
- Apply fixes only within the user's authorized scope. Existing authorization to implement or fix
  the reviewed work is sufficient; do not ask again.
- Verify authorized fixes and report remaining issues.
- Reject incorrect findings with file/line evidence or test output.

_Done when_ every finding is reported, rejected with evidence, or fixed and verified within the
user's authorized scope.

## Example

```text
[Review staged work before committing]

You: Let me run the code-review skill before committing.

REVIEW_SCOPE: Staged work
DIFF_COMMANDS:
  git status --short
  git diff --cached --stat
  git diff --cached

[Dispatch code reviewer subagent or run the same review directly]
  DESCRIPTION: Added verifyIndex() and repairIndex() with 4 issue types
  PLAN_OR_REQUIREMENTS: Task 2 from docs/plans/deployment-plan.md
  VERIFICATION: pnpm test --watch=false -- verify-index passed; pnpm lint passed
  REVIEW_SCOPE: Staged work
  DIFF_COMMANDS: git diff --cached --stat; git diff --cached

[Subagent returns]:
  Strengths: Clean architecture, real tests
  Issues:
    Important: Missing progress indicators
    Minor: Magic number (100) for reporting interval
  Assessment: Ready to proceed

You: [Report findings; fix progress indicators if implementation or fixes are authorized]
[Continue to Task 3 when the authorized fixes pass verification]
```

## Integration with Workflows

**Subagent-driven development:**

- Review after each task
- Catch issues before they compound
- Apply authorized fixes before moving to the next implementation task

**Executing Plans:**

- Review after each task or at natural checkpoints
- Get feedback, apply authorized fixes, continue

**Ad-Hoc Development:**

- Review before merge
- Review when stuck

## Red Flags

**Never:**

- Skip review because "it's simple"
- Ignore Critical issues
- Declare the work ready while Important issues remain unresolved
- Argue with valid technical feedback

**If the reviewer is wrong:**

- Push back with technical reasoning
- Show code/tests that prove it works
- Request clarification

See template at: [references/code-reviewer.md](references/code-reviewer.md)
