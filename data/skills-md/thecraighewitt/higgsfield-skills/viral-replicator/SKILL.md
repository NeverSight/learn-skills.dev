---
name: viral-replicator
description: Use when the user wants to either (a) deconstruct a viral Instagram/TikTok/YouTube Short and rebuild it for their brand, or (b) scrape product reviews from G2/Trustpilot and turn them into a testimonial-style video ad. Both paths produce a paste-ready Higgsfield video prompt. Triggers on phrases like "deconstruct this viral video", "rebuild this for my brand", "scrape these reviews into an ad", or "turn G2 reviews into a testimonial video".
---

# Viral Replicator + Review-to-Ad

Two paths, same destination: a Higgsfield-ready video prompt.

- **Path A — Viral replication.** Paste a viral video URL → deconstruct the structure → rebuild it for the user's brand.
- **Path B — Review-to-ad.** Point at a G2 product reviews URL → cluster reviews into testimonial themes → generate ad scripts.

## When to use

User prompts that should trigger this skill:
- "Deconstruct this Instagram video and rebuild it for my brand: <URL>"
- "What made this viral video work? Now make me a version of it."
- "Scrape Castos's G2 reviews and turn them into a testimonial ad."
- "Pull these reviews and write me 3 ad scripts."

## Routing

Route on the first user input:

| User input contains | Path |
|---|---|
| `instagram.com/p/`, `instagram.com/reel/`, `tiktok.com`, `youtube.com/shorts` | **Path A** |
| `g2.com/products/`, `trustpilot.com/review`, OR pasted review text | **Path B** |
| Both | Run Path A first, then ask whether to also run Path B |

---

## Path A — Viral replication

### Step 1 — Fetch the post

```bash
node skills/viral-replicator/scripts/fetch-ig-post.mjs <URL> --out output/viral-replicator/<slug>-<YYYY-MM-DD>/raw-post.json
```

The script captures: caption, hashtags, on-screen text, video poster, duration, engagement counts. If Instagram blocks the headless browser (common — they aggressively rate-limit), fall back to `examples/kallaway-fixture.md` and tell the user the demo is using a fixture.

The same script handles TikTok and YouTube Shorts URLs at best-effort; for YouTube Shorts especially, ask the user to paste the transcript if scraping fails.

### Step 2 — Deconstruct

Load `prompts/deconstruct-viral.md` and produce a structured breakdown: hook (0–3s), pattern interrupts, narrative arc, visual style, audio role, payoff, CTA shape, why-it-worked hypothesis.

Write to `output/viral-replicator/<slug>-<YYYY-MM-DD>/deconstruction.md`.

### Step 3 — Rebuild for the user's brand

Ask once: "What's the brand and topic this rebuild is for? One sentence." (Skip if the user already told you.)

Load `prompts/rebuild-viral.md` and produce a shot-by-shot script + a paste-ready Higgsfield video prompt using `templates/higgsfield-rebuild-prompt.md`.

Write to `output/viral-replicator/<slug>-<YYYY-MM-DD>/rebuild.md` and `higgsfield.md`.

### Step 4 — Render (optional)

If the Higgsfield MCP is connected, call `ToolSearch` with query `higgsfield` to find the current video-generation tool, then call it with the prompt from `templates/higgsfield-rebuild-prompt.md`. If not, the prompt sits paste-ready.

---

## Path B — Review-to-ad

### Step 1 — Scrape reviews

```bash
node skills/viral-replicator/scripts/scrape-g2-reviews.mjs <URL> --top 25 --out output/viral-replicator/<brand>-reviews-<YYYY-MM-DD>/raw-reviews.json
```

The script captures per review: reviewer name (or "Verified User"), role, company size, star rating, "what do you like best", "what do you dislike", quote excerpt. G2 has anti-bot protections — if the scrape is blocked, fall back to `examples/castos-g2-fixture.md` and tell the user.

For Trustpilot URLs, the script auto-switches selectors. For arbitrary review text the user pastes, skip Step 1 and feed the text directly into Step 2.

### Step 2 — Cluster into testimonial themes

Load `prompts/review-to-ad.md`. Produce 2–3 testimonial themes. Each theme:
- Theme name (the customer truth, NOT a feature name)
- 1 representative pull-quote per theme (verbatim, with reviewer attribution)
- Why this theme converts

Write to `output/viral-replicator/<brand>-reviews-<YYYY-MM-DD>/themes.md`.

### Step 3 — Ad-ify

For each theme, write a 30-second testimonial-style spot:
- Hook (0–3s) — uses the pull-quote or a paraphrase
- Setup (3–10s)
- Demonstration (10–22s)
- Payoff + CTA (22–30s)

Choose the visual treatment per theme:
- **Talking-head reconstruction** — for emotional / "this saved my business" testimonials
- **Text-on-b-roll with VO** — for technical / specific-feature testimonials
- **Side-by-side before/after** — for migration / switching testimonials

Use `templates/testimonial-ad-prompt.md` to write the Higgsfield video prompt for each spot.

Write to `output/viral-replicator/<brand>-reviews-<YYYY-MM-DD>/scripts.md` and `higgsfield.md`.

### Step 4 — Render (optional)

Same MCP discovery pattern as Path A.

---

## Output structure

```
output/viral-replicator/
├── <viral-post-slug>-<YYYY-MM-DD>/
│   ├── raw-post.json
│   ├── deconstruction.md
│   ├── rebuild.md
│   └── higgsfield.md
└── <brand>-reviews-<YYYY-MM-DD>/
    ├── raw-reviews.json
    ├── themes.md
    ├── scripts.md
    └── higgsfield.md
```

## Voice & tone

- For rebuilds: match the structure of the original, NOT the voice. The voice should sound like the user's brand.
- For testimonial ads: keep customer quotes verbatim where possible. Resist polishing — real language reads as real.
- No "transformative." No "game-changing." No "I never thought I could…" unless the customer literally said it.

## Demo commands

```
Deconstruct https://www.instagram.com/p/DAi1lWIPFuB/ and rebuild it for an insulated cup brand.
```

```
Scrape https://www.g2.com/products/castos/reviews and turn them into 3 testimonial ad scripts.
```
