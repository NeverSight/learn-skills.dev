---
name: terrateam-usage-guide
description: |
  A comprehensive guide for configuring and using Terrateam, an open-source GitOps CI/CD platform for Terraform and OpenTofu. Covers configuration file structure, access control, workflows, OIDC authentication, drift detection, and best practices for managing infrastructure through pull requests.
license: MIT
metadata:
  author: Stakpak <team@stakpak.dev>
  version: 1.0.9
---

# Terrateam Usage Guide

## Overview

Terrateam is an open-source GitOps CI/CD platform that automates Terraform and OpenTofu workflows through GitHub pull requests. It provides intelligent locking, policy enforcement, OIDC authentication, drift detection, and cost estimation.

**Key Capabilities:**
- Automatic plan/apply operations triggered by pull requests
- Tag-based configuration for targeting specific environments
- Fine-grained access control with team/role-based policies
- OIDC authentication for AWS and GCP (no static credentials)
- Drift detection with scheduled reconciliation
- Security scanning with Checkov and policy validation with Conftest

## Prerequisites

- GitHub repository with Terraform/OpenTofu code
- Terrateam installed (GitHub App or self-hosted)
- Cloud provider credentials configured (OIDC recommended)

## Workflow / Instructions

### Step 1: Create Configuration File

Create `.terrateam/config.yml` in your repository root. Terrateam uses sensible defaults if this file doesn't exist.

**Basic structure:**

```yaml
# .terrateam/config.yml
version: "1"

access_control:
  # Who can perform operations

apply_requirements:
  # Conditions before applying

dirs:
  # Directory-to-tag mappings

workflows:
  # Custom plan/apply steps

hooks:
  # Pre/post operation commands
```

### Step 2: Configure Directory Mappings

Map repository directories to tags and workspaces using the `dirs` section:

```yaml
dirs:
  # Production environment
  "environments/production":
    tags: [production, critical]
    workspaces:
      us-east-1:
        tags: [aws, us-east-1]
      eu-west-1:
        tags: [aws, eu-west-1]
    when_modified:
      file_patterns: ["${DIR}/*.tf", "${DIR}/*.tfvars"]
      autoplan: true
      autoapply: false

  # Staging environment
  "environments/staging":
    tags: [staging]
    when_modified:
      file_patterns: ["${DIR}/*.tf", "${DIR}/*.tfvars"]
      autoplan: true
      autoapply: true  # Auto-apply after merge

  # Shared modules (don't plan directly)
  "modules/*":
    tags: [module]
    when_modified:
      autoplan: false
```

**Key concepts:**
- `tags`: Labels for targeting with policies and workflows
- `workspaces`: Multiple Terraform workspaces per directory
- `${DIR}`: Variable representing the current directory path
- `autoplan`: Automatically run plan on PR creation/update
- `autoapply`: Automatically apply after PR merge

### Step 3: Configure Access Control

Define who can perform plan and apply operations:

```yaml
access_control:
  enabled: true
  policies:
    # Production: restricted apply access
    - tag_query: "production"
      plan: ['*']                           # Anyone can plan
      apply: ['team:sre', 'team:platform']  # Only specific teams can apply
      apply_autoapprove: ['user:lead-sre']  # Lead can skip approval
      apply_force: []                       # No one can force apply

    # Default policy for all other directories
    - tag_query: ""
      plan: ['*']
      apply: ['role:write']  # Anyone with write access
```

**Access specifiers:**
- `*`: Anyone
- `team:name`: GitHub team members
- `user:username`: Specific user
- `role:write`: Repository collaborators with write access

### Step 4: Configure Apply Requirements

Set conditions that must be met before applying:

```yaml
apply_requirements:
  create_pending_apply_check: true  # Prevents merge until applied

  checks:
    - tag_query: "production"
      approved:
        enabled: true
        any_of: ['team:sre', 'team:platform']
        any_of_count: 2           # Need 2 approvals
        all_of: ['user:security-lead']  # Always need security approval
      merge_conflicts:
        enabled: true
      status_checks:
        enabled: true
        ignore_matching: ["ci/.*"]  # Ignore CI checks

    - tag_query: ""  # Default
      approved:
        enabled: true
        any_of_count: 1
      merge_conflicts:
        enabled: true
```

### Step 5: Configure Workflows with OIDC

Define custom plan/apply steps with cloud authentication:

```yaml
workflows:
  # Production workflow with AWS OIDC
  - tag_query: "production"
    environment: "production"  # GitHub Environment
    plan:
      - type: oidc
        provider: aws
        role_arn: ${PROD_AWS_ROLE_ARN}
        region: us-east-1
        duration: 3600
      - type: init
        extra_args: ["-upgrade"]
      - type: plan
        extra_args: ["-var-file=prod.tfvars"]
      - type: checkov  # Security scanning
      - type: conftest  # Policy validation
    apply:
      - type: oidc
        provider: aws
        role_arn: ${PROD_AWS_ROLE_ARN}
        region: us-east-1
      - type: init
      - type: apply
        retry:
          enabled: true
          tries: 3

  # GCP workflow
  - tag_query: "gcp"
    plan:
      - type: oidc
        provider: gcp
        service_account: ${GCP_SERVICE_ACCOUNT}
        workload_identity_provider: ${GCP_WORKLOAD_IDENTITY_PROVIDER}
      - type: init
      - type: plan
    apply:
      - type: oidc
        provider: gcp
        service_account: ${GCP_SERVICE_ACCOUNT}
        workload_identity_provider: ${GCP_WORKLOAD_IDENTITY_PROVIDER}
      - type: init
      - type: apply

  # Default workflow
  - tag_query: ""
    plan:
      - type: init
      - type: plan
    apply:
      - type: init
      - type: apply
```

