---
name: secret-leak-check
description: Use this skill to detect potential secret and privacy leaks in changed files, staged diffs, commit messages, and git identity settings before code is shared or merged.
---

# Secret & Privacy Leak Check Skill

Use this skill when reviewing repository changes for accidental exposure of sensitive data.

## Skill Overview

This skill helps you detect:

1. Traditional secrets (tokens, API keys, credentials, connection strings).
2. Sensitive architecture details (database schema/internal topology details that should not be public).
3. Privacy data (personal email addresses, phone numbers, real names).
4. Leakage risks in commit messages.
5. Git identity/privacy misconfiguration in open-source contexts.

## Core Principles

1. **Scope first, then rules**: Determine scan scope before running pattern checks.
2. **Diff-first by default**: Prioritize review of newly introduced risk.
3. **Context-aware checks**: Apply open-source/GitHub-specific checks only when conditions match.
4. **Actionable results only**: Report findings with severity, location, and remediation guidance.

## Workflow

### Step 1: Determine Scan Scope

Use [references/scope_selection.md](references/scope_selection.md).

Default behavior when user gives no explicit scope:

1. Scan staged changes first (index vs `HEAD`, e.g., `git diff --cached`).
2. Then scan unstaged working tree changes (working tree vs index, e.g., `git diff`).
3. If no staged changes exist, scan all modified and untracked files in the working tree.

If user explicitly asks to scan all commits in a PR, expand scope to:

- Current staged diff (index vs `HEAD`, if any).
- Current unstaged/untracked working tree changes (working tree vs index, if any).
- Every commit in the PR range, scanned commit-by-commit for leak content in diffs and commit messages.

If user explicitly asks to scan all files, ignore diff-only logic and scan the entire requested range.
After scope is determined, build the concrete target file list. Do not report "full scan complete" unless all in-scope files satisfy both conditions.

If any files are excluded, list them explicitly with reason.

### Step 2: Apply Detection Rules by Data Category

Use [references/detection_rules.md](references/detection_rules.md).

Run category-specific checks for:

- Secret tokens and API keys.
- Credential-like material and high-risk config values.
- Database schema/internal structure leakage.
- PII and privacy data (email, phone, real name).

### Step 3: Run Scenario-Specific Checks

Load only relevant references:

- Diff/staging behavior: [references/scenario_diff_and_staging.md](references/scenario_diff_and_staging.md)
- Full-repo/range behavior: [references/scenario_full_scan.md](references/scenario_full_scan.md)
- Commit message review: [references/scenario_commit_messages.md](references/scenario_commit_messages.md)

If the user does not explicitly disable it, also check commit messages in the active scan range.
If user explicitly asks to scan all commits in a PR, commit message checks must cover each commit in that PR range.

### Step 4: Validate Git Identity Privacy (Conditional)

Use [references/scenario_git_identity_privacy.md](references/scenario_git_identity_privacy.md).

Rules:

1. Only for open-source project scenario: check whether git config email may expose personal email.
2. Only when the remote is GitHub: check whether a GitHub privacy email (`<id>+<username>@users.noreply.github.com`) is used when privacy is desired.

### Step 5: Report Findings

Use [references/reporting_template.md](references/reporting_template.md).

For each finding include:

- Severity (`critical`/`high`/`medium`/`low`)
- Category (`secret`/`privacy`/`metadata`)
- Location (file path, diff hunk, or commit hash/message)
- Why it is risky
- Concrete remediation

## Response Template

> **Scan Scope**: [staged diff / working-tree-vs-HEAD / changed files / full scan / pr-all-commits]
>
> **Context Checks**:
> - Open-source scenario: [yes/no]
> - GitHub remote detected: [yes/no]
>
> **Findings Summary**:
> - Critical: [count]
> - High: [count]
> - Medium: [count]
> - Low: [count]
>
> **Findings**:
> - [severity] [category] [location] — [risk] — [recommended fix]
>
> **Commit Message Review**:
> - [result for checked commit range]
>
> **Git Identity Privacy Check**:
> - [result and recommendation]
