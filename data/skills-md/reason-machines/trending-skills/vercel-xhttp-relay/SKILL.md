---
name: vercel-xhttp-relay
description: Deploy an XHTTP relay on Vercel Edge Functions to proxy Xray/V2Ray traffic and hide your origin server IP behind *.vercel.app
triggers:
  - set up xhttp relay on vercel
  - proxy xray traffic through vercel
  - hide vps ip with vercel edge
  - deploy v2ray relay vercel
  - xhttp vercel edge function
  - configure xray xhttp inbound
  - vercel xray forwarding setup
  - forward xhttp traffic vercel
---

# Vercel XHTTP Relay

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

A minimal Vercel Edge Function relay that forwards **XHTTP** traffic from Xray/V2Ray clients to a backend Xray server. Vercel's `*.vercel.app` domain acts as a CDN front, hiding your origin VPS IP from censors.

---

## Architecture

```
Client (v2rayN/Hiddify)
  → TLS (SNI=vercel.com) to *.vercel.app
    → Vercel Edge Function (relay, no buffer)
      → HTTP/2 to backend Xray XHTTP inbound
```

**Supported transports:** XHTTP only  
**Not supported on Vercel Edge:** WebSocket, gRPC, TCP, mKCP, QUIC, Reality

---

## Prerequisites

- Linux VPS outside Iran (Ubuntu 22.04/24.04 recommended), min 1 vCPU / 1 GB RAM
- A domain with an A record pointing to your VPS (DNS only, not proxied)
- Vercel account (free Hobby tier works for light personal use)
- Node.js + npm installed locally (for Vercel CLI)
- Xray v1.8.16+ installed on VPS

---

## Step 1 — Install Xray on VPS

```bash
# Update system
apt update && apt upgrade -y
apt install -y curl socat cron ufw

# Install Xray via official script
bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install

# Verify version (must be >= 1.8.16)
xray version

# Generate a UUID for your inbound
xray uuid
# Save this UUID — you'll need it in client and server configs
```

---

## Step 2 — Obtain a TLS Certificate

```bash
# Install acme.sh
curl https://get.acme.sh | sh
source ~/.bashrc   # or re-login

# Issue certificate (replace with your domain)
~/.acme.sh/acme.sh --issue --standalone -d xray.yourdomain.com

# Install certificate to Xray paths
~/.acme.sh/acme.sh --install-cert -d xray.yourdomain.com \
  --key-file  /etc/xray/private.key \
  --fullchain-file /etc/xray/cert.crt \
  --reloadcmd "systemctl restart xray"
```

---

## Step 3 — Xray Server Config (XHTTP Inbound)

`/etc/xray/config.json`:

```json
{
  "log": { "loglevel": "warning" },
  "inbounds": [
    {
      "port": 443,
      "protocol": "vless",
      "settings": {
        "clients": [
          {
            "id": "$YOUR_UUID",
            "flow": ""
          }
        ],
        "decryption": "none"
      },
      "streamSettings": {
        "network": "xhttp",
        "security": "tls",
        "tlsSettings": {
          "certificates": [
            {
              "certificateFile": "/etc/xray/cert.crt",
              "keyFile": "/etc/xray/private.key"
            }
          ]
        },
        "xhttpSettings": {
          "path": "/your-secret-path",
          "mode": "auto"
        }
      }
    }
  ],
  "outbounds": [
    { "protocol": "freedom", "tag": "direct" }
  ]
}
```

```bash
# Apply and start
systemctl restart xray
systemctl enable xray
systemctl status xray
```

---

## Step 4 — The Vercel Edge Relay (api/proxy.js)

The relay function streams request bodies and responses without buffering:

```javascript
// api/proxy.js  — Vercel Edge Function
export const config = { runtime: 'edge' };

const BACKEND = process.env.XRAY_BACKEND_URL;
// e.g. https://xray.yourdomain.com:443/your-secret-path

export default async function handler(req) {
  if (!BACKEND) {
    return new Response('Backend not configured', { status: 500 });
  }

  const url = new URL(req.url);
  const targetUrl = BACKEND + url.pathname.replace(/^\/proxy/, '') + url.search;

  // Forward all headers except host
  const headers = new Headers();
  for (const [key, value] of req.headers.entries()) {
    if (key.toLowerCase() !== 'host') {
      headers.set(key, value);
    }
  }

  try {
    const response = await fetch(targetUrl, {
      method: req.method,
      headers,
      body: req.method !== 'GET' && req.method !== 'HEAD' ? req.body : undefined,
      // @ts-ignore — duplex required for streaming body
      duplex: 'half',
    });

    return new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers: response.headers,
    });
  } catch (err) {
    return new Response(`Relay error: ${err.message}`, { status: 502 });
  }
}
```

---

## Step 5 — vercel.json

```json
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/api/proxy" }
  ]
}
```

---

## Step 6 — package.json (minimal)

```json
{
  "name": "vercel-xhttp-relay",
  "version": "1.0.0",
  "private": true
}
```

---

## Step 7 — Deploy to Vercel

### Via CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy (from project root)
vercel

# Set the backend environment variable
vercel env add XRAY_BACKEND_URL
# Enter: https://xray.yourdomain.com:443/your-secret-path

