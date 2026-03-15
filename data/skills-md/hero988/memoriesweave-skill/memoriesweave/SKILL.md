---
name: memoriesweave
description: Creates and manages photo memory collections on MemoriesWeave via its REST API. Use when the user mentions MemoriesWeave, memory collections, photo wallpapers, photo books, or wants to create/edit digital memories or print products using the MemoriesWeave API. Do not use for general photo editing, image generation, or non-MemoriesWeave tasks.
---

# MemoriesWeave API

Provides programmatic access to MemoriesWeave — a platform for creating photo memory collections with custom HTML layouts. The agent designs HTML layouts and pushes them to memories. The API provides photos, conversations, workspace context, and people data.

## How to call the API

**ALWAYS use `curl` via the Bash tool.** Do not use WebFetch, fetch(), or any other HTTP client — they fail due to redirects and auth header stripping.

```bash
API="https://grandiose-loris-729.eu-west-1.convex.site/api/v1"
KEY="<user-provided-api-key>"

curl -s "$API/ENDPOINT" -H "Authorization: Bearer $KEY"
```

The user provides their API key (format: `mw_sk_<32hex>`) when requesting this skill.

## Workflow: Creating or editing a memory

Follow these steps in order. Do not skip steps.

### Step 1: Lock the memory FIRST

The VERY FIRST API call must be locking the memory. Do this before gathering context, before reading HTML, before anything else. This shows a loading animation on the user's screen immediately.

```bash
curl -s -X POST "$API/memories/{memoryId}/lock" -H "Authorization: Bearer $KEY"
```

If creating a new memory (no memory ID yet), lock it immediately after creation.

### Step 2: Gather context

```bash
# Get workspace list
curl -s "$API/workspaces" -H "Authorization: Bearer $KEY"

# Get workspace context (who the people are, relationship info, instructions)
curl -s "$API/workspaces/{wsId}/context" -H "Authorization: Bearer $KEY"

# Get registered people (names, roles, descriptions)
curl -s "$API/workspaces/{wsId}/persons" -H "Authorization: Bearer $KEY"
```

### Step 3: Save a "before" snapshot

```bash
curl -s -X POST "$API/memories/{memoryId}/snapshots" \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d '{"label": "Before edit — description of planned change"}'
```

### Step 4: Select photos

Use tag filtering as a starting point, then verify with conversation context.

**IMPORTANT: dateFrom and dateTo must be Unix timestamps in milliseconds, NOT date strings.**
Example: July 1, 2025 = `1751328000000`, not `2025-07-01`. Calculate with: `new Date("2025-07-01").getTime()`

```bash
# Filter by tag (e.g. couple, selfie, portrait, traveling)
curl -s "$API/workspaces/{wsId}/photos?tag=couple&limit=50" -H "Authorization: Bearer $KEY"

# Filter by date range (Unix ms timestamps)
curl -s "$API/workspaces/{wsId}/photos?dateFrom=1751328000000&dateTo=1754006400000&limit=50" -H "Authorization: Bearer $KEY"

# If user provides a photo ID, fetch it directly
curl -s "$API/photos/{photoId}" -H "Authorization: Bearer $KEY"

# Get conversation context around a photo (what was happening when it was shared)
curl -s "$API/workspaces/{wsId}/conversations/by-photo/{photoId}" -H "Authorization: Bearer $KEY"
```

**Tags are AI-generated and may be inaccurate.** Use them as a first filter, then verify with conversation context. Do not rely on tags alone.

**Pagination:** If a search doesn't return enough results, check `meta.hasMore` in the response. If `true`, use the `cursor` value to fetch the next batch:

```bash
# First request
curl -s "$API/workspaces/{wsId}/photos?tag=couple&limit=50" -H "Authorization: Bearer $KEY"
# Response includes: "meta": { "cursor": "abc123", "hasMore": true }

# Get next batch using cursor
curl -s "$API/workspaces/{wsId}/photos?tag=couple&limit=50&cursor=abc123" -H "Authorization: Bearer $KEY"
```

Keep paginating until you find what you need or `hasMore` is `false`.

### Step 5: Choose the correct format

