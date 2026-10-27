---
name: terraform
description: Manage Spice.ai Cloud infrastructure as code with Terraform or OpenTofu using the spiceai/spiceai provider. Use this skill whenever the user wants to write Terraform/OpenTofu configs for Spice projects (the provider's `spiceai_app`), deployments, secrets, or org members, import existing Spice.ai resources into Terraform state, set up OAuth authentication for the provider, or use Terraform data sources for regions and container images. Also use when the user mentions "terraform" and "spice" together, or wants IaC for their Spice.ai Cloud infrastructure. For direct API management without Terraform, see cloud.
---

# Spice.ai Terraform Provider

Manage Spice.ai Cloud resources as infrastructure-as-code using the `spiceai/spiceai` Terraform provider. Supports apps, deployments, secrets, org members, and data sources for regions, runtime images, and API keys.

Spice.ai Cloud renamed apps to **projects** in Aug 2026. The provider (latest release v0.1.0) keeps the original names — `spiceai_app`, `spiceai_apps`, and `app_id` — so existing configurations work unchanged.

## Version Compatibility

Written for provider **`spiceai/spiceai` v0.1.x** (v0.1.0 is the only release) and the Spice.ai Cloud API as documented in September 2026; spicepod examples target **Spice v2.4.x** (checked against v2.4.0-rc.2).

- **Provider**: pin with `version = "~> 0.1"`. v0.1.0 keeps the pre-rename names (`spiceai_app`, `app_id`) and has no `storage_size_gb`. Check the [Registry](https://registry.terraform.io/providers/spiceai/spiceai/latest) for a newer release before using an argument this skill doesn't list.
- **Runtime**: a project runs the version its update channel resolves unless `image_tag` pins one (Enterprise plan). Stable can trail the latest OSS release — check the [changelog](https://docs.spice.ai/changelog) before relying on a new runtime feature in a spicepod.

| Old | Change | Use instead |
| --- | --- | --- |
| `image_tag = "1.5.0-models"` | `-models` tags removed in v2.0.0 | Omit `image_tag`, or a tag from `spiceai_container_images` (Enterprise) |
| `image_tag` on a non-Enterprise plan | Rejected (`403 image_tag_requires_enterprise`) | Omit it; the update channel selects the runtime |
| Spicepod `version = "v1beta1"` | Removed in v2.0.0 | `version = "v2"` (`v1` still loads, auto-migrated) |

## Provider Setup

```hcl
terraform {
  required_providers {
    spiceai = {
      source  = "spiceai/spiceai"
      version = "~> 0.1"
    }
  }
}

provider "spiceai" {
  client_id     = var.spiceai_client_id
  client_secret = var.spiceai_client_secret
  # api_endpoint = "https://api.spice.ai"  # optional, this is the default
}
```

**Requirements:** Terraform >= 1.0 or OpenTofu >= 1.0

### Authentication

The provider uses OAuth 2.0 Client Credentials. Set credentials via:

1. **Provider block** — `client_id` and `client_secret` arguments
2. **Environment variables** — `SPICEAI_CLIENT_ID` and `SPICEAI_CLIENT_SECRET` (plus optional `SPICEAI_API_ENDPOINT` and `SPICEAI_OAUTH_ENDPOINT`)

Create OAuth clients in the Spice.ai Portal: **Settings > OAuth Clients**. Grant the scopes the configuration needs (for example `apps:write`, `apps:delete`, `deployments:write`, `secrets:write`, `members:write`, `members:delete`). An OAuth client manages only the organization it was issued to.

```bash
export SPICEAI_CLIENT_ID="your-client-id"
export SPICEAI_CLIENT_SECRET="your-client-secret"
terraform plan
```

## Resources

### spiceai_app

Manages a Spice.ai Cloud project (formerly app).

```hcl
data "spiceai_regions" "available" {}

resource "spiceai_app" "analytics" {
  name        = "analytics-app"
  cname       = data.spiceai_regions.available.regions[0].cname
  description = "Production analytics"
  visibility  = "private"
  replicas    = 2

  spicepod = yamlencode({
    version = "v2"
    kind    = "Spicepod"
    name    = "analytics-app"
    datasets = [{
      from = "postgres:public.events"
      name = "events"
      params = {
        pg_host = "db.example.com"
        pg_user = "$${ secrets:PG_USER }"
        pg_pass = "$${ secrets:PG_PASS }"
      }
      acceleration = {
        enabled              = true
        engine               = "duckdb"
        refresh_check_interval = "5m"
      }
    }]
  })
}
```

**Arguments:**

| Argument                | Type   | Required | Notes                                                        |
| ----------------------- | ------ | -------- | ------------------------------------------------------------ |
| `name`                  | string | Yes      | 4–38 chars, letters/numbers/hyphens; forces replacement      |
| `cname`                 | string | Yes      | Region CNAME from `spiceai_regions` (e.g. `us-west-2-prod-aws-data`); forces replacement |
| `description`           | string | No       |                                                              |
| `visibility`            | string | No       | `public` or `private` (default: `private`)                   |
| `spicepod`              | string | No       | YAML or JSON spicepod configuration                          |
| `image_tag`             | string | No       | Pins the runtime version; Enterprise plan only (API `403` otherwise) |
| `replicas`              | number | No       | 1-10, within plan limits                                     |
| `region`                | string | No       | AWS region code                                              |
| `production_branch`     | string | No       | Git branch for production deployments                        |
| `node_group`            | string | No       | Kubernetes node group                                        |
| `storage_claim_size_gb` | number | No       | Persistent volume size in GB (Enterprise plan)               |

**Read-only attributes:** `id`, `api_key` (sensitive, primary key), `cluster_id`, `created_at`

Omit `image_tag` to deploy the runtime the project's update channel selects. A pinned tag must be a published version for that channel — take it from `spiceai_container_images` rather than hardcoding one.

### spiceai_deployment

Creates an immutable deployment for an app. Use `triggers` to auto-redeploy on config changes.

```hcl
resource "spiceai_deployment" "current" {
  app_id         = spiceai_app.analytics.id
  commit_message = "Deploy analytics app"

  triggers = {
    spicepod = spiceai_app.analytics.spicepod
    replicas = spiceai_app.analytics.replicas
  }
}
```

**Arguments:**

| Argument         | Type    | Required | Notes                                       |
| ---------------- | ------- | -------- | ------------------------------------------- |
| `app_id`         | string  | Yes      | App ID to deploy                            |
| `image_tag`      | string  | No       | Override runtime image (Enterprise plan)    |
| `replicas`       | number  | No       | Override replicas (1-10)                    |
| `debug`          | boolean | No       | Enable debug mode (default: false)          |
| `branch`         | string  | No       | Git branch for tracking                     |
| `commit_sha`     | string  | No       | Git commit SHA                              |
| `commit_message` | string  | No       | Deployment description                      |

**Read-only attributes:** `id`, `status` (`queued` | `in_progress` | `succeeded` | `failed` | `created`), `error_message`, `created_at`, `started_at`, `finished_at`

The `triggers` map causes Terraform to replace the deployment whenever any tracked value changes. Deployments are append-only: removing the resource only drops it from state and does not stop the running instance.

### spiceai_secret

Manages app secrets. Values are encrypted at rest.

```hcl
variable "secrets" {
  type      = map(string)
  sensitive = true
  default = {
    PG_USER       = "analytics"
    PG_PASS       = "secret123"
    OPENAI_API_KEY = "sk-..."
  }
}

resource "spiceai_secret" "app_secrets" {
  # for_each can't take a sensitive value: iterate the (non-secret) key names
  for_each = nonsensitive(toset(keys(var.secrets)))

  app_id = spiceai_app.analytics.id
  name   = each.key
  value  = var.secrets[each.key]
}
```

**Arguments:**

| Argument | Type   | Required | Notes                                                        |
| -------- | ------ | -------- | ------------------------------------------------------------ |
| `app_id` | number | Yes      |                                                              |
| `name`   | string | Yes      | Start with letter/underscore, alphanumeric + `_`; forces replacement |
| `value`  | string | Yes      | Sensitive. Must set manually after import (API masks values) |

**Read-only attributes:** `id`, `created_at`, `updated_at`

### spiceai_member

Manages organization members by Spice.ai username.

```hcl
variable "team" {
  type    = set(string)
  default = ["alice", "bob"]
}

resource "spiceai_member" "team" {
  for_each = var.team

  username = each.key
  roles    = ["member"]
}
```

**Arguments:**

| Argument   | Type     | Required | Notes                                                              |
| ---------- | -------- | -------- | ------------------------------------------------------------------ |
| `username` | string   | Yes      | Spice.ai username; forces replacement                              |
| `roles`    | string[] | No       | API default `["member"]`. Org roles: `admin`, `member`, `viewer` (read-only) |

**Read-only attributes:** `id` (same as `user_id`), `user_id`, `is_owner`, `created_at`

Organization owners cannot be managed via Terraform, and only an owner can grant `admin`.

## Data Sources

### spiceai_regions

```hcl
data "spiceai_regions" "available" {}

# Use: data.spiceai_regions.available.regions[0].cname
# Pick a region: one([for r in data.spiceai_regions.available.regions : r.cname if r.region == "us-west-2"])
```

Optional `env` filter (`prod` or `dev`). Returns `regions` list (each with `name`, `region`, `cname`, `provider`, `provider_name`, `is_default`, `disabled`) and `default` region identifier.

### spiceai_container_images

```hcl
data "spiceai_container_images" "stable" {
  channel = "stable"  # or "enterprise"
}

# Use: data.spiceai_container_images.stable.default
# Use: data.spiceai_container_images.stable.images[*].tag
```

Returns `images` list (each with `name`, `tag`, `channel`) and `default` tag. Only needed to pin `image_tag` (Enterprise plan).

### spiceai_api_keys

```hcl
data "spiceai_api_keys" "keys" {
  app_id = spiceai_app.analytics.id
}
```

Returns `api_key` (primary) and `api_key_2` (secondary), both sensitive.

### spiceai_app (data)

```hcl
data "spiceai_app" "existing" {
  id = "12345"
}
```

Retrieves details of an existing app by ID.

### spiceai_apps

```hcl
data "spiceai_apps" "all" {}

# Filter in Terraform
locals {
  prod_apps = [for app in data.spiceai_apps.all.apps : app if app.visibility == "private"]
}
```

Lists all apps in the organization.

### spiceai_members

```hcl
data "spiceai_members" "all" {}
```

Lists all organization members with `username`, `roles`, `is_owner`, and `user_id`.

### spiceai_secrets

```hcl
data "spiceai_secrets" "app" {
  app_id = spiceai_app.analytics.id
}
```

Lists secrets for an app. Values are always masked.

## Import

Import existing resources into Terraform state:

```bash
# App (by app ID)
terraform import spiceai_app.analytics 12345

# Deployment (appId/deploymentId)
terraform import spiceai_deployment.current 12345/67890

# Secret (appId/SECRET_NAME)
terraform import spiceai_secret.db_password 12345/DB_PASSWORD

# Member (by user ID)
terraform import spiceai_member.alice 789

# Member with for_each
terraform import 'spiceai_member.team["alice"]' 789
```

After importing `spiceai_secret`, manually set the `value` in your config — the API never returns plain-text values.

## Complete Example

```hcl
terraform {
  required_providers {
    spiceai = {
      source  = "spiceai/spiceai"
      version = "~> 0.1"
    }
  }
}

provider "spiceai" {}

# Look up available regions
data "spiceai_regions" "available" {}

# Create the app
resource "spiceai_app" "myapp" {
  name  = "my-analytics"
  cname = data.spiceai_regions.available.regions[0].cname

  spicepod = yamlencode({
    version  = "v2"
    kind     = "Spicepod"
    name     = "my-analytics"
    datasets = [{
      from = "postgres:public.events"
      name = "events"
      params = {
        pg_host = "db.example.com"
        pg_user = "$${ secrets:PG_USER }"
        pg_pass = "$${ secrets:PG_PASS }"
      }
    }]
    models = [{
      from = "openai:gpt-4o"
      name = "assistant"
      params = {
        openai_api_key = "$${ secrets:OPENAI_API_KEY }"
      }
    }]
  })
}

# Manage secrets
variable "app_secrets" {
  type      = map(string)
  sensitive = true
}

resource "spiceai_secret" "secrets" {
  for_each = nonsensitive(toset(keys(var.app_secrets)))
  app_id   = spiceai_app.myapp.id
  name     = each.key
  value    = var.app_secrets[each.key]
}

# Deploy (redeploys when app config changes)
resource "spiceai_deployment" "current" {
  app_id         = spiceai_app.myapp.id
  commit_message = "Managed by Terraform"

  triggers = {
    spicepod = spiceai_app.myapp.spicepod
  }

  depends_on = [spiceai_secret.secrets]
}

# Team access
resource "spiceai_member" "team" {
  for_each = toset(["alice", "bob"])
  username = each.key
}

# Outputs
output "app_id" {
  value = spiceai_app.myapp.id
}

output "api_key" {
  value     = spiceai_app.myapp.api_key
  sensitive = true
}

output "deployment_status" {
  value = spiceai_deployment.current.status
}
```

## Present Results to User

When generating Terraform configurations:
- Use `data.spiceai_regions` for region lookup instead of hardcoding
- Omit `image_tag` unless the organization is on the Enterprise plan; then take it from `data.spiceai_container_images` instead of hardcoding
- Use `version: v2` spicepods (`v1` still loads with automatic migration)
- Always use `for_each` for multiple secrets or members (over `nonsensitive(toset(keys(var.secrets)))` — `for_each` rejects sensitive values)
- Mark secret values and API keys as `sensitive`
- Include `triggers` on deployments to auto-redeploy on changes
- Use `depends_on` to ensure secrets exist before deploying
- Reference secrets in spicepod with `$${ secrets:NAME }` (double `$` for Terraform escaping)

## Troubleshooting

| Issue                                  | Solution                                                                        |
| -------------------------------------- | ------------------------------------------------------------------------------- |
| `401` or auth errors                   | Verify `SPICEAI_CLIENT_ID` / `SPICEAI_CLIENT_SECRET` and that the OAuth client hasn't expired |
| `403` with `insufficient_scope`        | Grant the OAuth client the scope the resource needs (e.g. `secrets:write`)      |
| `403 image_tag_requires_enterprise`    | Remove `image_tag` (and `triggers` on it); the update channel selects the runtime |
| Import loses secret value              | Expected — set `value` in config after import; API always masks values           |
| Deployment `failed`                    | Read `error_message`; a project needs a valid `spicepod` before it can deploy   |
| `409` on deployment                    | Previous deployment still in progress; wait or check status                     |
| Spicepod YAML syntax errors            | Use `yamlencode()` for type safety; validate YAML before applying               |
| `$$` showing in spicepod               | Use `$${ secrets:NAME }` in Terraform — the double `$` escapes to single `$`     |
| Cannot delete org owner                | Organization owners cannot be modified or removed via Terraform or the API      |
| Provider not found                     | Check `source = "spiceai/spiceai"` and run `terraform init`                     |

## Documentation

- [Terraform Provider Docs](https://docs.spice.ai/api/management-api/terraform)
- [Terraform Registry](https://registry.terraform.io/providers/spiceai/spiceai/latest)
- [GitHub Repository](https://github.com/spiceai/terraform-provider-spiceai)
- [Spice.ai Management API](https://docs.spice.ai/api/management-api/management)
