---
name: github-actions
description: Comprehensive GitHub Actions workflow authoring skill. Enables Claude to write production-grade CI/CD workflows with latest best practices, syntax, and security patterns. Use when creating or modifying GitHub Actions workflows, designing CI/CD pipelines, configuring workflow triggers/events/schedules, implementing security patterns (secrets, OIDC, attestations), creating custom actions, migrating from other CI systems, troubleshooting failed workflows, or any GitHub Actions automation task. Includes complete reference documentation extracted from official GitHub docs with source URLs for verification.
---

# GitHub Actions

## Quick Start

Create a workflow file at `.github/workflows/<name>.yml`:

```yaml
name: CI
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo "Hello World"
```

**Essential concepts:**
- **Workflow**: Automated process defined in YAML, runs in response to events
- **Job**: Set of steps that run on the same runner
- **Step**: Individual action or shell command
- **Action**: Reusable unit of code (GitHub marketplace or custom)
- **Event**: What triggers the workflow (push, pull_request, schedule, etc.)

## Common Workflow Patterns

### Continuous Integration (CI)
- **Testing**: Run tests on every push/PR
- **Linting**: Code quality checks
- **Building**: Compile code, build artifacts
- See: `references/tutorials/build-and-test-code/`

### Continuous Deployment (CD)
- **Deploy to production**: Merge to main → deploy
- **Multi-environment**: dev/staging/prod with approvals
- **Blue-green deployment**: Zero-downtime deployments
- See: `references/how-tos/deploy/`

### Scheduled Tasks
```yaml
on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight
```

### Matrix Builds
```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
    node: [14, 16, 18]
```

## Workflow Syntax Reference

### Required Structure
- `name`: Workflow name
- `on`: Triggers (events, schedules, manual)
- `jobs`: One or more jobs

### Key Job Fields
- `runs-on`: Runner type (ubuntu-latest, windows-latest, macos-latest, self-hosted)
- `steps`: Sequential list of steps
- `strategy`: Matrix, fail-fast, max-parallel
- `outputs`: Job-to-job data passing

### Key Step Types
```yaml
steps:
  - name: 'Checkout code'
    uses: actions/checkout@v4

  - name: 'Run script'
    run: npm test

  - name: 'Use action'
    uses: actions/setup-node@v4
    with:
      node-version: '18'
```

### Complete syntax reference: `references/reference/workflows-and-actions/workflow-syntax.md`

## Trigger Events

### Common Events
- `push`: Commits pushed to branch
- `pull_request`: PR opened/updated/closed
- `workflow_dispatch`: Manual trigger
- `schedule`: Cron-based execution

### Advanced Events
- `release`: Release published
- `workflow_call`: Reusable workflow
- `repository_dispatch`: Webhook-triggered
- `environment`: Environment deployment

**Complete events reference**: `references/reference/workflows-and-actions/events-that-trigger-workflows.md`

## Expressions and Contexts

### Expression Syntax
```yaml
if: github.event_name == 'push'
runs-on: ${{ matrix.os }}
```

### Common Contexts
- `github`: Event details, repo, actor, ref
- `env`: Environment variables
- `job`: Job status, outputs
- `steps`: Step outputs
- `runner`: Runner OS, architecture
- `secrets`: Encrypted secrets
- `vars`: Custom variables

**Complete expressions reference**: `references/reference/workflows-and-actions/expressions.md`
**Complete contexts reference**: `references/reference/workflows-and-actions/contexts.md`

## Security Best Practices

### Secrets Management
```yaml
steps:
  - run: deploy.sh ${{ secrets.API_KEY }}
```
- Never log secrets (GitHub auto-redacts)
- Use `secrets` context for sensitive data
- Store in repository Settings → Secrets

**Security guide**: `references/concepts/security/secrets.md`

### GITHUB_TOKEN
- Automatically provided authentication
- Scoped permissions for repo access
- Use for repo operations (clone, push, create PR)

**GITHUB_TOKEN reference**: `references/concepts/security/github_token.md`

### OIDC (OpenID Connect)
- Cloud deployments without long-lived credentials
- Supports AWS, Azure, GCP, and more
- Configure OIDC in workflow and cloud provider

**OIDC guide**: `references/concepts/security/openid-connect.md`

### Security Hardening
- Pin action versions (`@v4` not `@main`)
- Require approval for external workflows
- Use artifact attestations for supply chain security

**Security hardening**: `references/how-tos/security-harden-workflows/`

## Reusable Workflows and Actions

### Reusable Workflows
```yaml
# .github/workflows/reusable.yml
on:
  workflow_call:
    inputs:
      version:
        required: true
        type: string

# Call from another workflow
jobs:
  call:
    uses: org/repo/.github/workflows/reusable.yml@main
    with:
      version: '1.0'
```

