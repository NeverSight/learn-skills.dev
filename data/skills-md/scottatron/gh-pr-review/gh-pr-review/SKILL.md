---
name: gh-pr-review
description: Systematic workflow for addressing PR review comments using gh-pr-review CLI. Use when the user wants to work through PR review comments and prefers the gh-pr-review tool over helper scripts.
compatibility: Requires gh CLI auth, gh-pr-review on PATH, and network access to GitHub API.
metadata:
  author: scottatron
  version: "0.1.0"
---

# PR Review Comment Workflow (gh-pr-review CLI)

GitHub repo: https://github.com/scottatron/gh-pr-review

A systematic approach to addressing PR review comments efficiently: fetch all threads, present options for each issue, collect all decisions upfront, implement fixes in a single commit, and document resolutions.

## Requirements

- GitHub CLI (`gh`) installed and authenticated
- `gh-pr-review` CLI on `PATH`
- Repository write permissions (for resolving threads)

## Helper Commands (gh-pr-review CLI)

### Fetch review threads
Fetch review threads for a PR with resolution status.

```bash
# Unresolved threads only
 gh-pr-review list --pr [PR_NUMBER] --status unresolved

# All threads
 gh-pr-review list --pr [PR_NUMBER] --status all

# Resolved threads without replies
 gh-pr-review list --pr [PR_NUMBER] --status resolved-no-reply
```

Use `--repo owner/name` if not running within the repo. Use `--json` for structured output.

### Reply to a thread

```bash
 gh-pr-review reply --thread-id "THREAD_ID" --body "Reply message"
```

### Resolve or unresolve a thread

```bash
 gh-pr-review resolve --thread-id "THREAD_ID"
 gh-pr-review unresolve --thread-id "THREAD_ID"
```

## Core Workflow

### 1. Discovery

Fetch all unresolved review threads:

```bash
 gh-pr-review list --pr [PR_NUMBER] --status unresolved --json
```

If you need all threads, use `--status all`.

**Key data points:**
- `thread.id` - GraphQL thread ID (needed for replies/resolve/unresolve)
- `thread.isResolved` - Resolution status
- `thread.path` - File path
- `thread.line` - Line number
- `comments[].body` / `comments[].author.login` - comment context

Organize threads by file path, severity (Critical/Medium/Low), and theme (security, bugs, quality, docs).

### 2. Analysis

For each comment group:

1. Understand the issue and its impact
2. Identify 2-4 resolution approaches with trade-offs
3. Recommend best approach based on codebase patterns
4. Read relevant code context (affected files, related patterns, docs)

### 3. Decision Collection

Present ALL issues before implementing ANY fixes.

**Format:**
```
Issue #N: [Brief description]
File: path/to/file.ts:42
Severity: Critical/Medium/Low

Options:
1. [Quick fix] - [Trade-offs]
2. [Thorough fix] - [Trade-offs]
3. [Alternative] - [Trade-offs]

Recommendation: Option X because [reasoning]
```

Use AskUserQuestion to collect decisions:
- Present 1-4 issues per question
- Batch by theme or priority for large sets
- Include skip/defer options when appropriate

**Key Principle:** Never start implementing until user has decided on ALL comments.

### 4. Implementation

After collecting all decisions:

1. Plan file edit order (dependencies first)
2. Make all changes based on user's choices
3. Check for related code needing similar fixes
4. Update affected documentation
5. Reply to and resolve each thread as it's addressed:

```bash
 gh-pr-review reply --thread-id "THREAD_ID" --body "Fixed in collaboration with Claude Code - [brief description]"
 gh-pr-review resolve --thread-id "THREAD_ID"
```

6. Run tests

Keep changes focused - only what was discussed, maintain existing style, preserve backward compatibility.

### 5. Commit

Create comprehensive commit message:

```
fix: address [source] PR review comments

[One-sentence summary of scope]

**Critical Fixes:**
- [Security/bug fixes]

**Code Quality:**
- [Refactoring, best practices]

**Documentation:**
- [Examples, guides, comments]

**Changes:**
- path/to/file: [what changed and why]

All [N] review threads addressed.

Relates to #[PR_NUMBER]
```

Commit and push:
```bash
 git add [files]
 git commit -m "[message above]"
 git push
```

### 6. Verification

Verify all review threads are resolved:

```bash
 gh-pr-review list --pr [PR_NUMBER] --status unresolved --json
```

If any threads remain unresolved, investigate and address them before considering the work complete.

## Multi-Round Strategy

For PRs with many comments (>10), split into rounds:

- **Round 1:** Critical (security, bugs, breaking changes)
- **Round 2:** Code quality (refactoring, performance, best practices)
- **Round 3:** Polish (docs, examples, style)

Each round follows full workflow: Fetch → Analyze → Decide → Implement → Commit

## Quality Checkpoints

Before committing:
- All user decisions implemented correctly
- No unintended side effects
- Related code updated for consistency
- Documentation reflects changes
- Tests pass
- Commit message is comprehensive

## Common Patterns

**Security:** Always prioritize (Round 1), create issue if complex, document considerations

**Naming/Style:** Check existing patterns, apply consistently, update style guide if new pattern

**Dependencies:** Consider version compatibility, check breaking changes, update lock files

**Documentation:** Fix incorrect examples, update guides/READMEs, add comments for complex changes
