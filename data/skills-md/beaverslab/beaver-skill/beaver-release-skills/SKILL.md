---
name: beaver-release-skills
description: Universal release workflow. Auto-detects version files and changelogs. Supports Node.js, Python, Rust, Claude Plugin, and generic projects. Use when user says "release", "发布", "new version", "bump version", "push", "推送".
---

# Release Skills

Universal release workflow supporting any project type with multi-language changelog.

## Quick Start

Just run `/beaver-release-skills` - auto-detects your project configuration.

## Supported Projects

| Project Type | Version File | Auto-Detected |
|--------------|--------------|---------------|
| Node.js | package.json | ✓ |
| Python | pyproject.toml | ✓ |
| Rust | Cargo.toml | ✓ |
| Claude Plugin | marketplace.json | ✓ |
| Generic | VERSION / version.txt | ✓ |

## Options

| Flag | Description |
|------|-------------|
| `--dry-run` | Preview changes without executing |
| `--major` | Force major version bump |
| `--minor` | Force minor version bump |
| `--patch` | Force patch version bump |

## Workflow

### Step 1: Detect Project Configuration

1. Check for `.releaserc.yml` (optional config override)
2. Auto-detect version file by scanning (priority order):
   - `package.json` (Node.js)
   - `pyproject.toml` (Python)
   - `Cargo.toml` (Rust)
   - `marketplace.json` or `.claude-plugin/marketplace.json` (Claude Plugin)
   - `VERSION` or `version.txt` (Generic)
3. Scan for changelog files using glob patterns:
   - `CHANGELOG*.md`
   - `HISTORY*.md`
   - `CHANGES*.md`
4. Identify language of each changelog by filename suffix
5. Display detected configuration

**Language Detection Rules**:

| Filename Pattern | Language |
|------------------|----------|
| `CHANGELOG.md` (no suffix) | zh (default) |
| `CHANGELOG.en.md` / `CHANGELOG_EN.md` | en |
| `CHANGELOG.ja.md` / `CHANGELOG_JP.md` | ja |
| `CHANGELOG.ko.md` / `CHANGELOG_KR.md` | ko |
| `CHANGELOG.de.md` / `CHANGELOG_DE.md` | de |
| `CHANGELOG.fr.md` / `CHANGELOG_FR.md` | fr |
| `CHANGELOG.es.md` / `CHANGELOG_ES.md` | es |
| `CHANGELOG.{lang}.md` | Corresponding language code |

**Output Example**:
```
Project detected:
  Version file: package.json (1.2.3)
  Changelogs:
    - CHANGELOG.md (zh)
    - CHANGELOG.en.md (en)
    - CHANGELOG.ja.md (ja)
```

### Step 2: Analyze Changes Since Last Tag

```bash
LAST_TAG=$(git tag --sort=-v:refname | head -1)
if [ -z "$LAST_TAG" ]; then
  echo "No tags found. Treating all commits as unreleased."
  git log --oneline
else
  git log ${LAST_TAG}..HEAD --oneline
  git diff ${LAST_TAG}..HEAD --stat
fi
```

If no tags exist, treat all commits on the current branch as unreleased changes. The initial release version defaults to the version already present in the version file (e.g. `package.json`).

Categorize by conventional commit types:

| Type | Description |
|------|-------------|
| feat | New features |
| fix | Bug fixes |
| docs | Documentation |
| refactor | Code refactoring |
| perf | Performance improvements |
| test | Test changes |
| style | Formatting, styling |
| chore | Maintenance (skip in changelog) |

**Breaking Change Detection**:
- Commit message starts with `BREAKING CHANGE`
- Commit body/footer contains `BREAKING CHANGE:`
- Removed public APIs, renamed exports, changed interfaces

If breaking changes detected, warn user: "Breaking changes detected. Consider major version bump (--major flag)."

### Step 3: Determine Version Bump

Rules (in priority order):
1. User flag `--major/--minor/--patch` → Use specified
2. BREAKING CHANGE detected → Major bump (1.x.x → 2.0.0)
3. `feat:` commits present → Minor bump (1.2.x → 1.3.0)
4. Otherwise → Patch bump (1.2.3 → 1.2.4)

Display version change: `1.2.3 → 1.3.0`

### Step 4: Generate Multi-language Changelogs

For each detected changelog file:

