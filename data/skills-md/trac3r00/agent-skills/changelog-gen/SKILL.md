---
name: changelog-gen
description: Generates a categorized changelog skeleton from conventional commits since a tag or ref — Added/Changed/Fixed/Documentation/Internal sections with scope annotations preserved. Deterministic; the agent writes prose, this provides the honest skeleton from git history itself.
when_to_use: Before any release, when writing release notes, or when a project has conventional-commit history but no changelog discipline. NOT a prose writer — it produces the categorized skeleton; a human or agent writes the narrative on top.
version: 1.0.0
license: MIT
metadata:
  agentskills:
    tags: [changelog, releases, git, documentation]
---

# Changelog Gen

Release notes from the only honest source: the commit history itself.

## Commands

```bash
python3 scripts/changelog_gen.py                          # since last tag
python3 scripts/changelog_gen.py --since-tag v1.2.0
python3 scripts/changelog_gen.py --since HEAD~20 --json
python3 scripts/changelog_gen.py --out CHANGELOG.md
```

## Sections (conventional-commit mapping)

| Type | Section |
|---|---|
| `feat` | Added |
| `fix`, `revert` | Fixed |
| `refactor`, `perf`, `style` | Changed |
| `docs` | Documentation |
| `test`, `chore`, `build`, `ci` | Internal |

Scope annotations preserved: `feat(api): add tokens` -> "add tokens (api)".
Non-conventional commits land in Other — visible, not silently dropped.

## Pairs with

`git-master` (the history this reads), `repo-audit` (the repo hygiene gate
that would flag a missing changelog workflow).
