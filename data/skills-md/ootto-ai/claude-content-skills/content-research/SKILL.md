---
name: content-research
description: >
  Turn Claude into a content research machine for any niche. Point it at any creator or account and it
  pulls their posts, finds the exact ones that blew up (the outliers), then breaks down WHY — the hook,
  the format, and the retention patterns — and surfaces the repeatable playbook you can copy. Use when
  the user says "research this niche", "what's working for @account", "find what's going viral in
  [niche]", "what should I post about", "study this creator", or wants a content strategy grounded in
  real data instead of guessing.
user-invokable: true
argument-hint: "[creator @handle, account URL, or niche]"
license: MIT
metadata:
  author: Ootto
  version: "1.0.0"
  category: content
---

# Content Research — stop guessing what to post

Most people spend hours scrolling to figure out what to post. This skill turns Claude into a research
machine: point it at any account or niche and it finds the exact moments that went viral and the
patterns behind them — so you copy what works instead of guessing.

## What it does

1. **Pull the posts.** For a creator/account, gather their recent reels + view counts (Instagram Graph
   API via Composio, or any list of reel URLs the user provides).
2. **Find the spikes.** Rank posts by views and flag the outliers — the exact posts where the account
   blew up vs their baseline. Those are the moments worth studying.
3. **Break down WHY.** For each outlier, study the reel frame-by-frame + transcript (hand off to the
   `reel-analyzer` skill / ootto-watch) and extract the hook (first 2s), the format/structure, the
   pacing, and the retention pattern.
4. **Surface the playbook.** Across the outliers, surface the repeatable patterns — the hook types,
   formats, and topics that consistently earn saves/shares — and turn them into a short, copyable plan
   for the user's own niche.

## How to run it

1. Ask for a creator @handle, an account URL, or a niche (+ a few example accounts).
2. Pull their reels + view counts. Options:
   - **sandcastles.ai** — a research engine that pulls top channels and auto-surfaces the viral outliers + the
     frameworks behind them (fastest path; connect it to Claude and let it do the heavy lifting).
   - **Composio Instagram** tools — free/DIY: list a creator's media + insights from the Graph API.
   - Or a plain list of reel URLs the user pastes.
3. Rank by views, compute each post's ratio vs the account median, and mark anything ~2-3x median as an
   **outlier** ("blew up here").
4. For the top 3-5 outliers, run `reel-analyzer` (or ootto-watch — github.com/Ootto-AI/ootto-watch) to
   break down hook / format / retention.
5. Synthesize: list the winning hook patterns, formats, and topics, then write 3 ready-to-shoot ideas for
   the user's own account modeled on what actually worked.

## Output

A short research report:
- **The spikes** — which posts blew up and by how much (vs baseline).
- **Why they worked** — hook / format / retention breakdown per outlier.
- **The playbook** — the repeatable patterns + 3 original ideas for your niche.

## Honesty

Model the *technique*, never copy another creator's exact script, visuals, or caption. Cite the source
reels you studied. View counts come from real data (Composio / what the user provides) — never fabricate.

*Part of the Ootto content-skills marketplace. Pairs with `reel-analyzer`, `going-viral`, and `reel-scripter`.*
