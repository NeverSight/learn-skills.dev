---
name: wrangler-coder
description: This skill guides Cloudflare Workers and Pages development with Wrangler CLI. Use when creating Workers, configuring D1 databases, R2 storage, KV namespaces, Queues, or deploying to Cloudflare Pages.
allowed-tools: Read Write Edit Grep Glob Bash
---

# Wrangler Coder

Wrangler is Cloudflare's official CLI for Workers, Pages, D1, R2, KV, Queues, and AI.

## Installation

```bash
# npm
npm install -g wrangler

# pnpm
pnpm add -g wrangler

# Verify installation
wrangler --version
```

## Authentication

```bash
# Interactive login (opens browser)
wrangler login

# Check authentication status
wrangler whoami

# Logout
wrangler logout
```

**Environment Variables:**

```bash
# API Token (preferred for CI/CD)
export CLOUDFLARE_API_TOKEN="your-api-token"

# Or with 1Password
CLOUDFLARE_API_TOKEN=op://Infrastructure/Cloudflare/wrangler_token

# Account ID (optional, can be in wrangler.toml)
export CLOUDFLARE_ACCOUNT_ID="your-account-id"
```

## Project Initialization

```bash
# Create new Worker project
wrangler init my-worker

# Create from template
wrangler init my-worker --template cloudflare/worker-template

# Initialize in existing directory
wrangler init
```

## wrangler.toml Configuration

### Basic Worker

```toml
name = "my-worker"
main = "src/index.ts"
compatibility_date = "2024-12-01"

# Account ID (can also use CLOUDFLARE_ACCOUNT_ID env var)
account_id = "your-account-id"

# Worker settings
workers_dev = true  # Enable *.workers.dev subdomain
```

### Worker with Routes

```toml
name = "api-worker"
main = "src/index.ts"
compatibility_date = "2024-12-01"
account_id = "your-account-id"

# Custom domain routes
routes = [
  { pattern = "api.example.com/*", zone_name = "example.com" },
  { pattern = "example.com/api/*", zone_name = "example.com" }
]
```

### Multi-Environment Configuration

```toml
name = "my-worker"
main = "src/index.ts"
compatibility_date = "2024-12-01"
account_id = "your-account-id"

# Development (default)
workers_dev = true

# Staging environment
[env.staging]
name = "my-worker-staging"
routes = [
  { pattern = "staging-api.example.com/*", zone_name = "example.com" }
]
vars = { ENVIRONMENT = "staging" }

# Production environment
[env.production]
name = "my-worker-production"
routes = [
  { pattern = "api.example.com/*", zone_name = "example.com" }
]
vars = { ENVIRONMENT = "production" }
```

## Cloudflare Products

| Product | Resource |
|---------|----------|
| KV Namespaces | [references/kv-namespaces.md](references/kv-namespaces.md) |
| D1 Database & R2 Storage | [references/d1-r2.md](references/d1-r2.md) |
| Queues & Durable Objects | [references/queues-durable-objects.md](references/queues-durable-objects.md) |
| Workers AI | [references/workers-ai.md](references/workers-ai.md) |
| Cloudflare Pages | [references/pages.md](references/pages.md) |

## Secrets Management

```bash
# Add secret
wrangler secret put API_KEY
# (prompts for value)

# Add secret for specific environment
wrangler secret put API_KEY --env production

# List secrets
wrangler secret list

# Delete secret
wrangler secret delete API_KEY

# Bulk secrets from .dev.vars file (local dev only)
# Create .dev.vars file:
# API_KEY=xxx
# DB_PASSWORD=yyy
```

```typescript
export interface Env {
  API_KEY: string;
  DB_PASSWORD: string;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    // Access secrets from env
    const apiKey = env.API_KEY;
    return new Response(`Key length: ${apiKey.length}`);
  }
};
```

## Development Workflow

### Local Development

```bash
# Start local dev server
wrangler dev

# With specific environment
wrangler dev --env staging

# Custom port
wrangler dev --port 8787

# Remote mode (uses Cloudflare's network)
wrangler dev --remote

# Local mode with persistent storage
wrangler dev --persist-to ./data
```

### Testing

```bash
# Run tests with vitest (recommended)
npm install -D vitest @cloudflare/vitest-pool-workers

# vitest.config.ts
# import { defineWorkersConfig } from '@cloudflare/vitest-pool-workers/config';
# export default defineWorkersConfig({
#   test: { poolOptions: { workers: { wrangler: { configPath: './wrangler.toml' } } } }
# });
```

### Deployment

```bash
# Deploy to workers.dev
wrangler deploy

# Deploy to specific environment
wrangler deploy --env production

# Dry run (show what would be deployed)
wrangler deploy --dry-run

# Deploy with custom name
wrangler deploy --name my-custom-worker
```

### Logs and Debugging

```bash
# Tail logs (real-time)
wrangler tail

# Tail specific environment
wrangler tail --env production

# Filter logs
wrangler tail --status error
wrangler tail --search "user-id-123"
wrangler tail --ip 1.2.3.4

# View deployment versions
wrangler versions list

# Rollback to previous version
wrangler rollback
```

## Complete Worker Example

See [references/worker-example.md](references/worker-example.md) for a production-ready Worker with D1, KV, R2 bindings, multi-environment config, and CORS handling.

## Best Practices

- **Pin compatibility_date** - Ensures reproducible behavior across deployments
- **Use environments** - Separate staging/production configs in same file
- **Secrets via CLI** - Never commit secrets, use `wrangler secret put`
- **Local persistence** - Use `--persist-to` for consistent local dev state
- **Tail logs in production** - Debug issues with `wrangler tail --status error`
- **Version control wrangler.toml** - Track configuration changes
- **Use .dev.vars for local secrets** - Add to .gitignore
- **Batch D1 operations** - Reduce latency with `env.DB.batch()`
- **Cache strategically** - Use KV for frequently accessed data
- **Handle errors gracefully** - Return proper HTTP status codes
