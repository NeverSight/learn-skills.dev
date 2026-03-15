---
name: skill-release
description: (project - Skill) Sync and publish skills from .agents/skills/ to skills/ directory with version bumping and git automation. Use when releasing or updating skills, triggered by "release skills", "publish skills", "sync skills", "deploy skills", or when skill development is complete.
---

# Skill Release

Sync skills from `.agents/skills/` to `skills/` directory, bump version numbers, and push to git.

## Quick Start

```bash
# Release all skills with changes
scripts/release_skill.py

# Preview changes without executing
scripts/release_skill.py --dry-run

# Release specific skill only
scripts/release_skill.py --skill jimeng-api-image-gen
```

## Workflow

1. **Scan** `.agents/skills/` for all skills with SKILL.md
2. **Compare** with `skills/` directory using content hash
3. **Copy** changed skills, updating version (patch bump)
4. **Commit** with `git add . && git commit -m "chore: release skills"`
5. **Push** to remote repository

## Version Management

Version is stored in `package.json` at skill root:

```
skill-name/
├── SKILL.md
├── package.json    # contains "version": "1.2.3"
└── scripts/
```

- First release: `1.0.0`
- Updates: patch bump (`1.2.3` → `1.2.4`)
- Semver format: `major.minor.patch`

## Command Options

| Option | Description |
|--------|-------------|
| `--dry-run` | Preview changes without executing |
| `--skill NAME` | Process only the specified skill |

## Project Structure

```
project/
├── .agents/skills/     # Development source
│   ├── skill-a/
│   │   └── SKILL.md
│   └── skill-b/
│       └── SKILL.md
└── skills/             # Release destination
    ├── skill-a/
    │   └── SKILL.md    # Version added/updated
    └── skill-b/
        └── SKILL.md
```

## Requirements

- Python 3.8+
- Git repository with push access
- `.agents/skills/` and `skills/` directories

## Notes

- Only skills with SKILL.md are processed
- Unchanged skills are skipped
- Git operations require clean working directory
