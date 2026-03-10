---
name: configure-git-repository
description: >
  Configure a Git repository with proper .gitignore, branch strategy,
  commit conventions, hooks, and remote setup. Covers initial setup
  and common patterns for R, Node.js, and Python projects. Use when
  initializing version control for a new project, adding a .gitignore
  for a specific language or framework, setting up branch protection and
  conventions, or configuring commit hooks.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: git
  complexity: basic
  language: multi
  tags: git, version-control, gitignore, hooks, branching
---

# Configure Git Repository

Set up a Git repository with appropriate configuration for the project type.

## When to Use

- Initializing version control for a new project
- Adding `.gitignore` for a specific language/framework
- Setting up branch protection and conventions
- Configuring commit hooks

## Inputs

- **Required**: Project directory
- **Required**: Project type (R package, Node.js, Python, general)
- **Optional**: Remote repository URL
- **Optional**: Branch strategy (trunk-based, Git Flow)
- **Optional**: Commit message convention

## Procedure

### Step 1: Initialize Repository

```bash
cd /path/to/project
git init
git branch -M main
```

**Expected:** `.git/` directory created. Default branch is named `main`.

**On failure:** If `git init` fails, ensure Git is installed (`git --version`). If the directory already has a `.git/`, the repository is already initialized — skip this step.

### Step 2: Create .gitignore

**R Package**:

```gitignore
# R artifacts
.Rhistory
.RData
.Rproj.user/
*.Rproj

# Environment (sensitive)
.Renviron

# renv library (machine-specific)
renv/library/
renv/staging/
renv/cache/

# Build artifacts
*.tar.gz
src/*.o
src/*.so
src/*.dll

# Documentation build
docs/
inst/doc/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

**Node.js/TypeScript**:

```gitignore
node_modules/
dist/
build/
.next/
.env
.env.local
.env.*.local
*.log
npm-debug.log*
.DS_Store
Thumbs.db
.vscode/
.idea/
coverage/
```

**Python**:

```gitignore
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.eggs/
.venv/
venv/
.env
*.log
.mypy_cache/
.pytest_cache/
htmlcov/
.coverage
.DS_Store
.idea/
.vscode/
```

**Expected:** `.gitignore` file created with entries appropriate for the project type. Sensitive files (`.Renviron`, `.env`) and generated artifacts are excluded.

**On failure:** If unsure which entries to include, use `gitignore.io` or GitHub's `.gitignore` templates as a starting point and customize for the project.

### Step 3: Create Initial Commit

```bash
git add .gitignore
git add .  # Review what's being added first with git status
git commit -m "Initial project setup"
```

**Expected:** First commit created containing `.gitignore` and initial project files. `git log` shows one commit.

**On failure:** If `git commit` fails with "nothing to commit," ensure files were staged with `git add`. If it fails with an author identity error, set `git config user.name` and `git config user.email`.

### Step 4: Connect Remote

```bash
# Add remote
git remote add origin git@github.com:username/repo.git

# Push
git push -u origin main
```

**Expected:** Remote `origin` is configured. `git remote -v` shows fetch and push URLs. Initial commit is pushed to the remote.

**On failure:** If push fails with "Permission denied (publickey)," configure SSH keys (see `setup-wsl-dev-environment`). If the remote already exists, update it with `git remote set-url origin <url>`.

### Step 5: Set Up Branch Conventions

**Trunk-based (recommended for small teams)**:

- `main`: production-ready code
- Feature branches: `feature/description`
- Bug fixes: `fix/description`

```bash
# Create feature branch
git checkout -b feature/add-authentication

# After work is done, merge or create PR
git checkout main
git merge feature/add-authentication
```

**Expected:** Branch naming convention is established and documented. Team members know which prefix to use for each type of work.

**On failure:** If branches are already named inconsistently, rename them with `git branch -m old-name new-name` and update any open PRs.

### Step 6: Configure Commit Conventions

Conventional Commits format:

```
type(scope): description

feat: add user authentication
fix: correct calculation in weighted_mean
docs: update README installation section
test: add edge case tests for parser
refactor: extract helper function
chore: update dependencies
```

**Expected:** Commit message convention is documented and agreed upon by the team. Future commits follow the `type: description` format.

**On failure:** If team members are not following the convention, enforce it with a commit-msg hook that validates the format (see Step 7).

### Step 7: Set Up Pre-Commit Hooks (Optional)

Create `.githooks/pre-commit`:

```bash
#!/bin/bash
# Run linter before commit

# For R packages
if [ -f "DESCRIPTION" ]; then
  Rscript -e "lintr::lint_package()" || exit 1
fi

# For Node.js
if [ -f "package.json" ]; then
  npm run lint || exit 1
fi
```

```bash
chmod +x .githooks/pre-commit
git config core.hooksPath .githooks
```

**Expected:** Pre-commit hook runs automatically on each `git commit`. Linting errors block the commit until fixed.

**On failure:** If the hook does not run, verify `core.hooksPath` is set (`git config core.hooksPath`) and the hook file is executable (`chmod +x`).

### Step 8: Create README

```bash
# Minimal README
echo "# Project Name" > README.md
echo "" >> README.md
echo "Brief description of the project." >> README.md
git add README.md
git commit -m "Add README"
```

**Expected:** `README.md` committed to the repository. The project has a minimal but informative landing page on GitHub.

**On failure:** If `README.md` already exists, update it rather than overwriting. Use `usethis::use_readme_md()` in R projects for a template with badges.

## Validation

- [ ] `.gitignore` excludes sensitive and generated files
- [ ] No sensitive data (tokens, passwords) in tracked files
- [ ] Remote repository connected and accessible
- [ ] Branch naming conventions documented
- [ ] Initial commit created cleanly

## Common Pitfalls

- **Committing before .gitignore**: Add `.gitignore` first. Files already tracked aren't affected by later `.gitignore` entries.
- **Sensitive data in history**: If secrets are committed, they remain in history even after deletion. Use `git filter-repo` or BFG to clean.
- **Large binary files**: Don't commit large binaries. Use Git LFS for files > 1MB.
- **Line endings**: Set `core.autocrlf=input` on Windows/WSL to prevent CRLF/LF issues.

## Related Skills

- `commit-changes` - staging and committing workflow
- `manage-git-branches` - branch creation and conventions
- `create-r-package` - Git setup as part of R package creation
- `setup-wsl-dev-environment` - Git installation and SSH keys
- `create-github-release` - creating releases from the repository
- `security-audit-codebase` - check for committed secrets
