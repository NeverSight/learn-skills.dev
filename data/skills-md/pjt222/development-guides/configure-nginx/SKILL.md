---
name: configure-nginx
description: >
  Configure Nginx as a web server and reverse proxy. Covers static file
  serving, reverse proxy to upstream services, SSL/TLS termination with
  Let's Encrypt, location blocks, load balancing, rate limiting, and
  security headers. Use when serving static files in production, reverse
  proxying to backend services (Node.js, Python, R/Shiny), terminating
  SSL/TLS, load balancing across instances, or adding rate limiting and
  security headers to harden an endpoint.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: containerization
  complexity: intermediate
  language: multi
  tags: nginx, reverse-proxy, ssl, tls, lets-encrypt, web-server, security-headers
---

# Configure Nginx

Set up Nginx as a web server and reverse proxy with SSL termination and security hardening.

## When to Use

- Serving static files (HTML, CSS, JS) in production
- Reverse proxying to backend services (Node.js, Python, Go, R/Shiny)
- Terminating SSL/TLS with Let's Encrypt certificates
- Load balancing across multiple backend instances
- Adding rate limiting and security headers

## Inputs

- **Required**: Deployment target (Docker container or bare metal)
- **Required**: Backend service(s) to proxy (host:port)
- **Optional**: Domain name for SSL
- **Optional**: Static file directory

## Procedure

### Step 1: Basic Reverse Proxy

`nginx.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    upstream app {
        server app:3000;
    }

    server {
        listen 80;
        server_name example.com;

        location / {
            proxy_pass http://app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

Docker Compose service:

```yaml
services:
  nginx:
    image: nginx:1.27-alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - app
```

**Expected:** Requests to port 80 are forwarded to the app service.

### Step 2: Static File Serving

```nginx
server {
    listen 80;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /assets/ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff2?)$ {
        expires 6M;
        add_header Cache-Control "public";
    }
}
```

### Step 3: SSL/TLS with Let's Encrypt

Using certbot with the webroot method:

```nginx
server {
    listen 80;
    server_name example.com;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl;
    server_name example.com;

    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    location / {
        proxy_pass http://app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Docker Compose with certbot:

```yaml
services:
  nginx:
    image: nginx:1.27-alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - certbot-webroot:/var/www/certbot:ro
      - certbot-certs:/etc/letsencrypt:ro

  certbot:
    image: certbot/certbot
    volumes:
      - certbot-webroot:/var/www/certbot
      - certbot-certs:/etc/letsencrypt

volumes:
  certbot-webroot:
  certbot-certs:
```

Initial certificate:

```bash
docker compose run --rm certbot certonly \
  --webroot -w /var/www/certbot \
  -d example.com --email admin@example.com --agree-tos
```

**Expected:** HTTPS works with valid Let's Encrypt certificate.

**On failure:** Check DNS points to the server. Verify port 80 is open for ACME challenges.

### Step 4: Security Headers

```nginx
server {
    # ... SSL config above ...

    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline';" always;

    # Hide Nginx version
    server_tokens off;
}
```

### Step 5: Rate Limiting

```nginx
http {
    # Define rate limit zones
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=login:10m rate=1r/s;

    server {
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            proxy_pass http://app;
        }

        location /login {
            limit_req zone=login burst=5;
            proxy_pass http://app;
        }
    }
}
```

### Step 6: Load Balancing

```nginx
upstream app {
    least_conn;
    server app1:3000;
    server app2:3000;
    server app3:3000 backup;
}
```

| Method | Directive | Behavior |
|--------|-----------|----------|
| Round robin | (default) | Equal distribution |
| Least connections | `least_conn` | Routes to least busy |
| IP hash | `ip_hash` | Sticky sessions |
| Weighted | `server app:3000 weight=3` | Proportional |

### Step 7: Test Configuration

```bash
# Test config syntax
docker compose exec nginx nginx -t

# Reload without downtime
docker compose exec nginx nginx -s reload

# Check response headers
curl -I https://example.com
```

**Expected:** `nginx -t` reports syntax OK. Headers include security headers.

## Validation

- [ ] `nginx -t` reports configuration is valid
- [ ] HTTP redirects to HTTPS (if SSL enabled)
- [ ] Backend service is reachable through the proxy
- [ ] Security headers present in response
- [ ] Rate limiting triggers on excessive requests
- [ ] SSL Labs test gives A+ rating (if public)

## Common Pitfalls

- **Missing `proxy_set_header Host`**: Backend receives wrong host header, breaking virtual hosts and redirects.
- **`location` order matters**: Nginx uses the most specific match. Exact (`=`) > prefix (`^~`) > regex (`~`) > general prefix.
- **SSL certificate renewal**: Set up a cron or timer to run `certbot renew` and reload Nginx.
- **Large request bodies**: Default `client_max_body_size` is 1MB. Increase for file uploads: `client_max_body_size 50m;`.
- **WebSocket proxying**: Requires additional headers. See `configure-reverse-proxy` for the pattern.

## Related Skills

- `configure-reverse-proxy` - multi-tool proxy patterns including WebSocket and Traefik
- `setup-compose-stack` - compose stack that includes Nginx
- `deploy-searxng` - uses Nginx as frontend for SearXNG
- `configure-ingress-networking` - Kubernetes ingress (NGINX Ingress Controller)
