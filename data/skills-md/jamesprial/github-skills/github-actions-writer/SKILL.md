---
name: github-actions-writer
description: This skill should be used when users need to create, modify, optimize, or troubleshoot GitHub Actions CI/CD workflows. Use when users ask about automating builds, tests, deployments, or any GitHub Actions-related tasks. Triggers include requests like "create a CI workflow", "deploy to AWS", "automate testing", "setup GitHub Actions", or when debugging workflow failures.
---

# GitHub Actions Writer

## Overview

Write production-ready GitHub Actions workflows with built-in security, performance optimization, and best practices. Generate complete CI/CD pipelines, deployment workflows, and automation tasks using battle-tested templates and expert guidance.

## When to Use This Skill

Invoke this skill when users:
- Want to create new CI/CD workflows for any language or framework
- Need to deploy applications to cloud providers (AWS, Azure, GCP)
- Ask about automating tests, builds, or releases
- Have failing or slow GitHub Actions workflows
- Need security scanning or compliance checks
- Want to optimize workflow performance or reduce costs
- Request help with Docker builds, Kubernetes deployments, or multi-environment setups

## Core Capabilities

### 1. Interactive Workflow Generation

Ask targeted questions to understand requirements and generate customized workflows:

**Example interaction:**
```
User: "I need to test my Node.js app on every pull request"

Ask:
1. What Node.js versions do you need to support?
2. Do you use npm, yarn, or pnpm?
3. What test framework (Jest, Mocha, etc.)?
4. Do you need code coverage reporting?
5. Any special build steps required?

Generate: Complete node-ci.yml with testing, caching, coverage, and best practices
```

**Question framework:**
- **Language/Framework:** Detect from repository or ask
- **CI Goals:** Testing only, or also build/publish?
- **Deployment Target:** AWS, Azure, GCP, Docker registries, static hosting?
- **Environment Strategy:** Single environment or dev/staging/production?
- **Security Requirements:** OIDC, scanning, approval gates?
- **Performance Needs:** Caching, parallelization, cost optimization?

### 2. Template Selection and Customization

Use templates from `assets/templates/` as starting points, then customize based on specific requirements.

**Template categories:**

**CI Templates** (`assets/templates/ci/`):
- `node-ci.yml` - Node.js testing, building, npm publishing
- `python-ci.yml` - Python testing with pytest, linting, PyPI publishing
- `docker-build-push.yml` - Multi-registry Docker builds with security scanning
- `multi-language-matrix.yml` - Cross-platform/version matrix testing
- `monorepo-selective.yml` - Intelligent monorepo builds with path filtering

**Deployment Templates** (`assets/templates/cd/`):
- `aws-oidc-deploy.yml` - Secure AWS deployment with OIDC (no credentials)
- `kubernetes-gitops.yml` - GitOps-style K8s deployments
- `multi-environment.yml` - Dev → Staging → Production with approval gates

**Security Templates** (`assets/templates/security/`):
- `security-scan.yml` - Comprehensive security scanning (CodeQL, Snyk, Trivy, etc.)

**Advanced Patterns** (`assets/templates/advanced/`):
- `reusable-workflow.yml` - Organization-wide reusable workflows
- `composite-action/action.yml` - Custom composite actions

### 3. Apply Best Practices Automatically

Every generated workflow includes:

**Security:**
- ✅ Minimal explicit permissions (never `write-all`)
- ✅ OIDC authentication for cloud deployments (no long-lived credentials)
- ✅ Action versions pinned (security and stability)
- ✅ Input sanitization (prevent command injection)

**Performance:**
- ✅ Dependency caching with proper cache keys
- ✅ Concurrency control to cancel stale runs
- ✅ Appropriate timeouts to prevent hung jobs
- ✅ Path filtering to avoid unnecessary runs
- ✅ Job parallelization where possible

**Reliability:**
- ✅ Comprehensive inline documentation
- ✅ Error handling and conditionals
- ✅ Artifact management
- ✅ Clear job dependencies

### 4. Workflow Analysis and Enhancement

When users have existing workflows, analyze and improve them:

**Analysis process:**
1. Read the existing workflow file
2. Identify missing optimizations (caching, concurrency, timeouts)
3. Detect security issues (excessive permissions, injection risks)
4. Find performance bottlenecks
5. Suggest specific improvements with code examples

**Example:**
```
User: "My workflow is slow and expensive"

Analyze:
- Check for missing dependency caching → Add actions/cache
- Check for unnecessary full checkouts → Use fetch-depth: 1
- Check for serial jobs → Parallelize independent jobs
- Check for missing concurrency control → Add cancel-in-progress
- Check for large artifacts → Optimize artifact uploads
- Provide estimated time/cost savings
```

