---
name: gpt2api-openai-gateway
description: OpenAI-compatible SaaS gateway that reverse-engineers chatgpt.com to provide GPT Image 2, multi-account pooling, batch image generation, and billing management.
triggers:
  - set up gpt2api gateway
  - configure chatgpt account pool
  - generate images with gpt-image-2
  - deploy openai compatible proxy
  - batch image generation with chatgpt
  - add accounts to gpt2api
  - configure gpt2api proxy pool
  - integrate gpt2api with openai sdk
---

# gpt2api OpenAI Gateway

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

`gpt2api` is a self-hosted OpenAI-compatible API gateway that reverse-engineers `chatgpt.com` to expose GPT Image 2 / DALL·E 3 / IMG2 grayscale capabilities via standard `/v1/images/generations`, `/v1/images/edits`, and `/v1/chat/completions` endpoints. It provides multi-account pooling, proxy pooling, rate limiting, credit billing, and an admin dashboard.

---

## Installation & Deployment

### Docker Compose (Recommended)

```bash
git clone https://github.com/432539/gpt2api.git
cd gpt2api/deploy
cp .env.example .env
```

Edit `.env` — these three are **required**:

```env
JWT_SECRET=<generate with: openssl rand -base64 48 | tr -d '=/+' | cut -c1-48>
CRYPTO_AES_KEY=<generate with: openssl rand -hex 32>
MYSQL_ROOT_PASSWORD=<strong-password>
MYSQL_PASSWORD=<strong-password>
```

Generate secrets:

```bash
# CRYPTO_AES_KEY (must be exactly 64 hex chars = 32 bytes AES-256)
openssl rand -hex 32

# JWT_SECRET (>=32 chars)
openssl rand -base64 48 | tr -d '=/+' | cut -c1-48
```

Start services:

```bash
docker compose up -d --build
docker compose logs -f server
```

On startup the server automatically:
1. Waits for MySQL health check
2. Runs `goose up` database migrations
3. Starts HTTP on `:8080`

**Default admin credentials** (change immediately):
- URL: `http://<server-ip>:8080/`
- Email: `admin@example.com`
- Password: `admin123`

---

## Configuration

Main config file: `configs/config.yaml` (override with `GPT2API_*` env vars in Docker).

```yaml
app:
  listen: ":8080"
  base_url: "https://your-domain.com"   # used for signed image proxy URLs

mysql:
  dsn: "user:pass@tcp(mysql:3306)/gpt2api?parseTime=true"
  max_open_conns: 500

redis:
  addr: "redis:6379"
  pool_size: 500                          # needed for distributed locks & rate limiting

jwt:
  secret: "${JWT_SECRET}"
  access_ttl_sec: 7200
  refresh_ttl_sec: 604800

crypto:
  aes_key: "${CRYPTO_AES_KEY}"           # 64-char hex, encrypts account AT/cookies

scheduler:
  min_interval_sec: 10                   # minimum seconds between uses of same account
  daily_usage_ratio: 0.8                 # daily usage cap ratio before circuit break
  cooldown_429_sec: 300                  # backoff when upstream returns 429
```

Environment variable override pattern (Docker):

```env
GPT2API_APP_BASE_URL=https://api.example.com
GPT2API_SCHEDULER_MIN_INTERVAL_SEC=15
GPT2API_SCHEDULER_COOLDOWN_429_SEC=600
```

---

## Quick Start: First Image Generation

### 1. Add a Proxy

Via admin dashboard → **Proxy Management** → New Proxy, or via API:

```bash
curl -X POST http://localhost:8080/api/admin/proxies \
  -H "Authorization: Bearer $ADMIN_JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "proxy-us-01",
    "url": "http://user:pass@proxy.example.com:8080",
    "type": "http"
  }'
```

SOCKS5 example:
```bash
-d '{"name":"socks-01","url":"socks5://user:pass@proxy.example.com:1080","type":"socks5"}'
```

### 2. Import ChatGPT Accounts

Batch import via admin dashboard → **GPT Accounts** → Batch Import.

Supported formats — JSON session:
```json
[
  {
    "email": "user@example.com",
    "access_token": "$CHATGPT_ACCESS_TOKEN",
    "refresh_token": "$CHATGPT_REFRESH_TOKEN",
    "proxy_id": 1
  }
]
```

Or AT/RT/ST plain text (one per line in the UI).

### 3. Create an API Key

Admin dashboard → **User Management** → select user → **API Keys** → Create Key.

Or programmatically:
```bash
curl -X POST http://localhost:8080/api/user/apikeys \
  -H "Authorization: Bearer $USER_JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my-app-key",
    "rpm_limit": 60,
    "daily_quota": 1000,
    "model_whitelist": ["gpt-image-2", "picture_v2"]
  }'
```

### 4. Generate an Image

```bash
curl -X POST http://localhost:8080/v1/images/generations \
  -H "Authorization: Bearer sk-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-image-2",
    "prompt": "A serene mountain lake at sunset, photorealistic",
    "n": 2,
    "size": "1024x1024"
  }'
```

