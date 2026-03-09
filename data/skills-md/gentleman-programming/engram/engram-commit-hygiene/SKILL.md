---
name: engram-commit-hygiene
description: >
  Commit standards for Engram contributors.
  Trigger: Any commit creation, review, or branch cleanup.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

Use this skill when:
- Creating commits
- Reviewing commit history in a PR
- Cleaning up staged changes

---

## Rules

1. Use conventional commit format.
2. Keep one logical change per commit.
3. Message should explain why, not only what.
4. Never include `Co-Authored-By` in this repo.
5. Never commit generated/temp/local files.

---

## Pre-Commit Checklist

- [ ] Diff matches commit scope
- [ ] No secrets or credentials
- [ ] No binaries, coverage outputs, or local artifacts
- [ ] Tests relevant to the change passed
- [ ] Commit message is clear and conventional
