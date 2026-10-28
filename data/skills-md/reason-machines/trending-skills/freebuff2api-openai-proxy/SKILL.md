---
name: freebuff2api-openai-proxy
description: OpenAI-compatible proxy server for Freebuff that translates standard OpenAI API requests into Freebuff's backend format with multi-token rotation and Docker deployment.
triggers:
  - set up freebuff2api proxy
  - use freebuff with openai sdk
  - configure freebuff token rotation
  - deploy freebuff proxy docker
  - openai compatible freebuff proxy
  - freebuff auth token setup
  - proxy freebuff requests openai format
  - freebuff2api configuration
---

# Freebuff2API OpenAI Proxy

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Freebuff2API is an OpenAI-compatible proxy server written in Go that translates standard OpenAI API requests into Freebuff's backend format. It enables any OpenAI-compatible client, SDK, or CLI tool to use Freebuff's free models without modification.

## What It Does

- Exposes standard OpenAI endpoints (`/v1/chat/completions`, etc.)
- Dynamically randomizes client fingerprints to mimic official Freebuff SDK behavior
- Rotates multiple auth tokens on a configurable interval
- Routes outbound traffic through an optional HTTP proxy
- Ships as a multi-arch Docker image for easy deployment

## Getting Auth Tokens

Before deploying, obtain one or more Freebuff auth tokens:

**Method 1 — Web (easiest):**
Visit [https://freebuff.llm.pm](https://freebuff.llm.pm), log in with your Freebuff account, and copy the displayed token.

**Method 2 — Freebuff CLI:**
```bash
npm i -g freebuff
freebuff  # follow login prompts
```

Token is stored at:
- **Linux/macOS:** `~/.config/manicode/credentials.json`
- **Windows:** `C:\Users\<username>\.config\manicode\credentials.json`

```json
{
  "default": {
    "authToken": "fa82b5c1-e39d-4c7a-961f-d2b3c4e5f6a7"
  }
}
```

Copy the `authToken` value — this is your `AUTH_TOKENS` value.

## Installation & Deployment

### Docker (Recommended)

```bash
# Single token
docker run -d --name freebuff2api \
  -p 8080:8080 \
  -e AUTH_TOKENS="$FREEBUFF_TOKEN" \
  ghcr.io/quorinex/freebuff2api:latest

# Multiple tokens (comma-separated for higher throughput)
docker run -d --name freebuff2api \
  -p 8080:8080 \
  -e AUTH_TOKENS="$FREEBUFF_TOKEN_1,$FREEBUFF_TOKEN_2,$FREEBUFF_TOKEN_3" \
  ghcr.io/quorinex/freebuff2api:latest

# With HTTP proxy and API key protection
docker run -d --name freebuff2api \
  -p 8080:8080 \
  -e AUTH_TOKENS="$FREEBUFF_TOKEN" \
  -e API_KEYS="$MY_PROXY_API_KEY" \
  -e HTTP_PROXY="$HTTP_PROXY_URL" \
  ghcr.io/quorinex/freebuff2api:latest
```

### Docker Compose

```yaml
# docker-compose.yml
version: "3.8"
services:
  freebuff2api:
    image: ghcr.io/quorinex/freebuff2api:latest
    container_name: freebuff2api
    restart: unless-stopped
    ports:
      - "8080:8080"
    environment:
      AUTH_TOKENS: "${FREEBUFF_TOKENS}"
      API_KEYS: "${PROXY_API_KEYS}"
      ROTATION_INTERVAL: "6h"
      REQUEST_TIMEOUT: "15m"
    # Or mount a config file:
    # volumes:
    #   - ./config.json:/app/config.json
    # command: ["-config", "/app/config.json"]
```

```bash
# .env file
FREEBUFF_TOKENS=token1,token2,token3
PROXY_API_KEYS=my-secret-key
```

### Build from Source

Requirements: Go 1.23+

```bash
git clone https://github.com/Quorinex/Freebuff2API.git
cd Freebuff2API
go build -o freebuff2api .

# Run with config file
./freebuff2api -config config.json

# Run with environment variables
AUTH_TOKENS="$FREEBUFF_TOKEN" ./freebuff2api
```

```bash
docker build -t freebuff2api .
docker run -d -p 8080:8080 -e AUTH_TOKENS="$FREEBUFF_TOKEN" freebuff2api
```

## Configuration

### config.json

```json
{
  "LISTEN_ADDR": ":8080",
  "UPSTREAM_BASE_URL": "https://codebuff.com",
  "AUTH_TOKENS": ["token1", "token2"],
  "ROTATION_INTERVAL": "6h",
  "REQUEST_TIMEOUT": "15m",
  "API_KEYS": ["my-proxy-api-key"],
  "HTTP_PROXY": ""
}
```

### Configuration Reference

| Key / Env Var | Default | Description |
|---|---|---|
| `LISTEN_ADDR` | `:8080` | Proxy listen address |
| `UPSTREAM_BASE_URL` | `https://codebuff.com` | Freebuff backend URL |
| `AUTH_TOKENS` | — | Freebuff auth tokens (JSON array or comma-separated) |
| `ROTATION_INTERVAL` | `6h` | How often to rotate tokens |
| `REQUEST_TIMEOUT` | `15m` | Upstream request timeout |
| `API_KEYS` | `[]` | Client API keys for proxy auth (empty = open access) |
| `HTTP_PROXY` | `""` | HTTP proxy for outbound requests |

**Note:** Environment variables override JSON file values when both are set.

## Using the Proxy

Once running, point any OpenAI-compatible client at `http://localhost:8080`:

### curl

```bash
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $PROXY_API_KEY" \
  -d '{
    "model": "claude-3-5-sonnet",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

If `API_KEYS` is empty (open access), omit the Authorization header or use any value:
```bash
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "claude-3-5-sonnet", "messages": [{"role": "user", "content": "Hello!"}]}'
```

### Python (openai SDK)

```python
from openai import OpenAI
import os

