---
name: cc-gateway-ai-proxy
description: Deploy and configure CC Gateway, a reverse proxy that normalizes Claude Code device fingerprints and telemetry for privacy-preserving API proxying
triggers:
  - set up cc-gateway for claude code
  - proxy claude code through a gateway
  - normalize claude code telemetry
  - hide device fingerprint from anthropic
  - configure anthropic api reverse proxy
  - cc-gateway docker setup
  - rewrite claude code device id
  - gateway for multiple claude code machines
---

# CC Gateway — AI API Identity Gateway

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

CC Gateway is a TypeScript reverse proxy that sits between Claude Code clients and the Anthropic API. It normalizes 40+ device fingerprint dimensions (device ID, email, environment, RAM, headers, and system prompt content) to a single canonical identity, manages OAuth token refresh centrally, and prevents telemetry leakage from multi-machine setups.

## Architecture Overview

```
Client (Claude Code + env vars + Clash)
  └─► CC Gateway (rewrite + auth inject + SSE passthrough)
        └─► api.anthropic.com (single canonical identity)
              
Gateway also contacts:
  platform.claude.com (OAuth token refresh only)
```

**Three-layer defense:**
| Layer | Mechanism |
|-------|-----------|
| Env vars | Route CC traffic to gateway, disable side channels |
| Clash rules | Block any direct Anthropic connections at network level |
| Gateway | Rewrite all 40+ fingerprint dimensions in-flight |

## Installation

### Prerequisites
- Node.js 18+ or Docker
- A machine that has previously logged into Claude Code (for OAuth token extraction)

### Clone and Install

```bash
git clone https://github.com/motiful/cc-gateway.git
cd cc-gateway
npm install
```

### Generate Identity and Tokens

```bash
# Create a stable canonical identity (device_id, email, env profile)
npm run generate-identity

# Create a bearer token for a specific client machine
npm run generate-token my-laptop
npm run generate-token work-desktop
```

### Extract OAuth Token (from a logged-in machine)

```bash
# macOS — copies refresh_token from Keychain
bash scripts/extract-token.sh
```

### Configure

```bash
cp config.example.yaml config.yaml
```

Edit `config.yaml`:

```yaml
# config.yaml
identity:
  device_id: "GENERATED_DEVICE_ID"          # from generate-identity
  email: "canonical@example.com"
  platform: "darwin"
  arch: "arm64"
  node_version: "20.11.0"
  shell: "/bin/zsh"
  home: "/Users/canonical"
  working_directory: "/Users/canonical/projects"
  memory_gb: 16                              # canonical RAM value

oauth:
  refresh_token: "EXTRACTED_REFRESH_TOKEN"  # from extract-token.sh

clients:
  - name: my-laptop
    token: "GENERATED_CLIENT_TOKEN"
  - name: work-desktop
    token: "ANOTHER_CLIENT_TOKEN"

server:
  port: 8443
  tls: false                                 # true for production with certs
```

## Starting the Gateway

```bash
# Development (no TLS, hot reload)
npm run dev

# Production build
npm run build && npm start

# Docker Compose (recommended for production)
docker-compose up -d
```

### Docker Compose Example

```yaml
# docker-compose.yml
version: "3.8"
services:
  cc-gateway:
    build: .
    ports:
      - "8443:8443"
    volumes:
      - ./config.yaml:/app/config.yaml:ro
    restart: unless-stopped
    environment:
      - NODE_ENV=production
```

## Verification

```bash
# Health check
curl http://localhost:8443/_health

# Show before/after rewrite diff (requires client token)
curl -H "Authorization: Bearer YOUR_CLIENT_TOKEN" \
     http://localhost:8443/_verify
```

## Client Machine Setup

On each machine running Claude Code, set these environment variables:

