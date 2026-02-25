---
name: dokploy-api-mcp
description: >-
  Deploy and manage applications on Dokploy (self-hosted PaaS).
  Use when deploying apps, managing services (PostgreSQL, Redis),
  configuring domains, running migrations, or troubleshooting
  Dokploy deployments. Covers API (tRPC), CLI, MCP server,
  and common pitfalls with Next.js, Docker, and database drivers.
argument-hint: "[action] <details>"
user-invocable: true
disable-model-invocation: false
allowed-tools: Bash(curl *) Bash(npx *) Bash(docker *) Bash(ssh *) Bash(git *) Read Write WebFetch
metadata:
  author: ai-ads-agent
  version: "1.0"
  category: deployment
---

# Dokploy Deployment

Deploy and manage applications on a self-hosted Dokploy instance.
Dokploy is an open-source PaaS (alternative to Vercel/Heroku) using Docker + Traefik.

## Quick Reference

| Item | Value |
|------|-------|
| Dashboard | `https://<DOKPLOY_HOST>/` |
| API base | `https://<DOKPLOY_HOST>/api/` |
| Swagger UI | `https://<DOKPLOY_HOST>/swagger` (browser login required) |
| Auth header | `x-api-key: <TOKEN>` |
| CLI install | `npm install -g @dokploy/cli` |
| MCP server | `@ahdev/dokploy-mcp` (67 tools) |
| Docs | https://docs.dokploy.com |

## First Run — Setup

**On first use**, check if the Dokploy MCP server is configured. If not, run the interactive setup:

```
1. Check: does ~/.claude/mcp.json contain a "dokploy" server entry?
2. If NO → run: python3 ~/.claude/skills/dokploy-api-mcp/scripts/setup.py
3. The script will:
   - Ask for Dokploy URL (e.g., https://dokploy.example.com)
   - Ask for API key (generated in Dashboard → Settings → Profile → API/CLI)
   - Validate the connection
   - Auto-configure ~/.claude/mcp.json with the MCP server
4. Tell the user: "Restart Claude Code to activate the Dokploy MCP server."
```

**With CLI arguments** (non-interactive):

```bash
python3 ~/.claude/skills/dokploy-api-mcp/scripts/setup.py --url https://dokploy.example.com --key YOUR_API_KEY
```

**After setup**, the MCP server (`@ahdev/dokploy-mcp`, 67 tools) will be available on next Claude Code restart. Prefer MCP tools over curl for all operations.

## Environment Variables

Before using this skill, ensure these are available:

```
DOKPLOY_URL=https://dokploy.example.com
DOKPLOY_API_KEY=<generated-api-token>
```

Generate API token: Dashboard → Settings → Profile → API/CLI → Generate.

## Deployment Workflow

### Step 1: Check Current State

```bash
# Get application status
curl -s -X GET "${DOKPLOY_URL}/api/trpc/application.one?input=$(python3 -c "
import urllib.parse, json
print(urllib.parse.quote(json.dumps({'json':{'applicationId':'APP_ID'}})))
")" -H "x-api-key: ${DOKPLOY_API_KEY}"
```

### Step 2: Trigger Deploy

```bash
# Deploy application (POST — mutation)
curl -s -X POST "${DOKPLOY_URL}/api/application.deploy" \
  -H "x-api-key: ${DOKPLOY_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"json":{"applicationId":"APP_ID"}}'
```

### Step 3: Monitor Deploy Status

```bash
# Poll deployment status
curl -s -X GET "${DOKPLOY_URL}/api/trpc/deployment.all?input=$(python3 -c "
import urllib.parse, json
print(urllib.parse.quote(json.dumps({'json':{'applicationId':'APP_ID'}})))
")" -H "x-api-key: ${DOKPLOY_API_KEY}"
```

### Step 4: Verify Health

```bash
curl -sk "https://<app-domain>/api/health"
```

## API Reference

Dokploy uses **tRPC** internally. Two request formats:

### Queries (read) — GET with encoded input

```
GET /api/trpc/<router>.<procedure>?input=URL_ENCODED({"json":{...}})
Header: x-api-key: <token>
```

### Mutations (write) — POST with JSON body

```
POST /api/<router>.<procedure>
Header: x-api-key: <token>
Header: Content-Type: application/json
Body: {"json":{...}}
```

### Key Endpoints

See [references/API-REFERENCE.md](references/API-REFERENCE.md) for the full list.

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `project.all` | GET | List all projects |
| `project.one` | GET | Get project by ID |
| `application.one` | GET | Get app details + status |
| `application.deploy` | POST | Trigger deployment |
| `application.stop` | POST | Stop application |
| `application.start` | POST | Start application |
| `application.update` | POST | Update app settings |
| `application.saveBuildType` | POST | Change build type |
| `application.saveEnvironment` | POST | Set environment variables |
| `deployment.all` | GET | List deployments for app |
| `domain.byApplicationId` | GET | Get domains for app |
| `domain.create` | POST | Add custom domain |
| `postgres.one` | GET | Get PostgreSQL service |
| `postgres.update` | POST | Update PostgreSQL settings |
| `redis.one` | GET | Get Redis service |
| `docker.getContainersByAppNameMatch` | GET | List Docker containers |
| `application.readTraefikConfig` | GET | Read Traefik config |

## CLI Usage

