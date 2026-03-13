---
name: d6e-setup
description: Sets up a D6E platform instance using Docker Compose with an external PostgreSQL database. Use when deploying D6E, configuring environment variables, applying database schema, setting up HTTPS with Caddy, or troubleshooting D6E deployment issues.
---

# D6E Setup

## Overview

This skill guides the setup of a [D6E](https://github.com/d6e-ai/d6e) platform instance. D6E is an AI-native Business Intelligence platform that enables natural language data analysis. The deployment uses Docker Compose with pre-built images from GitHub Container Registry, an external PostgreSQL database, and Caddy for automatic HTTPS.

## When to Use

Apply this skill when users request:

- "Set up D6E on my server"
- "Deploy a D6E instance"
- "Configure D6E with my database"
- "Set up HTTPS for D6E"
- "I need to get D6E running"
- "Help me configure the D6E .env file"

## Prerequisites

- A Linux server (Ubuntu recommended) with Docker and Docker Compose installed
- An external PostgreSQL database (with pgvector extension recommended)
- A domain name pointed to the server (for HTTPS)
- d6e-auth credentials (client ID and secret) from the D6E administrator

### Installing Docker (Ubuntu)

```bash
sudo apt update
sudo apt install -y build-essential ca-certificates curl

sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

sudo usermod -aG docker $USER
newgrp docker
```

## Setup Steps

### Step 1: Clone the Repository

```bash
git clone https://github.com/d6e-ai/d6e-setup.git
cd d6e-setup
```

### Step 2: Create the .env File

```bash
cp .env.example .env
```

Edit `.env` and configure the following variables. See [reference.md](reference.md) for the full list of environment variables.

#### Required: Database Connection

Set `DATABASE_URL` to your external PostgreSQL connection string:

```
DATABASE_URL=postgres://username:password@your-db-host:5432/d6e
```

The database must have the pgvector extension available for embedding/similarity search features. If pgvector is not available, D6E will still work but vector-related features will be disabled.

#### Required: Container Token Secret

Generate a secure random string for Docker container authentication:

```bash
openssl rand -base64 32
```

Set the output as `D6E_CONTAINER_TOKEN_SECRET` in `.env`:

```
D6E_CONTAINER_TOKEN_SECRET=<generated-value>
```

#### Required: d6e-auth Configuration

D6E uses an external authentication service called d6e-auth. You need to obtain credentials from the D6E administrator.

**How to get credentials:**

1. Decide your D6E instance's public URL (e.g. `https://example.d6e.ai`)
2. Contact the d6e-auth administrator and provide this URL
3. The administrator will run the client registration script on the d6e-auth server and provide you with `D6E_AUTH_CLIENT_ID` and `D6E_AUTH_CLIENT_SECRET`

Set these values in `.env`:

```
D6E_AUTH_URL=https://www.d6e.ai
D6E_AUTH_CLIENT_ID=d6e_xxxxxxxxxxxx
D6E_AUTH_CLIENT_SECRET=d6es_xxxxxxxxxxxx
D6E_AUTH_JWT_ISSUER=d6e-auth
```

> **Note:** `D6E_AUTH_URL` is already set to `https://www.d6e.ai` in `.env.example`. You only need to set `D6E_AUTH_CLIENT_ID` and `D6E_AUTH_CLIENT_SECRET` which are obtained from the administrator.

#### Required: Origin URL

Set `ORIGIN` to your D6E instance's public URL. This is used by SvelteKit and for OAuth redirect URI validation:

```
ORIGIN=https://example.d6e.ai
```

#### Optional: LLM API Keys

Set these only if you need AI features:

```
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...
```

For local LLM servers (Ollama, LM Studio), the default Docker host URLs are pre-configured.

#### Optional: Embedding Configuration

If using similarity search features (requires `GOOGLE_API_KEY`):

```
EMBEDDING_MODEL=gemini-embedding-001
EMBEDDING_DIMENSIONS=768
```

### Step 3: Apply Database Schema

Connect to your external database and apply the seed SQL:

```bash
psql $DATABASE_URL < packages/migration/seed.sql
```

If `psql` is not installed locally, you can use Docker:

```bash
docker run --rm -i postgres:18 psql "$DATABASE_URL" < packages/migration/seed.sql
```

#### Apply Seed Data (Fonts and Libraries)

These scripts populate the `stf_library` table with fonts for PDF generation and JavaScript libraries for STF execution.

```bash
cd packages/migration
npm install pg
DATABASE_URL="postgres://username:password@your-db-host:5432/d6e" node scripts/seed_fonts.mjs
DATABASE_URL="postgres://username:password@your-db-host:5432/d6e" node scripts/seed_libraries.mjs
cd ../..
```

> **Note:** These scripts require Node.js to be installed on the machine running them.

### Step 4: Create the Caddyfile (HTTPS)

The `compose.yml` includes a Caddy reverse proxy that handles automatic HTTPS via Let's Encrypt. Create a `Caddyfile` in the project root:

```bash
cat > Caddyfile << 'EOF'
example.d6e.ai {
    reverse_proxy frontend:3000
}
EOF
```

Replace `example.d6e.ai` with your actual domain.

**How Caddy HTTPS works:**

- Caddy automatically obtains and renews TLS certificates from Let's Encrypt
- Ports 80 and 443 must be accessible from the internet
- The domain must have a DNS A record pointing to your server's public IP
- No manual certificate management is needed

**Multiple subdomains (optional):**

If you want to expose the API or MCP endpoints on separate subdomains:

```
example.d6e.ai {
    reverse_proxy frontend:3000
}

api.example.d6e.ai {
    reverse_proxy api:8080
}

mcp.example.d6e.ai {
    reverse_proxy mcp:8081
}
```

### Step 5: Start the Services

```bash
docker compose up -d
```

This starts the following services:

| Service    | Description                   | Default Port |
| ---------- | ----------------------------- | ------------ |
| `api`      | D6E API server (Rust/Axum)    | 8080         |
| `mcp`      | MCP server                    | 8081         |
| `frontend` | SvelteKit frontend            | 3000         |
| `caddy`    | Reverse proxy with auto HTTPS | 80, 443      |

### Step 6: Verify the Deployment

1. **Check all containers are running:**

   ```bash
   docker compose ps
   ```

   All services should show `running` status.

2. **Check logs for errors:**

   ```bash
   docker compose logs -f
   ```

3. **Access the application:**

   Open `https://your-domain.example.com` in a browser. You should see the D6E login page.

4. **Verify API health:**

   ```bash
   curl -s https://your-domain.example.com/api/v1/health
   ```

## Architecture

```
Internet
    │
    ▼
┌─────────┐    ┌──────────┐    ┌─────┐
│  Caddy   │───▶│ Frontend │───▶│ API │
│ (HTTPS)  │    │ (SSR)    │    │     │
└─────────┘    └──────────┘    └──┬──┘
   :80,:443       :3000          :8080
                    │              │
                    ▼              ▼
                ┌──────┐    ┌──────────┐
                │ MCP  │    │ External │
                │      │    │ Postgres │
                └──────┘    └──────────┘
                 :8081
```

- **Caddy**: Reverse proxy with automatic HTTPS (Let's Encrypt)
- **Frontend**: SvelteKit application (SSR), connects to API and MCP
- **API**: Rust/Axum REST + GraphQL server, connects to PostgreSQL
- **MCP**: Model Context Protocol server, proxies to API

## Updating

To update D6E to the latest version:

```bash
docker compose pull
docker compose up -d
```

If the database schema has changed, re-apply the seed SQL:

```bash
psql $DATABASE_URL < packages/migration/seed.sql
```

## Troubleshooting

### Containers fail to start

**Check logs:**

```bash
docker compose logs api
docker compose logs frontend
```

**Common causes:**

- `DATABASE_URL is required` error: Ensure `DATABASE_URL` is set in `.env`
- `D6E_CONTAINER_TOKEN_SECRET is required` error: Ensure `D6E_CONTAINER_TOKEN_SECRET` is set in `.env`
- Database connection refused: Verify the external database is accessible from the server

### HTTPS certificate not obtained

- Ensure ports 80 and 443 are open in your firewall
- Ensure the domain's DNS A record points to your server's IP
- Check Caddy logs: `docker compose logs caddy`

### Cannot log in

- Verify `D6E_AUTH_URL`, `D6E_AUTH_CLIENT_ID`, and `D6E_AUTH_CLIENT_SECRET` are correctly set
- Ensure the d6e-auth server is accessible from your D6E instance
- Confirm that `ORIGIN` matches your actual public URL (including `https://`)
- Contact the d6e-auth administrator to verify your client registration

### Docker STFs not executing

- Ensure `/var/run/docker.sock` is accessible (it is mounted read-only in `compose.yml`)
- Verify `D6E_CONTAINER_TOKEN_SECRET` is set

### Embedding / Vector features not working

- Ensure the PostgreSQL database has the pgvector extension installed
- Verify `GOOGLE_API_KEY` is set if using Google embedding models
- Check that `EMBEDDING_MODEL` and `EMBEDDING_DIMENSIONS` are configured

## Additional Resources

- [D6E Setup Repository](https://github.com/d6e-ai/d6e-setup) - Setup files cloned in Step 1
- [D6E Platform](https://github.com/d6e-ai/d6e) - Main D6E repository
- [D6E Docker STF Skills](https://github.com/d6e-ai/d6e-docker-stf-skills) - Skills for creating custom Docker STFs
- Environment variables reference: [reference.md](reference.md)
- Quick start guide: [../docs/QUICKSTART.md](../docs/QUICKSTART.md)
