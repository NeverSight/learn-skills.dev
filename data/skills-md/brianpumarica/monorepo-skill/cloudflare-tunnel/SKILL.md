---
name: cloudflare-tunnel
description: Automated setup, configuration, and production runbook for Cloudflare Tunnels (cloudflared) inside Docker Compose. Use whenever exposing local backends and databases running on Raspberry Pi 5 or home servers to the internet with HTTPS, configuring Zero Trust access policies, setting up public hostnames, handling CORS, and establishing secure remote database access without opening router ports or exposing public IPs.
---

# Cloudflare Tunnel Production Standard & Runbook

This skill provides the standard configuration and operational runbook for exposing containerized backend APIs and databases running on home servers (e.g., Raspberry Pi 5) or VPS using **Cloudflare Tunnels (`cloudflared`)** with Zero Trust security.

---

## 1. Architecture Overview

```
 [Client / Vercel Web] ──( HTTPS Request )──> [Cloudflare Edge]
                                                    │
                                         (Encrypted Tunnel / QUIC)
                                                    ▼
                                     [Raspberry Pi 5 / Server]
                                     ┌────────────────────────────────┐
                                     │ Docker Network: `app-net`      │
                                     │                                │
                                     │ ┌───────────────┐              │
                                     │ │  cloudflared  │ (Tunnel Svc) │
                                     │ └───────┬───────┘              │
                                     │         │ http://backend:3004  │
                                     │         ▼                      │
                                     │ ┌───────────────┐              │
                                     │ │  backend-prod │ (Port 3004)  │
                                     │ └───────┬───────┘              │
                                     │         │ postgres:5432        │
                                     │         ▼                      │
                                     │ ┌───────────────┐              │
                                     │ │   database    │ (Port 5432)  │
                                     │ └───────────────┘              │
                                     └────────────────────────────────┘
```

- **Zero Port Forwarding**: No need to open ports 80/443 on your home router.
- **Dynamic IP Immune**: Works reliably even if your ISP changes your public IP.
- **SSL Auto-Termination**: Cloudflare manages SSL certificates automatically.
- **DDoS & WAF Protection**: Requests are filtered at Cloudflare's edge before hitting the Pi.

---

## 2. Docker Compose Integration (`docker-compose.prod.yml`)

Add the `tunnel` service directly to your production Compose file so it starts automatically alongside your backend and database:

```yaml
services:
  database:
    image: pgvector/pgvector:pg16
    container_name: ${PROJECT_NAME:-app}-db
    restart: unless-stopped
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-postgres}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:?Required}
      POSTGRES_DB: ${POSTGRES_DB:-app}
    volumes:
      - db_data:/var/lib/postgresql/data
    networks:
      - app-net
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-postgres} -d ${POSTGRES_DB:-app}"]
      interval: 5s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: .
      dockerfile: apps/api/Dockerfile
      target: production
    container_name: ${PROJECT_NAME:-app}-api
    restart: unless-stopped
    environment:
      NODE_ENV: production
      PORT: 3004
      DATABASE_URL: postgres://${POSTGRES_USER:-postgres}:${POSTGRES_PASSWORD}@database:5432/${POSTGRES_DB:-app}
      CORS_ALLOWED_ORIGINS: ${CORS_ALLOWED_ORIGINS:-https://tudominio.com,https://tu-app.vercel.app}
    depends_on:
      database:
        condition: service_healthy
    networks:
      - app-net

  tunnel:
    image: cloudflare/cloudflared:latest
    container_name: ${PROJECT_NAME:-app}-tunnel
    restart: unless-stopped
    command: tunnel run --token ${CLOUDFLARE_TUNNEL_TOKEN}
    environment:
      - TUNNEL_METRICS=0.0.0.0:2000
    depends_on:
      - backend
    networks:
      - app-net

networks:
  app-net:
    driver: bridge

volumes:
  db_data:
```

---

## 3. Step-by-Step Setup Guide

