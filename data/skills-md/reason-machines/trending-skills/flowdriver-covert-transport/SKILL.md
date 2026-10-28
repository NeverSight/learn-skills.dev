---
name: flowdriver-covert-transport
description: Tunnel SOCKS5 traffic through Google Drive API requests to bypass restrictive networks and DPI inspection.
triggers:
  - tunnel traffic through google drive
  - bypass network restrictions with flowdriver
  - set up flowdriver socks5 proxy
  - covert transport through cloud storage
  - flowdriver client server setup
  - route traffic through google drive api
  - evade dpi with google drive tunnel
  - flowdriver configuration and deployment
---

# FlowDriver Covert Transport

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

FlowDriver tunnels SOCKS5 proxy traffic through Google Drive API calls, making network traffic appear as legitimate cloud storage activity. It treats a shared Drive folder as a bidirectional data queue: the client uploads binary-encoded request packets, the server polls for them, opens real TCP connections, and returns responses as Drive files.

---

## How It Works

```
Local App → SOCKS5 → FlowDriver Client → Google Drive Folder → FlowDriver Server → Internet
                      (upload requests)   (shared queue)        (download + proxy)
```

1. **Client** listens on a local SOCKS5 port, encodes TCP requests into a binary protocol, and uploads them to a Drive folder.
2. **Server** polls the same folder, downloads request files, opens real TCP connections to destinations, and uploads response files back.
3. Traffic appears as normal `googleapis.com` API calls — resilient against SNI-based and DPI filtering.

---

## Installation

### Prerequisites

- Go 1.25+
- Google Cloud project with Drive API enabled
- `credentials.json` (OAuth2 Desktop App credentials)

### Build

```bash
git clone https://github.com/NullLatency/FlowDriver.git
cd FlowDriver
go build -o bin/client ./cmd/client
go build -o bin/server ./cmd/server
```

---

## Google Drive API Setup

### Step 1: Enable the API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create or select a project
3. Enable **Google Drive API** under "APIs & Services"

### Step 2: Create OAuth2 Credentials

1. "APIs & Services" → "Credentials" → "Create Credentials" → **OAuth client ID**
2. Application type: **Desktop App**
3. Download the JSON → rename to `credentials.json`

### Step 3: Publish the App (Prevent Token Expiry)

In "OAuth consent screen", click **Publish App** — otherwise tokens expire every 7 days (Testing mode).

---

## Configuration

### Client Config (`client_config.json`)

```json
{
  "listen_addr": "127.0.0.1:1080",
  "storage_type": "google",
  "google_folder_id": "",
  "refresh_rate_ms": 150,
  "flush_rate_ms": 300,
  "transport": {
    "TargetIP": "216.239.38.120:443",
    "SNI": "google.com",
    "HostHeader": "www.googleapis.com"
  }
}
```

> Leave `google_folder_id` empty on first run — FlowDriver auto-creates a **"Flow-Data"** folder and saves the ID back to config.

### Server Config (`server_config.json`)

```json
{
  "storage_type": "google",
  "google_folder_id": "SAME_FOLDER_ID_AS_CLIENT",
  "refresh_rate_ms": 150,
  "flush_rate_ms": 300
}
```

> `google_folder_id` **must match** between client and server configs.

### Key Config Fields

| Field | Description | Recommended |
|---|---|---|
| `listen_addr` | Local SOCKS5 listener | `127.0.0.1:1080` |
| `refresh_rate_ms` | How often to poll Drive for new packets | ≥ 100ms |
| `flush_rate_ms` | How often to batch-upload pending data | ≥ 300ms |
| `transport.TargetIP` | Google API IP for direct TLS connection | `216.239.38.120:443` |
| `transport.SNI` | TLS SNI value sent in handshake | `google.com` |
| `transport.HostHeader` | HTTP Host header for API calls | `www.googleapis.com` |

---

## Running FlowDriver

### First-Time Authentication (Local Machine)

Run the client once to complete OAuth2 flow:

```bash
./bin/client -c client_config.json -gc credentials.json
```

1. A URL appears in the terminal — open it in your browser
2. Log in to Google and grant Drive permissions
3. You'll be redirected to `http://localhost/...` (page may not load — that's fine)
4. Copy the **full URL** from the address bar and paste it into the terminal
5. A `.token` file is created alongside `credentials.json`

### Deploy Server (Remote Machine)

```bash
# Copy both files to the server
scp credentials.json user@server:/path/to/flowdriver/
scp *.token user@server:/path/to/flowdriver/

# Ensure server_config.json has the correct google_folder_id
# (copy it from your local client_config.json after first run)

# Start the server
./bin/server -c server_config.json -gc credentials.json
```

The server auto-uses the existing `.token` — no browser needed.

### Start the Client

```bash
./bin/client -c client_config.json -gc credentials.json
```

### Use the SOCKS5 Proxy

```bash
# Test with curl
curl --socks5 127.0.0.1:1080 https://example.com

# Configure in browser (Firefox: Manual proxy → SOCKS5 → 127.0.0.1:1080)

# Use with any SOCKS5-aware application
export ALL_PROXY=socks5://127.0.0.1:1080
```

---

## CLI Reference

### Client

```bash
./bin/client -c <config_file> -gc <credentials_file>

# Flags:
#   -c    Path to client_config.json
#   -gc   Path to credentials.json (OAuth2)
```

### Server

```bash
./bin/server -c <config_file> -gc <credentials_file>

# Flags:
#   -c    Path to server_config.json
#   -gc   Path to credentials.json (OAuth2)
```

---

## Code Examples

### Verify SOCKS5 Proxy in Go

