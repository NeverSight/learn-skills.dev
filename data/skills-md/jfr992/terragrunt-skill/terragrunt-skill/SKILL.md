---
name: terragrunt-skill
description: |
  Use this skill when working with Terragrunt infrastructure configurations. Triggers include:
  - Setting up a new Terragrunt infrastructure catalog from scratch
  - Creating or managing Terragrunt stacks (terragrunt.stack.hcl)
  - Creating units that wrap OpenTofu modules from separate repos
  - Configuring live infrastructure repositories with root.hcl hierarchy
  - Setting up remote state backends (S3 with DynamoDB locking)
  - Multi-account/multi-environment deployments with cross-account role assumption
---

# Terragrunt Infrastructure Skill

## Overview

This skill provides guidance for infrastructure using Terragrunt with OpenTofu, following a three-repository pattern:

1. **Infrastructure Catalog** - Units and stacks that reference modules from separate repos
2. **Infrastructure Live** - Environment-specific deployments consuming the catalog
3. **Module Repos** - Separate repositories for each OpenTofu module (independent versioning)

## Quick Navigation

| Topic | Reference |
|-------|-----------|
| Naming conventions | [naming.md](references/naming.md) |
| Catalog structure | [catalog-structure.md](references/catalog-structure.md) |
| Live repo structure | [live-structure.md](references/live-structure.md) |
| Root/account/env configs | [root-config.md](references/root-config.md) |
| Unit dependencies | [dependencies.md](references/dependencies.md) |
| Catalog scaffolding | [catalog-scaffolding.md](references/catalog-scaffolding.md) |
| Stack commands | [stack-commands.md](references/stack-commands.md) |
| Patterns & best practices | [patterns.md](references/patterns.md) |
| State management | [state-management.md](references/state-management.md) |
| Multi-account setup | [multi-account.md](references/multi-account.md) |
| Performance optimization | [performance.md](references/performance.md) |
| CI/CD pipelines | [cicd-pipelines.md](references/cicd-pipelines.md) |

## Core Concepts

### Values Pattern

Units receive configuration through `values.xxx`:

```hcl
inputs = {
  name        = values.name
  environment = values.environment
  instance_class = try(values.instance_class, "db.t3.medium")  # Optional with default
}
```

### Reference Resolution

Units resolve symbolic references like `"../acm"` to dependency outputs:

```hcl
inputs = {
  acm_certificate_arn = try(values.acm_certificate_arn, "") == "../acm" ?
    dependency.acm.outputs.acm_certificate_arn :
    values.acm_certificate_arn
}
```

### Module Sourcing

Units reference modules via Git URL with version from values:

```hcl
terraform {
  source = "git::git@github.com:YOUR_ORG/modules/rds.git//app?ref=${values.version}"
}
```

## Common Operations

### Create New Unit

1. Create `units/<name>/terragrunt.hcl`
2. Reference module via Git URL with `${values.version}`
3. Use `values.xxx` for inputs
4. Add dependencies with mock outputs
5. Implement reference resolution for `"../unit"` patterns

### Create New Stack

1. Create `stacks/<name>/terragrunt.stack.hcl`
2. Define `locals` for computed values
3. Add `unit` blocks referencing catalog units
4. Pass values including version and dependency paths

### Deploy to New Environment

1. Create environment directory structure
2. Add `env.hcl` with `state_bucket_suffix`
3. Run `./setup-state-backend.sh` to create state resources
4. Add stack files referencing catalog

## Best Practices

1. **Pin module versions** - Use Git tags in `values.version`
2. **Pin catalog versions** - Use refs in unit source URLs
3. **Use reference resolution** - `"../unit"` → dependency outputs
4. **Provide mock outputs** - Enable plan/validate without dependencies
5. **Auto-detect features** - `length(keys(try(values.X, {}))) > 0`
6. **Override paths** - `try(values.X_path, "../default")`
7. **Separate state per environment** - Use `state_bucket_suffix`

## Common Pitfalls

1. **Git refspec error** - Use `//path?ref=branch` NOT `?ref=branch//path`
2. **Heredoc in ternary** - Wrap in parentheses: `condition ? (\n<<-EOF\n...\nEOF\n) : ""`
3. **Missing mock outputs** - Always provide for plan/validate
4. **Hardcoded paths** - Use local paths only for testing

## Version Management

- **Development:** Branch refs (`ref=feature-branch`)
- **Testing:** RC tags (`ref=v1.0.0-rc1`)
- **Production:** Stable tags (`ref=v1.0.0`)
