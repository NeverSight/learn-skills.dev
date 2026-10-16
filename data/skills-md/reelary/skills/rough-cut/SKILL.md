---
name: rough-cut
description: 'Turn a script, outline, shot list, blog post or theme into a video cut from the user''s own real footage (not AI-generated): rough cut, assembly edit, string-out, script to video, montage, highlight reel, recap, sizzle reel. Picks the best clip per line with alternatives, saves an editable project and exports MP4. Local with Reelary on Mac or Windows. Trigger on "rough cut", "assembly edit", "first cut", "script to video", "turn this script into a video", "make a video from my blog post", "text to video with my footage", "montage", "highlight reel", "recap video", "best moments", "year in review video", "trip video from my clips", "wedding highlights", "edit my footage into a video". Not for AI video generation, color grading or effects.'
---

# Rough cut

If the `reelary_*` tools are missing or nothing is indexed, use the [reelary](../reelary/SKILL.md) skill first.

## Steps

1. Get a script or shot list: one line per shot. Ask for the aspect ratio if unclear (16:9 default, 9:16 for social, 1:1).
2. Call `reelary_rough_cut` with `script` and `aspect`. Keep `max_clip_seconds` at the default 6 unless the input below says otherwise.
3. Review the draft: list each scene with its chosen clip; mention `empty_scenes` and suggest rephrasing those lines. If a pick looks wrong, set that scene's `chosen` to 1 or 2 (the alternatives).
4. Call `reelary_save_project` with a short name. The user can fine-tune it: `reelary_open_in_app` with the project id.
5. Export when asked: `reelary_export_video` with `project_id`, then poll `reelary_job_status` until `done` and give the output path. If `export_note` warned about free limits, say so before exporting.

Without MCP: `npx -y reelary cut "<script>" --aspect 16:9 --save "<name>"` then `npx -y reelary export <project_id>`.

## Script, blog post or notes to video

If the user gave prose, rewrite it into 4-12 short visual lines, one shot each, and show them for a quick OK before step 2. Report the file path and total length; offer a 9:16 version with [vertical-video](../vertical-video/SKILL.md).

## Montage, highlight reel, recap

Agree on the theme, length (30-60s works well; free exports cap at 60s) and aspect ratio. Write 6-12 short visual beats in order: wide establishing shot, details, people, peak moment, closing shot. Use `max_clip_seconds` around 3-4 for a punchy pace, and offer `reelary_open_in_app` to add music before exporting.

## Notes

- Free exports: 720p, watermark, 60 seconds max, 5 per month. Pro removes the limits.
- For frame-accurate finishing, grading or effects, hand off with [nle-export](../nle-export/SKILL.md).
