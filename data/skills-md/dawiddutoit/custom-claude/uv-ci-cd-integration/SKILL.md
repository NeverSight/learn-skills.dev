---
name: uv-ci-cd-integration
description: |
  Set up uv (Rust-based Python package manager) in CI/CD pipelines.
  Use when configuring GitHub Actions workflows, GitLab CI/CD, Docker builds, or matrix testing across Python versions.
  Includes patterns for cache optimization, frozen lockfiles, multi-stage builds, and PyPI publishing with trusted publishing.
  Covers GitHub Actions setup-uv action, Docker multi-stage production/development builds, and deployment patterns.
allowed-tools: Read, Bash, Write, Edit
---

# uv CI/CD Integration Skill

## Purpose

This skill helps integrate **uv** (the fast Rust-based Python package manager) into CI/CD pipelines and containerized deployments. It provides proven patterns for GitHub Actions, GitLab CI, Docker, and PyPI publishing that optimize for performance, reliability, and maintainability.

## Quick Start

**GitHub Actions (basic CI workflow):**
```bash
# Create .github/workflows/ci.yml
curl -s https://docs.astral.sh/uv/guides/integration/github/ | grep -A 30 "name: CI" > temp.yaml
```

**Docker (production build):**
```dockerfile
FROM python:3.12-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

FROM python:3.12-slim
COPY --from=builder /app/.venv /app/.venv
COPY . .
ENV PATH="/app/.venv/bin:$PATH"
CMD ["python", "-m", "myapp"]
```

**GitLab CI (basic pipeline):**
```bash
# Install uv in before_script, sync dependencies, run tests
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync --all-extras --dev
uv run pytest
```

## Instructions

### Step 1: Choose Your CI/CD Platform

Identify where your code is deployed:

1. **GitHub Actions** - Recommended for GitHub repositories (native support, `setup-uv` action)
2. **GitLab CI** - For GitLab instances (self-hosted or cloud)
3. **Docker** - For containerized deployments (multi-stage builds for optimization)
4. **Other** - Jenkins, Cirrus CI, GitHub Enterprise (manual setup required)

For each platform, you'll set up uv installation, dependency caching, and frozen lockfile enforcement.

### Step 2: Set Up Dependency Caching

**Why:** Cache shared across workflow runs dramatically reduces CI time (10-100x faster warm starts).

**GitHub Actions with setup-uv action:**
```yaml
- name: Install uv
  uses: astral-sh/setup-uv@v6
  with:
    version: "0.9.8"        # Optional: pin specific version
    enable-cache: true      # Enable dependency caching
    cache-dependency-glob: "uv.lock"  # Track changes to this file
```

**GitLab CI with custom cache:**
```yaml
variables:
  UV_CACHE_DIR: .uv-cache

cache:
  key: ${CI_COMMIT_REF_SLUG}
  paths:
    - .uv-cache
```

**Docker (layer caching):**
```dockerfile
# Layer caching: Only rebuild if pyproject.toml or uv.lock changes
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project
```

### Step 3: Configure Matrix Testing (Multiple Python Versions)

**Why:** Test against multiple Python versions to ensure compatibility.

**GitHub Actions with matrix:**
```yaml
strategy:
  matrix:
    python-version: ["3.11", "3.12", "3.13"]
steps:
  - uses: astral-sh/setup-uv@v6
  - run: uv python install ${{ matrix.python-version }}
    env:
      UV_PYTHON: ${{ matrix.python-version }}
  - run: uv sync --all-extras --dev
  - run: uv run pytest
```

**GitLab CI with parallel jobs:**
```yaml
test:3.11:
  image: python:3.11
  script:
    - curl -LsSf https://astral.sh/uv/install.sh | sh
    - uv sync --all-extras --dev
    - uv run pytest

test:3.12:
  image: python:3.12
  script:
    - curl -LsSf https://astral.sh/uv/install.sh | sh
    - uv sync --all-extras --dev
    - uv run pytest
```

### Step 4: Use Frozen Lockfiles in Production

**Why:** Frozen lockfiles ensure exact reproducibility - prevents unexpected updates.

**Command pattern:**
```bash
# Fails if lockfile is out of sync with pyproject.toml
uv sync --frozen --no-dev

# For development environments (interactive)
uv sync --all-extras --dev
```

**Docker production:** Always use `--frozen` flag
```dockerfile
RUN uv sync --frozen --no-dev --no-install-project
```

