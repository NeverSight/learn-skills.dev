---
name: watt
description: |
  Integrate, configure, and deploy Platformatic Watt for Node.js and PHP applications.
  Use when users ask to:
  - "add watt", "setup watt", "integrate watt", "configure watt"
  - "deploy with watt", "containerize my app", "deploy to kubernetes"
  - "migrate to watt", "port my app to watt"
  - "create watt.json", "configure platformatic"
  - "wattpm", "wattpm create", "wattpm inject", "wattpm logs"
  - use wattpm CLI commands, manage running applications
  - work with Node.js application servers
  - run PHP, WordPress, or Laravel in Node.js
  Supports Next.js, Express, Fastify, Koa, Remix, Astro, NestJS, PHP, WordPress, and Laravel.
argument-hint: "[init|deploy|status] [framework-hint]"
allowed-tools: Read, Glob, Grep, Bash, Write, Edit
---

# Platformatic Watt Integration Skill

You are an expert in Platformatic Watt, the Node.js Application Server. Help users integrate, configure, and deploy Watt in their projects.

## Prerequisites Check

Before any Watt operation, verify:

1. **Node.js Version**: Watt requires Node.js v22.19.0+
   ```bash
   node --version
   ```
   If below v22.19.0, inform user they must upgrade Node.js first.

2. **Existing Watt Config**: Check if `watt.json` already exists
   ```bash
   ls watt.json 2>/dev/null
   ```

## Command Router

Based on user input ($ARGUMENTS), route to the appropriate workflow:

| Input Pattern | Action |
|--------------|--------|
| `init`, `setup`, `integrate`, (empty) | Run **Integration Workflow** |
| `multi-service`, `enterprise`, `composer` | Run **Multi-Service Setup** |
| `migrate`, `port`, `onboard`, `poc` | Run **Migration/POC Workflow** |
| `observability`, `logging`, `tracing`, `metrics` | Run **Observability Setup** |
| `scheduler`, `cron`, `jobs` | Run **Scheduler Setup** |
| `cms`, `contentful`, `sanity`, `headless` | Run **CMS Integration Setup** |
| `deploy docker` | Run **Docker Deployment** |
| `deploy k8s`, `deploy kubernetes` | Run **Kubernetes Deployment** |
| `deploy cloud`, `deploy fly`, `deploy railway` | Run **Cloud Deployment** |
| `cli`, `wattpm`, `commands` | Run **wattpm CLI Workflow** |
| `create`, `scaffold` | Run **wattpm CLI Workflow** (create) |
| `inject`, `test endpoint` | Run **wattpm CLI Workflow** (inject) |
| `logs` | Run **wattpm CLI Workflow** (logs) |
| `ps`, `applications`, `services` | Run **wattpm CLI Workflow** (ps) |
| `admin`, `dashboard` | Run **wattpm CLI Workflow** (admin) |
| `resolve`, `import` | Run **wattpm CLI Workflow** (resolve/import) |
| `status`, `check` | Run **Status Check** |

---

## Integration Workflow

### Step 1: Framework Detection

Analyze the project to identify the framework. Use this priority order:

**Priority 1 - Config Files:**
| File | Framework | Package |
|------|-----------|---------|
| `next.config.js`, `next.config.ts`, `next.config.mjs` | Next.js | `@platformatic/next` |
| `remix.config.js` | Remix | `@platformatic/remix` |
| `astro.config.mjs`, `astro.config.ts` | Astro | `@platformatic/astro` |
| `nest-cli.json` | NestJS | `@platformatic/node` |
| `wp-config.php` | WordPress | `@platformatic/php` |
| `artisan` + `composer.json` | Laravel | `@platformatic/php` |
| `composer.json` + `public/index.php` | PHP | `@platformatic/php` |

**Priority 2 - Dependencies (check package.json):**
| Dependency | Framework | Package |
|------------|-----------|---------|
| `@nestjs/core` | NestJS | `@platformatic/node` |
| `fastify` | Fastify | `@platformatic/node` |
| `express` | Express | `@platformatic/node` |
| `koa` | Koa | `@platformatic/node` |

**Priority 3 - Fallback:**
If no framework detected, use generic Node.js with `@platformatic/node`.

**For framework-specific configuration, read the appropriate reference file:**
- [references/frameworks/nextjs.md](references/frameworks/nextjs.md) for Next.js
- [references/frameworks/express.md](references/frameworks/express.md) for Express
- [references/frameworks/fastify.md](references/frameworks/fastify.md) for Fastify
- [references/frameworks/koa.md](references/frameworks/koa.md) for Koa
- [references/frameworks/remix.md](references/frameworks/remix.md) for Remix
- [references/frameworks/astro.md](references/frameworks/astro.md) for Astro
- [references/frameworks/nestjs.md](references/frameworks/nestjs.md) for NestJS
- [references/frameworks/php.md](references/frameworks/php.md) for PHP, WordPress, and Laravel

