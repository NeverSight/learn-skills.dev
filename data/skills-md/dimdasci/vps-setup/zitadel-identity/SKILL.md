---
name: zitadel-identity
description: |
  Zitadel identity provider setup, configuration, and OIDC integration. Use when:
  (1) Setting up Zitadel as OIDC/OAuth2 identity provider
  (2) Configuring Zitadel with Caddy reverse proxy
  (3) Creating OAuth2/OIDC applications for services
  (4) Managing users, organizations, and service accounts
  (5) Integrating applications with Zitadel SSO (Nextcloud, Windmill, etc.)
  (6) Troubleshooting authentication, token, or connectivity issues
  (7) Using Zitadel APIs for automation
---

# Zitadel Identity Provider

Zitadel is a modern identity management platform providing OIDC, OAuth2, and SAML authentication. This skill covers Docker deployment with Caddy reverse proxy.

## Quick Reference

| Task | Command/Location |
|------|------------------|
| Console UI | `https://auth.example.com/ui/console` |
| OIDC Discovery | `https://auth.example.com/.well-known/openid-configuration` |
| Health check | `curl https://auth.example.com/healthz` |
| View logs | `docker compose logs -f zitadel zitadel-login` |
| Restart | `docker compose restart zitadel zitadel-login` |

## Architecture

```
Internet → Caddy (80/443) → Zitadel API (h2c://zitadel:8080)
                          → Login UI (http://zitadel-login:3000)

PostgreSQL ← zitadel-init (runs once)
           ← zitadel (API server)
```

Three containers:
- `zitadel-init` - Database initialization (runs once, exits)
- `zitadel` - API server (gRPC/REST on port 8080)
- `zitadel-login` - Login UI (port 3000)

## Essential Environment Variables

```bash
# Required
ZITADEL_MASTERKEY=<32-char-random-string>
ZITADEL_DATABASE_POSTGRES_HOST=postgres
ZITADEL_DATABASE_POSTGRES_USER_PASSWORD=<password>
ZITADEL_EXTERNALDOMAIN=auth.example.com
ZITADEL_EXTERNALPORT=443
ZITADEL_EXTERNALSECURE=true
ZITADEL_TLS_ENABLED=false  # Caddy handles TLS
```

Generate masterkey: `tr -dc A-Za-z0-9 </dev/urandom | head -c 32`

## Caddy Configuration

**Critical**: Use `h2c://` for HTTP/2 cleartext (required for gRPC):

```caddyfile
auth.example.com {
    handle /ui/v2/login/* {
        reverse_proxy http://zitadel-login:3000
    }
    handle {
        reverse_proxy h2c://zitadel:8080
    }
}
```

## Deployment Steps

1. **Start PostgreSQL**:
   ```bash
   docker compose up -d postgres
   ```

2. **Initialize database**:
   ```bash
   docker compose run zitadel-init
   ```

3. **Start services**:
   ```bash
   docker compose up -d zitadel zitadel-login caddy
   ```

4. **Verify health**:
   ```bash
   curl https://auth.example.com/healthz
   ```

5. **Access console**:
   ```
   https://auth.example.com/ui/console
   ```

## Creating OIDC Applications

1. Console → Organization → Projects → Applications → **+ New**
2. Select application type (Web, Native, API)
3. Configure redirect URIs
4. Save and copy **Client ID** and **Client Secret**

Common redirect URIs:
- Nextcloud: `https://files.example.com/apps/user_oidc/code`
- Windmill: `https://windmill.example.com/user/login_callback/zitadel`

## Service Users (API Access)

1. Console → Users → Service Users → **+ New**
2. Create Personal Access Token (PAT)
3. Assign roles (Org Owner, Project Owner)
4. Use in API calls:
   ```bash
   curl -H "Authorization: Bearer <PAT>" \
     https://auth.example.com/management/v1/orgs/me
   ```

## Reference Files

| File | When to Read |
|------|--------------|
| [configuration.md](references/configuration.md) | Environment variables, config file options |
| [caddy-integration.md](references/caddy-integration.md) | Reverse proxy setup, h2c configuration |
| [oidc-applications.md](references/oidc-applications.md) | Creating apps, Nextcloud integration |
| [api-reference.md](references/api-reference.md) | REST/gRPC endpoints, authentication |
| [troubleshooting.md](references/troubleshooting.md) | Common issues and diagnostics |

## Official Documentation

| Topic | URL |
|-------|-----|
| Self-Hosting | https://zitadel.com/docs/self-hosting/deploy/overview |
| Configuration | https://zitadel.com/docs/self-hosting/manage/configure |
| Caddy Setup | https://zitadel.com/docs/self-hosting/manage/reverseproxy/caddy |
| OIDC Integration | https://zitadel.com/docs/guides/integrate/login/oidc |
| API Reference | https://zitadel.com/docs/apis/introduction |
| Service Users | https://zitadel.com/docs/guides/integrate/service-users/personal-access-token |

## Troubleshooting Quick Guide

| Issue | Check |
|-------|-------|
| Container won't start | `docker compose logs zitadel` - check masterkey (32 chars) |
| Login page blank | `docker compose ps zitadel-login` - check Caddy routes |
| gRPC errors | Ensure `h2c://` in Caddyfile, not `http://` |
| OIDC 404 | `curl https://auth.example.com/healthz` - check external domain |
| Token invalid | Check issuer URL matches, token not expired |
