---
name: descope-terraform
description: Set up and manage Descope projects with Terraform. Use when configuring authentication infrastructure as code, managing environments, creating roles/permissions, setting up connectors, or deploying Descope project configurations.
---

# Descope Terraform Provider

Manage Descope authentication projects as infrastructure-as-code using the official Terraform provider.

## Prerequisites

- Terraform CLI installed
- Paid Descope License (Pro +)
- Management Key from Company Settings (https://app.descope.com/company)
- Management Key must be scoped for all projects if creating new projects

## Provider Setup

```hcl
terraform {
  required_providers {
    descope = {
      source = "descope/descope"
    }
  }
}

provider "descope" {
  management_key = var.descope_management_key
}

variable "descope_management_key" {
  type      = string
  sensitive = true
}
```

## Resources

| Resource | Purpose |
|----------|---------|
| `descope_project` | Full project configuration (auth methods, roles, connectors, flows, settings) |
| `descope_management_key` | Management keys with RBAC scoping |
| `descope_descoper` | Console user accounts with role assignments |

See `references/project-resource.md` for the full `descope_project` schema.
See `references/other-resources.md` for `descope_management_key` and `descope_descoper` schemas.

## Quick Start - New Project

```hcl
resource "descope_project" "myproject" {
  name = "my-project"
  tags = ["staging"]
}
```

## Common Configurations

### Authentication Methods

```hcl
resource "descope_project" "myproject" {
  name = "my-project"

  authentication = {
    magic_link = {
      expiration_time = "1 hour"
    }
    password = {
      lock          = true
      lock_attempts = 3
      min_length    = 8
    }
    sso = {
      merge_users  = true
      redirect_url = var.descope_redirect_url
    }
  }
}
```

### Roles & Permissions (RBAC)

```hcl
resource "descope_project" "myproject" {
  name = "my-project"

  authorization = {
    permissions = [
      { name = "read:data", description = "Read access" },
      { name = "write:data", description = "Write access" },
    ]
    roles = [
      {
        name        = "viewer"
        permissions = ["read:data"]
      },
      {
        name        = "editor"
        permissions = ["read:data", "write:data"]
      },
    ]
  }
}
```

### Connectors

```hcl
resource "descope_project" "myproject" {
  name = "my-project"

  connectors = {
    http = [{
      name         = "My Webhook"
      base_url     = var.webhook_url
      bearer_token = var.webhook_secret
    }]
    aws_s3 = [{
      name     = "Audit Logs"
      role_arn = "arn:aws:iam::YOUR_ACCOUNT:role/connector-role"
      region   = "us-east-1"
      bucket   = "audit-logs-bucket"
    }]
  }
}
```

### Project Settings

```hcl
resource "descope_project" "myproject" {
  name = "my-project"

  project_settings = {
    refresh_token_expiration = "3 weeks"
    enable_inactivity        = true
    inactivity_time          = "1 hour"
  }
}
```

## What Terraform Manages vs. What It Does NOT

**Managed by Terraform:**
- Project settings, authentication methods, authorization (roles/permissions)
- Connectors, applications (OIDC/SAML), flows, JWT templates
- Custom attributes, styles, widgets

**NOT managed by Terraform (use Console/SDK/API instead):**
- Individual users and tenants
- SSO connections and SCIM configurations
- Dynamic per-tenant settings

## DO NOT

- DO NOT hardcode `management_key` in `.tf` files - use variables or environment variables (`DESCOPE_MANAGEMENT_KEY`)
- DO NOT commit `.tfstate` files to version control - they contain sensitive data
- DO NOT skip `terraform plan` before `terraform apply`
- DO NOT use the deprecated `project_id` provider argument

## Workflow

```bash
terraform init      # Install provider
terraform plan      # Preview changes
terraform apply     # Apply changes
terraform destroy   # Remove managed resources
```

## References

- `references/project-resource.md` - Full descope_project schema and all nested blocks
- `references/other-resources.md` - descope_management_key and descope_descoper schemas
- `references/connectors.md` - All supported connector types and configuration