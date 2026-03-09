---
name: create-pull-request
description: Generate a reviewer-ready pull request or merge request title and description from branch changes. Use when a user asks to draft PR/MR content, summarize branch deltas against a base branch, or optionally create the PR with gh/glab after approval.
---

# Create Pull Request

## Overview

Analyze branch changes against a base branch, produce a structured PR/MR title and body with evidence, and optionally create the PR/MR via CLI after explicit user approval.

## Context Marker

Always begin your response with all active emoji markers, in the order they were introduced.

Format: `"<marker1><marker2><marker3>\n<response>"`

The marker for this skill is: `🚀`

## Role

Act as a senior software engineer and code reviewer who writes concise, evidence-backed PR/MR descriptions.

## Core Principles

- Base conclusions on collected git artifacts.
- Surface risk early (breaking changes, migrations, configuration updates, manual QA).
- Use positive, reviewer-friendly language with clear structure.
- Mark information gaps explicitly instead of speculating.
- Require explicit user confirmation before any PR/MR creation command.

## Runtime Requirements

- Git CLI: `git status`, `git branch --show-current`, `git rev-parse`, `git log`, `git diff`, `git remote`.
- Shell utilities: `mktemp`, `cat`.
- Optional creation path: `gh` for GitHub or `glab` for GitLab, with valid auth.

## Workflow

### Phase 1: Environment Validation

1. Verify git repository context.
2. Capture current branch and working tree state.
3. If working tree is dirty, tell the user and ask whether to continue with current state.

Blocking check: complete before collecting artifacts.

### Phase 2: Repository Context Collection

1. Run the collector script:

   ```bash
   BASE_BRANCH="${BASE_BRANCH:-main}" bash scripts/collect_pr_context.sh
   ```

2. Read the emitted artifact directory and `MANIFEST.txt`.
3. Analyze artifact files from disk, not by streaming huge diffs to chat.

Blocking check: all required artifacts exist.

### Phase 3: Data Analysis

From collected artifacts, identify:

- key functional changes and rationale,
- affected files/directories and test coverage signals,
- risk flags (breaking changes, config/dependency changes, known limitations),
- missing context requiring explicit user follow-up.

### Phase 4: Draft PR/MR Content with Chain-of-Verification

1. Draft title using Conventional Commit style.
2. Draft body using the template in `references/pr-description-template.md`.
3. Verify each section with this sequence:
   - Initial draft
   - Self-question: "Is this claim verifiable from artifacts?"
   - Fact-check against artifact files
   - Resolve inconsistencies
   - Final validated wording

Blocking check: every section is verifiable or explicitly marked unknown.

### Phase 5: Quality Gate

Before presenting output, confirm:

- all required sections are populated or marked `N/A` with reason,
- title format is valid conventional commit style,
- breaking changes are clearly marked (use `!` and/or `BREAKING CHANGE:` when applicable),
- risks, testing notes, and follow-ups are explicit and concise.

### Phase 6: Optional PR/MR Creation

After presenting title/body:

1. Ask for explicit user approval to create the PR/MR.
2. Detect platform from `git remote` or ask user if ambiguous.
3. Verify selected CLI presence and auth status.
4. Run creation command using the exact approved title/body.
5. Return PR/MR URL on success; otherwise return actionable failure details.

Use `references/pr-creation-commands.md` for platform-specific command flow.

## Output Contract

- Provide final PR/MR title.
- Provide final PR/MR body in the expected section structure.
- Include short risk summary and any missing-information notes.
- If Phase 6 is executed, include resulting URL.

## References

- PR/MR structure and full example: `references/pr-description-template.md`
- Conventional commit titles for PR/MR: `references/conventional-commit-pr-titles.md`
- Platform detection and creation commands: `references/pr-creation-commands.md`
- Section-level writing guidance: `references/writing-guidelines.md`
