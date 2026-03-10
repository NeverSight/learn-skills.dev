---
name: build-ci-cd-pipeline
description: >
  Design and implement multi-stage CI/CD pipelines using GitHub Actions with matrix builds,
  dependency caching, artifact management, and secret handling. Create workflows that span
  linting, testing, building, and deployment stages with parallel execution and conditional
  logic. Use when setting up automated testing and deployment for a new project, migrating
  from Jenkins or CircleCI to GitHub Actions, implementing matrix builds across platforms,
  adding build caching, or creating multi-stage pipelines with security scanning and quality
  gates.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: devops
  complexity: intermediate
  language: multi
  tags: ci-cd, github-actions, pipeline, automation, testing
---

# Build CI/CD Pipeline

Design and implement production-grade continuous integration and deployment pipelines with GitHub Actions.

## When to Use

- Setting up automated testing and deployment for a new project
- Migrating from Jenkins, Travis CI, or CircleCI to GitHub Actions
- Implementing matrix builds across multiple platforms or language versions
- Adding build caching to speed up CI/CD execution time
- Creating multi-stage pipelines with environment-specific deployments
- Implementing security scanning and code quality gates

## Inputs

- **Required**: Repository with code to test/build/deploy
- **Required**: GitHub Actions workflow directory (`.github/workflows/`)
- **Optional**: Secrets for deployment targets (AWS, Azure, Docker registries)
- **Optional**: Self-hosted runner configuration for specialized builds
- **Optional**: Branch protection rules and required status checks

## Procedure

### Step 1: Create Base Workflow Structure

Create `.github/workflows/ci.yml` with trigger configuration and basic job structure.

```yaml
name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
  workflow_dispatch:  # Manual trigger

env:
  NODE_VERSION: '18'
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  lint:
    name: Lint Code
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run ESLint
        run: npm run lint

      - name: Check formatting
        run: npm run format:check
```

**Expected:** Workflow file created with proper YAML syntax, triggers configured, and basic lint job defined.

**On failure:** Validate YAML syntax with `yamllint .github/workflows/ci.yml`. Check indentation (use spaces, not tabs). Verify action versions are current by checking GitHub Marketplace.

### Step 2: Implement Matrix Build Strategy

Add matrix builds to test across multiple platforms, language versions, or configurations.

```yaml
  test:
    name: Test (${{ matrix.os }}, Node ${{ matrix.node }})
    runs-on: ${{ matrix.os }}
    needs: lint
    strategy:
      fail-fast: false  # Continue testing other matrix combinations on failure
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        node: ['16', '18', '20']
        exclude:
          - os: macos-latest
            node: '16'  # Skip old Node on macOS

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js ${{ matrix.node }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run tests with coverage
        run: npm run test:coverage

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        if: matrix.os == 'ubuntu-latest' && matrix.node == '18'
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
          files: ./coverage/lcov.info
          fail_ci_if_error: true
```

**Expected:** Matrix generates 8 parallel jobs (3 OS × 3 Node versions - 1 exclusion). All tests pass across platforms. Coverage report uploads from single canonical job.

**On failure:** If matrix syntax errors occur, verify proper indentation and array notation. For flaky tests, add retry logic with `uses: nick-invision/retry@v2`. For platform-specific failures, add OS conditionals or expand exclusions.

### Step 3: Configure Dependency Caching and Artifact Management

Optimize build speed with intelligent caching and preserve build artifacts.

```yaml
  build:
    name: Build Application
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Cache build output
        uses: actions/cache@v3
        with:
          path: |
            .next/cache
            dist/
            build/
          key: ${{ runner.os }}-build-${{ hashFiles('**/package-lock.json') }}-${{ hashFiles('**/*.ts', '**/*.tsx') }}
          restore-keys: |
            ${{ runner.os }}-build-${{ hashFiles('**/package-lock.json') }}-
            ${{ runner.os }}-build-

      - name: Install dependencies
        run: npm ci

      - name: Build application
        run: npm run build
        env:
          NODE_ENV: production

      - name: Upload build artifacts
        uses: actions/upload-artifact@v3
        with:
          name: dist-${{ github.sha }}
          path: |
            dist/
            build/
          retention-days: 7
          if-no-files-found: error
```

**Expected:** First run downloads dependencies (slow), subsequent runs restore from cache (fast). Build artifacts upload successfully with unique SHA-based naming.

