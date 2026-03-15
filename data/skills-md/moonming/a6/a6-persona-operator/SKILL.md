---
name: a6-persona-operator
description: >-
  Persona skill for platform operators and DevOps engineers managing APISIX
  instances using the a6 CLI. Provides decision frameworks for day-to-day
  operations including deployment, monitoring, troubleshooting, scaling,
  security hardening, and disaster recovery workflows.
version: "1.0.0"
author: Apache APISIX Contributors
license: Apache-2.0
metadata:
  category: persona
  apisix_version: ">=3.0.0"
  a6_commands:
    - a6 route list
    - a6 upstream list
    - a6 upstream health
    - a6 config sync
    - a6 config dump
    - a6 config diff
    - a6 config validate
    - a6 debug logs
    - a6 debug trace
    - a6 health
    - a6 ssl create
    - a6 global-rule create
---

# a6-persona-operator

## Who This Is For

You are a **platform operator or DevOps engineer** responsible for:
- Managing one or more APISIX gateway instances
- Ensuring API availability and performance
- Deploying and rolling back configuration changes
- Monitoring health, diagnosing issues, and responding to incidents
- Enforcing security policies across all APIs

## Context Management

Operators typically manage multiple environments. Use contexts to switch
between them without re-entering connection details.

```bash
# Set up contexts for each environment
a6 context create dev --server http://apisix-dev:9180 --api-key dev-key-123
a6 context create staging --server http://apisix-staging:9180 --api-key staging-key-456
a6 context create prod --server http://apisix-prod:9180 --api-key prod-key-789

# Switch to production
a6 context use prod

# Check current context
a6 context current

# List all contexts
a6 context list
```

Always verify the active context before running destructive operations.

## Daily Operations Checklist

### 1. Health check

```bash
# Verify APISIX is reachable and get version
a6 health

# Check all upstream health status
a6 upstream list --output json | jq '.[] | {id: .id, name: .name}'
a6 upstream health <upstream-id>
```

### 2. Configuration audit

```bash
# Dump current state
a6 config dump > current-state.yaml

# Compare with expected state
a6 config diff -f expected-state.yaml

# Validate a config file before applying
a6 config validate -f new-config.yaml
```

### 3. Certificate management

```bash
# List SSL certificates and check expiry
a6 ssl list

# Upload a new certificate
a6 ssl create -f - <<'EOF'
{
  "cert": "-----BEGIN CERTIFICATE-----\n...\n-----END CERTIFICATE-----",
  "key": "-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----",
  "snis": ["api.example.com", "*.example.com"]
}
EOF
```

## Deployment Workflow

### Safe deployment pattern

```bash
# 1. Validate the config locally
a6 config validate -f new-config.yaml

# 2. Preview what will change
a6 config diff -f new-config.yaml

# 3. Apply to staging first
a6 --context staging config sync -f new-config.yaml

# 4. Verify staging
a6 --context staging health
a6 --context staging route list

# 5. Apply to production
a6 --context prod config sync -f new-config.yaml

# 6. Verify production
a6 --context prod health
```

### Rollback

```bash
# Keep a backup before every deployment
a6 config dump > backup-$(date +%Y%m%d-%H%M%S).yaml

# Rollback by syncing the backup
a6 config sync -f backup-20260308-143000.yaml
```

## Troubleshooting

### Request not reaching upstream

```bash
# 1. Check if the route exists
a6 route list
a6 route get <route-id> --output json

# 2. Trace the request path
a6 debug trace --uri /api/v1/users --method GET

# 3. Stream error logs in real-time
a6 debug logs --follow

# 4. Check upstream health
a6 upstream health <upstream-id>
```

### 502 Bad Gateway

```bash
# Check upstream node health
a6 upstream get <upstream-id> --output json

# Verify backend is reachable from APISIX
a6 debug trace --uri /failing-endpoint

# Check error logs for connection refused / timeout
a6 debug logs --follow --level error
```

### Authentication failures (401/403)

```bash
# Verify consumer exists and has correct credentials
a6 consumer list
a6 consumer get <username> --output json

# Check the route's auth plugin configuration
a6 route get <route-id> --output json | jq '.plugins'

# Check global rules that might override
a6 global-rule list --output json
```

## Security Hardening

### Global rate limiting

```bash
a6 global-rule create -f - <<'EOF'
{
  "id": "global-rate-limit",
  "plugins": {
    "limit-count": {
      "count": 10000,
      "time_window": 60,
      "key_type": "var",
      "key": "remote_addr",
      "rejected_code": 429
    }
  }
}
EOF
```

### Global IP restriction

```bash
a6 global-rule create -f - <<'EOF'
{
  "id": "global-ip-block",
  "plugins": {
    "ip-restriction": {
      "blacklist": ["10.0.0.0/8", "192.168.0.0/16"]
    }
  }
}
EOF
```

### Enforce CORS globally

```bash
a6 global-rule create -f - <<'EOF'
{
  "id": "global-cors",
  "plugins": {
    "cors": {
      "allow_origins": "https://app.example.com",
      "allow_methods": "GET,POST,PUT,DELETE,OPTIONS",
      "allow_headers": "Authorization,Content-Type",
      "max_age": 3600
    }
  }
}
EOF
```

## Monitoring Setup

### Enable Prometheus metrics

```bash
# Global rule to expose metrics for all routes
a6 global-rule create -f - <<'EOF'
{
  "id": "prometheus-metrics",
  "plugins": {
    "prometheus": {}
  }
}
EOF
```

Scrape metrics at `http://apisix:9091/apisix/prometheus/metrics`.

### Add HTTP logging

```bash
a6 global-rule create -f - <<'EOF'
{
  "id": "http-logging",
  "plugins": {
    "http-logger": {
      "uri": "http://log-collector:9200/_bulk",
      "batch_max_size": 1000,
      "inactive_timeout": 5
    }
  }
}
EOF
```

## Decision Framework

| Situation | Action |
|-----------|--------|
| New deployment | `config validate` → `config diff` → `config sync` (staging) → verify → `config sync` (prod) |
| Incident — route broken | `debug trace` → `debug logs` → fix → `config sync` |
| Incident — upstream down | `upstream health` → check backends → update nodes or enable health checks |
| Certificate expiring | `ssl list` → `ssl create` with new cert → `ssl delete` old |
| Performance issue | `debug logs` to find slow routes → add rate limiting or caching |
| Security audit | `config dump` → review global rules, auth plugins, IP restrictions |
| Rollback needed | `config sync -f backup.yaml` |
| New environment | `context create` → `config sync -f base-config.yaml` |

## Best Practices

1. **Always dump before sync** — `a6 config dump > backup.yaml` before every deployment
2. **Validate before apply** — `a6 config validate -f config.yaml` catches errors early
3. **Diff before sync** — `a6 config diff -f config.yaml` shows exactly what will change
4. **Stage before prod** — always apply to staging first, verify, then promote to production
5. **Use global rules sparingly** — they apply to ALL routes; prefer per-route plugins
6. **Monitor upstream health** — enable active health checks on critical upstreams
7. **Keep contexts organized** — name contexts clearly (prod, staging, dev) and verify
   the current context before destructive operations
8. **Version control configs** — store YAML configs in git for audit trail and rollback
