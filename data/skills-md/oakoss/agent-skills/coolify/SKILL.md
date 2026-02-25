---
name: coolify
description: |
  Coolify self-hosted PaaS for deploying applications, databases, and services via REST API and Git integration. Covers API authentication, deployment triggers, build packs (Nixpacks, Dockerfile, Compose), CI/CD with GitHub Actions webhooks, environment management, and Traefik proxy configuration.

  Use when deploying apps to Coolify, triggering deployments via API, configuring build packs, setting up GitHub Actions CI/CD pipelines, managing environment variables, or troubleshooting deployment failures.
license: MIT
metadata:
  author: oakoss
  version: '1.0'
  source: 'https://coolify.io/docs'
user-invocable: false
---

# Coolify

## Overview

Coolify is a self-hosted PaaS (Vercel/Netlify alternative) that deploys applications, databases, and services on your own infrastructure. It provides a REST API for programmatic control, supports multiple build packs, and uses Traefik for reverse proxy and SSL.

**When to use:** Deploying applications to self-hosted infrastructure, managing databases and services through API, automating deployments via CI/CD, self-hosting without vendor lock-in.

**When NOT to use:** Initial Coolify server installation (use the official install script via browser), managing Coolify's own infrastructure (Postgres, Redis — managed internally), or when a managed platform (Vercel, Railway) meets your needs without self-hosting requirements.

## Quick Reference

| Pattern               | Approach                                                | Key Points                                        |
| --------------------- | ------------------------------------------------------- | ------------------------------------------------- |
| API auth              | `Authorization: Bearer <token>` header                  | Token created in dashboard, scoped permissions    |
| List applications     | `GET /api/v1/applications`                              | Returns all apps with status and config           |
| Trigger deploy        | `GET /api/v1/deploy?uuid=<app>&force=true`              | Or use per-app webhook URL                        |
| Create application    | `POST /api/v1/applications/public`                      | Requires project_uuid, server_uuid, env_name      |
| Update application    | `PATCH /api/v1/applications/<uuid>`                     | Accepts build, health check, domain, limit fields |
| Auto-deploy           | Enable in Advanced > General                            | Deploys on every push to configured branch        |
| Webhook deploy        | `curl GET <webhook_url> -H "Authorization: Bearer ..."` | Controlled deploys from CI pipelines              |
| GitHub Actions deploy | Build image, push to registry, trigger webhook          | Full control over build + test before deploy      |
| Nixpacks build        | Auto-detected from source code                          | Zero-config for supported languages               |
| Dockerfile build      | Set build pack to `dockerfile`                          | Full control over build process                   |
| Compose build         | `docker-compose.yaml` as source of truth                | Multi-service stacks with Coolify labels          |
| Environment variables | API or dashboard per-environment                        | Interpolated in Compose via `${VAR}` syntax       |
| Domain routing        | `fqdn` field or Traefik labels in Compose               | Automatic SSL via Let's Encrypt                   |
| Health checks         | Configurable path, interval, retries via API            | Required for `running:healthy` status             |

## Common Mistakes

| Mistake                                         | Correct Pattern                                                    |
| ----------------------------------------------- | ------------------------------------------------------------------ |
| API returns "Unauthenticated"                   | Add `Accept: application/json` header alongside Bearer token       |
| Can't read sensitive fields (auto-deploy, etc.) | Token needs `view:sensitive` or `*` permission scope               |
| Auto-deploy not triggering                      | Verify GitHub App is connected and auto-deploy enabled in Advanced |
| Using API token without deploy permission       | Token needs explicit `deploy` permission to trigger deployments    |
| Health check fails on Compose services          | Add `exclude_from_hc: true` label for non-HTTP services            |
| Webhook deploy without auth header              | Always include `Authorization: Bearer <token>` with webhook calls  |
| Environment variables not available in build    | Use build arguments in Advanced menu, not runtime env vars         |
| Compose services can't communicate              | Use service names as hostnames within the same stack network       |

## Delegation

- **API exploration**: Use `Explore` agent to discover existing Coolify resources
- **Dockerfile optimization**: Use `Task` agent to review Dockerfiles for Coolify deployment
- **CI/CD pipeline design**: Use `Plan` agent for deployment workflow strategy

> If the `docker` skill is available, delegate Dockerfile authoring, multi-stage builds, and image optimization to it.
> If the `github-actions` skill is available, delegate workflow syntax and CI pipeline patterns to it.
> If the `ci-cd-architecture` skill is available, delegate deployment strategy and environment promotion to it.

## References

- [API: authentication, endpoints, common operations, and permission scopes](references/api-patterns.md)
- [Deployment: auto-deploy, webhooks, GitHub Actions, and CI/CD pipelines](references/deployment-strategies.md)
- [Build packs: Nixpacks, Dockerfile, Compose conventions, and configuration](references/build-packs.md)
