---
name: opentofu
description: |
  Infrastructure as code with OpenTofu (open-source Terraform fork) and Pulumi. Covers OpenTofu HCL syntax, providers, resources, data sources, modules, state management with remote backends, workspaces, importing existing infrastructure, plan/apply workflow, variable management, output values, provisioners, and state encryption (OpenTofu-exclusive). Includes Pulumi TypeScript/Python SDKs, stack management, component resources, config/secrets, state backends, policy as code, and automation API. Common patterns for multi-environment setups, module composition, CI/CD integration, drift detection, and secret management.

  Use when writing or reviewing HCL configurations, managing cloud infrastructure state, migrating from Terraform to OpenTofu, building Pulumi programs in TypeScript or Python, setting up multi-environment IaC pipelines, or implementing state encryption.
license: MIT
metadata:
  author: oakoss
  version: '1.0'
  source: 'https://opentofu.org/docs'
user-invocable: false
---

# OpenTofu

## Overview

OpenTofu is an open-source infrastructure as code tool that uses HCL (HashiCorp Configuration Language) to declaratively manage cloud infrastructure. It is a community-driven fork of Terraform, fully compatible with existing Terraform providers and modules, with exclusive features like native state encryption. Pulumi provides an alternative IaC approach using general-purpose languages (TypeScript, Python, Go) instead of HCL.

**When to use:** Managing cloud infrastructure declaratively, provisioning multi-cloud resources, enforcing infrastructure consistency across environments, encrypting state at rest (OpenTofu), using familiar programming languages for IaC (Pulumi).

**When NOT to use:** One-off scripts better suited to CLI tools, application-level configuration management (use Ansible/Chef), container orchestration logic (use Kubernetes manifests), simple static hosting (use platform-native tools).

## Quick Reference

| Pattern            | Tool / Command                         | Key Points                                     |
| ------------------ | -------------------------------------- | ---------------------------------------------- |
| Initialize project | `tofu init`                            | Downloads providers, initializes backend       |
| Preview changes    | `tofu plan`                            | Shows diff without applying                    |
| Apply changes      | `tofu apply`                           | Provisions/updates resources                   |
| Destroy resources  | `tofu destroy`                         | Tears down managed infrastructure              |
| Import resource    | `tofu import <addr> <id>`              | Brings existing resource under management      |
| State encryption   | `terraform.encryption` block           | OpenTofu-exclusive, AES-GCM with key providers |
| Remote backend     | `backend "s3"` / `backend "gcs"`       | Store state in cloud storage with locking      |
| Workspaces         | `tofu workspace new <name>`            | Isolated state per environment                 |
| Module usage       | `module "name" { source = "..." }`     | Reusable infrastructure components             |
| Output values      | `output "name" { value = ... }`        | Expose values for other configs or CI          |
| Variable files     | `terraform.tfvars` / `-var-file`       | Environment-specific variable overrides        |
| Pulumi new project | `pulumi new typescript`                | Scaffold TypeScript IaC project                |
| Pulumi preview     | `pulumi preview`                       | Shows planned changes                          |
| Pulumi deploy      | `pulumi up`                            | Provisions/updates resources                   |
| Pulumi config      | `pulumi config set key value`          | Stack-scoped configuration                     |
| Pulumi secrets     | `pulumi config set --secret key val`   | Encrypted config values                        |
| Pulumi stacks      | `pulumi stack select <name>`           | Switch between environments                    |
| Automation API     | `LocalWorkspace.createOrSelectStack()` | Programmatic stack management                  |

## Common Mistakes

| Mistake                                              | Correct Pattern                                                   |
| ---------------------------------------------------- | ----------------------------------------------------------------- |
| Storing state locally in team environments           | Configure remote backend (S3, GCS, Azure Blob) with state locking |
| Hardcoding provider credentials in HCL               | Use environment variables or provider-specific auth chains        |
| Using `tofu apply` without reviewing plan            | Run `tofu plan -out=plan.tfplan` then `tofu apply plan.tfplan`    |
| Editing state manually                               | Use `tofu state mv`, `tofu state rm`, or `tofu import`            |
| Ignoring `.terraform.lock.hcl`                       | Commit lock file for reproducible provider versions               |
| Using `count` for complex conditional resources      | Prefer `for_each` with maps for stable resource addressing        |
| Sharing one workspace for all environments           | Use separate workspaces or backend config per environment         |
| Putting secrets in `terraform.tfvars`                | Use `sensitive = true` variables, vault, or environment variables |
| Pulumi: creating resources outside component classes | Wrap related resources in ComponentResource for reuse             |
| Pulumi: not awaiting async operations                | Ensure all resource operations complete before stack export       |
| Skipping `tofu plan` in CI/CD                        | Always plan and require approval before apply in pipelines        |
| Not using `-target` carefully                        | Prefer full plans; `-target` can leave state inconsistent         |

## Delegation

- **Infrastructure pattern discovery**: Use `Explore` agent
- **IaC code review**: Use `Task` agent
- **Drift detection analysis**: Use `Task` agent

> If the `amazon-web-services` skill is available, delegate AWS resource patterns to it.
> If the `docker` skill is available, delegate container infrastructure patterns to it.
> If the `github-actions` skill is available, delegate CI/CD pipeline patterns to it.

## References

- [HCL syntax, resources, data sources, and providers](references/hcl-fundamentals.md)
- [Modules, composition, and reusable infrastructure](references/modules.md)
- [State management, remote backends, and locking](references/state-management.md)
- [State encryption with OpenTofu-exclusive key providers](references/state-encryption.md)
- [Variables, outputs, and environment configuration](references/variables-outputs.md)
- [Workspaces and multi-environment setups](references/workspaces.md)
- [Import existing infrastructure and migration patterns](references/import-migration.md)
- [Pulumi TypeScript and Python SDK patterns](references/pulumi-sdk.md)
- [Pulumi stacks, config, secrets, and automation API](references/pulumi-stacks.md)
- [CI/CD integration and drift detection](references/cicd-integration.md)
