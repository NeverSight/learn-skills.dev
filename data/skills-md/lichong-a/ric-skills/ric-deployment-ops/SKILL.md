---
name: ric-deployment-ops
description: "RIC deployment and operations skill. Use for build, packaging, environment configuration, health checks, release, rollback, Docker, CI/CD, runtime config, logs, monitoring, alerts, and production-readiness tasks while reusing shared infrastructure safely."
---
# RIC Deployment And Operations

Use this skill for deployment, CI/CD, packaging, operations, and runtime readiness.

## Preflight

Inspect:

- Build scripts.
- Environment variables.
- Dockerfiles/compose/k8s/CI files.
- Health checks.
- Logging config.
- Runtime ports.
- Database/cache/message dependencies.
- Rollback path.

## Principles

- Reuse shared infrastructure.
- Do not provision duplicate services without asking.
- Keep secrets in environment or secret manager.
- Do not hardcode host credentials.
- Add health/readiness checks.
- Make rollback possible.
- Keep migrations non-destructive.

## Environment

Document:

- Required variables.
- Optional variables.
- Defaults.
- Secret source.
- Example local values without real secrets.

## Release Safety

- Build before release.
- Run tests before release.
- Check migrations.
- Check feature flags/config toggles.
- Plan rollback.
- Monitor logs and health after deployment.

## Docker/CI

- Use project conventions.
- Keep images minimal but debuggable.
- Do not bake secrets into images.
- Cache dependencies safely.
- Pin versions where reproducibility matters.

## Verification

Report:

- Build/test commands.
- Health check endpoint.
- Required environment variables.
- Rollback notes.
- Known operational risks.

