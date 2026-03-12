---
name: humanize-readme
description: Rewrites a README.md to remove AI slop — buzzwords, generic openers, fake enthusiasm, and formulaic structure — replacing it with direct, honest, human-sounding writing. This skill should be used when the user wants to humanize a README, remove AI-generated writing patterns, make documentation sound less like ChatGPT wrote it, or asks to "fix the README", "humanize readme", "remove AI slop", "make it sound human".
metadata:
  author: b4r7x
  version: "1.0.0"
  argument-hint: <readme-path>
---

# Humanize README

Reads the current `README.md`, audits it for AI slop patterns, then rewrites it in a direct, honest, human voice.

## Workflow

### Step 1 — Read the README

```bash
cat README.md
```

Also check what the project actually is (to rewrite with specifics, not generics):

```bash
cat package.json 2>/dev/null | head -20
cat pyproject.toml 2>/dev/null | head -15
ls src/ 2>/dev/null | head -10
```

### Step 2 — Audit for slop

Read `references/slop-patterns.md` for the full list. Flag these in the README:

**High-signal slop patterns:**
- Banned buzzwords: `seamlessly`, `robust`, `scalable`, `leverage`, `cutting-edge`, `comprehensive`, `empower`, `intuitive`, `powerful`, `game-changer`
- 2026-era hedging/filler: `"it's worth noting"`, `"let's explore"`, `"this is designed to"`, `"makes it easy to"`, `"enables developers to"`, `"ensures"`, `"has been designed"`
- Generic openers starting with "In today's...", "This powerful tool...", "This repository aims to..."
- Feature lists with empty adjectives: "Blazing fast", "Enterprise-grade", "Intuitive API"
- Suspiciously polished completeness with no honest gaps
- Conclusions that philosophize about the project
- **Uniform sentence length** — every sentence the same rhythm (burstiness check)
- **No personal voice** — no "why it exists", no honest limitations, no tradeoffs mentioned

### Step 3 — Rewrite

Rewrite the README applying these rules:

**Voice:**
- Write like you'd explain the project over coffee — direct, specific, a bit casual
- Use the actual tech names (not "modern technologies" or "industry-standard tools")
- Keep code blocks, commands, and links exactly as they are
- Preserve the structure (sections) but rewrite the prose

**For each section:**
- **Project description / intro** — one or two sentences: what it does, why it exists. No superlatives.
- **Features** — remove adjectives, add specifics. Not "Fast" → state the actual number if known, otherwise just name the feature plainly
- **Installation / Usage** — keep as-is if already good; strip any "Welcome to the getting started..." filler
- **Why this project** — if it exists and sounds generic, rewrite with a real reason or remove it
- **Contributing / Closing** — strip "star this repo", philosophy, or over-long contributing guides

**Tone rules:**
- Honest about gaps: "Not tested on Windows", "Still experimental", "Works on my machine"
- Varied sentence lengths — short and long, not all the same
- No emoji unless they were already there (and even then, fewer)
- No exclamation marks unless genuinely warranted

**Do NOT:**
- Add content that wasn't there — only rewrite existing content
- Change technical accuracy — keep the same claims, just strip the fluff
- Make it curt to the point of being unhelpful — clarity > brevity
- Touch badge rows (`[![...](...)](#)` lines) — CI badges, version badges, license badges stay exactly as-is

### Step 4 — Output

Output the full rewritten README in a single fenced markdown code block so it can be copied directly.

Before the block, briefly note what you changed (2-3 bullet points max).

**For full banned phrase list and before/after examples:** `references/slop-patterns.md`
