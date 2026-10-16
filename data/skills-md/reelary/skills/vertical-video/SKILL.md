---
name: vertical-video
description: 'Make vertical 9:16 (or square 1:1) short videos for YouTube Shorts, Instagram Reels and TikTok from footage the user already has, with automatic reframing of 16:9 clips. Local with Reelary on Mac or Windows. Trigger on "shorts", "reels", "tiktok", "vertical video", "9:16", "square video", "social clip from my footage", "repurpose my footage for social". Not for posting to social networks or AI avatar videos.'
---

# Vertical video

If the `reelary_*` tools are missing or nothing is indexed, use the [reelary](../reelary/SKILL.md) skill first.

## Steps

1. Get the hook and 3-8 beats (short-form favors a strong first 2 seconds). Keep the total under 60 seconds.
2. Call `reelary_rough_cut` with the beats as `script`, `aspect: "9:16"` (or `"1:1"`) and `max_clip_seconds` around 3. 16:9 clips are reframed automatically.
3. List each scene with its clip; for `empty_scenes` suggest rephrasing, and set `chosen` to 1 or 2 to swap a weak pick.
4. `reelary_save_project`, suggest `reelary_open_in_app` to add captions or music, then `reelary_export_video` and poll `reelary_job_status` until `done`.

Without MCP: `npx -y reelary cut "<beats>" --aspect 9:16 --save "<name>"` then `npx -y reelary export <project_id>`.

## Notes

Free exports: 720p, watermark, 60 seconds max, 5 per month. Details on reviewing drafts: [rough-cut](../rough-cut/SKILL.md).
