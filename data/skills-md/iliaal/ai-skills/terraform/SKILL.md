---
name: terraform
description: >-
  Terraform and OpenTofu configuration, modules, testing, state management, and
  HCL review. Use when working with Terraform, OpenTofu, HCL, tfvars, tftest,
  state migration, or IaC patterns.
---

# Terraform & OpenTofu

## File Organization & Naming

| File | Purpose |
|------|---------|
| `terraform.tf` | Terraform + provider version requirements |
| `providers.tf` | Provider configurations |
| `main.tf` | Primary resources and data sources |
| `variables.tf` | Input variables (alphabetical) |
| `outputs.tf` | Output values (alphabetical) |
| `locals.tf` | Local values |

- Lowercase with underscores: `web_api`, not `webAPI` or `web-api`
- Descriptive nouns excluding resource type: `aws_instance.web_api` not `aws_instance.web_api_instance`
- Singular, not plural
- `this` for singleton resources (one of that type per module)
- Contextual variable prefixes: `vpc_cidr_block` not `cidr`

## Block Ordering

**Resources:** `count`/`for_each` (blank line after) → arguments → nested blocks → `tags` → `depends_on` → `lifecycle` (last)

**Variables:** `description` → `type` → `default` → `validation` → `nullable`

Every variable needs `type` + `description`. Every output needs `description`. Mark secrets `sensitive = true`.

## Module Structure

| Type | Scope | Example |
|------|-------|---------|
| Resource Module | Single logical group | VPC + subnets, SG + rules |
| Infrastructure Module | Collection of resource modules | Networking + compute for one region |
| Composition | Complete infrastructure | Spans regions/accounts |

```
module-name/
├── main.tf, variables.tf, outputs.tf, versions.tf
├── examples/
│   ├── minimal/
│   └── complete/
└── tests/
    └── defaults.tftest.hcl
```

Keep modules small (single responsibility). `examples/` double as documentation and integration test fixtures. Semantic versioning for all published modules.

## count vs for_each

| Scenario | Use |
|----------|-----|
| Boolean toggle (create or skip) | `count = condition ? 1 : 0` |
| Named/keyed items that may reorder | `for_each = toset(list)` or `map` |
| Fixed identical replicas | `count = N` |

Default to `for_each` — removing a middle item from a `count` list recreates all subsequent resources. Use `count` only for boolean conditionals or truly identical replicas.

## Testing

| Situation | Approach |
|-----------|----------|
| Quick validation | `terraform fmt -check && terraform validate` |
| Pre-commit | + `tflint` + `trivy config .` / `checkov -d .` |
| Logic validation (1.6+) | Native `terraform test` with `command = plan` |
| Cost-free unit tests (1.7+) | Native tests + `mock_provider` |
| Real infra validation | Native tests with `command = apply`, or Terratest (Go) |

**Native test essentials** (`.tftest.hcl` in `tests/`):
- `command = plan` for fast unit tests; `command = apply` for integration (default)
- `assert { condition = expr; error_message = "..." }` — multiple per run block
- `expect_failures = [var.name]` for negative testing (validate rejection of bad input)
- `mock_provider "aws" { mock_resource "..." { defaults = { ... } } }` — plan-mode only, no credentials, fast CI
- `variables {}` at file level (all runs) or within a `run` block (override)
- Reference prior run outputs: `run.setup.vpc_id`
- `parallel = true` on independent runs with separate state — creates sync point at next sequential run
- `state_key = "name"` required for `parallel = true` runs with independent state
- File naming: `*_unit_test.tftest.hcl` (plan mode) vs `*_integration_test.tftest.hcl` (apply mode)

## Version Pinning

| Component | Strategy | Example |
|-----------|----------|---------|
| Terraform | Pin minor | `required_version = "~> 1.9"` |
| Providers | Pin major | `version = "~> 5.0"` |
| Modules (prod) | Pin exact | `version = "5.1.2"` |
| Modules (dev) | Allow patch | `version = "~> 5.1"` |

Key modern features: `moved` blocks (1.1+), `optional()` with defaults (1.3+), native testing (1.6+), mock providers (1.7+), cross-variable validation (1.9+), write-only arguments (1.11+).
Stacks (HCP, preview): orchestrates multiple configs as a single deployment unit — evaluate for multi-environment patterns.

## State & Security

- Remote backend with locking: S3+DynamoDB, Azure Blob, GCS, or Terraform Cloud. Never local state for shared infrastructure.
- Encrypt state at rest. Never commit `.tfstate`, `.terraform/`, or `*.tfplan`. Always commit `.terraform.lock.hcl`.
- `default_tags` on provider for consistent resource tagging.
- Encryption at rest on all storage. Private networking by default — public access is opt-in.
- Least-privilege security groups. No `0.0.0.0/0` ingress without explicit justification.
- Never hardcode credentials — use assume_role, OIDC, or secrets managers.
- Pre-commit: `terraform fmt -recursive && terraform validate && trivy config .`
- `moved { from = old; to = new }` for refactoring resource names/modules without destroy-recreate. Remove block after apply.

## Troubleshooting

- State lock stuck: `terraform force-unlock <ID>` — only after confirming no other operation running
- Resource drift: `terraform plan -refresh-only` to detect, `terraform apply -refresh-only` to accept
- Replace tainted: `terraform apply -replace=ADDR` (not deprecated `terraform taint`)
- Import existing: `import` blocks (1.5+) for declarative import, or `terraform import ADDR ID`

## Dependency Management

Use `locals` with `try()` to control deletion ordering without explicit `depends_on`:

```hcl
locals {
  vpc_id = try(aws_vpc_ipv4_cidr_block_association.this[0].vpc_id, aws_vpc.this.id, "")
}
```

This forces Terraform to destroy subnets before CIDR associations — prevents deletion errors.

- `cidrsubnet(var.vpc_cidr, 8, count.index)` for calculated subnet CIDRs — never hardcode subnets
- Multi-region: `provider "aws" { alias = "eu_west_1" }` + `providers = { aws = aws.eu_west_1 }` in module blocks