### 5. Debugging and Troubleshooting

Reference `references/performance-and-troubleshooting.md` for common issues:

**Common problems:**
- "Resource not accessible by integration" → Add permissions
- Secrets not available → Use pull_request vs pull_request_target correctly
- Cache not restoring → Fix cache key patterns
- Workflow not triggering → Check filters and branch names
- Command injection vulnerabilities → Use environment variables

**Debugging techniques:**
- Enable debug logging (ACTIONS_RUNNER_DEBUG)
- Print context information
- Use conditional steps to isolate issues
- Check GitHub Actions status page

## Usage Workflows

### Workflow 1: Creating a New CI/CD Pipeline

1. **Understand the project:**
   - Detect language/framework from repository files
   - Identify package manager (package.json, requirements.txt, etc.)
   - Check for existing workflows

2. **Ask clarifying questions:**
   - What's the primary goal? (test, build, deploy, all)
   - Which environments? (staging, production)
   - Any specific requirements? (security scans, multi-platform, etc.)

3. **Select appropriate template:**
   - CI: Use `node-ci.yml`, `python-ci.yml`, etc.
   - CD: Use `aws-oidc-deploy.yml`, `kubernetes-gitops.yml`, etc.
   - Special cases: `monorepo-selective.yml`, `multi-language-matrix.yml`

4. **Customize the template:**
   - Update versions (Node.js, Python, etc.)
   - Adjust branch names
   - Configure paths for filtering
   - Add project-specific steps
   - Update deployment targets

5. **Add inline documentation:**
   - Explain WHY each section exists
   - Document required secrets/variables
   - Include setup instructions
   - Provide customization tips

6. **Validate before delivering:**
   - Check YAML syntax
   - Verify all required fields present
   - Ensure permissions are minimal
   - Confirm security best practices applied

### Workflow 2: Optimizing Existing Workflows

1. **Read the current workflow file**

2. **Analyze for issues:**
   - Missing caching → Calculate potential time savings
   - No concurrency control → Identify wasted runs
   - Excessive permissions → Suggest minimal set
   - No timeouts → Add appropriate limits
   - Poor parallelization → Identify independent jobs
   - Unpinned actions → Security risk
   - Command injection risks → Sanitization needed

3. **Prioritize improvements:**
   - Critical security issues first
   - High-impact performance optimizations
   - Best practices and polish

4. **Provide specific fixes:**
   - Show exact code changes
   - Explain impact of each change
   - Estimate time/cost savings

### Workflow 3: Troubleshooting Failures

1. **Understand the error:**
   - Read error message from user
   - Check workflow file if provided
   - Identify error pattern

2. **Reference troubleshooting guide:**
   - Use `references/performance-and-troubleshooting.md`
   - Match error to common patterns

3. **Provide solution:**
   - Explain root cause
   - Show exact fix
   - Suggest prevention measures

## Using Bundled Resources

### Templates (`assets/templates/`)

**How to use:**
1. Select the most appropriate template for the use case
2. Copy the template content
3. Customize:
   - Replace placeholder values (repository names, versions, etc.)
   - Remove unused jobs (e.g., disable Lambda deployment if only using ECS)
   - Add project-specific steps
4. Keep inline comments and documentation
5. Update configuration notes at the bottom

**Customization checklist:**
- [ ] Update language/framework versions
- [ ] Configure branch names and filters
- [ ] Set appropriate paths for path filtering
- [ ] Configure deployment targets
- [ ] Add required secrets documentation
- [ ] Test timeout values
- [ ] Verify permissions are minimal

### References (`references/`)

Load these into context when needed:

- **`syntax-quick-reference.md`:** Quick lookup for workflow syntax, triggers, expressions
  - Use when: User asks about specific syntax, or you need to verify expression format

- **`security-best-practices.md`:** Comprehensive security guide with OIDC setup, permissions, secrets
  - Use when: Creating workflows with deployment, handling secrets, or auditing security

- **`performance-and-troubleshooting.md`:** Performance optimization and common error solutions
  - Use when: Workflow is slow/expensive, or user reports errors

**How to reference:**
```
For detailed syntax: Read references/syntax-quick-reference.md
For security setup: Read references/security-best-practices.md
For debugging help: Read references/performance-and-troubleshooting.md
```

### Scripts (`scripts/`)

Provide these scripts to users for validation and auditing:

- **`validate_workflow.py`:** Validates workflow YAML for syntax, schema, best practices
  ```bash
  python3 scripts/validate_workflow.py .github/workflows/*.yml
  ```

