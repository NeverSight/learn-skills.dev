---
name: gooserelayvpn-socks5-tunnel
description: Expert knowledge for building, configuring, and operating GooseRelayVPN — a SOCKS5 VPN that tunnels raw TCP through Google Apps Script to a VPS exit server using AES-256-GCM encryption and domain fronting.
triggers:
  - set up GooseRelayVPN
  - tunnel traffic through Google Apps Script
  - configure SOCKS5 VPN with domain fronting
  - goose-client goose-server setup
  - domain fronted VPN tunnel
  - AES-GCM encrypted TCP proxy
  - bypass firewall with Google Apps Script tunnel
  - GooseRelayVPN configuration and deployment
---

# GooseRelayVPN SOCKS5 Tunnel Skill

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

## What It Does

GooseRelayVPN is a SOCKS5 proxy that tunnels raw TCP through a Google Apps Script web app to a self-hosted VPS exit server. The traffic path:

```
Browser/App
  -> SOCKS5 (127.0.0.1:1080)
  -> AES-256-GCM encrypted frames
  -> HTTPS to Google edge IP (SNI=www.google.com, Host=script.google.com)
  -> Apps Script doPost() — dumb forwarder, never sees plaintext
  -> Your VPS :8443/tunnel — decrypts, dials real target
  <- Same path in reverse via long-polling
```

Key properties:
- **Domain fronting**: TLS SNI shows `www.google.com`; actual host is `script.google.com`
- **End-to-end AES-256-GCM**: Google never holds the key
- **Raw TCP tunneling**: SSH, IMAP, custom protocols — anything SOCKS5 carries
- **Multi-deployment load balancing**: Round-robin + health-aware blacklist across multiple Apps Script deployments

---

## Architecture Overview

| Component | Location | Purpose |
|-----------|----------|---------|
| `goose-client` | Local machine | SOCKS5 listener, AES encrypt, HTTPS relay |
| Google Apps Script | Google cloud (free) | Dumb HTTP forwarder, domain-fronting layer |
| `goose-server` | Your VPS | AES decrypt, TCP dial to real targets |

---

## Installation

### Option A: Pre-built Binaries

```bash
# Client (local machine) - Linux example
wget https://github.com/kianmhz/GooseRelayVPN/releases/latest/download/GooseRelayVPN-client-vX.Y.Z-linux-amd64.tar.gz
tar -xzf GooseRelayVPN-client-vX.Y.Z-linux-amd64.tar.gz

# Server (VPS)
wget https://github.com/kianmhz/GooseRelayVPN/releases/latest/download/GooseRelayVPN-server-vX.Y.Z-linux-amd64.tar.gz
tar -xzf GooseRelayVPN-server-vX.Y.Z-linux-amd64.tar.gz
```

Platform suffixes: `windows-amd64`, `darwin-amd64`, `darwin-arm64`, `linux-amd64`, `android-arm64`

### Option B: Build from Source (Go 1.22+)

```bash
git clone https://github.com/kianmhz/GooseRelayVPN.git
cd GooseRelayVPN

# Build both binaries
go build -o goose-client ./cmd/client
go build -o goose-server ./cmd/server

# Cross-compile for Linux VPS from macOS/Windows
GOOS=linux GOARCH=amd64 go build -o goose-server-linux ./cmd/server
```

---

## Quick Start

### Step 1: Generate Secret Key

```bash
bash scripts/gen-key.sh
# Outputs a 64-character hex string — use this as tunnel_key in both configs
```

Or generate manually:
```bash
openssl rand -hex 32
```

### Step 2: Configure Client

`client_config.json`:
```json
{
  "socks_host":  "127.0.0.1",
  "socks_port":  1080,
  "google_host": "216.239.38.120",
  "sni":         "www.google.com",
  "script_keys": ["YOUR_APPS_SCRIPT_DEPLOYMENT_ID"],
  "tunnel_key":  "YOUR_64_CHAR_HEX_KEY"
}
```

### Step 3: Configure Server

`server_config.json`:
```json
{
  "server_host": "0.0.0.0",
  "server_port": 8443,
  "tunnel_key":  "SAME_64_CHAR_HEX_KEY_AS_CLIENT"
}
```

### Step 4: Deploy Google Apps Script

