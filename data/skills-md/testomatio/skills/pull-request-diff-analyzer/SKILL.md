---
name: pull-request-diff-analyzer
description: Analyze git diff/pull request changes to detect feature implementations and fixes, extract acceptance criteria, and identify related tickets. Use this skill when the user wants to understand what changed in a PR/branch, determine if it's a feature or bug fix, and get acceptance criteria for manual test case generation.
license: MIT
metadata:
  author: Testomat.io
  version: 1.0.0
---

# Pull Request Diff Analyzer

Analyze a git diff or PR to detect the change type and extract acceptance criteria for manual testing. **Analysis only** — never modify code.

## Step 1: Detect Branch Context and Scope

Get the current branch:

```bash
git branch --show-current
```

Detect the base branch, in order:

1. From PR context (preferred). If a PR number is known:

```bash
gh pr view {PR_NUMBER} --json baseRefName
```

`baseRefName` in the response is the PR's base branch.

- If the base branch cannot be detected, ask the user to specify it.

Get changed files:

```bash
git diff {BASE_BRANCH}...HEAD --name-only
```

For uncommitted local changes only:

```bash
git diff --name-only
```

For a GitHub PR with full diff view:

```bash
gh pr diff {PR_NUMBER}
```

**Skip to Step 3 with a short summary only (no acceptance criteria)** if:
- Current branch is `master`, `main`, `stable`, or the detected default branch in `baseRefName`.
- No files changed.
- All changes are non-source-code updates:
  - documentation/requirements (`*.md`, `docs/**`)
  - test updates and test docs (`*.test.md`, `test-flows/**`, `tests/e2e`)
  - CI/CD and infrastructure config (`.github/workflows/**`, `Jenkinsfile`)
  - lint/formatter/tooling configs
  - dependency version bumps without behavior changes
- No application/source code behavior changed.

**Proceed to Step 2** if source code changed (`src/**`, `lib/**`, `app/**`, or root `.ts`/`.js`/`.tsx`/`.jsx`/`.java`/`.py`/`.go`/`.rb`/`.php`/`.cs`/`.kt`/`.swift`/`.rs`, etc).

## Step 2: Analyze PR Context and Files

Get PR details:

```bash
gh pr view {PR_NUMBER} --json title,body,comments,reviews,issues
```

Extract testing-relevant info:
- Title — feature/fix name, affected component.
- Description — criteria, test scenarios.
- Comments — test notes, edge cases, reproductions.

Analyze **source code files only**:
- Directories: `src/**`, `lib/**`, `app/**`, `controllers/**`, `services/**`, `models/**`, `pages/**`, `components/**`, `handlers/**`, `modules/**`, etc.
- Extensions: `.ts`, `.js`, `.tsx`, `.jsx`, `.java`, `.py`, `.go`, `.rb`, `.php`, `.cs`, `.kt`, `.swift`, `.rs`
- Skip configs, dependencies, tests, docs, migrations, and other files not related to source code.

Detect PR type:
- Feature — new files, endpoints, components, modules.
- Fix — bug fixes, patches, hotfixes (check commits for "fix", "bug", "hotfix").
- Refactor — code restructure without behavior change.

### Optional: scan-automation-project

**Do not run `scan-automation-project` by default.** Run it only when extra project context adds clear value before writing acceptance criteria.

Run it if:
- The PR introduces new functionality or a significant feature change.
- You need to check whether similar manual tests already exist.
- The user explicitly asks ("check for duplicates", "what tests already exist", or similar).

Skip it if:
- The PR is a small fix or minor UI/component update.
- The diff already gives enough context to write ACs confidently.
- Changes are limited to docs, requirements, tests, configs, or non-source-code updates.
- The project does not appear to contain manual tests.
- Existing test inventory is not relevant for the requested task.

If it is unavailable:
- Continue without checking existing tests.
- Add this note to the AC output: `Manual test inventory not checked — verify existing tests manually if needed.`

Use scan results only to:
- Avoid duplicating existing manual test cases.
- Understand project structure, frameworks, and test organization.
- Improve relevance and consistency of generated acceptance criteria.

## Step 3: Summary with Acceptance Criteria

Output format:

```md
## PR Diff Summary

**PR Type:** ... (feature | fix | refactor)
**Branch:** ... (branch name, e.g. feature/user-auth)
**Changes:** ... (one sentence describing the overall purpose of this PR)
**Affected Files:**
- ... (bullet list of all affected files in this PR)

**Impacted Areas:**
- ... (1-3 bullets, only real impacted files/areas in the PR)

**Acceptance Criteria:**
- action to perform → expected result
- ...
```

Summary rules:
- Keep the summary concise and high-level.
- "Changes" is ONE sentence. Not a paragraph.
- "Impacted Areas" lists only meaningful business or technical impact.
- Omit empty sections instead of writing `None` or `N/A`.
- **Acceptance criteria MUST be testable and user-oriented.**
- Avoid generic statements like "code cleanup", "minor fixes", or "various improvements".
- Do NOT describe implementation details line-by-line.