client = OpenAI(
    base_url="http://localhost:8080/v1",
    api_key=os.environ.get("PROXY_API_KEY", "unused"),  # any value if API_KEYS is empty
)

response = client.chat.completions.create(
    model="claude-3-5-sonnet",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain async/await in Python."},
    ],
)
print(response.choices[0].message.content)
```

### Streaming

```python
from openai import OpenAI
import os

client = OpenAI(
    base_url="http://localhost:8080/v1",
    api_key=os.environ.get("PROXY_API_KEY", "unused"),
)

stream = client.chat.completions.create(
    model="claude-3-5-sonnet",
    messages=[{"role": "user", "content": "Write a short poem."}],
    stream=True,
)

for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="", flush=True)
print()
```

### Node.js (openai SDK)

```javascript
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "http://localhost:8080/v1",
  apiKey: process.env.PROXY_API_KEY ?? "unused",
});

const response = await client.chat.completions.create({
  model: "claude-3-5-sonnet",
  messages: [{ role: "user", content: "Hello from Node.js!" }],
});

console.log(response.choices[0].message.content);
```

### LangChain (Python)

```python
from langchain_openai import ChatOpenAI
import os

llm = ChatOpenAI(
    model="claude-3-5-sonnet",
    openai_api_base="http://localhost:8080/v1",
    openai_api_key=os.environ.get("PROXY_API_KEY", "unused"),
)

result = llm.invoke("What is the capital of France?")
print(result.content)
```

## Common Patterns

### Multi-Token Setup for Higher Throughput

Collect tokens from multiple Freebuff accounts:
```bash
# config.json approach
{
  "AUTH_TOKENS": [
    "token-account-1",
    "token-account-2",
    "token-account-3"
  ],
  "ROTATION_INTERVAL": "3h"
}

# Environment variable approach (comma-separated)
export AUTH_TOKENS="token1,token2,token3"
```

### Securing the Proxy with API Keys

```json
{
  "API_KEYS": ["secret-key-for-team", "another-key-for-ci"]
}
```

Clients must then include `Authorization: Bearer secret-key-for-team`.

### Using with HTTP Proxy (Corporate/Regional)

```json
{
  "HTTP_PROXY": "http://proxy.company.com:3128"
}
```

Or via environment:
```bash
docker run -d --name freebuff2api \
  -p 8080:8080 \
  -e AUTH_TOKENS="$FREEBUFF_TOKEN" \
  -e HTTP_PROXY="$CORPORATE_PROXY" \
  ghcr.io/quorinex/freebuff2api:latest
```

### Health Check / Verify Running

```bash
# Check the proxy is responding
curl -s http://localhost:8080/v1/models | jq .

# Or a minimal chat request
curl -s http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"claude-3-5-sonnet","messages":[{"role":"user","content":"ping"}]}' \
  | jq '.choices[0].message.content'
```

## Troubleshooting

### Proxy returns 401 Unauthorized
- If `API_KEYS` is configured, ensure your client sends `Authorization: Bearer <key>` matching one of the configured keys.
- If `API_KEYS` is empty `[]`, the proxy is open — no auth header needed.

### Auth token rejected / 403 from upstream
- Token may be expired — re-fetch from [https://freebuff.llm.pm](https://freebuff.llm.pm) or re-run `freebuff` CLI.
- Check `AUTH_TOKENS` is set correctly (not empty, no extra whitespace).

### Request timeouts
- Increase `REQUEST_TIMEOUT` beyond default `15m` for very long completions:
  ```json
  { "REQUEST_TIMEOUT": "30m" }
  ```

### Connection refused on localhost:8080
- Confirm the container/process is running: `docker ps` or `ps aux | grep freebuff2api`
- Check `LISTEN_ADDR` — if set to a specific interface (e.g., `127.0.0.1:8080`), ensure you're connecting to the right address.
- For Docker, verify the port mapping: `-p 8080:8080`

### Docker container exits immediately
```bash
# Check logs
docker logs freebuff2api

# Common cause: AUTH_TOKENS not set
docker run --rm -e AUTH_TOKENS="$FREEBUFF_TOKEN" ghcr.io/quorinex/freebuff2api:latest
```

### Multiple tokens not rotating
- Verify tokens are comma-separated (env var) or a JSON array (config file).
- Check `ROTATION_INTERVAL` is a valid Go duration string: `"1h"`, `"30m"`, `"6h"`, etc.

## Project Structure (Source)

```
Freebuff2API/
├── main.go           # Entry point, config loading, server startup
├── config.json       # Default config file (gitignored if contains secrets)
├── Dockerfile        # Multi-arch Docker build
├── go.mod / go.sum   # Go module dependencies
├── README.md
└── README_zh.md
```

## Key CLI Flag

```bash
./freebuff2api -config /path/to/config.json
```

The only CLI flag is `-config` to specify an alternate config file path. All other configuration is via the JSON file or environment variables.
