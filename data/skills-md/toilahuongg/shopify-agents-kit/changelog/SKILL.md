---
name: changelog
description: Generate and maintain changelogs following Keep a Changelog format. Analyzes git commits, categorizes changes, and produces well-structured release notes.
context: user-invocable
argument-hint: "[version] [--since=tag] [--format=md|json]"
---

# Changelog Generator

This skill generates and maintains changelogs following the [Keep a Changelog](https://keepachangelog.com/) format, integrated with [Conventional Commits](https://www.conventionalcommits.org/) and Semantic Versioning.

## Quick Start

When invoked, analyze git history and generate/update the changelog:

```bash
# Get commits since last tag
git log $(git describe --tags --abbrev=0 2>/dev/null || echo "")..HEAD --pretty=format:"%h %s" --no-merges

# Get all tags for reference
git tag --sort=-version:refname | head -10
```

## Changelog Format (Keep a Changelog)

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New features

### Changed
- Changes in existing functionality

### Deprecated
- Soon-to-be removed features

### Removed
- Removed features

### Fixed
- Bug fixes

### Security
- Vulnerability fixes

## [1.1.0] - 2024-01-26

### Added
- New `zustand-state` skill for state management
- New `form-validation` skill with Zod + Conform integration
- New `security-hardening` skill for Shopify apps

### Changed
- Updated `shopify-developer` agent with new skills
- Updated `tech-lead` agent with security-hardening skill

## [1.0.4] - 2024-01-20

### Fixed
- Initial stable release

[Unreleased]: https://github.com/user/repo/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/user/repo/compare/v1.0.4...v1.1.0
[1.0.4]: https://github.com/user/repo/releases/tag/v1.0.4
```

## Conventional Commits Mapping

Map commit prefixes to changelog categories:

| Commit Prefix | Changelog Category |
|---------------|-------------------|
| `feat:` | **Added** |
| `fix:` | **Fixed** |
| `docs:` | **Changed** (Documentation) |
| `style:` | **Changed** (Formatting) |
| `refactor:` | **Changed** |
| `perf:` | **Changed** (Performance) |
| `test:` | (Usually omitted) |
| `build:` | **Changed** (Build system) |
| `ci:` | (Usually omitted) |
| `chore:` | (Usually omitted) |
| `revert:` | **Removed** or **Fixed** |
| `security:` / `vuln:` | **Security** |
| `deprecate:` | **Deprecated** |
| `remove:` / `breaking:` | **Removed** |

## Generation Process

### Step 1: Analyze Git History

```bash
# Get commits since last release
git log v1.0.4..HEAD --pretty=format:"%H|%s|%an|%ad" --date=short

# Or since a specific date
git log --since="2024-01-01" --pretty=format:"%H|%s|%an|%ad" --date=short
```

### Step 2: Categorize Changes

Parse each commit message and categorize:

```typescript
interface ChangeEntry {
  category: 'Added' | 'Changed' | 'Deprecated' | 'Removed' | 'Fixed' | 'Security';
  description: string;
  commit: string;
  scope?: string;
  breaking?: boolean;
}

function categorizeCommit(message: string): ChangeEntry | null {
  const conventionalRegex = /^(\w+)(?:\(([^)]+)\))?(!)?:\s*(.+)$/;
  const match = message.match(conventionalRegex);

  if (!match) return null;

  const [, type, scope, breaking, description] = match;

  const categoryMap: Record<string, ChangeEntry['category']> = {
    feat: 'Added',
    fix: 'Fixed',
    docs: 'Changed',
    style: 'Changed',
    refactor: 'Changed',
    perf: 'Changed',
    security: 'Security',
    deprecate: 'Deprecated',
    remove: 'Removed',
  };

  return {
    category: categoryMap[type] || 'Changed',
    description,
    scope,
    breaking: !!breaking,
  };
}
```

### Step 3: Generate Markdown

```typescript
function generateChangelog(entries: ChangeEntry[], version: string, date: string): string {
  const grouped = groupBy(entries, 'category');
  const order = ['Added', 'Changed', 'Deprecated', 'Removed', 'Fixed', 'Security'];

  let output = `## [${version}] - ${date}\n\n`;

  for (const category of order) {
    if (grouped[category]?.length) {
      output += `### ${category}\n`;
      for (const entry of grouped[category]) {
        const scope = entry.scope ? `**${entry.scope}:** ` : '';
        const breaking = entry.breaking ? '⚠️ BREAKING: ' : '';
        output += `- ${breaking}${scope}${entry.description}\n`;
      }
      output += '\n';
    }
  }

  return output;
}
```

## Version Determination

Based on changes, suggest version bump:

| Change Type | Version Bump | Example |
|-------------|--------------|---------|
| Breaking changes (`!`) | **MAJOR** | 1.0.0 → 2.0.0 |
| New features (`feat`) | **MINOR** | 1.0.0 → 1.1.0 |
| Bug fixes (`fix`) | **PATCH** | 1.0.0 → 1.0.1 |
| Other changes | **PATCH** | 1.0.0 → 1.0.1 |

```typescript
function suggestVersionBump(entries: ChangeEntry[], currentVersion: string): string {
  const [major, minor, patch] = currentVersion.split('.').map(Number);

  if (entries.some(e => e.breaking)) {
    return `${major + 1}.0.0`;
  }
  if (entries.some(e => e.category === 'Added')) {
    return `${major}.${minor + 1}.0`;
  }
  return `${major}.${minor}.${patch + 1}`;
}
```

## Workflow Integration

### Pre-release Workflow

```bash
# 1. Generate changelog for unreleased changes
git log $(git describe --tags --abbrev=0)..HEAD --oneline

