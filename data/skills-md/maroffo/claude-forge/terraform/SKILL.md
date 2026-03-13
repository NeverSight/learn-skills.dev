---
name: terraform
description: "Terraform and Terragrunt for infrastructure as code. Use for IaC, modules, state management, HCL."
compatibility: "Requires terraform CLI. Optional: tflint, checkov, infracost."
allowed-tools: [mcp__acp__Read, mcp__acp__Edit, mcp__acp__Write, mcp__acp__Bash]
---

# ABOUTME: Terraform/Terragrunt IaC patterns, modules, state management
# ABOUTME: Best practices for HCL, DRY configs, security scanning

# Terraform & Terragrunt

## What's New (2025-2026)

| Feature | Description |
|---------|-------------|
| Import blocks | Declarative imports without CLI |
| Check blocks | Continuous validation assertions |
| Moved blocks | Refactor without state surgery |
| Ephemeral (OpenTofu) | Resources not stored in state |

**OpenTofu**: CNCF fork, 100% compatible, recommended for new projects (BSL licensing).

## Quick Reference

```bash
terraform init|plan|apply|destroy
terragrunt run-all apply
terraform fmt -recursive && terraform validate
terraform state list|show|rm|mv <resource>
```

**See:** `_AST_GREP.md` (sg patterns for HCL)

---

## Project Structure

**Simple:** `main.tf`, `variables.tf`, `outputs.tf`, `versions.tf`

**Multi-env:**
```
terraform/
├── modules/{vpc,eks}/
└── environments/{dev,staging,prod}/
```

## TF 1.5+ Blocks

```hcl
import { to = aws_instance.web; id = "i-1234567890abcdef0" }
moved { from = aws_instance.web; to = module.web.aws_instance.main }
check "health" {
  data "http" "api" { url = "https://api.example.com/health" }
  assert { condition = data.http.api.status_code == 200; error_message = "API down" }
}
```

---

## Terragrunt

**Benefits:** DRY configs, multi-env mgmt, dependency ordering, auto backend config

### Structure
```
infrastructure/
├── terragrunt.hcl           # Root
├── _envcommon/{vpc,eks}.hcl
├── {dev,staging,prod}/
│   └── {region}/{vpc,eks}/terragrunt.hcl
```

### Dependencies
```hcl
dependency "vpc" { config_path = "../vpc" }
inputs = { vpc_id = dependency.vpc.outputs.vpc_id }
```

---

## State Management

**Split by:** env, region, component, blast radius

```hcl
backend "s3" { bucket = "my-state"; key = "prod/terraform.tfstate"; encrypt = true; dynamodb_table = "terraform-locks" }
```

---

## Best Practices

| DO | DON'T |
|----|-------|
| Modules for reusable components | Hardcode values |
| Version modules | Commit .tfstate to git |
| `sensitive = true` for secrets | Share state across envs |

---

## Testing & Security

**Pipeline:** `fmt/validate` → `TFLint` → `Checkov/Trivy` → `Infracost`

```bash
terraform fmt -check -recursive && terraform validate
tflint --recursive
checkov -d . --framework terraform --compact
infracost breakdown --path .
```

---

## Code Review Checklist

**Security:** No hardcoded secrets, encrypted state, locking enabled, least-privilege IAM, Checkov passes

**Structure:** Versioned modules, validated variables, consistent naming

---

## Resources

| Tool | Purpose |
|------|---------|
| TFLint | Linter |
| Checkov | Security |
| Infracost | Cost estimation |

**Docs:** [Terraform](https://terraform.io/docs), [OpenTofu](https://opentofu.org/docs/), [Terragrunt](https://terragrunt.gruntwork.io/docs/)
