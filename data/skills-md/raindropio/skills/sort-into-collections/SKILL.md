---
name: sort-into-collections
description: "File Raindrop.io bookmarks into collections: sort Unsorted, move bookmarks on a topic into a collection, or create and suggest new collections. Use when the user asks to organize, sort, file, or move bookmarks, or to add collections."
---

# Sort into collections

Help the user file bookmarks into collections.

## Rules

- A bookmark lives in exactly one collection. Collections nest via `parent_id` (top level: `null`). A title alone is ambiguous: build the full path to understand what a collection means. System collections: `-1` Unsorted, `-99` Trash.
- Search results are candidates. Always fetch the maximum, then filter; silently skip irrelevant items.
- Use the largest batch each tool allows and split bigger sets into sequential calls. Deduplicate ids collected across pages.
- Report only what tool responses confirm. Never claim success after an error.

## Organize bookmarks

Use existing collections only. If nothing fits, ask and offer to create one.

Which bookmarks:

- Collection names given → search all bookmarks NOT in those collections, pick the best matches for each.
- Topic or query given → search bookmarks by meaning, then find fitting existing collections.
- "Unsorted" → fetch from collection `-1`, match to existing collections.
- Nothing specified → sample from Unsorted.

Which collections:

- User provided → validate against existing ones.
- Not provided → fetch existing collections and match them to each bookmark's content.

Move bookmarks with `update_bookmarks`.

## Create collections

Before: check whether a similar collection already exists by meaning, not exact name. If the user asked for the new one, warn about the overlap; if it was your idea, use the existing one. Follow the user's hierarchy style for placement; default to top level when nothing fits.

After: offer to organize bookmarks into the new collection.

When asked to suggest collections without specifics:

- Study the existing structure first: flat or nested, broad or granular, which themes are already covered, including nested ones.
- Propose genuine gaps only. Fewer than requested, or none, is fine.
- No micro-categories, no overlaps, no broad buckets where the user prefers granular ones. If there are no gaps, say so.