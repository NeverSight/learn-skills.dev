---
name: version-management
description: Maintains versions of skills, prompts, or documents. Provides version tagging, release management, changelogs, and rollback capabilities. Tracks changes to SKILL.md files, scripts, and resources using git-based version control with semantic versioning.
---

# Version Management Skill

A comprehensive version management system for skills, prompts, and documents in Claude Code. This skill provides professional version control capabilities including tagging releases, maintaining changelogs, and rolling back to previous versions when needed.

## Overview

This skill enables you to:
- **Tag releases** with semantic versioning (v1.0.0, v1.1.0, etc.)
- **Store changelogs** documenting changes between versions
- **Roll back** to previous versions if new instructions cause errors
- **Track changes** to SKILL.md, scripts, and resource files
- **Compare versions** to understand what changed
- **Archive versions** for long-term storage

## Core Concepts

### Version Format
Uses semantic versioning: `MAJOR.MINOR.PATCH`
- **MAJOR**: Breaking changes or complete rewrites
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, minor improvements

### Storage Structure
```
skills/<skill-name>/
├── SKILL.md                      # Current version
├── .versions/                    # Version history
│   ├── v1.0.0/
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   └── metadata.json
│   ├── v1.1.0/
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   └── metadata.json
│   └── CHANGELOG.md              # Complete change history
└── scripts/                      # Current scripts
```

### Metadata Format
Each version stores metadata in `metadata.json`:
```json
{
  "version": "1.0.0",
  "timestamp": "2025-11-18T12:00:00Z",
  "author": "Claude <noreply@anthropic.com>",
  "commit": "abc123...",
  "description": "Initial release with core functionality",
  "changes": [
    "Added version tagging",
    "Implemented rollback mechanism",
    "Created changelog template"
  ],
  "files_tracked": [
    "SKILL.md",
    "scripts/version_manager.sh"
  ]
}
```

## Workflow

### 1. Initialize Version Management for a Skill

**Input:**
- Skill name or path
- Initial version number (default: 0.1.0)

**Actions:**
1. Check if skill exists
2. Create `.versions/` directory
3. Create initial version snapshot
4. Initialize CHANGELOG.md
5. Create metadata.json

**Output:**
- Confirmation message with version number
- Location of version storage

### 2. Create New Version/Tag

**Input:**
- Skill name
- Version number or bump type (major/minor/patch)
- Description of changes
- Optional: List of specific changes

**Actions:**
1. Validate version number format
2. Check if version already exists
3. Create version directory
4. Copy current SKILL.md and scripts
5. Generate metadata.json
6. Update CHANGELOG.md
7. Create git tag (if in git repo)
8. Commit changes

**Output:**
- Version tag created: `v1.2.0`
- Changelog entry added
- Files tracked: [list]

### 3. List All Versions

**Input:**
- Skill name
- Optional: Filter by date range or version pattern

**Actions:**
1. Read `.versions/` directory
2. Parse metadata.json for each version
3. Sort by version number or date
4. Format output table

**Output:**
```
Version History for 'session-start-hook':

v1.2.0 | 2025-11-18 12:00 | Added validation for linters
v1.1.0 | 2025-11-15 10:30 | Improved error handling
v1.0.0 | 2025-11-10 09:00 | Initial release
```

### 4. Show Version Details

**Input:**
- Skill name
- Version number

**Actions:**
1. Locate version directory
2. Read metadata.json
3. Display comprehensive information
4. Show file changes from previous version

**Output:**
```
Version: v1.2.0
Date: 2025-11-18 12:00:00Z
Author: Claude <noreply@anthropic.com>
Commit: abc123def456

Description:
Added validation for linters and improved test coverage

Changes:
- Added lint validation step
- Improved error messages
- Updated documentation

Files Modified:
- SKILL.md (+45 lines, -12 lines)
- scripts/validator.sh (new file)
```

### 5. Compare Two Versions

**Input:**
- Skill name
- Version A (e.g., v1.0.0)
- Version B (e.g., v1.2.0)
- Optional: Specific file to compare

**Actions:**
1. Load both versions
2. Perform diff on SKILL.md and scripts
3. Highlight changes
4. Show metadata differences

**Output:**
- Unified diff format
- Summary of changes
- Changelog entries between versions

### 6. Roll Back to Previous Version

**Input:**
- Skill name
- Target version number
- Optional: Create backup of current version

**Actions:**
1. **CRITICAL**: Create backup of current state
2. Verify target version exists
3. Confirm rollback with user
4. Copy files from target version to current
5. Update metadata
6. Log rollback in CHANGELOG
7. Create git commit