```bash
# ~/.bashrc or ~/.zshrc

# Route all Claude Code API traffic through the gateway
export ANTHROPIC_BASE_URL="https://gateway.your-domain.com:8443"

# Disable side-channel telemetry (Datadog, GrowthBook, version checks)
export CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1

# Skip browser OAuth — gateway handles authentication
export CLAUDE_CODE_OAUTH_TOKEN="gateway-managed"

# Authenticate to the gateway with the per-machine token
export ANTHROPIC_CUSTOM_HEADERS="Proxy-Authorization: Bearer YOUR_CLIENT_TOKEN"
```

Or use the interactive setup script:

```bash
bash scripts/client-setup.sh
```

Then just run `claude` — no login prompt required.

## Clash Rules (Network-Level Blocking)

Add to your Clash configuration to block any direct Anthropic connections:

```yaml
# clash-rules.yaml excerpt
rules:
  - DOMAIN,gateway.your-domain.com,DIRECT      # Allow your gateway
  - DOMAIN-SUFFIX,anthropic.com,REJECT          # Block direct API calls
  - DOMAIN-SUFFIX,claude.com,REJECT             # Block direct OAuth
  - DOMAIN-SUFFIX,claude.ai,REJECT              # Block Claude web
  - DOMAIN-SUFFIX,datadoghq.com,REJECT          # Block Datadog telemetry
  - DOMAIN-SUFFIX,statsig.com,REJECT            # Block feature flags
```

See `clash-rules.yaml` in the repo for the full template.

## What Gets Rewritten

| Layer | Field | Transformation |
|-------|-------|----------------|
| Identity | `device_id` | → canonical ID from config |
| Identity | `email` | → canonical email |
| Environment | `env` object (40+ fields) | → entire object replaced |
| Process | `constrainedMemory` (physical RAM) | → canonical value |
| Process | `rss`, `heapTotal`, `heapUsed` | → randomized in realistic range |
| Headers | `User-Agent` | → canonical CC version string |
| Headers | `Authorization` | → real OAuth token (injected) |
| Headers | `x-anthropic-billing-header` | → canonical fingerprint |
| Prompt text | `Platform`, `Shell`, `OS Version` | → canonical values |
| Prompt text | `/Users/xxx/`, `/home/xxx/` | → canonical home prefix |
| Leak fields | `baseUrl` | → stripped |
| Leak fields | `gateway` provider field | → stripped |

## TypeScript Usage Examples

### Custom Rewriter Extension

```typescript
// src/rewriters/custom-field-rewriter.ts
import { RequestRewriter } from '../types';

export const customFieldRewriter: RequestRewriter = {
  name: 'custom-field-rewriter',
  
  rewriteBody(body: Record<string, unknown>, config: CanonicalConfig): Record<string, unknown> {
    // Strip any custom analytics fields your org adds
    const { __analytics, __session_debug, ...cleaned } = body as any;
    
    // Normalize any additional identity fields
    if (cleaned.metadata?.user_id) {
      cleaned.metadata.user_id = config.identity.device_id;
    }
    
    return cleaned;
  },
  
  rewriteHeaders(headers: Record<string, string>, config: CanonicalConfig): Record<string, string> {
    return {
      ...headers,
      'x-custom-client': 'canonical',
    };
  }
};
```

### Programmatic Gateway Start

```typescript
// scripts/start-with-monitoring.ts
import { createGateway } from '../src/gateway';
import { loadConfig } from '../src/config';

async function main() {
  const config = await loadConfig('./config.yaml');
  
  const gateway = await createGateway(config);
  
  gateway.on('request', ({ clientId, path }) => {
    console.log(`[${new Date().toISOString()}] ${clientId} → ${path}`);
  });
  
  gateway.on('rewrite', ({ field, before, after }) => {
    console.log(`Rewrote ${field}: ${before} → ${after}`);
  });
  
  gateway.on('tokenRefresh', ({ expiresAt }) => {
    console.log(`OAuth token refreshed, expires: ${expiresAt}`);
  });
  
  await gateway.listen(config.server.port);
  console.log(`Gateway running on port ${config.server.port}`);
}

main().catch(console.error);
```

### Token Generation (Programmatic)

