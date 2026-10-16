---
name: reelary
description: 'Reelary, the 100% local AI media library for your own videos and photos on Mac and Windows: install and connect it, index folders and external drives, check indexing progress, remove folders, fix errors. Use when the reelary_* tools are missing or fail, or the user wants to organize footage. Trigger on "Reelary", "media library", "index my videos", "organize my footage", "catalog my clips", "scan my drive", "make my footage searchable", "video library app", "digital asset management for video", "local video search app". Not for cloud storage or renaming files.'
---

# Reelary

Reelary indexes the user's own footage on their computer and lets agents search it by meaning, then cut the matches into a video. Everything runs locally; nothing is uploaded.

## Setup

1. Call `reelary_status`. If the tool does not exist, follow [install](references/install.md); never install without asking.
2. If no folders are indexed, ask where the footage lives and index it (below).

## Media library

1. `reelary_list_folders` to see what is indexed.
2. To add one: confirm the absolute path with the user, call `reelary_add_folder`, then poll `reelary_job_status` every few seconds and report progress (`detail` is the current file). Big libraries take a while; indexing continues in the background.
3. To remove one: `reelary_remove_folder` (only the index is removed; files stay).
4. When done, suggest a first search with the find-footage skill.

Without MCP: `npx -y reelary index <folder>` and `npx -y reelary status`.

- New and changed files inside indexed folders are picked up automatically while Reelary runs.
- External drives must be connected to search their footage.

## Other tasks

| The user wants | Skill |
|---|---|
| a shot, photo, quote, person or place | [find-footage](../find-footage/SKILL.md) |
| cutaways under a voiceover | [broll-finder](../broll-finder/SKILL.md) |
| a rough cut, script-to-video, montage or highlight reel | [rough-cut](../rough-cut/SKILL.md) |
| Shorts / Reels / TikTok | [vertical-video](../vertical-video/SKILL.md) |
| a Premiere / Final Cut / Resolve timeline | [nle-export](../nle-export/SKILL.md) |

Tool list: [tools](references/tools.md). Errors and limits: [troubleshooting](references/troubleshooting.md).

## Plans

Free: unlimited indexing, visual search and rough cuts; MP4 exports are 720p with a watermark, up to 60 seconds, 5 per month. Pro adds dialogue search, people, places, NLE export and full-quality exports. On `pro_required`, explain plainly and share the `upgrade_url` once; do not work around the limit.
