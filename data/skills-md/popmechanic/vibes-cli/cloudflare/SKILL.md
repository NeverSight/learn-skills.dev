---
name: cloudflare
description: Self-contained deploy automation — invoke directly, do not decompose. Deploys a Vibes app to Cloudflare Workers with subdomain registry. Uses KV for storage and native Web Crypto for JWT verification.
license: MIT
allowed-tools: Bash, Read, Glob, AskUserQuestion, Write
metadata:
  author: "Marcus Estes"
  version: "0.1.63"
---

> **Plan mode**: If you are planning work, this entire skill is ONE plan step: "Invoke /vibes:cloudflare". Do not decompose the steps below into separate plan tasks.

## Deploy to Cloudflare

Deploy your Vibes app to Cloudflare Workers with the subdomain registry.

### Prerequisites

1. **Cloudflare account** with Workers enabled
2. **Wrangler CLI** installed (`npm install -g wrangler`)
3. **KV namespace** created for registry storage

### Quick Deploy

```bash
cd skills/cloudflare/worker
npm install
wrangler deploy
```

### Environment Setup

Before deploying, set the required secrets:

```bash
cd skills/cloudflare/worker
npx wrangler secret put CLERK_PEM_PUBLIC_KEY
npx wrangler secret put CLERK_WEBHOOK_SECRET
```

### Deploy Script

For deploying with static assets (index.html, bundles, assets):

```bash
node scripts/deploy-cloudflare.js --name myapp --file index.html --clerk-key "pk_test_xxx"
```

The `--clerk-key` flag auto-fetches the PEM public key from Clerk's JWKS endpoint and sets it as `CLERK_PEM_PUBLIC_KEY`. Without it, the Worker can't verify JWTs for authenticated endpoints like `/claim`.

This automatically:
- Copies index.html to worker's public/
- Copies bundles/*.js (fireproof-vibes-bridge.js + fireproof-clerk-bundle.js)
- Copies assets/ directory (images, icons)
- Runs wrangler deploy

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/registry.json` | GET | Public registry read |
| `/check/:subdomain` | GET | Check subdomain availability |
| `/claim` | POST | Claim a subdomain (auth required) |
| `/webhook` | POST | Clerk subscription webhooks |
| `/api/ai/chat` | POST | AI proxy to OpenRouter (requires OPENROUTER_API_KEY) |

### KV Storage

The registry is stored in Cloudflare KV under the key `registry`. Schema:

```json
{
  "claims": { "subdomain": { "userId": "...", "claimedAt": "..." } },
  "reserved": ["admin", "api", "www"],
  "preallocated": {}
}
```

### Important: Custom Domain Required for Subdomains

Workers.dev domains only support one subdomain level for SSL. For multi-tenant
apps with subdomains (tenant.myapp.workers.dev), you MUST use a custom domain.

**Won't work:** `tenant.myapp.username.workers.dev` (SSL error)
**Will work:** `tenant.myapp.com` (with custom domain)

On workers.dev, use the `?subdomain=` query parameter for testing:
- `myapp.username.workers.dev` → landing page
- `myapp.username.workers.dev?subdomain=tenant` → tenant app
- `myapp.username.workers.dev?subdomain=admin` → admin dashboard

### Custom Domain Setup

1. **Add domain to Cloudflare** (get nameservers from Cloudflare DNS dashboard)
2. **Point registrar nameservers** to Cloudflare's assigned nameservers
3. **Delete conflicting DNS records** for the apex domain (A, AAAA, CNAME)
4. **Add Custom Domain** in Workers & Pages → your worker → Settings → Domains & Routes → Add → Custom Domain (apex: yourdomain.com)
5. **Add wildcard CNAME** in DNS: Name: `*`, Target: `<worker-name>.<username>.workers.dev` (Proxied: ON)
6. **Add Route** in Workers & Pages → your worker → Settings → Domains & Routes → Add → Route: `*.yourdomain.com/*`

After setup:
- `yourdomain.com` → landing page
- `tenant.yourdomain.com` → tenant app
- `admin.yourdomain.com` → admin dashboard

### Required Secrets

| Secret | Source | Purpose |
|--------|--------|---------|
| `CLERK_PEM_PUBLIC_KEY` | Clerk JWKS endpoint | JWT signature verification |
| `PERMITTED_ORIGINS` | Your domains | JWT azp claim validation |
| `CLERK_WEBHOOK_SECRET` | Clerk dashboard | Webhook signature verification |
| `OPENROUTER_API_KEY` | OpenRouter dashboard | AI proxy for `useAI()` hook (optional) |

**Setting secrets:**
```bash
cd skills/cloudflare/worker
npx wrangler secret put CLERK_PEM_PUBLIC_KEY
# Paste the PEM key (-----BEGIN PUBLIC KEY----- ... -----END PUBLIC KEY-----)

npx wrangler secret put CLERK_WEBHOOK_SECRET
# Paste the webhook signing secret from Clerk dashboard

npx wrangler secret put PERMITTED_ORIGINS
# Enter: https://yourdomain.com,https://*.yourdomain.com
```

**Getting CLERK_PEM_PUBLIC_KEY:**

1. Find your Clerk Frontend API URL in Clerk dashboard (e.g., `clerk.yourdomain.com`)
2. Fetch JWKS: `curl https://clerk.yourdomain.com/.well-known/jwks.json`
3. Convert JWK to PEM using Node.js:
```javascript
const crypto = require('crypto');
const jwk = { /* paste the key from jwks.json */ };
const pem = crypto.createPublicKey({ key: jwk, format: 'jwk' }).export({ type: 'spki', format: 'pem' });
console.log(pem);
```

### Deploy with --name Flag

Always use the `--name` flag to deploy to your app's worker:

```bash
node scripts/deploy-cloudflare.js --name myapp --file index.html
```

**Important:** The `--name` determines the worker URL. Without it, wrangler uses
the name from wrangler.toml (`vibes-registry`), not your app.

### AI Features

Apps using the `useAI()` hook call `/api/ai/chat` on the same origin. The worker proxies these requests to OpenRouter.

**Deploy with AI enabled:**

```bash
node scripts/deploy-cloudflare.js --name myapp --file index.html --clerk-key "pk_test_xxx" --ai-key "sk-or-v1-your-key"
```

The `--ai-key` flag sets the `OPENROUTER_API_KEY` secret on the worker after deployment. Without it, `/api/ai/chat` returns `{"error": "AI not configured"}`.

**Manual setup:**

```bash
npx wrangler secret put OPENROUTER_API_KEY --name myapp
# Paste your OpenRouter API key
```