### Step 1: Create Tunnel in Cloudflare Zero Trust Dashboard
1. Go to **Cloudflare Zero Trust Dashboard** > **Networks** > **Tunnels**.
2. Click **Create a Tunnel** > Select **Cloudflared**.
3. Name your tunnel (e.g., `raspi5-prod-api`).
4. Copy the **Tunnel Token** string from the installation command (it starts with `ey...`).
5. Add it to your production `.env` file on the Raspberry Pi:
   ```env
   CLOUDFLARE_TUNNEL_TOKEN=eyJhIjoi...
   ```

### Step 2: Configure Public Hostname Routing
In the Cloudflare Dashboard under your tunnel settings > **Public Hostnames**:

| Field | Value | Notes |
| :--- | :--- | :--- |
| **Public Hostname** | `api.tudominio.com` | Your registered subdomain |
| **Service Type** | `HTTP` | Internal protocol |
| **URL** | `backend:3004` | Resolves directly via Docker bridge network `app-net` |

> [!TIP]
> Use the container service name `backend:3004` as the URL, **not** `localhost:3004`, because `cloudflared` runs inside its own container on the same Docker bridge network.

### Step 3: Zero Trust Access Protection for Admin / Docs (Optional)
To protect Swagger docs (`/docs` or `/api/docs`) or administrative endpoints with OAuth login:
1. Go to **Zero Trust** > **Access** > **Applications**.
2. Click **Add an Application** > **Self-hosted**.
3. Application Domain: `api.tudominio.com/docs*` (or `/api/docs*`).
4. Add Policy: Rule type **Allow** -> Include **Emails** (your personal email).
5. Now requests to `/docs` require an email OTP or Google/GitHub login, while public API routes remain accessible.

---

## 4. Environment Variables Reference

Add these keys to your `.env.example`:

```env
# --- Cloudflare Tunnel ---
CLOUDFLARE_TUNNEL_TOKEN=your_cloudflare_tunnel_token_here

# --- Backend CORS Config ---
CORS_ALLOWED_ORIGINS=https://tudominio.com,https://tu-proyecto.vercel.app,http://localhost:8084
```

---

## 5. Exposing Database for Remote Development (Secure TCP)

If you need direct database connection (e.g. for DBeaver or Prisma Studio) from your local computer to the Raspberry Pi:

### Step 1: Add DB Public Hostname in Tunnel Dashboard
- Hostname: `db.tudominio.com`
- Service: `TCP://database:5432`

### Step 2: Connect from Local Machine
Run `cloudflared` on your local PC:
```bash
cloudflared access tcp --hostname db.tudominio.com --url localhost:54322
```
Now connect your local database client or Prisma to `localhost:54322`.

---

## 6. Verification and Troubleshooting

### Check Tunnel Status
```bash
docker compose -f docker-compose.prod.yml logs -f tunnel
```
Look for: `INF Connection ... registered connIndex=0 ... ip=... location=...`

### Verify Internal DNS Resolution
```bash
docker compose -f docker-compose.prod.yml exec tunnel ping -c 2 backend
```

### Common Issues:
- **Error 502 Bad Gateway**: Ensure `backend` is running and listening on `0.0.0.0:3004` (not `127.0.0.1:3004`).
- **CORS Blocked**: Ensure the backend includes the frontend domain in `CORS_ALLOWED_ORIGINS` and Cloudflare SSL mode is set to **Full** or **Full (Strict)**.
- **SSL Handshake Failed / `SEC_E_ILLEGAL_MESSAGE`**: Ocurre al usar subdominios anidados con dos puntos (ej. `api.proyecto.dominio.com`). El certificado gratuito Universal SSL de Cloudflare solo cubre `*.dominio.com` (un solo nivel de comodín). **Usar siempre guion**: `api-proyecto.dominio.com`, nunca dos puntos.
- **Terminal Web se desconecta al reiniciar**: Si la terminal web corre en el mismo túnel (`terminal.dominio.com`), `sudo systemctl restart cloudflared` corta el WebSocket momentáneamente ("Press enter to reconnect"): basta con presionar Enter tras 2 segundos para reconectar.

---

## 7. Deep-Dive Reference Guides

- [Cloudflare Zero Trust Access & Advanced Ingress Runbook](./references/zero-trust-access-and-ingress.md) (Service Tokens for CI/CD, multi-service routing, and TCP proxying).
