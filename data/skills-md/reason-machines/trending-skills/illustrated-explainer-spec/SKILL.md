---
name: illustrated-explainer-spec
description: Spec for building an infinite drill-down AI illustrated explainer web app where users type a topic and click to drill into generated watercolor-style images.
triggers:
  - implement the illustrated explainer spec
  - build a drill-down explainer app
  - create an infinite drill-down image generator
  - set up the illustrated explainer project
  - implement drill-down watercolor explainer
  - build AI image drill-down app
  - implement the flipbook explainer spec
  - create click-to-drill image explainer
---

# Illustrated Explainer Spec Implementation Guide

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

## What This Project Is

A spec (not a library) for building a locally-run single-page web app where:
1. User types a topic → AI generates a 16:9 watercolor-style illustrated explainer page
2. User clicks anywhere on the image → AI generates a "drill-into" next page for that spot
3. This repeats infinitely, preserving painting style across all pages
4. Content-addressed caching means identical queries/clicks never re-generate

The spec is **stack-agnostic** — you choose the framework, image model API, and language. This skill shows you how to implement it end-to-end.

---

## Architecture Overview

```
Browser (thin client)
  └── POST /api/page  ──►  Server
                              ├── hash → check disk cache
                              ├── composite red marker onto parent image
                              ├── call image model (text + optional image)
                              └── write PNG → return page object
```

### Page Object Shape

```typescript
interface Page {
  id: string;           // deterministic hash
  imageUrl: string;     // e.g. "/generated/abc123.png"
  parentId: string | null;
  parentClick: { x: number; y: number } | null;  // normalized 0–1
  initialQuery: string | null;  // only on page 1
}
```

---

## Recommended Stack (Node.js + Google Gemini)

```bash
mkdir explainer && cd explainer
npm init -y
npm install express sharp crypto @google/generative-ai cors dotenv
```

```
.env
GEMINI_API_KEY=your_key_here
CACHE_VERSION=v1
PORT=3000
```

---

## Server Implementation

### `server.js` — Full Reference Implementation

```javascript
import express from 'express';
import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import sharp from 'sharp';
import { GoogleGenerativeAI } from '@google/generative-ai';
import 'dotenv/config';

const app = express();
app.use(express.json());
app.use(express.static('public'));
app.use('/generated', express.static('public/generated'));

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
const VERSION = process.env.CACHE_VERSION || 'v1';
const GENERATED_DIR = path.join('public', 'generated');
fs.mkdirSync(GENERATED_DIR, { recursive: true });

// ── Content-addressed IDs ──────────────────────────────────────────────────

function hashFirstPage(query) {
  const normalized = query.trim().replace(/\s+/g, ' ').toLowerCase();
  return crypto
    .createHash('sha256')
    .update(`first${VERSION}${normalized}`)
    .digest('hex')
    .slice(0, 32);
}

function hashChildPage(parentId, x, y) {
  const rx = Math.round(x * 100) / 100;
  const ry = Math.round(y * 100) / 100;
  return crypto
    .createHash('sha256')
    .update(`child${VERSION}${parentId}${rx}${ry}`)
    .digest('hex')
    .slice(0, 32);
}

// ── Style description (single source of truth) ────────────────────────────

const STYLE_DESCRIPTION = `Painting style (must remain consistent across every page):
- Light warm paper background with generous margins
- Clean, even dark gray or black ink outlines, consistent thin line weight
- Soft watercolor washes, pale palette: ivory, pale green, pale blue, light gray, with restrained warm accents
- A large serif title printed at the top center of the image
- Calm, well-composed scene with breathing room

Strict exclusions:
- No decorative borders, seals, parchment aging, ornate fonts, or vintage texture
- No 3D render, photorealism, neon, dark themes, or modern app UI cards
- No dense paragraphs of text, watermarks, or tiny unreadable labels
- No tourist map roads, landmarks, transit, or "traveler-guide" framing`;

function firstPagePrompt(query) {
  return `${STYLE_DESCRIPTION}

Subject: ${query}

