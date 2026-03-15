---
name: semver-release
description: 'Automated version release workflow. Analyzes git commit history to infer semantic version, auto-detects version files across ecosystems, updates multilingual CHANGELOGs, creates git commit and tag. Use when: (1) user says "release", "publish version", "bump version", (2) user invokes /release command, (3) preparing to release a new version.'
argument-hint: "[version]"
disable-model-invocation: true
allowed-tools: Bash(git *), Glob, Read, Edit, Write, AskUserQuestion
---

# Versioning Workflow

Automated version release based on [Semantic Versioning 2.0.0](https://semver.org/).

## Execution Steps

### Step 0: Pre-flight Checks

1. Verify inside a git repository: `git rev-parse --is-inside-work-tree`
2. Check working directory is clean: `git status --porcelain`
   - **Abort if** uncommitted changes exist → prompt user to commit or stash first
3. Detect current branch: `git branch --show-current`
   - Store for use in Step 8 completion message

### Step 1: Project Configuration Detection

#### 1a: Detect Version Files

Scan the project root for version files. Check these common files first:

| File | Ecosystem |
|------|-----------|
| `package.json` | Node.js |
| `pyproject.toml` | Python |
| `Cargo.toml` | Rust |
| `pubspec.yaml` | Dart / Flutter |
| `VERSION` | Universal |

Also check for: `pom.xml`, `build.gradle(.kts)`, `*.gemspec`, `setup.py`, `setup.cfg`, `*.csproj`, `CMakeLists.txt`.

For complete extraction and update patterns for each file type, see [references/version-files.md](references/version-files.md).

If no version files are found, ask the user which file contains the version, or skip version file updates.

If multiple version files are found, all will be updated to maintain consistency.

#### 1b: Discover CHANGELOG Files

Detect CHANGELOG files in the project root:

1. Check if `CHANGELOG.md` exists — mark as primary (do NOT create yet; defer to Step 7)
2. Glob for `CHANGELOG-*.md` and `CHANGELOG.*.md` to discover multilingual variants

Examples: `CHANGELOG.zh-CN.md`, `CHANGELOG-ja.md`, `CHANGELOG.fr.md`

All discovered CHANGELOG files will be updated.

### Step 2: Get Last Version Tag

#### 2a: Find Latest Semver Tag

Find the latest semver tag reachable from HEAD:

```bash
git tag -l 'v[0-9]*.[0-9]*.[0-9]*' --sort=-v:refname | head -1
```

This filters for `vMAJOR.MINOR.PATCH` pattern only, ignoring non-version tags (e.g. `deploy-prod`, `build-123`).

If no matching tags exist, also try without `v` prefix:

```bash
git tag -l '[0-9]*.[0-9]*.[0-9]*' --sort=-v:refname | head -1
```

Use `v0.0.0` as baseline if no semver tags exist at all.

#### 2b: Version Consistency Check

Compare the version from the latest git tag with versions found in version files (Step 1a).

- **If consistent** → proceed with tag version as baseline
- **If mismatch** → report discrepancy to user:
  ```
  Version mismatch detected:
  - Git tag: v1.2.0
  - package.json: 1.3.0
  ```
  Ask user which version to use as the baseline. **Do not proceed silently.**

### Step 3: Analyze Commit History

Use the latest tag obtained in Step 2a as the range start:

```bash
git log v1.2.3..HEAD --pretty=format:"---commit---%n%s%n%b"
```

Parse **both subject and body** of each commit to identify type:

| Pattern | Location | Type | Version Impact |
|---------|----------|------|----------------|
| `BREAKING CHANGE:` in body/footer | body | breaking | MAJOR |
| `type(scope)!:` (exclamation before colon) | subject | breaking | MAJOR |
| `feat:` / `feat(scope):` / `✨ feat:` | subject | feat | MINOR |
| `fix:` / `fix(scope):` / `🐛 fix:` | subject | fix | PATCH |
| `perf:` / `perf(scope):` / `⚡️ perf:` | subject | perf | PATCH |
| `refactor:` / `refactor(scope):` / `♻️ refactor:` | subject | refactor | PATCH |
| `docs:` / `📝 docs:` | subject | docs | none |
| `chore:` / `🔧 chore:` / `⬆️ deps:` | subject | chore | none |

**If no commits found** → inform user there are no changes since the last release. Ask whether to abort or force a release.

### Step 4: Calculate New Version

**User override**: If `$ARGUMENTS` is a valid semver version (e.g. `1.0.0`, `2.0.0-rc.1`), use that version directly. Skip automatic calculation.

Based on current version `MAJOR.MINOR.PATCH`:

**When MAJOR ≥ 1** (stable API):

- Has breaking → `(MAJOR+1).0.0`
- Has feat → `MAJOR.(MINOR+1).0`
- Has fix/perf/refactor → `MAJOR.MINOR.(PATCH+1)`
- Only docs/chore → Ask user whether to force patch release

**When MAJOR = 0** (unstable / initial development):

- Has breaking → `0.(MINOR+1).0` (not 1.0.0)
- Has feat → `0.MINOR.(PATCH+1)`
- Has fix/perf/refactor → `0.MINOR.(PATCH+1)`
- Only docs/chore → Ask user whether to force patch release
- **Note**: Ask user "Do you want to promote to 1.0.0?" if breaking changes detected

Pre-release versions (e.g. `1.0.0-rc.1`) are only created via explicit user override.

### Step 5: Generate CHANGELOG Content

Read `[Unreleased]` section from each detected CHANGELOG file.

Merge git analysis with existing [Unreleased] content:
- Check for missing changes from git commits
- Deduplicate by semantic meaning
- Add missing changes to appropriate categories

Organize by category (include only non-empty categories):

```markdown
### Added
- ✨ New feature

### Changed
- ♻️ Refactor/improvement
- ⚡️ Performance optimization
- ⚠️ 💥 Breaking change

### Deprecated
- Deprecated feature

### Removed
- 🗑️ Removed feature

### Fixed
- 🐛 Bug fix

### Security
- 🔒️ Security fix
```

For complete category mapping and translation rules, see [references/changelog-categories.md](references/changelog-categories.md).

**Scope handling**: If commits include scopes (e.g. `feat(auth):`), include the scope as context in the CHANGELOG entry where it aids readability:
- `feat(auth): add OAuth login` → `✨ **auth**: Add OAuth login`
- If scope adds no value (e.g. generic scope), omit it.

**Translation rules for multilingual CHANGELOGs**:
- Emoji prefixes — identical across all languages
- Category headings — keep in English (`### Added`, etc.)
- Entry descriptions — translate to the target language
- Technical terms and proper nouns — preserve as-is

### Step 6: Interactive Preview

Show user all planned changes:

```
## Release Preview

Current version: v1.5.1
New version: v1.6.0

### Version Files to Update
- package.json: 1.5.1 → 1.6.0
- pyproject.toml: 1.5.1 → 1.6.0

### CHANGELOG Files to Update
- CHANGELOG.md (English)
- CHANGELOG.zh-CN.md (Chinese)

### Changes (English)

## [1.6.0] - 2026-02-12

### Added
- ✨ Add release skill for automated versioning

### Changes (中文)

## [1.6.0] - 2026-02-12

### Added
- ✨ 添加 release 技能用于自动化版本发布

Confirm release? (y/n)
```

Use AskUserQuestion tool to request user confirmation.

### Step 7: Execute Changes

After user confirmation, execute in order:

#### 7a: Update Version Files

Modify version in ALL detected version files using file-specific update patterns from [references/version-files.md](references/version-files.md).

#### 7b: Update CHANGELOG Files

For each detected CHANGELOG file:
- Move `[Unreleased]` content to new version section `[x.y.z] - YYYY-MM-DD`
- Create new empty `[Unreleased]` section

If `CHANGELOG.md` does not exist, create it now with the new version section.

#### 7c: Git Operations

Stage all version files and CHANGELOG files modified in Steps 7a–7b by name, then commit and tag:

```bash
git add package.json pyproject.toml CHANGELOG.md CHANGELOG.zh-CN.md
git commit -m "🔖 release: vX.Y.Z"
git tag -a vX.Y.Z -m "Release vX.Y.Z"
```

Replace the file list and version with actual values. Use **annotated tag** (`-a`) — includes author, date, and message. Required by `git push --follow-tags` and better supported by GitHub/GitLab Releases.

#### Failure Recovery

**If `git commit` fails** (e.g. pre-commit hook):
1. Check what went wrong: `git status`
2. All file modifications are still staged — fix the issue and create a **new** commit (do NOT use `--amend`)
3. If the user wants to abort entirely, restore all modified files:
   ```bash
   git checkout -- package.json pyproject.toml CHANGELOG.md
   ```
   Replace the file list with the actual files modified in Steps 7a–7b.

**If `git tag` fails** (e.g. tag already exists):
1. The commit has already been created — do NOT undo it
2. Report the error to the user
3. Suggest: `git tag -d vX.Y.Z` to remove the old tag, then retry

### Step 8: Completion Message

Use the branch name detected in Step 0 and the publish command matching the detected ecosystem. Example:

```
Version vX.Y.Z released successfully!

Updated files:
- package.json (1.5.1 → 1.6.0)
- pyproject.toml (1.5.1 → 1.6.0)
- CHANGELOG.md
- CHANGELOG.zh-CN.md

Next steps:
- git push origin main --follow-tags
- npm publish
```

Replace branch name, version, file list, and publish command with actual values. Use `--follow-tags` to push commit and annotated tag in a single command.

Ecosystem-specific publish commands:

| Ecosystem | Publish Command |
|-----------|----------------|
| Node.js | `npm publish` / `pnpm publish` |
| Python | `twine upload dist/*` |
| Rust | `cargo publish` |
| Dart/Flutter | `dart pub publish` / `flutter pub publish` |
| Java (Maven) | `mvn deploy` |
| Java (Gradle) | `./gradlew publish` |
| Ruby | `gem push *.gem` |
| .NET | `dotnet nuget push` |
