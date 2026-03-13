---
name: changelog-writing
description: Write and maintain changelogs following the Keep a Changelog convention. Use when creating a CHANGELOG.md, adding entries for a release, or reviewing changelog format and completeness.
license: MIT
metadata:
  author: kjanat
  version: "1.0"
---

# Changelog Writing

Write changelogs for humans, not machines. Follow the
[Keep a Changelog](https://keepachangelog.com/) convention.

## Format Rules

- File: `CHANGELOG.md` at project root
- Date format: ISO 8601 (`YYYY-MM-DD`)
- Latest version first (reverse chronological)
- One entry per version, every version documented
- Follow [Semantic Versioning](https://semver.org/)
- Version headings are linkable (comparison URLs at bottom)

## Change Categories

Group changes under these headings, in this order:

| Category     | Use for                            |
| ------------ | ---------------------------------- |
| `Added`      | New features                       |
| `Changed`    | Changes to existing functionality  |
| `Deprecated` | Features marked for future removal |
| `Removed`    | Features removed in this release   |
| `Fixed`      | Bug fixes                          |
| `Security`   | Vulnerability patches              |

Omit empty categories. Never invent new category names.

## Unreleased Section

Always keep an `## [Unreleased]` section at the top:

```markdown
## [Unreleased]

### Added

- New user profile endpoint.
```

At release time, move Unreleased entries into a new versioned heading.

## Version Heading Format

```markdown
## [1.2.0] - 2025-08-15
```

Yanked releases append `[YANKED]`:

```markdown
## [1.1.0] - 2025-07-01 [YANKED]
```

## Comparison Links

At the bottom of the file, define diff links for every version:

```markdown
[Unreleased]: https://github.com/org/repo/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/org/repo/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/org/repo/releases/tag/v1.1.0
```

## Anti-Patterns

| Don't                      | Why                                         |
| -------------------------- | ------------------------------------------- |
| Dump git log as changelog  | Noise: merge commits, docs changes, typos   |
| Skip deprecation notices   | Users can't prepare for breaking changes    |
| Use regional date formats  | Ambiguous (`01/02/03`). Use ISO 8601        |
| Document only some changes | Partial changelog is worse than none        |
| Use GitHub Releases alone  | Non-portable, less discoverable than a file |

## Writing Style

- Write entries as imperative statements from the user's perspective
- Focus on *what changed for the user*, not implementation details
- Be specific: "Add dark mode toggle in settings" not "Update UI"
- Group related changes into a single entry when appropriate

## Reading Order

| Task                 | Files to Read           |
| -------------------- | ----------------------- |
| Create new CHANGELOG | SKILL.md + example.md   |
| Add release entries  | SKILL.md (categories)   |
| Review format        | SKILL.md (format rules) |
| See full example     | example.md              |

## In This Reference

| File                                | Purpose                    |
| ----------------------------------- | -------------------------- |
| [example.md](references/example.md) | Complete example changelog |
