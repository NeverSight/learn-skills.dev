---
name: pr-49-review
description: Reviews pull request #49 for OpenAlgo observability changes, focusing on risks, security, and test coverage. Use when analyzing PR #49 or when the user asks about the local observability stack changes.
---

# PR #49 Review

## Quick start

Use this checklist to review PR #49:

1. Gather PR metadata and file list:
   - `gh pr view 49 --json title,body,files,commits,additions,deletions`
2. Inspect the diff:
   - `gh pr diff 49`
3. Identify risks (security, operational, regressions) and missing tests.
4. Provide a concise review with severity ordering.

## Review focus

- **Security**: default credentials, anonymous access, exposed ports, secrets in logs.
- **Operations**: logging paths, rotation, scheduler installs, cleanup/uninstall.
- **Correctness**: healthcheck logic, log parsing, alert thresholds.
- **Repo hygiene**: generated logs or artifacts committed, ignores updated.
- **Docs**: accurate commands, prerequisites, and troubleshooting steps.

## Output format

Provide feedback in this exact order:

- Critical issues
- Warnings
- Suggestions
- Summary of changes
- Test plan

Keep the feedback specific to PR #49 and reference files by path.
