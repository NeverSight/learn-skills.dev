---
name: keepachangelog
description: How to write and maintain a CHANGELOG.md following the Keep a Changelog 1.1.0 format (https://keepachangelog.com/en/1.1.0/) - project-agnostic. Covers the six change categories, the Unreleased section, version/date headers, comparison links, and yanked releases. Use when creating a new CHANGELOG.md, adding an entry for a release, or reviewing one for format compliance.
---

# Keep a Changelog

A changelog is for the humans reading your release, not a dump of
`git log`. This is the spec at
[keepachangelog.com/en/1.1.0](https://keepachangelog.com/en/1.1.0/),
distilled into what to actually do.

## Guiding principles

- Changelogs are for **humans**, not machines — write what a person
  upgrading needs to know, not every commit.
- **One entry per version**, no exceptions — even a patch release gets
  a section, not silence.
- **Group by type of change** (see the six categories below) — don't
  interleave a bug fix and a new feature in one paragraph.
- **Versions and sections are linkable** — a reader (or a bug report)
  should be able to point at exactly `## [1.4.2]`, not "somewhere in
  the changelog."
- **Latest version first** — reverse-chronological, always.
- **Every version shows its release date** — `YYYY-MM-DD`, no
  relative dates ("last week").
- **Say whether you follow [Semantic Versioning](../semver/SKILL.md)**
  — usually a one-line note near the top of the file.

## The six categories

Use exactly these, only the ones that apply to a given version, in this
order:

| Category | For |
|---|---|
| `Added` | New features |
| `Changed` | Changes to existing functionality |
| `Deprecated` | Features that still work but will be removed |
| `Removed` | Features that were removed |
| `Fixed` | Bug fixes |
| `Security` | Vulnerability fixes — call these out even if they'd otherwise read as `Fixed`, so a reader scanning for security-relevant changes doesn't have to read every line |

## Structure

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Thing that landed on `main` but hasn't shipped in a release yet.

## [1.4.2] - 2026-03-14

### Fixed
- The bug, described from the user's point of view, not the diff's.

## [1.4.1] - 2026-02-28

### Added
- ...

[Unreleased]: https://github.com/org/repo/compare/v1.4.2...HEAD
[1.4.2]: https://github.com/org/repo/compare/v1.4.1...v1.4.2
[1.4.1]: https://github.com/org/repo/compare/v1.4.0...v1.4.1
```

**`[Unreleased]` stays at the top, always** — it's where
already-merged changes go the moment they land, before there's a
version number for them yet. At release time, rename it to the
new version + date and open a fresh empty `[Unreleased]` above it —
don't leave the previous release's changes mixed in with the next
one's.

**Version headers**: `## [X.Y.Z] - YYYY-MM-DD` — the version in
brackets (so it can carry a link reference), a literal ` - `, then the
release date.

**Comparison links** at the bottom, one per version, pointing at a
diff between that version's tag and the one before it (or `HEAD`
for `Unreleased`) — not required by the spec, but the practical
way to make "versions are linkable" actually useful on GitHub/GitLab.

## Yanked releases

A version pulled after release (a broken build; a security
issue) still gets an entry — don't delete it, that erases the
record of what happened:

```markdown
## [0.4.1] - 2026-01-09 [YANKED]

### Fixed
- ...
```

The `[YANKED]` tag is both human-visible and machine-parseable, so
tooling reading the changelog can skip it when picking a version to
install.

## What NOT to do

- Don't write `## [1.4.2] - 2026-03-14` and then just paste raw commit
  subjects underneath — a changelog entry describes the observable
  effect on someone using the software, not the internal diff.
- Don't skip a version's section because "it was just a dependency
  bump" — if it shipped, it gets an entry (even a one-line
  `Changed` note), or the "one entry per version" principle is broken.
- Don't backdate or guess a release date — use the date the
  version was actually tagged/published.
