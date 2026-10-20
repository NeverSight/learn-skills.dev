---
name: ingest-new-instagram-recipes
description: Ingest the new Instagram recipe posts that starlitseal saved to urls.db into the vault, skipping any shortcode that already has a note, via a multi-agent grouchygiraffe-ingest workflow. Use when asked to process, ingest, or check the new insta recipes in urls.db, or to catch up on Instagram recipes added today or since a given time.
---

Invoking this skill authorizes the Workflow tool call in step 4.

The two helpers sit next to this file, at /Users/mtm/.claude/skills/ingest-new-instagram-recipes once deployed.

## 1. Find the candidates

```
uv run --no-active --script /Users/mtm/.claude/skills/ingest-new-instagram-recipes/new_shortcodes.py --verbose
```

It reads /Users/mtm/pdev/taylormonacelli/starlitseal/server/urls.db, reduces every Instagram URL to its shortcode, and drops any shortcode that `rg` finds in a vault note.

Each output line is `received_at`, shortcode, archived flag, and URL.

The window defaults to local midnight today, because `received_at` is UTC and a naive date filter misses the evening.

Pass `--since <ISO-8601 UTC>` when the user names a different window, such as "since yesterday".

The shortcode is the dedup key, because every note the workflow writes carries the Instagram URL.

A candidate that is archived but still has no note is usually a non-recipe from an earlier run, and the identify stage skips it again cheaply.

Step 1 is done when you hold the list of shortcodes; if it is empty, report that and stop.

## 2. Archive the unarchived ones

Every candidate whose archived flag is False needs a grouchygiraffe run first, so the workflow can upload the local `_thumb.jpg` rather than refetching from Instagram.

Check the lock is free with `pgrep -fl bin/grouchygiraffe`, write the URLs one per line to a manifest in `$CLAUDE_JOB_DIR/tmp` (or `$TMPDIR`), then run in the background:

```
uv run --no-active --project /Users/mtm/pdev/taylormonacelli/grouchygiraffe --directory /Users/mtm/pdev/taylormonacelli/grouchygiraffe grouchygiraffe --output-dir /Users/mtm/pdev/taylormonacelli/grouchygiraffe/data --manifest <manifest> --sleep 10s-40s --verbose
```

Step 2 is done when `<shortcode>.yaml` exists in /Users/mtm/pdev/taylormonacelli/grouchygiraffe/data for every candidate; carry any that failed to archive into the report instead of the workflow.

## 3. Pick the scope

Only the candidates in the window go forward.

Older archived posts without notes were deliberately left alone by earlier runs, so mention their count only if the user widened the window.

## 4. Run the workflow

Call Workflow with `scriptPath` set to /Users/mtm/.claude/skills/ingest-new-instagram-recipes/workflow.js and `args` set to the array of shortcodes.

Per shortcode it runs three stages as a pipeline.

- Identify runs grouchygiraffe-recipe-lookup, rejects non-recipes, and dedups on dish plus creator so an Instagram post never overwrites a YouTube or blog note of the same recipe.
- Upload pushes the archived `_thumb.jpg` to Imgur through a serial lock, because parallel uploads trip the Imgur throttle, and falls back to the logged-in web upload in Chrome when the API is blocked.
- Write runs recipe-cleanup, sets `pic`, and commits each note by pathspec, because other processes commit to the vault concurrently.

Step 4 is done when the workflow returns one result per shortcode.

## 5. Verify

Rerun the step 1 command; every shortcode reported written must be gone from its output.

Run `git log --oneline --no-walk --stat <hashes>` over the reported commits to confirm each note landed.

## 6. Report

Give a table with the note name, shortcode, and commit for each written note, leading with the note name.

List skipped shortcodes with their reason, and anything the workers flagged, such as paywalled quantities or a new creator hub note.
