---
name: obul-proxy
description: 'USE THIS SKILL WHEN: the user wants to proxy a request through Obul,
  call an x402 API directly, or needs to understand the Obul proxy URL pattern. Handles
  x402 payment negotiation automatically.'
endpoints:
- path: /healthz
  method: GET
  price: $0.00
  description: Health check
- path: /*
  method: ANY
  price: Varies
  description: Proxy any upstream x402 request
metadata:
  obul-skill:
    emoji: 🔗
    requires:
      env:
      - OBUL_API_KEY
      primaryEnv: OBUL_API_KEY
registries: {}
provider: dynamic
---

# Obul Proxy

Proxy any upstream request through Obul; Obul handles x402 discovery and payment flow automatically.

## Authentication

All requests route through the Obul proxy. Include your Obul API key in every request:

```json
{
  "headers": {
    "Content-Type": "application/json",
    "x-obul-api-key": "{{OBUL_API_KEY}}"
  }
}
```

Base URL: `https://proxy.obul.ai/proxy/{scheme}/{host}`

## Common Operations

### Health Check

Verify the Obul proxy is operational.

**Pricing:** $0.00

```json
{
  "method": "GET",
  "url": "https://proxy.obul.ai/healthz",
  "headers": {
    "Content-Type": "application/json",
    "x-obul-api-key": "{{OBUL_API_KEY}}"
  }
}
```

**Response:** Returns `{"status":"ok"}` when the proxy is healthy.

### Proxy a Request

Forward any HTTP request through the Obul proxy. The proxy handles x402 payment negotiation automatically.

**Pricing:** Varies based on upstream endpoint

```json
{
  "method": "POST",
  "url": "https://proxy.obul.ai/proxy/https/x402.browserbase.com/browser/session/create",
  "headers": {
    "Content-Type": "application/json",
    "x-obul-api-key": "{{OBUL_API_KEY}}"
  },
  "body": {}
}
```

**Response:** The proxied response from the upstream x402 endpoint.

## When to Use

- **Calling x402 endpoints** — Route any x402-enabled API call through Obul without handling payments manually.
- **Unified API access** — Use a single Obul API key to access multiple x402-enabled services.
- **Automatic payment handling** — Let Obul negotiate and process payments for per-request micropayments.

## Best Practices

- **Never reveal your API key** — Keep `OBUL_API_KEY` secure and never expose it in logs or client-side code.
- **Use environment variables** — Store your API key in `OBUL_API_KEY` env var and reference `{{OBUL_API_KEY}}` in requests.
- **Check health before use** — Verify the proxy is operational with `/healthz` if you encounter issues.
- **For errors** — See @skills/obul-api-errors/SKILL.md for complete error code reference and troubleshooting
