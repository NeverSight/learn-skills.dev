---
name: cloudflare-workers
description: |
  Deploy serverless applications on Cloudflare Workers. Covers project setup, JavaScript handler patterns, routing, deployment with Wrangler, and API token configuration. Suitable for APIs, proxies, edge computing, and request transformation.
license: MIT
metadata:
  author: Stakpak <team@stakpak.dev>
  version: 1.0.18
---

# Deploying Cloudflare Workers

## Quick Start

### Create and Deploy

```bash
# Create project
npm create cloudflare@latest my-worker -- --type=hello-world --ts=false --git=false --deploy=false
cd my-worker

# Deploy
export CLOUDFLARE_API_TOKEN="your-token-here"
export CLOUDFLARE_ACCOUNT_ID="your-account-id"
npx wrangler deploy
```

## Prerequisites

* Node.js 16.17.0 or later installed
* Cloudflare account (free tier works)
* Cloudflare API token with Workers permissions

## Setup

### 1. Create API Token

Before deployment, create a Cloudflare API token with proper permissions:

1. Go to https://dash.cloudflare.com/profile/api-tokens
2. Click **"Create Token"**
3. Select **"Edit Cloudflare Workers"** template
4. Click **"Continue to summary"** → **"Create Token"**
5. Save the token securely

**Required permissions:**
* Account: Workers Scripts (Edit)
* Account: Account Settings (Read)
* User: User Details (Read)

### 2. Register workers.dev Subdomain

If this is your first Worker deployment:

1. Go to Cloudflare Dashboard → Workers & Pages
2. Look for "Your subdomain" section
3. Click "Change" or "Set up"
4. Enter a unique subdomain name (e.g., `mycompany`)
5. Save

Your workers will be available at: `<worker-name>.<subdomain>.workers.dev`

### 3. Create Worker Project

Use C3 (create-cloudflare-cli) to scaffold the project:

```bash
npm create cloudflare@latest my-worker -- --type=hello-world --ts=false --git=false --deploy=false
cd my-worker
```

**Generated structure:**
```
my-worker/
├── src/
│   └── index.js      # Worker entry point
├── wrangler.jsonc    # Wrangler configuration
├── package.json
└── node_modules/
```

### 4. Configure Wrangler

Update `wrangler.jsonc` with your worker settings:

```jsonc
{
  "$schema": "./node_modules/wrangler/config-schema.json",
  "name": "my-worker",
  "main": "src/index.js",
  "compatibility_date": "2024-12-01",
  "observability": {
    "enabled": true
  }
}
```

**Key settings:**
* `name`: Worker name (becomes part of URL)
* `main`: Entry point file
* `compatibility_date`: Runtime compatibility version
* `observability`: Enable logging and metrics

### 5. Implement the Worker Handler

Workers use a fetch handler pattern. Create your worker logic in `src/index.js`:

```javascript
/**
 * Worker Handler Template
 * Handles routing, JSON responses, and CORS
 */

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;

    // CORS headers for all responses
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };

    // Handle OPTIONS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    // Route handling
    switch (path) {
      case '/health':
        return jsonResponse({
          status: 'healthy',
          service: 'my-worker',
          timestamp: new Date().toISOString()
        }, 200, corsHeaders);
      
      case '/api/endpoint':
        return handleApiEndpoint(request, url, corsHeaders);
      
      default:
        return jsonResponse({
          error: 'Not found',
          available_endpoints: ['GET /health', 'GET /api/endpoint']
        }, 404, corsHeaders);
    }
  },
};

function handleApiEndpoint(request, url, corsHeaders) {
  // Parse query parameters
  const params = url.searchParams;
  const param1 = params.get('param1');
  
  // Validate
  if (!param1) {
    return jsonResponse({
      error: 'Missing required parameter: param1'
    }, 400, corsHeaders);
  }
  
  // Process and return
  return jsonResponse({
    result: `Processed: ${param1}`
  }, 200, corsHeaders);
}

function jsonResponse(data, status = 200, additionalHeaders = {}) {
  return new Response(JSON.stringify(data, null, 2), {
    status: status,
    headers: {
      'Content-Type': 'application/json',
      ...additionalHeaders
    }
  });
}
```