1. Go to [script.google.com](https://script.google.com) → New project
2. Replace default code with `apps_script/Code.gs` contents
3. Edit the VPS URL line:
   ```javascript
   const VPS_URL = 'http://YOUR_VPS_PUBLIC_IP:8443/tunnel';
   ```
4. **Deploy → New deployment** → Type: **Web app**
   - Execute as: **Me**
   - Who has access: **Anyone**
5. Copy the **Deployment ID** → paste into `script_keys` in client config

> ⚠️ Every code edit requires a **new deployment** (not just saving). Old deployment IDs stop working if you only save without redeploying.

### Step 5: Open VPS Firewall

```bash
# UFW
sudo ufw allow 8443/tcp

# Verify from local machine
curl http://YOUR_VPS_IP:8443/healthz
# Expected: HTTP 200 empty body
```

Also check cloud provider firewall (AWS Security Groups, DigitalOcean Firewall, etc.) for inbound TCP 8443.

### Step 6: Run Server on VPS

```bash
./goose-server -config server_config.json
```

### Step 7: Run Client Locally

```bash
./goose-client -config client_config.json
```

Expected output:
```
CLIENT  INFO    GooseRelayVPN client starting
CLIENT  INFO    SOCKS5 proxy: socks5://127.0.0.1:1080
CLIENT  INFO    pre-flight OK: relay healthy, AES key matches end-to-end
CLIENT  INFO    ready: local SOCKS5 is listening on 127.0.0.1:1080
```

---

## CLI Reference

```bash
# Client
./goose-client -config client_config.json
./goose-client -config /path/to/custom_client.json

# Server
./goose-server -config server_config.json
./goose-server -config /path/to/custom_server.json
```

Both binaries take only `-config` flag pointing to their respective JSON config file.

---

## Configuration Reference

### Client Config (`client_config.json`)

| Field | Type | Description |
|-------|------|-------------|
| `socks_host` | string | SOCKS5 listener address. Use `0.0.0.0` for LAN sharing |
| `socks_port` | int | SOCKS5 listener port (default: `1080`) |
| `google_host` | string | Google edge IP for domain fronting (e.g. `216.239.38.120`) |
| `sni` | string | TLS SNI value (must be `www.google.com`) |
| `script_keys` | []string | One or more Apps Script Deployment IDs or full `/exec` URLs |
| `tunnel_key` | string | 64-char hex AES-256 key — must match server |

### Server Config (`server_config.json`)

| Field | Type | Description |
|-------|------|-------------|
| `server_host` | string | Bind address on VPS (use `0.0.0.0`) |
| `server_port` | int | Listen port (default: `8443`) |
| `tunnel_key` | string | 64-char hex AES-256 key — must match client |

---

## Multiple Deployments (Scaling)

Each Apps Script deployment handles ~20,000 calls/day. Add multiple deployment IDs to scale:

```json
{
  "socks_host":  "127.0.0.1",
  "socks_port":  1080,
  "google_host": "216.239.38.120",
  "sni":         "www.google.com",
  "script_keys": [
    "AKfycbx_DEPLOYMENT_ID_ONE_xxxx",
    "AKfycbx_DEPLOYMENT_ID_TWO_xxxx",
    "AKfycbx_DEPLOYMENT_ID_THREE_xxxx"
  ],
  "tunnel_key":  "YOUR_64_CHAR_HEX_KEY"
}
```

The client automatically:
- **Round-robins** across all deployments
- **Backs off** failing deployments (3s → 6s → 12s → up to ~48s)
- **Retries** failed polls on another deployment in the same cycle

All deployments point to the same VPS and use the same `tunnel_key`.

---

## Systemd Service (VPS)

```bash
sudo nano /etc/systemd/system/goose-relay.service
```

```ini
[Unit]
Description=GooseRelayVPN exit server
After=network.target

[Service]
Type=simple
WorkingDirectory=/root
ExecStart=/root/goose-server -config /root/server_config.json
Restart=always
RestartSec=3
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable goose-relay
sudo systemctl start goose-relay
sudo systemctl status goose-relay --no-pager

# View logs
journalctl -u goose-relay -f
```

---

## Google Apps Script (`Code.gs`)

The Apps Script is a thin forwarder. Key structure to understand:

```javascript
// apps_script/Code.gs — dumb forwarder pattern
const VPS_URL = 'http://YOUR_VPS_PUBLIC_IP:8443/tunnel';

function doPost(e) {
  // Forwards request body verbatim to VPS
  // Never decrypts — AES key never touches Google
  const response = UrlFetchApp.fetch(VPS_URL, {
    method: 'post',
    payload: e.postData.contents,
    headers: { 'Content-Type': 'application/octet-stream' },
    muteHttpExceptions: true
  });
  return ContentService.createTextOutput(response.getContent())
    .setMimeType(ContentService.MimeType.OCTET_STREAM);
}
```

---

## Code Examples

### Programmatic Config Generation (Go)

```go
package main

import (
    "crypto/rand"
    "encoding/hex"
    "encoding/json"
    "fmt"
    "os"
)

type ClientConfig struct {
    SocksHost  string   `json:"socks_host"`
    SocksPort  int      `json:"socks_port"`
    GoogleHost string   `json:"google_host"`
    SNI        string   `json:"sni"`
    ScriptKeys []string `json:"script_keys"`
    TunnelKey  string   `json:"tunnel_key"`
}

type ServerConfig struct {
    ServerHost string `json:"server_host"`
    ServerPort int    `json:"server_port"`
    TunnelKey  string `json:"tunnel_key"`
}

func generateTunnelKey() (string, error) {
    b := make([]byte, 32)
    if _, err := rand.Read(b); err != nil {
        return "", err
    }
    return hex.EncodeToString(b), nil
}

func main() {
    key, err := generateTunnelKey()
    if err != nil {
        panic(err)
    }

    clientCfg := ClientConfig{
        SocksHost:  "127.0.0.1",
        SocksPort:  1080,
        GoogleHost: "216.239.38.120",
        SNI:        "www.google.com",
        ScriptKeys: []string{os.Getenv("APPS_SCRIPT_DEPLOYMENT_ID")},
        TunnelKey:  key,
    }

    serverCfg := ServerConfig{
        ServerHost: "0.0.0.0",
        ServerPort: 8443,
        TunnelKey:  key,
    }

    clientJSON, _ := json.MarshalIndent(clientCfg, "", "  ")
    serverJSON, _ := json.MarshalIndent(serverCfg, "", "  ")

    os.WriteFile("client_config.json", clientJSON, 0600)
    os.WriteFile("server_config.json", serverJSON, 0600)

    fmt.Printf("Generated key: %s\n", key)
    fmt.Println("Configs written to client_config.json and server_config.json")
}
```

### Health Check Script (Bash)

```bash
#!/usr/bin/env bash
# check-relay.sh — verify VPS endpoint is reachable before starting client
VPS_IP="${GOOSE_VPS_IP:?Set GOOSE_VPS_IP env var}"
VPS_PORT="${GOOSE_VPS_PORT:-8443}"

echo "Checking VPS health endpoint..."
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
    --connect-timeout 5 \
    "http://${VPS_IP}:${VPS_PORT}/healthz")

if [ "$HTTP_STATUS" = "200" ]; then
    echo "✓ VPS is reachable (HTTP $HTTP_STATUS)"
    exit 0
else
    echo "✗ VPS health check failed (HTTP $HTTP_STATUS)"
    echo "  Check: ufw, cloud firewall, server process running?"
    exit 1
fi
```

### SOCKS5 Proxy Test (Go)

```go
package main

import (
    "fmt"
    "io"
    "net"
    "net/http"
    "os"

    "golang.org/x/net/proxy"
)

func main() {
    // Test the GooseRelayVPN SOCKS5 proxy
    socksAddr := "127.0.0.1:1080"

    dialer, err := proxy.SOCKS5("tcp", socksAddr, nil, proxy.Direct)
    if err != nil {
        fmt.Fprintf(os.Stderr, "Failed to create SOCKS5 dialer: %v\n", err)
        os.Exit(1)
    }

    transport := &http.Transport{
        Dial: func(network, addr string) (net.Conn, error) {
            return dialer.Dial(network, addr)
        },
    }

    client := &http.Client{Transport: transport}

    resp, err := client.Get("https://api.ipify.org?format=json")
    if err != nil {
        fmt.Fprintf(os.Stderr, "Request failed: %v\n", err)
        os.Exit(1)
    }
    defer resp.Body.Close()

    body, _ := io.ReadAll(resp.Body)
    fmt.Printf("Exit IP (should be your VPS IP): %s\n", body)
}
```

### Docker Compose for VPS Deployment

```yaml
# docker-compose.yml — run goose-server on VPS
version: '3.8'

services:
  goose-server:
    image: golang:1.22-alpine
    working_dir: /app
    volumes:
      - ./GooseRelayVPN:/app
      - ./server_config.json:/app/server_config.json:ro
    command: >
      sh -c "go build -o /tmp/goose-server ./cmd/server &&
             /tmp/goose-server -config /app/server_config.json"
    ports:
      - "8443:8443"
    restart: always
    environment:
      - CGO_ENABLED=0
```

---

## Browser Configuration

### Firefox
1. Settings → Network Settings → Manual proxy configuration
2. SOCKS Host: `127.0.0.1`, Port: `1080`
3. Select **SOCKS v5**
4. ✅ Check **Proxy DNS when using SOCKS v5** (prevents DNS leaks)

### Chrome/Edge
Use [FoxyProxy](https://chrome.google.com/webstore/detail/foxyproxy-standard/gcknhkkoolaabfmlnjonogaaifnjlfnp) or [SwitchyOmega](https://chrome.google.com/webstore/detail/proxy-switchyomega/padekgcemlokbadohgkifijomclgjgif):
- Protocol: SOCKS5
- Server: `127.0.0.1`
- Port: `1080`

### System-wide (macOS)
System Preferences → Network → Advanced → Proxies → SOCKS Proxy: `127.0.0.1:1080`

### curl / wget
```bash
curl --socks5-hostname 127.0.0.1:1080 https://api.ipify.org
wget -e "use_proxy=yes" -e "http_proxy=socks5h://127.0.0.1:1080" https://api.ipify.org
```

### SSH through tunnel
```bash
ssh -o ProxyCommand="nc -X 5 -x 127.0.0.1:1080 %h %p" user@remote-host
```

---

## LAN Sharing

To allow other devices on your local network to use the tunnel:

```json
{
  "socks_host": "0.0.0.0",
  "socks_port": 1080,
  ...
}
```

Other devices connect to `YOUR_LOCAL_IP:1080` as their SOCKS5 proxy.

> ⚠️ Only do this on trusted networks — any LAN device can consume your Apps Script quota.

---

## Troubleshooting

### Pre-flight check fails at startup

The client runs automatic checks. Match error message to cause:

| Error | Likely Cause | Fix |
|-------|-------------|-----|
| `relay healthy` fails | Apps Script unreachable | Check deployment ID, redeploy script |
| `AES key mismatch` | `tunnel_key` differs between client/server | Copy exact same key to both configs |
| Connection refused on `curl healthz` | Port 8443 blocked | `ufw allow 8443/tcp` + cloud firewall rule |
| `script_keys` empty | Forgot to paste deployment ID | Deploy Apps Script → copy Deployment ID |

### Apps Script quota exhausted

```
Symptom: tunnel stops working, resets ~10:30 AM Iran time (GMT+3:30)
Fix: Add more deployment IDs to script_keys array
```

Each deployment: ~20,000 calls/day. Client polls ~1/second idle.

### Server not receiving traffic

```bash
# On VPS: verify server is listening
ss -tlnp | grep 8443

# Test healthz endpoint locally on VPS
curl localhost:8443/healthz

# Test from external (your machine)
curl http://YOUR_VPS_IP:8443/healthz

# Check firewall
sudo ufw status
```

### Apps Script returning errors

- Verify `VPS_URL` in `Code.gs` uses correct VPS IP and port 8443
- Verify Apps Script is deployed as **Web app** with **Anyone** access
- After any code edit, create a **New deployment** — don't reuse old deployment ID
- Check Apps Script execution log: script.google.com → Executions tab

### Key mismatch debugging

```bash
# Verify key lengths match (should both be 64 chars)
cat client_config.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(len(d['tunnel_key']), d['tunnel_key'][:8]+'...')"
cat server_config.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(len(d['tunnel_key']), d['tunnel_key'][:8]+'...')"
```

### systemd service won't start

```bash
sudo systemctl status goose-relay --no-pager
journalctl -u goose-relay -n 50 --no-pager

# Common fix: wrong binary path in ExecStart
which goose-server  # find actual path
```

### DNS leaks

Ensure browser uses **proxy DNS** (Firefox: "Proxy DNS when using SOCKS v5"). Without this, DNS queries bypass the tunnel.

---

## Security Notes

- **Never share `tunnel_key`** — anyone with it can use your VPS as an exit node
- Store configs with restricted permissions: `chmod 600 client_config.json server_config.json`
- Google never sees plaintext — AES key never touches Apps Script
- The `mitm` topic in the repo refers to traffic inspection capability; no local MITM cert is needed for this project (unlike `MasterHttpRelayVPN`)
- Quota resets daily; rotate deployment IDs periodically if quota is a concern

---

## Common Patterns

### Environment-based config generation

```bash
# Generate config from environment variables
cat > client_config.json << EOF
{
  "socks_host":  "127.0.0.1",
  "socks_port":  1080,
  "google_host": "216.239.38.120",
  "sni":         "www.google.com",
  "script_keys": ["${APPS_SCRIPT_DEPLOYMENT_ID}"],
  "tunnel_key":  "${GOOSE_TUNNEL_KEY}"
}
EOF

cat > server_config.json << EOF
{
  "server_host": "0.0.0.0",
  "server_port": 8443,
  "tunnel_key":  "${GOOSE_TUNNEL_KEY}"
}
EOF
```

### Multiple Google accounts for maximum capacity

```json
{
  "script_keys": [
    "AKfycbx_account1_deployment1",
    "AKfycbx_account1_deployment2",
    "AKfycbx_account2_deployment1",
    "AKfycbx_account2_deployment2"
  ]
}
```

Deploy `Code.gs` under different Google accounts for independent quotas. All point to the same VPS.

### Verify exit IP after setup

```bash
# Should show your VPS IP, not your real IP
curl --socks5-hostname 127.0.0.1:1080 https://api.ipify.org
```
