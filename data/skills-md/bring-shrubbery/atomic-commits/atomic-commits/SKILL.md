---
name: atomic-commits
description: Enforces atomic commit workflow — breaks implementation into small, self-contained units and commits after each one. Use when implementing features, fixing bugs, or making any multi-step code changes.
---

# Atomic Commits

Every task follows this rhythm: **plan, then repeat (implement one thing → verify → commit).**

## 1. Plan

Before coding, break the task into atomic steps. List them. Each step is one logical change — one concern, one purpose. The codebase must work after each step.

## 2. Implement → Verify → Commit (repeat for each step)

Do one step. Verify it works. Commit it. Move to the next.

**One commit = one logical change.** Not two things. Not "a feature and its tests." Not "a rename and a behavior change." One thing.

Commit format: `type: what changed`
Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `style`, `perf`

Stage only the files that belong to that change. Never `--no-verify`.

## 3. Stay honest

- If a step should split further, split it.
- If tests break from your change, fix them in the same commit — the unit isn't done until it works.
- Never amend a previous atomic commit to sneak in more changes. Make a new commit.