1. **Identify language** from filename suffix
2. **Detect third-party contributors** (requires `gh` CLI; skip if unavailable):
   - Check merge commits: `git log ${LAST_TAG}..HEAD --merges --pretty=format:"%H %s"`
   - For each merged PR, identify the PR author via `gh pr view <number> --json author --jq '.author.login'`
   - Compare against repo owner (`gh repo view --json owner --jq '.owner.login'`)
   - If PR author ≠ repo owner → third-party contributor
   - **Fallback**: If `gh` is not installed or not authenticated, skip contributor detection and omit `(by @username)` attributions. This does not block the release.
3. **Generate content in that language**:
   - Section titles in target language
   - Change descriptions written naturally in target language (not translated)
   - Date format: YYYY-MM-DD (universal)
   - **Third-party contributions**: Append contributor attribution `(by @username)` to the changelog entry
4. **Insert at file head** (preserve existing content)

**Section title translations, changelog format, attribution rules, and multi-language examples**: See [references/changelog-i18n.md](references/changelog-i18n.md).

### Step 5: Group Changes by Skill/Module

**Applicability check**: Only run this step if the project has a `skills/` directory. For standard single-package projects (Python, Rust, generic), skip Steps 5–6 and proceed directly to Step 7, using a single release commit for all changes.

Analyze commits since last tag and group by affected skill/module:

1. **Identify changed files** per commit
2. **Group by skill/module**:
   - `skills/<skill-name>/*` → Group under that skill
   - Root files (CLAUDE.md, etc.) → Group as "project"
   - Multiple skills in one commit → Split into multiple groups
3. **For each group**, identify related README updates needed

**Example Grouping**:
```
beaver-image-gen:
  - feat: add new style options
  - fix: handle transparent backgrounds
  → README updates: options table

beaver-xhs-images:
  - refactor: improve panel layout algorithm
  → No README updates needed

project:
  - docs: update CLAUDE.md architecture section
```

### Step 6: Commit Each Skill/Module Separately

For each skill/module group (in order of changes):

1. **Check README updates needed**:
   - Scan `README*.md` for mentions of this skill/module
   - Verify options/flags documented correctly
   - Update usage examples if syntax changed
   - Update feature descriptions if behavior changed

2. **Stage and commit**:
   ```bash
   git add skills/<skill-name>/*
   git add README.md README.zh.md  # If updated for this skill
   git commit -m "<type>(<skill-name>): <meaningful description>"
   ```

3. **Commit message format**:
   - Use conventional commit format: `<type>(<scope>): <description>`
   - `<type>`: feat, fix, refactor, docs, perf, etc.
   - `<scope>`: skill name or "project"
   - `<description>`: Clear, meaningful description of changes

**Example Commits**:
```bash
git commit -m "feat(beaver-image-gen): add new style options"
git commit -m "fix(beaver-xhs-images): handle transparent backgrounds"
git commit -m "docs(project): update architecture documentation"
```

**Common README Updates Needed**:
| Change Type | README Section to Check |
|-------------|------------------------|
| New options/flags | Options table, usage examples |
| Renamed options | Options table, usage examples |
| New features | Feature description, examples |
| Breaking changes | Migration notes, deprecation warnings |
| Restructured internals | Architecture section (if exposed to users) |

### Step 7: Write Changelog and Update Version

Step 4 defines the changelog format and language rules. This step executes the actual file writes:

1. **Write changelog entries** into each detected changelog file (insert at head, preserve existing content)
2. **Update version file**:
   - Read version file (JSON/TOML/text)
   - Update version number
   - Write back (preserve formatting)

**Version Paths by File Type**:

| File | Path |
|------|------|
| package.json | `$.version` |
| pyproject.toml | `project.version` |
| Cargo.toml | `package.version` |
| marketplace.json | `$.metadata.version` |
| VERSION / version.txt | Direct content |

### Step 8: User Confirmation

Before creating the release commit, ask user to confirm:

**Use AskUserQuestion with two questions**:

1. **Version bump** (single select):
   - Show recommended version based on Step 3 analysis
   - Options: recommended (with label), other semver options
   - Example: `1.2.3 → 1.3.0 (Recommended)`, `1.2.3 → 1.2.4`, `1.2.3 → 2.0.0`

2. **Push to remote** (single select):
   - Options: "Yes, push after commit", "No, keep local only"

