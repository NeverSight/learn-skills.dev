---
name: meltflex-3d
description: Produce 3D assets with MeltFlex AI. Use when the user wants a downloadable 3D model (GLB) of a furniture piece from one photo; a 3D model or a rendered 3D picture from a 2D floorplan; or an explorable 3D world (Gaussian splat, .spz plus a hosted viewer link) from a room photo or render. Covers polling long builds (HTTP 202) and refreshing expired world links. Works directly against the MeltFlex REST API — no extra install required. Companion to /meltflex:design.
---

# MeltFlex — 3D from photos and floorplans

Three endpoints, one API key. All of them take a picture in and give a hosted 3D asset out.

| Want | Endpoint | Output | Credits | Typical time |
|------|----------|--------|---------|--------------|
| A 3D model of **one furniture piece** | `POST /api/v1/furniture-3d` | GLB (+ signed USDZ / FBX / OBJ) | 75 | 2–3 min |
| A 3D model of a **floorplan** | `POST /api/v1/floorplan-to-3d` (`output: "model"`) | GLB | 100 | ~3 min |
| A rendered **3D picture** of a floorplan | `POST /api/v1/floorplan-to-3d` (`output: "render"`) | PNG | 10 | ~20 s |
| An **explorable 3D world** of a room | `POST /api/v1/world` | .spz splat + viewer link | 30 (draft) / 200 (hd) | ~1 min / ~5 min |

If the `meltflex-mcp` server is configured, prefer its tools — `furniture_to_3d`, `floorplan_to_3d`, `generate_world` — they poll and save files for you. The CLI equivalents are `meltflex furniture`, `meltflex floorplan`, `meltflex world`.

## Prerequisites

