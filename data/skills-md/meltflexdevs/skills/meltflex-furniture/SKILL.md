---
name: meltflex-furniture
description: Place specific real furniture or decor products into a room photo using MeltFlex AI. Use when the user wants exact items (a particular sofa, bed, table, lamp) staged into a room while matching their real colors, materials, and proportions. Companion to /meltflex:design.
---

# MeltFlex — Furniture Placement

This skill places **specific products** into a room photo: you provide the room plus one or more reference images of the exact furniture/decor, and MeltFlex composes them into the scene with correct perspective, lighting, and shadows. Same MeltFlex REST API, no extra install.

For general restyling without specific products, use `/meltflex:design`. To turn a photo of a furniture piece into a downloadable **3D model** (GLB), use `/meltflex:3d` (`POST /api/v1/furniture-3d`, 75 credits).

## Prerequisites

A MeltFlex API key (`mf_sk_...`, any active subscription) in `MELTFLEX_API_KEY`. Get one at <https://www.meltflexai.com/settings>. Each generation costs **10 credits** (auto-refunded on failure), billed to the user's account.

## Endpoint

`POST https://www.meltflexai.com/api/v1/generate`

Body:
- `prompt` (string, required) — placement instruction.
- `imageUrl` **or** `image` — the room photo.
- `referenceImageUrls` (string[]) — up to **10** public URLs of the products to place. (Or `referenceImages` as base64 data URLs for local files.)
- `referenceProducts` (object[], optional) — metadata per reference, e.g. `[{"name": "Modular Sofa"}]`, to help placement.
- `resolution` (`"512"|"1K"|"2K"`), `designLevel` (`"lite"|"quick"|"pro"`), `variations` (1–3) — the same optional quality/batch fields as `/meltflex:design`.

Response: `{ "success": true, "image": "data:image/png;base64,...", "images": ["data:..."], "count": 1, "creditsUsed": 10 }`.

## Example

```python
import os, base64, requests

resp = requests.post(
    "https://www.meltflexai.com/api/v1/generate",
    headers={"Authorization": f"Bearer {os.environ['MELTFLEX_API_KEY']}"},
    json={
        "imageUrl": "https://your-cdn.com/empty-room.jpg",
        "prompt": "Place these furniture items naturally in this living room, matching their exact look.",
        "referenceImageUrls": [
            "https://your-cdn.com/modular-sofa.jpg",
            "https://your-cdn.com/oak-coffee-table.jpg"
        ],
        "referenceProducts": [{"name": "Modular Sofa"}, {"name": "Oak Coffee Table"}],
    },
    timeout=180,
)
data = resp.json()
if data.get("success"):
    open("furnished.png", "wb").write(base64.b64decode(data["image"].split(",", 1)[1]))
```

## How to work with the user

1. **Need a room photo + at least one product image.** If the user names a product but gives no image, ask for a photo or URL of it.
2. **Use clean product shots** (white/neutral background) for best matching.
3. **Name the products** in `referenceProducts` so the AI places them correctly.
4. Up to **10** reference items per call. Report the saved path and credits used.
5. Errors behave the same as `/meltflex:design` (402 credits, 401 key, 429 rate, 5xx auto-refund).

## Tips

- Prefer URLs over base64 for both the room and references — faster, avoids the 15 MB limit.
- For multiple items, describe the desired arrangement in the prompt ("sofa against the back wall, coffee table centered").