- **`security_audit.py`:** Audits workflows for security issues
  ```bash
  python3 scripts/security_audit.py .github/workflows/*.yml --fail-on=high
  ```

**When to suggest:**
- After generating workflows: "Validate with `validate_workflow.py`"
- For security-sensitive workflows: "Audit with `security_audit.py`"
- CI/CD integration: "Add these scripts to your workflow for continuous validation"

## Common Patterns and Examples

### Pattern 1: Simple CI Testing

**User request:** "Test my Node.js app on PRs"

**Response:**
```yaml
name: CI

on:
  pull_request:

permissions:
  contents: read

concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true

jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm test
```

### Pattern 2: Multi-Environment Deployment

**User request:** "Deploy to staging on develop, production on main with approval"

**Use:** `assets/templates/cd/multi-environment.yml`
- Customize branch names
- Configure environments in GitHub settings
- Add required reviewers for production

### Pattern 3: Secure Cloud Deployment

**User request:** "Deploy to AWS without storing credentials"

**Use:** `assets/templates/cd/aws-oidc-deploy.yml`
- Guide user through OIDC setup in AWS
- Configure IAM role with trust policy
- Add role ARN to secrets
- Enable `id-token: write` permission

### Pattern 4: Monorepo Optimization

**User request:** "Only build changed packages in my monorepo"

**Use:** `assets/templates/ci/monorepo-selective.yml`
- Configure path filters for each package
- Set up job dependencies
- Use caching for shared dependencies

## Security Checklist

Before delivering any workflow, ensure:

- [ ] Permissions explicitly set (never rely on defaults)
- [ ] Permissions are minimal (only what's needed)
- [ ] Actions pinned to specific versions
- [ ] No secrets in code or logs
- [ ] User input sanitized (use env vars, not direct interpolation)
- [ ] `pull_request_target` used correctly (if at all)
- [ ] OIDC recommended for cloud deployments
- [ ] Self-hosted runners NOT used for public repos
- [ ] Timeouts set on all jobs
- [ ] Concurrency control configured

## Tips for Success

1. **Always explain WHY:** Include inline comments explaining decisions
2. **Provide context:** Document required setup (secrets, environments, etc.)
3. **Be specific:** Use actual values, not placeholders where possible
4. **Test before suggesting:** Mentally verify workflow syntax and logic
5. **Offer validation:** Suggest using validation scripts
6. **Consider security first:** OIDC over credentials, minimal permissions
7. **Optimize by default:** Caching, concurrency, timeouts
8. **Make it educational:** Users should learn, not just copy-paste

## Example Interactions

### Example 1: Complete Setup

```
User: I need to deploy my React app to AWS S3 when I push to main

Response:
1. Ask: "Do you have an existing S3 bucket and CloudFront distribution?"
2. If yes: Provide aws-oidc-deploy.yml S3 deployment section
3. Guide OIDC setup:
   - Create OIDC provider in AWS
   - Create IAM role with trust policy
   - Add S3 permissions to role
   - Save role ARN as secret
4. Customize workflow:
   - Update bucket name
   - Add CloudFront invalidation
   - Configure cache headers
5. Provide complete workflow with inline docs
```

### Example 2: Optimization

```
User: My CI takes 15 minutes and costs too much

Response:
1. Ask: "Can you share your workflow file?"
2. Analyze:
   - Missing cache → npm ci takes 5 min every time
   - No concurrency → old runs still running
   - Sequential jobs → lint and test can run in parallel
3. Provide specific fixes:
   - Add actions/setup-node cache
   - Add concurrency group
   - Parallelize independent jobs
   - Estimate: Reduce to 6 minutes, save 60% cost
4. Show before/after comparison
```

### Example 3: Security Fix

```
User: Security scan flagged my workflow

Response:
1. Analyze the workflow
2. Identify issues:
   - permissions: write-all → CRITICAL
   - Unpinned actions → HIGH
   - Direct secret usage in run → MEDIUM
3. Provide fixes:
   - Set minimal permissions
   - Pin actions to SHA
   - Use environment variables for secrets
4. Explain WHY each fix matters
5. Suggest running security_audit.py regularly
```

---

## Success Criteria

A successful GitHub Actions workflow:
- ✅ Works on first try (no syntax errors)
- ✅ Is secure (minimal permissions, OIDC, input sanitization)
- ✅ Is performant (caching, concurrency, parallelization)
- ✅ Is well-documented (inline comments, setup instructions)
- ✅ Follows best practices (timeouts, error handling, artifact management)
- ✅ Is maintainable (clear structure, sensible defaults)
- ✅ Educates the user (explains decisions, provides context)
