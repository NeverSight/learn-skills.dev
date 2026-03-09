---
name: webhooks
displayName: Webhooks
description: "Add, debug, and manage webhook providers in the joelclaw webhook gateway. Use when: adding a new webhook integration (GitHub, Stripe, Vercel, etc.), debugging webhook signature failures, checking webhook delivery, testing webhook endpoints, registering webhooks with external services, or reviewing webhook provider implementations. Triggers on: 'add a webhook', 'new webhook provider', 'webhook not working', 'webhook signature failed', 'register webhook', 'webhook debug', 'verify webhook', 'add Vercel/GitHub/Stripe webhook', 'webhook 401', 'test webhook endpoint', or any external service webhook integration task."
version: 1.0.0
author: Joel Hooks
tags: [joelclaw, webhooks, integrations, signatures, inngest]
---

# Webhook Gateway Operations

Manage the joelclaw webhook gateway — add providers, debug delivery, register with external services.

## Architecture

```
External Service → Tailscale Funnel :443 → Worker :3111 → /webhooks/:provider
  → verifySignature() → normalizePayload() → (queue pilot or direct Inngest event) → notify function → gateway
```

- **ADR-0048**: Webhook Gateway for External Service Integration
- **Gateway skill**: Use `gateway push`/`gateway test` patterns for delivery checks

## Current Providers

| Provider | Events | Signature | Funnel URL |
|----------|--------|-----------|------------|
| todoist | comment.added, task.completed, task.created | HMAC-SHA256 (`x-todoist-hmac-sha256`) | `https://panda.tail7af24.ts.net/webhooks/todoist` |
| front | message.received, message.sent, assignee.changed | HMAC-SHA1 (`x-front-signature`) | `https://panda.tail7af24.ts.net/webhooks/front` |
| vercel | deploy.succeeded, deploy.error, deploy.created, deploy.canceled | HMAC-SHA1 (`x-vercel-signature`) | `https://panda.tail7af24.ts.net/webhooks/vercel` |
| github | workflow_run.completed, package.published | HMAC-SHA256 (`x-hub-signature-256`) | `https://panda.tail7af24.ts.net/webhooks/github` |

**Current ADR-0217 pilot note:** when `QUEUE_PILOTS=github`, the webhook gateway enqueues normalized `github/workflow_run.completed` events into the shared Redis queue instead of posting them directly to Inngest. The Restate drainer then forwards the concrete event name `github/workflow_run.completed`. `github/package.published` still goes direct.

## Adding a New Provider

See [references/new-provider-checklist.md](references/new-provider-checklist.md) for the full 8-step checklist.

**Quick summary:**
1. Create `providers/{name}.ts` implementing `WebhookProvider` interface
2. Register in `server.ts` provider map
3. Create Inngest notify function(s) in `functions/{name}-notify.ts`
4. Export from `functions/index.ts` and add to `functions/index.host.ts` (or `index.cluster.ts` when cluster-owned)
5. Store webhook secret in `agent-secrets` → add lease to `start.sh`
6. Deploy: `joelclaw inngest restart-worker --register`
7. Register webhook URL with external service
8. Verify E2E with `curl` + real webhook

## Key Files

| File | Purpose |
|------|---------|
| `packages/system-bus/src/webhooks/types.ts` | `WebhookProvider` interface, `NormalizedEvent` type |
| `packages/system-bus/src/webhooks/server.ts` | Hono router — dispatches to providers, rate limiting |
| `packages/system-bus/src/webhooks/providers/` | Provider implementations (one file per service) |
| `packages/system-bus/src/inngest/functions/*-notify.ts` | Gateway notification functions per provider |
| `packages/system-bus/src/inngest/functions/index.ts` | Function exports barrel |
| `packages/system-bus/src/inngest/functions/index.host.ts` | Host worker function registration (current active role) |
| `packages/system-bus/src/inngest/functions/index.cluster.ts` | Cluster worker function registration (future/role split) |
| `packages/system-bus/src/serve.ts` | Worker role selection + health endpoint + webhook provider list |
| `~/Code/joelhooks/joelclaw/packages/system-bus/start.sh` | Secret leasing on host worker startup |

