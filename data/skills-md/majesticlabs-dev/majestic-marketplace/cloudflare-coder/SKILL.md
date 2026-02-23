---
name: cloudflare-coder
description: This skill guides provisioning Cloudflare infrastructure with OpenTofu/Terraform. Use when managing zones, DNS records, WAF rules, SSL settings, Page Rules, or cache configuration.
allowed-tools: Read Write Edit Grep Glob Bash
---

## Provider Setup

```hcl
terraform {
  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 4.0"
    }
  }
}

provider "cloudflare" {
  # Uses CLOUDFLARE_API_TOKEN env var
}
```

### Authentication

```bash
export CLOUDFLARE_API_TOKEN="your-api-token"
# Or with 1Password
CLOUDFLARE_API_TOKEN=op://Infrastructure/Cloudflare/api_token
```

See [references/cloudflare-api-permissions.md](references/cloudflare-api-permissions.md) for token permissions and legacy API key setup.

## Data Sources

### Get Zone by Name

```hcl
data "cloudflare_zone" "main" {
  name = "example.com"
}
```

### Get Account ID

```hcl
data "cloudflare_accounts" "main" {
  name = "My Account"
}

output "account_id" {
  value = data.cloudflare_accounts.main.accounts[0].id
}
```

## DNS Records

### Basic Records

```hcl
resource "cloudflare_record" "root" {
  zone_id = data.cloudflare_zone.main.id
  name    = "@"
  type    = "A"
  content = var.server_ip
  ttl     = 1  # 1 = automatic
  proxied = true
}

resource "cloudflare_record" "www" {
  zone_id = data.cloudflare_zone.main.id
  name    = "www"
  type    = "CNAME"
  content = "@"
  ttl     = 1
  proxied = true
}

resource "cloudflare_record" "mx_primary" {
  zone_id  = data.cloudflare_zone.main.id
  name     = "@"
  type     = "MX"
  content  = "mail.example.com"
  ttl      = 3600
  priority = 10
  proxied  = false  # MX cannot be proxied
}
```

### DNS Records with for_each

```hcl
locals {
  dns_records = {
    api = {
      type    = "A"
      content = var.api_server_ip
      proxied = true
    }
    staging = {
      type    = "A"
      content = var.staging_server_ip
      proxied = true
    }
    mail = {
      type    = "A"
      content = var.mail_server_ip
      proxied = false
    }
  }
}

resource "cloudflare_record" "subdomain" {
  for_each = local.dns_records

  zone_id = data.cloudflare_zone.main.id
  name    = each.key
  type    = each.value.type
  content = each.value.content
  ttl     = 1
  proxied = each.value.proxied
}
```

## SSL/TLS Settings

### Zone SSL Settings

```hcl
resource "cloudflare_zone_settings_override" "ssl" {
  zone_id = data.cloudflare_zone.main.id

  settings {
    ssl                      = "strict"
    min_tls_version          = "1.2"
    always_use_https         = "on"
    automatic_https_rewrites = "on"
    tls_1_3                  = "on"
    opportunistic_encryption = "on"

    security_header {
      enabled            = true
      max_age            = 31536000
      include_subdomains = true
      preload            = true
      nosniff            = true
    }
  }
}
```

### Origin Certificates

```hcl
resource "cloudflare_origin_ca_certificate" "origin" {
  csr                = tls_cert_request.origin.cert_request_pem
  hostnames          = ["example.com", "*.example.com"]
  request_type       = "origin-rsa"
  requested_validity = 5475  # 15 years (max)
}

resource "tls_private_key" "origin" {
  algorithm = "RSA"
  rsa_bits  = 2048
}

resource "tls_cert_request" "origin" {
  private_key_pem = tls_private_key.origin.private_key_pem

  subject {
    common_name  = "example.com"
    organization = "Example Inc"
  }
}

output "origin_certificate" {
  value     = cloudflare_origin_ca_certificate.origin.certificate
  sensitive = true
}
```

