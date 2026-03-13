---
name: instagram-extract
description: Extract text, links, and key takeaways from Instagram/Threads posts (especially carousels) and LinkedIn posts using an already-logged-in Brave/Chrome tab via OpenClaw Browser Relay. Use when the user pastes an Instagram/Threads/LinkedIn URL (or forwards screenshots) and asks something generic like “save it”, “capture this”, “summarize and store”, or “put this in the vault” — you should decide what’s worth saving, classify it into the right pillar, save it to the local KB and/or ingest prompts via the laniameda-kb skill, and also emit a compact JSON payload into a media-agent inbox file for downstream reuse.
---

# Instagram Extract

Use Instagram as a “find + capture” stream: the user pastes a post link and says something generic like **“save it”**, and you decide what’s worth capturing, how to summarize it, and where it belongs.

The workflow should be **agentic** (use judgment) rather than deterministic.

Hard constraints:
- Use the logged-in browser relay (`browser` tool with `profile="chrome"`) when available.
- Classify + save into the right pillar so it’s reusable later.
- Report back in **bullet points** (no full transcript unless asked).
- After saving, **notify the media agent** by appending a compact JSON record to the shared inbox file (details below).

Scope constraints (current reality):
- This skill is for **Instagram + Threads + LinkedIn** (logged-in via Browser Relay / existing Chrome/Brave profile).
- **X/Twitter**: don’t try to force it in Brave if it’s blocked; treat as out-of-scope for this skill (we’ll use a different approach/tool later).

## Pillars (classification targets)
Pick the **single best fit** (canonical save) and optionally add a **secondary tag** when it overlaps. Do **not** duplicate saves across pillars unless the user explicitly asks.

Current pillars Michael wants to save:

Use these pillar ids in the media-agent inbox payload:
1) **Prompts — creating images** (`prompts_image`)
2) **Tutorials/knowledge — marketing workflows** (`tutorials_marketing`) — frameworks, copywriting, growth, positioning
3) **Design systems / design inspiration** (`design_inspo`) — UI patterns, components, typography, layout
4) **Prompts — web design / development** (`prompts_webdev`) — UI prompts, landing page prompts, component prompts

Also include optional tags like: `storytelling`, `hooks`, `carousel`, `landing_page`, `ui`, `prompt_template`, `checklist`, `case_study`.

## Lightweight workflow (guidance, not a script)

### 1) Get access to the real post (relay)
- Try to use **browser relay takeover** (`profile="chrome"`).
- If relay isn’t attached, ask the user to attach it (toolbar icon → badge ON).
- If token is required, have the user set the gateway token in extension Options.

### 2) Extract enough to be useful
Prioritize signal over completeness.

For **Instagram/Threads**:
- Caption: prefer `og:description` / `og:title`.
- Carousel: grab slide text via image `alt` text (fast); OCR only when the slide text is garbled or crucial.

For **LinkedIn**:
- Expand “see more” if present and extract the full post text.
- If it’s a document carousel or images and text extraction is limited, still capture the media URLs + summarize what’s visible.

For all platforms:
- Links: collect outbound URLs/domains if present.
- Media: collect image URLs when available (good enough for downstream reuse).

### 3) Decide what matters (summarize)
Write **5–10 bullets** focusing on:
- the core idea / framework
- anything immediately actionable
- any reusable templates (hooks, structures, checklists)
- any concrete examples worth saving

### 4) Decide what to do with it (agentic routing)
You’re optimizing for **future reuse**, not perfect capture.

Default behavior Michael wants:
- If the user says **"save it"** and the post is **weak/low-signal** (generic motivation, no reusable artifact), **ask once**: “Not worth saving (too generic). Save anyway?”
- If the user says **"force save"** / **"save anyway"**: save regardless.
- If the user says **"light save"**: save a tiny note (title + link + 3 bullets) even if it’s generic.