**Output:**
- Rollback successful: `v1.2.0` → `v1.0.0`
- Backup created at: `.versions/backup-2025-11-18-120000/`
- Changes reverted: [list]

**Safety Checks:**
- Always create backup before rollback
- Require explicit confirmation
- Verify file integrity
- Test rolled-back version if possible

### 7. Update Changelog

**Input:**
- Skill name
- Version number
- Change entries
- Optional: Category (Added/Changed/Fixed/Removed)

**Actions:**
1. Read current CHANGELOG.md
2. Add new entries under version heading
3. Format according to Keep a Changelog standard
4. Update timestamp
5. Save changes

**Output:**
- Changelog updated for version `v1.2.0`
- 3 entries added under "Added" category

### 8. Export Version Archive

**Input:**
- Skill name
- Version number or "all"
- Output format (tar.gz/zip)
- Destination path

**Actions:**
1. Collect version files
2. Include metadata and changelog
3. Create archive
4. Verify integrity
5. Generate checksum

**Output:**
- Archive created: `session-start-hook-v1.2.0.tar.gz`
- Size: 45 KB
- SHA256: abc123...
- Location: `/path/to/archive`

## Change Detection

The skill automatically tracks changes to:

### Monitored Files
- **SKILL.md**: Main skill definition
- **scripts/**: All executable scripts
- **templates/**: Template files
- **resources/**: Additional resources

### Change Types Detected
- **Content changes**: Line additions/deletions
- **New files**: Files added to skill directory
- **Deleted files**: Files removed
- **Renamed files**: File moves/renames
- **Permission changes**: Executable bit changes

### Detection Method
```bash
# Compare against previous version
git diff v1.0.0..v1.1.0 -- skills/skill-name/

# Track specific files
git log --follow -- skills/skill-name/SKILL.md
```

## Error Recovery

### Common Issues and Solutions

**Issue**: Rollback fails due to corrupted version
**Solution**:
1. Check `.versions/` directory for intact versions
2. Use next-most-recent stable version
3. Restore from git history if available

**Issue**: Version tag already exists
**Solution**:
1. List existing versions
2. Increment version number
3. Or use `--force` flag to overwrite (dangerous)

**Issue**: Changelog merge conflict
**Solution**:
1. Export current changelog
2. Restore from version history
3. Manually merge entries
4. Validate format

## Integration with Git

### Git Tag Creation
```bash
# Create annotated tag
git tag -a v1.2.0 -m "Version 1.2.0: Added validation"

# Push tag to remote
git push origin v1.2.0
```

### Branch-Based Versioning
- Development: `claude/version-mgmt-<session-id>`
- Releases: Tagged commits on main branch
- Hotfixes: Patch version bumps

### Commit Messages
```
feat(version-mgmt): Add rollback capability

- Implement version rollback with safety checks
- Add backup creation before rollback
- Update changelog automatically

Version: v1.2.0
Skill: version-management
```

## Best Practices

### When to Create Versions

**Always version when:**
- Making breaking changes to skill behavior
- Adding new major features
- Before deploying to production
- After significant testing/validation
- Completing a milestone

**Consider versioning when:**
- Fixing bugs
- Improving documentation
- Refactoring code
- Updating dependencies

**Skip versioning for:**
- Typo fixes
- Comment updates
- Formatting changes

### Version Numbering Guidelines

**Bump MAJOR (1.0.0 → 2.0.0):**
- Incompatible API changes
- Complete skill rewrite
- Breaking changes to workflow

**Bump MINOR (1.0.0 → 1.1.0):**
- New features added
- New workflow steps
- Backward-compatible enhancements

**Bump PATCH (1.0.0 → 1.0.1):**
- Bug fixes
- Documentation improvements
- Minor tweaks

### Changelog Writing

Follow [Keep a Changelog](https://keepachangelog.com/) format:

```markdown
## [1.2.0] - 2025-11-18

### Added
- New rollback safety checks
- Automatic backup creation
- Version comparison feature

### Changed
- Improved error messages in validator
- Updated documentation structure

### Fixed
- Rollback file permission issues
- Changelog formatting errors

### Removed
- Deprecated legacy backup format
```

## Example Usage Scenarios

### Scenario 1: Version a New Skill

```
User: I've created a new skill called 'code-reviewer'. Please version it.

Claude: I'll initialize version management for the 'code-reviewer' skill.

1. Creating version structure
2. Taking initial snapshot as v0.1.0
3. Initializing CHANGELOG.md
4. Creating metadata

✓ Version v0.1.0 created for 'code-reviewer'
✓ Tracking: SKILL.md, scripts/reviewer.sh
✓ Changelog initialized

Next steps:
- Make improvements to your skill
- When ready, create v1.0.0 for first stable release
```

### Scenario 2: Create Release After Updates

```
User: I've updated the code-reviewer skill. Tag it as v1.0.0.

Claude: I'll create version v1.0.0 for 'code-reviewer'.

Detected changes:
- SKILL.md: +67 lines, -23 lines
- scripts/reviewer.sh: +145 lines (new)
- scripts/analyzer.py: +89 lines (new)

Please provide a description of changes:

User: Added Python code analysis and improved markdown documentation

Claude: Creating version v1.0.0...

✓ Version snapshot created
✓ Metadata saved
✓ Changelog updated
✓ Git tag created: v1.0.0

Version v1.0.0 Summary:
- Description: Added Python code analysis and improved markdown documentation
- Files tracked: 3
- Total changes: +301 lines, -23 lines
- Date: 2025-11-18 12:30:00Z
```

### Scenario 3: Rollback After Error

```
User: The new version v1.1.0 is causing errors. Roll back to v1.0.0.

Claude: I'll initiate rollback from v1.1.0 to v1.0.0 for 'code-reviewer'.

⚠️  WARNING: This will replace current files with v1.0.0

Rollback plan:
1. Create backup of current state
2. Restore files from v1.0.0
3. Update metadata
4. Log rollback in changelog
5. Create git commit

Proceed with rollback? (yes/no)

User: yes

Claude: Executing rollback...

✓ Backup created: .versions/backup-2025-11-18-123000/
✓ Files restored from v1.0.0
✓ SKILL.md restored
✓ scripts/ restored
✓ Metadata updated
✓ Changelog entry added
✓ Git commit created

Rollback successful!
Current version: v1.0.0
Backup location: .versions/backup-2025-11-18-123000/

You can now fix the issues and create v1.1.1.
```

### Scenario 4: Compare Versions

```
User: Show me what changed between v1.0.0 and v1.2.0

Claude: Comparing versions v1.0.0 and v1.2.0 for 'code-reviewer'...

Version Metadata:
v1.0.0 (2025-11-18) → v1.2.0 (2025-11-20)

Changelog Entries:
[1.1.0] - 2025-11-19
  Added: Error recovery mechanisms
  Fixed: File permission handling

[1.2.0] - 2025-11-20
  Added: Version comparison feature
  Changed: Improved validation logic

File Changes:

SKILL.md:
  +89 lines, -34 lines

scripts/reviewer.sh:
  +45 lines, -12 lines

scripts/comparator.sh:
  +156 lines (new file)

Total: +290 lines, -46 lines across 3 files
```

## Security Considerations

### File Integrity
- SHA256 checksums for version archives
- Verify file integrity before rollback
- Detect tampering in version history

### Permissions
- Preserve file permissions in versions
- Restore correct permissions on rollback
- Validate script execution permissions

### Backup Safety
- Always create backup before destructive operations
- Store backups with timestamp
- Automatic cleanup of old backups (optional)

## Performance Optimization

### Large Skills
- Incremental backups (store diffs instead of full copies)
- Compression for version archives
- Lazy loading of version metadata

### Storage Management
- Configurable retention policy
- Auto-archive old versions
- Cleanup of orphaned versions

## Validation & Testing

Before finalizing a version:

1. **Syntax validation**: Verify YAML frontmatter
2. **File integrity**: Check all tracked files exist
3. **Metadata completeness**: Ensure all required fields
4. **Changelog format**: Validate Keep a Changelog format
5. **Git consistency**: Verify git tags match version numbers
6. **Rollback test**: Verify rollback to previous version works

## Troubleshooting

### Version Not Found
```bash
# List all versions
ls -la skills/<skill-name>/.versions/

# Check git tags
git tag -l "v*"
```

### Corrupted Metadata
```bash
# Regenerate from git history
git log --follow -- skills/<skill-name>/SKILL.md
```

### Rollback Failed
```bash
# Restore from backup
cp -r .versions/backup-*/ ./
```

## Summary

The version-management skill provides professional version control for Claude Code skills, enabling:
- Safe experimentation with rollback capability
- Professional changelog maintenance
- Clear version history
- Error recovery mechanisms
- Integration with git workflows

Use this skill whenever you need to:
- Track changes to skills over time
- Create stable releases
- Document evolution of prompts
- Recover from problematic changes
- Archive skill versions

## Related Commands

- `git tag`: View git tags
- `git diff`: Compare versions
- `git log`: View commit history
- `git checkout`: Switch versions (use with caution)

## References

- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [Git Tagging](https://git-scm.com/book/en/v2/Git-Basics-Tagging)
