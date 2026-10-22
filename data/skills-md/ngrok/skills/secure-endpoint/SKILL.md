---
name: secure-endpoint
description: Put authentication, rate limiting, IP restrictions, header rules, or a custom response in front of an ngrok endpoint using a Traffic Policy, without changing application code. Covers requiring login (OAuth/OIDC), locking to specific IPs, blocking or denying requests, returning a maintenance page or custom response, and injecting or stripping headers. Use when the user wants to protect, gate, throttle, or add an API-gateway layer to an endpoint. Use when the user says "add auth to my ngrok URL", "require Google login", "rate limit my endpoint", "restrict by IP", "block a path", or "put up a maintenance page".
license: MIT
metadata:
  author: ngrok
  version: "1.0"
  category: security
  surface: job
compatibility: Requires ngrok CLI installed and authenticated.
---

# Secure an endpoint

Add access control, throttling, or an edge response to an endpoint with a Traffic Policy - no app changes. One skill covers the common gates; jump to the scenario that matches the ask.

## Before you start

Auth is required (`ngrok-setup`). Pull action configs and, if the endpoint being secured is a private receiver, the internal-binding rules from `ngrok-engine`.

## Scenarios

### Require login (OAuth / OIDC)

Gate the endpoint behind an identity provider, then optionally restrict to specific users.

```yaml
on_http_request:
  - actions:
      - type: oauth
        config: { provider: google }
  - expressions:
      - "!actions.ngrok.oauth.identity.email.endsWith('@yourcompany.com')"
    actions:
      - type: deny
```

Full provider list and raw OIDC: `ngrok-engine` -> `ngrok-engine/references/auth-actions.md`.

### Lock to specific IPs

Allow only known addresses/CIDRs; deny the rest.

```yaml
on_http_request:
  - actions:
      - type: restrict-ips
        config:
          enforce: true
          allow:
            - 203.0.113.4/32
            - 198.51.100.0/24
```

Use `restrict-ips` for ranges. `conn.client_ip in [...]` does exact string
comparison: it matches a bare address (`'203.0.113.4'`) but never a CIDR, because
`203.0.113.4` is not equal to the string `203.0.113.4/32` - so a list of CIDRs
matches nothing and the rule denies everyone. `restrict-ips` is what evaluates
CIDRs. A CEL `in` test is fine for a couple of exact addresses.

### Block a path or condition (deny)

```yaml
on_http_request:
  - expressions: ["req.url.path.startsWith('/admin')"]
    actions:
      - type: deny
        config: { status_code: 403 }
```

### Rate limit

Throttle by client to protect the upstream. Get the current `rate-limit` action config from `ngrok-engine` (it takes a name, rate, bucket key, algorithm, and capacity) and attach it the same way as the others.

### Maintenance page / custom response

Return a response straight from the edge without hitting the upstream.

```yaml
on_http_request:
  - actions:
      - type: custom-response
        config:
          status_code: 503
          headers: { content-type: text/html }
          body: "<html><body><h1>Back soon</h1></body></html>"
```

Health check that never touches the app:

```yaml
on_http_request:
  - expressions: ["req.url.path == '/healthz'"]
    actions:
      - type: custom-response
        config:
          {
            status_code: 200,
            headers: { content-type: text/plain },
            body: "ok",
          }
```

### Add / strip headers

Usually a supporting step (inject an upstream auth header, add CORS, remove a header). See `add-headers` in `ngrok-engine`.

## Combining

Rules run in order; stack them. Typical API-gateway front door: restrict-ips -> oauth -> rate-limit -> forward. Keep terminating actions (`deny`, `custom-response`) in the rule that should stop the chain.

## Apply it

Attach the policy on the user's surface - see `ngrok-surfaces`. Same policy body everywhere.

## Notes for agents

- Match the scenario to the user's words; don't dump all of them.
- These compose with other jobs: securing a webhook receiver is this skill's auth rules plus `receive-webhooks`' verify+forward.
- No app code changes - if you're reaching for the app's auth middleware, stop; that's what this replaces.