```bash
curl -s "$API/digital-formats" -H "Authorization: Bearer $KEY"
```

Common formats: Phone Wallpaper (1170x2532 iPhone 13, 1320x2868 iPhone 16 Pro Max), Desktop (3840x2160), Social Post (1080x1080).

### Step 5b: VERIFY every photo before using it

Before including ANY photo in your design, you MUST verify it exists and get its actual data by calling:

```bash
curl -s "$API/photos/{photoId}" -H "Authorization: Bearer $KEY"
```

**NEVER fabricate, guess, or construct photo URLs.** Every photo URL must come from an actual API response (`urls.original`, `urls.medium`, or `urls.thumbnail`). If a photo search returns no results for a month, report that to the user — do not invent URLs.

**Verification checklist for every photo:**
1. You received the photo ID from the API (not made up)
2. You called `GET /photos/{photoId}` and got a valid response
3. The `dateTaken` field matches the month you're placing it on
4. The `tags` or photo content matches what you expect (couple/selfie/andrea etc.)
5. The `urls.original` URL is what you're putting in the HTML

If the API returns empty results for a time period, try different search strategies:
- Search by `tag=couple`, `tag=selfie`, `tag=andrea` without date range
- Then filter results by `dateTaken` in your code
- Try broader date ranges
- If truly no photos exist for a month, tell the user

### Step 6: Design HTML and push

Design self-contained HTML with inline styles. For multi-page memories, wrap each page in `<div data-mw-page="N">`.

```bash
curl -s -X PATCH "$API/memories/{memoryId}" \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d '{"customHtml": "<div data-mw-page=\"1\" style=\"width:1170px;height:2532px;...\">...</div>"}'
```

When resizing, include `digitalFormat` in the same PATCH:

```bash
curl -s -X PATCH "$API/memories/{memoryId}" \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d '{"customHtml": "...", "digitalFormat": {"category": "phone_wallpaper", "widthPx": 1170, "heightPx": 2532, "outputFormat": "png"}}'
```

### Step 7: Verify ALL images load, then screenshot

Before screenshotting, verify that every image URL in your HTML actually loads. Extract all image URLs from your HTML and spot-check at least 3 by fetching them:

```bash
curl -sI "https://pub-....r2.dev/photos/.../photo.jpg" | head -1
# Should return: HTTP/2 200 (not 404 or 403)
```

If any return 404, you used a fabricated or wrong URL — go back to Step 5b and fix it.

Then take screenshots to verify the design:

```bash
curl -s "https://www.memoriesweave.com/api/screenshot?memoryId={memoryId}&page=1" \
  -H "Authorization: Bearer $KEY"
```

Optional query params: `widthPx` and `heightPx` to override dimensions (useful for physical products where dimensions come from the product specs, not digitalFormat). Example: `&widthPx=3772&heightPx=5250` for wall calendars.

Returns `{ "data": { "screenshotUrl": "https://..." } }`. Download and view the screenshot. Check that:
- All photos are visible (no broken image icons)
- Photos show the correct people/content
- No duplicate-looking photos on the same page
- Text is readable and correctly positioned
- **Captions match the actual photo they appear under** — you cannot determine which photo is in which position from HTML order alone. You MUST screenshot the page and visually confirm that each caption describes the photo it appears next to. Tags can be misleading (e.g. a "couple selfie on a bridge" might be tagged "coffee date" if they were near a cafe).

**When editing captions:** ALWAYS screenshot the page BEFORE changing any caption text. Look at the screenshot to understand which photo is in position 1, 2, and 3. Then match your caption to what you actually see in the screenshot.

### Step 8: Save an "after" snapshot

```bash
curl -s -X POST "$API/memories/{memoryId}/snapshots" \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d '{"label": "After edit — description of what changed"}'
```

### Step 9: Unlock the memory

This removes the loading animation from the user's screen.

```bash
curl -s -X POST "$API/memories/{memoryId}/unlock" -H "Authorization: Bearer $KEY"
```

**Always unlock when done**, even if an error occurred.

## Product-specific rules

