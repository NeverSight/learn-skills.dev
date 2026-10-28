---
name: weclaw-wechat-ai-bridge
description: Connect WeChat to AI agents (Claude, Codex, Gemini, Kimi, etc.) using the WeClaw bridge in Go.
triggers:
  - connect wechat to claude
  - wechat ai agent bridge
  - weclaw setup and configuration
  - send messages from wechat to ai
  - weclaw agent integration
  - bridge wechat with openai compatible api
  - weclaw proactive messaging
  - wechat bot with ai backend
---

# WeClaw — WeChat AI Agent Bridge

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

WeClaw connects WeChat to AI agents (Claude, Codex, Gemini, Kimi, OpenClaw, etc.) via a Go-based bridge. It handles QR-code login, message routing, media conversion, and agent lifecycle. Supports three agent modes: ACP (JSON-RPC subprocess, fastest), CLI (new process per message), and HTTP (OpenAI-compatible REST).

---

## Installation

```bash
# One-line installer
curl -sSL https://raw.githubusercontent.com/fastclaw-ai/weclaw/main/install.sh | sh

# Via Go toolchain
go install github.com/fastclaw-ai/weclaw@latest

# Via Docker
docker run -it -v ~/.weclaw:/root/.weclaw ghcr.io/fastclaw-ai/weclaw start
```

---

## First-Run Flow

```bash
weclaw start        # Shows QR code → scan with WeChat → auto-detects agents → saves config
weclaw login        # Add/re-authenticate a WeChat account
weclaw status       # Show running state and active agent
weclaw stop         # Stop the background daemon
weclaw start -f     # Foreground mode (debug/verbose)
```

Logs: `~/.weclaw/weclaw.log`  
Config: `~/.weclaw/config.json`

---

## Configuration

```json
{
  "default_agent": "claude",
  "agents": {
    "claude": {
      "type": "acp",
      "command": "/usr/local/bin/claude-agent-acp",
      "model": "sonnet"
    },
    "codex": {
      "type": "acp",
      "command": "/usr/local/bin/codex-acp"
    },
    "claude-cli": {
      "type": "cli",
      "command": "/usr/local/bin/claude",
      "args": ["--dangerously-skip-permissions"]
    },
    "codex-cli": {
      "type": "cli",
      "command": "/usr/local/bin/codex",
      "args": ["--skip-git-repo-check"]
    },
    "openclaw": {
      "type": "http",
      "endpoint": "https://api.example.com/v1/chat/completions",
      "api_key": "$OPENCLAW_GATEWAY_TOKEN",
      "model": "openclaw:main"
    }
  }
}
```

### Environment Variables

| Variable | Purpose |
|----------|---------|
| `WECLAW_DEFAULT_AGENT` | Override default agent at runtime |
| `WECLAW_API_ADDR` | Change local HTTP API address (default `127.0.0.1:18011`) |
| `OPENCLAW_GATEWAY_URL` | HTTP agent endpoint |
| `OPENCLAW_GATEWAY_TOKEN` | HTTP agent API token |

---

## Agent Modes

| Mode | Process model | Best for |
|------|--------------|----------|
| `acp` | Long-running subprocess, JSON-RPC over stdio | Claude, Codex, Kimi, Gemini — fastest, session reuse |
| `cli` | New process per message, `--resume` for sessions | `claude -p`, `codex exec` |
| `http` | OpenAI-compatible `/v1/chat/completions` | Any REST-accessible model |

Auto-detection prefers `acp` over `cli` when both binaries exist.

---

## Chat Commands (send as WeChat messages)

| Command | Action |
|---------|--------|
| `hello` | Send to default agent |
| `/codex write a sort function` | Route to named agent |
| `/cc explain this code` | Use alias (`/cc` → claude) |
| `/claude` | Switch default agent to Claude (persisted) |
| `/status` | Show active agent info |
| `/help` | List available commands |

### Built-in Aliases

| Alias | Agent |
|-------|-------|
| `/cc` | claude |
| `/cx` | codex |
| `/cs` | cursor |
| `/km` | kimi |
| `/gm` | gemini |
| `/ocd` | opencode |
| `/oc` | openclaw |

---

## Proactive Messaging — CLI

```bash
# Send plain text
weclaw send --to "user_id@im.wechat" --text "Hello from WeClaw"

# Send an image
weclaw send --to "user_id@im.wechat" --media "https://example.com/photo.png"

# Send text + media together
weclaw send --to "user_id@im.wechat" \
  --text "Check this out" \
  --media "https://example.com/photo.png"

# Send a file
weclaw send --to "user_id@im.wechat" --media "https://example.com/report.pdf"
```

---

## Proactive Messaging — HTTP API

The local API listens on `127.0.0.1:18011` while `weclaw start` is running.

```bash
# Send text
curl -X POST http://127.0.0.1:18011/api/send \
  -H "Content-Type: application/json" \
  -d '{"to": "user_id@im.wechat", "text": "Hello from WeClaw"}'

# Send image
curl -X POST http://127.0.0.1:18011/api/send \
  -H "Content-Type: application/json" \
  -d '{"to": "user_id@im.wechat", "media_url": "https://example.com/photo.png"}'

# Send text + media
curl -X POST http://127.0.0.1:18011/api/send \
  -H "Content-Type: application/json" \
  -d '{"to": "user_id@im.wechat", "text": "See this", "media_url": "https://example.com/photo.png"}'
```

