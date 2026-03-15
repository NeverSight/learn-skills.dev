---
name: github-actions
description: GitHub Actions CI/CD mastery for workflows, matrix builds, caching, secrets, and reusable actions. Use when user asks to "set up CI", "create a workflow", "add GitHub Actions", "matrix builds", "cache dependencies", "deploy with actions", "reusable workflows", or any CI/CD pipeline tasks.
---

# GitHub Actions

CI/CD workflows with GitHub Actions.

## Workflow Basics

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npm test
```

## Triggers

```yaml
on:
  # Branch events
  push:
    branches: [main, "release/**"]
    paths: ["src/**", "tests/**"]      # Only when these paths change
    paths-ignore: ["docs/**", "*.md"]  # Ignore these paths

  pull_request:
    branches: [main]
    types: [opened, synchronize, reopened]

  # Scheduled
  schedule:
    - cron: "0 6 * * 1"  # Every Monday at 6 AM UTC

  # Manual
  workflow_dispatch:
    inputs:
      environment:
        description: "Deploy target"
        required: true
        default: "staging"
        type: choice
        options: [staging, production]

  # On release
  release:
    types: [published]

  # From another workflow
  workflow_call:
    inputs:
      node-version:
        type: string
        default: "20"
```

## Matrix Builds

```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        node: [18, 20, 22]
        exclude:
          - os: macos-latest
            node: 18
        include:
          - os: ubuntu-latest
            node: 20
            coverage: true

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
      - run: npm ci
      - run: npm test
      - if: matrix.coverage
        run: npm run coverage
```

## Caching

```yaml
# Node.js
- uses: actions/setup-node@v4
  with:
    node-version: 20
    cache: "npm"

# Python
- uses: actions/setup-python@v5
  with:
    python-version: "3.12"
    cache: "pip"

# Custom cache
- uses: actions/cache@v4
  with:
    path: |
      ~/.cache/pip
      .mypy_cache
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```

## Secrets & Environment Variables

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production    # GitHub environment with protection rules
    env:
      NODE_ENV: production
    steps:
      - run: echo "Deploying..."
        env:
          API_KEY: ${{ secrets.API_KEY }}
          DATABASE_URL: ${{ secrets.DATABASE_URL }}

      # Using GITHUB_TOKEN (auto-provided)
      - run: gh pr comment --body "Deployed!"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Common Workflow Patterns

### Node.js CI

```yaml
name: Node CI
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
      - run: npm ci
      - run: npm run lint
      - run: npm test
      - run: npm run build
```

### Python CI

```yaml
name: Python CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
      - run: pip install -r requirements.txt
      - run: pytest --cov --cov-report=xml
```

### Docker Build & Push

```yaml
name: Docker
on:
  push:
    tags: ["v*"]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v5
        with:
          push: true
          tags: ghcr.io/${{ github.repository }}:${{ github.ref_name }}
```

### Deploy to Environments

```yaml
name: Deploy
on:
  push:
    branches: [main]
jobs:
  staging:
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/checkout@v4
      - run: ./deploy.sh staging

  production:
    needs: staging
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      - run: ./deploy.sh production
```

## Job Dependencies & Outputs

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      version: ${{ steps.version.outputs.value }}
    steps:
      - id: version
        run: echo "value=$(cat VERSION)" >> $GITHUB_OUTPUT

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying ${{ needs.build.outputs.version }}"
```

## Conditionals

```yaml
steps:
  - if: github.event_name == 'push'
    run: echo "This is a push"

  - if: github.ref == 'refs/heads/main'
    run: echo "On main branch"

  - if: contains(github.event.head_commit.message, '[skip ci]')
    run: echo "Skipping"

  - if: success()   # Previous steps succeeded
    run: echo "All good"

  - if: failure()   # Previous step failed
    run: echo "Something failed"

  - if: always()    # Run regardless
    run: echo "Cleanup"
```

## Reusable Workflows

```yaml
# .github/workflows/reusable-test.yml
on:
  workflow_call:
    inputs:
      node-version:
        type: string
        default: "20"
    secrets:
      npm-token:
        required: false

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
      - run: npm ci
      - run: npm test

# Caller workflow
jobs:
  call-tests:
    uses: ./.github/workflows/reusable-test.yml
    with:
      node-version: "20"
    secrets: inherit
```

## Reference

For workflow templates and popular actions: `references/workflows.md` and `references/actions.md`
