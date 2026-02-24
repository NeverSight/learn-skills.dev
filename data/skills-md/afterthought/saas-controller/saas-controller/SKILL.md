---
name: saas-controller
description: >
  Configure and operate saas-controller services in devenv projects.
  Use when configuring cloud services (Zuplo, Frontegg),
  running sc up for local dev, deploying with sc deploy, managing
  secrets with secretspec profiles, or troubleshooting saas-controller.
license: MIT
metadata:
  author: afterthought
  version: "1.0.0"
---

# SaaS Controller

Multi-cloud service orchestration for [devenv](https://devenv.sh). Declarative service definitions with pluggable providers. Manages local dev (`sc up` with Tailscale HTTPS) and cloud deployment (`sc deploy`).

## Architecture

Providers own the full service lifecycle. Each provider generates its own docker-compose stack with a Tailscale sidecar for HTTPS on the tailnet.

```
┌──────────────────────────────────────────────────────┐
│                  saas-controller                      │
│                                                       │
│  ┌────────────────────────────────────────────────┐  │
│  │              Providers (WHAT)                   │  │
│  │  Each provider owns up() + deploy()            │  │
│  ├────────────────────────────────────────────────┤  │
│  │  zuplo          │ API gateway + docs portal    │  │
│  │  docker-compose │ Generic compose stacks       │  │
│  │  [your own]     │ via externalProviders        │  │
│  └────────────────────────────────────────────────┘  │
│                                                       │
│  sc up topology (per service):                        │
│  ┌──────────────────────────────────────────┐        │
│  │ docker-compose stack                      │        │
│  │  ┌───────────┐  ┌──────────────────────┐ │        │
│  │  │ tailscale │  │ app container(s)     │ │        │
│  │  │ sidecar   │◀─│ network_mode:        │ │        │
│  │  │           │  │   service:tailscale  │ │        │
│  │  │ HTTPS:443 │  │ PORT=3000            │ │        │
│  │  └───────────┘  └──────────────────────┘ │        │
│  │  URL: https://sc-<slug>-<service>.<tailnet> │     │
│  └──────────────────────────────────────────┘        │
└──────────────────────────────────────────────────────┘
```

## Import

```nix
# devenv.yaml
imports:
  - github:afterthought/saas-controller
```

Or as a flake input:

```nix
# flake.nix
inputs.saas-controller.url = "github:afterthought/saas-controller";
# In your devenv module:
imports = [ inputs.saas-controller.outPath ];
```

## Example A: Minimal Service

A hello-world service running locally with Tailscale HTTPS:

```nix
# devenv.nix
{ pkgs, lib, config, ... }:
{
  imports = [ /* saas-controller module */ ];

  saas-controller.services.hello-world = {
    enable = true;
    provider = "hello-world";
    providerConfig = {
      path = "examples/hello-world";  # dir with server.mjs + Dockerfile
    };
    environments = {
      local.enable = true;
    };
  };
}
```

```bash
sc up              # Starts compose stack with tailscale sidecar
                   # Prints: https://sc-<slug>-hello-world.<tailnet>:443
```

## Example B: Zuplo Gateway with Secrets

A Zuplo API gateway with secretspec profiles, multiple environments, and secret management:

```nix
{ pkgs, lib, config, ... }:
{
  imports = [ /* saas-controller module */ ];

  saas-controller.services.my-gateway = {
    enable = true;
    displayName = "My API Gateway";
    provider = "zuplo";
    providerConfig = {
      project = "my-gateway";       # Zuplo project name
      account = "my-account";       # Zuplo account
      path = "services/my-gateway"; # Path to zuplo project in repo
    };

    environments = {
      local.enable = true;
      production.enable = true;
      preview.enable = true;
    };

    # Secret management
    secretspec = {
      auth.provider = "client-myorg";  # SecretSpec provider alias
      auth.saToken = "client-myorg";   # 1Password SA token alias
      environments = {
        local = {
          serviceProfiles = [ "tailscale" ];
          # → validates TS_CLIENT_SECRET, TS_CLIENT_ID
        };
        production = {
          serviceProfiles = [ "zuplo-backend" ];
          # → validates zuplo secrets for production
        };
      };
      tags = [ "tailscale" "zuplo" ]; # For filtered checking
    };
  };
}
```

```bash
sc up                              # Start locally with tailscale HTTPS
sc deploy my-gateway -e production  # Deploy to production
sc check-secrets --tag tailscale   # Validate tailscale secrets
```

## Secret Profiles

Secrets are managed in two layers: controller-level profile definitions and per-service composition.

### Controller Level: Define profiles

```nix
saas-controller.secretProfiles = {
  tailscale = {
    TS_CLIENT_SECRET = {
      description = "Tailscale OAuth client secret";
      required = true;
      providers = [ "saas-controller" ];
    };
    TS_CLIENT_ID = {
      description = "Tailscale OAuth client ID";
      required = false;
      providers = [ "saas-controller" ];
    };
  };
  my-api-keys = {
    API_KEY = {
      description = "External API key";
      providers = [ "saas-controller" ];
    };
  };
};
```

### Service Level: Compose profiles per environment

```nix
services.my-service.secretspec = {
  auth.provider = "client-myorg";      # SecretSpec provider alias
  auth.saToken = "client-myorg";       # 1Password SA token alias
  environments = {
    local = {
      serviceProfiles = [ "tailscale" ];
      # Only tailscale secrets needed locally
    };
    production = {
      serviceProfiles = [ "my-api-keys" ];
      # API keys needed for production deployment
    };
  };
  tags = [ "tailscale" ];            # For sc check-secrets --tag
};
```

### Provider Auto-Export

Providers can declare `secretProfiles` in their implementation. These are automatically merged into `saas-controller.secretProfiles`. When a service uses a provider, that provider's profiles are auto-included — no manual wiring needed.

For example, the `zuplo` provider exports `zuplo` and `zudoku` profiles. Any service with `provider = "zuplo"` automatically gets those profiles available.

### Checking Secrets

```bash
sc check-secrets                         # Check all services
sc check-secrets --tag tailscale         # Only tailscale-tagged services
sc check-secrets --service my-gateway    # Specific service
sc secret-status                         # Show secret-to-service mapping table
```

## CLI Reference

```bash
# Local development
sc up                                    # Start all local services
sc up my-gateway                         # Start specific service

# Deployment
sc deploy                                # Deploy all to production (default)
sc deploy --environment production       # Deploy all to production
sc deploy my-gateway -e preview          # Deploy specific service to preview
sc undeploy my-gateway                   # Remove persistent service

# Secret management
sc check-secrets                         # Validate all service secrets
sc check-secrets --tag tailscale         # Filter by tag
sc check-secrets --service my-gateway    # Filter by service
sc secret-status                         # Secret-to-service mapping table

# Secret reconciliation
sc setup-env production                  # Check all secrets for production
sc diff-secrets local production         # Compare secrets between environments
sc reconcile-secrets                     # Show all secrets across all environments
sc reconcile-secrets -e production       # Show secrets for one environment

# Other
sc help                                  # Show help
provision-projects                       # One-time project setup
```

### Task Integration

```bash
# sc up is also available as a devenv task
devenv tasks run saas:up

# Deploy with environment via task input
DEVENV_TASK_INPUT='{"environment": "production"}' devenv tasks run saas-deploy:my-gateway
```

## Provider Summary

| Provider | providerConfig keys | sc up? | Auto-exported profiles |
|----------|-------------------|--------|----------------------|
| `zuplo` | `project`, `account`, `path` | Yes | `zuplo`, `zudoku` |
| `docker-compose` | `path`, `composeFile`(opt), `tailscale`(opt) | Yes | (none) |

For detailed provider documentation: read `references/provider-reference.md`

## Extensibility

Register custom providers:

```nix
saas-controller.externalProviders.my-provider = ./providers/my-provider.nix;
```

See [EXTENDING.md](../../EXTENDING.md) for provider authoring guide and template.

## Tailscale Setup

`sc up` requires one-time Tailscale setup (ACL tags, OAuth client). See `references/tailscale-setup.md` for step-by-step instructions.

## SA Token Provider Setup

Services with `secretspec.auth.saToken` need the `sa-tokens` secretspec provider alias configured. The secretspec.toml is auto-generated from service configs at nix eval time — developers only configure the provider backend once.

**One-time setup per machine:**

```bash
secretspec config provider add sa-tokens "keyring://"   # macOS Keychain
secretspec config provider add sa-tokens "env://"       # Environment variables (CI)
```

**Naming:** `saToken = "client-willdan"` maps to `OP_SA_CLIENT_WILLDAN`.

**Verify:** `secretspec config provider list`

## Deeper Questions

For questions not covered here, use DeepWiki MCP:

```
ask_question("afterthought/saas-controller", "<your question>")
```

Or read the source at `github:afterthought/saas-controller`.
