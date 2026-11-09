---
name: bfl-api
description: BFL FLUX API integration guide covering endpoints, async polling patterns, rate limiting, error handling, webhooks, and regional endpoints with Python and TypeScript code examples.
metadata:
  author: Black Forest Labs
  version: "1.0.0"
  tags: flux, bfl, api, integration, webhooks, rate-limiting
---

# BFL API Integration Guide

Use this skill when integrating BFL FLUX APIs into applications for image generation, editing, and processing.

## First: Check API Key

**Before generating images, verify your API key is set:**

```bash
echo $BFL_API_KEY
```

If empty or you see "Not authenticated" errors, see [API Key Setup](#api-key-setup) below.

## Important: Image URLs Expire in 10 Minutes

Result URLs from the API are temporary. Download images immediately after generation completes - do not store or cache the URLs themselves.

## When to Use

- Setting up BFL API client
- Implementing async polling patterns
- Handling rate limits and errors
- Configuring webhooks for production
- Selecting regional endpoints
- Building production-ready integrations

## Quick Reference

### Base Endpoints

| Region | Endpoint                | Use Case                    |
| ------ | ----------------------- | --------------------------- |
| Global | `https://api.bfl.ai`    | Default, automatic failover |
| EU     | `https://api.eu.bfl.ai` | GDPR compliance             |
| US     | `https://api.us.bfl.ai` | US data residency           |

### Model Endpoints & Pricing

> **Credit pricing:** 1 credit = $0.01 USD. FLUX.2 uses megapixel-based pricing (cost scales with resolution).

#### FLUX.2 Models

| Model             | Path                  | 1st MP | +MP  | 1MP T2I | 1MP I2I | Best For                           |
| ----------------- | --------------------- | ------ | ---- | ------- | ------- | ---------------------------------- |
| FLUX.2 [klein] 4B | `/v1/flux-2-klein-4b` | 1.4c   | 0.1c | $0.014  | $0.015  | Real-time, high volume             |
| FLUX.2 [klein] 9B | `/v1/flux-2-klein-9b` | 1.5c   | 0.2c | $0.015  | $0.017  | Balanced quality/speed             |
| FLUX.2 [pro]      | `/v1/flux-2-pro`      | 3c     | 1.5c | $0.03   | $0.045  | Production, fast turnaround        |
| FLUX.2 [max]      | `/v1/flux-2-max`      | 7c     | 3c   | $0.07   | $0.10   | Maximum quality                    |
| FLUX.2 [flex]     | `/v1/flux-2-flex`     | 5c     | 5c   | $0.05   | $0.10   | Typography, adjustable controls    |
| FLUX.2 [dev]      | -                     | -      | -    | Free    | Free    | Local development (non-commercial) |

> **Pricing formula:** `(firstMP + (outputMP-1) * mpPrice) + (inputMP * mpPrice)` in cents

#### FLUX.1 Models

| Model                | Path                     | Price/Image | Best For                      |
| -------------------- | ------------------------ | ----------- | ----------------------------- |
| FLUX.1 Kontext [pro] | `/v1/flux-kontext`       | $0.04       | Image editing with context    |
| FLUX.1 Kontext [max] | `/v1/flux-kontext-max`   | $0.08       | Max quality editing           |
| FLUX1.1 [pro]        | `/v1/flux-pro-1.1`       | $0.04       | Standard T2I, fast & reliable |
| FLUX1.1 [pro] Ultra  | `/v1/flux-pro-1.1-ultra` | $0.06       | Ultra high-resolution         |
| FLUX1.1 [pro] Raw    | `/v1/flux-pro-1.1-raw`   | $0.06       | Candid photography feel       |
| FLUX.1 Fill [pro]    | `/v1/flux-pro-1.0-fill`  | $0.05       | Inpainting                    |

> **Tip:** All FLUX.2 models support image editing via the `input_image` parameter - no separate editing endpoint needed. Use [bfl.ai/pricing](https://bfl.ai/pricing) calculator for exact costs at different resolutions.

### Image Input for Editing

**Preferred: Use URLs directly** - simpler and more convenient than base64.

**Single image editing:**

```bash
curl -X POST "https://api.bfl.ai/v1/flux-2-pro" \
  -H "x-key: $BFL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Change the background to a sunset",
    "input_image": "https://example.com/photo.jpg"
  }'
```

**Multi-reference editing:**

```bash
curl -X POST "https://api.bfl.ai/v1/flux-2-pro" \
  -H "x-key: $BFL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "The person from image 1 in the environment from image 2",
    "input_image": "https://example.com/person.jpg",
    "input_image_2": "https://example.com/background.jpg"
  }'
```

The API fetches URLs automatically. Both URL and base64 work, but URLs are recommended when available.

### Multi-Reference I2I

FLUX.2 models support multiple input images for combining elements, style transfer, and character consistency:

| Model                 | Max References |
| --------------------- | -------------- |
| FLUX.2 [klein]        | 4 images       |
| FLUX.2 [pro/max/flex] | 8 images       |

**Parameters:** `input_image`, `input_image_2`, `input_image_3`, ... `input_image_8`

**Prompt pattern:** Reference images by number in your prompt:

- "The subject from image 1 in the environment from image 2"
- "Apply the style of image 2 to the scene in image 1"
- "The person from image 1 wearing the outfit from image 2, in the pose from image 3"

> For detailed multi-reference patterns (character consistency, style transfer, pose guidance), see `flux-best-practices/rules/multi-reference-editing.md`

### Rate Limits

| Tier                      | Concurrent Requests |
| ------------------------- | ------------------- |
| Standard (most endpoints) | 24                  |

### Polling vs Webhooks

| Approach     | Use When                                                                             |
| ------------ | ------------------------------------------------------------------------------------ |
| **Polling**  | Scripts, CLI tools, local development, single requests, simple integrations          |
| **Webhooks** | Production apps, high volume, server-to-server, when you need immediate notification |

**Start with polling** - it's simpler and works everywhere. Switch to webhooks when you need to scale or want event-driven architecture.

### Key Behaviors

- **Polling**: Response includes `polling_url` for async results
- **URL Expiration**: Result URLs expire after 10 minutes
- **Webhook Support**: Configure `webhook_url` for production workloads

## API Key Setup

**Required**: The `BFL_API_KEY` environment variable must be set before using the API.

### Quick Check

```bash
echo $BFL_API_KEY
```

### If Not Set

1. **Get a key**: Go to https://dashboard.bfl.ai/get-started → Click **"Create Key"** → Select organization
2. **Save to `.env`** (recommended for persistence):
   ```bash
   echo 'BFL_API_KEY=bfl_your_key_here' >> .env
   echo '.env' >> .gitignore  # Don't commit secrets
   ```

See [references/api-key-setup.md](references/api-key-setup.md) for detailed setup instructions.

## Authentication

```bash
x-key: YOUR_API_KEY
```

## Basic Request Flow

```
1. POST request to model endpoint
   └─> Response: { "polling_url": "..." }

2. GET polling_url (repeat until complete)
   └─> Response: { "status": "Pending" | "Ready" | "Error", ... }

3. When Ready, download result URL
   └─> URL expires in 10 minutes - download immediately
```

## Related

- **Prompting best practices** (T2I, I2I, typography, colors): see the **flux-best-practices** skill
- **Multi-reference patterns** (character consistency, style transfer, pose guidance): see `flux-best-practices/rules/multi-reference-editing.md`

## References

- [references/api-key-setup.md](references/api-key-setup.md) - **API key creation and configuration**
- [references/endpoints.md](references/endpoints.md) - Complete endpoint documentation
- [references/polling-patterns.md](references/polling-patterns.md) - Async polling implementation
- [references/rate-limiting.md](references/rate-limiting.md) - Rate limit handling strategies
- [references/error-handling.md](references/error-handling.md) - Error codes and recovery
- [references/webhook-integration.md](references/webhook-integration.md) - Webhook setup and security

### Code Examples

> **Note:** cURL examples are preferred by default as they work universally without requiring Python or Node.js. Use language-specific clients when building production applications.

- [references/code-examples/curl-examples.sh](references/code-examples/curl-examples.sh) - **cURL examples (recommended)**
- [references/code-examples/python-client.py](references/code-examples/python-client.py) - Python client
- [references/code-examples/typescript-client.ts](references/code-examples/typescript-client.ts) - TypeScript client

## Quick Start Example

### 1. Submit Generation Request

```bash
curl -s -X POST "https://api.bfl.ai/v1/flux-2-pro" \
  -H "x-key: $BFL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "A serene mountain landscape at sunset", "width": 1024, "height": 1024}'
```

Response:

```json
{ "id": "abc123", "polling_url": "https://api.bfl.ai/v1/get_result?id=abc123" }
```

### 2. Poll for Result

```bash
curl -s "POLLING_URL" -H "x-key: $BFL_API_KEY"
```

Response when ready:

```json
{ "status": "Ready", "result": { "sample": "https://...", "seed": 1234 } }
```

### 3. Download Image

```bash
curl -s -o output.png "IMAGE_URL"
```

> **Tip:** Result URLs expire in 10 minutes. Download immediately after status becomes `Ready`.

### 4. Multi-Reference Example

Combine elements from multiple images:

```bash
curl -s -X POST "https://api.bfl.ai/v1/flux-2-pro" \
  -H "x-key: $BFL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "The cat from image 1 sitting in the cozy room from image 2",
    "input_image": "https://example.com/cat.jpg",
    "input_image_2": "https://example.com/room.jpg",
    "width": 1024,
    "height": 1024
  }'
```

Reference images by number in your prompt. See [Multi-Reference I2I](#multi-reference-i2i) for limits and patterns.
