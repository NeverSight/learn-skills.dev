---
name: nginx
description: |
  Nginx web server and reverse proxy expert: configuration, reverse proxying, load balancing,
  SSL/TLS termination, rate limiting, caching, gzip compression, WebSocket proxying, and
  security hardening. Use for nginx.conf creation/review, performance tuning, HTTPS setup,
  upstream configuration, and troubleshooting.
metadata:
  tags: nginx, reverse-proxy, load-balancer, ssl, tls, web-server, devops, caching
---

# Nginx Expert

## When to Use

- Creating or reviewing nginx configuration files
- Setting up reverse proxy or load balancer
- Configuring SSL/TLS and HTTPS
- Implementing rate limiting or access control
- Optimizing performance (caching, gzip, keepalive)
- WebSocket proxying
- Serving static content
- Debugging nginx issues (502, 504, connection errors)

**Out of scope** (recommend dedicated skills):
- Docker containerization -> docker expert
- Kubernetes ingress controllers -> kubernetes expert
- Application-level code -> relevant framework skill

## Core Principles

1. **Security-first** -- TLS 1.2+ only, strong ciphers, no server tokens, rate limiting
2. **Minimal exposure** -- only expose what's needed, hide upstream details
3. **Performance** -- leverage caching, gzip, keepalive connections, sendfile
4. **Clarity** -- well-organized config with comments, logical server/location blocks

## Configuration File Structure

```
main (global)
├── events { }          -- connection processing
├── http { }            -- HTTP server config
│   ├── upstream { }    -- backend server groups
│   ├── server { }      -- virtual hosts
│   │   ├── location { } -- request routing
│   │   └── location { }
│   └── server { }
└── stream { }          -- TCP/UDP proxying
```

**Key rules:**
- Simple directives end with semicolon (`;`)
- Block directives use braces (`{` `}`)
- Directives inherit from parent contexts unless overridden
- Comments start with `#`
- Default config path: `/etc/nginx/nginx.conf`

## Process Management

```bash
nginx -t           # test configuration syntax
nginx -s reload    # graceful reload (re-read config)
nginx -s quit      # graceful shutdown
nginx -s stop      # fast shutdown
nginx -s reopen    # reopen log files
```

## Location Matching

Priority order (highest to lowest):

| Modifier | Type | Example |
|---|---|---|
| `=` | Exact match | `location = /` |
| `^~` | Prefix (skip regex) | `location ^~ /images/` |
| `~` | Regex (case-sensitive) | `location ~ \.php$` |
| `~*` | Regex (case-insensitive) | `location ~* \.(jpg\|png)$` |
| (none) | Prefix | `location /docs/` |

**Algorithm:** Check all prefix locations (remember longest) -> if longest has `^~`, use it -> check regex in config order (first match wins) -> fallback to longest prefix.

## Serving Static Content

```nginx
server {
    listen 80;
    server_name example.com;
    root /var/www/html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location ~* \.(js|css|png|jpg|gif|ico|svg|woff2?)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### root vs alias

```nginx
# root: appends URI to path
location /images/ {
    root /data;           # /images/photo.jpg -> /data/images/photo.jpg
}

# alias: replaces matched location
location /images/ {
    alias /data/photos/;  # /images/photo.jpg -> /data/photos/photo.jpg
}
```

## Reverse Proxy

```nginx
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### proxy_pass URI Behavior

```nginx
# WITH trailing slash -- strips location prefix
location /api/ {
    proxy_pass http://backend/;    # /api/users -> /users
}

# WITHOUT trailing slash -- passes full URI
location /api/ {
    proxy_pass http://backend;     # /api/users -> /api/users
}
```

Full proxy and upstream reference: [references/proxy-upstream.md](references/proxy-upstream.md)

## Load Balancing

```nginx
# Round-robin (default)
upstream backend {
    server backend1.example.com;
    server backend2.example.com;
}

# Weighted
upstream backend {
    server backend1.example.com weight=5;
    server backend2.example.com weight=1;
}

# Least connections
upstream backend {
    least_conn;
    server backend1.example.com;
    server backend2.example.com;
}

# IP hash (session persistence)
upstream backend {
    ip_hash;
    server backend1.example.com;
    server backend2.example.com;
}
```

### Server Parameters

- `weight=N` -- server weight (default 1)
- `max_fails=N` -- failures before marking unavailable (default 1)
- `fail_timeout=T` -- failure window AND unavailability duration (default 10s)
- `max_conns=N` -- max simultaneous connections (default 0 = unlimited)
- `backup` -- only used when primary servers are all down
- `down` -- permanently marked as unavailable

### Upstream Keepalive

```nginx
upstream backend {
    server backend1.example.com;
    keepalive 32;
}

server {
    location / {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
    }
}
```

Full proxy and upstream reference: [references/proxy-upstream.md](references/proxy-upstream.md)

## SSL/TLS

```nginx
server {
    listen 443 ssl;
    server_name example.com;

    ssl_certificate     /etc/nginx/ssl/example.com.crt;
    ssl_certificate_key /etc/nginx/ssl/example.com.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
}

# HTTP to HTTPS redirect
server {
    listen 80;
    server_name example.com;
    return 301 https://$host$request_uri;
}
```

Full SSL/TLS reference (OCSP, SNI, cert chains, hardening): [references/ssl-tls.md](references/ssl-tls.md)

## Rate Limiting

