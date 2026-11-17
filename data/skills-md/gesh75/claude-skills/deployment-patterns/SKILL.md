---
name: deployment-patterns
description: Deployment workflows, CI/CD pipeline patterns, Docker containerization, health checks, rollback strategies, and production readiness checklists for web applications.
origin: ECC
---

# Deployment Patterns

Production deployment workflows and CI/CD best practices.

## When to Activate

- Setting up CI/CD pipelines
- Dockerizing an application
- Planning deployment strategy (blue-green, canary, rolling)
- Implementing health checks and readiness probes
- Preparing for a production release
- Configuring environment-specific settings

## Deployment Strategies

### Rolling Deployment (Default)

Replace instances gradually — old and new versions run simultaneously during rollout.

```
Instance 1: v1 → v2  (update first)
Instance 2: v1        (still running v1)
Instance 3: v1        (still running v1)

Instance 1: v2
Instance 2: v1 → v2  (update second)
Instance 3: v1

Instance 1: v2
Instance 2: v2
Instance 3: v1 → v2  (update last)
```

**Pros:** Zero downtime, gradual rollout
**Cons:** Two versions run simultaneously — requires backward-compatible changes
**Use when:** Standard deployments, backward-compatible changes

### Blue-Green Deployment

Run two identical environments. Switch traffic atomically.

```
Blue  (v1) ← traffic
Green (v2)   idle, running new version

# After verification:
Blue  (v1)   idle (becomes standby)
Green (v2) ← traffic
```

**Pros:** Instant rollback (switch back to blue), clean cutover
**Cons:** Requires 2x infrastructure during deployment
**Use when:** Critical services, zero-tolerance for issues

### Canary Deployment

Route a small percentage of traffic to the new version first.

```
v1: 95% of traffic
v2:  5% of traffic  (canary)

# If metrics look good:
v1: 50% of traffic
v2: 50% of traffic

# Final:
v2: 100% of traffic
```

**Pros:** Catches issues with real traffic before full rollout
**Cons:** Requires traffic splitting infrastructure, monitoring
**Use when:** High-traffic services, risky changes, feature flags

## Docker

Build production images with multi-stage Dockerfiles, run as non-root, pin versions, and add a `HEALTHCHECK`. Full Node.js / Go / Python(Django) Dockerfiles and the good/bad practices list are in [reference/docker.md](reference/docker.md). For general Docker/Compose patterns (local dev, security, networking, volumes), see the **docker-patterns** skill.

## CI/CD Pipeline

### Pipeline Stages

```
PR opened:
  lint → typecheck → unit tests → integration tests → preview deploy

Merged to main:
  lint → typecheck → unit tests → integration tests → build image → deploy staging → smoke tests → deploy production
```

Full GitHub Actions workflow (test → build/push image → deploy) in [reference/cicd.md](reference/cicd.md).

## Health Checks

Expose a simple `/health` (200/`ok`) for probes and a `/health/detailed` that checks dependencies (DB, Redis, external APIs) and returns 503 when degraded. Wire Kubernetes liveness/readiness/startup probes to `/health`. Endpoint code and probe YAML in [reference/health-and-config.md](reference/health-and-config.md).

## Environment Configuration

Follow the Twelve-Factor pattern: all config via environment variables, never in code. Validate config at startup and fail fast (e.g., a Zod schema). Examples in [reference/health-and-config.md](reference/health-and-config.md).

## Rollback Strategy

Prefer instant rollback to a previous tagged image/deployment (`kubectl rollout undo`, `vercel rollback`, `railway up --commit <sha>`). Keep DB migrations backward-compatible so rollback never requires a destructive down-migration. Commands and the rollback checklist in [reference/health-and-config.md](reference/health-and-config.md).

## Production Readiness Checklist

Before any production deployment:

### Application
- [ ] All tests pass (unit, integration, E2E)
- [ ] No hardcoded secrets in code or config files
- [ ] Error handling covers all edge cases
- [ ] Logging is structured (JSON) and does not contain PII
- [ ] Health check endpoint returns meaningful status

### Infrastructure
- [ ] Docker image builds reproducibly (pinned versions)
- [ ] Environment variables documented and validated at startup
- [ ] Resource limits set (CPU, memory)
- [ ] Horizontal scaling configured (min/max instances)
- [ ] SSL/TLS enabled on all endpoints

### Monitoring
- [ ] Application metrics exported (request rate, latency, errors)
- [ ] Alerts configured for error rate > threshold
- [ ] Log aggregation set up (structured logs, searchable)
- [ ] Uptime monitoring on health endpoint

### Security
- [ ] Dependencies scanned for CVEs
- [ ] CORS configured for allowed origins only
- [ ] Rate limiting enabled on public endpoints
- [ ] Authentication and authorization verified
- [ ] Security headers set (CSP, HSTS, X-Frame-Options)

### Operations
- [ ] Rollback plan documented and tested
- [ ] Database migration tested against production-sized data
- [ ] Runbook for common failure scenarios
- [ ] On-call rotation and escalation path defined

## Reference Files

- [reference/docker.md](reference/docker.md) — read when writing a production Dockerfile; multi-stage builds for Node.js, Go, and Python/Django plus the Docker good/bad practices list.
- [reference/cicd.md](reference/cicd.md) — read when setting up a pipeline; full GitHub Actions test/build/deploy workflow and stage breakdown.
- [reference/health-and-config.md](reference/health-and-config.md) — read when implementing health endpoints, K8s probes, env validation, or rollback commands.