### Composite Actions
Combine multiple steps into a reusable action.

### Custom Actions
- JavaScript/TypeScript actions
- Docker actions
- Composite actions

**Reusable workflows**: `references/concepts/workflows-and-actions/reusing-workflow-configurations.md`
**Custom actions**: `references/concepts/workflows-and-actions/custom-actions.md`

## Deployment Patterns

### Environments
```yaml
jobs:
  deploy:
    environment: production
    environment:
      url: https://example.com
```

### Deployment Protection Rules
- Require approval before production
- Restrict who can deploy
- Wait timers for manual review

### Third-Platform Deployments
- **Azure**: App Service, Kubernetes, Static Web Apps
- **AWS**: ECS, EKS, Lambda
- **GCP**: Kubernetes Engine, Cloud Run

**Deployment guides**: `references/how-tos/deploy/`

## Caching Dependencies

```yaml
- uses: actions/cache@v4
  with:
    path: node_modules
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
```

**Caching reference**: `references/concepts/workflows-and-actions/dependency-caching.md`

## Artifacts and Logs

### Upload Artifacts
```yaml
- uses: actions/upload-artifact@v4
  with:
    name: build-output
    path: dist/
```

### Download Artifacts
```yaml
- uses: actions/download-artifact@v4
  with:
    name: build-output
```

**Artifacts reference**: `references/concepts/workflows-and-actions/workflow-artifacts.md`

## Troubleshooting

### Enable Debug Logging
Add secret `ACTIONS_STEP_DEBUG` and `ACTIONS_RUNNER_DEBUG` to repository.

### Common Issues
- **Permission errors**: Check `permissions` scope
- **Path issues**: Use `${{ github.workspace }}`
- **Secret issues**: Verify secret names and scopes

### Viewing Logs
- Actions tab → Workflow run → Job → Step
- Download logs for offline analysis

**Troubleshooting guide**: `references/how-tos/troubleshoot-workflows.md`

## Migrating from Other CI Systems

- **Jenkins**: Import tool and manual patterns
- **GitLab CI**: Syntax differences and equivalents
- **CircleCI**: Migration patterns
- **Travis CI**: Direct equivalents

**Migration guides**: `references/tutorials/migrate-to-github-actions/`

## Language-Specific Guides

- **Node.js**: `references/tutorials/build-and-test-code/nodejs.md`
- **Python**: `references/tutorials/build-and-test-code/python.md`
- **Java**: Maven, Gradle, Ant guides
- **.NET**: Build and test patterns
- **Go, Rust, Ruby, PowerShell**: Specific guides

## Runners

### GitHub-Hosted Runners
- **ubuntu-latest**: Linux (Ubuntu)
- **windows-latest**: Windows Server
- **macos-latest**: macOS
- **Larger runners**: More CPU/memory (paid)

### Self-Hosted Runners
- Custom environments
- Private network access
- Custom tools and dependencies

**Runners reference**: `references/concepts/runners/`

## Complete Documentation Index

All 242 documentation files are available in `references/`:

### Getting Started
- Quickstart: `references/get-started/quickstart.md`
- Understanding Actions: `references/get-started/understand-github-actions.md`
- CI/CD overview: `references/get-started/continuous-*.md`

### Concepts
- Workflows: `references/concepts/workflows-and-actions/`
- Runners: `references/concepts/runners/`
- Security: `references/concepts/security/`

### How-To Guides
- Write workflows: `references/how-tos/write-workflows/`
- Deploy: `references/how-tos/deploy/`
- Create actions: `references/how-tos/create-and-publish-actions/`
- Security hardening: `references/how-tos/security-harden-workflows/`

### Reference
- Workflow syntax: `references/reference/workflows-and-actions/workflow-syntax.md`
- Events: `references/reference/workflows-and-actions/events-that-trigger-workflows.md`
- Expressions: `references/reference/workflows-and-actions/expressions.md`
- Contexts: `references/reference/workflows-and-actions/contexts.md`
- Variables: `references/reference/workflows-and-actions/variables.md`
- Workflow commands: `references/reference/workflows-and-actions/workflow-commands.md`

### Tutorials
- Build and test: `references/tutorials/build-and-test-code/`
- Migrate to Actions: `references/tutorials/migrate-to-github-actions/`
- Create actions: `references/tutorials/create-actions/`
- Publish packages: `references/tutorials/publish-packages/`

**Complete index**: `references/_index.md`

## Online Documentation

All documentation files include source URLs linking to the official GitHub Docs. Use these links to:
- Verify information is current
- Check for updates and changes
- View rendered examples and screenshots
- Report issues or suggest improvements

**Official GitHub Actions Docs**: https://docs.github.com/en/actions
