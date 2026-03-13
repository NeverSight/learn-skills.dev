---
name: coolify
description: "Coolify — open-source self-hostable PaaS for deploying apps, databases, and services via Docker. Use when building with Coolify or asking about its deployment configuration, environment variables, reverse proxy setup, health checks, persistent storage, or Git-based CI/CD integration. Fetch live documentation for up-to-date details."
---

# Coolify

Coolify is an open-source, self-hostable platform-as-a-service for deploying applications, databases, and services via Docker on your own servers.

## Documentation

- **Docs**: https://coolify.io/docs/llms.txt

## Best Practices

- **Health checks are required for zero-downtime deploys** — Traefik will route traffic to new containers as soon as the port is open, not when the app is ready. Without an explicit health check (Dockerfile `HEALTHCHECK` or UI config), requests hit containers mid-startup or before migrations finish. Always configure a health check endpoint before relying on rolling updates.

- **Destinations are isolated Docker networks** — Services on different destinations cannot reach each other by container name. A database on `destination-a` and an app on `destination-b` require explicit DNS or IP configuration. Default assumption from Heroku/Railway (all services on the same network) does not apply here.

- **Persistent volume paths must match the container's write path exactly** — Mounting `/data` in the UI does nothing if the app writes to `/app/data`. Bind mounts require exact path matching inside the container; symbolic links and relative paths do not survive container restarts. Always verify the container's actual write path before configuring volumes.

- **Nixpacks silently fails with private registries or `.npmrc`** — Auto-detection works for standard public projects but skips `.npmrc`, private package registries, and non-standard monorepo layouts without a clear error. If a build works locally but fails in Coolify with Nixpacks, switch to a Dockerfile and pass registry credentials as build-time environment variables.

- **DNS must resolve before Let's Encrypt challenges are attempted** — Coolify will attempt ACME challenges as soon as a domain is configured. If DNS has not propagated, the challenge fails and retries for hours without a prominent alert. Verify DNS resolution externally before adding the domain in Coolify, especially for wildcard certificates requiring DNS-01 via Cloudflare or Hetzner.

- **Entrypoint shell scripts must forward SIGTERM explicitly** — Rolling updates send SIGTERM to the old container for graceful shutdown. Shell script entrypoints (e.g., `entrypoint.sh`) do not forward signals by default, causing the container to be killed after the timeout rather than gracefully shut down. Use `exec` as the last command in entrypoint scripts (e.g., `exec "$@"`) or handle signals explicitly.