```go
package main

import (
    "fmt"
    "io"
    "net/http"
    "golang.org/x/net/proxy"
)

func main() {
    // Connect through FlowDriver SOCKS5 proxy
    dialer, err := proxy.SOCKS5("tcp", "127.0.0.1:1080", nil, proxy.Direct)
    if err != nil {
        panic(err)
    }

    transport := &http.Transport{Dial: dialer.Dial}
    client := &http.Client{Transport: transport}

    resp, err := client.Get("https://httpbin.org/ip")
    if err != nil {
        panic(err)
    }
    defer resp.Body.Close()

    body, _ := io.ReadAll(resp.Body)
    fmt.Println(string(body))
}
```

### Programmatic Config Generation

```go
package main

import (
    "encoding/json"
    "os"
)

type TransportConfig struct {
    TargetIP   string
    SNI        string
    HostHeader string
}

type ClientConfig struct {
    ListenAddr     string          `json:"listen_addr"`
    StorageType    string          `json:"storage_type"`
    GoogleFolderID string          `json:"google_folder_id"`
    RefreshRateMs  int             `json:"refresh_rate_ms"`
    FlushRateMs    int             `json:"flush_rate_ms"`
    Transport      TransportConfig `json:"transport"`
}

func main() {
    cfg := ClientConfig{
        ListenAddr:     "127.0.0.1:1080",
        StorageType:    "google",
        GoogleFolderID: "", // auto-created on first run
        RefreshRateMs:  150,
        FlushRateMs:    300,
        Transport: TransportConfig{
            TargetIP:   "216.239.38.120:443",
            SNI:        "google.com",
            HostHeader: "www.googleapis.com",
        },
    }

    data, _ := json.MarshalIndent(cfg, "", "  ")
    os.WriteFile("client_config.json", data, 0644)
}
```

### Using with `proxychains`

```bash
# /etc/proxychains4.conf
# Add at the bottom:
# socks5  127.0.0.1  1080

proxychains4 curl https://example.com
proxychains4 ssh user@remote-host
```

---

## Common Patterns

### Pattern: High-Latency Stable Connection

For restricted networks where stability matters more than speed:

```json
{
  "refresh_rate_ms": 300,
  "flush_rate_ms": 500
}
```

### Pattern: Multiple Concurrent Users

Increase poll intervals to avoid quota exhaustion:

```json
{
  "refresh_rate_ms": 200,
  "flush_rate_ms": 400
}
```

### Pattern: Systemd Service (Server)

```ini
# /etc/systemd/system/flowdriver.service
[Unit]
Description=FlowDriver Covert Transport Server
After=network.target

[Service]
Type=simple
WorkingDirectory=/opt/flowdriver
ExecStart=/opt/flowdriver/bin/server -c server_config.json -gc credentials.json
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable flowdriver
sudo systemctl start flowdriver
sudo systemctl status flowdriver
```

### Pattern: Docker Deployment (Server)

```dockerfile
FROM golang:1.25-alpine AS builder
WORKDIR /app
COPY . .
RUN go build -o bin/server ./cmd/server

FROM alpine:latest
WORKDIR /app
COPY --from=builder /app/bin/server .
# Mount credentials.json, .token, and server_config.json as volumes
CMD ["./server", "-c", "server_config.json", "-gc", "credentials.json"]
```

```bash
docker run -d \
  -v $(pwd)/credentials.json:/app/credentials.json \
  -v $(pwd)/*.token:/app/ \
  -v $(pwd)/server_config.json:/app/server_config.json \
  flowdriver-server
```

---

## Troubleshooting

### Token Expires Every 7 Days

**Cause**: App is in "Testing" mode on Google Cloud.  
**Fix**: Go to OAuth consent screen → **Publish App**. Re-authenticate once after publishing.

### `google_folder_id` Mismatch

**Symptom**: Server polls indefinitely, client uploads but gets no responses.  
**Fix**: After the first client run, check `client_config.json` for the auto-saved `google_folder_id`. Copy it exactly into `server_config.json`.

### API Quota Exhausted (429 errors)

**Symptom**: Connections slow down or fail after sustained use.  
**Fix**: Increase `refresh_rate_ms` and `flush_rate_ms` to ≥ 200ms. Never go below 100ms.

```json
{
  "refresh_rate_ms": 200,
  "flush_rate_ms": 400
}
```

### OAuth Callback URL Doesn't Load

**Expected behavior** — the browser redirecting to `http://localhost/...` and showing an error page is normal. Copy the full URL from the address bar anyway and paste it into the terminal.

### `.token` File Not Found on Server

```bash
# The token file is named after credentials, check for it:
ls -la /path/to/flowdriver/*.token

# Re-run auth on local machine and re-copy:
./bin/client -c client_config.json -gc credentials.json
scp *.token user@server:/path/to/flowdriver/
```

### Build Fails — Wrong Go Version

```bash
go version  # must be 1.25+
# Install latest Go from https://go.dev/dl/
```

### Test SOCKS5 Proxy Connectivity

```bash
# Basic connectivity test
curl -v --socks5 127.0.0.1:1080 https://httpbin.org/ip

# If it hangs: check client is running and authenticated
# If connection refused: verify listen_addr in client_config.json
```

---

## Performance Considerations

| Scenario | `refresh_rate_ms` | `flush_rate_ms` |
|---|---|---|
| Single user, fast | 100 | 300 |
| Single user, stable | 150 | 300 |
| Multi-user / heavy | 200 | 400 |
| Quota-conscious | 300 | 500 |

- Each poll is a Drive API `list` call — aggressive polling burns quota fast
- Response latency = `refresh_rate_ms` + upload/download time (typically 200–800ms total RTT)
- Not suitable for real-time protocols (VoIP, gaming) — best for HTTP/HTTPS browsing and SSH
