---
name: jb-committer
description: Groups related git changes into coherent commits and drafts commit messages. Use when the user asks to commit, commit current changes, or create a commit.
private: true
allowed-tools: Bash(git:*)
skill_author: bjesuiter@gmail.com
---

# Committer Skill

Author: bjesuiter

## When to use (keywords: commit, commit-current, commit-only)

Use this skill when the user asks to create commits or commit the current change set.

## Commit related changes (keyword: commit)

Read all uncommitted changes in the git working directory: unstaged, staged, and untracked.

Group them by logical change, for example:
- Renaming a function/variable/class across multiple files
- Adding a new feature: component + route + tests + types all belong together
- Moving/refactoring code from one file to another (delete in A, add in B)
- Updating imports after relocating a file
- Adding a dependency to package.json and its usages in source files
- Bug fix that touches multiple related files
- Configuration changes that belong together (e.g., tsconfig.json + package.json for a new compiler option)
- Type definition changes and the code that uses those types
- A new test file alongside the implementation it tests
- Documentation updates that describe the same feature across multiple docs
- Deleting dead code across multiple files
- Updating API endpoints: handler + route registration + client calls + tests

Commit all related changes together.
Make multiple commits if needed.
Choose a clear message that describes the semantic meaning of the change.
After finishing the commit(s), always push to the remote.

**When using "beans" for ticketing and issue tracking**
- A change in the beans file should be committed together with the change that is related to the ticket.
- Before committing: a ticket related to the current change should be changed to status "done" if the ticket is finished; otherwise the ticket status change needs to be committed in a second commit.

## Commit only one change (keyword: commit-current or commit-only)

Sometimes the user wants to only commit files related to a single change.
If the user asks for "commit-current" or "commit-only", find all files related to the current change in the chat session and only commit those files as described above. Do not write or commit unrelated change files.
After creating the commit, always push to the remote.

## Example

Input: "commit-current"
Output: Stage only files related to the current change and create a single commit with a concise message.