Compose a single 16:9 illustrated explainer page about the subject above.
Let the scene's content (objects, layout, metaphor) be whatever best
explains the subject — cross-section, exploded view, timeline, anatomy,
flow, comparison, or scene — chosen to fit this specific topic.

Output a single PNG image, 16:9. Print the title clearly inside the image.`;
}

const CHILD_PAGE_PROMPT = `${STYLE_DESCRIPTION}

You are continuing an illustrated explainer book.
The provided image is the previous page. A red circle marks
the area the reader pointed at.

Generate the next page: a single 16:9 image that goes deeper
into whatever the red circle is on — zoom in, expand its inner
structure, or show its mechanism.

Critical: match the painting style of the provided image exactly
— same line weight, same paper tone, same pastel palette, same
title typography. The two pages must feel like consecutive spreads
in the same hand-drawn book.

Do NOT include the red circle or any cursor mark in the output.

Output a single PNG image, 16:9.`;

// ── Red marker compositing ─────────────────────────────────────────────────

async function compositeRedMarker(imagePath, nx, ny) {
  const img = sharp(imagePath);
  const { width, height } = await img.metadata();
  const cx = Math.round(nx * width);
  const cy = Math.round(ny * height);
  const radius = Math.round(width * 0.04);

  // Build SVG marker: outer ring + inner dot
  const svg = `<svg width="${width}" height="${height}" xmlns="http://www.w3.org/2000/svg">
    <circle cx="${cx}" cy="${cy}" r="${radius}" fill="rgba(220,30,30,0.25)" stroke="red" stroke-width="${Math.max(3, radius * 0.15)}"/>
    <circle cx="${cx}" cy="${cy}" r="${Math.round(radius * 0.3)}" fill="red" stroke="white" stroke-width="2"/>
  </svg>`;

  return img
    .composite([{ input: Buffer.from(svg), blend: 'over' }])
    .png()
    .toBuffer();
}

// ── Image model call ───────────────────────────────────────────────────────

async function callImageModel(prompt, referenceImageBuffer = null) {
  const model = genAI.getGenerativeModel({ model: 'gemini-2.0-flash-preview-image-generation' });

  const parts = [{ text: prompt }];
  if (referenceImageBuffer) {
    parts.push({
      inlineData: {
        mimeType: 'image/png',
        data: referenceImageBuffer.toString('base64'),
      },
    });
  }

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 120_000);

  try {
    const result = await model.generateContent({
      contents: [{ role: 'user', parts }],
      generationConfig: { responseModalities: ['IMAGE'] },
    });
    clearTimeout(timeout);

    const candidates = result.response.candidates ?? [];
    for (const candidate of candidates) {
      for (const part of candidate.content?.parts ?? []) {
        if (part.inlineData?.mimeType?.startsWith('image/')) {
          return Buffer.from(part.inlineData.data, 'base64');
        }
      }
    }
    throw new Error('No inline image in model response');
  } catch (err) {
    clearTimeout(timeout);
    throw err;
  }
}

// ── Generation queue (serialize requests) ─────────────────────────────────

let queue = Promise.resolve();

function enqueue(fn) {
  queue = queue.then(fn, fn);  // always advance queue even on error
  return queue;
}

// ── Core generation logic ──────────────────────────────────────────────────

async function generatePage(id, prompt, referenceImageBuffer) {
  const outPath = path.join(GENERATED_DIR, `${id}.png`);

  // Cache hit
  if (fs.existsSync(outPath) && fs.statSync(outPath).size > 0) {
    return `/generated/${id}.png`;
  }

  const imageBytes = await callImageModel(prompt, referenceImageBuffer);
  fs.writeFileSync(outPath, imageBytes);
  return `/generated/${id}.png`;
}

// ── /api/page endpoint ────────────────────────────────────────────────────

const ID_REGEX = /^[0-9a-f]{32}$/;

app.post('/api/page', async (req, res) => {
  const { query, parentId, parentClick } = req.body;

  // Validate
  if (query !== undefined) {
    if (typeof query !== 'string' || query.trim().length < 1 || query.length > 300) {
      return res.status(400).json({ error: 'query must be 1–300 chars' });
    }
  } else {
    if (!ID_REGEX.test(parentId)) {
      return res.status(400).json({ error: 'invalid parentId' });
    }
    const { x, y } = parentClick ?? {};
    if (
      typeof x !== 'number' || typeof y !== 'number' ||
      !isFinite(x) || !isFinite(y) ||
      x < 0 || x > 1 || y < 0 || y > 1
    ) {
      return res.status(400).json({ error: 'x and y must be finite floats in [0, 1]' });
    }
  }

  try {
    const page = await enqueue(async () => {
      if (query !== undefined) {
        // First page
        const trimmed = query.trim();
        const id = hashFirstPage(trimmed);
        const imageUrl = await generatePage(id, firstPagePrompt(trimmed), null);
        return { id, imageUrl, parentId: null, parentClick: null, initialQuery: trimmed };
      } else {
        // Child page
        const id = hashChildPage(parentId, parentClick.x, parentClick.y);
        const parentPath = path.join(GENERATED_DIR, `${parentId}.png`);

        if (!fs.existsSync(parentPath)) {
          throw new Error('Parent image not found');
        }

        const markedBuffer = await compositeRedMarker(parentPath, parentClick.x, parentClick.y);
        const imageUrl = await generatePage(id, CHILD_PAGE_PROMPT, markedBuffer);
        return { id, imageUrl, parentId, parentClick, initialQuery: null };
      }
    });

    res.json({ page });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Generation failed, try clicking elsewhere.' });
  }
});

app.listen(process.env.PORT || 3000, () => {
  console.log(`Explainer running on http://localhost:${process.env.PORT || 3000}`);
});
```

---

## Client Implementation

### `public/index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Drill-Down Explainer</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: system-ui, sans-serif; background: #1a1a1a; color: #eee; display: flex; flex-direction: column; height: 100vh; }
    #topbar { display: flex; align-items: center; gap: 12px; padding: 10px 16px; background: #111; flex-shrink: 0; }
    #appname { font-weight: bold; font-size: 1.1rem; }
    #counter { font-size: 0.85rem; color: #aaa; margin-right: auto; }
    #topic-input { flex: 1; padding: 6px 10px; border-radius: 6px; border: none; font-size: 1rem; max-width: 420px; }
    button { padding: 6px 14px; border-radius: 6px; border: none; cursor: pointer; font-size: 0.9rem; background: #444; color: #eee; }
    button:disabled { opacity: 0.4; cursor: not-allowed; }
    #generate-btn { background: #4a7eff; color: #fff; }
    #canvas-area { flex: 1; position: relative; display: flex; align-items: center; justify-content: center; overflow: hidden; }
    #page-img { max-width: 100%; max-height: 100%; cursor: crosshair; display: block; }
    #loading-overlay { position: absolute; inset: 0; background: rgba(0,0,0,0.55); display: flex; align-items: center; justify-content: center; font-size: 1.2rem; display: none; }
    #error-banner { background: #b00; color: #fff; padding: 6px 16px; font-size: 0.9rem; display: none; flex-shrink: 0; }
    #thumbstrip { display: flex; gap: 8px; padding: 8px 16px; background: #111; overflow-x: auto; flex-shrink: 0; min-height: 72px; }
    .thumb { width: 96px; height: 54px; object-fit: cover; border-radius: 4px; cursor: pointer; border: 2px solid transparent; flex-shrink: 0; }
    .thumb.active { border-color: #4a7eff; }
    .ripple { position: absolute; border-radius: 50%; background: rgba(255,80,80,0.5); transform: scale(0); animation: ripple 0.6s ease-out forwards; pointer-events: none; width: 40px; height: 40px; margin: -20px; }
    @keyframes ripple { to { transform: scale(3); opacity: 0; } }
  </style>
</head>
<body>
<div id="topbar">
  <span id="appname">🔍 Explainer</span>
  <span id="counter"></span>
  <input id="topic-input" placeholder="Type a topic…" maxlength="300" />
  <button id="generate-btn">Generate</button>
  <button id="back-btn" disabled>← Back</button>
  <button id="reset-btn" disabled>Reset</button>
</div>
<div id="error-banner"></div>
<div id="canvas-area">
  <img id="page-img" style="display:none" alt="Explainer page" />
  <div id="loading-overlay">Generating the next page…</div>
</div>
<div id="thumbstrip"></div>

<script>
  const state = { pages: [], currentIndex: -1, loading: false };

  const topicInput = document.getElementById('topic-input');
  const generateBtn = document.getElementById('generate-btn');
  const backBtn = document.getElementById('back-btn');
  const resetBtn = document.getElementById('reset-btn');
  const counter = document.getElementById('counter');
  const canvasArea = document.getElementById('canvas-area');
  const pageImg = document.getElementById('page-img');
  const loadingOverlay = document.getElementById('loading-overlay');
  const errorBanner = document.getElementById('error-banner');
  const thumbstrip = document.getElementById('thumbstrip');

  function showError(msg) {
    errorBanner.textContent = msg;
    errorBanner.style.display = 'block';
  }
  function clearError() { errorBanner.style.display = 'none'; }

  function setLoading(val) {
    state.loading = val;
    loadingOverlay.style.display = val ? 'flex' : 'none';
    topicInput.disabled = val;
    generateBtn.disabled = val;
  }

  function render() {
    const { pages, currentIndex } = state;
    const hasCurrent = currentIndex >= 0;
    const current = hasCurrent ? pages[currentIndex] : null;

    counter.textContent = hasCurrent ? `${currentIndex + 1} / ${pages.length}` : '';
    backBtn.disabled = currentIndex <= 0;
    resetBtn.disabled = pages.length === 0;

    pageImg.style.display = current ? 'block' : 'none';
    if (current) pageImg.src = current.imageUrl;

    // Thumbnails
    thumbstrip.innerHTML = '';
    pages.forEach((p, i) => {
      const img = document.createElement('img');
      img.className = 'thumb' + (i === currentIndex ? ' active' : '');
      img.src = p.imageUrl;
      img.title = `Page ${i + 1}`;
      img.addEventListener('click', () => { state.currentIndex = i; render(); });
      thumbstrip.appendChild(img);
    });
    if (thumbstrip.lastChild) {
      thumbstrip.lastChild.scrollIntoView({ inline: 'end', behavior: 'smooth' });
    }
  }

  async function postPage(body) {
    const res = await fetch('/api/page', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.error || 'Server error');
    }
    return (await res.json()).page;
  }

  generateBtn.addEventListener('click', async () => {
    const query = topicInput.value.trim();
    if (!query || state.loading) return;
    clearError();
    setLoading(true);
    try {
      const page = await postPage({ query });
      state.pages = [page];
      state.currentIndex = 0;
      render();
    } catch (e) { showError(e.message); }
    finally { setLoading(false); }
  });

  topicInput.addEventListener('keydown', e => { if (e.key === 'Enter') generateBtn.click(); });

  pageImg.addEventListener('click', async (e) => {
    if (state.loading || state.currentIndex < 0) return;
    const rect = pageImg.getBoundingClientRect();
    const x = (e.clientX - rect.left) / rect.width;
    const y = (e.clientY - rect.top) / rect.height;

    // Ripple animation
    const ripple = document.createElement('div');
    ripple.className = 'ripple';
    ripple.style.left = e.clientX - canvasArea.getBoundingClientRect().left + 'px';
    ripple.style.top = e.clientY - canvasArea.getBoundingClientRect().top + 'px';
    canvasArea.appendChild(ripple);
    setTimeout(() => ripple.remove(), 700);

    const current = state.pages[state.currentIndex];
    clearError();
    setLoading(true);
    try {
      const page = await postPage({ parentId: current.id, parentClick: { x, y } });
      // Truncate forward history, append new
      state.pages = state.pages.slice(0, state.currentIndex + 1);
      state.pages.push(page);
      state.currentIndex = state.pages.length - 1;
      render();
    } catch (e) { showError(e.message); }
    finally { setLoading(false); }
  });

  backBtn.addEventListener('click', () => {
    if (state.currentIndex > 0) { state.currentIndex--; render(); }
  });

  resetBtn.addEventListener('click', () => {
    state.pages = []; state.currentIndex = -1;
    topicInput.value = '';
    clearError();
    render();
  });

  render();
</script>
</body>
</html>
```

---

## Configuration

### Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GEMINI_API_KEY` | Yes | Google Gemini API key |
| `CACHE_VERSION` | No | Bump to invalidate all caches (default: `v1`) |
| `PORT` | No | Server port (default: `3000`) |

### `package.json`

```json
{
  "type": "module",
  "scripts": {
    "start": "node server.js",
    "dev": "node --watch server.js"
  }
}
```

### Running

```bash
# Set your API key
export GEMINI_API_KEY=your_key_here

# Start server
npm start

# Dev mode (auto-restart on file change)
npm run dev
```

---

## Alternative: OpenAI gpt-image-1

If using OpenAI instead of Gemini, replace `callImageModel`:

```javascript
import OpenAI from 'openai';
const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

async function callImageModel(prompt, referenceImageBuffer = null) {
  if (!referenceImageBuffer) {
    // First page — text-to-image
    const res = await openai.images.generate({
      model: 'gpt-image-1',
      prompt,
      size: '1792x1024',  // closest 16:9
      response_format: 'b64_json',
    });
    return Buffer.from(res.data[0].b64_json, 'base64');
  }

  // Child page — image edit / variation with reference
  const { toFile } = await import('openai');
  const imageFile = await toFile(referenceImageBuffer, 'parent.png', { type: 'image/png' });
  const res = await openai.images.edit({
    model: 'gpt-image-1',
    image: imageFile,
    prompt,
    size: '1792x1024',
    response_format: 'b64_json',
  });
  return Buffer.from(res.data[0].b64_json, 'base64');
}
```

---

## Common Patterns

### Invalidating the Cache

Bump `CACHE_VERSION` in `.env`:
```bash
CACHE_VERSION=v2
```
All new requests will compute new hashes and regenerate. Old files in `public/generated/` can be deleted manually.

### Inspecting Cached Files

```bash
ls public/generated/     # all generated PNGs, named by hash
```

### Testing Cache Hit (no model call)

```bash
# Generate once
curl -X POST http://localhost:3000/api/page \
  -H 'Content-Type: application/json' \
  -d '{"query":"how volcanoes work"}'

# Second call — check server logs, model should NOT be called
curl -X POST http://localhost:3000/api/page \
  -H 'Content-Type: application/json' \
  -d '{"query":"how volcanoes work"}'
```

### Testing Child Page

```bash
# Use the id from a first-page response
curl -X POST http://localhost:3000/api/page \
  -H 'Content-Type: application/json' \
  -d '{"parentId":"<id-from-first-page>","parentClick":{"x":0.5,"y":0.5}}'
```

---

## Acceptance Checklist

From the spec §12 — verify each:

- [ ] "how volcanoes work" → watercolor-style page, title inside image, no map elements
- [ ] "how a smartphone is built" → cross-section/exploded view, same style
- [ ] Click visible object → next page drills into that object, style matches
- [ ] Drill 5 pages deep → style stays consistent across all pages
- [ ] Back button returns to previous page; thumbnails jump without network request
- [ ] Reset clears state back to empty input
- [ ] Restart server, type same query → returns instantly (disk cache hit)
- [ ] Two rapid clicks → second request waits for first to complete (check server logs)

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `No inline image in model response` | Model returned text only; check model name supports image output and `responseModalities: ['IMAGE']` is set |
| Style drifts across pages | Ensure `STYLE_DESCRIPTION` is one const — never duplicated or paraphrased in prompts |
| Red marker not visible on dark images | Increase ring radius (`width * 0.05`) or add white stroke on outer ring |
| Second click fires before first finishes | Check serialization queue — both requests must be inside `enqueue()` |
| Cache miss after server restart | Verify `CACHE_VERSION` hasn't changed and `public/generated/` is not being cleaned on start |
| `Parent image not found` 500 error | Client sent a `parentId` for a page whose PNG was deleted; clear state and start over |
| Images too slow | Add a lightweight loading progress bar; generation typically takes 10–30s per page |
