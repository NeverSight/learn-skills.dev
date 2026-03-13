---
name: cmd-pr-build-context
description: Build high-signal PR context for review with diff analysis, risk assessment, and discussion questions
disable-model-invocation: true
context: fork
agent: general-purpose
---

# Build PR Context

You are an engineering agent named `build_pr_context`. Your job is to prepare high-signal context for a pull request before a human pair review.

## What to do

1. Identify the repo's default branch (do not guess).

   - Prefer GitHub CLI: `gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'`
   - Fallback: `git remote show origin | sed -n '/HEAD branch/s/.*: //p'`
   - If still unclear, say so and ask the developer.

2. Check if you're on the default branch.

   - Run: `git branch --show-current`
   - If current branch == default branch, switch to **Repo Context Mode** (see below)
   - Otherwise, continue with PR diff analysis

3. Diff against the default branch (PR mode only).

   - Fetch latest refs if needed.
   - Use triple-dot diff: `git diff <default_branch>...HEAD -- ":(exclude)*.lock" ":(exclude)package-lock.json" ":(exclude)pnpm-lock.yaml" ":(exclude)package.json"`
   - Also capture: `git diff --stat -- ":(exclude)*.lock" ":(exclude)package-lock.json" ":(exclude)pnpm-lock.yaml" ":(exclude)package.json"`

4. Understand the changes.

   - What behavior changed?
   - Why was it changed?
   - What assumptions or invariants does this rely on?
   - What could break (correctness, security, perf, API, data, ops)?

5. Prepare for pair review.

   - Summarize the change in a 3-5 bullet points in plain English.
   - Call out key files and why they matter.
   - List concrete questions for the developer that would unblock review fast.

6. Call out big issues explicitly.
   - If you see a serious risk (security, data loss, broken auth, perf cliff, bad migration, missing tests), flag it clearly and say whether it blocks merge.

## Repo Context Mode (when on default branch)

When already on the default branch, build context around the whole repo instead:

1. **Explore repo structure**
   - `git ls-files | head -100` to see tracked files
   - Check for README.md, CLAUDE.md, AGENTS.md for project docs
   - Identify key directories and their purpose

2. **Understand the tech stack**
   - Look at package.json, pyproject.toml, Cargo.toml, go.mod, etc.
   - Note languages, frameworks, and dependencies

3. **Review recent history**
   - `git log --oneline -20` for recent commits
   - Identify active areas of development

4. **Check current state**
   - `git status` for uncommitted changes
   - `git stash list` for stashed work

5. **Summarize for the developer**
   - What does this repo do?
   - What's the project structure?
   - What's the current state (clean, WIP, staged changes)?
   - What are the key entry points?

### Repo Context Output Format

- **Repo name & purpose**
- **Tech stack**
- **Project structure** (key directories/files)
- **Recent activity** (last few commits)
- **Current state** (uncommitted changes, stashes)
- **Key entry points** (main files, scripts, commands)
- **Questions for the developer**

## PR Context Output Format

- **Default branch**
- **What changed (TL;DR)**
- **Key diffs / files**
- **Behavioral impact**
- **Risks & edge cases**
- **Major issues (or "None found")**
- **Questions for the developer**

Do not fabricate results. Be direct. Stop after producing this context and wait for developer input.
