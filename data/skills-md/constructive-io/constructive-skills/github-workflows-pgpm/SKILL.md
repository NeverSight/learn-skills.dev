---
name: github-workflows-pgpm
description: Configure GitHub Actions workflows for PostgreSQL database testing, PGPM migrations, and CI/CD pipelines in Constructive projects. Use when setting up CI/CD for a PGPM-based project, configuring PostgreSQL service containers in GitHub Actions, or running database tests in CI.
---

Configure GitHub Actions workflows for PostgreSQL database testing, PGPM migrations, and CI/CD pipelines in Constructive projects.

## When to Apply

Use this skill when:
- Setting up CI/CD for a PGPM-based project
- Configuring PostgreSQL service containers in GitHub Actions
- Running database tests with pgsql-test in CI
- Generating SDKs or types from database schemas in CI
- Building and publishing Docker images for PostgreSQL

## Core Workflow Pattern

Every Constructive CI workflow follows this pattern:

1. **Spin up PostgreSQL service container** with health checks
2. **Install pnpm and Node.js** with caching
3. **Cache and install pgpm CLI** globally
4. **Build the workspace** with `pnpm -r build`
5. **Bootstrap database users** with `pgpm admin-users`
6. **Run tests** per package

## PostgreSQL Service Container

Use the Constructive PostgreSQL image with extensions pre-installed:

```yaml
services:
  pg_db:
    image: ghcr.io/constructive-io/docker/postgres-plus:17
    env:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    options: >-
      --health-cmd pg_isready
      --health-interval 10s
      --health-timeout 5s
      --health-retries 5
    ports:
      - 5432:5432
```

For simpler setups without custom extensions:

```yaml
services:
  pg_db:
    image: pyramation/postgres:17
    env:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    options: >-
      --health-cmd pg_isready
      --health-interval 10s
      --health-timeout 5s
      --health-retries 5
    ports:
      - 5432:5432
```

## Environment Variables

Standard PostgreSQL environment variables for tests:

```yaml
env:
  PGHOST: localhost
  PGPORT: 5432
  PGUSER: postgres
  PGPASSWORD: password
```

For MinIO/S3 testing (uploads, storage):

```yaml
env:
  MINIO_ENDPOINT: http://localhost:9000
  AWS_ACCESS_KEY: minioadmin
  AWS_SECRET_KEY: minioadmin
  AWS_REGION: us-east-1
  BUCKET_NAME: test-bucket
```

## PGPM CLI Caching

Cache the pgpm CLI to speed up workflows:

```yaml
env:
  PGPM_VERSION: '2.7.9'

steps:
  - name: Cache pgpm CLI
    uses: actions/cache@v4
    with:
      path: ~/.npm
      key: pgpm-${{ runner.os }}-${{ env.PGPM_VERSION }}

  - name: Install pgpm CLI globally
    run: npm install -g pgpm@${{ env.PGPM_VERSION }}
```

## Database User Bootstrap

Before running tests, bootstrap the database users:

```yaml
- name: Seed pg and app_user
  run: |
    pgpm admin-users bootstrap --yes
    pgpm admin-users add --test --yes
```

This creates:
- The `app_user` role for RLS testing
- Test-specific roles and permissions

## Complete Test Workflow

Full workflow for running tests across multiple packages:

```yaml
name: CI tests
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}-tests
  cancel-in-progress: true

env:
  PGPM_VERSION: '2.7.9'

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      fail-fast: false
      matrix:
        package:
          - packages/my-package
          - packages/another-package

    env:
      PGHOST: localhost
      PGPORT: 5432
      PGUSER: postgres
      PGPASSWORD: password

    services:
      pg_db:
        image: ghcr.io/constructive-io/docker/postgres-plus:17
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: password
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - name: Configure Git
        run: |
          git config --global user.name "CI Test User"
          git config --global user.email "ci@example.com"

      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup pnpm
        uses: pnpm/action-setup@v2
        with:
          version: 10

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install

      - name: Cache pgpm CLI
        uses: actions/cache@v4
        with:
          path: ~/.npm
          key: pgpm-${{ runner.os }}-${{ env.PGPM_VERSION }}

      - name: Install pgpm CLI globally
        run: npm install -g pgpm@${{ env.PGPM_VERSION }}

      - name: Build
        run: pnpm -r build

      - name: Seed pg and app_user
        run: |
          pgpm admin-users bootstrap --yes
          pgpm admin-users add --test --yes

      - name: Test ${{ matrix.package }}
        run: cd ./${{ matrix.package }} && pnpm test
```

## Integration Test Workflow

For running pgpm's built-in integration tests:

```yaml
- name: Run Integration Tests
  run: pgpm test-packages
```

This runs all package tests defined in the pgpm workspace.

## SDK Generation Workflow

Generate typed SDKs from database schemas:

