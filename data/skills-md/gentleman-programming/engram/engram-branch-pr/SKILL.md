---
name: engram-branch-pr
description: >
  Branch and PR workflow for Engram contributors.
  Trigger: When starting any change that will be proposed through GitHub.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

Use this skill when:
- Starting a new feature, fix, or refactor
- Splitting work into multiple PRs
- Preparing a PR for review and merge

---

## Core Rules

1. Create a focused branch (`feat/*`, `fix/*`, `chore/*`).
2. Keep one logical scope per branch.
3. Push early and often to avoid large risky diffs.
4. Open PRs with intent, risk, and validation evidence.
5. Do not mix unrelated changes in the same PR.

---

## PR Structure

Include:
- Problem statement (why this change exists)
- Solution summary (what changed)
- Risk notes (what could break)
- Validation (tests/commands executed)
- Follow-ups (what is intentionally out of scope)

---

## Merge Checklist

- [ ] Branch name matches scope
- [ ] Diff is focused and reviewable
- [ ] Tests relevant to the change pass
- [ ] No temporary files or local artifacts included
- [ ] PR description explains why, not only what
