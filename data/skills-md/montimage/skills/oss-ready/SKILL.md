---
name: oss-ready
version: 1.2.0
description: Transform projects into professional open-source repositories with standard components. Use when users ask to "make this open source", "add open source files", "setup OSS standards", "create contributing guide", "add license", or want to prepare a project for public release with README, CONTRIBUTING, LICENSE, and GitHub templates.
---

# OSS Ready

Transform projects into professional open-source repositories with standard components.

## Workflow

### 0. Create Feature Branch

Before making any changes:
1. Check the current branch - if already on a feature branch for this task, skip
2. Check the repo for branch naming conventions (e.g., `feat/`, `feature/`, etc.)
3. Create and switch to a new branch following the repo's convention, or fallback to: `feat/oss-ready`

### 1. Analyze Project

Identify:
- Primary language(s) and tech stack
- Project purpose and functionality
- Existing documentation to preserve
- Package manager (npm, pip, cargo, etc.)

### 2. Create/Update Core Files

**README.md** - Enhance with:
- Project overview and motivation
- Key features list
- Quick start (< 5 min setup)
- Prerequisites and installation
- Usage examples with code
- Project structure
- Technology stack
- Contributing link
- License badge

**CONTRIBUTING.md** - Include:
- How to contribute overview
- Development setup
- Branching strategy (feature branches from main)
- Commit conventions (Conventional Commits)
- PR process and review expectations
- Coding standards
- Testing requirements

**LICENSE** - Default to MIT unless specified.

**CODE_OF_CONDUCT.md** - Contributor Covenant.

**SECURITY.md** - Vulnerability reporting process.

**IMPORTANT — Copy asset files using shell commands only.** Some asset files (CODE_OF_CONDUCT.md, SECURITY.md) contain language about harassment, abuse, and vulnerability disclosure that **will trigger content filtering** if you attempt to read and re-write the content. Always use `cp` to copy these files. Never read their contents into context and write them back out.

```bash
# Copy from the skill's assets directory — use cp, do NOT read+write
SKILL_ASSETS="{SKILL_DIR}/assets"
cp "$SKILL_ASSETS/LICENSE-MIT" LICENSE
cp "$SKILL_ASSETS/CODE_OF_CONDUCT.md" CODE_OF_CONDUCT.md
cp "$SKILL_ASSETS/SECURITY.md" SECURITY.md
```

After copying, only use `sed` to replace placeholders (e.g., `[INSERT CONTACT METHOD]`, `[INSERT EMAIL]`) with project-specific values. Do not rewrite the full file.

### 3. Create GitHub Templates

Copy from the skill's `assets/.github/` using shell commands:

```bash
mkdir -p .github/ISSUE_TEMPLATE
cp "$SKILL_ASSETS/.github/ISSUE_TEMPLATE/bug_report.md" .github/ISSUE_TEMPLATE/
cp "$SKILL_ASSETS/.github/ISSUE_TEMPLATE/feature_request.md" .github/ISSUE_TEMPLATE/
cp "$SKILL_ASSETS/.github/PULL_REQUEST_TEMPLATE.md" .github/
```

### 4. Create Documentation Structure

```
docs/
├── ARCHITECTURE.md    # System design, components
├── DEVELOPMENT.md     # Dev setup, debugging
├── DEPLOYMENT.md      # Production deployment
└── CHANGELOG.md       # Version history
```

### 5. Update Project Metadata

Update package file based on tech stack:
- **Node.js**: `package.json` - name, description, keywords, repository, license
- **Python**: `pyproject.toml` or `setup.py`
- **Rust**: `Cargo.toml`
- **Go**: `go.mod` + README badges

### 6. Ensure .gitignore

Verify comprehensive patterns for the tech stack.

### 7. Present Checklist

After completion, show:
- [x] Files created/updated
- [ ] Items needing manual review
- Recommendations for next steps

## Guidelines

- Preserve existing content - enhance, don't replace
- Use professional, welcoming tone
- Adapt to project's actual tech stack
- Include working examples from the actual codebase

## Assets

Templates in `assets/`:
- `LICENSE-MIT` - MIT license template
- `CODE_OF_CONDUCT.md` - Contributor Covenant
- `SECURITY.md` - Security policy template
- `.github/ISSUE_TEMPLATE/bug_report.md`
- `.github/ISSUE_TEMPLATE/feature_request.md`
- `.github/PULL_REQUEST_TEMPLATE.md`