**Supported media types:** `png`, `jpg`, `gif`, `webp`, `mp4`, `mov`, `pdf`, `doc`, `zip`.

Change listen address:
```bash
WECLAW_API_ADDR=0.0.0.0:18011 weclaw start
```

---

## Go Integration Example

Call the WeClaw HTTP API from a Go service to send notifications:

```go
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
)

type SendRequest struct {
	To       string `json:"to"`
	Text     string `json:"text,omitempty"`
	MediaURL string `json:"media_url,omitempty"`
}

type SendResponse struct {
	OK      bool   `json:"ok"`
	Message string `json:"message,omitempty"`
}

func sendToWeChat(to, text, mediaURL string) error {
	apiAddr := os.Getenv("WECLAW_API_ADDR")
	if apiAddr == "" {
		apiAddr = "127.0.0.1:18011"
	}

	req := SendRequest{To: to, Text: text, MediaURL: mediaURL}
	body, err := json.Marshal(req)
	if err != nil {
		return fmt.Errorf("marshal: %w", err)
	}

	resp, err := http.Post(
		fmt.Sprintf("http://%s/api/send", apiAddr),
		"application/json",
		bytes.NewReader(body),
	)
	if err != nil {
		return fmt.Errorf("post: %w", err)
	}
	defer resp.Body.Close()

	var result SendResponse
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return fmt.Errorf("decode: %w", err)
	}
	if !result.OK {
		return fmt.Errorf("weclaw error: %s", result.Message)
	}
	return nil
}

func main() {
	recipient := os.Getenv("WECHAT_RECIPIENT_ID") // e.g. "user_id@im.wechat"
	if err := sendToWeChat(recipient, "Build succeeded ✅", ""); err != nil {
		fmt.Fprintf(os.Stderr, "failed: %v\n", err)
		os.Exit(1)
	}
	fmt.Println("Message sent.")
}
```

---

## Docker Setup

```bash
# Build image
docker build -t weclaw .

# Step 1: Interactive login (scan QR code)
docker run -it -v ~/.weclaw:/root/.weclaw weclaw login

# Step 2: Run daemon with HTTP agent
docker run -d --name weclaw \
  -v ~/.weclaw:/root/.weclaw \
  -e OPENCLAW_GATEWAY_URL=https://api.example.com \
  -e OPENCLAW_GATEWAY_TOKEN="$OPENCLAW_GATEWAY_TOKEN" \
  weclaw

# Expose the local API externally (bind carefully — no auth by default)
docker run -d --name weclaw \
  -v ~/.weclaw:/root/.weclaw \
  -e WECLAW_API_ADDR=0.0.0.0:18011 \
  -p 18011:18011 \
  -e OPENCLAW_GATEWAY_TOKEN="$OPENCLAW_GATEWAY_TOKEN" \
  weclaw

docker logs -f weclaw
```

> ACP/CLI agents require the agent binary inside the container. Mount the binary or build a custom image. HTTP agents work out of the box.

---

## System Service (Auto-start)

**macOS (launchd):**
```bash
cp service/com.fastclaw.weclaw.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.fastclaw.weclaw.plist
```

**Linux (systemd):**
```bash
sudo cp service/weclaw.service /etc/systemd/system/
sudo systemctl enable --now weclaw
journalctl -u weclaw -f
```

---

## Development

```bash
make dev                        # Hot reload
go build -o weclaw .            # Build binary
./weclaw start -f               # Run in foreground
```

**Releasing:**
```bash
git tag v0.1.0
git push origin v0.1.0
# GitHub Actions builds darwin/linux × amd64/arm64 and uploads release artifacts
```

---

## Common Patterns

### Pattern: Per-user agent routing
Send `/claude` or `/codex` as a WeChat message to switch the default agent. The choice persists in `~/.weclaw/config.json` across restarts.

### Pattern: CI/CD build notifications
After a build, call `weclaw send` or POST to the HTTP API to push results to a WeChat contact or group.

### Pattern: Media from agent
If an agent reply contains `![alt](https://...)`, WeClaw auto-downloads, AES-128-ECB encrypts, uploads to WeChat CDN, and delivers as a native image message — no extra config needed.

### Pattern: Disable permission prompts for headless use
```json
{
  "claude": { "type": "cli", "command": "/usr/local/bin/claude",
               "args": ["--dangerously-skip-permissions"] },
  "codex":  { "type": "cli", "command": "/usr/local/bin/codex",
               "args": ["--skip-git-repo-check"] }
}
```
ACP agents handle permissions automatically and do not need these flags.

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| QR code not appearing | Run `weclaw login` explicitly; ensure terminal supports UTF-8 |
| Agent not auto-detected | Check binary is on `$PATH`; run `weclaw status` |
| `connection refused` on HTTP API | Confirm `weclaw start` is running; check `WECLAW_API_ADDR` |
| Agent permission prompts block responses | Add `--dangerously-skip-permissions` (Claude) or `--skip-git-repo-check` (Codex) to `args`; or use ACP mode |
| Docker — no agent binary | Mount binary: `-v /usr/local/bin/claude:/usr/local/bin/claude`; or use HTTP mode |
| Markdown not rendering | WeClaw strips markdown automatically for WeChat plain-text display; this is expected |
| Logs | `tail -f ~/.weclaw/weclaw.log` or `docker logs -f weclaw` |
