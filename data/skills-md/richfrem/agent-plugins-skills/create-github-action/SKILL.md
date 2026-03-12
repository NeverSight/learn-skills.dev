---
name: create-github-action
description: Scaffold a traditional deterministic GitHub Actions CI/CD workflow. Use this when creating build, test, deploy, lint, release, or security scan pipelines. This is distinct from agentic workflows — no AI is involved at runtime.
allowed-tools: Bash, Read, Write
---
# GitHub Actions Scaffolder

You are scaffolding a **traditional GitHub Actions YAML workflow** — deterministic CI/CD automation with no AI at runtime. This is different from agentic workflows.

## When to Use This Skill vs Others

| Task | Use This Skill | Use `create-agentic-workflow` |
|---|---|---|
| Run tests on every PR | ✅ | ❌ |
| Build and publish a Docker image | ✅ | ❌ |
| Deploy to GitHub Pages | ✅ | ❌ |
| Check if PR matches the spec | ❌ | ✅ |
| Daily repo health report | ❌ | ✅ |
| Code review with AI judgment | ❌ | ✅ |

## Execution Steps

### 1. Gather Requirements

Ask the user for the following context:

1. **Workflow Category**: What does this workflow need to do?
   - **Test** — run unit/integration tests on PR/push (pytest, jest, go test, etc.)
   - **Build** — compile, bundle, or build Docker images
   - **Lint** — run linters or formatters (ruff, eslint, markdownlint, etc.)
   - **Deploy** — publish to GitHub Pages, Vercel, AWS, etc.
   - **Release** — create GitHub releases, publish npm/PyPI packages
   - **Security** — dependency audits, SAST, secret scanning (CodeQL, trivy, etc.)
   - **Maintenance** — scheduled jobs, stale issue cleanup, dependency updates
   - **Custom** — describe the steps manually

2. **Platform/Language**: What stack? (Python, Node.js, Go, Docker, .NET, etc.)

3. **Trigger Events**: When should this fire?
   - `pull_request` — on PR open/update (most quality gates)
   - `push` to main — on merge to main (post-merge validation, deploys)
   - `workflow_dispatch` — manual run
   - `schedule` — cron schedule (maintenance jobs)
   - `release` — on GitHub Release published

### 2. Generate the Workflow

Run the scaffold script:

```bash
python ./scripts/scaffold_github_action.py \
  --skill-dir <path-to-skill-directory> \
  --category <test|build|lint|deploy|release|security|maintenance|custom> \
  --platform <python|nodejs|go|docker|dotnet|generic> \
  [--triggers pull_request push schedule workflow_dispatch] \
  [--name "My Workflow Name"] \
  [--branch main]
```

The script outputs a ready-to-use `.yml` file in `.github/workflows/`.

### 3. Post-Scaffold Guidance

After generating, advise the user:

- **Platform-specific secrets**: Some steps require repository secrets (e.g., `PYPI_TOKEN`, `NPM_TOKEN`, `DOCKER_PASSWORD`, `DEPLOY_KEY`).
- **Pinned action versions**: All generated steps use pinned `@v4`/`@v3` action refs for security.
- **Permissions**: Generated workflows declare minimal permissions (`contents: read` by default, elevated only when needed).
- **Review before committing**: Treat workflow YAML as code — review it before merging.

## GitHub Actions Key Reference

### Available Trigger Events

| Trigger | Fires when | Common for |
|---|---|---|
| `pull_request` | PR opened/updated | Tests, lint, security |
| `push` | Branch pushed | Deploy, release checks |
| `schedule` (cron) | On a time schedule | Maintenance, reports |
| `workflow_dispatch` | Manual button click | Deploys, one-off jobs |
| `release` | Release published | Package publishing |
| `issues` | Issue opened/labeled | Triage, notifications |
| `workflow_call` | Called by another workflow | Reusable sub-workflows |

### Permissions Model

```yaml
permissions:
  contents: read      # Read repo files
  contents: write     # Commit files, push
  pull-requests: write # Comment on PRs
  issues: write       # Create/update issues
  packages: write     # Publish packages
  id-token: write     # OIDC (for cloud deploys)
```

> Always declare minimum required permissions. The `GITHUB_TOKEN` grants no permissions by default unless declared.

### Common Action Patterns

```yaml
# Checkout
- uses: actions/checkout@v4

# Setup language
- uses: actions/setup-python@v5
  with:
    python-version: "3.12"

# Cache dependencies
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}

# Upload artifacts
- uses: actions/upload-artifact@v4
  with:
    name: report
    path: output/

# Publish GitHub Release
- uses: softprops/action-gh-release@v2
  with:
    files: dist/*
```


## Next Actions
- Offer to run `audit-plugin` to validate the generated artifacts.
