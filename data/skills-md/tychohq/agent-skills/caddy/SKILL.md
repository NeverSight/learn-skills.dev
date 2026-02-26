---
name: caddy
slug: caddy-reverse-proxy
version: 1.0.0
description: Add, manage, and troubleshoot Caddy reverse proxy routes for local apps via wildcard subdomains.
compatibility: macOS (LaunchDaemon) or Linux (systemd). Requires Caddy, Tailscale, Vercel DNS account.
---

# Caddy — Wildcard Reverse Proxy for Local Apps

Routes `*.YOUR_DOMAIN` subdomains to local services over HTTPS via Caddy reverse proxy with automatic Let's Encrypt certificates. Designed for Tailscale-only access (no public exposure).

> **DNS provider:** This skill uses **Vercel DNS** for DNS-01 ACME challenges. If you use a different DNS provider, swap the `caddy-dns/vercel` plugin and TLS snippet for your provider's equivalent (see [caddy-dns](https://github.com/caddy-dns)).

## Add a New App

1. **Create a background service** (LaunchAgent on macOS, systemd on Linux) — see `reference.md` for templates
2. **Add to Caddyfile** (`~/.config/caddy/Caddyfile`):
   ```caddy
   appname.YOUR_DOMAIN {
       import vercel_tls
       reverse_proxy localhost:31XX
   }
   ```
   Also add a `<li>` entry in the dashboard HTML block at the top.
3. **Reload Caddy:**
   ```bash
   ~/.local/bin/caddy reload --config ~/.config/caddy/Caddyfile --address localhost:2019
   ```
   TLS cert provisioning takes 30–60 seconds (DNS-01 challenge).
4. **If it connects to OpenClaw Gateway** — see `OPENCLAW.md` in this folder for gateway-specific config.

## Quick Dev Servers

Companion skill: [dev-serve](https://clawhub.com/skills/dev-serve) — one-command dev server + Caddy routing.

```bash
dev-serve up ~/projects/myapp        # → https://myapp.YOUR_DOMAIN
dev-serve down myapp
dev-serve ls
```

## Reload / Restart

```bash
# Reload config (no restart, no sudo)
~/.local/bin/caddy reload --config ~/.config/caddy/Caddyfile --address localhost:2019

# Full restart
# macOS:
sudo launchctl unload /Library/LaunchDaemons/com.caddyserver.caddy.plist
sudo launchctl load /Library/LaunchDaemons/com.caddyserver.caddy.plist
# Linux:
systemctl --user restart caddy
```

## Troubleshoot

- **Cert not issuing:** `tail -50 /var/log/caddy-error.log | grep -i error` — likely expired Vercel API token
- **DNS not resolving:** `dig +short appname.YOUR_DOMAIN` — should return your Tailscale IP
- **TLS error (curl exit 35):** Cert hasn't provisioned yet, wait 30-60s

For full reference (example apps, key files, build instructions): see `reference.md`.
For OpenClaw gateway integration: see `OPENCLAW.md`.