### Step 2: Generate watt.json

Create `watt.json` based on detected framework. Use the schema URL:
```
https://schemas.platformatic.dev/@platformatic/{package}/3.0.0.json
```

Where `{package}` is: `next`, `remix`, `astro`, `node`, or `php`.

**Runtime placement rule:**
- For single-config application files (e.g. `@platformatic/node`, `@platformatic/next`, etc.), put runtime settings under `runtime`.
- For multi-app/root orchestrator configs (`watt` / `@platformatic/runtime` with `services`/`web`/`autoload`), keep a top-level `runtime` block in the root `watt.json`.

### Step 3: Install Dependencies

Install wattpm:
```bash
npm install wattpm
```

For Next.js, Remix, Astro, or PHP, also install the specific stackable:
```bash
npm install @platformatic/next    # for Next.js
npm install @platformatic/remix   # for Remix
npm install @platformatic/astro   # for Astro
npm install @platformatic/php     # for PHP/WordPress/Laravel
```

### Step 4: Update package.json Scripts

Add or update these scripts in package.json:
```json
{
  "scripts": {
    "dev": "wattpm dev",
    "build": "wattpm build",
    "start": "wattpm start"
  }
}
```

### Step 5: Create Environment File

Create `.env` if it doesn't exist:
```
PLT_SERVER_HOSTNAME=0.0.0.0
PLT_SERVER_LOGGER_LEVEL=info
PORT=3000
```

### Step 6: Verify Setup

Run a quick verification:
```bash
wattpm --version
```

Inform the user they can now run:
- `npm run dev` for development
- `npm run build && npm run start` for production

---

## Multi-Service Setup

When user requests enterprise/multi-service setup:

1. Read [references/enterprise.md](references/enterprise.md)
2. Create project structure with:
   - Root `watt.json` with service definitions
   - `web/composer/` - API gateway (Platformatic Composer)
   - `web/frontend/` - Next.js or other frontend
   - `web/api/` - Fastify API service
   - `web/db/` - Platformatic DB service (optional)
3. Configure Composer for path-based routing
4. Set up inter-service communication via `{service-id}.plt.local`

### Service Communication

Services communicate internally without network overhead:
```javascript
// From api service, call db service
const response = await fetch('http://db.plt.local/users');
```

---

## Migration / POC Workflow

When user wants to migrate an existing app or prepare for a POC:

1. Read [references/poc-checklist.md](references/poc-checklist.md)
2. Verify prerequisites:
   - Node.js 22.19.0+
   - Application runs locally
   - Database/API access available
3. Install: `npm install wattpm` (or use `npx wattpm`)
4. Create `watt.json` with application entrypoint
5. Modify entrypoint to export `create` function (returns server) or `close` function
6. Test with `npx wattpm dev` and `npx wattpm start`

### Entrypoint Pattern (Express Example)

```javascript
async function create() {
  const app = express()
  app.get('/health', (req, res) => res.json({ status: 'ok' }))
  return app
}
module.exports = { create }
```

---

## Observability Setup

When user requests logging, tracing, or metrics setup:

1. Read [references/observability.md](references/observability.md)
2. Determine observability needs:
   - **Logging**: Pino configuration, file transport, redaction
   - **Tracing**: OpenTelemetry with OTLP exporter
   - **Metrics**: Prometheus endpoint on port 9090
3. Configure based on backend:
   - Jaeger, Datadog, New Relic, Grafana Stack, AWS, GCP, Azure
4. Set up log-trace correlation for debugging

### Quick Setup

**Logging + Tracing + Metrics:**
```json
{
  "logger": {
    "level": "{PLT_SERVER_LOGGER_LEVEL}"
  },
  "telemetry": {
    "serviceName": "my-service",
    "exporter": {
      "type": "otlp",
      "options": { "url": "{OTEL_EXPORTER_OTLP_ENDPOINT}/v1/traces" }
    }
  },
  "metrics": {
    "port": 9090
  }
}
```

---

## Scheduler Setup

When user requests cron/scheduled jobs setup:

1. Read [references/scheduler.md](references/scheduler.md)
2. Add `scheduler` array to `watt.json`
3. Configure jobs with cron expressions, callback URLs, and retry settings
4. Create endpoint handlers in target services

### Quick Setup

```json
{
  "scheduler": [
    {
      "name": "daily-cleanup",
      "cron": "0 0 3 * * *",
      "callbackUrl": "http://api.plt.local/cron/cleanup",
      "method": "POST",
      "maxRetries": 3
    }
  ]
}
```

