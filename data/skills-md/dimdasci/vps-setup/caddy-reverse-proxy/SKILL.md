---
name: caddy-reverse-proxy
description: |
  Caddy web server configuration for reverse proxy and automatic HTTPS. Use when:
  (1) Writing Caddyfile configurations for reverse proxy setups
  (2) Configuring automatic HTTPS with Let's Encrypt
  (3) Setting up wildcard certificates with DNS challenge
  (4) Integrating Caddy with Docker containers (same network or host services)
  (5) Configuring request matchers, handle blocks, and routing patterns
  (6) Setting up load balancing and health checks
  (7) Troubleshooting TLS, upstream connectivity, or configuration issues
  (8) Configuring header manipulation (header_up, header_down)
---

# Caddy Reverse Proxy

Caddy is a web server with automatic HTTPS. It obtains and renews certificates automatically, redirects HTTP to HTTPS, and provides a simple configuration syntax.

## Quick Reference

| Task | Syntax |
|------|--------|
| Basic proxy | `reverse_proxy backend:8080` |
| Multiple upstreams | `reverse_proxy node1:80 node2:80` |
| Path routing | `handle /api/* { reverse_proxy api:8080 }` |
| Strip path prefix | `handle_path /api/* { reverse_proxy api:8080 }` |
| Set request header | `header_up Host localhost` |
| Remove response header | `header_down -Server` |
| Wildcard cert | `tls { dns cloudflare {env.CF_API_TOKEN} }` |
| Reload config | `caddy reload --config /etc/caddy/Caddyfile` |

## Basic Patterns

### Simple Reverse Proxy

```
example.com {
    reverse_proxy backend:8080
}
```

### Multiple Sites

```
app.example.com {
    reverse_proxy app:3000
}

api.example.com {
    reverse_proxy api:8080
}
```

### Path-Based Routing

```
example.com {
    handle /api/* {
        reverse_proxy api:8080
    }
    handle {
        reverse_proxy frontend:3000
    }
}
```

### Strip Path Prefix

```
example.com {
    handle_path /api/* {
        reverse_proxy api:8080  # /api/users → /users
    }
}
```

## Header Manipulation

```
example.com {
    reverse_proxy backend:8080 {
        # Set Host header (required by some backends)
        header_up Host localhost

        # Add client IP
        header_up X-Real-IP {remote_host}

        # Remove sensitive header
        header_up -Authorization

        # Remove server identity from response
        header_down -Server
    }
}
```

## Docker Integration

### Proxy to Container (Same Network)

```yaml
# docker-compose.yml
services:
  caddy:
    image: caddy:2-alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile:ro
      - caddy_data:/data
    networks:
      - web

  app:
    image: myapp
    networks:
      - web
    expose:
      - "8080"
```

```
# Caddyfile - use container name as hostname
example.com {
    reverse_proxy app:8080
}
```

### Proxy to Host Service

```yaml
services:
  caddy:
    extra_hosts:
      - "host.docker.internal:host-gateway"
```

```
example.com {
    reverse_proxy host.docker.internal:8080
}
```

## TLS Configuration

### Automatic (Default)

Caddy automatically obtains certificates when:
- Domain DNS points to server
- Ports 80/443 accessible

### Wildcard Certificates

Requires DNS provider plugin:

```
*.example.com {
    tls {
        dns cloudflare {env.CF_API_TOKEN}
    }

    @app1 host app1.example.com
    handle @app1 {
        reverse_proxy app1:8080
    }

    @app2 host app2.example.com
    handle @app2 {
        reverse_proxy app2:8080
    }
}
```

### Internal/Development

```
localhost {
    tls internal
    reverse_proxy app:8080
}
```

## Request Matchers

```
# Path matching
@api path /api/*

# Header matching
@websocket header Connection *Upgrade*

# Method matching
@post method POST

# Combined (AND logic)
@api_post {
    path /api/*
    method POST
}

# Use matcher
handle @api {
    reverse_proxy api:8080
}
```

## Load Balancing

```
example.com {
    reverse_proxy node1:80 node2:80 node3:80 {
        lb_policy round_robin
        health_uri /health
        health_interval 30s
    }
}
```

## Common Configurations

### Security Headers

```
(security) {
    header {
        Strict-Transport-Security "max-age=31536000; includeSubDomains"
        X-Content-Type-Options nosniff
        X-Frame-Options SAMEORIGIN
        Referrer-Policy strict-origin-when-cross-origin
    }
}

example.com {
    import security
    reverse_proxy backend:8080
}
```

### www Redirect

```
www.example.com {
    redir https://example.com{uri} permanent
}
```

### SPA (Single Page App)

```
example.com {
    root * /srv
    try_files {path} /index.html
    file_server
}
```

### gRPC / HTTP/2 Cleartext

```
example.com {
    reverse_proxy h2c://grpc-server:9000
}
```

## Global Options

```
{
    email admin@example.com

    # Use staging for testing
    # acme_ca https://acme-staging-v02.api.letsencrypt.org/directory
}

example.com {
    # site config
}
```

## Reference Files

| File | When to Read |
|------|--------------|
| [reverse-proxy.md](references/reverse-proxy.md) | Load balancing, health checks, transport options |
| [caddyfile-syntax.md](references/caddyfile-syntax.md) | Matchers, handle blocks, directives |
| [tls-certificates.md](references/tls-certificates.md) | DNS challenge, wildcards, mTLS |
| [docker-patterns.md](references/docker-patterns.md) | Docker Compose, networks, host access |
| [troubleshooting.md](references/troubleshooting.md) | Common errors and diagnostics |

## Common Issues

| Problem | Solution |
|---------|----------|
| "no upstreams available" | Check backend running, same Docker network |
| "connection refused" | Backend binding to 0.0.0.0, not 127.0.0.1 |
| Certificate not obtained | Check DNS points to server, ports 80/443 open |
| 403 Forbidden | Backend needs `header_up Host localhost` |
| WebSocket fails | Usually works; check `flush_interval -1` for SSE |

## Verification Commands

```bash
# Validate config
caddy validate --config /etc/caddy/Caddyfile

# Format config
caddy fmt --overwrite /etc/caddy/Caddyfile

# Reload (zero-downtime)
caddy reload --config /etc/caddy/Caddyfile

# Debug mode
# Add to global options: { debug }

# Check certificate
openssl s_client -connect example.com:443 -servername example.com
```

## Official Documentation

| Topic | URL |
|-------|-----|
| Caddyfile | https://caddyserver.com/docs/caddyfile |
| reverse_proxy | https://caddyserver.com/docs/caddyfile/directives/reverse_proxy |
| Automatic HTTPS | https://caddyserver.com/docs/automatic-https |
| Common Patterns | https://caddyserver.com/docs/caddyfile/patterns |