**Handler parameters:**
* `request`: Incoming HTTP Request object
* `env`: Environment bindings (KV, D1, secrets, etc.)
* `ctx`: Execution context (waitUntil, passThroughOnException)

### 6. Test Locally

Run the development server:

```bash
npx wrangler dev
```

Test the worker at `http://localhost:8787`:
```bash
curl http://localhost:8787/health
curl "http://localhost:8787/api/endpoint?param1=test"
```

### 7. Deploy to Production

Deploy using environment variables for authentication:

```bash
export CLOUDFLARE_API_TOKEN="your-token-here"
export CLOUDFLARE_ACCOUNT_ID="your-account-id"
npx wrangler deploy
```

**Finding your Account ID:**
* Dashboard → Workers & Pages → Account ID in sidebar
* Or from the URL: `dash.cloudflare.com/<account-id>/workers`

### 8. Verify Deployment

Test the live worker:

```bash
# Health check
curl https://my-worker.mysubdomain.workers.dev/health

# API endpoint
curl "https://my-worker.mysubdomain.workers.dev/api/endpoint?param1=test"
```

## Common Patterns

### Request Method Handling

```javascript
switch (request.method) {
  case 'GET':
    return handleGet(url);
  case 'POST':
    const body = await request.json();
    return handlePost(body);
  case 'PUT':
    return handlePut(request);
  case 'DELETE':
    return handleDelete(url);
  default:
    return jsonResponse({ error: 'Method not allowed' }, 405);
}
```

### Path Parameter Extraction

```javascript
// For paths like /users/123
const match = path.match(/^\/users\/(\d+)$/);
if (match) {
  const userId = match[1];
  return handleUser(userId);
}
```

### Environment Variables and Secrets

Add to `wrangler.jsonc`:
```jsonc
{
  "vars": {
    "API_VERSION": "v1"
  }
}
```

Add secrets via CLI:
```bash
npx wrangler secret put API_KEY
```

Access in handler:
```javascript
async fetch(request, env, ctx) {
  const version = env.API_VERSION;
  const apiKey = env.API_KEY;
}
```

### KV Storage Binding

Add to `wrangler.jsonc`:
```jsonc
{
  "kv_namespaces": [
    { "binding": "CACHE", "id": "your-kv-namespace-id" }
  ]
}
```

Use in handler:
```javascript
// Read
const value = await env.CACHE.get('key');

// Write
await env.CACHE.put('key', 'value', { expirationTtl: 3600 });
```

## Deployment Options

| Method | Use Case |
|--------|----------|
| `workers.dev` subdomain | Quick testing, hobby projects |
| Custom Domain | Production deployments |
| Routes | Add Workers to existing domains |

### Custom Domain Setup

Add to `wrangler.jsonc`:
```jsonc
{
  "routes": [
    { "pattern": "api.example.com/*", "custom_domain": true }
  ]
}
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Authentication error | Verify API token has correct permissions, check CLOUDFLARE_ACCOUNT_ID is set correctly, ensure token hasn't expired |
| workers.dev subdomain not registered | Go to Dashboard → Workers & Pages → Set up subdomain (must be done before first deployment) |
| SSL handshake failures | New deployments may take 1-2 minutes for SSL provisioning, try accessing via browser first, check with `curl --insecure` to bypass local SSL issues |
| Worker not updating | Clear browser cache, check deployment version ID in output, use `wrangler tail` to see live logs |

## References

* [Cloudflare Workers Documentation](https://developers.cloudflare.com/workers/)
* [Wrangler Configuration](https://developers.cloudflare.com/workers/wrangler/configuration/)
* [Workers Runtime APIs](https://developers.cloudflare.com/workers/runtime-apis/)
* [Fetch Handler Reference](https://developers.cloudflare.com/workers/runtime-apis/handlers/fetch/)
* [API Token Creation](https://developers.cloudflare.com/fundamentals/api/get-started/create-token/)