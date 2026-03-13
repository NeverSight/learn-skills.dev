---
name: logokit
description: "Generate AI-powered logos via the LogoKit API. Use when the user asks to create a logo, brand identity, or icon for their project."
---

# LogoKit - AI Logo Generation

Generate professional logos through the LogoKit API. This skill handles the full workflow: creating a logo generation job, polling for completion, and downloading the final assets.

## Prerequisites

- A LogoKit API key (obtain from the LogoKit dashboard at https://logokit.app)
- Credits purchased on the dashboard (1 logo generation = 1 credit)

## Configuration

Set the API key as an environment variable:

```bash
export LOGOKIT_API_KEY="lk_your_api_key_here"
```

Or pass it directly in the Authorization header.

## API Base URL

```
https://api.logokit.app
```

## Workflow

### Step 0: Check Credit Balance

Before generating, check if the user has enough credits:

```bash
curl https://api.logokit.app/v1/credits \
  -H "Authorization: Bearer $LOGOKIT_API_KEY"
```

**Response:**
```json
{
  "credits": 10,
  "purchaseUrl": "https://logokit.app",
  "apiVersion": "v1"
}
```

If `credits` is 0, **stop and tell the user**: "クレジットがありません。こちらからクレジットを購入してください: https://logokit.app"

### Step 1: Create a Logo Generation Job

```bash
curl -X POST https://api.logokit.app/v1/logo-jobs \
  -H "Authorization: Bearer $LOGOKIT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "brandName": "Acme Corp",
    "category": "SaaS",
    "style": "Minimal",
    "color": { "type": "auto" },
    "markType": "IconWordmark"
  }'
```

**Response (201):**
```json
{
  "jobId": "job_abc123",
  "state": "pending",
  "createdAt": "2026-01-01T00:00:00.000Z",
  "apiVersion": "v1"
}
```

### Step 2: Poll for Completion

```bash
curl https://api.logokit.app/v1/logo-jobs/{jobId} \
  -H "Authorization: Bearer $LOGOKIT_API_KEY"
```

Poll every 3-5 seconds. The job progresses through states: `pending` → `processing` → `completed`.

**Response when completed:**
```json
{
  "job": {
    "jobId": "job_abc123",
    "state": "completed",
    "progress": 100,
    "createdAt": "2026-01-01T00:00:00.000Z",
    "input": { "brandName": "Acme Corp", "..." : "..." },
    "candidates": [
      {
        "candidateId": "cand_xyz",
        "assets": {
          "squarePng": "https://...",
          "wordmarkPng": "https://...",
          "trimmedPng": "https://...",
          "svg": "https://..."
        }
      }
    ]
  },
  "apiVersion": "v1"
}
```

### Step 3: Generate Derivative Assets (favicon, SNS icons)

After the logo job completes, trigger derivative generation for the selected candidate:

```bash
curl -X POST https://api.logokit.app/v1/downloads/{jobId}/{candidateId}/derivatives \
  -H "Authorization: Bearer $LOGOKIT_API_KEY"
```

**Response:**
```json
{
  "status": "generated",
  "derivativeCount": 6,
  "apiVersion": "v1"
}
```

This endpoint is idempotent — if derivatives are already generated, it returns `"status": "already_generated"`.

### Step 4: List Available Assets

```bash
curl https://api.logokit.app/v1/downloads/{jobId}/{candidateId} \
  -H "Authorization: Bearer $LOGOKIT_API_KEY"
```

**Response (after derivatives are generated):**
```json
{
  "jobId": "job_abc123",
  "candidateId": "cand_xyz",
  "assets": [
    { "type": "square", "filename": "square.png", "url": "https://...", "category": "base", "description": "Square logo (1024x1024)" },
    { "type": "wordmark", "filename": "wordmark.png", "url": "https://...", "category": "base", "description": "Wordmark logo" },
    { "type": "trimmed", "filename": "trimmed.png", "url": "https://...", "category": "base", "description": "Trimmed logo (transparent padding removed)" },
    { "type": "svg", "filename": "logo.svg", "url": "https://...", "category": "base", "description": "Vector logo (SVG)" },
    { "type": "favicon-16x16", "filename": "favicon-16x16.png", "url": "https://...", "category": "favicon", "description": "Browser tab favicon (small)" },
    { "type": "favicon-32x32", "filename": "favicon-32x32.png", "url": "https://...", "category": "favicon", "description": "Browser tab favicon (standard)" },
    { "type": "apple-touch-icon", "filename": "apple-touch-icon.png", "url": "https://...", "category": "favicon", "description": "iOS home screen icon" },
    { "type": "android-chrome-192x192", "filename": "android-chrome-192x192.png", "url": "https://...", "category": "favicon", "description": "Android home screen icon" },
    { "type": "android-chrome-512x512", "filename": "android-chrome-512x512.png", "url": "https://...", "category": "favicon", "description": "Android splash screen icon" },
    { "type": "sns-icon", "filename": "sns-icon.png", "url": "https://...", "category": "sns", "description": "SNS profile icon" }
  ],
  "apiVersion": "v1"
}
```

Note: Base assets vary per candidate — not all include `trimmed` or `svg`. Derivative assets appear only after Step 3.

### Step 5: Download All Assets

There is no bulk download endpoint. Download each asset individually by type.

**Directory structure**: `logos/{jobId}/{candidateId}/` per candidate, with subdirectories by category.

```bash
# Download a single asset
curl -o logo-square.png \
  https://api.logokit.app/v1/downloads/{jobId}/{candidateId}/square \
  -H "Authorization: Bearer $LOGOKIT_API_KEY"
```

**To download all assets for a candidate**, use the asset list from Step 4:

```bash
# Example: download all assets for a candidate
BASE_DIR="logos/{jobId}/{candidateId}"
mkdir -p "${BASE_DIR}"/{logo,favicon,sns}

# Base assets
for asset in square wordmark trimmed svg; do
  curl -sf -o "${BASE_DIR}/logo/${asset}.png" \
    "https://api.logokit.app/v1/downloads/{jobId}/{candidateId}/${asset}" \
    -H "Authorization: Bearer $LOGOKIT_API_KEY" \
    && echo "Downloaded ${asset}" \
    || echo "Skipped ${asset} (not available)"
done

# Favicon assets
for asset in favicon-16x16 favicon-32x32 apple-touch-icon android-chrome-192x192 android-chrome-512x512; do
  curl -sf -o "${BASE_DIR}/favicon/${asset}.png" \
    "https://api.logokit.app/v1/downloads/{jobId}/{candidateId}/${asset}" \
    -H "Authorization: Bearer $LOGOKIT_API_KEY" \
    && echo "Downloaded ${asset}" \
    || echo "Skipped ${asset} (not available)"
done

# SNS assets
curl -sf -o "${BASE_DIR}/sns/sns-icon.png" \
  "https://api.logokit.app/v1/downloads/{jobId}/{candidateId}/sns-icon" \
  -H "Authorization: Bearer $LOGOKIT_API_KEY" \
  && echo "Downloaded sns-icon" \
  || echo "Skipped sns-icon (not available)"
```

**Resulting directory structure:**
```
logos/
└── {jobId}/
    ├── {candidateId-1}/
    │   ├── logo/
    │   │   ├── square.png
    │   │   ├── wordmark.png
    │   │   ├── trimmed.png
    │   │   └── logo.svg
    │   ├── favicon/
    │   │   ├── favicon-16x16.png
    │   │   ├── favicon-32x32.png
    │   │   ├── apple-touch-icon.png
    │   │   ├── android-chrome-192x192.png
    │   │   └── android-chrome-512x512.png
    │   └── sns/
    │       └── sns-icon.png
    ├── {candidateId-2}/
    │   └── ...
    └── {candidateId-3}/
        └── ...
```

## Brand Brief Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `brandName` | string | Yes | Brand name (1-100 chars) |
| `category` | enum | Yes | `SaaS`, `Restaurant`, `Personal`, `EC`, `Creator`, `Other` |
| `style` | enum | Yes | `Minimal`, `Bold`, `Playful`, `Elegant`, `Tech`, `Retro` |
| `color` | object | Yes | Color config (see below) |
| `markType` | enum | Yes | `Wordmark`, `IconWordmark` |
| `tagline` | string | No | Tagline (max 200 chars) |
| `keywords` | string[] | No | Up to 3 keywords (each max 50 chars) |
| `ngItems` | string | No | Things to avoid (max 500 chars) |

### Color Configuration

```json
// Auto - let AI choose
{ "type": "auto" }

// Named palette
{ "type": "palette", "value": "ocean" }

// Specific hex color
{ "type": "hex", "value": "#FF5733" }
```

## Asset Types

**Base assets** (availability varies per candidate):
- `square` - Square logo (1024x1024 PNG)
- `wordmark` - Wordmark logo (PNG)
- `trimmed` - Trimmed logo, transparent padding removed (PNG) — may not be present
- `svg` - Vector logo (SVG) — may not be present

**Derivative assets** (generated via `POST .../derivatives`, then downloadable):
- `favicon-16x16` - Browser tab favicon, small (16x16 PNG)
- `favicon-32x32` - Browser tab favicon, standard (32x32 PNG)
- `apple-touch-icon` - iOS home screen icon (180x180 PNG)
- `android-chrome-192x192` - Android home screen icon (192x192 PNG)
- `android-chrome-512x512` - Android splash screen icon (512x512 PNG)
- `sns-icon` - SNS profile icon (1024x1024 PNG)

## Error Handling

| Status | Meaning | Action |
|--------|---------|--------|
| 400 | Invalid request / validation error | Fix request body |
| 402 | Insufficient credits | Tell user to purchase credits at https://logokit.app |
| 403 | Forbidden / insufficient scope | Check API key permissions |
| 429 | Rate limited | Wait and retry (check `Retry-After` header) |
| 503 | Service unavailable | Retry after a few seconds |

## Guidelines for AI Agents

1. **Always check credits first** - call `GET /v1/credits` before generating. If credits are 0, tell the user to purchase at the `purchaseUrl` returned in the response. Do NOT attempt generation with 0 credits.
2. **Ask the user interactively** - use question/prompt tools (e.g., `AskUserQuestion`, `ask_followup_question`) to gather brand details before generating. Ask the following in a single prompt if your tool supports multiple questions:
   - **Brand name** (free text input)
   - **Category**: `SaaS`, `Restaurant`, `Personal`, `EC`, `Creator`, `Other` — infer from project context if possible and present as the recommended default
   - **Style**: `Minimal` (recommended default), `Bold`, `Playful`, `Elegant`, `Tech`, `Retro`
   - **Mark type**: `IconWordmark` (recommended default), `Wordmark`
   - **Color**: default to `auto` unless the user has a preference. Options: `auto` (AI chooses), palette name, or specific hex code
   - **Tagline** (optional, free text)
   - **Keywords** (optional, up to 3)
3. **Default to** `"color": { "type": "auto" }` and `"markType": "IconWordmark"` unless the user specifies otherwise.
4. **Poll patiently** - logo generation takes 15-60 seconds. Poll every 5 seconds and inform the user it's in progress.
5. **Generate derivatives after completion** - once the logo job completes, call `POST /v1/downloads/:jobId/:candidateId/derivatives` for each candidate to generate favicons and SNS icons. This is idempotent and safe to call multiple times.
6. **Retry derivative generation on failure** - if the derivatives endpoint returns a 500 or other server error, wait 3 seconds and retry up to 2 more times (3 attempts total). Log which candidates succeeded and which failed after all retries are exhausted.
7. **Download all assets by default** - after derivatives are generated, list assets (Step 4) and download all available ones. Save into `logos/{jobId}/{candidateId}/` with subdirectories `logo/`, `favicon/`, `sns/`. No need to ask which to download unless the user specifies.
8. **Handle missing assets** - not all candidates have `trimmed` or `svg`. Skip gracefully if an asset returns 404.
9. **Handle 402 gracefully** - if credits are insufficient despite the check, direct the user to https://logokit.app to purchase more.