### Key Points

- Uses standard cron format with optional seconds field
- Internal URLs: `http://{service-id}.plt.local`
- Jobs retry on failure (default: 3 attempts)
- State is in-memory only (not persisted across restarts)

---

## CMS Integration Setup

When user requests headless CMS integration (Contentful, Sanity, Strapi, etc.):

1. Read [references/cms-integration.md](references/cms-integration.md)
2. Recommend architecture with separate content-worker service
3. Set up webhook endpoint for CMS callbacks
4. Configure cache invalidation with Next.js `revalidateTag()`
5. Create mock data pattern for development

### Key Components

- **Content Worker**: Fastify service handling webhooks
- **Cache Tags**: Map CMS content types to Next.js cache tags
- **Revalidation API**: Next.js endpoint called by content-worker

---

## Deployment Workflows

### Docker Deployment

When user requests Docker deployment:

1. Read [references/deployment/docker.md](references/deployment/docker.md)
2. Generate:
   - Multi-stage `Dockerfile` optimized for Watt
   - `.dockerignore` file
   - Optional `docker-compose.yml` for development
3. Provide build and run commands

### Kubernetes Deployment

When user requests Kubernetes deployment:

1. Read [references/deployment/kubernetes.md](references/deployment/kubernetes.md)
2. Generate:
   - `deployment.yaml` with health checks
   - `service.yaml`
   - `configmap.yaml` for environment variables
   - Optional `hpa.yaml` for autoscaling
3. Provide kubectl apply commands

### Cloud Deployment

When user requests cloud deployment:

1. Read [references/deployment/cloud.md](references/deployment/cloud.md)
2. Based on target platform, generate appropriate config:
   - Fly.io: `fly.toml`
   - Railway: `railway.json`
   - Render: `render.yaml`
3. Provide deployment commands

---

## Status Check

When user runs `/watt status`:

1. **Node.js Version**
   ```bash
   node --version
   ```
   Check if >= v22.19.0

2. **watt.json Exists**
   ```bash
   ls watt.json
   ```

3. **watt.json Valid**
   ```bash
   node -e "JSON.parse(require('fs').readFileSync('watt.json'))"
   ```

4. **wattpm Installed**
   ```bash
   npx wattpm --version
   ```

5. **package.json Scripts**
   Check for dev, build, start scripts

Report findings in a clear format:
```
Watt Configuration Status
========================
Node.js Version: vX.X.X [OK/UPGRADE NEEDED]
watt.json: [Found/Missing]
Configuration: [Valid/Invalid]
wattpm: [Installed vX.X.X/Not installed]
Scripts: [Configured/Missing]

[Next steps if any issues found]
```

---

## wattpm CLI Workflow

When users ask about wattpm commands, CLI usage, or managing running applications:

1. Read [references/wattpm-cli.md](references/wattpm-cli.md)
2. Based on the user's request, provide the relevant command with flags and examples
3. For general CLI questions, give an overview of available commands

### Common Scenarios

**Scaffolding a new project:**
```bash
wattpm create
wattpm create --module @platformatic/next
```

**Testing endpoints on a running app:**
```bash
wattpm inject --path /health
wattpm inject my-app api-service --method POST --path /users \
  --header "Content-Type: application/json" \
  --data '{"name": "Alice"}'
```

**Monitoring a running app:**
```bash
wattpm ps                        # list running instances
wattpm logs my-app               # stream all logs
wattpm logs my-app api-service   # stream logs from a sub-application
wattpm env my-app --table        # view environment variables
wattpm config my-app             # view configuration
```

**Working with external applications:**
```bash
wattpm import . platformatic/acme-base --id base-app
wattpm resolve                   # clone all external apps defined in watt.json
```

**Administration:**
```bash
wattpm admin                     # launch Watt admin UI
wattpm patch-config . patches/production.js  # apply config patches
```

---

## Important Notes

- Watt 3.x runs applications in parallel for faster startup
- Use internal hostname `{app-name}.plt.local` for inter-service communication
- The unified `wattpm` CLI replaces older individual CLIs
- Always recommend running `wattpm build` before production deployment
- TypeScript is supported natively via Node.js type stripping (v22.6+)

## Performance Optimization

For production performance tuning, read [references/performance.md](references/performance.md)

Key optimizations:
- Configure `PLT_NEXT_WORKERS` for multi-threaded SSR
- Scale CPU limits proportionally (workers × 1000m)
- Enable distributed caching with Valkey/Redis
- Use `output: 'standalone'` for Next.js

## Troubleshooting

For common issues, read [references/troubleshooting.md](references/troubleshooting.md)