**Workflow step types:**
- `oidc`: Cloud provider authentication
- `init`: terraform init
- `plan`: terraform plan
- `apply`: terraform apply
- `run`: Custom command
- `env`: Set environment variable
- `checkov`: Security scanning
- `conftest`: OPA policy validation

### Step 6: Configure Hooks

Run commands before/after operations:

```yaml
hooks:
  all:
    pre:
      # Set environment variables
      - type: env
        name: TF_VAR_commit_sha
        cmd: ['git', 'rev-parse', 'HEAD']
      # Source secrets
      - type: env
        method: source
        cmd: ['./scripts/load-secrets.sh']
        sensitive: true
    post:
      - type: run
        cmd: ['rm', '-f', '*.tmp']
        run_on: always
        ignore_errors: true

  plan:
    post:
      - type: drift_create_issue  # Create issue on drift

  apply:
    post:
      - type: run
        cmd: ['./scripts/notify-slack.sh']
        run_on: success
```

### Step 7: Configure Drift Detection

Enable scheduled drift detection:

```yaml
drift:
  enabled: true
  schedules:
    production:
      schedule: "hourly"
      tag_query: "production"
      reconcile: false  # Don't auto-fix
      window:
        start: "09:00"
        end: "17:00"
    staging:
      schedule: "daily"
      tag_query: "staging"
      reconcile: true  # Auto-fix drift
```

### Step 8: Configure Cost Estimation

Enable Infracost integration:

```yaml
cost_estimation:
  enabled: true
  provider: infracost
  currency: USD
```

## Pull Request Commands

Trigger operations via PR comments:

| Command | Description |
|---------|-------------|
| `terrateam plan` | Run plan for all changed directories |
| `terrateam plan dir:path` | Plan specific directory |
| `terrateam apply` | Apply all planned changes |
| `terrateam apply dir:path` | Apply specific directory |
| `terrateam apply-autoapprove` | Apply without approval (if permitted) |
| `terrateam apply-force` | Force apply (if permitted) |
| `terrateam unlock` | Release locks |
| `terrateam gate approve <token>` | Approve gated step |

## Tag Query Syntax

Target specific resources using tag queries:

```yaml
# Single tag
tag_query: "production"

# AND logic
tag_query: "production AND aws"

# OR logic
tag_query: "staging OR development"

# Directory-based
tag_query: "dir:environments/production"

# Workspace-based
tag_query: "workspace:us-east-1"

# Combined
tag_query: "production AND aws AND dir:environments/*"
```

## Common Patterns

### Multi-Environment Setup

```yaml
dirs:
  "env/prod": { tags: [prod, critical] }
  "env/staging": { tags: [staging] }
  "env/dev": { tags: [dev] }

workflows:
  - tag_query: "prod"
    plan:
      - type: init
      - type: plan
        extra_args: ["-var-file=prod.tfvars"]
  - tag_query: "staging"
    plan:
      - type: init
      - type: plan
        extra_args: ["-var-file=staging.tfvars"]
```

### Layered Infrastructure with Dependencies

```yaml
dirs:
  "network":
    when_modified:
      autoplan: true
  "compute":
    when_modified:
      depends_on: "dir:network"
  "applications":
    when_modified:
      depends_on: "dir:compute"
```

### Security Scanning with Gates

```yaml
workflows:
  - tag_query: "production"
    plan:
      - type: init
      - type: plan
      - type: checkov
        gate:
          token: "security-override"
          any_of: ["team:security"]
      - type: conftest
        gate:
          token: "policy-override"
          all_of: ["team:compliance"]
```

### Terragrunt Support

```yaml
engine:
  name: terragrunt
  version: "0.45.0"
  tf_version: "1.5.0"

workflows:
  - tag_query: "terragrunt"
    plan:
      - type: init
      - type: plan
    apply:
      - type: init
      - type: apply
```

## Best Practices

1. **Start Simple**: Begin with minimal configuration, add complexity as needed
2. **Use Tags**: Organize resources with meaningful tags for policy targeting
3. **Layer Security**: Combine access control, apply requirements, and workflows
4. **OIDC Over Static Credentials**: Use OIDC for cloud authentication
5. **Environment Separation**: Different policies for production vs staging
6. **Test Workflows**: Validate complex workflows in non-production first
7. **Automate Wisely**: Be cautious with autoapply and drift reconciliation
8. **Version Control**: Always specify configuration version

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Plan not triggering | Check `when_modified.file_patterns` matches changed files |
| Apply blocked | Verify `apply_requirements` conditions are met |
| OIDC failing | Confirm role ARN and trust policy configuration |
| Lock conflicts | Use `terrateam unlock` to release stale locks |
| Drift not detected | Verify `drift.schedules` configuration and time window |

## Environment Variables

Terrateam provides built-in variables:

| Variable | Description |
|----------|-------------|
| `TERRATEAM_DIR` | Current directory being processed |
| `TERRATEAM_WORKSPACE` | Current Terraform workspace |
| `TERRATEAM_ROOT` | Repository root path |
| `TERRATEAM_PLAN_FILE` | Path to generated plan file |

## References

- [Terrateam Documentation](https://docs.terrateam.io)
- [Configuration Reference](https://docs.terrateam.io/reference/configuration/)
- [GitHub Repository](https://github.com/terrateamio/terrateam)
- [Terrateam Blog](https://terrateam.io/blog)