---
name: git-commit-conventional
description: Create Conventional Commit messages and execute safe git commits from working tree changes. Use when users ask to create a commit, write a conventional commit message, split broad changes into multiple commits, stage only parts of files, run pre-commit before committing, or perform a quick commit-time quality review with severity guardrails.
---

# Git Commit Conventional

## Overview

Generate clear Conventional Commit messages, decide commit grouping, run commit-time checks, and create commit(s) safely.

## Context Marker

Always begin your response with all active emoji markers, in the order they were introduced.

Format: `"<marker1><marker2><marker3>\n<response>"`

The marker for this skill is: `🎯`

## Workflow

1. Inspect repository context:
   - Run `git log -n 20 --pretty=format:%s` for subject style context only.
   - Run `git status`.
1. Select the diff to analyze:
   - If staged changes exist, use `git diff --staged` and ignore unstaged changes.
   - If nothing is staged, run `git diff` and ask whether to stage all or specific files before committing.
1. Evaluate commit pressure using balanced thresholds:
   - Count changed files and changed lines from the active diff context.
   - Classify zone:
     - `green`: `<=5` files and `<=150` changed lines.
     - `yellow`: `6-12` files or `151-400` changed lines.
     - `red`: `>12` files or `>400` changed lines.
   - Apply zone behavior:
     - `green`: proceed with normal commit boundary analysis.
     - `yellow`: recommend splitting and record a risk note if user chooses a single commit.
     - `red`: require a split plan before proceeding; only continue single-commit flow with explicit user override.
1. Decide single versus multiple commits with an explicit framework:
   - Check logical separation: split when changes serve multiple distinct goals.
   - Check file-type mixing: split documentation changes from code changes when they can stand alone.
   - Check implementation versus tests: split when test updates are independent from implementation updates.
   - Check formatting versus logic: split formatting-only churn from behavior changes.
   - Check dependencies versus behavior: split dependency and tooling updates from code behavior changes.
   - Check mixed-purpose hunks in the same file: split by hunk when one file contains unrelated intents (for example, rename plus refactor).
   - Check size and reviewability: consider splitting broad changes (for example, over roughly 150 changed lines) by module or feature.
   - Check issue/feature boundaries: split when multiple bugs or features are addressed in one diff.
   - Keep together when changes are small and focused on one purpose.
   - Keep together when changes are tightly coupled and splitting would create non-functional or misleading history.
   - Keep together when all changes are part of one coherent refactor.
1. Stage changes intentionally for the selected commit boundary:
   - Use `git add -p` to stage only relevant hunks when a file mixes logical changes.
   - Use `git add -e` only when hunk editing is required and apply minimal edits.
   - After staging, verify scope with `git diff --staged` and `git diff` before proceeding.
   - If partial staging would create a broken intermediate commit, keep dependent hunks together.
1. Run a concise quality review before committing:
   - Check correctness, maintainability, security, performance, and tests.
   - Classify findings by severity: Critical, High, Medium, Low.
   - Present findings using this structure: Executive Summary; Issues by severity with file/line references; Suggested fixes with brief examples; Positive observations; Actionable next steps.
   - If any Critical or High issue is found, stop and request explicit user confirmation before committing.
1. If `.pre-commit-config.yaml` exists, run `pre-commit run`:
   - Never bypass hooks.
   - For trivial fixes, apply changes, restage files, and rerun hooks with a max of 2 retries.
   - Stop retrying when hooks pass, when retries are exhausted, or when reruns make no additional file changes.
   - If hooks still fail after retries, stop and ask the user for direction.
   - For non-trivial fixes, present the proposed fix to the user and get approval before applying and proceeding.
   - Treat formatting-only or whitespace-only hook edits as trivial auto-fixes.
   - Track every auto-fixed file and the hook that changed it.
1. Generate commit message(s) in strict Conventional Commit format:
   - Subject must match `<type>(<scope>): <subject>` or `<type>: <subject>`.
   - If subject format is invalid, regenerate until format is valid.
   - Keep subject imperative and concise.
   - If the change is breaking, use `!` and add explicit breaking-change explanation in the body and/or footer (`BREAKING CHANGE: ...`).
   - Include body to document context and rationale.
   - Only exclude a body when the changes are very, very small.
1. Apply AI attribution policy before each commit:
   - Always include a footer-only `Co-Authored-By` attribution on agent-created commits.
   - Never mention AI generation in the subject or body.
   - Use best effort self-identification to determine AI name and email from runtime/model self-awareness metadata.
   - If email is not readily available, use `no-reply@example.com`.
   - If name is not readily available, use `AI Assistant`.
   - Never block commit flow by asking the user for attribution identity.
1. Use deterministic output contract for single-commit and multi-commit runs:
   - Before committing, present `Commit Plan`:
     - `commit_count`
     - `threshold_zone_encountered`
     - `boundaries_rationale`
     - `scope_per_commit`
   - Before each commit, present `Per-Commit Preview`:
     - `index` (`i/N`)
     - `staged_files`
     - `subject`
     - `body_present`
     - `footers`
     - `checks_to_run`
   - After each commit, present `Per-Commit Result`:
     - `hash`
     - `subject`
     - `hook_result`
     - `auto_fix_files`

1. Validate message format and create commit(s):
   - Show generated message(s) in chat.
   - Run `git commit` with the generated message(s).
   - For multiple commits, stage the right files before each commit.
   - In the final commit summary to the user, include:
     - Ordered `<hash> <subject>` list.
     - `Pre-commit changes` note:
       - If auto-fixes were applied, list hook id(s) and file path(s).
       - If none were applied, explicitly say `Pre-commit changes: none`.
     - `ai_attribution_applied: yes/no`.
     - `working_tree_status: clean/not clean`.

## Mandatory Rules

- Never use hook bypass flags such as `--no-verify` or `-n`.
- Never commit when Critical or High review issues are present unless the user explicitly confirms.
- Never include unrelated files in a commit.
- Never stage an entire file when only some hunks belong to the current commit boundary.
- Always report whether pre-commit auto-fixed files before finalizing the commit result message.

## References

- Conventional commit types, scopes, and templates: `references/conventional-commits.md`
- Review severity rubric and reporting format: `references/review-guardrails.md`
- Commit pressure zones and threshold behavior: `references/commit-hygiene-thresholds.md`
- AI attribution policy for commits: `references/ai-attribution.md`