**Wall calendars** MUST always have exactly **14 pages**: cover + 12 months (Jan-Dec) + back page. Each month page needs a correct calendar grid with proper day-of-week starts. Dimensions: `3772x5250px`. Never use duplicate photos across pages. Every photo on relationship months must show the people (not food, scenery, or screenshots).

**Phone wallpapers** support up to 10 pages. Each page is a standalone wallpaper at the device's resolution.

## Photo selection rules

1. **Always check conversation context** around candidate photos before selecting them.
2. **If user provides a photo ID**, use it directly via `GET /photos/{photoId}`.
3. **Prefer** tags: `couple`, `selfie`, `portrait`, `andrea`, `suliman`, `romantic`, `joyful`, `traveling`.
4. **Avoid** tags: `food`, `screenshot`, `meme`, `document`, `sticker`, `illustration` (unless requested).
5. **Prefer portrait orientation** (height > width) for phone wallpapers.
6. Use `urls.original` for high-resolution output, `urls.medium` for web display.
7. **No duplicate or visually similar photos on the same page or across pages.** Check the `fileName` field — it contains a timestamp like `00013190-PHOTO-2025-09-27-19-46-12.jpg`. If two photos have timestamps within **5 minutes** of each other, they are from the same event/session and look nearly identical (e.g. two photobooth strips from the same booth, two selfies at the same spot). When placing multiple photos on the same page, ensure each photo is from a **different date or different event** (timestamps at least 1 hour apart).
8. **Cover and back pages must use unique photos** not used on any month page.
9. **Each month's photos must be from that actual month.** Check the `dateTaken` timestamp. Do not use April photos on the August page.
10. **Use the earliest occurrence of a photo.** Photos in WhatsApp are sometimes resent months later. The `dateTaken` field reflects when the photo was originally taken, NOT when it was shared in the chat. When filtering by date range, a photo taken in July may appear in a December conversation chunk because it was resent. Always use `dateTaken` to determine which month a photo belongs to — if `dateTaken` says July, it goes on the July page, never December, even if it was found in a December conversation search.

## Photo URLs

Each photo has three variants:
- `urls.thumbnail` — 300px wide WebP
- `urls.medium` — 800px wide WebP
- `urls.original` — Full resolution

## Slideshow / Digital Frame Video Export

Render multi-page digital memories as MP4 videos with Ken Burns effects and transitions. Only available for digital memories (not physical products). The rendered video includes AI quality review via Gemini.

### Workflow

1. Design a multi-page memory first (at least 2 pages with `data-mw-page`)
2. Configure the slideshow:
   ```bash
   curl -s -X POST "$API/memories/{memoryId}/slideshow/render" \
     -H "Authorization: Bearer $KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "resolution": "1920x1080",
       "reviewModel": "google/gemini-3-flash-preview",
       "slides": [
         {"page": 1, "durationSeconds": 6, "kenBurns": {"direction": "zoom_in_center", "intensity": 0.3}, "transition": {"type": "crossfade", "durationSeconds": 1.5}},
         {"page": 2, "durationSeconds": 5, "kenBurns": {"direction": "pan_left", "intensity": 0.5}, "transition": {"type": "fade_black", "durationSeconds": 2.0}},
         {"page": 3, "durationSeconds": 7, "kenBurns": {"direction": "zoom_out_center", "intensity": 0.3}}
       ]
     }'
   ```
3. Poll for completion:
   ```bash
   curl -s "$API/memories/{memoryId}/slideshow" -H "Authorization: Bearer $KEY"
   ```
4. When status is "completed", download the video from the `videoUrl` field
5. Read the `reviewFeedback` for quality assessment
6. If issues are identified, adjust the config and re-render

### Ken Burns Directions
| Direction | Description | Best for |
|-----------|-------------|----------|
| zoom_in_center | Slow zoom into center | Portraits, close-ups |
| zoom_out_center | Start zoomed, pull out | Group shots, landscapes |
| pan_left | Pan from right to left | Wide scenes, landscapes |
| pan_right | Pan from left to right | Wide scenes |
| pan_up | Pan from bottom to top | Tall subjects |
| pan_down | Pan from top to bottom | Tall subjects |
| none | No motion (static) | Text-heavy slides |