# Redeploy with env var active
vercel --prod
```

### Via Dashboard (no CLI needed)

1. Push repo to GitHub
2. Go to [vercel.com/new](https://vercel.com/new) → Import repo
3. **Settings → Environment Variables** → add `XRAY_BACKEND_URL`
4. Deploy

Your relay URL will be: `https://your-project.vercel.app`

---

## Step 8 — Client Configuration (v2rayN / Hiddify)

| Field | Value |
|---|---|
| Protocol | VLESS |
| Address | `your-project.vercel.app` |
| Port | `443` |
| UUID | `$YOUR_UUID` (from `xray uuid`) |
| Transport | XHTTP |
| Path | `/your-secret-path` |
| TLS | TLS |
| SNI | `vercel.com` |
| Fingerprint | `chrome` |
| Flow | *(empty)* |

**VLESS link format:**
```
vless://$YOUR_UUID@your-project.vercel.app:443?encryption=none&security=tls&sni=vercel.com&fp=chrome&type=xhttp&path=%2Fyour-secret-path#MyVercelRelay
```

---

## Project File Structure

```
vercel-xhttp-relay/
├── api/
│   └── proxy.js        # Edge Function relay
├── vercel.json         # Rewrite rules
└── package.json
```

---

## Environment Variables

| Variable | Description | Example |
|---|---|---|
| `XRAY_BACKEND_URL` | Full URL to your Xray XHTTP inbound | `https://xray.yourdomain.com:443/secret-path` |

Set via CLI:
```bash
vercel env add XRAY_BACKEND_URL production
vercel env add XRAY_BACKEND_URL preview
```

Or in `vercel.json` for non-secret config (not recommended for backend URLs):
```json
{
  "env": {
    "XRAY_BACKEND_URL": "@xray-backend-url"
  }
}
```

---

## Firewall Setup on VPS

```bash
# Allow SSH, XHTTP port
ufw allow 22/tcp
ufw allow 443/tcp
ufw enable
ufw status
```

---

## Common Patterns

### Multiple Vercel Projects for Failover

Deploy the same relay to multiple Vercel accounts and configure load balance in v2rayN:

```json
// v2rayN outbound balancer (simplified concept)
{
  "tag": "balancer",
  "selector": ["relay1", "relay2", "relay3"]
}
```

### Check Vercel Usage

```bash
vercel billing
# Or monitor at: https://vercel.com/dashboard → Usage tab
```

### Redeploy After Config Change

```bash
vercel --prod
```

### View Logs

```bash
vercel logs your-project.vercel.app --follow
```

---

## Troubleshooting

### 502 Bad Gateway from Vercel

```bash
# Check Xray is running
systemctl status xray

# Check Xray logs
journalctl -u xray -f

# Verify port 443 is open
ufw status
ss -tlnp | grep 443

# Test backend directly (from your local machine, not Iran)
curl -v https://xray.yourdomain.com:443/your-secret-path
```

### DNS Not Resolving

```bash
# Mac/Linux
dig @8.8.8.8 xray.yourdomain.com +short

# Windows PowerShell
Resolve-DnsName xray.yourdomain.com -Server 8.8.8.8 -Type A
```

DNS record must be **DNS only** (grey cloud in Cloudflare), not proxied.

### TLS Certificate Issues

```bash
# Check cert expiry
~/.acme.sh/acme.sh --list

# Renew manually
~/.acme.sh/acme.sh --renew -d xray.yourdomain.com --force

# Verify cert is valid
openssl x509 -in /etc/xray/cert.crt -noout -dates
```

### Xray Config Validation

```bash
xray run -test -c /etc/xray/config.json
# Should output: Configuration OK
```

### Client Can't Connect

- Confirm SNI is set to `vercel.com`, not your project domain
- Confirm transport is `xhttp` (not `ws`, `grpc`, etc.)
- Confirm path matches exactly between server config and client
- Check UUID matches exactly

### Vercel Account Paused (Hobby Bandwidth Exceeded)

Hobby plan counts bandwidth twice (client↔Vercel + Vercel↔origin). To avoid:
- Exclude 4K video and large downloads from the proxy
- Use multiple Hobby accounts with failover
- Upgrade to Pro ($20/month) and set Spend Management limits

---

## Vercel Hobby Plan Limits (Reference)

| Resource | Limit |
|---|---|
| Edge Function invocations | 500,000 / month |
| Fast Origin Transfer | 10 GB / month (counts both directions) |
| Bandwidth (to client) | 100 GB / month |
| Edge Function duration | 30 seconds max per request |

> Monitor at **Vercel Dashboard → Usage**. Vercel sends email alerts at 80% and 100%.

---

## Key Commands Cheatsheet

```bash
# VPS: install/manage Xray
bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install
xray uuid
xray version
xray run -test -c /etc/xray/config.json
systemctl restart xray && systemctl status xray
journalctl -u xray -f

# Local: Vercel CLI
npm i -g vercel
vercel login
vercel                          # deploy preview
vercel --prod                   # deploy production
vercel env add XRAY_BACKEND_URL
vercel logs your-project.vercel.app --follow
vercel billing
```
