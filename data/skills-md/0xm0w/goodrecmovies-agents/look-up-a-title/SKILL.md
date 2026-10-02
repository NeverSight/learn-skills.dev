---
name: look-up-a-title
description: Look up where a specific movie or series lands in the goodrecmovies ranking by its IMDb id. Use when checking how good a specific title really is or where it ranks.
---

# Look up a title

Detail URLs are the IMDb id under /movie/ or /series/ and never change.

## Steps

1. Fetch the detail page as Markdown: append `.md` — e.g.
   https://goodrecmovies.com/movie/tt0111161.md — or call the MCP tool
   `get_title` ({ "tconst": "tt0111161" }) at https://goodrecmovies.com/mcp.
2. The answer carries the GRM score, the tier band, the rank within its kind,
   the vote count, and the detail-page URL.

## Do not

- Guess ids: an unknown id returns 404 — tell the user the title is not in
  the corpus rather than inventing a score.
