---
name: laniameda-kb
description: >-
  Save prompts, images, tutorials, links, and ideas to the laniameda.gallery Convex knowledge base.
  Use when the user says save this, store this, add to KB, save to vault, pastes a prompt,
  forwards a Telegram post with a prompt, sends reference images, or wants to remember something.
  Auto-classifies content into the correct pillar (creators/cars/designs/dump).
  ownerUserId is always read from KB_OWNER_USER_ID env var, never passed by the caller.
---

# laniameda-kb

Save content to the laniameda.gallery Convex KB via the HTTP API.

## Project
- **Name:** laniameda.gallery
- **Repo:** `/Users/michael/work/laniameda/laniameda.gallery`

## Script
```bash
bun run ~/.agents/skills/laniameda-kb/scripts/ingest.ts '<json>'
```

---

## Pillar auto-classification (your job as agent)

Content is organized into 4 pillars. **Always determine the pillar before saving.** Use the rules below.

| Pillar | What goes here | Signals |
|---|---|---|
| `creators` | AI influencer / fashion / portrait prompts | people, faces, fashion, editorial, beauty, influencer, character, pose, studio lighting, lookbook, outfit, model |
| `cars` | Cinematic automotive references and prompts | car, vehicle, automotive, road, drive, racing, mechanical, engine, wheel, headlights, motion blur |
| `designs` | Website, UI, mobile, component, app designs | UI, UX, website, landing page, dashboard, component, mobile app, layout, Figma, web design, interface |
| `dump` | Anything else that's useful but doesn't fit | general prompts, abstract, nature, architecture, food, misc |

**When in doubt:** `dump`. Never leave `pillar` empty.

### Quick classification examples
- "cinematic fashion shoot, editorial lighting, high contrast" → `creators`
- "BMW M3 on mountain road, volumetric fog, 8K" → `cars`
- "SaaS landing page dark theme, glassmorphism" → `designs`
- "sunset over ocean, watercolor style" → `dump`
- portrait prompt with people → `creators`
- UI screenshot or web design reference → `designs`

---

## Key fields
- `ownerUserId` — **read from `KB_OWNER_USER_ID` env var automatically, never pass it**
- `pillar` — **always set this** (see auto-classification above): `"creators"` | `"cars"` | `"designs"` | `"dump"`
- `promptText` — text/prompt content
- `tagNames` — array of tags (always include category + pillar as tag)
- `imagePath` — local path for inbound media (preferred over base64)
- `imageUrl` — remote URL to fetch and store
- `ingestKey` — auto-generated if omitted (dedup protection)
- `modelName` — AI model used: `"Midjourney"`, `"FLUX"`, `"Nano Banana Pro"`, `"Runway"`, `"Kling"`, `"Sora"`, `"CDANCe"`, etc.
- `generationType` — `"image_gen"` | `"video_gen"` | `"ui_design"` | `"other"`
- `promptType` — `"image_gen"` | `"video_gen"` | `"ui_design"` | `"cinematic"` | `"ugc_ad"` | `"other"`
- `domain` — freeform category: `"fashion"`, `"portrait"`, `"automotive"`, `"architecture"`, `"web design"`, etc.

---

## Tagging
Always include a category tag: `prompts`, `tutorials`, `resources`, or `ideas`.
Always include the pillar as a tag: `creators`, `cars`, `designs`, or `dump`.
Add relevant style/tool tags: `cinematic`, `midjourney`, `flux`, `fashion`, `portrait`, `automotive`, `ui`, etc.

---

## Common patterns

**Single image + prompt (most common — Telegram forward):**
```bash
bun run ~/.agents/skills/laniameda-kb/scripts/ingest.ts '{
  "promptText": "Cinematic close-up, golden hour, 35mm film grain, fashion editorial...",
  "imagePath": "/Users/michael/.openclaw/media/inbound/file_xxx.jpg",
  "pillar": "creators",
  "modelName": "Midjourney",
  "generationType": "image_gen",
  "domain": "fashion",
  "tagNames": ["prompts", "cinematic", "midjourney", "creators"]
}'
```

**Image only (no prompt text — reference save):**
```bash
bun run ~/.agents/skills/laniameda-kb/scripts/ingest.ts '{
  "imagePath": "/Users/michael/.openclaw/media/inbound/file_xxx.jpg",
  "pillar": "designs",
  "domain": "web design",
  "tagNames": ["resources", "ui", "designs"]
}'
```

**One prompt + multiple variation images:**
Use the same `promptText` + `promptIngestKey` in every item:
```bash
bun run ~/.agents/skills/laniameda-kb/scripts/ingest.ts '[
  { "promptText": "...", "promptIngestKey": "my-slug", "pillar": "cars", "imagePath": "/path/1.jpg", "tagNames": ["prompts", "cars"] },
  { "promptText": "...", "promptIngestKey": "my-slug", "pillar": "cars", "imagePath": "/path/2.jpg", "tagNames": ["prompts", "cars"] }
]'
```

**Batch (distinct unrelated items):**
```bash
bun run ~/.agents/skills/laniameda-kb/scripts/ingest.ts '[
  { "promptText": "...", "pillar": "creators", "tagNames": ["prompts", "creators"] },
  { "imageUrl": "https://...", "pillar": "designs", "tagNames": ["resources", "designs"] }
]'
```

**⚠️ Orphaned assets mistake:**
If you save variation images WITHOUT `promptText` + `promptIngestKey`, assets are saved as orphans. Always include both when using the variations pattern.

---

## After saving
Report: pillar assigned, what was saved, model tagged, tags applied. If duplicate (same ingestKey) → "already in KB".

## Schema changes
If the Convex schema has changed, read `references/convex-interface.md` before running.
