---
name: tilt-dev
description: Manage local development environments with Tilt. Use when working with projects that run services via Tilt (indicated by presence of Tiltfile), including checking service status, viewing logs, troubleshooting connectivity issues, or managing the Tilt stack. Essential for projects using Tiltfile with local_resource for orchestrating backend, frontend, and other services.
---

# Tilt Development Environment Management

Manage and troubleshoot local development stacks orchestrated by Tilt.

## Quick Start

Script paths shown as `scripts/...` assume your current working directory is `skills/tilt-dev/`. From repo root, use `skills/tilt-dev/scripts/...`.

### Check if Services Are Running

Always check before starting Tilt:

```bash
# Run status check script
scripts/check_tilt_status.sh [port]

# Or manually
tilt get uiresources --port <PORT>
```

### Check Service Health

```bash
# Run health check script
scripts/get_service_health.sh

# Or manually check endpoints
curl http://localhost:3000/health     # Backend
curl http://localhost:3001/           # Frontend
curl http://localhost:4111/swagger-ui # Mastra
```

### Start Tilt

Only if services are not already running:

```bash
tilt up --port <PORT>
```

Common ports: 10102, 10301, 10350

### View Logs

```bash
tilt logs --port <PORT> <resource>

# Follow logs
tilt logs --port <PORT> <resource> --follow
```

### Stop Tilt

```bash
tilt down
```

## Important Principles

### Always Check First

Services are likely already running with hot reload. Never blindly run `tilt up` without checking status first.

### Prefer Health Checks Over Restarts

Check health endpoints and logs before restarting services. Tilt hot-reloads changes automatically.

### Use the Tilt UI

Access at `http://localhost:<PORT>` for:

- Real-time resource status
- Build logs
- Service restarts
- Error messages

## Common Workflows

### Debug Service Not Responding

1. Check Tilt UI resource status
2. View resource logs: `tilt logs --port <PORT> <resource>`
3. Check health endpoint with curl
4. Review error messages in logs

### View Recent Errors

```bash
# Tail logs for specific service
tilt logs --port <PORT> <resource> | tail -50

# Follow logs in real-time
tilt logs --port <PORT> <resource> --follow
```

### Diagnose Tilt Issues

```bash
tilt doctor
```

## Reference

See [references/tilt_commands.md](references/tilt_commands.md) for:

- Complete command reference
- Tiltfile (Starlark) syntax guidelines
- Project-specific examples
- Troubleshooting guide
- Port conventions

## Scripts

- `scripts/check_tilt_status.sh [port]` - Check if Tilt is running and list resources
- `scripts/get_service_health.sh` - Check health endpoints for common services
