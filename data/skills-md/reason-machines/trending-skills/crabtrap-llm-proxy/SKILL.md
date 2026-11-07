---
name: crabtrap-llm-proxy
description: LLM-as-a-judge HTTP/HTTPS proxy that secures AI agents by intercepting and evaluating outbound requests against security policies before they reach external APIs.
triggers:
  - set up CrabTrap proxy for my AI agent
  - intercept outbound HTTP requests from agents
  - add security policies for agent API calls
  - block unauthorized requests from LLM agents
  - configure CrabTrap to guard agent traffic
  - use LLM judge to evaluate proxy requests
  - audit log agent HTTP requests with CrabTrap
  - protect against SSRF and prompt injection in agents
---

# CrabTrap LLM Proxy

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

CrabTrap is a transparent HTTP/HTTPS forward proxy that sits between AI agents and external APIs. Every outbound request is intercepted, checked against deterministic static rules, then evaluated by an LLM judge against a natural-language security policy. Blocked requests return a 403 with a reason; all decisions are logged to PostgreSQL.

## Architecture Overview

```
Agent → CrabTrap Proxy (:8080) → [Static Rules] → [LLM Judge] → External API
                ↓
         Admin UI (:8081)
                ↓
           PostgreSQL
```

**Key concepts:**
- **Static rules** — deterministic prefix/exact/glob URL matching, checked first (no LLM call)
- **LLM judge** — natural-language policy evaluated only when no static rule matches
- **Audit log** — every request, decision, and response stored in PostgreSQL
- **SSRF protection** — blocks RFC 1918, loopback, link-local, and other private ranges

## Installation

### Docker Compose (Recommended)

```yaml
# docker-compose.yml
services:
  crabtrap:
    image: quay.io/brexhq/crabtrap:latest
    ports:
      - "8080:8080"   # proxy
      - "8081:8081"   # admin UI
    environment:
      - DATABASE_URL=postgres://crabtrap:password@postgres:5432/crabtrap
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./config/gateway.yaml:/app/config/gateway.yaml
    depends_on:
      - postgres

  postgres:
    image: postgres:16
    environment:
      POSTGRES_USER: crabtrap
      POSTGRES_PASSWORD: password
      POSTGRES_DB: crabtrap
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

```bash
docker compose up -d

# Copy the generated CA certificate (needed for HTTPS interception)
docker compose cp crabtrap:/app/certs/ca.crt ./ca.crt
```

### Initial Setup

```bash
# Create an admin user and capture the token
admin_token=$(docker compose exec -it crabtrap ./gateway create-admin-user my-admin \
    | tail -n1 | cut -d" " -f2)

# Create an agent user (returns a gateway_auth_token)
token=$(curl -X POST http://localhost:8081/admin/users \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${admin_token}" \
    -d '{"id": "my-agent@example.com", "is_admin": false}' \
    | jq -r '.channels[] | select(.channel_type == "gateway_auth") | .gateway_auth_token')

echo "Agent proxy token: $token"

# Test the proxy
curl -x "http://${token}:@localhost:8080" \
    --cacert ca.crt \
    https://httpbin.org/get
```

## Configuration

### Full Configuration Reference

```yaml
# config/gateway.yaml
proxy:
  port: 8080
  read_timeout: 30s
  write_timeout: 30s
  idle_timeout: 120s
  rate_limit:
    requests_per_second: 50
    burst: 100
  # CIDR ranges allowed even though they're private (e.g. internal APIs)
  ssrf_allowlist:
    - "10.0.0.0/8"   # only if you explicitly need internal access

tls:
  ca_cert_path: /app/certs/ca.crt
  ca_key_path: /app/certs/ca.key
  cert_cache_size: 10000  # per-host cert cache

approval:
  mode: llm           # "llm" or "passthrough"
  timeout: 30s

llm_judge:
  provider: openai
  model: gpt-4o
  fallback_mode: deny   # "deny" or "passthrough" when LLM unavailable
  circuit_breaker:
    failure_threshold: 5
    reset_timeout: 10s

database:
  url: ${DATABASE_URL}  # supports env var expansion

audit:
  output: stderr    # "stderr", "stdout", or a file path like "/var/log/crabtrap.json"

log_level: info     # debug | info | warn | error
```

### Environment Variables

```bash
DATABASE_URL=postgres://user:password@host:5432/dbname
OPENAI_API_KEY=sk-...          # if using OpenAI as LLM judge
ANTHROPIC_API_KEY=sk-ant-...   # if using Anthropic
```

## CLI Commands

```bash
# Start the proxy
./gateway serve --config /app/config/gateway.yaml

# Create an admin user (outputs web token on last line)
./gateway create-admin-user <username>

# Run database migrations
./gateway migrate

# Replay audit log entries against a policy (eval mode)
./gateway eval --policy-id <id> --limit 100
```

## Admin API

All admin endpoints require `Authorization: Bearer <admin_token>`.

### User Management

```bash
# List all users
curl http://localhost:8081/admin/users \
    -H "Authorization: Bearer ${admin_token}"

