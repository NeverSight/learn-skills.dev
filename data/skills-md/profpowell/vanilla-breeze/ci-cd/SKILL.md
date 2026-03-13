---
name: ci-cd
description: Configure GitHub Actions for automated testing, building, and deployment. Use when setting up CI/CD pipelines, automating releases, or managing deployment workflows.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# CI/CD Skill

Automate testing, building, and deployment with GitHub Actions.

## Directory Structure

```
.github/
├── workflows/
│   ├── ci.yml              # Continuous integration
│   ├── deploy.yml          # Deployment
│   └── release.yml         # Release automation
└── dependabot.yml          # Dependency updates
```

## Basic CI Workflow

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
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Lint
        run: npm run lint

      - name: Test
        run: npm test

      - name: Build
        run: npm run build
```

## Deploy to Cloudflare Pages

```yaml
# .github/workflows/deploy.yml
name: Deploy to Cloudflare Pages

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build
        env:
          NODE_ENV: production

      - name: Deploy to Cloudflare Pages
        uses: cloudflare/pages-action@v1
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
          projectName: my-project
          directory: dist
          gitHubToken: ${{ secrets.GITHUB_TOKEN }}
```

## Deploy to DigitalOcean App Platform

```yaml
# .github/workflows/deploy-do.yml
name: Deploy to DigitalOcean

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Install doctl
        uses: digitalocean/action-doctl@v2
        with:
          token: ${{ secrets.DIGITALOCEAN_ACCESS_TOKEN }}

      - name: Deploy to App Platform
        run: doctl apps create-deployment ${{ secrets.DO_APP_ID }}
```

## Deploy to DigitalOcean Droplet (SSH)

```yaml
# .github/workflows/deploy-droplet.yml
name: Deploy to Droplet

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Deploy via SSH
        uses: appleboy/ssh-action@v1.0.0
        with:
          host: ${{ secrets.DROPLET_HOST }}
          username: ${{ secrets.DROPLET_USER }}
          key: ${{ secrets.DROPLET_SSH_KEY }}
          script: |
            cd /var/www/my-app
            git pull origin main
            npm ci --only=production
            npm run build
            pm2 reload ecosystem.config.js
```

## Matrix Testing

Test across multiple Node.js versions:

```yaml
# .github/workflows/ci.yml
jobs:
  test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        node-version: [18, 20, 22]

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'

      - run: npm ci
      - run: npm test
```

## Caching

```yaml
jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      # Cache build output
      - name: Cache build
        uses: actions/cache@v4
        with:
          path: dist
          key: build-${{ hashFiles('src/**', 'package-lock.json') }}

      - run: npm ci

      - name: Build (if not cached)
        run: |
          if [ ! -d "dist" ]; then
            npm run build
          fi
```

## Environment-Specific Deploys

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches:
      - main      # Production
      - staging   # Staging

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - run: npm ci

      - name: Build
        run: npm run build
        env:
          NODE_ENV: ${{ github.ref == 'refs/heads/main' && 'production' || 'staging' }}

      - name: Deploy to Production
        if: github.ref == 'refs/heads/main'
        run: npx wrangler pages deploy dist --project-name=my-app
        env:
          CLOUDFLARE_API_TOKEN: ${{ secrets.CLOUDFLARE_API_TOKEN }}

      - name: Deploy to Staging
        if: github.ref == 'refs/heads/staging'
        run: npx wrangler pages deploy dist --project-name=my-app-staging
        env:
          CLOUDFLARE_API_TOKEN: ${{ secrets.CLOUDFLARE_API_TOKEN }}
```

## Secrets Management

### Required Secrets

Set in repository Settings > Secrets and variables > Actions:

| Secret | Description |
|--------|-------------|
| `CLOUDFLARE_API_TOKEN` | Cloudflare API token with Pages edit permission |
| `CLOUDFLARE_ACCOUNT_ID` | Cloudflare account ID |
| `DIGITALOCEAN_ACCESS_TOKEN` | DigitalOcean API token |
| `DROPLET_HOST` | Droplet IP or hostname |
| `DROPLET_USER` | SSH username |
| `DROPLET_SSH_KEY` | Private SSH key |

### Using Secrets

```yaml
env:
  API_KEY: ${{ secrets.API_KEY }}

# Or per-step
- name: Deploy
  run: ./deploy.sh
  env:
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

## Pull Request Checks

```yaml
# .github/workflows/pr.yml
name: PR Checks

on:
  pull_request:
    branches: [main]

jobs:
  check:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - run: npm ci
      - run: npm run lint
      - run: npm test
      - run: npm run build

      # Comment bundle size on PR
      - name: Report bundle size
        uses: preactjs/compressed-size-action@v2
        with:
          repo-token: ${{ secrets.GITHUB_TOKEN }}
```

## Release Automation

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - run: npm ci
      - run: npm run build

      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          files: dist/*
          generate_release_notes: true
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Deploy
        run: npx wrangler pages deploy dist --project-name=my-app
        env:
          CLOUDFLARE_API_TOKEN: ${{ secrets.CLOUDFLARE_API_TOKEN }}
```

## Dependabot Configuration

```yaml
# .github/dependabot.yml
version: 2

updates:
  # NPM dependencies
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    groups:
      # Group minor/patch updates
      dependencies:
        patterns:
          - "*"
        update-types:
          - "minor"
          - "patch"

  # GitHub Actions
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

## Workflow Templates

### Reusable Workflow

```yaml
# .github/workflows/build.yml
name: Build

on:
  workflow_call:
    inputs:
      node-version:
        required: false
        type: string
        default: '20'
    outputs:
      artifact-name:
        value: ${{ jobs.build.outputs.artifact-name }}

jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      artifact-name: build-${{ github.sha }}

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
          cache: 'npm'

      - run: npm ci
      - run: npm run build

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: build-${{ github.sha }}
          path: dist/
```

### Using Reusable Workflow

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  build:
    uses: ./.github/workflows/build.yml

  deploy:
    needs: build
    runs-on: ubuntu-latest

    steps:
      - name: Download artifact
        uses: actions/download-artifact@v4
        with:
          name: ${{ needs.build.outputs.artifact-name }}
          path: dist/

      - name: Deploy
        run: npx wrangler pages deploy dist
        env:
          CLOUDFLARE_API_TOKEN: ${{ secrets.CLOUDFLARE_API_TOKEN }}
```

## Checklist

Before enabling CI/CD:

- [ ] All required secrets are set
- [ ] Workflows have correct triggers
- [ ] Build command works locally
- [ ] Tests pass locally
- [ ] Deployment credentials are scoped appropriately
- [ ] Branch protection rules configured
- [ ] Dependabot enabled for security updates

## Related Skills

- **deployment** - Deployment target configuration
- **env-config** - Environment variable management
- **unit-testing** - Test configuration
- **security** - Credential management