**GitHub Actions CI:**
```yaml
- name: Sync with frozen lockfile
  run: uv sync --frozen --all-extras --dev
```

Commit `uv.lock` to version control. Update it with `uv lock --upgrade` when ready.

### Step 5: Implement Production Deployment Patterns

**Multi-stage Docker build (recommended for size/security):**

```dockerfile
# Stage 1: Builder - compile dependencies
FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# Stage 2: Runtime - minimal image with only .venv
FROM python:3.12-slim

WORKDIR /app
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY . .

# Ensure virtual environment is in PATH
ENV PATH="/app/.venv/bin:$PATH"

# Run application
CMD ["python", "-m", "myapp"]
```

**Benefits:**
- Final image ~70% smaller (builder dependencies not included)
- Faster deployments and reduced bandwidth
- Improved security (build tools not in production)

### Step 6: Set Up PyPI Publishing with Trusted Publishing

**Why:** Trusted publishing (OIDC) is more secure than static tokens. No need to manage secrets.

**GitHub Actions workflow:**

```yaml
name: Publish

on:
  push:
    tags:
      - "v*"

jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      id-token: write  # Required for OIDC/trusted publishing
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v6

      - name: Build distributions
        run: uv build

      - name: Publish to PyPI
        run: uv publish
        # No credentials needed - uses OIDC tokens
```

**Setup in PyPI (one-time):**
1. Go to https://pypi.org/manage/account/
2. Add "Trusted Publisher" for your GitHub repository
3. Set trusted publisher to your GitHub organization/repository + workflow name

**For custom index/private PyPI:**
```yaml
- name: Publish to custom index
  run: uv publish --index-url https://example.org/pypi
  env:
    UV_PUBLISH_TOKEN: ${{ secrets.CUSTOM_PYPI_TOKEN }}
```

## Examples

### Example 1: Complete GitHub Actions CI Workflow

See `examples/github-actions-complete.yml` for a production-ready workflow including:
- uv installation with caching
- Multiple Python version matrix
- Linting, type checking, testing
- Coverage reporting
- Dependency vulnerability scanning

### Example 2: Docker Development Environment

See `examples/dockerfile-development` for a development-optimized Dockerfile that includes:
- uv installation with all dev dependencies
- Source code mounting for hot reload
- All development tools (linters, type checkers, test frameworks)

### Example 3: GitLab CI Pipeline Configuration

See `examples/gitlab-ci-complete.yml` for a complete GitLab CI setup including:
- Matrix testing across Python versions
- Parallel jobs for linting and testing
- Cache optimization
- Test coverage artifacts

### Example 4: PyPI Publishing Workflow

See `examples/pypi-publishing-workflow.yml` for:
- Trusted publishing (OIDC) setup
- Automated versioning from git tags
- Publication to both PyPI and test PyPI
- Release notes generation

## Requirements

### System Requirements

- **Git repository**: GitHub, GitLab, or another CI/CD platform
- **uv available**: Version 0.9.0 or later (action/installation script ensures this)
- **Docker** (if using container deployments): Docker 20.10+ for multi-stage builds
- **lockfile**: `uv.lock` must be committed to version control

### Credentials (Optional)

- **PyPI Token** (only for legacy token auth): Create at https://pypi.org/manage/account/publishing/
  - Better approach: Use trusted publishing (OIDC) - no credentials needed
- **Private PyPI credentials** (if using custom index): Configure via environment variables or keyring

### Python Versions

- **Tested**: Python 3.11, 3.12, 3.13
- **Minimum**: Python 3.9 (for uv itself), but recommend 3.11+
- **Pin in `.python-version`**: Create with `uv python pin 3.12`

## See Also

- [examples/github-actions-complete.yml](./examples/github-actions-complete.yml) - Full CI workflow with all features
- [examples/dockerfile-development](./examples/dockerfile-development) - Development container setup
- [examples/gitlab-ci-complete.yml](./examples/gitlab-ci-complete.yml) - GitLab CI pipeline
- [examples/pypi-publishing-workflow.yml](./examples/pypi-publishing-workflow.yml) - Publishing automation
- [references/cache-optimization.md](./references/cache-optimization.md) - Cache strategies and tuning
- [references/docker-patterns.md](./references/docker-patterns.md) - Advanced Docker patterns
- [references/troubleshooting.md](./references/troubleshooting.md) - Common issues and solutions