## Debugging Webhooks

### Check if webhook is arriving

```bash
# Watch worker logs
joelclaw logs worker --follow --grep webhook

# Or directly
curl -s http://localhost:3111/ | jq .webhooks
# → { endpoint: "/webhooks/:provider", providers: ["todoist", "front", "vercel"] }
```

### Signature verification failures

```bash
# Test with manual HMAC (SHA1 example for Vercel)
SECRET="your-webhook-secret"
BODY='{"type":"test-webhook","payload":{}}'
HMAC=$(echo -n "$BODY" | openssl dgst -sha1 -hmac "$SECRET" -binary | xxd -p)
curl -X POST http://localhost:3111/webhooks/vercel \
  -H "Content-Type: application/json" \
  -H "x-vercel-signature: $HMAC" \
  -d "$BODY"
```

Common failures:
- **Wrong secret** — Todoist uses `client_secret` (not "Verification token"), Vercel uses the secret from webhook creation, Front uses the rules-based secret
- **Encoding mismatch** — Todoist = base64, Vercel = hex, Front = base64 over compact JSON
- **Body mutation** — Caddy/proxy rewrites body. Use Tailscale Funnel → worker directly
- **Rate limited** — 20 auth failures per IP per minute. Wait or restart worker

### Check Inngest received events

```bash
joelclaw runs --count 5
# Look for vercel-deploy-*, todoist-*, front-* function runs
```

### Gateway not receiving notifications

```bash
joelclaw gateway status
joelclaw gateway events   # Peek pending events
```

## Registering Webhooks with Services

### Vercel (Pro/Enterprise required)

```bash
# Via Vercel dashboard: Settings → Webhooks → Create
# Or via API:
VERCEL_TOKEN="your-api-token"
curl -X POST "https://api.vercel.com/v1/webhooks" \
  -H "Authorization: Bearer $VERCEL_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://panda.tail7af24.ts.net/webhooks/vercel",
    "events": ["deployment.created", "deployment.succeeded", "deployment.error", "deployment.canceled"]
  }'
```

The response includes a `secret` — store it: `secrets add vercel_webhook_secret --value "..."`

### GitHub

Set up via repo Settings → Webhooks:
- **URL**: `https://panda.tail7af24.ts.net/webhooks/github`
- **Content type**: `application/json`
- **Secret**: generate one, store as `github_webhook_secret`
- **Events**: push, pull_request, deployment_status, or "Send me everything"

### Todoist

Already configured via Todoist App Console → Webhooks tab.
Uses `client_secret` as HMAC key (not the "Verification token").

### Front

Already configured via Front Rules → "Trigger a webhook" action.
Rules webhooks scope to specific inboxes at the rule layer.

## Signature Algorithms by Provider

| Provider | Algorithm | Encoding | Header | Secret Source |
|----------|-----------|----------|--------|---------------|
| Todoist | HMAC-SHA256 | base64 | `x-todoist-hmac-sha256` | App Console → client_secret |
| Front | HMAC-SHA1 | base64 (over compact JSON) | `x-front-signature` | Rules webhook secret |
| Vercel | HMAC-SHA1 | hex | `x-vercel-signature` | Webhook creation response |
| GitHub | HMAC-SHA256 | hex (prefixed `sha256=`) | `x-hub-signature-256` | Webhook config secret |
| Stripe | HMAC-SHA256 | hex | `stripe-signature` (structured) | Endpoint signing secret |

## Gotchas

- **Caddy drops Funnel POST bodies** — Point Tailscale Funnel directly at worker `:3111`, not through Caddy
- **`joelclaw inngest restart-worker --register` after deploy** — ensures restart + registration in one step
- **Vercel webhooks are Pro/Enterprise only** — free plans cannot create account-level webhooks
- **Front has TWO webhook types** — App-level (SHA256, challenges) vs Rules-based (SHA1, no challenges). We use Rules-based
- **agent-secrets v0.5.0+** — raw output is default, don't pass `--raw` flag
- **Idempotency keys** on all events — safe to receive duplicates from retry-happy providers
