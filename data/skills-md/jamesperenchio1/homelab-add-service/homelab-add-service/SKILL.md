---
name: homelab-add-service
description: Add a new service to my homelab — Docker/LXC deployment, Caddy reverse proxy, Authentik SSO, and Cloudflare DNS
---

# homelab-add-service

Onboard a new service to my homelab infrastructure. Covers deployment, reverse proxy routing, SSO authentication, and DNS.

## When to use

When I want to add a new self-hosted service to my homelab — whether it's a Docker container, an LXC container, or a native service.

## Architecture

```
Internet → Cloudflare (TLS termination) → cloudflared tunnel → Caddy (port 80) → backend service
```

- **Host:** Ubuntu server at `192.168.1.102`
- **Reverse proxy:** Caddy at `/etc/caddy/Caddyfile`
- **SSO:** Authentik at `localhost:9000` (compose at `/opt/authentik/docker-compose.yml`)
- **Tunnel:** Cloudflare Tunnel via `cloudflared` (systemd service)
- **LXC:** Managed by LXD (snap), containers on `10.55.205.x` subnet

## Instructions

### 1. Gather requirements

Ask me:
- **Service name** and what it does
- **Subdomain** (e.g., `myapp.gingerbrosshop.com`)
- **Deployment method:** Docker on host or LXC container
- **Auth method:** Authentik forward auth, native OIDC, or no auth
- **Storage needs:** Does it need access to `/mnt/hdd` or `/mnt/nvme-usb`?
- **Port:** What port the service listens on

### 2. Deploy the service

**If Docker on host:**
- Create a compose file at `/opt/<service-name>/docker-compose.yml`
- Use a dedicated directory under `/opt/` for each service
- Bind to `127.0.0.1:<port>` unless it needs LAN access
- Add volume mounts for persistent data and any shared storage
- Start with `cd /opt/<service-name> && sudo docker compose up -d`

**If LXC container:**
- Launch with `lxc launch ubuntu:24.04 <name>` (or appropriate image)
- Configure with `lxc exec <name> -- bash`
- If it needs host storage, add a disk device: `lxc config device add <name> <label> disk source=/mnt/... path=/mnt/...`
- Note the container IP from `lxc list` for Caddy config

### 3. Configure Caddy reverse proxy

Edit `/etc/caddy/Caddyfile` and add a new site block.

**Critical rules:**
- Always hardcode `header_up X-Forwarded-Proto https` — never use `{http.request.scheme}` (Cloudflare terminates TLS, so scheme is always `http` at Caddy)
- For Docker services on host, proxy to `localhost:<port>`
- For LXC services, proxy to `<container-ip>:<port>`

**With Authentik forward auth:**
```caddy
<subdomain>.gingerbrosshop.com {
    forward_auth localhost:9000 {
        uri /outpost.goauthentik.io/auth/caddy
        copy_headers X-Authentik-Username X-Authentik-Groups X-Authentik-Entitlements X-Authentik-Email X-Authentik-Name X-Authentik-Uid X-Authentik-Jwt X-Authentik-Meta-Jwks X-Authentik-Meta-Outpost X-Authentik-Meta-Provider X-Authentik-Meta-App X-Authentik-Meta-Version
        trusted_proxies private_ranges
    }
    reverse_proxy <backend-address> {
        header_up X-Forwarded-Proto https
    }
}
```

**Without auth (or native OIDC only):**
```caddy
<subdomain>.gingerbrosshop.com {
    reverse_proxy <backend-address> {
        header_up X-Forwarded-Proto https
    }
}
```

**If the service uses WebSockets**, use a bare `reverse_proxy` directive (forward auth + WebSockets works fine with this pattern).

Apply with: `sudo systemctl reload caddy`

### 4. Configure Authentik SSO (if needed)

**For forward auth:**
1. Create an Application in Authentik (via API or UI) with slug matching the subdomain
2. Create a Proxy Provider with:
   - `external_host`: `https://<subdomain>.gingerbrosshop.com`
   - `mode`: `forward_single`
3. Link the provider to the application
4. Restart Authentik server so the embedded outpost picks up the new config:
   ```bash
   cd /opt/authentik && sudo docker compose restart server
   ```

**For native OIDC:**
1. Create an OAuth2/OpenID Provider in Authentik with:
   - `redirect_uris`: must be a list of objects `[{"matching_mode":"strict","url":"https://<subdomain>.gingerbrosshop.com/callback"}]` — NOT plain strings
   - Note the client ID and client secret
2. Create an Application linked to the provider
3. Configure the service with the OIDC credentials
4. Restart Authentik server: `cd /opt/authentik && sudo docker compose restart server`

### 5. Configure Cloudflare DNS and Tunnel

- Add a **CNAME** record in Cloudflare DNS for `<subdomain>` pointing to the tunnel hostname
- Or add a public hostname entry in the Cloudflare Tunnel config routing `<subdomain>.gingerbrosshop.com` → `http://192.168.1.102:80`
- **Every subdomain must route to Caddy on port 80** — never route directly to a backend service (bypasses auth)

### 6. Verify

1. Check Caddy config is valid: `caddy validate --config /etc/caddy/Caddyfile`
2. Check the service is reachable locally: `curl -s -o /dev/null -w "%{http_code}" http://<backend-address>/`
3. Check the public URL works: `curl -s -o /dev/null -w "%{http_code}" -L https://<subdomain>.gingerbrosshop.com/`
4. If using forward auth, verify redirect to Authentik login page
5. Check logs if something is wrong:
   - Caddy: `journalctl -u caddy -f`
   - Authentik: `cd /opt/authentik && sudo docker compose logs server --tail=50 -f`
   - Service: `sudo docker logs <name> --tail=50 -f` or `lxc exec <name> -- journalctl -f`

## Common gotchas

- `docker restart docker` restarts ALL containers — use `docker compose restart` or `docker restart <name>` instead
- After Authentik API/config changes, always restart the server for the embedded outpost to pick up changes
- Authentik is bound to `192.168.1.102:9000`, not `127.0.0.1:9000`
- LXC container name for Jellyfin is `dashboard`, not `jellyfin`
- Docker DNS can break after systemd-resolved restart — fix with `docker compose up -d --force-recreate <service>`
