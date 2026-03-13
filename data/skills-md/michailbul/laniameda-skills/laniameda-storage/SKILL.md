---
name: laniameda-storage
description: >
  Save pillar-tagged prompts + reference assets (from Instagram or any source) into the
  Laniameda Prompt Storage dashboard (Convex KB).

  Use when the user says "save this", "store this", "add to vault", shares a prompt/
  recipe/workflow, or sends reference media worth reusing.

  Rules: single item = one prompt or one asset. Batch = JSON array. Variations share
  the same promptText + promptIngestKey. Never concatenate distinct prompts.

  ownerUserId is always read from KB_OWNER_USER_ID env var automatically (never passed
  by the caller).
---

# laniameda-storage

Save content to the Convex prompt-storager KB via the HTTP API.

## Script
```bash
bun run ~/.agents/skills/laniameda-storage/scripts/ingest.ts '<json>'
```

## Key fields
- `ownerUserId` — **read from `KB_OWNER_USER_ID` env var automatically, never pass it in JSON**
- `promptText` — text/prompt content
- `tagNames` — array of tags (see tagging below)
- `imagePath` — local path for inbound media (preferred over base64)
- `imageUrl` — remote URL to fetch and store
- `ingestKey` — auto-generated if omitted (dedup protection)
- `modelName` — AI model that generated this (e.g. `"Midjourney"`, `"FLUX"`, `"Nano Banana Pro"`, `"Runway"`, `"Kling"`, `"Sora"`, `"CDANCe"`)
- `generationType` — `"image_gen"` | `"video_gen"` | `"ui_design"` | `"other"`
- `promptType` — `"image_gen"` | `"video_gen"` | `"ui_design"` | `"cinematic"` | `"ugc_ad"` | `"other"`
- `domain` — freeform category: `"product photography"`, `"portrait"`, `"architecture"`, `"fashion"`, etc.

**Single prompt + image with model tag:**
```bash
bun run ~/.agents/skills/laniameda-storage/scripts/ingest.ts '{
  "promptText": "Cinematic close-up, golden hour, 35mm film grain...",
  "imagePath": "/Users/michael/.openclaw/media/inbound/file_xxx.jpg",
  "modelName": "Midjourney",
  "generationType": "image_gen",
  "promptType": "cinematic",
  "domain": "portrait",
  "tagNames": ["prompts", "cinematic", "midjourney"]
}'
```

## Tagging
Always include a category tag: `prompts`, `tutorials`, `resources`, or `ideas`.

**Keep tags digestible (default): 3–5 tags total.**
- Don’t dump long keyword lists.
- Don’t include generation parameters as tags (e.g., Midjourney flags like `--ar`, `--raw`, etc.).

If the user explicitly asks for **creative tags**, include the literal tag `creative` (and still keep the total to ~3–5).

Add relevant tool/style tags as needed: `midjourney`, `flux`, `cinematic`, `portrait`, `character`, etc.

## Common patterns

**Single prompt:**
```bash
bun run ~/.agents/skills/laniameda-storage/scripts/ingest.ts '{
  "promptText": "...",
  "tagNames": ["prompts", "tag1"]
}'
```

**Single prompt + image (inbound Telegram media):**
```bash
bun run ~/.agents/skills/laniameda-storage/scripts/ingest.ts '{
  "promptText": "...",
  "imagePath": "/Users/michael/.openclaw/media/inbound/file_xxx.jpg",
  "tagNames": ["prompts", "ai-image"]
}'
```

**One prompt with multiple variation images (e.g. same template, different brand examples):**
Use the same `promptText` + same `promptIngestKey` in every item. The prompt is created once (deduped on `promptIngestKey`); each asset is linked to the same prompt.
```bash
bun run ~/.agents/skills/laniameda-storage/scripts/ingest.ts '[
  { "promptText": "...", "promptIngestKey": "my-prompt-slug", "imagePath": "/path/example1.jpg", "tagNames": ["prompts", "fashion"] },
  { "promptText": "...", "promptIngestKey": "my-prompt-slug", "imagePath": "/path/example2.jpg", "tagNames": ["prompts", "fashion"] },
  { "promptText": "...", "promptIngestKey": "my-prompt-slug", "imagePath": "/path/example3.jpg", "tagNames": ["prompts", "fashion"] }
]'
```
Result: ONE prompt record, THREE assets — all linked to the same prompt via `promptId`.

**When to use this pattern:**
- User shares a prompt template with multiple example outputs/variations
- Multiple brand applications of the same prompt (e.g. fashion lookbook for Ozon, Yandex, etc.)
- Same prompt, different style results

**Batch (multiple distinct prompts or unrelated images):**
Pass a JSON array without a shared `promptIngestKey` — each item is fully independent:
```bash
bun run ~/.agents/skills/laniameda-storage/scripts/ingest.ts '[
  { "promptText": "prompt one", "tagNames": ["prompts", "cinematic"] },
  { "promptText": "prompt two", "imagePath": "/path/img.jpg", "tagNames": ["prompts", "portrait"] },
  { "imageUrl": "https://...", "tagNames": ["resources"] }
]'
```
Returns array of `{ promptId?, assetId? }` — one result per item.

**When to use batch vs. prompt+variations:**
- Multiple distinct prompts → plain batch (no shared `promptIngestKey`)
- Same prompt + multiple example images → shared `promptIngestKey` pattern above
- Never concatenate multiple distinct prompts into one `promptText`

**⚠️ Common mistake — orphaned assets:**
If you save variation images WITHOUT `promptText` + `promptIngestKey`, those assets will be saved
as orphans (no prompt link). Always include both in every item when using the variations pattern.

## After saving
Report: what was saved, tags applied. If duplicate (same ingestKey), say "already in KB".

## Schema changes
If the Convex schema or action signature has changed, read `references/convex-interface.md` before running — it has the source file paths and current interface docs.
