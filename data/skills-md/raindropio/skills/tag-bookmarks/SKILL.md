---
name: tag-bookmarks
description: "Add tags to Raindrop.io bookmarks: tag untagged or specific bookmarks, tag by topic, or suggest tags for a collection. Use when the user asks to tag bookmarks or to choose tags for them. Not for renaming or merging tags."
---

# Tag bookmarks

Help the user tag bookmarks.

## Rules

- Max 5 tags per bookmark. Pass tags without `#`.
- Existing tags first. Invent a tag only if the user asks or nothing fits, and ask first.
- Use `lacks_tags` to skip bookmarks that already have a given tag.
- Search results are candidates. Always fetch the maximum, then filter; silently skip irrelevant items.
- Use the largest batch each tool allows and split bigger sets into sequential calls. Deduplicate ids collected across pages.
- Report only what tool responses confirm. Never claim success after an error.

## Which bookmarks

- Explicit reference → use those.
- Topic or query → search bookmarks by meaning.
- Only tags given, no topic → for each tag, search by meaning and pick the best matches.
- Nothing specified → take up to 10 existing tags with the fewest bookmarks and search matching bookmarks for each. Skip tags with no candidates; if results are thin, try the next batch of tags.

## Which tags

- User provided → validate against existing tags, normalize variants.
- Not provided → fetch existing tags and match them to each bookmark's content. For a collection, analyze its themes and match them against existing tags.
- Nothing fits → ask before inventing.

## Inventing tags

- For specific bookmarks → base them on content, avoid near-duplicates of existing tags.
- For the whole library → find gaps in themes and propose new tags; once approved, treat them as user provided.

Add tags with `update_bookmarks`.