**On failure:** If cache misses frequently, verify cache key includes all relevant file hashes. For upload failures, check path exists and glob patterns match actual build output. Verify `retention-days` meets organizational policies.

### Step 4: Implement Security Scanning and Quality Gates

Add security vulnerability scanning and code quality enforcement.

```yaml
  security:
    name: Security Scan
    runs-on: ubuntu-latest
    needs: lint
    permissions:
      security-events: write  # Required for uploading SARIF results
    steps:
      - uses: actions/checkout@v4

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'CRITICAL,HIGH'

      - name: Upload Trivy results to GitHub Security
        uses: github/codeql-action/upload-sarif@v2
        if: always()  # Upload even if scan finds vulnerabilities
        with:
          sarif_file: 'trivy-results.sarif'

      - name: Dependency audit
        run: npm audit --audit-level=high
        continue-on-error: true  # Don't fail build, but show warnings

      - name: Check for leaked secrets
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: ${{ github.event.repository.default_branch }}
          head: HEAD
```

**Expected:** Security scans complete, results upload to GitHub Security tab. Critical vulnerabilities block merge if branch protection configured. No secrets detected in commits.

**On failure:** For false positives, create `.trivyignore` file with CVE IDs and justifications. For audit failures, review `npm audit fix` suggestions. For secret detection false positives, add patterns to `.trufflehog.yml` exclude list.

### Step 5: Configure Environment-Specific Deployments

Set up deployment stages with environment protection rules and approval gates.

```yaml
  deploy-staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    needs: [build, security]
    if: github.ref == 'refs/heads/develop'
    environment:
      name: staging
      url: https://staging.example.com
    steps:
      - name: Download build artifacts
        uses: actions/download-artifact@v3
        with:
          name: dist-${{ github.sha }}
          path: ./dist

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_STAGING }}
          aws-region: us-east-1

      - name: Deploy to S3
        run: |
          aws s3 sync ./dist s3://${{ secrets.S3_BUCKET_STAGING }} --delete
          aws cloudfront create-invalidation --distribution-id ${{ secrets.CF_DIST_STAGING }} --paths "/*"

  deploy-production:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: [build, security]
    if: github.ref == 'refs/heads/main'
    environment:
      name: production
      url: https://example.com
    steps:
      - name: Download build artifacts
        uses: actions/download-artifact@v3
        with:
          name: dist-${{ github.sha }}
          path: ./dist

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_PRODUCTION }}
          aws-region: us-east-1

      - name: Deploy to S3 with blue-green
        run: |
          # Deploy to new version
          aws s3 sync ./dist s3://${{ secrets.S3_BUCKET_PRODUCTION }}/releases/${{ github.sha }} --delete

          # Update symlink to new version
          aws s3 cp s3://${{ secrets.S3_BUCKET_PRODUCTION }}/releases/${{ github.sha }} s3://${{ secrets.S3_BUCKET_PRODUCTION }}/current --recursive

          # Invalidate CloudFront
          aws cloudfront create-invalidation --distribution-id ${{ secrets.CF_DIST_PRODUCTION }} --paths "/*"

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v1
        if: startsWith(github.ref, 'refs/tags/')
        with:
          files: ./dist/**/*
          generate_release_notes: true
```

**Expected:** Staging deploys automatically on develop branch. Production requires manual approval (configured in GitHub Environment settings). CloudFront invalidation clears CDN cache. Release created for tagged commits.

**On failure:** For AWS credential errors, verify OIDC trust relationship allows `role-to-assume`. For S3 sync failures, check bucket policies and IAM permissions. For environment approval issues, verify protection rules in Settings > Environments.

### Step 6: Add Notification and Monitoring Integration

Integrate Slack notifications, deployment tracking, and performance monitoring.

