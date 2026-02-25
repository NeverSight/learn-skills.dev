---
name: eve-local-dev-loop
description: Local Docker Compose development loop for Eve-compatible apps, with handoff to staging deploys.
---

# Eve Local Dev Loop (Docker Compose)

Use this skill to run and test the app locally with Docker Compose, then hand off to Eve for staging deploys.

## Preconditions

- A `compose.yaml` or `docker-compose.yml` exists in the repo.
- The Eve manifest (`.eve/manifest.yaml`) reflects the same services and ports.

## Local Run

```bash
# Start local services
docker compose up --build

# View logs
docker compose logs -f

# Stop and clean
docker compose down -v
```

## Keep Compose and Manifest in Sync

- Match service names and exposed ports between Compose and the Eve manifest.
- If a service is public in production, set `x-eve.ingress.public: true` in the manifest.
- Use `${secret.KEY}` in the manifest and keep local values in `.eve/dev-secrets.yaml`.

## Local Environment Variables

- Prefer `.env` for Compose and `.eve/dev-secrets.yaml` for manifest interpolation.
- Never commit secrets; keep `.eve/dev-secrets.yaml` in `.gitignore`.

## Promote to Staging

```bash
# Ensure profile and auth are set
eve profile use staging
eve auth status

# Set required secrets
eve secrets set API_KEY "value" --project proj_xxx

# Deploy to staging (requires --ref with 40-char SHA or a ref resolved against --repo-dir)
eve env deploy staging --ref main --repo-dir .

# If the environment has a pipeline configured, this triggers the pipeline.
# Use --direct to bypass pipeline and deploy directly:
eve env deploy staging --ref main --repo-dir . --direct
```

Track the deploy job:

```bash
eve job list --phase active
eve job follow <job-id>
eve job result <job-id>
```

## If Local Works but Staging Fails

- Re-check manifest parity with Compose.
- Verify secrets exist in Eve (`eve secrets list`).
- Use `eve job diagnose <job-id>` for failure details.
