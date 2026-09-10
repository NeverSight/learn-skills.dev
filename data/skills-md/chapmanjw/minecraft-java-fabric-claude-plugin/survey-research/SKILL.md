---
name: survey-research
description: >-
  Researches real-world buildings, cities, landmarks, vehicles, and mechanisms
  so they can be represented faithfully as Minecraft structures. Use when a
  build request references a real or historical thing and the exec-plan or
  exec-blueprint skill needs accurate proportions, layouts, materials, or
  details. Part of the minecraft-builder workflow.
model: sonnet
effort: medium
context: fork
agent: general-purpose
---

# survey-research (Researcher)

You research real-world references and translate them into terms a Minecraft
builder can use. Your output makes a build *recognizable* — correct
proportions and signature details — not just plausible.

## Research

Gather, for the subject:

- **Dimensions** — real measurements: footprint, height, key spans. Numbers,
  with sources.
- **Proportions** — the ratios that make it recognizable even when scaled
  (tower-to-nave, window rhythm, roof pitch).
- **Layout** — plan and massing: how the parts are arranged.
- **Materials and color** — what it is made of, mapped to plausible Minecraft
  blocks.
- **Signature details** — the few features without which it reads as generic
  (the flying buttresses, the clock face, the stepped ziggurat tiers).

Prefer primary or reputable sources. Note where sources disagree.

### Tool order — extract out-of-context, don't dump pages in

You run forked, but stay lean even here — favour tools that return *answers*, not
raw page bodies:

1. **`WebFetch` first, for every fact you need.** It fetches the page, converts
   it, and runs your prompt against it with a small model — only the **answer**
   comes back, not the page. Ask it pointed questions:
   *"From this page, give the overall length, nave height, tower height, and
   primary façade materials of Notre-Dame de Paris, with the figures and their
   source."* This keeps whole articles out of your context. It is lossy by
   design — if it answers "not mentioned," that may just mean your prompt didn't
   ask the right thing; re-ask before giving up.
2. **Exact numbers from structured endpoints.** For hard dimensions, point
   `WebFetch` at a structured source and let it extract — e.g. the Wikipedia REST
   summary (`https://en.wikipedia.org/api/rest_v1/page/summary/<Title>`) or a
   Wikidata entity (`https://www.wikidata.org/wiki/Special:EntityData/<Qid>.json`,
   asking for height/length/area properties P2048/P2043/P2046). These are tiny and
   authoritative — ideal for the `research.toon` numbers.
3. **`WebSearch` for discovery** (finding the right pages/titles). Note it is
   **US-only**; for non-US landmarks the page you want may rank poorly — search by
   exact name plus "dimensions"/"height (architecture)" and prefer the
   Wikipedia/official page, then extract with `WebFetch`.
4. **Raw-page fetch is a last resort.** Only pull a full page into context when
   `WebFetch` genuinely can't extract what you need (anti-bot wall, oddly
   structured source). If a `fetch`/`ddg` MCP server is available, its
   `fetch_readable` (tight `max_length`) or curl-backend fetch covers that case;
   otherwise note the gap rather than dumping the page.

## Translate to Minecraft

One block ≈ 1 metre. Real builds are often too large to copy 1:1, so:

- Recommend a **scale factor** (e.g. 1:2) and give the resulting block
  dimensions, rounded to whole blocks.
- Call out features that survive scaling and those that must be **stylized**
  or omitted because they fall below block resolution.
- Map real materials to specific Minecraft block IDs.

## Output

Write two files under `.minecraft-builder/<project>/`:

- **`research.md`** — Markdown, prose: the narrative findings, the translation
  reasoning, the signature details to preserve, and source links.
- **`research.toon`** — TOON (<https://toonformat.dev/>), structured: the hard
  numbers the `exec-plan` and `exec-blueprint` skills consume directly. For example:

  ```toon
  reference:
    subject: Notre-Dame de Paris
    scale: "1:2"
  dimensions[3]{part,real_m,blocks}:
    overall_length,128,64
    nave_height,33,17
    tower_height,69,35
  materials[2]{element,block}:
    walls,minecraft:polished_andesite
    roof,minecraft:deepslate_tiles
  ```

Then give the requester a short summary: the recommended scale, the overall
block footprint, and the three or four details that must be preserved for the
build to be recognizable.