```yaml
  notify:
    name: Notify Results
    runs-on: ubuntu-latest
    needs: [deploy-staging, deploy-production]
    if: always()  # Run even if previous jobs fail
    steps:
      - name: Check job status
        id: status
        run: |
          if [ "${{ needs.deploy-production.result }}" == "success" ]; then
            echo "status=success" >> $GITHUB_OUTPUT
            echo "color=#00FF00" >> $GITHUB_OUTPUT
          else
            echo "status=failure" >> $GITHUB_OUTPUT
            echo "color=#FF0000" >> $GITHUB_OUTPUT
          fi

      - name: Send Slack notification
        uses: slackapi/slack-github-action@v1.24.0
        with:
          payload: |
            {
              "text": "Deployment ${{ steps.status.outputs.status }}",
              "blocks": [
                {
                  "type": "header",
                  "text": {
                    "type": "plain_text",
                    "text": "🚀 Deployment Status: ${{ steps.status.outputs.status }}"
                  }
                },
                {
                  "type": "section",
                  "fields": [
                    {"type": "mrkdwn", "text": "*Repository:*\n${{ github.repository }}"},
                    {"type": "mrkdwn", "text": "*Branch:*\n${{ github.ref_name }}"},
                    {"type": "mrkdwn", "text": "*Commit:*\n${{ github.sha }}"},
                    {"type": "mrkdwn", "text": "*Actor:*\n${{ github.actor }}"}
                  ]
                },
                {
                  "type": "actions",
                  "elements": [
                    {
                      "type": "button",
                      "text": {"type": "plain_text", "text": "View Workflow"},
                      "url": "${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}"
                    }
                  ]
                }
              ]
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
          SLACK_WEBHOOK_TYPE: INCOMING_WEBHOOK

      - name: Record deployment in Datadog
        if: steps.status.outputs.status == 'success'
        run: |
          curl -X POST "https://api.datadoghq.com/api/v1/events" \
            -H "Content-Type: application/json" \
            -H "DD-API-KEY: ${{ secrets.DD_API_KEY }}" \
            -d @- <<EOF
          {
            "title": "Deployment: ${{ github.repository }}",
            "text": "Deployed commit ${{ github.sha }} to production",
            "tags": ["env:production", "service:${{ github.event.repository.name }}"],
            "alert_type": "info"
          }
          EOF
```

**Expected:** Slack receives formatted notification with deployment status, repository details, and clickable workflow link. Datadog event logged for successful production deployments with appropriate tags.

**On failure:** For Slack failures, verify webhook URL is valid and workspace allows incoming webhooks. Test with `curl -X POST $SLACK_WEBHOOK_URL -d '{"text":"test"}'`. For Datadog failures, verify API key has event submission permissions.

## Validation

- [ ] Workflow syntax validates with `yamllint` or GitHub's workflow editor
- [ ] All jobs have explicit dependencies (`needs:`) to control execution order
- [ ] Matrix builds cover all target platforms and versions
- [ ] Caching reduces build time by >50% on subsequent runs
- [ ] Secrets are stored in GitHub Secrets, never hardcoded in workflow files
- [ ] Security scans upload results to GitHub Security tab
- [ ] Environment protection rules require approval for production deployments
- [ ] Failed deployments don't leave system in inconsistent state
- [ ] Notifications reach appropriate channels (Slack, email, monitoring tools)
- [ ] Workflow completes in <10 minutes for typical changes

## Common Pitfalls

- **Cache key too broad**: Using `${{ runner.os }}-build-` as cache key causes false hits when dependencies change. Include `hashFiles('**/package-lock.json')` in key.

- **Artifact name collisions**: Using static artifact names like `dist` causes overwrites in concurrent builds. Include `${{ github.sha }}` or `${{ matrix.os }}-${{ matrix.node }}` in names.

- **Secrets in logs**: Avoid `echo $SECRET` or similar commands. GitHub masks registered secrets, but derived values may leak. Use `::add-mask::` for dynamic secrets.

- **Insufficient permissions**: Default `GITHUB_TOKEN` has limited permissions. Add explicit `permissions:` block for security events, packages, issues, etc.

- **Missing if conditionals**: Jobs run on all triggers unless guarded with `if: github.ref == 'refs/heads/main'`. Prevent accidental production deploys from PRs.

- **No rollback strategy**: Deployment failures leave system in broken state. Implement blue-green or canary deployments with automatic rollback on health check failures.

- **Hardcoded values**: Workflow contains environment-specific URLs, bucket names, or API endpoints. Use environment variables and GitHub Secrets.

- **No timeout limits**: Jobs hang indefinitely on network issues or infinite loops. Add `timeout-minutes: 15` to all jobs.

## Related Skills

- `setup-github-actions-ci` - Initial GitHub Actions configuration for R packages and basic projects
- `commit-changes` - Proper Git workflow integration with CI/CD triggers
- `configure-git-repository` - Repository settings and branch protection rules
- `setup-container-registry` - Docker image builds in CI/CD pipelines
- `implement-gitops-workflow` - ArgoCD/Flux integration with CI/CD
