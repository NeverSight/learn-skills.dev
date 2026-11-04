---
name: commit-messages
description: Use when writing, reviewing, or editing git commit messages
---

# Commit Messages

Guidelines for writing clear, concise commit messages that communicate intent at a glance.

## When to Use

- Writing a commit message for new changes
- Squashing or rebasing commits
- Reviewing commit messages for clarity

**NOT for:** tag messages, merge commit messages from automated tools, or changelog entries.

## Procedure

1. **Write a concise subject line** — the first line is what most people see:
   - Soft maximum 160 characters; shorter is better
   - Use imperative mood: "Add feature", not "Added" or "Adds"
   - Capitalize the first letter; no trailing period
   - Summarize the change, not the process

2. **Separate subject from body with a blank line** — required for tools to parse correctly. Skip the body if the subject alone is sufficient.

3. **Write the body when context is needed** — explain *why*, not *what*:
   - Wrap at ~72 characters per line
   - Motivate the change; explain constraints or decisions
   - Reference issues with `Fixes #123` or `Refs #456`

4. **One logical change per commit** — if the message needs "and" to describe the change, it probably belongs in two commits.

## What to Include

- **What changed** at a high level
- **Why** the change was made (especially in the body)
- **Breaking changes** or migration notes, if any
- **Issue references** when applicable

## What Not to Include

- **File lists** — `git diff` and `git show` already show this
- **Vague descriptions** — "fix bug", "update stuff", "WIP"
- **Multiple unrelated changes** — split into separate commits
- **Implementation details** — the diff shows how; the message explains why

## Pitfalls

- **Vague subjects:** "fix bug" tells the reader nothing. Name the bug or the fix.
- **Past tense:** "Added feature" reads like a diary. Use imperative: "Add feature".
- **Subject too long:** Over 160 characters gets truncated in most views. Keep it scannable.
- **No blank line after subject:** Breaks tooling (git log --oneline, GitHub, changelogs).
- **Mega-commits:** If the message is a novel, the commit is too large. Split it.
- **Commented-out code in message:** Don't paste diffs or code into the message body.

## Verification

After writing a commit message, confirm:

- Subject is under 160 characters and summarizes the change
- Imperative mood is used ("Fix", "Add", "Update")
- Blank line separates subject from body (if body exists)
- Body explains *why*, not *what*
- One logical change per commit

Quick checklist:
```
Is the subject under 160 characters?
Does it use imperative mood?
Is there a blank line after the subject?
Does the body explain why (if present)?
Could this commit be split into smaller ones?
```