```yaml
name: generate-sdk
on:
  workflow_dispatch:
    inputs:
      commit_changes:
        description: 'Commit and push generated SDK changes'
        required: false
        default: 'false'
        type: boolean

jobs:
  generate-sdk:
    runs-on: ubuntu-latest
    
    # ... services and setup steps ...

    steps:
      # ... checkout, pnpm, node, pgpm setup ...

      - name: Build
        run: pnpm -r build

      - name: Seed pg and app_user
        run: |
          pgpm admin-users bootstrap --yes
          pgpm admin-users add --test --yes

      - name: Generate SDK
        run: |
          cd sdk/my-sdk
          pnpm run generate

      - name: Check for changes
        id: check_changes
        run: |
          if git diff --quiet sdk/my-sdk/src/generated; then
            echo "has_changes=false" >> $GITHUB_OUTPUT
          else
            echo "has_changes=true" >> $GITHUB_OUTPUT
          fi

      - name: Commit and push changes
        if: ${{ inputs.commit_changes == 'true' && steps.check_changes.outputs.has_changes == 'true' }}
        run: |
          git add sdk/my-sdk/src/generated
          git commit -m "chore: regenerate SDK types"
          git push

      - name: Upload generated SDK as artifact
        if: ${{ steps.check_changes.outputs.has_changes == 'true' }}
        uses: actions/upload-artifact@v4
        with:
          name: generated-sdk
          path: sdk/my-sdk/src/generated
          retention-days: 7
```

## Test Sharding

For large test suites, split tests across parallel jobs:

```yaml
strategy:
  fail-fast: false
  matrix:
    package: [packages/core]
    test_pattern: ['']
    include:
      - package: packages/large-package
        test_pattern: 'auth|rls'
        shard_name: 'large-package-auth-rls'
      - package: packages/large-package
        test_pattern: 'permissions|orgs'
        shard_name: 'large-package-permissions-orgs'

steps:
  - name: Test ${{ matrix.package }}${{ matrix.shard_name && format(' ({0})', matrix.shard_name) || '' }}
    shell: bash
    run: |
      cd ./${{ matrix.package }}
      if [ -n "${{ matrix.test_pattern }}" ]; then
        pnpm test -- "${{ matrix.test_pattern }}"
      else
        pnpm test
      fi
```

## MinIO Service Container

For testing uploads and S3-compatible storage:

```yaml
services:
  minio_cdn:
    image: minio/minio:edge-cicd
    env:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    ports:
      - 9000:9000
      - 9001:9001
    options: >-
      --health-cmd "curl -f http://localhost:9000/minio/health/live || exit 1"
      --health-interval 10s
      --health-timeout 5s
      --health-retries 5
```

## Concurrency Control

Prevent duplicate workflow runs:

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}-tests
  cancel-in-progress: true
```

## Docker Build Workflow

Build and push PostgreSQL images:

```yaml
name: Docker
on:
  workflow_dispatch:
    inputs:
      process:
        description: 'Process to build'
        type: choice
        options: [pgvector, postgis, pgvector-postgis]

jobs:
  build-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    env:
      REPO: ghcr.io/${{ github.repository_owner }}
      PLATFORMS: linux/amd64,linux/arm64

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push
        run: |
          make \
            PROCESS=${{ inputs.process }} \
            REPO_NAME=$REPO \
            PLATFORMS="$PLATFORMS" \
            build-push-process
```

## Per-Package Environment Variables

Pass package-specific environment variables:

```yaml
strategy:
  matrix:
    include:
      - package: packages/client
        env:
          TEST_DATABASE_URL: postgres://postgres:password@localhost:5432/postgres
      - package: uploads/s3-streamer
        env:
          BUCKET_NAME: test-bucket

steps:
  - name: Test ${{ matrix.package }}
    run: cd ./${{ matrix.package }} && pnpm test
    env: ${{ matrix.env }}
```

## Best Practices

1. **Always use health checks** — Ensure PostgreSQL is ready before tests run
2. **Cache pgpm CLI** — Speeds up workflow execution significantly
3. **Use concurrency control** — Prevent duplicate runs on rapid pushes
4. **Configure Git** — Required for tests that use git operations
5. **Use matrix strategy** — Run tests in parallel across packages
6. **Bootstrap users before tests** — `pgpm admin-users` creates required roles
7. **Use fail-fast: false** — Let all tests complete even if some fail
8. **Pin pgpm version** — Ensure consistent behavior across runs

## References

- Related skill: `pgsql-test` for database testing framework
- Related skill: `pgpm` (`references/workspace.md`) for PGPM project setup
- Related skill: `pnpm-workspace` for PNPM monorepo configuration
- [GitHub Actions documentation](https://docs.github.com/en/actions)
- [pnpm/action-setup](https://github.com/pnpm/action-setup)
