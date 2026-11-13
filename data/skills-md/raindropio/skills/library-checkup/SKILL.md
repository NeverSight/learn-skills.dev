---
name: library-checkup
description: "Find and fix problems in a Raindrop.io library: duplicate or inconsistent tags, bookmarks in the wrong collection or with the wrong tags, duplicate bookmarks, broken links, and emptying the Trash. Use when the user asks to clean up, tidy, or check their library, tags, or collections."
---

# Library checkup

Find problems in the user's library and fix what they approve. Run only the check the user asked for; if the request is general, ask which checks to run. Show only actionable findings; when a check is clean, say so in one line.

## Rules

- Collections nest via `parent_id` (top level: `null`). A title alone is ambiguous: build the full path. System collections: `-1` Unsorted, `-99` Trash.
- Pass tags without `#`.
- Check results are candidates, noisy with false positives. Verify each one and silently skip false positives.
- Use the largest batch each tool allows and split bigger sets into sequential calls. Deduplicate ids collected across pages.
- Report only what tool responses confirm. Never claim success after an error.

## Clean up tags

Find duplicates (case, spacing, `-` vs `_`, typos, plurals) and group the variants. Pick a canonical form and merge the others into it. Identify the dominant style (e.g. lowercase, kebab-case) and rename outliers, even single tags that break the pattern. If the renamed form already exists, merge instead. Apply with `update_tags`.

## Bookmarks in wrong collections

Call `find_misplaced_bookmarks` with as many collections as it allows: those the user named, otherwise picked purely at random. Candidates come from semantic similarity. Show only genuinely misplaced bookmarks; if all look fine, say nothing is wrong.

## Bookmarks with wrong tags

Call `find_mistagged_bookmarks` with as many tags as it allows: those the user named, otherwise picked purely at random. Candidates come from semantic distance to the tag. Show only genuinely wrong tags; if all look fine, say the tags are accurate.

## Duplicates and broken links

Use `find_bookmarks` with `is_duplicate` or `has_broken_link`. List what was found and let the user decide what to remove. `delete_bookmarks` moves bookmarks to Trash; deleting one that is already in Trash removes it permanently.

## Empty Trash

Only when the user explicitly asks. Call `delete_collections` with id `-99`: this single call removes all trashed bookmarks. Skip other steps.