```nginx
http {
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

    server {
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            limit_req_status 429;
            proxy_pass http://backend;
        }
    }
}
```

- `rate=Nr/s` or `rate=Nr/m` -- requests per second/minute (leaky bucket)
- `burst=N` -- allow N excess requests to queue
- `nodelay` -- process burst immediately without delay
- `$binary_remote_addr` -- preferred over `$remote_addr` (4/16 bytes vs string)

Full security reference: [references/security.md](references/security.md)

## Gzip Compression

```nginx
http {
    gzip on;
    gzip_comp_level 5;
    gzip_min_length 256;
    gzip_vary on;
    gzip_proxied any;
    gzip_types text/plain text/css text/javascript
               application/javascript application/json
               application/xml image/svg+xml;
}
```

`text/html` is always compressed -- don't list it in `gzip_types`.

## WebSocket Proxying

```nginx
http {
    map $http_upgrade $connection_upgrade {
        default upgrade;
        ''      close;
    }

    server {
        location /ws/ {
            proxy_pass http://websocket_backend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection $connection_upgrade;
            proxy_read_timeout 3600s;
            proxy_send_timeout 3600s;
        }
    }
}
```

Default `proxy_read_timeout` is 60s -- idle WebSocket connections will be closed. Increase the timeout or use backend ping frames.

## Logging

```nginx
http {
    log_format main '$remote_addr - $remote_user [$time_local] '
                    '"$request" $status $body_bytes_sent '
                    '"$http_referer" "$http_user_agent" '
                    '$request_time $upstream_response_time';

    access_log /var/log/nginx/access.log main;
    error_log  /var/log/nginx/error.log warn;

    server {
        location /health {
            access_log off;
            return 200 "OK";
        }
    }
}
```

## Performance Tuning

```nginx
worker_processes auto;

events {
    worker_connections 1024;
    multi_accept on;
}

http {
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65s;
    keepalive_requests 1000;

    open_file_cache max=1000 inactive=20s;
    open_file_cache_valid 30s;
    open_file_cache_min_uses 2;
    open_file_cache_errors on;
}
```

Full caching and performance reference: [references/caching-performance.md](references/caching-performance.md)

## Production Checklist

- [ ] `nginx -t` passes
- [ ] `server_tokens off`
- [ ] SSL/TLS with TLSv1.2+ only
- [ ] HTTP to HTTPS redirect
- [ ] HSTS header enabled
- [ ] Security headers (X-Frame-Options, CSP, X-Content-Type-Options)
- [ ] Rate limiting on sensitive endpoints
- [ ] `client_max_body_size` set appropriately
- [ ] Gzip compression enabled
- [ ] Static asset caching with `expires`
- [ ] Logging configured with rotation
- [ ] Hidden files blocked (`location ~ /\. { deny all; }`)
- [ ] Upstream keepalive with `proxy_http_version 1.1`
- [ ] `worker_processes auto`, `sendfile on`, `tcp_nopush on`

## Anti-Patterns

| Don't | Do Instead |
|---|---|
| Use `if` for complex routing | Use `map` + variables or multiple `location` blocks |
| Leave `server_tokens` on | `server_tokens off;` |
| Allow TLSv1.0/1.1 | `ssl_protocols TLSv1.2 TLSv1.3;` |
| Use `proxy_pass` without `Host` header | Set `proxy_set_header Host $host;` |
| Skip `proxy_http_version` with keepalive | `proxy_http_version 1.1;` and clear Connection header |
| Hardcode IPs in config | Use `upstream` blocks with named servers |
| Ignore `proxy_read_timeout` for long requests | Tune per-location based on expected response times |
| Use `root` inside `if` blocks | Place `root` in `server` or `location` context |

## Diagnostics

### 502 Bad Gateway
- Backend is down or not listening
- Check `proxy_pass` URL and backend connectivity

### 504 Gateway Timeout
- Backend is too slow -- increase `proxy_read_timeout`

### 413 Request Entity Too Large
- Increase `client_max_body_size`

### Configuration Errors
- Always test before reload: `nginx -t`
- Check error log: `tail -f /var/log/nginx/error.log`

## Key Variables

| Variable | Description |
|---|---|
| `$host` | Host header or server name |
| `$remote_addr` | Client IP address |
| `$binary_remote_addr` | Client IP in binary (for limit zones) |
| `$proxy_add_x_forwarded_for` | X-Forwarded-For + client IP |
| `$scheme` | `http` or `https` |
| `$request_uri` | Full original URI with query string |
| `$uri` | Normalized URI (without query string) |
| `$args` | Query string |
| `$upstream_response_time` | Response time from upstream |
| `$upstream_cache_status` | Cache hit/miss status |

## Reference Index

| Topic | File |
|-------|------|
| Proxy module, upstream, load balancing, timeouts, buffering, keepalive | [references/proxy-upstream.md](references/proxy-upstream.md) |
| SSL/TLS, HTTPS, certificates, OCSP, SNI, HTTP/2, HTTP/3 | [references/ssl-tls.md](references/ssl-tls.md) |
| Security headers, rate limiting, access control, client limits | [references/security.md](references/security.md) |
| Proxy caching, gzip, performance tuning, open file cache | [references/caching-performance.md](references/caching-performance.md) |
| Full config patterns: API gateway, SPA, microservices, logging | [references/common-patterns.md](references/common-patterns.md) |
