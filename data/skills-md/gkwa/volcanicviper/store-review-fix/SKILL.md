---
name: store-review-fix
description: Fix the next vault note that carries the storereview tag. Reads the note's store review section for context, applies the outline-headings skill, reports every change, then removes the store review section and the storereview tag, commits, opens the note in a new Obsidian tab, and reports how many storereview notes remain. Use when asked to fix another store review note, work through the storereview queue, or find the next note with the store review tag.
---

## Store Review Fix

A note tagged `storereview` has a "store review" section that records headings moved above its Stores section.

The queue is every note carrying that tag.

Each run clears one note from the queue, including removing its section and tag.

## Steps

1. Find the notes that carry the `storereview` tag, using the islandiguana skill or the vault MCP tag search, and pick one that has not been fixed yet.
2. Read the note and read its "store review" section first, because it names the headings that were moved and so gives the context for the fix.
3. Make the edits that context calls for, applying the outline-headings skill for every rule about headings, links and nesting.
4. Update any heading quoted inside the "store review" section so it matches the renamed heading, before the section is removed.
5. Commit the fix with `git commit -- <path>`.
6. Tell the user each change made, as a short list, so the user can judge whether the changes are accurate.
7. Remove the "store review" section and remove `storereview` from the `tags` list in the front matter.
8. Commit the removal on its own with `git commit -- <path>`, so it can be reverted separately from the fix.
9. Open the note in a new Obsidian tab with obsidian-cli.
10. Search the tag again and tell the user how many notes still carry `storereview`.

## Removing the section

- The section is the `## store review` heading and everything under it up to the next heading.
- Leave no run of more than one blank line behind.
- Remove only the `storereview` entry from `tags`, and keep every other tag.
- If the user objects to a change in the report, restore the previous state from git and adjust it, since the fix and the removal are separate commits.

## Gotchas

- Git tracks the filename with its original casing, which may differ from the file on disk, so run `git ls-files "[Xx]..."` with the first letter bracketed before committing.
- A background loop may commit the vault every few minutes with the message `stuff`, so a commit that reports no changes means the loop already captured the edit.
- Confirm that with `git log --oneline -3 -- <path>` and report it rather than retrying.
- Do not edit the loop.
- `status.showUntrackedFiles=no` is global, so a new file never shows in `git status`.

## Counting the queue

- Count notes that carry the tag in their front matter, not notes that merely mention the words.
- Report one number for the tag, since "review" and "store review" are the same `storereview` tag.
- The note just fixed no longer counts, because its tag is gone.

## Note conventions that still apply

Follow the vault conventions in /Users/mtm/Documents/Obsidian Vault/CLAUDE.md.

Never use italics, bold, or emphasis in a note.

Each sentence is its own paragraph.

Do not reformat anything else in the note.