`MELTFLEX_API_KEY` (`mf_sk_...`, any active subscription, from <https://www.meltflexai.com/settings>). Every call: `Authorization: Bearer $MELTFLEX_API_KEY`, `Content-Type: application/json`. Credits are deducted up front and refunded automatically if a build fails.

Every endpoint takes the source picture as either `imageUrl` (public URL, preferred) **or** `image` (base64 data URL, `data:image/jpeg;base64,...`, body limit 15 MB). JPEG, PNG or WebP.

## Long builds: HTTP 202 and polling

The 3D builds run inside the request for up to 5 minutes. If the model is still building when that budget ends, the server answers **HTTP 202** with a job id and a `pollUrl`. Nothing is lost: the credits stay on the job and you `GET` the poll URL every 5–10 seconds until it finishes. On a failed job the poll response carries `error` and `refunded: true` (the refund happens exactly once, however often you poll). Always use a client timeout of at least 300 s and always handle 202.

```python
import os, time, requests

H = {"Authorization": f"Bearer {os.environ['MELTFLEX_API_KEY']}"}

def run_3d(url, body):
    r = requests.post(url, headers=H, json=body, timeout=310)
    data = r.json()
    while r.status_code == 202:                      # still building — poll
        time.sleep(8)
        r = requests.get(data["pollUrl"], headers=H, timeout=60)
        data = r.json()
    if not data.get("success"):
        raise RuntimeError(data.get("error") or data.get("message") or data)
    return data
```

## 1. Furniture photo → GLB 3D model

`POST https://www.meltflexai.com/api/v1/furniture-3d` — **75 credits**.

Body:
- `imageUrl` / `image` — one piece of furniture, front three-quarter view, plain or white background, nothing cropped.
- `textured` (boolean, default `true`) — `false` skips the texture pass and returns bare geometry: faster, smaller file, same price.

Finished response (HTTP 200):
```json
{
  "success": true, "status": "SUCCEEDED", "taskId": "0193f1a2-...",
  "modelUrl": "https://.../meshes/api_..._0193f1a2.glb",
  "thumbnailUrl": "https://.../meshes/api_..._0193f1a2.png",
  "format": "glb",
  "formats": { "glb": "https://assets.meshy.ai/...", "usdz": "...", "fbx": "...", "obj": "..." },
  "textured": true, "creditsUsed": 75
}
```
`modelUrl` and `thumbnailUrl` are hosted by MeltFlex and permanent. `formats` are the engine's own signed links (valid about 72 hours) — download the USDZ/FBX/OBJ right away if the user needs them.

Still building → HTTP 202 `{ "status": "IN_PROGRESS", "taskId", "progress": 64, "pollUrl": ".../api/v1/furniture-3d?taskId=..." }`. Poll `GET /api/v1/furniture-3d?taskId=...`.

```python
data = run_3d("https://www.meltflexai.com/api/v1/furniture-3d",
              {"imageUrl": "https://your-cdn.com/armchair.jpg"})
open("armchair.glb", "wb").write(requests.get(data["modelUrl"], timeout=120).content)
print("Saved armchair.glb — credits used:", data["creditsUsed"])
```

## 2. Floorplan → GLB model, or a rendered 3D picture

`POST https://www.meltflexai.com/api/v1/floorplan-to-3d`

Body:
- `imageUrl` / `image` — the 2D floorplan.
- `output` — `"model"` (default) returns a GLB mesh, **100 credits**; `"render"` returns a rendered 3D picture of the plan, **10 credits**.
- `textured` (boolean, `model` only, default `true`) — `false` = bare walls, faster and smaller, same price.
- `style` (`render` only) — `photorealistic` (default), `3d-model`, `drawing`, `sketch`, `wireframe`, `clay`.
- `view` (`render` only) — `isometric` (default) or `topdown`.
- `furniture` (`render` only) — `furnished` (default, matches the plan's symbols), `empty`, or `styled` (furnished plus rugs, art, plants, a set table).
- `interiorStyle` (`render` only, photorealistic and 3d-model styles) — `auto` (default), `modern`, `scandinavian`, `minimalist`, `japandi`, `coastal`, `industrial`, `luxury`, `traditional`.
- `labels` (`render` only) — `full` (default, names + sizes + dimension lines), `names`, or `none`.

An unknown option value returns HTTP 400 listing the valid values.

`model` response: `{ "success": true, "output": "model", "modelUrl": "https://.../floorplans/model.glb", "format": "glb", "textured": true, "creditsUsed": 100 }`.
`render` response: `{ "success": true, "output": "render", "imageUrl": "https://.../floorplans/render.png", "format": "png", "style": "...", "view": "...", "furniture": "...", "interiorStyle": "...", "labels": "...", "creditsUsed": 10 }`.

A render takes about 20 seconds; a GLB conversion about 3 minutes and normally finishes inside the request (keep the 300 s timeout). If storage is briefly unavailable the file comes back inline instead: the GLB as base64 under `model`, the render as a data URL under `image`.

Good practice: run a cheap `render` first so the user can confirm the plan reads correctly, then spend 100 credits on the `model`.

## 3. Room photo or render → explorable 3D world

`POST https://www.meltflexai.com/api/v1/world`

Body:
- `imageUrl` / `image` — a normal interior photo or a MeltFlex render (a 360° panorama is detected automatically). A `/meltflex:design` result is a great input.
- `model` — `draft` (default): fast walkable world, **30 credits**, about a minute. `hd`: sharper, holds up close, **200 credits**, about five minutes. Anything else is HTTP 400.
- `name` (≤ 64 chars) — a label shown in the hosted viewer.

Finished response (HTTP 200):
```json
{
  "success": true, "done": true,
  "worldId": "8641d179-d7c6-4b39-94b6-101a420e8d80",
  "spzUrl": "https://cdn.marble.worldlabs.ai/.../full_res.spz?...",
  "spzUrls": { "full_res": "...", "500k": "...", "100k": "..." },
  "thumbnailUrl": "https://.../thumbnail.jpg?...",
  "caption": "A bright Scandinavian living room with a balcony",
  "viewerUrl": "https://marble.worldlabs.ai/world/8641d179-...",
  "format": "spz", "operationId": "op_...", "model": "draft", "creditsUsed": 30
}
```
`spzUrl` is the densest splat; `spzUrls` adds lighter tiers for a progressive open (the 100k file is about 1 MB). All are served with open CORS. **The links are signed and expire after a few days — persist `worldId`, not the links.** `viewerUrl` is a hosted viewer you can hand to the user directly.

Still building → HTTP 202 `{ "done": false, "status": "IN_PROGRESS", "operationId": "op_...", "pollUrl": ".../api/v1/world?operationId=op_..." }`. Draft worlds usually finish inside the request; treat 202 as the normal path for `hd`.

- `GET /api/v1/world?operationId=...` — poll a running build (`done: false` while building; `status: "FAILED"` + `refunded: true` on failure).
- `GET /api/v1/world?worldId=...` — **free**: fresh signed links for a world built earlier, same shape as the finished response. Call it right before showing the world.

```python
data = run_3d("https://www.meltflexai.com/api/v1/world",
              {"imageUrl": "https://your-cdn.com/living-room.jpg", "model": "draft", "name": "Living room"})
print("World id:", data["worldId"])          # store this; the links expire
print("Open it:", data["viewerUrl"])
open("world.spz", "wb").write(requests.get(data["spzUrl"], timeout=300).content)
```

Showing a world in a page: load the `.spz` with three.js + Spark (`SplatMesh`); a GLB with three.js `GLTFLoader`. Snippets for both are in the API docs: <https://www.meltflexai.com/api#world-3d> and <https://www.meltflexai.com/api#furniture-3d>.

## How to work with the user

1. **Match the endpoint to the input.** One product photo → `furniture-3d`. A floorplan drawing → `floorplan-to-3d`. A room photo or render → `world`. If the user wants a 3D picture rather than a mesh, `floorplan-to-3d` with `output: "render"` is 10× cheaper.
2. **Say the price before spending** on anything above 30 credits (furniture 75, floorplan model 100, hd world 200). Offer `draft` before `hd`, and `render` before `model`.
3. **Expect minutes, not seconds.** Tell the user the build is running; poll on 202; never re-POST the same job (that would charge again).
4. **Report** the saved path or hosted URL, the `worldId` / `taskId`, and credits used. For worlds, give the `viewerUrl`.
5. **Errors:** 400 = bad option value (the body lists the valid ones); 401 = bad key; 402 = insufficient credits (point to /settings); 429 = back off; a FAILED job = refunded automatically.

## Tips

- Furniture photos: one piece, plain background, nothing cropped; front three-quarter view gives the best mesh.
- Floorplans: a clean plan with clear walls converts best; text on the plan is fine for `render`, and is removed automatically for `model`.
- Worlds: a wide, well-lit interior shot with visible floor and ceiling gives the most walkable result; a `/meltflex:design` render at `resolution: "2K"` is ideal.
- Never print or commit the API key.
