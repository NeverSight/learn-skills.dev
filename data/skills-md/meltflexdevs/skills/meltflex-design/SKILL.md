---
name: meltflex-design
description: Generate photorealistic interior and exterior redesigns from a photo using MeltFlex AI. Use when the user wants to restyle, redesign, declutter, virtually stage, or re-theme a room, facade, or garden; swap a floor, wall finish, staircase, doors or windows; redesign a kitchen or bathroom; turn a 3D draft into a photo; or preview a space in a different style, material, or season. Can also produce a cinematic video walkthrough; for 3D models and 3D worlds see the companion skill meltflex-3d. Works directly against the MeltFlex REST API — no extra install required.
---

# MeltFlex — AI Interior Design

MeltFlex turns a real photo of a space into a redesigned, photorealistic result. This skill calls the MeltFlex REST API directly, so it works in any agent without installing anything else. (If the `meltflex-mcp` server is configured, prefer its `generate_interior` tool — it handles file I/O for you.)

To place **specific furniture products** into a room, use the companion skill `/meltflex:furniture`. For 3D output (a furniture GLB, a floorplan model, an explorable 3D world), use `/meltflex:3d`.

## Prerequisites

The user needs a MeltFlex API key (`mf_sk_...`), available on an active subscription at <https://www.meltflexai.com/settings>. Expect it in the `MELTFLEX_API_KEY` environment variable. If missing, ask them to set it:

```bash
export MELTFLEX_API_KEY="mf_sk_..."
```

Each generation costs **10 credits**, deducted upfront and auto-refunded on failure. Credits belong to the user's account.

## The one endpoint

`POST https://www.meltflexai.com/api/v1/generate`

Headers: `Authorization: Bearer $MELTFLEX_API_KEY`, `Content-Type: application/json`.

Body:
- `prompt` (string, required) — the redesign instruction.
- `imageUrl` (string) **or** `image` (base64 data URL) — the source photo. Prefer `imageUrl`.
- `resolution` (string, optional) — output quality: `"512"`, `"1K"`, or `"2K"` (sharpest). Defaults to model auto.
- `designLevel` (string, optional) — `"lite"` (faster & cheaper, −2 credits), `"quick"` (default), or `"pro"` (most detailed, HIGH thinking, +5 credits).
- `mask` (boolean, optional) — region edit. When `true`, the source image must have the area to change painted **solid red**; the prompt is applied only to those red-marked regions and the rest is preserved. Use for "change only this part".
- `variations` (number, optional) — batch of `1`–`3` images in one call (default 1). Charged per image; failed variations are refunded.

Response: `{ "success": true, "image": "data:...", "images": ["data:..."], "count": 1, "creditsUsed": 10 }`.

## Modes

Every mode is the same endpoint with a mode-tuned prompt. Pick the mode that matches the request and lead the prompt with it.

| Mode | What it's for | Prompt lead-in |
|------|---------------|----------------|
| `restyle` | Change a room's style/theme | "Redesign this room in <style>: …" |
| `virtual_staging` | Furnish an empty room | "Furnish this empty room as a <style> <room type>: …" |
| `layout_boost` | Rearrange existing furniture | "Rearrange the existing furniture into a more open, functional layout; keep the same pieces" |
| `declutter` | Clean up / depersonalize | "Declutter and tidy this room, keep the layout, neutral staging" |
| `exterior` | Building facade / house exterior | "Redesign this house exterior in <style>, keep structure" |
| `garden` | Landscaping / outdoor | "Redesign this garden: <plants, paving, mood>" |
| `wall_texture` | Change wall material/finish | "Change the walls to <material/color>, keep everything else" |
| `floor_restyle` | Change flooring | "Replace the floor with <material>, keep everything else" |
| `stairs` | Restyle a staircase in place | "Restyle the staircase (<treads, railing>), keep its position and surroundings" |
| `doors` | Swap interior doors | "Replace the doors with <style>, keep the walls and flooring" |
| `windows` | Swap window frames/glazing | "Change the windows to <frame/glazing>, keep the wall openings" |
| `kitchen` | Whole kitchen redesign | "Redesign this kitchen in <style>, keep the footprint and plumbing" |
| `bathroom` | Whole bathroom redesign | "Redesign this bathroom in <style>, keep the layout and plumbing" |
| `photo_to_render` | Draft / SketchUp → photo | "Turn this 3D draft into a photorealistic photograph, keep the geometry and camera" |
| `seasonal` | Lighting / season variation | "Show this room at <time of day / season> with <lighting>" |
| `region_edit` | Change only one marked area | Send `mask: true` with the region painted **solid red** in the image; "Put <thing> in the red area, keep the rest" |

