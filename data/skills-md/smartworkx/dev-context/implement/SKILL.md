---
name: implement
description: >-
  Implement a feature from issue, specs, and docs, then propose a PR.
  TRIGGER when: user asks to implement, build, or code a feature, or to create a PR from an issue.
  Examples: "implement issue 42", "build the export feature", "implement and open a PR".
  DO NOT TRIGGER when: user wants to create an issue, write specs, or just commit changes.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Agent, AskUserQuestion, WebFetch, WebSearch, Skill
---

Implement a feature by reading all prepared context, then commit, push, and create a PR.

## Branch Setup

- **In a worktree** (sibling directory with a feature branch already checked out) → work in the current directory
- **On main** → invoke the `feature-branch` skill (via `Skill` tool) with the issue number as argument, then `cd` into the created worktree before continuing

## Steps

1. Resolve the issue — the argument can be:
   - A **GitHub issue number or URL** → fetch with `gh issue view`
   - A **description** → search with `gh issue list --search "<description>"` to find the matching issue
   - Nothing → ask the user what to implement

2. Read all available context — start with what's already on the branch:
   - Run `git log main..HEAD --oneline` to see commits on the feature branch (design work, specs, ADRs may already be committed)
   - Read any specs in `doc/spec/` related to the feature
   - Read any ADRs in `doc/adr/` related to the feature
   - Read any docs in `doc/` related to the feature
   - Review existing code and tests in the affected areas

3. Implement the feature based on the gathered context:
   - Follow specs as acceptance criteria
   - Respect architectural decisions from ADRs
   - Match existing code style and patterns

4. When implementation is complete — commit, push, and create a PR:
   - Stage relevant files — prefer `git add <file>...` over `git add -A`
   - Do NOT stage files that look like secrets (`.env`, credentials, tokens)
   - Extract the issue number from the current branch name (e.g. `42-add-export` → `#42`)
   - Commit with message: `#<number> <imperative summary>`
   - Push with `git push -u origin <branch>`
   - Create PR with `gh pr create`:
     - Title: imperative, under 70 chars
     - Body includes "Closes #<number>" to auto-link the issue
   - Show the PR URL when done

## Rules

- Follow commit message convention: `#<number> <imperative summary>`
- If there are no changes to commit, tell the user
