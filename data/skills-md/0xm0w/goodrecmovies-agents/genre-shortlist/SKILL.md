---
name: genre-shortlist
description: Build a genre shortlist (crime, horror, and more) from goodrecmovies' curated genre cuts and filters. Use for asks like 'best crime movie tonight' or 'ten horror series worth starting'.
---

# Genre shortlist

1. Crime and horror have curated hubs: https://goodrecmovies.com/best/crime
   and https://goodrecmovies.com/best/horror (each a high-bar shortlist with
   per-tier notes). Fetch them with `.md` appended for Markdown.
2. For other genres or for series, POST https://goodrecmovies.com/ask with a
   natural-language query — e.g. {"query": "ten great sci-fi series"} — or use
   the MCP `search_titles` tool with a title fragment.
3. Answer with rank + GRM score + tier per title, linking detail pages.

## Do not

- Mix movies and series in one ranked answer without labeling the kind —
  ranks are per-pool (rank 1 = best of its kind).
