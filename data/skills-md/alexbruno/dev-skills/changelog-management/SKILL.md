---
name: changelog-management
description: >-
  Maintain and update a standardized root `CHANGELOG.md` following Keep a
  Changelog and Semantic Versioning. Use this skill to initialize or update
  changelog entries, categorize changes, prepare release cuts, and proactively
  prompt the user when notable changes warrant updating the changelog.
---

# Changelog Management

Maintain a clean, human-readable record of notable changes at the repository root in `CHANGELOG.md`.

This skill enforces the widely adopted [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) standard and aligns with [Semantic Versioning (SemVer)](https://semver.org/spec/v2.0.0.html).

---

## Core Principles

1. **Root Location**: Always maintain the changelog in `CHANGELOG.md` at the project root. Initialize it from `./resources/CHANGELOG.md` if it does not exist yet.
2. **Written for Humans**: Changelogs are for people, not machines. Summarize user-facing, functional, or architectural impacts clearly; do not paste raw git commit logs.
3. **Always Track `[Unreleased]`**: Ongoing contributions are accumulated in the `## [Unreleased]` section at the top of the file before a release is cut.
4. **Standard Categories**: Group entries strictly under standard category headings (omit empty categories in published releases):
   - `### Added` — for new features and public capabilities.
   - `### Changed` — for changes in existing functionality.
   - `### Deprecated` — for features scheduled for removal in future releases.
   - `### Removed` — for features now removed.
   - `### Fixed` — for bug fixes.
   - `### Security` — for vulnerability remediations or security enhancements.

---

## Proactive Suggestion Triggers

The agent must proactively suggest updating `CHANGELOG.md` at opportunistic moments, rather than waiting for an explicit command:

### When to Suggest

- **Feature or Bugfix Completion**: After implementing or verifying a feature, bug fix, or behavioral change (e.g., when completing a vertical slice or signing off on `workflow/SPEC.md` / `workflow/PLAN.md`).
- **Breaking Changes or Deprecations**: Immediately upon modifying a public API, configuration schema, database contract, or CLI flag.
- **Pre-Commit / Pre-PR / Code Review**: During code review or before preparing a PR or commit that introduces notable changes.
- **Release Preparation**: When the user mentions tagging, publishing, or releasing a new version.

### Prompting Format

When a qualifying change occurs, offer a clear, ready-to-use proposal:

> *"I noticed we just implemented `<brief description of change>`. Would you like me to record this under `[Unreleased]` (`Added` / `Fixed` / `Changed`) in `CHANGELOG.md`?"*

### When NOT to Suggest (Avoid Noise)

Do **not** prompt the user or update `CHANGELOG.md` for:
- Routine internal refactorings that preserve behavior and interfaces.
- Typo corrections in internal comments or documentation.
- Test-only adjustments, benchmark tweaks, or local development tool configs (unless they affect consumers or project contributors significantly).

---

## Changelog Entry Guidelines

Each bullet under a category should follow these rules:

- **Imperative or descriptive summary**: Begin with a capitalized verb or concise summary (e.g., `- Add support for...`, `- Fix memory leak in...`, `- Deprecate legacy auth flag...`).
- **Link issues / PRs / contributors (if applicable)**: Append issue or PR references (e.g., `(#123)`) when known.
- **Highlight breaking changes**: Prefix breaking modifications explicitly with `**BREAKING:**` under `### Changed` or `### Removed`.

---

## Release Bumping Workflow

When cutting a release (e.g., from `Unreleased` to `v1.2.0`):

1. **Determine SemVer Level**:
   - `MAJOR` (`X.0.0`): One or more breaking changes.
   - `MINOR` (`0.X.0`): New backward-compatible features (`Added`).
   - `PATCH` (`0.0.X`): Backward-compatible bug fixes (`Fixed`).
2. **Transform `[Unreleased]`**:
   - Create a new header below `## [Unreleased]`: `## [X.Y.Z] - YYYY-MM-DD` (using current date in ISO format).
   - Move all accumulated bullets from `[Unreleased]` into the new release section.
   - Leave `## [Unreleased]` empty, ready for subsequent work.
3. **Compare Links (Optional)**:
   - If the repository uses GitHub/GitLab tag comparisons, update or append diff links at the bottom of `CHANGELOG.md` (e.g., `[Unreleased]: https://github.com/org/repo/compare/v1.2.0...HEAD`).