For surface- and fixture-swap modes (`wall_texture`, `floor_restyle`, `stairs`, `doors`, `windows`), you can attach the target material or product as a reference image (`referenceImageUrls`) to match it exactly — see `/meltflex:furniture` for the reference mechanic.

Always preserve room structure (walls, windows, doors, flooring) **unless** the mode is explicitly about changing it.

## How to run it

Use a small script so you can decode the base64 result to a file (Python example):

```python
import os, base64, requests

resp = requests.post(
    "https://www.meltflexai.com/api/v1/generate",
    headers={"Authorization": f"Bearer {os.environ['MELTFLEX_API_KEY']}"},
    json={
        "imageUrl": "https://your-cdn.com/empty-room.jpg",
        "prompt": "Redesign in warm Scandinavian style: light oak floor, beige linen sofa, soft daylight. Preserve windows and walls.",
    },
    timeout=180,
)
data = resp.json()
if data.get("success"):
    open("redesign.png", "wb").write(base64.b64decode(data["image"].split(",", 1)[1]))
    print("Saved redesign.png")
else:
    print("Error:", data.get("error") or data.get("message"))
```

For a **local** source photo, send it as a data URL in `image` instead of `imageUrl`:

```python
import base64, mimetypes
path = "living-room.jpg"
mime = mimetypes.guess_type(path)[0] or "image/jpeg"
b64 = base64.b64encode(open(path, "rb").read()).decode()
body = {"image": f"data:{mime};base64,{b64}", "prompt": "..."}
```

## How to work with the user

1. **Always need a source photo.** MeltFlex restyles an existing photo — it does not invent spaces from scratch. If the user gives only a description, ask for a file path or URL.
2. **Pick a mode**, then write a **specific** prompt — materials, colors, furniture, lighting, mood. "make it cozy" → "Warm Scandinavian living room: light oak floor, beige linen sofa, cream wool rug, soft diffused daylight."
3. **Report** the saved path and credits used; offer to iterate.
4. **Errors**: 402 = insufficient credits (point to /settings); 401 = bad/missing key; 429 = rate limited (retry with backoff); 5xx = failed, credits auto-refunded.

## Beyond still images: video & 3D

The same account and API key unlock more endpoints. Use them when the request goes past a still redesign:

- **Cinematic video walkthrough** — animate a still (a MeltFlex render or any interior photo) into a short walkthrough clip (Veo 3.1).
  `POST /api/v1/video` with `{ imageUrl, durationSeconds: 4|8, aspectRatio: "16:9"|"9:16", prompt? }` → `{ videoUrl, durationSeconds, aspectRatio, creditsUsed }` (a hosted MP4). Costs **100** credits (4s) or **150** (8s). Allow up to ~5 minutes.
- **Floorplan → 3D** — a 2D plan into a rendered 3D picture (`output: "render"`, **10** credits, ~20 s) or a downloadable GLB model (`output: "model"`, **100** credits, ~3 min). `POST /api/v1/floorplan-to-3d`.
- **Furniture photo → 3D model** — one product photo into a textured GLB (plus USDZ/FBX/OBJ links). `POST /api/v1/furniture-3d`, **75** credits, ~2–3 min.
- **Photo → explorable 3D world** — a room photo or one of your renders into a walkable Gaussian-splat world with a hosted viewer link. `POST /api/v1/world`, **30** credits (`draft`) or **200** (`hd`).

The three 3D endpoints can answer HTTP 202 and need polling; the companion skill `/meltflex:3d` documents all of them with request/response shapes and a polling helper. Full reference: <https://www.meltflexai.com/api>.

## Tips

- Prefer `imageUrl` over base64 — avoids the 15 MB body limit and is faster.
- Input images ≥1024px on the long side give the best results.
- Never print or commit the API key.
