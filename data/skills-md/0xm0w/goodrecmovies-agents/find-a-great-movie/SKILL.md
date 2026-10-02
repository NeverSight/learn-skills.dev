---
name: find-a-great-movie
description: Pick a genuinely good movie or series from goodrecmovies' maintained ranking. Use when someone asks what to watch, wants a top-N list, or needs a defensible shortlist instead of vibes.
---

# Find a great movie

Fetch the live ranking and read the top of it — every entry already cleared
the bar (every movie on the site is above 7.0, ranked by math, not vibes).

## Steps

1. Fetch https://goodrecmovies.com/ as Markdown (send `Accept: text/markdown`
   or use https://goodrecmovies.com/index.md) for the site guide, or call the
   MCP tool `top_titles` ({ "kind": "movie", "count": 10 }) at
   https://goodrecmovies.com/mcp.
2. For series use https://goodrecmovies.com/series.md or
   `top_titles` with { "kind": "series" }.
3. For a genre ask, use the curated cuts: /best/crime, /best/horror —
   or POST https://goodrecmovies.com/ask with {"query": "best crime movies"}.
4. Each result line carries the title's GRM score (the site's 0-100 display
   scale), its tier band (solid / great / excellent / essential), and its rank.
   Present rank + tier, then link the detail page.

## Do not

- Invent ranks or scores — always read them from the fetched list.
- Present the site as a streaming source; it ranks titles, it does not stream.