## Cache Rules

### Modern Cache Rules (Rulesets)

```hcl
resource "cloudflare_ruleset" "cache" {
  zone_id     = data.cloudflare_zone.main.id
  name        = "Cache Rules"
  description = "Caching configuration"
  kind        = "zone"
  phase       = "http_request_cache_settings"

  rules {
    action = "set_cache_settings"
    action_parameters {
      cache = true
      edge_ttl {
        mode    = "override_origin"
        default = 2592000  # 30 days
      }
      browser_ttl {
        mode    = "override_origin"
        default = 86400  # 1 day
      }
    }
    expression  = "(http.request.uri.path.extension in {\"css\" \"js\" \"jpg\" \"jpeg\" \"png\" \"gif\" \"svg\" \"woff\" \"woff2\"})"
    description = "Cache static assets"
    enabled     = true
  }

  rules {
    action = "set_cache_settings"
    action_parameters {
      cache = false
    }
    expression  = "(starts_with(http.request.uri.path, \"/api/\"))"
    description = "Bypass cache for API"
    enabled     = true
  }

}
```

## Redirect Rules

```hcl
resource "cloudflare_ruleset" "redirects" {
  zone_id     = data.cloudflare_zone.main.id
  name        = "Redirects"
  description = "URL redirects"
  kind        = "zone"
  phase       = "http_request_dynamic_redirect"

  rules {
    action = "redirect"
    action_parameters {
      from_value {
        status_code = 301
        target_url {
          expression = "concat(\"https://example.com\", http.request.uri.path)"
        }
        preserve_query_string = true
      }
    }
    expression  = "(http.host eq \"www.example.com\")"
    description = "Redirect www to apex"
    enabled     = true
  }

  rules {
    action = "redirect"
    action_parameters {
      from_value {
        status_code = 301
        target_url {
          value = "https://example.com/new-page"
        }
      }
    }
    expression  = "(http.request.uri.path eq \"/old-page\")"
    description = "Redirect old page to new"
    enabled     = true
  }
}
```

## Zone Settings

### Performance Settings

```hcl
resource "cloudflare_zone_settings_override" "performance" {
  zone_id = data.cloudflare_zone.main.id

  settings {
    brotli        = "on"
    early_hints   = "on"
    http2         = "on"
    http3         = "on"
    zero_rtt      = "on"
    rocket_loader = "on"

    minify {
      css  = "on"
      html = "on"
      js   = "on"
    }
  }
}
```

### Security Settings

```hcl
resource "cloudflare_zone_settings_override" "security" {
  zone_id = data.cloudflare_zone.main.id

  settings {
    security_level      = "medium"  # off, essentially_off, low, medium, high, under_attack
    challenge_ttl       = 1800
    browser_check       = "on"
    email_obfuscation   = "on"
    server_side_exclude = "on"
    hotlink_protection  = "on"
    ip_geolocation      = "on"
  }
}
```

## Workers Routes

```hcl
resource "cloudflare_worker_route" "api" {
  zone_id     = data.cloudflare_zone.main.id
  pattern     = "example.com/api/*"
  script_name = cloudflare_worker_script.api.name
}

resource "cloudflare_worker_script" "api" {
  account_id = var.cloudflare_account_id
  name       = "api-worker"
  content    = file("${path.module}/workers/api.js")
  module     = true

  plain_text_binding {
    name = "ENVIRONMENT"
    text = var.environment
  }

  secret_text_binding {
    name = "API_KEY"
    text = var.api_key
  }
}
```

## References

- [references/cloudflare-api-permissions.md](references/cloudflare-api-permissions.md) - Token permissions and auth setup
- [references/waf.md](references/waf.md) - IP access rules, WAF custom rules, managed rulesets
- [references/load-balancer.md](references/load-balancer.md) - Argo Smart Routing, load balancer config
- [references/production-zone.md](references/production-zone.md) - Complete production Terraform configuration