```typescript
// scripts/provision-client.ts
import { generateClientToken, addClientToConfig } from '../src/auth';

async function provisionNewMachine(machineName: string) {
  const token = await generateClientToken(machineName);
  
  await addClientToConfig('./config.yaml', {
    name: machineName,
    token,
    created_at: new Date().toISOString(),
  });
  
  console.log(`Client token for ${machineName}:`);
  console.log(token);
  console.log('\nAdd to client machine:');
  console.log(`export ANTHROPIC_CUSTOM_HEADERS="Proxy-Authorization: Bearer ${token}"`);
}

provisionNewMachine(process.argv[2] ?? 'new-machine');
```

## Key npm Scripts

| Command | Purpose |
|---------|---------|
| `npm run dev` | Start with hot reload (development) |
| `npm run build` | Compile TypeScript to `dist/` |
| `npm start` | Run compiled production build |
| `npm test` | Run rewriter test suite (13 tests) |
| `npm run generate-identity` | Create canonical device profile |
| `npm run generate-token <name>` | Create per-client bearer token |

## Common Patterns

### Multiple Machines, One Identity

```bash
# On gateway server — generate once
npm run generate-identity
# → device_id: abc-123, email: canonical@proxy.local

# Provision each machine
npm run generate-token laptop-home    # → token-aaa
npm run generate-token laptop-work    # → token-bbb  
npm run generate-token desktop        # → token-ccc

# All three machines present as the same device to Anthropic
```

### Rotating the Canonical Identity

```bash
# Generate a new identity (e.g., after a suspected flag)
npm run generate-identity --force

# Update config.yaml with new device_id
# Restart gateway — all clients immediately use new identity
docker-compose restart cc-gateway
```

### Checking for New Telemetry Fields After CC Updates

```bash
# After a Claude Code update, use _verify to diff
curl -H "Authorization: Bearer $TOKEN" \
     http://localhost:8443/_verify | jq '.unrewritten_fields'

# Monitor Clash logs for new endpoints
# Any REJECT hits on new domains = new hardcoded endpoints
```

## Troubleshooting

### `claude` still prompts for browser login
- Ensure `CLAUDE_CODE_OAUTH_TOKEN=gateway-managed` is exported
- Verify `ANTHROPIC_BASE_URL` points to your running gateway
- Check gateway logs: `docker-compose logs -f cc-gateway`

### 401 Unauthorized from gateway
- Confirm `ANTHROPIC_CUSTOM_HEADERS` contains `Proxy-Authorization: Bearer <token>`
- Verify the token in config.yaml matches the one set in env var
- Run `curl -H "Authorization: Bearer $TOKEN" http://localhost:8443/_health`

### OAuth token expired
```bash
# Re-extract from a logged-in machine
bash scripts/extract-token.sh
# Paste new refresh_token into config.yaml
docker-compose restart cc-gateway
```

### MCP servers bypassing gateway
MCP uses `mcp-proxy.anthropic.com` which ignores `ANTHROPIC_BASE_URL`. Add to Clash:
```yaml
- DOMAIN,mcp-proxy.anthropic.com,REJECT
```

### Requests reaching Anthropic directly (Clash not blocking)
- Check Clash is running: `clash -v`
- Verify rules are loaded: look for REJECT entries in Clash dashboard
- Test: `curl https://api.anthropic.com` — should fail if Clash is active

### Gateway rewrite not applying to a new field
After a Claude Code update, new telemetry fields may not be covered. Check `/_verify` for `unrewritten_fields`, then open an issue or add a custom rewriter (see Custom Rewriter Extension above).

## Caveats

- **MCP servers** — hardcoded endpoint, use Clash to block if not needed
- **CC updates** — monitor Clash REJECT logs after every Claude Code update for new endpoints
- **Refresh token lifetime** — if the OAuth refresh token expires, re-run `extract-token.sh`
- **ToS** — do not use for account sharing; intended for managing your own devices under one subscription
- **Alpha** — test with a non-primary account before production use
