---
name: changelog-generator
description: Generate changelogs from git commit history in multiple formats (Keep a Changelog, Conventional Changelog, grouped by date). Use when the user asks to 'generate changelog', 'create release notes', 'summarize commits', 'what changed since last release', or needs a CHANGELOG.md file created or updated. Triggers on any changelog, release notes, or commit summary task.
---

# Changelog Generator

Generate structured changelogs from git commit history. Supports Conventional Commits parsing, semantic grouping, and multiple output formats.

## Quick Start

Run the bundled script to generate a changelog:

```bash
python3 scripts/generate_changelog.py [--from TAG] [--to TAG] [--format FORMAT] [--output FILE]
```

Options:
- `--from`: Start ref (tag, commit, branch). Defaults to latest tag.
- `--to`: End ref. Defaults to HEAD.
- `--format`: Output format — `keepachangelog` (default), `conventional`, `grouped`.
- `--output`: Write to file instead of stdout. Use `CHANGELOG.md` for standard placement.
- `--version`: Custom version label for the header (e.g. `v1.3.0`). Defaults to `--to` ref.
- `--prepend`: Insert new entries into existing file below the H1 header (requires `--output`).
- `--no-merges`: Exclude merge commits.
- `--exclude-types`: Comma-separated commit types to skip (e.g. `chore,ci,test`).

## Format Selection

| Scenario | Recommended Format |
|----------|--------------------|
| Open-source library release | `keepachangelog` |
| Project using Conventional Commits | `conventional` |
| Internal team update / sprint summary | `grouped` |

## Workflow

1. Determine the commit range (user-specified tags, or auto-detect latest tag to HEAD)
2. Run `scripts/generate_changelog.py` with appropriate flags
3. Review the generated output for accuracy
4. If writing to CHANGELOG.md, prepend new entries above existing content

## Commit Parsing

The script parses Conventional Commits (`type(scope): description`) and groups them:

| Prefix | Category |
|--------|----------|
| `feat` | Added |
| `fix` | Fixed |
| `docs` | Documentation |
| `refactor`, `style` | Changed |
| `perf` | Performance |
| `test` | Tests |
| `chore`, `ci`, `build` | Maintenance |
| `revert` | Removed |
| `deprecate` | Deprecated |
| `security` | Security |
| `!` suffix or `BREAKING CHANGE` | Breaking Changes |

Non-conventional commits are grouped under "Other".

## Output Formats

For detailed format specifications and examples, see [references/formats.md](references/formats.md).

- **keepachangelog**: Follows Keep a Changelog spec. Best for libraries and open-source projects.
- **conventional**: Follows Conventional Changelog style. Best for projects using Conventional Commits.
- **grouped**: Simple date-grouped list. Best for internal projects or quick summaries.

## Edge Cases

- No tags found: Use first commit as `--from`.
- Merge commits: Included by default. Pass `--no-merges` to exclude.
- Empty range: Script exits with message, no output file written.
- Existing CHANGELOG.md: Use `--prepend` to insert above old entries instead of overwriting.

## Examples

```bash
# Generate changelog from latest tag to HEAD (default)
python3 scripts/generate_changelog.py

# Generate for a specific release
python3 scripts/generate_changelog.py --from v1.2.0 --to v1.3.0 --version v1.3.0

# Append to existing CHANGELOG.md
python3 scripts/generate_changelog.py --version v1.3.0 --output CHANGELOG.md --prepend

# Conventional format, no merge commits
python3 scripts/generate_changelog.py --format conventional --no-merges

# Exclude chore and ci commits
python3 scripts/generate_changelog.py --exclude-types chore,ci

# Quick internal summary grouped by date
python3 scripts/generate_changelog.py --format grouped --output release-notes.md
```