### Transition Types
| Type | FFmpeg Effect | Feel |
|------|--------------|------|
| crossfade | Dissolve | Classic, elegant |
| fade_black | Fade to black | Chapter break |
| fade_white | Fade to white | Dreamy |
| slide_left | Slide left | Timeline progression |
| slide_right | Slide right | Reverse timeline |
| circle_open | Circle reveal | Nostalgic, vintage |
| dissolve | Pixel dissolve | Soft, organic |
| wipe_right | Wipe right | Clean, modern |

### Resolutions
| Resolution | Label | Best for |
|-----------|-------|----------|
| 1920x1080 | Full HD | Digital frames, Chromecast, most TVs |
| 3840x2160 | 4K UHD | Samsung Frame TV, 4K displays |

### Pricing
- **Rendering:** Free (compute only, no AI cost)
- **AI Review:** Gemini Flash ~$0.04/review, Gemini Pro ~$0.10/review (credits deducted with 2x markup)

## Endpoint reference

### Account
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/me` | User info and plan |
| GET | `/me/credits` | Credit balance |
| GET | `/me/usage` | Usage summary |

### Workspaces
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/workspaces` | List workspaces |
| GET | `/workspaces/:id` | Workspace details |
| GET | `/workspaces/:id/context` | AI context (description, relationship, instructions) |
| GET | `/workspaces/:id/persons` | Registered people |

### Photos
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/workspaces/:wsId/photos` | List photos. Params: `cursor`, `limit`, `tag`, `dateFrom`, `dateTo` |
| GET | `/photos/:id` | Single photo details and URLs |
| PATCH | `/photos/:id` | Update caption or tags |

### Memories
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/workspaces/:wsId/memories` | List memories |
| GET | `/memories/:id` | Memory details |
| POST | `/workspaces/:wsId/memories` | Create memory. Body: `title`, `description`, optional `digitalFormat` |
| PATCH | `/memories/:id` | Update `title`, `description`, `customHtml`, or `digitalFormat` |
| DELETE | `/memories/:id` | Delete memory |
| GET | `/memories/:id/html` | Get rendered HTML |
| POST | `/memories/:id/lock` | Show AI working overlay on frontend |
| POST | `/memories/:id/unlock` | Remove AI working overlay |
| GET | `/memories/:id/snapshots` | List version history |
| POST | `/memories/:id/snapshots` | Create snapshot. Body: `{"label": "..."}` |
| POST | `/memories/:id/snapshots/:snapId/restore` | Restore a previous version |

### Conversations
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/workspaces/:wsId/conversations` | List chat chunks |
| GET | `/workspaces/:wsId/conversations/search?start=TS&end=TS` | Search by date range |
| GET | `/workspaces/:wsId/conversations/by-photo/:photoId` | Messages around a photo |

### Formats and products
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/digital-formats` | All format presets with dimensions |
| GET | `/products` | Print product catalog |

### Slideshow (digital memories only)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/memories/:id/slideshow/render` | Trigger slideshow video render with Ken Burns + transitions |
| GET | `/memories/:id/slideshow` | Get slideshow render status + video download URL |
| GET | `/slideshow/presets` | List available Ken Burns, transition, and resolution presets |

### Screenshot (uses website domain, not API domain)
| Method | URL | Description |
|--------|-----|-------------|
| GET | `https://www.memoriesweave.com/api/screenshot?memoryId=X&page=N` | Render page to JPEG |

## Pricing

- **Free:** All GET endpoints, CRUD operations, pushing HTML, snapshots, lock/unlock.
- **Credits:** AI operations only (design chat, content generation, photo captioning via Trigger.dev pipeline). The agent designing HTML does not consume credits.

## Rate limits

| Plan | Requests/min | AI ops/min |
|------|-------------|-----------|
| Free | 10 | 2 |
| Starter | 30 | 5 |
| Plus | 60 | 10 |
| Pro | 120 | 20 |

## Error codes

| Code | Status | Meaning |
|------|--------|---------|
| `bad_request` | 400 | Invalid parameters |
| `unauthorized` | 401 | Missing or invalid API key |
| `not_found` | 404 | Resource not found |
| `rate_limited` | 429 | Too many requests |
| `internal_error` | 500 | Server error |
