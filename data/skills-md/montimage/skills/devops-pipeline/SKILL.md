---
name: devops-pipeline
version: 1.1.0
description: Implement pre-commit hooks and GitHub Actions for quality assurance. Use when asked to "setup CI/CD", "add pre-commit hooks", "create GitHub Actions", "setup quality gates", "automate testing", "add linting to CI", "setup code quality checks", "configure CI pipeline", "add automated checks", or any DevOps automation for code quality. Detects project type and configures appropriate tools. Trigger this skill whenever the user mentions CI, CD, pre-commit, GitHub Actions, linting automation, or quality gates — even if they don't use those exact terms.
---

# DevOps Pipeline

Implement comprehensive DevOps quality gates adapted to project type.

## Repo Sync Before Edits (mandatory)

Before making any changes, sync with the remote to avoid conflicts:

```bash
branch="$(git rev-parse --abbrev-ref HEAD)"
git fetch origin
git pull --rebase origin "$branch"
```

If the working tree is dirty, stash first, sync, then pop. If `origin` is missing or conflicts occur, stop and ask the user before continuing.

## Workflow

### 0. Create Feature Branch

Before making any changes:
1. Check the current branch — if already on a feature branch for this task, skip
2. Check the repo for branch naming conventions (e.g., `feat/`, `feature/`, etc.)
3. Create and switch to a new branch following the repo's convention, or fallback to: `feat/devops-pipeline`

### 1. Analyze Project

Detect project characteristics:

```bash
# Check for package files and configs
ls -la package.json pyproject.toml Cargo.toml go.mod pom.xml build.gradle *.csproj 2>/dev/null
ls -la .eslintrc* .prettierrc* tsconfig.json mypy.ini setup.cfg ruff.toml 2>/dev/null
ls -la .pre-commit-config.yaml .github/workflows/*.yml 2>/dev/null
```

Identify:
- **Languages**: JS/TS, Python, Go, Rust, Java, C#, etc.
- **Frameworks**: React, Next.js, Django, FastAPI, etc.
- **Build system**: npm, yarn, pnpm, pip, poetry, cargo, go, maven, gradle
- **Existing tooling**: Linters, formatters, type checkers already configured

### 2. Configure Pre-commit Hooks

Install pre-commit framework:

```bash
pip install pre-commit  # or brew install pre-commit
```

Create `.pre-commit-config.yaml` based on detected stack. See [references/precommit-configs.md](references/precommit-configs.md) for language-specific configurations.

Install hooks:

```bash
pre-commit install
pre-commit run --all-files  # Test on existing code
```

### 3. Create GitHub Actions Workflows

Create `.github/workflows/ci.yml` mirroring pre-commit checks. See [references/github-actions.md](references/github-actions.md) for workflow templates.

Key principles:
- Mirror pre-commit checks for consistency
- Use caching for dependencies
- Run on push and pull_request
- Add matrix testing for multiple versions if needed

### 4. Verify Pipeline

```bash
# Test pre-commit locally
pre-commit run --all-files

# Commit and push to trigger CI
git add .pre-commit-config.yaml .github/
git commit -m "ci: add pre-commit hooks and GitHub Actions"
git push
```

Check GitHub Actions tab for workflow status.

## Tool Selection by Language

| Language | Formatter | Linter | Security | Types |
|----------|-----------|--------|----------|-------|
| JS/TS | Prettier | ESLint | npm audit | TypeScript |
| Python | Black/Ruff | Ruff | Bandit | mypy |
| Go | gofmt | golangci-lint | gosec | built-in |
| Rust | rustfmt | Clippy | cargo-audit | built-in |
| Java | google-java-format | Checkstyle | SpotBugs | - |

## Resources

- [references/precommit-configs.md](references/precommit-configs.md) - Pre-commit configurations by language
- [references/github-actions.md](references/github-actions.md) - GitHub Actions workflow templates
