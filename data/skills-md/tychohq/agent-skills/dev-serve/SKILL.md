---
name: dev-serve
version: 1.0.0
description: Start and manage tmux-backed dev servers exposed through Caddy at wildcard subdomains.
---

# dev-serve — One-Command Dev Server Hosting

Start a dev server in a tmux session and expose it via Caddy at `<project>.YOUR_DOMAIN`. One command up, one command down.

## Setup

1. **Install the script:**
   ```bash
   cp scripts/dev-serve.sh ~/.local/bin/dev-serve
   chmod +x ~/.local/bin/dev-serve
   ```

2. **Set your domain** (one of):
   - Export `DEV_SERVE_DOMAIN` in your shell profile
   - Or edit the `DOMAIN` variable in the script

3. **Requirements:**
   - Caddy running with wildcard DNS + TLS (see [caddy](https://clawhub.com/skills/caddy) skill)
   - `tmux`, `jq`, `curl`
   - Caddy admin API on `localhost:2019`

## CLI

```bash
dev-serve up <repo-path> [port]      # Start dev server + add Caddy route
dev-serve down <name>                # Stop dev server + remove Caddy route
dev-serve ls                         # List active dev servers
dev-serve restart <name>             # Restart dev server (keep Caddy route)
```

## How It Works

1. Derives subdomain from the repo folder name (`~/projects/myapp` → `myapp.YOUR_DOMAIN`)
2. Detects the dev command from `package.json` `scripts.dev` (supports vite, next, nuxt, sveltekit)
3. Auto-patches Vite `allowedHosts` if a vite config file exists
4. Starts the dev server in a tmux session named `dev-<name>` with `--host 0.0.0.0 --port <port>`
5. Adds a Caddy route + dashboard link to the Caddyfile
6. Reloads Caddy via admin API (no sudo, no restart)
7. Verifies end-to-end: waits for the dev server to listen, then polls HTTPS until 2xx/3xx (up to 90s)

## Examples

```bash
# Start with auto-assigned port (starts at 5200, skips used ports)
dev-serve up ~/projects/myapp
# → https://myapp.YOUR_DOMAIN

# Explicit port
dev-serve up ~/projects/myapp 5200

# Override dev command
DEV_CMD="bun dev" dev-serve up ~/projects/myapp 5300

# Stop and clean up
dev-serve down myapp

# List what's running
dev-serve ls
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `DEV_SERVE_DOMAIN` | *(must be set)* | Your wildcard domain (e.g. `mini.example.com`) |
| `DEV_SERVE_STATE_DIR` | `~/.config/dev-serve` | Where state JSON is stored |
| `CADDYFILE` | `~/.config/caddy/Caddyfile` | Path to your Caddyfile |
| `CADDY_ADMIN` | `http://localhost:2019` | Caddy admin API address |
| `DEV_CMD` | *(auto-detected)* | Override the dev server command |

## Port Convention

- **Permanent services:** 3100 range (managed in Caddyfile directly)
- **Dev servers:** 5200+ (managed by dev-serve, auto-assigned)

## Vite `allowedHosts`

Vite blocks requests from unrecognized hostnames. `dev-serve up` automatically patches `vite.config.ts` (or `.js`/`.mts`/`.mjs`) to add the subdomain. If auto-patching fails, it prints the manual fix.

## Architecture

```
Browser (Tailscale / LAN / etc.)
  → DNS: *.YOUR_DOMAIN → your server IP
    → Caddy (HTTPS with auto certs)
      → reverse_proxy localhost:<port>
        → Dev server (in tmux session)
```

## Companion Skills

- **[caddy](https://clawhub.com/skills/caddy)** — Required. Sets up the Caddy reverse proxy with wildcard TLS.

## Troubleshooting

**Dev server not starting:**
```bash
tmux attach -t dev-<name>    # see what happened
```

**Cert not provisioning (curl exit 35):**
Wait 30-60s for DNS-01 challenge. Check `tail -20 /var/log/caddy-error.log`.

**Caddy reload failed:**
```bash
caddy reload --config ~/.config/caddy/Caddyfile --address localhost:2019
```

**403 from Vite:**
The subdomain wasn't added to `allowedHosts`. Add it manually to your `vite.config.ts`:
```ts
server: { allowedHosts: ['myapp.YOUR_DOMAIN'] }
```
