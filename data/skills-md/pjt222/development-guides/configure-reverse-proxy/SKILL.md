---
name: configure-reverse-proxy
description: >
  Configure reverse proxy patterns across multiple tools including Nginx,
  Traefik, and ShinyProxy. Covers WebSocket proxying, path-based and
  host-based routing, SSL termination, and Docker label auto-discovery.
  Use when routing multiple services behind a single entry point, proxying
  WebSocket connections (Shiny, Socket.IO), auto-discovering Docker services
  with Traefik labels, or adding SSL termination to services that don't
  handle TLS natively.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: containerization
  complexity: intermediate
  language: multi
  tags: reverse-proxy, traefik, nginx, websocket, routing, shinyproxy, ssl
---

# Configure Reverse Proxy

Set up reverse proxy patterns for routing traffic to backend services using Nginx, Traefik, or ShinyProxy.

## When to Use

- Routing multiple services behind a single entry point
- Proxying WebSocket connections (Shiny, Socket.IO, live reload)
- Auto-discovering Docker services with Traefik labels
- Path-based or host-based routing to different backends
- Adding SSL termination to services that don't handle TLS

## Inputs

- **Required**: Backend services to proxy (host:port)
- **Required**: Routing strategy (path-based, host-based, or both)
- **Optional**: Proxy tool preference (Nginx, Traefik)
- **Optional**: Domain name(s) for host-based routing
- **Optional**: WebSocket endpoints to proxy

## Procedure

### Step 1: Choose Proxy Tool

| Feature | Nginx | Traefik |
|---------|-------|---------|
| Configuration | Static files | Docker labels / dynamic |
| Auto-discovery | No (manual) | Yes (Docker provider) |
| Let's Encrypt | Via certbot | Built-in ACME |
| Dashboard | No (3rd party) | Built-in |
| WebSocket | Manual config | Automatic |
| Best for | Static config, high traffic | Dynamic Docker environments |

### Step 2: Nginx — Path-Based Routing

```nginx
server {
    listen 80;

    location /api/ {
        proxy_pass http://api:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /app/ {
        proxy_pass http://webapp:3000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
    }
}
```

**Note:** Trailing `/` on `proxy_pass` strips the location prefix. `proxy_pass http://api:8000/;` with `location /api/` forwards `/api/users` as `/users`.

### Step 3: Nginx — Host-Based Routing

```nginx
server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://api:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

server {
    listen 80;
    server_name app.example.com;

    location / {
        proxy_pass http://webapp:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Step 4: Nginx — WebSocket Proxying

WebSockets require upgrade headers. Essential for Shiny, Socket.IO, and live reload:

```nginx
location /ws/ {
    proxy_pass http://app:3000;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_read_timeout 86400;
}
```

For Shiny apps specifically:

```nginx
map $http_upgrade $connection_upgrade {
    default upgrade;
    ''      close;
}

server {
    location / {
        proxy_pass http://shiny:3838;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
        proxy_set_header Host $host;
        proxy_read_timeout 86400;
        proxy_buffering off;
    }
}
```

**Expected:** WebSocket connections establish and persist.

**On failure:** Check `proxy_http_version 1.1` is set. Verify `Upgrade` and `Connection` headers.

### Step 5: Traefik — Docker Label Auto-Discovery

`docker-compose.yml`:

```yaml
services:
  traefik:
    image: traefik:v3.2
    command:
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      - "--certificatesresolvers.letsencrypt.acme.email=admin@example.com"
      - "--certificatesresolvers.letsencrypt.acme.storage=/letsencrypt/acme.json"
      - "--certificatesresolvers.letsencrypt.acme.httpchallenge.entrypoint=web"
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - letsencrypt:/letsencrypt

  api:
    image: myapi:latest
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.api.rule=Host(`api.example.com`)"
      - "traefik.http.routers.api.entrypoints=websecure"
      - "traefik.http.routers.api.tls.certresolver=letsencrypt"
      - "traefik.http.services.api.loadbalancer.server.port=8000"

  webapp:
    image: myapp:latest
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.webapp.rule=Host(`app.example.com`)"
      - "traefik.http.routers.webapp.entrypoints=websecure"
      - "traefik.http.routers.webapp.tls.certresolver=letsencrypt"
      - "traefik.http.services.webapp.loadbalancer.server.port=3000"

volumes:
  letsencrypt:
```

**Expected:** Traefik auto-discovers services via labels, provisions SSL certificates.

### Step 6: Traefik — Path-Based Routing with Labels

```yaml
services:
  api:
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.api.rule=Host(`example.com`) && PathPrefix(`/api`)"
      - "traefik.http.routers.api.middlewares=strip-api"
      - "traefik.http.middlewares.strip-api.stripprefix.prefixes=/api"
      - "traefik.http.services.api.loadbalancer.server.port=8000"
```

### Step 7: Traefik — Rate Limiting and Headers

```yaml
labels:
  - "traefik.http.middlewares.ratelimit.ratelimit.average=100"
  - "traefik.http.middlewares.ratelimit.ratelimit.burst=50"
  - "traefik.http.middlewares.security.headers.stsSeconds=63072000"
  - "traefik.http.middlewares.security.headers.contentTypeNosniff=true"
  - "traefik.http.middlewares.security.headers.frameDeny=true"
  - "traefik.http.routers.app.middlewares=ratelimit,security"
```

### Step 8: Verify Proxy Configuration

```bash
# Nginx: test config
docker compose exec nginx nginx -t

# Check routing
curl -H "Host: api.example.com" http://localhost/health

# Check WebSocket (needs wscat: npm install -g wscat)
wscat -c ws://localhost/ws/

# Traefik dashboard (if enabled)
# http://localhost:8080/dashboard/
```

**Expected:** Requests route to correct backends. WebSocket upgrades succeed.

## Validation

- [ ] HTTP requests route to the correct backend based on path or host
- [ ] WebSocket connections establish and maintain
- [ ] SSL termination works (if configured)
- [ ] Backend services receive correct `Host`, `X-Real-IP`, `X-Forwarded-For` headers
- [ ] Traefik auto-discovers new services via labels (if using Traefik)
- [ ] Configuration survives `docker compose restart`

## Common Pitfalls

- **Trailing slash mismatch**: `proxy_pass http://app/` vs `http://app` behaves differently with path stripping in Nginx.
- **WebSocket timeout**: Default `proxy_read_timeout` is 60s. Long-lived WebSocket connections need `86400` (24h).
- **Docker socket security**: Mounting `/var/run/docker.sock` in Traefik gives it full Docker access. Use `ro` mount and consider socket proxy.
- **DNS resolution**: Nginx resolves upstreams at startup. Use `resolver 127.0.0.11` for Docker's internal DNS with dynamic services.
- **Missing `proxy_buffering off`**: Shiny and SSE endpoints need `proxy_buffering off` for real-time streaming.

## Related Skills

- `configure-nginx` - detailed Nginx configuration with SSL and security headers
- `deploy-shinyproxy` - ShinyProxy for containerized Shiny app hosting
- `setup-compose-stack` - compose stack that uses a reverse proxy
- `configure-api-gateway` - API gateway patterns with Kong and Traefik