Response:
```json
{
  "created": 1713456789,
  "data": [
    {
      "url": "https://your-domain.com/p/img/task123/0?exp=1713460389&sig=abc123"
    },
    {
      "url": "https://your-domain.com/p/img/task123/1?exp=1713460389&sig=def456"
    }
  ]
}
```

---

## API Reference

### Image Generation
```
POST /v1/images/generations
```
```json
{
  "model": "gpt-image-2",      // or "picture_v2" for IMG2 grayscale
  "prompt": "your prompt",
  "n": 1,                       // number of images (1-4 recommended)
  "size": "1024x1024",          // "1024x1024" | "1792x1024" | "1024x1792"
  "response_format": "url"      // "url" | "b64_json"
}
```

### Image Edit (img2img)
```
POST /v1/images/edits
Content-Type: multipart/form-data
```
```bash
curl -X POST http://localhost:8080/v1/images/edits \
  -H "Authorization: Bearer sk-your-api-key" \
  -F "image=@input.png" \
  -F "prompt=Make the sky more dramatic" \
  -F "model=gpt-image-2" \
  -F "n=1"
```

### Check Task Status
```
GET /v1/images/tasks/:id
Authorization: Bearer sk-your-api-key
```

### List Models
```
GET /v1/models
Authorization: Bearer sk-your-api-key
```

### Chat Completions (preserved, UI disabled)
```
POST /v1/chat/completions
```
```json
{
  "model": "gpt-4o",
  "messages": [{"role": "user", "content": "Hello"}],
  "stream": true
}
```

---

## Using with OpenAI SDK

### Python
```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ["GPT2API_KEY"],          # your sk- key from the dashboard
    base_url="http://localhost:8080/v1"          # or your production domain
)

# Single image
response = client.images.generate(
    model="gpt-image-2",
    prompt="A futuristic city skyline at night, cyberpunk style",
    n=1,
    size="1024x1024"
)
print(response.data[0].url)

# Batch images
response = client.images.generate(
    model="gpt-image-2",
    prompt="Abstract watercolor painting, vibrant colors",
    n=4,
    size="1024x1792"   # 9:16 portrait
)
for img in response.data:
    print(img.url)
```

### Node.js / TypeScript
```typescript
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.GPT2API_KEY,
  baseURL: process.env.GPT2API_BASE_URL ?? "http://localhost:8080/v1",
});

async function generateImages(prompt: string, count: number = 2) {
  const response = await client.images.generate({
    model: "gpt-image-2",
    prompt,
    n: count,
    size: "1024x1024",
  });
  return response.data.map((img) => img.url);
}

// Image edit
async function editImage(imagePath: string, prompt: string) {
  const fs = await import("fs");
  const response = await client.images.edit({
    image: fs.createReadStream(imagePath),
    prompt,
    model: "gpt-image-2",
  });
  return response.data[0].url;
}
```

### Go
```go
package main

import (
    "context"
    "fmt"
    "os"

    openai "github.com/sashabaranov/go-openai"
)

func main() {
    cfg := openai.DefaultConfig(os.Getenv("GPT2API_KEY"))
    cfg.BaseURL = os.Getenv("GPT2API_BASE_URL") // e.g. "http://localhost:8080/v1"
    client := openai.NewClientWithConfig(cfg)

    resp, err := client.CreateImage(context.Background(), openai.ImageRequest{
        Model:  "gpt-image-2",
        Prompt: "A tranquil Japanese garden with cherry blossoms",
        N:      2,
        Size:   openai.CreateImageSize1024x1024,
    })
    if err != nil {
        panic(err)
    }
    for _, img := range resp.Data {
        fmt.Println(img.URL)
    }
}
```

---

## Key Concepts

### IMG2 Grayscale Hit

IMG2 is a grayscale (A/B test) feature on `chatgpt.com` that returns multiple high-res final images in a single call. The gateway:

1. Sends the generation request
2. Detects `preview_only` in the tool message response
3. Automatically retries up to 3 times within the same conversation to capture IMG2 output
4. Returns all signed image URLs aggregated

Use model `picture_v2` to specifically target the IMG2 grayscale path:
```json
{ "model": "picture_v2", "prompt": "...", "n": 1 }
```

Successful IMG2 hit shows in logs:
```
image runner result summary turns_used=1 is_preview=false signed_count=2
```

### Account Pool Scheduling

The scheduler uses Redis distributed locks to serialize account usage:

- `min_interval_sec`: minimum gap between consecutive uses of the same account
- `daily_usage_ratio`: if an account hits this fraction of its daily limit, it's circuit-broken
- `cooldown_429_sec`: account is cooled down after receiving a 429 from upstream
- Accounts are bound 1:1 to `oai-device-id` / `oai-session-id` fingerprints (stored in DB)

### Image Proxy & Anti-Hotlink

All returned image URLs go through the built-in HMAC-signed proxy:
```
/p/img/:task_id/:index?exp=<unix_timestamp>&sig=<hmac_sha256>
```

This bypasses `chatgpt.com`'s `estuary/content` 403 hotlink protection. The proxy fetches and streams the image server-side when accessed.