# Create a user
curl -X POST http://localhost:8081/admin/users \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${admin_token}" \
    -d '{
      "id": "agent-prod@example.com",
      "is_admin": false
    }'

# Delete a user
curl -X DELETE http://localhost:8081/admin/users/agent-prod@example.com \
    -H "Authorization: Bearer ${admin_token}"
```

### Static Rules

```bash
# List static rules for a user
curl "http://localhost:8081/admin/users/agent-prod@example.com/rules" \
    -H "Authorization: Bearer ${admin_token}"

# Create an allow rule (prefix match)
curl -X POST "http://localhost:8081/admin/users/agent-prod@example.com/rules" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${admin_token}" \
    -d '{
      "pattern": "https://api.github.com/repos/myorg/",
      "pattern_type": "prefix",
      "action": "allow",
      "methods": ["GET"],
      "description": "Allow reading our org repos"
    }'

# Create a deny rule (glob match)
curl -X POST "http://localhost:8081/admin/users/agent-prod@example.com/rules" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${admin_token}" \
    -d '{
      "pattern": "https://api.github.com/repos/*/delete",
      "pattern_type": "glob",
      "action": "deny",
      "description": "Never allow repo deletion"
    }'

# Create an exact match rule
curl -X POST "http://localhost:8081/admin/users/agent-prod@example.com/rules" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${admin_token}" \
    -d '{
      "pattern": "https://slack.com/api/chat.postMessage",
      "pattern_type": "exact",
      "action": "allow",
      "methods": ["POST"],
      "description": "Allow posting Slack messages"
    }'
```

**Pattern types:**
- `prefix` — URL must start with the pattern
- `exact` — URL must match exactly
- `glob` — wildcard matching with `*`

**Rule priority:** `deny` rules always take priority over `allow` rules.

### LLM Policies

```bash
# Get current policy for a user
curl "http://localhost:8081/admin/users/agent-prod@example.com/policy" \
    -H "Authorization: Bearer ${admin_token}"

# Set/update a policy
curl -X PUT "http://localhost:8081/admin/users/agent-prod@example.com/policy" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${admin_token}" \
    -d '{
      "policy": "This agent assists with GitHub repository management for the myorg organization.\n\nALLOWED:\n- Read operations (GET) on any github.com endpoint\n- Creating issues and pull request comments in myorg repositories\n- Posting messages to the #eng-alerts Slack channel only\n\nDENIED:\n- Any write operations outside the myorg GitHub organization\n- Deleting any resources\n- Accessing credentials, secrets, or environment variables\n- Any requests to non-whitelisted domains"
    }'

# List policy versions
curl "http://localhost:8081/admin/users/agent-prod@example.com/policy/versions" \
    -H "Authorization: Bearer ${admin_token}"
```

### Audit Log

```bash
# Query audit entries
curl "http://localhost:8081/admin/audit?limit=50&offset=0" \
    -H "Authorization: Bearer ${admin_token}"

# Filter by user
curl "http://localhost:8081/admin/audit?user_id=agent-prod@example.com&limit=20" \
    -H "Authorization: Bearer ${admin_token}"

# Filter by decision
curl "http://localhost:8081/admin/audit?decision=deny&limit=20" \
    -H "Authorization: Bearer ${admin_token}"
```

## Connecting an Agent

### Python Agent Example

```python
import os
import httpx

PROXY_TOKEN = os.environ["CRABTRAP_TOKEN"]
PROXY_URL = f"http://{PROXY_TOKEN}:@localhost:8080"
CA_CERT_PATH = "./ca.crt"

# httpx client with CrabTrap proxy
client = httpx.Client(
    proxies={
        "http://": PROXY_URL,
        "https://": PROXY_URL,
    },
    verify=CA_CERT_PATH,
)

# All requests through this client go through CrabTrap
response = client.get("https://api.github.com/repos/myorg/myrepo")
```

### Using Environment Variables (Standard Proxy)

```bash
export HTTP_PROXY="http://${CRABTRAP_TOKEN}:@localhost:8080"
export HTTPS_PROXY="http://${CRABTRAP_TOKEN}:@localhost:8080"
export REQUESTS_CA_BUNDLE="./ca.crt"  # Python requests
export SSL_CERT_FILE="./ca.crt"       # general
export NODE_EXTRA_CA_CERTS="./ca.crt" # Node.js
```

### Node.js Agent Example

```javascript
import { HttpsProxyAgent } from 'https-proxy-agent';
import fetch from 'node-fetch';

const proxyToken = process.env.CRABTRAP_TOKEN;
const agent = new HttpsProxyAgent(`http://${proxyToken}:@localhost:8080`);

// Fetch through CrabTrap
const response = await fetch('https://api.github.com/repos/myorg/myrepo', {
  agent,
  headers: { Authorization: `Bearer ${process.env.GITHUB_TOKEN}` },
});
```

### LangChain / OpenAI SDK

```python
import os
import httpx
from openai import OpenAI

PROXY_TOKEN = os.environ["CRABTRAP_TOKEN"]