**Example Output Before Confirmation**:
```
Commits created:
  1. feat(beaver-image-gen): add new style options
  2. fix(beaver-xhs-images): handle transparent backgrounds
  3. docs(project): update architecture documentation

Changelog preview (zh):
  ## 1.3.0 - 2026-01-22
  ### 新功能
  - beaver-image-gen 新增风格选项
  ### 修复
  - beaver-xhs-images 修复背景透明处理问题

Ready to create release commit and tag.
```

### Step 9: Create Release Commit and Tag

After user confirmation:

1. **Stage version and changelog files**:
   ```bash
   git add <version-file>
   git add CHANGELOG*.md
   ```

2. **Create release commit**:
   ```bash
   git commit -m "chore: release v{VERSION}"
   ```

3. **Create tag**:
   ```bash
   git tag v{VERSION}
   ```

4. **Push if user confirmed** (Step 8):
   ```bash
   git push origin HEAD
   git push origin v{VERSION}
   ```

**Note**: Do NOT add Co-Authored-By line. This is a release commit, not a code contribution.

**Post-Release Output**:
```
Release v1.3.0 created.

Commits:
  1. feat(beaver-image-gen): add new style options
  2. fix(beaver-xhs-images): handle transparent backgrounds
  3. docs(project): update architecture documentation
  4. chore: release v1.3.0

Tag: v1.3.0
Status: Pushed to origin  # or "Local only - run git push when ready"
```

5. **Check CI status** (if pushed and `gh` is available):
   ```bash
   gh run list --limit 1
   ```
   If a CI workflow was triggered by the tag push (e.g. documentation builds or testing via GitHub Actions), display its status and URL so the user can monitor it. If `gh` is unavailable, remind the user to check the Actions tab manually.

## Configuration (.releaserc.yml)

Optional config file in project root to override defaults:

```yaml
# .releaserc.yml - Optional configuration

# Version file (auto-detected if not specified)
version:
  file: package.json
  path: $.version  # JSONPath for JSON, dotted path for TOML

# Changelog files (auto-detected if not specified)
changelog:
  files:
    - path: CHANGELOG.md
      lang: zh
    - path: CHANGELOG.en.md
      lang: en
    - path: CHANGELOG.ja.md
      lang: ja

  # Section mapping (conventional commit type → changelog section)
  # Use null to skip a type in changelog
  sections:
    feat: Features
    fix: Fixes
    docs: Documentation
    refactor: Refactor
    perf: Performance
    test: Tests
    chore: null

# Commit message format
commit:
  message: "chore: release v{version}"

# Tag format
tag:
  prefix: v  # Results in v1.0.0
  sign: false

# Additional files to include in release commit
include:
  - README.md
  - package.json
```

## Dry-Run Mode

When `--dry-run` is specified:

```
=== DRY RUN MODE ===

Project detected:
  Version file: package.json (1.2.3)
  Changelogs: CHANGELOG.md (zh), CHANGELOG.en.md (en)

Last tag: v1.2.3
Proposed version: v1.3.0

Changes grouped by skill/module:
  beaver-image-gen:
    - feat: add new style options
    - fix: handle transparent backgrounds
    → Commit: feat(beaver-image-gen): add new style options
    → README updates: options table

  beaver-xhs-images:
    - fix: handle transparent backgrounds
    → Commit: fix(beaver-xhs-images): handle transparent backgrounds
    → No README updates

Changelog preview (zh):
  ## 1.3.0 - 2026-01-22
  ### 新功能
  - beaver-image-gen 新增风格选项
  ### 修复
  - beaver-xhs-images 修复背景透明处理问题

Changelog preview (en):
  ## 1.3.0 - 2026-01-22
  ### Features
  - beaver-image-gen: add new style options
  ### Fixes
  - beaver-xhs-images: handle transparent backgrounds

Commits to create:
  1. feat(beaver-image-gen): add new style options
  2. fix(beaver-xhs-images): handle transparent backgrounds
  3. chore: release v1.3.0

No changes made. Run without --dry-run to execute.
```

## Example Usage

```
/beaver-release-skills              # Auto-detect version bump
/beaver-release-skills --dry-run    # Preview only
/beaver-release-skills --minor      # Force minor bump
/beaver-release-skills --patch      # Force patch bump
/beaver-release-skills --major      # Force major bump (with confirmation)
```

## When to Use

Trigger this skill when user requests:
- "release", "发布", "create release", "new version", "新版本"
- "bump version", "update version", "更新版本"
- "prepare release"
- "push to remote" (with uncommitted changes)

**Important**: If user says "just push" or "直接 push" with uncommitted changes, STILL follow all steps above first.