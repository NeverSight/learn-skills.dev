---
name: analyse-issue
description: Analyze GitHub issues by link or issue number. Use when a user says "analyse issue"/"analyze issue" or provides a GitHub issue URL/number and asks to fetch the issue content, verify it matches the current repo, and inspect local code to confirm the problem.
---

# Analyse Issue

## Overview

Fetch the issue details, verify repo alignment, and inspect the local codebase to confirm or refute the reported problem. Provide an evidence-backed analysis with clear next steps.

## Workflow

### 1) Parse the issue input

- If input is a GitHub issue URL, extract owner/repo and issue number.
- If input is just a number, assume the current repo unless the user specifies another repo.
- If the provider is not GitHub or is unclear, ask for clarification before proceeding.

### 2) Verify local repo matches the issue

- Ensure the current directory is inside a git repo (`git rev-parse --show-toplevel`).
- Identify the target remote (prefer `origin`); normalize SSH/HTTPS to `owner/repo`.
- If the issue URL repo does not match the local `owner/repo`, stop and ask the user to switch directories or confirm the target repo.
- If no remote or multiple candidates exist, ask the user which repo to use.

### 3) Fetch issue content

Prefer `gh` when available:

- `gh issue view <num> --json title,body,labels,comments,author,createdAt,updatedAt`
- If URL provided, run against that repo: `gh issue view <num> -R owner/repo --json ...`

Fallbacks:

- `gh api repos/{owner}/{repo}/issues/{num}` and `.../comments` if you need more fields.
- If `gh` is unavailable but `GITHUB_TOKEN` exists, use `curl` with the GitHub API.
- If neither works, ask the user to paste the issue content.

Capture at least: title, body, labels, environment details, repro steps, expected/actual behavior, and key comment insights.

### 4) Analyze the codebase

- Translate the issue into concrete signals (keywords, error messages, stack traces, config names).
- Use `rg` to locate relevant code, tests, and configs.
- Trace the execution path: entry points -> core logic -> dependencies.
- Identify likely failure points: missing checks, edge cases, incorrect assumptions, data shape mismatches, concurrency/timing issues.
- If appropriate and safe, run focused tests; otherwise propose targeted tests to validate the hypothesis.

### 5) Confirm or qualify the issue

- Provide evidence with file references and reasoning.
- If you can only reason without running tests, state assumptions and confidence.
- If evidence is insufficient, list the exact missing info needed.

### 6) Respond with a structured analysis

Include:

- Issue summary (expected vs actual)
- Repo match verification
- Evidence (files/functions)
- Root-cause hypothesis or confirmed cause
- Suggested fix approach
- Questions or missing data
- Next steps (tests, logs, repro)

## Output conventions

- Respond in the user's language when clear; default to Chinese for Chinese prompts.
- Keep analysis concise but include concrete file pointers and evidence.
- Do not claim confirmation without code-based evidence or reproduction.
