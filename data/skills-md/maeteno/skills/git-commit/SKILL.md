---
name: git-commit
description: Generate well-structured, descriptive git commit messages following conventional commit standards. Use when the user wants to commit changes, asks for help writing commit messages, or invokes /commit. Analyzes staged/unstaged changes and produces clear, informative commit messages.
---

# Git Commit

## Overview

This skill generates high-quality git commit messages by analyzing code changes and following the Conventional Commits specification. Good commit messages serve as the historical record of a project's evolution, enabling developers to understand the motivation and impact of every change.

## When to Use This Skill

Use this skill when users:
- Want to commit their code changes
- Ask for help writing a commit message
- Use `/commit` or similar commit-related commands
- Want to review and improve an existing commit message

## Workflow

### Step 1: Analyze Changes

Run the following commands in parallel to understand the current state:

1. `git status` — identify staged and unstaged changes
2. `git diff --cached` — view staged changes in detail
3. `git diff` — view unstaged changes (if nothing is staged)
4. `git log --oneline -5` — check recent commit style for consistency

If nothing is staged, inform the user and ask whether to stage all changes or select specific files.

### Step 2: Understand the Changes

- Read the diffs carefully to understand **what** changed and **why**
- Identify the primary purpose of the change (one commit = one purpose)
- Determine the appropriate commit type and scope
- Note any breaking changes

### Step 3: Generate the Commit Message

Follow the structured format below to compose the message, then present it to the user for confirmation before committing.

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Subject Line Rules

- Format: `<type>(<scope>): <subject>`
- `scope` is optional, use it when the change targets a specific module/component
- `subject` must be concise (under 72 characters total for the entire subject line)
- Use imperative mood ("add feature" not "added feature")
- Do not end with a period
- Clearly convey the purpose of the change

### Body (Optional)

- Separate from subject with a blank line
- Explain **what** and **why**, not **how** (the code shows how)
- Use bullet points for multiple related changes
- Wrap lines at 72 characters

### Footer (Optional)

- Reference related issues: `Closes #123`, `Refs #456`
- Note breaking changes: `BREAKING CHANGE: description`

## Type Reference

| Type       | Description                                              |
|------------|----------------------------------------------------------|
| `feat`     | A new feature                                            |
| `fix`      | A bug fix                                                |
| `docs`     | Documentation only changes                               |
| `style`    | Formatting, whitespace, etc. (no logic change)           |
| `refactor` | Code restructuring (no new feature, no bug fix)          |
| `perf`     | Performance improvement                                  |
| `test`     | Adding or updating tests                                 |
| `chore`    | Build process, dependencies, tooling changes             |
| `merge`    | Merge branches                                           |
| `revert`   | Revert a previous commit                                 |

## Anti-Patterns (MUST Avoid)

These commit messages are vague and useless — never generate messages like:

- `Fix bug`
- `Update code`
- `Modify class`
- `WIP`
- `Minor changes`
- `Misc fixes`

Every commit message must clearly communicate the purpose of the change.

## Examples

### Example 1: Simple feature (subject only)

```
feat(auth): add OAuth2 login support
```

### Example 2: Bug fix with body

```
fix(cart): resolve incorrect total when removing items

The cart total was not recalculated after removing an item due to
a stale cache. Clear the price cache before recalculating totals.

Closes #234
```

### Example 3: Refactor with bullet points

```
refactor: simplify libvirt create calls

- Minimize duplicated code for create
- Make wait_for_destroy happen on shutdown instead of undefine
- Allow for destruction of an instance while leaving the domain
```

### Example 4: Breaking change

```
feat(api)!: change authentication endpoint response format

The /auth/login endpoint now returns a structured token object
instead of a plain string. All API clients must update their
token parsing logic.

BREAKING CHANGE: /auth/login response changed from string to
{ token: string, expiresAt: number }
```

### Example 5: Performance improvement

```
perf(scheduler): add CPU architecture filter support

In a mixed environment of running different CPU architectures,
one would not want to run an ARM instance on a x86_64 host and
vice versa. This filter prevents instances from being scheduled
on incompatible hosts.

- Add ARM as a valid architecture to the filter
- The ArchFilter is not turned on by default
```

## Guidelines

- **One purpose per commit**: If a change does multiple things, suggest splitting into separate commits
- **Match project style**: Check `git log` and follow the existing convention in the repository
- **Language**: Write commit messages in English by default. Only use Chinese if the user's invocation command explicitly requests it (e.g., "用中文提交")
- **No AI attribution**: Never include `Co-Authored-By: Claude`, `Generated by Claude`, or any other AI-related tags, signatures, or identifiers in the commit message
- **User confirmation required**: Always present the proposed commit message to the user first. Do NOT run `git commit` until the user explicitly confirms or approves the message