### Credit Billing System

- Users have a credit wallet; credits are pre-deducted before generation
- Group multipliers allow VIP / internal / reseller pricing tiers
- Billing settled after successful generation; failed calls are refunded
- EPay (易支付) integration for recharge

---

## Admin Operations

### Account Pool Management

```bash
# Check account statuses via API
curl http://localhost:8080/api/admin/accounts \
  -H "Authorization: Bearer $ADMIN_JWT"

# Manually trigger account token refresh
curl -X POST http://localhost:8080/api/admin/accounts/123/refresh \
  -H "Authorization: Bearer $ADMIN_JWT"

# Bulk import accounts (JSON body)
curl -X POST http://localhost:8080/api/admin/accounts/batch \
  -H "Authorization: Bearer $ADMIN_JWT" \
  -H "Content-Type: application/json" \
  -d @accounts.json
```

### Database Backup & Restore

Via admin dashboard → **Data Backup**, or:

```bash
# Trigger backup
curl -X POST http://localhost:8080/api/admin/backups \
  -H "Authorization: Bearer $ADMIN_JWT"

# List backups
curl http://localhost:8080/api/admin/backups \
  -H "Authorization: Bearer $ADMIN_JWT"

# Download backup
curl http://localhost:8080/api/admin/backups/backup-2026-04-21.sql.gz \
  -H "Authorization: Bearer $ADMIN_JWT" \
  -o backup.sql.gz
```

### User Credit Management

```bash
# Add credits to a user
curl -X POST http://localhost:8080/api/admin/users/42/credits \
  -H "Authorization: Bearer $ADMIN_JWT" \
  -H "Content-Type: application/json" \
  -d '{"amount": 10000, "note": "Manual top-up"}'
```

---

## Directory Structure

```
gpt2api/
├── cmd/server/          # main entry point
├── configs/
│   ├── config.yaml      # main config
│   └── config.example.yaml
├── deploy/
│   ├── docker-compose.yml
│   ├── .env.example
│   └── README.md        # horizontal scaling guide
├── internal/
│   ├── api/             # Gin route handlers
│   ├── chatgpt/         # upstream client (utls, sentinel, SSE parser)
│   ├── scheduler/       # account pool scheduler + Redis leases
│   ├── billing/         # credit wallet + EPay integration
│   ├── proxy/           # proxy pool health checks
│   ├── imgproxy/        # HMAC-signed image proxy
│   └── model/           # DB models + migrations (goose)
├── web/                 # Vue 3 frontend source
└── docs/screenshots/
```

---

## Enabling Chat Completions

The `/v1/chat/completions` route is fully implemented but the UI entry is disabled via a feature flag due to upstream sentinel instability. To re-enable:

```go
// internal/api/routes.go — find the feature flag:
const enableChatCompletions = false   // change to true
```

Rebuild and redeploy:
```bash
docker compose up -d --build server
```

---

## Troubleshooting

### No accounts available / all accounts idle
```bash
# Check account pool status
docker compose logs server | grep "scheduler"

# Common causes:
# 1. min_interval_sec too high — reduce in config
# 2. All accounts in cooldown — check for 429s upstream
# 3. Proxy unhealthy — verify proxy health score in dashboard
```

### Images return 403 when accessed directly
Expected behavior — all image URLs must go through the `/p/img/` proxy. Ensure `base_url` in config matches your actual domain so signed URLs are correct.

### `is_preview=true` in logs (IMG2 not hitting)
The account doesn't have IMG2 grayscale enabled. Either:
- Try different accounts (grayscale is account-specific)
- Use `gpt-image-2` model instead of `picture_v2`
- The gateway retries up to 3 times automatically

### Redis lock timeout errors
```yaml
redis:
  pool_size: 500    # increase if seeing lock contention under high concurrency
```

### Database migration fails on startup
```bash
docker compose exec server goose -dir /app/migrations mysql "$DSN" status
docker compose exec server goose -dir /app/migrations mysql "$DSN" up
```

### TLS fingerprint / JA3 detection
The gateway uses `refraction-networking/utls` to mimic Edge 143 browser TLS fingerprint. If accounts are getting flagged:
- Ensure each account is bound to a dedicated proxy (avoid IP mixing)
- Check `oai-device-id` binding is consistent (stored per-account in DB)
- Rotate accounts that have been flagged

### High memory usage
Reduce connection pool sizes for smaller deployments:
```yaml
mysql:
  max_open_conns: 50
redis:
  pool_size: 50
```

---

## Security Checklist

- [ ] Change default admin password immediately after first login
- [ ] Set strong `JWT_SECRET` (≥32 chars random)
- [ ] Set `CRYPTO_AES_KEY` to exactly 64 hex chars
- [ ] Set strong MySQL passwords
- [ ] Configure `base_url` to your HTTPS domain
- [ ] Set up nginx reverse proxy with TLS in front of `:8080`
- [ ] Configure API key IP whitelists for sensitive keys
- [ ] Enable audit log review in admin dashboard
