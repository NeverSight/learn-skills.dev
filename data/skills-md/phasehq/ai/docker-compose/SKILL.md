---
name: docker-compose
description: |
  Deploy Phase Console with Docker Compose. Triggers: "deploy Phase with Docker Compose",
  "self-host Phase on Docker", "install Phase Console Docker", "Phase Docker Compose setup",
  "set up Phase on my server", "Phase self-hosting Docker", "fix Phase SSL certificate",
  "get a real certificate for Phase", "replace self-signed cert Phase", "Let's Encrypt Phase Docker"
---

# Deploy Phase Console with Docker Compose

This skill deploys Phase Console using Docker Compose and sets up valid Let's Encrypt TLS certificates. The default Phase Docker Compose setup ships with a self-signed certificate — this skill upgrades it to a trusted Let's Encrypt certificate as part of the deployment.

The agent writes config files and runs docker/certbot commands directly. The user only handles values that require their own secrets or credentials.

## Important Principles

- **Autopilot by default.** Write files and run commands without asking for permission at each step. Preview generated files once before writing, then proceed.
- **Never handle secrets directly.** Write `.env` configuration as a shell script (`configure-env.sh`) that auto-generates cryptographic secrets with `openssl rand -hex 32` and marks OAuth credentials with `# EDIT_ME`. Tell the user to fill those in and run the script. Never ask the user to type secret values into the chat.
- **License key is not a secret.** If the user has a Phase Enterprise license key, ask them to paste it directly into the chat.
- **Preserve nginx routing.** All modifications to `nginx/default.conf` must keep the existing routing intact: `/service/` proxies to `backend:8000`, `/` proxies to `frontend:3000`.
- **Reference files for details.** See `refs/docker-compose-deployment.md` for exact file templates and commands, and `refs/troubleshooting.md` for diagnosing issues.

## Workflow

### Phase 1 — Prerequisites

Run these checks automatically without asking:

1. `which docker` — if missing, tell the user to install Docker from https://docs.docker.com/engine/install/ and stop
2. `docker compose version` — if missing or fails, tell the user to install the Docker Compose plugin and stop
3. Check if Phase is already running:
   ```bash
   docker compose ps 2>/dev/null
   ```
   If Phase containers are already up (`phase-nginx`, `phase-frontend`, `phase-backend` etc.), this is an **existing installation** — skip Phase 2 (fresh install) and go straight to Phase 3 (Let's Encrypt setup).

Once checks pass, proceed without waiting for the user.

### Phase 2 — Configuration Questions (fresh install only)

Ask all questions in a single message:

1. **Domain name** — The FQDN where Phase will run (e.g., `phase.example.com`). Required — must be a real domain pointing to this server for Let's Encrypt to work.
2. **Email address** — For Let's Encrypt certificate expiry notifications and the `.env` contact address.
3. **SSO provider(s)** — Which identity providers to enable (comma-separated):
   - `google`, `github`, `gitlab`, `authentik`
   - `google-oidc`, `jumpcloud-oidc`, `entra-id-oidc`, `okta-oidc`
   - `github-enterprise`
4. **Phase Enterprise license** — Do they have a license key? If yes, ask them to paste it here.

Once answered, proceed to Phase 3.

### Phase 3 — Let's Encrypt Setup Questions

Ask only what's needed (some may already be known from Phase 2):

1. **Domain** — if not already collected
2. **Email for Let's Encrypt** — if not already collected
3. **Working directory** — where is the `docker-compose.yml` located? Default: current directory. The agent needs this to run `docker compose` commands with the right context.

### Phase 4 — File Setup (fresh install only)

#### 4a. Download base configs

Run automatically:

```bash
curl -o docker-compose.yml https://raw.githubusercontent.com/phasehq/console/main/docker-compose.yml
curl -o .env.example https://raw.githubusercontent.com/phasehq/console/main/.env.example
mkdir -p nginx
curl -o nginx/default.conf https://raw.githubusercontent.com/phasehq/console/main/nginx/default.conf
curl -o nginx/Dockerfile https://raw.githubusercontent.com/phasehq/console/main/nginx/Dockerfile
```

#### 4b. Write configure-env.sh

Write `configure-env.sh` — a script the user edits and runs to produce a valid `.env`. Auto-generate all cryptographic secrets. Mark OAuth credentials with `# EDIT_ME`. See references for the full template.

Write the file and `chmod +x configure-env.sh`. Tell the user: "Edit the `# EDIT_ME` lines in `configure-env.sh` then run it to generate your `.env`. Let me know when it's done."

Wait for confirmation before proceeding.

### Phase 5 — Let's Encrypt Certificate Setup

This is the core of the skill and applies to both fresh installs and existing deployments.

#### 5a. Verify DNS

Before doing anything with certificates, verify the domain resolves to this server:

```bash
dig @8.8.8.8 {domain} +short
dig @1.1.1.1 {domain} +short
dig @9.9.9.9 {domain} +short
dig @208.67.222.222 {domain} +short
```

All should return the server's public IP. If any are inconsistent or NXDOMAIN, tell the user to fix DNS first and wait. Do not proceed until at least 3 of 4 resolvers agree — Let's Encrypt will fail ACME challenges on an unresolved domain.

If the user doesn't know their server's public IP:
```bash
curl -s https://api.ipify.org
```

#### 5b. Patch docker-compose.yml

Add the certbot service and shared volumes to `docker-compose.yml`, and add volume mounts to the nginx service. See references for the exact patch. Run automatically — show a diff-style preview of what's changing before applying.

Key changes:
- Add `certbot-webroot` and `certbot-certs` named volumes
- Mount both into the nginx service
- Add the `certbot` service definition

#### 5c. Patch nginx/default.conf

Replace the nginx config with the Let's Encrypt-ready version from references. This version:
- **HTTP server block** (port 80): serves ACME challenges at `/.well-known/acme-challenge/`, redirects everything else to HTTPS
- **HTTPS server block** (port 443): initially still uses the self-signed cert baked into the nginx image (`/etc/nginx/ssl/nginx.crt`); preserves all existing routing (`/service/` → backend, `/` → frontend)
- Mounts the certbot webroot volume for challenge file serving

Show the full new config as a preview, then write it.

#### 5d. Apply and restart nginx

```bash
docker compose up -d --build nginx
```

The `--build` flag is needed because the nginx Dockerfile generates the self-signed cert at build time. After this, nginx is running with:
- Port 80: serves ACME challenges + redirects to HTTPS
- Port 443: still using self-signed cert (temporary)

#### 5e. Get the Let's Encrypt certificate

Run automatically:

```bash
docker compose run --rm certbot certonly \
  --webroot \
  --webroot-path=/var/www/certbot \
  --email {email} \
  --agree-tos \
  --no-eff-email \
  -d {domain}
```

If this fails, consult `refs/troubleshooting.md` for ACME challenge errors.

#### 5f. Switch nginx to Let's Encrypt cert

Update the two `ssl_certificate` lines in `nginx/default.conf` to point to the Let's Encrypt cert paths:

```
ssl_certificate /etc/letsencrypt/live/{domain}/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/{domain}/privkey.pem;
```

Then reload nginx (no restart needed — reload picks up the new cert without dropping connections):

```bash
docker compose exec nginx nginx -s reload
```

#### 5g. Verify

```bash
curl -sv https://{domain}/api/health 2>&1 | grep -E "SSL|issuer|subject|expire"
```

Confirm the issuer is `Let's Encrypt` and the cert is valid.

#### 5h. Set up auto-renewal

Write a cron job that renews the cert twice daily (Let's Encrypt certs expire in 90 days; certbot only actually renews when within 30 days):

```bash
(crontab -l 2>/dev/null; echo "0 0,12 * * * cd {working_dir} && docker compose run --rm certbot renew --quiet && docker compose exec nginx nginx -s reload") | crontab -
```

Show the user the installed cron entry:
```bash
crontab -l
```

Tell the user: "Your Phase Console is live at `https://{domain}` with a trusted Let's Encrypt certificate. It will auto-renew every 12 hours when within 30 days of expiry."

### Phase 6 — Verification

Run automatically:

```bash
docker compose ps
```

All containers should show `running`. Check health endpoints:

```bash
curl -s https://{domain}/api/health
curl -s https://{domain}/service/health/
```

Both should return a 200 response. If any container is unhealthy, consult `refs/troubleshooting.md`.

## Upgrading Phase

```bash
docker compose pull
docker compose up -d
```

## Uninstalling

```bash
docker compose down -v   # -v removes volumes including the database
```

Remove certbot cron job:
```bash
crontab -l | grep -v certbot | crontab -
```