# 2. Update CHANGELOG.md with new version section

# 3. Commit changelog
git add CHANGELOG.md
git commit -m "docs: update changelog for v1.2.0"

# 4. Create version tag
git tag -a v1.2.0 -m "Release v1.2.0"

# 5. Push with tags
git push --follow-tags
```

### GitHub Release Integration

Generate release notes for GitHub:

```bash
# Extract latest version section from CHANGELOG.md
sed -n '/^## \[1\.2\.0\]/,/^## \[/p' CHANGELOG.md | head -n -1

# Create GitHub release
gh release create v1.2.0 --title "v1.2.0" --notes-file release-notes.md
```

## Output Formats

### Markdown (Default)

Standard Keep a Changelog format as shown above.

### JSON

```json
{
  "version": "1.1.0",
  "date": "2024-01-26",
  "changes": {
    "added": [
      "New `zustand-state` skill for state management",
      "New `form-validation` skill with Zod + Conform integration"
    ],
    "changed": [
      "Updated `shopify-developer` agent with new skills"
    ],
    "fixed": [],
    "security": []
  }
}
```

### Release Notes (Simplified)

```markdown
# Release v1.1.0

## Highlights
- 🎉 3 new skills added for better Shopify development

## What's New
- **zustand-state**: State management with Zustand
- **form-validation**: Form validation with Zod + Conform
- **security-hardening**: Security best practices

## Improvements
- Updated agents with new skill integrations

---
Full changelog: https://github.com/user/repo/blob/main/CHANGELOG.md
```

## Best Practices

### DO
- ✅ Write changelogs for humans, not machines
- ✅ Use present tense ("Add feature" not "Added feature")
- ✅ Group changes by type (Added, Changed, Fixed, etc.)
- ✅ Include links to issues/PRs when relevant
- ✅ Highlight breaking changes prominently
- ✅ Keep entries concise but descriptive

### DON'T
- ❌ Include every single commit (filter noise)
- ❌ Use technical jargon without explanation
- ❌ Forget to update [Unreleased] section
- ❌ Mix different versions in one section
- ❌ Skip security-related changes

## Commands Reference

```bash
# View commits since last tag
git log $(git describe --tags --abbrev=0)..HEAD --oneline

# View commits between two tags
git log v1.0.0..v1.1.0 --oneline

# Get commit count by type
git log --oneline | grep -E "^[a-f0-9]+ (feat|fix|docs):" | wc -l

# List all contributors since last release
git log $(git describe --tags --abbrev=0)..HEAD --format="%an" | sort -u

# Generate commit list with dates
git log --since="2024-01-01" --pretty=format:"- %s (%ad)" --date=short
```

## Example Invocations

```
/changelog                    # Generate for unreleased changes
/changelog 1.2.0              # Generate for specific version
/changelog --since=v1.0.0     # Changes since specific tag
/changelog --format=json      # Output as JSON
```