Use these heuristics (not rules):
- **If it’s directly reusable instructions** (a prompt, a template, a checklist, a swipeable structure) → save it.
- **If it’s vibes with no payload** (generic motivation, no concrete steps) → don’t over-save; create a tiny note only if the framing is uniquely good.
- **If it’s ambiguous**, ask *one* clarifying question max (e.g., “Do you want this saved as marketing knowledge or as design inspiration?”). Otherwise, pick your best guess and proceed.

Routing:
- **Prompt content** (copy/paste generation instructions) → ingest via **`prompt-kb`**.
- **Tutorials/knowledge (marketing workflows)** → local KB note.
- **Design systems / design inspiration** → local KB note focused on patterns.
- If it contains both a reusable prompt and a useful framework → save **both** (local KB summary + prompt-kb ingest).

### 5) Save (create durable artifacts)

#### A) Local KB save (tutorials/knowledge/design inspiration)
Save **one canonical note** in a stable, platform-agnostic structure:
- `kb/pillars/<pillar_id>/YYYY/MM/<YYYY-MM-DD>-<short-slug>.md`

Where `pillar_id` is one of:
- `tutorials_marketing`
- `design_inspo`
(If it’s a prompt-first asset, you can still save a short KB note, but the canonical storage may be `prompt-kb`.)

Also store a **raw capture** (optional but recommended when extraction is messy) in:
- `kb/inbox/<platform>/YYYY/MM/<YYYY-MM-DD>-<short-slug>.md`

`<platform>` is `instagram` | `threads` | `linkedin`.

Note format (keep it tight):
- Title (human readable)
- Source URL
- Platform (`instagram|threads|linkedin`)
- Pillar (primary) + optional tags (secondary)
- 5–10 bullet summary (your synthesis)
- Why it matters (1–2 bullets)
- Reusable templates/checklists (if any)
- Links found (if any)
- Media (image URLs if available)
- Optional: extracted text only when it’s actually useful later

Slug guidance:
- Prefer something that will be searchable later: `<topic>-<creator>` or `<framework>-<topic>`.

#### B) Prompt vault ingest (prompt-kb)
- Use `prompt-kb`.
- Tagging:
  - Always include one: `prompts` | `tutorials` | `resources` | `ideas`
  - Add `image_gen` / `video_gen` / `ui_design` when appropriate
  - Add tool/model tags if known
- Multiple slides/images for the same prompt template → shared `promptIngestKey`.

#### C) Media-agent handoff (always)
Append a single JSON line to: `kb/_media_agent_inbox/ingest.jsonl`

Schema (keep it compact):
```json
{
  "createdAt": "YYYY-MM-DDTHH:mm:ssZ",
  "platform": "instagram|threads|linkedin",
  "url": "...",
  "pillar": "prompts_image|tutorials_marketing|design_inspo|prompts_webdev",
  "tags": ["optional", "tags"],
  "title": "...",
  "summary": ["...", "..."],
  "links": ["..."],
  "media": ["https://..."],
  "repurpose": {
    "x": {"hook": "...", "outline": ["...", "..."]},
    "carousel": {"slideTitles": ["...", "..."]},
    "shortVideo": {"beats": ["hook...", "beat...", "cta..."]},
    "cta": "..."
  },
  "saved": {
    "kbPaths": ["kb/..."],
    "promptKb": {"ingestKey": "optional", "tags": ["..."]}
  }
}
```
Implementation hint: use a tiny Python one-liner to append JSONL so you don’t need to read/overwrite the file.

### 6) Telegram report (bullet points only)
Return:
- what it is (1 line)
- 5–10 key takeaways
- why it matters (1–2 bullets)
- links found (if any)
- what got saved + where (file path and/or “ingested to Convex”) + pillar + tags
- **Repurpose Pack (ALWAYS)** — written in **Michael’s voice** (blunt, marketing-first, specific):
  - X post: 1 hook + 3–5 bullet outline
  - Carousel: 6–8 slide titles
  - Short video: 15–30s script beats (hook → beats → CTA)
  - CTA: suggested comment keyword / next step