```bash
# Install
npm install -g @dokploy/cli

# Authenticate (creates ~/.config/dokploy/config.json)
dokploy authenticate

# Verify token
dokploy verify

# Application management
dokploy app create   # Create new application
dokploy app deploy   # Deploy application
dokploy app stop     # Stop application
dokploy app delete   # Delete application

# Database management
dokploy db create    # Create database service
dokploy db delete    # Delete database service

# Environment variables
dokploy env set      # Set env vars
dokploy env list     # List env vars

# Project management
dokploy project create
dokploy project list
```

## MCP Server (67 tools — preferred for AI agents)

**When MCP is available, prefer MCP tools over curl.** MCP handles tRPC URL encoding and response parsing automatically.

See [references/MCP-TOOLS.md](references/MCP-TOOLS.md) for the full 67-tool reference.

### Setup

**Automatic** (recommended): Run the setup script from the "First Run" section above — it configures MCP automatically.

**Manual** (`~/.claude/mcp.json`):

```json
{
  "mcpServers": {
    "dokploy": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@ahdev/dokploy-mcp"],
      "env": {
        "DOKPLOY_URL": "https://dokploy.example.com/api",
        "DOKPLOY_API_KEY": "<your-api-token>"
      }
    }
  }
}
```

**Note:** On macOS/Linux use `"command": "npx"` directly instead of `cmd /c`.

### Key MCP Tools by Category

**Projects:** `project-all`, `project-one`, `project-create`, `project-update`, `project-duplicate`, `project-remove`

**Applications (26 tools):**
- Status: `application-one`, `application-create`, `application-update`, `application-delete`, `application-move`
- Deploy: `application-deploy`, `application-redeploy`, `application-start`, `application-stop`, `application-cancelDeployment`, `application-reload`
- Config: `application-saveBuildType`, `application-saveEnvironment`
- Git: `application-saveGithubProvider`, `application-saveGitlabProvider`, `application-saveBitbucketProvider`, `application-saveGiteaProvider`, `application-saveGitProvider`, `application-saveDockerProvider`, `application-disconnectGitProvider`
- Monitoring: `application-readAppMonitoring`, `application-readTraefikConfig`, `application-updateTraefikConfig`

**Domains (9 tools):** `domain-byApplicationId`, `domain-create`, `domain-update`, `domain-delete`, `domain-validateDomain`, `domain-generateDomain`

**PostgreSQL (13 tools):** `postgres-create`, `postgres-one`, `postgres-update`, `postgres-remove`, `postgres-deploy`, `postgres-start`, `postgres-stop`, `postgres-rebuild`, `postgres-saveExternalPort`, `postgres-saveEnvironment`

**MySQL (13 tools):** Same pattern with `mysql-*` prefix.

### MCP Deployment Workflow

```
1. application-one                → check current status
2. application-saveEnvironment    → set/update env vars if needed
3. application-saveBuildType      → ensure Dockerfile build configured
4. application-deploy             → trigger deployment
5. application-one                → poll until applicationStatus = "done"
6. curl health endpoint           → verify app is working
```

### MCP Limitations (use curl or Dashboard)

- **Build/container logs** — WebSocket only, no MCP tool
- **Redis management** — not in MCP, use `redis.*` API via curl
- **MariaDB/MongoDB** — not in MCP, use `mariadb.*`/`mongo.*` API
- **Docker Compose** — not in MCP, use `compose.*` API
- **Backups, notifications, schedules** — not in MCP

## Common Pitfalls

See [references/PITFALLS.md](references/PITFALLS.md) for detailed solutions.

| Problem | Cause | Fix |
|---------|-------|-----|
| `COPY /app/public` fails | Git ignores empty dirs | `RUN mkdir -p public` in Dockerfile |
| DB connection error | Neon HTTP driver vs standard PG | Use `postgres` (postgres.js) package |
| Clerk `publishableKey` missing | SSG validates env at build | `export const dynamic = "force-dynamic"` + skip provider in build phase |
| Container crash with migrate.mjs | standalone output lacks modules | Run migrations via in-app API endpoint |
| Build logs unavailable via API | WebSocket only, no REST | Check Dashboard UI or poll `deployment.all` for status |
| Container logs unavailable via API | WebSocket only | Use Dashboard UI |
| External DB port unreachable | VPS firewall blocks port | Use internal Docker network names |
| SSL certificate error from curl | Self-signed or Let's Encrypt delay | Use `curl -sk` or wait for cert provisioning |
| 404 on API routes after deploy | Route not in standalone output | Verify route exists in `.next/standalone` |

## Build Types

Dokploy supports:

| Type | When to use |
|------|-------------|
| **Dockerfile** | Custom builds, multi-stage, full control |
| **Nixpacks** | Auto-detect language, zero config |
| **Buildpack** | Heroku/Paketo compatible apps |
| **Docker Image** | Pre-built images from registry |

## Services (Databases)

Create via Dashboard → Project → Add Service:

- **PostgreSQL** — internal hostname: `<appName>:5432`
- **MySQL/MariaDB** — internal hostname: `<appName>:3306`
- **MongoDB** — internal hostname: `<appName>:27017`
- **Redis** — internal hostname: `<appName>:6379`

Internal hostnames use Docker network. External ports optional (may need firewall rules).

## Domain & SSL

1. Add domain via Dashboard or API (`domain.create`)
2. Point DNS A-record to VPS IP
3. Dokploy auto-provisions Let's Encrypt certificate via Traefik
4. HTTPS works automatically after DNS propagation

## Next.js Specific Guide

See [references/NEXTJS-GUIDE.md](references/NEXTJS-GUIDE.md) for full details on deploying Next.js to Dokploy.