# Route OpenAI calls through CrabTrap too (optional — lets you audit LLM calls)
http_client = httpx.Client(
    proxies={"https://": f"http://{PROXY_TOKEN}:@localhost:8080"},
    verify="./ca.crt",
)

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
    http_client=http_client,
)
```

## Writing Effective Policies

Policies are natural-language strings evaluated by the LLM judge. Be explicit about allowed and denied behaviors.

```text
# Example policy for a GitHub PR review agent
This agent reviews pull requests and posts review comments for the acme-corp GitHub organization.

ALLOWED:
- GET requests to api.github.com for any repository in the acme-corp organization
- POST to https://api.github.com/repos/acme-corp/*/pulls/*/reviews (submit reviews)
- POST to https://api.github.com/repos/acme-corp/*/issues/*/comments (post comments)

DENIED:
- Any requests outside of api.github.com
- DELETE or PATCH requests to any endpoint
- Accessing /orgs/acme-corp/members or any user/credential endpoints
- Requests containing secrets, tokens, or API keys in the body
- Requests to change repository settings, branch protection, or webhooks

When in doubt, deny the request and explain why.
```

**Policy writing tips:**
1. Start with what the agent is supposed to do (scope context for the LLM)
2. List explicit ALLOWED patterns before DENIED
3. Add a catch-all denial at the end
4. Deny rules in static rules are evaluated before LLM — use them for hard limits

## Policy Builder (Agentic Policy Generation)

CrabTrap can analyze observed traffic and draft a policy automatically:

```bash
# Trigger policy builder via admin API
curl -X POST "http://localhost:8081/admin/users/agent-prod@example.com/policy/build" \
    -H "Authorization: Bearer ${admin_token}" \
    -d '{"sample_limit": 200}'
```

The builder runs an agentic loop, analyzes recent audit entries, and proposes a policy draft for review in the UI.

## Eval System

Replay historical audit entries against a policy to measure accuracy before deploying:

```bash
# Run eval from CLI
./gateway eval \
    --user-id agent-prod@example.com \
    --policy-id <version-id> \
    --limit 500

# Or via API
curl -X POST "http://localhost:8081/admin/users/agent-prod@example.com/policy/eval" \
    -H "Authorization: Bearer ${admin_token}" \
    -d '{"policy_version_id": "<id>", "sample_limit": 500}'
```

Eval compares LLM judge decisions against the historical ground truth and reports accuracy, false positive rate, and false negative rate.

## Troubleshooting

### TLS Certificate Errors

```bash
# Agent gets SSL verification error
# → Make sure the CA cert is trusted

# For curl:
curl --cacert ./ca.crt -x "http://${token}:@localhost:8080" https://example.com

# For Python requests:
export REQUESTS_CA_BUNDLE=./ca.crt

# For Node.js:
export NODE_EXTRA_CA_CERTS=./ca.crt

# Regenerate certs if expired:
docker compose exec crabtrap ./gateway gen-certs
docker compose cp crabtrap:/app/certs/ca.crt ./ca.crt
```

### All Requests Being Blocked (LLM Unavailable)

```yaml
# In gateway.yaml — change fallback to passthrough during LLM outages
llm_judge:
  fallback_mode: passthrough  # default is "deny"
```

Or check circuit breaker status:
```bash
curl http://localhost:8081/admin/health \
    -H "Authorization: Bearer ${admin_token}"
```

### SSRF Blocks Legitimate Internal APIs

```yaml
proxy:
  ssrf_allowlist:
    - "10.10.0.0/16"   # your internal API subnet
```

### Rate Limiting

```yaml
proxy:
  rate_limit:
    requests_per_second: 200   # increase for high-throughput agents
    burst: 400
```

### Debug Logging

```yaml
log_level: debug
audit:
  output: /var/log/crabtrap-debug.json
```

```bash
# Stream logs
docker compose logs -f crabtrap

# Query recent denials from audit log
curl "http://localhost:8081/admin/audit?decision=deny&limit=10" \
    -H "Authorization: Bearer ${admin_token}" | jq '.entries[].reason'
```

### Database Connection Issues

```bash
# Check migration status
docker compose exec crabtrap ./gateway migrate --dry-run

# Force re-run migrations
docker compose exec crabtrap ./gateway migrate --force
```

## Development

```bash
# Clone and build
git clone https://github.com/brexhq/CrabTrap
cd CrabTrap

make build        # production binary (embeds web UI)
make build-web    # rebuild React UI only
make test         # lint + race-condition tests
make fmt          # format Go code
make lint         # go vet + staticcheck
```

### Project Layout Quick Reference

| Path | Purpose |
|------|---------|
| `cmd/gateway/` | Entry point, admin API wiring |
| `internal/proxy/` | MITM proxy, TLS generation, SSRF, rate limiting |
| `internal/approval/` | Static rules engine + orchestration |
| `internal/judge/` | LLM prompt construction + response parsing |
| `internal/llm/` | LLM adapters, circuit breaker |
| `internal/builder/` | Agentic policy builder loop |
| `internal/eval/` | Eval/replay system |
| `internal/admin/` | Admin API routes and auth |
| `pkg/types/` | Shared types (StaticRule, LLMPolicy, AuditEntry) |
| `web/src/` | React + TypeScript admin UI |
